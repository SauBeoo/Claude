# -*- coding: utf-8 -*-
"""Thiết kế NỀN thumbnail kiểu v23 (full-bleed moody, một ảnh liền) — bước TRƯỚC make_thumb.py.

Gom các kỹ thuật đã chốt 2026-07-11 (video 01_jinzo-tabemono, `thumbnail_v6_moody.png`):
- mirror/crop đưa chủ thể về một phía;
- gradient tối một phía (low-key relight) thay cho panel đen — KHÔNG lộ mép ghép;
- cắt vật thể từ ảnh khác (HSV mask + BFS từ mép) rồi ghép CHÌM VÀO CẢNH:
  grade tối/ấm + unsharp + bóng đổ ellipse — như vật thật được chụp cùng cảnh,
  KHÔNG sticker hoạt hình đè lên ảnh photo (user cấm, xem 02_THUMBNAIL_TITLE_RULES.md A5).

Ví dụ tái tạo nền video jinzo:
  python tools/compose_thumb_bg.py "<giỏ chuối.jpg>" bg.jpg --mirror --crop 0,40,1880,1097 \
    --grad l --cutout-src "<kidney_model_cc0.jpg>" --cutout-box 20,25,495,585 \
    --obj-w 620 --obj-x 1275 --obj-bottom 10
Sau đó:  python tools/make_thumb.py bg.jpg out.png --stack l --fill ...
"""
import argparse
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
W, H = 1920, 1080


def cutout_object(src_img: Image.Image, box) -> Image.Image:
    """Cắt vật thể khỏi nền sáng ít bão hòa (board/tường studio) bằng HSV mask + BFS từ mép."""
    crop = src_img.crop(box).convert("RGB")
    hsv = np.array(crop.convert("HSV")).astype(int)
    s, v = hsv[:, :, 1], hsv[:, :, 2]
    bgmask = (s < 70) & (v > 120)
    h, w = bgmask.shape
    connected = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bgmask[y, x] and not connected[y, x]:
                connected[y, x] = True
                dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bgmask[y, x] and not connected[y, x]:
                connected[y, x] = True
                dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and bgmask[ny, nx] and not connected[ny, nx]:
                connected[ny, nx] = True
                dq.append((ny, nx))
    alpha = Image.fromarray((~connected * 255).astype("uint8"))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
    out = crop.convert("RGBA")
    out.putalpha(alpha)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photo", help="ảnh nền gốc (moody, chủ thể một phía sau mirror/crop)")
    ap.add_argument("out", help="file nền 1920x1080 xuất ra (jpg)")
    ap.add_argument("--mirror", action="store_true", help="lật ngang (đưa chủ thể sang phía kia)")
    ap.add_argument("--crop", default="", help="x0,y0,x1,y1 (px ảnh gốc) crop TRƯỚC khi resize — chọn vùng 16:9")
    ap.add_argument("--grad", choices=["l", "r", ""], default="", help="phía đánh gradient tối (phía đặt chữ)")
    ap.add_argument("--grad-reach", type=int, default=1280, help="gradient tan hết ở x này (px khung 1920)")
    ap.add_argument("--grad-max", type=int, default=243, help="độ tối tại mép (0-255)")
    ap.add_argument("--grad-exp", type=float, default=1.15, help="số mũ falloff")
    # vật thể ghép (tạng/vật chứng...) — 2 cách nạp
    ap.add_argument("--cutout", default="", help="PNG RGBA cutout có sẵn")
    ap.add_argument("--cutout-src", default="", help="ảnh nguồn để cắt vật thể (nền sáng studio)")
    ap.add_argument("--cutout-box", default="", help="x0,y0,x1,y1 vùng chứa vật thể trong --cutout-src (né logo hãng)")
    ap.add_argument("--cutout-save", default="", help="lưu cutout ra file (mặc định: <out>_cutout.png khi cắt mới)")
    ap.add_argument("--obj-w", type=int, default=620, help="bề ngang vật thể sau resize")
    ap.add_argument("--obj-x", type=int, default=1275, help="toạ độ x đặt vật thể")
    ap.add_argument("--obj-y", type=int, default=-1, help="toạ độ y (mặc định: neo đáy theo --obj-bottom)")
    ap.add_argument("--obj-bottom", type=int, default=10, help="khoảng cách mép dưới khi neo đáy")
    ap.add_argument("--obj-bright", type=float, default=0.92, help="grade tối vật thể cho chìm vào cảnh")
    ap.add_argument("--obj-contrast", type=float, default=1.06)
    ap.add_argument("--obj-warm", type=int, default=28, help="alpha lớp phủ ấm (255,185,110); 0 = tắt")
    ap.add_argument("--obj-sharpen", action="store_true", default=True, help="UnsharpMask cho rõ vân (mặc định bật)")
    ap.add_argument("--no-obj-sharpen", dest="obj_sharpen", action="store_false")
    args = ap.parse_args()

    bg = Image.open(args.photo).convert("RGB")
    if args.mirror:
        bg = ImageOps.mirror(bg)
    if args.crop:
        x0, y0, x1, y1 = (int(v) for v in args.crop.split(","))
        if x1 > bg.width or y1 > bg.height:
            raise SystemExit(f"crop {x1}x{y1} vượt khung ảnh {bg.width}x{bg.height} — PIL sẽ độn đen, chỉnh lại")
        bg = bg.crop((x0, y0, x1, y1))
    bg = bg.resize((W, H), Image.LANCZOS)

    if args.grad:
        gd = np.zeros(W)
        for x in range(W):
            t = (args.grad_reach - x) / args.grad_reach if args.grad == "l" else (x - (W - args.grad_reach)) / args.grad_reach
            t = max(0.0, min(1.0, t))
            gd[x] = int(args.grad_max * (t ** args.grad_exp))
        grad = Image.fromarray(np.tile(gd.astype("uint8"), (H, 1)))
        bg = Image.composite(Image.new("RGB", bg.size, (5, 4, 6)), bg, grad)

    canvas = bg.convert("RGBA")

    kid = None
    if args.cutout:
        kid = Image.open(args.cutout).convert("RGBA")
    elif args.cutout_src:
        if not args.cutout_box:
            raise SystemExit("--cutout-src cần kèm --cutout-box")
        box = tuple(int(v) for v in args.cutout_box.split(","))
        kid = cutout_object(Image.open(args.cutout_src), box)
        save_to = args.cutout_save or str(Path(args.out).with_suffix("")) + "_cutout.png"
        kid.save(save_to)
        print("cutout →", save_to)

    if kid is not None:
        kw = args.obj_w
        obj = kid.resize((kw, int(kid.height * kw / kid.width)), Image.LANCZOS)
        if args.obj_sharpen:
            obj = obj.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=2))
        obj = ImageEnhance.Brightness(obj).enhance(args.obj_bright)
        obj = ImageEnhance.Contrast(obj).enhance(args.obj_contrast)
        if args.obj_warm > 0:
            warm = Image.new("RGBA", obj.size, (255, 185, 110, args.obj_warm))
            empty = Image.new("RGBA", obj.size, (0, 0, 0, 0))
            obj = Image.alpha_composite(obj, Image.composite(warm, empty, obj.split()[3]))
        ox = args.obj_x
        oy = args.obj_y if args.obj_y >= 0 else H - obj.height - args.obj_bottom
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse((ox + 15, oy + obj.height - 70, ox + kw - 5, oy + obj.height + 26), fill=(0, 0, 0, 160))
        canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(20)))
        canvas.alpha_composite(obj, (ox, oy))

    canvas.convert("RGB").save(args.out, quality=95)
    print("OK nền", args.out, "— tiếp: make_thumb.py để đè chữ")


if __name__ == "__main__":
    main()
