"""sonusai calc_metric_spenh

usage: calc_metric_spenh [-hvtpws] [-i MIXID] [-e WER] [-m WMNAME] PLOC TLOC

options:
    -h, --help
    -v, --verbose               Be verbose.
    -i MIXID, --mixid MIXID     Mixture ID(s) to process, can be range like 0:maxmix+1 [default: *].
    -t, --truth-est-mode        Calculate extraction and metrics using truth (instead of prediction).
    -p, --plot                  Enable PDF plots file generation per mixture.
    -w, --wav                   Generate WAV files per mixture.
    -s, --summary               Enable summary files generation.
    -e WER, --wer-method WER    Word-Error-Rate method: deepgram, google, aixplain_whisper
                                or whisper (locally run) [default: none]
    -m WMNAME, --whisper-model  Whisper model name used in aixplain_whisper and whisper WER methods.
                                [default: small_en]

Calculate speech enhancement metrics of prediction data in PLOC using SonusAI mixture data
in TLOC as truth/label reference. Metric and extraction data files are written into PLOC.

PLOC  directory containing prediction data in .h5 files created from truth/label mixture data in TLOC
TLOC  directory with SonusAI mixture database of truth/label mixture data

For whisper WER methods, the possible models used in local processing (WER = whisper) are:
    {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}
but note most are very computationally demanding and can overwhelm/hang a local system.

Outputs the following to PLOC (where id is mixd number 0:num_mixtures):
    <id>_metric_spenh.txt

    If --plot:
        <id>_metric_spenh.pdf

    If --wav:
        <id>_target.wav
        <id>_target_est.wav
        <id>_noise.wav
        <id>_noise_est.wav
        <id>_mixture.wav

        If --truth-est-mode:
            <id>_target_truth_est.wav
            <id>_noise_truth_est.wav

    If --summary:
        metric_spenh_targetf_summary.txt
        metric_spenh_targetf_summary.csv
        metric_spenh_targetf_list.csv
        metric_spenh_targetf_estats_list.csv

        If --truth-est-mode:
            metric_spenh_targetf_truth_list.csv
            metric_spenh_targetf_estats_truth_list.csv

TBD
Metric and extraction data are written into prediction location PLOC as separate files per mixture.

    -d PLOC, --ploc PLOC        Location of SonusAI predict data.

Inputs:

"""
from dataclasses import dataclass
from typing import Optional
from typing import Tuple
from typing import Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sonusai import logger
from sonusai.mixture import AudioF
from sonusai.mixture import AudioT
from sonusai.mixture import Feature
from sonusai.mixture import Location
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict
from sonusai.utils import calc_asr

matplotlib.use('SVG')


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    mixdb: Optional[MixtureDatabase] = None
    predict_location: Optional[Location] = None
    truth_est_mode: Optional[bool] = None
    enable_plot: Optional[bool] = None
    enable_wav: Optional[bool] = None
    wer_method: Optional[str] = None
    whisper_model: Optional[str] = None


MP_GLOBAL = MPGlobal()


def power_compress(spec):
    mag = np.abs(spec)
    phase = np.angle(spec)
    mag = mag ** 0.3
    real_compress = mag * np.cos(phase)
    imag_compress = mag * np.sin(phase)
    return real_compress + 1j * imag_compress


def power_uncompress(spec):
    mag = np.abs(spec)
    phase = np.angle(spec)
    mag = mag ** (1. / 0.3)
    real_uncompress = mag * np.cos(phase)
    imag_uncompress = mag * np.sin(phase)
    return real_uncompress + 1j * imag_uncompress


def mean_square_error(hypothesis: np.ndarray,
                      reference: np.ndarray,
                      squared: bool = False) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate root-mean-square error or mean square error

    :param hypothesis: [frames, bins]
    :param reference: [frames, bins]
    :param squared: calculate mean square rather than root-mean-square
    :return: mean, mean per bin, mean per frame
    """
    sq_err = np.square(reference - hypothesis)

    # mean over frames for value per bin
    err_b = np.mean(sq_err, axis=0)
    # mean over bins for value per frame
    err_f = np.mean(sq_err, axis=1)
    # mean over all
    err = np.mean(sq_err)

    if not squared:
        err_b = np.sqrt(err_b)
        err_f = np.sqrt(err_f)
        err = np.sqrt(err)

    return err, err_b, err_f


def mean_abs_percentage_error(hypothesis: np.ndarray,
                              reference: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate mean abs percentage error

    If inputs are complex, calculates average: mape(real)/2 + mape(imag)/2

    :param hypothesis: [frames, bins]
    :param reference: [frames, bins]
    :return: mean, mean per bin, mean per frame
    """
    if not np.iscomplexobj(reference) and not np.iscomplexobj(hypothesis):
        abs_err = 100 * np.abs((reference - hypothesis) / (reference + np.finfo(np.float32).eps))
    else:
        reference_r = np.real(reference)
        reference_i = np.imag(reference)
        hypothesis_r = np.real(hypothesis)
        hypothesis_i = np.imag(hypothesis)
        abs_err_r = 100 * np.abs((reference_r - hypothesis_r) / (reference_r + np.finfo(np.float32).eps))
        abs_err_i = 100 * np.abs((reference_i - hypothesis_i) / (reference_i + np.finfo(np.float32).eps))
        abs_err = (abs_err_r / 2) + (abs_err_i / 2)

    # mean over frames for value per bin
    err_b = np.around(np.mean(abs_err, axis=0), 3)
    # mean over bins for value per frame
    err_f = np.around(np.mean(abs_err, axis=1), 3)
    # mean over all
    err = np.around(np.mean(abs_err), 3)

    return err, err_b, err_f


def log_error(reference: np.ndarray, hypothesis: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate log error

    :param reference: complex or real [frames, bins]
    :param hypothesis: complex or real [frames, bins]
    :return: mean, mean per bin, mean per frame
    """
    reference_sq = np.real(reference * np.conjugate(reference))
    hypothesis_sq = np.real(hypothesis * np.conjugate(hypothesis))
    log_err = abs(10 * np.log10((reference_sq + np.finfo(np.float32).eps) / (hypothesis_sq + np.finfo(np.float32).eps)))
    # log_err = abs(10 * np.log10(reference_sq / (hypothesis_sq + np.finfo(np.float32).eps) + np.finfo(np.float32).eps))

    # mean over frames for value per bin
    err_b = np.around(np.mean(log_err, axis=0), 3)
    # mean over bins for value per frame
    err_f = np.around(np.mean(log_err, axis=1), 3)
    # mean over all
    err = np.around(np.mean(log_err), 3)

    return err, err_b, err_f


def phase_distance(reference: np.ndarray, hypothesis: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate weighted phase distance error

    :param reference: complex [frames, bins]
    :param hypothesis: complex [frames, bins]
    :return: mean, mean per bin, mean per frame
    """
    reference_mag = np.abs(reference)
    # rh_angle_diff = np.angle(reference) - np.angle(hypothesis)
    rh_angle_diff = np.angle(reference / (hypothesis + 1e-7)) * 180 / np.pi  # angle diff +/-180

    # weighted mean over all (scalar)
    ref_weight = reference_mag / (np.sum(reference_mag) + 1e-7)  # frames x bins
    err = np.around(np.sum(ref_weight * rh_angle_diff), 3)

    # weighted mean over frames (value per bin)
    err_b = np.zeros(reference.shape[1])
    for bi in range(reference.shape[1]):
        ref_weight = reference_mag[:, bi] / (np.sum(reference_mag[:, bi], axis=0) + 1e-7)
        err_b[bi] = np.around(np.sum(ref_weight * rh_angle_diff[:, bi]), 3)

    # weighted mean over bins (value per frame)
    err_f = np.zeros(reference.shape[0])
    for fi in range(reference.shape[0]):
        ref_weight = reference_mag[fi, :] / (np.sum(reference_mag[fi, :]) + 1e-7)
        err_f[fi] = np.around(np.sum(ref_weight * rh_angle_diff[fi, :]), 3)

    return err, err_b, err_f


def plot_mixpred(mixture: AudioT,
                 mixture_f: AudioF,
                 target: Optional[AudioT] = None,
                 feature: Optional[Feature] = None,
                 predict: Optional[Predict] = None,
                 tp_title: str = '') -> plt.figure:
    from sonusai.mixture import SAMPLE_RATE

    num_plots = 2
    if feature is not None:
        num_plots += 1
    if predict is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    p = 0
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[p].plot(x_axis, mixture, label='Mixture', color='mistyrose')
    ax[0].set_ylabel('magnitude', color='tab:blue')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    if target is not None:  # Plot target time-domain waveform on top of mixture
        ax[0].plot(x_axis, target, label='Target', color='tab:blue')
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[p].set_title('Waveform')

    # Plot the mixture spectrogram
    p += 1
    ax[p].imshow(np.transpose(mixture_f), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Mixture')

    if feature is not None:
        p += 1
        ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Feature')

    if predict is not None:
        p += 1
        im = ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + tp_title)
        plt.colorbar(im, location='bottom')

    return fig


def plot_pdb_predtruth(predict: np.ndarray,
                       truth_f: Union[np.ndarray, None] = None,
                       metric: Union[np.ndarray, None] = None,
                       tp_title: str = '') -> plt.figure:
    """Plot predict and optionally truth and a metric in power db, e.g. applies 10*log10(predict)"""
    num_plots = 2
    if truth_f is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    tmp = 10 * np.log10(predict.transpose() + np.finfo(np.float32).eps)
    im = ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')
    plt.colorbar(im, location='bottom')

    if truth_f is not None:
        p += 1
        tmp = 10 * np.log10(truth_f.transpose() + np.finfo(np.float32).eps)
        im = ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')
        plt.colorbar(im, location='bottom')

    # Plot the predict avg, and optionally truth avg and metric lines
    pred_avg = 10 * np.log10(np.mean(predict, axis=-1) + np.finfo(np.float32).eps)
    p += 1
    x_axis = np.arange(len(pred_avg), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, pred_avg, color='black', linestyle='dashed', label='Predict mean over freq.')
    ax[p].set_ylabel('mean db', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_f is not None:
        truth_avg = 10 * np.log10(np.mean(truth_f, axis=-1) + np.finfo(np.float32).eps)
        ax[p].plot(x_axis, truth_avg, color='green', linestyle='dashed', label='Truth mean over freq.')

    if metric is not None:  # instantiate 2nd y-axis that shares the same x-axis
        ax2 = ax[p].twinx()
        color2 = 'red'
        ax2.plot(x_axis, metric, color=color2, label='sig distortion (mse db)')
        ax2.set_xlim(x_axis[0], x_axis[-1])
        ax2.set_ylim([0, np.max(metric)])
        ax2.set_ylabel('spectral distortion (mse db)', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        ax[p].set_title('SNR and SNR mse (mean over freq. db)')
    else:
        ax[p].set_title('SNR (mean over freq. db)')
        # ax[0].tick_params(axis='y', labelcolor=color)
    return fig


def plot_epredtruth(predict: np.ndarray,
                    predict_wav: np.ndarray,
                    truth_f: Union[np.ndarray, None] = None,
                    truth_wav: Union[np.ndarray, None] = None,
                    metric: Union[np.ndarray, None] = None,
                    tp_title: str = '') -> plt.figure:
    """Plot predict spectrogram and waveform and optionally truth and a metric)"""
    num_plots = 2
    if truth_f is not None:
        num_plots += 1
    if metric is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    im = ax[p].imshow(predict.transpose(), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')
    plt.colorbar(im, location='bottom')

    if truth_f is not None:  # plot truth if provided and use same colormap as predict
        p += 1
        ax[p].imshow(truth_f.transpose(), im.cmap, aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')

    # Plot the predict wav, and optionally truth avg and metric lines
    p += 1
    x_axis = np.arange(len(predict_wav), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, predict_wav, color='black', linestyle='dashed', label='Speech Estimate')
    ax[p].set_ylabel('Amplitude', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_wav is not None:
        ntrim = len(truth_wav) - len(predict_wav)
        if ntrim > 0:
            truth_wav = truth_wav[0:-ntrim]
        ax[p].plot(x_axis, truth_wav, color='green', linestyle='dashed', label='True Target')

    # Plot the metric lines
    if metric is not None:
        p += 1
        if metric.ndim > 1:  # if it has multiple dims, plot 1st
            metric1 = metric[:, 0]
        else:
            metric1 = metric  # if single dim, plot it as 1st
        x_axis = np.arange(len(metric1), dtype=np.float32)  # / SAMPLE_RATE
        ax[p].plot(x_axis, metric1, color='red', label='Target LogErr')
        ax[p].set_ylabel('log error db', color='red')
        ax[p].set_xlim(x_axis[0], x_axis[-1])
        ax[p].set_ylim([-0.01, np.max(metric1) + .01])
        if metric.ndim > 1:
            if metric.shape[1] > 1:
                metr2 = metric[:, 1]
                ax2 = ax[p].twinx()
                color2 = 'blue'
                ax2.plot(x_axis, metr2, color=color2, label='phase dist (deg)')
                # ax2.set_ylim([-180.0, +180.0])
                if np.max(metr2) - np.min(metr2) > .1:
                    ax2.set_ylim([np.min(metr2), np.max(metr2)])
                ax2.set_ylabel('phase dist (deg)', color=color2)
                ax2.tick_params(axis='y', labelcolor=color2)
                # ax[p].set_title('SNR and SNR mse (mean over freq. db)')

    return fig


def _process_mixture(mixid: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    from os.path import basename
    from os.path import join
    from os.path import splitext

    import h5py

    from sonusai import SonusAIError
    from sonusai.metrics import calc_pcm
    from sonusai.metrics import calc_pesq
    from sonusai.metrics import calc_sa_sdr
    from sonusai.metrics import calc_wsdr
    from sonusai.metrics import calc_wer
    from sonusai.utils import float_to_int16
    from sonusai.utils import unstack_complex
    from sonusai.utils import write_wav
    from sonusai.utils import reshape_outputs

    mixdb = MP_GLOBAL.mixdb
    predict_location = MP_GLOBAL.predict_location
    truth_est_mode = MP_GLOBAL.truth_est_mode
    enable_plot = MP_GLOBAL.enable_plot
    enable_wav = MP_GLOBAL.enable_wav
    wer_method = MP_GLOBAL.wer_method
    whisper_model = MP_GLOBAL.whisper_model

    # 1)  Read predict data, var predict with shape [BatchSize,Classes] or [BatchSize,Tsteps,Classes]
    output_name = join(predict_location, mixdb.mixtures[mixid].name)
    predict = None
    if not truth_est_mode:
        base_name = splitext(output_name)[0]
        try:
            with h5py.File(output_name, 'r') as f:
                predict = np.array(f['predict'])
        except Exception as e:
            raise SonusAIError(f'Error reading {output_name}: {e}')
        # reshape to always be [frames,classes] where ndim==3 case frames = batch * tsteps
        if predict.ndim > 2:  # TBD generalize to somehow detect if timestep dim exists, some cases > 2 don't have
            # logger.debug(f'Prediction reshape from {predict.shape} to remove timestep dimension.')
            predict, _ = reshape_outputs(predict=predict, timesteps=predict.shape[1])
    else:
        # in truth estimation mode we use the truth instead of prediction to see metrics with perfect input
        # so don't bother to read prediction and mark outputs with tru suffix, i.e. 0000_truest_*
        base_name = splitext(output_name)[0] + '_truest'

    # 2) Collect true target, noise, mixture data, trim to predict size if needed
    target = mixdb.mixture_target(mixid)
    target_f = mixdb.mixture_target_f(mixid, target=target)
    noise = mixdb.mixture_noise(mixid)
    noise_f = mixdb.mixture_noise_f(mixid, noise=noise)
    mixture = mixdb.mixture_mixture(mixid, target=target, noise=noise)
    mixture_f = mixdb.mixture_mixture_f(mixid, mixture=mixture)
    segsnr_f = mixdb.mixture_segsnr(mixid, target=target, noise=noise)
    segsnr_f[segsnr_f == np.inf] = 7.944e8  # 99dB
    segsnr_f[segsnr_f == -np.inf] = 1.258e-10  # -99dB
    # need to use inv-tf to match #samples & latency shift properties of predict inv tf
    targetfi, _ = mixdb.inverse_transform(target_f)
    noisefi, _ = mixdb.inverse_transform(noise_f)
    # mixturefi = mixdb.inverse_transform(mixture_f)

    # gen feature, truth - note feature only used for plots
    # TBD parse truth_f for different formats and also multi-truth
    feature, truth_f = mixdb.mixture_ft(mixid, mixture=mixture)
    truth_type = mixdb.targets[mixdb.mixtures[mixid].target_file_index[0]].truth_settings[0].function
    if truth_type == 'target_mixture_f':
        half = truth_f.shape[-1] // 2
        truth_f = truth_f[..., :half]  # extract target_f only

    if not truth_est_mode:
        if predict.shape[0] < target_f.shape[0]:  # target_f, truth_f, mixture_f, etc. same size
            trimf = target_f.shape[0] - predict.shape[0]
            logger.debug(f'Warning: prediction frames less than mixture, trimming {trimf} frames from all truth.')
            target_f = target_f[0:-trimf, :]
            targetfi, _ = mixdb.inverse_transform(target_f)
            trimt = target.shape[0] - targetfi.shape[0]
            target = target[0:-trimt]
            noise_f = noise_f[0:-trimf, :]
            noise = noise[0:-trimt]
            mixture_f = mixture_f[0:-trimf, :]
            mixture = mixture[0:-trimt]
            truth_f = truth_f[0:-trimf, :]
        elif predict.shape[0] > target_f.shape[0]:
            raise SonusAIError(f'Error: prediction has more frames than true mixture '
                               f'{predict.shape[0]} vs {truth_f.shape[0]}')

    # 3) Extraction - format proper complex and wav estimates and truth (unstack, uncompress, inv tf, etc.)
    if truth_est_mode:
        predict = truth_f  # substitute truth for the prediction (for test/debug)
        predict_complex = unstack_complex(predict)  # unstack
        # if feat has compressed mag and truth does not, compress it
        if mixdb.feature[0:2] == 'hn' and mixdb.targets[0].truth_settings[0].function[0:10] != 'targetcmpr':
            predict_complex = power_compress(predict_complex)  # from uncompressed truth
    else:
        predict_complex = unstack_complex(predict)

    truth_f_complex = unstack_complex(truth_f)
    if mixdb.feature[0:2] == 'hn':  # if feat has compressed mag
        # estimate noise in uncompressed-mag domain
        noise_est_complex = mixture_f - power_uncompress(predict_complex)
        predict_complex = power_uncompress(predict_complex)  # uncompress if truth is compressed
    else:  # cn, c8, ..
        noise_est_complex = mixture_f - predict_complex

    target_est_wav, _ = mixdb.inverse_transform(predict_complex)
    noise_est_wav, _ = mixdb.inverse_transform(noise_est_complex)

    # 4) Metrics
    # Target/Speech logerr - PSD estimation accuracy symmetric mean log-spectral distortion
    lerr_tg, lerr_tg_bin, lerr_tg_frame = log_error(reference=truth_f_complex, hypothesis=predict_complex)
    # Noise logerr - PSD estimation accuracy
    lerr_n, lerr_n_bin, lerr_n_frame = log_error(reference=noise_f, hypothesis=noise_est_complex)
    # PCM loss metric
    ytrue_f = np.concatenate((truth_f_complex[:, np.newaxis, :], noise_f[:, np.newaxis, :]), axis=1)
    ypred_f = np.concatenate((predict_complex[:, np.newaxis, :], noise_est_complex[:, np.newaxis, :]), axis=1)
    pcm, pcm_bin, pcm_frame = calc_pcm(hypothesis=ypred_f, reference=ytrue_f, with_log=True)

    # Phase distance
    phd, phd_bin, phd_frame = phase_distance(hypothesis=predict_complex, reference=truth_f_complex)

    # Noise td logerr
    # lerr_nt, lerr_nt_bin, lerr_nt_frame = log_error(noisefi, noise_truth_est_audio)

    # SA-SDR (time-domain source-aggragated SDR)
    ytrue = np.concatenate((targetfi[:, np.newaxis], noisefi[:, np.newaxis]), axis=1)
    ypred = np.concatenate((target_est_wav[:, np.newaxis], noise_est_wav[:, np.newaxis]), axis=1)
    # note: w/o scale is more pessimistic number
    sa_sdr, _ = calc_sa_sdr(hypothesis=ypred, reference=ytrue)

    wsdr, wsdr_cc, wsdr_cw = calc_wsdr(hypothesis=ypred, reference=ytrue, with_log=True)
    logger.debug(f'wsdr weight sum for mixid {mixid} = {np.sum(wsdr_cw)}.')
    logger.debug(f'wsdr cweights = {wsdr_cw}.')
    logger.debug(f'wsdr ccoefs for mixid {mixid} = {wsdr_cc}.')

    # Speech intelligibility measure - PESQ
    if int(mixdb.mixtures[mixid].snr) > -99:
        pesq_speech = calc_pesq(hypothesis=target_est_wav, reference=target)
        pesq_mixture = calc_pesq(hypothesis=mixture, reference=target)
        # pesq improvement
        pesq_impr = pesq_speech - pesq_mixture
        # pesq improvement %
        pesq_impr_pc = pesq_impr / (pesq_mixture + np.finfo(np.float32).eps) * 100
    else:
        pesq_speech = 0
        pesq_mixture = 0
        pesq_impr_pc = np.float32(0)

    # Calc WER
    if wer_method == 'none':
        asr_tt = ''
        asr_mx = ''
        asr_tge = ''
        wer_mx = float('nan')
        wer_tge = float('nan')
        wer_pi = float('nan')
    else:
        if mixdb.asr_manifest:
            asr_tt = mixdb.mixid_asr_data(mixid)[0]  # ignore mixup
        else:
            asr_tt = calc_asr(target, engine=wer_method, whisper_model_name=whisper_model).text  # target truth

        if asr_tt:
            asr_mx = calc_asr(mixture, engine=wer_method, whisper_model_name=whisper_model).text
            asr_tge = calc_asr(target_est_wav, engine=wer_method, whisper_model_name=whisper_model).text

            wer_mx = calc_wer(asr_mx, asr_tt).wer * 100  # mixture wer
            wer_tge = calc_wer(asr_tge, asr_tt).wer * 100  # target estimate wer
            if wer_mx == 0.0:
                if wer_tge == 0.0:
                    wer_pi = 0.0
                else:
                    wer_pi = -999.0
            else:
                wer_pi = 100 * (wer_mx - wer_tge) / wer_mx
        else:
            if mixdb.mixtures[mixid].snr != -99:
                print(f'Warning: mixid {mixid} asr truth is empty, setting to 0% wer')
            asr_mx = ''
            asr_tge = ''
            wer_mx = float(0)
            wer_tge = float(0)
            wer_pi = float(0)

    # 5) Save per mixture metric results
    # Single row in table of scalar metrics per mixture
    mtable1_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi%', 'MXWER', 'WER', 'WERi%', 'WSDR', 'SASDR',
                   'PCM', 'SPLERR', 'NLERR', 'PD', 'SPFILE', 'NFILE']
    ti = mixdb.mixtures[mixid].target_file_index[0]
    ni = mixdb.mixtures[mixid].noise_file_index
    metr1 = [mixdb.mixtures[mixid].snr, pesq_mixture, pesq_speech, pesq_impr_pc, wer_mx, wer_tge, wer_pi, wsdr,
             sa_sdr, pcm, lerr_tg, lerr_n, phd, basename(mixdb.targets[ti].name), basename(mixdb.noises[ni].name)]
    mtab1 = pd.DataFrame([metr1], columns=mtable1_col, index=[mixid])

    # Stats of per frame estimation metrics
    metr2 = pd.DataFrame({'SSNR':  segsnr_f,
                          'PCM':   pcm_frame,
                          'SLERR': lerr_tg_frame,
                          'NLERR': lerr_n_frame,
                          'SPD':   phd_frame})
    metr2 = metr2.describe()  # Use pandas stat function
    metr2['SSNR'][1:] = metr2['SSNR'][1:].apply(lambda x: 10 * np.log10(x))  # Change SSNR stats to dB, except count
    # create a single row in multi-column header
    new_labels = pd.MultiIndex.from_product([metr2.columns,
                                             ['Avg', 'Min', 'Med', 'Max', 'Std']],
                                            names=['Metric', 'Stat'])
    dat1row = metr2.loc[['mean', 'min', '50%', 'max', 'std'], :].T.stack().to_numpy().reshape((1, -1))
    mtab2 = pd.DataFrame(dat1row,
                         index=[mixid],
                         columns=new_labels)
    mtab2.insert(0, 'MXSNR', mixdb.mixtures[mixid].snr, False)  # add MXSNR as the first metric column

    all_metrics_table_1 = mtab1  # return to be collected by process
    all_metrics_table_2 = mtab2  # return to be collected by process

    metric_name = base_name + '_metric_spenh.txt'
    with open(metric_name, 'w') as f:
        print('Speech enhancement metrics:', file=f)
        print(mtab1.round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
        print('', file=f)
        print(f'Extraction statistics over {mixture_f.shape[0]} frames:', file=f)
        print(metr2.round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
        print('', file=f)
        print(f'Target path: {mixdb.targets[ti].name}', file=f)
        print(f'Noise path: {mixdb.noises[ni].name}', file=f)
        if wer_method != 'none':
            print(f'WER method: {wer_method} and whisper model (if used):  {whisper_model}', file=f)
            if mixdb.asr_manifest:
                print(f'ASR truth from manifest:  {asr_tt}', file=f)
            else:
                print(f'ASR truth from wer method:  {asr_tt}', file=f)
            print(f'ASR result for mixture:  {asr_mx}', file=f)
            print(f'ASR result for prediction:  {asr_tge}', file=f)
        # print(f'PESQ improvement: {pesq_impr:0.2f}, {pesq_impr_pc:0.1f}%', file=f)

    # 7) write wav files
    if enable_wav:
        write_wav(name=base_name + '_mixture.wav', audio=float_to_int16(mixture))
        write_wav(name=base_name + '_target.wav', audio=float_to_int16(target))
        write_wav(name=base_name + '_noise.wav', audio=float_to_int16(noise))
        write_wav(name=base_name + '_target_est.wav', audio=float_to_int16(target_est_wav))
        write_wav(name=base_name + '_noise_est.wav', audio=float_to_int16(noise_est_wav))

        # debug code to test for perfect reconstruction of the extraction method
        # note both 75% olsa-hanns and 50% olsa-hann modes checked to have perfect reconstruction
        # target_r = mixdb.inverse_transform(target_f)
        # noise_r = mixdb.inverse_transform(noise_f)
        # _write_wav(name=base_name + '_target_r.wav', audio=float_to_int16(target_r))
        # _write_wav(name=base_name + '_noise_r.wav', audio=float_to_int16(noise_r)) # chk perfect rec

    # 8) Write out plot file
    if enable_plot:
        from matplotlib.backends.backend_pdf import PdfPages
        plot_fname = base_name + '_metric_spenh.pdf'

        # Reshape feature to eliminate overlap redundancy for easier to understand spectrogram view
        # Original size (frames, stride, num_bands), decimates in stride dimension only if step is > 1
        # Reshape to get frames*decimated_stride, num_bands
        step = int(mixdb.feature_samples / mixdb.feature_step_samples)
        if feature.ndim != 3:
            raise SonusAIError(f'feature does not have 3 dimensions: frames, stride, num_bands')

        # for feature cn*00n**
        feat_sgram = unstack_complex(feature)
        feat_sgram = 20 * np.log10(abs(feat_sgram) + np.finfo(np.float32).eps)
        feat_sgram = feat_sgram[:, -step:, :]  # decimate,  Fx1xB
        feat_sgram = np.reshape(feat_sgram, (feat_sgram.shape[0] * feat_sgram.shape[1], feat_sgram.shape[2]))

        with PdfPages(plot_fname) as pdf:
            # page1 we always have a mixture and prediction, target optional if truth provided
            tfunc_name = mixdb.targets[0].truth_settings[0].function  # first target, assumes all have same
            if tfunc_name == 'mapped_snr_f':
                # leave as unmapped snr
                predplot = predict
                tfunc_name = mixdb.targets[0].truth_settings[0].function
            elif tfunc_name == 'target_f' or 'target_mixture_f':
                predplot = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            else:
                # use dB scale
                predplot = 10 * np.log10(predict + np.finfo(np.float32).eps)
                tfunc_name = tfunc_name + ' (db)'

            mixspec = 20 * np.log10(abs(mixture_f) + np.finfo(np.float32).eps)
            pdf.savefig(plot_mixpred(mixture=mixture,
                                     mixture_f=mixspec,
                                     target=target,
                                     feature=feat_sgram,
                                     predict=predplot,
                                     tp_title=tfunc_name))

            # ----- page 2, plot unmapped predict, opt truth reconstructed and line plots of mean-over-f
            # pdf.savefig(plot_pdb_predtruth(predict=pred_snr_f, tp_title='predict snr_f (db)'))

            # page 3 speech extraction
            tg_spec = 20 * np.log10(abs(target_f) + np.finfo(np.float32).eps)
            tg_est_spec = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            # n_spec = np.reshape(n_spec,(n_spec.shape[0] * n_spec.shape[1], n_spec.shape[2]))
            pdf.savefig(plot_epredtruth(predict=tg_est_spec,
                                        predict_wav=target_est_wav,
                                        truth_f=tg_spec,
                                        truth_wav=targetfi,
                                        metric=np.vstack((lerr_tg_frame, phd_frame)).T,
                                        tp_title='speech estimate'))

            # page 4 noise extraction
            n_spec = 20 * np.log10(abs(noise_f) + np.finfo(np.float32).eps)
            n_est_spec = 20 * np.log10(abs(noise_est_complex) + np.finfo(np.float32).eps)
            pdf.savefig(plot_epredtruth(predict=n_est_spec,
                                        predict_wav=noise_est_wav,
                                        truth_f=n_spec,
                                        truth_wav=noisefi,
                                        metric=lerr_n_frame,
                                        tp_title='noise estimate'))

            # Plot error waveforms
            # tg_err_wav = targetfi - target_est_wav
            # tg_err_spec = 20*np.log10(np.abs(target_f - predict_complex))

        plt.close('all')

    return all_metrics_table_1, all_metrics_table_2


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    predict_location = args['PLOC']
    wer_method = args['--wer-method'].lower()
    truth_est_mode = args['--truth-est-mode']
    enable_plot = args['--plot']
    enable_wav = args['--wav']
    enable_summary = args['--summary']
    truth_location = args['TLOC']
    whisper_model = args['--whisper-model'].lower()

    from os.path import join, isdir, basename
    import glob
    from tqdm import tqdm
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import p_tqdm_map

    # Check prediction subdirectory
    if not isdir(predict_location):
        print(f'The specified predict location {predict_location} is not a valid subdirectory path, exiting ...')

    # allpfiles = listdir(predict_location)
    allph5files = glob.glob(predict_location + "/*.h5")
    predict_logfile = glob.glob(predict_location + "/*predict.log")
    if len(allph5files) <= 0 and not truth_est_mode:
        print(f'Subdirectory {predict_location} has no files with .h5 extension, exiting ...')
    else:
        logger.info(f'Found {len(allph5files)} prediction .h5 files.')
    if len(predict_logfile) == 0:
        logger.info(f'Warning, predict location {predict_location} has no prediction log files.')
    else:
        logger.info(f'Found predict log {basename(predict_logfile[0])} in predict location.')

    # Setup logging file
    create_file_handler(join(predict_location, 'calc_metric_spenh.log'))
    update_console_handler(verbose)
    initial_log_messages('calc_metric_spenh')

    mixdb = MixtureDatabase(config=truth_location)
    mixids = mixdb.mixids_to_list(mixids)
    logger.info(f'Found mixdb of {len(mixdb.mixtures)} total mixtures, '
                f'with {mixdb.num_classes} classes in {truth_location}')
    logger.info(f'Only running specified subset of {len(mixids)} mixtures')

    enable_asr_warmup = False
    if wer_method == 'none':
        fnb = 'metric_spenh_'
    elif wer_method == 'google':
        fnb = 'metric_spenh_ggl_'
        logger.info(f'WER enabled with method {wer_method}')
        enable_asr_warmup = True
    elif wer_method == 'deepgram':
        fnb = 'metric_spenh_dgram_'
        logger.info(f'WER enabled with method {wer_method}')
        enable_asr_warmup = True
    elif wer_method == 'aixplain_whisper':
        fnb = 'metric_spenh_whsp_' + whisper_model + '_'
        logger.info(f'WER enabled with method {wer_method} and whisper model {whisper_model}')
        enable_asr_warmup = True
    elif wer_method == 'whisper':
        fnb = 'metric_spenh_whspl_' + whisper_model + '_'
        logger.info(f'WER enabled with method {wer_method} and whisper model {whisper_model}')
        enable_asr_warmup = True
    else:
        logger.error(f'Unrecognized WER method: {wer_method}')
        return

    if enable_asr_warmup:
        from sonusai.mixture import DEFAULT_SPEECH
        from sonusai.mixture import read_audio
        audio = read_audio(DEFAULT_SPEECH)
        logger.info(f'Warming up asr method, note for cloud service this could take up to a few min ...')
        asr_chk = calc_asr(audio, engine=wer_method, whisper_model_name=whisper_model)
        logger.info(f'Warmup completed, results {asr_chk}')

    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.predict_location = predict_location
    MP_GLOBAL.truth_est_mode = truth_est_mode
    MP_GLOBAL.enable_plot = enable_plot
    MP_GLOBAL.enable_wav = enable_wav
    MP_GLOBAL.wer_method = wer_method
    MP_GLOBAL.whisper_model = whisper_model

    # Individual mixtures use pandas print, set precision to 2 decimal places
    # pd.set_option('float_format', '{:.2f}'.format)
    progress = tqdm(total=len(mixids))
    all_metrics_tables = p_tqdm_map(_process_mixture, mixids, progress=progress)
    progress.close()

    all_metrics_table_1 = pd.concat([item[0] for item in all_metrics_tables])
    all_metrics_table_2 = pd.concat([item[1] for item in all_metrics_tables])

    if not enable_summary:
        return

    # 9) Done with mixtures, write out summary metrics
    # Calculate SNR summary avg of each non-random snr
    all_mtab1_sorted = all_metrics_table_1.sort_values(by=['MXSNR', 'SPFILE'])
    all_mtab2_sorted = all_metrics_table_2.sort_values(by=['MXSNR'])
    mtab_snr_summary = None
    mtab_snr_summary_em = None
    for snri in range(0, len(mixdb.snrs)):
        tmp = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(numeric_only=True).to_frame().T
        # avoid nan when subset of mixids specified
        if ~np.isnan(tmp.iloc[0].to_numpy()[0]).any():
            mtab_snr_summary = pd.concat([mtab_snr_summary, tmp])

        tmp = all_mtab2_sorted[all_mtab2_sorted['MXSNR'] == mixdb.snrs[snri]].mean(numeric_only=True).to_frame().T
        # avoid nan when subset of mixids specified (mxsnr will be nan if no data):
        if ~np.isnan(tmp.iloc[0].to_numpy()[0]).any():
            mtab_snr_summary_em = pd.concat([mtab_snr_summary_em, tmp])

    # Correct percentages in snr summary table
    mtab_snr_summary['PESQi%'] = 100 * (mtab_snr_summary['PESQ'] - mtab_snr_summary['MXPESQ']) / np.maximum(
        mtab_snr_summary['MXPESQ'], 0.01)
    for i in range(len(mtab_snr_summary)):
        tmp_mxwer = mtab_snr_summary['MXWER'].iloc[i]
        tmp_wer = mtab_snr_summary['WER'].iloc[i]
        if tmp_mxwer == 0.0:
            if tmp_wer == 0.0:
                mtab_snr_summary['WERi%'].iloc[i] = 0.0
            else:
                mtab_snr_summary['WERi%'].iloc[i] = -999.0
        else:
            mtab_snr_summary['WERi%'].iloc[i] = 100 * (tmp_mxwer - tmp_wer) / tmp_mxwer

    # Calculate avg metrics over all mixtures except -99
    all_mtab1_sorted_nom99 = all_mtab1_sorted[all_mtab1_sorted.MXSNR != -99]
    all_nom99_mean = all_mtab1_sorted_nom99.mean(numeric_only=True)

    # correct the percentage averages with a direct calculation (PESQ% and WER%):
    all_nom99_mean[3] = 100 * (all_nom99_mean[2] - all_nom99_mean[1]) / np.maximum(all_nom99_mean[1], 0.01)  # pesq%
    if all_nom99_mean[4] == 0.0:
        if all_nom99_mean[5] == 0.0:
            all_nom99_mean[6] = 0.0
        else:
            all_nom99_mean[6] = -999.0
    else:
        all_nom99_mean[6] = 100 * (all_nom99_mean[4] - all_nom99_mean[5]) / all_nom99_mean[4]  # wer%

    num_mix = len(mixids)
    if num_mix > 1:
        # Print pandas data to files using precision to 2 decimals
        # pd.set_option('float_format', '{:.2f}'.format)
        csp = 0

        if not truth_est_mode:
            ofname = join(predict_location, fnb + 'summary.txt')
        else:
            ofname = join(predict_location, fnb + 'summary_truest.txt')

        with open(ofname, 'w') as f:
            print(f'WER enabled with method {wer_method}, whisper model, if used: {whisper_model}', file=f)
            print(f'Speech enhancement metrics avg over all {len(all_mtab1_sorted_nom99)} non -99 SNR mixtures:',
                  file=f)
            print(all_nom99_mean.to_frame().T.round(2).to_string(float_format=lambda x: "{:.2f}".format(x),
                                                                 index=False), file=f)
            print(f'\nSpeech enhancement metrics avg over each SNR:', file=f)
            print(mtab_snr_summary.round(2).to_string(float_format=lambda x: "{:.2f}".format(x), index=False), file=f)
            print('', file=f)
            print(f'Extraction statistics stats avg over each SNR:', file=f)
            # with pd.option_context('display.max_colwidth', 9):
            # with pd.set_option('float_format', '{:.1f}'.format):
            print(mtab_snr_summary_em.round(1).to_string(float_format=lambda x: "{:.1f}".format(x), index=False),
                  file=f)
            print('', file=f)
            # pd.set_option('float_format', '{:.2f}'.format)

            print(f'Speech enhancement metrics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_1.describe().round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
            print('', file=f)
            print(f'Extraction statistics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_2.describe().round(2).to_string(float_format=lambda x: "{:.1f}".format(x)), file=f)
            print('', file=f)

            print('Speech enhancement metrics all-mixtures list:', file=f)
            # print(all_metrics_table_1.head().style.format(precision=2), file=f)
            print(all_metrics_table_1.round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
            print('', file=f)
            print('Extraction statistics all-mixtures list:', file=f)
            print(all_metrics_table_2.round(2).to_string(float_format=lambda x: "{:.1f}".format(x)), file=f)

        # Write summary to .csv file
        if not truth_est_mode:
            csv_name = join(predict_location, fnb + 'summary.csv')
        else:
            csv_name = join(predict_location, fnb + 'summary_truest.csv')
        header_args = {
            'mode':     'a',
            'encoding': 'utf-8',
            'index':    False,
            'header':   False,
        }
        table_args = {
            'mode':     'a',
            'encoding': 'utf-8',
        }
        label = f'Speech enhancement metrics avg over all {len(all_mtab1_sorted_nom99)} non -99 SNR mixtures:'
        pd.DataFrame([label]).to_csv(csv_name, header=False, index=False)  # open as write
        all_nom99_mean.to_frame().T.round(2).to_csv(csv_name, index=False, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        pd.DataFrame([f'Speech enhancement metrics avg over each SNR:']).to_csv(csv_name, **header_args)
        mtab_snr_summary.round(2).to_csv(csv_name, index=False, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        pd.DataFrame([f'Extraction statistics stats avg over each SNR:']).to_csv(csv_name, **header_args)
        mtab_snr_summary_em.round(2).to_csv(csv_name, index=False, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        label = f'Speech enhancement metrics stats over {num_mix} mixtures:'
        pd.DataFrame([label]).to_csv(csv_name, **header_args)
        all_metrics_table_1.describe().round(2).to_csv(csv_name, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        label = f'Extraction statistics stats over {num_mix} mixtures:'
        pd.DataFrame([label]).to_csv(csv_name, **header_args)
        all_metrics_table_2.describe().round(2).to_csv(csv_name, **table_args)
        label = f'WER enabled with method {wer_method}, whisper model, if used: {whisper_model}'
        pd.DataFrame([label]).to_csv(csv_name, **header_args)

        if not truth_est_mode:
            csv_name = join(predict_location, fnb + 'list.csv')
        else:
            csv_name = join(predict_location, fnb + 'list_truest.csv')
        pd.DataFrame(['Speech enhancement metrics list:']).to_csv(csv_name, header=False, index=False)  # open as write
        all_metrics_table_1.round(2).to_csv(csv_name, **table_args)

        if not truth_est_mode:
            csv_name = join(predict_location, fnb + 'estats_list.csv')
        else:
            csv_name = join(predict_location, fnb + 'estats_list_truest.csv')
        pd.DataFrame(['Extraction statistics list:']).to_csv(csv_name, header=False, index=False)  # open as write
        all_metrics_table_2.round(2).to_csv(csv_name, **table_args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
