import argparse
import cv2
import numpy as np
from .color_conversion import convert_bgr_to_hsv
from .reshape import reshape
from .filter import filter_gaussian, filter_median
from .histogram import equallize_histogram
from .segmentation import threshold, flood_fill
from .identification import SegmentFeatureExtractor
from .recognition import recognize_shapes, recognize_logo
from .utils import show_segments, draw_bounding_box


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("INPUT", metavar="FILE", help="input file")
    parser.add_argument("OUTPUT", metavar="FILE", nargs="?", help="output file")
    parser.add_argument(
        "-s",
        "--size-factor",
        action="store",
        type=float,
        default=0.5,
        help="size factor, multiplicator",
    )
    parser.add_argument(
        "-g",
        "--filter-gaussian",
        action="store_true",
        help="filter with gaussian filter",
    )
    parser.add_argument(
        "-m", "--filter-median", action="store_true", help="filter with median filter"
    )
    parser.add_argument(
        "-e", "--equallize-histogram", action="store_true", help="equallize histogram"
    )
    parser.add_argument(
        "-f",
        "--segment-minimum-size",
        action="store",
        type=float,
        default=0.01,
        help="minimum segment size in percentage in 1d",
    )
    parser.add_argument(
        "-t",
        "--segment-maximum-size",
        action="store",
        type=float,
        default=0.3,
        help="maximum segment size in percentage in 1d",
    )
    parser.add_argument(
        "-r",
        "--result",
        choices=["mask", "box"],
        action="store",
        type=str,
        default="box",
        help="What result to produce, either mask or original image with bounging box",
    )
    parser.add_argument(
        "--show-color-mask",
        action="store_true",
        help="shows color mask",
    )
    parser.add_argument(
        "--show-segments",
        action="store_true",
        help="shows all segments",
    )
    parser.add_argument(
        "--show-shapes",
        action="store_true",
        help="shows all recognized shapes",
    )

    moments = {
        "triangle": {
            "min": [
                0.2,
                0.0072,
                0.0028,
                0.0001,
                -384.0,
                -0.000285,
                0.0078,
                0.83,
            ],
            "max": [
                0.231,
                0.016,
                0.0063,
                0.00031,
                660.432,
                1.68798e-05,
                0.0096,
                0.885,
            ],
        },
        "square": {
            "min": [
                0.164,
                2.149e-05,
                0.0,
                0.0,
                -0.05,
                -4.513e-07,
                0.0066,
                0.9643,
            ],
            "max": [
                0.17115,
                0.001381,
                4.042e-05,
                8.95e-07,
                0.002,
                6.242e-07,
                0.007,
                0.985,
            ],
        },
        "frame": {
            "min": [
                1.38,
                0.00045,
                -0.0167,
                -0.0075,
                -201000000000.0,
                -46230.5029,
                0.47,
                0.26,
            ],
            "max": [
                2.304,
                0.1105,
                0.0182,
                0.01536,
                272345000000000.0,
                25.18,
                1.33,
                0.34,
            ],
        },
    }

    red_bounds = [
        {
            "min": (0, 145, 40),
            "max": (20, 255, 255),
        },
        {
            "min": (170, 145, 40),
            "max": (255, 255, 255),
        },
    ]

    args = parser.parse_args()

    image = cv2.imread(args.INPUT)
    subject = reshape(image, args.size_factor)

    if args.filter_gaussian:
        subject = filter_gaussian(subject)

    if args.filter_median:
        subject = filter_median(subject)

    subject = convert_bgr_to_hsv(subject)

    if args.equallize_histogram:
        subject = equallize_histogram(subject, 2)

    mask = threshold(subject, red_bounds[0]["min"], red_bounds[0]["max"]) | threshold(
        subject, red_bounds[1]["min"], red_bounds[1]["max"]
    )
    if args.show_color_mask:
        cv2.imshow("color mask", mask)
        cv2.waitKey(0)

    segments_mask, segments_colors = flood_fill(mask)

    segments = SegmentFeatureExtractor.get_segments_for(
        segments_mask,
        segments_colors,
        args.segment_minimum_size,
        args.segment_maximum_size,
    )

    if args.show_segments:
        show_segments(
            segments,
            shape=segments_mask.shape,
        )

    recognized_shapes = recognize_shapes(segments, moments)

    if args.show_shapes:
        bm = show_segments(
            recognized_shapes["triangle"],
            shape=segments_mask.shape,
            color=(255, 0, 0),
            show=False,
        )
        bm = show_segments(
            recognized_shapes["square"], bitmap=bm, color=(0, 255, 0), show=False
        )
        show_segments(recognized_shapes["frame"], bitmap=bm, color=(0, 0, 255))

    recognized_logos = recognize_logo(recognized_shapes)

    if args.result == "mask":
        result = None
        for logo in recognized_logos:
            result = show_segments(
                logo[1],
                color=(255, 255, 255),
                shape=segments_mask.shape,
                bitmap=result,
                show=False,
            )
        result = reshape(result, 1 / args.size_factor)
    else:
        result = image
        for logo in recognized_logos:
            result = draw_bounding_box(
                result, logo[0], scale_factor=(1 / args.size_factor)
            )

    if args.OUTPUT:
        cv2.imwrite(args.OUTPUT, result)
    else:
        cv2.imshow("result", result)
        cv2.waitKey(0)
