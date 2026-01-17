import os
import cv2

# 👉 CHANGE THIS PATH to your RAW image folder (example: post-pitting)
IMAGE_FOLDER = r"D:\gemini\oam\debati\Benkmura VF-20260117T124255Z-1-003\Benkmura VF\Raw Data\Post-Pitting"

sizes = {}

for file in os.listdir(IMAGE_FOLDER):
    if file.lower().endswith((".jpg", ".png")):
        path = os.path.join(IMAGE_FOLDER, file)
        img = cv2.imread(path)

        if img is None:
            print("Cannot read:", file)
            continue

        h, w, c = img.shape
        sizes[(h, w)] = sizes.get((h, w), 0) + 1

print("\nImage Size Summary:\n")
for size, count in sizes.items():
    print(f"{size} : {count} images")
