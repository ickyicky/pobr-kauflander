import numpy as np


def filter_gaussian(image: np.ndarray) -> np.ndarray:
    """filter_gaussian.

    :param image:
    :type image: np.ndarray
    :rtype: np.ndarray
    """
    gaussian_matrix = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    filtered = image.astype(np.uint)
    rows, cols, _ = image.shape
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            fragment = image[x - 1 : x + 2, y - 1 : y + 2]
            filtered[x, y] = np.array(
                [
                    np.multiply(fragment[..., 0], gaussian_matrix).sum(),
                    np.multiply(fragment[..., 1], gaussian_matrix).sum(),
                    np.multiply(fragment[..., 2], gaussian_matrix).sum(),
                ]
            )
    return (filtered / gaussian_matrix.sum()).astype(image.dtype)


def filter_median(image: np.ndarray) -> np.ndarray:
    """filter_median.

    :param image:
    :type image: np.ndarray
    :rtype: np.ndarray
    """
    filtered = image.copy()
    rows, cols, _ = image.shape
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            fragment = np.reshape(
                image[x - 1 : x + 2, y - 1 : y + 2].astype(image.dtype), (9, 3)
            )

            for i in range(3):
                fragment[..., i].sort()

            filtered[x, y] = fragment[5]
    return filtered.astype(image.dtype)
