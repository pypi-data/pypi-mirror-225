from sonusai.mixture.truth_functions.data import Data
from sonusai.mixture.types import Truth


def phoneme(_data: Data) -> Truth:
    # Read in .txt transcript and run a Python function to generate text grid data
    # (indicating which phonemes are active)
    # Then generate truth based on this data and put in the correct classes based on config.index
    from sonusai import SonusAIError

    raise SonusAIError('Truth function phoneme is not supported yet')
