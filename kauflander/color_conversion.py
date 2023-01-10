import numpy as np


def convert_bgr_to_hsv(image: np.ndarray) -> np.ndarray:
    """convert_bgr_to_hsv.

    Algorithm inspired by wikipedia formulas for HSV
    https://en.wikipedia.org/wiki/HSL_and_HSV

    :param image:
    :type image: np.ndarray
    :rtype: np.ndarray
    """
    result = np.zeros_like(image)
    image = image / 255
    R, G, B = 2, 1, 0
    r = image[..., R]
    b = image[..., B]
    g = image[..., G]

    vmax = image.max(2)
    vmin = image.min(2)
    diff = vmax - vmin

    cmax = image.argmax(2)
    non_zeros = diff != 0.0

    where = (cmax == R) & non_zeros
    result[where, 0] = np.floor(
        (60.0 * np.mod(((g[where] - b[where]) / diff[where]), 6.0)) / 2.0
    )

    where = (cmax == G) & non_zeros
    result[where, 0] = np.floor(
        (60.0 * (((b[where] - r[where]) / diff[where]) + 2.0)) / 2.0
    )

    where = (cmax == B) & non_zeros
    result[where, 0] = np.floor(
        (60.0 * (((r[where] - g[where]) / diff[where]) + 4.0)) / 2.0
    )

    where = vmax != 0
    result[where, 1] = diff[where] / vmax[where] * 255

    result[..., 2] = vmax * 255

    return result
