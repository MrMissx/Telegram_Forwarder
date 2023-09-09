from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler

from forwarder import OWNER_ID, bot


async def get_id(update: Update, _):
    message = update.effective_message
    if not message:
        return

    if message.reply_to_message:
        if message.reply_to_message.forward_from:  # Forwarded user
            sender = message.reply_to_message.forward_from
            forwarder = message.reply_to_message.from_user
            return await message.reply_text(
                f"🙋‍♂️ The original sender ({sender.first_name}), ID is: `{sender.id}`\n"
                f"⏩ The forwarder ({forwarder.first_name if forwarder else 'Unknown'}) ID: `{forwarder.id if forwarder else 'Unknown'}`",
                parse_mode=ParseMode.MARKDOWN,
            )

        if message.reply_to_message.forward_from_chat:  # Forwarded channel
            channel = message.reply_to_message.forward_from_chat
            forwarder = message.reply_to_message.from_user
            return await message.reply_text(
                f"💬 The channel {channel.title} ID: `{channel.id}`\n"
                f"⏩ The forwarder ({forwarder.first_name if forwarder else 'Unknown'}) ID: `{forwarder.id if forwarder else 'Unknown'}`",
            )

        user = message.reply_to_message.from_user
        return await message.reply_text(
            f"🙋‍♂️ {user.first_name if user else 'Unknown'} ID: `{user.id if user else 'Unknown'}`"
        )

    chat = update.effective_chat
    if not chat:
        return

    if chat.type == "private":  # Private chat with the bot
        return await message.reply_text(f"🙋‍♂️ Your ID is `{chat.id}`.")

    result = f"👥 Chat ID: {chat.id}"
    if chat.is_forum:
        result += f"\n💬 Forum/Topic ID: {message.message_thread_id}"
    return await message.reply_text(
        result,
        parse_mode=ParseMode.MARKDOWN,
    )


GET_ID_HANDLER = MessageHandler(
    filters.COMMAND & filters.Regex(r"^/id") & (filters.User(OWNER_ID) | filters.ChatType.CHANNEL),
    get_id,
)

bot.add_handler(GET_ID_HANDLER)
