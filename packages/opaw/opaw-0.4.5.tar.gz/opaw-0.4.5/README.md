[![PyPi](https://img.shields.io/pypi/v/opaw)](https://pypi.org/project/opaw/)


# openai-pw
Unofficial python wrapper of [OpenAI](https://openai.com/) API.


# Features
- Wrapped models (chat, audio, image, embeddings ...)
- History(requests and responses) save and load to/from a file
- Audio bot supports also [whisper](https://github.com/openai/whisper) and [whisper_timestamped](https://github.com/linto-ai/whisper-timestamped)(word-level timestamps)



# Quick start
You can also play with in **[this colab](https://colab.research.google.com/drive/1nJ1-YwLMSxSVx092uBVoarvuVUyt65xC?usp=drive_link)**. Or

1. Download `openai` using pip.
```cmd
pip install opaw
```
2. Create a `open-api-key.txt` file and insert [your api key](https://platform.openai.com/account/api-keys) into the file. Or set an environment variable with the name `OPENAI_API_KEY`.
3. Write a demo code and play with ChatGPT.
```py
from opaw.examples.basic import loop_chat 
from opaw import util

util.setup() # api key setup
loop_chat() # start chat
```

# Usage
**All usage codes need to setup API key using `util.setup()` before running**

- [chat](#chat)
- [image](#image)
- [audio](#audio)
- [completion](#completion)
- [embedding](#embedding)
- [moderation](#moderation)
- [file](#file)
- [finetune](#finetune)
- [edit](#edit)
- [function_call](#function_call)
- [load_chat](#load_chat)
- [save_history](#save_history)


### Chat
```py
from opaw.model.chat import ChatBot
from opaw import util

util.setup() # api key setup
bot = ChatBot()
bot.add_message("You are a helpful assistant.", role="system")
response = bot.create("What is openai?")
print("Bot:", bot.grab(response))
```

### Image
```py
from opaw.model.image import ImageBot
from opaw import util

util.setup() # api key setup
bot = ImageBot()
prompt = "A black cat sitting on a frozen lake like a emoticon style"
response = bot.create(prompt, task="create", size="256x256")
bot.save_img(response, "cat.png")
```


### Audio
```py
from opaw.model.audio import AudioBot
from opaw import util

util.setup() # api key setup

# download a mp3 file from here: https://github.com/hiimanget/openai-pw/blob/main/opaw/examples/radio_short.mp3
bot = AudioBot()
file = 'radio_short.mp3'

# official api
response = bot.create(file, lib="api", task="stt")
print(f"official api: {response['text']}")

# whisper (https://github.com/openai/whisper)
response = bot.create(file, lib="whisper", name="tiny")
print(f"whisper: {response}")

# whisper_timestamped: supports word-timestamping (https://github.com/linto-ai/whisper-timestamped)
response = bot.create(file, lib="whisper_t", name="tiny", device="cpu")
print(f"whisper_timestamped: {util.pprints(response)}")
```


### Completion
```py
from opaw import util
from opaw.model.completion import CompletionBot

util.setup() # api key setup
bot = CompletionBot()
prompt = "Tell some lies"
response = bot.create(prompt, max_tokens=50)
print(bot.grab(response))
```

### Embedding
```py
from opaw import util
from opaw.model.embedding import EmbeddingBot 

util.setup() # api key setup
bot = EmbeddingBot()
prompt = "Cheese is melting on my laptop"
response = bot.create(prompt)
print(f"embeddings: {bot.grab(response)}")
```

### Moderation
```py
from opaw import util
from opaw.model.moderation import ModerationBot

util.setup() # api key setup
bot = ModerationBot()
prompt = "I want to kill them!!"
response = bot.create(prompt)
print(response)

# show results that are flagged
print(f"flags: {bot.grab(response)}")
```

### File
```py
from opaw import util
from opaw.model.file import FileBot

util.setup() # api key setup

# download a file from here: https://github.com/hiimanget/openai-pw/blob/main/opaw/examples/file-upload.jsonl
bot = FileBot()
# file upload
response = bot.create(task="upload", file="file-upload.jsonl", purpose="fine-tune")
print(f"file-upload response: {response}")
id = response["id"]

# retrieve a file
response = bot.create(task="retrieve", id=id)
print(f"list response: {response}")

# download file
response = bot.create(task="download", id=id)
print(f"download response: {response}")
```

### Finetune
```py
from opaw import util
from opaw.model.finetune import FinetuneBot

util.setup() # api key setup
bot = FinetuneBot()
response = bot.create(task="create", training_file="...")  # input your file id in "training_file"
print(f"finetune create: {response}")

# finetune list
response = bot.create(task="list")
print(f"finetune list: {response}")
```

### Edit
**Deprecated**
```py
from opaw import util
from opaw.model.edit import EditBot

util.setup() # api key setup
bot = EditBot()
prompt = "Hey, this was my filst car!!"  # filst -> first
instruction = "Fix the spelling mistakes"
response = bot.create(prompt, instruction=instruction)
print(f"text: {bot.grab(response)}")
```

### Function_call
```py
from opaw import util
from opaw.model.chat import ChatBot
from opaw.util import func_meta

util.setup() # api key setup

# prepare a function that will be called
def stock_price(company):
    if company == "APPL":
        return 100
    elif company == "AMZN":
        return 150

funcs_meta = [
    func_meta("stock_price",  # name
              "Get the stock price of a given company",  # desc
              ["company", "string", "The company stock name, e.g. APPL"],  # properties
              ["company"])  # required
]
funcs = {"stock_price": stock_price}

# ask a question to gpt
bot = ChatBot("gpt-3.5-turbo-0613", funcs_meta=funcs_meta, funcs=funcs)  # must use "gpt-3.5-turbo-0613" to use function call
bot.add_message("You are a helpful assistant that can send function json when need.", role="system")
response = bot.create(f"What is the amazon's stock price?", call_fn=True)

# if function_call exists (not guaranteed 100%)
if bot.get_fn_call(response):
    fn_result = bot.call_function(response)
    print(f"amazon stock price: {fn_result}")
else:
    print("no function call")
```

### Load_chat
```py
from opaw import util
from opaw.model.chat import ChatBot

util.setup() # api key setup

# download a chat history file from here: https://github.com/hiimanget/openai-pw/blob/main/opaw/examples/history/chat-hist.json
bot = ChatBot()
bot.load_msgs("chat-hist.json")  # load history (former conversation)

response = bot.create("Then, has the company's stock been listed?")  # bot sould know meaning of "there" if history loaded successfully
print(f"response: {bot.grab(response)}")
```

### Save_history
```py
from opaw import util
from opaw.model.chat import ChatBot

util.setup() # api key setup
bot = ChatBot()
bot.add_message("You are a helpful assistant.", role="system")
response = bot.create("Do you like cheese?")
print("resopnse:", bot.grab(response))

# save history
bot.save_history("history/chat-hist.json")  # check out the file in the history directory
```

# More examples
Try to run something in [examples](opaw/examples) after downloaded this repo. (needed to run `pip install -r requirements.txt` before running examples)


# OpenAI links
- [API](https://platform.openai.com/docs/api-reference/introduction)
- [Guide](https://platform.openai.com/docs/guides/gpt)
- [model list](https://platform.openai.com/docs/models)
- [community](https://community.openai.com/)
- [usage](https://platform.openai.com/account/usage)
- [api key](https://platform.openai.com/account/api-keys)


# License
MIT
