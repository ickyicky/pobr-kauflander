import numpy as np
from enum import Enum


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
    new_shape = np.round(np.array(image.shape[:2]) * scale_factor).astype(np.uint)
    reshaped = np.zeros((*new_shape, 3), dtype=image.dtype)

    for x in range(new_shape[0]):
        for y in range(new_shape[1]):
            prim_coords = np.array((x, y)) / scale_factor
            base_coords = np.floor(prim_coords)

            neighbours = np.array(
                (
                    base_coords,
                    np.mod(base_coords + (0, 1), image.shape[:2]),
                    np.mod(base_coords + (1, 0), image.shape[:2]),
                    np.mod(base_coords + (1, 1), image.shape[:2]),
                )
            ).astype(np.uint)
            distances = np.sqrt(np.sum(np.power(neighbours - prim_coords, 2), 1))
            lowest_distance = np.argmin(distances)
            reshaped[x, y] = image[tuple(neighbours[lowest_distance])]

    return reshaped
