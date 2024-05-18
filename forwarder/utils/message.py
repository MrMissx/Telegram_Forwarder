import re

from typing import List


def predicate_text(filters: List[str], text: str) -> bool:
    """Check if the text contains any of the filters"""
    for i in filters:
        pattern = r"( |^|[^\w])" + re.escape(i) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False
