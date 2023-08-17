from opaw.util import log
from opaw.examples import funcs
from opaw.model.chat import ChatBot
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("function_call", "logs/function_call.log")

# bot (https://platform.openai.com/docs/guides/gpt/function-calling
bot = ChatBot("gpt-3.5-turbo-0613", funcs_meta=funcs.funcs_meta, funcs=funcs.funcs)
bot.add_message("You are a helpful assistant that can send function json when need.", role="system")

response = bot.create(f"What is the amazon's stock price?", call_fn=True)

# if function_call exists
if bot.get_fn_call(response):
    fn_result = bot.call_function(response)
    logger.info(f"amazon stock price: {fn_result}")
else:
    logger.info("no function call")

# save model history
bot.save_history("history/function-call-hist.json")
