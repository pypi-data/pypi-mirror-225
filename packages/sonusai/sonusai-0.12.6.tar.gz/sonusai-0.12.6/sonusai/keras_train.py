"""sonusai keras_train

usage: keras_train [-hgv] (-m MODEL) (-l VLOC) [-w KMODEL] [-e EPOCHS] [-b BATCH] [-t TSTEPS] [-p ESP] TLOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -m MODEL, --model MODEL         Model Python file with build and/or hypermodel functions.
    -l VLOC, --vloc VLOC            Location of SonusAI mixture database to use for validation.
    -w KMODEL, --weights KMODEL     Keras model weights file.
    -e EPOCHS, --epochs EPOCHS      Number of epochs to use in training. [default: 8].
    -b BATCH, --batch BATCH         Batch size.
    -t TSTEPS, --tsteps TSTEPS      Timesteps.
    -p ESP, --patience ESP          Early stopping patience.
    -g, --loss-batch-log            Enable per-batch loss log. [default: False]

Use Keras to train a model defined by a Python definition file and SonusAI genft data.

Inputs:
    TLOC    A SonusAI mixture database directory to use for training data.
    VLOC    A SonusAI mixture database directory to use for validation data.

Results are written into subdirectory <MODEL>-<TIMESTAMP>.
Per-batch loss history, if enabled, is written to <basename>-history-lossb.npy

"""
import tensorflow as tf

from sonusai import logger


class LossBatchHistory(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.history = None

    def on_train_begin(self, logs=None):
        self.history = {'loss': []}

    def on_batch_end(self, batch, logs=None):
        if logs is None:
            logs = {}
        self.history['loss'].append(logs.get('loss'))


class SonusAIModelCheckpoint(tf.keras.callbacks.ModelCheckpoint):
    def __init__(self,
                 filepath,
                 monitor: str = "val_loss",
                 verbose: int = 0,
                 save_best_only: bool = False,
                 save_weights_only: bool = False,
                 mode: str = "auto",
                 save_freq="epoch",
                 options=None,
                 initial_value_threshold=None,
                 **kwargs):
        super().__init__(filepath,
                         monitor,
                         verbose,
                         save_best_only,
                         save_weights_only,
                         mode,
                         save_freq,
                         options,
                         initial_value_threshold,
                         **kwargs)
        self.feature = kwargs.get('feature', None)
        self.num_classes = kwargs.get('num_classes', None)

    def _save_model(self, epoch, batch, logs):
        import h5py

        super()._save_model(epoch, batch, logs)

        with h5py.File(self.filepath, 'a') as f:
            if self.feature is not None:
                f.attrs['sonusai_feature'] = self.feature
            if self.num_classes is not None:
                f.attrs['sonusai_num_classes'] = str(self.num_classes)


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
    esp = args['--patience']
    loss_batch_log = args['--loss-batch-log']
    t_name = args['TLOC']

    import warnings
    from os import makedirs
    from os import walk
    from os.path import basename
    from os.path import join
    from os.path import splitext

    import h5py
    import keras_tuner as kt
    import numpy as np

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        from keras import backend as kb
        from keras.callbacks import EarlyStopping

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.data_generator import KerasFromH5
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import check_keras_overrides
    from sonusai.utils import create_ts_name
    from sonusai.utils import import_keras_model
    from sonusai.utils import stratified_shuffle_split_mixid
    from sonusai.utils import reshape_outputs
    from sonusai.utils import get_frames_per_batch

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
    create_file_handler(join(output_dir, 'keras_train.log'))
    update_console_handler(verbose)
    initial_log_messages('keras_train')

    logger.info(f'tensorflow    {tf.__version__}')
    logger.info(f'keras         {tf.keras.__version__}')
    logger.info('')

    t_mixdb = MixtureDatabase(config=t_name)
    logger.info(f'Training: found {len(t_mixdb.mixtures)} mixtures with {t_mixdb.num_classes} classes from {t_name}')

    v_mixdb = MixtureDatabase(config=v_name)
    logger.info(f'Validation: found {len(v_mixdb.mixtures)} mixtures with {v_mixdb.num_classes} classes from {v_name}')

    # Import model definition file
    logger.info(f'Importing {model_base}')
    model = import_keras_model(model_name)

    # Check overrides
    timesteps = check_keras_overrides(model, t_mixdb.feature, t_mixdb.num_classes, timesteps, batch_size)
    # Calculate batches per epoch, use ceiling as last batch is zero extended
    frames_per_batch = get_frames_per_batch(batch_size, timesteps)
    batches_per_epoch = int(np.ceil(t_mixdb.total_feature_frames('*') / frames_per_batch))

    logger.info('Building and compiling model')
    try:
        hypermodel = model.MyHyperModel(feature=t_mixdb.feature,
                                        num_classes=t_mixdb.num_classes,
                                        timesteps=timesteps,
                                        batch_size=batch_size)
        built_model = hypermodel.build_model(kt.HyperParameters())
        built_model = hypermodel.compile_default(built_model, batches_per_epoch)
    except Exception as e:
        logger.exception(f'Error: build_model() in {model_base} failed: {e}')
        raise SystemExit(1)

    kb.clear_session()
    logger.info('')
    built_model.summary(print_fn=logger.info)
    logger.info('')
    logger.info(f'feature       {hypermodel.feature}')
    logger.info(f'num_classes   {hypermodel.num_classes}')
    logger.info(f'batch_size    {hypermodel.batch_size}')
    logger.info(f'timesteps     {hypermodel.timesteps}')
    logger.info(f'flatten       {hypermodel.flatten}')
    logger.info(f'add1ch        {hypermodel.add1ch}')
    logger.info(f'truth_mutex   {hypermodel.truth_mutex}')
    logger.info(f'lossf         {hypermodel.lossf}')
    logger.info(f'input_shape   {hypermodel.input_shape}')
    logger.info(f'optimizer     {built_model.optimizer.get_config()}')
    logger.info('')

    t_mixid = t_mixdb.mixids_to_list()
    v_mixid = v_mixdb.mixids_to_list()

    stratify = False
    if stratify:
        logger.info(f'Stratifying training data')
        t_mixid, _, _, _ = stratified_shuffle_split_mixid(t_mixdb, vsplit=0)

    # Use SonusAI DataGenerator to create validation feature/truth on the fly
    v_datagen = KerasFromH5(mixdb=v_mixdb,
                            mixids=v_mixid,
                            batch_size=hypermodel.batch_size,
                            timesteps=hypermodel.timesteps,
                            flatten=hypermodel.flatten,
                            add1ch=hypermodel.add1ch,
                            shuffle=False)

    # Prepare class weighting
    # class_count = np.ceil(np.array(get_class_count_from_mixids(t_mixdb, t_mixid)) / t_mixdb.feature_step_samples)
    # if t_mixdb.truth_mutex:
    #     other_weight = 16.0
    #     logger.info(f'Detected single-label mode (truth_mutex); setting other weight to {other_weight}')
    #     class_count[-1] = class_count[-1] / other_weight

    # Use SonusAI DataGenerator to create training feature/truth on the fly
    t_datagen = KerasFromH5(mixdb=t_mixdb,
                            mixids=t_mixid,
                            batch_size=hypermodel.batch_size,
                            timesteps=hypermodel.timesteps,
                            flatten=hypermodel.flatten,
                            add1ch=hypermodel.add1ch,
                            shuffle=True)

    # TODO: If hypermodel.es exists, then use it; otherwise use default here
    if esp is None:
        es = EarlyStopping(monitor='val_loss',
                           mode='min',
                           verbose=1,
                           patience=8)
    else:
        es = EarlyStopping(monitor='val_loss',
                           mode='min',
                           verbose=1,
                           patience=int(esp))

    ckpt_callback = SonusAIModelCheckpoint(filepath=base_name + '-ckpt-weights.h5',
                                           save_weights_only=True,
                                           monitor='val_loss',
                                           mode='min',
                                           save_best_only=True,
                                           feature=hypermodel.feature,
                                           num_classes=hypermodel.num_classes)

    csv_logger = tf.keras.callbacks.CSVLogger(base_name + '-history.csv')
    callbacks = [es, ckpt_callback, csv_logger]
    # loss_batch_log = True
    loss_batchlogger = None
    if loss_batch_log is True:
        loss_batchlogger = LossBatchHistory()
        callbacks.append(loss_batchlogger)
        logger.info(f'Adding per batch loss logging to training')

    if weights_name is not None:
        logger.info(f'Loading weights from {weights_name}')
        built_model.load_weights(weights_name)

    logger.info('')
    logger.info(f'Training with no class weighting and early stopping patience = {es.patience}')
    logger.info(f'  training mixtures    {len(t_mixid)}')
    logger.info(f'  validation mixtures  {len(v_mixid)}')
    logger.info('')

    history = built_model.fit(t_datagen,
                              batch_size=hypermodel.batch_size,
                              epochs=epochs,
                              validation_data=v_datagen,
                              shuffle=False,
                              callbacks=callbacks)

    # Save history into numpy file
    history_name = base_name + '-history'
    np.save(history_name, history.history)
    # Note: Reload with history=np.load(history_name, allow_pickle='TRUE').item()
    logger.info(f'Saved training history to numpy file {history_name}.npy')
    if loss_batch_log is True:
        his_batch_loss_name = base_name + '-history-lossb.npy'
        np.save(his_batch_loss_name, loss_batchlogger.history)
        logger.info(f'Saved per-batch loss history to numpy file {his_batch_loss_name}')

    # Find checkpoint file and load weights for prediction and model save
    checkpoint_name = None
    for path, dirs, files in walk(output_dir):
        for file in files:
            if "ckpt" in file:
                checkpoint_name = file

    if checkpoint_name is not None:
        logger.info('Using best checkpoint for prediction and model exports')
        built_model.load_weights(join(output_dir, checkpoint_name))
    else:
        logger.info('Using last epoch for prediction and model exports')

    # save for later model export(s)
    weight_name = base_name + '.h5'
    built_model.save(weight_name)
    with h5py.File(weight_name, 'a') as f:
        f.attrs['sonusai_feature'] = hypermodel.feature
        f.attrs['sonusai_num_classes'] = str(hypermodel.num_classes)
    logger.info(f'Saved trained model to {weight_name}')

    # Compute prediction metrics on validation data using the best checkpoint
    v_predict = built_model.predict(v_datagen, batch_size=hypermodel.batch_size, verbose=1)
    v_predict, _ = reshape_outputs(predict=v_predict, timesteps=hypermodel.timesteps)

    # Write data to separate files
    v_predict_dir = base_name + '-valpredict'
    makedirs(v_predict_dir, exist_ok=True)
    for idx, mixid in enumerate(v_mixid):
        output_name = join(v_predict_dir, v_mixdb.mixtures[mixid].name)
        indices = v_datagen.file_indices[idx]
        frames = indices.stop - indices.start
        data = v_predict[indices]
        # The predict operation may produce less data due to timesteps and batches may not dividing evenly
        # Only write data if it exists
        if data.shape[0] == frames:
            with h5py.File(output_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset('predict', data=data)

    logger.info(f'Wrote validation predict data to {v_predict_dir}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
