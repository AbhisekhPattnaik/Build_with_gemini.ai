import cv2, os

OP1_IMG = r"D:\gemini\oam_project\op1_ortho.jpg"
OP3_IMG = r"D:\gemini\oam_project\op3_ortho.jpg"

OUT1 = r"D:\gemini\oam_project\patches_op1"
OUT3 = r"D:\gemini\oam_project\patches_op3"

os.makedirs(OUT1, exist_ok=True)
os.makedirs(OUT3, exist_ok=True)

img1 = cv2.imread(OP1_IMG)
img3 = cv2.imread(OP3_IMG)

if img1 is None or img3 is None:
    print("❌ Ortho images not loaded. Check path and file name.")
    exit()

h, w, _ = img1.shape
PATCH = 128

count = 0

for y in range(0, h-PATCH, PATCH):
    for x in range(0, w-PATCH, PATCH):

        p1 = img1[y:y+PATCH, x:x+PATCH]
        p3 = img3[y:y+PATCH, x:x+PATCH]

        name = f"{x}_{y}.jpg"

        cv2.imwrite(os.path.join(OUT1, name), p1)
        cv2.imwrite(os.path.join(OUT3, name), p3)

        count += 1

print("✅ Matched patches created:", count)
