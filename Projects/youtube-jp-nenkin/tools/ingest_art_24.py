# -*- coding: utf-8 -*-
r"""ingest_art_24.py — nhận 45 ảnh AI lô video 24 (Downloads\download (7)) → cắt watermark
+ đóng khung photocard (42) / cutout sticker magenta (3) → 06_VIDEO/24_.../{photocard,sticker}/.

Map ghép bằng NỘI DUNG (tên file generator đặt theo cảnh, không theo tên builder) — đã đối
chiếu bằng mắt từng ảnh. 6 cặp đánh dấu `~` là ghép GẦN ĐÚNG, soi lại nếu nghi ngờ.

CHẠY:  python tools/ingest_art_24.py            (dry-run, chỉ in bản đồ)
       python tools/ingest_art_24.py --go       (thật)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import make_photocard as MP  # noqa: E402
import cutout_sticker as CS  # noqa: E402

DL = Path.home() / "Downloads" / "download (7)"
PROJ = Path(__file__).resolve().parents[1]
SLUG = "24_shien-kyufukin-midori-futo-9gatsu"
VDIR = PROJ / "06_VIDEO" / SLUG

# (tiền tố tên file generator, tên đích, ghi chú)
STICKER_MAP = [
    ("Green_envelope_on_magenta_backgr", "el_green_envelope"),
    ("Blank_postcard_form_collage",      "el_hagaki"),
    ("Japanese_postage_stamp_collage",   "el_stamp"),
]

# seed/rotation xen kẽ dấu — tránh 2 ảnh liền kề nghiêng cùng chiều
# (tiền tố, tên đích, seed, rot, variant) — variant = thứ tự xuất hiện khi 1 tiền tố khớp
# ≥2 file (0 = file KHÔNG có hậu tố `_2`, 1 = file CÓ hậu tố `_2`). Không dùng regex vì
# "_2" của hậu tố trùng ký tự với "_2" trong cụm ngày `_202609010050` → match nhầm.
PHOTOCARD_MAP = [
    ("Hand_reaching_into_mailbox_slot",     "card_24_futou",             1, -1.8, 0),
    ("Green_envelope_on_table",             "card_24_futou_b",           2,  2.1, 0),
    ("Elderly_couple_reading_letters",      "card_24_taisho",            3, -1.5, 0),
    ("Elderly_person_reaching_into_mai",    "card_24_tomaru",            4,  2.3, 0),
    ("Research_desk_with_envelope_and",     "card_24_kenkyu",            5, -2.0, 0),
    ("Paper_collage_of_mailboxes",          "card_24_yubinbako",         6,  1.6, 0),
    ("Vintage_newspaper_collage_with_m",    "card_24_yubinbako_b",       7, -1.9, 0),
    ("Postcard_slid_from_green_envelope",   "card_24_naka",              8,  2.2, 0),
    ("Paper_collage_of_empty_bedroom",      "card_24_aratani",           9, -1.6, 0),
    ("Family_paper_collage_editorial_f",    "card_24_setai",            10,  1.8, 0),
    ("Cardboard_boxes_stacked_by_door",     "card_24_setai_b",          11, -2.1, 0),
    ("Paper_collage_of_calendar_pages",     "card_24_kyonen",           12,  1.5, 0),
    ("Paper_collage_calculator_on_desk",    "card_24_keisan",           13, -1.7, 0),
    ("Elderly_woman_by_kitchen_window",     "card_24_watanabe",         14,  2.0, 0),
    ("Elderly_woman_sitting_at_table",      "card_24_watanabe_b",       15, -1.4, 0),  # ~
    ("Elderly_woman_reading_blank_post",    "card_24_watanabe_hagaki",  16,  1.9, 0),
    ("Elderly_woman_pressing_postage_s",    "card_24_watanabe_hagaki_b",17, -2.3, 1),  # ~
    ("Vintage_paper_collage_of_envelope",   "card_24_tsuchi",           18,  1.6, 0),  # ~
    ("Elderly_person_viewing_bank_pass",    "card_24_watanabe_kingaku", 19, -1.8, 0),
    ("Envelope_with_red_X_mark",            "card_24_zero",             20,  2.1, 0),
    ("Elderly_person_certificate_paper",    "card_24_menjo",            21, -1.5, 0),
    ("Paper_collage_showing_empty_room",    "card_24_shougai",          22,  1.7, 0),  # ~
    ("Elderly_woman_opening_desk_drawer",   "card_24_kitte",            23, -2.2, 0),
    ("Elderly_woman_pressing_postage_s",    "card_24_kitte_b",          24,  1.4, 0),
    ("Kerosene_heater_in_home_entryway",    "card_24_touyu",            25, -1.9, 0),
    ("Smartphone_and_tea_on_table",         "card_24_cta",              26,  2.0, 0),
    ("Elderly_hand_touching_empty_mailbox", "card_24_konai",            27, -1.6, 0),
    ("Paper_collage_with_circled_calendar", "card_24_3kagetsu",         28,  1.8, 0),
    ("Paper_collage_of_wooden_doors",       "card_24_henkou",           29, -2.0, 0),
    ("Envelope_and_clock_on_table",         "card_24_tomaru_2",         30,  1.5, 0),
    ("Elderly_woman_near_window",           "card_24_nakamura",         31, -1.7, 0),
    ("Elderly_woman_writing_at_table",      "card_24_nakamura_b",       32,  2.2, 0),
    ("Elderly_woman_checking_empty_mai",    "card_24_tomatta",          33, -1.4, 0),
    ("Woman_reaching_for_telephone_han",    "card_24_saikai",           34,  1.9, 0),
    ("Elderly_hand_dialing_old_telephone",  "card_24_soudan",           35, -2.1, 0),
    ("Elderly_woman_marking_wall_calendar", "card_24_calendar_maru",    36,  1.6, 0),
    ("Vintage_newsprint_paper_collage",     "card_24_kigen",            37, -1.8, 1),  # ~
    ("Vintage_newsprint_paper_collage",     "card_24_ichigatsu",        38,  2.0, 0),  # ~
    ("Elderly_hand_hovering_over_ATM",      "card_24_sagi",             39, -1.5, 0),
    ("Paper_collage_with_tea_cup",          "card_24_cta2",             40,  1.7, 0),
    ("Elderly_couple_framed_on_shelf",      "card_24_yokoku",           41, -2.3, 0),
    ("Vintage_newspaper_editorial_pape",    "card_24_yokoku_b",         42,  1.4, 0),  # ~
]


def find_one(folder: Path, prefix: str, variant: int, used: set):
    """Tìm file khớp bằng TIỀN TỐ THUẦN (không regex) — `variant` chọn file thứ mấy
    trong số các file cùng tiền tố (0-index, sắp theo tên: file KHÔNG `_2` luôn đứng
    trước file `_2` vì '.' < '_' trong bảng mã)."""
    cand = sorted(p for p in folder.iterdir() if p not in used and p.stem.startswith(prefix))
    if variant < len(cand):
        return cand[variant]
    return None


def main() -> int:
    go = "--go" in sys.argv
    if not DL.exists():
        print(f"🔴 không thấy {DL}")
        return 1

    st_dst = VDIR / "sticker"
    pc_dst = VDIR / "photocard"
    st_dst.mkdir(parents=True, exist_ok=True)
    pc_dst.mkdir(parents=True, exist_ok=True)

    used = set()
    ok, miss = 0, []

    print("── STICKER (magenta cutout) ──")
    for prefix, name in STICKER_MAP:
        src = find_one(DL, prefix, 0, used)
        if src is None:
            miss.append((prefix, name))
            print(f"🔴 THIẾU nguồn: {prefix} → {name}")
            continue
        used.add(src)
        if go:
            r, err = CS.cut(src, st_dst / f"{name}.png")
            if err:
                print(f"🔴 {src.name} → {name}: {err}")
                continue
            w, h, dropped, tint = r
            flag = "" if tint == 0 else f"  ⚠ {tint}px vệt tím"
            print(f"   ✓ {name:<20} {w}×{h}  blob bỏ={dropped}{flag}  ← {src.name}")
        else:
            print(f"   {name:<20} ← {src.name}")
        ok += 1

    print("\n── PHOTOCARD (torn-paper frame, cắt watermark) ──")
    for prefix, name, seed, rot, variant in PHOTOCARD_MAP:
        src = find_one(DL, prefix, variant, used)
        if src is None:
            miss.append((prefix, name))
            print(f"🔴 THIẾU nguồn: {prefix} → {name}")
            continue
        used.add(src)
        if go:
            sz = MP.build(src, pc_dst / f"{name}.png", seed=seed, rot=rot)
            print(f"   ✓ {name:<28} {sz[0]}×{sz[1]}  (xoay {rot:+.1f}°)  ← {src.name}")
        else:
            print(f"   {name:<28} (xoay {rot:+.1f}°)  ← {src.name}")
        ok += 1

    spare = [p.name for p in DL.iterdir() if p not in used]
    print(f"\nghép được {ok}/{len(STICKER_MAP) + len(PHOTOCARD_MAP)}")
    if miss:
        print(f"🔴 THIẾU {len(miss)} — chưa map được")
    if spare:
        print(f"ⓘ {len(spare)} ảnh THỪA (không dùng): {spare}")
    if not go:
        print("\n(dry-run — thêm --go để chép thật)")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
