import openai
from opaw.model.bot import Bot
from opaw import util

class EmbeddingBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/embeddings
    """
    def __init__(self, model=util.default_models["embedding"]):
        super().__init__(model, "embedding")

    def create(self, input, **kargs):
        if input is None:
            return None

        request = {
            "model": self.model,
            "input": input,
            **kargs
        }

        self._history_req(request)
        response = openai.Embedding.create(**request)
        self._history_res(response)
        return response

    def grab(self, response):
        """
        :return: response's embeddings
        """
        return response["data"][0]["embedding"]
