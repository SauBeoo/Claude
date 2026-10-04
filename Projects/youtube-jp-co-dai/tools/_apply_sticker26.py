# -*- coding: utf-8 -*-
"""Ghép ảnh sticker video 26 theo NỘI DUNG tên file (generator đặt tên tự do)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cutout_sticker26 as C  # noqa: E402
import sticker_prompts_collage26 as S  # noqa: E402

SRC = Path(r"C:\Users\tuana\Downloads\download")

MAP = {
    "Blank_official_certificate_sticker": "el_hyou_shou",
    "Blank_price_tag_sticker":            "el_nefuda_shiro",
    "Blank_tag_glowing_anime_style":      "el_muryou_fuda",
    "Blue_arrow_pointing_downward":       "el_yajirushi_ao",
    "Brass_balance_scale_illustration":   "el_tenbin_kami_garasu",
    "Brass_door_lock_illustration":       "el_kagi",
    "Breeze_lines_anime_illustration":    "el_kaze_samu",
    "Cartoon_sun_sticker":                "el_taiyou_ya",
    "Cat_walking_away":                   "el_neko_sakeru",
    "Ceramic_teapot_illustration":        "el_kyuusu_cha",
    "Child_finger_poking_through_paper":  "el_yubi_ana",
    "Circular_ring_symbolising_harmony":  "el_wa",
    "Closed_wooden_shutter_panel":        "el_amado",
    "Clothes_iron_standing_upright":      "el_airon",
    "Crescent_moon_and_stars_sticker":    "el_tsuki_shime",
    "Crescent_smile_sticker_on_magenta":  "el_hohoemi",
    "Cutter_knife_illustration":          "el_kattaa2",
    "Cutter_knife_with_new_blade":        "el_kattaa_ha",
    "Damp_towel_illustration":            "el_taoru_nure",
    "Detergent_bottle_illustration":      "el_senzai_bin",
    "Double_pane_window_diagram":         "el_uchimado_zu",
    "Dust_cloud_sticker_design":          "el_hokori",
    "Dusty_cobweb_in_corner":             "el_kumo_no_su",
    "Elderly_couple_silhouette_sticker":  "el_sofubo_kage",
    "Elderly_hand_pointing_downward":     "el_yubi_sasu",
    "Falling_line_graph_sticker":         "el_gurafu_ochiru",
    "Finger_touching_wooden_surface":     "el_yubisaki",
    "Folded_fabric_curtain_swatch_sti":   "el_kaaten_nunoji",
    "Glass_spray_bottle_illustration":    "el_kirifuki_bin",
    "Gleaming_light_band_sticker":        "el_kuuki_sou",
    "Glow_question_mark_illustration":    "el_hatena_ai",
    "Glowing_paper_rectangle_on_magenta": "el_pin_to",
    "Glowing_threads_sticker_design":     "el_senni_kirakira",
    "Golden_sparkle_stars_sticker":       "el_hoshi_kagayaki",
    "Hand_holding_paste_brush":           "el_shokunin_te",
    "Hand_lifting_screen_panel":          "el_te_kakeru",
    "Handheld_vacuum_cleaner_nozzle_i":   "el_souji_ki",
    "Hygrometer_dial_sticker_illustra":   "el_shitsudokei",
    "Illustrated_speech_bubble_sticker":  "el_toho_kao",
    "Japanese_noren_doorway_curtain_i":   "el_noren",
    "Knitted_socks_folded_together":      "el_kutsushita",
    "Light_glowing_through_paper_silh":   "el_yuuhi_kage",
    "Magnifying_glass_illustration_202608310110.jpeg": "el_mushimegane",
    "Magnifying_glass_illustration_202608310110_2.jpeg": "el_kensabikyou",
    "Mould_spots_on_wooden_surface":      "el_shimi_ten",
    "Orange_heat-shimmer_lines_rising":   "el_atatakai_kuuki",
    "Pale_mist_wisps_curling":            "el_iki_moya",
    "Paper_held_up_to_light":             "el_hikari_kazashi",
    "Paper_lantern_on_wooden_stand":      "el_andon_akari",
    "Paper_screen_anime_illustration":    "el_kansou_kage",
    "Paper_sticker_on_magenta_background": "el_kouyoku_kami",
    "Paste_brush_illustration":           "el_nori_bake",
    "Photo-frame_sticker_on_magenta_b":   "el_omoide_frame",
    "Potted_garden_tree_illustration":    "el_niwaki",
    "Question_mark_illustration_202608310110.jpeg": "el_hatena_dai",
    "Question_mark_speech_bubble_illu":   "el_toikake_kumo",
    "Question_mark_sticker_on_magenta":   "el_hatena_shiro",
    "Rolled_handmade_washi_paper_bundle": "el_washi_maki",
    "Rolled_plastic_curtain_sticker_i":   "el_juushi_curtain",
    "Rolled_plastic_sheet_illustration":  "el_purasuchikku_maki",
    "Sealed_white_envelope_illustration": "el_fuutou_kuni",
    "Shoji_screen_panel_sticker":         "el_shouji_koma",
    "Shoji_screen_sticker":               "el_shouji_ura",
    "Shopping_basket_with_paper_roll":    "el_daiso_kago",
    "Sleeping_cat_illustration":          "el_neko_marumaru",
    "Small_wooden_toolbox_illustration":  "el_dougu_bako",
    "Smartphone_sticker_on_magenta_ba":   "el_smartphone_ai",
    "Smiling_face_sticker":               "el_warau_haha",
    "Snow-covered_window_ledge_illust":   "el_yuki_mado",
    "Sparkle_shapes_sticker_on_magenta":  "el_kagayaki",
    "Speech_bubble_sticker_on_magenta":   "el_comment_fukidashi",
    "Spray_bottle_illustration":          "el_kirifuki",
    "Sun_setting_on_solid_background":    "el_taiyou_nishi",
    "Sword_resting_on_wooden_stand":      "el_bushi_katana",
    "Taiko_drum_skin_surface":            "el_taiko_kawa",
    "Thermometer_sticker_on_magenta_b":   "el_ondokei",
    "Tool_belt_with_tools":               "el_kouji_gyousha",
    "Translucent_mist_swirl_illustration": "el_kaisou_moya",
    "Two_hands_holding_delicate_object":  "el_te_yasashiku",
    "Two_panes_of_glass_glowing":         "el_garasu_nimai",
    "Vapour_drifting_sideways_illustr":   "el_shitsuke_moya",
    "Washi_paper_glowing_warmly_202608310110.jpeg": "el_kami_kagayaki",
    "Washi_paper_glowing_warmly_202608310110_2.jpeg": "el_kami_hikari2",
    "Washi_paper_sticker_on_magenta":     "el_kami_ichimai",
    "Water_droplets_trickling_down_su":   "el_suiteki_retsu",
    "White_candle_on_magenta_background": "el_rousoku",
    "Window_pane_cross-section_diagram":  "el_mado_danmen",
    "Window_with_airflow_illustration":   "el_kanki_mado",
    "Windowsill_sticker_on_magenta_ba":   "el_kansou_mado",
    "Wooden_lattice_frame_illustration":  "el_kumiko_ryoumen",
    "Wooden_sliding_door_illustration":   "el_toji_mon",
    "Wooden_window_frame_illustration":   "el_mado_kanki",
}


def main():
    apply = "--apply" in sys.argv
    files = sorted(SRC.iterdir())
    dst = C.PROJ / "06_VIDEO" / C.STEM / "sticker"
    dst.mkdir(parents=True, exist_ok=True)

    # 1) validate: moi file khop dung 1 key, moi key trong SPEC duoc dung dung 1 lan
    pairs, unmatched = [], []
    for p in files:
        tgt = MAP.get(p.name) or next((v for k, v in MAP.items() if p.name.startswith(k)), None)
        if not tgt:
            unmatched.append(p.name)
            continue
        pairs.append((p, tgt))
    used = [t for _, t in pairs]
    dup = sorted({t for t in used if used.count(t) > 1})
    all_keys = set(S.SPEC.keys())
    missing = sorted(all_keys - set(used))
    extra = sorted(set(used) - all_keys)
    print(f"file: {len(files)} · khớp: {len(pairs)} · không khớp: {len(unmatched)}")
    if unmatched:
        print("⚠ KHÔNG khớp MAP:")
        for u in unmatched:
            print("   ", u)
    if dup:
        print(f"🔴 TRÙNG target (2 file cùng 1 el_): {dup}")
    if missing:
        print(f"🔴 THIẾU {len(missing)} key chưa có file: {missing}")
    if extra:
        print(f"🔴 target LẠ không có trong SPEC: {extra}")
    if unmatched or dup or missing or extra:
        print("\n⛔ CHƯA APPLY — sửa MAP rồi chạy lại.")
        return 1

    for i, (p, tgt) in enumerate(pairs):
        im = C._imread(p)
        out, viol = C.cutout(im)
        if out is None:
            print(f"🔴 {p.name}: không tách được (nền không phải magenta?)")
            continue
        flag = "⚠ TÍM" if viol > 50 else "ok"
        if apply:
            C._imwrite(dst / f"{tgt}.png", out)
        print(f"   {'✓' if apply else '·'} {tgt:<22} {out.shape[1]}x{out.shape[0]}  tím={viol:<5} {flag}  ← {p.name}")

    print(f"\n{'✓ ghi' if apply else '· xem trước'} {len(pairs)}/92 sticker → {dst}")
    if apply:
        import cv2
        import numpy as np
        h = 220
        cols = []
        for _, tgt in pairs:
            o = cv2.imdecode(np.fromfile(str(dst / f"{tgt}.png"), np.uint8), cv2.IMREAD_UNCHANGED)
            s = h / o.shape[0]
            r = cv2.resize(o, (max(1, int(o.shape[1] * s)), h))
            bg = np.full((h, r.shape[1], 3), C.PAPER[::-1], np.uint8)
            a = r[..., 3:4].astype(np.float32) / 255
            comp = (r[..., :3] * a + bg * (1 - a)).astype(np.uint8)
            cols.append(comp)
        per_row = 10
        rows = [np.hstack(cols[i:i + per_row]) for i in range(0, len(cols), per_row)]
        w = max(r.shape[1] for r in rows)
        rows = [np.pad(r, ((0, 0), (0, w - r.shape[1]), (0, 0)), constant_values=245) for r in rows]
        sheet = np.vstack(rows)
        C._imwrite(dst / "_sticker_sheet.jpg", sheet)
        print(f"[SHEET] {dst / '_sticker_sheet.jpg'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
