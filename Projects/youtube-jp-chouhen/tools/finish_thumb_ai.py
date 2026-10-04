# -*- coding: utf-8 -*-
"""finish_thumb_ai.py — nghiệm thu thumbnail GEN BẰNG AI (chữ bake sẵn trong ảnh).

Dùng cho phương án B của kênh chouhen (user chỉ định 2026-08-05): user gen ảnh đã có chữ,
tool này làm 4 việc bắt buộc còn lại, không cái nào được bỏ:

  1. XOÁ WATERMARK model (✦ Gemini/Imagen) — theo đúng cách duy nhất đã chốt
     ([[feedback_thumbnail_health_chi_dua_prompt]]): seed = điểm sáng nhất trong ô CHỈ chứa
     watermark → BFS ngưỡng ~60 → **assert vùng <4000 px và bbox không lan về chủ thể** →
     giãn 3 px → fill median nền local.
     ⛔ Ba cách SAI đã thử ở video 22 health, đừng làm lại: patch nền từ phía trên (kéo chủ
     thể vào) · fill bbox chữ nhật + mask ngưỡng (cắt phẳng mép chủ thể thành bậc vuông) ·
     BFS cả dải (lan sang chủ thể: 8.387 px thay vì 783).
  2. Dập HUY HIỆU TRÒN nhận diện kênh (真夜中 — vòng kem + lòng navy + trăng khuyết) ở góc
     TRÊN-PHẢI, cùng hằng số với `make_thumb_textwall.py --mark-style circle` để bản gen AI
     và bản tool render trông là **một kênh**. Góc dưới đã bị timestamp YouTube chiếm
     ([[feedback_thumbnail_goc_duoi_phai_cua_youtube]]).
  3. Chuẩn hoá 16:9 → 1920×1080, xuất JPG dưới trần 2 MB của YouTube.
  4. Xuất preview **168px + 120px** để duyệt mắt (gate `audience-45plus.md` §1 mục 5).

    python tools/finish_thumb_ai.py <ảnh gen> -o 06_VIDEO/<slug>/thumb_T1_ai.jpg
    python tools/finish_thumb_ai.py <ảnh> -o out.jpg --no-mark      # bỏ huy hiệu
    python tools/finish_thumb_ai.py <ảnh> -o out.jpg --wm-box 0.90,0.90,1.0,1.0
"""
import argparse
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H = 1920, 1080
MARK_D, MARK_PAD = 124, 14                      # y hệt make_thumb_textwall.py
CREAM = (244, 230, 198, 255)
NAVY = (16, 20, 34, 236)
WM_BOX = (0.905, 0.900, 1.0, 1.0)               # ô mặc định chứa ✦ (góc dưới-phải)
BFS_THRESH = 60                                 # sáng hơn nền local ngần này = pixel dấu
MAX_COMP = 4000                                 # vượt = đang lan sang chủ thể → dừng


def remove_watermark(img, box, thresh=BFS_THRESH, max_comp=MAX_COMP):
    """Trả (img đã xoá, số px đã sửa, ghi chú). Không sửa được thì trả nguyên ảnh + lý do."""
    px = img.load()
    w, h = img.size
    x0, y0 = int(box[0] * w), int(box[1] * h)
    x1, y1 = min(w, int(box[2] * w)), min(h, int(box[3] * h))
    if x1 - x0 < 8 or y1 - y0 < 8:
        return img, 0, "ô watermark quá nhỏ"

    def lum(x, y):
        r, g, b = px[x, y][:3]
        return 0.299 * r + 0.587 * g + 0.114 * b

    # nền local = median độ sáng của ô (dấu chỉ chiếm phần nhỏ nên median ≈ nền)
    vals = sorted(lum(x, y) for y in range(y0, y1, 2) for x in range(x0, x1, 2))
    base = vals[len(vals) // 2]
    seed = max(((x, y) for y in range(y0, y1) for x in range(x0, x1)),
               key=lambda p: lum(*p))
    if lum(*seed) - base < thresh:
        return img, 0, f"không thấy dấu nào sáng hơn nền {thresh} (nền {base:.0f})"

    seen = {seed}
    comp = []
    q = deque([seed])
    while q:
        x, y = q.popleft()
        comp.append((x, y))
        if len(comp) > max_comp:
            return img, 0, (f"vùng lan >{max_comp} px → NGỜ là đang ăn vào chủ thể, "
                            f"KHÔNG sửa (hạ --wm-box cho khít dấu rồi chạy lại)")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            nx, ny = x + dx, y + dy
            if x0 <= nx < x1 and y0 <= ny < y1 and (nx, ny) not in seen \
                    and lum(nx, ny) - base >= thresh * 0.55:
                seen.add((nx, ny))
                q.append((nx, ny))

    bx0 = min(p[0] for p in comp); bx1 = max(p[0] for p in comp)
    by0 = min(p[1] for p in comp); by1 = max(p[1] for p in comp)
    if bx0 <= x0 + 1 or by0 <= y0 + 1:
        return img, 0, (f"bbox dấu ({bx0},{by0})-({bx1},{by1}) chạm mép ô → có thể là chủ "
                        f"thể, KHÔNG sửa")

    fill = set(comp)                              # giãn 3 px cho hết viền mờ
    for _ in range(3):
        for x, y in list(fill):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if x0 <= x + dx < x1 and y0 <= y + dy < y1:
                    fill.add((x + dx, y + dy))

    # màu vá = median màu của viền quanh vùng vá (nền thật, không phải nền từ nơi khác)
    ring = [px[x, y][:3] for x, y in
            {(x + dx, y + dy) for x, y in fill for dx, dy in ((4, 0), (-4, 0), (0, 4), (0, -4))}
            - fill if x0 <= x < x1 and y0 <= y < y1]
    if not ring:
        return img, 0, "không lấy được màu nền quanh dấu"
    med = tuple(sorted(c[i] for c in ring)[len(ring) // 2] for i in range(3))
    for x, y in fill:
        px[x, y] = med
    return img, len(fill), f"vá {len(fill)} px bằng màu nền {med}, bbox {bx1-bx0}×{by1-by0}"


def patch_box_gradient(img, box):
    """Vá TOÀN Ô bằng nội suy bilinear từ 4 mép ô — dùng khi ngưỡng độ sáng KHÔNG tách được
    dấu khỏi nền (nền là gradient sáng, ca T2 video 17: nền local 114, dấu chỉ hơn ~40).

    ⚠️ CHỈ dùng khi đã soi zoom và chắc trong ô **không có chủ thể nào** (nền trơn: mặt
    kính, tường, trời). Khác hẳn cách SAI "fill bbox 1 màu phẳng" đã bị kết án ở video 22:
    ở đây nội suy theo 4 mép nên gradient được giữ, không sinh ô vuông lệch tông.
    """
    px = img.load()
    w, h = img.size
    x0, y0 = int(box[0] * w), int(box[1] * h)
    x1, y1 = min(w, int(box[2] * w)), min(h, int(box[3] * h))
    top = [px[x, max(0, y0 - 2)][:3] for x in range(x0, x1)]
    bot = [px[x, min(h - 1, y1 + 1)][:3] for x in range(x0, x1)]
    lef = [px[max(0, x0 - 2), y][:3] for y in range(y0, y1)]
    rig = [px[min(w - 1, x1 + 1), y][:3] for y in range(y0, y1)]
    bw, bh = x1 - x0, y1 - y0
    for j in range(bh):
        fy = j / max(bh - 1, 1)
        for i in range(bw):
            fx = i / max(bw - 1, 1)
            c = []
            for k in range(3):
                v = ((1 - fy) * top[i][k] + fy * bot[i][k]
                     + (1 - fx) * lef[j][k] + fx * rig[j][k]) / 2
                c.append(int(max(0, min(255, v))))
            px[x0 + i, y0 + j] = tuple(c)
    return img, bw * bh, f"nội suy gradient toàn ô {bw}×{bh} px (nền trơn, không có chủ thể)"


def remove_watermark_hipass(img, box, thresh=14, ksize=61):
    """Xoá dấu bằng MEDIAN CAO TẦN — cách đúng khi dấu nằm trên GRADIENT hoặc trên BIÊN.

    Ca gốc T2 video 17: dấu ✦ nằm ngay trên đường biên khung cửa sổ sáng. Hai cách trước
    đều thất bại và cả hai đã được kiểm bằng mắt:
      * `remove_watermark` (BFS ngưỡng vs median cả ô): nền local 114, dấu chỉ hơn ~40 →
        ngưỡng nào tách được dấu thì cũng lan ra gradient, gate chặn đúng.
      * `patch_box_gradient` (nội suy 4 mép): ô nằm trên biên nên nội suy sinh **khối sáng
        vuông rõ rệt** — đúng lỗi "bậc vuông" mà video 22 health đã bị kết án.

    Cách này: median filter kernel LỚN HƠN dấu ⇒ ảnh median giữ nguyên gradient và biên
    nhưng **xoá sạch dấu**; chỗ nào sáng hơn ảnh median quá `thresh` thì lấy pixel median
    thay vào. Không có ô, không có bậc, gradient nguyên vẹn.
    """
    from PIL import ImageFilter
    w, h = img.size
    x0, y0 = int(box[0] * w), int(box[1] * h)
    x1, y1 = min(w, int(box[2] * w)), min(h, int(box[3] * h))
    tile = img.crop((x0, y0, x1, y1))
    if min(tile.size) < ksize:
        ksize = max(3, (min(tile.size) // 2) * 2 - 1)
    med = tile.filter(ImageFilter.MedianFilter(ksize if ksize % 2 else ksize + 1))
    tp, mp = tile.load(), med.load()
    n = 0
    for j in range(tile.height):
        for i in range(tile.width):
            a, b = tp[i, j], mp[i, j]
            la = 0.299 * a[0] + 0.587 * a[1] + 0.114 * a[2]
            lb = 0.299 * b[0] + 0.587 * b[1] + 0.114 * b[2]
            if la - lb >= thresh:
                tp[i, j] = b
                n += 1
    img.paste(tile, (x0, y0))
    pct = 100 * n / (tile.width * tile.height)
    return img, n, (f"median cao tần k={ksize}: vá {n} px ({pct:.1f}% của ô "
                    f"{tile.width}x{tile.height}) — gradient/biên giữ nguyên")


def stamp_circle(img):
    """Huy hiệu tròn 真夜中 góc trên-phải — cùng hằng số với make_thumb_textwall."""
    d = ImageDraw.Draw(img, "RGBA")
    D, PAD = MARK_D, MARK_PAD
    x1, y1 = img.width - PAD - D, PAD
    lay = Image.new("RGBA", (D + 8, D + 8), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    dl.ellipse([4, 4, D + 3, D + 3], fill=NAVY)
    dl.ellipse([4, 4, D + 3, D + 3], outline=CREAM, width=5)
    r = int(D * 0.30)
    mc = (D + 8) // 2
    dl.ellipse([mc - r, mc - r, mc + r, mc + r], fill=CREAM)
    # 🔴 VÁ 2026-08-08: hệ số 0.9 → 0.42. File này bị BỎ QUÊN khi vá khuôn huy hiệu ngày
    # 2026-08-06 (make_thumb_textwall.py và stamp_mark.py đã sửa, file này thì chưa), nên
    # mọi thumbnail nghiệm thu bằng nó có đĩa navy TRÀN 9px ra ngoài vành kem thành cái mỏm.
    # Đây là lỗi ĐỘC LẬP với tool web đã gỡ — giữ nguyên bản vá, đừng đảo lại.
    dl.ellipse([mc - r + int(r * 0.72), mc - r - 2, mc + r + int(r * 0.42), mc + r + 2],
               fill=NAVY)
    img.paste(lay, (x1 - 4, y1 - 4), lay)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--no-mark", action="store_true")
    ap.add_argument("--wm-box", help="x0,y0,x1,y1 dạng tỉ lệ 0–1 (mặc định góc dưới-phải)")
    ap.add_argument("--thresh", type=int, default=BFS_THRESH,
                    help="ngưỡng sáng hơn nền để coi là pixel dấu; NÂNG khi nền là "
                         "gradient (cửa sổ sáng) làm BFS lan ra nền")
    ap.add_argument("--patch-box", action="store_true",
                    help="vá cả ô bằng nội suy gradient 4 mép — chỉ khi ô CHỈ có nền trơn")
    ap.add_argument("--hipass", action="store_true",
                    help="xoá dấu bằng median cao tần — dùng khi dấu nằm trên gradient/biên")
    ap.add_argument("--hp-thresh", type=int, default=14)
    ap.add_argument("--quality", type=int, default=92)
    a = ap.parse_args()

    img = Image.open(a.src).convert("RGB")
    print(f"vào : {Path(a.src).name}  {img.width}×{img.height}")

    box = tuple(float(v) for v in a.wm_box.split(",")) if a.wm_box else WM_BOX
    if a.hipass:
        img, n, note = remove_watermark_hipass(img, box, thresh=a.hp_thresh)
    elif a.patch_box:
        img, n, note = patch_box_gradient(img, box)
    else:
        img, n, note = remove_watermark(img, box, thresh=a.thresh)
    print(f"watermark: {note}")

    if (img.width, img.height) != (W, H):        # crop giữa về 16:9 rồi resize
        tr = W / H
        r = img.width / img.height
        if r > tr:
            nw = int(img.height * tr)
            img = img.crop(((img.width - nw) // 2, 0, (img.width - nw) // 2 + nw, img.height))
        elif r < tr:
            nh = int(img.width / tr)
            img = img.crop((0, (img.height - nh) // 2, img.width, (img.height - nh) // 2 + nh))
        img = img.resize((W, H), Image.LANCZOS)
        print(f"chuẩn hoá → {W}×{H}")

    if not a.no_mark:
        img = stamp_circle(img)
        print(f"huy hiệu tròn 真夜中 @ góc trên-phải (Ø{MARK_D}, lề {MARK_PAD})")

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    q = a.quality
    while True:
        img.save(out, quality=q, subsampling=1, optimize=True)
        mb = out.stat().st_size / 1024 / 1024
        if mb <= 2.0 or q <= 70:
            break
        q -= 6
    print(f"ra  : {out}  {mb:.2f} MB (q{q})" + ("  ⚠️ VƯỢT trần 2 MB" if mb > 2 else ""))

    for p in (168, 120):
        img.resize((p, int(p * H / W)), Image.LANCZOS).save(
            out.with_name(out.stem + f"_prev{p}.png"))
    print(f"preview: {out.stem}_prev168.png / _prev120.png → DUYỆT MẮT trước khi giao")


if __name__ == "__main__":
    main()
