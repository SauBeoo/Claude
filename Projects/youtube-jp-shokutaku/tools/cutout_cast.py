# -*- coding: utf-8 -*-
r"""Tach nen MAGENTA cua anh cast -> PNG alpha trong assets/cast/ (kenh shokutaku).

    python tools\cutout_cast.py "C:\Users\tuana\Downloads\<folder>"          # xem thu
    python tools\cutout_cast.py <src> --apply                                # ghi that
    python tools\cutout_cast.py <src> --apply --tol 90                       # noi nguong

VI SAO NEN MAGENTA (khong phai nen trang): cast la CU GIA — toc bac + ao kem/trang. Tach
theo nguong SANG thi an mat toc va ao. Nen `#FF00FF` khong bao gio co trong palette pastel
cua nguoi ⇒ tach bang KHOANG CACH MAU, sach tuyet doi. Prompt gen: `cast_prompts_FLOW.txt`.

Ghep ten file: theo `cast_prompts_TENFILE.txt` (thu tu dong = thu tu prompt trong FLOW),
doi chieu bang token de khong phu thuoc thu tu tai ve.
"""
import argparse
import io
import re
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(io.FileIO(1, "w"), encoding="utf-8", errors="replace",
                              line_buffering=True)

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "18_ringo-tabekata"
DST = ROOT / "assets" / "cast"
KEY = np.array([255, 0, 255])          # magenta thuan

# 🔴 GHEP TEN: ten file generator dat theo NOI DUNG ANH ("Woman_speaking_in_apron"), khong
# chua "minori"/"kikite" ⇒ ghep bang token-overlap thi SAI GIOI TINH: lan dau `minori_smile`
# bat vao "Man_listening_with_interested_smile" chi vi trung chu "smile".
# => (a) khoa GIOI TINH truoc, (b) roi moi so tu khoa HANH DONG.
GENDER = {"minori": "woman", "kikite": "man"}
ACTION = {
    "minori_talk":       ("speaking",),
    "minori_point":      ("pointing",),
    # ⚠️ KHONG dung key rong kieu "apple"/"holding": "apple" bat nham
    # "Woman_eating_apple_slice" (dung cua minori_taste) va "holding" bat nham
    # "Woman_holding_hand_up" (dung cua minori_stop). Key phai DAC TRUNG cho dung tu the.
    "minori_hold":       ("holding_red_apple", "holding red apple"),
    "minori_stop":       ("hand_up", "hand up"),
    "minori_taste":      ("eating",),
    "minori_smile":      ("smiling",),
    "kikite_listen":     ("listening",),
    "kikite_worried":    ("worried",),
    "kikite_surprised":  ("surprised",),
    "kikite_relieved":   ("relief", "relieved"),
    "kikite_note":       ("writing", "notebook"),
    "kikite_nod":        ("nodding", "thumbs"),
}


def keep_main_blob(alpha):
    """Chi giu KHOI LON NHAT — loai ✦ watermark va moi dom roi.

    🔴 Bat buoc, khong phai toi uu: dau ✦ cua generator la mau TRANG NHAT tren nen
    magenta ⇒ no KHONG bi nguong mau loai, nen bbox se phinh ra tan goc duoi-phai va cast
    mang theo mot dom sang. Crop theo bbox alpha ma khong loc blob thi ✦ di vao san khau.
    """
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 8).astype(np.uint8), 8)
    if n <= 2:                                     # chi co nen + 1 khoi
        return alpha, 0
    areas = stats[1:, cv2.CC_STAT_AREA]
    main = 1 + int(np.argmax(areas))
    dropped = int(len(areas) - 1)
    return np.where(lab == main, alpha, 0).astype(np.uint8), dropped


def has_white_edge(rgb, solid):
    """Anh gen co VIEN TRANG sticker quanh nhan vat hay khong?

    Do do sang cua vanh 5px trong cung cua mask. Anh co vien sticker -> vanh gan trang
    (>230). Anh khong co -> vanh la NET NAU/mau ao (<200).
    """
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    ring = (solid > 0) & (cv2.erode(solid, k) == 0)
    if ring.sum() < 200:
        return True
    return float(np.asarray(rgb)[ring].mean()) > 230


def add_white_edge(rgba, px=11):
    """Ve VIEN TRANG quanh silhouette (kieu cat bang keo) — cho anh gen thieu vien.

    🔴 Vi sao can: lo dau 10/12 anh co vien trang sticker san, nhung lo GEN LAI (2026-08-21)
    tra ve `Man_showing_surprised_expression` KHONG co vien. Tron hai kieu trong mot video
    thi thay ngay (anh co vien noi hon), va `--erode` an vao NET NAU thay vi vien trang.
    Cach lam: dilate alpha ra px, to TRANG, roi dan nhan vat len tren.
    """
    a = np.asarray(rgba)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (px * 2 + 1,) * 2)
    grown = cv2.dilate((a[:, :, 3] > 8).astype(np.uint8), k) * 255
    base = Image.fromarray(np.dstack([
        np.full(a.shape[:2], 255, np.uint8), np.full(a.shape[:2], 255, np.uint8),
        np.full(a.shape[:2], 255, np.uint8), grown.astype(np.uint8)]), "RGBA")
    base.alpha_composite(rgba)
    return base


def cutout(im, tol, erode=3):
    """Bo pixel gan magenta, CO mask vao trong, giu khoi lon nhat, crop sat bbox.

    🔴 CACH CHUA VET TIM (da thu 1 cach SAI truoc do): ban dau ham nay "keo mau vien ve
    xam" bang cach ha R va B theo G. Vo dung, va do duoc: 1.400/1.400 px vien VAN tim.
    Vi sao: magenta la (255,0,255) — G ≈ 0, nen ha R/B theo G ra (145,0,90) = van do tim.
    Suy mau tu CHINH pixel da nhiem thi khong bao gio sach.
    ⇒ Cach dung o day: anh gen co VIEN TRANG sticker day quanh nhan vat, nen chi can CO
    mask vao ~3px la moi pixel con lai deu nam sau trong vien trang, khong con nhiem
    magenta. Mat 3px vien trang, doi lai sach tuyet doi — va vien trang van con day.
    """
    a = np.asarray(im.convert("RGB")).astype(int)
    dist = np.sqrt(((a - KEY) ** 2).sum(axis=2))
    solid = (dist > tol).astype(np.uint8)
    solid, dropped = keep_main_blob(solid * 255)
    solid = (solid > 0).astype(np.uint8)
    had_edge = has_white_edge(im.convert("RGB"), solid)

    # 🔴 Anh KHONG co vien trang phai co SAU HON: magenta tiep giap thang net ve nen vanh
    # anti-alias nhiem rong hon; erode 3 de lai VET HONG o mep hong (do duoc o
    # kikite_surprised lo gen lai). Vien trang se duoc TU VE bu lai sau do.
    px = erode if had_edge else erode + 4
    if px > 0:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (px * 2 + 1,) * 2)
        solid = cv2.erode(solid, k)
    # mem 1px cho het rang cua, KHONG lam vien phinh tro lai ra vung nhiem
    alpha = cv2.GaussianBlur(solid * 255, (3, 3), 0)

    out = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")
    if not had_edge:                                # anh gen thieu vien -> tu ve
        out = add_white_edge(out)
    bbox = out.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    return (out.crop(bbox) if bbox else out), (alpha > 8).mean(), dropped, had_edge


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--tol", type=int, default=110,
                    help="nguong khoang cach mau (mac dinh 110; sot vet tim -> tang)")
    ap.add_argument("--erode", type=int, default=3,
                    help="co mask vao trong bao nhieu px (mac dinh 3; con vet tim -> tang)")
    a = ap.parse_args()

    rows = (VD / "cast_prompts_TENFILE.txt").read_text(encoding="utf-8").splitlines()[1:]
    want = [r.split("\t")[0] for r in rows if r.strip()]
    srcs = sorted(Path(a.src).glob("*.png")) + sorted(Path(a.src).glob("*.jpe*g"))
    print(f"nguon {len(srcs)} anh | can {len(want)} cast: {', '.join(want)}\n")

    used, plan = set(), []
    for name in want:
        stem = Path(name).stem
        want_sex = GENDER.get(stem.split("_")[0], "")
        keys = ACTION.get(stem, ())
        hit = None
        for p in srcs:
            low = p.stem.lower().replace("-", "_")
            if p in used:
                continue
            if want_sex and want_sex not in low:          # gate GIOI TINH — chan cung
                continue
            if any(k.replace(" ", "_") in low or k in low for k in keys):
                hit = p
                break
        if hit is not None:
            used.add(hit)
        plan.append((name, hit))

    for name, p in plan:
        print(f"{name:24s} ← {p.name if p else '🔴 CHUA CO ANH'}")
    spare = [p.name for p in srcs if p not in used]
    if spare:
        print(f"\nⓘ {len(spare)} anh nguon KHONG dung: {', '.join(spare)}")
    if not a.apply:
        print("\n(xem thu — them --apply de ghi that)")
        return 0

    DST.mkdir(parents=True, exist_ok=True)
    n = 0
    for name, p in plan:
        if p is None:
            continue
        out, keep, dropped, had_edge = cutout(Image.open(p), a.tol, a.erode)
        out.save(DST / name)
        flag = "⚠️ giu <8% khung — nguong qua gat?" if keep < 0.08 else ""
        print(f"  {name}: {out.width}x{out.height}  giu {keep*100:4.1f}% pixel"
              f"  bo {dropped} dom roi (✦)"
              f"  {'vien san' if had_edge else '➕ TU VE vien trang'} {flag}")
        n += 1
    print(f"\nghi {n} cast -> {DST.relative_to(ROOT)}")
    print("⚠️ SOI VIEN 1:1 quanh toc/vai: con vet tim thi tang --tol; an mat toc thi giam.")
    print("   Xong: chay lai ingest_slides_18.py --apply (canh bao CHUA CO CAST phai het).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
