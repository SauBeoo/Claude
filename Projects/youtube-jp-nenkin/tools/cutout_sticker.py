# -*- coding: utf-8 -*-
r"""cutout_sticker.py — cắt nền MAGENTA khỏi lô sticker AI → PNG alpha cho Remotion.

Chép cơ chế đã chứng minh ở `media-library.md` §2.10 ⑨ (lô 12 cast shokutaku), 4 luật:
 ① tách theo **KHOẢNG CÁCH MÀU** tới magenta, không theo ngưỡng sáng (vật của kênh này hay
    là giấy kem / tóc bạc / áo trắng — ngưỡng sáng ăn mất).
 ② 🔴 **CO MASK vào ~3px** (`erode`), đừng "sửa màu" pixel viền: cách sai đã đo là hạ R/B
    theo G → 1.400/1.400 px viền VẪN tím, vì magenta có G≈0 nên hạ xong ra (145,0,90) = vẫn
    đỏ tím. Suy màu từ pixel đã nhiễm thì không bao giờ sạch. Ảnh có viền giấy trắng dày nên
    co 3px là mọi pixel còn lại nằm sâu trong viền.
 ③ **Lọc BLOB LỚN NHẤT** — bắt buộc, không phải tối ưu: dấu ✦ watermark là trắng nhạt trên
    magenta nên ngưỡng màu KHÔNG loại nó ⇒ bbox phình tới góc dưới-phải và sticker mang theo
    một đốm sáng. (Đây cũng là lý do lô này không cần bước xoá ✦ riêng.)
 ④ **Nghiệm thu: dán lên ĐÚNG màu nền khung** rồi soi — trên nền trắng thì vệt tím vô hình.

CHẠY:  python tools/cutout_sticker.py <slug> [--src <thư mục ảnh gen>]
"""
import pathlib
import sys
from pathlib import Path

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
DEFAULT_SRC = Path(r"C:\Users\tuana\Downloads")

# Map TIỀN TỐ tên file generator → tên đích. Generator đặt tên theo NỘI DUNG ảnh nó vẽ,
# nên thứ tự alphabet KHÔNG khớp thứ tự SPEC ⇒ phải map tường minh, đối chiếu bằng mắt.
MAP = {
    "Smartphone_collage_on_magenta":     "el_smartphone.png",
    "Green_tea_cup_on_saucer":           "el_teacup.png",
    "Folded_vintage_newspaper_collage":  "el_newspaper.png",
    "Telephone_handset_radiating_soun":  "el_speaker_robot.png",
    "Desk_calendar_page_on_magenta":     "el_calendar.png",
    "Closed_Japanese_bank_passbook":     "el_passbook.png",
    "Blank_ID_card_collage":             "el_mynumber_card.png",
    "Elderly_man_hand_collage":          "el_hand_stop.png",
    "Red_starburst_paper_collage":       "el_burst_red.png",
    "Blank_booklet_on_magenta":          "el_nenkin_techo.png",
    "Elderly_man_using_telephone":       "el_senior_phone.png",
    "Blank_emblem_paper_collage":        "el_police_badge.png",
    "Stack_of_Japanese_coins":           "el_coin_stack.png",
    "Bar_chart_rising_arrow":            "el_chart_up.png",
    "Elderly_men_fishing_collage":       "el_two_anglers.png",
}

# LÔ v18 (2026-08-30) — 6 sticker giảm lặp cho video 18, đối chiếu mắt sheet Downloads/download (2)
MAP18 = {
    "Blank_paper_slips_collage":         "el_house_bills.png",
    "Blank_signpost_pointing_three":     "el_signpost.png",
    "Magnifying_glass_on_magenta":       "el_magnifying_glass.png",
    "Medicine_bottle_and_pill_collage":  "el_medicine_bottle.png",
    "Paper_heart_with_ECG_line":         "el_heart_pulse.png",
    "Percent_symbol_paper_collage":      "el_percent_badge.png",
}

MAGENTA = np.array([255, 0, 255], dtype=np.float32)   # BGR-agnostic: so ở RGB
TOL = 118.0        # khoảng cách màu tới magenta coi là NỀN
ERODE_PX = 3       # luật ② — co mask vào trong, giữ viền giấy trắng
PAPER = (242, 237, 228)   # màu nền khung để nghiệm thu (luật ④)


def _imread(p):
    """🔴 `cv2.imread` KHÔNG đọc được path có ký tự non-ASCII trên Windows (trả None).
    Tên file generator đặt có ký tự `…` (U+2026) ⇒ 2/15 ảnh báo "đọc không được".
    Đọc bằng numpy rồi `imdecode` là đường duy nhất chạy được với path Unicode."""
    buf = np.fromfile(str(p), dtype=np.uint8)
    return cv2.imdecode(buf, cv2.IMREAD_COLOR)


def _imwrite(p, im):
    """cv2.imwrite cũng chết với path Unicode — encode rồi tofile."""
    ok, buf = cv2.imencode(pathlib.Path(p).suffix, im)
    if ok:
        buf.tofile(str(p))
    return ok


def cut(path_in, path_out):
    im = _imread(path_in)
    if im is None:
        return None, "đọc không được"
    rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32)
    dist = np.linalg.norm(rgb - MAGENTA, axis=2)
    fg = (dist > TOL).astype(np.uint8)                      # 1 = vật

    # ③ chỉ giữ khối lớn nhất — loại ✦ watermark và vụn rác
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fg, 8)
    if n > 1:
        big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        dropped = n - 2
        fg = (lab == big).astype(np.uint8)
    else:
        dropped = 0

    # ② co mask vào trong
    fg = cv2.erode(fg, np.ones((3, 3), np.uint8), iterations=ERODE_PX)

    # ②b 🔴 LOẠI PIXEL MAGENTA KHỎI MASK — erode hình học MỘT MÌNH KHÔNG ĐỦ.
    # Đo thật lô 15 ảnh (2026-08-26): sau erode 3px vẫn còn **tới 21.573 px** viền tím
    # (`el_mynumber_card`). Lý do: viền giấy trắng của ảnh gen bị nhiễm magenta khá sâu và
    # KHÔNG thuần magenta nữa (dist > TOL) nên nó nằm trong fg, erode chỉ cắt theo hình
    # học nên không biết pixel nào bị nhiễm. ⇒ phải loại theo MÀU: pixel nào ngả magenta
    # (R−G>34 và B−G>34) thì bỏ khỏi mask, rồi mới co 1px cho mượt.
    rgbi = rgb.astype(np.int16)
    magenta_ish = ((rgbi[:, :, 0] - rgbi[:, :, 1] > 34) &
                   (rgbi[:, :, 2] - rgbi[:, :, 1] > 34)).astype(np.uint8)
    fg = (fg & (1 - magenta_ish)).astype(np.uint8)
    fg = cv2.erode(fg, np.ones((3, 3), np.uint8), iterations=1)
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    # giữ lại đúng khối lớn nhất lần nữa (loại theo màu có thể chẻ mask thành nhiều mảnh)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(fg, 8)
    if n2 > 2:
        fg = (lab2 == 1 + int(np.argmax(st2[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)

    a = (fg * 255).astype(np.uint8)
    out = np.dstack([cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)[:, :, :3], a])
    ys, xs = np.where(fg > 0)
    if len(xs) == 0:
        return None, "mask RỖNG — nền có phải magenta thuần không?"
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    _imwrite(path_out, out)

    # 🔴 PHÉP ĐO PHẢI ĐẾM PIXEL ĐẶC, KHÔNG PHẢI PIXEL BÁN TRONG SUỐT.
    # Bản đầu đếm `8 < alpha < 250` → **luôn trả 0** vì erode cho alpha nhị phân (0/255),
    # nên gate báo "sạch" trong khi mắt thấy vệt tím rõ ở 14/15 ảnh. Đây đúng là cái
    # `media-library.md` §2.10 ⑤ cảnh báo: *số đo và exit code không chứng minh ✦/vệt đã
    # sạch*. Phép đo đúng: pixel **alpha>250** mà ngả magenta.
    o = out.astype(np.int16)
    op = o[:, :, 3] > 250
    tint = int(np.sum(op & (o[:, :, 2] - o[:, :, 1] > 40) & (o[:, :, 0] - o[:, :, 1] > 40)))
    return (out.shape[1], out.shape[0], dropped, tint), None


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
    if not slug:
        print("dùng: python tools/cutout_sticker.py <slug> [--src <folder>]")
        return 1
    src = DEFAULT_SRC
    if "--src" in sys.argv:
        src = Path(sys.argv[sys.argv.index("--src") + 1])
    global MAP
    if "--v18" in sys.argv:
        MAP = MAP18
    vdir = PROJ / "06_VIDEO" / slug
    dst = vdir / "sticker"
    dst.mkdir(parents=True, exist_ok=True)

    files = []
    for ext in ("*.jpeg", "*.jpg", "*.png"):
        files += sorted(src.glob(ext))
    if not files:
        print(f"⚠ không thấy ảnh nào trong {src}")
        return 1

    print(f"   {len(files)} ảnh nguồn · {len(MAP)} tên đích cần map")
    print("⚠ MAP THEO TIỀN TỐ TÊN FILE, đối chiếu bằng MẮT 2026-08-26 — KHÔNG map theo thứ")
    print("  tự: generator đặt tên theo NỘI DUNG ảnh nên thứ tự alphabet ≠ thứ tự SPEC.")
    ok, used = 0, set()
    for prefix, name in MAP.items():
        cand = [f for f in files if f.name.startswith(prefix) and f not in used]
        if not cand:
            print(f"🔴 THIẾU nguồn: {prefix} → {name}")
            continue
        f = cand[0]
        used.add(f)
        r, err = cut(f, dst / name)
        if err:
            print(f"🔴 {f.name} → {name}: {err}")
            continue
        w, h, dropped, tint = r
        flag = "" if tint == 0 else f"  ⚠ {tint}px vệt tím"
        print(f"   ✓ {name:<26} {w}×{h}  blob bỏ={dropped}{flag}")
        ok += 1
    print(f"\n✓ {ok}/{len(MAP)} sticker → {dst}")
    print("⛔ NGHIỆM THU: dán lên nền kem (242,237,228) rồi soi sheet — nền trắng che vệt tím")
    return 0


if __name__ == "__main__":
    sys.exit(main())
