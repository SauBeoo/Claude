# -*- coding: utf-8 -*-
r"""ingest_art21.py — nhan 11 ANH TINH thay cho clip bang trang cua video 21.

Anh vao: mot thu muc chua 11 file (thu tu = thu tu trong `flow21_REDO_IMG.txt`).
Anh ra:  `06_VIDEO/<STEM>/clips/a21_<key>.png`, **1920x1080**.

LAM 3 VIEC:
 ① 🔴 XOA WATERMARK — bat buoc theo `media-library.md` §2.10 ⑤b (user: *"luc nao
    cung phai xoa watermark cho toi"*). Cach: **CAT KHUNG** (khong patch — patch
    de lai vet tren nen co van).
    ⚠️ **PHAI DO LAI THEO TUNG LO** (§2.10 ⑤): toa do ✦ khac nhau giua cac lo,
    va co ✦ con doi theo NEN (nen xam thi ✦ to hon, co tia dai). Chay
    `--probe <thu_muc>` truoc → no cat goc duoi-phai cua tung anh ra
    `_probe_art/` de SOI BANG MAT, roi dien `--cut <ti_le>`.
 ② 📐 CAT ve dung 16:9 roi scale 1920x1080 (anh gen thuong 1376x768 = 16:9 san,
    nhung sau khi cat mep phai thi phai trim lai chieu cao).
 ③ 📛 DOI TEN theo `flow21_REDO_IMG_TENFILE.txt`.

CHAY:  python tools/ingest_art21.py --probe <thu_muc>     # soi watermark truoc
       python tools/ingest_art21.py <thu_muc> [--cut 0.908]
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image  # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
OUT = os.path.join(VD, "clips")
W, H = 1920, 1080
EXT = (".png", ".jpg", ".jpeg", ".webp")


def rows():
    p = os.path.join(VD, "flow21_REDO_IMG_TENFILE.txt")
    out = []
    for ln in io.open(p, encoding="utf-8").read().split("\n")[1:]:
        c = ln.split("\t")
        if len(c) >= 4 and c[0].strip().isdigit():
            out.append((int(c[0]), c[2].strip(), c[3].strip()))
    return out


def src_files(d):
    fs = [f for f in sorted(os.listdir(d)) if f.lower().endswith(EXT)]
    return [os.path.join(d, f) for f in fs]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    probe = "--probe" in sys.argv
    cut = 0.908
    for i, a in enumerate(sys.argv):
        if a == "--cut" and i + 1 < len(sys.argv):
            cut = float(sys.argv[i + 1])
    if not args:
        print(__doc__.split("CHAY:")[1])
        return 1
    d = args[0]
    if not os.path.isdir(d):
        print(f"🔴 khong thay thu muc: {d}")
        return 1

    R = rows()
    fs = src_files(d)
    print(f"{len(fs)} anh trong thu muc · {len(R)} cho can lap")
    for p in fs[:3]:
        print(f"   {os.path.basename(p):40s} {Image.open(p).size}")

    if probe:
        pd = os.path.join(VD, "_probe_art")
        os.makedirs(pd, exist_ok=True)
        for p in fs:
            im = Image.open(p).convert("RGB")
            w, h = im.size
            # goc duoi-phai, ~20% x 18% — du rong de thay ca tia dai
            im.crop((int(w * 0.80), int(h * 0.82), w, h)).save(
                os.path.join(pd, "wm_" + os.path.basename(p) + ".png"))
        print(f"\n→ {pd}  ({len(fs)} anh goc duoi-phai)")
        print("   SOI BANG MAT roi chay lai khong co --probe, kem --cut <ti_le>")
        return 0

    if len(fs) != len(R):
        print(f"🔴 so anh ({len(fs)}) khac so cho ({len(R)}) — dat dung 11 anh "
              f"theo thu tu `flow21_REDO_IMG.txt` roi chay lai")
        return 1

    os.makedirs(OUT, exist_ok=True)
    for (j, fn, key), p in zip(R, fs):
        im = Image.open(p).convert("RGB")
        w, h = im.size
        nw = int(w * cut)                      # bo mep phai (nơi ✦ dong)
        nh = int(round(nw / (W / H)))          # trim chieu cao ve dung 16:9
        if nh > h:                             # anh vao hep hon 16:9
            nh = h
            nw = int(round(nh * (W / H)))
        im.crop((0, 0, nw, nh)).resize((W, H), Image.LANCZOS).save(
            os.path.join(OUT, fn))
        print(f"[{j:2d}/{len(R)}] {fn:32s} {w}x{h} -> cat {nw}x{nh} -> {W}x{H}")
    print(f"\nXONG: {OUT}")
    print("   Buoc ke: python tools/build_remotion_21.py  (GATE asset phai ✅ 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
