# -*- coding: utf-8 -*-
r"""make_genten_21.py — cat 9 anh 原典 tu screenshot THAT + khoanh do.

⛔ **KHONG GEN AI.** Day la BANG CHUNG cua bai (`handmade-layer.md` §2 · gate X5
   cua `video-vox`): chu phai DOC DUOC, cam lam mo, cam ve lai.

NGUON — 4 trang, da chup 2026-09-04 bang `chrome-headless-shell` cua Remotion
(`node_modules/.remotion/chrome-headless-shell/.../chrome-headless-shell.exe`),
anh goc de o `06_VIDEO/<STEM>/_genten_raw/`:
  nta_full.png  1400x3000  国税庁「高齢者と税（年金と税）」
                https://www.nta.go.jp/publication/pamph/koho/kurashi/html/03_1.htm
  faq_full.png  1400x2600  年金機構 FAQ「提出しなかった場合はどうなるのですか」
  kami_full.png 1400x4200  年金機構「令和8年分…紙の提出方法」
  r9_full.png   1400x3200  年金機構「令和9年分…紙の提出方法」

🔴 TOA DO CHOT BANG MAT, khong bang may — cung ly le nhu `media-library.md`
   §2.10 ⑤ (dinh vi bang may that bai 4/4 lan o anh co chu). Cach lam: chia anh
   full thanh dai 900px, doc tung dai, ghi lai y tuyet doi cua dong can khoanh.

📐 KHUNG RA: **1920x1080**. Cat vung rong `CW=990` (dung be rong cot noi dung
   cua ca 4 trang) x cao 557 => dung 16:9 => scale 1,94x, chu 16px thanh ~31px,
   doc duoc o dien thoai cho tep 45+ (`audience-45plus.md` §3 doi co >=22).

CHAY:  python tools/make_genten_21.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image, ImageDraw  # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
RAW = os.path.join(VD, "_genten_raw")
OUT = os.path.join(VD, "genten")

W, H = 1920, 1080
CW, CH = 990, 557          # 990/557 = 1,7774 ~ 16:9
X0 = 200                   # le trai cot noi dung cua ca 4 trang
RED = (208, 32, 32)
LW = 4                     # be day vien khoanh (truoc khi scale ~1,9x)

# ── 9 the: (ten, anh nguon, tam doc vung cat, [hop khoanh do], ghi chu) ──────
# hop khoanh = (x0, y0, x1, y1) trong TOA DO ANH FULL
CARDS = [
 ("genten21_01", "nta_full.png", 2205,
  [(212, 2186, 902, 2210)],
  "国税庁 源泉徴収と確定申告 — dong 155万円/205万円"),
 ("genten21_02", "nta_full.png", 2282,
  [(212, 2272, 775, 2296)],
  "国税庁 ※令和9年分は…214万円"),
 ("genten21_03", "nta_full.png", 2240,
  [(210, 2126, 905, 2170), (212, 2186, 902, 2250)],
  "国税庁 ca khoi 源泉徴収と確定申告 (heading + doan)"),
 ("genten21_04", "faq_full.png", 730,
  [(210, 716, 1180, 742)],
  "年金機構 FAQ — 提出した場合と提出しなかった場合で、所得税率に差はありません"),
 ("genten21_05", "faq_full.png", 845,
  [(222, 790, 1120, 840), (222, 852, 900, 902)],
  "年金機構 FAQ — 2 cong thuc 提出した/しなかった (5.105%)"),
 ("genten21_06", "r9_full.png", 590,
  [(210, 566, 1180, 612)],
  "年金機構 令和9年分 — 期限に間に合わない場合でも、なるべく早くご提出を"),
 ("genten21_07", "kami_full.png", 1080,
  [(212, 1068, 1175, 1094)],
  "年金機構 令和8年分 — さかのぼって源泉徴収税額の再計算を行います"),
 ("genten21_08", "nta_full.png", 2440,
  [(210, 2518, 905, 2600)],
  "国税庁 確定申告不要制度 注1 — 還付を受けるためには確定申告書を提出"),
 ("genten21_09", "nta_full.png", 2420,
  [(210, 2330, 905, 2372), (222, 2418, 905, 2500)],
  "国税庁 年金所得者の確定申告不要制度 — heading + 2 dieu kien 400万/20万"),
 # ⭐ the thu 10, them 2026-09-04: khoi 原典④ dai 18,4s ma chi co 2 anh => 9,2s
 #    moi anh, VUOT san 9,0s cua `audience-45plus.md` §2.0b (gate nhip hinh bat).
 #    Chia 3 anh => 6,1s. Khong the keo dai anh, nen phai them anh.
 ("genten21_10", "nta_full.png", 2440,
  [(222, 2418, 905, 2440), (210, 2518, 905, 2600)],
  "国税庁 dieu kien 1 (400万) + 注1 — bat cap 'khong phai khai' vs 'muon hoan thi phai khai'"),
]


def snap(crop, r):
    """Snap hop khoanh vao RANH GIOI DONG CHU THAT, roi chua le = nua khe trang.

    🔴 VI SAO PHAI CO HAM NAY: ban dau tao padding co dinh 6px, va vong do **de
       len chu cua dong DUOI** o ca 2/2 the da soi (the 01 che dong 生命保険契約
       等…, the 04 che dong なかった場合でも…). Dong cach nhau ~30px ma chu cao
       ~24px => khe trang chi ~6px, tuc padding doan 6px la CHAC CHAN de.
       Cach dung: **do khe trang thuc** roi lay nua khe. Cung ho voi
       `audience-45plus.md` §2.0f — placement phai doc tu noi dung, khong tu
       mot hang so.
    """
    import numpy as np
    x0, y0, x1, y1 = (int(v) for v in r)
    a = np.asarray(crop.convert("L"))
    H_, W_ = a.shape
    x0c, x1c = max(0, x0), min(W_, x1)
    if x1c - x0c < 8:
        return (x0 - 6, y0 - 6, x1 + 6, y1 + 6)
    ink = (a[:, x0c:x1c] < 150).sum(axis=1) > 0      # hang co muc trong dai x

    def edge(y, step):
        """Tu y, di theo `step` toi khi ra khoi vet muc; tra ve bien + nua khe."""
        j = max(0, min(H_ - 1, y))
        # bam vao vet muc gan nhat (neu y dang o vung trang)
        for _ in range(14):
            if ink[j]:
                break
            j = max(0, min(H_ - 1, j + step))
        # di ra khoi vet muc
        while 0 < j < H_ - 1 and ink[j]:
            j += step
        # dem khe trang lien tiep
        gap, k = 0, j
        while 0 <= k < H_ and not ink[k] and gap < 20:
            gap += 1
            k += step
        return j + step * max(1, min(gap // 2, 6))

    ny0, ny1 = edge(y0, -1), edge(y1, +1)
    if ny1 - ny0 < 10:                               # do that bai -> quay ve pad
        ny0, ny1 = y0 - 4, y1 + 4
    return (x0 - 8, ny0, x1 + 8, ny1)


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.isdir(RAW):
        print(f"🔴 khong thay {RAW} — chua chup screenshot")
        return 1
    src_cache, made, bad = {}, [], []
    for name, srcfn, ycen, boxes, note in CARDS:
        sp = os.path.join(RAW, srcfn)
        if not os.path.exists(sp):
            bad.append(f"{name}: thieu {srcfn}")
            continue
        if srcfn not in src_cache:
            src_cache[srcfn] = Image.open(sp).convert("RGB")
        im = src_cache[srcfn]
        SW, SH = im.size
        # 🔴 VUNG CAT SUY TU CHINH HOP KHOANH, khong dung hang so.
        #    Ban dau tao dat `CW=990` theo cot noi dung cua trang 国税庁 — va
        #    gate bat ngay 3/9 the: cot cua trang 年金機構 rong toi x=1180 nen
        #    hop khoanh LOT ra ngoai vung cat. Do la loi cua HANG SO PHONG DOAN
        #    (dung ho `audience-45plus.md` §2.0f: gate/placement phai doc tu noi
        #    dung thay vi tu mot con so doan).
        bx0 = min(b[0] for b in boxes) - 26
        bx1 = max(b[2] for b in boxes) + 26
        cw = max(CW, bx1 - bx0)
        ch = int(round(cw / (W / H)))          # giu dung 16:9
        left = max(0, min(SW - cw, bx0)) if cw <= SW else 0
        cw = min(cw, SW)
        ch = int(round(cw / (W / H)))
        top = max(0, min(SH - ch, int(ycen - ch / 2)))
        CW_, CH_ = cw, ch
        crop = im.crop((left, top, left + cw, top + ch)).copy()
        d = ImageDraw.Draw(crop)
        n_in = 0
        for (bx0, by0, bx1, by1) in boxes:
            r = snap(crop, (bx0 - left, by0 - top, bx1 - left, by1 - top))
            # 🔴 hop khoanh phai NAM TRON trong vung cat, neu khong la khoanh
            #    truot ra ngoai khung ma anh van "trong nhu binh thuong"
            if r[0] < 0 or r[1] < 0 or r[2] > CW_ or r[3] > CH_:
                bad.append(f"{name}: hop khoanh {(bx0, by0, bx1, by1)} LOT ra "
                           f"ngoai vung cat (top={top})")
                continue
            d.rounded_rectangle(r, radius=10, outline=RED, width=LW)
            n_in += 1
        if n_in == 0:
            bad.append(f"{name}: KHONG co hop khoanh nao ve duoc")
        # 🔴 GATE FOOTER (them 2026-09-04): the 08 lot ca **footer trang web +
        #    dai den** vao 15% duoi khung — nhin nhu anh bi cat, va phu de nam
        #    de len dai den do. Chi lo khi soi still, khong lo tren sheet.
        #    Do: dai 15% duoi, hang nao co trung binh sang < 90 = dai den.
        import numpy as np
        aa = np.asarray(crop.convert("L")).astype(float)
        band = aa[int(aa.shape[0] * 0.85):, :]
        dark = int((band.mean(axis=1) < 90).sum())
        if dark >= 3:
            bad.append(f"{name}: {dark} hang TOI o 15% duoi = footer/dai den "
                       f"trang web lot vao khung — ha `ycen` xuong")
        out = crop.resize((W, H), Image.LANCZOS)
        p = os.path.join(OUT, name + ".png")
        out.save(p)
        made.append((name, srcfn, n_in, note))

    print(f"→ {OUT}")
    for name, srcfn, k, note in made:
        print(f"   {name}.png  ({srcfn:14s} · {k} khoanh)  {note}")
    print(f"\n   {len(made)}/9 the · scale {W/CW:.2f}x")
    if bad:
        print("\n🔴 " + "\n🔴 ".join(bad))
        return 1
    print("✅ du 9 the 原典")
    return 0


if __name__ == "__main__":
    sys.exit(main())
