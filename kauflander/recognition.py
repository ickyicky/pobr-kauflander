import numpy as np
from .identification import SegmentFeatureExtractor, BoundingBox
from typing import Dict, List, Tuple


def recognize_shapes(
    segments: List[SegmentFeatureExtractor], recipes: Dict[str, Dict[str, List[int]]]
) -> Dict[str, List[SegmentFeatureExtractor]]:
    """recongize_shapes.

    :param segments:
    :type segments: List[SegmentFeatureExtractor]
    :param recipes:
    :type recipes: Dict
    :rtype: Dict
    """
    recognized_shapes = {}

    for shape in recipes:
        recognized_shapes[shape] = []

        for segment in segments:
            if (segment.central_moments <= recipes[shape]["max"]).all() and (
                segment.central_moments >= recipes[shape]["min"]
            ).all():
                recognized_shapes[shape].append(segment)

    return recognized_shapes


def recognize_logo(
    recognized_shapes: Dict[str, List[SegmentFeatureExtractor]]
) -> List[Tuple[BoundingBox, List[SegmentFeatureExtractor]]]:
    """recognize_logo.

    :param recognized_shapes:
    :type recognized_shapes: Dict[str, List[SegmentFeatureExtractor]]
    :rtype: List[Tuple[BoundingBox, List[SegmentFeatureExtractor]]]
    """
    recognized_logos = []

    for frame in recognized_shapes["frame"]:
        bounding_box = frame.get_bounding_box()
        triangles = [
            s
            for s in recognized_shapes["triangle"]
            if bounding_box.contains(s.get_bounding_box())
        ]
        squares = [
            s
            for s in recognized_shapes["square"]
            if bounding_box.contains(s.get_bounding_box())
        ]
        segments = triangles + squares
        segments.append(frame)

        if len(triangles) == 2 and len(squares) == 2 and len(set(segments)) == 5:
            recognized_logos.append((bounding_box, segments))

    return recognized_logos
