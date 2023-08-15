from typing import *
from .methods.base import BaseMethod
from .methods.regex import *
from .methods.model import *

DEFAULT_STEP_TYPES = Literal["all", "regex", "models"]
DEFAULT_REGEX_STEPS = [EmailCleaner, DateCleaner, TimeCleaner]
DEFAULT_MODEL_STEPS = [HuggingFacePipeline]
STEP_TYPE = Union[BaseMethod, Callable[[str], str]]


class TextCleaner:
    def __init__(self, steps: Union[DEFAULT_STEP_TYPES, List[STEP_TYPE]]):
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
        for step in self.steps:
            text = step(text)
        return text
