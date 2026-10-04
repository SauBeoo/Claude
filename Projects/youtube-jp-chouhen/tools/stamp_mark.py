# -*- coding: utf-8 -*-
"""
stamp_mark.py — dán DẤU NHẬN DIỆN KÊNH lên một ảnh thumbnail ĐÃ CÓ SẴN CHỮ.

Vì sao cần: `make_thumb_textwall.py` vẽ huy hiệu ở cuối pipeline vẽ chữ, nên nó chỉ
dùng được khi CHỮ DO TOOL VẼ. Với **phương án B** (chữ nằm trong ảnh AI — xem
`THUMBNAIL_PROMPT.md`) thì ảnh không đi qua tool đó, và huy hiệu bị thiếu.
Sự cố thật: video 18 bản T3 giao thiếu huy hiệu, user bắt được (2026-08-06).

⚠️ Code vẽ ở đây là BẢN COPY NGUYÊN VĂN nhánh `circle` của make_thumb_textwall.py
(hằng D=124, PAD=14, CREAM, r=0.30·D, offset trăng khuyết). Sửa khuôn thì phải sửa
CẢ HAI CHỖ, nếu không hai nhánh sẽ lệch nhau và dấu nhận diện mất giá trị —
nó chỉ có giá trị khi KHÔNG BAO GIỜ đổi.

📌 Có BA bản sao (file này · make_thumb_textwall.py nhánh circle · finish_thumb_ai.py), và
đúng cái đã lo ở trên ĐÃ xảy ra một lần: bản vá 2026-08-06 (hệ số trăng khuyết 0.9 → 0.42,
chữa đĩa navy tràn 9px ra ngoài vành kem thành cái mỏm) áp cho 2 chỗ nhưng bỏ quên
`finish_thumb_ai.py`, phát hiện 2026-08-08. Sửa khuôn thì sửa ĐỦ BA chỗ.

Dùng:
    python tools/stamp_mark.py <in.jpg> <out.png> [--style circle]
    python tools/stamp_mark.py <in.jpg> <out.png> --check   # chỉ in vùng sẽ bị đè
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

D_MARK, PAD = 124, 14
CREAM = (244, 230, 198, 255)
NAVY = (16, 20, 34, 236)


def stamp_circle(img: Image.Image) -> Image.Image:
    """Huy hiệu TRÒN góc TRÊN-PHẢI: vòng ngoài kem + lòng navy + vầng trăng khuyết
    (真夜中 = nửa đêm). Copy nguyên văn từ make_thumb_textwall.py nhánh 'circle'."""
    img = img.convert("RGB")
    W, H = img.size
    D = D_MARK
    x1, y1 = W - PAD - D, PAD
    lay = Image.new("RGBA", (D + 8, D + 8), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    dl.ellipse([4, 4, D + 3, D + 3], fill=NAVY)                  # lòng navy
    dl.ellipse([4, 4, D + 3, D + 3], outline=CREAM, width=5)     # vòng đóng khung
    r = int(D * 0.30)                                            # trăng khuyết
    mc = (D + 8) // 2
    dl.ellipse([mc - r, mc - r, mc + r, mc + r], fill=CREAM)
    # ⚠️ SỬA 2026-08-06 cùng lượt với make_thumb_textwall.py: 0.9 → 0.42.
    # Hệ số cũ đẩy mép phải đĩa khoét tới x=136 > vành x=127 → tràn 9px, thành cái mỏm.
    dl.ellipse([mc - r + int(r * 0.72), mc - r - 2, mc + r + int(r * 0.42), mc + r + 2],
               fill=NAVY)
    img.paste(lay, (x1 - 4, y1 - 4), lay)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--style", choices=["circle"], default="circle",
                    help="hiện chỉ có circle — kiểu ĐANG KHOÁ của kênh")
    ap.add_argument("--check", action="store_true",
                    help="chỉ in vùng huy hiệu sẽ chiếm, không ghi file")
    a = ap.parse_args()

    im = Image.open(a.src)
    W, H = im.size
    box = (W - PAD - D_MARK, PAD, W - PAD, PAD + D_MARK)
    print(f"ảnh {W}x{H} | huy hiệu Ø{D_MARK} lề {PAD} → chiếm {box}")
    if a.check:
        return
    if not a.out:
        sys.exit("cần <out>")
    out = stamp_circle(im)
    p = Path(a.out)
    out.save(p)
    if p.suffix.lower() == ".png":
        j = p.with_suffix(".jpg")
        out.save(j, quality=95)
        mb = j.stat().st_size / 1048576
        print(f"OK {p}  +  {j} ({mb:.2f} MB q95)")
        if p.stat().st_size / 1048576 >= 2:
            print(f"   ⚠️ PNG {p.stat().st_size/1048576:.2f} MB ≥ trần 2 MB của YouTube "
                  f"→ upload bản .jpg")
    else:
        print(f"OK {p}")


if __name__ == "__main__":
    main()
