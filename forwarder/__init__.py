import logging
import json
from os import getenv

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from forwarder.utils import get_source


load_dotenv(".env")

# load json file
with open("chat_list.json") as data:
    CONFIG = json.load(data)

SOURCE_CHAT = get_source(CONFIG)

logging.basicConfig(
    format="[ %(asctime)s: %(levelname)-8s ] %(name)-20s - %(message)s",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    LOGGER.error("No BOT_TOKEN token provided!")
    exit(1)
OWNER_ID = int(getenv("OWNER_ID", "0"))
REMOVE_TAG = getenv("REMOVE_TAG", "False") in {"true", "True", 1}

bot = ApplicationBuilder().token(BOT_TOKEN).build()
