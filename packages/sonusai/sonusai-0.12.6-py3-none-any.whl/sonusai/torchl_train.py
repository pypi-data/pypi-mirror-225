"""sonusai torchl_train

usage: torchl_train [-hgv] (-m MODEL) (-l VLOC) [-w CKPT] [-e EPOCHS] [-b BATCH] [-t TSTEPS] [-p ESP] TLOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -m MODEL, --model MODEL         Python .py file with MyHyperModel custom PyLightning class definition.
    -l VLOC, --vloc VLOC            Location of SonusAI mixture database to use for validation.
    -w CKPT, --weights CKPT         Optional Pytorch Lightning checkpoint file for initializing model weights.
    -e EPOCHS, --epochs EPOCHS      Number of epochs to use in training. [default: 8].
    -b BATCH, --batch BATCH         Batch size.
    -t TSTEPS, --tsteps TSTEPS      Timesteps.
    -p ESP, --patience ESP          Early stopping patience. [default: 12]
    -g, --loss-batch-log            Enable per-batch loss log. [default: False]

Train a Pytorch lightning model defined in MODEL .py using Sonusai mixture data in TLOC.

Inputs:
    TLOC    A SonusAI mixture database directory to use for training data.
    VLOC    A SonusAI mixture database directory to use for validation data.

Results are written into subdirectory <MODEL>-<TIMESTAMP>.
Per-batch loss history, if enabled, is written to <basename>-history-lossb.npy

"""
from sonusai import logger


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    model_name = args['--model']
    weights_name = args['--weights']
    v_name = args['--vloc']
    epochs = int(args['--epochs'])
    batch_size = args['--batch']
    timesteps = args['--tsteps']
    esp = int(args['--patience'])
    loss_batch_log = args['--loss-batch-log']
    t_name = args['TLOC']

    import warnings
    from os import makedirs
    from os.path import basename
    from os.path import join
    from os.path import splitext

    # import keras_tuner as kt
    import numpy as np

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # from keras import backend as kb
        # from keras.callbacks import EarlyStopping

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.data_generator import TorchFromMixtureDatabase
    # from sonusai.data_generator import KerasFromH5
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import create_ts_name
    from sonusai.utils import import_keras_model
    from sonusai.utils import get_frames_per_batch
    from lightning.pytorch import Trainer
    from pytorch_lightning.loggers.csv_logs import CSVLogger
    from lightning.pytorch.callbacks import ModelSummary
    from lightning.pytorch.callbacks import ModelCheckpoint
    from lightning.pytorch.callbacks import EarlyStopping
    from lightning.pytorch.loggers import TensorBoardLogger

    model_base = basename(model_name)
    model_root = splitext(model_base)[0]

    if batch_size is not None:
        batch_size = int(batch_size)

    if timesteps is not None:
        timesteps = int(timesteps)

    output_dir = create_ts_name(model_root)
    makedirs(output_dir, exist_ok=True)
    base_name = join(output_dir, model_root)

    # Setup logging file
    create_file_handler(join(output_dir, 'torchl_train.log'))
    update_console_handler(verbose)
    initial_log_messages('torchl_train')
    logger.info('')

    t_mixdb = MixtureDatabase(config=t_name)
    logger.info(f'Training: found {len(t_mixdb.mixtures)} mixtures with {t_mixdb.num_classes} classes from {t_name}')

    v_mixdb = MixtureDatabase(config=v_name)
    logger.info(f'Validation: found {len(v_mixdb.mixtures)} mixtures with {v_mixdb.num_classes} classes from {v_name}')

    # Import model definition file
    logger.info(f'Importing {model_base}')
    model = import_keras_model(model_name)  # note works for pytorch lightning as well as keras

    # Check overrides
    # timesteps = check_keras_overrides(model, t_mixdb.feature, t_mixdb.num_classes, timesteps, batch_size)
    # Calculate batches per epoch, use ceiling as last batch is zero extended
    frames_per_batch = get_frames_per_batch(batch_size, timesteps)
    batches_per_epoch = int(np.ceil(t_mixdb.total_feature_frames('*') / frames_per_batch))

    logger.info('Building and compiling model')
    try:
        hypermodel = model.MyHyperModel(feature=t_mixdb.feature,
                                        # num_classes=t_mixdb.num_classes,
                                        timesteps=timesteps,
                                        batch_size=batch_size)
    except Exception as e:
        logger.exception(f'Error: building {model_base} failed: {e}')
        raise SystemExit(1)

    logger.info('')
    # built_model.summary(print_fn=logger.info)
    # logger.info(summary(model))
    logger.info('')
    logger.info(f'feature       {hypermodel.hparams.feature}')
    logger.info(f'batch_size    {hypermodel.hparams.batch_size}')
    logger.info(f'timesteps     {hypermodel.hparams.timesteps}')
    logger.info(f'num_classes   {hypermodel.num_classes}')
    logger.info(f'flatten       {hypermodel.flatten}')
    logger.info(f'add1ch        {hypermodel.add1ch}')
    logger.info(f'input_shape   {hypermodel.input_shape}')
    logger.info(f'truth_mutex   {hypermodel.truth_mutex}')
    #    logger.info(f'lossf         {hypermodel.lossf}')
    logger.info(f'optimizer     {hypermodel.configure_optimizers()}')
    logger.info('')

    t_mixid = t_mixdb.mixids_to_list()
    v_mixid = v_mixdb.mixids_to_list()

    # Use SonusAI DataGenerator to create validation feature/truth on the fly
    sampler = None  # TBD how to stratify, also see stratified_shuffle_split_mixid(t_mixdb, vsplit=0)
    t_datagen = TorchFromMixtureDatabase(mixdb=t_mixdb,
                                         mixids=t_mixid,
                                         batch_size=hypermodel.hparams.batch_size,
                                         cut_len=hypermodel.hparams.timesteps,
                                         flatten=hypermodel.flatten,
                                         add1ch=hypermodel.add1ch,
                                         random_cut=True,
                                         sampler=sampler,
                                         drop_last=True,
                                         num_workers=1)

    v_datagen = TorchFromMixtureDatabase(mixdb=v_mixdb,
                                         mixids=v_mixid,
                                         batch_size=1,
                                         cut_len=0,
                                         flatten=hypermodel.flatten,
                                         add1ch=hypermodel.add1ch,
                                         random_cut=False,
                                         sampler=sampler,
                                         drop_last=True,
                                         num_workers=0)

    # TODO: If hypermodel.es exists, then use it; otherwise use default here
    csvl = CSVLogger(output_dir, name="logs", version="")
    tbl = TensorBoardLogger(output_dir, "logs", "", log_graph=True, default_hp_metric=False)
    es_cb = EarlyStopping(monitor="val_loss", min_delta=0.00, patience=esp, verbose=False, mode="min")
    ckpt_cb = ModelCheckpoint(dirpath=output_dir + '/ckpt/', save_top_k=5, monitor="val_loss",
                              mode="min", filename=model_root + "-{epoch:03d}-{val_loss:.3g}")
    callbacks = [ModelSummary(max_depth=2), ckpt_cb, es_cb]

    profiler = None  # 'advanced'
    if profiler == 'advanced':
        from lightning.pytorch.profilers import AdvancedProfiler
        profiler = AdvancedProfiler(dirpath=output_dir, filename="perf_logs")
    else:
        profiler = None

    # # loss_batch_log = True
    # loss_batchlogger = None
    # if loss_batch_log is True:
    #     loss_batchlogger = LossBatchHistory()
    #     callbacks.append(loss_batchlogger)
    #     logger.info(f'Adding per batch loss logging to training')
    #
    if weights_name is not None:
        logger.info(f'Loading weights from {weights_name}')
        hypermodel = hypermodel.load_from_checkpoint(weights_name)
    logger.info(f'  training mixtures    {len(t_mixid)}')
    logger.info(f'  validation mixtures  {len(v_mixid)}')
    logger.info(f'Starting training with early stopping patience = {esp} ...')
    logger.info('')

    trainer = Trainer(max_epochs=epochs,
                      default_root_dir=output_dir,
                      logger=[tbl, csvl],
                      profiler=profiler,
                      # precision='16-mixed',
                      # accelerator="cpu",
                      # devices=4,
                      callbacks=callbacks)
    trainer.fit(hypermodel, t_datagen, v_datagen)

    # history = built_model.fit(t_datagen,
    #                           batch_size=hypermodel.batch_size,
    #                           epochs=epochs,
    #                           validation_data=v_datagen,
    #                           shuffle=False,
    #                           callbacks=callbacks)

    # # Save history into numpy file
    # history_name = base_name + '-history'
    # np.save(history_name, history.history)
    # # Note: Reload with history=np.load(history_name, allow_pickle='TRUE').item()
    # logger.info(f'Saved training history to numpy file {history_name}.npy')
    # if loss_batch_log is True:
    #     his_batch_loss_name = base_name + '-history-lossb.npy'
    #     np.save(his_batch_loss_name, loss_batchlogger.history)
    #     logger.info(f'Saved per-batch loss history to numpy file {his_batch_loss_name}')
    #
    # # Find checkpoint file and load weights for prediction and model save
    # checkpoint_name = None
    # for path, dirs, files in walk(output_dir):
    #     for f in files:
    #         if "ckpt" in f:
    #             checkpoint_name = f
    #
    # if checkpoint_name is not None:
    #     logger.info('Using best checkpoint for prediction and model exports')
    #     built_model.load_weights(join(output_dir, checkpoint_name))
    # else:
    #     logger.info('Using last epoch for prediction and model exports')
    #
    # # save for later model export(s)
    # weight_name = base_name + '.h5'
    # built_model.save(weight_name)
    # with h5py.File(weight_name, 'a') as f:
    #     f.attrs['sonusai_feature'] = hypermodel.feature
    #     f.attrs['sonusai_num_classes'] = str(hypermodel.num_classes)
    # logger.info(f'Saved trained model to {weight_name}')
    #
    # # Compute prediction metrics on validation data using the best checkpoint
    # v_predict = built_model.predict(v_datagen, batch_size=hypermodel.batch_size, verbose=1)
    # v_predict, _ = reshape_outputs(predict=v_predict, timesteps=hypermodel.timesteps)
    #
    # # Write data to separate files
    # v_predict_dir = base_name + '-valpredict'
    # makedirs(v_predict_dir, exist_ok=True)
    # for idx, mixid in enumerate(v_mixid):
    #     output_name = join(v_predict_dir, v_mixdb.mixtures[mixid].name)
    #     indices = v_datagen.file_indices[idx]
    #     frames = indices.stop - indices.start
    #     data = v_predict[indices]
    #     # The predict operation may produce less data due to timesteps and batches may not dividing evenly
    #     # Only write data if it exists
    #     if data.shape[0] == frames:
    #         with h5py.File(output_name, 'a') as f:
    #             if 'predict' in f:
    #                 del f['predict']
    #             f.create_dataset('predict', data=data)
    #
    # logger.info(f'Wrote validation predict data to {v_predict_dir}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
