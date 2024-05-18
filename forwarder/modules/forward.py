import asyncio
from typing import Union, Optional

from telegram import Update, Message, MessageId
from telegram.error import ChatMigrated, RetryAfter
from telegram.ext import MessageHandler, filters, ContextTypes

from forwarder import bot, REMOVE_TAG, LOGGER
from forwarder.utils import get_destination, get_config, predicate_text


async def send_message(
    message: Message, chat_id: int, thread_id: Optional[int] = None
) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        return await message.copy(chat_id, message_thread_id=thread_id)  # type: ignore
    return await message.forward(chat_id, message_thread_id=thread_id)  # type: ignore


async def forwarder(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    source = update.effective_chat

    if not message or not source:
        return

    dest = get_destination(source.id, message.message_thread_id)

    for config in dest:

        if config.filters:
            if not predicate_text(config.filters, message.text or ""):
                return
        if config.blacklist:
            if predicate_text(config.blacklist, message.text or ""):
                return

        for chat in config.destination:
            LOGGER.debug(f"Forwarding message {source.id} to {chat}")
            try:
                await send_message(message, chat.get_id(), chat.get_topic())
            except RetryAfter as err:
                LOGGER.warning(f"Rate limited, retrying in {err.retry_after} seconds")
                await asyncio.sleep(err.retry_after + 0.2)
                await send_message(message, chat.get_id(), thread_id=chat.get_topic())
            except ChatMigrated as err:
                await send_message(message, err.new_chat_id)
                LOGGER.warning(
                    f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!"
                )
            except Exception as err:
                LOGGER.warning(f"Failed to forward message from {source.id} to {chat} due to {err}")


FORWARD_HANDLER = MessageHandler(
    filters.Chat([config.source.get_id() for config in get_config()])
    & ~filters.COMMAND
    & ~filters.StatusUpdate.ALL,
    forwarder,
)
bot.add_handler(FORWARD_HANDLER)
