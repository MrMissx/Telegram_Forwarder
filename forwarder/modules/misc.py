from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler

from forwarder import OWNER_ID, bot


async def get_id(update: Update, _):
    message = update.effective_message
    if not message:
        return

    if message.reply_to_message:  # Message is a reply to another message
        if message.reply_to_message.forward_from:  # Replied message is a forward from a user
            sender = message.reply_to_message.forward_from
            forwarder = message.reply_to_message.from_user
            await message.reply_text(
                "The original sender, {}, has an ID of `{}`. \n"
                "The forwarder, {}, has an ID of `{}`.".format(
                    sender.first_name,
                    sender.id,
                    forwarder.first_name if forwarder else "Unknown",
                    forwarder.id if forwarder else "Unknown",
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        elif (
            message.reply_to_message.forward_from_chat
        ):  # Replied message is a forward from a channel
            channel = message.reply_to_message.forward_from_chat
            forwarder = message.reply_to_message.from_user
            await message.reply_text(
                "The channel, {}, has an ID of `{}`. \n"
                "The forwarder, {}, has an ID of `{}`.".format(
                    channel.title,
                    channel.id,
                    forwarder.first_name if forwarder else "Unknown",
                    forwarder.id if forwarder else "Unknown",
                ),
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            user = message.reply_to_message.from_user  # Replied message is a message from a user
            await message.reply_text(
                "{}'s ID is `{}`.".format(
                    user.first_name if user else "Unknown", user.id if user else "Unknown"
                ),
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        chat = update.effective_chat
        if not chat:
            return

        if chat.type == "private":  # Private chat with the bot
            await message.reply_text(
                "Your ID is `{}`.".format(chat.id), parse_mode=ParseMode.MARKDOWN
            )

        else:  # Group chat where the bot is a member
            await message.reply_text(
                "This group's ID is `{}`.".format(chat.id),
                parse_mode=ParseMode.MARKDOWN,
            )


GET_ID_HANDLER = MessageHandler(
    filters.COMMAND & filters.Regex(r"^/id") & (filters.User(OWNER_ID) | filters.ChatType.CHANNEL),
    get_id,
)

bot.add_handler(GET_ID_HANDLER)
