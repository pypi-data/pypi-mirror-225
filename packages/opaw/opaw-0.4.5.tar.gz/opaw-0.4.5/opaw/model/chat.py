import copy
import io
import json
import openai
from opaw.model.bot import Bot
from opaw import util


class ChatBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/chat
    """

    def __init__(self, model=util.default_models["chat"],
                 messages=None, funcs=None, funcs_meta=None):
        super().__init__(model, "chat")

        # messages: conversation list of dict, contains role and content (see chat-history.json)
        self.messages = [] if messages is None else messages
        self.funcs = [] if funcs is None else funcs  # callback functions
        self.funcs_meta = [] if funcs_meta is None else funcs_meta  # contains name, desc, params...

    def create(self, content=None, call_fn=False, memory=-1, **kargs):
        """
        Gets a response from bot
        :param content: get a response with messages (content)
        :param call_fn: if true, function call will be enabled
        :param memory: number of recent message limit (if -1, no limit)
        :param kargs: other args (if call_fn is True, self.funcs_info will be passed to "functions")
        :return:
        """
        # default
        role = kargs["role"] if "role" in kargs else "user"

        # options
        if call_fn:
            kargs["functions"] = self.funcs_meta  # pass functions meta info

        if content is not None:
            content = str(content)
            self.add_message(content, role=role)

        msgs = copy.deepcopy(self.messages)
        if memory >= 0:
            msgs = self.messages[-memory - 1:]  # -1 is for the appended last response

        request = {
            "model": self.model,
            "messages": msgs,
            **kargs
        }

        self._history_req(request)

        response = openai.ChatCompletion.create(**request)

        # insert response message to the messages
        res_msg = self._get_msg(response)
        self.messages.append(res_msg)
        self._history_res(response)

        return response

    def add_message(self, content, role="user"):
        self.messages.append({"role": role, "content": content})

    def call_function(self, response):
        fn_call = self.get_fn_call(response)

        # if function_call exist
        if fn_call:
            function_name = fn_call["name"]
            function = self.funcs[function_name]

            fn_args = json.loads(fn_call["arguments"])
            return function(**fn_args)

    def get_fn_call(self, response):
        return self._get_msg(response).get("function_call")

    def total_tokens(self, messages):
        """
        returns number of used all tokens
        """
        return sum([int(msg["usage"]["total_tokens"]) for msg in messages])

    def load_msgs(self, history):
        """
        loads conversation history
        :param history: type could be a file or file path or dict
        """

        if isinstance(history, str):  # file path (str)
            with open(history) as f:
                hist = json.load(f)
        elif isinstance(history, io.IOBase):  # file
            hist = json.load(history)
        elif isinstance(history, dict):  # json dict
            hist = history
        else:
            return

        # load history
        self.history = copy.deepcopy(hist)

        # load messages of the last request
        self.messages = next((item["messages"] for item in hist[::-1] if "messages" in item), [])

        # insert last response to messages
        last_res_msg = next((self._get_msg(item) for item in hist[::-1] if "choices" in item), None)
        self.messages.append(last_res_msg)

    def _get_msg(self, response):
        """
        :return: grabs a bot's message of the response message
        """
        return response["choices"][0]["message"]

    def grab(self, response):
        """
        :return: grabs a message content of the response message
        """
        return self._get_msg(response)["content"]
