from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async

from forwarder import FROM_CHATS, TO_CHATS, LOGGER, dispatcher


@run_async
def forward(bot: Bot, update: Update):
    message = update.effective_message  # type: Optional[Message]
    from_chat_id = update.effective_chat.id
    from_chat_name = update.effective_chat.title or update.effective_chat.first_name
    
    for chat in TO_CHATS:
        to_chat_name = bot.get_chat(chat).title or bot.get_chat(chat).first_name
        try:
            bot.forward_message(chat_id=chat, from_chat_id=from_chat_id, message_id=message.message_id)
        
        except:
            LOGGER.exception("Error while forwarding message from chat \"{}\" to chat \"{}\".".\
                             format(from_chat_name, to_chat_name))


try:
    FORWARD_HANDLER = MessageHandler(Filters.chat(FROM_CHATS) & ~Filters.status_update & ~Filters.command,
                                     forward)
    
    dispatcher.add_handler(FORWARD_HANDLER)

except ValueError:  # When FROM_CHATS list is not set because user doesn't know chat id(s)
    LOGGER.warn("I can't Forward because your FROM_CHATS list is empty.")
