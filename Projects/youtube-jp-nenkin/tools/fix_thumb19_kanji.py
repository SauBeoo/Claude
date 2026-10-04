# -*- coding: utf-8 -*-
r"""fix_thumb19_kanji.py — xoa KANJI RAC trong thumbnail T2 cua video 19.

🔴 VAN DE: anh gen (task_002) co hai cho chu Nhat **VO NGHIA** do model tu ve:
   · bien hieu phia sau : 「試業試務出口」  (試業試務 khong phai tu; dung phai la
                          職業相談窓口 / 出口)
   · to giay goc duoi   : 「耽証券」        (耽 = "me dam" — vo nghia o day)
   Prompt da ghi "no extra text anywhere" nhung model **van ve chu vao bien hieu
   va giay to** — dung bay `ab-3title-3thumb.md` §3.1 cau 2 canh bao (phai ghi
   `no characters written anywhere` NGAY O KHOI DAO CU).

⚖️ Vi sao van phai xu du o gate 168px KHONG doc ra: YouTube hien thumbnail toi
   **400-600px** o trang video va mobile full-width, va nguoi Nhat nhin ra kanji
   sai ngay. Luat kenh: *"soi TUNG ky tu truoc khi giao, sai mot net la loai"*.

CACH VA — khac nhau cho hai cho:
  ① to giay (chu NET, nen trang phang)  -> dung lai nen theo **trung vi tung
     HANG** trong chinh to giay + nhieu nhe. Nen phang nen trung vi hang khop
     gan tuyet doi (`media-library.md` §2.10 ⑤b muc 3).
  ② bien hieu (chu da MO san, nen co van) -> **blur manh them**. Vung nay von
     ngoai net lay nen blur khong lo; dung lai nen thi ra vet chu nhat.

CHAY:  python tools/fix_thumb19_kanji.py
"""
import io
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = os.path.join("F:" + os.sep, "Youtube", "Dự_án_mới_3_xm444qin")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")

# toa do CHOT BANG MAT tren anh 1376x768 (soi crop 1:1, khong tin may —
# `media-library.md` §2.10 ⑤ muc 5: dinh vi bang may that bai 4/4 o anh co chu)
PAPER = (541, 674, 634, 716)      # 「耽証券」 tren to giay
SIGN = (1010, 20, 1320, 70)       # 「試業試務出口」 tren bien hieu


def fix_paper(a, box):
    """Dung lai nen theo trung vi tung HANG (nen to giay phang)."""
    x0, y0, x1, y1 = box
    pad = 14
    for y in range(y0, y1):
        # lay mau tu hai ben canh dong chu, cung hang
        left = a[y, max(0, x0 - pad):x0].astype(float)
        right = a[y, x1:x1 + pad].astype(float)
        ref = np.concatenate([left, right], axis=0)
        if len(ref) == 0:
            continue
        med = np.median(ref, axis=0)
        noise = np.random.uniform(-1.2, 1.2, size=(x1 - x0, 3))
        new = np.clip(med + noise, 0, 255)
        # blend MEM theo chieu ngang + doc de khong de lai vet chu nhat
        wx = np.ones(x1 - x0)
        f = 10
        wx[:f] = np.linspace(0, 1, f)
        wx[-f:] = np.linspace(1, 0, f)
        dy = min(y - y0, y1 - 1 - y)
        wy = min(1.0, (dy + 1) / 8.0)
        w = (wx * wy)[:, None]
        a[y, x0:x1] = (a[y, x0:x1] * (1 - w) + new * w).astype(np.uint8)
    return a


def _feather_mask(w, h, fade=12):
    """Mat na mo bien — chan 'vet hinh chu nhat' ma §2.10 ⑤ ket an."""
    m = Image.new("L", (w, h), 255)
    a = np.array(m).astype(float)
    for i in range(fade):
        v = 255.0 * (i + 1) / (fade + 1)
        a[i, :] = np.minimum(a[i, :], v)
        a[h - 1 - i, :] = np.minimum(a[h - 1 - i, :], v)
        a[:, i] = np.minimum(a[:, i], v)
        a[:, w - 1 - i] = np.minimum(a[:, w - 1 - i], v)
    return Image.fromarray(a.astype(np.uint8))


def fix_sign(im, box):
    """Blur manh vung bien hieu, dan qua MAT NA MO BIEN de khong lo ranh."""
    x0, y0, x1, y1 = box
    pad = 18                              # blur ca vien roi moi blend nguoc lai
    bx = (max(0, x0 - pad), max(0, y0 - pad), x1 + pad, y1 + pad)
    reg = im.crop(bx).filter(ImageFilter.GaussianBlur(8))
    w, h = reg.size
    im.paste(reg, (bx[0], bx[1]), _feather_mask(w, h, fade=pad))
    return im


def main():
    src = os.path.join(SRC, "task_002_1_image.jpg")
    if not os.path.exists(src):
        print(f"🔴 khong thay {src}")
        sys.exit(1)
    im = Image.open(src).convert("RGB")
    assert im.size == (1376, 768), f"cho doi 1376x768, nhan {im.size}"

    im = fix_sign(im, SIGN)
    a = np.array(im)
    a = fix_paper(a, PAPER)
    out_im = Image.fromarray(a)

    # xuat ra FILE RIENG, khong ghi de nguon (media-library §2.10 ⑤b muc 7)
    os.makedirs(VD, exist_ok=True)
    out = os.path.join(VD, "_thumb_fixed_T2.png")
    out_im.save(out)
    # ban soi 1:1 hai vung da va
    for nm, b in (("paper", PAPER), ("sign", SIGN)):
        x0, y0, x1, y1 = b
        m = 26
        c = out_im.crop((max(0, x0 - m), max(0, y0 - m), x1 + m, y1 + m))
        c = c.resize((c.size[0] * 4, c.size[1] * 4), Image.LANCZOS)
        c.save(os.path.join(VD, f"_check_T2_{nm}.png"))
    print(f"OK -> {out}")
    print(f"   soi 1:1: _check_T2_paper.png · _check_T2_sign.png")


if __name__ == "__main__":
    main()
