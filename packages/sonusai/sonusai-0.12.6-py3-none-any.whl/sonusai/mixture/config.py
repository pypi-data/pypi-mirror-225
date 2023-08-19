from typing import Dict
from typing import List
from typing import Union

from sonusai.mixture.types import ImpulseResponseFiles
from sonusai.mixture.types import Location
from sonusai.mixture.types import NoiseFiles
from sonusai.mixture.types import SpectralMasks
from sonusai.mixture.types import TargetFiles


def raw_load_config(name: Location) -> Dict:
    """Load YAML config file

    :param name: File name
    :return: Dictionary of config data
    """
    import yaml

    with open(file=name, mode='r') as f:
        config = yaml.safe_load(f)

    return config


def get_default_config() -> Dict:
    """Load default SonusAI config

    :return: Dictionary of default config data
    """
    from sonusai import SonusAIError
    from sonusai.mixture import DEFAULT_CONFIG

    try:
        return raw_load_config(DEFAULT_CONFIG)
    except Exception as e:
        raise SonusAIError(f'Error loading default config: {e}')


def load_config(name: Location) -> Dict:
    """Load SonusAI default config and update with given location (performing SonusAI variable substitution)

    :param name: Directory containing mixture database
    :return: Dictionary of config data
    """
    from os.path import join

    return update_config_from_file(name=join(name, 'config.yml'), config=get_default_config())


def update_config_from_file(name: Location, config: Dict) -> Dict:
    """Update the given config with the config in the YAML file

    :param name: File name
    :param config: Config dictionary to update
    :return: Updated config dictionary
    """
    from copy import deepcopy

    from sonusai import SonusAIError
    from sonusai.mixture import REQUIRED_CONFIGS
    from sonusai.mixture import VALID_CONFIGS
    from sonusai.mixture import VALID_NOISE_MIX_MODES

    updated_config = deepcopy(config)

    try:
        new_config = raw_load_config(name)
    except Exception as e:
        raise SonusAIError(f'Error loading config from {name}: {e}')

    # Check for unrecognized keys
    for key in new_config:
        if key not in VALID_CONFIGS:
            nice_list = '\n'.join([f'  {item}' for item in VALID_CONFIGS])
            raise SonusAIError(f'Invalid config parameter in {name}: {key}.\n'
                               f'Valid config parameters are:\n{nice_list}')

    # Use default config as base and overwrite with given config keys as found
    for key in updated_config:
        if key in new_config:
            if key not in ['truth_settings']:
                updated_config[key] = new_config[key]

    # Handle 'truth_settings' special case
    if 'truth_settings' in new_config:
        updated_config['truth_settings'] = deepcopy(new_config['truth_settings'])

    if not isinstance(updated_config['truth_settings'], list):
        updated_config['truth_settings'] = [updated_config['truth_settings']]

    default = deepcopy(config['truth_settings'])
    if not isinstance(default, list):
        default = [default]

    updated_config['truth_settings'] = update_truth_settings(updated_config['truth_settings'], default)

    # Check for required keys
    for key in REQUIRED_CONFIGS:
        if key not in updated_config:
            raise SonusAIError(f'Missing required config in {name}: {key}')

    # Check for non-empty spectral masks
    if len(updated_config['spectral_masks']) == 0:
        updated_config['spectral_masks'] = config['spectral_masks']

    # Check for valid noise_mix_mode
    if updated_config['noise_mix_mode'] not in VALID_NOISE_MIX_MODES:
        nice_list = '\n'.join([f'  {item}' for item in VALID_NOISE_MIX_MODES])
        raise SonusAIError(f'Invalid noise_mix_mode in {name}.\n'
                           f'Valid noise mix modes are:\n{nice_list}')

    return updated_config


def update_truth_settings(given: Union[List[Dict], Dict], default: List[Dict] = None) -> List[Dict]:
    """Update missing fields in given 'truth_settings' with default values

    :param given: The dictionary of given truth settings
    :param default: The dictionary of default truth settings
    :return: Updated dictionary of truth settings
    """
    from copy import deepcopy

    from sonusai import SonusAIError
    from sonusai.mixture import VALID_TRUTH_SETTINGS

    if isinstance(given, list):
        truth_settings = deepcopy(given)
    else:
        truth_settings = [deepcopy(given)]

    if default is not None and len(truth_settings) != len(default):
        raise SonusAIError(f'Length of given does not match default')

    for n in range(len(truth_settings)):
        for key in truth_settings[n]:
            if key not in VALID_TRUTH_SETTINGS:
                nice_list = '\n'.join([f'  {item}' for item in VALID_TRUTH_SETTINGS])
                raise SonusAIError(f'Invalid truth_settings: {key}.\nValid truth_settings are:\n{nice_list}')

        for key in VALID_TRUTH_SETTINGS:
            if key not in truth_settings[n]:
                if default is not None and key in default[n]:
                    truth_settings[n][key] = default[n][key]
                else:
                    raise SonusAIError(f'Missing required truth_settings: {key}')

    for truth_setting in truth_settings:
        if not isinstance(truth_setting['index'], list):
            truth_setting['index'] = [truth_setting['index']]

    return truth_settings


def get_hierarchical_config_files(root: str, leaf: str) -> List[Location]:
    """Get a hierarchical list of config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :return: List of config files found in the hierarchy
    """
    import os
    from pathlib import Path

    from sonusai import SonusAIError

    config_file = 'config.yml'

    root_path = Path(os.path.abspath(root))
    if not root_path.is_dir():
        raise SonusAIError(f'Given root, {root_path}, is not a directory.')

    leaf_path = Path(os.path.abspath(leaf))
    if not leaf_path.is_dir():
        raise SonusAIError(f'Given leaf, {leaf_path}, is not a directory.')

    common = os.path.commonpath((root_path, leaf_path))
    if os.path.normpath(common) != os.path.normpath(root_path):
        raise SonusAIError(f'Given leaf, {leaf_path}, is not in the hierarchy of the given root, {root_path}')

    top_config_file = os.path.join(root_path, config_file)
    if not Path(top_config_file).is_file():
        raise SonusAIError(f'Could not find {top_config_file}')

    current = leaf_path
    config_files = []
    while current != root_path:
        local_config_file = Path(os.path.join(current, config_file))
        if local_config_file.is_file():
            config_files.append(str(local_config_file))
        current = current.parent

    config_files.append(top_config_file)
    return list(reversed(config_files))


def update_config_from_hierarchy(root: str, leaf: str, config: dict) -> dict:
    """Update the given config using the hierarchical config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :param config: Config to update
    :return: Updated config
    """
    from copy import deepcopy

    new_config = deepcopy(config)
    config_files = get_hierarchical_config_files(root=root, leaf=leaf)
    for config_file in config_files:
        new_config = update_config_from_file(name=config_file, config=new_config)

    return new_config


def get_max_class(num_classes: int, truth_mutex: bool) -> int:
    """Get the maximum class index

    :param num_classes: Number of classes
    :param truth_mutex: Truth is mutex mode
    :return: Highest class index
    """
    max_class = num_classes
    if truth_mutex:
        max_class -= 1
    return max_class


def get_target_files(config: dict, show_progress: bool = False) -> TargetFiles:
    """Get the list of target files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of target files
    """
    from itertools import chain

    from tqdm import tqdm

    from sonusai import SonusAIError
    from sonusai.mixture import TargetFiles
    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import p_tqdm_map

    truth_settings = config.get('truth_settings', list())
    target_level_type = config.get('target_level_type', None)
    target_files = list(chain.from_iterable([_append_target_files(target_file=target,
                                                                  truth_settings=truth_settings,
                                                                  target_level_type=target_level_type)
                                             for target in config['targets']]))

    progress = tqdm(total=len(target_files), disable=not show_progress)
    target_files = p_tqdm_map(_get_samples, target_files, progress=progress)
    progress.close()

    max_class = get_max_class(config['num_classes'], config['truth_mode'] == 'mutex')

    for target_file in target_files:
        target_file['truth_settings'] = update_truth_settings(target_file['truth_settings'], config['truth_settings'])

        for truth_setting in target_file['truth_settings']:
            if any(idx > max_class for idx in truth_setting['index']):
                raise SonusAIError('invalid truth index')

    return dataclass_from_dict(TargetFiles, target_files)


def _append_target_files(target_file: Union[dict, str],
                         truth_settings: List[dict],
                         target_level_type: str,
                         tokens: dict = None) -> List[dict]:
    """Process target files list and append as needed

    :param target_file: Target file entry to append to the list
    :param truth_settings: Truth settings
    :param target_level_type: Target level type
    :param tokens: Tokens used for variable expansion
    :return: List of target files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from sonusai import SonusAIError
    from sonusai.mixture import tokenized_expand
    from sonusai.mixture import tokenized_replace
    from sonusai.mixture import validate_input_file

    if tokens is None:
        tokens = {}

    if isinstance(target_file, dict):
        if 'name' in target_file:
            in_name = target_file['name']
        else:
            raise SonusAIError('Target list contained record without name')

        if 'truth_settings' in target_file:
            truth_settings = target_file['truth_settings']
        if 'target_level_type' in target_file:
            target_level_type = target_file['target_level_type']
    else:
        in_name = target_file

    in_name, new_tokens = tokenized_expand(in_name)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')

    target_files: List[dict] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                target_files.extend(_append_target_files(target_file=child,
                                                         truth_settings=truth_settings,
                                                         target_level_type=target_level_type,
                                                         tokens=tokens))
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                target_files.extend(_append_target_files(target_file=child,
                                                                         truth_settings=truth_settings,
                                                                         target_level_type=target_level_type,
                                                                         tokens=tokens))
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'targets' in yml_config:
                            for record in yml_config['targets']:
                                target_files.extend(_append_target_files(target_file=record,
                                                                         truth_settings=truth_settings,
                                                                         target_level_type=target_level_type,
                                                                         tokens=tokens))
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    validate_input_file(name)
                    entry: dict = {
                        'expanded_name': name,
                        'name':          tokenized_replace(name, tokens),
                    }
                    if len(truth_settings) > 0:
                        entry['truth_settings'] = truth_settings
                        for truth_setting in entry['truth_settings']:
                            if 'function' in truth_setting and truth_setting['function'] == 'file':
                                truth_setting['config']['file'] = splitext(entry['name'])[0] + '.h5'
                    if target_level_type is not None:
                        entry['target_level_type'] = target_level_type
                    target_files.append(entry)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')

    return target_files


def get_noise_files(config: dict, show_progress: bool = False) -> NoiseFiles:
    """Get the list of noise files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of noise file
    """
    from itertools import chain

    from tqdm import tqdm

    from sonusai.mixture import NoiseFiles
    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import p_tqdm_map

    noise_files = list(chain.from_iterable([_append_noise_files(noise_file=noise) for noise in config['noises']]))

    progress = tqdm(total=len(noise_files), disable=not show_progress)
    noise_files = p_tqdm_map(_get_samples, noise_files, progress=progress)
    progress.close()

    return dataclass_from_dict(NoiseFiles, noise_files)


def _append_noise_files(noise_file: Union[dict, str], tokens: dict = None) -> List[dict]:
    """Process noise files list and append as needed

    :param noise_file: Noise file entry to append to the list
    :param tokens: Tokens used for variable expansion
    :return: List of noise files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from sonusai import SonusAIError
    from sonusai.mixture import tokenized_expand
    from sonusai.mixture import tokenized_replace
    from sonusai.mixture import validate_input_file

    if tokens is None:
        tokens = {}

    if isinstance(noise_file, dict):
        if 'name' in noise_file:
            in_name = noise_file['name']
        else:
            raise SonusAIError('Noise list contained record without name')
    else:
        in_name = noise_file

    in_name, new_tokens = tokenized_expand(in_name)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')

    noise_files: List[dict] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                noise_files.extend(_append_noise_files(noise_file=child, tokens=tokens))
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                noise_files.extend(_append_noise_files(noise_file=child, tokens=tokens))
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'noises' in yml_config:
                            for record in yml_config['noises']:
                                noise_files.extend(_append_noise_files(noise_file=record, tokens=tokens))
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    validate_input_file(name)
                    entry: dict = {
                        'expanded_name': name,
                        'name':          tokenized_replace(name, tokens),
                    }
                    noise_files.append(entry)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')

    return noise_files


def get_ir_files(config: dict, show_progress: bool = False) -> ImpulseResponseFiles:
    """Get the list of impulse response files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of impulse response files
    """
    from itertools import chain

    return list(chain.from_iterable([_append_ir_files(ir_file=ir) for ir in config['impulse_responses']]))


def _append_ir_files(ir_file: Location,
                     tokens: dict = None) -> List[Location]:
    """Process impulse response files list and append as needed

    :param ir_file: Impulse response file entry to append to the list
    :param tokens: Tokens used for variable expansion
    :return: List of impulse response files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from sonusai import SonusAIError
    from sonusai.mixture import tokenized_expand
    from sonusai.mixture import tokenized_replace
    from sonusai.mixture import validate_input_file

    if tokens is None:
        tokens = {}

    in_name, new_tokens = tokenized_expand(ir_file)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')

    ir_files: List[Location] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                ir_files.extend(_append_ir_files(ir_file=child, tokens=tokens))
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                ir_files.extend(_append_ir_files(ir_file=child, tokens=tokens))
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'impulse_responses' in yml_config:
                            for record in yml_config['impulse_responses']:
                                ir_files.extend(_append_ir_files(ir_file=record, tokens=tokens))
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    validate_input_file(name)
                    ir_files.append(tokenized_replace(name, tokens))
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')

    return ir_files


def get_class_weights_threshold(config: Dict) -> List[float]:
    """Get the class_weights_threshold from a config

    :param config: Config dictionary
    :return: class_weights_threshold
    """
    from sonusai import SonusAIError

    class_weights_threshold = config['class_weights_threshold']
    num_classes = config['num_classes']

    if not isinstance(class_weights_threshold, list):
        class_weights_threshold = [class_weights_threshold]

    if len(class_weights_threshold) == 1:
        class_weights_threshold = [class_weights_threshold[0]] * num_classes

    if len(class_weights_threshold) != num_classes:
        raise SonusAIError(f'invalid class_weights_threshold length: {len(class_weights_threshold)}')

    return class_weights_threshold


def generate_mixture_filename(mixid: int, width: int) -> str:
    """Generate a zero-padded mixture file name

    :param mixid: Mixture ID
    :param width: Width of mixid
    :return: Zero-padded mixture file name
    """
    return f'{mixid:0{width}}.h5'


def generate_coefficients_filename(idx: int, width: int) -> str:
    """Generate a zero-padded coefficients file name

    :param idx: IR index
    :param width: Width of idx
    :return: Zero-padded coefficients file name
    """
    return f'ir_{idx:0{width}}.txt'


def get_spectral_masks(config: dict) -> SpectralMasks:
    """Get the list of spectral masks from a config

    :param config: Config dictionary
    :return: List of spectral masks
    """
    from sonusai import SonusAIError
    from sonusai.mixture import SpectralMasks
    from sonusai.utils import dataclass_from_dict

    try:
        return dataclass_from_dict(SpectralMasks, config['spectral_masks'])
    except Exception as e:
        raise SonusAIError(f'Error in spectral_masks: {e}')


def _get_samples(entry: dict) -> dict:
    from sonusai.mixture import read_audio

    entry['samples'] = len(read_audio(entry['expanded_name']))
    del entry['expanded_name']
    return entry
