import argparse
import cv2
import numpy as np
from .color_conversion import convert_bgr_to_hsv
from .reshape import reshape
from .filter import filter_gaussian, filter_median
from .histogram import equallize_histogram


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("INPUT", metavar="FILE", help="input file")
    parser.add_argument("OUTPUT", metavar="FILE", help="output file")
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

    subject = cv2.cvtColor(subject, cv2.COLOR_HSV2BGR)
    cv2.imwrite(args.OUTPUT, subject)
