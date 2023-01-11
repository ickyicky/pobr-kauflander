import numpy as np
from typing import Tuple, Union, Optional, List


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

    mask = np.zeros(image.shape[:2], dtype=np.ubyte)
    mask[where] = 255
    return mask


def flood_fill(
    mask: np.ndarray,
) -> Tuple[np.ndarray, List[np.ndarray]]:
    """flood_fill.

    :param mask:
    :type mask: np.ndarray
    :rtype: Tuple[np.ndarray, np.ndarray]
    """
    segmnets_mask = np.zeros((*mask.shape[:2], 3), dtype=np.ubyte)
    segmnets_mask[np.where(mask == 255)] = (255, 255, 255)
    colors = []
    checked = set()

    while True:
        # find next non flooded segment
        available_segments = np.stack(
            np.where((segmnets_mask == (255, 255, 255)).all(2))
        ).swapaxes(0, 1)

        if available_segments.shape[0] == 0:
            break

        if len(colors) >= 255 * 255 * 255:
            raise Exception("Too many segments, no more colors available for them")

        chosen = available_segments[np.random.choice(available_segments.shape[0])]

        while (color := np.random.randint(0, 255, 3)) in colors:
            pass

        point_queue = [chosen]

        while point_queue:
            chosen = point_queue.pop()

            checked.add(tuple(chosen))

            try:
                if mask[tuple(chosen)] == 255:
                    segmnets_mask[tuple(chosen)] = color
                    for direction in (
                        (1, 1),
                        (1, 0),
                        (1, -1),
                        (0, 1),
                        (0, -1),
                        (-1, 1),
                        (-1, 0),
                        (-1, -1),
                    ):
                        to_check = chosen + direction
                        # don't check same point multiple times
                        if tuple(to_check) not in checked:
                            point_queue.append(to_check)
            except IndexError:
                continue

    return segmnets_mask, colors
