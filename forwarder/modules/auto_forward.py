from typing import Union

from telegram import Message, MessageId
from telegram.ext import CallbackContext, Filters, MessageHandler
from telegram.error import ChatMigrated
from telegram.update import Update

from forwarder import FROM_CHATS, LOGGER, REMOVE_TAG, TO_CHATS, dispatcher


def send_message(message: Message, chat_id: int) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        return message.copy(chat_id)
    return message.forward(chat_id)



def forward(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not message or not chat:
        return
    from_chat_name = chat.title or chat.first_name

    for chat in TO_CHATS:
        to_chat_name = (
            context.bot.get_chat(chat).title or context.bot.get_chat(chat).first_name
        )
        try:
            send_message(message, chat)
        except ChatMigrated as err:
            send_message(message, err.new_chat_id)
            LOGGER.warning(f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!")
        except:
            LOGGER.exception(
                'Error while forwarding message from chat "{}" to chat "{}".'.format(
                    from_chat_name, to_chat_name
                )
            )


try:
    FORWARD_HANDLER = MessageHandler(
        Filters.chat(FROM_CHATS) & ~Filters.status_update & ~Filters.command,
        forward,
        run_async=True,
    )

    dispatcher.add_handler(FORWARD_HANDLER)

except ValueError:  # When FROM_CHATS list is not set because user doesn't know chat id(s)
    LOGGER.warn("I can't FORWARD_HANDLER because your FROM_CHATS list is empty.")
