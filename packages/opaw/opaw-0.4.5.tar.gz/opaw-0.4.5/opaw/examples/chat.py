from opaw.util import log
from opaw.model.chat import ChatBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("chat", "logs/chat.log")

# chat
def chat(prompt, **kargs):
    response = bot.create(prompt, **kargs)
    logger.info(f"response: {bot.grab(response)}")


bot = ChatBot()
bot.add_message("You are a helpful assistant.", role="system")

chat("What is openai?")
chat("Then, who made it?")

# if memory is 0, bot don't know previous conversation (see chat-history.json for detail)
chat("What models are made in there?", memory=0)
chat("You know what I have said before now. What models are made in there?")  # bot knows previous conversation now

# save history if needed
bot.save_history("history/chat-hist.json")
