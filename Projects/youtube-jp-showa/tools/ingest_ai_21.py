# -*- coding: utf-8 -*-
"""ingest_ai_21.py — nhan lo AI video 21 tu Downloads -> cells_in_ai/ai_NN_<key>.png|.mp4 da LAM SACH.

Lam sach (media-library.md §2.10 ⑤b ⑧): cat vien den (pillarbox, max-kenh <=12 tai 3 moc) -> CAT ✦ mep phai
o 0,905W -> trim 16:9 chia doi tren/duoi -> 1920x1080. Anh: PNG. Clip: giu fps goc (24), crf 16.
Ban goc giu o _ai_in/ (khong ghi de). Ghep canh <- file bang MAT (ten file Flow tu dat, khong tin ten).

    python tools/ingest_ai_21.py            # lam sach + in bao cao
    python tools/ingest_ai_21.py --corners  # sheet 1:1 goc duoi-phai + 3 goc con lai de soi ✦
"""
import sys, json, subprocess, io
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
import numpy as np

VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\21_umaredoshi-okane")
IN = VD / "_ai_in"; OUT = VD / "cells_in_ai"; OUT.mkdir(exist_ok=True)
WM = 0.905

# key -> (anh tinh, clip hoac None). Anh = anh goc cua clip neu co (cung khung).
MAP = {
 "siblings_tsucho": ('Tháng_9_29_-_10_36/Elderly_siblings_kneeling_at_table_20260929121251.jpg', None),
 "tsucho_pencil": ('_crops/i10_passbook_crop.jpg', None),
 "ane_silent": ('Tháng_9_29_-_14_27/Woman_looking_at_passbook_20260929143301.jpg', 'Tháng_9_29_-_14_27/Woman_reading_book_on_tatami_20260929143301.mp4'),
 "ane_confess": (None, 'Tháng_9_29_-_14_27/Woman_looking_at_page_20260929143301.mp4'),
 "ane_window": ('Tháng_9_29_-_10_36/Woman_sitting_by_window_20260929121251.jpg', None),
 "haha_iei": ('Tháng_9_29_-_12_13/Elderly_siblings_praying_at_altar_20260929141921.jpg', None),
 "tsucho_close": ('_crops/i12_passbook_crop.jpg', None),
 "coin_palm": ('Tháng_9_29_-_14_20/Woman_placing_coin_in_child_20260929142652.jpg', 'Tháng_9_29_-_14_20/Mother_and_daughter_exchanging_coin_20260929142652.mp4'),
 "coin_phoenix_macro": ('Tháng_9_29_-_10_36/Girl_turning_coin_under_light_20260929121251.jpg', None),
 "haha_young_speak": ('Tháng_9_29_-_10_36/Woman_kneeling_on_tatami_mat_20260929121251.jpg', None),
 "ane_futon_coin": ('Tháng_9_29_-_10_36/Girl_holding_coin_in_futon_20260929121252.jpg', None),
 "far_banknote": ('Tháng_9_29_-_10_36/Adult_paying_banknote_at_shop_20260929121251.jpg', None),
 "haha_young_smile": ('Tháng_9_29_-_10_36/Woman_in_kitchen_smiling_20260929121251.jpg', None),
 "haha_brush": ('Tháng_9_29_-_10_36/Woman_writing_at_table_20260929121251.jpg', None),
 "tailor_kyoto": ('Tháng_9_29_-_10_36/Man_sewing_at_machine_20260929121251.jpg', None),
 "kids_lottery": ('Tháng_9_29_-_10_36/Children_looking_at_New_Year_20260929121251.jpg', None),
 "haha_genkan_wait": ('Tháng_9_29_-_10_36/Woman_standing_in_doorway_20260929121251.jpg', None),
 "radio_wood": ('Tháng_9_29_-_10_36/Woman_kneeling_beside_radio_20260929121251.jpg', None),
 "radio_night": ('Tháng_9_29_-_14_20/Woman_and_girl_indoors_20260929142652.jpg', 'Tháng_9_29_-_14_20/Mother_and_daughter_inside_room_20260929142652.mp4'),
 "radio_back_glow": ('Tháng_9_29_-_10_36/Glowing_tube_radio_in_dark_20260929121251.jpg', None),
 "family_listen": ('Tháng_9_29_-_10_36/Woman_and_girl_listening_to_20260929121251.jpg', None),
 "radio_dial_close": ('Tháng_9_29_-_10_36/People_near_wooden_radio_20260929121251.jpg', None),
 "tv_color_1968": ('Tháng_9_29_-_10_36/People_in_Japanese_living_room_20260929121251.jpg', None),
 "haha_radio_quiet": ('Tháng_9_29_-_10_36/Tube_radio_on_tea_cabinet_20260929121251.jpg', None),
 "kakeibo_pencil": ('Tháng_9_29_-_10_36/Account_book_on_table_20260929121251.jpg', None),
 "tabakoya_call": ('Tháng_9_29_-_10_36/Woman_leaning_from_shop_window_20260929121251.jpg', None),
 "haha_run_sandal": ('Tháng_9_29_-_14_20/Woman_hurries_along_wooden_lane_20260929142652.jpg', 'Tháng_9_29_-_14_20/Woman_walks_along_lane_20260929142652.mp4'),
 "haha_decide": ('Tháng_9_29_-_10_36/Woman_kneeling_with_savings_bundle_20260929121252.jpg', None),
 "haha_count_savings": ('Tháng_9_29_-_10_36/Woman_untying_cloth_bundle_20260929121251.jpg', None),
 "kurodenwa_lace": ('Tháng_9_29_-_10_36/Rotary_telephone_on_wooden_cabinet_20260929121251.jpg', None),
 "haha_first_call": ('Tháng_9_29_-_14_32/Woman_holding_telephone_at_night_20260929143902.jpg', 'Tháng_9_29_-_14_32/Woman_making_phone_call_indoors_20260929143902.mp4'),
 "tsucho_interest": ('Tháng_9_29_-_10_36/Passbook_on_table_with_pencil_20260929121251.jpg', None),
 "haha_tsucho_drawer": ('Tháng_9_29_-_10_36/Woman_slides_passbook_into_drawer_20260929121251.jpg', None),
 "ane_goukaku": ('Tháng_9_29_-_14_27/Young_woman_standing_among_students_20260929143301.jpg', 'Tháng_9_29_-_14_27/Woman_covering_her_mouth_20260929143301.mp4'),
 "ryo_room": ('Tháng_9_29_-_10_36/Students_in_dormitory_room_20260929121251.jpg', None),
 "ryo_phone": ('Tháng_9_29_-_10_36/Woman_using_public_telephone_20260929121251.jpg', None),
 "univ_notice": ('Tháng_9_29_-_10_36/Students_walking_in_university_c…_20260929121251.jpg', None),
 "lecture_hall": ('Tháng_9_29_-_10_36/Students_in_university_lecture_hall_20260929121251.jpg', None),
 "yubin_window": ('Tháng_9_29_-_14_32/Woman_counting_banknotes_at_counter_20260929143902.jpg', 'Tháng_9_29_-_14_32/Clerk_stamping_slip_in_shop_20260929143902.mp4'),
 "ane_young_photo": ('Tháng_9_29_-_10_36/Woman_standing_near_university_gate_20260929121252.jpg', None),
 "private_univ": ('Tháng_9_29_-_10_36/Students_walking_at_university_b…_20260929121251.jpg', None),
 "siblings_night2": ('Tháng_9_29_-_12_13/Older_adults_examining_blank_pas…_20260929141921.jpg', None),
 "tsucho_pages": ('Tháng_9_29_-_12_13/Hands_turning_passbook_pages_20260929141921.jpg', None),
 "tsucho_rows": ('Tháng_9_29_-_12_13/Man_touching_blank_passbook_20260929141921.jpg', None),
 "tsucho_out1": ('Tháng_9_29_-_12_13/Woman_touching_blank_passbook_20260929141921.jpg', None),
 "tsucho_out2": ('Tháng_9_29_-_12_13/Man_touching_blank_passbook_20260929141921_2.jpg', None),
 "haha_bond_kept": ('Tháng_9_29_-_12_13/Woman_holding_certificate_in_drawer_20260929141921.jpg', None),
 "haha_phone_old": ('Tháng_9_29_-_12_13/Woman_holding_telephone_with_smile_20260929141921.jpg', None),
 "tsucho_first": ('Tháng_9_29_-_12_13/Passbook_and_photograph_on_table_20260929141921.jpg', None),
 "ane_handbag": ('Tháng_9_29_-_12_13/Woman_opening_paper_packet_indoors_20260929141921.jpg', None),
 "coin_unwrap": ('Tháng_9_29_-_14_32/Woman_unfolding_paper_with_coin_20260929143902.jpg', 'Tháng_9_29_-_14_32/Woman_opening_paper_with_coin_20260929143902.mp4'),
 "ane_tears": ('Tháng_9_29_-_12_13/Woman_looking_down_at_night_20260929141921.jpg', None),
 "coin_on_tsucho": ('Tháng_9_29_-_14_32/Woman_holding_coin_over_passbook_20260929143902.jpg', 'Tháng_9_29_-_14_32/Woman_places_coin_on_page_20260929143902.mp4'),
 "ane_smile": ('Tháng_9_29_-_12_13/Woman_sitting_at_table_smiling_20260929141921.jpg', None),
 "siblings_back": ('Tháng_9_29_-_10_36/Buddhist_altar_with_portrait_pho…_20260929121251.jpg', None),
 "table_bg": (None, None),
 "table_bg_b": (None, None),
 "table_bg_c": (None, None),
 "tsucho_coin_light": (None, None),
}
# anh DU cua user dung lam o THU HAI de chẻ khe clip AI qua tran 9,6s (ten file co dinh, khong theo thu tu S)
EXTRA = {
}
# ghi so CO Y KHONG DUNG (ai-video-regen.md §1: ghi ca thu da nhan lan thu bo)
UNUSED = {
 "v00-v05 (Woman_telling_story / Storyteller)": "HOAT HINH nen hong — nham kenh yawa, khong phai showa",
 "i09": "ban thay the tailor (co bien 仕立 AI ve)",
 "i14 i15 i16": "khong khop prompt nao",
}


def order():
    import gen_realism_21 as R
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
    sh.save(VD / "_review21" / "wm_corners_ai.jpg", quality=90)
    print("->", VD / "_review21" / "wm_corners_ai.jpg", len(fs), "file")


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
