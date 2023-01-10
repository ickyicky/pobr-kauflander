import argparse
import cv2
import numpy as np
from .color_conversion import convert_bgr_to_csv
from .reshape import reshape
from .filter import filter_gaussian, filter_median


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

    args = parser.parse_args()

    image = cv2.imread(args.INPUT)

    reshaped = reshape(image, args.size_factor)

    if args.filter_gaussian:
        reshaped = filter_gaussian(reshaped)

    if args.filter_median:
        reshaped = filter_median(reshaped)

    converted = convert_bgr_to_csv(reshaped)
    converted = cv2.cvtColor(converted, cv2.COLOR_HSV2BGR)
    cv2.imwrite(args.OUTPUT, reshaped)
