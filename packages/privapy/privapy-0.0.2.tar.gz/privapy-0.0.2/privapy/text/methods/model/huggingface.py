"""HuggingFace pipeline method for text cleaning."""
from transformers import pipeline

from ..base import BaseMethod


class HuggingFacePipeline(BaseMethod):
    """HuggingFace pipeline method for text cleaning. Uses `transformers` `ner`
    pipeline to detect entities and replace them with a replacement string.
    """

    def __init__(
        self, model_name: str = "dslim/bert-base-NER", replacement: str = "<<ENT>>"
    ):
        """Initialize HuggingFacePipeline
        Args:
            model_name (str, optional): the name of the model to use.
            Defaults to "dslim/bert-base-NER".
            replacement (str, optional): the replacement string to use for entities.
            Defaults to "<<ENT>>".
        """
        self.model_name = model_name
        self.model = pipeline("ner", model=self.model_name, grouped_entities=True)
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        """Clean a text by replacing entities with a replacement string.
        Args:
            text (str): the text to clean
        Returns:
            str: the cleaned text
        """
        entities = self.model(text)
        for entity in entities:
            text = text.replace(entity["word"], self.replacement)
        return text
