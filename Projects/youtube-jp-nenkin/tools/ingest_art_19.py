# -*- coding: utf-8 -*-
"""Nhận 82 ảnh AI lô video 19 → đổi tên theo builder + xoá ✦ + đóng khung/cắt nền.

Chạy:  python tools/ingest_art_19.py            (dry-run, chỉ in bản đồ)
       python tools/ingest_art_19.py --go       (thật)

Bản đồ dưới ghép bằng NỘI DUNG (tên file generator đặt theo cảnh, không theo tên builder).
⚠️ Mấy dòng đánh dấu ~ là ghép GẦN ĐÚNG — phải soi mắt trước khi cho qua.
"""
import shutil
import sys
from pathlib import Path

DL = Path.home() / "Downloads"
D5, D6 = DL / "download (5)", DL / "download (6)"
PROJ = Path(__file__).resolve().parents[1]
VDIR = PROJ / "06_VIDEO" / "19_kounenrei-koyou-keizoku-kyufu"

# (thư mục, tiền tố tên file generator) -> tên builder
MAP = [
    # ── sticker (nền magenta) ─────────────────────────────────────────────
    (D6, "Blank_payslip_on_solid_background", "el_kyuryo_meisai", "st"),
    (D6, "Downward_bar_chart_collage", "el_chart_down", "st"),
    (D6, "Lapel_pin_on_magenta_background", "el_shashou", "st"),
    (D6, "Two_men_seated_at_desk", "el_two_men_desk", "st"),
    (D6, "Red_stamp_circle_collage", "el_zero_stamp", "st"),
    # ── ふたりの男性 ──────────────────────────────────────────────────────
    (D5, "Two_men_holding_envelopes", "card_19_futari", "pc"),
    (D5, "Older_hands_holding_brown_envelopes", "card_19_futari_b", "pc"),
    (D5, "Men_walking_in_office_corridor", "card_19_futari_c", "pc"),
    (D5, "Paper_collage_of_workplace_lockers", "card_19_futari_d", "pc"),
    # ── 給料明細 ──────────────────────────────────────────────────────────
    (D5, "Man_holding_payslip_at_table", "card_19_kyuryo_meisai", "pc"),
    (D5, "Payslip_on_wooden_table", "card_19_kyuryo_meisai_b", "pc"),
    # ── 対象は ────────────────────────────────────────────────────────────
    (D5, "Man_checking_warehouse_inventory", "card_19_hataraku", "pc"),
    (D5, "Elderly_person_lifting_cardboard", "card_19_hataraku_b", "pc"),
    (D5, "Man_inserting_card_into_clock", "card_19_hataraku_c", "pc"),
    # ── 三つの問い ────────────────────────────────────────────────────────
    (D6, "Elderly_man_sitting_at_desk", "card_19_hatena", "pc"),
    (D5, "Envelopes_fanned_out_on_desk", "card_19_hatena_b", "pc"),
    (D5, "Elderly_man_holding_brown_envelope", "card_19_hatena_c", "pc"),
    # ── 研究室 ────────────────────────────────────────────────────────────
    (D6, "Elderly_person_at_research_desk", "card_19_kenkyu", "pc"),
    (D5, "Magnifying_glass_on_government", "card_19_kenkyu_b", "pc"),
    # ── 下がった分を補う ──────────────────────────────────────────────────
    (D6, "Hands_exchanging_banknotes_collage", "card_19_koyou_hoken", "pc"),
    (D5, "Elderly_person_placing_banknotes", "card_19_koyou_hoken_b", "pc"),
    # ── 七十五パーセント ──────────────────────────────────────────────────
    (D6, "Measuring_stick_and_coin_stack", "card_19_75percent", "pc"),
    (D5, "Red_thread_crossing_measuring_stick", "card_19_75percent_b", "pc"),
    # ── 松本さん ──────────────────────────────────────────────────────────
    (D6, "Man_opening_desk_drawer", "card_19_matsumoto", "pc"),
    (D5, "Elderly_man_holding_metal_pin", "card_19_matsumoto_b", "pc"),
    (D5, "Older_man_closing_desk_drawer", "card_19_matsumoto_c", "pc"),
    # ── 落とし穴（上限） ──────────────────────────────────────────────────
    (D5, "Coins_and_ruler_on_desk", "card_19_jougen", "pc"),
    (D5, "Ruler_pressing_coin_stack", "card_19_jougen_b", "pc"),
    (D6, "Ruler_pressing_stack_of_coins", "card_19_jougen_c", "pc~"),   # ~ gần đúng
    (D5, "Person_holding_coin_over_stack", "card_19_jougen_d", "pc"),
    # ── 二万八千円 ────────────────────────────────────────────────────────
    (D6, "Elderly_man_reading_passbook", "card_19_28000", "pc"),
    (D5, "Older_finger_on_bank_passbook", "card_19_28000_b", "pc"),
    (D5, "Kitchen_table_collage_with_items", "card_19_28000_c", "pc"),
    # ── 本題 ──────────────────────────────────────────────────────────────
    (D5, "Elderly_person_viewing_governmen", "card_19_hondai", "pc"),
    (D6, "Elderly_person_reading_leaflet", "card_19_hondai_b", "pc~"),  # ~ gần đúng
    # ── 八十四万円 ────────────────────────────────────────────────────────
    (D5, "Paper_collage_of_banknote_stack", "card_19_84man", "pc"),
    (D6, "Torn_banknote_stack_on_table", "card_19_84man_b", "pc"),
    # ── 分かれ目は誕生日 ──────────────────────────────────────────────────
    (D6, "Elderly_person_circling_calendar", "card_19_tanjoubi", "pc"),
    (D5, "Calendar_circled_in_red_marker", "card_19_tanjoubi_b", "pc"),
    (D5, "Calendar_pages_on_desk", "card_19_tanjoubi_c", "pc"),
    (D5, "Marker_lying_beside_wall_calendar", "card_19_tanjoubi_d", "pc"),
    # ── 割合が厳しい ──────────────────────────────────────────────────────
    (D6, "Brass_balance_scale_with_coins", "card_19_wariai", "pc"),
    # ── 同僚のかた ────────────────────────────────────────────────────────
    (D6, "Man_sitting_in_break_room", "card_19_douryou", "pc"),
    (D5, "Man_holding_creased_paper_document", "card_19_douryou_b", "pc"),
    (D5, "Elderly_man_handling_paper_envelope", "card_19_douryou_c", "pc"),
    # ── 一円も出ません ────────────────────────────────────────────────────
    (D6, "Elderly_person_holding_empty_hand", "card_19_zero", "pc"),
    (D5, "Empty_envelope_on_desk", "card_19_zero_b", "pc"),
    # ── CTA ───────────────────────────────────────────────────────────────
    (D6, "Elderly_people_looking_at_tablet", "card_19_cta", "pc"),
    (D5, "Elderly_couple_holding_tablet", "card_19_cta_b", "pc"),
    (D5, "Elderly_person_pouring_tea", "card_19_cta_c", "pc"),
    (D5, "Elderly_couple_seated_together", "card_19_cta_d", "pc"),
    # ── 二つ目の窓口 ──────────────────────────────────────────────────────
    (D6, "Elderly_man_standing_between_cou", "card_19_madoguchi2", "pc"),
    (D5, "Paper_collage_of_service_counter", "card_19_madoguchi2_b", "pc"),
    # ── ここは正確に ──────────────────────────────────────────────────────
    (D6, "Elderly_man_gesturing_at_desk", "card_19_tadashi", "pc"),
    (D5, "Elderly_person_making_gesture", "card_19_tadashi_b", "pc"),
    (D5, "Elderly_man_adjusting_reading_gl", "card_19_tadashi_c", "pc"),
    # ── 繰上げ受給 ────────────────────────────────────────────────────────
    (D6, "Elderly_person_beside_tipped_hou", "card_19_kuriage", "pc"),
    (D5, "Sand_spilled_on_desk", "card_19_kuriage_b", "pc"),
    (D5, "Hourglass_standing_on_desk", "card_19_kuriage_c", "pc"),
    # ── 二重に削られます ──────────────────────────────────────────────────
    (D6, "Scissors_cutting_paper_on_desk", "card_19_nijuu", "pc"),
    (D5, "Scissors_cutting_paper_strip", "card_19_nijuu_b", "pc"),
    (D5, "Paper_strips_on_desk", "card_19_nijuu_c", "pc"),
    # ── 戻りません ────────────────────────────────────────────────────────
    (D6, "Elderly_person_touching_turnstil", "card_19_modoranai", "pc"),
    (D5, "Elderly_hand_on_turnstile_gate", "card_19_modoranai_b", "pc"),
    (D5, "Paper_collage_of_empty_corridor", "card_19_modoranai_c", "pc"),
    # ── 給料明細を見る ────────────────────────────────────────────────────
    (D6, "Finger_tracing_payslip_with_magn", "card_19_meisai_check", "pc"),
    (D5, "Hand_analyzing_blank_payslip_doc", "card_19_meisai_check_b", "pc"),
    # ── 四か月以内 ────────────────────────────────────────────────────────
    (D6, "Calendar_pages_on_desk", "card_19_4kagetsu", "pc"),
    (D5, "Calendar_page_corner_lifting", "card_19_4kagetsu_b", "pc"),
    (D5, "Elderly_person_tearing_calendar", "card_19_4kagetsu_c", "pc"),
    # ── 二つの窓口 ────────────────────────────────────────────────────────
    (D6, "Elderly_man_examining_documents", "card_19_futatsu_mado", "pc"),
    (D5, "Hands_resting_on_documents", "card_19_futatsu_mado_b", "pc"),
    # ── ご注意 ────────────────────────────────────────────────────────────
    (D6, "Paper_collage_of_information_desk", "card_19_chuui", "pc"),
    (D5, "Leaflet_stand_paper_collage", "card_19_chuui_b", "pc"),
    (D5, "Empty_chair_before_information_c", "card_19_chuui_c", "pc"),
    # ── 次回予告 ──────────────────────────────────────────────────────────
    (D6, "Elderly_woman_reading_paper_notice", "card_19_yokoku", "pc"),
    (D5, "Elderly_woman_holding_notice_sheet", "card_19_yokoku_b", "pc"),
    (D5, "Glasses_and_teacup_on_table", "card_19_yokoku_c", "pc"),
    (D5, "Elderly_woman_sitting_by_lamp", "card_19_yokoku_d", "pc"),
]


def find(folder: Path, prefix: str):
    if not folder.exists():
        return None
    c = [p for p in folder.iterdir() if p.name.startswith(prefix)]
    return c[0] if c else None


def main() -> int:
    go = "--go" in sys.argv
    raw = VDIR / "_raw"
    raw.mkdir(parents=True, exist_ok=True)
    ok, miss, used = 0, [], set()
    for folder, prefix, dest, kind in MAP:
        src = find(folder, prefix)
        if src is None:
            miss.append((prefix, dest))
            continue
        used.add(str(src))
        ok += 1
        if go:
            shutil.copy(src, raw / f"{dest}.png")
    print(f"ghép được {ok}/{len(MAP)}")
    if miss:
        print(f"🔴 KHÔNG THẤY {len(miss)} file:")
        for p, d in miss:
            print(f"   {d:26s} <- thiếu '{p}*'")
    spare = []
    for folder in (D5, D6):
        if folder.exists():
            spare += [p.name for p in folder.iterdir() if str(p) not in used]
    if spare:
        print(f"ⓘ {len(spare)} ảnh THỪA (không dùng): {spare}")
    if go:
        print(f"→ đã chép vào {raw}")
    else:
        print("(dry-run — thêm --go để chép thật)")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
