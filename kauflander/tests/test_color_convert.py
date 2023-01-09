from kauflander.color_conversion import convert_bgr_to_csv
import cv2
import numpy as np


def test_convert_bgr_to_hsv(image):
    result = cv2.cvtColor(convert_bgr_to_csv(image), cv2.COLOR_HSV2BGR)
    difference = result - image
    tolerance = 10
    assert ((difference < tolerance) | (difference > (255 - tolerance))).all()
