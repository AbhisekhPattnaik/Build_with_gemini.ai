import cv2
import os
import numpy as np

OP3 = r"D:\gemini\oam_project\patch_03_patches"

alive = 0
dead = 0

for name in os.listdir(OP3):
    path = os.path.join(OP3, name)
    img = cv2.imread(path)

    if img is None:
        continue

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([35, 40, 40])
    upper = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    green = cv2.countNonZero(mask)

    if green > 80:
        alive += 1
    else:
        dead += 1

print("Estimated Alive patches:", alive)
print("Estimated Dead patches:", dead)
print("Green coverage survival %:", alive*100/(alive+dead+1))
