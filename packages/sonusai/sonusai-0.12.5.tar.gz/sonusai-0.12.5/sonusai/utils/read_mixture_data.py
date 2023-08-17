from typing import Optional
from typing import Tuple

import numpy as np


def read_mixture_data(filename: str) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]:
    """Read mixture, target, and noise data from given HDF5 file and return them as a tuple."""
    import h5py

    if not filename:
        return None, None, None

    with h5py.File(filename, 'r') as f:
        return np.array(f['mixture']), np.array(f['target']), np.array(f['noise'])
