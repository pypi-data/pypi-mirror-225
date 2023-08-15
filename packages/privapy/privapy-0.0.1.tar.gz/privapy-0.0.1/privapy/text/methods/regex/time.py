import re
from ..base import BaseMethod


def clean_time(text: str, replacement: str = "<<TIME>>") -> str:
    for pattern in [
        r"\d{2}:\d{2}:\d{2}",
        r"\d{2}:\d{2}",
    ]:
        text = re.sub(pattern, replacement, text)
    return text


class TimeCleaner(BaseMethod):
    def __init__(self, replacement: str = "<<TIME>>"):
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        return clean_time(text, replacement=self.replacement)
