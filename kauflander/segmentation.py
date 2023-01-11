import numpy as np
from typing import Tuple, Union, Optional


def threshold(
    image: np.ndarray,
    lower_range: Union[Tuple[int], int],
    upper_range: Union[Tuple[int], int],
    axis: Optional[Union[int, Tuple[int]]] = None,
) -> np.ndarray:
    """threshold.

    :param imge:
    :type imge: np.ndarray
    :param lower_range:
    :type lower_range: Union[Tuple[int], int]
    :param upper_range:
    :type upper_range: Union[Tuple[int], int]
    :param axis:
    :rtype: np.ndarray
    """
    if axis is not None:
        data = image[..., axis]
    else:
        data = image

    where = np.where(((data >= lower_range) & (data <= upper_range)).all(2))

    mask = np.zeros(image.shape[:2], image.dtype)
    mask[where] = 255
    return mask
