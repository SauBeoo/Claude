# -*- coding: utf-8 -*-
r"""strip_wm_star.py — xoa dau ✦ tren THUMBNAIL da bake chu, bang PHEP MO + PHEP DONG.

    python tools\strip_wm_star.py <file-or-folder> -o <outdir> [--size 1920x1080]

VI SAO CO THEM TOOL NAY (do tren lo 1376x768 cua video 29, 2026-09-06)
  Rule `media-library.md` §2.10⑤b ghi "thumbnail thi VA, cach duy nhat chay duoc la dung
  lai nen theo TRUNG VI TUNG HANG" (tool `youtube-jp-shokutaku/tools/strip_wm_thumb.py`).
  Tren lo nay cach do HONG, va ly do la mot phat hien moi:

  1. ✦ cua lo nay ve bang **NET TOI mảnh (~2px)**, khong phai net sang. Do bang residual
     co dau (anh - GaussianBlur): net sao cho gia tri AM. Moi tool cu chi bat net SANG
     (tophat / "sang hon trung vi hang") nen go duoc mot nua, con nguyen hinh sao.
  2. ✦ nam DE LEN BIEN CHAT LIEU (canh da mai + go + tuong sang). Trung vi theo HANG keo
     mau tu ca hang -> ra **KHOI CHU NHAT xam**, do bang mat tren ca 3 anh T1/T2/T3.
  3. `cv2.inpaint` (Telea) voi mat na beo thi **chew canh da mai thanh cuc toi**.

CACH LAM O DAY — thay the CO TINH AN TOAN, khong "bo" noi dung nao
  pixel trong mat na duoc thay bang ban **CLOSING** (xoa net TOI mong hon kernel) hoac
  **OPENING** (xoa net SANG mong hon kernel). Cai gi DAY hon kernel — canh da mai, van go,
  mep vat — thi closing/opening tra ve dung gia tri cu, nen khong the pha vat that. Chi
  nhung net mong bang net sao moi bi thay. Cong nhieu +-0,7 de khong "phang nhu nhua".

⚠️ Vi tri ✦ van phai **DO BANG MAT** theo tung lo kich thuoc (dinh vi bang may that bai
   4/4 o anh co chu — rule §2.10⑤b). Cach do: crop goc duoi-phai, phong >=5x, xem residual
   co dau; ghi hop vao STAR_BOX.
⚠️ Exit code KHONG chung minh ✦ sach — soi mat 1:1 ca 4 goc tung anh.
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Hop chua ✦ — DO BANG MAT theo tung lo kich thuoc cua generator.
# (1376,768): tam sao ~(1277,670), be ngang ~57px, cao ~44px -> hop rong hon moi ben.
STAR_BOX = {
    (1376, 768): (1244, 632, 1320, 712),
}


def _ell(k):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))


def clean(im, bx, thr_d, thr_b, kclose, kopen, kdet, dil, feather, rng):
    """Tra ve so pixel mat na theo tung chieu + 2 ban do de xuat anh debug."""
    x0, y0, x1, y1 = bx
    box = im[y0:y1, x0:x1].astype(np.float32)
    g = cv2.cvtColor(box.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    black = cv2.morphologyEx(g, cv2.MORPH_BLACKHAT, _ell(kdet))   # net TOI mong
    top = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, _ell(kdet))       # net SANG mong
    out = box.copy()
    px = {}
    for name, raw, repl_k, op in (("toi", black > thr_d, kclose, cv2.MORPH_CLOSE),
                                  ("sang", top > thr_b, kopen, cv2.MORPH_OPEN)):
        m = raw.astype(np.uint8) * 255
        if dil > 1:
            m = cv2.dilate(m, _ell(dil))
        px[name] = int((m > 0).sum())
        if not px[name]:
            continue
        repl = cv2.morphologyEx(out, op, _ell(repl_k))
        a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), feather)[..., None]
        out = out * (1 - a) + repl * a
    out += rng.normal(0, 0.7, out.shape)
    im[y0:y1, x0:x1] = np.clip(out, 0, 255).astype(np.uint8)
    return px, black, top


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--box", default=None,
                    help="hop ✦ do bang mat: 'x0,y0,x1,y1' (pixel anh goc). Bo qua STAR_BOX.")
    ap.add_argument("--thr-dark", type=float, default=6.0,
                    help="nguong blackhat nhan NET TOI (mac dinh 6)")
    ap.add_argument("--thr-bright", type=float, default=8.0,
                    help="nguong tophat nhan NET SANG (mac dinh 8)")
    ap.add_argument("--kclose", type=int, default=3,
                    help="kernel CLOSING — phai NHO hon be day vat that gan do "
                         "(canh da mai ~5px thi de 3, dung tang)")
    ap.add_argument("--kopen", type=int, default=5)
    ap.add_argument("--kdet", type=int, default=7, help="kernel do tophat/blackhat")
    ap.add_argument("--dil", type=int, default=2)
    ap.add_argument("--feather", type=float, default=0.8)
    ap.add_argument("--size", default="", help="vd 1920x1080; de trong = giu kich thuoc goc")
    ap.add_argument("--only", default=None, help="chi xu ly file co chuoi nay trong ten")
    a = ap.parse_args()

    t = Path(a.target)
    files = sorted(p for p in t.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")) \
        if t.is_dir() else [t]
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    manual = tuple(int(v) for v in a.box.split(",")) if a.box else None

    for f in files:
        if a.only and a.only not in f.name:
            continue
        im = cv2.imdecode(np.fromfile(str(f), np.uint8), cv2.IMREAD_COLOR)
        H, W = im.shape[:2]
        bx = manual or STAR_BOX.get((W, H))
        if not bx:
            print(f"  {f.name}: BO QUA — chua co hop ✦ cho lo {W}x{H}, phai DO BANG MAT truoc")
            continue
        px, black, top = clean(im, bx, a.thr_dark, a.thr_bright, a.kclose, a.kopen,
                               a.kdet, a.dil, a.feather, rng)
        vis = np.hstack([np.clip(black * 5, 0, 255).astype(np.uint8),
                         np.clip(top * 5, 0, 255).astype(np.uint8)])
        cv2.imwrite(str(out / f"_dbg_{f.stem}.png"),
                    cv2.resize(vis, (vis.shape[1] * 6, vis.shape[0] * 6),
                               interpolation=cv2.INTER_NEAREST))
        if a.size:
            w, h = (int(v) for v in a.size.split("x"))
            im = cv2.resize(im, (w, h), interpolation=cv2.INTER_LANCZOS4)
        p = out / (f.stem + ".jpg")
        cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 95])[1].tofile(str(p))
        print(f"  {f.name} ({W}x{H}) -> {p.name}  px mat na {px}")
    print("\n⚠️ Exit code KHONG chung minh ✦ sach — soi mat 1:1 ca 4 goc tung anh.")


if __name__ == "__main__":
    main()
