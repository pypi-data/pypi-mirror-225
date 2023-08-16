"""Date cleaner method for text cleaning."""
import re
from ..base import BaseMethod


def clean_date(text: str, replacement: str = "<<DATE>>") -> str:
    """Clean a text by replacing dates with a replacement string.

    Args:
        text (str): the text to clean
        replacement (str, optional): The string to replace dates with. Defaults to "<<DATE>>".

    Returns:
        str: the cleaned text
    """
    for pattern in [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}/\d{2}/\d{4}",
    ]:
        text = re.sub(pattern, replacement, text)
    return text


class DateCleaner(BaseMethod):
    """Date cleaner method for text cleaning."""

    def __init__(self, replacement: str = "<<DATE>>"):
        """Initialize DateCleaner
        Args:
            replacement (str, optional): The string to replace dates with. Defaults to "<<DATE>>".
        """
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        """Clean a text by replacing dates with a replacement string.
        Args:
            text (str): the text to clean
        Returns:
            str: the cleaned text
        """
        return clean_date(text, replacement=self.replacement)
