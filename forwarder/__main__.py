import importlib

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters

from forwarder import (API_KEY, CERT_PATH, IP_ADDRESS, LOGGER, OWNER_ID, PORT,
                       URL, WEBHOOK, dispatcher, updater)
from forwarder.modules import ALL_MODULES

PM_START_TEXT = """
Hey {}, I'm {}!
I'm a bot used to forward messages from one chat to another.

To obtain a list of commands, use /help.
"""

PM_HELP_TEXT = """
Here is a list of usable commands:
 - /start : Starts the bot.
 - /help : Sends you this help message.

just send /id in private chat/group/channel and i will reply it's id.
"""

for module in ALL_MODULES:
    importlib.import_module("forwarder.modules." + module)


def start(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    if chat.type == "private":
        message.reply_text(
            PM_START_TEXT.format(user.first_name, dispatcher.bot.first_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        message.reply_text("I'm up and running!")


def help(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message

    if not chat.type == "private":
        message.reply_text("Contact me via PM to get a list of usable commands.")
    else:
        message.reply_text(PM_HELP_TEXT)


def main():
    start_handler = CommandHandler(
        "start", start, filters=Filters.user(OWNER_ID), run_async=True
    )
    help_handler = CommandHandler(
        "help", help, filters=Filters.user(OWNER_ID), run_async=True
    )
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    if WEBHOOK and URL:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen=IP_ADDRESS, port=PORT, url_path=API_KEY)

        if CERT_PATH:
            updater.bot.set_webhook(
                url=URL + API_KEY, certificate=open(CERT_PATH, "rb")
            )
        else:
            updater.bot.set_webhook(url=URL + API_KEY)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
