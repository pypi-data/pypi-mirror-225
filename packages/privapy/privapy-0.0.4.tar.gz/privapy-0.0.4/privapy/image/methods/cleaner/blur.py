"""Class to clean images using a blur method."""

from typing import List
import cv2
import numpy as np

from ..base import BaseCleaner


class BlurCleaner(BaseCleaner):
    """Class to clean images using a blur method."""

    def __init__(self, blur_size: int = 25):
        """Initialize the BlurCleaner.

        Args:
            blur_size (int, optional): Size of the blur kernel. Defaults to 25.
        """
        self.blur_size = blur_size

    def clean(self, image: np.ndarray, bounding_boxes: List[np.ndarray]):
        """Clean an image using a blur method.
        Args:
            image (np.ndarray): Image to clean.
            bounding_boxes (List[np.ndarray]): List of bounding boxes of detected objects.
        Returns:
            np.ndarray: Cleaned image.
        """
        for box in bounding_boxes:
            xmin, ymin, xmax, ymax = box
            image[ymin:ymax, xmin:xmax] = cv2.blur(
                image[ymin:ymax, xmin:xmax], (self.blur_size, self.blur_size)
            )
        return image
