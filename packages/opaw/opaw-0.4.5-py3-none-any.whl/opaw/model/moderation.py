import openai
from opaw.model.bot import Bot
from opaw import util


class ModerationBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/moderations
    """

    def __init__(self, model=util.default_models["moderation"]):
        super().__init__(model, "moderation")

    def create(self, input, **kargs):
        if input is None:
            return None

        request = {
            "model": self.model,
            "input": input,
            **kargs
        }

        self._history_req(request)
        response = openai.Moderation.create(**request)
        self._history_res(response)
        return response

    def grab(self, response):
        """
        :return: a dict containing flagged categories and scores (e.g. {"violence": 0.523, "sexual": 0.833})
        """
        result = response["results"][0]
        categories = result["categories"]
        scores = result["category_scores"]
        return {flag: scores[flag] for flag, value in categories.items() if value}
