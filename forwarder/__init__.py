import logging
import json
from os import getenv, path

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

load_dotenv(".env")


logging.basicConfig(
    format="[ %(asctime)s: %(levelname)-8s ] %(name)-20s - %(message)s",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

httpx_logger = logging.getLogger('httpx')
httpx_logger.setLevel(logging.WARNING)

# load json file
config_name = "chat_list.json"
if not path.isfile(config_name):
    LOGGER.error("No chat_list.json config file found! Exiting...")
    exit(1)
with open(config_name, "r") as data:
    CONFIG = json.load(data)


BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    LOGGER.error("No BOT_TOKEN token provided!")
    exit(1)
OWNER_ID = int(getenv("OWNER_ID", "0"))
REMOVE_TAG = getenv("REMOVE_TAG", "False") in {"true", "True", 1}

bot = ApplicationBuilder().token(BOT_TOKEN).build()
