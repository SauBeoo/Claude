# -*- coding: utf-8 -*-
"""Sinh SLIDES.json + prompt gen anh cho video 05 (dagashiya-10en) — nhip ~6s/khung.

Theo dung khuon build_scenes_04.py: moi ITEM co danh sach SHOTS (coverage kieu dien anh),
script tu tinh khung thoi gian that (uoc luong theo ky tu, he so RATE) roi CHIA DEU N shot
vao khung do. Khac video 04 o cho: video 05 co NHIEU anh THAT (Wikimedia Commons, da tai ve
real_photos/) thay vi 100% AI — moi shot co kind "real" (dung anh co san, KHONG can gen) hoac
"ai" (can gen, ghi vao scene_prompts_FLOW.txt).

User chot 2026-08-26: "tam 6s chuyen frame anh 1 lan nhe. Neu video that dai thi co the de
nguyen nhe" — video nay khong co video that (chi anh thoughat), nen quy tac 6s ap dung deu.
"""
import io, sys, re, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "05_dagashiya-10en_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "05_dagashiya-10en_SLIDES.json"
OUT_DIR = ROOT / "06_VIDEO" / "05_dagashiya-10en"
RATE = 3.983

LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, "
        "faded warm Fujicolor palette, soft natural light, gentle film grain, "
        "slight vignette, nostalgic documentary photography, muted greens and ochres, "
        "natural imperfect framing, 16:9")

PRESET = {
    "shop_interior": ("inside a small Showa-era shop, dark stained wood shelving, "
                       "worn plank floor, low ceiling, one bare bulb, dusty still air, "
                       "no street and no sky in frame"),
    "shotengai": ("narrow Showa shopping street, wooden shopfronts, fabric awnings and "
                  "noren curtains, hand-painted signage kept out of focus, worn asphalt "
                  "and concrete"),
    "lot": ("a small unpaved vacant lot behind Showa shopfronts, packed dirt ground, "
            "a low wooden fence, a few stacked wooden crates, patches of dry grass at "
            "the edges"),
}

AVOID = ("no watermark, no logo, no signature, no sparkle mark. "
         "Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, "
         "modern clothing, sneakers with logos, readable text or signage, brand logos, "
         "western faces, anime style, oversaturated HDR look, close-up faces.")

# ============================================================================
# ITEM_RANGES: (line_idx_start, line_idx_end_exclusive) -- xac dinh bang content_lines
# ============================================================================
ITEM_RANGES = {
    "item1": (0, 8), "item2": (8, 12), "item3": (12, 17), "item4": (17, 21),
    "item5": (21, 26), "cta": (26, 27), "item6": (27, 31), "item7": (31, 36),
    "item8": (36, 42), "item9": (42, 49), "item10": (49, 53), "ending": (53, 57),
}

# ============================================================================
# SHOTS theo section. Moi phan tu: (name, preset, desc, kind)
#   kind="real" -> name la ten file trong real_photos/ (KHONG can gen, xem ghi chu crop)
#   kind="ai"   -> can gen, prompt ghi vao scene_prompts_FLOW.txt
# ============================================================================
SHOTS = {

"item1": [
    ("jt_01_shop_barrels", "shop_interior", "PHIM 1959: quay みやげ long den bong bay -> khoi lu huong — cold open", "vid", 10),
    ("jt_04_kids_miyage", "shop_interior", "PHIM 1959: dam tre truoc tiem みやげ", "vid", 14),
    ("jt_21_boy_greencap", "shop_interior", "PHIM 1959: be trai mu xanh ben me", "vid", 12),
    ("jt_03_shotengai_walk", "shop_interior", "PHIM 1959: pho mua sam kimono xe dap", "vid", 12),
    ("ai_01_coldopen_glasscase", "shop_interior", "extreme close-up of a glass display case, warm amber light reflecting off the glass, soft blurred shapes of wrapped candy behind it, a faint breath-fog shape near the bottom edge, no face visible, low angle looking up into the case", "ai"),
    ("ai_02_ten_coins_hand", "shop_interior", "close-up of an open child-sized palm holding exactly ten Japanese 10-yen coins, warm directional light, worn wooden counter blurred below, no face or arm above the wrist visible", "ai"),
    ("ai_03_smartball_wide", "shop_interior", "wide shot of a dim corner inside the shop, an old wooden smart ball table standing alone against the wall, a single bare bulb hanging above it, no people in frame", "ai"),
    ("ai_137_smartball_table_sub", "shop_interior", "old wooden smart ball table standing inside a dim shop, worn lacquered wood, a single bare bulb above, no people", "ai"),
    ("ai_04_smartball_balls_insert", "shop_interior", "extreme close-up of several small silver metal balls sitting inside the wooden scoring grooves of a smart ball table, warm side light catching the metal", "ai"),
    ("ai_05_lever_finger", "shop_interior", "close-up of a single finger resting on the flipper lever of an old smart ball machine, worn wood texture, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_06_coinslot_brass", "shop_interior", "extreme close-up of a worn brass coin slot on the side of a smart ball table, warm light catching the tarnished metal", "ai"),
    ("ai_07_second_table_idle", "shop_interior", "wide shot of a second smart ball table standing idle in shadow, no one seated at it, faint dust in the still air", "ai"),
    ("ai_08_prize_jar", "shop_interior", "close-up of small prize tokens stacked inside a glass jar beside a game table, warm light", "ai"),
    ("ai_09_dust_beam", "shop_interior", "close-up of fine dust motes drifting through a thin beam of warm light near an old wooden machine", "ai"),
    ("ai_10_bulb_glow_wood", "shop_interior", "medium shot of a single bare bulb's warm glow reflecting off polished old wood shelving", "ai"),
    ("ai_11_wood_grain_worn", "shop_interior", "extreme close-up of worn wooden counter grain, smoothed pale by decades of hands resting on it", "ai"),
    ("ai_12_sandals_step", "shop_interior", "wide shot of a small pair of indoor sandals left neatly beside a wooden shop step, warm light, no people", "ai"),
    ("ai_13_wall_clock", "shop_interior", "close-up of a simple round wall clock ticking above old wooden shelves, soft warm light", "ai"),
    ("ai_14_doorway_threshold", "shop_interior", "medium shot of a wooden shop doorway threshold with warm afternoon light spilling across it, no people", "ai"),
    ("ai_15_noren_sway", "shop_interior", "close-up of a faded fabric shop curtain swaying gently near the entrance, warm backlight", "ai"),
    ("ai_16_candy_jars_bg", "shop_interior", "wide shot of rows of glass candy jars softly blurred on dark wooden shelving in the background, warm light", "ai"),
    ("ai_17_price_tag_blur", "shop_interior", "close-up of a small hand-written wooden price tag, text softly blurred and illegible, warm light", "ai"),
    ("ai_18_stool_beside", "shop_interior", "medium shot of a low wooden stool sitting beside an old game table, warm light, no people", "ai"),
    ("ai_19_coin_return_tray", "shop_interior", "close-up of a single coin resting in a machine's worn metal return tray, warm light", "ai"),
    ("ai_20_window_light", "shop_interior", "wide shot of warm afternoon light coming through a small shop window, dust visible in the beam", "ai"),
    ("ai_21_cobweb_corner", "shop_interior", "close-up of a faint cobweb in the corner near a ceiling beam, soft warm light", "ai"),
    ("ai_22_glasscase_corner", "shop_interior", "medium shot of a glass display case corner, soft blurred candy shapes inside, warm reflection", "ai"),
    ("ai_23_hand_toward_case", "shop_interior", "close-up of a hand reaching toward a glass display case, warm light, no face or arm above the wrist visible", "ai"),
],

"item2": [
    ("item2_kuji_aizu", "shop_interior", "[ANH THAT — dung thang, hop 三角くじ that, KHONG co nguoi]", "real"),
    ("ai_138_kuji_tickets_wall_sub", "shop_interior", "wall densely covered with small folded triangular paper lottery tickets, warm light, no people", "ai"),
    ("ai_24_kuji_pull_hand", "shop_interior", "close-up of a hand reaching up to pull one small folded triangular paper lottery ticket from a densely packed wall of hundreds, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_25_kuji_unfold", "shop_interior", "extreme close-up of a small folded paper ticket being unfolded, a faint printed symbol just visible, warm light, no readable text", "ai"),
    ("ai_26_kuji_wall_wide", "shop_interior", "wide shot of a wall covered edge to edge with hundreds of small folded paper lottery tickets, warm light", "ai"),
    ("ai_27_candy_prize_tray", "shop_interior", "close-up of a small pile of unwrapped candy prizes resting in a shallow tray, warm light", "ai"),
    ("ai_28_hand_hesitate", "shop_interior", "medium shot of a small hand hesitating over a wall of paper tickets, warm light, no face visible", "ai"),
    ("ai_29_winning_ticket", "shop_interior", "close-up of a single ticket marked with a faint printed symbol, warm light, no readable text", "ai"),
    ("ai_30_wall_corner_light", "shop_interior", "wide shot of the ticket wall's corner catching warm afternoon light", "ai"),
    ("ai_31_paper_scraps", "shop_interior", "close-up of small torn paper scraps scattered on a wooden counter below the ticket wall, warm light", "ai"),
],

"item3": [
    ("jt_12_nakamise", "shop_interior", "PHIM 1959: pho quay 仲見世 long den", "vid", 22),
    ("ai_139_toy_rifle_red_sub", "shotengai", "cork-tipped toy rifle resting on a worn red fabric counter outside a shopfront, warm light, no people", "ai"),
    ("ai_32_cork_rifle_barrel", "shotengai", "close-up of a cork-tipped toy rifle barrel resting on a worn red fabric counter, warm evening light", "ai"),
    ("ai_33_prize_shelf", "shotengai", "close-up of small toy prizes lined neatly on a low wooden shelf, warm evening light", "ai"),
    ("ai_34_bench_wide_empty", "shotengai", "wide shot of an empty wooden shooting-gallery bench under a shop awning, warm late-afternoon light, no people", "ai"),
    ("ai_35_cork_pellets_dish", "shotengai", "close-up of a small stack of cork ammunition pellets resting in a shallow dish, warm light", "ai"),
    ("ai_36_red_cloth_light", "shotengai", "medium shot of worn red fabric counter catching the last warm light of the day", "ai"),
    ("ai_37_price_sign_blur", "shotengai", "close-up of a small paper price sign, text softly blurred and illegible, warm light", "ai"),
    ("ai_38_bench_low_angle", "shotengai", "wide shot of the shooting bench from a low angle, long evening shadows stretching across it, no people", "ai"),
    ("ai_39_cork_bounce_target", "shotengai", "close-up of a single cork bouncing off a felt-covered target board, motion blur, warm light", "ai"),
],

"item4": [
    ("jt_11_stall_toys_kids", "shop_interior", "PHIM 1959: quay do choi chong chong, tre xem hang", "vid", 14),
    ("item4_shinkansen_game", "shop_interior", "[ANH THAT — HERO SHOT, dung gan nguyen khung, mo may 新幹線ゲーム khe ¥10 ro]", "real"),
    ("ai_40_coinslot_10yen_plate", "shop_interior", "extreme close-up of a small metal plate marked with a coin symbol beside a coin slot on an old game machine, warm light", "ai"),
    ("ai_41_thumb_lever", "shop_interior", "close-up of a hand's thumb pressing down on a side lever of an old coin-operated game machine, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_42_ball_track", "shop_interior", "extreme close-up of a small metal ball bearing rolling along a painted game board track behind glass, warm light", "ai"),
    ("ai_43_machine_near_register", "shop_interior", "wide shot of an old coin-operated game machine standing near a shop register, warm side light, no people", "ai"),
    ("ai_44_metal_corner_worn", "shop_interior", "close-up of a worn painted metal corner of a game machine's frame, warm light", "ai"),
    ("ai_45_glass_front_reflect", "shop_interior", "medium shot of a game machine's glass front reflecting warm afternoon light", "ai"),
    ("ai_46_ticket_dispenser", "shop_interior", "close-up of small printed prize tickets tucked into a dispenser slot, warm light, no readable text", "ai"),
    ("ai_47_machine_shadow_floor", "shop_interior", "wide shot of a game machine's long shadow stretching across the wooden floor, warm light", "ai"),
    ("ai_48_coin_balanced_edge", "shop_interior", "extreme close-up of a single ten-yen coin balanced on the edge of a game machine, warm light", "ai"),
],

"item5": [
    ("jt_08_stall_lanterns_a", "shop_interior", "PHIM 1959: quay le hoi long den do choi treo", "vid", 12),
    ("jt_09_stall_redfish", "shop_interior", "PHIM 1959: ca do do choi, bong bay xanh", "vid", 10),
    ("ai_49_gachagacha_wide", "shotengai", "wide shot of two old capsule-toy vending machines standing side by side just inside a shop's entrance, colorful plastic capsules visible through the round glass domes, worn painted metal legs, hand-crank levers, warm afternoon light from the doorway, no people", "ai"),
    ("ai_50_gachagacha_crank_hand", "shotengai", "close-up of a hand gripping and turning the crank handle of an old capsule-toy vending machine, worn metal texture, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_51_capsules_dome", "shotengai", "close-up of plain colorful plastic capsules visible through a round glass dome, no printed characters or readable text on them, warm light", "ai"),
    ("ai_52_capsule_falling_tray", "shotengai", "close-up of a single plain colorful capsule falling into a machine's metal tray, motion blur, warm light", "ai"),
    ("ai_53_machine_legs_worn", "shotengai", "medium shot of the worn painted metal legs of a capsule-toy machine, warm light", "ai"),
    ("ai_54_doorway_light_machines", "shotengai", "wide shot of warm doorway light spilling onto a row of capsule-toy machines, no people", "ai"),
    ("ai_55_coinslot_machine_face", "shotengai", "extreme close-up of a small coin slot on a capsule-toy machine's metal face, warm light", "ai"),
    ("ai_56_hand_cup_capsule", "shotengai", "close-up of a hand cupping a single fallen capsule, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_57_machine_shadow_wood", "shotengai", "medium shot of a capsule-toy machine's shadow falling across an old wooden floor, warm light", "ai"),
    ("ai_58_dust_fingerprints_glass", "shotengai", "extreme close-up of fine dust and faint fingerprints on a machine's glass dome, warm light", "ai"),
    ("ai_59_street_glimpse_doorway", "shotengai", "wide shot of a narrow Showa shopping street glimpsed faintly through an open doorway beside the machines, soft focus, no people", "ai"),
    ("ai_60_handle_paint_chip", "shotengai", "close-up of worn paint chipping on a capsule-toy machine's crank handle, warm light", "ai"),
],

"cta": [
    ("jt_15_matsuri_street", "shop_interior", "PHIM 1959: pho quay duoi hoa dao 商店街", "vid", 16),
    ("jt_20_shoeshine_street", "shop_interior", "PHIM 1959: tho danh giay ngoi hang", "vid", 12),
    ("ai_61_shop_wide_ambient", "shop_interior", "wide shot of warm afternoon light filling the small shop, dust motes drifting slowly, no people, a quiet still moment", "ai"),
    ("ai_62_shelves_blur", "shop_interior", "medium shot of shelves of jarred candy softly out of focus in warm light, no people", "ai"),
    ("ai_63_bulb_glow_aisle", "shop_interior", "close-up of a single bare bulb glowing warm above an empty aisle, soft light", "ai"),
    ("ai_64_counter_edge_worn", "shop_interior", "close-up of an old wooden counter's worn edge catching warm light", "ai"),
    ("ai_65_shop_from_doorway", "shop_interior", "wide shot of the shop's interior seen from just inside the doorway looking in, warm light, no people", "ai"),
    ("ai_66_paper_fan_counter", "shop_interior", "close-up of a small paper fan resting on a wooden counter, warm light", "ai"),
    ("ai_67_light_floorboards", "shop_interior", "medium shot of warm afternoon light crossing old wooden floorboards, quiet, no people", "ai"),
],

"item6": [
    ("jt_22_street_kids", "lot", "PHIM 1959: tre em ben duong pho", "vid", 10),
    ("jt_16_lion_dance", "shop_interior", "PHIM 1959: mua lan tren duong", "vid", 13),
    ("ai_68_lot_wide_crate", "lot", "wide shot of a small unpaved vacant lot behind shopfronts, a low wooden crate used as a spinning-top battle stage in the center, a few pairs of small feet in rubber sandals standing around it, long warm afternoon shadows, no faces visible", "ai"),
    ("item6_beigoma", "lot", "[ANH THAT — dung thang, con quay kim loai can canh, KHONG co nguoi]", "real"),
    ("item6_menko", "lot", "[ANH THAT — dung thang, bo the メンコ ve vo si, KHONG co nguoi]", "real"),
    ("ai_69_cord_wind_hand", "lot", "close-up of a hand tightly winding a length of cord around a small metal spinning top, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_70_top_spinning_blur", "lot", "close-up of a metal spinning top mid-spin on a wooden crate, motion blur, warm light", "ai"),
    ("ai_71_feet_crouched_crate", "lot", "medium shot of small feet in rubber sandals crouched around a wooden crate, warm light, no faces visible", "ai"),
    ("ai_72_menko_facedown", "lot", "close-up of a single flat card flipped face-down on packed dirt ground after a loss, warm light", "ai"),
    ("ai_73_lot_shadows_long", "lot", "wide shot of long warm shadows crossing the packed dirt ground of a small vacant lot, no people", "ai"),
    ("ai_74_crate_surface_scarred", "lot", "close-up of a worn wooden crate surface scarred and dented from years of play, warm light", "ai"),
],

"item7": [
    ("jt_10_balloons_kusuri", "shop_interior", "PHIM 1959: chum bong bay nhieu mau tren dau", "vid", 14),
    ("jt_19_kids_balloon_crowd", "shop_interior", "PHIM 1959: be gai cam bong bay do", "vid", 10),
    ("ai_75_tarai_wide", "lot", "wide shot of a round tin washtub sitting on a low wooden stool in a small vacant lot, colorful water balloons floating on the surface, warm afternoon light reflecting off the water, a folding stool beside it, no people", "ai"),
    ("item7_yoyo", "lot", "[ANH THAT — dung thang, chau bong nuoc nhieu mau cuc dep, chi lo tay nguoi lon o mep khung khong phai mat]", "real"),
    ("ai_76_string_dip_balloon", "lot", "close-up of a thin twisted paper string dipping toward a floating water balloon, warm light", "ai"),
    ("ai_77_string_snap_drift", "lot", "close-up of a thin paper string snapping, a colorful water balloon drifting free on the surface, warm light", "ai"),
    ("ai_78_folding_stool", "lot", "medium shot of a small folding stool sitting beside a tin washtub, warm light, no people", "ai"),
    ("ai_79_droplets_rim", "lot", "extreme close-up of water droplets beading on a tin tub's worn metal rim, warm light", "ai"),
    ("ai_80_water_glint_wide", "lot", "wide shot of warm afternoon light glinting off the water's surface inside a tin tub, no people", "ai"),
    ("ai_81_balloon_held_string", "lot", "close-up of a caught water balloon held by its short paper string, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_82_tub_shadow_dirt", "lot", "medium shot of a tin tub's shadow stretching across packed dirt ground, warm light", "ai"),
],

"item8": [
    ("jt_06_craftsman", "shop_interior", "PHIM 1959: tay tho lam viec ben hop go", "vid", 10),
    ("jt_13_ladies_lanterns", "shop_interior", "PHIM 1959: ba cu truoc quay long den", "vid", 16),
    ("jt_14_toy_vendor_table", "shop_interior", "PHIM 1959: ong ban do choi/keo tren ban nho", "vid", 7),
    ("ai_83_obachan_hands_apron", "shop_interior", "low-angle shot of an elderly Japanese woman's hands and the edge of a faded cotton apron, seen from behind a worn wooden shop counter, one hand reaching to place a few candies into a small paper bag beside a stack of coins, face and head out of frame, warm shop light", "ai"),
    ("ai_84_tissue_apron_pocket", "shop_interior", "extreme close-up of a folded tissue paper peeking out of the pocket of a faded cotton apron, worn fabric texture, soft warm light, no face visible", "ai"),
    ("ai_85_coins_counted_counter", "shop_interior", "close-up of a few coins being counted out on a worn wooden counter, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_86_paperbag_folded", "shop_interior", "close-up of a small paper bag being folded closed by a pair of hands, warm light, no face visible", "ai"),
    ("ai_87_register_area_wide", "shop_interior", "medium shot of an old shop register area, warm light, no people visible", "ai"),
    ("ai_88_abacus_shelf", "shop_interior", "close-up of a worn wooden abacus resting on a shelf beside the register, warm light", "ai"),
    ("ai_89_extra_candy_added", "shop_interior", "close-up of a hand placing one extra piece of candy into a small paper bag, warm light, no face visible", "ai"),
    ("ai_90_counter_low_eyelevel", "shop_interior", "wide shot of a shop counter seen from a child's low eye level, warm light, no face visible above the counter edge", "ai"),
    ("ai_91_apron_hem_frayed", "shop_interior", "extreme close-up of a faded cotton apron's frayed hem, soft warm light", "ai"),
    ("ai_92_small_stool_behind", "shop_interior", "close-up of a small wooden stool tucked behind a shop counter, warm light, no people", "ai"),
    ("ai_93_till_drawer_open", "shop_interior", "close-up of a worn wooden till drawer half open, a few coins visible inside, warm light", "ai"),
    ("ai_94_closed_sign_dusk", "shop_interior", "wide shot of a glass shop door with a small hand-lettered sign turned to face outward, warm dusk light, no people, no readable text", "ai"),
    ("ai_95_dust_empty_stool", "shop_interior", "close-up of fine dust settling in a beam of light on an empty stool by the register, quiet", "ai"),
    ("ai_96_counter_empty_fading", "shop_interior", "medium shot of the shop counter now empty, warm light slowly fading, no people", "ai"),
],

"item9": [
    ("jt_17_boy_camera", "shop_interior", "PHIM 1959: be trai tap trung cam may anh", "vid", 9),
    ("jt_18_schoolkids", "shop_interior", "PHIM 1959: dam hoc sinh dong phuc", "vid", 11),
    ("item9_katanuki", "shop_interior", "[ANH THAT — CAN CROP KY: chi lay bang カタヌキ菓子 + tay + vun keo trang o giua-duoi khung, bo het nguoi/ao hien dai xung quanh]", "real"),
    ("ai_97_candy_board_shapes", "shop_interior", "close-up of a thin printed candy board with faint pastel animal and star shapes pressed into it, warm side light, no hands or faces visible", "ai"),
    ("ai_98_needle_beside_board", "shop_interior", "extreme close-up of a sewing needle resting beside a printed candy board on a worn wooden counter, warm light", "ai"),
    ("ai_99_white_dust_fingertip", "shop_interior", "extreme close-up of fine white candy dust clinging to a fingertip, warm light, no face visible", "ai"),
    ("ai_100_board_edge_crack", "shop_interior", "close-up of a thin candy board's edge cracking slightly under gentle pressure, warm light", "ai"),
    ("ai_101_needle_working_shape", "shop_interior", "medium shot of a hand carefully working a needle around a pressed shape on a candy board, warm light, no face visible", "ai"),
    ("ai_102_prize_coins_counted", "shop_interior", "close-up of a small pile of coins being counted out as a prize on a wooden counter, warm light, no face visible", "ai"),
    ("ai_103_prize_chart_blurred", "shop_interior", "wide shot of a glass display case with a small hand-lettered prize chart faintly visible, softly blurred and illegible, warm light", "ai"),
    ("ai_104_shape_lifted_free", "shop_interior", "close-up of a completed, uncracked candy shape being lifted carefully free of its board, warm light", "ai"),
    ("ai_105_intent_posture_behind", "shop_interior", "medium shot of a small figure's intent posture leaning over a shop counter, seen strictly from behind, warm light, no face visible", "ai"),
    ("ai_106_shoulders_still_behind", "shop_interior", "close-up of still shoulders and held breath, seen strictly from behind, warm light, no face visible", "ai"),
    ("ai_107_cracked_piece_aside", "shop_interior", "close-up of a small cracked candy piece set aside on the counter, a quiet failure, warm light", "ai"),
    ("ai_108_counter_scattered_dust", "shop_interior", "wide shot of a wooden counter scattered with fine candy dust and a few finished shapes, warm light, no people", "ai"),
    ("ai_109_needle_tip_light", "shop_interior", "extreme close-up of warm light catching the fine tip of a sewing needle, soft focus behind it", "ai"),
    ("ai_110_board_tilted_light", "shop_interior", "close-up of a thin candy board tilted to catch better light, a hand steadying its edge, no face visible", "ai"),
    ("ai_111_hand_steady_edge", "shop_interior", "extreme close-up of a hand steadying a candy board against a worn counter edge, warm light, no face visible", "ai"),
    ("ai_112_glasscase_glow_wide", "shop_interior", "wide shot of a glass display case glowing warm in the late afternoon light, quiet, no people", "ai"),
    ("ai_113_coins_pushed_back", "shop_interior", "close-up of a small stack of coins being pushed back across a counter as a prize, warm light, no face visible", "ai"),
    ("ai_114_shop_calm_after", "shop_interior", "medium shot of the shop's interior calm and still again, warm light, no people", "ai"),
    ("ai_115_finished_shape_held_light", "shop_interior", "close-up of a finished, uncracked candy shape held up gently to catch the light, no face or arm above the wrist visible", "ai"),
],

"item10": [
    ("jt_07_veg_cart", "shop_interior", "PHIM 1959: xe rau ban rong", "vid", 10),
    ("jt_02_alley_signs", "shop_interior", "PHIM 1959: pho bang hieu Bar, xe co", "vid", 10),
    ("ai_135_storefront_a", "shotengai", "wide shot of a small Showa-era candy shop storefront seen from across a narrow residential street, a wooden sliding door half open, warm late-afternoon light, no people", "ai"),
    ("ai_16_dagashiya_wide_FALLBACK", "shotengai", "wide shot of a small Showa-era candy shop storefront seen from across a narrow residential street, a wooden sliding door half open, hand-painted wooden price boards leaning against the wall outside, a single bicycle parked nearby, warm late-afternoon light, no people", "ai"),
    ("ai_136_storefront_b", "shotengai", "medium shot of the same small candy shop storefront from a slightly different angle, a bicycle parked nearby, warm light, no people", "ai"),
    ("ai_116_priceboard_leaning", "shotengai", "close-up of a hand-painted wooden price board leaning against a shop's outer wall, text softly blurred and illegible, warm light", "ai"),
    ("ai_117_street_sign_dusk", "shotengai", "wide shot of a narrow street with a shop's sign faintly visible in the distance, warm dusk light, no readable text, no people", "ai"),
    ("ai_118_bicycle_parked", "shotengai", "close-up of a single old bicycle parked outside a shop, no rider, warm light", "ai"),
    ("ai_119_door_half_open", "shotengai", "medium shot of a wooden sliding shop door half open, warm light spilling out from inside, no people", "ai"),
    ("ai_120_weathered_signboard", "shotengai", "close-up of a weathered wooden sign board mounted on a shop wall, text softly blurred and illegible, warm light", "ai"),
    ("ai_121_street_empty_dusk", "shotengai", "wide shot of a narrow Showa shopping street now empty, long evening shadows, no people", "ai"),
    ("ai_122_paint_peeling_frame", "shotengai", "close-up of paint gently peeling on a shop's old wooden window frame, warm light", "ai"),
    ("ai_17_walking_away", "shotengai", "wide shot from behind, walking away down a narrow Showa-era residential street, a small shop's warm glow shrinking in the distance behind, long evening shadows, no face visible", "ai"),
],

"ending": [
    ("jt_05_kids_train", "shop_interior", "PHIM 1959: tre em vay tay tu cua so tau", "vid", 10),
    ("px_coin_spinning", "shop_interior", "PEXELS: dong xu quay roi do", "vid", 12),
    ("px_coins_hand_jar", "shop_interior", "PEXELS: tay bo xu vao hu", "vid", 12),
    ("ai_18_umaibou_coin_ending", "shop_interior", "close-up of a single wrapped snack stick candy and one lone Japanese 10-yen coin resting side by side on a worn wooden shop counter, warm side light, shallow depth of field, no hands or faces visible", "ai"),
    ("ai_123_coin_spin_stop", "shop_interior", "close-up of a single coin spinning slowly to a stop on a wooden counter, warm light", "ai"),
    ("ai_124_counter_quiet_evening", "shop_interior", "medium shot of a shop counter now quiet in warm evening light, no people", "ai"),
    ("ai_125_coin_release_gentle", "shop_interior", "close-up of a hand gently releasing a single coin onto a wooden counter, warm light, no face visible", "ai"),
    ("ai_126_shop_wide_still", "shop_interior", "wide shot of the whole shop interior, warm and still, no people, quiet evening light", "ai"),
    ("ai_127_dust_last_light", "shop_interior", "close-up of dust motes drifting slowly in the day's last warm light", "ai"),
    ("ai_128_glasscase_reflect_once_more", "shop_interior", "medium shot of a glass display case one more time, warm reflection, soft blurred candy shapes inside", "ai"),
    ("ai_129_wrapper_catch_light", "shop_interior", "close-up of a small candy wrapper catching the last warm light on a counter", "ai"),
    ("ai_130_door_closing_soft", "shop_interior", "wide shot of a shop door closing softly, warm light narrowing to a sliver, no people", "ai"),
    ("ai_131_counter_grain_lastlight", "shop_interior", "close-up of a wooden counter's grain catching the very last warm light of the day", "ai"),
    ("ai_132_street_empty_evening", "shotengai", "medium shot of an empty street outside the shop, evening settling, soft warm light", "ai"),
    ("ai_133_star_light_glasscase", "shop_interior", "extreme close-up of a single point of warm light catching the corner of a glass display case, quiet", "ai"),
    ("ai_134_street_dusk_wide_final", "shotengai", "wide shot of the whole narrow street at dusk, shop lights beginning to glow gently here and there, quiet and still", "ai"),
],
}


def content_lines(raw):
    out = []
    for l in raw.split("\n"):
        s = re.sub(r"\[[^\]]*\]", "", l).strip()
        if s:
            out.append(s)
    return out


def line_starts(lines):
    starts, cum = [], 0.0
    for l in lines:
        starts.append(cum / RATE)
        cum += len(l)
    total = cum / RATE
    ends = starts[1:] + [total]
    return starts, ends, total


def find_line_and_offset(t, starts, ends):
    for i, (s, e) in enumerate(zip(starts, ends)):
        if s <= t < e or (i == len(starts) - 1 and t >= s):
            return i, round(t - s, 2)
    return len(starts) - 1, 0.0


IMG_SLOT = 6.0      # muc tieu giay/anh
IMG_SLOT_MIN = 5.5  # duoi muc nay thi tu bo anh AI (khong bao gio bo anh THAT / clip)
FOOTAGE = OUT_DIR / "footage_raw"
CLIPS = OUT_DIR / "clips"


def place_section(shots, window_start, window_end):
    """Clip 'vid' giu NGUYEN do dai that; phan thoi gian con lai chia deu cho anh.
    Neu slot anh < IMG_SLOT_MIN -> bo dan anh AI (tu cuoi section) cho toi khi du."""
    shots = list(shots)
    while True:
        vid_total = sum(sh[4] for sh in shots if sh[3] == "vid")
        n_img = sum(1 for sh in shots if sh[3] != "vid")
        win = window_end - window_start
        slot = (win - vid_total) / n_img if n_img else 0
        if slot >= IMG_SLOT_MIN or n_img == 0:
            break
        # bo anh AI cuoi cung
        ai_idx = [k for k, sh in enumerate(shots) if sh[3] == "ai"]
        if not ai_idx:
            break
        shots.pop(ai_idx[-1])
    out, t = [], window_start
    for sh in shots:
        out.append((t, sh))
        t += sh[4] if sh[3] == "vid" else slot
    return out, slot, len(shots)


def main():
    import shutil
    raw = TTS.read_text(encoding="utf-8")
    lines = content_lines(raw)
    starts, ends, total = line_starts(lines)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CLIPS.mkdir(exist_ok=True)

    slides, flow, names, rows, entries = [], [], [], [], []
    err = 0
    report = []
    for section, (li0, li1) in ITEM_RANGES.items():
        ws = starts[li0]
        we = starts[li1] if li1 < len(starts) else total
        placed, slot, n_kept = place_section(SHOTS[section], ws, we)
        dropped = len(SHOTS[section]) - n_kept
        report.append(f"   {section:7} {we-ws:6.1f}s  clip={sum(sh[4] for _,sh in placed if sh[3]=='vid'):5.1f}s  anh={sum(1 for _,sh in placed if sh[3]!='vid'):3d} x {slot:4.1f}s  bo_AI={dropped}")
        for t, sh in placed:
            entries.append((t, sh, section))
    entries.sort(key=lambda x: x[0])

    for t, shot, section in entries:
        idx, off = find_line_and_offset(t, starts, ends)
        m = lines[idx][:14]
        if not any(m in L for L in lines):
            print(f"[LOI] match khong khop: {m}"); err += 1; continue
        name, preset, desc, kind = shot[:4]
        ent = {"match": m, "photo": True}
        if off:
            ent["offset"] = off
        pos = len(slides)
        if kind == "vid":
            ent = {"match": m, "video": True}
            if off: ent["offset"] = off
            src = FOOTAGE / f"{name}.mp4"
            ent["source"] = f"footage_raw/{name}.mp4"
            ent["dur"] = shot[4]
            if src.exists():
                dst = CLIPS / f"clip_{pos:02d}.mp4"
                if dst.exists(): dst.unlink()
                try: os_link = __import__("os").link; os_link(src, dst)
                except Exception: shutil.copy2(src, dst)
            else:
                print(f"[CANH BAO] thieu clip {src.name} (chay cut_archival/prep_pexels truoc)")
        elif kind == "real":
            ent["source"] = f"real_photos/{name}.jpg"
        elif kind == "real_pending":
            ent["source"] = f"real_photos/{name}.jpg (CHUA TAI - dung fallback AI ke tiep neu thieu)"
        else:
            ent["source"] = f"slides_img/{name}.jpg (AI, xem scene_prompts_FLOW.txt)"
        slides.append(ent)
        tag = {"real": "ANH THAT", "real_pending": "ANH THAT (cho tai)", "ai": "AI can gen", "vid": f"CLIP THAT {shot[4] if kind=='vid' else 0}s"}[kind]
        names.append(f"slide_{pos:03d}_{name}  [{tag}]  (t~{t:.1f}s, section={section}, offset={off}s)")
        rows.append((pos, name, preset, m, desc, kind, section))
        if kind == "ai":
            flow.append(f"{desc}, {PRESET[preset]}, {LOCK}. {AVOID}")

    PAIRS = [("no street", "shopping street"), ("no people", "figures"), ("no face", "face"), ("indoor", "outdoor")]
    def _positive(text, pos):
        t2 = re.sub(r"\bno\b(?:\s+\w+){0,3}\s+" + re.escape(pos), " ", text)
        return re.search(r"\b" + re.escape(pos) + r"\b", t2) is not None
    for i, name, preset, m, desc, kind, section in rows:
        if kind != "ai": continue
        low = f"{desc}, {PRESET[preset]}, {LOCK}".lower()
        for neg, pos in PAIRS:
            if neg in low and _positive(low, pos):
                print(f"[LOI] prompt {i:03d} ({name}) TU MAU THUAN: '{neg}' vs '{pos}'"); err += 1
    seen = set()
    for s_ in slides:
        key = (s_["match"], s_.get("offset", 0.0))
        if key in seen: print(f"[LOI] trung match+offset: {key}"); err += 1
        seen.add(key)
    if err:
        print(f"\n[X] {err} loi - KHONG ghi file"); sys.exit(1)

    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT_DIR / "scene_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (OUT_DIR / "scene_prompts_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    n_real = sum(1 for r in rows if r[5] == "real"); n_pend = sum(1 for r in rows if r[5] == "real_pending")
    n_ai = sum(1 for r in rows if r[5] == "ai"); n_vid = sum(1 for r in rows if r[5] == "vid")
    vid_sec = sum(sh[4] for _, sh, _ in entries if sh[3] == "vid")
    with open(OUT_DIR / "scene_prompts_BLOCKS.md", "w", encoding="utf-8") as f:
        f.write("# Prompt gen anh AI — 05_dagashiya-10en (clip that giu nguyen do dai, anh ~6s/khung)\n\n")
        f.write(f"> Tong {len(rows)} khung: **{n_vid} CLIP THAT ({vid_sec:.0f}s = {vid_sec/total*100:.0f}% video)** + **{n_real} anh THAT** + {n_pend} anh THAT cho tai + **{n_ai} can gen AI**.\n")
        f.write("> Gen bang Nano Banana/Gemini, 16:9, 3 ban/canh -> duyet mat chon 1.\n\n")
        for i, name, preset, m, desc, kind, section in rows:
            if kind != "ai": continue
            f.write(f"## {i:03d} — {name}  (preset: {preset}, section: {section})\nKhớp dòng: _{m}…_\n\n```\n{desc}, {PRESET[preset]}, {LOCK}. {AVOID}\n```\n\n")
    print(f"OK {len(slides)} entry -> {OUT_JSON.name}")
    print(f"   do dai uoc tinh: {total:6.1f}s = {int(total)//60}:{int(total)%60:02d}")
    print("\n".join(report))
    print(f"   CLIP THAT: {n_vid} ({vid_sec:.0f}s = {vid_sec/total*100:.0f}%) | ANH THAT: {n_real} | cho tai: {n_pend} | AI can gen: {n_ai}")


if __name__ == "__main__":
    main()
