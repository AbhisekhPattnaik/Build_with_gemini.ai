import cv2
import os

INPUT = r"D:\gemini\oam_project\patch_01_patches"
OUTPUT = r"D:\OAM_Project\data\detected_preview"

os.makedirs(OUTPUT, exist_ok=True)

count = 0

for img_name in os.listdir(INPUT)[:30]:   # only first 30 images
    path = os.path.join(INPUT, img_name)
    img = cv2.imread(path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 300:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imwrite(os.path.join(OUTPUT, img_name), img)
    count += 1

print("Saved preview images:", count)
