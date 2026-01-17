import os
import cv2

PATCH_DIR = r"D:\gemini\oam_project\patch_01_patches"
PIT_LIST = r"D:\OAM_Project\data\pit_list.txt"

f = open(PIT_LIST, "w")

count = 0

for img_name in os.listdir(PATCH_DIR):
    path = os.path.join(PATCH_DIR, img_name)
    img = cv2.imread(path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 300:
            f.write(img_name + "\n")
            count += 1
            break

f.close()
print("Pit patches found:", count)
