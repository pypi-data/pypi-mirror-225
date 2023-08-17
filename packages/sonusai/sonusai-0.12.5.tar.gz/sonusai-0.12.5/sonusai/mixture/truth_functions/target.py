from typing import List

from pyaaware import ForwardTransform

from sonusai.mixture.truth_functions.data import Data
from sonusai.mixture.types import AudioF
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import Truth


def target_f(data: Data) -> Truth:
    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.target_fft.bins:
        raise SonusAIError(f'Invalid num_classes for target_f truth: {data.config.num_classes}')

    target_freq = _gen_f(data.target_audio, data.target_fft, len(data.offsets))
    for idx, offset in enumerate(data.offsets):
        data.truth = _stack(data=target_freq[idx],
                            offset=offset,
                            frame_size=data.frame_size,
                            zero_based_indices=data.zero_based_indices,
                            bins=data.target_fft.bins,
                            start=0,
                            truth=data.truth)

    return data.truth


def target_mixture_f(data: Data) -> Truth:
    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.target_fft.bins + 2 * data.noise_fft.bins:
        raise SonusAIError(f'Invalid num_classes for target_mixture_f truth: {data.config.num_classes}')

    target_freq = _gen_f(data.target_audio, data.target_fft, len(data.offsets))
    noise_freq = _gen_f(data.noise_audio, data.noise_fft, len(data.offsets))

    mixture_freq = target_freq + noise_freq
    for idx, offset in enumerate(data.offsets):
        data.truth = _stack(data=target_freq[idx],
                            offset=offset,
                            frame_size=data.frame_size,
                            zero_based_indices=data.zero_based_indices,
                            bins=data.target_fft.bins,
                            start=0,
                            truth=data.truth)

        data.truth = _stack(data=mixture_freq[idx],
                            offset=offset,
                            frame_size=data.frame_size,
                            zero_based_indices=data.zero_based_indices,
                            bins=data.target_fft.bins,
                            start=data.target_fft.bins * 2,
                            truth=data.truth)

    return data.truth


def target_swin_f(data: Data) -> Truth:
    import numpy as np

    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.target_fft.bins:
        raise SonusAIError(f'Invalid num_classes for target_swin_f truth: {data.config.num_classes}')

    for idx, offset in enumerate(data.offsets):
        target_freq, _ = data.target_fft.execute(
            np.multiply(data.target_audio[offset:offset + data.frame_size], data.swin))
        target_freq = target_freq.transpose()

        indices = slice(offset, offset + data.frame_size)
        for index in data.zero_based_indices:
            bins = _get_bin_slice(index, data.target_fft.bins)
            data.truth[indices, bins] = np.real(target_freq[idx])

            bins = _get_bin_slice(bins.stop, data.target_fft.bins)
            data.truth[indices, bins] = np.imag(target_freq[idx])

    return data.truth


def _gen_f(audio: AudioT, transform: ForwardTransform, expected_frames: int) -> AudioF:
    from sonusai import SonusAIError

    freq, _ = transform.execute_all(audio)
    freq = freq.transpose()
    if len(freq) != expected_frames:
        raise SonusAIError(f'Number of frames, {len(freq)}, is not number of frames expected, {expected_frames}')
    return freq


def _get_bin_slice(start: int, length: int) -> slice:
    return slice(start, start + length)


def _stack(data: AudioF,
           offset: int,
           frame_size: int,
           zero_based_indices: List[int],
           bins: int,
           start: int,
           truth: Truth) -> Truth:
    import numpy as np

    i = _get_bin_slice(offset, frame_size)
    for index in zero_based_indices:
        b = _get_bin_slice(index + start, bins)
        truth[i, b] = np.real(data)

        b = _get_bin_slice(b.stop, bins)
        truth[i, b] = np.imag(data)

    return truth
