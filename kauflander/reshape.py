import numpy as np
from enum import Enum
from typing import Tuple


def reshape(image, scale_factor: float) -> np.ndarray:
    """reshape.

    Nearest Neighbour algorithm.

    For each pixel of resized image we determine which pixel
    from original image is the closest one and take it's value

    :param image:
    :param scale_factor:
    :type scale_factor: float
    :rtype: np.ndarray
    """
    shape = image.shape[:2]
    new_shape = np.round(np.array(shape) * scale_factor).astype(np.uint)
    reshaped = np.zeros((*new_shape, 3), dtype=image.dtype)

    for x in range(new_shape[0]):
        for y in range(new_shape[1]):
            reshaped[x, y] = image[get_nearest_neighbour((x, y), scale_factor, shape)]

    return reshaped


def get_nearest_neighbour(
    point: Tuple[int, int], scale_factor: float, shape: Tuple[int, int]
) -> Tuple[int, int]:
    """get_nearest_neighbour.

    :param point:
    :type point: Tuple[int, int]
    :param scale_factor:
    :type scale_factor: float
    :rtype: Tuple[int, int]
    """
    prim_coords = np.array(point) / scale_factor
    base_coords = np.floor(prim_coords)

    neighbours = np.array(
        (
            base_coords,
            np.mod(base_coords + (0, 1), shape),
            np.mod(base_coords + (1, 0), shape),
            np.mod(base_coords + (1, 1), shape),
        )
    ).astype(np.uint)
    distances = np.sqrt(np.sum(np.power(neighbours - prim_coords, 2), 1))
    lowest_distance = np.argmin(distances)
    return tuple(neighbours[lowest_distance])
