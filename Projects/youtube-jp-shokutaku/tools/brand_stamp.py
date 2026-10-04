# -*- coding: utf-8 -*-
r"""brand_stamp.py — đóng DẤU NHẬN DIỆN KÊNH lên thumbnail đã render.

    python tools\brand_stamp.py <in.png> <out.png> --style bar|frame|seal

Vì sao có tool này (user chốt 2026-08-03): *"tôi muốn thumbnail sao để những lần sau
họ biết đó là kênh của mình"*. Nhận diện KHÔNG được lấy từ vị trí cột chữ — luật
`02_THUMBNAIL_TITLE_RULES.md` A6 buộc xoay layout trái↔phải giữa các video để chống
lặp. Nên nhận diện phải là một dấu CỐ ĐỊNH, luôn ở cùng chỗ, cùng màu, mọi video.

Nguyên tắc thiết kế: dấu phải nhận ra ở **168px** nhưng **không ăn diện tích chữ chính**
(gate `audience-45plus.md` §1: dòng chính ≥1/3 khung) → nên đặt ở dải mép, không đặt
giữa khung, và cao ≤9% chiều cao.

Chạy SAU make_thumb.py. Tool tự xuất preview 480/168/120 để duyệt gate.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/YuGothB.ttc"
NAME = "60代からの食卓"
YELLOW = (255, 222, 0)
RED = (255, 62, 48)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (43, 31, 20)


def f(sz):
    return ImageFont.truetype(FONT, sz)


def style_bar(im, name):
    """Dải chân trang đục + vạch vàng + tên kênh (ít xâm phạm nhất)."""
    W, H = im.size
    bh = int(H * 0.085)
    bar = Image.new("RGBA", (W, bh), DARK + (215,))
    im.paste(bar, (0, H - bh), bar)
    d = ImageDraw.Draw(im)
    d.rectangle((0, H - bh - 7, W, H - bh), fill=YELLOW)
    fs = int(bh * 0.62)
    fo = f(fs)
    bb = d.textbbox((0, 0), name, font=fo)
    d.text((W - (bb[2] - bb[0]) - int(W * 0.022), H - bh + (bh - (bb[3] - bb[1])) // 2 - bb[1]),
           name, font=fo, fill=WHITE)
    return im


def style_frame(im, name):
    """Viền vàng quanh khung + tag đỏ góc trên-trái."""
    W, H = im.size
    d = ImageDraw.Draw(im)
    t = 14
    d.rectangle((0, 0, W - 1, H - 1), outline=YELLOW, width=t)
    fs = int(H * 0.055)
    fo = f(fs)
    bb = d.textbbox((0, 0), name, font=fo)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = int(fs * 0.42)
    x0, y0 = t + 6, t + 6
    d.rectangle((x0, y0, x0 + tw + pad * 2, y0 + th + pad * 2), fill=RED)
    d.text((x0 + pad, y0 + pad - bb[1]), name, font=fo, fill=WHITE)
    return im


def style_seal(im, name, corner="bl"):
    """Dải dọc vàng bên trái + con dấu tròn đỏ 「食卓」.

    ⚠️ NHÀ MẶC ĐỊNH của con dấu là góc DƯỚI-TRÁI (`bl`) — giữ nguyên để nhận diện
    cố định mọi video (luật `02_THUMBNAIL_TITLE_RULES.md` A5.5).
    `--corner tr` là NGOẠI LỆ chỉ dùng khi cột chữ chiếm hết mép dưới-trái (ca thật:
    video 11, chữ gen sẵn trong ảnh nằm bên trái, dấu đè mất 2 ký của 「捨てないで」).
    ⛔ KHÔNG dùng `br` — góc dưới-phải là chỗ YouTube in timestamp thời lượng.
    """
    W, H = im.size
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 26, H), fill=YELLOW)
    r = int(H * 0.135)
    if corner == "tr":
        cx, cy = W - r - int(W * 0.012), r + int(H * 0.045)
    elif corner == "tl":
        cx, cy = 26 + r + int(W * 0.012), r + int(H * 0.045)
    else:
        cx, cy = 26 + r + int(W * 0.012), H - r - int(H * 0.045)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED, outline=WHITE, width=6)
    fo = f(int(r * 0.92))
    bb = d.textbbox((0, 0), "食卓", font=fo)
    d.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]), "食卓",
           font=fo, fill=WHITE)
    return im


STYLES = {"bar": style_bar, "frame": style_frame, "seal": style_seal}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--style", choices=STYLES, default="bar")
    ap.add_argument("--name", default=NAME)
    ap.add_argument("--corner", choices=("bl", "tl", "tr"), default="bl",
                    help="chỉ style seal: nhà mặc định bl (dưới-trái). tr/tl = ngoại lệ "
                         "khi cột chữ chiếm mép dưới-trái. KHÔNG có br (timestamp YouTube)")
    a = ap.parse_args()

    im = Image.open(a.src).convert("RGB")
    im = (style_seal(im, a.name, a.corner) if a.style == "seal"
          else STYLES[a.style](im, a.name))
    out = Path(a.out)
    im.save(out)
    for px in (480, 168, 120):
        p = im.copy()
        p.thumbnail((px, px * 10))
        p.save(out.with_name(out.stem + f"_preview{px}.png"))
    print(f"OK ({a.style}) {out} + preview480/168/120")


if __name__ == "__main__":
    main()
