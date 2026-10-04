# -*- coding: utf-8 -*-
r"""Nhap anh user gen -> slides_img_photo/slide_XX.jpg (video 17).

    python tools\ingest_slides_17.py "C:\Users\tuana\Downloads\download (2)"
    python tools\ingest_slides_17.py <src> --apply      # thuc su ghi file

VIEC:
  1. GHEP TEN: ten file generator dat = tom tat SUBJECT -> khop voi SUBJECT cua tung
     slot bang token overlap. In bang de soi mat, va liet ke slot CHUA co anh.
  2. XOA WATERMARK ✦ bang CACH CAT (media-library.md §2.10 ⑤b: anh slide -> CAT, khong va).
     Lo nay 1376x768, ✦ do bang MAT o 8+4 anh: nam ben PHAI x=1250 (0,908W).
     -> cat phai tai 1250, roi center-crop doc ve 16:9 (1250x703).
     Center-crop (khong trim day) vi nhieu prompt neo chu the vao MEP DUOI.
  3. Backup ban goc sang _wm_orig/ truoc khi ghi (co --restore).
"""
import argparse
import io
import json
import os
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "17_chuseishibo-oyatsu"
IMG = VD / "slides_img_photo"
ORIG = VD / "_wm_orig"
CUT_X = 1250          # mep trai ✦ do bang mat = ~1265; cat tai 1250 cho an toan
AR = 16 / 9

STOP = {"a", "an", "the", "of", "on", "in", "at", "and", "with", "to", "from", "by",
        "one", "two", "three", "four", "five", "six", "still", "same", "now", "its",
        "their", "for", "into", "over", "under", "beside", "next", "up", "down"}


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", action="store_true")
    ap.add_argument("--slots", help="chi nhap vao cac slot nay, vd slide_10.jpg,slide_64.jpg "
                                    "(BAT BUOC khi nguon la lo bo sung — neu khong, map greedy "
                                    "tren ca 103 slot se GHI DE nham anh dang dung)")
    a = ap.parse_args()

    if a.restore:
        n = 0
        for f in sorted(ORIG.glob("*.jpg")):
            shutil.copy2(f, IMG / f.name)
            n += 1
        print(f"restore {n} anh tu _wm_orig/")
        return 0

    # ── doc SUBJECT tung slot tu file prompt ────────────────────────────────
    flow = (VD / "slide_prompts_FLOW.txt").read_text(encoding="utf-8").splitlines()
    tenfile = (VD / "slide_prompts_TENFILE.txt").read_text(encoding="utf-8").splitlines()[1:]
    slots = []
    for line, tf in zip(flow, tenfile):
        m = re.search(r"SUBJECT: (.*?)\. SETTING", line)
        slots.append({"name": tf.split("\t")[0], "subj": m.group(1) if m else "",
                      "moc": tf.split("\t")[1], "mode": tf.split("\t")[2].strip()})

    if a.slots:
        keep = {s.strip() for s in a.slots.split(",")}
        slots = [s for s in slots if s["name"] in keep]
        if len(slots) != len(keep):
            print(f"⚠️ chi tim thay {len(slots)}/{len(keep)} slot chi dinh")
    srcs = sorted(Path(a.src).glob("*.jpe*g")) + sorted(Path(a.src).glob("*.png"))
    print(f"nguon: {len(srcs)} anh | slot can: {len(slots)}\n")

    # ── ghep greedy theo diem overlap ───────────────────────────────────────
    pairs = []
    for s in srcs:
        st = toks(re.sub(r"_\d{12,}$", "", s.stem))
        for i, sl in enumerate(slots):
            sc = len(st & toks(sl["subj"])) / max(len(st), 1)
            pairs.append((sc, i, s))
    pairs.sort(key=lambda x: -x[0])
    used_slot, used_src, pick = set(), set(), {}
    for sc, i, s in pairs:
        if sc <= 0 or i in used_slot or s in used_src:
            continue
        used_slot.add(i)
        used_src.add(s)
        pick[i] = (s, sc)

    weak = [(i, pick[i][1]) for i in pick if pick[i][1] < 0.34]
    miss = [i for i in range(len(slots)) if i not in pick]
    extra = [s for s in srcs if s not in used_src]

    for i in sorted(pick):
        s, sc = pick[i]
        flag = "  ⚠️ YEU" if sc < 0.34 else ""
        print(f"  {slots[i]['name']:18} {slots[i]['moc']} {slots[i]['mode']:6} <- "
              f"{s.stem[:46]:48} {sc:.2f}{flag}")

    print(f"\nghep duoc {len(pick)}/{len(slots)} slot | ghep yeu {len(weak)} | "
          f"anh thua {len(extra)}")
    if miss:
        print("\n🔴 SLOT CHUA CO ANH — can gen them:")
        for i in miss:
            print(f"   {slots[i]['name']:18} {slots[i]['moc']} {slots[i]['mode']:6} "
                  f"{slots[i]['subj'][:70]}")
    if extra:
        print("\nⓘ anh nguon khong khop slot nao:")
        for s in extra:
            print(f"   {s.name}")

    if not a.apply:
        print("\n(dry-run — them --apply de cat ✦ va ghi vao slides_img_photo/)")
        return 0

    IMG.mkdir(parents=True, exist_ok=True)
    ORIG.mkdir(parents=True, exist_ok=True)
    for i in sorted(pick):
        s, _ = pick[i]
        im = Image.open(s).convert("RGB")
        W, H = im.size
        if (W, H) != (1376, 768):
            print(f"   ⚠️ {s.name}: {W}x{H} khac lo 1376x768 -> BO QUA (toa do ✦ khac)")
            continue
        im = im.crop((0, 0, CUT_X, H))                 # cat bo ✦ ben phai
        h = int(CUT_X / AR)
        top = (H - h) // 2                             # center-crop doc, giu mep duoi
        im = im.crop((0, top, CUT_X, top + h))
        dst = IMG / slots[i]["name"]
        shutil.copy2(s, ORIG / slots[i]["name"])
        im.save(dst, quality=93)
    print(f"\n✅ ghi {len(pick)} anh vao {IMG.relative_to(ROOT)} "
          f"(da cat ✦: 1376x768 -> {CUT_X}x{int(CUT_X/AR)}) · backup goc: _wm_orig/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
