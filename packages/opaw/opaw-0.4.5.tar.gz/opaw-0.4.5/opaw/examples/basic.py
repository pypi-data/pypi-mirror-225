from time import sleep
from opaw.util import log
from opaw import util
from opaw.examples import setup
from opaw.model.chat import ChatBot

# logger
logger = log.get("basic", "logs/basic.log")

def loop_chat(model="gpt-3.5-turbo",
              system_prompt="You are a helpful assistant.",
              history_file="history/basic-hist.json"):
    bot = ChatBot(model)
    bot.add_message(system_prompt, role="system")
    logger.info("(type \"bye\" to quit.)")
    sleep(0.1)  # wait for the logger buffering

    while True:
        user_input = input("User: ")
        if "bye" in user_input:
            logger.info("BYE!")
            break
        response = bot.create(user_input)
        logger.info(f"Bot: {bot.grab(response)}\n")
        sleep(0.1)  # wait for the logger buffering

    bot.save_history(history_file)


# api key
setup()

# start model
loop_chat()

# You can also set system prompt if needed
# util.loop_chat(system_prompt="You are a liar. So you always have to lie to me.")
