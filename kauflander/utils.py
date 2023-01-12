from matplotlib import pyplot as plt
import cv2
import numpy as np
from typing import List, Tuple, Optional
from .identification import SegmentFeatureExtractor, BoundingBox


def show_segments(
    segments: List[SegmentFeatureExtractor],
    color: Optional[Tuple[int, int, int]] = None,
    show: bool = True,
    bitmap: Optional[np.ndarray] = None,
    shape: Optional[Tuple[int, int, int]] = None,
) -> np.ndarray:
    """show_segments.

    :param segments:
    :type segments: List[SegmentFeatureExtractor]
    :param color:
    :type color: Optional[Tuple[int, int, int]]
    :param show:
    :type show: bool
    :param bitmap:
    :type bitmap: Optional[np.ndarray]
    :param shape:
    :type shape: Optional[Tuple[int, int, int]]
    :rtype: np.ndarray
    """
    if bitmap is None:
        bitmap = np.zeros(shape, dtype=np.ubyte)

    for segment in segments:
        for where in segment.where:
            bitmap[tuple(where)] = color or segment.color

    if show:
        plt.imshow(bitmap)
        plt.show()

    return bitmap


def draw_bounding_box(
    image: np.ndarray,
    bounding_box: BoundingBox,
    color: Tuple[int, int, int] = (255, 0, 0),
    thickness: int = 3,
    scale_factor: float = 1,
) -> np.ndarray:
    """draw_bounding_box.

    :param image:
    :type image: np.ndarray
    :param bounding_box:
    :type bounding_box: BoundingBox
    :param color:
    :type color: Tuple[int, int, int]
    :param thickness:
    :type thickness: int
    :rtype: np.ndarray
    """
    mins = np.round(np.array(bounding_box.mins) * scale_factor)
    mins = np.clip(mins, (0, 0), (image.shape[0] - 1, image.shape[1] - 1)).astype(
        np.uint
    )
    maxes = np.round(np.array(bounding_box.maxes) * scale_factor)
    maxes = np.clip(maxes, (0, 0), (image.shape[0] - 1, image.shape[1] - 1)).astype(
        np.uint
    )

    return cv2.rectangle(
        image,
        mins[::-1],
        maxes[::-1],
        color,
        thickness,
    )
