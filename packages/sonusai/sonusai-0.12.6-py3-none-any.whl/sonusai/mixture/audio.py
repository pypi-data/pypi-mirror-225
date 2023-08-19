from typing import Tuple

import sox
from pyaaware import ForwardTransform
from pyaaware import InverseTransform

from sonusai.mixture.types import AudioF
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import EnergyT
from sonusai.mixture.types import ImpulseResponseRawData
from sonusai.mixture.types import Location


def get_next_noise(audio: AudioT, offset: int, length: int) -> AudioT:
    """Get next sequence of noise data from noise audio file

    :param audio: Overall noise audio (entire file's worth of data)
    :param offset: Starting sample
    :param length: Number of samples to get
    :return: Sequence of noise audio data
    """
    import numpy as np

    return np.take(audio, range(offset, offset + length), mode='wrap')


def read_ir(audio_file: Location) -> ImpulseResponseRawData:
    """Read impulse response data

    :param audio_file: Audio file name
    :return: ImpulseResponseRawData object
    """
    import tempfile

    import numpy as np
    from scipy.io import wavfile

    from sonusai import SonusAIError
    from sonusai.mixture import ImpulseResponseData
    from sonusai.mixture import ImpulseResponseRawData
    from sonusai.mixture import apply_ir
    from sonusai.mixture import tokenized_expand

    expanded_name, _ = tokenized_expand(audio_file)

    # Read impulse response data from audio file
    try:
        sample_rate, data = wavfile.read(expanded_name)
    except Exception as e:
        if audio_file != expanded_name:
            raise SonusAIError(f'Error reading {audio_file} (expanded: {expanded_name}): {e}')
        else:
            raise SonusAIError(f'Error reading {audio_file}: {e}')

    # Normalize to -20 dBFS to avoid clipping when applying IR
    max_data = max(abs(data)) * 10
    data = (data / max_data).astype(np.float32)

    # Find offset to align convolved audio with original
    temp = tempfile.NamedTemporaryFile(mode='w+t')
    try:
        for d in data:
            temp.write(f'{d:f}\n')
        temp.seek(0)

        ir = ImpulseResponseData(
            name=audio_file,
            sample_rate=sample_rate,
            offset=0,
            length=len(data),
            coefficients_file=temp.name)
        x = np.zeros((ir.length,), dtype=np.float32)
        x[0] = 1
        y = list(apply_ir(x, ir))
    finally:
        temp.close()

    return ImpulseResponseRawData(
        name=audio_file,
        sample_rate=sample_rate,
        offset=y.index(max(y)),
        filter=data)


def save_ir_data(name: Location, data: AudioT) -> None:
    with open(name, 'w+t') as f:
        for d in data:
            f.write(f'{d:f}\n')


def read_audio(name: Location) -> AudioT:
    """Read audio data from a file

    :param name: File name
    :return: Array of time domain audio data
    """
    from typing import Any

    import numpy as np

    from sonusai import SonusAIError
    from sonusai.mixture import BIT_DEPTH
    from sonusai.mixture import CHANNEL_COUNT
    from sonusai.mixture import ENCODING
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import tokenized_expand

    def encode_output(buffer: Any) -> np.ndarray:
        if BIT_DEPTH == 8:
            return np.frombuffer(buffer, dtype=np.int8)

        if BIT_DEPTH == 16:
            return np.frombuffer(buffer, dtype=np.int16)

        if BIT_DEPTH == 24:
            return np.frombuffer(buffer, dtype=np.int32)

        if BIT_DEPTH == 32:
            if ENCODING == 'floating-point':
                return np.frombuffer(buffer, dtype=np.float32)
            return np.frombuffer(buffer, dtype=np.int32)

        if BIT_DEPTH == 64:
            return np.frombuffer(buffer, dtype=np.float64)

        raise SonusAIError(f'Invalid BIT_DEPTH {BIT_DEPTH}')

    expanded_name, _ = tokenized_expand(name)

    try:
        # Read in and convert to desired format
        # NOTE: pysox format transformations do not handle encoding properly; need to use direct call to sox instead
        args = [
            '-D',
            '-G',
            expanded_name,
            '-t', 'raw',
            '-r', str(SAMPLE_RATE),
            '-b', str(BIT_DEPTH),
            '-c', str(CHANNEL_COUNT),
            '-e', ENCODING,
            '-',
            'remix', '1',
        ]
        status, out, err = sox.core.sox(args, None, False)
        if status != 0:
            raise SonusAIError(f'sox stdout: {out}\nsox stderr: {err}')

        return encode_output(out)

    except Exception as e:
        if name != expanded_name:
            raise SonusAIError(f'Error reading {name} (expanded: {expanded_name}):\n{e}')
        else:
            raise SonusAIError(f'Error reading {name}:\n{e}')


def calculate_transform_from_audio(audio: AudioT,
                                   transform: ForwardTransform) -> Tuple[AudioF, EnergyT]:
    """Apply forward transform to input audio data to generate transform data

    :param audio: Time domain data [samples]
    :param transform: ForwardTransform object
    :return: Frequency domain data [frames, bins], Energy [frames]
    """
    f, e = transform.execute_all(audio)
    return f.transpose(), e


def calculate_audio_from_transform(data: AudioF,
                                   transform: InverseTransform,
                                   trim: bool = True) -> Tuple[AudioT, EnergyT]:
    """Apply inverse transform to input transform data to generate audio data

    :param data: Frequency domain data [frames, bins]
    :param transform: InverseTransform object
    :param trim: Removes starting samples so output waveform will be time-aligned with input waveform to the transform
    :return: Time domain data [samples], Energy [frames]
    """
    t, e = transform.execute_all(data.transpose())
    if trim:
        t = t[transform.N - transform.R:]

    return t, e


def get_duration(audio: AudioT) -> float:
    """Get duration of audio in seconds

    :param audio: Time domain data [samples]
    :return: Duration of audio in seconds
    """
    from sonusai.mixture import SAMPLE_RATE

    return len(audio) / SAMPLE_RATE


class Transformer(sox.Transformer):
    """Override certain sox.Transformer methods
    """

    def fir(self, coefficients):
        """Use SoX’s FFT convolution engine with given FIR filter coefficients.

        The SonusAI override allows coefficients to be either a list of numbers
        or a string containing a text file with the coefficients.

        Parameters
        ----------
        coefficients : list or str
            fir filter coefficients

        """
        from sonusai import SonusAIError

        if not isinstance(coefficients, list) and not isinstance(coefficients, str):
            raise SonusAIError("coefficients must be a list or a str.")

        if isinstance(coefficients, list) and not all([sox.core.is_number(c) for c in coefficients]):
            raise SonusAIError("coefficients list must be numbers.")

        effect_args = ['fir']
        if isinstance(coefficients, list):
            effect_args.extend(['{:f}'.format(c) for c in coefficients])
        else:
            effect_args.append(coefficients)

        self.effects.extend(effect_args)
        self.effects_log.append('fir')

        return self

    def tempo(self, factor, audio_type=None, quick=False):
        """Time stretch audio without changing pitch.

        This effect uses the WSOLA algorithm. The audio is chopped up into
        segments which are then shifted in the time domain and overlapped
        (cross-faded) at points where their waveforms are most similar as
        determined by measurement of least squares.

        The SonusAI override does not generate a warning for small factors.
        The sox.Transformer's implementation of stretch does not invert
        the factor even though it says that it does; this invalidates the
        factor size check and produces the wrong result.

        Parameters
        ----------
        factor : float
            The ratio of new tempo to the old tempo.
            For ex. 1.1 speeds up the tempo by 10%; 0.9 slows it down by 10%.
        audio_type : str
            Type of audio, which optimizes algorithm parameters. One of:
             * m : Music,
             * s : Speech,
             * l : Linear (useful when factor is close to 1),
        quick : bool, default=False
            If True, this effect will run faster but with lower sound quality.

        See Also
        --------
        stretch, speed, pitch

        """
        from sox.core import is_number

        from sonusai import SonusAIError
        from sonusai import logger

        if not is_number(factor) or factor <= 0:
            raise SonusAIError('factor must be a positive number')

        if factor < 0.5 or factor > 2:
            logger.warning('Using an extreme time stretching factor. Quality of results will be poor')

        if audio_type not in [None, 'm', 's', 'l']:
            raise SonusAIError("audio_type must be one of None, 'm', 's', or 'l'.")

        if not isinstance(quick, bool):
            raise SonusAIError('quick must be a boolean')

        effect_args = ['tempo']

        if quick:
            effect_args.append('-q')

        if audio_type is not None:
            effect_args.append('-{}'.format(audio_type))

        effect_args.append('{:f}'.format(factor))

        self.effects.extend(effect_args)
        self.effects_log.append('tempo')

        return self


def validate_input_file(input_filepath: str) -> None:
    from os.path import exists
    from os.path import splitext

    from sox.core import VALID_FORMATS

    from sonusai import SonusAIError

    if not exists(input_filepath):
        raise SonusAIError(f'input_filepath {input_filepath} does not exist.')

    ext = splitext(input_filepath)[1][1:].lower()
    if ext not in VALID_FORMATS:
        raise SonusAIError(f'This installation of SoX cannot process .{ext} files')
