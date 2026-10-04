# -*- coding: utf-8 -*-
r"""Nhap 94 anh AI cho video 16: doi ten theo slide_NN + kiem tra + backup.

    python tools\ingest_slides_16.py --check     # chi bao cao, khong ghi gi
    python tools\ingest_slides_16.py             # copy + doi ten vao slides_img_photo/

MAP la BANG TAY (MAP duoi day), khong phai token-matching:
  token-matching tren ten file AI (rat co dong) tra ve 9 shot bi trung + 11 shot rong
  -> khong dung duoc. Doi chieu bang mat 1:1 roi khoa cung o day.

Kiem tra tu dong:
  1. du 94 file, khong file nao thua/thieu, khong shot nao trong
  2. kich thuoc >= 1920 chieu ngang (fetch_photos cua kenh doi >=1920)
  3. ti le ~16:9 (renderer cover-crop -> lech ti le la mat mep)
  4. do sang trung binh -> canh bao anh qua toi (tep 45+ bi phat nang khi hinh toi)
  5. WATERMARK: quet goc duoi-phai, so voi trung vi HANG (media-library 2.10 muc 5)
"""
import argparse
import io
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"C:\Users\tuana\Downloads\download (4)")
DST = ROOT / "06_VIDEO" / "16_banana-yoru-toire" / "slides_img_photo"
BAK = ROOT / "06_VIDEO" / "16_banana-yoru-toire" / "_slides_orig"

# slide_NN  ->  ten file (bo duoi _<timestamp>.jpeg)
MAP = {
    0: "Banana_and_clock_on_plate", 1: "Swollen_ankle_with_sock_impression",
    2: "Empty_dark_hallway_in_night", 3: "Walking_shoes_and_cane_on",
    4: "Glass_of_water_on_table", 5: "Bananas_in_woven_basket",
    6: "Clock_above_empty_chair", 7: "Hand_pushing_glass_of_water",
    8: "Empty_glass_on_draining_rack", 9: "Elderly_person_dozing_in_armchair",
    10: "Elderly_person_holding_forehead", 11: "Glasses_of_water_on_counter",
    12: "Empty_futon_in_bedroom", 13: "Water_flowing_down_sink_drain",
    14: "Tea_leaves_in_sink_drain", 15: "Still_kitchen_before_sunrise",
    16: "Water_drop_hanging_from_tap", 17: "Alarm_clock_on_bedside_table",
    18: "Tidy_home_kitchen_with_kettle", 19: "Japanese_home_dinner_flat_lay",
    20: "Teacup_and_blank_notepad", 21: "Woman_holding_teacup_looking_out",
    22: "Night_light_glowing_above_shoes", 23: "Elderly_woman_standing_in_hallway",
    24: "Hairdressing_salon_chair_beside_", 25: "Elderly_woman_showing_swollen_ankle",
    26: "Older_woman_sitting_on_bed", 27: "Light_glowing_from_bathroom_doorway",
    28: "Elderly_person_preparing_vegetab", 29: "Bare_feet_on_wooden_floor",
    30: "Person_pressing_thumb_on_shin", 31: "Thumb_indentation_on_shin_skin",
    32: "Water_pouches_hanging_from_ankles", 33: "Elderly_person_lying_on_futon",
    34: "Water_moving_through_tube", 35: "Toilet_door_ajar_with_slippers",
    36: "Kitchen_kettle_steaming_on_counter", 37: "Hand_resting_near_smartphone",
    38: "Ripe_banana_standing_in_bowl", 39: "Salt_cellar_and_water_glass",
    40: "Hand_lifting_banana_from_basket", 41: "Banana_lying_on_kitchen_scale",
    42: "Peeled_banana_on_white_plate", 43: "Three_meal_trays_on_table",
    44: "Banana_beside_home_meals", 45: "Tired_kitchen_with_waiting_dishes",
    46: "Person_peeling_banana", 47: "Person_holding_pharmacy_bag",
    48: "Two_teacups_with_rising_steam", 49: "Banana_and_glasses_on_table",
    50: "Hand_reaching_for_banana", 51: "Banana_crossing_near_wristwatch",
    52: "Banana_resting_in_open_palm", 53: "Banana_cut_on_cutting_board",
    54: "Bedside_alarm_clock_in_dark", 55: "Elderly_person_finding_slippers",
    56: "Toothbrush_and_banana_peel_basin", 57: "Bare_feet_stepping_onto_floor",
    58: "Two_bananas_lying_side_by", 59: "Chopsticks_bridging_banana_and_r",
    60: "Bananas_piled_on_plate", 61: "Banana_on_plate",
    62: "Blender_jug_holding_banana_ingre", 63: "Banana_smoothie_with_straw",
    64: "Glass_of_milky_smoothie", 65: "Woman_eating_banana_indoors",
    66: "Banana_slices_arranged_on_plate", 67: "Empty_chair_in_Japanese_kitchen",
    68: "Water_glass_and_banana_standing", 69: "Sunlight_falling_across_tatami_f",
    70: "Sunlit_kitchen_in_Japanese_home", 71: "Two_chairs_facing_each_other",
    72: "Kitchen_wall_clock_showing_time", 73: "Feet_resting_on_chair",
    74: "Older_woman_eating_banana", 75: "Cup_of_barley_tea_steaming",
    76: "Elderly_person_sitting_on_chair", 77: "Elderly_feet_resting_on_cushion",
    78: "Sunset_lighting_living_room_inte", 79: "Elderly_person_walking_residenti",
    80: "Kitchen_window_shows_evening_day", 81: "Woman_sitting_with_plate",
    82: "Banana_on_plate_on_knees", 83: "Night_light_in_morning_corridor",
    84: "Untouched_futon_in_morning_light", 85: "Sunlight_across_wooden_hallway_f",
    86: "Banana_tea_and_cushion_arranged", 87: "Chair_pulled_up_in_kitchen",
    88: "Elderly_hand_between_clock_and", 89: "Fruit_basket_in_kitchen_window",
    90: "Two_elderly_friends_sharing_tea", 91: "Teacup_and_reading_glasses_on",
    92: "Elderly_person_resting_hands_on", 93: "Japanese_family_dinner_table_set",
}


def stem(name):
    return re.sub(r"_\d{10,}\.jpe?g$", "", name).replace("\u2026", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    files = sorted(SRC.glob("*.jpeg")) + sorted(SRC.glob("*.jpg"))
    by = {}
    for f in files:
        by.setdefault(stem(f.name), []).append(f)

    errs, warns = [], []
    if len(files) != 94:
        errs.append(f"co {len(files)} file, can 94")
    for i in range(94):
        if i not in MAP:
            errs.append(f"slide_{i:02d}: chua co trong MAP")
        elif MAP[i] not in by:
            errs.append(f"slide_{i:02d}: khong tim thay file '{MAP[i]}'")
    used = set(MAP.values())
    for k in by:
        if k not in used:
            errs.append(f"file THUA (khong shot nao dung): {k}")
    if len(set(MAP.values())) != len(MAP):
        errs.append("MAP co ten file bi dung 2 lan")

    if errs:
        print("[LOI]")
        for e in errs:
            print("   ", e)
        return 1

    try:
        from PIL import Image, ImageStat
    except ImportError:
        print("can Pillow"); return 1

    rows = []
    for i in range(94):
        f = by[MAP[i]][0]
        im = Image.open(f).convert("RGB")
        w, h = im.size
        ratio = w / h
        g = im.convert("L")
        mean = ImageStat.Stat(g).mean[0]
        # watermark: goc duoi-phai, so voi trung vi CUA CHINH HANG do
        px = g.load()
        x0, x1 = int(w * 0.86), w
        y0, y1 = int(h * 0.83), h
        peak = 0
        import statistics
        for y in range(y0, y1, 2):
            row = [px[x, y] for x in range(0, w, 4)]
            med = statistics.median(row)
            for x in range(x0, x1, 2):
                peak = max(peak, px[x, y] - med)
        rows.append((i, w, h, ratio, mean, peak, f.name))
        if w < 1920:
            warns.append(f"slide_{i:02d}: chi {w}x{h} (<1920 ngang)")
        if abs(ratio - 16 / 9) > 0.02:
            warns.append(f"slide_{i:02d}: ti le {ratio:.3f}, lech 16:9 -> cover-crop se cat mep")

    dark = sorted(rows, key=lambda r: r[4])[:8]
    wm = sorted(rows, key=lambda r: -r[5])[:8]

    print(f"OK  94/94 file khop MAP | {rows[0][1]}x{rows[0][2]} | ti le {rows[0][3]:.3f}")
    if warns:
        print(f"\n[CANH BAO] {len(warns)}")
        for x in warns[:12]:
            print("   ", x)
    print("\n8 anh TOI NHAT (tep 45+ bi phat khi hinh toi — soi mat truoc khi giu):")
    for i, w, h, r, mean, peak, n in dark:
        print(f"    slide_{i:02d}  do sang {mean:5.1f}  {n[:52]}")
    print("\n8 anh nghi CO WATERMARK nhat (chenh so voi trung vi hang, goc duoi-phai):")
    for i, w, h, r, mean, peak, n in wm:
        print(f"    slide_{i:02d}  chenh {peak:5.0f}  {n[:52]}")
    print("\n  ⚠️ So do KHONG chung minh duoc sach — media-library 2.10 muc 5: may do")
    print("     truot 7/8 o lo anh nen sang. Phai SOI MAT 1:1 ca 4 goc.")

    if a.check:
        print("\n(--check: khong ghi file nao)")
        return 0

    # ── CAT WATERMARK ✦ ────────────────────────────────────────────────────
    # Vi tri ✦ CHOT BANG MAT tren _wm_ruler.png (may do bao hoa o mep vung quet,
    # dung cai bay media-library 2.10 muc 5 da canh bao). Do duoc: mep TRAI cua ✦
    # nam o x 1253-1260 tren ca lo 1376x768 -> cat tai x=1248 (0,907W), tru them
    # 5px an toan. Sau do trim DAY ve dung 16:9 (khuon co-dai 19 da chay).
    CUT_X, TARGET = 1248, 16 / 9
    DST.mkdir(parents=True, exist_ok=True)
    BAK.mkdir(parents=True, exist_ok=True)
    for i in range(94):
        f = by[MAP[i]][0]
        shutil.copy2(f, BAK / f.name)
        im = Image.open(f).convert("RGB")
        w, h = im.size
        cx = CUT_X if w == 1376 else int(w * 0.907)
        im = im.crop((0, 0, cx, h))
        nh = int(cx / TARGET)
        if nh < h:
            im = im.crop((0, 0, cx, nh))          # trim DAY
        else:
            im = im.crop((0, 0, int(h * TARGET), h))
        im = im.resize((1920, 1080), Image.LANCZOS)
        im.save(DST / f"slide_{i:02d}.jpg", quality=94)
    (DST.parent / "_map_slide16.json").write_text(
        json.dumps({f"slide_{i:02d}.jpg": MAP[i] for i in range(94)},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {DST.relative_to(ROOT)}  (94 file slide_00.jpg .. slide_93.jpg)")
    print(f"-> {BAK.relative_to(ROOT)}  (ban goc, de --restore tay)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
