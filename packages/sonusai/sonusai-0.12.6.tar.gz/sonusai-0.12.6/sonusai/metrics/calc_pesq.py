import numpy as np


def calc_pesq(hypothesis: np.ndarray, reference: np.ndarray, error_value: float = 0.0) -> float:
    """Computes the PESQ score of speech estimate audio vs. the clean speech estimate audio

    Upon error, assigns a value of 0, or user specified value in error_value

    :param hypothesis: speech estimated audio
    :param reference: speech reference audio
    :param error_value:
    :return: value between -0.5 to 4.5
    """
    import warnings

    from pesq import pesq

    from sonusai import logger
    from sonusai.mixture import SAMPLE_RATE

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            score = pesq(SAMPLE_RATE, reference, hypothesis, mode='wb')
    except Exception as e:
        logger.debug(f'PESQ error {e}')
        score = error_value

    return score
