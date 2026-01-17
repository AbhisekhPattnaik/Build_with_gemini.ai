import os

OP1 = r"D:\gemini\oam_project\patch_01_patches"
OP3 = r"D:\gemini\oam_project\patch_03_patches"

c = 0
for name in os.listdir(OP1):
    if os.path.exists(os.path.join(OP3, name)):
        c += 1

print("Matching patches:", c)
print("OP1 total:", len(os.listdir(OP1)))
print("OP3 total:", len(os.listdir(OP3)))
