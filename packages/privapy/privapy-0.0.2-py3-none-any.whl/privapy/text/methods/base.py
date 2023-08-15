"""Base class for text cleaning methods."""


class BaseMethod:
    """Base class for text cleaning methods."""

    replacement: str

    def __call__(self, text: str) -> str:
        """Call the cleaning method.
        Args:
            text (str): the text to clean
        Returns:
            str: the cleaned text
        """
        raise NotImplementedError
