"""Class for obscuring objects from images."""

from typing import Union
import numpy as np
import PIL

from .methods.base import BaseCleaner, BaseDetector
from .methods.cleaner import BlurCleaner
from .methods.model import HuggingFacePipelineDetector


class ImageCleaner:
    """Class for obscuring objects from images."""

    def __init__(self, detector: BaseDetector = None, cleaner: BaseCleaner = None):
        """Initialize the ImageCleaner.

        Args:
            detector: The detector to use. Defaults to HuggingFacePipelineDetector.
            cleaner: The cleaner to use. Defaults to BlurCleaner.
        """
        self.detector = HuggingFacePipelineDetector() if detector is None else detector
        self.cleaner = BlurCleaner() if cleaner is None else cleaner

    def clean(
        self, image: Union[PIL.Image.Image, np.ndarray]
    ) -> Union[PIL.Image.Image, np.ndarray]:
        """Clean the image.

        Args:
            image (Union[PIL.Image.Image, np.ndarray]): The image to clean.
        Returns:
            Union[PIL.Image.Image, np.ndarray]: The cleaned image. Type is same as input.
        """
        input_type = type(image)
        if isinstance(image, np.ndarray):
            image = PIL.Image.fromarray(image)
        boxes = self.detector.get_bounding_boxes(image)
        image = np.array(image)
        image = self.cleaner.clean(image, boxes)
        return (
            image if isinstance(input_type, np.ndarray) else PIL.Image.fromarray(image)
        )

    def clean_file(self, path: str) -> PIL.Image.Image:
        """Clean the image at the given path.

        Args:
            path (str): The path to the image to clean.

        Returns:
            PIL.Image.Image: The cleaned image.
        """
        image = PIL.Image.open(path)
        return self.clean(image)
