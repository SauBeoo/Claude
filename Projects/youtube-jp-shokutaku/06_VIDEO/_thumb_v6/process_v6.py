# -*- coding: utf-8 -*-
"""process_v6.py — làm sạch + đóng dấu 食卓 cho lô thumbnail v6 (9 video, gen 2026-08-05).

Luồng (đúc từ 4 lần làm ở co-dai):
  1. clone-stamp xoá watermark ✦ với offset do MÁY tìm (KHÔNG dùng cv2.inpaint — nền có
     kết cấu thì nó trả ô phẳng còn hằn bóng ngôi sao).
  2. chuẩn khung: ảnh gen 2752×1536 = 1,7917 KHÔNG phải 16:9 → center-crop + resize 1920×1080.
  3. tự CHỌN GÓC đóng badge: chấm điểm 4 góc theo mật độ chữ + năng lượng biên, ưu tiên góc
     ở phía ĐỐI DIỆN cột chữ, tránh góc dưới-phải (YouTube đè ô thời lượng).
  4. đóng dấu bằng tools/stamp_brand_shokutaku.py (spec khoá).
  5. đo dòng chính (% chiều cao) + xuất contact sheet 168/120 để duyệt mắt.
"""
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
PROJ = HERE.parents[1]
sys.path.insert(0, str(PROJ.parent / "youtube-jp-co-dai" / "06_VIDEO" / "_thumb_v3"))
sys.path.insert(0, str(HERE))
from fix_v3 import best_offset, clone_patch, to_16x9  # noqa: E402
from find_sparkles import find_sparkles  # noqa: E402

# video → (videoId, file nguồn trong Downloads)
DL = Path(r"C:\Users\tuana\Downloads")
JOBS = [
    ("01", "mQevRS1qBbk", "Soft-boiled_egg_on_ceramic_dish_202608051907.jpeg"),
    ("02", "31KXwgHbLY0", "Bowl_of_blueberries_on_table_202608051720.jpeg"),
    ("03", "BKh-sdhsNUg", "Anatomical_kidney_model_on_counter_202608051729.jpeg"),
    ("04", "DD_AED6woII", "Glass_of_milk_and_bone_202608051737.jpeg"),
    ("05", "BL7KtdXpl_A", "Natto_bowl_and_kidney_model_202608051739.jpeg"),
    ("06", "dabD8WcvXu8", "Glass_of_tomato_juice_2K_202608051742.jpeg"),
    ("07", "utNRgxBSf-8", "Bowl_of_azuki_beans_2K_202608051749.jpeg"),
    ("08", "ySxrtSzj8Bg", "Teapot_and_teacup_on_table_202608051921.jpeg"),
    ("09", "LvBPBN1Jg4U", "Wooden_dipper_lifting_honey_2K_202608051906.jpeg"),
    ("10", "Iazj6ey7gyI", "Half_cabbage_on_cutting_board_202608051906.jpeg"),
]


def text_mask(a: np.ndarray) -> np.ndarray:
    """Pixel thuộc khối chữ: trắng / đỏ / vàng bão hoà, HOẶC viền đen dày quanh chúng."""
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lum = 0.299 * R + 0.587 * G + 0.114 * B
    mx, mn = a.max(2), a.min(2)
    white = (lum > 210) & ((mx - mn) < 45)
    red = (R > 165) & (R - G > 70) & (R - B > 70)
    yellow = (R > 200) & (G > 155) & (B < 115)
    dark = lum < 70
    m = (white | red | yellow).astype(np.uint8)
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    return ((m > 0) & (white | red | yellow | dark)).astype(np.uint8)


def pick_corner(a: np.ndarray) -> tuple[str, dict]:
    """Chọn góc rảnh nhất cho badge. Điểm càng thấp càng rảnh."""
    H, W = a.shape[:2]
    tm = text_mask(a)
    gray = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    edge = cv2.Laplacian(gray, cv2.CV_64F)
    bs = int(H * 0.32)                                  # ô góc rộng hơn badge một chút
    boxes = {"tl": (0, 0), "tr": (W - bs, 0), "bl": (0, H - bs), "br": (W - bs, H - bs)}
    # phía cột chữ = nửa nào nhiều pixel chữ hơn
    txt_right = tm[:, W // 2:].sum() > tm[:, :W // 2].sum()
    sc = {}
    for k, (x, y) in boxes.items():
        t = tm[y:y + bs, x:x + bs].mean()
        e = np.abs(edge[y:y + bs, x:x + bs]).mean() / 255
        pen = 0.0
        if k == "br":
            pen += 5.0                                   # ô thời lượng YouTube
        if (k in ("tr", "br")) == txt_right:
            pen += 1.5                                   # cùng phía cột chữ
        if k in ("bl", "br"):
            pen += 0.25                                  # ưu tiên nhẹ cho góc trên
        sc[k] = round(t * 10 + e + pen, 3)
    return min(sc, key=sc.get), sc


# Ghi đè tay khi auto-pick đè lên CHỦ THỂ (auto chỉ đo mật độ chữ + biên, không biết đâu là
# phần nhận diện của món): 03 badge tr trùm đỉnh mô hình thận · 05 tr trùm đỉnh thận ·
# 06 bl nằm trên chùm cà chua. Cả 3 dời sang góc trống thật.

def best_offset_avoid(im, box, avoid, ring=18, span=460, step=6, horizontal_only=False):
    """Như best_offset nhưng CẤM lấy nguồn ở vùng có vệt ✦ khác.

    🔴 Bẫy dính 2026-08-05 (ca 07 あずき, 3 vệt gần nhau): best_offset chấm điểm bằng vành
    quanh hộp; vành quanh vệt A giống vành quanh vệt B nên nó chọn nguồn = chỗ vệt B →
    vá xong DÁN THÊM một ngôi sao vào. Lặp mấy vòng vẫn 'CÒN 2 vệt' đúng vì thế.
    """
    import numpy as _np
    a = _np.array(im.convert("RGB")).astype(_np.float32)
    H, W = a.shape[:2]
    x0, y0, x1, y1 = box
    ox0, oy0, ox1, oy1 = x0 - ring, y0 - ring, x1 + ring, y1 + ring
    tgt = a[oy0:oy1, ox0:ox1]
    hole = _np.ones(tgt.shape[:2], bool)
    hole[ring:-ring, ring:-ring] = False
    best, bo = None, (0, 0)
    dys = [0] if horizontal_only else range(-span, span + 1, step)
    for dy in dys:
        for dx in range(-span, span + 1, step):
            if abs(dx) < (x1 - x0) // 2 and abs(dy) < (y1 - y0) // 2:
                continue
            sx0, sy0, sx1, sy1 = ox0 + dx, oy0 + dy, ox1 + dx, oy1 + dy
            if not (0 <= sx0 and sx1 <= W and 0 <= sy0 and sy1 <= H):
                continue
            if any(not (sx1 <= b[0] or sx0 >= b[2] or sy1 <= b[1] or sy0 >= b[3]) for b in avoid):
                continue                      # nguồn chạm vệt khác → bỏ
            cand = a[sy0:sy1, sx0:sx1]
            if cand.shape != tgt.shape:
                continue
            d = float(((cand[hole] - tgt[hole]) ** 2).mean())
            if best is None or d < best:
                best, bo = d, (dx, dy)
    return bo, best


# Ảnh có VÂN CHẠY NGANG (mặt bàn gỗ 07): chỉ được clone dịch NGANG, dy=0. Bẫy đã dính:
# để best_offset tự do 2 trục thì nó chọn (dx,dy) làm lệch vân → hằn nguyên VỆT CHỮ NHẬT
# trên gỗ, nhìn tệ hơn hẳn cái watermark định xoá.
HORIZONTAL_ONLY = set()

# ⛔ BỎ VÁ HẲN cho các ảnh này — ĐÃ THỬ VÀ DỪNG (2026-08-05, video 07 あずき).
# Vùng ✦ của 07 nằm đúng ranh sáng/tối chéo trên mặt bàn gỗ vân ngang. Đã thử: best_offset
# tự do 2 trục · ép dy=0 (giữ vân) · hộp trùm cả chùm. Cách nào cũng hằn một VỆT CHỮ NHẬT
# rõ hơn hẳn cái watermark mờ định xoá. → Giữ nguyên 2 ✦ mờ, đó là lựa chọn ÍT XẤU HƠN.
# Muốn sạch tuyệt đối thì gen lại ảnh 07, không phải vá thêm.
SKIP_PATCH = {"07"}

# 🔴 HỘP TAY, chỉ cho ảnh còn sót sau khi dò tự động (01·07 — đã soi bằng mắt).
# Lý do phải có: mỗi ảnh có HAI ✦ cạnh nhau (một to ~96px + một nhỏ ~48px). Phép MORPH_CLOSE
# của detector nhập nhèm hai cái thành MỘT hộp nằm GIỮA chúng → vá vào khoảng trống, không
# trúng cái nào, mà hàm vẫn báo "đã vá 1 vệt". Hộp dưới trùm cả chùm.
MANUAL_BOXES = {
    "01": [(2495, 1270, 2705, 1500)],   # nới lên 30px: còn sót chóp trên của ngôi sao
    "07": [(2495, 1300, 2705, 1500)],
}

CORNER_FIX = {"03": "bl", "06": "tl", "08": "tl"}  # 08: bl đè lên chén trà (chủ thể)  # 05 BỎ override: bl đè mất chữ 「7」 của 「7つの組合せ」 — auto-pick tr đúng


def main() -> None:
    (HERE / "src").mkdir(parents=True, exist_ok=True)
    rows = []
    for n, vid, fname in JOBS:
        src = HERE / "src" / f"{n}_src.jpg"
        # LUÔN ghi đè: bẫy đã dính — lô trước để lại 04_src.jpg (bản bảng đen) nên bản mới
        # bị bỏ qua và đóng dấu lên ẢNH CŨ. Cùng họ bẫy resume của render (render-background §2.5).
        src.write_bytes((DL / fname).read_bytes())
        im = Image.open(src).convert("RGB")

        # 🔴 KHÔNG dùng hộp cố định nữa. Bẫy dính 2026-08-05: các bản 01·08 có HAI dấu ✦
        # (một to mờ + một nhỏ); WM_BOX chỉ trùm cái nhỏ nên cái to còn nguyên, mà lệnh vẫn
        # in như thành công. Vị trí ✦ không cố định ⇒ phải DÒ rồi vá từng vệt.
        # 🔴 Bẫy thứ hai (ca 07): dò trên ảnh ĐÃ thu nhỏ 1920 thì vệt mờ tụt dưới ngưỡng →
        # bỏ sót, rồi hiện lại sau khi nén JPEG. ⇒ dò + vá ở FULL-RES rồi mới resize.
        Ws, Hs = im.size
        boxes = [] if n in SKIP_PATCH else (MANUAL_BOXES.get(n) or find_sparkles(im))
        R = 22
        boxes = [(max(R, b[0]), max(R, b[1]), min(Ws - R, b[2]), min(Hs - R, b[3])) for b in boxes]
        boxes = [b for b in boxes if b[2] - b[0] > 8 and b[3] - b[1] > 8]
        for bx in boxes:
            o2, _ = best_offset_avoid(im, bx, [b for b in boxes if b is not bx],
                                      horizontal_only=(n in HORIZONTAL_ONLY))
            im = clone_patch(im, bx, o2)
        left = [] if n in SKIP_PATCH else find_sparkles(im)
        if left:
            print(f"[{n}] ⚠️ CÒN {len(left)} vệt ✦ sau khi vá: {left}")
        ssd = f"{len(boxes)} vệt"
        off = boxes

        out = to_16x9(im)
        png = HERE / f"{n}_v6.png"
        out.save(png)

        corner, sc = pick_corner(np.array(out))
        corner = CORNER_FIX.get(n, corner)
        r = subprocess.run(
            [sys.executable, str(PROJ / "tools" / "stamp_brand_shokutaku.py"), str(png),
             "-o", str(HERE / f"{n}_v6_brand.png"), "--corner", corner],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode:
            print(f"[{n}] ❌ stamp lỗi: {(r.stderr or '').strip()[:200]}")
            continue
        bp = HERE / f"{n}_v6_brand.png"
        jp = HERE / f"{n}_v6_brand.jpg"
        Image.open(bp).save(jp, quality=92, subsampling=0)

        # đo dòng chính (khối chữ ĐỎ hoặc VÀNG cao nhất)
        b = np.array(Image.open(jp).convert("RGB")).astype(np.int16)
        H, W = b.shape[:2]
        R, G, B = b[:, :, 0], b[:, :, 1], b[:, :, 2]
        # 🔴 Bẫy đo: cà chua / mô hình thận cũng ĐỎ → mask đỏ đếm luôn cả món, ra 54% ảo.
        # Chỉ đo trong nửa khung CÓ cột chữ, và trừ ô badge.
        tmh = text_mask(np.array(Image.open(jp).convert("RGB")))
        txt_right = tmh[:, W // 2:].sum() > tmh[:, :W // 2].sum()
        best = 0
        for m in (((R > 170) & (R - G > 70) & (R - B > 70)),
                  ((R > 205) & (G > 160) & (B < 115))):
            mm = m.astype(np.uint8)
            if txt_right:
                mm[:, :int(W * 0.45)] = 0
            else:
                mm[:, int(W * 0.55):] = 0
            mm[:int(H * 0.34), int(W * 0.70):] = 0        # trừ ô badge nếu ở tr
            mm[:int(H * 0.34), :int(W * 0.30)] = 0        # trừ ô badge nếu ở tl
            mm[int(H * 0.66):, :int(W * 0.30)] = 0        # badge bl
            mm[int(H * 0.66):, int(W * 0.70):] = 0        # badge br
            cn, _, st, _ = cv2.connectedComponentsWithStats(mm, 8)
            for j in range(1, cn):
                if st[j, cv2.CC_STAT_AREA] > 3000 and st[j, cv2.CC_STAT_HEIGHT] < H * 0.55:
                    best = max(best, st[j, cv2.CC_STAT_HEIGHT])
        lum = (0.299 * R + 0.587 * G + 0.114 * B).mean()
        rows.append((n, vid, corner, best / H * 100, lum, jp.stat().st_size / 1024 / 1024, ssd))
        print(f"[{n}] ✦vá {ssd} badge={corner} {sc} | dòng chính {best/H*100:.1f}% "
              f"| sáng {lum:.0f} | {jp.stat().st_size/1024/1024:.2f} MB")

    # contact sheet: 3 cot x 3 hang, moi o co ban 168px + 120px
    S = Image.new("RGB", (3 * 320 + 40, 3 * 200 + 40), (22, 22, 26))
    d = ImageDraw.Draw(S)
    for i, (n, vid, corner, ml, lum, mb, _) in enumerate(rows):
        im = Image.open(HERE / f"{n}_v6_brand.jpg")
        x, y = 20 + (i % 3) * 320, 20 + (i // 3) * 200
        S.paste(im.resize((280, 158), Image.LANCZOS), (x, y))
        S.paste(im.resize((120, 68), Image.LANCZOS), (x + 150, y + 90))
        d.text((x, y + 162), f"{n}  badge={corner}  main={ml:.0f}%  lum={lum:.0f}", fill=(225, 225, 225))
    S.save(HERE / "_sheet_v6.png")
    print(f"\ncontact sheet → {HERE / '_sheet_v6.png'}  ({len(rows)} bản)")


if __name__ == "__main__":
    main()
