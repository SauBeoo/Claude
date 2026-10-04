# -*- coding: utf-8 -*-
r"""make_genten_21b.py — 原典 khuôn MỚI: ảnh chụp thật, cắt CHẶT, KHÔNG vẽ khoanh vào ảnh.

Khác `make_genten_21.py` ở ba chỗ, cả ba đều có số:

① **KHUNG RA = Ô `art` CỦA THẺ (940×606), KHÔNG phải 1920×1080.**
   Bản cũ xuất full-frame nên cắt rộng `CW=990` vẫn ra scale 1,94×. Nhét đúng ảnh đó
   vào ô `art` của lớp sân khấu thì scale tụt còn **0,95× — NHỎ HƠN CẢ TRANG WEB GỐC**
   (đo 2026-09-06). Muốn giữ scale ≥1,40 (chữ web 16px → 22px = sàn `audience-45plus`
   §3) thì bề rộng cắt phải **≤671px**:
       scale = 940 / CW   ⇒  CW 990→0,95×  ·  800→1,18×  ·  700→1,34×  ·  **671→1,40×**

② **KHOANH THEO **CÂU**, KHÔNG THEO **DÒNG**.** Bảng `CARDS` của bản cũ khoanh trọn dòng
   (vd `(210,716,1180,742)` = **970px**) nên không đời nào lọt 671px. Nhưng câu thật sự
   cần trích — 「提出した場合と提出しなかった場合で、所得税率に差はありません。」 — chỉ
   rộng **~490px**; phần còn lại của dòng là câu KHÁC. Khoanh theo câu vừa lọt crop, vừa
   trỏ đúng thứ đang đọc.
   ⚖️ Câu nào dài thật (>671px) thì cắt rộng hơn và **chấp nhận scale <1,40** — tool in
   cảnh báo. Lúc đó lớp đọc được là pin `quote` (chữ do FONT vẽ, luôn sắc nét), còn ảnh
   chụp giữ vai **bằng chứng xuất xứ**. Đây đúng cách フクロウ 1,63M làm: screenshot bảng
   chữ nhỏ + nhãn TO đè lên + trích nguyên văn bên dưới.

③ **KHÔNG VẼ KHOANH VÀO ẢNH.** Xuất `genten_boxes.json` = toạ độ hộp theo TỈ LỆ của ảnh
   ra, để builder gắn thành pin `frame` — khoanh **MỌC DẦN** đúng lúc lời đọc tới
   「赤で囲んだ」. Vẽ sẵn vào ảnh thì khoanh có mặt từ giây đầu, mất hết ý nghĩa chỉ trỏ.

⛔ **KHÔNG GEN AI.** Đây là BẰNG CHỨNG: chữ phải đọc được, cấm làm mờ, cấm vẽ lại.
   Ảnh gốc chụp 2026-09-04 bằng `chrome-headless-shell`, để ở `06_VIDEO/<STEM>/_genten_raw/`.

🔴 Toạ độ chốt BẰNG MẮT, không bằng máy — cùng lý lẽ `media-library.md` §2.10 ⑤
   (định vị bằng máy thất bại 4/4 lần ở ảnh có chữ).

CHẠY:  python tools/make_genten_21b.py [--only genten21b_04]
"""
import argparse
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image  # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
RAW = os.path.join(VD, "_genten_raw")
OUT = os.path.join(VD, "genten_b")

# ── ô `art` của make_stage khi thẻ KHÔNG có `cap` (đo bằng máy 2026-09-06) ──────
# 🔴 Thẻ 原典 CỐ Ý không dùng `cap`: có `cap` thì ô tụt còn 940×546 và scale rơi thêm.
#    Lời chú thích đi vào pin `quote`, chỗ nó đọc được, chứ không đi vào `cap`.
BW, BH = 940, 606
SCALE_MIN = 1.40                 # sàn: chữ web 16px → 22px (`audience-45plus` §3)
CW_MAX = int(BW / SCALE_MIN)     # = 671
MARGIN = 26                      # lề quanh hộp khoanh, trong toạ độ ảnh GỐC

# ── thẻ: (tên, ảnh nguồn, [hộp (x0,y0,x1,y1) trong ảnh FULL], nguồn ghi, trích) ──
# 🔴 Hộp = CÂU, không phải DÒNG. Đo bằng mắt trên `_genten_raw/*.png`.
NL = "\n"
CARDS = [
    ("genten21b_04", "faq_full.png",
     [(210, 714, 703, 744)],
     "日本年金機構「扶養親族等申告書」FAQ（令和8年8月時点）",
     "提出した場合と提出しなかった場合で、" + NL + "《所得税率に差はありません》。"),
    ("genten21b_05", "faq_full.png",
     [(222, 788, 1122, 842), (222, 850, 900, 904)],
     "日本年金機構「扶養親族等申告書」FAQ（令和8年8月時点）",
     "どちらの式も、合計税率は《五・一〇五パーセント》。" + NL + "違うのは、引ける控除のほうです。"),
]


def build(name, src, boxes, srcline, quote, report):
    p = os.path.join(RAW, src)
    if not os.path.exists(p):
        print(f"  🔴 thiếu ảnh gốc {src}")
        return None
    im = Image.open(p).convert("RGB")
    IW, IH = im.size
    x0 = min(b[0] for b in boxes) - MARGIN
    x1 = max(b[2] for b in boxes) + MARGIN
    y0 = min(b[1] for b in boxes) - MARGIN
    y1 = max(b[3] for b in boxes) + MARGIN
    need_w = x1 - x0

    # bề rộng cắt: ưu tiên CW_MAX; hộp rộng hơn thì phải nới (và mất scale)
    cw = max(need_w, min(CW_MAX, need_w if need_w > CW_MAX else CW_MAX))
    if need_w > CW_MAX:
        cw = need_w
    else:
        cw = CW_MAX
    ch = int(round(cw * BH / BW))

    # canh giữa cụm hộp trong khung cắt, rồi kẹp vào trong ảnh
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    cx0 = int(round(max(0, min(IW - cw, cx - cw / 2))))
    cy0 = int(round(max(0, min(IH - ch, cy - ch / 2))))
    crop = im.crop((cx0, cy0, cx0 + cw, cy0 + ch))
    outim = crop.resize((BW, BH), Image.LANCZOS)

    os.makedirs(OUT, exist_ok=True)
    fp = os.path.join(OUT, name + ".png")
    outim.save(fp)

    scale = BW / cw
    fr = [[round((b[0] - cx0) / cw, 4), round((b[1] - cy0) / ch, 4),
           round((b[2] - cx0) / cw, 4), round((b[3] - cy0) / ch, 4)] for b in boxes]
    ok = all(0 <= f[0] and 0 <= f[1] and f[2] <= 1 and f[3] <= 1 for f in fr)
    flag = "✅" if scale >= SCALE_MIN else "⚠️ "
    print(f"  {flag} {name}  cắt {cw}×{ch} → {BW}×{BH}  scale {scale:.2f}×  "
          f"chữ 16px→{16*scale:.0f}px" + ("" if ok else "   🔴 HỘP LỌT RA NGOÀI KHUNG"))
    if scale < SCALE_MIN:
        print(f"      câu dài {need_w}px > {CW_MAX}px ⇒ không đạt sàn {SCALE_MIN}×. "
              f"Ảnh giữ vai BẰNG CHỨNG, lớp đọc được là pin `quote`.")
    report[name] = {"img": fp.replace("\\", "/"), "boxes": fr, "src": srcline,
                    "quote": quote, "scale": round(scale, 3), "crop_w": cw,
                    "fits": ok}
    return fp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="chỉ dựng 1 thẻ")
    a = ap.parse_args()
    print(f"── 原典 khuôn mới → ô art {BW}×{BH} · sàn scale {SCALE_MIN}× (cắt ≤{CW_MAX}px) ──")
    rep = {}
    for name, src, boxes, srcline, quote in CARDS:
        if a.only and name != a.only:
            continue
        build(name, src, boxes, srcline, quote, rep)
    jp = os.path.join(VD, "genten_boxes.json")
    old = {}
    if os.path.exists(jp):
        old = json.load(io.open(jp, encoding="utf-8"))
    old.update(rep)
    io.open(jp, "w", encoding="utf-8").write(json.dumps(old, ensure_ascii=False, indent=1))
    print(f"→ {OUT}\n→ {jp}  ({len(old)} thẻ)")
    bad = [k for k, v in rep.items() if not v["fits"]]
    if bad:
        print(f"🔴 hộp lọt ra ngoài khung ở: {', '.join(bad)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
