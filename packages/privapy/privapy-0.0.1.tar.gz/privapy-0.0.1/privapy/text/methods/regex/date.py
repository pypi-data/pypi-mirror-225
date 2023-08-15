import re
from ..base import BaseMethod


def clean_date(text: str, replacement: str = "<<DATE>>") -> str:
    for pattern in [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}/\d{2}/\d{4}",
    ]:
        text = re.sub(pattern, replacement, text)
    return text


class DateCleaner(BaseMethod):
    def __init__(self, replacement: str = "<<DATE>>"):
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        return clean_date(text, replacement=self.replacement)
