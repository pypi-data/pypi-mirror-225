from sonusai.utils import ASRResult
from sonusai.utils.asr_functions.data import Data


def whisper(data: Data) -> ASRResult:
    from whisper import load_model

    whisper_model = data.whisper_model
    if whisper_model is None:
        whisper_model = load_model(data.whisper_model_name, device=data.device)

    return ASRResult(text=whisper_model.transcribe(data.audio, fp16=False)['text'])


"""
Whisper results:
{
  'text': ' The birch canoe slid on the smooth planks.',
  'segments': [
    {
      'id': 0,
      'seek': 0,
      'start': 0.0,
      'end': 2.4,
      'text': ' The birch canoe slid on the smooth planks.',
      'tokens': [
        50363,
        383,
        35122,
        354,
        47434,
        27803,
        319,
        262,
        7209,
        1410,
        591,
        13,
        50483
      ],
      'temperature': 0.0,
      'avg_logprob': -0.4188103675842285,
      'compression_ratio': 0.8571428571428571,
      'no_speech_prob': 0.003438911633566022
    }
  ],
  'language': 'en'
}
"""
