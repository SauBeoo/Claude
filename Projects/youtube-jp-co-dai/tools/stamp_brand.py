# -*- coding: utf-8 -*-
r"""
stamp_brand.py — đóng DẤU NHẬN DIỆN KÊNH 古代の秘訣 lên thumbnail.

VÌ SAO PHẢI LÀ TOOL, KHÔNG PHẢI AI BAKE (user yêu cầu 2026-08-04
"thêm 1 chút để nhận biết đó là kênh mình"):
  Dấu nhận diện chỉ có tác dụng khi nó **giống hệt từng pixel qua MỌI video**.
  AI gen thì mỗi lần vẽ một kiểu → không bao giờ thành nhận diện. Nên dấu phải
  do PIL đè, và spec khoá cứng trong file này. ⛔ Đừng đổi spec giữa các video —
  đổi là mất sạch giá trị nhận diện đã tích được.

Bài học đã đúc vào spec:
  · Đặt **GÓC TRÊN–PHẢI**. Góc dưới–phải là của YouTube (nó đè timestamp thời lượng
    lên đó — memory `feedback_thumbnail_goc_duoi_phai_cua_youtube`); góc dưới–trái
    thường đã có badge giá/số của khuôn B1.
  · Neo bằng **1 glyph lớn 「秘」** chứ không chỉ bằng tên kênh: ở 168px thì chữ nhỏ
    thành cháo, còn một glyph to + khối màu vẫn đọc ra là "kênh đó".
  · Màu = đúng bộ Vox của kênh (vàng #FFD200 trên nền ink #16181D) → thumbnail và
    thẻ trong video cùng một họ.

CHẠY
    python tools\stamp_brand.py <ảnh vào> [-o <ảnh ra>] [--scale 1.0] [--pos tr|tl]
    python tools\stamp_brand.py <ảnh vào> --preview      # xuất thêm bản 168px/120px

Không có -o thì ghi ra `<tên>_brand.<ext>` cạnh file gốc (KHÔNG ghi đè bản gốc).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FONTS = Path(r"E:\Claude\Projects\_media_library\fonts")
F_BLACK = FONTS / "NotoSansJP-Black.otf"
F_BOLD = FONTS / "NotoSansJP-Bold.otf"

# ── SPEC ĐÃ KHOÁ — đừng đổi giữa các video ────────────────────────────────────
INK = (22, 24, 29)
YELLOW = (255, 210, 0)
WHITE = (248, 248, 245)
PLATE_H = 0.120        # chiều cao khối dấu = 12% chiều cao khung.
                       # ⭐ CHỐT 2026-08-04 sau khi so A/B 3 cỡ ở 168px (0,092 / 0,120 /
                       # 0,143): 0,092 quá mờ, 0,143 nặng và đáy khối gần chạm mũi tên đỏ.
                       # 0,120 = khối vàng đọc ra là một dấu riêng mà không tranh chỗ.
MARGIN = 0.022         # lề từ cạnh khung
SEAL = "秘"            # glyph neo — đọc được ở 168px
NAME = "古代の秘訣"
ALPHA = 234            # nền khối hơi trong để không "dán tem" quá thô


def stamp(src: Path, out: Path, scale: float = 1.0, pos: str = "tr", dy: float = 0.0) -> Path:
    """dy = dịch dấu xuống, theo TỈ LỆ chiều cao khung (0.13 ≈ xuống một dòng chữ).
    ⚠️ CHỈ dùng khi góc chuẩn bị chữ của ảnh chiếm — ca gốc: video 04 ゴキブリ,
    AI kéo dòng phụ 「ゴキブリが出ない家」 full khung nên cả tr lẫn tl đều đè mất 1 ký.
    Dấu lệch vị trí thì yếu giá trị nhận diện → đừng dùng nếu không bắt buộc."""
    im = Image.open(src).convert("RGB")
    W, H = im.size
    ph = int(H * PLATE_H * scale)
    pad = int(ph * 0.20)
    seal_f = ImageFont.truetype(str(F_BLACK), int(ph * 0.74))
    name_f = ImageFont.truetype(str(F_BOLD), int(ph * 0.40))

    sb = seal_f.getbbox(SEAL)
    nb = name_f.getbbox(NAME)
    seal_w, name_w = sb[2] - sb[0], nb[2] - nb[0]
    pw = pad + int(ph * 0.78) + int(pad * 0.9) + name_w + pad

    x = W - pw - int(W * MARGIN) if pos == "tr" else int(W * MARGIN)
    y = int(H * (MARGIN + dy))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = int(ph * 0.26)
    d.rounded_rectangle([x, y, x + pw, y + ph], r, fill=(*INK, ALPHA))
    # ô vuông vàng bọc glyph 「秘」 — khối màu này là thứ đọc được ở 168px
    bx, by, bs = x + pad, y + int(ph * 0.13), int(ph * 0.74)
    d.rounded_rectangle([bx, by, bx + bs, by + bs], int(bs * 0.20), fill=YELLOW)
    d.text((bx + bs / 2, by + bs / 2), SEAL, font=seal_f, fill=INK, anchor="mm")
    d.text((bx + bs + int(pad * 0.9), y + ph / 2), NAME, font=name_f, fill=WHITE, anchor="lm")

    im = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
    q = {"quality": 95} if out.suffix.lower() in (".jpg", ".jpeg") else {}
    im.save(out, **q)
    return out


def previews(p: Path):
    im = Image.open(p).convert("RGB")
    for w in (168, 120):
        h = round(w * im.height / im.width)
        o = p.with_name(f"{p.stem}_prev{w}.png")
        im.resize((w, h), Image.LANCZOS).resize((w * 5, h * 5), Image.NEAREST).save(o)
        print(f"  {w}px → {o.name}")


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("-")]
    if not a:
        print(__doc__); return
    src = Path(a[0])
    out = (Path(sys.argv[sys.argv.index("-o") + 1]) if "-o" in sys.argv
           else src.with_name(f"{src.stem}_brand{src.suffix}"))
    scale = float(sys.argv[sys.argv.index("--scale") + 1]) if "--scale" in sys.argv else 1.0
    pos = sys.argv[sys.argv.index("--pos") + 1] if "--pos" in sys.argv else "tr"
    dy = float(sys.argv[sys.argv.index("--dy") + 1]) if "--dy" in sys.argv else 0.0
    p = stamp(src, out, scale, pos, dy)
    print(f"[BRAND] {p}")
    if "--preview" in sys.argv:
        previews(p)


if __name__ == "__main__":
    main()
