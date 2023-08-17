import openai
from opaw.model.bot import Bot
from opaw import util


class EditBot(Bot):
    """
    Deprecated model

    https://platform.openai.com/docs/api-reference/edits
    """

    def __init__(self, model=util.default_models["edit"]):
        """
        Deprecated model
        """
        super().__init__(model, "edit")

    def create(self, input, **kargs):
        """
        Deprecated model
        """
        if input is None:
            return None

        request = {
            "model": self.model,
            "input": input,
            **kargs
        }

        self._history_req(request)
        response = openai.Edit.create(**request)
        self._history_res(response)
        return response

    def grab(self, response):
        """
        :return: response's text
        """
        return response["choices"][0]["text"]
