# -*- coding: utf-8 -*-
"""Doi chieu lo anh tai ve <-> 74 slot cua video 20, copy vao dung cho.

Giong place19.py: khop bang token-overlap giua TEN FILE va cau SUBJ cua prompt.
In ra bang de NGUOI DUYET — sai map = dung hinh o sai nhip, gate nao cung khong bat duoc.

    python tools\\place20.py            # xem truoc, KHONG copy
    python tools\\place20.py --apply    # copy that
"""
import argparse, io, re, shutil, sys, unicodedata
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = Path(r"C:\Users\tuana\Downloads\download (6)")
PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "20_sentei-koshin-akinasu"
VD = PROJ / "06_VIDEO" / SLUG
S = PROJ / "03_SCRIPTS"

fl = S.joinpath(f"{SLUG}_IMG_FLOW.txt").read_text(encoding="utf-8").strip().split("\n")
nm = [re.sub(r"^\s*\d+\s+", "", l).strip()
      for l in S.joinpath(f"{SLUG}_IMG_NAMES.txt").read_text(encoding="utf-8").strip().split("\n")]
subj = [f.split("no watermark. ", 1)[1] for f in fl]
assert len(subj) == len(nm), f"FLOW {len(subj)} != NAMES {len(nm)}"

STOP = {"a", "an", "the", "of", "in", "on", "at", "with", "and", "from", "into", "for",
        "close", "up", "extreme", "seen", "straight", "down", "above", "side", "by",
        "feel", "wide", "view", "very", "its", "that", "onto", "one", "two", "three",
        "same", "still", "only", "out", "over", "no", "not", "all", "but", "already"}


def tok(s):
    s = unicodedata.normalize("NFKD", s).lower()
    return {w for w in re.split(r"[^a-z0-9]+", s) if w and w not in STOP and len(w) > 2}


# ⭐ GAN TAY — chot bang MAT tren contact sheet, ap TRUOC khop tu dong.
# Ly do: matcher tham lam (greedy) gan sai 3 cho that:
#   · anh MU ROM TREO (canh dong bai) bi keo len slide_06 (canh ong hang xom lau mo hoi)
#     => mat luon cu dong nhan vat, va slide_51 thanh rong
#   · 'grips' (macro can go mon) vs 'blade' (luoi keo+xeng) bi dao cho nhau
# Ten file ghi PREFIX, khong ghi duoi + timestamp.
FORCE = {
 "slides_img/slide_03.jpg":                      "Staked_eggplant_plants_in_garden",
 "slides_img/slide_06.jpg":                      "Person_wiping_brow_in_garden",
 "slides_img/slide_08.jpg":                      "Eggplant_plants_in_vegetable_garden",
 "slides_img/slide_16.jpg":                      "Pruning_shears_in_vegetable_garden",
 "slides_img/slide_22.jpg":                      "Pouring_granular_fertilizer_from",
 "slides_img/slide_51.jpg":                      "Straw_hat_hanging_in_garden",
 "slides_img/slide_53.jpg":                      "Eggplant_plants_in_home_garden",
 "ai_clean/three_tools_on_soil.jpeg":            "Garden_tools_laid_on_soil",
 "ai_clean/garden_shears_and_spade_leaning.jpeg":"Pruning_shears_and_spade_grips",
 "ai_clean/shears_and_spade_side_by_side.jpeg":  "Pruning_shears_and_spade_blade",
}

files = [p for p in SRC.iterdir() if p.suffix.lower() in (".jpeg", ".jpg", ".png")]
ftok = {p: tok(re.sub(r"_\d{12,}$", "", p.stem)) for p in files}

used, ok, miss = set(), [], []
_forced = {}
for slot, pref in FORCE.items():
    hit = next((p for p in files if p.name.startswith(pref[:26])), None)
    if hit is None:
        raise SystemExit(f"[LOI] FORCE khong tim thay file bat dau bang {pref!r}")
    _forced[slot] = hit
    used.add(hit)

for s, n in zip(subj, nm):
    if n in _forced:
        ok.append((n, _forced[n], 1.00, s))
        continue
    st = tok(s)
    best, bs = None, 0.0
    for p, t in ftok.items():
        if p in used:
            continue
        sc = len(st & t) / max(1, len(st | t))
        if sc > bs:
            bs, best = sc, p
    if best and bs >= 0.20:
        used.add(best)
        ok.append((n, best, bs, s))
    else:
        miss.append((n, s, bs))

ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()

print(f"KHOP {len(ok)}/{len(nm)} slot · file thua {len(files) - len(used)}\n")
print("  diem  slot                                    <- file tai ve")
for n, p, sc, s in ok:
    flag = "  " if sc >= 0.34 else "⚠ "
    print(f"{flag}{sc:.2f}  {n:<40} <- {p.name[:46]}")
if miss:
    print("\n🔴 SLOT THIEU:")
    for n, s, sc in miss:
        print(f"   {n:<40} (diem tot nhat {sc:.2f})  can: {s[:66]}")
left = [p.name for p in files if p not in used]
if left:
    print("\n📦 FILE CHUA DUNG:")
    for x in left:
        print("   ", x[:70])

if a.apply:
    for n, p, sc, s in ok:
        dst = VD / n
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
    print(f"\n✅ da copy {len(ok)} anh vao {VD}")
else:
    print("\n(xem truoc — them --apply de copy that)")
