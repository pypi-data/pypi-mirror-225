import re
from importlib import resources

REQUIRED_CONFIGS = [
    'asr_manifest',
    'class_balancing',
    'class_balancing_augmentation',
    'class_labels',
    'class_weights_threshold',
    'feature',
    'impulse_responses',
    'noise_augmentations',
    'noise_mix_mode',
    'noises',
    'num_classes',
    'random_snrs',
    'seed',
    'snrs',
    'spectral_masks',
    'target_augmentations',
    'target_level_type',
    'targets',
    'truth_mode',
    'truth_reduction_function',
    'truth_settings',
]
OPTIONAL_CONFIGS = [
    'output',
]
VALID_CONFIGS = REQUIRED_CONFIGS + OPTIONAL_CONFIGS
VALID_TRUTH_SETTINGS = ['function', 'config', 'index']
VALID_AUGMENTATIONS = ['normalize', 'gain', 'pitch', 'tempo', 'eq1', 'eq2', 'eq3', 'lpf', 'ir', 'count', 'mixup']
VALID_NOISE_MIX_MODES = ['exhaustive', 'non-exhaustive', 'non-combinatorial']
RAND_PATTERN = re.compile(r'rand\(([-+]?(\d+(\.\d*)?|\.\d+)),\s*([-+]?(\d+(\.\d*)?|\.\d+))\)')
SAMPLE_RATE = 16000
BIT_DEPTH = 32
ENCODING = 'floating-point'
CHANNEL_COUNT = 1
SAMPLE_BYTES = BIT_DEPTH // 8
FLOAT_BYTES = 4

with resources.path('sonusai.data', 'whitenoise.wav') as path:
    DEFAULT_NOISE = str(path)

with resources.path('sonusai.data', 'genmixdb.yml') as path:
    DEFAULT_CONFIG = str(path)

with resources.path('sonusai.data', 'speech_ma01_01.wav') as path:
    DEFAULT_SPEECH = str(path)
