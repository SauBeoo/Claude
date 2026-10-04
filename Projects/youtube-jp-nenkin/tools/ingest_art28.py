# -*- coding: utf-8 -*-
r"""ingest_art28.py — gom ảnh 92 ô của video 28 từ 4 lô gen, xoá ✦, chuẩn hoá.

VÌ SAO CÓ BẢNG MAP TAY (`art_map28.json`):
tên file do model đặt theo nội dung, **trùng nhau hàng loạt** (`Elderly_woman_climbing_step_blocks`
có 4 bản trong một lô) ⇒ khớp bằng token tên file sai 17/92 ô. Bảng map được soi bằng mắt qua
contact sheet, và từ vòng REDO3 trở đi ảnh CÓ CHỮ nên map chắc chắn.

ƯU TIÊN LÔ MỚI: 17_30 > 17_05 > 16_44 > 15_50 — mỗi lô sau là một vòng sửa của lô trước.

XOÁ ✦ (`media-library.md` §2.10 ⑤b — luật cứng: ảnh còn ✦ = chưa xong):
lô này 1376×768, ✦ cố định ở **(0,937W · 0,879H)**, soi mắt trên 6 mẫu.
⛔ KHÔNG tô màu nền: có ảnh ✦ nằm **đè lên khối navy**, tô kem là ra vệt.
⇒ dùng `cv2.inpaint` Navier-Stokes với mask = pixel sáng hơn trung vị cục bộ. Nền là một tông
phẳng nên không cần ghép vân như §2.10 ⑥b (ca ảnh thật có vệt nắng chéo).

CHẠY:  python tools/ingest_art28.py            → art_final/shot_KKK.png + kiểm
       python tools/ingest_art28.py --probe    → thêm sheet soi góc ✦ sau khi vá
"""
import io
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "28_kouki-75sai-tanjyotsuki-hokenryo"
VD = PROJ / "06_VIDEO" / STEM
DL = Path(r"C:\Users\tuana\Downloads")
LOTS = {"17_30": DL / "Sep 18 - 17_30", "17_05": DL / "Sep 18 - 17_05",
        "16_44": DL / "Sep 18 - 16_44", "15_50": DL / "Sep 18 - 15_50 (1)"}

STAR_XY = (0.937, 0.879)     # tâm ✦, đo bằng mắt trên 6 mẫu của lô này
STAR_R = 46                  # bán kính hộp quét (✦ đo được ~50px bề ngang)


def find_file(lot: str, prefix: str):
    """Tìm file theo tiền tố. Hậu tố `|2` = lấy bản THỨ HAI cùng tiền tố."""
    want2 = prefix.endswith("|2")
    pre = prefix[:-2] if want2 else prefix
    d = LOTS[lot]
    hits = sorted(f for f in os.listdir(d) if f.startswith(pre))
    if not hits:
        return None
    return d / (hits[1] if (want2 and len(hits) > 1) else hits[0])


def strip_star(bgr):
    """Xoá ✦ bằng inpaint. Trả (ảnh, số pixel đã vá)."""
    h, w = bgr.shape[:2]
    cx, cy = int(w * STAR_XY[0]), int(h * STAR_XY[1])
    x0, y0 = max(0, cx - STAR_R), max(0, cy - STAR_R)
    x1, y1 = min(w, cx + STAR_R), min(h, cy + STAR_R)
    box = bgr[y0:y1, x0:x1]
    g = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY).astype(np.int16)
    # ✦ sáng hơn NỀN CỤC BỘ (kem lẫn navy) ⇒ so với trung vị của chính hộp
    med = int(np.median(g))
    # 🔴 NGƯỠNG ĐO ĐƯỢC, KHÔNG ĐOÁN: ✦ chỉ sáng hơn nền **7 mức** (237 -> 244).
    # Bản đầu đặt >10 ⇒ bắt 0 px trên 75/92 ảnh, và exit code vẫn 0 — đúng cảnh báo
    # `media-library.md` §2.10 ⑤: *số đo và exit code không chứng minh ✦ đã sạch*.
    # Chỉ soi mắt góc ảnh mới lộ. Ngưỡng 3 bắt ~700 px = đúng cỡ ✦.
    mask = ((g - med) > 3).astype(np.uint8) * 255
    # kẹp mask trong đĩa r=40 quanh tâm ✦ — chặn nó lan sang vật sáng khác trong hộp
    yy, xx = np.ogrid[:mask.shape[0], :mask.shape[1]]
    disc = ((xx - (cx - x0))**2 + (yy - (cy - y0))**2) <= 40**2
    mask[~disc] = 0
    if mask.sum() == 0:
        return bgr, 0
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
    box_fixed = cv2.inpaint(box, mask, 6, cv2.INPAINT_NS)
    out = bgr.copy()
    out[y0:y1, x0:x1] = box_fixed
    return out, int((mask > 0).sum())


def main() -> int:
    mp = json.loads((VD / "art_map28.json").read_text(encoding="utf-8"))
    dst = VD / "art_final"
    dst.mkdir(parents=True, exist_ok=True)

    used, miss, done, patched = {}, [], 0, 0
    for k in range(92):
        ent = mp.get(str(k))
        if not ent:
            miss.append((k, "chưa map"))
            continue
        lot, pre = ent
        src = find_file(lot, pre)
        if src is None:
            miss.append((k, f"{lot}/{pre} KHÔNG THẤY FILE"))
            continue
        key = str(src)
        used.setdefault(key, []).append(k)
        img = cv2.imdecode(np.fromfile(str(src), dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            miss.append((k, f"đọc lỗi {src.name}"))
            continue
        img, npx = strip_star(img)
        patched += 1 if npx else 0
        if (img.shape[1], img.shape[0]) != (1920, 1080):
            img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
        Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(dst / f"shot_{k:03d}.png")
        done += 1

    dup = {f: ks for f, ks in used.items() if len(ks) > 1}
    print(f"ingest: {done}/92 ô · đã vá ✦ {patched} ảnh")
    print(f"ảnh bị dùng lại: {len(dup)}")
    for f, ks in dup.items():
        print(f"   🔴 {Path(f).name[:52]} -> ô {ks}")
    if miss:
        print(f"\n🔴 THIẾU {len(miss)} ô:")
        for k, why in miss:
            print(f"   ô {k}: {why}")
    (VD / "_MISSING_ART.json").write_text(
        json.dumps([k for k, _ in miss], ensure_ascii=False), encoding="utf-8")
    return 1 if (miss or dup) else 0


if __name__ == "__main__":
    raise SystemExit(main())
