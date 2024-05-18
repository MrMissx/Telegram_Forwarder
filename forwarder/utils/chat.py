from typing import List, List, Union, Optional

from forwarder import CONFIG


PARSED_CONFIG = []


class ChatConfig:
    __chat: Union[str, int]

    def __init__(self, chat_id: Union[str, int]):
        self.__chat = chat_id

    def __repr__(self) -> str:
        if self.is_topic:
            return f"{self.get_id()}#{self.get_topic()}"
        return str(self.get_id())

    @property
    def is_topic(self) -> bool:
        if isinstance(self.__chat, str) and len(self.__chat.split("#")) == 2:
            return True
        return False

    def get_topic(self) -> Optional[int]:
        if not self.is_topic:
            return None

        if isinstance(self.__chat, int):
            return None

        return int(self.__chat.split("#")[1])

    def get_id(self) -> int:
        if isinstance(self.__chat, int):
            return self.__chat
        return int(self.__chat.split("#")[0])


class ForwardConfig:
    source: ChatConfig
    destination: List[ChatConfig]
    filters: Optional[List[str]]
    blacklist: Optional[List[str]]

    def __init__(
        self,
        source: Union[str, int],
        destination: List[Union[str, int]],
        filters: Optional[List[str]] = None,
        blacklist: Optional[List[str]] = None,
    ):
        self.source = ChatConfig(source)
        self.destination = [ChatConfig(item) for item in destination]
        self.filters = filters
        self.blacklist = blacklist


def get_config() -> List[ForwardConfig]:
    global PARSED_CONFIG
    if PARSED_CONFIG:
        return PARSED_CONFIG

    PARSED_CONFIG = [
        ForwardConfig(
            source=chat["source"],
            destination=chat["destination"],
            filters=chat.get("filters"),
            blacklist=chat.get("blacklist"),
        )
        for chat in CONFIG
    ]
    return PARSED_CONFIG


def get_destination(chat_id: int, topic_id: Optional[int] = None) -> List[ForwardConfig]:
    """Get destination from a specific source chat

    Args:
        chat_id (`int`): source chat id
        topic_id (`Optional[int]`): source topic id. Defaults to None.
    """

    dest: List[ForwardConfig] = []

    for chat in get_config():
        if chat.source.get_id() == chat_id and chat.source.get_topic() == topic_id:
            dest.append(chat)
    return dest
