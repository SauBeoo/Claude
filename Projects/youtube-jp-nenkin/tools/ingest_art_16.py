# -*- coding: utf-8 -*-
r"""ingest_art_16.py — nhận lô 21 ảnh AI của video 16: đổi tên → cắt ✦ → ép 1,60.

LÔ NÀY (đo bằng mắt 2026-08-24, sheet góc dưới-phải 1:1 cả 21 ảnh + grid 1:1 ảnh nền navy):
- 1376×768, ✦ MỘT dấu/ảnh ở góc dưới-phải, tâm ~(0,931W · 0,875H) = (1281, 672),
  mép trái ✦ xấu nhất ~1246 (ảnh Man_looking nền navy — ✦ to nhất lô, KHÔNG tia dài).
- 3 góc còn lại soi 8 mẫu (sáng + tối): SẠCH.
- CẮT x 0..1229 → 1229×768 = 1,600 đúng tỉ lệ slot `img` 940×588, và bỏ ✦ (dư 17px).
  Máy đo local-contrast ở lô này TRƯỢT (gradient navy→sáng nuốt phép đo) — đừng đổi sang dò máy.

CHẠY:  python tools/ingest_art_16.py            # backup _wm_orig/ + đổi tên + cắt → art/
       python tools/ingest_art_16.py --restore   # trả bản gốc (xoá output, giữ backup)
"""
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\tuana\Downloads\download (7)")
SRC2 = Path(r"C:\Users\tuana\Downloads\download (8)")   # lô 2: 8 ảnh NỀN MỜ (bgimg)
SRC3 = Path(r"C:\Users\tuana\Downloads\download (12)")  # lô 3: 8 ảnh PANEL cho layout pict
VDIR = PROJ / "06_VIDEO" / "16_shotokuzei-12gatsu-seisan-kangen"
ART = VDIR / "art"
BAK = ART / "_wm_orig"

EXPECT = (1376, 768)   # lô khác cỡ ⇒ toạ độ ✦ khác ⇒ CHẶN, soi lại bằng mắt
CUT_W = 1229           # 1229×768 = 1,600 và bỏ ✦ (mép trái ✦ xấu nhất 1246)

# generator-name prefix → tên file SLIDES cần (mapping duyệt mắt 2026-08-24, khớp 21/21 FLOW)
MAP = {
    "ATM_corner_low_illustration":        "bg_tsucho_atm.png",
    "Calculator_and_notebook_on_desk":    "bg_dentaku_techou.png",
    "Couple_sitting_at_table":            "art_ima_stove.png",
    "Elderly_couple_laughing_together":   "art_fusai_ima.png",
    "Elderly_hand_pointing_at_passbook":  "art_tsucho_12gatsu.png",
    "Elderly_hands_holding_blank_paper":  "bg_tsuchisho_te.png",
    "Elderly_man_holding_blank_paper":    "art_takahashi_warau.png",
    "Elderly_man_holding_calculator":     "art_takahashi_dentaku.png",
    "Elderly_man_waving_in_apron":        "art_tanaka_shigoto.png",
    "Elderly_person_examining":           "art_machigai_gimon.png",
    "Elderly_woman_viewing_bank_passbook": "art_okusama_tsucho.png",
    "Envelope_lying_on_wooden_table":     "art_chairo_fuutou.png",
    "Faint_telephone_on_small_table":     "bg_denwa_shinpai.png",
    "Hooded_figure_holding_phone":        "art_sagi_denwa.png",
    "Kerosene_stove_and_passbook_on":     "bg_tsucho_stove.png",
    "Man_looking_at_paper":               "art_takahashi_tsubuyaki.png",
    "Man_opening_wooden_drawer":          "art_hikidashi_sagasu.png",
    "Notice_paper_and_reading_glasses":   "art_furikomi_tsuchisho.png",
    "Open_notebook_and_pen":              "bg_note_pen.png",
    "Study_desk_with_small_lamp":         "bg_kenkyu_desk.png",
    "Wooden_desk_drawer_with_envelope":   "art_nemuru_kami.png",
    # ── LÔ 2 (2026-08-24): 8 ảnh NỀN MỜ cho các thẻ đang trơ chữ. Prompt +
    # bảng nội dung: `06_VIDEO/16_.../bg_prompts_BLOCKS.md` + `bg_prompts_FLOW.txt`.
    # ⚠️ Tên khoá dưới đây là PHỎNG ĐOÁN theo nội dung prompt — generator đặt tên theo
    # ảnh nó vẽ, nên sau khi gen phải đối chiếu tên thật rồi sửa lại đúng ở đây.
    # Tool in "⚠ nguồn KHÔNG dùng tới" cho file nào không khớp, dùng dòng đó để sửa.
    # ✅ tên THẬT do generator đặt (lô `download (8)`, đối chiếu 2026-08-24) — đã thay
    # bộ tên phỏng đoán ban đầu, đúng quy trình ghi ở khối chú thích trên.
    "Papers_and_pen_on_desk":             "bg_shorui_tsumi.png",
    "Closed_bank_passbook_and_calendar":  "bg_tsucho_calendar.png",
    "Older_adults_standing_in_space":     "bg_nenkin_hitobito.png",
    "Hand_pointing_at_notebook_page":     "bg_note_yubi.png",
    "Japanese_coins_on_wooden_table":     "bg_kozeni_tsumi.png",
    "Calculator_lying_on_table":          "bg_dentaku_hitori.png",
    "Notice_sheet_on_table":              "bg_tsuchisho_gyou.png",
    "Wallet_and_coin_discs_on":           "bg_saifu_kozeni.png",
    # ── LÔ 3 (2026-08-25): panel ảnh TO cho 3 thẻ chuyển từ `check`/`steps` sang `pict`
    # (user: *"thay vì text hãy cho nó thành các ảnh minh hoạ… hiển thị lần lượt theo sub"*).
    # Prompt gốc: `06_VIDEO/16_shotokuzei-12gatsu-seisan-kangen/art2_prompts_FLOW.txt`
    "Man_holding_notice_sheet":           "art_p7_hikareteru.png",
    "Elderly_woman_holding_notice_sheet": "art_p7_taisyougai.png",
    "Open_bank_passbook_vector":          "art_p43_uwanose.png",
    "Closed_mailbox_with_crossed":        "art_p43_betsubin.png",
    "Envelope_crossed_out_with_X":        "art_p43_genkin.png",
    "Hand_inserting_passbook_into_ATM":   "art_p55_kicho.png",
    "Finger_pointing_at_blank_paper":     "art_p55_ran.png",
    "Elderly_hands_comparing_blank":      "art_p55_kurabe.png",
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
        return

    files = []
    for d in (SRC, SRC2, SRC3):
        for ext in ("*.jpeg", "*.jpg", "*.png"):
            files += sorted(d.glob(ext))
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
    print(f"✓ {len(done)}/21 ảnh: đổi tên + cắt ✦ + ép {CUT_W}×768 = {CUT_W/768:.3f}")
    for m in miss:
        print(f"🔴 THIẾU nguồn: {m}")
    left = [f.name for f in files if f not in used]
    for l in left:
        print(f"⚠ nguồn KHÔNG dùng tới: {l}")
    print("⛔ NGHIỆM THU: soi 1:1 dải mép phải MỚI của cả 21 ảnh — sheet thu nhỏ CHO QUA ✦.")


if __name__ == "__main__":
    main()
