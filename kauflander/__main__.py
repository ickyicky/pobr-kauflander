import argparse
import cv2
import numpy as np
from .color_conversion import convert_bgr_to_csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("INPUT", metavar="FILE", help="input file")
    parser.add_argument("OUTPUT", metavar="FILE", help="output file")

    args = parser.parse_args()

    image = cv2.imread(args.INPUT)
    converted = convert_bgr_to_csv(image)
    converted = cv2.cvtColor(converted, cv2.COLOR_HSV2BGR)
    cv2.imwrite(args.OUTPUT, converted)
