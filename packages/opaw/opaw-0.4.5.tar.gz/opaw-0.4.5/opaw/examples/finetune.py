from opaw.util import log
from opaw.model.finetune import FinetuneBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("finetune", "logs/finetune.log")

# finetune create
bot = FinetuneBot()
response = bot.create(task="create", training_file="file-ZyeAvL8tuTrQ1dG3elrRPB9Z")
logger.info(f"finetune create: {response}")

# finetune list
response = bot.create(task="list")
logger.info(f"finetune list: {response}")

# save history if needed
bot.save_history("history/finetune-hist.json")
