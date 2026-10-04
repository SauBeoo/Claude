# -*- coding: utf-8 -*-
r"""ingest_art_17.py — nhận lô ảnh AI paper-collage của video 17: đổi tên → cắt ✦ → ép 1,60.

LÔ PROBE (5 ảnh, đo bằng mắt 2026-08-26 — soi zoom 3× vùng x1130-1376 · y600-768 cả 5 ảnh):
- 1376×768. ✦ thấy rõ ở ảnh `Elderly_man_holding_phone`: tâm ~(1273, 670) = **0,925W · 0,872H**
  — khớp hằng số lô 1376×768 đã ghi ở `media-library.md` §2.10 ⑤b (0,928W · 0,878H).
- 4 ảnh còn lại: ✦ nằm trên nền có hoạ tiết (washi tape / trang giấy / nền đỏ) nên KHÔNG
  soi ra được bằng mắt — ⚠️ *không soi ra ≠ không có*. Vẫn cắt cùng mốc cho cả lô.
- 3 góc còn lại: soi sheet 1:1 → SẠCH.
- CẮT x 0..1229 → **1229×768 = 1,600** đúng tỉ lệ slot `img` 940×588, và bỏ ✦ (dư ~24px so
  mép trái ✦ xấu nhất ~1253). ⚠️ Máy đo local-contrast KHÔNG dùng ở lô này (§2.10 ⑤b mục 5:
  đã thất bại 4/4 lần ở ảnh có chữ; lô này có micro-text trên mảnh báo).

⚠️ CẮT LÀ MẤT ĐỒ TRANG TRÍ BÊN PHẢI ở 2 ảnh (`hovering` có washi tape mép phải, `fishing`
có trang giấy trắng bên phải) — chấp nhận có chủ ý: đó là phần trống/trang trí, không phải
chủ thể, và prompt đã cố ý ghim "right-hand fifth empty" đúng để chịu được cú cắt này.

CHẠY:  python tools/ingest_art_17.py            # backup _wm_orig/ + đổi tên + cắt → art/
       python tools/ingest_art_17.py --restore   # trả bản gốc (xoá output, giữ backup)
"""
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\tuana\Downloads\download")
VDIR = PROJ / "06_VIDEO" / "17_nenkin-sagi-jidoonsei-shikyuteishi"
ART = VDIR / "art"
BAK = ART / "_wm_orig"

EXPECT = (1376, 768)   # lô khác cỡ ⇒ toạ độ ✦ khác ⇒ CHẶN, soi lại bằng mắt
CUT_W = 1229           # 1229×768 = 1,600 và bỏ ✦ (mép trái ✦ xấu nhất ~1253)

# generator-name prefix → tên file SLIDES cần.
# Mapping duyệt MẮT 2026-08-26 (đối chiếu từng ảnh với `art_prompts_TENFILE.txt`).
# ⚠️ Generator đặt tên theo ảnh NÓ VẼ, không theo prompt ⇒ luôn phải đối chiếu bằng mắt,
# đừng suy từ thứ tự dòng FLOW (bài học `ingest_art_16.py`).
MAP = {
    "Vibrating_smartphone_on_wood":  "art_denwa_furueru.png",     # entry 0 · img · nền kem
    "Elderly_man_hovering_over_sm":  "art_te_tomaru.png",         # CAO TRÀO · img · nền đỏ
    "Elderly_man_holding_phone":     "art_tsucho_kakenaosu.png",  # panel · pict · nền navy
    "Newspaper_paper_collage_of_d":  "bg_tsukue_denwa.png",       # NỀN NHẠT · bgimg
    "Two_elderly_men_fishing":       "art_tsuri_nakama.png",      # chất người 第11章 · img
}


def main():
    ART.mkdir(parents=True, exist_ok=True)
    BAK.mkdir(parents=True, exist_ok=True)
    if "--restore" in sys.argv:
        n = 0
        for tgt in MAP.values():
            p = ART / tgt
            if p.exists():
                p.unlink()
                n += 1
        print(f"↩ đã xoá {n} output; bản gốc còn trong {BAK}")
        return 0

    files = []
    for ext in ("*.jpeg", "*.jpg", "*.png"):
        files += sorted(SRC.glob(ext))
    used, done, miss = set(), [], []
    for prefix, tgt in MAP.items():
        cand = [f for f in files if f.name.startswith(prefix) and f not in used]
        if not cand:
            miss.append(f"{prefix} → {tgt}")
            continue
        f = cand[0]
        used.add(f)
        im = Image.open(f).convert("RGB")
        if im.size != EXPECT:
            print(f"🔴 CHẶN {f.name}: {im.size} ≠ lô {EXPECT} — toạ độ ✦ đo cho lô kia")
            continue
        b = BAK / f.name
        if not b.exists():
            im.save(b)
        im.crop((0, 0, CUT_W, im.height)).save(ART / tgt)
        done.append(tgt)

    print(f"✓ {len(done)}/{len(MAP)} ảnh: đổi tên + cắt ✦ + ép {CUT_W}×768 = {CUT_W/768:.3f}")
    for t in done:
        print(f"   - {t}")
    for m in miss:
        print(f"🔴 THIẾU nguồn: {m}")
    for l in [f.name for f in files if f not in used]:
        print(f"⚠ nguồn KHÔNG dùng tới: {l}")
    print("⛔ NGHIỆM THU: soi 1:1 dải mép phải MỚI của cả lô — sheet thu nhỏ CHO QUA ✦.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
