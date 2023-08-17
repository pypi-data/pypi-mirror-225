import openai
from opaw.model.bot import Bot
from opaw import util


class FileBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/files
    """

    def __init__(self):
        super().__init__("bot", "file")

    def create(self, _=None, **kargs):
        """
        :param _: is not used (use kargs instead)
        """
        if "task" not in kargs:
            return None

        model = openai.File
        methods = {
            "list": model.list,
            "upload": model.create,  # file
            "delete": model.delete,  # sid
            "retrieve": model.retrieve,  # id
            "download": model.download,  # id
        }

        task = kargs.pop('task')
        if task not in methods:
            return None

        request = {
            **kargs
        }
        self._history_req(request)

        if task == "upload":
            request["file"] = open(request["file"], "rb")
        response = methods[task](**request)

        if task == "download":
            # convert byte (b"") response to
            self._history_res(response.decode("utf-8"))
        else:
            self._history_res(response)

        return response

    def grab(self, response):
        """
        :return: original response
        """
        return response
