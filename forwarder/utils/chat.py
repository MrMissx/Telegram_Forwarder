from typing import List, List, Union, TypedDict, Optional

from forwarder import CONFIG


class ChatConfig(TypedDict):
    chat_id: int
    thread_id: Optional[int]


def parse_topic(chat_id: Union[str, int]) -> ChatConfig:
    if isinstance(chat_id, str):
        raw = chat_id.split("#")
        if len(raw) == 2:
            return {"chat_id": int(raw[0]), "thread_id": int(raw[1])}
        return {"chat_id": int(raw[0]), "thread_id": None}

    return {"chat_id": chat_id, "thread_id": None}


def get_source() -> List[ChatConfig]:
    return [parse_topic(chat["source"]) for chat in CONFIG]


def get_destenation(chat_id: int, topic_id: Optional[int] = None) -> List[ChatConfig]:
    """Get destination from a specific source chat

    Args:
        chat_id (`int`): source chat id
        topic_id (`Optional[int]`): source topic id. Defaults to None.
    """

    dest: List[ChatConfig] = []

    for chat in CONFIG:
        parsed = parse_topic(chat["source"])
        if parsed["chat_id"] == chat_id and (topic_id is None or parsed["thread_id"] == topic_id):
            dest.extend([parse_topic(item) for item in chat["destination"]])
    return dest
