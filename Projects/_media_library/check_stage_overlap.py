# -*- coding: utf-8 -*-
"""check_stage_overlap.py — GATE MÁY: dò thẻ sân khấu có CHỮ ĐỌC KHÔNG ĐƯỢC.

HAI LẦN SAI CỦA GATE NÀY, ghi lại để không lặp:
  · v1 (2026-08-10 sáng) đo "pixel chữ có ĐỔI MÀU không" → bắt được ca ảnh `fill` ĐÈ lên chữ,
    nhưng **cho qua** ca clip_53 「待たずに、聞く」: dòng ✗ màu xám nằm trên cái điện thoại xám
    (chỉ 33 px đổi màu, dưới ngưỡng) — chữ vẫn mất hẳn. Vì "đổi màu" ≠ "đọc được".
  · v2 (file này) đo ĐÚNG THỨ CẦN ĐO: **tương phản độ sáng giữa pixel chữ và nền quanh nó**,
    trên chính khung có ảnh. Chữ trùng màu nền ⇒ tương phản thấp ⇒ FAIL, dù chẳng "đè" gì.

CÁCH ĐO
  1. Dựng 2 khung: có ảnh (A) và bỏ hết khoá ảnh (B).
  2. Mặt nạ CHỮ = pixel ở B khác màu card → đó chắc chắn là chữ/ký hiệu, không phải ảnh.
  3. Trên A: so độ sáng trung vị của pixel-chữ với độ sáng trung vị của VÀNH quanh chữ
     (giãn mặt nạ rồi trừ đi chính nó). Chênh < `--min-contrast` ⇒ chữ chìm.
  4. Báo cả pixel chữ bị ảnh phủ trực tiếp (giữ phép đo của v1 làm chỉ số phụ).

CHẠY: python check_stage_overlap.py --slides <SLIDES.json> --art <art dir> [--channel nenkin]
Exit 1 nếu có thẻ lỗi (cắm vào .cmd làm gate).
"""
import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

IMG_KEYS = ("img", "fill", "bgimg")


def boxsum(x, r):
    """Tổng cửa sổ (2r+1)² bằng ảnh tích phân — PIL không blur được mode 'F'."""
    p = np.pad(x, r + 1, mode="edge")
    s = p.cumsum(0).cumsum(1)
    s = np.pad(s, ((1, 0), (1, 0)))
    h, w = x.shape
    return (s[2 * r + 1:2 * r + 1 + h, 2 * r + 1:2 * r + 1 + w]
            - s[0:h, 2 * r + 1:2 * r + 1 + w]
            - s[2 * r + 1:2 * r + 1 + h, 0:w] + s[0:h, 0:w])


def load_ms():
    spec = importlib.util.spec_from_file_location(
        "ms", Path(__file__).resolve().parent / "make_stage.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    return ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides", required=True)
    ap.add_argument("--art", required=True)
    ap.add_argument("--channel")
    ap.add_argument("--min-contrast", type=float, default=42.0,
                    help="chênh độ sáng tối thiểu giữa chữ và nền quanh nó (0–255)")
    ap.add_argument("--max-covered", type=int, default=60,
                    help="số pixel chữ bị ảnh phủ trực tiếp thì coi là bị đè")
    a = ap.parse_args()

    ms = load_ms()
    if a.channel:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                               "youtube-jp-health" / "tools"))
        from channels import CHANNELS  # noqa: PLC0415
        ch = CHANNELS[a.channel]
        for k, g in (("stage_card", "CARDC"), ("stage_bg_top", "BG_TOP"),
                     ("stage_bg_bot", "BG_BOT")):
            if ch.get(k):
                setattr(ms, g, tuple(ch[k]))
        ms._BG_CACHE.clear()
    ms.ART_ROOTS[:] = [Path(a.art)]

    sl = json.loads(Path(a.slides).read_text(encoding="utf-8"))
    X0, X1 = ms.CONTENT_X0 - 80, ms.CONTENT_X1 + 80
    Y0, Y1 = ms.CARD_Y0 + 16, ms.CARD_Y1 - 16
    card = np.array(ms.CARDC, dtype=int)
    bad = []
    for i, e in enumerate(sl):
        sp = e.get("stage")
        if not sp or not any(sp.get(k) for k in IMG_KEYS):
            continue
        if sp.get("layout") in ("art", "photo"):
            continue                      # ảnh LÀ nội dung, không có chữ để chìm
        clean = copy.deepcopy(sp)
        for k in IMG_KEYS:
            clean.pop(k, None)
        A = np.asarray(ms.frame(copy.deepcopy(sp), 99)[0]).astype(int)[Y0:Y1, X0:X1]
        B = np.asarray(ms.frame(clean, 99)[0]).astype(int)[Y0:Y1, X0:X1]
        ink = np.abs(B - card).sum(2) > 90          # mặt nạ CHỮ (từ khung không ảnh)
        if ink.sum() < 200:
            continue
        # 🔴 SỬA 2 LỖI ĐO (2026-08-10, sau khi gate v2 vẫn cho clip_53 lọt):
        # ① **Trung vị toàn bộ chữ CHE MẤT một dòng chìm** — thẻ 53 ra 194 vì tiêu đề + dòng ✓
        #    đậm chiếm đa số, còn dòng ✗ xám trên điện thoại xám chỉ là thiểu số.
        #    ⇒ đo tương phản TỪNG PIXEL rồi lấy **phân vị 5%** (chỗ tệ nhất), không lấy trung vị.
        # ② **Chỉ số "phủ" vô nghĩa với `bgimg`** — ảnh nền làm CẢ tấm bảng đổi màu theo thiết kế,
        #    nên mọi pixel chữ đều "đổi" (8.000–13.000 px) và gate báo động sai hàng loạt.
        #    ⇒ chỉ kiểm "phủ" khi thẻ dùng `fill` (hộp ảnh đè lên), không kiểm với `bgimg`.
        # ⚠️ LỖI ĐO THỨ BA (cùng lượt): ước lượng nền bằng blur CẢ khung thì blur chứa luôn
        # chữ → lõi nét chữ ra ~0 tương phản và gate báo động toàn bộ 20 thẻ.
        # ⇒ Nền phải ước lượng **CHỈ TỪ PIXEL KHÔNG PHẢI CHỮ**: lấy trung bình cục bộ của
        # vùng ngoài mặt nạ (blur giá trị đã che, chia cho blur của chính mặt nạ).
        lumA = A.mean(2)
        notink = (~ink).astype(np.float64)
        R = 19
        num, den = boxsum(lumA * notink, R), boxsum(notink, R)
        # ⚠️ LỖI ĐO THỨ TƯ: lõi nét chữ HERO rất dày (cỡ ~200px) nên cửa sổ 19px quanh nó
        # gần như toàn chữ ⇒ `den` ~0 ⇒ không có nền để so ⇒ trước đây fallback về lumA và
        # ra tương phản 0,0, gate báo động sai ở [20] và [30]. Đúng cách: **loại những pixel
        # KHÔNG ĐO ĐƯỢC** khỏi phép thống kê, đừng gán cho chúng một con số bịa.
        area = (2 * R + 1) ** 2
        ok_px = den > area * 0.15
        bgest = num / np.maximum(den, 1e-6)
        sel = ink & ok_px
        if sel.sum() < 200:
            print(f"  [{i:02d}] {sp.get('layout'):7s} (chữ quá dày, không đủ nền để đo — bỏ qua)")
            continue
        per_px = np.abs(lumA - bgest)[sel]
        c = float(np.percentile(per_px, 5))
        covered = (int((ink & (np.abs(A - B).mean(2) > 40)).sum())
                   if sp.get("fill") else 0)
        fail = c < a.min_contrast or covered > a.max_covered
        tag = "🔴 CHỮ CHÌM" if c < a.min_contrast else ("🔴 BỊ ĐÈ" if fail else "ok")
        print(f"  [{i:02d}] {sp.get('layout'):7s} tương phản p5 {c:5.1f}  phủ {covered:5d}  "
              f"{tag:12s} {sp.get('title','')[:30]}")
        if fail:
            bad.append((i, sp.get("layout"), round(c, 1), covered, sp.get("title", "")[:32]))
    print()
    if bad:
        print(f"🔴 {len(bad)} THẺ CHỮ KHÔNG ĐỌC ĐƯỢC (ngưỡng tương phản {a.min_contrast}):")
        for i, L, c, cv, t in bad:
            print(f"     [{i:02d}] {L} tương phản {c} · phủ {cv}px  {t}")
        sys.exit(1)
    print(f"✅ Mọi thẻ có ảnh đều đạt tương phản ≥ {a.min_contrast}")


if __name__ == "__main__":
    main()
