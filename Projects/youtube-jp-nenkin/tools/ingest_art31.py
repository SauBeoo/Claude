# -*- coding: utf-8 -*-
r"""ingest_art31.py — gom ảnh video 31 từ các lô Flow, xoá ✦, ghi art_final/shot_KKK.png.

Chép khuôn `ingest_art30.py` (đọc docstring ở đó).
LÔ:
  · lô 1 `Tháng 9 27 - 17_50.zip` (76/81 ảnh) — ĐÃ SOI MẮT 76/76 đúng ô (2026-09-27). Bản ghép đóng
    băng ở `art_map31_lot1.json`: ⛔ không ghép lại bằng token (8 dòng FLOW REDO đã đổi chữ ⇒
    Hungarian sẽ xếp lệch). Dòng bị loại/thiếu = `img31_prompts.REDO1_WHY` (lý do ghi ở đó).
  · lô REDO1 (đối số 1) — Hungarian trên SUBJECT của `img31_FLOW_REDO1.txt` ↔ tên file.
    ⛔ Điểm token là PHỎNG ĐOÁN — soi sheet từng ô sau khi chạy.
✦: CẮT 0,905W + trim 16:9 chia đôi (`media-library.md` §2.10 ⑤b mục 2) · ô vật sát mép phải mà ✦
trên nền phẳng ⇒ VÁ (PATCH) · dải trắng generator vẽ ngang khung ⇒ tô lại (BAND).
Ảnh lô 1 của dòng bị LOẠI dời sang `art_final/rejected/` (không xoá, không bao giờ quay lại).
CHẠY:  python tools/ingest_art31.py                    (chỉ lô 1)
       python tools/ingest_art31.py "<zip lô REDO1>"   (lô 1 + lô REDO1)
"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.optimize import linear_sum_assignment

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
from img31_prompts import REDO1_WHY  # noqa: E402

STEM = "31_fuyo-shinkokusho-hikazei-domino"
VD = PROJ / "06_VIDEO" / STEM
ART = VD / "art_final"
DL = Path(r"C:\Users\tuana\Downloads")
LOT1 = DL / "Tháng 9 27 - 17_50.zip"
MAP1 = VD / "art_map31_lot1.json"
CUT = 0.905
WM = (0.930, 0.878)
N_SHOTS = 91  # plan31: 81 ô AI + 10 ô 原典
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


def cut(im):
    W, H = im.size
    x1 = int(W * CUT)
    h2 = int(x1 / 16 * 9)
    dy = (H - h2) // 2
    return im.crop((0, dy, x1, dy + h2)).resize((1920, 1080), Image.LANCZOS)


# Ô mà vật chính chạy sát mép phải (cắt 0,905W làm mất nửa vật) mà ✦ nằm trên nền kem PHẲNG,
# tách khỏi vật ⇒ nhánh VÁ (`media-library.md` §2.10 ⑤b mục 3), không cắt. Chốt bằng MẮT 1:1.
#   F61 (shot_070): bó báo kẹp phong bì tới ~0,945W; ✦ ở (0,929W · 0,872H), bó báo kết ở y≈0,74H.
PATCH = {61}
WM_R = 36


def patch_star(im):
    a = np.asarray(im).astype(np.float32)
    H, W = a.shape[:2]
    cx, cy = int(W * 0.930), int(H * 0.873)
    xs = np.r_[cx - 80:cx - 45, cx + 45:min(W, cx + 80)]
    rng = np.random.default_rng(31)
    for y in range(cy - WM_R, cy + WM_R):
        med = np.median(a[y, xs], axis=0)
        a[y, cx - WM_R:cx + WM_R] = med + rng.normal(0, 1.2, (2 * WM_R, 3))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((1920, 1080), Image.LANCZOS)


# Dải trắng + vạch xám generator vẽ NGANG KHUNG (`media-library.md` §2.10 ⑧) — không ở mép
# nên trim không bắt được. Toạ độ trên bản 1920×1080 SAU cắt, đo bằng máy + soi mắt 1:1.
#   F56 (shot_065): vạch xám y 952–964 + dải trắng 966–982, ngay dưới cạnh bàn (y≈930).
BAND = {56: (950, 986)}


def fill_band(im, y0, y1):
    a = np.asarray(im).copy()
    a[y0:y1] = a[y0 - 4]
    return Image.fromarray(a)


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


def imgs(z):
    return [i.filename for i in z.infolist() if i.filename.lower().endswith((".jpg", ".jpeg", ".png"))]


def emit(z, n, d, shot, lot, score, rows, warn, used):
    im = Image.open(io.BytesIO(z.read(n))).convert("RGB")
    li = lost_ink(im)
    if li > 0.5 and d not in PATCH:
        warn.append((d, shot, n[:44], li))
    out = patch_star(im) if d in PATCH else cut(im)
    if d in BAND:
        out = fill_band(out, *BAND[d])
    out.save(ART / f"shot_{shot:03d}.png")
    used.append((lot, n))
    rows.append(dict(flow=d, shot=shot, lot=lot, file=n, score=round(float(score), 2),
                     lost_ink=round(li, 2)))


def main() -> int:
    ten = [l for l in open(VD / "img31_TENFILE.txt", encoding="utf-8") if l.startswith("dong ")]
    shot_of = {int(m.group(1)): int(m.group(2)) for l in ten
               for m in [re.match(r"dong (\d+) -> shot_(\d+)\.png", l)] if m}
    ART.mkdir(parents=True, exist_ok=True)
    rows, warn, used, weak = [], [], [], []

    # ── lô 1: theo bản đồ ĐÃ DUYỆT, bỏ dòng REDO ──
    z1 = zipfile.ZipFile(LOT1)
    m1 = [r for r in json.loads(MAP1.read_text(encoding="utf-8")) if r["flow"] not in REDO1_WHY]
    for r in m1:
        emit(z1, r["file"], r["flow"], shot_of[r["flow"]], 1, r["score"], rows, warn, used)
    rej = ART / "rejected"
    for d in REDO1_WHY:
        f = ART / f"shot_{shot_of[d]:03d}.png"
        if f.exists() and not (len(sys.argv) > 1):
            rej.mkdir(exist_ok=True)
            f.replace(rej / f"lot1_{f.name}")
    print(f"lô 1: {LOT1.name} · nhận {len(m1)} ô (đã soi mắt) · REDO {len(REDO1_WHY)} dòng")

    # ── lô REDO1 (tuỳ chọn) ──
    if len(sys.argv) > 1:
        rd = sorted(REDO1_WHY)
        rflow = [l.rstrip("\n") for l in open(VD / "img31_FLOW_REDO1.txt", encoding="utf-8")]
        if len(rflow) != len(rd):
            print("🔴 img31_FLOW_REDO1 lệch REDO1_WHY — chạy lại img31_prompts.py")
            return 1
        z2 = zipfile.ZipFile(sys.argv[1])
        n2 = imgs(z2)
        print(f"lô REDO1: {Path(sys.argv[1]).name} · {len(n2)} ảnh / {len(rd)} dòng")
        if len(n2) > len(rd):
            print("🔴 lô REDO thừa ảnh — đừng ghép mù")
            return 1
        subs = [l.split("SUBJECT:", 1)[1] for l in rflow]
        nt = [toks(re.sub(r"_\d{14}(_\d)?\.(jpe?g|png)$", "", n).replace("_", " ")) for n in n2]
        M = np.array([[len(toks(s) & b) / max(1, len(b)) for b in nt] for s in subs])
        r, c = linear_sum_assignment(-M)
        for i, j in zip(r, c):
            d = rd[int(i)]
            if M[i, j] < 0.34:
                weak.append((d, shot_of[d], n2[j][:44], M[i, j]))
            emit(z2, n2[j], d, shot_of[d], 2, M[i, j], rows, warn, used)

    (VD / "art_map31.json").write_text(json.dumps(sorted(rows, key=lambda r: r["flow"]),
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ô ảnh AI: {len(rows)} · ảnh bị dùng lại: {len(used) - len(set(used))}")
    print(f"✦: cắt {CUT}W + trim 16:9 → 1920×1080 · VÁ: {sorted(PATCH)} · tô dải: {sorted(BAND)}")
    print(f"⚠️ ô có mực trong dải bị cắt (>0,5%) — SOI MẮT: {len(warn)}")
    for w in warn:
        print("    FLOW %2d · shot_%03d · %s · %.2f%%" % w)
    print(f"⚠️ ô REDO ghép token YẾU (<0,34) — SOI MẮT đúng ô: {len(weak)}")
    for w in weak:
        print("    FLOW %2d · shot_%03d · %s · %.2f" % w)
    got = {r["flow"] for r in rows}
    for d in sorted(set(shot_of) - got):
        print(f"🔴 dòng FLOW {d} (shot_{shot_of[d]:03d}) chưa có ảnh")
    miss = [k for k in range(N_SHOTS) if not (ART / f"shot_{k:03d}.png").exists()]
    print(f"🔴 ô thiếu ảnh trong art_final: {miss}" if miss
          else f"✅ đủ {N_SHOTS}/{N_SHOTS} ô (kể cả 10 原典)")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
