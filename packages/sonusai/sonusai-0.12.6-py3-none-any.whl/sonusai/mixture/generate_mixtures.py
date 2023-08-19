from typing import List
from typing import Tuple

from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import Augmentations
from sonusai.mixture.types import AugmentedTargets
from sonusai.mixture.types import NoiseFiles


def generate_mixtures(mixdb: MixtureDatabase,
                      augmented_targets: AugmentedTargets,
                      noise_files: NoiseFiles,
                      noise_augmentations: Augmentations,
                      mixups: List[int]) -> Tuple[int, int]:
    """Generate mixtures and append to mixture database

    :param mixdb: Mixture database
    :param augmented_targets: List of augmented targets
    :param noise_files: List of noise files
    :param noise_augmentations: List of noise augmentations
    :param mixups: List of mixup values
    :return: (Number of noise files used, number of noise samples used)
    """
    from sonusai import SonusAIError

    if mixdb.noise_mix_mode == 'exhaustive':
        return _exhaustive_noise_mix(mixdb=mixdb,
                                     augmented_targets=augmented_targets,
                                     noise_files=noise_files,
                                     noise_augmentations=noise_augmentations,
                                     mixups=mixups)

    if mixdb.noise_mix_mode == 'non-exhaustive':
        return _non_exhaustive_noise_mix(mixdb=mixdb,
                                         augmented_targets=augmented_targets,
                                         mixups=mixups)

    if mixdb.noise_mix_mode == 'non-combinatorial':
        return _non_combinatorial_noise_mix(mixdb=mixdb,
                                            augmented_targets=augmented_targets,
                                            mixups=mixups)

    raise SonusAIError(f'invalid noise_mix_mode: {mixdb.noise_mix_mode}')


def _exhaustive_noise_mix(mixdb: MixtureDatabase,
                          augmented_targets: AugmentedTargets,
                          noise_files: NoiseFiles,
                          noise_augmentations: Augmentations,
                          mixups: List[int]) -> Tuple[int, int]:
    """Exhaustive noise mix mode
    Use every noise/augmentation with every target/augmentation.

    :param mixdb: Mixture database
    :param augmented_targets: List of augmented targets
    :param noise_files: List of noise files
    :param noise_augmentations: List of noise augmentations
    :param mixups: List of mixup values
    :return: (Number of noise files used, number of noise samples used)
    """
    from random import randint

    import numpy as np

    from sonusai.mixture import MRecord
    from sonusai.mixture import get_augmented_target_indices_for_mixup

    used_noise_files = len(noise_files) * len(noise_augmentations)
    used_noise_samples = 0

    augmented_target_indices_for_mixups = [get_augmented_target_indices_for_mixup(mixdb=mixdb,
                                                                                  augmented_targets=augmented_targets,
                                                                                  mixup=mixup) for mixup in mixups]
    for noise_file_index in range(len(noise_files)):
        for noise_augmentation_index in range(len(noise_augmentations)):
            noise_offset = 0
            noise_length = mixdb.augmented_noise_length(noise_file_index, noise_augmentation_index)

            for augmented_target_indices_for_mixup in augmented_target_indices_for_mixups:
                for augmented_target_indices in augmented_target_indices_for_mixup:
                    (target_file_index,
                     target_augmentation_index,
                     target_length) = _get_target_info(mixdb=mixdb,
                                                       augmented_target_indices=augmented_target_indices,
                                                       augmented_targets=augmented_targets)

                    for spectral_mask_index in range(len(mixdb.spectral_masks)):
                        for snr in mixdb.all_snrs:
                            mixdb.mixtures.append(MRecord(
                                name=None,
                                target_file_index=target_file_index,
                                target_augmentation_index=target_augmentation_index,
                                noise_file_index=noise_file_index,
                                noise_offset=noise_offset,
                                noise_augmentation_index=noise_augmentation_index,
                                samples=target_length,
                                snr=snr.value,
                                spectral_mask_index=spectral_mask_index,
                                spectral_mask_seed=randint(0, np.iinfo('i').max),
                                random_snr=snr.is_random))

                            noise_offset = int((noise_offset + target_length) % noise_length)
                            used_noise_samples += target_length

    return used_noise_files, used_noise_samples


def _non_exhaustive_noise_mix(mixdb: MixtureDatabase,
                              augmented_targets: AugmentedTargets,
                              mixups: List[int]) -> Tuple[int, int]:
    """Non-exhaustive noise mix mode
    Cycle through every target/augmentation without necessarily using all
    noise/augmentation combinations (reduced data set).

    :param mixdb: Mixture database
    :param augmented_targets: List of augmented targets
    :param mixups: List of mixup values
    :return: (Number of noise files used, number of noise samples used)
    """
    from random import randint

    import numpy as np

    from sonusai.mixture import MRecord
    from sonusai.mixture import get_augmented_target_indices_for_mixup

    used_noise_files = set()
    used_noise_samples = 0
    noise_offset = 0
    noise_file_index = 0
    noise_augmentation_index = 0

    augmented_target_indices_for_mixups = [get_augmented_target_indices_for_mixup(mixdb=mixdb,
                                                                                  augmented_targets=augmented_targets,
                                                                                  mixup=mixup) for mixup in mixups]
    for mixup in augmented_target_indices_for_mixups:
        for augmented_target_indices in mixup:
            (target_file_index,
             target_augmentation_index,
             target_length) = _get_target_info(mixdb=mixdb,
                                               augmented_target_indices=augmented_target_indices,
                                               augmented_targets=augmented_targets)

            for spectral_mask_index in range(len(mixdb.spectral_masks)):
                for snr in mixdb.all_snrs:
                    used_noise_files.add(f'{noise_file_index}_{noise_augmentation_index}')
                    (noise_file_index,
                     noise_augmentation_index,
                     noise_offset) = _get_next_noise_offset(mixdb=mixdb,
                                                            target_length=target_length,
                                                            noise_file_index=noise_file_index,
                                                            noise_augmentation_index=noise_augmentation_index,
                                                            noise_offset=noise_offset)

                    mixdb.mixtures.append(MRecord(
                        name=None,
                        target_file_index=target_file_index,
                        target_augmentation_index=target_augmentation_index,
                        noise_file_index=noise_file_index,
                        noise_augmentation_index=noise_augmentation_index,
                        noise_offset=noise_offset,
                        samples=target_length,
                        snr=snr.value,
                        spectral_mask_index=spectral_mask_index,
                        spectral_mask_seed=randint(0, np.iinfo('i').max),
                        random_snr=snr.is_random))

                    noise_offset += target_length
                    used_noise_samples += target_length

    return len(used_noise_files), used_noise_samples


def _non_combinatorial_noise_mix(mixdb: MixtureDatabase,
                                 augmented_targets: AugmentedTargets,
                                 mixups: List[int]) -> Tuple[int, int]:
    """Non-combinatorial noise mix mode
    Combine a target/augmentation with a single cut of a noise/augmentation
    non-exhaustively (each target/augmentation does not use each noise/augmentation).
    Cut has random start and loop back to beginning if end of noise/augmentation is reached.

    :param mixdb: Mixture database
    :param augmented_targets: List of augmented targets
    :param mixups: List of mixup values
    :return: (Number of noise files used, number of noise samples used)
    """
    from random import choice
    from random import randint

    import numpy as np

    from sonusai.mixture import MRecord
    from sonusai.mixture import get_augmented_target_indices_for_mixup

    used_noise_files = set()
    used_noise_samples = 0
    noise_file_index = 0
    noise_augmentation_index = 0

    augmented_target_indices_for_mixups = [get_augmented_target_indices_for_mixup(mixdb=mixdb,
                                                                                  augmented_targets=augmented_targets,
                                                                                  mixup=mixup) for mixup in mixups]
    for mixup in augmented_target_indices_for_mixups:
        for augmented_target_indices in mixup:
            (target_file_index,
             target_augmentation_index,
             target_length) = _get_target_info(mixdb=mixdb,
                                               augmented_target_indices=augmented_target_indices,
                                               augmented_targets=augmented_targets)

            for spectral_mask_index in range(len(mixdb.spectral_masks)):
                for snr in mixdb.all_snrs:
                    used_noise_files.add(f'{noise_file_index}_{noise_augmentation_index}')
                    (noise_file_index,
                     noise_augmentation_index,
                     noise_length) = _get_next_noise_indices(mixdb=mixdb,
                                                             noise_file_index=noise_file_index,
                                                             noise_augmentation_index=noise_augmentation_index)

                    mixdb.mixtures.append(MRecord(
                        name=None,
                        target_file_index=target_file_index,
                        target_augmentation_index=target_augmentation_index,
                        noise_file_index=noise_file_index,
                        noise_augmentation_index=noise_augmentation_index,
                        noise_offset=choice(range(noise_length)),
                        samples=target_length,
                        snr=snr.value,
                        spectral_mask_index=spectral_mask_index,
                        spectral_mask_seed=randint(0, np.iinfo('i').max),
                        random_snr=snr.is_random))

                    used_noise_samples += target_length

    return len(used_noise_files), used_noise_samples


def _get_next_noise_indices(mixdb: MixtureDatabase,
                            noise_file_index: int,
                            noise_augmentation_index: int) -> Tuple[int, int, int]:
    noise_augmentation_index += 1
    if noise_augmentation_index == len(mixdb.noise_augmentations):
        noise_augmentation_index = 0
        noise_file_index += 1
        if noise_file_index == len(mixdb.noises):
            noise_file_index = 0

    return (noise_file_index,
            noise_augmentation_index,
            mixdb.augmented_noise_length(noise_file_index, noise_augmentation_index))


def _get_next_noise_offset(mixdb: MixtureDatabase,
                           target_length: int,
                           noise_file_index: int,
                           noise_augmentation_index: int,
                           noise_offset: int) -> Tuple[int, int, int]:
    from sonusai import SonusAIError

    if noise_offset + target_length >= mixdb.augmented_noise_length(noise_file_index, noise_augmentation_index):
        if noise_offset == 0:
            raise SonusAIError('Length of target audio exceeds length of noise audio')

        noise_offset = 0
        noise_augmentation_index += 1
        if noise_augmentation_index == len(mixdb.noise_augmentations):
            noise_augmentation_index = 0
            noise_file_index += 1
            if noise_file_index == len(mixdb.noises):
                noise_file_index = 0

    return noise_file_index, noise_augmentation_index, noise_offset


def _get_target_info(mixdb: MixtureDatabase,
                     augmented_target_indices: List[int],
                     augmented_targets: AugmentedTargets) -> Tuple[List[int], List[int], int]:
    from sonusai.mixture import estimate_augmented_length_from_length

    target_file_index = []
    target_augmentation_index = []
    target_length = 0
    for idx in augmented_target_indices:
        tfi = augmented_targets[idx].target_file_index
        tai = augmented_targets[idx].target_augmentation_index

        target_file_index.append(tfi)
        target_augmentation_index.append(tai)

        target_length = max(estimate_augmented_length_from_length(length=mixdb.targets[tfi].samples,
                                                                  augmentation=mixdb.target_augmentations[tai],
                                                                  length_common_denominator=mixdb.feature_step_samples),
                            target_length)
    return target_file_index, target_augmentation_index, target_length
