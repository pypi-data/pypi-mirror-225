from dataclasses import dataclass
from typing import Any

from sonusai.mixture.types import AudioT


@dataclass(frozen=True)
class Data:
    audio: AudioT
    whisper_model: Any = None
    whisper_model_name: str = None
    device: str = None
