from dataclasses import dataclass
from typing import Any
from typing import Union

from sonusai.mixture import AudioT
from sonusai.mixture import Location


@dataclass(frozen=True)
class ASRResult:
    text: str
    confidence: float = None


def calc_asr(audio: Union[AudioT, Location],
             engine: str = 'deepgram',
             whisper_model: Any = None,
             whisper_model_name: str = 'base.en',
             device: str = None) -> ASRResult:
    """Run ASR on audio

    :param audio: Numpy array of audio samples or location of an audio file
    :param engine: Type of ASR engine to use
    :param whisper_model: A preloaded Whisper ASR model
    :param whisper_model_name: Name of Whisper ASR model to use if none was provided
    :param device: the device to put the ASR model into
    :return: ASRResult object containing text and confidence
    """
    from copy import copy

    import numpy as np

    from sonusai import SonusAIError
    from sonusai.mixture import read_audio
    from sonusai.utils import asr_functions
    from sonusai.utils.asr_functions.data import Data

    if not isinstance(audio, np.ndarray):
        audio = copy(read_audio(audio))

    data = Data(audio, whisper_model, whisper_model_name, device)

    try:
        return getattr(asr_functions, engine)(data)
    except AttributeError:
        raise SonusAIError(f'Unsupported ASR function: {engine}')
