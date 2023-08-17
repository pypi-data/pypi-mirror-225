from opaw.util import log
from opaw.model.file import FileBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("file", "logs/file.log")

bot = FileBot()

# file upload
response = bot.create(task="upload", file="file-upload.jsonl", purpose="fine-tune")
logger.info(f"file-upload response: {response}")
id = response["id"]

# retrieve a file
response = bot.create(task="retrieve", id=id)
logger.info(f"list response: {response}")

# download file
response = bot.create(task="download", id=id)
logger.info(f"download response: {response}")

# save history if needed
bot.save_history("history/file-hist.json")

