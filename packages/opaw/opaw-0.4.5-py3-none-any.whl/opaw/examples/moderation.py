from opaw.util import log
from opaw.model.moderation import ModerationBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("moderation", "logs/moderation.log")

# moderation
bot = ModerationBot()
prompt = "I want to kill them!!"
response = bot.create(prompt)
logger.info(response)

# show results that are flagged
logger.info(f"flags: {bot.grab(response)}")

# save history if needed
bot.save_history("history/moderation-hist.json")
