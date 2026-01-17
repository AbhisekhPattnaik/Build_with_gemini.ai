import cv2
import os
import numpy as np

OP3 = r"D:\gemini\oam_project\patch_03_patches"
PIT_LIST = r"D:\OAM_Project\data\pit_list.txt"

alive = 0
dead = 0

with open(PIT_LIST) as f:
    names = f.readlines()

for name in names:
    name = name.strip()
    path = os.path.join(OP3, name)

    if not os.path.exists(path):
        continue

    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([35, 40, 40])
    upper = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    green = cv2.countNonZero(mask)

    if green > 80:
        alive += 1
    else:
        dead += 1

print("Alive saplings:", alive)
print("Dead saplings:", dead)
print("Survival %:", alive*100/(alive+dead+1))
