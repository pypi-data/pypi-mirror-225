from typing import Optional
from typing import Tuple
from typing import Type

import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.data import Sampler

from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase


class MixtureDatabaseDataset(Dataset):
    """Generates a PyTorch dataset from a SonusAI mixture database
    """

    def __init__(self,
                 mixdb: MixtureDatabase,
                 mixids: GeneralizedIDs,
                 cut_len: int,
                 flatten: bool,
                 add1ch: bool,
                 random_cut: bool = True):
        """Initialization
        """
        self.mixdb = mixdb
        self.mixids = self.mixdb.mixids_to_list(mixids)
        self.cut_len = cut_len
        self.flatten = flatten
        self.add1ch = add1ch
        self.random_cut = random_cut

    def __len__(self):
        return len(self.mixids)

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """Get data from one mixture
        """
        import random

        from sonusai.utils import reshape_inputs

        feature, truth = self.mixdb.mixture_ft(self.mixids[idx])
        feature, truth = reshape_inputs(feature=feature,
                                        truth=truth,
                                        batch_size=1,
                                        timesteps=0,
                                        flatten=self.flatten,
                                        add1ch=self.add1ch)

        length = feature.shape[0]

        if self.cut_len > 0:
            if length < self.cut_len:
                feature_final = []
                truth_final = []
                for _ in range(self.cut_len // length):
                    feature_final.append(feature)
                    truth_final.append(truth)
                feature_final.append(feature[: self.cut_len % length])
                truth_final.append(truth[: self.cut_len % length])
                feature = np.vstack([feature_final[i] for i in range(len(feature_final))])
                truth = np.vstack([truth_final[i] for i in range(len(truth_final))])
            else:
                if self.random_cut:
                    start = random.randint(0, length - self.cut_len)
                else:
                    start = 0
                feature = feature[start:start + self.cut_len]
                truth = truth[start:start + self.cut_len]

        return feature, truth


class AawareDataLoader(DataLoader):
    _cut_len: Optional[int] = None

    @property
    def cut_len(self) -> int:
        return self._cut_len

    @cut_len.setter
    def cut_len(self, value: int) -> None:
        self._cut_len = value


def TorchFromMixtureDatabase(mixdb: MixtureDatabase,
                             mixids: GeneralizedIDs,
                             batch_size: int,
                             flatten: bool,
                             add1ch: bool,
                             num_workers: int = 0,
                             cut_len: int = 0,
                             drop_last: bool = False,
                             shuffle: bool = False,
                             random_cut: bool = True,
                             sampler: Optional[Type[Sampler]] = None,
                             pin_memory: bool = False) -> AawareDataLoader:
    """Generates a PyTorch dataloader from a SonusAI mixture database
    """
    dataset = MixtureDatabaseDataset(mixdb=mixdb,
                                     mixids=mixids,
                                     cut_len=cut_len,
                                     flatten=flatten,
                                     add1ch=add1ch,
                                     random_cut=random_cut)

    if sampler is not None:
        my_sampler = sampler(dataset)
    else:
        my_sampler = None

    result = AawareDataLoader(dataset=dataset,
                              batch_size=batch_size,
                              pin_memory=pin_memory,
                              shuffle=shuffle,
                              sampler=my_sampler,
                              drop_last=drop_last,
                              num_workers=num_workers)

    result.cut_len = cut_len

    return result
