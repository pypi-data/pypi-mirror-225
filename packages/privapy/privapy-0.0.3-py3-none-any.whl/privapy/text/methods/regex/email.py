"""Cleaning methods for emails."""
import re
from ..base import BaseMethod


def clean_email(text: str, replacement: str = "<<EMAIL>>") -> str:
    """Clean a text by replacing emails with a replacement string.
    Args:
        text (str): the text to clean
        replacement (str, optional): The string to replace emails with. Defaults to "<<EMAIL>>".
    Returns:
        str: the cleaned text
    """
    return re.sub(r"[\w\.-]+@[\w\.-]+", replacement, text)


class EmailCleaner(BaseMethod):
    """Email cleaner method for text cleaning."""

    def __init__(self, replacement: str = "<<EMAIL>>"):
        """Initialize EmailCleaner
        Args:
            replacement (str, optional): The string to replace emails with. Defaults to "<<EMAIL>>".
        """
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        """Clean a text by replacing emails with a replacement string.
        Args:
            text (str): the text to clean
        Returns:
            str: the cleaned text
        """
        return clean_email(text, self.replacement)
