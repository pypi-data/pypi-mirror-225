from opaw.util import log
from opaw.model.embedding import EmbeddingBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("embedding", "logs/embedding.log")

# embedding
bot = EmbeddingBot()
prompt = "Cheese is melting on my laptop"
response = bot.create(prompt)
logger.info(f"embeddings: {bot.grab(response)}")

# save history if needed
bot.save_history("history/embedding-hist.json")


