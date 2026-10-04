# -*- coding: utf-8 -*-
r"""Dung SLIDES + 3 file prompt anh cho video 16 (バナナ x 夜のトイレ).
Prompt viet theo VAN PHAP STORYBOARD (khoi SHOT / SUBJECT / SETTING / LIGHT / LENS).

    python tools\build_slides_16.py

Xuat:
  04_SCRIPTS/16_banana-yoru-toire_SLIDES_photo.json     (renderer doc)
  06_VIDEO/16_banana-yoru-toire/slide_prompts_FLOW.txt      (1 prompt / 1 DONG -> bom extension)
  06_VIDEO/16_banana-yoru-toire/slide_prompts_TENFILE.txt   (ten file <-> moc <-> cue)
  06_VIDEO/16_banana-yoru-toire/slide_prompts_BLOCKS.md     (ban nguoi doc, giu dang KHOI)

── VAN PHAP STORYBOARD (chot 2026-08-16) ──────────────────────────────────────
  SHOT    : co canh + QUAN HE VOI MEP KHUNG   <- khong bao gio ta phan tram
  SUBJECT : chu the + hanh dong
  SETTING : boi canh
  LIGHT   : nguon sang + huong + chat sang     <- tung anh tu quyet (1/3 la canh dem)
  LENS    : suy tu co canh, bang LENS[]        <- may quyet, nguoi khong phai nghi
  STYLE   : hang so, giong nhau ca 93 anh
  NEG     : hang so

  🔴 Vi sao FRAMING phai ta bang MEP KHUNG: media-library.md 2.10 muc 6 do duoc
     "model nghe VI TRI, khong nghe TI LE" (xin `filling the LEFT two-thirds` ->
     tra ve nguoi toan than NHO). Nen viet `cropped by the bottom edge at the ankle`,
     KHONG viet `chiem 60% khung`.
  🔴 FLOW.txt nen ve 1 DONG (extension bom ca file); BLOCKS.md giu dang khoi de nguoi
     doc va sua. Cung khuon voi prompt thumbnail (ab-3title-3thumb.md 3.1 Buoc 4).

── Luat da ap ────────────────────────────────────────────────────────────────
  - match = nguyen van 1 DONG trong _TTS.md (bo dau cau cuoi) -> chac chan la substring
  - moi entry cach entry truoc >= 6 giay, mat do <= 6 doi hinh/phut (audience-45plus.md 2)
  - entry 0 = CHU THE = QUA CHUOI + dong ho 2 gio (media-library.md 2.0)
  - 100% ANH, KHONG slide-chu nao (media-library.md 2.9)
  - nhan vat 静江さん dung CUNG MOT cau ta o moi slot -> nhan ra la mot nguoi
  - badge `rank` CHI cho 3 loi an chuoi (一つめ/二つめ/三つめ)
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "16_banana-yoru-toire_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "16_banana-yoru-toire_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "16_banana-yoru-toire"

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

CHAR = ("a Japanese woman in her early seventies, silver-grey hair cut short, soft lilac "
        "cardigan over a cream blouse, gentle tired eyes, no glasses")

# (line_idx, rank, SHOT, frame_note, SUBJECT, SETTING, LIGHT)
PLAN = [
    # ── COLD OPEN ────────────────────────────────────────────────────────────
    (0, "", "CU", "the banana fills the lower half and is cropped by the left edge; the clock stands behind it, whole",
     "one ripe yellow banana on a small white plate, and a round twin-bell alarm clock whose hands point clearly to two o'clock on a completely blank dial",
     "a wooden kitchen counter at night, dark window behind", "a single warm ceiling lamp from above, everything else falling into shadow"),
    (3, "", "ECU", "the ankle fills the frame and is cropped by the bottom edge at the heel",
     "an elderly bare ankle with a deep sock elastic ring pressed into slightly swollen skin, the sock rolled down around the foot",
     "beside a low chair on a tatami floor", "one warm floor lamp low and from the left, long soft shadow"),
    (6, "", "LOW", "the corridor runs from the bottom edge to a door at the far end, floorboards filling the lower third",
     "an empty dark hallway, one sliding door left slightly open at the far end",
     "a Japanese house in the middle of the night", "faint blue moonlight only, no lamp, deep shadow"),
    (9, "", "MS", "the shoes sit on the step at the bottom edge, the door filling the frame behind them",
     "an unused pair of walking shoes and a walking cane leaning against the wall",
     "the entryway step of a Japanese house", "thin cold daylight through frosted glass"),
    (12, "", "CU", "the glass stands just left of centre, cropped by the bottom edge, clock blurred behind",
     "a full glass of water sitting completely untouched", "a bedside table at night",
     "one small bedside lamp from the right, the room behind it dark"),
    (16, "", "MS", "the basket sits centre, one banana lying loose in the foreground cropped by the bottom edge",
     "a bunch of ripe bananas in a woven basket, one banana separated and lying in front",
     "a kitchen counter", "low late-afternoon sun coming in almost horizontally from the left"),
    (20, "", "MS", "the clock high in the frame near the top edge, the empty chair below it cropped by the bottom edge",
     "a plain round wall clock and an empty wooden dining chair beneath it",
     "a Japanese kitchen wall", "long low afternoon sun raking across the wall"),
    # ── KHOI 1 · NUOC BI NGHI OAN ────────────────────────────────────────────
    (22, "", "MCU", "the hand enters from the right edge, the glass sits centre still full",
     "an elderly hand pushing a full glass of water gently away across the table",
     "a dining table", "flat afternoon daylight from a window behind"),
    (26, "", "CU", "the glass stands centre on the rack, cropped by the bottom edge",
     "an empty water glass turned upside down on a draining rack, completely dry",
     "beside a kitchen sink", "cool overcast daylight from the window above the sink"),
    (30, "", "MS", "the armchair fills the right half, the newspaper slipping out of frame at the bottom edge",
     "an elderly person dozing off in an armchair, head tilted back, an unread newspaper sliding off the lap",
     "a Japanese living room in the afternoon", "bright hazy daylight through a thin curtain"),
    (32, "", "MCU", "the hand and forehead fill the upper frame, the face half cut by the top edge",
     "an elderly person's hand pressed against their own forehead while seated",
     "at a dining table in the late afternoon", "warm low sun from the side, heavy shadow under the brow"),
    (35, "", "MS", "eight glasses in one unbroken row spanning the frame from the left edge to the right edge",
     "eight identical clear glasses of water lined up in a row",
     "a wooden kitchen counter", "even flat daylight, no strong shadow, graphic and clean"),
    (37, "", "WS", "the futon runs diagonally from the bottom edge to the upper right",
     "an empty futon with the covers thrown back and a faint body impression left in the sheet",
     "a tatami bedroom in the morning", "pale dawn light through paper screens"),
    (40, "", "ECU", "the drain hole sits dead centre and fills most of the frame",
     "a stainless sink drain with water flowing generously and freely down it",
     "a kitchen sink", "bright clean daylight from directly above"),
    (42, "", "ECU", "the same drain hole dead centre, same distance, filling most of the frame",
     "the same stainless sink drain with only a weak thin trickle, tea leaves and debris caught around the opening",
     "a kitchen sink", "dull cool light, flatter and greyer than the previous shot"),
    (45, "", "WS", "the window runs from the top edge down to the counter, which is cut by the bottom edge",
     "a still kitchen before sunrise, one lamp not yet switched on",
     "a Japanese kitchen", "blue-grey pre-dawn light only, no warm source"),
    (49, "", "ECU", "the drop hangs at the centre against darkness, tap cropped by the top edge",
     "a single drop of water hanging from a tap, caught the instant before it falls",
     "over a kitchen sink", "one hard side light, black background"),
    (54, "", "CU", "the clock face fills the right half, bedding blurred across the bottom edge",
     "a small alarm clock on a bedside table, its blank dial faintly lit",
     "a dark bedroom", "only a night light from below, everything else black"),
    # ── PERSONA ──────────────────────────────────────────────────────────────
    (57, "", "WS", "the kitchen runs the full width, apron hanging near the left edge",
     "a tidy home kitchen with an apron on a hook and a kettle on the stove, nobody present",
     "a Japanese home", "warm morning light through a window on the left"),
    (61, "", "OH", "the tray fills the frame, chopsticks crossing from the lower left corner",
     "a simple Japanese home dinner of rice, miso soup and one small side dish, chopsticks on the bowl rim",
     "a wooden table", "warm lamp light from above, soft shadows under the bowls"),
    (64, "", "CU", "the teacup at the left edge, the blank notepad running from the centre to the right edge",
     "a teacup of green tea and a small notepad with a pencil, the paper completely blank",
     "a kitchen table", "soft diffused window light from the left"),
    # ── 静江さん NHIP 1 ──────────────────────────────────────────────────────
    (67, "", "MS", "she sits in the left half, the window filling the right, her body cropped by the bottom edge",
     f"{CHAR}, sitting alone at a low table with both hands around a teacup, looking out of the window",
     "a Japanese living room at dusk", "fading orange daylight from the window, one lamp not yet on"),
    (70, "", "CU", "the night light glows at the centre, shoes lined up along the bottom edge",
     "a small plug-in night light glowing, neatly arranged shoes below it",
     "the entryway of a Japanese house", "the night light is the only source, everything beyond it black"),
    (72, "", "MS", "she stands in the right half, her head near the top edge, corridor receding to the left",
     f"{CHAR}, in a nightgown standing in a dark hallway, one hand flat on the wall",
     "a Japanese house at night", "only the entryway night light, weak and from behind her"),
    (75, "", "WS", "the salon chair centre, the mirror filling the wall behind it edge to edge",
     "an old hairdressing salon chair beside a large mirror, scissors and combs on the counter, nobody present",
     "a small neighbourhood beauty salon", "warm nostalgic afternoon light through a shopfront window"),
    (79, "", "ECU", "the calf fills the frame vertically, cropped by both the top and bottom edges",
     "an elderly woman's calf and ankle in the evening, sock rolled down, a sharp red elastic groove circling slightly swollen skin",
     "seated indoors", "one warm indoor lamp raking across the skin from the left"),
    # ── CHINH DIEN: CHAN LA THU PHAM ────────────────────────────────────────
    (84, "", "MS", "she sits in the centre, feet on the floor at the bottom edge, bed cropped by the right edge",
     f"{CHAR}, sitting on the edge of a bed at night with shoulders slumped, feet flat on the floor",
     "a bedroom at night", "one small lamp beside her, the rest of the room dark"),
    (88, "", "WS", "the lit doorway is a bright rectangle at the far end, dark room framing all four edges",
     "a bathroom doorway glowing with light at the end of a dark corridor",
     "seen from inside a dark bedroom", "hard light spilling from the doorway only, everything else black"),
    (91, "", "MS", "the figure fills the right half from behind, cropped at the shoulders by the top edge",
     "an elderly person standing at a kitchen counter preparing vegetables, seen from behind at waist height",
     "a home kitchen", "ordinary flat daytime light from the window ahead"),
    (94, "", "CU", "both feet fill the frame side by side, cropped by the bottom edge, slippers at the right edge",
     "two bare elderly feet and ankles on a wooden floor in the evening, visibly puffier than they would be in the morning, slippers just removed",
     "a Japanese living room", "one warm floor lamp from the right, low and soft"),
    (98, "", "ECU", "the shin and thumb fill the frame, cropped by the left and bottom edges",
     "an elderly person's thumb pressing firmly into the front of their own lower shin, trouser leg rolled up",
     "seated on a chair indoors", "one warm indoor lamp from the left, texture of the skin clearly visible"),
    (99, "", "ECU", "the same shin at the same distance, the dent dead centre",
     "a lower leg just after the thumb has been lifted, a clear round dent still remaining in the skin",
     "seated on a chair indoors", "the same warm indoor lamp from the left"),
    (101, "", "CU", "both ankles side by side cropped by the bottom edge, the bags hanging just below them",
     "two soft translucent pouches of water hanging from thin cords tied around a pair of bare ankles, gently swollen skin above them, quiet and matter-of-fact rather than surreal",
     "standing on a wooden floor indoors", "warm even indoor light, soft shadow under the pouches"),
    (103, "", "WS", "the feet are nearest camera at the bottom edge, the body receding to the top edge",
     "an elderly person lying on a futon at night seen from the feet end, blanket pulled up",
     "a tatami bedroom", "one dim lamp beside the futon, deep shadow in the corners"),
    (105, "", "ECU", "the tube runs diagonally from the lower left corner to the upper right",
     "clear water moving through a soft translucent tube, gentle and unhurried, abstract",
     "against a plain dark background", "one warm rim light from behind, edge of the tube glowing"),
    (107, "", "WS", "the door gap is a bright vertical slit slightly left of centre, floor filling the bottom edge",
     "a toilet door left ajar with light spilling out onto the corridor floor, slippers set in front of it",
     "a Japanese house at night", "light from behind the door only"),
    (110, "", "WS", "the counter runs the full width, the clock high near the top right edge",
     "a kitchen with a clock on the wall and a kettle steaming gently, nobody present",
     "a Japanese home at four in the afternoon", "long low sunlight raking horizontally across the counter"),
    (115, "", "CU", "the phone lies flat centre with a dark screen, teacup cropped by the right edge",
     "a smartphone lying face up on a table beside a teacup, an elderly hand resting near it",
     "a kotatsu table", "warm evening room light from above"),
    # ── BANANA · KALI · GENTEN ───────────────────────────────────────────────
    (116, "", "CU", "the banana stands upright dead centre, its tip near the top edge",
     "one ripe banana standing upright in a small ceramic bowl", "a kitchen counter",
     "warm late-afternoon sun from the left, one clean highlight down the peel"),
    (119, "", "CU", "the salt cellar at the left edge, the glass at the right, empty space between them",
     "a small ceramic salt cellar and a glass of water standing side by side",
     "a wooden table", "even daylight from above, minimal shadow"),
    (121, "", "MCU", "the hand enters from the top edge, the banana lifted clear of the basket at centre",
     "an elderly hand lifting a single banana out of a fruit basket",
     "a kitchen counter", "warm afternoon light from the left"),
    (123, "", "CU", "the scale fills the lower frame cropped by the bottom edge, the banana lying across it",
     "a banana lying on a small flat kitchen scale with a plain white blank dial showing nothing",
     "a kitchen counter", "bright even daylight, no glare on the dial"),
    (126, "", "OH", "the plate fills the frame, the opened peel curling toward the lower right corner",
     "a peeled banana lying on a plain white plate beside its opened skin",
     "a kitchen table", "bright even light from above, soft shadow under the plate"),
    (128, "", "OH", "three separate trays in one unbroken row from the left edge to the right edge",
     "breakfast, lunch and dinner of one ordinary day laid out side by side as three separate trays",
     "a long wooden table", "flat even daylight, all three trays lit the same"),
    (130, "", "OH", "the day's meals spread across the whole frame, the single banana small near the bottom edge",
     "one banana placed beside a full day of home meals arranged together, the banana visibly small among them",
     "a large table", "even flat daylight"),
    (134, "", "WS", "the sink with waiting dishes at the left edge, the stove at the right, room running the full width",
     "a tired kitchen in the early evening, dishes waiting in the sink, one pot on the stove",
     "a Japanese home", "the light going orange, one ceiling lamp just switched on"),
    (138, "", "CU", "the hand and banana fill the frame, cropped by the bottom edge at the wrist",
     "an elderly hand peeling a banana with one hand, the peel opening cleanly",
     "over a kitchen counter", "warm light from the left, clean and simple"),
    (141, "", "MCU", "both hands and the bag fill the lower frame, cropped by the bottom edge",
     "an elderly person's hands resting on a small folded paper pharmacy bag, plain and unmarked",
     "a dining table", "calm even daylight, no drama"),
    (145, "", "CU", "two cups side by side at centre, window blown out behind them at the top edge",
     "two teacups of warm tea with steam rising", "a wooden table by a window",
     "backlit by low afternoon sun, the steam catching the light"),
    # ── BA LOI AN CHUOI ──────────────────────────────────────────────────────
    (149, "", "CU", "the banana lies centre with folded reading glasses beside it, bedding blurred at the top edge",
     "a ripe banana resting on a bedside table beside a folded pair of reading glasses",
     "a bedroom at night", "one bedside lamp from the right, warm and small"),
    (152, "一つめ", "MCU", "the hand enters from the right edge reaching toward the banana at centre-left",
     "an elderly hand reaching for a banana on a bedside table in the dark, futon already laid out behind",
     "a bedroom at night", "only the bedside lamp, a pool of light around the table"),
    (156, "", "CU", "the watch at the left edge, the banana crossing to the right edge",
     "a wristwatch with a plain blank face lying beside a banana",
     "a kitchen counter", "soft evening light from above"),
    (158, "", "CU", "the palm and banana fill the frame, cropped by the bottom edge at the wrist",
     "a banana resting in an open palm, photographed straight on to show its weight and thickness",
     "against a plain neutral background", "one strong side light from the left, the far side falling dark"),
    (160, "", "ECU", "the cut face fills the whole frame edge to edge",
     "a banana cut straight through, the moist dense flesh and its water sheen filling the view",
     "on a cutting board", "one hard raking light from the left picking up the moisture"),
    (163, "", "CU", "the clock fills the centre, the rest of the frame black to all four edges",
     "a bedside alarm clock with a plain blank dial, barely visible",
     "a completely dark bedroom", "almost no light, one faint glow on the dial"),
    (166, "", "MS", "the figure sits centre, feet searching at the bottom edge, room dark to the edges",
     "an elderly person sitting up on the edge of the futon in the middle of the night, feet searching for slippers",
     "a tatami bedroom", "only a night light from the corridor"),
    (168, "", "CU", "the cup and toothbrush at the left, the banana peel draped over the basin edge at the right",
     "a toothbrush standing in a cup by a bathroom mirror with a banana peel on the edge of the basin",
     "a small bathroom at night", "one harsh overhead bathroom light, cold and unflattering"),
    (171, "", "CU", "the feet enter from the top edge, floorboards running to all other edges",
     "bare feet stepping onto a cold dark wooden hallway floor, seen from above",
     "a Japanese house at night", "faint blue light only, the floor looking cold"),
    (172, "二つめ", "CU", "two bananas lying side by side across the frame, one cropped by the right edge",
     "two ripe bananas side by side, one already peeled halfway",
     "a kitchen counter", "warm even daylight"),
    (176, "", "OH", "the rice bowl at the left, the banana at the right, chopsticks bridging them",
     "a banana beside a rice bowl filled to exactly half, chopsticks laid across the bowl",
     "a wooden table", "warm even light from above"),
    (178, "", "CU", "three bananas stacked and cropped by the right edge, plate cut by the bottom edge",
     "three bananas piled on a plate, slightly too many for one person",
     "a dining table", "even light, plain background"),
    (181, "", "OH", "one banana alone dead centre, generous empty table on all four sides",
     "a single banana on a clean white plate, nothing else",
     "a wooden table", "calm even daylight, one soft shadow"),
    (183, "三つめ", "CU", "the blender jug fills the frame, cropped by the top edge at the rim",
     "a kitchen blender jug holding banana chunks, milk and yoghurt, not yet blended",
     "a kitchen counter", "bright morning light from the right"),
    (186, "", "CU", "the glass stands centre, cropped by the top edge, straw leaning to the right",
     "a tall glass of thick pale banana smoothie with a straw in it",
     "a kitchen counter", "bright morning light from the left"),
    (188, "", "CU", "the glass fills the frame from the bottom edge to near the top edge, seen dead level",
     "a full glass of milky smoothie photographed from the side so the sheer volume of liquid is obvious",
     "against a plain background", "flat cool light, no distraction"),
    (192, "", "MS", "she fills the left half, plate at the bottom edge, room falling away to the right",
     f"{CHAR}, sitting on a dining chair eating a piece of banana slowly, shoulders relaxed",
     "a home dining room", "warm afternoon light from a window on the left"),
    (196, "", "OH", "the plate fills the frame, the fork entering from the lower right corner",
     "a banana cut into neat round slices arranged on a small plate with a fork beside it",
     "a wooden table", "warm evening lamp light from above"),
    # ── CU LAT ───────────────────────────────────────────────────────────────
    (198, "", "WS", "the chair sits left of centre, its long shadow running to the bottom edge",
     "an empty kitchen chair pulled out from the table, nobody there",
     "a Japanese kitchen in the late afternoon", "one low sun from the right throwing a long shadow"),
    (200, "", "CU", "the glass at the left edge, the banana at the right, both untouched at centre depth",
     "a full water glass and a banana standing side by side on a bedside table, neither touched",
     "a bedroom at night", "one bedside lamp, small warm pool of light"),
    (204, "", "WS", "the bar of sunlight runs from the left edge diagonally to the lower right",
     "a long bar of warm sunlight falling across an empty tatami floor",
     "a Japanese living room in the late afternoon", "low direct sun through a window, dust visible in the beam"),
    (209, "", "WS", "the kitchen runs the full width, the clock near the top right edge",
     "a bright kitchen fully awake in the afternoon, everything warm and in order, nobody present",
     "a Japanese home", "strong warm late-afternoon light filling the room"),
    # ── TRA LOOP: 夕方の十分 ─────────────────────────────────────────────────
    (212, "", "WS", "two chairs face each other across the centre, table cropped by the left edge",
     "two wooden dining chairs facing one another, empty and waiting",
     "a Japanese dining room at four in the afternoon", "low sun through a lace curtain, soft pattern on the floor"),
    (216, "", "CU", "the clock fills the right half, sunlight falling across the wall to the left edge",
     "a plain wall clock in a warm kitchen reading late afternoon",
     "a kitchen wall", "low sun raking across the wall from the left"),
    (220, "", "MS", "seen from the side, the seated body at the left edge, both feet raised at centre, knees clearly higher than the hips",
     "an elderly person seated on a dining chair with both feet resting up on the opposite chair on two folded floor cushions",
     "a home dining room", "warm afternoon light from a window behind"),
    (223, "", "MS", "she fills the right half, her raised feet cropped by the left edge, plate on her lap",
     f"{CHAR}, sitting with her feet up on the opposite chair, holding a peeled banana and taking a small bite",
     "a home dining room", "soft afternoon light through a lace curtain"),
    (227, "", "CU", "the cup sits centre cropped by the bottom edge, steam rising toward the top edge",
     "a small ceramic cup of warm barley tea steaming gently",
     "a dining table in the late afternoon", "backlit by low sun, the steam catching the light"),
    (230, "", "MS", "the emptied plate and cup at the bottom edge, raised feet still visible at the left edge",
     "an empty plate with a folded banana peel and a drained teacup, the feet still resting on the opposite chair",
     "a home dining room", "warm late light from the window"),
    (233, "", "CU", "both feet fill the frame resting on the cushion, cropped by the left and right edges",
     "two elderly feet resting relaxed on a folded cushion on a chair",
     "a home dining room", "warm low sunlight falling directly across them"),
    (236, "", "WS", "the window fills the right half, the chair and cushion in the foreground at the left edge",
     "a living room as the sun sets outside the window, a chair and cushion in the foreground",
     "a Japanese home", "strong orange sunset light flooding in from the right"),
    (239, "", "WS", "the figure is small at the centre with the street receding to the top edge",
     "an elderly person walking slowly along a residential street, seen from behind",
     "an ordinary Japanese neighbourhood in the early afternoon", "bright open daylight, clear and plain"),
    (243, "", "WS", "the window fills the upper frame, the tidy counter running along the bottom edge",
     "a kitchen window showing the last daylight of the evening, the room still bright and tidy inside",
     "a Japanese home", "the last daylight outside plus one warm ceiling lamp inside"),
    # ── 静江さん NHIP 2 ──────────────────────────────────────────────────────
    (245, "", "MS", "she fills the centre, feet up on a low stool cropped by the bottom edge",
     f"{CHAR}, sitting in her living room armchair with her feet up on a low stool and a plate on her lap",
     "a Japanese living room in the evening", "warm room lamp plus a faint flicker from an off-screen television"),
    (248, "", "CU", "the plate on the knees fills the lower frame, hands relaxed at the left and right edges",
     "a small plate resting on someone's knees with a peeled banana on it, hands resting easily at the sides",
     "a living room armchair", "warm indoor lamp light from above"),
    (252, "", "WS", "the night light glows small at the left edge while morning light floods the corridor to the right",
     "a plug-in night light still switched on, but the corridor beyond already full of morning light",
     "the entryway of a Japanese house", "bright natural morning light overpowering the little lamp"),
    # ── DINH BAI · RECAP · KET ───────────────────────────────────────────────
    (254, "", "WS", "the neat bedding runs diagonally from the bottom edge to the upper right, undisturbed",
     "an untouched futon in the early morning, the bedding still neat, nobody having got up in the night",
     "a tatami bedroom", "clean morning sunlight falling across it through paper screens"),
    (257, "", "WS", "the hallway runs from the bottom edge to the far end, slippers at the right edge",
     "warm morning sunlight lying across a wooden hallway floor, slippers set neatly to one side, nobody there",
     "a Japanese house", "direct morning sun through a side window"),
    (260, "", "OH", "the three objects sit in a row across the centre with clear space around each",
     "a banana, a cup of barley tea and a folded cushion arranged simply side by side",
     "a wooden dining table in the late afternoon", "warm even light from above"),
    (264, "", "WS", "one chair at the left edge, the second being drawn up to face it at the centre",
     "a second dining chair pulled up to face the first one, nobody in the frame",
     "a warm Japanese kitchen", "low afternoon sun from the right"),
    (267, "", "CU", "the small alarm clock at the left edge, the phone lying flat at the right, hand entering from the bottom edge",
     "a small alarm clock with a blank dial standing next to a smartphone lying face up, an elderly hand resting between them",
     "a kotatsu table in the evening", "warm room light from above"),
    (271, "", "WS", "the open window fills the right half, the fruit basket on the counter at the left edge",
     "a bright kitchen with the window open and the curtain lifting slightly, a fruit basket on the counter",
     "a Japanese home in the morning", "fresh clear morning light pouring in"),
    (273, "", "MS", "the two figures fill the lower frame from behind, the window bright at the top edge",
     "two elderly friends sitting together at a table sharing tea, seen from behind",
     "by a window in the afternoon", "backlit by warm afternoon sun, faces not visible"),
    (276, "", "WS", "the low table at the centre, the room falling softly dark toward all edges",
     "a calm living room in the evening with a teacup and folded reading glasses on a low table",
     "a Japanese home", "one soft lamp in the corner, everything else gently dim"),
    (279, "", "CU", "both hands fill the lower frame, the teacup at the right edge",
     "an elderly person's hands resting quietly on a table beside a teacup",
     "a dining table", "warm even light, peaceful and still"),
    (281, "", "OH", "the set table fills the frame corner to corner",
     "a Japanese family dinner table set for the evening meal with rice, soup and small dishes",
     "a home dining room", "warm lamp light from directly above, inviting"),
]


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


def main():
    body = body_lines()
    raw = TTS.read_text(encoding="utf-8")
    starts, t = [], 0.0
    for b in body:
        starts.append(t)
        t += len(b) / CPS + PER_LINE
    total = t

    slides, flow, tenfile, blocks = [], [], [], []
    prev, errs, seen = -99.0, [], set()
    for n, (idx, rank, shot, frame, subj, setting, light) in enumerate(PLAN):
        if idx >= len(body):
            errs.append(f"entry {n}: line index {idx} vuot so dong ({len(body)})")
            continue
        if idx in seen:
            errs.append(f"entry {n}: line index {idx} bi dung 2 lan")
        seen.add(idx)
        if shot not in SHOTS:
            errs.append(f"entry {n}: shot code la '{shot}', khong co trong SHOTS")
            continue
        line = body[idx]
        match = line.rstrip("。")
        if match not in raw:
            errs.append(f"entry {n}: match KHONG phai substring -> {match}")
        gap = starts[idx] - prev
        if gap < 6:
            errs.append(f"entry {n} (dong {idx}, {starts[idx]:.0f}s): cach entry truoc {gap:.1f}s < 6s")
        prev = starts[idx]
        if re.search(r"\d+\s*%|percent|two-thirds|half the frame width", frame):
            errs.append(f"entry {n}: SHOT ta TI LE -> phai ta bang MEP KHUNG (media-library 2.10-6)")

        e = {"match": match, "photo": True, "q": "AI-GEN"}
        if rank:
            e["rank"] = rank
        slides.append(e)

        bl = build_blocks(shot, frame, subj, setting, light)
        flow.append(" ".join(f"{k}: {v}." for k, v in bl))
        mm, ss = int(starts[idx]) // 60, int(starts[idx]) % 60
        tenfile.append(f"slide_{n:02d}.jpg\t{mm:02d}:{ss:02d}\t{shot:3}\t{rank or '-':6}\t{line}")
        blocks.append(
            f"### slide_{n:02d}.jpg — {mm:02d}:{ss:02d} — {shot}"
            + (f" — badge `{rank}`" if rank else "") + "\n"
            f"- cue: `{line}`\n\n```\n"
            + "\n".join(f"{k:<8}: {v}" for k, v in bl if k not in ("STYLE", "NEG"))
            + "\n```\n")

    if errs:
        print("[LOI] khong xuat file:")
        for e in errs:
            print("   ", e)
        return 1

    VD.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (VD / "slide_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "slide_prompts_TENFILE.txt").write_text(
        "ten file\tmoc\tshot\tbadge\tcau cue trong _TTS.md\n" + "\n".join(tenfile) + "\n",
        encoding="utf-8")
    (VD / "slide_prompts_BLOCKS.md").write_text(
        f"# Video 16 — {len(slides)} shot (van phap STORYBOARD)\n\n"
        "> Moi prompt = 7 khoi: **SHOT / SUBJECT / SETTING / LIGHT / LENS / STYLE / NEG**.\n"
        "> Duoi day chi in 5 khoi dau (STYLE va NEG giong het nhau o ca 93 shot, ghi mot lan o cuoi).\n"
        "> `slide_prompts_FLOW.txt` la dung noi dung nay nen ve **1 dong / 1 prompt** cho extension.\n\n"
        "🔴 **SHOT luon ta bang QUAN HE VOI MEP KHUNG, khong bao gio ta phan tram.**\n"
        "Do duoc o `media-library.md` §2.10 ⑥: model **nghe VI TRI, khong nghe TI LE**\n"
        "(xin `filling the LEFT two-thirds` -> tra ve nguoi toan than NHO, vi tri dung co sai).\n"
        "Tool co gate chan cac chuoi `%` / `two-thirds` trong khoi SHOT.\n\n"
        f"**LENS suy tu co canh (may quyet, nguoi khong phai nghi):**\n\n"
        + "\n".join(f"- `{k}` ({SHOTS[k]}) -> {v}" for k, v in LENS.items())
        + f"\n\n**Nhan vat 静江さん** (cung mot cau ta o moi slot, de nhan ra la mot nguoi):\n\n"
          f"> {CHAR}\n\n"
          f"**STYLE (hang so):** `{STYLE}`\n\n**NEG (hang so):** `{NEG}`\n\n---\n\n"
        + "\n".join(blocks), encoding="utf-8")

    n = len(slides)
    gaps = [starts[PLAN[i][0]] - starts[PLAN[i - 1][0]] for i in range(1, len(PLAN))]
    lens_ = [len(p) for p in flow]
    from collections import Counter
    cnt = Counter(p[2] for p in PLAN)
    print(f"OK  {n} shot | video ~{int(total)//60}'{int(total)%60:02d}")
    print(f"    {total/n:.1f} giay/anh | {n/(total/60):.2f} doi hinh/phut  (tran 6/phut)")
    print(f"    gap nho nhat {min(gaps):.1f}s (tran duoi 6s) | gap lon nhat {max(gaps):.1f}s")
    print(f"    prompt: ngan nhat {min(lens_)} ky | dai nhat {max(lens_)} ky | trung binh {sum(lens_)//n}")
    print("    co canh: " + " ".join(f"{k}={cnt[k]}" for k in SHOTS if cnt[k]))
    print(f"    badge: " + " ".join(f"{r}={sum(1 for s in slides if s.get('rank')==r)}"
                                    for r in ["一つめ", "二つめ", "三つめ"]))
    for f in (OUT_JSON, VD / "slide_prompts_FLOW.txt",
              VD / "slide_prompts_TENFILE.txt", VD / "slide_prompts_BLOCKS.md"):
        print(f"    -> {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
