import base64
import requests
from urllib.parse import urlparse
import openai
from opaw.model.bot import Bot
from opaw import util


class ImageBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/images
    """

    def __init__(self, model=util.default_models["image"]):
        super().__init__(model, "image")

    def create(self, prompt, **kargs):
        """
        :kargs: select task "create" or "edit" or "variation"
        """
        if prompt is None or "task" not in kargs:
            return None

        model = openai.Image
        methods = {
            "create": model.create,
            "edit": model.create_edit,
            "variation": model.create_variation
        }

        task = kargs.pop('task')
        if task not in methods:
            return None

        request = {
            "prompt": prompt,
            **kargs
        }

        if task == "variation":  # remove prompt when variation
            request.pop("prompt")

        self._history_req(request)

        response = methods[task](**request)
        self._history_res(response)
        return response

    def save_img(self, response, path):
        """
        saves given image to the path
        :param response: the response from create()
        :param path: the path to be saved
        """
        util.mkdirs(path)  # create parent dirs
        data = self.grab(response)
        d_format = self.img_format(data)

        if d_format == "url":
            data = requests.get(data)
            with open(path, "wb") as f:
                f.write(data.content)
        elif d_format == "uri":
            with open(path, "wb") as f:
                f.write(base64.b64decode(data))

    def img_format(self, data):
        """
       img could be url or data scheme encoded in base64
       """
        parsed = urlparse(data)
        return "url" if parsed.scheme and parsed.netloc else "uri"

    def grab(self, response):
        """
        :return: url or uri(data scheme) of the response
        """
        res = response['data'][0]
        return res['url'] if 'url' in res else res['b64_json']
