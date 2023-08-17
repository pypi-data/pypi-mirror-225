from sonusai.utils import ASRResult
from sonusai.utils.asr_functions.data import Data


def google(data: Data) -> ASRResult:
    import tempfile
    from os import getenv
    from os.path import join

    import speech_recognition as sr

    from sonusai import SonusAIError
    from sonusai.utils import ASRResult
    from sonusai.utils import float_to_int16
    from sonusai.utils import write_wav

    key = getenv('GOOGLE_SPEECH_API_KEY')
    if key is None:
        raise SonusAIError('GOOGLE_SPEECH_API_KEY environment variable does not exist')

    r = sr.Recognizer()
    with tempfile.TemporaryDirectory() as tmp:
        file = join(tmp, 'asr.wav')
        write_wav(name=file, audio=float_to_int16(data.audio))

        with sr.AudioFile(file) as source:
            audio = r.record(source)

        try:
            results = r.recognize_google(audio, key=key, show_all=True)
            if not isinstance(results, dict) or len(results.get('alternative', [])) == 0:
                raise SonusAIError('speech_recognition: UnknownValueError')

            if 'confidence' in results['alternative']:
                # return alternative with highest confidence score
                best_hypothesis = max(results['alternative'], key=lambda alternative: alternative['confidence'])
            else:
                # when there is no confidence available, we arbitrarily choose the first hypothesis.
                best_hypothesis = results['alternative'][0]
            if "transcript" not in best_hypothesis:
                raise SonusAIError('speech_recognition: UnknownValueError')
            confidence = best_hypothesis.get('confidence', 0.5)
            return ASRResult(text=best_hypothesis['transcript'], confidence=confidence)
        except sr.UnknownValueError:
            return ASRResult(text='', confidence=0)
        except sr.RequestError as e:
            raise SonusAIError(f'Could not request results from Google Speech Recognition service: {e}')


"""
Google results:
{
  "result": [
    {
      "alternative": [
        {
          "transcript": "the Birch canoe slid on the smooth planks",
          "confidence": 0.94228178
        },
        {
          "transcript": "the Burj canoe slid on the smooth planks"
        },
        {
          "transcript": "the Birch canoe slid on the smooth plank"
        },
        {
          "transcript": "the Birch canoe slit on the smooth planks"
        },
        {
          "transcript": "the Birch canoes slid on the smooth planks"
        }
      ],
      "final": true
    }
  ],
  "result_index": 0
}
"""
