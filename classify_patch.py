import cv2, os, numpy as np

OP1 = r"D:\gemini\oam_project\patch_01_patches"
OP3 = r"D:\gemini\oam_project\patch_03_patches"

ALIVE_DIR = r"D:\gemini\oam_project\alive_patches"
DEAD_DIR  = r"D:\gemini\oam_project\dead_patches"

os.makedirs(ALIVE_DIR, exist_ok=True)
os.makedirs(DEAD_DIR, exist_ok=True)

alive = 0
dead = 0

op3_files = os.listdir(OP3)

for f1 in os.listdir(OP1):

    if not f1.endswith(".png"):
        continue

    # extract patch coord part: _x_y.png
    coord = "_".join(f1.split("_")[-2:])

    match = None
    for f3 in op3_files:
        if f3.endswith(coord):
            match = f3
            break

    if match is None:
        continue

    img = cv2.imread(os.path.join(OP3, match))
    if img is None:
        continue

    h,w,_ = img.shape
    center = img[h//4:3*h//4, w//4:3*w//4]

    hsv = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)
    lower = np.array([35,40,40])
    upper = np.array([85,255,255])
    green = cv2.countNonZero(cv2.inRange(hsv, lower, upper))

    g = center[:,:,1].astype(float)
    r = center[:,:,2].astype(float)
    veg = (g-r)/(g+r+1e-5)

    if green > 60 and veg.mean() > 0.03:
        alive += 1
        cv2.imwrite(os.path.join(ALIVE_DIR, match), img)
    else:
        dead += 1
        cv2.imwrite(os.path.join(DEAD_DIR, match), img)

print("Alive:", alive)
print("Dead:", dead)
print("Survival %:", round(alive*100/(alive+dead+1),2))

import cv2, os, numpy as np

PATCH_DIR = r"D:\gemini\oam_project\patch_03_patches"
DEAD_DIR  = r"D:\gemini\oam_project\dead_patches"

coords = []

for f in os.listdir(DEAD_DIR):
    if f.endswith(".png"):
        parts = f.split("_")
        x = int(parts[-2])
        y = int(parts[-1].replace(".png",""))
        coords.append((x,y))

# estimate map size
xs = [c[0] for c in coords]
ys = [c[1] for c in coords]

W = max(xs) + 1024
H = max(ys) + 1024

map_img = np.zeros((H, W, 3), dtype=np.uint8)

for (x,y) in coords:
    cv2.rectangle(map_img, (x,y), (x+1024,y+1024), (0,0,255), -1)

cv2.imwrite(r"D:\gemini\oam_project\casualty_grid_map.png", map_img)
print("Saved casualty_grid_map.png")
