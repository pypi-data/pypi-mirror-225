from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import numpy.typing as npt
from dataclasses_json import DataClassJsonMixin

AudioT = npt.NDArray[np.float32]
AudiosT = List[AudioT]

ListAudiosT = List[AudiosT]

Truth = npt.NDArray[np.float32]
Segsnr = npt.NDArray[np.float32]

AudioF = npt.NDArray[np.complex64]
AudiosF = List[AudioF]

EnergyT = npt.NDArray[np.float32]
EnergyF = npt.NDArray[np.float32]

Feature = npt.NDArray[np.float32]

Predict = npt.NDArray[np.float32]

Location = str

# Json type defined to maintain compatibility with DataClassJsonMixin
Json = Union[dict, list, str, int, float, bool, None]


class DataClassSonusAIMixin(DataClassJsonMixin):
    from typing import Dict

    def __str__(self):
        return f'{self.to_dict()}'

    # Override DataClassJsonMixin to remove dictionary keys with values of None
    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        def del_none(d):
            if isinstance(d, dict):
                for key, value in list(d.items()):
                    if value is None:
                        del d[key]
                    elif isinstance(value, dict):
                        del_none(value)
                    elif isinstance(value, list):
                        for item in value:
                            del_none(item)
            elif isinstance(d, list):
                for item in d:
                    del_none(item)
            return d

        return del_none(super().to_dict(encode_json))


@dataclass(frozen=True)
class TruthSetting(DataClassSonusAIMixin):
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[List[int]] = None


TruthSettings = List[TruthSetting]
OptionalNumberStr = Optional[Union[float, int, str]]
OptionalListNumberStr = Optional[List[Union[float, int, str]]]


@dataclass
class Augmentation(DataClassSonusAIMixin):
    normalize: OptionalNumberStr = None
    pitch: OptionalNumberStr = None
    tempo: OptionalNumberStr = None
    gain: OptionalNumberStr = None
    eq1: OptionalListNumberStr = None
    eq2: OptionalListNumberStr = None
    eq3: OptionalListNumberStr = None
    lpf: OptionalNumberStr = None
    ir: OptionalNumberStr = None
    count: Optional[int] = None
    mixup: Optional[int] = 1


Augmentations = List[Augmentation]


@dataclass
class TargetFile(DataClassSonusAIMixin):
    name: Location
    samples: int
    truth_settings: TruthSettings
    class_balancing_augmentation: Optional[Augmentation] = None
    target_level_type: Optional[str] = None

    @property
    def duration(self) -> float:
        from sonusai.mixture import SAMPLE_RATE

        return self.samples / SAMPLE_RATE


TargetFiles = List[TargetFile]


@dataclass
class AugmentedTarget(DataClassSonusAIMixin):
    target_augmentation_index: int
    target_file_index: int


AugmentedTargets = List[AugmentedTarget]


@dataclass
class NoiseFile(DataClassSonusAIMixin):
    name: Location
    samples: int
    augmentations: Optional[Augmentations] = None

    @property
    def duration(self) -> float:
        from sonusai.mixture import SAMPLE_RATE

        return self.samples / SAMPLE_RATE


NoiseFiles = List[NoiseFile]
ClassCount = List[int]

GeneralizedIDs = Union[str, int, List[int], range]


@dataclass(frozen=True)
class TruthFunctionConfig(DataClassSonusAIMixin):
    feature: str
    mutex: bool
    num_classes: int
    target_gain: float
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[List[int]] = None


@dataclass
class GenMixData:
    targets: AudiosT = None
    noise: AudioT = None
    mixture: AudioT = None
    truth_t: Optional[Truth] = None
    segsnr_t: Optional[Segsnr] = None


@dataclass
class GenFTData:
    feature: Optional[Feature] = None
    truth_f: Optional[Truth] = None
    segsnr: Optional[Segsnr] = None


@dataclass(frozen=True)
class ImpulseResponseData:
    name: Location
    sample_rate: int
    offset: int
    length: int
    coefficients_file: Location


@dataclass(frozen=True)
class ImpulseResponseRawData:
    name: Location
    sample_rate: int
    offset: int
    filter: AudioT


ImpulseResponseFiles = List[Location]


@dataclass(frozen=True)
class SpectralMask:
    f_max_width: int
    f_num: int
    t_max_width: int
    t_num: int
    t_max_percent: int


SpectralMasks = List[SpectralMask]


@dataclass(frozen=True)
class UniversalSNR:
    is_random: bool
    raw_value: Union[float, str]

    @property
    def value(self) -> float:
        from sonusai.mixture import evaluate_random_rule

        if self.is_random:
            return float(evaluate_random_rule(str(self.raw_value)))

        return float(self.raw_value)
