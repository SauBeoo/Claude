# -*- coding: utf-8 -*-
"""Rap anh video 01 kyushoku BAN 2 (2026-08-04): index theo 01_kyushoku_SLIDES.json v2."""
import os, shutil, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"E:\Claude\Projects\youtube-jp-showa"
SRC = os.path.join(ROOT, "06_VIDEO", "_asset_test")
DST = os.path.join(ROOT, "06_VIDEO", "01_kyushoku", "slides_img")
os.makedirs(DST, exist_ok=True)

def copy(src, idx):
    shutil.copyfile(os.path.join(SRC, src), os.path.join(DST, f"slide_{idx:02d}.jpg"))
    print(f"slide_{idx:02d} <- {src}")

def crop(src, idx, fx1, fy1, fx2, fy2):
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    w, h = im.size
    im.crop((int(w*fx1), int(h*fy1), int(w*fx2), int(h*fy2))).save(
        os.path.join(DST, f"slide_{idx:02d}.jpg"), quality=93)
    print(f"slide_{idx:02d} <- {src} (crop)")

# COLD OPEN lien thanh
copy("agepan_orig.jpg", 0)
copy("reitomikan_0.jpg", 1)
copy("tetrapack_0.jpg", 2)
copy("sakiware_0.jpg", 3)
# 04 = clip street
copy("kujira_orig.jpg", 5)
# 06 = drawn quiz
crop("agepan_orig.jpg", 7, .05, .28, .62, .95)
# 08 = drawn S27
crop("agepan_orig.jpg", 9, .30, .05, .75, .55)
copy("trays_0.jpg", 10)
# 11 = drawn menu
crop("kujira_orig.jpg", 12, .10, .45, .55, .95)
# 13 = drawn touban / 14 = drawn dasshifunnyu
copy("bin_gyunyu_0.jpg", 15)
copy("milkcap_0.jpg", 16)
copy("stove_0.jpg", 17)
copy("tetrapack_0.jpg", 18)
copy("milmake_0.jpg", 19)
# 20 = drawn milmake
copy("kyushoku_ban_0.jpg", 21)
copy("kinchaku_0.jpg", 22)
# 23 = clip fish dock
crop("kujira_orig.jpg", 24, .48, .40, .92, .92)
copy("softmen_0.jpg", 25)
crop("curry_0.jpg", 26, .12, .12, .88, .88)
# 27 = drawn flow
copy("peas_0.jpg", 28)
# 29-31 = drawn
# 32 = clip matsuri
copy("reitomikan_0.jpg", 33)
copy("pool_0.jpg", 34)
crop("kujira_orig.jpg", 35, .36, .17, .66, .50)
copy("sakiware_0.jpg", 36)
crop("trays_0.jpg", 37, .35, .25, 1.0, 1.0)
copy("kyushoku_ban_0.jpg", 38)
# 39/40 = clip BW
# 41 = drawn timeline
crop("trays_0.jpg", 42, .40, .0, .95, .70)
copy("kujira_orig.jpg", 43)
# 44 = drawn end card
print("XONG anh ban 2.")
