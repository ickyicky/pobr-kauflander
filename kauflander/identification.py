import numpy as np
from typing import List, Any


class SegmentFeatureExtractor:
    """SegmentFeatureExtractor."""

    def __init__(self, mask: np.ndarray, color: np.ndarray) -> None:
        """__init__.

        :param color:
        :type color: List[np.ndarray]
        :param mask:
        :type mask: np.ndarray
        :rtype: None
        """
        self.color = color
        self.mask = mask
        self.where = np.stack(np.where((mask == color).all(2))).swapaxes(0, 1)
        self.area = self.where.shape[0]

    def calculate_moments(self) -> None:
        """calculate_moments.

        Calculates M1 to M7

        :rtype: None
        """
        self.moment_0_0 = self.find_moment(0, 0)
        self.moment_1_0 = self.find_moment(1, 0)
        self.moment_0_1 = self.find_moment(0, 1)

        self.i_center = self.moment_1_0 / self.moment_0_0
        self.j_center = self.moment_0_1 / self.moment_0_0

        central_moment_1_1 = self.find_central_moment(1, 1)
        central_moment_0_2 = self.find_central_moment(0, 2)
        central_moment_2_0 = self.find_central_moment(2, 0)
        central_moment_1_2 = self.find_central_moment(1, 2)
        central_moment_2_1 = self.find_central_moment(2, 1)
        central_moment_3_0 = self.find_central_moment(3, 0)
        central_moment_0_3 = self.find_central_moment(0, 3)

        M1 = (central_moment_2_0 + central_moment_0_2) / np.power(self.moment_0_0, 2)
        M2 = (
            np.power((central_moment_2_0 - central_moment_0_2), 2)
            + 4 * np.power(central_moment_1_1, 2)
        ) / np.power(self.moment_0_0, 4)
        M3 = (
            np.power((central_moment_3_0 - 3 * central_moment_1_2), 2)
            + np.power((3 * central_moment_2_1 - central_moment_0_3), 2)
        ) / np.power(self.moment_0_0, 5)
        M4 = (
            np.power((central_moment_3_0 + central_moment_1_2), 2)
            + np.power((central_moment_2_1 + central_moment_0_3), 2)
        ) / np.power(self.moment_0_0, 5)
        M5 = (
            (central_moment_3_0 - 3 * central_moment_1_2)
            * (central_moment_3_0 + central_moment_1_2)
            * (
                np.power((central_moment_3_0 + central_moment_1_2), 2)
                - 3 * np.power((central_moment_2_1 + central_moment_0_3), 2)
            )
            + (3 * central_moment_2_1 - central_moment_0_3)
            * (central_moment_2_1 + central_moment_0_3)
            * (
                3 * np.power((central_moment_3_0 + central_moment_1_2), 2)
                - np.power((central_moment_2_1 + central_moment_0_3), 2)
            )
        ) / np.power(self.moment_0_0, 10)
        M6 = (
            (central_moment_2_0 - central_moment_0_2)
            * (
                (
                    np.power((central_moment_3_0 + central_moment_1_2), 2)
                    - np.power((central_moment_2_1 + central_moment_0_3), 2)
                )
            )
            + 4
            * central_moment_1_1
            * (central_moment_3_0 + central_moment_1_2)
            * (central_moment_2_1 + central_moment_0_3)
        ) / np.power(self.moment_0_0, 7)
        M7 = (
            central_moment_2_0 * central_moment_0_2 - np.power(central_moment_1_1, 2)
        ) / np.power(self.moment_0_0, 4)

        W4 = self.area / np.sqrt(
            2
            * np.pi
            * np.power((self.where - (self.j_center, self.i_center)), (2, 2)).sum()
        )

        self.central_moments = np.array((M1, M2, M3, M4, M5, M6, M7, W4))

    def find_moment(self, p: int, q: int) -> int:
        """find_moment.

        :param p:
        :type p: int
        :param q:
        :type q: int
        :rtype: int
        """
        values = np.power(self.where, (q, p))
        return (values[..., 0] * values[..., 1]).sum()

    def find_central_moment(self, p: int, q: int) -> int:
        """find_central_moment.

        :param p:
        :type p: int
        :param q:
        :type q: int
        :rtype: int
        """
        values = np.power((self.where - (self.j_center, self.i_center)), (q, p))
        return (values[..., 0] * values[..., 1]).sum()

    def get_bounding_box(self) -> "BoundingBox":
        """get_bounding_box.

        :rtype: "BoundingBox"
        """
        return BoundingBox(np.min(self.where, 0), np.max(self.where, 0))

    def __hash__(self) -> Any:
        """__hash__.

        :rtype: Any
        """
        return hash(tuple(self.color))

    def __eq__(self, other) -> bool:
        """__eq__.

        :param other:
        :rtype: bool
        """
        return (self.color == other.color).all()

    @classmethod
    def get_segments_for(
        cls,
        mask: np.ndarray,
        colors: List[np.ndarray],
        min_size: float,
        max_size: float,
    ) -> "List[SegmentFeatureExtractor]":
        """get_segments_for.

        :param mask:
        :type mask: np.ndarray
        :param colors:
        :type colors: List[np.ndarray]
        :param min_size:
        :type min_size: float
        :param max_size:
        :type max_size: float
        :rtype: "List[SegmentFeatureExtractor]"
        """
        segments_feature_extractors = [
            cls(
                mask,
                color,
            )
            for color in colors
        ]

        min_size = mask.shape[0] * mask.shape[1] * (min_size**2)
        max_size = mask.shape[0] * mask.shape[1] * (max_size**2)

        segments_feature_extractors = [
            segment
            for segment in segments_feature_extractors
            if (segment.area < max_size and segment.area > min_size)
        ]

        for segment in segments_feature_extractors:
            segment.calculate_moments()

        return segments_feature_extractors


class BoundingBox:
    """BoundingBox."""

    def __init__(self, mins: np.ndarray, maxes: np.ndarray):
        """__init__.

        :param center:
        :type center: Tuple[int, int]
        :param dims:
        :type dims: Tuple[int, int]
        """
        self.mins = mins
        self.maxes = maxes

    def contains(self, box: "BoundingBox") -> bool:
        """contains.

        :param box:
        :type box: "BoundingBox"
        :rtype: bool
        """
        return (self.mins < box.mins).all() and (self.maxes > box.maxes).all()
