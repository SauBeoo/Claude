# -*- coding: utf-8 -*-
r"""ingest_c22.py — nhan LO CLIP t2v cua video 22 (62 khe `c22_*`) vao project Remotion.

BON LO NGUON:
    Sep 10 - 17_58 (23) + 18_02 (23) + 18_03 (15) = 61 clip  -> lo GOC
    Sep 10 - 20_02 (25)                                       -> lo GEN LAI vong 1
Chi so trong bang `MAP` = thu tu `sorted()` cua tung lo, noi lai theo dung thu tu tren
(giong y sheet nghiem thu `S61B_*.png` / `SR_*.png`), nen doc bang la truy ra duoc ANH.

BA VIEC:
  (1) DOI TEN theo khe. Bang `MAP` la ban **DA SOI MAT tung clip** tren 20 sheet 2-3 frame,
      KHONG phai ket qua fuzzy-match. Hai lan match bang may (`map61.json`, `map61b.json`)
      deu sai >=8 cho, trong do co ca khe ENTRY 0 (clip 「葬儀のあと」 bi day sang scene 87).
      => Gate `CAP` duoi day kep tung chi so voi caption Flow: lo ve khac thu tu thi
         ingest DUNG NGAY, khong doi ten sai im lang.
  (2) KHONG CAT WATERMARK. Da soi 1:1 **ca 4 goc** cua 12 clip nen sang nhat o CA HAI lo
      (`WM4C.png`) -> khong co dau (*) nao. Lo i2v truoc co (*) vi no den tu ANH START-FRAME;
      lo nay la t2v thuan nen khong co. => giu tron khung 1280x720, chi upscale 1,50x thay vi
      1,71x nhu ban i2v (cat 12,5% roi keo len). Net hon han.
      LUU Y: day la ket luan DO DUOC cho lo nay, khong phai mien tru. Lo sau van phai soi lai
      (`media-library.md` 2.10 (5)b: vi tri va co (*) doi theo tung lo).
  (3) SCALE 1920x1080 @24fps, bo audio. GIU 24fps — clip Veo la 24fps, ep 30 thi 27% frame
      lap => judder (`feedback_fps_clip_phai_khop_renderer`).

RESUME so **mtime** nguon vs dich (`render-background.md` 2.5), khong so "da ton tai chua".

CHAY:  python tools/ingest_c22.py            # tat ca
       python tools/ingest_c22.py --check    # chi kiem, khong dung ffmpeg
       python tools/ingest_c22.py c22_02 c22_46
"""
import glob
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DL_OLD = [r"C:\Users\tuana\Downloads\Sep 10 - 17_58",
          r"C:\Users\tuana\Downloads\Sep 10 - 18_02",
          r"C:\Users\tuana\Downloads\Sep 10 - 18_03"]
DL_NEW = [r"C:\Users\tuana\Downloads\Sep 10 - 20_02"]
# lo GEN LAI vong 2 (10 clip) — chinh sach so PAIR/ONE/NONE cua `redo2_flow22.py`
DL_Z = [r"C:\Users\tuana\Downloads\Sep 10 - 21_33"]
# lo GEN LAI vong 3 (3 clip)
DL_W = [r"C:\Users\tuana\Downloads\Sep 10 - 22_19"]
OUT = r"E:\Claude\Projects\remotion-vox\public\projects\nenkin-22full\assets"

W, H, FPS = 1920, 1080, 24

# ── BANG MAP — DA SOI MAT (sheet S61B_00..12 va SR_0..6) ────────────────────
# khe -> ("O"|"R", chi so trong lo, caption Flow de gate)
MAP = {
    # ---- lo GOC (O) ---------------------------------------------------------
    "c22_00":   ("Z",  7, "Woman_bows_at_low_table"),  # khung anh tho TRON, hoa cuc — entry 0
    "c22_03":   ("O", 13, "Elderly_woman_viewing_spreadshee"),
    "c22_05_1": ("O",  5, "Elderly_man_pushing_envelope"),
    "c22_07":   ("Z",  0, "Elderly_couple_sitting_together"),  # bac tam cap SACH
    "c22_11":   ("O",  0, "Clerk_talking_with_elderly_visitor"),
    "c22_15":   ("O", 17, "People_queuing_at_office_counter"),
    "c22_17":   ("O",  1, "Clerks_talking_with_elderly_visi"),
    "c22_21_1": ("O", 12, "Elderly_woman_reading_spreadshee"),
    "c22_21_2": ("O", 15, "Man_looking_at_tablet_screen"),       # ! framing gan nhu chi co tay
    "c22_22":   ("Z",  9, "Woman_on_telephone_in_waiting"),  # bang tuong SACH
    "c22_24":   ("O",  7, "Elderly_man_sitting_at_counter"),
    # ⛔ c22_31_1 DA BO: sau 3 vong khong lan nao dung (v1 36,0000 · v2 dung so
    #    nhung cast khong phai nguoi Nhat · v3 36,000 sai gia tri). Scene 31 nay
    #    dung DUNG MOT clip (`c22_31_2`) — xem SHOT_OVERRIDE o build_remotion_22full.
    "c22_31_2": ("Z",  5, "Man_viewing_spreadsheet_on_monitor"),  # 360,000 4/15 360,000 — dung ca hai
    "c22_34":   ("O", 22, "Woman_viewing_spreadsheet_on_mon"),
    "c22_36":   ("O", 24, "Elderly_man_drawing_line"),
    "c22_37_1": ("O", 37, "Older_couple_nodding_in_kitchen"),
    "c22_37_2": ("O", 23, "Couple_sitting_and_nodding_together"),
    "c22_39":   ("Z",  2, "Elderly_man_using_laptop"),  # man hinh bang chu nho, khong so to
    "c22_41":   ("O", 44, "Woman_sitting_at_paperwork_table"),
    "c22_46":   ("W",  2, "Woman_pointing_at_computer_monitor"),  # Flow bo qua 2 lan, doi chu the moi ra
    "c22_47":   ("O", 60, "Woman_straightening_up_indoors"),
    "c22_52":   ("O", 29, "Elderly_woman_looking_at_spreads"),
    "c22_53":   ("Z",  4, "Man_turning_head_in_room"),  # lich/bien SACH
    "c22_56_2": ("O", 41, "Staff_handing_out_leaflets"),
    "c22_57":   ("O",  9, "Elderly_man_viewing_spreadsheet_"),
    "c22_59":   ("O", 39, "Older_woman_lifting_teacup"),
    "c22_63":   ("O", 30, "Elderly_woman_viewing_spreadshee"),
    "c22_66":   ("O", 57, "Man_pointing_at_spreadsheet_monitor"),
    "c22_68":   ("O", 54, "Elderly_woman_reading_papers"),
    "c22_69":   ("Z",  1, "Elderly_man_turns_head"),  # giay chu nho, khong doc duoc
    "c22_70":   ("O", 51, "Elderly_man_viewing_spreadsheet_"),
    "c22_74_2": ("O", 55, "Elderly_woman_straightens_up"),
    "c22_76":   ("O", 48, "Elderly_man_sitting_at_table"),
    "c22_77":   ("O", 58, "Operators_working_in_tax_office"),
    "c22_78":   ("O", 56, "Elderly_woman_tilts_head"),
    "c22_87":   ("O", 53, "Elderly_woman_nods_at_table"),
    "c22_89":   ("O", 46, "Clerk_receiving_envelope_at_counte"),
    # ---- lo GEN LAI vong 1 (R) ---------------------------------------------
    "c22_02":   ("Z",  8, "Woman_holding_bank_passbook"),  # v2 la ban TOT NHAT trong 3: 360,000 dung + mot dong rac nho
    "c22_05_2": ("R",  3, "Elderly_man_holding_envelopes"),
    "c22_08":   ("R", 17, "Older_man_holding_phone"),
    "c22_16":   ("R",  0, "Clerk_pointing_at_spreadsheet_mo"),
    "c22_20":   ("R",  8, "Elderly_man_sitting_at_table"),
    "c22_23":   ("R", 12, "Elderly_man_viewing_spreadsheet_"),
    "c22_28":   ("R", 20, "Staff_briefing_elderly_people_in"),
    "c22_29":   ("R",  5, "Elderly_man_holding_phone_with"),
    "c22_33":   ("R",  6, "Elderly_man_leaning_back_surprised"),
    "c22_35":   ("R", 23, "Woman_holding_bank_passbook"),
    "c22_37_3": ("R",  1, "Couple_sitting_and_nodding_together"),
    "c22_38":   ("Z",  6, "Older_man_holding_financial_docu"),  # to khai chu nho + con dau do, khong so to
    "c22_44":   ("R", 16, "Older_man_holding_palm_out"),
    "c22_48":   ("R", 19, "Seven_wooden_blocks_on_table"),
    "c22_55":   ("R", 13, "Elderly_people_in_care_facility"),
    "c22_56_1": ("R", 22, "Staff_handing_out_leaflets_to"),
    "c22_58":   ("R", 10, "Elderly_man_viewing_desktop_monitor"),
    "c22_62_1": ("R", 15, "Man_holding_card_near_face"),
    "c22_62_2": ("R", 14, "Man_holding_card_in_study"),
    "c22_64":   ("R",  7, "Elderly_man_shaking_head"),
    "c22_65":   ("R", 21, "Staff_briefing_elderly_people_in"),
    "c22_74_1": ("R", 18, "Older_woman_straightens_up_at"),
    "c22_86":   ("R",  9, "Elderly_man_speaking_at_table"),
    "c22_88":   ("R", 11, "Elderly_man_viewing_spreadsheet_"),
    "c22_90":   ("R",  2, "Elderly_couple_nodding_together"),
}

# khe CON phai gen lai sau vong 2 — prompt o `flow22_REDO3_FLOW.txt`
# Khong con khe nao phai gen lai. Hai cho con khiem khuyet, DA CHOT cach xu ly:
#   c22_02   — dung ban v2 (360,000 DUNG, con mot dong rac nho ben duoi). Ba vong deu khong
#              ra ban sach tuyet doi => nhan ban tot nhat, khong gen vong 4.
#   scene 31 — bo `c22_31_1`, dung MOT clip `c22_31_2` (hoan hao) cho ca 9,7s.
REGEN = set()


def lots(dirs):
    out = []
    for d in dirs:
        out += sorted(glob.glob(os.path.join(d, "*.mp4")))
    return out


def main() -> int:
    only = {a for a in sys.argv[1:] if a.startswith("c22_")}
    check = "--check" in sys.argv
    src = {"O": lots(DL_OLD), "R": lots(DL_NEW), "Z": lots(DL_Z), "W": lots(DL_W)}
    print(f"lo GOC {len(src['O'])} · v1 {len(src['R'])} · v2 {len(src['Z'])} "
          f"· v3 {len(src['W'])}")
    if (len(src["O"]), len(src["R"]), len(src["Z"]), len(src["W"])) != (61, 25, 10, 3):
        print("GATE DO: so clip nguon khong khop (61 + 25 + 10 + 3) — MAP dua theo thu tu do")
        return 1
    os.makedirs(OUT, exist_ok=True)

    bad, done, skip = [], 0, 0
    for stem, (lot, idx, cap) in sorted(MAP.items()):
        p = src[lot][idx]
        base = os.path.basename(p)
        # GATE: caption phai khop — lo ve khac thu tu thi dung ngay
        if not base.startswith(cap):
            bad.append(f"{stem}: cho '{cap}' o {lot}[{idx}] nhung thay '{base}'")
            continue
        if only and stem not in only:
            continue
        dst = os.path.join(OUT, stem + ".mp4")
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(p):
            skip += 1
            continue
        if check:
            done += 1
            continue
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", p,
             "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
             "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", dst], check=True)
        done += 1
        flag = " [GEN LAI]" if stem in REGEN else ""
        print(f"  ok {stem:<10} <- {lot}[{idx}] {base[:52]}{flag}")

    if bad:
        print("\nGATE DO — caption khong khop, KHONG doi ten mu:")
        for b in bad:
            print("   " + b)
        return 1

    have = {os.path.splitext(f)[0] for f in os.listdir(OUT) if f.endswith(".mp4")}
    miss = sorted(set(MAP) - have)
    print(f"\n{'ok' if not miss else 'GATE DO'} {len(MAP) - len(miss)}/{len(MAP)} khe co clip"
          f"  (dung {done}, bo qua {skip} vi da moi hon nguon)")
    if miss:
        print("   thieu: " + ", ".join(miss))
    extra = sorted(have - set(MAP))
    if extra:
        print("   la:    " + ", ".join(extra))
    print(f"\n   {len(REGEN)} khe CON SAI, prompt gen lai o flow22_REDO2_FLOW.txt:")
    print("     " + ", ".join(sorted(REGEN)))
    return 0 if not miss else 1


if __name__ == "__main__":
    sys.exit(main())
