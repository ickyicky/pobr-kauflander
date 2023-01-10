import numpy as np
from typing import Union, List, Tuple, Dict


def create_histogram(image: np.ndarray) -> Dict[int, int]:
    """create_histogram.

    :param image:
    :type image: np.ndarray
    :rtype: Dict[int, int]
    """
    histogram = {i: 0 for i in range(0, 256)}

    for row in image:
        for pixel in row:
            histogram[np.round(pixel.mean())] += 1

    return histogram


def create_lut(histogram: Dict[int, int], item_count: int) -> Dict[int, int]:
    """create_lut.

    :param histogram:
    :type histogram: Dict[int, int]
    :param item_count:
    :type item_count: int
    :rtype: Dict[int, int]
    """
    lut = {i: 0 for i in range(0, 256)}

    probability_sum = 0

    for i, h in histogram.items():
        probability_sum += h
        lut[i] = probability_sum * 255 / item_count

    return lut


def equallize_histogram(
    image: np.ndarray, color_index: Union[Tuple[int], List[int], int] = 0
) -> np.ndarray:
    """equallize_histogram.

    :param image:
    :type image: np.ndarray
    :param color_index:
    :type color_index: Union[Tuple[int], List[int], int]
    :rtype: np.ndarray
    """
    values = image[..., color_index]

    histogram = create_histogram(values)
    item_count = image.shape[0] * image.shape[1]

    look_up_table = create_lut(histogram, item_count)

    equallized = image.copy()

    for i, row in enumerate(values):
        for j, pixel in enumerate(row):
            mean_value = np.round(pixel.mean())

            if mean_value == 0:
                continue

            new_mean_value = look_up_table[int(mean_value)]
            equallized[i, j, color_index] = np.clip(
                np.round(pixel.astype(np.float32) / mean_value * new_mean_value), 0, 255
            )

    return equallized
