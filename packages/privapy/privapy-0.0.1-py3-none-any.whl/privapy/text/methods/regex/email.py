import re
from ..base import BaseMethod


def clean_email(text: str, replacement: str = "<<EMAIL>>") -> str:
    return re.sub(r"[\w\.-]+@[\w\.-]+", replacement, text)


class EmailCleaner(BaseMethod):
    def __init__(self, replacement: str = "<<EMAIL>>"):
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        return clean_email(text, self.replacement)
