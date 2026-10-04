# -*- coding: utf-8 -*-
"""Xep 289 anh da xoa ✦ theo DUNG THU TU CANH -> img_seq/img_001.png ...

Doc ban do tu IMG_ASSIGN.txt (sinh boi match_imgs_38.py tu nhan soi bang MAT).
Ten file co SO THU TU la hop dong voi `scene_render.py --photo-inorder`, vi o do
thu tu canh = thu tu TEN FILE (sorted). Doi ten o day, khong doi o renderer.
"""
import sys, os, re, io, glob, shutil
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-chouhen\06_VIDEO\38_enpitsu-no-meibo"
CLEAN = os.path.join(VD, "img_clean")
SEQ = os.path.join(VD, "img_seq")
SRC = r"C:\Users\tuana\Downloads\Tháng 9 17 - 19_43"

src_order = sorted(glob.glob(os.path.join(SRC, "*.jpeg")), key=lambda p: os.path.getmtime(p))
by_id = {i: os.path.splitext(os.path.basename(p))[0] + ".png"
         for i, p in enumerate(src_order, 1)}

pairs = []
for ln in io.open(os.path.join(VD, "IMG_ASSIGN.txt"), encoding="utf-8"):
    m = re.match(r"\s*(\d+)\s+(\S+)\s+(\S+)\s+pov=(\d)\s+<-\s+anh #(\d+)", ln)
    if m:
        pairs.append((int(m.group(1)), m.group(2), m.group(3), int(m.group(5))))
pairs.sort()
print("cap canh<-anh:", len(pairs))
assert len({p[3] for p in pairs}) == len(pairs), "co anh bi dung 2 lan"

if os.path.isdir(SEQ):
    shutil.rmtree(SEQ)
os.makedirs(SEQ)
miss = []
for n, sid, preset, imid in pairs:
    src = os.path.join(CLEAN, by_id[imid])
    if not os.path.exists(src):
        miss.append((n, by_id[imid]))
        continue
    shutil.copy2(src, os.path.join(SEQ, "img_%03d_%s_%s.png" % (n, sid, preset)))
print("da xep:", len(pairs) - len(miss), "| thieu:", len(miss), miss[:5])
print("->", SEQ)
