# -*- coding: utf-8 -*-
r"""cutout_sticker25.py — cắt nền MAGENTA lô sticker video 25 → 06_VIDEO/25_*/sticker/el_*.png

Chép cơ chế `youtube-jp-nenkin/tools/cutout_sticker.py` (đã đo trên 15 sticker nenkin-17):
 ① tách theo KHOẢNG CÁCH MÀU tới magenta (không ngưỡng sáng)
 ② 🔴 loại pixel NGẢ magenta theo màu (R−G>34 và B−G>34) rồi erode 1px — erode hình học một
    mình để lại tới 21.573px viền tím (đo nenkin)
 ③ giữ BLOB LỚN NHẤT (loại ✦ watermark trắng nhạt)
 ④ nghiệm thu: đếm pixel alpha>250 mà ngả magenta (KHÔNG đếm alpha bán trong suốt — phép đo
    đó từng báo sạch 15/15 trong khi mắt thấy tím), + dán lên nền giấy → sheet

🔴 Ghép tên: generator đặt tên theo NỘI DUNG ảnh, không theo SPEC ⇒ MAP tiền tố → tên đích,
   điền TAY sau khi `ls` folder gen (đối chiếu bằng mắt). Ảnh không khớp MAP → in ra, bỏ qua.

CHẠY:  python tools/cutout_sticker25.py --src "C:\Users\tuana\Downloads\<folder>" [--apply]
"""
import sys
from pathlib import Path

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
STEM = "25_mizugame-suyaki-tarai"

# tiền tố tên file generator (đủ dài để duy nhất) → tên đích. ĐIỀN SAU KHI XEM FOLDER GEN.
MAP = {   # lô Downloads/download (8), 2026-08-28
    "Damp_white_hand_towel":          "el_taoru.png",
    "Folded_newspaper":               "el_newspaper.png",
    "Grandmother_speaking":           "cast_haha_talk.png",
    "Grandmother_standing_listening": "cast_haha_back.png",
    "Green_tea_cup":                  "el_teacup.png",
    "Japanese_uchiwa":                "el_uchiwa.png",
    "Man_pointing":                   "cast_kataribe_point.png",
    "Man_scratching":                 "cast_kataribe_wry.png",
    "Man_talking_warmly":             "cast_kataribe_talk.png",
    "Mosquito_coil":                  "el_katorisenko.png",
    "Old_glass_mercury":              "el_ondokei.png",
    "Red_comic_starburst":            "el_burst_red.png",
    "Retro_electric_desk_fan":        "el_senpuuki.png",
    "Showa-era_refrigerator":         "el_reizouko.png",
    "Stack_of_Japanese_coins":        "el_coin_stack.png",
    "Terracotta_flowerpot":           "el_uekibachi.png",
    "Terracotta_water_jar":           "el_mizugame.png",
    "Torn_desk_calendar":             "el_calendar.png",
    "Two_eggplants":                  "el_nasu.png",
    "Vapour_wisps":                   "el_yuge.png",
    "Water_drops":                    "el_mizu_shizuku.png",
    "Water_pouring_from_kitchen_tap": "el_jaguchi.png",
    "Wooden_washtub":                 "el_tarai.png",
    # lô download (10) — 28 sticker (41 file còn lại là hero gen lại, bỏ qua)
    "Crescent_moon":        "el_tsuki_yoru.png",   "Wooden_ladle":         "el_hishaku.png",
    "Bottle_of_Japanese_barley": "el_mugicha.png", "Glass_of_cold_water":  "el_koppu.png",
    "Wooden_wall_clock":    "el_tokei.png",        "Folded_white_kitchen_apron": "el_kappogi.png",
    "Indigo_furoshiki":     "el_furoshiki.png",    "Magnifying_glass":     "el_kakudai.png",
    "Bowl_of_ice_water":    "el_koorimizu.png",    "Laboratory_flask":     "el_flask.png",
    "Water_bottle_standing": "el_bottle.png",      "Wet_cloth_hanging":    "el_nureta_nuno.png",
    "Elderly_hand_pointing": "el_yubi.png",        "Question_mark":        "el_hatena.png",
    "Wind_lines":           "el_kaze.png",         "Blank_price_tag":      "el_nefuda.png",
    "Cartoon_sun":          "el_taiyou.png",       "Rain_cloud":           "el_amagumo.png",
    "Clay_pots_in_cut-away": "el_tsubo_nijuu.png", "Tomatoes_in_pile":     "el_tomato.png",
    "Gold_medal":           "el_medal.png",        "Camping_lantern":      "el_lantern.png",
    "Cooler_box":           "el_cooler.png",       "Japanese_ambulance":   "el_kyukyusha.png",
    "Water_splashing_on_hand": "el_te_no_kou.png", "Air-conditioner_remote": "el_remocon.png",
    "Unplugged_power_plug": "el_plug_off.png",     "Sand_on_wooden_scoop": "el_suna.png",
    # lô download (11) — 50 sticker
    "Ceramic_vase":         "el_tsubo_tsuya.png",  "Cluster_of_sparkle":   "el_kirakira.png",
    "Pottery_kiln":         "el_kama.png",         "Ceramic_tanuki":       "el_tanuki.png",
    "Clay_flask":           "el_tokkuri.png",      "Old_stone_well":       "el_ido.png",
    "Warning_sign":         "el_keihou.png",       "Wind_chime":           "el_furin.png",
    "Sweat_drops":          "el_ase.png",          "Bamboo_ladle_holding": "el_take_hishaku.png",
    "Red_cross_mark":       "el_batsu.png",        "First-aid_box":        "el_kyukyu_bako.png",
    "Damp_rolled_white_towel": "el_kubi_taoru.png", "Farming_hoe":         "el_kuwa.png",
    "Persimmon_branch":     "el_kaki.png",         "Smartphone_illustration": "el_smartphone.png",
    "Japanese_ceramic_teapot": "el_kyuusu.png",    "Inflatable_children":  "el_pool.png",
    "Striped_inflatable_swim_ring": "el_ukiwa.png", "Showa-era_television": "el_terebi.png",
    "Washing_machine":      "el_sentakuki.png",    "Water_splashing_against": "el_shibuki.png",
    "Shinto_altar_shelf":   "el_kamidana.png",     "Water_pipe_illustration": "el_suidoukan.png",
    "Tin_bucket":           "el_baketsu.png",      "Folded_reading_glasses": "el_megane.png",
    "Indigo_floor_cushion": "el_zabuton.png",      "Sealed_envelope":      "el_fuutou.png",
    "Clay_water_jar_illustration": "el_kame_modern.png", "Brown_paper_shopping_bag": "el_fukuro.png",
    "Brass_balance_scale":  "el_tenbin.png",       "Electric_power_plug_in_socket": "el_plug.png",
    "Cracked_concrete_wall": "el_concrete.png",    "Heat_shimmer_lines":   "el_netsu.png",
    "Japanese_window":      "el_mado.png",         "Potted_garden_tree":   "el_niwaki.png",
    "Worn_leather_wallet":  "el_saifu.png",        "Five_small_stars":     "el_hoshi.png",
    "Paper_lantern_lamp":   "el_akari.png",
    "Straw_hat_illustration_202608280130_2": "el_mugiwara.png",   # mũ rơm vành (soi mắt)
    "Straw_hat_illustration_202608280130.":  "el_sugegasa.png",   # nón chóp 菅笠
    "Concentric_water_ripples": "el_hamon.png",    "Old_house_telephone":  "el_denwa.png",
    "Metal_bucket_filled_with_ice": "el_koori_bucket.png", "Paper_fan_folding": "el_sensu.png",
    "Cobweb_in_corner":     "el_kumonosu.png",     "Hydrangea_flower":     "el_dry_flower.png",
    "Frosty_ice_pack":      "el_horeizai.png",     "Old_Japanese_bicycle": "el_jitensha.png",
    "Hanging_indigo_patterned_tenugui": "el_tenugui.png",
}

TOL = 118.0
PAPER = (242, 237, 228)


def _imread(p):
    buf = np.fromfile(str(p), dtype=np.uint8)
    return cv2.imdecode(buf, cv2.IMREAD_COLOR)


def _imwrite(p, im):
    ok, buf = cv2.imencode(p.suffix, im)
    if ok:
        buf.tofile(str(p))
    return ok


def cutout(bgr):
    rgb = bgr[:, :, ::-1].astype(np.float32)
    dist = np.linalg.norm(rgb - np.array([255, 0, 255], np.float32), axis=2)
    mask = (dist > TOL).astype(np.uint8)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    tinted = (r - g > 34) & (b - g > 34)
    mask[tinted] = 0
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n > 1:
        big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        mask = (lab == big).astype(np.uint8)
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None, 0
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    out = np.dstack([bgr, (mask * 255).astype(np.uint8)])[y0:y1, x0:x1]
    # nghiệm thu ④
    o = out.astype(np.int32)
    solid = o[..., 3] > 250
    viol = int((solid & (o[..., 2] - o[..., 1] > 40) & (o[..., 0] - o[..., 1] > 40)).sum())
    return out, viol


def main():
    if "--src" not in sys.argv:
        print("dùng: python tools/cutout_sticker25.py --src <folder> [--apply]")
        return 1
    src = Path(sys.argv[sys.argv.index("--src") + 1])
    apply = "--apply" in sys.argv
    dst = PROJ / "06_VIDEO" / STEM / "sticker"
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
    # --order: ghép theo THỨ TỰ mtime ↔ TENFILE (extension gen đúng thứ tự FLOW) — dùng cho lô
    # 78 sticker lô 2, khỏi điền MAP 78 dòng. Kiểm bảng in ra bằng mắt trước --apply.
    order = {}
    if "--order" in sys.argv:
        ten = [l.split()[0] for l in (PROJ / "06_VIDEO" / STEM / "sticker_prompts_TENFILE.txt")
               .read_text(encoding="utf-8").splitlines() if l.strip()]
        byt = sorted(files, key=lambda q: q.stat().st_mtime)
        if len(byt) != len(ten):
            print(f"⚠ folder {len(byt)} ảnh ≠ TENFILE {len(ten)} — ghép {min(len(byt), len(ten))} cái đầu, SOI BẢNG")
        order = {q.name: t for q, t in zip(byt, ten)}
    done, un = 0, []
    tiles = []
    for p in files:
        tgt = order.get(p.name) or next((v for k, v in MAP.items() if p.name.startswith(k)), None)
        if not tgt:
            un.append(p.name)
            continue
        im = _imread(p)
        if im is None:
            print(f"🔴 đọc không được {p.name}")
            continue
        out, viol = cutout(im)
        if out is None:
            print(f"🔴 {p.name}: không tách được (nền không phải magenta?)")
            continue
        flag = "⚠ TÍM" if viol > 50 else "ok"
        print(f"   {'✓' if apply else '·'} {tgt:<22} {out.shape[1]}×{out.shape[0]}  tím={viol:<5} {flag}  ← {p.name[:48]}")
        if apply:
            # cast_*.png → 06_VIDEO/25/cast/<tên không tiền tố>.png (builder đọc ở đó)
            if tgt.startswith("cast_"):
                cd = dst.parent / "cast"
                cd.mkdir(exist_ok=True)
                _imwrite(cd / tgt[5:], out)
            else:
                _imwrite(dst / tgt, out)
            done += 1
        tiles.append((tgt, out))
    if un:
        print(f"\n⚠ {len(un)} ảnh không khớp MAP (điền MAP rồi chạy lại):")
        for u in un:
            print(f"     {u}")
    if tiles:      # sheet nghiệm thu trên nền giấy
        h = 260
        cols = []
        for _, o in tiles:
            s = h / o.shape[0]
            r = cv2.resize(o, (max(1, int(o.shape[1] * s)), h))
            bg = np.full((h, r.shape[1], 3), PAPER[::-1], np.uint8)
            a = r[..., 3:4].astype(np.float32) / 255
            comp = (r[..., :3] * a + bg * (1 - a)).astype(np.uint8)
            cols.append(comp)
        sheet = np.hstack(cols)
        _imwrite(dst / "_sticker_sheet.jpg", sheet)
        print(f"[SHEET] {dst / '_sticker_sheet.jpg'}")
    print(f"\n{'✓ ghi' if apply else '· xem trước'} {done if apply else len(tiles)} sticker → {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
