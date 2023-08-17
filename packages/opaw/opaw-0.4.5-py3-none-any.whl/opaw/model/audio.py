import whisper
import whisper_timestamped as whisper_t
import openai
from opaw.model.bot import Bot
from opaw import util


class AudioBot(Bot):
    """
    - official api doc: https://platform.openai.com/docs/api-reference/audio
    - whisper github: https://github.com/openai/whisper
    - whisper_timestamped github: https://github.com/linto-ai/whisper-timestamped
    """

    def __init__(self, model=util.default_models["audio"], ):
        super().__init__(model, "audio")

    def create(self, file, **kargs):
        """
        returns response using selected library
        :param file: audio file path (mp3, mp4, mpeg, mpga, m4a, wav, or webm)
        :param kargs: params for each library (lib: "api"(official api doc) or "whisper"(whisper) or "whisper_t"(whisper_timestamped))
        """
        lib = kargs.pop("lib", "api")

        if lib == "api":
            response = self._create_api(file, **kargs)
        elif lib == "whisper":
            response = self._create_whisper(file, **kargs)
        elif lib == "whisper_t":
            response = self._create_whisper_t(file, **kargs)
        else:
            return None

        # save response to history at once for all libraries
        self._history_res(response)
        return response

    def _create_api(self, file, **kargs):
        """
        In kargs, you can specify the following parameters:
        - select task "stt(transcript)" or "mt(translation)"
        - language (stt): https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        - params that each library supports

        :param file: audio file path
        :param kargs: params for each library
        """
        if file is None or "task" not in kargs:
            return None

        model = openai.Audio
        methods = {
            "transcript": model.transcribe,
            "stt": model.transcribe,
            "translation": model.translate,
            "mt": model.translate,
        }

        # remove task from request
        task = kargs.pop('task')
        if task not in methods:
            return None

        request = {"model": self.model, "file": file, **kargs}
        self._history_req(request)
        request["file"] = open(file, "rb")
        response = methods[task](**request)
        return response

    def _create_whisper(self, file, **kargs):
        request = {"file": file, **kargs}
        self._history_req(request)

        # whisper.load_model function args
        model = whisper.load_model(**util.pop_func_args(whisper.load_model, kargs))

        # model.transcribe function args
        return model.transcribe(file, **util.pop_func_args(model.transcribe, kargs))

    def _create_whisper_t(self, file, **kargs):
        request = {"file": file, **kargs}
        self._history_req(request)

        # whisper_t.load_audio function args
        audio = whisper_t.load_audio(file, **util.pop_func_args(whisper_t.load_audio, kargs))

        # whisper_t.load_model function args
        model = whisper_t.load_model(**util.pop_func_args(whisper_t.load_model, kargs))

        # whisper_t.transcribe function args
        return whisper_t.transcribe(model, audio, **util.pop_func_args(whisper_t.transcribe, kargs))

    def grab(self, response):
        """
        :return: response's text
        """
        return response["text"]  # all libraries have "text" key
