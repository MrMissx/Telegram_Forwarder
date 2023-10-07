from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler

from forwarder import OWNER_ID, bot


async def get_id(update: Update, _):
    message = update.effective_message
    chat = update.effective_chat
    if not message or not chat:
        return

    if chat.type == "private":  # Private chat with the bot
        return await message.reply_text(f"🙋‍♂️ Your ID is `{chat.id}`")

    result = f"👥 Chat ID: `{chat.id}`"
    if chat.is_forum:
        result += f"\n💬 Forum/Topic ID: `{message.message_thread_id}`"

    if message.reply_to_message:
        forwarder = message.reply_to_message.from_user
        if message.reply_to_message.forward_from:  # Forwarded user
            sender = message.reply_to_message.forward_from
            result += f"🙋‍♂️ The original sender ({sender.first_name}), ID is: `{sender.id}`\n"
            result += f"⏩ The forwarder ({forwarder.first_name if forwarder else 'Unknown'}) ID: `{forwarder.id if forwarder else 'Unknown'}`"

        if message.reply_to_message.forward_from_chat:  # Forwarded channel
            channel = message.reply_to_message.forward_from_chat
            result += f"💬 The channel {channel.title} ID: `{channel.id}`\n"
            result += f"⏩ The forwarder ({forwarder.first_name if forwarder else 'Unknown'}) ID: `{forwarder.id if forwarder else 'Unknown'}`"

    return await message.reply_text(
        result,
        parse_mode=ParseMode.MARKDOWN,
    )


GET_ID_HANDLER = MessageHandler(
    filters.COMMAND & filters.Regex(r"^/id") & (filters.User(OWNER_ID) | filters.ChatType.CHANNEL),
    get_id,
)

bot.add_handler(GET_ID_HANDLER)
