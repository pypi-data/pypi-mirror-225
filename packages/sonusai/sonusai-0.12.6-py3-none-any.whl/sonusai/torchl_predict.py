"""sonusai torchl_predict

usage: torchl_predict [-hvrw] [-i MIXID] [-m MODEL] (-k CKPT) [-b BATCH] [-t TSTEPS] INPUT ...

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to use if input is a mixture database. [default: *].
    -m MODEL, --model MODEL         Pytorch lightning model .py file path.
    -k CKPT, --checkpoint CKPT      Pytorch lightning checkpoint file with weights.
    -b BATCH, --batch BATCH         Batch size (deprecated and forced to 1). [default: 1]
    -t TSTEPS, --tsteps TSTEPS      Timesteps. If 0, dim is not included/expected in model. [default: 0]
    -r, --reset                     Reset model between each file.
    -w, --wavdbg                    Write debug .wav files of feature input, truth, and predict. [default: False]

Run pytorch lightning prediction on a SonusAI mixture database using a model and checkpoint inputs.
The torch lightning model is imported from MODEL .py file and weights loaded from checkpoint file CKPT.

Inputs:
    MODEL       Path to a .py with MyHyperModel Pytorch Lightning model class definition
    CKPT        A pytorch lightning checkpoint file with weights.
    INPUT       The input data must be one of the following:
                * directory
                  Use SonusAI mixture database directory, generate feature and truth data if not found.
                  Run prediction on the feature. The MIXID is required (or default which is *)

                * Single WAV file or glob of WAV files
                  Using the given model, generate feature data and run prediction. A model file must be
                  provided. The MIXID is ignored.

Outputs the following to tpredict-<TIMESTAMP> directory:
    <id>.h5
        dataset:    predict
    torch_predict.log

"""
from typing import Any

import torch

from sonusai import logger
from sonusai.mixture import Feature


def power_compress(x):
    real = x[..., 0]
    imag = x[..., 1]
    spec = torch.complex(real, imag)
    mag = torch.abs(spec)
    phase = torch.angle(spec)
    mag = mag ** 0.3
    real_compress = mag * torch.cos(phase)
    imag_compress = mag * torch.sin(phase)
    return torch.stack([real_compress, imag_compress], 1)


def power_uncompress(real, imag):
    spec = torch.complex(real, imag)
    mag = torch.abs(spec)
    phase = torch.angle(spec)
    mag = mag ** (1. / 0.3)
    real_compress = mag * torch.cos(phase)
    imag_compress = mag * torch.sin(phase)
    return torch.stack([real_compress, imag_compress], -1)


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    modelpath = args['--model']
    ckpt_name = args['--checkpoint']
    batch_size = args['--batch']
    timesteps = args['--tsteps']
    reset = args['--reset']
    wavdbg = args['--wavdbg']  # write .wav if true
    input_name = args['INPUT']

    from os import makedirs
    from os.path import basename
    from os.path import isdir
    from os.path import isfile
    from os.path import join
    from os.path import splitext
    from os.path import normpath
    import h5py
    from sonusai.utils import write_wav
    # from sonusai.utils import float_to_int16

    from torchinfo import summary
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_feature_from_audio
    from sonusai.utils import import_keras_model
    from sonusai.mixture import read_audio
    from sonusai.utils import create_ts_name
    from sonusai.data_generator import TorchFromMixtureDatabase

    if batch_size is not None:
        batch_size = int(batch_size)
    if batch_size != 1:
        batch_size = 1
        logger.info(f'For now prediction only supports batch_size = 1, forcing it to 1 now')

    if timesteps is not None:
        timesteps = int(timesteps)

    if len(input_name) == 1 and isdir(input_name[0]):
        in_basename = basename(normpath(input_name[0]))
    else:
        in_basename = ''

    output_dir = create_ts_name('tpredict-' + in_basename)
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    logger.info(f'Created output subdirectory {output_dir}')
    create_file_handler(join(output_dir, 'torchl_predict.log'))
    update_console_handler(verbose)
    initial_log_messages('torch_predict')
    logger.info(f'torch    {torch.__version__}')

    try:
        checkpoint = torch.load(ckpt_name, map_location=lambda storage, loc: storage)
        # Note other possible way to load model (not working)
        # model = litemodule.L.LightningModule.load_from_checkpoint(ckpt_name, **hparams)
    except Exception as e:
        logger.exception(f'Error: could not load checkpoint from {ckpt_name}: {e}')
        raise SystemExit(1)

    # Import model definition file
    model_base = basename(modelpath)
    model_root = splitext(model_base)[0]
    logger.info(f'Importing {modelpath}')
    litemodule = import_keras_model(modelpath)

    if 'hyper_parameters' in checkpoint:
        hparams = checkpoint['hyper_parameters']
        logger.info(f'Found checkpoint file with hyper-params named {checkpoint["hparams_name"]} '
                    f'with {len(hparams)} total hparams.')
        if batch_size is not None and hparams['batch_size'] != batch_size:
            if batch_size != 1:
                batch_size = 1
                logger.info(f'For now prediction only supports batch_size = 1, forcing it to 1 now')
            logger.info(f'Overriding batch_size: default = {hparams["batch_size"]}; specified = {batch_size}.')
            hparams["batch_size"] = batch_size

        if timesteps is not None:
            if hparams['timesteps'] == 0 and timesteps != 0:
                logger.warning(f'Model does not contain timesteps; ignoring override.')
                timesteps = 0

            if hparams['timesteps'] != 0 and timesteps == 0:
                logger.warning(f'Model contains timesteps; ignoring override, using model default.')
                timesteps = hparams['timesteps']

            if hparams['timesteps'] != timesteps:
                logger.info(f'Overriding timesteps: default = {hparams["timesteps"]}; specified = {timesteps}.')
                hparams['timesteps'] = timesteps

        logger.info(f'Building model with hparams and batch_size={batch_size}, timesteps={timesteps}')
        try:
            model = litemodule.MyHyperModel(**hparams)  # use hparams
            # litemodule.MyHyperModel.load_from_checkpoint(ckpt_name, **hparams)
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_base} failed: {e}')
            raise SystemExit(1)
    else:
        logger.info(f'Warning: found checkpoint with no hyper-parameters, building model with defaults')
        try:
            tmp = litemodule.MyHyperModel()  # use default hparams
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_base} failed: {e}')
            raise SystemExit(1)

        if batch_size is not None:
            if tmp.batch_size != batch_size:
                logger.info(f'Overriding batch_size: default = {tmp.batch_size}; specified = {batch_size}.')
        else:
            batch_size = tmp.batch_size  # inherit

        if timesteps is not None:
            if tmp.timesteps == 0 and timesteps != 0:
                logger.warning(f'Model does not contain timesteps; ignoring override.')
                timesteps = 0

            if tmp.timesteps != 0 and timesteps == 0:
                logger.warning(f'Model contains timesteps; ignoring override.')
                timesteps = tmp.timesteps

            if tmp.timesteps != timesteps:
                logger.info(f'Overriding timesteps: default = {tmp.timesteps}; specified = {timesteps}.')
        else:
            timesteps = tmp.timesteps

        logger.info(f'Building model with default hparams and batch_size= {batch_size}, timesteps={timesteps}')
        model = litemodule.MyHyperModel(timesteps=timesteps, batch_size=batch_size)

    logger.info('')
    logger.info(summary(model))
    logger.info('')
    logger.info(f'feature       {model.feature}')
    logger.info(f'num_classes   {model.num_classes}')
    logger.info(f'batch_size    {model.batch_size}')
    logger.info(f'timesteps     {model.timesteps}')
    logger.info(f'flatten       {model.flatten}')
    logger.info(f'add1ch        {model.add1ch}')
    logger.info(f'truth_mutex   {model.truth_mutex}')
    logger.info(f'input_shape   {model.input_shape}')
    logger.info('')
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()

    logger.info('')
    # Load mixture database and setup dataloader
    if len(input_name) == 1 and isdir(input_name[0]):  # Single path to mixdb subdir
        input_name = input_name[0]
        logger.info(f'Loading mixture database from {input_name}')
        mixdb = MixtureDatabase(config=input_name)
        logger.info(f'Sonusai mixture db: found {len(mixdb.mixtures)} mixtures with {mixdb.num_classes} classes')

        if mixdb.feature != model.feature:
            logger.exception(f'Feature in mixture database {mixdb.feature} does not match feature in model')
            raise SystemExit(1)

        # TBD check num_classes ??

        p_mixids = mixdb.mixids_to_list(mixids)
        sampler = None
        p_datagen = TorchFromMixtureDatabase(mixdb=mixdb,
                                             mixids=p_mixids,
                                             batch_size=model.batch_size,
                                             cut_len=0,
                                             flatten=model.flatten,
                                             add1ch=model.add1ch,
                                             random_cut=False,
                                             sampler=sampler,
                                             drop_last=False,
                                             num_workers=0)

        if wavdbg:  # setup for wav write if enabled
            # Info needed to setup inverse transform
            from pyaaware import FeatureGenerator
            from pyaaware import TorchInverseTransform
            from torchaudio import save
            # from sonusai.utils import write_wav

            half = model.num_classes // 2
            fg = FeatureGenerator(feature_mode=model.feature,
                                  num_classes=model.num_classes,
                                  truth_mutex=model.truth_mutex)
            itf = TorchInverseTransform(N=fg.itransform_N,
                                        R=fg.itransform_R,
                                        bin_start=fg.bin_start,
                                        bin_end=fg.bin_end,
                                        ttype=fg.itransform_ttype)

            if mixdb.targets[0].truth_settings[0].function == 'target_f' or \
                    mixdb.targets[0].truth_settings[0].function == 'target_mixture_f':
                enable_truth_wav = True
            else:
                enable_truth_wav = False

            if mixdb.targets[0].truth_settings[0].function == 'target_mixture_f':
                enable_mix_wav = True
            else:
                enable_mix_wav = False

        if reset:
            logger.info(f'Running {len(mixdb.mixtures)} mixtures individually with model reset ...')
            for idx, val in enumerate(p_datagen):
                # truth = val[0]
                feature = val[1]
                with torch.no_grad():
                    ypred = model(feature)
                output_name = join(output_dir, mixdb.mixtures[idx].name)
                pdat = ypred.detach().numpy()
                if timesteps > 0:
                    logger.debug(f'In and out tsteps: {feature.shape[1]},{pdat.shape[1]}')
                logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
                with h5py.File(output_name, 'a') as f:
                    if 'predict' in f:
                        del f['predict']
                    f.create_dataset('predict', data=pdat)

                if wavdbg:
                    owav_base = splitext(output_name)[0]
                    tmp = torch.complex(ypred[..., :half], ypred[..., half:]).permute(2, 0, 1).detach()
                    predwav, _ = itf.execute_all(tmp)
                    # predwav, _ = calculate_audio_from_transform(tmp, itf, trim=True)
                    save(owav_base + '.wav', predwav.permute([1, 0]), 16000, encoding='PCM_S', bits_per_sample=16)
                    if enable_truth_wav:
                        # Note this support truth type target_f and target_mixture_f
                        tmp = torch.complex(val[0][..., :half], val[0][..., half:2 * half]).permute(2, 0, 1).detach()
                        truthwav, _ = itf.execute_all(tmp)
                        save(owav_base + '_truth.wav', truthwav.permute([1, 0]), 16000, encoding='PCM_S',
                             bits_per_sample=16)

                    if enable_mix_wav:
                        tmp = torch.complex(val[0][..., 2 * half:3 * half], val[0][..., 3 * half:]).permute(2, 0, 1)
                        mixwav, _ = itf.execute_all(tmp.detach())
                        save(owav_base + "_mix.wav", mixwav.permute([1, 0]), 16000, encoding='PCM_S',
                             bits_per_sample=16)
                        # write_wav(owav_base + "_truth.wav", truthwav, 16000)

        else:
            logger.info(f'Running {len(mixdb.mixtures)} mixtures with model builtin prediction loop ...')
            from lightning.pytorch import Trainer
            trainer = Trainer(default_root_dir=output_dir,
                              accelerator='auto')  # prints avail GPU, TPU, IPU, HPU and selected device
            # logger.info(f'Strategy: {trainer.strategy.strategy_name}')  # doesn't work for ddp strategy
            logger.info(f'Accelerator stats: {trainer.accelerator.get_device_stats(device=None)}')
            logger.info(f'World size: {trainer.world_size}')
            logger.info(f'Nodes: {trainer.num_nodes}')
            logger.info(f'Devices: {trainer.accelerator.auto_device_count()}')

            # Use builtin lightning prediction loop, returns a list
            # predictions = trainer.predict(model, p_datagen)  # standard method, but no support distributed
            trainer.predict(model, p_datagen)
            predictions = model.predict_outputs
            # all_predictions = torch.cat(predictions)   #  predictions = torch.cat(predictions).cpu()
            if trainer.world_size > 1:
                # print(f'Predictions returned: {len(all_predictions)}')
                ddp_max_mem = torch.cuda.max_memory_allocated(trainer.local_rank) / 1000
                logger.info(f"GPU {trainer.local_rank} max memory using DDP: {ddp_max_mem:.2f} MB")
                gathered = [None] * torch.distributed.get_world_size()
                torch.distributed.all_gather_object(gathered, predictions)
                torch.distributed.barrier()
                if not trainer.is_global_zero:
                    return
                predictions = sum(gathered, [])
                if trainer.global_rank == 0:
                    logger.info(f"All predictions gathered: {len(predictions)}")

            logger.info(f'Predictions returned: {len(predictions)}')
            for idx, mixid in enumerate(p_mixids):
                # print(f'{idx}, {mixid}')
                output_name = join(output_dir, mixdb.mixtures[mixid].name)
                pdat = predictions[idx].cpu().numpy()
                logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
                with h5py.File(output_name, 'a') as f:
                    if 'predict' in f:
                        del f['predict']
                    f.create_dataset('predict', data=pdat)

                if wavdbg:
                    owav_base = splitext(output_name)[0]
                    tmp = torch.complex(predictions[idx][..., :half], predictions[idx][..., half:]).permute(2, 1, 0)
                    predwav, _ = itf.execute_all(tmp.squeeze().detach().numpy())
                    write_wav(owav_base + ".wav", predwav.detach().numpy(), 16000)

        logger.info(f'Saved results to {output_dir}')
        return

        # if reset:
        #     # reset mode cycles through each file one at a time
        #     for mixid in mixids:
        #         feature, _ = mixdb.mixture_ft(mixid)
        #         if feature.shape[0] > 2500:
        #             print(f'Trimming input frames from {feature.shape[0]} to {2500},')
        #             feature = feature[0:2500,::]
        #         half = feature.shape[-1] // 2
        #         noisy_spec_cmplx = torch.complex(torch.tensor(feature[..., :half]),
        #                                          torch.tensor(feature[..., half:])).to(device)
        #         del feature
        #
        #         predict = _pad_and_predict(built_model=model, feature=noisy_spec_cmplx)
        #         del noisy_spec_cmplx
        #
        #         audio_est = torch_istft_olsa_hanns(predict, mixdb.it_config.N, mixdb.it_config.R).cpu()
        #         del predict
        #         output_name = join(output_dir, splitext(mixdb.mixtures[mixid].name)[0]+'.wav')
        #         print(f'Saving prediction to {output_name}')
        #         write_wav(name=output_name, audio=float_to_int16(audio_est.detach().numpy()).transpose())
        #
        #         torch.cuda.empty_cache()
        #
        #         # TBD .h5 predict file optional output file
        #         # output_name = join(output_dir, mixdb.mixtures[mixid].name)
        #         # with h5py.File(output_name, 'a') as f:
        #         #     if 'predict' in f:
        #         #         del f['predict']
        #         #     f.create_dataset(name='predict', data=predict)
        #
        # else:
        #     # Run all data at once using a data generator
        #     feature = KerasFromH5(mixdb=mixdb,
        #                           mixids=mixids,
        #                           batch_size=hypermodel.batch_size,
        #                           timesteps=hypermodel.timesteps,
        #                           flatten=hypermodel.flatten,
        #                           add1ch=hypermodel.add1ch)
        #
        #     predict = built_model.predict(feature, batch_size=hypermodel.batch_size, verbose=1)
        #     predict, _ = reshape_outputs(predict=predict, timesteps=hypermodel.timesteps)
        #
        #     # Write data to separate files
        #     for idx, mixid in enumerate(mixids):
        #         output_name = join(output_dir, mixdb.mixtures[mixid].name)
        #         with h5py.File(output_name, 'a') as f:
        #             if 'predict' in f:
        #                 del f['predict']
        #             f.create_dataset('predict', data=predict[feature.file_indices[idx]])
        #
        # logger.info(f'Saved results to {output_dir}')
        # return

    if not all(isfile(file) and splitext(file)[1] == '.wav' for file in input_name):
        logger.exception(f'Do not know how to process input from {input_name}')
        raise SystemExit(1)

    logger.info(f'Run prediction on {len(input_name):,} WAV files')
    for file in input_name:
        # Convert WAV to feature data
        audio = read_audio(file)
        feature = get_feature_from_audio(audio=audio, feature=model.feature)

        # feature, predict = _pad_and_predict(hypermodel=hypermodel,
        #                                     built_model=built_model,
        #                                     feature=feature,
        #                                     frames_per_batch=frames_per_batch)

        # clean = torch_istft_olsa_hanns(clean_spec_cmplx, mixdb.ift_config.N, mixdb.ift_config.R)

        output_name = join(output_dir, splitext(basename(file))[0] + '.h5')
        with h5py.File(output_name, 'a') as f:
            if 'feature' in f:
                del f['feature']
            f.create_dataset(name='feature', data=feature)

            # if 'predict' in f:
            #     del f['predict']
            # f.create_dataset(name='predict', data=predict)

    logger.info(f'Saved results to {output_dir}')
    del model


def _pad_and_predict(built_model: Any, feature: Feature) -> torch.Tensor:
    """
    Run prediction on feature [frames,1,bins*2] (stacked complex numpy array, stride/tsteps=1)
    Returns predict output [batch,frames,bins] in complex torch.tensor
    """
    noisy_spec = power_compress(torch.view_as_real(torch.from_numpy(feature).permute(1, 0, 2)))
    # print(f'noisy_spec type {type(noisy_spec_cmplx)}')
    # print(f'noisy_spec dtype {noisy_spec_cmplx.dtype}')
    # print(f'noisy_spec size {noisy_spec_cmplx.shape}')
    with torch.no_grad():
        est_real, est_imag = built_model(noisy_spec)  # expects in size [batch, 2, tsteps, bins]
    est_real, est_imag = est_real.permute(0, 1, 3, 2), est_imag.permute(0, 1, 3, 2)
    est_spec_uncompress = torch.view_as_complex(power_uncompress(est_real, est_imag).squeeze(1))
    # inv tf want [ch,frames,bins] complex (synonymous with [batch,tsteps,bins]), keep as torch.tensor
    predict = est_spec_uncompress.permute(0, 2, 1)  # .detach().numpy()

    return predict


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
