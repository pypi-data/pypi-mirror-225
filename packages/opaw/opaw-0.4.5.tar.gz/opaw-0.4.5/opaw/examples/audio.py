from opaw.util import log
from opaw.model.audio import AudioBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("audio", "logs/audio.log")

# audio
bot = AudioBot()

# transcript (language: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
file = "radio_short.mp3"

# official api
response = bot.create(file, lib="api", task="stt")
logger.info(f"official api: {bot.grab(response)}")

# whisper
response = bot.create(file, lib="whisper", name="tiny")
logger.info(f"whisper: {response}")

# whisper_timestamped
response = bot.create(file, lib="whisper_t", name="tiny", device="cpu")
logger.info(f"whisper_timestamped: {util.pprints(response)}")

# save history if needed
bot.save_history("history/audio-hist.json")
