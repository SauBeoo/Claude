# -*- coding: utf-8 -*-
r"""Nap anh GEN LAI (vong 2+) de len slide_NN.jpg — cung pipeline cat ✦ nhu vong 1.

    python tools\ingest_regen_16.py --src "C:\Users\tuana\Downloads\download (5)" \
        --take 47=Person_holding_pharmacy_bag 53=Banana_snapped_in_two ...

Hoac de trong --take thi doc bang ACCEPT ben duoi.
Ban cu luon duoc doi ten thanh slide_NN.rejN.jpg trong _slides_orig/ truoc khi ghi de.
"""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "16_banana-yoru-toire"
DST = VD / "slides_img_photo"
BAK = VD / "_slides_orig"

# slide -> ten file (bo duoi _<timestamp>.jpeg) — chi nhung ban DA DUYET
ACCEPT = {
    47: "Person_holding_pharmacy_bag",
    53: "Banana_snapped_in_two",
    59: "Rice_bowl_and_banana_arrangement",
    76: "Feet_resting_on_dining_table",
}

CUT_X, TARGET = 1248, 16 / 9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    a = ap.parse_args()
    from PIL import Image
    src = Path(a.src)
    by = {}
    for f in list(src.glob("*.jpeg")) + list(src.glob("*.jpg")):
        by[f.name.rsplit("_", 1)[0]] = f

    miss = [k for k in ACCEPT.values() if k not in by]
    if miss:
        print("[LOI] khong thay file:", miss)
        return 1

    BAK.mkdir(parents=True, exist_ok=True)
    for i, name in sorted(ACCEPT.items()):
        old = DST / f"slide_{i:02d}.jpg"
        if old.exists():
            n = 1
            while (BAK / f"slide_{i:02d}.rej{n}.jpg").exists():
                n += 1
            shutil.copy2(old, BAK / f"slide_{i:02d}.rej{n}.jpg")
        f = by[name]
        shutil.copy2(f, BAK / f.name)
        im = Image.open(f).convert("RGB")
        w, h = im.size
        cx = CUT_X if w == 1376 else int(w * 0.907)
        im = im.crop((0, 0, cx, h))
        nh = int(cx / TARGET)
        im = im.crop((0, 0, cx, nh)) if nh < h else im.crop((0, 0, int(h * TARGET), h))
        im.resize((1920, 1080), Image.LANCZOS).save(old, quality=94)
        print(f"  slide_{i:02d}  <- {f.name[:46]}   ({w}x{h} -> cat x<{cx} -> 1920x1080)")
    print(f"\nOK {len(ACCEPT)} slide da thay. Ban cu luu o {BAK.name}/slide_NN.rejN.jpg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
