# -*- coding: utf-8 -*-
"""ingest_ai_22.py — nhan lo AI video 22 tu Downloads -> cells_in_ai/ai_NN_<key>.png|.mp4 da LAM SACH.

Lam sach (media-library.md §2.10 ⑤b ⑧): cat vien den (pillarbox, max-kenh <=12 tai 3 moc) -> CAT ✦ mep phai
o 0,905W -> trim 16:9 chia doi tren/duoi -> 1920x1080. Anh: PNG. Clip: giu fps goc (24), crf 16.
Ban goc giu o _ai_in/ (khong ghi de). Ghep canh <- file bang MAT (ten file Flow tu dat, khong tin ten).

    python tools/ingest_ai_22.py            # lam sach + in bao cao
    python tools/ingest_ai_22.py --corners  # sheet 1:1 goc duoi-phai + 3 goc con lai de soi ✦
"""
import sys, json, subprocess, io
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
import numpy as np

VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\22_kieta-shigoto")
IN = VD / "_ai_in"; OUT = VD / "cells_in_ai"; OUT.mkdir(exist_ok=True)
WM = 0.905

# key -> (anh tinh, clip hoac None). Anh = anh goc cua clip neu co (cung khung).
# key -> (anh tinh, clip hoac None). Ghep bang MAT tren _review22/ai_in_*.jpg (2026-10-04).
MAP = {
 'conductor_young': ('Tháng_10_04_-_17_58/Girl_standing_by_bus_20261004182241.jpg', None),
 'bag_coins': ('Tháng_10_04_-_17_58/Girl_wearing_coin_bag_20261004182241.jpg', None),
 'envelope_father': ('Tháng_10_04_-_17_47/Girl_offering_envelope_to_father_20261004175222.jpg', 'Tháng_10_04_-_17_47/Woman_handing_envelope_to_man_20261004175223.mp4'),
 'haha77_bus': ('Tháng_10_04_-_17_47/Woman_sitting_on_bus_20261004175222.jpg', 'Tháng_10_04_-_17_47/Woman_looking_out_window_20261004175223.mp4'),
 'envelope_drawer': ('Tháng_10_04_-_17_58/Open_drawer_in_dark_hut_20261004182241.jpg', None),
 'depot_rollcall': ('Tháng_10_04_-_17_58/Bus_conductors_standing_at_dawn_20261004182241.jpg', None),
 'conductor_lean': ('Tháng_10_04_-_17_47/Girl_calling_from_bus_20261004175222.jpg', 'Tháng_10_04_-_17_47/Woman_waves_as_bus_departs_20261004175223.mp4'),
 'fingers_cracked': ('Tháng_10_04_-_17_58/Girl_sorting_coins_20261004182240.jpg', None),
 'count_sales': ('Tháng_10_04_-_17_58/Girl_counting_coins_at_table_20261004182240.jpg', None),
 'conductor_last_day': ('Tháng_10_04_-_17_58/Young_woman_holding_cap_20261004182241.jpg', None),
 'sofu_keeper': ('Tháng_10_04_-_17_58/Man_holding_flag_at_crossing_20261004182240.jpg', None),
 'sofu_handle': ('Tháng_10_04_-_17_47/Man_turning_railway_barrier_crank_20261004175222.jpg', 'Tháng_10_04_-_17_47/Man_lowering_barrier_arm_20261004175223.mp4'),
 'girl_bento_hut': ('Tháng_10_04_-_17_58/Girl_walking_along_railway_20261004182241.jpg', None),
 'flag_ignored': ('Tháng_10_04_-_17_58/Man_holding_signal_flag_20261004182241.jpg', None),
 'miners_walk': ('Tháng_10_04_-_17_47/Japanese_coal_miners_walking_20261004175222.jpg', 'Tháng_10_04_-_17_47/Men_walking_towards_mine_20261004175223.mp4'),
 'miner_black_face': ('Tháng_10_04_-_17_58/Coal_miner_standing_outside_pithead_20261004182241.jpg', None),
 'boy_sentan': ('Tháng_10_04_-_17_58/Boy_sorting_coal_in_shed_20261004182240.jpg', None),
 'father_bus_morning': ('Tháng_10_04_-_17_58/Man_waiting_at_bus_stop_20261004182241.jpg', None),
 'coins_ready_palm': ('Tháng_10_04_-_17_58/Man_holding_coins_for_bus_20261004182241.jpg', None),
 'conductor_smile': ('add_1004/Young_woman_on_bus_2K_20261004194314.jpg', None),
 'haha_switchboard': ('Tháng_10_04_-_17_52/Woman_operating_manual_switchboard_20261004175743.jpg', 'Tháng_10_04_-_17_52/Woman_lifts_cord_from_shelf_20261004175743.mp4'),
 'headset_on': ('Tháng_10_04_-_17_58/Woman_using_telephone_switchboard_20261004182241.jpg', None),
 'plug_in': ('Tháng_10_04_-_17_52/Woman_operating_telephone_switch…_20261004175743.jpg', 'Tháng_10_04_-_17_52/Person_plugging_in_lamp_20261004175743.mp4'),
 'operators_row': ('Tháng_10_04_-_17_58/Women_operating_manual_switchboard_20261004182240.jpg', None),
 'dekasegi_phone': ('Tháng_10_04_-_17_58/Labourer_using_public_telephone_20261004182241.jpg', None),
 'haha_listen': ('Tháng_10_04_-_17_58/Woman_operating_switchboard_at_n…_20261004182241.jpg', None),
 'operators_reassigned': ('add_1004/Women_listening_to_man_in_2K_20261004193647.jpg', None),
 'headset_stain': ('Tháng_10_04_-_17_58/Women_operating_manual_telephone…_20261004182241.jpg', None),
 'haha_typist': ('Tháng_10_04_-_17_58/Woman_using_Japanese_typewriter_20261004182241.jpg', None),
 'haha_rub_arm': ('Tháng_10_04_-_17_58/Woman_rubbing_arm_beside_child_20261004182241.jpg', None),
 'wordpro_desk': ('Tháng_10_04_-_17_58/Office_machine_in_1970s_office_20261004182241.jpg', None),
 'wordpro_price': ('Tháng_10_04_-_17_58/Office_desk_with_covered_typewriter_20261004182241.jpg', None),
 'haha_wordpro': ('Tháng_10_04_-_17_58/Woman_typing_at_office_keyboard_20261004182241.jpg', None),
 'envelope_drawer2': ('Tháng_10_04_-_17_58/Keeper_inside_hut_at_night_20261004182241.jpg', None),
 'electric_barrier': ('Tháng_10_04_-_17_58/Level-crossing_barrier_at_night_20261004182240.jpg', None),
 'haha_bento_night': ('Tháng_10_04_-_17_58/Woman_walking_along_railway_20261004182241.jpg', None),
 'envelope_reveal': ('Tháng_10_04_-_17_52/Man_holding_pay_envelope_20261004175743.jpg', 'Tháng_10_04_-_17_52/Man_lifting_envelope_from_drawer_20261004175743.mp4'),
 'envelope_sealed': ('Tháng_10_04_-_17_58/Hands_holding_paper_pay_envelope_20261004182241.jpg', None),
 'sofu_hand_over': ('Tháng_10_04_-_17_52/Man_handing_envelope_to_woman_20261004175743.jpg', 'Tháng_10_04_-_17_52/Man_places_envelope_in_hands_20261004175743.mp4'),
 'barrier_auto_night': ('Tháng_10_04_-_17_58/Level_crossing_barrier_lowering_20261004182241.jpg', None),
 'haha_cry_hut': ('Tháng_10_04_-_17_52/Woman_holding_envelope_crying_20261004175743.jpg', 'Tháng_10_04_-_17_52/Woman_crying_over_envelope_20261004175743.mp4'),
 'haha77_bus2': ('Tháng_10_04_-_17_58/Woman_riding_bus_smiling_20261004182241.jpg', None),
 'envelope_bag': ('Tháng_10_04_-_17_58/Woman_holding_handbag_on_bus_20261004182241.jpg', None),
 'haha77_smile': ('Tháng_10_04_-_17_58/Elderly_woman_smiling_on_bus_20261004182241.jpg', None),
 'envelope_old_hands': ('Tháng_10_04_-_17_58/Hands_holding_paper_pay_envelope_20261004182241_2.jpg', None),
}
EXTRA = {
}
UNUSED = {
 "Man_using_public_telephone_20261004182240.jpg": "ban thu hai cua dekasegi_phone (chon Labourer_... vi dung prompt hon)",
 "People_listening_in_office_20261004182240.jpg": "ban dau cua operators_reassigned, thay bang ban 2K cam headset (user gen lai 2026-10-04)",
}


def order():
    import gen_realism_22 as R
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
    sh.save(VD / "_review22" / "wm_corners_ai.jpg", quality=90)
    print("->", VD / "_review22" / "wm_corners_ai.jpg", len(fs), "file")


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
