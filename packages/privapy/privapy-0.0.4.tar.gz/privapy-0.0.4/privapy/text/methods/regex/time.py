"""Time cleaner method for text cleaning."""
import re
from ..base import BaseMethod


def clean_time(text: str, replacement: str = "<<TIME>>") -> str:
    """Clean a text by replacing times with a replacement string.
    Args:
        text (str): the text to clean
        replacement (str, optional): The string to replace times with. Defaults to "<<TIME>>".
    Returns:
        str: the cleaned text
    """
    for pattern in (
        r"\d{2}:\d{2}:\d{2}",
        r"\d{2}:\d{2}",
    ):
        text = re.sub(pattern, replacement, text)
    return text


class TimeCleaner(BaseMethod):
    """Time cleaner method for text cleaning."""

    def __init__(self, replacement: str = "<<TIME>>"):
        """Initialize TimeCleaner
        Args:
            replacement (str, optional): The string to replace times with. Defaults to "<<TIME>>".
        """
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        """Clean a text by replacing times with a replacement string.
        Args:
            text (str): the text to clean
        Returns:
            str: the cleaned text
        """
        return clean_time(text, replacement=self.replacement)
