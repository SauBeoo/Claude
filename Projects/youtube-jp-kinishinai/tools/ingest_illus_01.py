# -*- coding: utf-8 -*-
"""ingest_illus_01.py — nap 74 anh MINH HOA 絵本 (lo zip 14_01) vao slides_img/slide_NN.png.

- MAP: slide -> file (khop bang mat tren sheet 2026-10-02; ten file do Flow dat, khong theo thu tu)
- Cat ✦ (lo 1376x768: ~0,928W/0,878H) + bo MANG TRANG TRONG: model hieu "chua goc duoi-phai trong" thanh ve mot
  khoi trang phang (23/74 anh bi). Tim khung 16:9 LON NHAT (dich + thu nho toi 0,62) sao cho:
    ① khong chua vung ✦ (x > 0,905W va y > 0,86H)   ② vung "trang phang" (sang > 238 va gradient thap) <= 1,5%
  roi phong len 1920x1080 (Lanczos). Khong tim duoc -> bao LOI (gen lai), khong nap.
- HOLD: slide khong co anh rieng -> giu anh slide ke truoc (thanh mot canh dai, khong lap anh khac cho).
Xuat sheet duyet _plan/_illus_sheet_*.jpg + bao cao ti le cat moi anh.
Chay: python tools/ingest_illus_01.py 01_kuchiguse-hitonome
"""
import sys, io, json
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
BATCH = "_user_raw/illus_1401"
MAP = {
    0: "Woman_bowing_at_post_office", 1: "Woman_lying_awake_in_futon", 2: "Woman_sitting_in_futon",
    5: "Watchman_glowing_lantern_in_room", 6: "Woman_bows_and_serves_tea", 8: "Two_women_sitting_at_table",
    9: "Family_gathering_around_kotatsu_20261002221851.jpg", 12: "Man_returning_glove_to_woman",
    13: "Woman_at_kimono_counter", 14: "Woman_folding_gift-wrap_on_table", 15: "Woman_bows_to_customer",
    16: "Hand_writing_thank-you_letter", 17: "Watchman_casting_shadow_in_room", 18: "Man_holding_door_open_outdoors",
    21: "Boy_offering_bus_seat", 22: "Woman_holding_anpan_bun", 23: "People_crossing_Japanese_city_st",
    25: "Woman_walking_in_shopping_arcade_20261002221851.jpg", 26: "Eyeglasses_beside_mirror_on_table",
    27: "People_in_university_corridor", 28: "Student_walking_into_classroom", 30: "Woman_walking_past_shop_windows",
    32: "Woman_walking_in_shopping_arcade_20261002221851_2", 34: "Neighbours_chat_in_courtyard",
    36: "Residents_raise_hands_together", 37: "Housewives_chatting_in_courtyard", 40: "People_raising_hands_in_meeting",
    41: "Residents_disagreeing_in_communi", 42: "Woman_smiling_at_community_gathe", 44: "Woman_attending_community_meeting",
    45: "Two_women_whispering_at_door", 46: "Two_women_laughing_over_coffee", 48: "Woman_walks_on_city_street",
    49: "People_in_tatami_room_20261002221851.jpg", 50: "Two_strangers_chat_on_bench", 52: "People_on_park_path",
    53: "Woman_talking_on_phone", 55: "Woman_laughing_on_phone", 56: "Two_women_walking_autumn_path",
    57: "Older_woman_standing_at_window", 60: "Woman_holding_hands_in_lap", 61: "Women_talking_on_park_bench",
    65: "People_at_polite_tea_gathering", 67: "Woman_on_phone_in_room", 68: "Woman_wiping_tears_in_kitchen",
    70: "Woman_looking_at_mirror_reflection", 72: "Woman_holding_flyer_outside_buil", 73: "Teenage_girl_before_elders",
    74: "Older_couple_walks_autumn_park", 76: "Closed_boxes_on_shelf", 78: "Woman_waiting_on_railway_platform",
    79: "Woman_walking_on_path", 82: "Woman_holding_cup_in_kitchen", 83: "Family_arguing_at_dinner_table",
    84: "Mother_enduring_at_table", 85: "People_sitting_in_study_room", 86: "Woman_keeping_blank_face",
    87: "Woman_glancing_toward_kitchen", 91: "Two_women_laughing_at_kitchen", 93: "Family_gathering_in_Japanese_home",
    94: "Woman_ladling_ozoni_in_kitchen", 95: "Mother_standing_for_family_photos", 96: "Woman_turning_toward_kitchen_sink",
    97: "People_in_tatami_room_20261002221851_2", 99: "Woman_unties_apron_under_kotatsu", 100: "Boy_staring_at_grandmother",
    101: "Family_laughing_around_kotatsu", 103: "Woman_at_kotatsu_in_home", 105: "Two_women_turning_album_pages",
    106: "Watchman_resting_in_tatami_room", 108: "Family_gathering_around_kotatsu_20261002221851_2",
    110: "Green_tea_by_sunny_window",
}
HOLD = {59: 60, 62: 61}       # slide -> slide co anh (mot canh dai)
# khung ep tay (ti le W/H) — mang trong co van giay ma may khong bat (soi mat 2026-10-02): 83 = anh GHEP 2 o, 94 = dai trang phai
FORCE = {83: (0.0, 0.12, 0.70, None), 94: (0.0, 0.10, 0.80, None)}
UNUSED_OK = {"Woman_on_phone_in_home", "Woman_sitting_in_home"}


def blank_mask(rgb):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    grad = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
    grad = cv2.blur(grad, (15, 15))
    # chi MANG TRANG "chua cho": gan trang tuyet doi + phang tuyet doi + LIEN KHOI cham mep phai/day + >= 1,5% anh.
    # Ban dau (>238, grad<6) bat ca tuong/giay/troi sang -> 7 anh "khong cat duoc", 29 anh cat qua sau.
    # Mang trong co khi la KEM (~230-240) co van giay nhe -> do do PHANG bang do lech chuan cuc bo, khong bang do sang.
    mu = cv2.blur(g, (21, 21)); sd = np.sqrt(np.maximum(cv2.blur(g * g, (21, 21)) - mu * mu, 0))
    raw = ((g > 212) & (grad < 5) & (sd < 3.0)).astype(np.uint8)
    raw = cv2.morphologyEx(raw, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(raw, connectivity=8)
    H, W = g.shape
    keep = np.zeros_like(raw, bool)
    for k in range(1, n):
        x, y, w, h, a = st[k]
        if a >= 0.006 * H * W and (x + w >= W - 3 or y + h >= H - 3):
            keep |= lab == k
    return keep


def best_crop(rgb):
    H, W = rgb.shape[:2]
    m = blank_mask(rgb).astype(np.float32)
    ii = cv2.integral(m)
    def frac(x0, y0, x1, y1):
        return (ii[y1, x1] - ii[y0, x1] - ii[y1, x0] + ii[y0, x0]) / ((x1 - x0) * (y1 - y0))
    for s in np.arange(0.905, 0.60, -0.015):
        w = int(W * s); h = int(round(w * 9 / 16))
        if h > H:
            h = H; w = int(round(h * 16 / 9))
        best = None
        for y0 in range(0, H - h + 1, 8):
            for x0 in range(0, W - w + 1, 8):
                x1, y1 = x0 + w, y0 + h
                if x1 > 0.905 * W and y1 > 0.86 * H:       # chua vung ✦
                    continue
                fr = frac(x0, y0, x1, y1)
                if fr <= 0.002 and (best is None or fr < best[0]):
                    best = (fr, x0, y0, x1, y1)
        if best:
            return s, best
    return None, None


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    files = sorted((vd / BATCH).rglob("*.jpg"))
    out = vd / "slides_img"
    bk = vd / "slides_img_photo_bak"; bk.mkdir(exist_ok=True)
    used, rep, bad = set(), [], []
    for slot, pref in sorted(MAP.items()):
        hit = [f for f in files if f.name.startswith(pref) or f.name == pref]
        assert len(hit) == 1, f"slide {slot}: 「{pref}」 khop {len(hit)}"
        f = hit[0]; assert f.name not in used, f"{f.name} dung 2 lan"; used.add(f.name)
        rgb = np.asarray(Image.open(f).convert("RGB"))
        if slot in FORCE:
            Hh, Ww = rgb.shape[:2]; fx0, fy0, fx1, _ = FORCE[slot]
            x0, x1 = int(fx0 * Ww), int(fx1 * Ww); h = int(round((x1 - x0) * 9 / 16)); y0 = min(int(fy0 * Hh), Hh - h)
            s, b = (fx1 - fx0), (0.0, x0, y0, x1, y0 + h)
        else:
            s, b = best_crop(rgb)
        if not b:
            bad.append((slot, f.name)); continue
        _, x0, y0, x1, y1 = b
        dst = out / f"slide_{slot:02d}.png"
        if dst.exists() and not (bk / dst.name).exists():
            dst.replace(bk / dst.name)                    # giu ban anh nguoi that cu
        Image.fromarray(rgb[y0:y1, x0:x1]).resize((1920, 1080), Image.LANCZOS).save(dst)
        rep.append((slot, round(s, 3), f.name[:38]))
    for a, b in HOLD.items():
        Image.open(out / f"slide_{b:02d}.png").save(out / f"slide_{a:02d}.png")
    left = [f.name for f in files if f.name not in used and not any(f.name.startswith(u) for u in UNUSED_OK)]
    tight = [r for r in rep if r[1] < 0.80]
    print(f"nap {len(rep)} anh · HOLD {HOLD} · loi {bad} · chua dung (ngoai du kien) {left}")
    print("cat sau (< 0,80 khung):", tight)
    tw, th, c = 384, 216, 6
    items = sorted(list(MAP) + list(HOLD))
    for k in range(0, len(items), 42):
        part = items[k:k + 42]
        sh = Image.new("RGB", (tw * c, th * ((len(part) + c - 1) // c)), "white"); d = ImageDraw.Draw(sh)
        for j, i in enumerate(part):
            x, y = (j % c) * tw, (j // c) * th
            sh.paste(Image.open(out / f"slide_{i:02d}.png").resize((tw, th)), (x, y))
            d.rectangle([x, y, x + 40, y + 18], fill="black"); d.text((x + 3, y + 3), str(i), fill="yellow")
        sh.save(vd / "_plan" / f"_illus_sheet_{k // 42}.jpg", quality=85)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
