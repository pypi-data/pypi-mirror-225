"""Text cleaner module."""

from typing import Callable, List, Literal, Union
from .methods.base import BaseMethod
from .methods.regex import EmailCleaner, DateCleaner, TimeCleaner
from .methods.model import HuggingFacePipeline

DEFAULT_STEP_TYPES = Literal["all", "regex", "models"]
DEFAULT_REGEX_STEPS = [EmailCleaner, DateCleaner, TimeCleaner]
DEFAULT_MODEL_STEPS = [HuggingFacePipeline]
STEP_TYPE = Union[BaseMethod, Callable[[str], str]]


class TextCleaner:
    """Text cleaner class used to excecute a series of cleaning steps on a text."""

    def __init__(self, steps: Union[DEFAULT_STEP_TYPES, List[STEP_TYPE]] = "all"):
        """Initialize TextCleaner

        Args:
            steps (Union[DEFAULT_STEP_TYPES, List[STEP_TYPE]]): the cleaning steps to
            excecute on the text. Can be a list of BaseMethod objects or a list of functions
            that take a string and return a string. Alternatively, can be a string with the
            value "all", "regex" or "models" to use the default steps. Defaults to "all".

        Raises:
            ValueError: if steps is string that does not match any of the accepted values.

        """
        if isinstance(steps, str):
            if steps == "all":
                steps = DEFAULT_REGEX_STEPS + DEFAULT_MODEL_STEPS
            elif steps == "regex":
                steps = DEFAULT_REGEX_STEPS
            elif steps == "models":
                steps = DEFAULT_MODEL_STEPS
            else:
                raise ValueError(
                    f"Invalid step type: {steps}. Accepted values are {DEFAULT_STEP_TYPES}."
                )
            steps = [step() for step in steps]
        self.steps = steps

    def clean(self, text: str) -> str:
        """Clean a text by excecuting the cleaning steps.

        Args:
            text (str): the text to clean

        Returns:
            str: the cleaned text
        """
        for step in self.steps:
            text = step(text)
        return text
