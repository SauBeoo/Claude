# -*- coding: utf-8 -*-
r"""strip_wm_t1_23.py — xoa dau (*) tren ban T1 GEN LAI cua video 23 (lo 2K 2752x1536).

LUAT: `media-library.md` §2.10 (5)b — anh AI con (*) la CHUA XONG.

VI SAO KHONG DUNG LAI `strip_wm_thumb23.py`:
  · Lo KHAC CO (2752x1536 vs 1376x768) => toa do (*) khac han. Do lai: **1 dau**, bbox
    **47x46px**, tam **(2639,1423) = (0,959W · 0,926H)** — khop hang so da ghi cho lo 2K
    la (0,958W · 0,926H). ⚠️ Nhung so DAU thi khac: so ghi 2 dau, lo nay chi **1**
    (§6d: so dau trong mot lo KHONG co dinh — phai quet, dung tin bang hang so).
  · Nen duoi (*) la **GIAY KE O**, khong phai nen phang. Ca ba cach cu deu hong o day:
      - trung vi HANG (§3): luoi doc bi keo thanh vet
      - inpaint NS (§6b): xoa luon duong luoi chay qua => thung mot o
      - phep dong/mo (§6c): net luoi day ngang net sao nen bi an theo

CHON NHANH — **VA, khong CAT** (§6d: chon theo CHU co chay sat mep khong):
  chu banner 「もうすぐ年金を受け取る方へ」 chay toi **x=2649 = 0,963W**, ma (*) bat dau o
  x=2616 = 0,951W ⇒ cat phai la **mat chu 「へ」**. Do la dieu kien §6d noi toi.

CACH VA: luoi la cau truc **TUAN HOAN** (do duoc chu ky **20px** ca hai chieu), nen chep
mot khoi sach lech **dung boi so chu ky** thi duong luoi tu khop. Tool thu nhieu offset,
cham diem tung cai bang (a) khong co blob sang (khong dinh sao/vien ao) (b) mau khop vanh
quanh (*), roi lay cai tot nhat va tron mem theo `distanceTransform`.

CHAY:  python tools/strip_wm_t1_23.py
"""
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\23_nenkin-seikyusho-todokanai")
SRC = os.path.join(VD, "_thumb_raw",
                   "Man_holding_postcard_with_envelope_2K_20260913163212.jpeg")
# ⛔ ten NGOAI pattern `thumb_T*` (§2.10 (7))
DST = os.path.join(VD, "_thumb_clean", "_wm_fixed_T1.png")

CX, CY, R = 2639, 1423, 32        # tam + ban kinh (bbox do duoc 47x46 => r>=24+8)
GRID = 20                          # chu ky luoi, do bang autocorrelation


def imread(p):
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)


def imwrite(p, a):
    ok, buf = cv2.imencode(".png", a)
    assert ok
    buf.tofile(p)


def main():
    a = imread(SRC)
    H, W = a.shape[:2]
    print(f"anh {W}x{H} · (*) tam ({CX},{CY}) r={R}")

    box = R + 6
    # 🔴 MAT NA PHAI BAM HINH SAO, KHONG DUOC LA HINH TRON.
    #    Mep ao xanh chay o x~2617, tuc NAM TRONG hinh tron r=32 quanh (2639,1423).
    #    inpaint lan truyen tu BIEN cua mat na => bien co pixel ao thi mau toi bi keo
    #    vao giua vet va (thay ro o vong thu 3: mot vet mo toi ben trai).
    #    Lay mat na tu chinh RESIDUAL (sang hon trung vi cuc bo) roi no 4px: no om dung
    #    canh sao, khong cham ao.
    _g0 = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32)
    _gm0 = cv2.cvtColor(cv2.medianBlur(a, 121), cv2.COLOR_BGR2GRAY).astype(np.float32)
    mask = np.zeros((H, W), np.uint8)
    _roi = (_g0 - _gm0)[CY - R:CY + R, CX - R:CX + R] > 6
    mask[CY - R:CY + R, CX - R:CX + R] = (_roi * 255).astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((9, 9), np.uint8))
    print(f"mat na bam sao: {int((mask > 0).sum())} px "
          f"(hinh tron r={R} se la {int(np.pi * R * R)} px)")

    # vanh quanh (*) — dung lam chuan mau
    ring = np.zeros((H, W), np.uint8)
    cv2.circle(ring, (CX, CY), R + 14, 255, -1)
    cv2.circle(ring, (CX, CY), R + 2, 0, -1)
    ref = a[ring > 0].astype(np.float32).mean(axis=0)

    g = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gm = cv2.cvtColor(cv2.medianBlur(a, 121), cv2.COLOR_BGR2GRAY).astype(np.float32)
    resid = g - gm

    # ── CACH VA: inpaint giu gradient, roi DUNG LAI duong luoi bi xoa ──────
    # 🔴 Da thu va BO cach "chep khoi lech boi so chu ky luoi": nen KHONG dong nhat
    #    (co vignette + ao xanh ngay ben canh), nen khoi nguon cach 240px mang tong
    #    NAU CAM sang => vet va lo hon ca cai sao. Bai hoc: luoi tuan hoan khong co
    #    nghia la NEN tuan hoan.
    # Do truoc: trong mask (x 2607-2671, y 1391-1455) **khong co duong ngang nao**,
    # chi co MOT duong doc o x=2651-2652 (dai toi 2579-2617 la MEP AO, khong phai luoi).
    # ⛔ DA THU VA BO `cv2.inpaint`: mep AO xanh dam chay ngay ben trai (*), va NS lan
    #    truyen tu BIEN mat na nen keo mau toi cua ao vao giua vet va — ra mot vet mo
    #    hinh sao, van nhin thay. Thu ca mat na tron (r=32) lan mat na BAM HINH SAO:
    #    deu dinh, vi cai sai nam o HUONG lan truyen, khong o co mat na.
    #
    # ✅ NOI SUY THEO COT — dung cho hinh hoc nay, va sach tuyet doi:
    #    · ao nam ke NGANG voi (*) => noi suy DOC khong bao gio cham toi no;
    #    · duong luoi cat qua mat na la duong DOC (x=2651) => noi suy doc **giu nguyen**
    #      no, khong can ve lai gi ca (buoc ve lai chinh la cai da lam hong vong truoc).
    #    · nen giay co gradient doc muot => noi suy tuyen tinh khop gan nhu tuyet doi.
    out = a.copy().astype(np.float32)
    ys, xs_ = np.nonzero(mask)
    for x in np.unique(xs_):
        col = np.nonzero(mask[:, x])[0]
        y0c, y1c = int(col.min()), int(col.max())
        top, bot = y0c - 1, y1c + 1
        if top < 0 or bot >= H:
            continue
        pa, pb = out[top, x], out[bot, x]
        n_ = bot - top
        t = np.linspace(0, 1, n_ + 1)[1:-1, None]
        out[top + 1:bot, x] = pa[None, :] * (1 - t) + pb[None, :] * t
    out = np.clip(out, 0, 255).astype(np.uint8)

    # hat nhieu nhe cho khoi phang nhu nhua
    n = np.random.normal(0, 0.8, out.shape).astype(np.float32)
    out = np.clip(out.astype(np.float32) + n, 0, 255).astype(np.uint8)

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    imwrite(DST, out)

    # ── nghiem thu bang may: residual trong vung (*) phai ve muc nen ────────
    g2 = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gm2 = cv2.cvtColor(cv2.medianBlur(out, 121), cv2.COLOR_BGR2GRAY).astype(np.float32)
    r2 = (g2 - gm2)[CY - R:CY + R, CX - R:CX + R]
    r1 = resid[CY - R:CY + R, CX - R:CX + R]
    print(f"residual trong vung (*): truoc {r1.max():.1f} -> sau {r2.max():.1f}")
    print(f"-> {DST}")
    print("⛔ VAN PHAI SOI 1:1 — so do khong chung minh sach (§2.10 (5) canh bao cuoi).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
