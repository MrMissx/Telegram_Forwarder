from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters
from telegram.constants import ParseMode

from forwarder import bot, OWNER_ID

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    if not (chat and message and user):
        return

    if chat.type == "private":
        await message.reply_text(
            PM_START_TEXT.format(user.first_name, context.bot.first_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply_text("I'm up and running!")


async def help(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message
    if not (chat and message):
        return

    if not chat.type == "private":
        await message.reply_text("Contact me via PM to get a list of usable commands.")
    else:
        await message.reply_text(PM_HELP_TEXT)


bot.add_handler(CommandHandler("start", start, filters=filters.User(OWNER_ID)))
bot.add_handler(CommandHandler("help", help, filters=filters.User(OWNER_ID)))
