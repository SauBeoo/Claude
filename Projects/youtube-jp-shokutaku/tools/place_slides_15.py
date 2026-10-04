# -*- coding: utf-8 -*-
r"""Map 78 anh AI (ten tu sinh) -> slide_XX.jpg cho video 15, roi copy vao slides_img_photo.

    python tools\place_slides_15.py --check     # chi in bang doi chieu, khong copy
    python tools\place_slides_15.py             # copy that

Vi sao can file nay: extension dat ten theo NOI DUNG prompt, khong theo thu tu.
Renderer doc theo index 0-based -> gan sai thu tu la sai hinh ca bai.
Ba anh "phu nu o bep" (slot 02 / 28 / 75) da SOI MAT truoc khi gan, khong doan theo ten.
"""
import argparse
import io
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SRC = [Path(r"C:\Users\tuana\Downloads\download (5)"),      # lo 1: 78 anh
       Path(r"C:\Users\tuana\Downloads\download (1)")]      # lo 2: 4 anh gen lai (13/17/25/54)
DST = ROOT / "06_VIDEO" / "15_shoga-tabekata" / "slides_img_photo"

# slot -> phan dau ten file (khong tinh duoi/timestamp).  None = CHUA CO ANH.
MAP = {
    0: "Grated_ginger_on_silken_tofu",
    1: "Rice_bowl_on_dining_table",
    2: "Woman_standing_at_kitchen_counter",      # soi mat: tay bam mep bep, khong thay mat
    3: "Sandals_left_on_doorstep",
    4: "Simmering_dashi_broth_with_ginger",
    5: "Hand_lifting_grilled_fish_chopst",
    6: "Miso_soup_bowl_with_ginger",
    7: "Ginger_slices_dropped_into_pot",
    8: "Simmering_broth_with_ginger_slices",
    9: "Person_holding_hot_soup_bowl",
    10: "Grated_ginger_drying_on_plate_202608132200",
    11: "Steam_rising_from_miso_soup",
    12: "Ginger_paste_in_refrigerator_door",
    13: "Hand_squeezing_ginger_into_soup",       # lo 2 (gen lai)
    14: "Tidy_Japanese_home_kitchen",
    15: "Notepad_and_pencil_on_table",
    16: "Ginger_slices_on_cutting_board",
    17: "Chopsticks_holding_sliced_ginger",      # lo 2 (gen lai)
    18: "Fingertips_holding_translucent_g",
    19: "Hands_slicing_ginger_on_board",
    20: "Cut_ginger_rhizome_cross-section",
    21: "Hands_scrubbing_ginger_rhizome",
    22: "Bowl_of_miso_soup",
    23: "Person_holding_warm_bowl",
    24: "Woman_seated_at_dining_table",
    25: "Wet_sponge_in_metal_tin",               # lo 2 - lo 1 ra chong dia, da loai
    26: "Chilled_tofu_summer_supper",
    27: "Woman_seated_at_kitchen_table",
    28: "Older_woman_standing_at_kitchen",        # soi mat: CHAR + con gai o cua
    29: "Hand_pulling_kitchen_drawer",
    30: "Grated_ginger_on_chilled_tofu",
    31: "Summer_table_with_cold_dishes",
    32: "Sweat_drying_near_electric_fan",
    33: "Elderly_person_sitting_in_room",
    34: "Person_touching_bare_ankle",
    35: "Cold_dishes_and_miso_soup",
    36: "Cold_somen_noodles_with_ginger",
    37: "Government_booklet_and_reading_g",
    38: "Hand_turning_booklet_page",
    39: "Hands_resting_together_on_table",
    40: "Raw_fish_on_kitchen_scale",
    41: "Grilled_fish_fillet_on_dish",
    42: "Ginger_rhizome_in_vegetable_basket",
    43: "Two_teacups_on_kitchen_table",
    44: "Grated_ginger_on_plate",
    45: "Ginger_rhizomes_on_counter",
    46: "Gas_flame_burning_under_pot",
    47: "Elderly_person_experiencing_abdo",
    48: "Hand_pushing_breakfast_tray",
    49: "Hand_lifting_soup_bowl",
    50: "Hand_resting_on_table",
    51: "Ginger_slices_on_dish",
    52: "Ginger_drink_sachet_and_water",
    53: "Hand_turning_blank_sachet_over",
    54: "Pouring_sugar_into_ginger_drink",       # lo 2 - lo 1 ra chi cai chen, da loai
    55: "Reading_glasses_on_kitchen_table",
    56: "Ginger_grater_and_ginger_rhizomes",
    57: "Mother_and_daughter_sitting_toge",
    58: "Three_ginger_rhizomes_on_counter",
    59: "Grated_ginger_drying_on_plate_202608132201",
    60: "Bare_feet_stepping_on_scale",
    61: "Teacup_and_pencil_on_table",
    62: "Steaming_bowl_of_miso_soup",
    63: "Ginger_slices_on_wooden_board",
    64: "Broth_poured_into_bowl",
    65: "Ginger_simmering_in_pot",
    66: "Woman_adding_ginger_to_soup",
    67: "Woman_smiling_at_rice_bowl",
    68: "Hand_dropping_ginger_into_pot",
    69: "Ginger_slices_beside_empty_plate",
    70: "Gas_flame_heating_pot",
    71: "Japanese_supper_on_wooden_table",
    72: "Thin_ginger_slices_steaming_in",
    73: "Ginger_slices_in_drying_basket",
    74: "Ginger_rhizome_on_kitchen_counter",
    75: "Elderly_woman_at_kitchen_counter",       # soi mat: sau lung, canh cua so buoi sang
    76: "Hands_washing_vegetables_in_sink",
    77: "Supper_table_laid_for_one",
    78: "Teacup_on_empty_kitchen_table",
    79: "Japanese_supper_for_one",
}

N_SLOT = 80


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    files = []
    for sd in SRC:
        for ext in ("*.jpeg", "*.jpg", "*.png"):
            files += sorted(sd.glob(ext))
    used, missing, dup, notfound = {}, [], [], []

    for slot in range(N_SLOT):
        stem = MAP.get(slot)
        if stem is None:
            missing.append(slot)
            continue
        hit = [f for f in files if f.name.startswith(stem)]
        if not hit:
            notfound.append((slot, stem))
        elif len(hit) > 1:
            dup.append((slot, stem, [h.name for h in hit]))
        else:
            f = hit[0]
            if f in used.values():
                dup.append((slot, stem, ["DUNG LAI FILE DA GAN"]))
            used[slot] = f

    unused = [f.name for f in files if f not in used.values()]

    print(f"nguon : {len(SRC)} folder  ({len(files)} file)")
    print(f"gan   : {len(used)}/{N_SLOT} slot")
    if notfound:
        print("\n[LOI] khong tim thay file cho slot:")
        for s, st in notfound:
            print(f"   slot {s:02d}  <- {st}")
    if dup:
        print("\n[LOI] mo ho / trung:")
        for s, st, names in dup:
            print(f"   slot {s:02d}  <- {st}  :: {names}")
    if missing:
        print(f"\n[THIEU ANH] {len(missing)} slot chua co: " + ", ".join(f"{s:02d}" for s in missing))
    if unused:
        print(f"\n[CHUA DUNG] {len(unused)} file: " + ", ".join(unused))

    if notfound or dup:
        print("\n=> KHONG copy. Sua MAP roi chay lai.")
        return 1

    if a.check:
        print("\n(--check: khong copy)")
        return 0

    DST.mkdir(parents=True, exist_ok=True)
    for slot, f in sorted(used.items()):
        shutil.copy2(f, DST / f"slide_{slot:02d}.jpg")
    print(f"\nOK copy {len(used)} file -> {DST.relative_to(ROOT)}")
    if missing:
        print(f"🔴 CON THIEU {len(missing)} ANH -> CHUA DUOC RENDER VIDEO "
              f"(render-background.md §1.5): slot " + ", ".join(f"{s:02d}" for s in missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
