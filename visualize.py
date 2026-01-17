import os

BASE = r"D:\gemini"

for root, dirs, files in os.walk(BASE):
    if "patch" in root.lower() or "alive" in root.lower() or "dead" in root.lower():
        print("\nFOLDER:", root)
        print("FILES:", files[:5])

for root, dirs, files in os.walk(r"D:\gemini"):
    for f in files:
        if f.lower().endswith((".jpg",".png",".tif")) and ("ortho" in f.lower() or "full" in f.lower()):
            print(root, f)
