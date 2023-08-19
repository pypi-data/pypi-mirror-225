from sonusai.utils import ASRResult
from sonusai.utils.asr_functions.data import Data


def aixplain_whisper(data: Data) -> ASRResult:
    import tempfile
    from os import getenv
    from os.path import join

    from aixplain.factories.model_factory import ModelFactory

    from sonusai import SonusAIError
    from sonusai.utils import ASRResult
    from sonusai.utils import float_to_int16
    from sonusai.utils import write_wav

    whisper_model = data.whisper_model
    if whisper_model is None:
        envvar = 'AIXP_WHISPER_' + data.whisper_model_name.upper()
        modelkey = getenv(envvar)
        if modelkey is None:
            raise SonusAIError(f'{envvar} environment variable does not exist')

        whisper_model = ModelFactory.create_asset_from_id(modelkey)

    with tempfile.TemporaryDirectory() as tmp:
        file = join(tmp, 'asr.wav')
        write_wav(name=file, audio=float_to_int16(data.audio))

        retry = 5
        count = 0
        while True:
            try:
                results = whisper_model.run(file)
                return ASRResult(text=results['data'], confidence=results['confidence'])
            except Exception as e:
                count += 1
                print(f'Warning: aiXplain exception: {e}')
                if count >= retry:
                    raise SonusAIError(f'Whisper exception: {e.args}')


"""
aiXplain Whisper results:
{
  'completed': True,
  'data': 'The birch canoe slid on the smooth planks.',
  'usedCredits': 3.194770833333333e-05,
  'runTime': 114.029,
  'confidence': None,
  'details': [],
  'rawData': {
    'predictions': [
      ' The birch canoe slid on the smooth planks.'
    ]
  },
  'status': 'SUCCESS'
}
"""
