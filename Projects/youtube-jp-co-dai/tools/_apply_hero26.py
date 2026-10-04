# -*- coding: utf-8 -*-
"""Ghép ảnh hero video 26 theo NỘI DUNG tên file (mtime lệch thứ tự FLOW)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_photocard26 as M  # noqa: E402

SRC = Path(r"C:\Users\tuana\Downloads\download (3)")

MAP = {
    "Adult_cutting_shoji_paper":               "card_kodomo_anzen",
    "Afternoon_sun_streaming_through_":         "card_nishimuki_taiyou",
    "Child_poking_shoji_paper_screen":          "card_kodomo_ana",
    "Cloud_drifting_above_home_window":         "card_shichou_toikake",
    "Condensation_water_droplets_on_w":         "card_ketsuro_mado",
    "Craftsman_spraying_water_on_paper":        "card_shokunin_mizu",
    "Elderly_couple_sitting_at_table":          "card_share_onegai",
    "Elderly_couple_sitting_in_room":           "card_sofubo_shouji",
    "Elderly_woman_smiling_portrait":           "card_haha_natsukashi",
    "Elderly_woman_standing_skeptical":         "card_mitsue_utagai",
    "Evening_light_through_shoji_screen":       "card_kumiawase",
    "Glass_window_and_shoji_screen":            "card_kuuki_sou_hikaku",
    "Glowing_question_mark_at_doorway":         "card_nazo_toi",
    "Hand_rubbing_candle_on_windowsill":        "card_rousoku_shikii",
    "Hands_holding_shoji_paper_panel":          "card_shouji_taisetsu",
    "Lantern_shining_through_shoji_door":       "card_shimei_tojiru",
    "Macro_close-up_of_washi_paper":            "card_washi_sen_macro",
    "Mould_spots_on_wooden_frame":              "card_kabi_macro",
    "Pamphlets_and_envelope_on_desk":           "card_kuni_uchimado",
    "Person_closing_shoji_screen":              "card_watashi_machigai",
    "Person_hanging_shoji_screen":              "card_muryou_kaifuku",
    "Person_peeling_washi_paper":               "card_nori_hagasu",
    "Person_spraying_water_on_shoji":           "card_watashi_taiken",
    "Quiet_windowsill_scene_at_dusk":           "card_kaisou_boutou",
    "Samurai_interior_with_glowing_sc":         "card_bushi_akari_shouji",
    "Shoji_paper_drying_in_breeze":             "card_taiko_hari",
    "Shoji_screen_and_plastic_curtain":         "card_kasoku_hikaku",
    "Shoji_screen_in_dim_storeroom":            "card_kieta_dougu",
    "Snow_viewed_from_warm_room":               "card_taikobari_yukiguni",
    "Traditional_Japanese_house_exter":         "card_furui_ie_gaikan",
    "Two_hygrometers_on_windowsills":           "card_shitsudokei",
    "Washi_paper_fibers_glowing":               "card_kami_iki",
    "Washi_paper_lantern_glowing_softly":       "card_kami_hikari",
    "Woman_hanging_curtain_near_cat":           "card_curtain_koukan",
    "Woman_reaching_for_window_paper":          "card_urikoba",
    "Woman_rubbing_arms_for_warmth":            "card_mitsue_samuke",
    "Woman_standing_near_kitchen_shelf":        "card_gimon_kaji",
    "Woman_touching_curtain_with_regret":       "card_mitsue_kizuku",
    "Woman_touching_damp_wooden_windo":         "card_mado_shimi",
    "Woman_touching_windowsill_with_cat":       "card_mitsue_kaiketsu",
    "Wooden_rain_shutter_beside_screen":        "card_bouhan_amado",
}


def main():
    apply = "--apply" in sys.argv
    files = list(SRC.iterdir())
    dst = M.PROJ / "06_VIDEO" / M.STEM / "photocard"
    dst.mkdir(parents=True, exist_ok=True)
    used = set()
    pairs = []
    for p in files:
        tgt = next((v for k, v in MAP.items() if p.name.startswith(k)), None)
        if not tgt:
            print(f"⚠ KHÔNG khớp MAP: {p.name}")
            continue
        pairs.append((p, tgt))
        used.add(tgt)
    missing = set(MAP.values()) - used
    if missing:
        print(f"🔴 THIẾU {len(missing)} card không tìm thấy file nguồn: {sorted(missing)}")
    rots = [-2.1, 1.7, -1.5, 2.2, -1.8, 1.4, -2.3, 1.6]
    for i, (p, tgt) in enumerate(pairs):
        if apply:
            sz = M.build(p, dst / f"{tgt}.png", i + 1, rots[i % len(rots)])
            print(f"   ✓ {tgt:<28} {sz[0]}x{sz[1]} ← {p.name}")
        else:
            print(f"   · {tgt:<28} ← {p.name}")
    print(f"\n{'✓ ghi' if apply else '· xem trước'} {len(pairs)}/{len(MAP)} photocard")
    if apply and not missing and len(pairs) == len(MAP):
        ims = [M.Image.open(dst / f"{t}.png").convert("RGB") for _, t in pairs]
        tw = 300
        ims = [im.resize((tw, int(tw * im.height / im.width))) for im in ims]
        cols = 6
        rows = (len(ims) + cols - 1) // cols
        sh = M.Image.new("RGB", (cols * tw, rows * ims[0].height), M.PAPER)
        for i, im in enumerate(ims):
            sh.paste(im, ((i % cols) * tw, (i // cols) * ims[0].height))
        sh.save(dst / "_photocard_sheet.jpg", quality=86)
        print(f"[SHEET] {dst / '_photocard_sheet.jpg'}")


if __name__ == "__main__":
    main()
