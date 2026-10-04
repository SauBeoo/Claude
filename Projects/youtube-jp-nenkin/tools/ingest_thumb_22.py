# -*- coding: utf-8 -*-
r"""ingest_thumb_22.py — nhan lo thumbnail AI cua video 22, xuat ban dung chuan.

LO: 2 anh 2752x1536 trong ~/Downloads (gen 2026-09-11 14:44 va 14:49).
  · 14:49 `Woman_holding_bank_passbook_asto…`  -> **T1** khuon BAKE 9 KHOI (09/10)
  · 14:44 `Woman_viewing_pension_bank_passbook` -> **T2** khuon TELOP live (21)
  => bien thu giua T1/T2 la **PHONG CACH**, chu giong het nhau tung ky tu.

VIEC TOOL LAM:
  1. **Kiem ✦**: da soi 1:1 CA 4 GOC + 2 vi tri hang so cua lo 2752x1536
     (`media-library.md` §2.10 ⑤b muc 5: 0,958W·0,926H va 0,930W·0,890H)
     => **LO NAY KHONG CO ✦**. Tool van in lai canh bao de lan sau soi lai,
     vi day la SO DO cua mot lo, khong phai mien tru.
  2. **Cat ve 16:9**: 2752/1536 = 1,7917 ≠ 1,7778 => thua **21px** be ngang.
     Cat DEU 2 ben (10/11px) roi resize 1920x1080.
  3. Xuat `.png` + `.jpg` q95 (tran 2 MB cua YouTube, `ab-3title-3thumb.md` §3 muc 4).
  4. Do **hero cao/rong** + **o timestamp goc duoi-phai** (4,0% x 3,2% = 46x20 tren
     1280x720 -> 77x35 tren 1920x1080) phai 0% muc.
  5. Xuat sheet duyet **168px** va **120px**.

CHAY:  python tools/ingest_thumb_22.py
"""
import io
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "22_mishikyu-nenkin-36man")
DL = os.path.join(os.path.expanduser("~"), "Downloads")

SRC = {
    "T1": ("Woman_holding_bank_passbook_asto", "khuon BAKE 9 KHOI (09/10)"),
    "T2": ("Woman_viewing_pension_bank_passbook", "khuon TELOP live (21)"),
}
OUT = "thumb_{tag}_mishikyu-36man"
W, H = 1920, 1080
# o timestamp YouTube: ~4,0% x 3,2% khung (media-library §2.10 ⑤b / audience-45plus)
TS_W, TS_H = int(W * 0.040), int(H * 0.032)


def find(prefix):
    for n in sorted(os.listdir(DL)):
        if n.startswith(prefix) and n.lower().endswith((".jpeg", ".jpg", ".png")):
            return os.path.join(DL, n)
    return None


def hero_box(im):
    """Bbox cua chu hero vang/cam, bo vung nguoi ben phai."""
    import cv2
    a = np.asarray(im.convert("RGB")).astype(int)
    h, w, _ = a.shape
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    m = ((R > 190) & (G > 120) & (G < 225) & (B < 110)).astype(np.uint8)
    m[:, int(w * 0.70):] = 0          # bo nguoi
    m[:int(h * 0.22)] = 0             # bo banner
    m[int(h * 0.88):] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n < 2:
        return None
    ar = st[1:, 4]
    keep = [i + 1 for i, v in enumerate(ar) if v > 0.08 * ar.max()]
    x0 = min(st[i, 0] for i in keep); y0 = min(st[i, 1] for i in keep)
    x1 = max(st[i, 0] + st[i, 2] for i in keep)
    y1 = max(st[i, 1] + st[i, 3] for i in keep)
    return x0, y0, x1, y1


def main():
    print("⚠️  ✦ WATERMARK: lo nay da soi 1:1 ca 4 GOC + 2 vi tri hang so cua lo")
    print("    2752x1536 => KHONG CO ✦. Lo sau van phai soi lai (media-library §2.10 ⑤b).")
    rows = []
    for tag, (prefix, ten) in SRC.items():
        src = find(prefix)
        if not src:
            print(f"🔴 {tag}: khong thay anh nguon `{prefix}*` trong ~/Downloads")
            continue
        im = Image.open(src).convert("RGB")
        w0, h0 = im.size
        # cat ve 16:9, chia deu 2 ben
        want = int(round(h0 * 16 / 9))
        if w0 > want:
            d = w0 - want
            im = im.crop((d // 2, 0, w0 - (d - d // 2), h0))
        elif w0 < want:
            wh = int(round(w0 * 9 / 16))
            d = h0 - wh
            im = im.crop((0, d // 2, w0, h0 - (d - d // 2)))
        im = im.resize((W, H), Image.LANCZOS)
        base = os.path.join(VD, OUT.format(tag=tag))
        im.save(base + ".png")
        im.save(base + ".jpg", quality=95, subsampling=0)
        png_mb = os.path.getsize(base + ".png") / 1e6
        jpg_mb = os.path.getsize(base + ".jpg") / 1e6

        hb = hero_box(im)
        hero = (f"{(hb[3]-hb[1])/H*100:.1f}% cao · {(hb[2]-hb[0])/W*100:.1f}% rong"
                if hb else "khong do duoc")
        ts = np.asarray(im.crop((W - TS_W, H - TS_H, W, H)).convert("L")).astype(int)
        ink = float((np.abs(ts - int(np.median(ts))) > 45).mean() * 100)

        for px in (168, 120):
            im.resize((px, int(px * 9 / 16)), Image.LANCZOS).save(f"{base}_prev{px}.png")

        print(f"\n{tag} — {ten}")
        print(f"   nguon : {os.path.basename(src)}  {w0}x{h0} -> cat {w0-want if w0>want else 0}px -> {W}x{H}")
        print(f"   xuat  : {os.path.basename(base)}.png ({png_mb:.2f} MB) + .jpg ({jpg_mb:.2f} MB)"
              + ("   ⚠️ PNG >2MB, dung ban .jpg" if png_mb > 2 else ""))
        print(f"   HERO  : {hero}" + ("   ✅ qua gate 2 (>=33,3%)" if hb and (hb[3]-hb[1])/H >= 1/3 else "   (duoi 33,3% — xem §6.10)"))
        print(f"   o timestamp goc duoi-phai: {ink:.1f}% muc" + ("  ✅" if ink < 1 else "  🔴 CO CHU/HINH DAM"))
        print(f"   sheet duyet: {os.path.basename(base)}_prev168.png · _prev120.png")
        rows.append((tag, hero, ink))
    print("\n=> Duyet MAT: mo ca 2 file _prev168 va _prev120, doc duoc dong chinh + "
          "nhan ra bieu cam moi giao.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
