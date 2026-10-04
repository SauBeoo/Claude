# -*- coding: utf-8 -*-
"""Doi chieu lo anh MOI <-> danh sach TODO cua video 19, copy vao dung cho.

Dung: python tools/place19b.py "C:\\Users\\tuana\\Downloads\\download (1)"
Khac place19.py: chi khop trong pham vi _IMG_NAMES_TODO.txt (36 slot), va GHI DE
ban cu — vi lo 1 sai framing (room thay vi macro), giu lai la giu cai sai.
"""
import re, shutil, sys, unicodedata
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\tuana\Downloads\download (1)")
PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
VD = PROJ / "06_VIDEO" / "19_haisuiko-naze-tsumaru"
S = PROJ / "03_SCRIPTS"
SLUG = "19_haisuiko-naze-tsumaru"

todo_f = S.joinpath(f"{SLUG}_IMG_FLOW_TODO.txt").read_text(encoding="utf-8").strip().split("\n")
todo_n = [re.sub(r"\s+\[.*$","",re.sub(r"^\s*\d+\s+","",l)).strip()
          for l in S.joinpath(f"{SLUG}_IMG_NAMES_TODO.txt").read_text(encoding="utf-8").strip().split("\n")]
subj = [f.split("no watermark. ", 1)[1] for f in todo_f]

STOP = {"a", "an", "the", "of", "in", "on", "at", "with", "and", "from", "into", "for",
        "close", "up", "extreme", "seen", "straight", "down", "above", "side", "by",
        "feel", "wide", "view", "very", "its", "that", "onto", "shot", "macro", "photograph"}


def tok(s):
    s = unicodedata.normalize("NFKD", s).lower()
    return {w for w in re.split(r"[^a-z0-9]+", s) if w and w not in STOP and len(w) > 2}


files = [p for p in SRC.iterdir() if p.suffix.lower() in (".jpeg", ".jpg", ".png")]
ftok = {p: tok(re.sub(r"_\d{12,}$", "", p.stem)) for p in files}

used, ok, miss = set(), [], []
for s, n in zip(subj, todo_n):
    st = tok(s)
    best, bs = None, 0.0
    for p, t in ftok.items():
        if p in used:
            continue
        sc = len(st & t) / max(1, len(st | t))
        if sc > bs:
            bs, best = sc, p
    if best and bs >= 0.30:
        used.add(best)
        ok.append((n, best, round(bs, 2)))
    else:
        miss.append((n, round(bs, 2)))

for n, src, _ in ok:
    dst = VD / n
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

print(f"dat {len(ok)}/{len(todo_n)} anh TODO  |  thieu {len(miss)}  |  anh du {len(files)-len(used)}")
for n, sc in miss:
    print(f"  THIEU  {n}  (diem cao nhat {sc})")
for p in files:
    if p not in used:
        print(f"  DU     {p.name}")

# ── kiem phu do TOAN BO 81 slot
allf = S.joinpath(f"{SLUG}_IMG_FLOW.txt").read_text(encoding="utf-8").strip().split("\n")
alln = [re.sub(r"^\s*\d+\s+","",l).strip() for l in S.joinpath(f"{SLUG}_IMG_NAMES.txt").read_text(encoding="utf-8").strip().split("\n")]
have = [n for n in alln if (VD / n).exists()]
vox = [n for n in alln if n.startswith("ai_clean")]
voxhave = [n for n in vox if (VD / n).exists()]
print(f"\nTONG: {len(have)}/81 anh  ·  vox {len(voxhave)}/{len(vox)}  ·  "
      f"slides {len(have)-len(voxhave)}/{len(alln)-len(vox)}")
for n in alln:
    if not (VD / n).exists():
        print(f"  con thieu: {n}")
