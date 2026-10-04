# -*- coding: utf-8 -*-
r"""ingest_card3_17.py — lô CARD3 (7 ảnh) của video 17: đổi tên → cắt ✦ → ép 1,60.

LÔ: 7 ảnh, 1376×768 — CÙNG cỡ với lô PROBE/CARD/CARD2 nên dùng lại mốc cắt đã đo.
✦ SOI BẰNG MẮT 2026-08-26 (sheet 1:1 crop x1150-1376 · y560-768, cả 7 ảnh):
  thấy rõ ✦ ở **7/7**, mép trái tia sáng nhất ~x=1262 (tâm ~1273 = 0,925W · 0,872H).
  ⚠️ Lần này khác lô PROBE: ở đó 4/5 ảnh ✦ nằm trên nền hoạ tiết nên KHÔNG soi ra;
  lô này nền góc phải toàn màu phẳng (đỏ / kem / navy) nên ✦ hiện rõ cả 7 → xác nhận
  lại hằng số, không phải suy diễn.
  ⛔ Máy đo local-contrast KHÔNG dùng (media-library.md §2.10 ⑤b mục 5: thất bại 4/4
  lần ở ảnh có chữ — lô này có micro-text trên mảnh báo).
CẮT x 0..1229 → 1229×768 = 1,600 (đúng tỉ lệ slot img 940×588), dư ~33px so mép ✦.

⚠️ Hai ảnh (`pointing_at_screen`, `Magnifying_glass`) có DẢI TRẮNG mép phải ~1/8 khung —
cú cắt xoá đúng phần đó, có chủ ý: prompt ghim "right-hand fifth empty" để chịu cắt.

CHẠY:  python tools/ingest_card3_17.py             # backup + đổi tên + cắt → art/
       python tools/ingest_card3_17.py --restore    # xoá output, giữ backup
"""
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\tuana\Downloads\download (4)")
VDIR = PROJ / "06_VIDEO" / "17_nenkin-sagi-jidoonsei-shikyuteishi"
ART = VDIR / "art"
BAK = ART / "_wm_orig"

EXPECT = (1376, 768)
CUT_W = 1229

# generator-name prefix → tên file cần. Duyệt MẮT trên `_sheet_card3.png` 2026-08-26,
# đối chiếu từng ảnh với dòng SCENE trong `art_prompts_photocard3_FLOW.txt`.
# ⚠️ Generator đặt tên theo ảnh NÓ VẼ, không theo thứ tự prompt ⇒ luôn đối chiếu mắt.
MAP = {
    "Elderly_man_hovering_hand_over":     "card_src_c2_te_tomaru.png",    # tay dừng, nhìn TỪ TRÊN
    "Man_resting_hand_on_table":          "card_src_c9_hitokoto.png",     # đt úp mặt, đã thoát
    "Magnifying_glass_examining_blank":   "card_src_c4_keisatsu.png",     # trang cảnh báo + kính lúp
    "Elderly_hand_holding_smartphone":    "card_src_c9_mail_sms.png",     # tin nhắn giả
    "Elderly_man_listening_on_telephone": "card_src_c2_hito_no_koe.png",  # giọng người thân thiện
    "Elderly_person_pointing_at_screen":  "card_src_c4_genten.png",       # màn hình trang cơ quan
    "Elderly_person_viewing_signposts":   "card_src_c12_jikai.png",       # ngã ba 60/65/70
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

    files = [p for p in sorted(SRC.iterdir())
             if p.suffix.lower() in (".jpeg", ".jpg", ".png")]
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
        out = im.crop((0, 0, CUT_W, im.height))
        out.save(ART / tgt)
        done.append((tgt, out.size))

    for t, s in done:
        print(f"   ✓ {t:<32} {s[0]}×{s[1]}  ({s[0]/s[1]:.3f})")
    for m in miss:
        print(f"   🔴 THIẾU nguồn: {m}")
    print(f"\n✓ {len(done)}/{len(MAP)} ảnh → {ART}")
    left = [f.name for f in files if f not in used]
    if left:
        print(f"⚠ còn {len(left)} ảnh chưa dùng trong lô: {left}")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
