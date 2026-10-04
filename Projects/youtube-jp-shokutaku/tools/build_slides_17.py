# -*- coding: utf-8 -*-
r"""Dung SLIDES + prompt anh cho video 17 — v2 (2026-08-18).

    python tools\build_slides_17.py

⭐ v2 = THIET KE LAI theo phong cach co-dai + health (user chot 2026-08-18):
  - XUONG = make_shot.py -> BUILD-ON BANG HINH (focus / inset / soft / wipe).
    Khung DUNG YEN, cai dong la anh duoc lap vao. channels.py da tat "motion"
    (pan + build-on cung luc = hai chuyen dong danh nhau).
  - DIEM NHAN = 13 the `vox` cho SO LIEU (~16%, dung ti le co-dai video 22).
    NGOAI LE co chu cho media-library.md §2.9 — moi the BAT BUOC co nen ANH THAT.
  - transition dissolve 0.45s + watermark 60代の食卓: da them vao channels.py.

Xuat:
  04_SCRIPTS/17_chuseishibo-oyatsu_SLIDES_photo.json
  06_VIDEO/17_chuseishibo-oyatsu/slide_prompts_FLOW.txt / _TENFILE.txt / _BLOCKS.md
  06_VIDEO/17_chuseishibo-oyatsu/vox_prompts_FLOW.txt  (anh nen cho 13 the so lieu)

Van phap prompt (SHOT/SUBJECT/SETTING/LIGHT/LENS/STYLE/NEG): xem build_slides_16.py.
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "17_chuseishibo-oyatsu_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "17_chuseishibo-oyatsu_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "17_chuseishibo-oyatsu"

CPS, PER_LINE = 4.40, 0.25

STYLE = ("photorealistic documentary photography, Japanese home, muted deep navy and "
         "warm amber accents, calm clean composition, natural imperfect surfaces")
NEG = ("no text, no letters, no numbers, no captions, no watermark, no logo, "
       "no extra people, no doctors, no white coats")

SHOTS = {
    "ECU": "extreme close-up",
    "CU": "close-up",
    "MCU": "medium close-up",
    "MS": "medium shot",
    "WS": "wide shot",
    "OH": "overhead flat-lay shot looking straight down",
    "LOW": "low-angle shot taken at floor level",
}
LENS = {
    "ECU": "90mm macro, f/2.8, focus on the nearest surface",
    "CU": "85mm, f/2.0, shallow background",
    "MCU": "85mm, f/2.8",
    "MS": "50mm, f/2.8",
    "WS": "28mm, f/4, deep focus",
    "OH": "50mm, f/5.6, sensor parallel to the table",
    "LOW": "24mm, f/4, camera resting on the floor",
}

CHAR = ("a Japanese woman of sixty-nine, grey hair pinned back simply, a soft grey-blue "
        "cardigan over a pale blouse, calm patient face, small reading glasses on a cord")

# AN DU XUYEN BAI — cung mot goc may, lap 3 lan
SINK = "a home kitchen sink piled with unwashed bowls and plates after a meal"

# (line_idx, rank, SHOT, frame_note, SUBJECT, SETTING, LIGHT)
PLAN = [
    # ── COLD OPEN ───────────────────────────────────────────────────────────
    (0, "", "CU", "the plate of tempura fills the lower half cropped by the bottom edge, the clock standing whole behind it",
     "a plate of freshly fried tempura beside a round table clock whose hands point clearly to ten on a completely blank dial",
     "a family dining table at night", "one warm ceiling lamp from above, the room behind falling dark"),
    (2, "", "WS", "the window fills the upper frame, the tidy counter running along the bottom edge",
     "a quiet kitchen at eight in the morning, nothing cooking yet, one cup left out",
     "a Japanese home", "flat pale morning light through the window, no lamp on"),
    (4, "", "OH", "the breakfast tray fills the frame corner to corner",
     "a simple Japanese breakfast of rice, miso soup and grilled fish, chopsticks resting on the bowl rim",
     "a wooden table", "even morning light from above, soft shadows under the bowls"),
    (6, "", "ECU", "the paper fills the frame at a slight angle, one printed row circled in red pen, the printed characters too soft to read",
     "a health check-up result sheet with faint ruled rows and one row marked with a red pen circle, the print blurred and unreadable",
     "on a kitchen table", "raking window light from the left, the paper slightly creased"),
    (8, "", "MCU", "the hand and cup fill the centre, the cup already tilting, cropped by the bottom edge",
     "an elderly hand losing its grip on a teacup, the cup tipping",
     "at a low table in the morning", "soft window light from the right"),
    (11, "", "ECU", "the ankle fills the frame cropped by the bottom edge at the heel",
     "an elderly bare ankle with a deep sock elastic ring pressed into slightly swollen skin",
     "beside a low chair on a tatami floor", "one warm floor lamp low from the left"),
    (13, "", "MS", "the tin sits centre on the shelf, a hand entering from the right edge",
     "a hand reaching into an open sweets tin on a kitchen shelf in the afternoon",
     "a Japanese kitchen", "low afternoon sun coming in almost horizontally"),
    (16, "", "CU", "the clock face fills the right half, the calendar page blurred at the left edge",
     "a plain round wall clock with a completely blank dial beside a blank paper calendar page",
     "a kitchen wall", "even daylight, graphic and clean"),
    # ── ITEM1 · 四十時間 ─────────────────────────────────────────────────────
    (18, "", "OH", "the four empty plates sit in a row across the centre with clear space around each",
     "four identical empty white plates arranged in a straight row",
     "a wooden table", "flat even light from above, no strong shadow"),
    (20, "", "ECU", "the oil surface fills the frame, one ripple rising toward the top edge",
     "the surface of warm oil in a pan rising into a single slow swell",
     "on a stovetop", "hard overhead light catching the moving surface"),
    (22, "", "CU", "the hourglass stands centre cropped by the bottom edge, most of the sand still in the upper bulb",
     "a large hourglass with the sand only a third of the way down",
     "on a windowsill", "warm side light through the glass"),
    (28, "", "CU", "the small plate at the centre with a single peeled mandarin, clock blurred behind",
     "one peeled mandarin on a small plate with a table clock out of focus behind it",
     "a dining table in mid-afternoon", "warm low sun from the right"),
    (32, "", "CU", "the clock fills the frame, cropped by the left and right edges, dial completely blank",
     "a large round clock face with a blank dial and plain black hands",
     "a kitchen wall", "even light, no glare"),
    (35, "", "WS", "the sink runs from the left edge to the centre, dishes piled above the rim",
     SINK, "a Japanese kitchen after dinner", "one warm ceiling light, the window black behind"),
    (36, "", "MCU", "the intercom panel at the right edge, wet hands entering from the left edge",
     "a home intercom on the wall lighting up while a pair of wet hands is still holding a sponge",
     "a kitchen entrance", "warm indoor light, slight motion blur on the hands"),
    (37, "", "ECU", "the soapy hands fill the frame, cropped by both side edges",
     "two hands covered in white dish foam, held still",
     "over a kitchen sink", "cool daylight from a window above the sink"),
    (39, "", "OH", "three plates and one small saucer arranged around the centre",
     "three dinner plates and one small saucer laid out together on a table",
     "a wooden table", "even light from above"),
    (41, "", "CU", "the tap fills the upper frame, water running strongly into the sink cropped by the bottom edge",
     "a kitchen tap running water freely and generously",
     "a kitchen sink", "bright clean daylight from above"),
    (43, "", "MS", "the oil bottle small at the left edge, the clock large at the right edge",
     "a small bottle of cooking oil placed far from a large table clock, both on the same counter",
     "a kitchen counter", "flat side light, plain and clear"),
    (44, "", "OH", "twenty-four squares of a blank grid fill the frame corner to corner",
     "a hand-ruled blank paper grid of twenty-four empty squares, pencil lying across one corner",
     "on a kitchen table", "even daylight, the pencil casting one soft shadow"),
    (46, "", "CU", "the closed notebook at the centre, cropped by the bottom edge, pencil beside it",
     "a closed plain notebook with a pencil resting on the cover",
     "a kitchen table", "warm afternoon light from the left"),
    # ── PERSONA ─────────────────────────────────────────────────────────────
    (47, "", "WS", "the kitchen runs the full width, an apron hanging near the left edge",
     "a tidy home kitchen with an apron on a hook and a kettle on the stove, nobody present",
     "a Japanese home", "warm morning light through a window on the left"),
    (50, "", "CU", "the tray of home dishes at the centre, an empty medicine box pushed to the right edge",
     "a simple home meal tray in focus with an unopened pill organiser pushed away to the side",
     "a dining table", "warm even light from above"),
    (52, "", "CU", "the teacup at the left edge, a blank notepad running to the right edge",
     "a teacup of green tea and a small notepad with a pencil, the paper completely blank",
     "a kitchen table", "soft diffused window light from the left"),
    (54, "", "WS", "the window fills the right half, rooftops receding to the top edge",
     "a view over ordinary Japanese neighbourhood rooftops from a kitchen window",
     "a Japanese home", "clear plain afternoon light"),
    # ── フサ子さん NHIP 1 ───────────────────────────────────────────────────
    (56, "", "MS", "she sits in the left half, the window filling the right, cropped by the bottom edge",
     f"{CHAR}, sitting alone at a low table with both hands around a teacup",
     "a Japanese living room in the afternoon", "soft daylight from the window, one lamp not yet on"),
    (58, "", "WS", "the old post office counter runs from the left edge to the centre",
     "the wooden counter of a small old-fashioned Japanese post office, nobody present",
     "a neighbourhood post office", "warm nostalgic afternoon light through a shopfront window"),
    (60, "", "OH", "the plate fills the centre with clear space around it",
     "a small plate with one peeled mandarin, a cup of unsweetened yoghurt and three dried sardines",
     "a wooden table", "even soft light from above"),
    (62, "", "CU", "the parcel box at the centre cropped by the bottom edge, the packet of dried fish beside it",
     "an opened cardboard parcel from family with a packet of small dried sardines inside",
     "on a kitchen floor by the entrance", "warm hallway light from above"),
    (64, "", "ECU", "the result sheet fills the frame at a slight angle, one row circled in red, print unreadable",
     "a health check-up sheet with faint ruled rows, one row circled in red pen, the print soft and unreadable",
     "on a kitchen table", "flat window light from the left"),
    (65, "", "MCU", "she fills the right half, her hands in her lap, cropped by the left edge",
     f"{CHAR}, sitting with her hands folded in her lap, a small resigned smile",
     "a clinic waiting area", "cool even ceiling light"),
    (67, "", "MCU", "her hands fill the lower frame peeling a mandarin, the clock blurred at the top edge",
     f"{CHAR}, peeling a mandarin slowly with both hands",
     "a living room table at three in the afternoon", "warm low sun from the right"),
    (69, "", "OH", "the same plate as before, the three items in the same places",
     "the same small plate with a mandarin, yoghurt and dried sardines, unchanged",
     "a wooden table", "even soft light from above"),
    (72, "", "CU", "the clock fills the frame, the blank dial dead centre",
     "a plain table clock with a blank dial, seen straight on",
     "a kitchen shelf", "warm lamp light from the right"),
    # ── AN DU LON LEN: dau ngam vao tuong ───────────────────────────────────
    (75, "", "WS", "the sink at the centre, exactly the same angle as before, more dishes than before",
     f"{SINK}, the same camera position as earlier, the pile higher",
     "a Japanese kitchen", "the same warm ceiling light as before"),
    (77, "", "ECU", "the wall surface fills the frame, cropped by every edge",
     "a kitchen wall behind a stove with a faint yellow film of old oil, barely visible",
     "a Japanese kitchen", "raking side light revealing the film"),
    (79, "", "ECU", "the extractor fan blade fills the frame, a fingertip entering from the right edge",
     "a fingertip pressed against an extractor fan blade coated in hardened brown grease",
     "above a stove", "hard directional light showing the sticky texture"),
    (80, "", "ECU", "the cut hose fills the frame again, the same angle as the cold open, wall clearly thicker",
     "the same cut-open garden hose, its inner wall noticeably thicker and rougher than before",
     "on a workbench", "hard side light"),
    (82, "", "OH", "three meal trays plus one small plate arranged in a row across the frame",
     "three full meal trays and one small snack plate laid out in a line",
     "a wooden table", "even light from above"),
    # ── 原典 ────────────────────────────────────────────────────────────────
    (85, "", "CU", "the closed booklet at the centre cropped by the bottom edge, plain cover, no readable print",
     "a plain medical guideline booklet lying closed on a desk, its cover blank and matte",
     "a quiet desk", "even neutral daylight"),
    (87, "", "ECU", "the blood tube at the centre held upright, cropped by the bottom edge",
     "a single sealed blood sample tube held upright in a rack, no labels",
     "a clinic bench", "clean cool light from above"),
    (89, "", "ECU", "the ruled sheet fills the frame, one line drawn firmly across it in red, no readable print",
     "a blank ruled results form with a single red line drawn across one row",
     "on a desk", "flat even light"),
    (92, "", "MCU", "the two sheets side by side filling the frame, both blurred beyond reading",
     "two similar blank result sheets laid side by side for comparison",
     "on a table", "even daylight from above"),
    (95, "", "MS", "the drawer open at the bottom edge, hands lifting an envelope at the centre",
     "elderly hands lifting a plain envelope of old papers out of a drawer",
     "a Japanese living room chest", "warm afternoon light from the side"),
    (97, "", "ECU", "the corner of the sheet fills the frame, a fingertip resting beside a small printed block, print unreadable",
     "a fingertip resting next to a small printed block in the corner of a form, the characters too soft to read",
     "on a kitchen table", "raking light from the left"),
    (99, "", "MCU", "the same result sheet, now held up toward the window at the centre",
     "elderly hands holding a result sheet up toward the light of a window",
     "by a kitchen window", "bright backlight through the paper"),
    (101, "", "MS", "the smartphone flat at the centre of the table, a hand resting beside it",
     "a smartphone lying face up on a kotatsu table with an elderly hand resting near it",
     "a Japanese living room", "warm room light from above"),
    # ── 三つの「つい」 ───────────────────────────────────────────────────────
    (103, "", "OH", "three small plates in a row across the centre, evenly spaced",
     "three identical small empty plates arranged in a row",
     "a wooden table", "even light from above"),
    (105, "一つめ", "CU", "the mandarin and clock fill the frame together, clock hands clearly at three",
     "a peeled mandarin on a plate beside a table clock whose hands point to three on a blank dial",
     "a living room table", "warm afternoon sun from the right"),
    (111, "", "OH", "one long gap between trays, now broken in the middle by a small plate",
     "two meal trays far apart with one small snack plate placed exactly between them",
     "a wooden table", "even light from above"),
    (113, "", "MS", "the sink again at the same angle, a single small bowl added on top of the pile",
     f"{SINK}, one extra small bowl newly placed on top",
     "a Japanese kitchen", "the same warm ceiling light"),
    (116, "", "MS", "the tea things fill the centre, two cups, cropped by the bottom edge",
     "a teapot and two cups set out for an afternoon break, a plate of small sweets between them",
     "a Japanese living room table", "warm afternoon light through a lace curtain"),
    (118, "", "CU", "two cups on a tray at the centre, steam rising toward the top edge",
     "two cups of freshly poured green tea steaming on a small tray",
     "a low table", "backlit by low afternoon sun, the steam catching the light"),
    # ── つい② ───────────────────────────────────────────────────────────────
    (121, "二つめ", "CU", "the small dish at the left edge, the dark bedroom filling the right",
     "a small dish of rice crackers on a bedside table late at night",
     "a Japanese bedroom", "one weak bedside lamp, everything beyond it black"),
    (124, "", "CU", "the clock fills the right half, its dial blank, bedding blurred at the bottom edge",
     "a small alarm clock on a bedside table in a dark room",
     "a Japanese bedroom", "only a night light from below"),
    (126, "", "MCU", "the hand entering from the top edge, fingers over the cracker dish at the centre",
     "an elderly hand picking a single rice cracker from a dish late in the evening",
     "a living room table", "one warm lamp from the side, the room dim"),
    (128, "", "WS", "the room dark, the futon at the centre, one figure lying still",
     "a person lying asleep under a futon, the room completely still",
     "a tatami bedroom at night", "only faint moonlight, deep shadow"),
    (129, "", "LOW", "the corridor runs from the bottom edge to a lit door at the far end",
     "an empty dark hallway with one door left slightly open at the far end",
     "a Japanese house in the middle of the night", "faint light spilling from the far doorway only"),
    (131, "", "MCU", "the shoulders and lowered head fill the frame, cropped by the top edge",
     "an elderly person sitting on the edge of a bed in the morning, shoulders heavy, head lowered",
     "a bedroom at dawn", "pale grey morning light from a curtained window"),
    # ── つい③ ───────────────────────────────────────────────────────────────
    (134, "", "MS", "the two chairs face each other across the table, both empty, cropped by the bottom edge",
     "two dining chairs pulled up facing each other at a table set with two cups of tea",
     "a Japanese home in the afternoon", "warm side light through a lace curtain"),
    (137, "三つめ", "OH", "the tray at the centre holds only a coffee cup, the rest of the table bare",
     "a breakfast table with nothing on it but a single cup of black coffee",
     "a wooden table", "cool morning light from the left"),
    (139, "", "OH", "the long empty table runs from the left edge to the right edge, no dishes at all",
     "a completely empty dining table, wiped clean, nothing on it",
     "a Japanese dining room", "flat pale daylight"),
    (142, "", "CU", "the clock at the left edge and a second clock at the right edge, both dials blank",
     "two identical table clocks standing apart on the same counter, hands at different positions",
     "a kitchen counter", "even daylight, graphic and clean"),
    (144, "", "ECU", "the pan surface fills the frame, the oil swelling much higher than before",
     "the surface of oil in a pan rising into a tall sharp swell",
     "on a stovetop", "hard overhead light on the moving surface"),
    (147, "", "OH", "the lunch tray fills the frame, noticeably fuller than the earlier trays",
     "an unusually full Japanese lunch tray with a large bowl of rice and several side dishes",
     "a wooden table", "warm even light from above"),
    (149, "", "MCU", "the hand entering from the right edge toward the sweets tin at the centre",
     "an elderly hand reaching into a sweets tin again in the afternoon",
     "a kitchen shelf", "low afternoon sun from the left"),
    (152, "", "OH", "three items in a row: a mandarin, dried sardines and an empty coffee cup",
     "a mandarin, a small pile of dried sardines and an empty coffee cup arranged in a row",
     "a wooden table", "even light from above"),
    (155, "", "CU", "the mandarin at the left edge, a wrapped sweet pushed away at the right edge",
     "a peeled mandarin chosen and a wrapped sweet pushed aside",
     "a living room table", "warm afternoon light"),
    (157, "", "OH", "the small supper tray at the centre with a lot of empty table around it",
     "a very small evening meal of rice and pickles on a large empty table",
     "a Japanese dining room", "one warm ceiling lamp, the corners dim"),
    (161, "", "OH", "the same plate of three items again, exactly the same arrangement",
     "the same small plate with a mandarin, yoghurt and dried sardines, unchanged again",
     "a wooden table", "even soft light from above"),
    (164, "", "ECU", "the dried sardines fill the frame, cropped by both side edges",
     "a handful of small dried sardines seen extremely close, dry and silvery",
     "on a small plate", "hard side light showing the texture"),
    (166, "", "ECU", "the result sheet again, the same red circle, same angle as before",
     "the same health check-up sheet with the same red pen circle, print unreadable",
     "on a kitchen table", "flat window light from the left"),
    # ── CU LAT ──────────────────────────────────────────────────────────────
    (168, "", "MCU", "her hands folded on the table fill the lower frame, face cropped by the top edge",
     f"{CHAR}, hands folded on a table, sitting very still",
     "a Japanese living room", "soft window light from the left"),
    (171, "", "OH", "one mandarin sits alone in the middle of a wide empty table",
     "a single peeled mandarin placed exactly in the middle of a large empty table",
     "a wooden table", "one clean overhead light, strong empty space around it"),
    (173, "", "OH", "the mandarin now touching the edge of a full lunch tray at the left",
     "a mandarin placed right beside a full lunch tray, the two touching",
     "a wooden table", "even light from above"),
    (175, "", "MCU", "the shoulders relaxing, hands opening on the lap, cropped by the top edge",
     "an elderly person's shoulders dropping and hands opening in their lap, tension leaving",
     "a Japanese living room chair", "warm afternoon light from the side"),
    (178, "", "OH", "every dish still present on the table, nothing removed",
     "a complete home meal with a mandarin, sweets and tea all present together",
     "a wooden table", "warm inviting light from above"),
    # ── DEM 5 GIAY ──────────────────────────────────────────────────────────
    (181, "", "CU", "the wristwatch on the table at the left edge, a pencil at the right edge",
     "an old wristwatch lying flat on a table beside a pencil, blank dial",
     "a kitchen table", "soft daylight from the left"),
    (185, "", "OH", "six small marks spaced unevenly along one ruled line across the frame",
     "a hand-drawn horizontal line on plain paper with six pencil marks along it, no writing",
     "on a kitchen table", "even flat daylight"),
    (187, "", "OH", "six sink-loads of dishes crowding the frame to every edge",
     "an impossibly large pile of dishes from six separate meals crowded on one counter",
     "a Japanese kitchen", "flat overhead kitchen light"),
    # ── TRA LOOP · 器のルール ───────────────────────────────────────────────
    (189, "", "OH", "the empty grid again, now with three squares lightly shaded",
     "the same hand-ruled paper grid with three of the squares shaded in pencil",
     "a kitchen table", "even daylight"),
    (191, "", "MS", "the shopping bag folded at the left edge, the kitchen empty behind",
     "a folded empty shopping bag put away on a hook, nothing bought",
     "a Japanese kitchen entrance", "plain daylight"),
    (195, "", "OH", "the same table, the mandarin now placed on the tray beside the rice bowl",
     "the same laid table with a peeled mandarin added onto the tray beside the rice bowl",
     "a home dining room", "the same warm light from above"),
    (196, "", "MS", "hands lifting the tray away at the centre, the table clearing toward the bottom edge",
     "elderly hands carrying a tray of used dishes away from the table",
     "a home dining room", "warm ceiling light, slight motion in the hands"),
    (200, "一つめ", "OH", "the lunch tray at the centre with the mandarin resting on its edge",
     "a lunch tray still on the table with a peeled mandarin placed on its rim",
     "a wooden table", "warm midday light from above"),
    (204, "二つめ", "OH", "the dinner tray at the centre with a small dish of crackers set on it",
     "a dinner tray with a small dish of rice crackers placed on the same tray",
     "a home dining room", "warm lamp light from above"),
    (206, "", "WS", "the futon at the centre, the bedside table beside it now completely empty",
     "a neatly laid futon with an empty bedside table beside it, no plate, no crumbs",
     "a tatami bedroom at night", "one soft lamp, calm and dim"),
    (207, "三つめ", "OH", "the breakfast tray fills the frame, complete, with rice and soup",
     "a proper Japanese breakfast tray with rice, miso soup and a small side dish",
     "a wooden table", "clear morning light from above"),
    (209, "", "OH", "three trays in a row across the frame, no extra plate anywhere",
     "exactly three meal trays laid out in a row with nothing between them",
     "a wooden table", "even light from above"),
    (211, "", "OH", "the same three trays, each one just as full as before",
     "three full meal trays, generous portions, nothing reduced",
     "a wooden table", "warm even light"),
    (214, "", "CU", "the clock at the right edge showing nine, the dark window at the left",
     "a table clock beside a dark kitchen window at night, hands near nine on a blank dial",
     "a Japanese kitchen", "one warm lamp, the window black"),
    (217, "", "CU", "the small rice ball on a plate at the centre, cropped by the bottom edge",
     "half a rice ball on a small plate in the late afternoon",
     "a kitchen counter", "low warm sun from the right"),
    (219, "", "CU", "the pill organiser at the centre, cropped by the bottom edge, blank lids",
     "a weekly pill organiser with plain unmarked lids sitting closed on a table",
     "a kitchen table", "even neutral daylight"),
    (221, "", "MS", "two chairs facing each other across a desk, both empty",
     "two empty chairs facing each other across a small consulting desk",
     "a quiet clinic room", "cool even ceiling light"),
    # ── フサ子さん NHIP 2 · KET ─────────────────────────────────────────────
    (223, "", "MS", "she fills the centre at the table, the lunch tray still in front of her",
     f"{CHAR}, sitting at a table with her finished lunch tray still in front of her, peeling a mandarin",
     "a Japanese living room at midday", "bright natural light from the window"),
    (227, "", "MCU", "she fills the right half, her face turned toward the garden at the left edge",
     f"{CHAR}, standing at an open veranda door looking out at a small garden",
     "a Japanese house in the afternoon", "warm outdoor light falling on her face"),
    (228, "", "WS", "the garden fills the frame, the watering can at the bottom edge",
     "a small Japanese home garden with a watering can set down among potted plants",
     "outside a veranda", "bright clear afternoon sun"),
    (231, "", "MS", "she waters the plants at the centre, cropped by the bottom edge",
     f"{CHAR}, watering potted plants in her garden with a small can",
     "a small home garden", "warm late afternoon sun from behind"),
    (233, "", "ECU", "the ankle fills the frame again, the same angle as the cold open, the mark much fainter",
     "an elderly ankle with only a very faint sock mark, the skin looking easier",
     "beside a low chair on a tatami floor", "the same warm floor lamp from the left"),
    (235, "", "OH", "the lunch tray and the mandarin together at the centre with clear space around them",
     "a lunch tray with a mandarin on its rim, photographed simply and clearly",
     "a wooden table", "clean even light from above"),
    (238, "", "OH", "the tray at the centre, a hand placing the mandarin onto it from the right edge",
     "a hand setting a peeled mandarin onto a lunch tray that is still on the table",
     "a wooden table", "warm midday light"),
    (240, "", "CU", "two teacups at the centre, one slightly turned toward the viewer",
     "two teacups set out on a table as if for a conversation",
     "a Japanese living room", "soft afternoon light"),
    (244, "", "MS", "the two figures fill the lower frame from behind, the window bright at the top edge",
     "two elderly friends sitting together at a table sharing tea, seen from behind",
     "by a window in the afternoon", "backlit by warm afternoon sun, faces not visible"),
    (247, "", "MCU", "two hands passing a small wrapped parcel at the centre, cropped by the bottom edge",
     "an elderly hand passing a small wrapped box of food to another hand",
     "at a doorway of a Japanese home", "warm afternoon light from outside"),
    (249, "", "WS", "the kitchen runs the full width, everything put away, the counter bare",
     "a completely tidied kitchen in the evening, counter clear, one lamp on",
     "a Japanese home", "one warm lamp, calm and quiet"),
    (251, "", "MCU", "the hands lifting the last bowl at the centre, cropped by the bottom edge",
     "elderly hands lifting the last bowl from a table at the end of a meal",
     "a home dining room", "warm ceiling light"),
    (252, "", "MS", "the figure walking away from the camera along a bright hallway toward the far edge",
     "an elderly person walking steadily down a sunlit hallway, seen from behind",
     "a Japanese house in the morning", "bright natural morning light"),
    (255, "", "CU", "both hands resting on the table fill the lower frame, teacup at the right edge",
     "an elderly person's hands resting quietly on a table beside a teacup",
     "a dining table", "warm even light, peaceful and still"),
    (258, "", "MS", "two chairs at a low table, one teacup on each side",
     "a small table set with two cups as if a conversation is about to begin",
     "a quiet Japanese room", "soft daylight from a window"),
    (260, "", "OH", "the set dinner table fills the frame corner to corner",
     "a Japanese family dinner table set for the evening meal, rice, soup and small dishes",
     "a home dining room", "warm lamp light from directly above, inviting"),
]


# ── v2 · MODE BUILD-ON cho tung canh (make_shot) ──────────────────────────────
#   focus = chi dich danh (vong do ve dan)   inset = phong to mot chi tiet
#   wipe  = doi trang thai (anh B de len A)  soft  = cau ke (mac dinh)
MODES = {
    0: "focus", 2: "soft", 4: "inset", 6: "focus", 8: "inset", 11: "focus",
    13: "inset", 16: "soft", 18: "inset", 28: "focus", 35: "wipe", 37: "inset",
    39: "soft", 41: "inset", 44: "soft", 47: "soft", 50: "inset", 52: "soft",
    56: "soft", 58: "soft", 60: "inset", 62: "inset", 64: "focus", 65: "soft",
    67: "inset", 72: "focus", 75: "wipe", 77: "focus", 79: "inset", 80: "focus",
    82: "soft", 87: "inset", 92: "soft", 95: "soft", 97: "focus", 99: "inset",
    101: "soft", 103: "soft", 105: "focus", 113: "inset", 116: "soft", 118: "inset",
    121: "focus", 124: "soft", 126: "inset", 129: "soft", 131: "soft", 134: "soft",
    137: "focus", 139: "soft", 144: "inset", 147: "inset", 149: "inset", 155: "focus",
    157: "soft", 161: "soft", 164: "inset", 166: "focus", 168: "soft", 171: "focus",
    173: "wipe", 175: "soft", 178: "soft", 181: "inset", 189: "soft", 191: "soft",
    196: "wipe", 200: "focus", 204: "inset", 206: "soft", 207: "inset", 211: "soft",
    214: "focus", 217: "inset", 219: "focus", 221: "soft", 223: "inset", 227: "soft",
    228: "soft", 231: "soft", 233: "focus", 238: "inset", 240: "soft", 244: "soft",
    247: "inset", 249: "soft", 251: "inset", 255: "soft", 260: "soft",
    # 13 diem so lieu (v3): anh that + nhan so
    20: "inset", 22: "focus", 32: "focus", 43: "focus", 89: "focus", 111: "focus",
    128: "inset", 142: "focus", 152: "soft", 185: "focus", 195: "focus",
    209: "focus", 235: "soft",
}
# Bo bot cho thua (user chot: rut 110 -> ~85 entry, moi canh co build-on)
DROP = {54, 69, 105, 118, 139, 157, 191, 206, 221, 240, 249}

# ── v3 (user chot 2026-08-18: "khong dung anh viet bang slides, dung ANH THAT
#     roi them anh minh hoa hieu ung vao") ──────────────────────────────────────
# LOP THE CHU vox DA BI BO HAN. 13 diem so lieu gio la ANH THAT + NHAN SO de len,
# ve bang make_shot (hop nhan nho o duoi, xuat hien o giay 2.55) — annotate, khong
# phai slide. Dieu nay tra kenh ve dung media-library.md §2.9 (cam moi slide-chu).
VOX = {}

# line_idx -> nhan ngan de len anh (<=10 ky). Chi cho nhung cau CO SO.
LABELS = {
    20: "3〜4時間で山",
    22: "10時間",
    32: "24時間しかない",
    43: "4回",
    89: "175",
    111: "3時間と4時間",
    128: "8時間",
    142: "17時間",
    185: "4時間もない",
    195: "器のあいだだけ",
    209: "4回 → 3回",
}

# Anh cho 13 diem so lieu — SO PHAI NAM TRONG CHINH BUC ANH (vat dem duoc),
# nhan chi de xac nhan lai. (SHOT, frame, SUBJECT, SETTING, LIGHT)
NUMIMG = {
    20: ("MS", "three identical plates in a row from the left edge to the right edge, the third one pushed forward",
         "three identical dinner plates in a row, the first two empty and the third still full",
         "a wooden table", "warm even light from above"),
    22: ("CU", "the hourglass stands centre cropped by the bottom edge, sand a third down",
         "a large hourglass with the sand only a third of the way down",
         "on a windowsill beside a wall clock", "warm side light through the glass"),
    32: ("OH", "the table fills the frame, four meal trays crowded together with no gap between them",
         "four full meal trays pushed together on a table clearly too small for them, edges overlapping",
         "a wooden table", "flat even light from above"),
    43: ("OH", "four empty plates in a row across the centre with clear space around each",
         "four identical empty white plates in a straight row",
         "a wooden table", "flat even light from above, no strong shadow"),
    89: ("CU", "the closed booklet at the centre cropped by the bottom edge, cover blank",
         "a plain guideline booklet lying closed beside a blood sample tube, cover blank and matte, print unreadable",
         "a quiet clinic desk", "even neutral daylight"),
    111: ("OH", "one long table runs edge to edge, two trays far apart, one small plate exactly between them",
          "two meal trays at opposite ends of a long table with a single small snack plate in the middle",
          "a wooden table", "even light from above"),
    128: ("WS", "the futon at the centre, the bedside table beside it holding a small dish",
          "a laid futon at night with a small dish of rice crackers on the bedside table",
          "a tatami bedroom", "one weak bedside lamp, the rest black"),
    142: ("OH", "the empty table runs from edge to edge, one coffee cup alone at the centre",
          "a bare breakfast table with only a single cup of black coffee on it",
          "a wooden table", "cool morning light from the left"),
    152: ("OH", "three items in a row across the centre, evenly spaced",
          "a peeled mandarin, a small pile of dried sardines and an empty coffee cup in a row",
          "a wooden table", "even light from above"),
    185: ("OH", "six small plates spaced unevenly along one long table from the left edge to the right edge",
          "six small plates of different sizes spread along a long table, none of them far apart",
          "a wooden table", "even flat daylight"),
    195: ("OH", "the laid table fills the frame corner to corner, a mandarin resting on the tray rim",
          "a Japanese meal fully laid out with a peeled mandarin placed on the rim of the same tray",
          "a home dining room", "warm lamp light from directly above, inviting"),
    209: ("OH", "three meal trays in a row with nothing at all between them",
          "exactly three full meal trays laid out in a row, generous portions, no extra plate",
          "a wooden table", "warm even light from above"),
    235: ("CU", "both hands resting on the table fill the lower frame, teacup at the right edge",
          "an elderly person's hands resting quietly on a table beside a teacup",
          "a dining table", "warm even light, peaceful and still"),
}

# ── v4 · LOP FX + AVATAR (shot_fx.py, user: "them anh tao hieu ung va anh avatar,
#     nang tam cam xuc, hieu ung manh liet hon") ────────────────────────────────
#   stamp  = dong dau con SO chot        cross = cau phu dinh
#   smudge = vet muc, beat nang          tag   = cau chi dan
# FX thay cho `label` o 11 diem so lieu — dau dong manh hon nhan hop nho.
FX = {
    # cold open: cu xoan + cua tu
    2:   [dict(kind="stamp", text="8時", at=[0.72, 0.30], t=1.5)],
    6:   [dict(kind="cross", at=[0.30, 0.38], size=200, t=1.6)],
    16:  [dict(kind="stamp", text="40時間", at=[0.70, 0.28], t=1.5)],
    # ITEM1 · phep tinh
    20:  [dict(kind="stamp", text="3〜4時間", at=[0.30, 0.26], t=1.5)],
    22:  [dict(kind="stamp", text="10時間", at=[0.68, 0.30], t=1.4)],
    32:  [dict(kind="stamp", text="24時間", at=[0.26, 0.22], t=1.5),
          dict(kind="stamp", text="40時間ぶん", at=[0.72, 0.30], t=2.4)],
    43:  [dict(kind="stamp", text="4回", at=[0.72, 0.26], t=1.5)],
    # an du bep ngam dau
    77:  [dict(kind="tag", text="十年で取れなくなる", at=[0.50, 0.26], size=46, t=1.7)],
    # nguon
    89:  [dict(kind="stamp", text="175", at=[0.70, 0.32], t=1.6)],
    # ba cai "tui"
    111: [dict(kind="stamp", text="3+4時間", at=[0.28, 0.24], t=1.5),
          dict(kind="tag", text="ここで割れる", at=[0.60, 0.30], size=46, t=2.4)],
    128: [dict(kind="stamp", text="8時間", at=[0.30, 0.28], t=1.5)],
    142: [dict(kind="stamp", text="17時間", at=[0.70, 0.26], t=1.5)],
    # cu lat
    169: [dict(kind="tag", text="中身ではない", at=[0.44, 0.26], size=50, t=1.6)],
    171: [dict(kind="tag", text="置いた場所", at=[0.50, 0.30], size=52, t=1.6)],
    # dem 5 giay + payoff
    185: [dict(kind="stamp", text="4時間もない", at=[0.66, 0.26], t=1.6)],
    195: [dict(kind="tag", text="器のあいだだけ", at=[0.50, 0.26], size=56, t=1.5)],
    200: [dict(kind="tag", text="お昼の器と一緒に", at=[0.52, 0.28], size=48, t=1.6)],
    204: [dict(kind="tag", text="器を下げる前に", at=[0.50, 0.28], size=48, t=1.6)],
    209: [dict(kind="stamp", text="4回→3回", at=[0.68, 0.26], t=1.5)],
    # YMYL
    219: [dict(kind="tag", text="先生にご相談を", at=[0.50, 0.28], size=48, t=1.6)],
}

# AVATAR フサ子さん — nhan vat CASE (nguoi duoc KE VE), khong phai nguoi dan.
# ⚠️ Nguoi dan みのり CO Y KHONG co avatar: giong doc la NAM (青山龍星), gan mot
#    guong mat nu vao nguoi dan la lech; フサ子 thi hop vi ba la nhan vat trong chuyen.
AVATAR = {
    # 🔴 Anh NEN cua 5/6 slot nay VON DA la chinh ba cu (generator tra ve nguoi du
    #    prompt ta vat) -> dan them cutout = HAI ba giong het nhau trong mot khung.
    #    Bat duoc khi soi sheet 2026-08-18. Nen: canh nao nen DA CO NGUOI thi chi
    #    ve BONG BONG (figure=False); chi canh nen VAT moi dan cutout that.
    65:  dict(figure=False, side="left",
              bubble="先生には、様子を見ましょう、と言われるだけなのよ", bubble_t=2.0),
    161: dict(name="fusako_mandarin", side="left", h=0.82, t=1.1),      # nen = dia quyt (vat)
    227: dict(figure=False, side="left",
              bubble="三時になると、手持ちぶさたでねえ。かわりに、庭に出るようになったの",
              bubble_t=2.2),
    238: dict(name="fusako_tray", side="right", h=0.78, t=1.0),         # nen = mam com (vat)
}


# Anh B cua tung cap `wipe` (A -> B la DOI TRANG THAI, phai chi dinh tay:
# ban auto "clean, fresh" chi dung cho cap bep bua->sach).
WIPE_B = {
    35: ("the same sink from the SAME camera position, now empty and wiped",
         "an empty clean kitchen sink, every dish washed and put away on the rack"),
    75: ("the same wall and extractor hood from the SAME camera position, the film now heavy",
         "the same kitchen wall behind the stove, the oil film now thick, brown and sticky"),
    173: ("the same table from the SAME overhead position, the mandarin MOVED next to the tray",
          "the same mandarin, now resting against the rim of a full lunch tray instead of standing alone"),
    196: ("the same table from the SAME camera position, now cleared",
          "the same dining table with every dish taken away, wiped and completely bare"),
}

IMGDIR_ABS = str(VD / "slides_img_photo").replace("\\", "/")


def body_lines():
    out = []
    for ln in TTS.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"\[[^\]]*\]", "", s).strip()
        if s:
            out.append(s)
    return out


def build_blocks(shot, frame, subj, setting, light):
    return [
        ("SHOT", f"{SHOTS[shot]}, {frame}"),
        ("SUBJECT", subj),
        ("SETTING", setting),
        ("LIGHT", light),
        ("LENS", LENS[shot]),
        ("STYLE", STYLE),
        ("NEG", NEG),
    ]


def focus_of(mode, n):
    """Vong khoanh / tam inset — lech nhe theo n de 80 canh khong lap mot cho."""
    xs = [0.42, 0.54, 0.62, 0.48, 0.58]
    ys = [0.46, 0.52, 0.44, 0.55, 0.50]
    return [xs[n % 5], ys[n % 5], 0.17 if mode == "focus" else 0.13]


def main():
    lines = body_lines()
    starts, acc = [], 0.0
    for l in lines:
        starts.append(acc)
        acc += len(l) / CPS + PER_LINE
    total = acc

    # ── gom: PLAN (anh) + VOX (the so lieu), xep theo line_idx ────────────────
    items = []
    for idx, rank, shot, frame, subj, setting, light in PLAN:
        if idx in DROP or idx in NUMIMG:  # line so lieu -> dung anh rieng o NUMIMG
            continue
        items.append(("shot", idx, rank, shot, frame, subj, setting, light))
    for idx, art in NUMIMG.items():           # v3: diem so lieu = anh that + nhan
        shot, frame, subj, setting, light = art
        items.append(("shot", idx, "", shot, frame, subj, setting, light))
    items.sort(key=lambda x: x[1])

    errs, slides, flow, tenfile, blocks, voxflow = [], [], [], [], [], []
    seen, prev = set(), -999.0
    nimg = nvox = 0
    for n, it in enumerate(items):
        typ, idx = it[0], it[1]
        if idx >= len(lines):
            errs.append(f"entry {n}: line_idx {idx} vuot so dong ({len(lines)})")
            continue
        if idx in seen:
            errs.append(f"entry {n}: line_idx {idx} bi dung hai lan (shot va vox trung cho)")
        seen.add(idx)
        if starts[idx] - prev < 6.0:
            errs.append(f"entry {n} (line {idx}): cach entry truoc {starts[idx]-prev:.1f}s "
                        f"(<6s, audience-45plus 2)")
        prev = starts[idx]
        line = lines[idx]
        m = line.rstrip("。？」")
        if m not in line:
            errs.append(f"entry {n}: match khong phai substring")
        if sum(1 for l in lines if m in l) > 1:
            errs.append(f"entry {n}: match '{m[:18]}' khop NHIEU dong -> cue se nhay sai cho")
        mm, ss = int(starts[idx]) // 60, int(starts[idx]) % 60

        if typ == "shot":
            _, _, rank, shot, frame, subj, setting, light = it
            mode = MODES.get(idx, "soft")
            if shot not in SHOTS:
                errs.append(f"entry {n}: shot la {shot}")
            for bad in ("%", "two-thirds", "half of the frame width", "percent"):
                if bad in frame:
                    errs.append(f"entry {n}: SHOT ta ti le ('{bad}') — phai ta bang MEP KHUNG")
            fn = f"slide_{nimg:02d}.jpg"
            sp = {"mode": mode, "photo": fn}
            if mode in ("focus", "inset"):
                sp["focus"] = focus_of(mode, n)
            if mode == "inset":
                sp["inset_pos"] = ["bl", "br"][nimg % 2]
            if mode == "wipe":
                sp["photo2"] = f"slide_{nimg:02d}_b.jpg"
            if idx in FX:                     # v4: dau dong / X / vet muc / nhan
                sp["fx"] = FX[idx]
            elif idx in LABELS:               # con lai: nhan hop nho
                sp["label"] = LABELS[idx]
            if idx in AVATAR:                 # v4: nhan vat フサ子さん
                sp["avatar"] = dict(AVATAR[idx], channel="shokutaku")
            e = {"match": m, "photo": False, "video": True, "shot": sp}
            if rank:
                e["rank"] = rank
            slides.append(e)
            bl = build_blocks(shot, frame, subj, setting, light)
            flow.append(" ".join(f"{k}: {v}." for k, v in bl))
            tenfile.append(f"{fn}\t{mm:02d}:{ss:02d}\t{mode:5}\t{shot:3}\t{rank or '-':6}\t{line}")
            if mode == "wipe":
                if idx not in WIPE_B:
                    errs.append(f"entry {n} (line {idx}): mode wipe nhung thieu anh B trong WIPE_B")
                    continue
                fb, sb = WIPE_B[idx]
                bl2 = build_blocks(shot, fb, sb, setting, light)
                flow.append(" ".join(f"{k}: {v}." for k, v in bl2))
                tenfile.append(f"slide_{nimg:02d}_b.jpg\t{mm:02d}:{ss:02d}\twipe-B\t{shot:3}\t-     \t"
                               f"(anh B cua {fn})")
            blocks.append(
                f"### {fn} — {mm:02d}:{ss:02d} — **{mode}** — {shot}"
                + (f" — badge `{rank}`" if rank else "") + "\n"
                f"- cue: `{line}`\n\n```\n"
                + "\n".join(f"{k:<8}: {v}" for k, v in bl if k not in ("STYLE", "NEG"))
                + "\n```\n")
            nimg += 1
    if errs:
        print("[LOI] khong xuat file:")
        for e in errs:
            print("   ", e)
        return 1

    VD.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (VD / "slide_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "slide_prompts_TENFILE.txt").write_text(
        "ten file\tmoc\tmode\tshot/kind\tbadge\tcau cue trong _TTS.md\n" + "\n".join(tenfile) + "\n",
        encoding="utf-8")
    (VD / "slide_prompts_BLOCKS.md").write_text(
        f"# Video 17 — {len(slides)} entry (v2: build-on bang HINH + {nvox} the so lieu)\n\n"
        "> **Xuong = `make_shot.py`** (focus / inset / soft / wipe): khung DUNG YEN,\n"
        "> anh phu + vong do duoc LAP VAO theo loi doc (0,55s -> 1,70s -> dung im).\n"
        "> **Diem nhan = the `vox`** cho so lieu, moi the co nen ANH THAT.\n\n"
        "🔴 SHOT luon ta bang QUAN HE VOI MEP KHUNG, khong bao gio ta phan tram\n"
        "(`media-library.md` §2.10 ⑥). Tool co gate chan `%`.\n\n"
        "🔴 Giay to trong anh phai TRONG / khong doc duoc chu (`media-library.md` §2.10 ⑦).\n\n"
        f"**Anh can gen:** {nimg} anh slide (`slide_XX.jpg`, + `_b` cho wipe) trong\n"
        f"`slide_prompts_FLOW.txt`, va {nvox} anh nen the so lieu (`vox_XX.jpg`) trong\n"
        "`vox_prompts_FLOW.txt`. Hai file rieng vi anh vox nen THOANG hon (chu de len tren).\n\n"
        f"**LENS suy tu co canh:**\n\n"
        + "\n".join(f"- `{k}` ({SHOTS[k]}) -> {v}" for k, v in LENS.items())
        + f"\n\n**Nhan vat 中井フサ子さん:**\n\n> {CHAR}\n\n"
          f"**STYLE:** `{STYLE}`\n\n**NEG:** `{NEG}`\n\n---\n\n"
        + "\n".join(blocks), encoding="utf-8")

    n = len(slides)
    gaps = [starts[items[i][1]] - starts[items[i - 1][1]] for i in range(1, len(items))]
    from collections import Counter
    cm = Counter(MODES.get(i[1], "soft") for i in items if i[0] == "shot")
    ck = Counter(i[2]["kind"] for i in items if i[0] == "vox")
    print(f"OK  {n} entry ({nimg} shot + {nvox} vox) | video ~{int(total)//60}'{int(total)%60:02d}")
    print(f"    {total/n:.1f} giay/entry | {n/(total/60):.2f} doi hinh/phut  (tran 6/phut)")
    print(f"    gap nho nhat {min(gaps):.1f}s | gap lon nhat {max(gaps):.1f}s")
    print(f"    vox = {nvox}/{n} = {nvox/n*100:.0f}%  (co-dai video 22: 16%)")
    print("    mode: " + " ".join(f"{k}={v}" for k, v in cm.most_common()))
    print("    kind: " + " ".join(f"{k}={v}" for k, v in ck.most_common()))
    nfx = sum(1 for i in items if i[1] in FX)
    nav = sum(1 for i in items if i[1] in AVATAR)
    print(f"    FX: {nfx} canh ({sum(len(v) for k, v in FX.items() if any(i[1] == k for i in items))} "
          f"hieu ung) | AVATAR: {nav} canh")
    wipes = sum(1 for i in items if i[0] == "shot" and MODES.get(i[1]) == "wipe")
    print(f"    ANH CAN GEN: {nimg + wipes} slide (co {wipes} anh B cho wipe) + {nvox} vox = "
          f"{nimg + wipes + nvox}")
    for f in (OUT_JSON, VD / "slide_prompts_FLOW.txt",
              VD / "slide_prompts_TENFILE.txt", VD / "slide_prompts_BLOCKS.md"):
        print(f"    -> {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
