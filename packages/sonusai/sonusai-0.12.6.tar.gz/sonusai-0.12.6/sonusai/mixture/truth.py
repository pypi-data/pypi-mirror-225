from typing import List

from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import Truth
from sonusai.mixture.types import TruthFunctionConfig


def truth_function(target_audio: AudioT, noise_audio: AudioT, config: TruthFunctionConfig) -> Truth:
    from sonusai import SonusAIError
    from sonusai.mixture import truth_functions
    from sonusai.mixture.truth_functions.data import Data

    data = Data(target_audio, noise_audio, config)
    if data.config.target_gain == 0:
        return data.truth

    try:
        return getattr(truth_functions, data.config.function)(data)
    except AttributeError:
        raise SonusAIError(f'Unsupported truth function: {data.config.function}')


def get_truth_indices_for_mixid(mixdb: MixtureDatabase, mixid: int) -> List[int]:
    """Get a list of truth indices for a given mixid."""
    from sonusai.mixture.targets import get_truth_indices_for_target

    indices: List[int] = []
    for target_file_index in mixdb.mixtures[mixid].target_file_index:
        indices.append(*get_truth_indices_for_target(mixdb.targets[target_file_index]))

    return sorted(list(set(indices)))


def truth_reduction(x: Truth, func: str) -> Truth:
    import numpy as np

    from sonusai import SonusAIError

    if func == 'max':
        return np.max(x, axis=0)

    if func == 'mean':
        return np.mean(x, axis=0)

    raise SonusAIError(f'Invalid truth reduction function: {func}')
