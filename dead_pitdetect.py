import cv2
import numpy as np
import csv

# -------- PATHS (EDIT THESE) ----------
IMG1_PATH = r"D:\gemini\oam_project\op1_ortho.jpg"  # before
IMG3_PATH = r"D:\gemini\oam_project\op3_ortho.jpg"  # after

PATCH = 64   # grid size
GREEN_THRESH = 0.08  # 8% green area
# -------------------------------------


img1 = cv2.imread(IMG1_PATH)
img3 = cv2.imread(IMG3_PATH)

if img1 is None or img3 is None:
    print("Images not loaded. Check path.")
    exit()

h, w, _ = img1.shape

dead_points = []
alive = 0
dead = 0

vis = img3.copy()

for y in range(0, h, PATCH):
    for x in range(0, w, PATCH):

        p1 = img1[y:y+PATCH, x:x+PATCH]
        p3 = img3[y:y+PATCH, x:x+PATCH]

        if p1.shape[0] < PATCH or p1.shape[1] < PATCH:
            continue

        hsv1 = cv2.cvtColor(p1, cv2.COLOR_BGR2HSV)
        hsv3 = cv2.cvtColor(p3, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv1, (35,40,40), (85,255,255))
        mask3 = cv2.inRange(hsv3, (35,40,40), (85,255,255))

        g1 = np.sum(mask1 > 0) / (PATCH*PATCH)
        g3 = np.sum(mask3 > 0) / (PATCH*PATCH)

        cx = x + PATCH//2
        cy = y + PATCH//2

        if g1 > GREEN_THRESH and g3 < GREEN_THRESH:
            dead += 1
            dead_points.append((cx, cy))
            cv2.circle(vis, (cx, cy), 5, (0,0,255), -1)
        elif g3 > GREEN_THRESH:
            alive += 1
            cv2.circle(vis, (cx, cy), 3, (0,255,0), -1)

print("Alive pits:", alive)
print("Dead pits:", dead)

# save image
cv2.imwrite("dead_pits_visual.png", vis)
print("Saved: dead_pits_visual.png")

# save coordinates
with open("dead_pits_pixels.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["x_pixel", "y_pixel"])
    writer.writerows(dead_points)

print("Saved: dead_pits_pixels.csv")

print("Done.")