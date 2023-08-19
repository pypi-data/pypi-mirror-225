from sonusai.mixture.truth_functions.data import Data
from sonusai.mixture.types import Truth


def _core(data: Data, polar: bool) -> Truth:
    import numpy as np

    from sonusai import SonusAIError

    if data.config.num_classes != data.target_fft.bins:
        raise SonusAIError(f'Invalid num_classes for crm truth: {data.config.num_classes}')

    if data.target_fft.bins != data.noise_fft.bins:
        raise SonusAIError('Transform size mismatch for crm truth')

    for offset in data.offsets:
        target_f = data.target_fft.execute(data.target_audio[offset:offset + data.frame_size]).astype(np.complex64)
        noise_f = data.noise_fft.execute(data.noise_audio[offset:offset + data.frame_size]).astype(np.complex64)
        mixture_f = target_f + noise_f

        crm_data = np.empty(target_f.shape, dtype=np.complex64)
        with np.nditer(target_f, flags=['multi_index'], op_flags=[['readwrite']]) as it:
            for _ in it:
                num = target_f[it.multi_index]
                den = mixture_f[it.multi_index]
                if num == 0:
                    crm_data[it.multi_index] = 0
                elif den == 0:
                    crm_data[it.multi_index] = complex(np.inf, np.inf)
                else:
                    crm_data[it.multi_index] = num / den

        indices = slice(offset, offset + data.frame_size)

        def c1(c_data: np.ndarray, is_polar: bool) -> np.ndarray:
            if is_polar:
                return np.absolute(c_data)
            return np.real(c_data)

        def c2(c_data: np.ndarray, is_polar: bool) -> np.ndarray:
            if is_polar:
                return np.angle(c_data)
            return np.imag(c_data)

        for index in data.zero_based_indices:
            data.truth[indices, index:index + data.target_fft.bins] = c1(crm_data, polar)
            data.truth[indices, (index + data.target_fft.bins):(index + 2 * data.target_fft.bins)] = c2(crm_data, polar)

    return data.truth


def crm(data: Data) -> Truth:
    return _core(data=data, polar=False)


def crmp(data: Data) -> Truth:
    return _core(data=data, polar=True)
