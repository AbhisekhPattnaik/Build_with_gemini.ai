"""Classifier stubs for presence/absence at pit locations."""

from pathlib import Path

def classify_patch(image, x, y, radius_px):
    """Given an image (numpy array) and pixel center (x,y), return True if green vegetation present.

    This is a heuristic fallback: convert to HSV and check green pixel ratio.
    """
    import numpy as np
    import cv2

    h, w = image.shape[:2]
    x = int(round(x)); y = int(round(y))
    r = int(max(3, round(radius_px*1.5)))
    x0, x1 = max(0, x-r), min(w, x+r)
    y0, y1 = max(0, y-r), min(h, y+r)
    patch = image[y0:y1, x0:x1]
    if patch.size == 0:
        return False
    hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
    lower = np.array([30, 30, 30])
    upper = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    green_ratio = (mask>0).sum() / mask.size
    return green_ratio > 0.05
