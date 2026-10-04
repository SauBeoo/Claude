# -*- coding: utf-8 -*-
r"""Doi chieu lo anh tai ve <-> 86 slot cua video 21, copy vao dung cho.

Giong place19/20.py: khop bang token-overlap giua TEN FILE va cau SUBJ cua prompt.
In ra bang de NGUOI DUYET — sai map = dung hinh o sai nhip, khong gate nao bat duoc.

    python tools\place21.py --src "C:\Users\tuana\Downloads\<folder>"           # xem truoc
    python tools\place21.py --src "C:\Users\tuana\Downloads\<folder>" --apply   # copy that
"""
import argparse, io, re, shutil, sys, unicodedata
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "21_furo-no-kabi-modoru"
VD = PROJ / "06_VIDEO" / SLUG
S = PROJ / "03_SCRIPTS"

fl = S.joinpath(f"{SLUG}_IMG_FLOW.txt").read_text(encoding="utf-8").strip().split("\n")
nm = [re.sub(r"^\s*\d+\s+", "", l).strip()
      for l in S.joinpath(f"{SLUG}_IMG_NAMES.txt").read_text(encoding="utf-8").strip().split("\n")]
subj = [f.split("no watermark. ", 1)[1] if "no watermark. " in f else f for f in fl]
assert len(subj) == len(nm), f"FLOW {len(subj)} != NAMES {len(nm)}"

STOP = {"a", "an", "the", "of", "in", "on", "at", "with", "and", "from", "into", "for",
        "close", "up", "extreme", "seen", "straight", "down", "above", "side", "by",
        "feel", "wide", "view", "very", "its", "that", "onto", "one", "two", "three",
        "same", "still", "only", "out", "over", "no", "not", "all", "but", "already",
        "photorealistic", "cinematic", "documentary", "macro", "photograph", "light",
        "palette", "muted", "colors", "shallow", "depth", "field", "fine", "detail",
        "calm", "quiet", "mood", "horizontal", "text", "letters", "logos", "brand",
        "labels", "human", "faces", "watermark", "frame", "subject", "fills", "tight",
        "crop", "plain", "dark", "focus", "background", "hard", "directional", "high",
        "micro", "soft", "natural", "cool", "warm", "neutral"}

# ⭐ GAN TAY — chot bang MAT tren contact sheet, ap TRUOC khop tu dong.
#    (dien vao khi soi bang lan dau thay slot nao lech)
FORCE = {
 # chot bang MAT sau lan khop dau (matcher tham lam gan sai 5 cho):
 "slides_img/slide_35.jpg":            "Spraying_bottle_in_bathroom",
 "slides_img/slide_80.jpg":            "Open_bathroom_window_with_breeze",   # slot 78 la phong KHONG cua so
 "slides_img/slide_82.jpg":            "Macro_of_spots_on_sealant",          # gion CO dom
 "slides_img/wipe_wall_dry.jpg":       "Dry_bathroom_wall",                  # anh SAU cua cap wipe
 "slides_img/slide_36.jpg":            "Wiper_resting_against_bathroom_wall",
}


def tok(s):
    s = unicodedata.normalize("NFKD", s).lower()
    return {w for w in re.split(r"[^a-z0-9]+", s) if w and w not in STOP and len(w) > 2}


ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True, help="folder anh tai ve")
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()

SRC = Path(a.src)
files = [p for p in SRC.iterdir() if p.suffix.lower() in (".jpeg", ".jpg", ".png")]
if not files:
    raise SystemExit(f"[LOI] khong co anh trong {SRC}")
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
    if best and bs >= 0.18:
        used.add(best)
        ok.append((n, best, bs, s))
    else:
        miss.append((n, s, bs))

print(f"KHOP {len(ok)}/{len(nm)} slot · file thua {len(files) - len(used)}\n")
print("  diem  slot                                      <- file tai ve")
for n, p, sc, s in ok:
    flag = "  " if sc >= 0.30 else "! "
    print(f"{flag}{sc:.2f}  {n:<42} <- {p.name[:44]}")
if miss:
    print("\n[!] SLOT THIEU:")
    for n, s, sc in miss:
        print(f"   {n:<42} (diem tot nhat {sc:.2f})  can: {s[:64]}")
left = [p.name for p in files if p not in used]
if left:
    print("\n[?] FILE CHUA DUNG:")
    for x in left:
        print("   ", x[:70])

if a.apply:
    for n, p, sc, s in ok:
        dst = VD / n
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
    print(f"\n[OK] da copy {len(ok)} anh vao {VD}")
    print("     buoc ke: xoa watermark -> make_vox -> make_shot -> check_vox -> render")
else:
    print("\n(xem truoc — them --apply de copy that)")
