# -*- coding: utf-8 -*-
"""Sinh SLIDES.json + prompt gen anh cho video 06 (shokyu-kakeibo) — nhip ~6s/khung.

Theo dung khuon build_scenes_05.py: moi SECTION co danh sach SHOTS (coverage kieu dien anh),
script tu tinh khung thoi gian that (uoc luong theo ky tu, he so RATE) roi CHIA DEU N shot
vao khung do. Clip phim THAT ("vid") giu NGUYEN do dai; phan con lai chia deu cho anh AI.

Khac video 05: video nay co 17 CLIP PHIM THAT (Japan Today 1959, CC0) + 111 anh AI, KHONG co
anh that Wikimedia (chu de la do vat rieng tu: phong bi luong, so tiet kiem, dong ho — khong
co anh PD dung chu de).

⚠️ CAVEAT phim 1959 cho bai ke ve 1970: clip la B-ROLL KHONG KHI, khong phai bang chung nam
thang. Chi tiet: tools/archival_spec_06.json "_caveat".
"""
import io, sys, re, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "06_shokyu-kakeibo_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "06_shokyu-kakeibo_SLIDES.json"
OUT_DIR = ROOT / "06_VIDEO" / "06_shokyu-kakeibo"
RATE = 3.983

# ---------------------------------------------------------------------------
# TANG A — STYLE LOCK bat bien cua kenh (04_VIDEOGEN_PROMPTS.md §1A), khong doi
# ---------------------------------------------------------------------------
LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, "
        "faded warm Fujicolor palette, soft natural light, gentle film grain, "
        "slight vignette, nostalgic documentary photography, muted greens and ochres, "
        "natural imperfect framing, 16:9")

# ---------------------------------------------------------------------------
# TANG B — boi canh. Bai nay la mot NGAY DI BO qua khu pho quanh ky tuc xa, nen
# cac preset deu thuoc CUNG MOT KHU: ky tuc xa + pho truoc cua + hang quan trong pho.
# Luat: preset TRONG NHA khong bao gio chua "street" (gate tu kiem o cuoi file).
# ---------------------------------------------------------------------------
PRESET = {
    "dorm": ("inside a 1970 Japanese company dormitory, narrow wooden corridor, thin plaster "
             "walls, three-mat tatami rooms, one bare bulb, still dusty air, "
             "no street and no sky in frame"),
    "office": ("a small 1970 Japanese company office, grey steel desks, stacked paper ledgers, "
               "a frosted glass partition, worn linoleum floor, no street and no sky in frame"),
    "sento": ("inside a Showa public bathhouse, pale tiled washing floor, rows of low brass "
              "faucets, small wooden stools, high wooden ceiling with drifting steam, "
              "no street and no sky in frame"),
    "canteen": ("a dormitory dining hall in 1970 Japan, long wooden tables, aluminium trays, "
                "a large rice pot on a steel counter, plain painted walls, "
                "no street and no sky in frame"),
    "yatai": ("a night ramen stall on a Showa street corner, cloth curtain, steam over a worn "
              "wooden counter, one paper lantern, damp asphalt underfoot"),
    "kissaten": ("inside a Showa coffee shop, thick upholstered sofas, dark wood panelling, dim "
                 "shaded lamps, heavy still air, no street and no sky in frame"),
    "cinema": ("inside a Showa movie theatre, rows of worn red seats, heavy velvet curtains, "
               "dim house lights, no street and no sky in frame"),
    "postoffice": ("inside a small Showa post office, a long wooden counter, a wire mesh screen "
                   "at the window, worn linoleum floor, no street and no sky in frame"),
    "furusato": ("a rural Japanese farmhouse around 1970, tatami room, a low table by a paper "
                 "screen window, muted country daylight, no city and no asphalt in frame"),
    "watchshop": ("inside a small Showa watch shop, a glass display case lit from within, dark "
                  "wood frame, dim ceiling light, no street and no sky in frame"),
    "home": ("small Showa house interior, tatami room, wooden sliding doors, low table, "
             "single bare bulb, no street and no sky in frame"),
    "street": ("a Showa city street around 1970, low concrete and wooden buildings, hand-painted "
               "signage kept out of focus, tram wires overhead, worn asphalt"),
}

AVOID = ("no watermark, no logo, no signature, no sparkle mark. "
         "Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, "
         "modern clothing, sneakers with logos, readable text or signage, brand logos, "
         "western faces, anime style, oversaturated HDR look, close-up faces.")

# ---------------------------------------------------------------------------
# SECTION_RANGES: (line_idx_start, line_idx_end_exclusive) tren content_lines
# ---------------------------------------------------------------------------
SECTION_RANGES = {
    "cold":   (0, 4),     # 0.0-21.8    phong bi + dau ngon tay
    "intro":  (4, 8),     # 21.8-84.4   khung 10 diem + CU CUOC + du bao 大卒/高卒
    "item1":  (8, 13),    # 84.4-143.4  額面
    "item2":  (13, 19),   # 143.4-219.7 寮費・食費
    "item3":  (19, 25),   # 219.7-289.5 銭湯
    "item4":  (25, 30),   # 289.5-356.3 まかない・米
    "item5":  (30, 34),   # 356.3-402.2 中華そば
    "cta":    (34, 35),   # 402.2-440.4 CTA giua video
    "item6":  (35, 41),   # 440.4-505.6 映画館
    "item7":  (41, 46),   # 505.6-543.3 たばこ
    "item8":  (46, 50),   # 543.3-584.0 喫茶店
    "item9":  (50, 55),   # 584.0-663.1 仕送り
    "item10": (55, 63),   # 663.1-739.4 残ったお金・通帳
    "watch":  (63, 67),   # 739.4-766.8 腕時計
    "ending": (67, 72),   # 766.8-821.7 dong bai
}

# ---------------------------------------------------------------------------
# SHOTS theo section. Moi phan tu: (name, preset, desc, kind[, dur])
#   kind="vid" -> ten file trong footage_raw/ (cat bang tools/archival_spec_06.json), dur = giay THAT
#   kind="ai"  -> can gen, prompt ghi vao scene_prompts_FLOW.txt
# ⭐ media-library §2.0: ENTRY 0 phai la CHU THE cua bai -> phong bi luong, khong phai ngon tay.
# ---------------------------------------------------------------------------
SHOTS = {

"cold": [
    ("ai_01_envelope_desk", "dorm", "a plain brown pay envelope lying alone on a small wooden desk, its edge slightly bulging, warm low light from a single bulb, nothing else on the desk, no hands in frame", "ai"),
    ("ai_02_fingertips_thickness", "dorm", "extreme close-up of two fingertips pinching the edge of a thick brown paper envelope to feel its thickness, warm light, no face or arm above the wrist visible", "ai"),
    ("jt06_01_crowd_toward", "street", "PHIM 1959: dam nguoi di bo huong ve may quay — 'あなたは、覚えていますか'", "vid", 8),
],

"intro": [
    ("jt06_02_tokyo_skyline", "street", "PHIM 1959: pho + bang hieu cao tang, o to", "vid", 10),
    ("ai_03_envelope_two_hands", "dorm", "close-up of two hands holding an unopened brown pay envelope over a low table, warm light, no face or arm above the elbow visible", "ai"),
    ("ai_04_notebook_blank", "dorm", "close-up of an old ruled household account notebook lying open and completely blank on a low table beside a pencil, warm light, no writing visible on the pages", "ai"),
    ("jt06_03_ginza_district", "street", "PHIM 1959: khu nha cao tang, bang hieu tron do, xe co", "vid", 9),
    ("ai_05_coins_row", "dorm", "close-up of a small row of worn coins lined up on a wooden desk beside a folded envelope, warm side light", "ai"),
    ("ai_06_room_bulb_wide", "dorm", "wide shot of a bare three-mat tatami room lit by one bare bulb, a folded futon in the corner and a low table in the middle, no people in frame", "ai"),
    ("ai_07_bills_counting", "dorm", "extreme close-up of dry paper banknotes being counted between two thumbs, warm light, no face visible", "ai"),
    ("ai_08_envelope_open_edge", "dorm", "extreme close-up of the torn top edge of a brown pay envelope with the corners of banknotes just showing inside, warm light", "ai"),
    ("ai_09_desk_lamp_night", "dorm", "medium shot of a small desk beside a window at night, a shaded lamp casting a warm circle of light on the wood, no people in frame", "ai"),
],

"item1": [
    ("ai_10_payslip_folded", "dorm", "close-up of a folded slip of thin paper resting on a wooden desk beside an opened envelope, the printing softly blurred and illegible, warm light", "ai"),
    ("ai_11_hand_flat_bills", "dorm", "close-up of a flat open palm holding a small stack of worn banknotes, warm directional light, no face or arm above the wrist visible", "ai"),
    ("jt06_04_office_street", "street", "PHIM 1959: bien tau dien ngam + nguoi tre di duong + toa nha van phong", "vid", 8),
    ("ai_12_office_desks", "office", "wide shot of a row of grey steel desks in a small company office, stacked ledgers and a wooden abacus on one desk, no people in frame", "ai"),
    ("ai_13_card_rack_wall", "office", "close-up of a wooden rack of blank card slots on an office wall, warm light, the cards completely blank", "ai"),
    ("ai_14_two_envelopes", "dorm", "close-up of two brown pay envelopes lying side by side on a desk, one visibly thicker than the other, warm light", "ai"),
    ("ai_15_corridor_two_doors", "dorm", "wide shot of a narrow dormitory corridor with two plain wooden doors facing each other, one bare bulb overhead, no people in frame", "ai"),
    ("ai_16_radio_shelf", "dorm", "close-up of a small valve radio on a wooden shelf against a thin wall, its dial glowing faintly, warm light", "ai"),
    ("ai_17_hand_pocket_envelope", "dorm", "close-up of a hand sliding a brown envelope into the breast pocket of a work jacket, warm light, no face visible", "ai"),
    ("ai_18_abacus_beads", "office", "extreme close-up of the worn beads of a wooden abacus catching warm light on a steel desk", "ai"),
    ("ai_19_ledger_column", "office", "close-up of an open paper ledger with faint ruled columns on a steel desk, the handwriting softly blurred and illegible, warm light", "ai"),
],

"item2": [
    ("jt06_09_shoten_street_day", "street", "PHIM 1959: pho hang quan ban ngay, nguoi di bo — duong tu cong ty ve ky tuc xa", "vid", 7),
    ("ai_20_dorm_entrance_shoes", "dorm", "wide shot of the entrance hall of a company dormitory, rows of worn shoes lined up on a concrete step, warm evening light, no people in frame", "ai"),
    ("jt06_05_young_workers", "street", "PHIM 1959: bon co gai dong phuc lao dong vua di vua cuoi", "vid", 6),
    ("ai_21_room_futon_mirror", "dorm", "wide shot of a three-mat tatami room with a folded futon, a small round mirror on the wall and a wicker trunk in the corner, no people in frame", "ai"),
    ("ai_22_wicker_trunk", "dorm", "close-up of an old wicker travel trunk with worn leather straps sitting on tatami, warm light", "ai"),
    ("ai_23_thin_wall_shadow", "dorm", "medium shot of a thin plaster dormitory wall with a faint shadow cast across it by a bare bulb, quiet and empty", "ai"),
    ("jt06_06_plaza_crossing", "street", "PHIM 1959: dam nguoi bang qua quang truong, tau dien phia sau", "vid", 12),
    ("ai_24_envelope_thin_backlit", "dorm", "close-up of a hand holding up a thin brown envelope against the light, warm backlight through the paper, no face visible", "ai"),
    ("ai_25_notice_board_blank", "dorm", "close-up of a plain wooden notice board on a dormitory wall with blank paper slips pinned to it, warm light, the slips completely blank", "ai"),
    ("ai_26_slippers_corridor", "dorm", "wide shot of a pair of worn slippers left at the end of a dim dormitory corridor under one bare bulb, no people in frame", "ai"),
    ("ai_27_window_night_dorm", "dorm", "medium shot of a dormitory window at night with a curtain half drawn, faint glow beyond the glass, no people in frame", "ai"),
    ("ai_29_two_figures_night_walk", "street", "wide shot of two figures walking away down a dim night street with towels over their shoulders, seen from far behind, one warm streetlight", "ai"),
    ("ai_28_towel_on_shoulder", "dorm", "close-up of a folded towel resting on the shoulder of a work jacket, warm light, no face visible", "ai"),
],

"item3": [
    ("ai_30_sento_curtain_doorway", "street", "medium shot of a bathhouse cloth curtain hanging in a lit doorway at night, warm light spilling onto the pavement, no people in frame", "ai"),
    ("ai_31_shoe_lockers", "sento", "close-up of a row of wooden shoe lockers with worn wooden keys in their slots, warm light", "ai"),
    ("ai_32_attendant_counter", "sento", "wide shot of a raised wooden attendant's counter just inside a bathhouse entrance, a small tin coin tray on top, no people in frame", "ai"),
    ("ai_33_yellow_basin", "sento", "extreme close-up of a yellow plastic bathing basin lying upturned on a wet tiled floor, warm light, the basin completely plain and unmarked", "ai"),
    ("ai_34_faucet_row", "sento", "medium shot of a row of low brass faucets along a tiled bathhouse wall, water beading on the tiles", "ai"),
    ("ai_35_wooden_stools", "sento", "close-up of small wooden bathing stools stacked beside a tiled wall on a wet floor, warm light", "ai"),
    ("ai_36_steam_ceiling", "sento", "wide shot of steam drifting under the high wooden ceiling of a bathhouse, soft light falling through a high window", "ai"),
    ("ai_37_bath_edge_water", "sento", "close-up of the tiled edge of a hot bath with the water surface steaming, no people in frame", "ai"),
    ("ai_38_coins_on_counter", "sento", "close-up of a hand placing small coins on a worn wooden counter, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_39_fogged_mirror", "sento", "close-up of a fogged bathhouse wall mirror with beads of water running down it, warm light", "ai"),
    ("ai_40_night_return_street", "street", "wide shot of a quiet night street with a single distant figure walking away, a towel over one shoulder, one warm streetlight", "ai"),
],

"item4": [
    ("ai_41_misoshiru_bowl", "canteen", "extreme close-up of a lacquer bowl of miso soup steaming on a wooden table, warm light", "ai"),
    ("ai_42_meal_tray", "canteen", "close-up of a simple meal tray holding white rice, miso soup and a single grilled fish, warm light", "ai"),
    ("jt06_07_taue", "furusato", "PHIM 1959: 田植え cay lua duoi ruong nuoc", "vid", 12),
    ("ai_43_long_table_wide", "canteen", "wide shot of a long dining table in a dormitory hall with empty stools along both sides, no people in frame", "ai"),
    ("ai_44_rice_pot_paddle", "canteen", "close-up of a large aluminium rice pot with a wooden paddle resting on its rim, steam rising", "ai"),
    ("jt06_08_ine_drying", "furusato", "PHIM 1959: bo lua phoi tren dong", "vid", 10),
    ("ai_45_rice_grains_bowl", "canteen", "extreme close-up of white rice grains heaped in a plain bowl, warm side light", "ai"),
    ("ai_46_rice_sack", "canteen", "close-up of an old cloth rice sack leaning against a wooden wall beside a square wooden measuring box, warm light, the cloth completely plain", "ai"),
    ("ai_47_chopsticks_over_bowl", "canteen", "close-up of a hand lifting chopsticks over a bowl of rice, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_48_empty_bowls_stack", "canteen", "close-up of empty bowls stacked on a wooden table after a meal, warm light", "ai"),
],

"item5": [
    ("ai_49b_broth_pot_steam", "yatai", "close-up of a large pot of broth steaming behind the counter of a night stall, warm light, no people in frame", "ai"),
    ("ai_49_yatai_lantern", "yatai", "medium shot of a paper lantern glowing above a night ramen stall with a cloth curtain below, no people in frame, the lantern completely plain", "ai"),
    ("ai_50_ramen_bowl_steam", "yatai", "extreme close-up of a bowl of soy-broth ramen steaming on a wooden counter, warm light", "ai"),
    ("ai_51_counter_stools_night", "yatai", "wide shot of the empty wooden counter of a night ramen stall with three stools, steam drifting, no people in frame", "ai"),
    ("ai_52_noodles_lifted", "yatai", "close-up of noodles being lifted from a bowl with chopsticks, steam rising, no face visible", "ai"),
    ("ai_53_coins_damp_counter", "yatai", "close-up of a few coins left on a damp wooden counter beside an empty bowl, warm light", "ai"),
    ("ai_54_curtain_backlit", "yatai", "close-up of the cloth curtain of a night stall backlit from inside, a warm glow coming through the fabric", "ai"),
    ("ai_55_empty_bowl_chopsticks", "yatai", "close-up of an empty ramen bowl with chopsticks laid across it on a wooden counter, warm light", "ai"),
],

"cta": [
    ("jt06_10_ongakukai_crowd", "street", "PHIM 1959: khan gia ngoi kin xem buoi dien ngoai troi", "vid", 9),
    ("ai_56_notebook_page_turn", "dorm", "close-up of a hand turning the page of an old ruled notebook on a low table, warm light, the pages blank, no face visible", "ai"),
    ("ai_57_pencil_on_page", "dorm", "extreme close-up of a worn pencil lying across a blank ruled page, warm light", "ai"),
    ("ai_58_room_evening_wide", "dorm", "wide shot of a small tatami room in the evening with a low table and a notebook under warm bulb light, no people in frame", "ai"),
    ("ai_59_window_faint_glow", "dorm", "medium shot of a dormitory window with a faint glow beyond the glass and a warm reflection on the pane, no people in frame", "ai"),
    ("ai_60_folding_envelope", "dorm", "close-up of a hand folding an empty brown envelope in half on a table, warm light, no face visible", "ai"),
],

"item6": [
    ("ai_61_cinema_front_night", "street", "wide shot of a cinema frontage at night with tall hand-painted billboards kept out of focus and bare bulbs along the front, no people in frame", "ai"),
    ("jt06_11_depaato_welcome", "street", "PHIM 1959: mat tien bach hoa + xe buyt", "vid", 9),
    ("ai_62_ticket_window", "cinema", "close-up of a small ticket window with a worn wooden sill and a brass coin tray, dim light, the sill completely bare", "ai"),
    ("ai_63_ticket_stub", "cinema", "extreme close-up of a small blank paper ticket stub held between two fingers, dim light, no face visible", "ai"),
    ("ai_64_red_seats_empty", "cinema", "wide shot of rows of worn red seats in a dim auditorium, no people in frame", "ai"),
    ("jt06_12_crowd_dense", "street", "PHIM 1959: dam dong day dac tren pho", "vid", 8),
    ("ai_65_heavy_curtain", "cinema", "medium shot of a heavy velvet curtain drawn across a screen, dim house lights above", "ai"),
    ("ai_66_projector_beam", "cinema", "medium shot of a dusty beam of projector light crossing a dark auditorium above empty seats", "ai"),
    ("ai_67_seat_armrest", "cinema", "extreme close-up of a worn velvet armrest between two seats, dim light", "ai"),
    ("ai_68_billboard_unlit", "street", "medium shot of a cinema billboard frontage with its bulbs unlit, seen from across a quiet road, the painted panels kept out of focus, no people in frame", "ai"),
],

"item7": [
    ("ai_69_cig_pack_in_hand", "street", "close-up of a small plain paper cigarette pack held in a hand under a streetlight at night, no face visible, the pack completely unmarked", "ai"),
    ("ai_70_match_flare", "street", "extreme close-up of a wooden match flaring inside cupped hands at night, warm light, no face visible", "ai"),
    ("ai_71_smoke_in_streetlight", "street", "medium shot of cigarette smoke drifting through the cone of a night streetlight, no people in frame", "ai"),
    ("ai_72_tobacco_kiosk_closed", "street", "medium shot of a small wooden tobacco kiosk window shuttered for the night, warm light nearby, the shutter completely plain, no people in frame", "ai"),
    ("ai_73_ashtray_low_table", "dorm", "close-up of a chipped glass ashtray on a low table with one cigarette resting on its rim, warm bulb light", "ai"),
    ("ai_74_country_station_lights", "furusato", "wide shot of the faint lights of a small country railway station seen from far across dark night fields", "ai"),
    ("ai_74b_smoke_past_bulb", "dorm", "close-up of a thin ribbon of cigarette smoke rising slowly past a bare bulb, warm light, no people in frame", "ai"),
],

"item8": [
    ("jt06_13_tearoom_men", "street", "PHIM 1959: nam thanh nien com-le di ngang toa nha co quan tra", "vid", 8),
    ("ai_75_coffee_shop_window", "street", "medium shot of a coffee shop window at street level with warm lamplight inside, the glass reflecting the pavement, the window completely plain, no people in frame", "ai"),
    ("ai_76_cup_and_saucer", "kissaten", "extreme close-up of a coffee cup and saucer with a small spoon on a dark wooden table, warm dim light", "ai"),
    ("ai_77_sofa_dim_corner", "kissaten", "wide shot of thick upholstered sofas around a low table in a dim coffee shop, no people in frame", "ai"),
    ("ai_78_water_glass_lamp", "kissaten", "close-up of a plain glass of water catching the warm glow of a shaded lamp on a dark table", "ai"),
    ("ai_79_record_player_corner", "kissaten", "medium shot of an old record player and a wooden speaker standing in a dim corner, warm light, no people in frame", "ai"),
],

"item9": [
    ("ai_80_registered_envelope", "postoffice", "close-up of a small stiff paper envelope with a thin red border lying on a wooden counter, warm light, the envelope completely blank", "ai"),
    ("ai_81_bills_into_envelope", "dorm", "close-up of banknotes being slid into a small envelope on a low table, warm bulb light, no face visible", "ai"),
    ("ai_82_pressing_flap_closed", "dorm", "extreme close-up of a hand pressing the flap of an envelope closed on a table, warm light, no face visible", "ai"),
    ("jt06_14_chatsumi", "furusato", "PHIM 1959: hai che, non rom trang giua doi che", "vid", 12),
    ("ai_83_letter_paper_held", "dorm", "close-up of a sheet of thin letter paper held in one hand under a bulb, the handwriting softly blurred and illegible", "ai"),
    ("ai_84_letter_on_tatami", "furusato", "close-up of a worn letter envelope resting on a tatami mat beside a low table, muted daylight, the envelope blank", "ai"),
    ("jt06_15_wara_stacks", "furusato", "PHIM 1959: dong rom + mai che tren dong", "vid", 9),
    ("ai_85_older_hands_mending", "furusato", "close-up of a pair of older hands mending cloth on a low table by a paper screen window, muted daylight, no face visible", "ai"),
    ("ai_86_farmhouse_room", "furusato", "wide shot of a quiet farmhouse tatami room with a low table and a paper screen window, muted daylight, no people in frame", "ai"),
    ("ai_87_stamp_pressed", "postoffice", "close-up of a wooden-handled rubber stamp being pressed onto a blank paper form on a counter, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_88_post_counter_wide", "postoffice", "wide shot of a small post office counter with a wire mesh screen and a worn linoleum floor, no people in frame", "ai"),
    ("ai_89_treadle_sewing_machine", "furusato", "close-up of an old treadle sewing machine standing by a window in a plain room, muted daylight, no people in frame", "ai"),
],

"item10": [
    ("ai_90_few_coins_left", "dorm", "extreme close-up of a few coins and one folded banknote left on a wooden desk, warm light", "ai"),
    ("ai_91_flattened_envelope", "dorm", "close-up of a flattened empty brown envelope lying on a desk, warm light", "ai"),
    ("ai_92_notebook_columns", "dorm", "close-up of an old ruled notebook open on a low table showing faint pencil column lines, the writing softly blurred and illegible", "ai"),
    ("jt06_16_ekimae_plaza", "street", "PHIM 1959: quang truong truoc ga + toa nha bach hoa", "vid", 9),
    ("ai_93_single_banknote", "dorm", "extreme close-up of a single worn banknote held flat between two fingers under a bulb, no face visible", "ai"),
    ("ai_94_passbook_open", "postoffice", "close-up of a small savings passbook lying open on a wooden counter, the printed lines softly blurred and illegible", "ai"),
    ("ai_95_ink_pad_and_stamp", "postoffice", "extreme close-up of a worn red ink pad and a wooden stamp lying on a counter, warm light", "ai"),
    ("jt06_17_street_walk", "street", "PHIM 1959: nguoi xach tui di tren pho", "vid", 12),
    ("ai_96_passbook_into_pocket", "dorm", "close-up of a small passbook being slipped into a jacket pocket, warm light, no face visible", "ai"),
    ("ai_97_counter_grille", "postoffice", "medium shot of a post office window grille with a plain wooden shelf below it, warm light, no people in frame", "ai"),
    ("ai_98_two_passbooks", "dorm", "close-up of two small savings passbooks lying side by side on a desk, warm light, both covers completely plain", "ai"),
    ("ai_99_desk_night_reckoning", "dorm", "wide shot of a low table at night holding a notebook, a pencil and a folded envelope under a bare bulb, no people in frame", "ai"),
],

"watch": [
    ("ai_100_watch_case_lit", "watchshop", "wide shot of a lit glass display case of wristwatches in a small shop, dark wood frame, no people in frame", "ai"),
    ("ai_101_watch_on_tray", "watchshop", "extreme close-up of a simple silver wristwatch with a leather strap lying on a velvet tray, warm light, the dial completely plain", "ai"),
    ("ai_102_fingertip_on_glass", "watchshop", "close-up of a fingertip resting on the glass of a display case, a warm reflection across the pane, no face or arm above the wrist visible", "ai"),
    ("ai_103_watch_fastened_wrist", "dorm", "close-up of a wristwatch being fastened around a wrist, warm bulb light, no face visible", "ai"),
],

"ending": [
    ("ai_104_envelope_on_palm", "dorm", "close-up of an empty brown envelope resting on an open palm, warm light, no face or arm above the wrist visible", "ai"),
    ("ai_105_two_futons_room", "dorm", "wide shot of a three-mat tatami room with two folded futons side by side under one bare bulb, no people in frame", "ai"),
    ("ai_106_new_year_cards", "home", "close-up of a small stack of plain postcards on a low table, muted daylight, the cards completely blank", "ai"),
    ("ai_107_drawer_half_open", "home", "close-up of a wooden drawer pulled half open with an old wristwatch lying inside among folded cloth, muted daylight", "ai"),
    ("ai_108_stopped_watch", "home", "extreme close-up of an old wristwatch with its hands stopped and dust on the glass, muted daylight, the dial completely plain", "ai"),
    ("ai_109_hand_closing_drawer", "home", "close-up of a hand pushing a wooden drawer closed, muted daylight, no face visible", "ai"),
    ("ai_110_screen_window_morning", "home", "medium shot of a paper screen window with soft morning light coming through it, no people in frame", "ai"),
    ("ai_111_notebook_closed", "dorm", "close-up of an old ruled notebook lying closed on a low table with a pencil beside it, warm light", "ai"),
    ("ai_112_room_empty_last", "dorm", "wide shot of an empty three-mat tatami room with the bulb switched off and only faint light from the window, quiet and still", "ai"),
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


def uniq_match(lines, idx):
    """Tien to ngan nhat cua dong idx ma CHI khop dung mot dong trong bai.
    🔴 Bat buoc: line 20 (ここで、もうひとつ聞かせてください。この年、東京の銭湯…) la tien to
    cua line 37 (…映画館の入場料…) o 14 ky tu dau -> renderer se cue nham dong."""
    L = lines[idx]
    for n in range(14, len(L) + 1, 2):
        m = L[:n]
        if sum(1 for x in lines if m in x) == 1:
            return m
    return L


def find_line_and_offset(t, starts, ends):
    for i, (s, e) in enumerate(zip(starts, ends)):
        if s <= t < e or (i == len(starts) - 1 and t >= s):
            return i, round(t - s, 2)
    return len(starts) - 1, 0.0


IMG_SLOT = 6.0      # muc tieu giay/anh (tran ~6s/frame cua kenh showa)
IMG_SLOT_MIN = 5.5  # duoi muc nay thi tu bo anh AI (khong bao gio bo clip THAT)
FOOTAGE = OUT_DIR / "footage_raw"
CLIPS = OUT_DIR / "clips"


def place_section(shots, window_start, window_end):
    """Clip 'vid' giu NGUYEN do dai that; thoi gian con lai chia deu cho anh.
    Neu slot anh < IMG_SLOT_MIN -> bo dan anh AI (tu cuoi section) cho toi khi du."""
    shots = list(shots)
    while True:
        vid_total = sum(sh[4] for sh in shots if sh[3] == "vid")
        n_img = sum(1 for sh in shots if sh[3] != "vid")
        win = window_end - window_start
        slot = (win - vid_total) / n_img if n_img else 0
        if slot >= IMG_SLOT_MIN or n_img == 0:
            break
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
    # 🔴 DON clips/ TRUOC MOI LUOT BUILD: ten file la clip_<VI TRI>.mp4, ma vi tri doi khi
    # them/bot 1 shot -> file cu con lai o vi tri khac se duoc video_render.py nhat nham
    # (dung ho bay "resume dung file cu" cua render-background.md §2.5).
    for f in CLIPS.glob("clip_*.mp4"):
        f.unlink()

    slides, flow, names, rows, entries = [], [], [], [], []
    err = 0
    report = []
    for section, (li0, li1) in SECTION_RANGES.items():
        ws = starts[li0]
        we = starts[li1] if li1 < len(starts) else total
        placed, slot, n_kept = place_section(SHOTS[section], ws, we)
        dropped = len(SHOTS[section]) - n_kept
        vidsec = sum(sh[4] for _, sh in placed if sh[3] == "vid")
        nimg = sum(1 for _, sh in placed if sh[3] != "vid")
        report.append(f"   {section:7} {we-ws:6.1f}s  clip={vidsec:5.1f}s  anh={nimg:3d} x {slot:4.1f}s  bo_AI={dropped}")
        for t, sh in placed:
            entries.append((t, sh, section))
    entries.sort(key=lambda x: x[0])

    for t, shot, section in entries:
        idx, off = find_line_and_offset(t, starts, ends)
        m = uniq_match(lines, idx)
        if sum(1 for L in lines if m in L) != 1:
            print(f"[LOI] match khong duy nhat/khong khop: {m}"); err += 1; continue
        name, preset, desc, kind = shot[:4]
        pos = len(slides)
        if kind == "vid":
            ent = {"match": m, "video": True}
            if off: ent["offset"] = off
            ent["source"] = f"footage_raw/{name}.mp4"
            ent["dur"] = shot[4]
            src = FOOTAGE / f"{name}.mp4"
            if src.exists():
                dst = CLIPS / f"clip_{pos:02d}.mp4"
                if dst.exists(): dst.unlink()
                try: __import__("os").link(src, dst)
                except Exception: shutil.copy2(src, dst)
            else:
                print(f"[CANH BAO] thieu clip {src.name} (chay cut_archival.py --spec tools/archival_spec_06.json truoc)")
        else:
            ent = {"match": m, "photo": True}
            if off: ent["offset"] = off
            ent["source"] = f"slides_img/{name}.jpg (AI, xem scene_prompts_FLOW.txt)"
        slides.append(ent)
        tag = {"ai": "AI can gen", "vid": f"CLIP THAT {shot[4] if kind == 'vid' else 0}s"}[kind]
        names.append(f"slide_{pos:03d}_{name}  [{tag}]  (t~{t:.1f}s, section={section}, offset={off}s)")
        rows.append((pos, name, preset, m, desc, kind, section))
        if kind == "ai":
            flow.append(f"{desc}, {PRESET[preset]}, {LOCK}. {AVOID}")

    # gate tu-mau-thuan: preset "no street" ma canh lai co street, v.v.
    PAIRS = [("no street", "street"), ("no people", "figures"), ("no face", "face"),
             ("no sky", "sky"), ("no city", "city")]
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
    n_ai = sum(1 for r in rows if r[5] == "ai"); n_vid = sum(1 for r in rows if r[5] == "vid")
    vid_sec = sum(sh[4] for _, sh, _ in entries if sh[3] == "vid")
    with open(OUT_DIR / "scene_prompts_BLOCKS.md", "w", encoding="utf-8") as f:
        f.write("# Prompt gen anh AI — 06_shokyu-kakeibo (clip that giu nguyen do dai, anh ~6s/khung)\n\n")
        f.write(f"> Tong {len(rows)} khung: **{n_vid} CLIP THAT ({vid_sec:.0f}s = {vid_sec/total*100:.0f}% video)** + **{n_ai} can gen AI**.\n")
        f.write("> Gen bang Nano Banana/Gemini/Flow, 16:9, 3 ban/canh -> duyet mat chon 1. Xoa watermark ✦ truoc khi dung.\n\n")
        for i, name, preset, m, desc, kind, section in rows:
            if kind != "ai": continue
            f.write(f"## {i:03d} — {name}  (preset: {preset}, section: {section})\n")
            f.write(f"Khớp dòng: _{m}…_\n\n```\n{desc}, {PRESET[preset]}, {LOCK}. {AVOID}\n```\n\n")
    print(f"OK {len(slides)} entry -> {OUT_JSON.name}")
    print(f"   do dai uoc tinh: {total:6.1f}s = {int(total)//60}:{int(total)%60:02d}")
    print("\n".join(report))
    print(f"   CLIP THAT: {n_vid} ({vid_sec:.0f}s = {vid_sec/total*100:.0f}%) | AI can gen: {n_ai}")


if __name__ == "__main__":
    main()
