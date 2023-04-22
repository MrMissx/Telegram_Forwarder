from typing import Mapping, Set, List, Any


def get_source(config: List[Mapping[str, Any]]) -> Set[int]:
    return {int(chat["source"]) for chat in config}


def get_destenation(source: int, config: List[Mapping[str, Any]]) -> Set[int]:
    dest = set()
    for chat in config:
        if chat["source"] == source:
            dest.update(chat["destination"])
    return dest
