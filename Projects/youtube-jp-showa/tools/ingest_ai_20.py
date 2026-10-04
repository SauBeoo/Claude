# -*- coding: utf-8 -*-
"""ingest_ai_20.py — nhan lo AI video 20 tu Downloads -> cells_in_ai/ai_NN_<key>.png|.mp4 da LAM SACH.

Lam sach (media-library.md §2.10 ⑤b ⑧): cat vien den (pillarbox, max-kenh <=12 tai 3 moc) -> CAT ✦ mep phai
o 0,905W -> trim 16:9 chia doi tren/duoi -> 1920x1080. Anh: PNG. Clip: giu fps goc (24), crf 16.
Ban goc giu o _ai_in/ (khong ghi de). Ghep canh <- file bang MAT (ten file Flow tu dat, khong tin ten).

    python tools/ingest_ai_20.py            # lam sach + in bao cao
    python tools/ingest_ai_20.py --corners  # sheet 1:1 goc duoi-phai + 3 goc con lai de soi ✦
"""
import sys, json, subprocess, io
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
import numpy as np

VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\20_sumai-okane")
IN = VD / "_ai_in"; OUT = VD / "cells_in_ai"; OUT.mkdir(exist_ok=True)
WM = 0.905
A, B, C, L = "z18_41/", "z19_20/", "z19_29/", "loose/"

# key -> (anh tinh, clip hoac None). Anh = anh goc cua clip neu co (cung khung).
MAP = {
 "hagaki_bundle":      (C + "Open_tea_cabinet_drawer_postcards_20260927193143.jpg", C + "Woman_lifts_postcards_from_drawer_20260927193144.mp4"),
 "hagaki_turn":        (A + "Woman_turning_over_blank_postcards_20260927191401.jpg", None),
 "drawer_empty":       (A + "Looking_into_tea_cabinet_drawer_20260927191401.jpg", None),
 "father_print":       (A + "Man_working_at_printing_press_20260927191401.jpg", None),
 "fudousan_door":      (A + "Couple_reflected_in_glass_door_20260927191401.jpg", None),
 "apart_corridor":     (A + "Woman_walking_down_wooden_corridor_20260927191401.jpg", None),
 "window_monohoshi":   ("z19_39/Woman_opening_window_in_room_20260927194034.jpg", None),   # REDO1 (lo 1 ra anh ghep 4 o) · me dung ngoai cua so — CO Y NHAN, van doc ra "mo cua, sao phoi sat ben"
 "father_nod":         ("z19_39/Parents_standing_in_tatami_room_20260927194034.jpg", None),   # REDO1 (lo 1 ra anh ghep 2 o)
 "two_envelopes":      (A + "Envelopes_on_table_with_tea_20260927191401.jpg", None),
 "shared_toilet":      (A + "Wooden_apartment_corridor_at_dawn_20260927191401.jpg", None),
 "toilet_line":        (A + "Tenants_waiting_outside_toilet_door_20260927191401.jpg", None),
 "senmenki_prep":      (A + "Woman_tucking_towel_into_basin_20260927191401.jpg", None),
 "night_walk_geta":    (A + "Parents_walking_in_residential_lane_20260927191401.jpg", None),
 "mother_baby_sento":  (A + "Mother_drying_baby_in_bathhouse_20260927191401.jpg", L + "Mother_drying_baby_with_towel_20260927191800.mp4"),
 "mother_dress_baby":  (A + "Mother_buttoning_cardigan_on_baby_20260927191401.jpg", None),
 "sento_noren_night":  (A + "Woman_entering_bathhouse_with_baby_20260927191401.jpg", None),
 "mother_tub_baby":    (A + "Woman_holding_baby_in_bath_20260927191401.jpg", L + "Mother_lowers_baby_into_water_20260927191849.mp4"),
 "bandai_lady":        (A + "Woman_sitting_in_bathhouse_booth_20260927191401.jpg", None),
 "after_bath_walk":    (A + "Woman_carrying_baby_in_lane_20260927191401.jpg", None),
 "father_flyer":       (A + "Father_holding_paper_at_home_20260927191401.jpg", L + "Father_unfolds_sheet_for_woman_20260927191855.mp4"),
 "flyer_table":        (A + "Man_sitting_at_tatami_table_20260927191401.jpg", None),
 "mother_reads_flyer": (A + "Mother_holding_paper_indoors_20260927191401.jpg", None),
 "hagaki_single":      (A + "Postcard_on_wooden_tea_cabinet_20260927191401.jpg", None),
 "hagaki_six_table":   (A + "Japanese_postcards_on_wooden_table_20260927191401.jpg", None),
 "father_smoke_out":   (A + "Man_smoking_near_apartment_stair…_20260927191401.jpg", None),
 "mother_drawer":      (A + "Woman_sliding_postcard_into_drawer_20260927191401.jpg", None),
 "hagaki_seventh":     (A + "Woman_approaching_postcard_near_…_20260927191401.jpg", None),
 "danchi_boxes":       (A + "Woman_stepping_into_bathroom_20260927191401.jpg", None),
 "danchi_bath_mother": (B + "Mother_holding_child_in_bathtub_20260927192346.jpg", B + "Mother_holding_child_in_bathtub_20260927192347.mp4"),
 "father_beer":        (B + "Man_sitting_beside_sleeping_child_20260927192346.jpg", B + "Man_sitting_beside_sleeping_child_20260927192347.mp4"),
 "futon_room":         (A + "Family_sleeping_in_apartment_20260927191401.jpg", None),
 "coat_pocket":        (A + "Woman_opening_coat_pocket_20260927191401.jpg", None),
 "passbook_small":     (A + "Passbook_on_table_with_tea_20260927191401.jpg", None),
 "house_frame":        (A + "Carpenters_building_house_on_plot_20260927191401.jpg", None),
 "hanko_form":         (B + "Parents_stamping_paper_at_table_20260927192346.jpg", B + "Parents_stamping_paper_at_table_20260927192347.mp4"),
 "house_pillar":       (A + "Man_standing_in_wooden_house_20260927191401.jpg", None),
 "mother_worried":     (A + "Mother_and_father_at_table_20260927191401.jpg", None),
 "nameplate_nail":     (A + "Man_hammering_wooden_nameplate_20260927191401.jpg", None),
 "new_bath_window":    (A + "Wooden_bathtub_with_steaming_water_20260927191401.jpg", None),
 "father_old_porch":   (A + "Elderly_man_sitting_on_veranda_20260927191401.jpg", None),
 "chadansu_open":      (A + "Tea_cabinet_in_tatami_room_20260927191401.jpg", None),
 "hands_rubber_band":  (A + "Woman_removing_rubber_band_from_20260927191401.jpg", None),
 "hagaki_back_0":      (A + "Postcard_lying_on_tatami_20260927191401.jpg", None),
 "hagaki_back_1":      (A + "Woman_holding_blank_postcard_20260927191401.jpg", None),
 "hagaki_back_2":      (A + "Postcard_on_wooden_table_20260927191401.jpg", None),
 "hagaki_back_3":      (A + "Japanese_postcard_on_wooden_box_20260927191401.jpg", None),
 "hagaki_back_4":      (A + "Japanese_postcard_on_paper_sill_20260927191401.jpg", None),
 "hagaki_back_5":      (A + "Woman_holding_blank_postcard_20260927191401_2.jpg", None),
 "hagaki_back_6":      (A + "Japanese_postcard_on_tea_cabinet_20260927191401.jpg", None),
 "drawer_hagaki_stack": (A + "Postcards_displayed_on_folded_ca…_20260927191401.jpg", None),
 "mother_young_letter": (A + "Mother_holding_postcard_in_room_20260927191401.jpg", None),
 "old_father_wallet":  (C + "Elderly_man_holding_worn_wallet_20260927193143.jpg", C + "Old_man_opening_wallet_20260927193144.mp4"),
 "worn_hagaki":        (A + "Man_holding_old_postcard_20260927191401.jpg", None),
 "father_goes_out":    (None, None),   # hook v3 — cho anh cua user
 "mother_argue":       ("v3/Mother_and_father_arguing_2K_20260927235054.jpg", None),   # hook v3 · Animate bi Flow chan 3 lan -> anh TINH
 "mother_argue":       ("v3/Mother_and_father_arguing_2K_20260927235054.jpg", None),   # hook v3 · Animate bi Flow chan 3 lan -> anh TINH (ban 2K, net hon ban 1376 trong z23_40)
 "father_goes_out":    ("z23_40/Man_opening_apartment_door_20260927235512.jpg", None),  # hook v3 dong 5
 "couple_table":       (None, "z23_40/Woman_sliding_postcard_to_man_20260927235512.mp4"),  # dong 55 (ban ngay -> khong hop hook 冬の夜)
 "bandai_lady_old":    (A + "Woman_holding_curtain_in_bathhouse_20260927191401.jpg", None),
}
# anh DU cua user dung lam o THU HAI de chẻ khe clip AI qua tran 9,6s (ten file co dinh, khong theo thu tu S)
EXTRA = {
 "ai_55_mother_tub_still":  A + "Woman_holding_baby_in_bath_20260927191401.jpg",       # dong 40 (clip 17 phu dong 39)
 "ai_56_danchi_bath_b":     A + "Mother_holding_toddler_in_bathtub_20260927191401.jpg", # dong 75
 "ai_57_hanko_form_b":      A + "Father_holding_seal_with_mother_20260927191401.jpg",   # dong 94 nua sau
 "ai_58_hagaki_drawer_b":   A + "Old_postcards_in_tea_cabinet_20260927191401.jpg",       # dong 7 — thay pxv:v_letter__03 (chu viet tay TIENG ANH, hook 25s)
}
# ghi so CO Y KHONG DUNG (ai-video-regen.md §1: ghi ca thu da nhan lan thu bo)
UNUSED = {
 "z23_40/Man_and_woman_looking_at_20260927235512.jpg": "anh goc cua clip couple_table -> dung = trung hinh",
 "z23_40/Mother_and_father_arguing_20260927235512.jpg": "ban 1376 cua anh 2K da dung",
 A + "Man_sitting_beside_sleeping_child_20260927191401.jpg": "ban thay the father_beer — dung ban 19_20 (anh goc cua clip)",
 A + "Father_holding_old_leather_wallet_20260927191401.jpg": "ban thay the old_father_wallet",
 B + "Elderly_man_holding_worn_wallet_20260927192346.jpg": "anh goc clip Father_holding_old_leather_wallet (thay the)",
 B + "Postcards_in_open_wooden_drawer_20260927192346.jpg": "anh goc clip People_bowing (thay the)",
 B + "Father_holding_old_leather_wallet_20260927192347.mp4": "clip vi thay the — chon Old_man_opening_wallet (ro dong tac mo vi)",
 B + "People_bowing_in_morning_light_20260927192347.mp4": "clip ngan keo thay the — chon Woman_lifts_postcards (co tay nhac bo thiep)",
}


def order():
    import gen_realism_20 as R
    return {s["key"]: i for i, s in enumerate(R.S, 1)}


def bars(frames):
    """so cot den lien tiep o mep trai/phai (max-kenh <=12 o MOI moc).
    🔴 nguong 22 cua luat bat nham TUONG TOI (bon tam: mep phai 18-25) -> cat oan 48px; vien that <=12 (do 1-2)."""
    m = np.max(np.stack([f.max(axis=2) for f in frames]), axis=0)      # HxW
    col = m.max(axis=0)
    l = 0
    while l < len(col) // 4 and col[l] <= 12: l += 1
    r = 0
    while r < len(col) // 4 and col[-1 - r] <= 12: r += 1
    return l, r


WM_1080 = 0.870   # 🔴 lo Veo 1920x1080 co HAI ✦, cai trai bat dau x=1702 (0,886W) -> 0,905 cat khong toi (soi 1:1 2026-09-27)


def box(w, h, l, r, wm=WM):
    x0, x1 = l, int(round(l + (w - l - r) * wm))
    cw = x1 - x0; ch = int(round(cw * 9 / 16))
    if ch > h:                        # hiem: anh qua bet -> cat ngang them
        ch = h; cw = int(round(h * 16 / 9)); x1 = x0 + cw
    y0 = (h - ch) // 2
    return x0, y0, cw, ch


def do_img(src, dst):
    im = Image.open(src).convert("RGB"); a = np.asarray(im)
    l, r = bars([a])
    x0, y0, cw, ch = box(im.width, im.height, l, r)
    im.crop((x0, y0, x0 + cw, y0 + ch)).resize((1920, 1080), Image.LANCZOS).save(dst)
    return "anh %dx%d vien %d/%d -> cat %d:%d+%d+%d" % (im.width, im.height, l, r, cw, ch, x0, y0)


def frame(src, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True).stdout
    return np.asarray(Image.open(io.BytesIO(raw)).convert("RGB"))


def do_vid(src, dst):
    fs = [frame(src, t) for t in (0.5, 4.0, 7.5)]
    h, w = fs[0].shape[:2]
    l, r = bars(fs)
    x0, y0, cw, ch = box(w, h, l, r, WM_1080 if w >= 1920 else WM)
    vf = "crop=%d:%d:%d:%d,scale=1920:1080:flags=lanczos,setsar=1" % (cw, ch, x0, y0)
    p = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", vf, "-an", "-c:v", "libx264",
                        "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", str(dst)], capture_output=True, text=True)
    if p.returncode: raise RuntimeError(p.stderr[-300:])
    return "clip %dx%d vien %d/%d -> cat %d:%d+%d+%d" % (w, h, l, r, cw, ch, x0, y0)


def corners():
    """sheet: moi file 1 hang = 4 goc 1:1 (240x160), goc duoi-phai dat CUOI — noi ✦ hay o."""
    fs = sorted(OUT.glob("ai_*.*"))
    S = 240, 160
    sh = Image.new("RGB", (S[0] * 4 + 330, S[1] * len(fs)), "black")
    from PIL import ImageDraw
    d = ImageDraw.Draw(sh)
    for k, f in enumerate(fs):
        a = Image.fromarray(frame(f, 7.5)) if f.suffix == ".mp4" else Image.open(f).convert("RGB")
        W, H = a.size
        for c, (x, y) in enumerate(((0, 0), (W - S[0], 0), (0, H - S[1]), (W - S[0], H - S[1]))):
            sh.paste(a.crop((x, y, x + S[0], y + S[1])), (c * S[0], k * S[1]))
        d.text((S[0] * 4 + 6, k * S[1] + 6), f.name[:40], fill="yellow")
    sh.save(VD / "_review20" / "wm_corners_ai.jpg", quality=90)
    print("->", VD / "_review20" / "wm_corners_ai.jpg", len(fs), "file")


def main():
    sys.path.insert(0, str(Path(__file__).parent))
    idx = order()
    miss = sorted(set(idx) - set(MAP)); assert not miss, miss
    bad, todo = [], []
    for key, (img, vid) in MAP.items():
        stem = "ai_%02d_%s" % (idx[key], key)
        if not img and not vid:
            todo.append(key); continue
        for src, ext, fn in ((img, ".png", do_img), (vid, ".mp4", do_vid)):
            if not src: continue
            s = IN / src; dst = OUT / (stem + ext)
            if not s.exists(): bad.append((key, src)); continue
            if dst.exists() and dst.stat().st_mtime >= s.stat().st_mtime and dst.stat().st_mtime >= Path(__file__).stat().st_mtime:
                continue
            print("%-24s %s" % (stem + ext, fn(s, dst)))
    for stem, src in EXTRA.items():
        s_, d_ = IN / src, OUT / (stem + ".png")
        if not (d_.exists() and d_.stat().st_mtime >= max(s_.stat().st_mtime, Path(__file__).stat().st_mtime)):
            print("%-24s %s" % (stem + ".png", do_img(s_, d_)))
    print("\nda nhan: %d anh · %d clip" % (len(list(OUT.glob("*.png"))), len(list(OUT.glob("*.mp4")))))
    if todo: print("🔴 CAN GEN LAI:", todo)
    if bad: print("🔴 KHONG THAY FILE:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--corners" in sys.argv:
        corners(); sys.exit(0)
    sys.exit(main())
