# -*- coding: utf-8 -*-
r"""ingest_art30.py — gom ảnh video 30 từ 2 lô, xoá ✦ bằng CẮT, ghi art_final/shot_KKK.png.

LÔ:
  · `Tháng 9 24 - 18_19.zip` (92 ảnh) — lô đầu cho 91 dòng `img30_FLOW.txt`
  · `Tháng 9 25 - 16_08.zip` (10 ảnh) — REDO1 cho 10 dòng trong `img30_prompts.REDO`
  ⛔ 10 ảnh lô đầu của các dòng REDO KHÔNG được dùng (đã loại khi soi — lý do ghi ở REDO).

GHÉP: lô đầu bằng Hungarian trên điểm token (tên file ↔ subject) — đã soi mắt 91/91 đúng ô
(2026-09-25). Lô REDO **ghép tay theo mắt**: token đảo 2 ảnh kính lúp (R9/R10 — cùng từ
magnifying/notice, khác nhau ở «trong kính» vs «cạnh kính», token không thấy).

✦: CẮT 0,905W + trim 16:9 chia đôi (cùng khuôn `strip_wm_crop29.py`, `media-library.md` §2.10 ⑤b
mục 2). Lô này có BAKE CHỮ ⇒ tool đo mực trong dải bị cắt (0,905–1,0W, trừ vùng ✦) và báo ô nào
có nội dung bị cắt — phải soi mắt ô đó.
CHẠY:  python tools/ingest_art30.py
"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy.optimize import linear_sum_assignment

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
import img30_prompts as ip  # noqa: E402

VD = PROJ / "06_VIDEO" / "30_nenkin-furikomi-10gatsu-fueru-hito"
ART = VD / "art_final"
DL = Path(r"C:\Users\tuana\Downloads")
LOT1 = DL / "Tháng 9 24 - 18_19.zip"
LOT2 = DL / "Tháng 9 25 - 16_08.zip"
CUT = 0.905
WM = (0.930, 0.878)
# REDO: dòng FLOW → tên file lô 2 (tiền tố) — chốt bằng MẮT
REDO_FILES = {3: "Elderly_man_reading_passbook", 21: "Elderly_woman_sitting_at_kotatsu",
              22: "Woman_reading_notice_at_table", 23: "Six_envelopes_with_coin_stacks",
              37: "Pension_booklet_and_coin_envelopes", 41: "Four_notices_fanned",
              46: "Three_notices_laid", 48: "Hand_pointing_at_notice",
              50: "Magnifying_glass_enlarging", 53: "Magnifying_glass_on_document"}
STOP = set("a an the of on in at to and with one two three four its it them their by from for "
           "same other side lying laid seen held resting beside is are into under over his her "
           "small".split())


def toks(s):
    out = set()
    for w in re.findall(r"[a-z]+", s.lower()):
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if w not in STOP and len(w) > 2:
            out.add(w)
    return out


def load(z, n):
    return Image.open(io.BytesIO(z.read(n))).convert("RGB")


def cut(im):
    W, H = im.size
    x1 = int(W * CUT)
    h2 = int(x1 / 16 * 9)
    dy = (H - h2) // 2
    return im.crop((0, dy, x1, dy + h2)).resize((1920, 1080), Image.LANCZOS)


# Ô mà SỐ LƯỢNG vật là nội dung (6 phong bì / 3 phong bì) — cắt 0,905W làm mất vật cuối
# (đo: 6,6–28,6% mực trong dải cắt). ✦ ở các ô này nằm trên nền kem PHẲNG ⇒ nhánh VÁ
# (`media-library.md` §2.10 ⑤b mục 3: trung vị TỪNG HÀNG + nhiễu ±1,2), không cắt.
PATCH = {23, 37, 70, 72}
WM_R = 36


def patch_star(im):
    a = np.asarray(im).astype(np.float32)
    H, W = a.shape[:2]
    cx, cy = int(W * 0.930), int(H * 0.873)
    xs = np.r_[cx - 80:cx - 45, cx + 45:min(W, cx + 80)]
    rng = np.random.default_rng(30)
    for y in range(cy - WM_R, cy + WM_R):
        med = np.median(a[y, xs], axis=0)
        a[y, cx - WM_R:cx + WM_R] = med + rng.normal(0, 1.2, (2 * WM_R, 3))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((1920, 1080), Image.LANCZOS)


def lost_ink(im):
    """% pixel KHÁC NỀN trong dải bị cắt (trừ ô ✦). >0,5% ⇒ nội dung bị cắt, soi mắt."""
    a = np.asarray(im).astype(int)
    H, W = a.shape[:2]
    bg = a[6, 6]
    s = a[:, int(W * CUT):]
    d = np.abs(s - bg).sum(2) > 90
    wx, wy = int(W * WM[0]) - int(W * CUT), int(H * WM[1])
    d[max(0, wy - 60):wy + 60, max(0, wx - 60):wx + 60] = False
    return 100 * d.mean()


def main() -> int:
    z1, z2 = zipfile.ZipFile(LOT1), zipfile.ZipFile(LOT2)
    n1 = [i.filename for i in z1.infolist()]
    n2 = [i.filename for i in z2.infolist()]
    flow = [l.rstrip("\n") for l in open(VD / "img30_FLOW.txt", encoding="utf-8")]
    ten = [l for l in open(VD / "img30_TENFILE.txt", encoding="utf-8") if l.startswith("dong ")]
    shot_of = {int(m.group(1)): int(m.group(2)) for l in ten
               for m in [re.match(r"dong (\d+) -> shot_(\d+)\.png", l)]}
    subs = [l.split("SUBJECT:", 1)[1] if "SUBJECT:" in l else l[-450:] for l in flow]
    nt = [toks(re.sub(r"_\d{14}(_\d)?\.jpg$", "", n).replace("_", " ")) for n in n1]
    M = np.array([[len(toks(s) & b) / max(1, len(b)) for b in nt] for s in subs])
    r, c = linear_sum_assignment(-M)
    pick = {i + 1: (z1, n1[j], M[i, j]) for i, j in zip(r, c)}
    assert set(REDO_FILES) == set(ip.REDO), "REDO_FILES lệch img30_prompts.REDO"
    for d, pre in REDO_FILES.items():
        hit = [n for n in n2 if n.startswith(pre)]
        assert len(hit) == 1, (pre, hit)
        pick[d] = (z2, hit[0], 1.0)
    ART.mkdir(parents=True, exist_ok=True)
    used, rows, warn = [], [], []
    for d in range(1, len(flow) + 1):
        z, n, sc = pick[d]
        im = load(z, n)
        li = lost_ink(im)
        if li > 0.5 and d not in PATCH:
            warn.append((d, shot_of[d], n[:40], round(li, 2)))
        (patch_star(im) if d in PATCH else cut(im)).save(ART / f"shot_{shot_of[d]:03d}.png")
        used.append(n)
        rows.append(dict(flow=d, shot=shot_of[d], lot=2 if z is z2 else 1, file=n,
                         score=round(float(sc), 2), lost_ink=round(li, 2)))
    (VD / "art_map30.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ô ảnh AI: {len(rows)} · từ lô REDO: {sum(r['lot'] == 2 for r in rows)} · "
          f"ảnh bị dùng lại: {len(used) - len(set(used))}")
    print(f"cắt ✦ tại {CUT}W + trim 16:9 → 1920×1080")
    print(f"⚠️ ô có mực trong dải bị cắt (>0,5%) — SOI MẮT: {len(warn)}")
    for w in warn:
        print("    FLOW %2d · shot_%03d · %s · %.2f%%" % w)
    miss = [k for k in range(98) if not (ART / f"shot_{k:03d}.png").exists()]
    print(f"🔴 ô thiếu ảnh trong art_final: {miss}" if miss else "✅ đủ 98/98 ô (kể cả 7 原典)")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
