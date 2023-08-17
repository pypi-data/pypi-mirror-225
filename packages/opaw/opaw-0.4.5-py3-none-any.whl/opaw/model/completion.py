import openai
from opaw.model.bot import Bot
from opaw import util

class CompletionBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/completions
    """
    def __init__(self, model=util.default_models["completion"]):
        super().__init__(model, "completion")

    def create(self, prompt, **kargs):
        if prompt is None:
            return None

        request = {
            "model": self.model,
            "prompt": prompt,
            **kargs
        }

        self._history_req(request)
        response = openai.Completion.create(**request)
        self._history_res(response)
        return response

    def grab(self, response):
        """
        :return: response's text
        """
        return response["choices"][0]["text"]