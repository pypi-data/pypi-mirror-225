import io
from datetime import datetime
from opaw import util
import json
import os
import time
import copy
import math


class Bot:
    """
    https://platform.openai.com/docs/api-reference/introduction
    """

    def __init__(self, model, type="bot"):
        self.model = model
        # chat, completion, image, audio, embedding, file, finetune, moderation, edit
        self.type = type
        self.history = []

    def create(self, prompt, **kargs):
        """
        Send prompt to the bot and gets a result
        :param prompt: the prompt to send
        :param kargs: other args
        :return: response from the bot
        """
        pass

    def _history_req(self, request):
        """
        history user's request
        """
        if request:
            self.history.append(copy.deepcopy(request))


    def _history_res(self, response):
        """
        history response of the bot
        """
        if response:
            self.history.append(copy.deepcopy(response))

    def save_history(self, file):
        """
        saves history in the given file or directory
        :param file: the history file name (parent dirs will be created automatically)
        """

        # save with date format if dir is given
        if os.path.isdir(file):
            now = datetime.now().strftime("%Y%m%dT%H%M%S")
            file = os.path.join(file, f"{now}.json")

        # make all parent dirs
        util.mkdirs(file)
        with open(file, "w") as f:
            json.dump(self.history, f, indent="\t")

    def load_history(self, hist):
        """
        loads history
        :param hist: type could be a file or file path or dict
        """
        if isinstance(hist, str):  # file path
            with open(hist) as f:
                self.history = json.load(f)
        elif isinstance(hist, io.IOBase):  # file
            self.history = json.load(hist)
        elif isinstance(hist, dict):  # json dict
            self.history = hist

    def grab(self, response):
        """
        grabs important data from response
        :param response: the response from the bot
        :return: grabbed data
        """
        pass
