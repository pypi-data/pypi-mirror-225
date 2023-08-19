from sonusai.mixture.types import Feature
from sonusai.mixture.types import SpectralMask


def apply_spectral_mask(feature: Feature, spectral_mask: SpectralMask, seed: int = None) -> Feature:
    """Apply frequency and time masking

    Implementation of SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition

    Ref: https://arxiv.org/pdf/1904.08779.pdf

    f_width consecutive bands [f_start, f_start + f_width) are masked, where f_width is chosen from a uniform
    distribution from 0 to the f_max_width, and f_start is chosen from [0, bands - f_width).

    t_width consecutive frames [t_start, t_start + t_width) are masked, where t_width is chosen from a uniform
    distribution from 0 to the t_max_width, and t_start is chosen from [0, frames - t_width).

    A time mask cannot be wider than t_max_percent times the number of frames.

    :param feature: Numpy array of feature data [frames, strides, bands]
    :param spectral_mask: Spectral mask parameters
    :param seed: Random number seed
    :return: Augmented feature
    """
    import numpy as np

    from sonusai import SonusAIError

    if feature.ndim != 3:
        raise SonusAIError('feature input must have three dimensions [frames, strides, bands]')

    frames, strides, bands = feature.shape

    f_max_width = spectral_mask.f_max_width
    if f_max_width not in range(0, bands + 1):
        f_max_width = bands

    rng = np.random.default_rng(seed)

    # apply f_num frequency masks to the feature
    for _ in range(spectral_mask.f_num):
        f_width = int(rng.uniform(0, f_max_width))
        f_start = rng.integers(0, bands - f_width, endpoint=True)
        feature[:, :, f_start:f_start + f_width] = 0

    # apply t_num time masks to the feature
    t_upper_bound = int(spectral_mask.t_max_percent / 100 * frames)
    for _ in range(spectral_mask.t_num):
        t_width = min(int(rng.uniform(0, spectral_mask.t_max_width)), t_upper_bound)
        t_start = rng.integers(0, frames - t_width, endpoint=True)
        feature[t_start:t_start + t_width, :, :] = 0

    return feature
