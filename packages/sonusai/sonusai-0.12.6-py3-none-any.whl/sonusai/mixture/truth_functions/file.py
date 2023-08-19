from sonusai.mixture.truth_functions.data import Data
from sonusai.mixture.types import Truth


def file(data: Data) -> Truth:
    import h5py
    import numpy as np

    from sonusai import SonusAIError

    if data.config.config is None:
        raise SonusAIError('Truth function file missing config')

    parameters = ['file']
    for parameter in parameters:
        if 'file' not in data.config.config:
            raise SonusAIError(f'Truth function file config missing required parameter: {parameter}')

    with h5py.File(data.config.config['file'], 'r') as f:
        if 'truth_t' not in f:
            raise SonusAIError('Truth file does not contain truth_t dataset')
        truth_in = np.array(f['truth_t'])

    if truth_in.ndim != 2:
        raise SonusAIError('Truth file data is not 2 dimensions')

    if truth_in.shape[0] != len(data.target_audio):
        raise SonusAIError('Truth file does not contain the right amount of samples')

    if len(data.zero_based_indices) > 1:
        if len(data.zero_based_indices) != truth_in.shape[1]:
            raise SonusAIError('Truth file does not contain the right amount of classes')

        data.truth[:, data.zero_based_indices] = truth_in
    else:
        index = data.zero_based_indices[0]
        if index + truth_in.shape[1] > data.config.num_classes:
            raise SonusAIError('Truth file contains too many classes')

        data.truth[:, index:index + truth_in.shape[1]] = truth_in

    return data.truth
