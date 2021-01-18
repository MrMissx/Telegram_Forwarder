from telegram.ext import MessageHandler, Filters

from forwarder import FROM_CHATS, TO_CHATS, LOGGER, dispatcher


def forward(update, context):
    message = update.effective_message  # type: Optional[Message]
    from_chat_id = update.effective_chat.id
    from_chat_name = update.effective_chat.title or update.effective_chat.first_name
    
    for chat in TO_CHATS:
        to_chat_name = context.bot.get_chat(chat).title or context.bot.get_chat(chat).first_name
        try:
            context.bot.forward_message(chat_id=chat, from_chat_id=from_chat_id, message_id=message.message_id)
        
        except:
            LOGGER.exception("Error while forwarding message from chat \"{}\" to chat \"{}\".".\
                             format(from_chat_name, to_chat_name))


try:
    FORWARD_HANDLER = MessageHandler(
        Filters.chat(FROM_CHATS) & ~Filters.status_update & ~Filters.command,
        forward,
        run_async=True
    )
    
    dispatcher.add_handler(FORWARD_HANDLER)

except ValueError:  # When FROM_CHATS list is not set because user doesn't know chat id(s)
    LOGGER.warn("I can't FORWARD_HANDLER because your FROM_CHATS list is empty.")
