# -*- coding: utf-8 -*-
"""Doi chieu lo anh tai ve <-> 81 slot cua video 19, copy cai khop vao dung cho,
va xuat file prompt CHI cho slot con thieu (khong gen lai ca 81)."""
import re, shutil, unicodedata
from pathlib import Path

SRC = Path(r"C:\Users\tuana\Downloads\download (2)")
PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
VD = PROJ / "06_VIDEO" / "19_haisuiko-naze-tsumaru"
S = PROJ / "03_SCRIPTS"
SLUG = "19_haisuiko-naze-tsumaru"

fl = S.joinpath(f"{SLUG}_IMG_FLOW.txt").read_text(encoding="utf-8").strip().split("\n")
nm = [re.sub(r"^\s*\d+\s+","",l).strip() for l in S.joinpath(f"{SLUG}_IMG_NAMES.txt").read_text(encoding="utf-8").strip().split("\n")]
subj = [f.split("no watermark. ", 1)[1] for f in fl]

STOP = {"a", "an", "the", "of", "in", "on", "at", "with", "and", "from", "into", "for",
        "close", "up", "extreme", "seen", "straight", "down", "above", "side", "by",
        "feel", "wide", "view", "very", "its", "that", "onto"}


def tok(s):
    s = unicodedata.normalize("NFKD", s).lower()
    return {w for w in re.split(r"[^a-z0-9]+", s) if w and w not in STOP and len(w) > 2}


files = [p for p in SRC.iterdir() if p.suffix.lower() in (".jpeg", ".jpg", ".png")]
ftok = {p: tok(re.sub(r"_\d{12,}$", "", p.stem)) for p in files}

used, ok, miss = set(), [], []
for s, n in zip(subj, nm):
    st = tok(s)
    best, bs = None, 0.0
    for p, t in ftok.items():
        if p in used:
            continue
        sc = len(st & t) / max(1, len(st | t))
        if sc > bs:
            bs, best = sc, p
    if best and bs >= 0.34:
        used.add(best)
        ok.append((n, best))
    else:
        miss.append((n, s))

for n, src in ok:
    dst = VD / n
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

if miss:
    LOCK = fl[0].split(". grease")[0] if False else subj and fl[0][:fl[0].index("no watermark.") + 13]
    S.joinpath(f"{SLUG}_IMG_FLOW_MISSING.txt").write_text(
        "\n".join(f"{LOCK} {s}" for _, s in miss) + "\n", encoding="utf-8")
    S.joinpath(f"{SLUG}_IMG_NAMES_MISSING.txt").write_text(
        "\n".join(f"{i+1:3d}  {n}" for i, (n, _) in enumerate(miss)) + "\n", encoding="utf-8")

print(f"da dat {len(ok)}/81 anh  |  thieu {len(miss)}  |  anh du khong dung {len(files)-len(used)}")
print(f"  slides_img: {sum(1 for n,_ in ok if n.startswith('slides_img'))}/63")
print(f"  ai_clean  : {sum(1 for n,_ in ok if n.startswith('ai_clean'))}/18")
