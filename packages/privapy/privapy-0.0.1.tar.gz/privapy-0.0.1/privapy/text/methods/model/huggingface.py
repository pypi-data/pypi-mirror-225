from transformers import pipeline

from ..base import BaseMethod


class HuggingFacePipeline(BaseMethod):
    def __init__(
        self, model_name: str = "dslim/bert-base-NER", replacement: str = "<<ENT>>"
    ):
        self.model_name = model_name
        self.model = pipeline("ner", model=self.model_name, grouped_entities=True)
        self.replacement = replacement

    def __call__(self, text: str) -> str:
        entities = self.model(text)
        for entity in entities:
            text = text.replace(entity["word"], self.replacement)
        return text
