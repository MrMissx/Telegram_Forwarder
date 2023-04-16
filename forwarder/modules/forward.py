from typing import Union

from telegram import Update, Message, MessageId
from telegram.error import ChatMigrated
from telegram.ext import MessageHandler, filters, ContextTypes

from forwarder import bot, CONFIG, REMOVE_TAG, LOGGER
from forwarder.utils import get_source, get_destenation


async def send_message(message: Message, chat_id: int) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        return await message.copy(chat_id)
    return await message.forward(chat_id)


async def forwarder(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    source = update.effective_chat

    if not message or not source:
        return

    for chat in get_destenation(source.id, CONFIG):
        try:
            await send_message(message, chat)
        except ChatMigrated as err:
            await send_message(message, err.new_chat_id)
            LOGGER.warning(
                f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!"
            )
        except Exception:
            LOGGER.warning(f"Failed to forward message from {source.id} to {chat}")


FORWARD_HANDLER = MessageHandler(
    filters.Chat(get_source(CONFIG)) & ~filters.COMMAND & ~filters.StatusUpdate.ALL,
    forwarder,
)
bot.add_handler(FORWARD_HANDLER)
