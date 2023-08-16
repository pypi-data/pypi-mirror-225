"""Class for detecting faces in images using HuggingFace's face detection model."""

from typing import List, Optional

import numpy as np
from PIL import Image
from transformers import pipeline

from ..base import BaseDetector


class HuggingFacePipelineDetector(BaseDetector):
    """HuggingFace pipeline detector class."""

    def __init__(
        self,
        model_name: str = "facebook/detr-resnet-50",
        labels: Optional[List[str]] = None,
        **kwargs,
    ):
        """Initialize HuggingFace pipeline detector.
        Args:
            model_name (str): Name of model to use. Defaults to "facebook/detr-resnet-50".
            labels (Optional[List[str]]): List of labels to use. ["person"] is used if
            `None` is provided.

        Returns:
            List[np.ndarray]: List of bounding boxes.
        """
        if labels is None:
            labels = ["person"]
        self.detector = pipeline("object-detection", model=model_name, **kwargs)
        self.labels = labels

    def get_bounding_boxes(self, image: Image) -> List[np.ndarray]:
        """Get bounding boxes of faces in image."""
        res = self.detector(image)
        boxes = []
        for obj in res:
            if obj["label"] in self.labels:
                box = obj["box"]
                boxes.append(
                    np.array([box["xmin"], box["ymin"], box["xmax"], box["ymax"]])
                )
        return boxes
