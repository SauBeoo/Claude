# -*- coding: utf-8 -*-
"""Dung SLIDES.json cho video 13 tu timeline THAT.

Ba luat cua kenh, cai vao day:
  1. CUE CUNG  — moi clip neo vao t0 cua MOT DONG that (CLAUDE.md §Visual).
     Chi khi mot dong dai hon TRAN moi chen cat phu trong long dong (offset).
  2. TRAN 8,0s — chia theo TRAN, khong chia theo trung binh
     (`feedback_phan_bo_theo_tran`): tham lam lay moc dong XA NHAT con <= 8,0s.
  3. Entry 0 = "video": true (`feedback_showa_coldopen_clip_that_giay_0` —
     phan "phim that" da thay bang t2v tu 2026-09-04, phan "giay 0 phai DONG"
     van con hieu luc).

Gate CHAN chay SAU khi ghi file (bai hoc: gate exit(1) truoc khi ghi lam
SLIDES giu nguyen ban cu, sua 4 luot khong hieu vi sao cue cung khong an).
"""
import sys, json, math
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

STEM = "13_kosodate-joushiki"
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / STEM
OUT = ROOT / "03_SCRIPTS" / (STEM + "_SLIDES.json")

MAX_CLIP = 8.0      # tran cung cua kenh (CLAUDE.md §Visual — Flow gen toi da 8s)
EPS = 1e-6

d = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
lines, total = d["lines"], d["total"]
starts = [ln["start"] for ln in lines]

# ---------- 1. chon moc cat ----------
cuts = [0.0]
cur = 0.0
while cur < total - 0.05:
    far = None
    for s in starts:
        if s <= cur + EPS:
            continue
        if s - cur > MAX_CLIP + EPS:
            break
        far = s
    if far is not None:
        cuts.append(far)
        cur = far
        continue
    nxt = next((s for s in starts if s > cur + EPS), total)
    gap = nxt - cur
    n = math.ceil(gap / MAX_CLIP)          # chia theo TRAN
    step = gap / n
    for t in range(1, n):
        cuts.append(round(cur + t * step, 2))
    if nxt >= total - 0.05:
        cur = total
    else:
        cuts.append(nxt)
        cur = nxt

# ---------- 2. cut -> entry (match + offset) ----------
def owner(t):
    k = 0
    for i, s in enumerate(starts):
        if s <= t + EPS:
            k = i
        else:
            break
    return k

def uniq_match(li):
    """Chuoi con NGAN NHAT sao cho dong DAU TIEN chua no dung la dong li."""
    txt = lines[li]["text"]
    for n in range(6, len(txt) + 1):
        m = txt[:n]
        if next(i for i, ln in enumerate(lines) if m in ln["text"]) == li:
            return m
    return None

entries, rows, bad = [], [], []
for idx, t in enumerate(cuts):
    li = owner(t)
    m = uniq_match(li)
    if m is None:
        bad.append((idx, li, lines[li]["text"][:20]))
        m = lines[li]["text"][:10]
    e = {"match": m, "video": True, "source": "clips/clip_%02d.mp4" % idx,
         "offset": round(t - lines[li]["start"], 2)}
    end = cuts[idx + 1] if idx + 1 < len(cuts) else total
    e["dur"] = round(end - t, 2)           # renderer BO QUA khoa nay; de nguoi doc
    entries.append(e)
    rows.append("%3d  %7.2fs  %5.2fs  L%-3d  %s" %
                (idx, t, end - t, li, lines[li]["text"][:34]))

OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
(VD / "clips").mkdir(parents=True, exist_ok=True)
(VD / "clips" / "_MAP.txt").write_text(
    "idx     bat dau    dai   dong  loi\n" + "\n".join(rows) + "\n", encoding="utf-8")

# ---------- 3. GATE (sau khi ghi) ----------
durs = [cuts[i + 1] - cuts[i] for i in range(len(cuts) - 1)] + [total - cuts[-1]]
over = [(i, round(x, 2)) for i, x in enumerate(durs) if x > MAX_CLIP + 0.01]
tiny = [(i, round(x, 2)) for i, x in enumerate(durs) if x < 2.0]
intra = sum(1 for e in entries if e["offset"] > 0.01)

print("=== SLIDES %s ===" % STEM)
print("tong          : %.1fs = %.2f phut | %d dong loi" % (total, total / 60, len(lines)))
print("so clip       : %d" % len(entries))
print("dai clip      : min %.2fs | trung binh %.2fs | max %.2fs"
      % (min(durs), sum(durs) / len(durs), max(durs)))
print("doi hinh/phut : %.1f" % (len(entries) / (total / 60)))
print("cue cung      : %d/%d neo dung dau dong (con lai la cat trong long dong)"
      % (len(entries) - intra, len(entries)))
print("entry 0 video : %s" % entries[0]["video"])
print("-" * 58)
ok = True
if over:
    print("[CHAN] %d khe > TRAN %.1fs: %s" % (len(over), MAX_CLIP, over[:8])); ok = False
else:
    print("[OK  ] khong khe nao > TRAN %.1fs" % MAX_CLIP)
if bad:
    print("[CHAN] %d match KHONG duy nhat: %s" % (len(bad), bad[:5])); ok = False
else:
    print("[OK  ] 152 match duy nhat" if len(lines) == 152 else "[OK  ] match duy nhat")
if not entries[0]["video"]:
    print("[CHAN] entry 0 phai la clip dong"); ok = False
if tiny:
    print("[warn] %d clip < 2,0s (gen 8s roi cat): %s" % (len(tiny), tiny[:8]))
print("-" * 58)
print("SLIDES -> %s" % OUT)
print("MAP    -> %s" % (VD / "clips" / "_MAP.txt"))
print("KET QUA: %s" % ("SACH" if ok else "CO LOI CHAN"))
sys.exit(0 if ok else 1)
