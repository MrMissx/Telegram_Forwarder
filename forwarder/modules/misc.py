from telegram import Bot, Update
from telegram import ParseMode
from telegram.ext import MessageHandler, Filters

from forwarder import OWNER_ID, FROM_CHATS, TO_CHATS, dispatcher


def get_id(update, context):
    message = update.effective_message    # type: Optional[Message]

    if message.reply_to_message:  # Message is a reply to another message
        if message.reply_to_message.forward_from:  # Replied message is a forward from a user
            sender = message.reply_to_message.forward_from
            forwarder = message.reply_to_message.from_user
            message.reply_text(
                "The original sender, {}, has an ID of `{}`. \n"
                "The forwarder, {}, has an ID of `{}`.".format(
                    sender.first_name, sender.id,
                    forwarder.first_name, forwarder.id), parse_mode=ParseMode.MARKDOWN)
        elif message.reply_to_message.forward_from_chat:  # Replied message is a forward from a channel
            channel = message.reply_to_message.forward_from_chat
            forwarder = message.reply_to_message.from_user
            message.reply_text(
                "The channel, {}, has an ID of `{}`. \n"
                "The forwarder, {}, has an ID of `{}`.".format(
                    channel.title, channel.id,
                    forwarder.first_name, forwarder.id), parse_mode=ParseMode.MARKDOWN)
        
        else:
            user = message.reply_to_message.from_user  # Replied message is a message from a user
            message.reply_text("{}'s ID is `{}`.".format(user.first_name, user.id), parse_mode=ParseMode.MARKDOWN)

    else:
        chat = update.effective_chat
        
        if chat.type == "private":  # Private chat with the bot
            message.reply_text("Your ID is `{}`.".format(chat.id), parse_mode=ParseMode.MARKDOWN)
        
        else:  # Group chat where the bot is a member
            message.reply_text("This group's ID is `{}`.".format(chat.id), parse_mode=ParseMode.MARKDOWN)


GET_ID_HANDLER = MessageHandler(
    Filters.command & Filters.regex(r"^/id") & (Filters.user(OWNER_ID) | Filters.update.channel_posts),
    get_id,
    run_async=True,
)

dispatcher.add_handler(GET_ID_HANDLER)