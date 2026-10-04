# -*- coding: utf-8 -*-
r"""_scenes20_human.py — lop CON NGUOI cho prompt video 20 (ap SAU `_scenes20_real`).

User chot 2026-09-03, sau khi doc prompt shot 1 (hanh lang + phong bi roi):
   *"video cua toi dai 8s. Toi muon prompt no phai la mot cai gi do kieu nhu
    hien thuc chu khong phai tao ra chi can nem cho no hanh dong. Toi muon no
    nhu hoat dong binh thuong cua con nguoi"*

🔴 HAI BENH CUA BAN TRUOC (nhin thang, khong bao chua):
  ① **Khong co nguoi trong khung.** Hanh lang trong, phong bi "tu roi", anh sang
     "tu sang len", rem "tu lay". Do la anh tinh bi rung, khong phai con nguoi.
     ~30/83 shot la vat-khong-nguoi hoac chi micro-motion (xu "tu" xep, den LED
     "tu" bat). Voi 8 giay, "nhe nhang" = "chet".
  ② **Viet nhu lenh may.** `PERFORMANCE:` `CONTINUITY:` "nothing may read as a
     frozen still" "put all the movement in the first four seconds". Nguoi that
     khong dien theo nhan. Va no lai la MAT DO RANG BUOC — thu `_policy20.py` §②
     vua canh bao.

📐 KHUON MOI — MOT NGUOI, MOT VIEC, TRON 8 GIAY:
  · Anh tinh (`sc`) PHAI co nguoi o **tu the BAT DAU** cua viec do. i2v khong
    tu sinh ra nguoi khong co trong anh — muon co nguoi nhat phong bi thi anh
    phai co nguoi dang buoc toi phong bi.
  · Chuyen dong (`mo`) viet nhu **mot dong trong kich ban quay phim tai lieu**:
    "She walks the last two steps, bends, picks the envelope up, straightens,
    turns it over to read the front, and turns back toward the corridor."
    Ba nhip tu nhien: **toi → lam → dung lai**. Khong nhan, khong "PERFORMANCE".
  · Viec phai la viec **nguoi ta thuc su lam** voi vat do: nhat thu, mo thu,
    deo kinh, lat mat sau, dem xu, bat cong tac, lau kinh, roi tra. Khong co
    "anh sang dich chuyen", khong co "bui bay".
  · Ca video la nguoi ke chuyen doc; **nhan vat khong noi** (mieng ngam) — nhung
    ho duoc lam moi thu khac.
  · Hai shot co y de TRONG nguoi (`anata`: phong khach vang) van them mot ban tay
    dat tach tra roi rut di — su vang mat chi doc ra duoc khi CO nguoi vua roi.

⚖️ Bo luat "don chuyen dong vao 4 giay dau" cua video 19 — nó sinh ra tu benh
   AI het da o nua sau clip, nhung cach chua dung la cho no MOT VIEC TRON VEN
   de lam suot 8 giay (toi → lam → dung), khong phai nhoi nhanh roi de trong.

Cach dung: HUMAN[key] ghi de `sc`/`mo`/`cast`/`hands` LEN TREN ket qua cua
`_scenes20_real`. Key nao khong co o day thi giu nguyen.
"""

HUMAN = {

# ───────────────────────── COLD OPEN ─────────────────────────────────────
"todoku": dict(cast="W1", props=["P_ENV"],
    sc="the entrance hall of a quiet Japanese house in the morning, seen from "
       "inside: a woman of 66 in a grey-blue cardigan has just stepped into the "
       "hall from the corridor and is looking down at a single white window "
       "envelope lying on the polished wooden floor by the door, one hand "
       "resting on the wall, soft daylight through the frosted glass",
    mo="She walks the last two steps to the door, steadies herself with one hand "
       "on the wall, bends at the knees and picks the envelope up off the floor. "
       "She straightens slowly, turns the envelope over to look at the front, "
       "stands a moment reading the address, then turns back toward the "
       "corridor with it in her hand."),

"hiraku": dict(
    mo="She unfolds the letter with both hands and smooths it flat on the table, "
       "then takes her reading glasses down from her head and puts them on. She "
       "leans in, one finger tracing down the page, and stops partway. She reads "
       "that line again, then sits back a little in her chair."),

"meutagau": dict(
    mo="She reads the line once more, her eyes moving along it, then lifts them "
       "off the page and looks at nothing for a moment. Her hand comes up to her "
       "mouth. She looks back down, turns the sheet over to check the back, "
       "turns it face up again and lays it flat on the table."),

"hazu": dict(
    mo="She walks up to the wall calendar with the letter in one hand, lifts the "
       "page to glance at the month underneath, lets it fall back, and taps the "
       "ringed date with a finger. She looks from the calendar down to the "
       "letter and back up, then turns away toward the table."),

"anata": dict(hands="W1", props=["P_LIVING", "P_ENV"],
    sc="an ordinary Japanese living room at dusk with nobody sitting in it: one "
       "white window envelope lies unopened in the middle of the low table, two "
       "cups set out, the television dark, the last daylight coming in low "
       "through the window; a woman's hand and cardigan sleeve are just "
       "entering the frame at the side, setting a fresh cup of tea down",
    mo="She sets the cup down, notices the envelope, picks it up and turns it "
       "over to read the front. She stands holding it for a moment, then puts "
       "it back down unopened exactly where it was, squares it with two "
       "fingers, and leaves the room the way she came."),

"taishou": dict(
    mo="He steps out of the door, turns back to say a word to someone inside "
       "and raises a hand in a small wave, tucks his tie into his jacket with "
       "the other hand, then walks down the two steps and off along the street. "
       "The door swings slowly closed behind him."),

"taishou_b": dict(
    mo="She stands in the open doorway looking down the empty street, then "
       "looks at the envelope in her hands and turns it over. She tucks it "
       "under her arm, steps back inside, and pulls the door shut behind her."),

"naze": dict(
    mo="She sits with her chin on her hands looking at the letter, then reaches "
       "for her pen, pulls a notepad across, and writes a short line. She "
       "underlines it, puts the pen down, and looks at the letter again with "
       "her head tilted."),

"omoichigai": dict(hands="W1",
    sc="an overhead view of the kitchen table: the printed letter lies flat, and "
       "beside it a woman's hands hold a pencil over a small ruled notebook on "
       "which a simple shape has been sketched, morning light across the wood",
    mo="She draws a small box on the notebook page, looks at it, crosses it out "
       "with two quick strokes, and starts a fresh sketch beside it — a longer, "
       "wider shape. She taps the pencil on the page twice and puts it down."),

"yonbunno3": dict(
    sc="a close overhead shot of a plain round rice cake on a pale ceramic plate "
       "on the kitchen table; an elderly woman's hands hold a small kitchen "
       "knife above it, about to cut, a folded cloth beside the plate",
    mo="She cuts the rice cake into quarters with two clean strokes, wipes the "
       "blade on the cloth, then slides three of the pieces to one side of the "
       "plate with the flat of the knife and leaves the fourth where it is. She "
       "sets the knife down and looks at the plate."),

"nanno": dict(cast="M3", hands=None,
    sc="the researcher in a charcoal cardigan seated at his study desk with the "
       "wooden model house in front of him, both floors unlit, and two identical "
       "kraft envelopes lying on the desk — one beside the ground floor, one "
       "beside the upper floor; he is reaching toward them",
    mo="He picks up the envelope beside the ground floor, weighs it in his hand, "
       "sets it back, picks up the one beside the upper floor, then holds them "
       "both side by side and looks from one to the other. He puts them down "
       "together in front of the model and sits back."),

"keisan": dict(
    mo="She types a figure into the calculator, writes the result in the "
       "notebook, types the next, writes again, then runs her finger down the "
       "column she has written and circles the last number. She takes her "
       "glasses off and rubs her eyes."),

"kenkyu": dict(
    mo="He types a few keys, waits for the page, then turns the laptop toward "
       "the camera with both hands and adjusts the screen angle. He picks up "
       "his pen and points its cap at one part of the page, then looks up at "
       "the camera and gives a small nod."),

"kenkyu_b": dict(
    mo="His finger traces slowly along one row of the web page, pauses, taps "
       "twice on one spot, then he scrolls the page down a little on the "
       "trackpad and traces the next row. He picks up his pen and makes a "
       "short note on the pad beside the laptop."),

# ───────────────────────── 第1章 二階建て ─────────────────────────────────
"nikaidate": dict(hands="M3",
    sc="the wooden two-storey model house on the study desk under the window, "
       "an elderly man's hands just setting it down in the middle of the desk, "
       "its two interior lights still off, soft daylight",
    mo="He sets the model down in the middle of the desk and squares it with "
       "both hands, then reaches behind it and flicks a small switch — the "
       "lights inside both floors come on. He rests his hands on the desk "
       "either side of the model."),

"ikkai": dict(hands="M3",
    mo="He reaches behind the model and switches the upper floor's light off so "
       "only the ground floor glows, then lays a line of coins one after "
       "another along the desk in front of the model, each clicking down "
       "beside the last. He straightens the row with a fingertip."),

"nikai": dict(hands="M3",
    mo="He switches the ground floor's light off and the upper floor's on, then "
       "sets a small stack of coins on the balcony ledge of the upper floor and "
       "adds two more on top one at a time. He steadies the stack with a "
       "fingertip and takes his hand away."),

"awaseta": dict(hands="M3",
    mo="He switches both lights on so the whole house glows, then takes the "
       "folded reading glasses and the wristwatch from the corner of the desk "
       "and lays them together on the cloth beside the model. He squares them "
       "with a fingertip, sits back, and looks at the desk."),

"dochira": dict(cast="W1", hands=None,
    sc="the 66-year-old woman seated across the study desk from the camera, the "
       "wooden model house between her and the viewer with both lights off; she "
       "is reaching toward it, her hand hovering between the two floors",
    mo="Her hand hovers by the upper floor, lowers to the ground floor, comes "
       "back up — then she draws it back into her lap and looks across the desk "
       "toward the researcher, waiting for the answer."),

"nikai_dake": dict(
    mo="He puts both hands on the upper floor of the model, lifts it clear of the "
       "house, and holds it up at chest height with its light still glowing. He "
       "turns it slightly so the camera sees the whole piece, then holds it "
       "steady above the dark ground floor."),

"ikkai_hairanai": dict(hands="M3",
    mo="He sets the lit upper floor down at the top of the desk, picks up a "
       "plain grey card, and lays it flat over the roof line of the dark "
       "ground floor, squaring it with two fingers. He sits back and folds his "
       "hands."),

"gokai_shin": dict(
    mo="He gestures toward the dark ground floor with an open hand and shakes "
       "his head slightly, then holds up one finger and points from the ground "
       "floor to the lit upper floor and back. He rests his hand flat on the "
       "desk beside the model."),

"zero": dict(
    sc="the researcher's hands lifting the dark ground-floor block of the model "
       "off the desk, the lit upper floor already set to one side on the bare "
       "desktop, a clean rectangle of dust where the block stood, hard side light",
    mo="He lifts the ground-floor block off the desk with both hands, turns, and "
       "sets it down on a chair out of frame. He comes back, looks at the upper "
       "floor standing alone on the bare desk, and brushes the dust rectangle "
       "where the block had been with his palm."),

"hikitsugarenai": dict(cast="W1",
    sc="a quiet corner of a Japanese home: the 66-year-old woman kneeling in "
       "front of a small dark-wood shelf that holds a plain wooden picture "
       "frame standing turned well away from the camera, only its back and edge "
       "visible, beside a single white flower in a slim vase; she holds a small "
       "water jug, soft afternoon light from the side",
    mo="She tops up the water in the vase from the jug, sets the jug down on the "
       "floor, brushes a little dust from the shelf with her fingertips, and "
       "rests her hands on her knees for a moment before pushing herself up to "
       "stand."),

# ───────────────────────── 第2章 佐藤さん ─────────────────────────────────
"sato": dict(
    mo="She turns from the window, walks to the table, pulls out a chair and "
       "sits down, smoothing her cardigan. She folds her hands on the table and "
       "looks toward the camera with a small polite smile, glances down, and "
       "looks up again."),

"sato_boutou": dict(
    mo="She picks up the folded letter, opens it, and reads it once more — "
       "calmer this time — then folds it back along its crease and sets it to "
       "one side. She reaches for her tea, takes a sip, and puts the cup down."),

"furikomi": dict(
    mo="She unfolds the wide slip and smooths it flat with both hands, puts her "
       "glasses on, and runs her finger along the top row of the table, then "
       "down the left column, stopping at one entry. She taps it twice and "
       "looks up."),

"jibun_kiso": dict(
    mo="Her finger moves from the first row down to the second, separate row "
       "and rests there. She picks up a pencil, draws a small tick beside that "
       "row, then a bracket around it, and sets the pencil down."),

"mangaku": dict(hands="W1",
    sc="a close shot on the kitchen table of an elderly woman's hands counting "
       "brass coins from a loose pile onto a neat stack, evenly lit",
    mo="She counts coins onto the stack one at a time from the pile beside it — "
       "five, six, seven — then squares the stack between her palms, pushes the "
       "leftover coins to one side, and rests her hands on the table."),

"chigau": dict(
    mo="She lifts the cup with both hands, blows across it, takes a small sip "
       "and sets it down. She glances at the papers pushed aside, pulls one "
       "back toward her, looks at it, and pushes it away again with a small "
       "shake of her head and the beginning of a smile."),

"chigau_b": dict(
    mo="She crosses out the old figure in the notebook with a single line, "
       "writes a new one underneath, and underlines it. She closes the "
       "notebook, lays her pen on top, and rests her hand on the cover."),

# ───────────────────────── 第3章 遺族基礎年金 ─────────────────────────────
"kodomo": dict(
    mo="She sits looking at the two empty places, then leans across and "
       "straightens the small bowls and chopsticks so they sit square. She "
       "picks up her own bowl, holds it in both hands without eating, and sets "
       "it down again."),

"izoku_kiso": dict(hands="M3",
    mo="He switches on the ground floor's light, then picks up two small card "
       "standees from beside the model and stands them in the doorway one at a "
       "time, steadying each until it stops rocking. He looks at them and gives "
       "a small nod."),

"izoku_kiso_b": dict(
    mo="She counts a stack of coins onto the desk in front of the two small "
       "standees one coin at a time, then squares the stack and pushes it a "
       "little closer to them. She rests her fingertips on the desk beside it."),

"jyuhassai": dict(cast="K1",
    sc="the mother in her late thirties reaching up to a cream wall calendar "
       "with a red pen, about to ring the last date on the page; beside the "
       "calendar a dark navy jacket hangs on a hook, cool clear daylight",
    mo="She rings the last date on the calendar with the red pen, caps the pen, "
       "then turns to the jacket on its hook, brushes the shoulder flat with her "
       "hand, and straightens it on the hanger."),

"sotsugyou": dict(
    mo="She stands at the gateway holding the paper tube, looks down the road, "
       "takes a few slow steps forward, stops, and turns the tube over in her "
       "hands. Petals drift past; she brushes one from her sleeve."),

"kakei_kawaru": dict(
    mo="She turns a page of the account book, runs her finger down a column, "
       "picks up the calculator and types a figure, writes the result, then "
       "sits back with the pen held against her lips, looking at the page."),

"seikei": dict(cast="W1",
    sc="the 66-year-old woman at her kitchen table in the morning setting a "
       "second place across from her own — a second rice bowl in her hands, "
       "chopsticks and one shared teapot already on the table",
    mo="She sets the second rice bowl down across from her own, lays the "
       "chopsticks on their rest, pours tea into both cups from the pot, and "
       "sits down at her own place with her hands beside her bowl."),

"happyakugojuu": dict(
    mo="She lays the wooden ruler across the printed sheet, slides it down to "
       "one line and holds it there, running her finger along its edge. She "
       "picks up a pencil, draws a short line along the ruler, and lifts the "
       "ruler away."),

"mikomi": dict(
    mo="She holds the ruler in place with one hand and with the other pencils a "
       "series of dots stepping down from the top left toward the ruler, then "
       "carries the last dots past it and below the line. She sets the pencil "
       "down and looks at the page."),

"junban": dict(hands="M3",
    sc="a low shot along the study desk: an elderly man's hands are placing "
       "small hand-cut card standees of family figures in a single-file row "
       "from front to back, four already standing, two still in his hand",
    mo="He places the last two standees at the back of the row, nudges each "
       "into line, then bends down to look along the row at eye level and "
       "straightens the front one with a fingertip."),

"junban_b": dict(hands="M3",
    mo="He slides the front standee onto the pencilled cross, moves the second "
       "up close behind it, adjusts the gap with two fingers, and taps the "
       "cross beside the front one."),

"saki_no_juni": dict(hands="M3",
    mo="He picks up a white envelope, moves it along the row past each standee "
       "without stopping, and leans it against the front figure's base. He "
       "shows an empty palm to the rest of the row and lets his hand drop."),

# ───────────────────────── CTA ────────────────────────────────────────────
"cta": dict(
    mo="The husband leans forward and taps the tablet screen, the wife leans "
       "in to look and laughs at something on it; he nods, reaches for his "
       "teacup, and sits back. She pats his knee."),

"cta_b": dict(
    mo="She holds the tablet up between them; he points at the screen, she nods "
       "and taps it, and they both smile. She lowers the tablet to her lap and "
       "looks at him."),

"cta_c": dict(hands=None,
    sc="a close shot of the low living-room table: the tablet lying flat with a "
       "soft glow, two teacups, a small notepad and a pen; an elderly woman's "
       "hand in a lilac sleeve is reaching for the pen, warm lamplight",
    mo="She picks up the pen, writes a short line on the notepad, and sets the "
       "pen back down. Her other hand lifts one teacup out of frame, and a "
       "moment later sets it back, a little emptier."),

"cta_d": dict(
    mo="He gives a thumbs-up toward the tablet; she laughs and pushes his hand "
       "down gently; he laughs too, and they settle back into the sofa "
       "together, her hand on his forearm."),

# ───────────────────────── 第4章 六十五歳の段差 ───────────────────────────
"dansa": dict(
    sc="a real outdoor concrete staircase between two levels of a Japanese "
       "housing estate, pale walls either side and open sky above; the "
       "66-year-old woman is climbing the last steps toward a small landing "
       "that then drops ONE step down to a lower terrace, a shopping bag on "
       "her shoulder",
    mo="She climbs the last two steps to the landing, pauses at the edge and "
       "looks down at the single step below, puts a hand on the wall, and steps "
       "carefully down onto the lower terrace. She stands there and looks back "
       "up."),

"dansa_b": dict(
    mo="She turns to look back up at the landing, rests a hand on the wall, "
       "then faces forward again, shifts the bag on her shoulder, and walks "
       "slowly on out of frame."),

"madoguchi": dict(
    mo="She walks up to the counter, sets her notebook and folded letter down, "
       "pushes them a little toward the far side, and clasps her hands in front "
       "of her. She glances up at the sign boards and back down, waiting."),

"kotae": dict(
    mo="The staff member picks up the letter, reads it, sets it down and turns "
       "it to face the woman, then points to one line and traces along it. She "
       "shakes her head gently and opens her hand — not a mistake — then folds "
       "her hands on the counter."),

"owatta": dict(
    mo="She looks down at the letter on the counter, nods slowly twice, picks up "
       "the notebook and the letter and holds them against her chest. She "
       "thanks the staff member with a small bow and turns away from the "
       "counter."),

"kafu_kasan": dict(
    mo="She picks up the leaflet, turns it toward herself and reads, then "
       "underlines one line with the pencil from the counter. She turns the "
       "leaflet toward the camera and taps the underlined line."),

"yonjuu_rokujuugo": dict(
    mo="He uncaps the orange marker, sets the tip at the first tick, and draws a "
       "thick bar steadily along the guide line to the second tick. He caps the "
       "marker, steps back half a pace, and points at the two ends of the bar "
       "in turn."),

"uwanose": dict(hands="M3",
    sc="a close shot on the study desk of an elderly man's hands holding a "
       "small stack of brass coins just above a taller stack already standing "
       "there, about to set it on top, even soft light",
    mo="He sets the smaller stack squarely on top of the existing stack and "
       "adjusts it until it sits straight. He runs a finger up the side of the "
       "combined column and taps the top."),

"keikateki": dict(
    mo="He holds the marker on its edge just past the second tick and draws a "
       "thin narrow line onward a short way. He caps it, points at the thick "
       "bar and then at the thin line, and gives a small shrug."),

"keikateki_b": dict(hands="M3",
    sc="a close desk shot of an elderly man's hands laying a yellowed calendar "
       "page from decades ago flat on the wooden desk, a ruler and a pencil "
       "beside it, warm lamp light",
    mo="He sets a ruler vertically on the old calendar page between two "
       "columns, draws a firm pencil line down the page along it, lifts the "
       "ruler away, and taps the left side of the line."),

"mikkosare": dict(
    mo="He pulls the leaflet toward him, picks up the magnifying glass, and "
       "moves it slowly down the page to the small print at the bottom. He "
       "stops, leans in closer, reads, then looks up over his glasses at the "
       "camera."),

"nijuunen": dict(
    sc="the researcher at the whiteboard, a bold red vertical line already "
       "drawn on it and one thick orange bar running across and past the red "
       "line; he holds the orange marker at the start of a second bar below "
       "the first",
    mo="He draws the lower orange bar steadily toward the red line and stops a "
       "hand's width short of it. He caps the marker and holds his palm up flat "
       "in the gap between the end of the bar and the red line."),

"tsukanai": dict(
    mo="She reaches for the smaller stack of coins to set it on top of the "
       "larger one, stops, and instead carries it back to the side and out of "
       "frame. She looks at the single stack left standing and rests her hand "
       "flat beside it."),

"kekka_kawaru": dict(hands="M3",
    sc="two identical sets of keepsakes laid side by side on the study desk — "
       "each a pair of folded reading glasses and a worn wristwatch on its own "
       "small cloth; an elderly man's hands are placing a stack of brass coins "
       "in front of the left set, the space in front of the right one bare",
    mo="He sets the coin stack down in front of the left set, then moves his "
       "hand across to the space in front of the right one, hesitates there, "
       "and takes it away empty. He rests both hands on the desk."),

"teikibin": dict(
    mo="She unfolds the pale-blue leaflet, puts on her glasses, and runs her "
       "finger along the boxed rows to one section. She pulls the tablet "
       "closer, taps the screen, and looks between the leaflet and the screen."),

"riyuu": dict(
    mo="Her eyes stop on one point; she reads it again, then sits back a little "
       "and breathes out. She takes her glasses off, holds them in one hand, "
       "and looks at the leaflet a long moment before nodding to herself."),

# ───────────────────────── 第5章 働いても増えない ─────────────────────────
"mittsume": dict(
    mo="He turns to a fresh page, flattens it, writes a short heading at the "
       "top and underlines it, and sets the pen down across the page. He looks "
       "up at the camera and briefly raises three fingers."),

"super": dict(
    mo="She lifts daikon from the crate two at a time and lays them in a neat "
       "row on the display, turns one so the leaves face the same way as the "
       "others, wipes her hands on her apron, and reaches for the next crate."),

"fueru": dict(
    mo="She sets coins one at a time onto the growing stack from a small pile "
       "at her side, pausing between each, then squares the stack between her "
       "fingers and pushes it a little forward."),

"tedori": dict(
    mo="She writes a figure in the notebook, looks up and smiles slightly to "
       "herself, taps the pen against the page, then adds another figure under "
       "the first and draws a line beneath both."),

"naranai": dict(
    mo="She looks down at the two figures and her smile fades; she draws a slow "
       "line through the second one, sets the pen down, and sits back with her "
       "hands in her lap, looking at the page."),

"sousai": dict(
    mo="She lifts two coins off the taller stack and sets them onto the shorter "
       "one, then two more, watching the scale's display as she does it. She "
       "points at the display, then at each stack in turn, and folds her arms."),

"shirazu": dict(
    mo="She reads down the roster with her finger, picks up the pencil, "
       "hesitates over one row, then writes her hours in the box and initials "
       "it. She steps back and looks at the sheet before walking off."),

"zeikin": dict(
    mo="She reads the last line of the leaflet, lets out a breath, and lays it "
       "down flat. She takes her glasses off, folds them and sets them on the "
       "leaflet, and sits back with her hands loosely clasped, looking out the "
       "window."),

"zeikin_b": dict(hands="W1",
    sc="a close shot on the kitchen table of an elderly woman's hands beside a "
       "whole neat stack of brass coins and a printed leaflet lying flat next "
       "to it, a few loose coins to one side, calm daylight",
    mo="She slides the leaflet toward the coin stack, looks at the stack, then "
       "picks up a few loose coins from the side and adds them to the top "
       "rather than taking any away. She pats the top of the stack lightly."),

# ───────────────────────── 第6章 改正 ─────────────────────────────────────
"kaisei": dict(hands="M3",
    sc="a close desk shot of an elderly man's hands opening a plain bound "
       "reference booklet to a marked page, a cream wall calendar leaning "
       "against the wall behind with one month ringed in red, warm lamp light",
    mo="He opens the booklet to the marked page and flattens it, then reaches "
       "for the calendar leaning against the wall, taps the ringed month, and "
       "sets it back. He runs his finger down the page of the booklet."),

"ochitsuite": dict(
    mo="He raises both hands, palms down, and lowers them slowly in a calming "
       "gesture, then rests them on the desk. He nods once, takes his glasses "
       "off, cleans them briefly on his cardigan, and puts them back on."),

"eikyou_nashi": dict(
    mo="He draws the wide orange arc over the three figures in one steady "
       "stroke, caps the marker, and taps each figure under the arc in turn "
       "with the capped end. He steps back half a pace."),

"korekara": dict(
    mo="He draws two more simple figures with quick black strokes beside the "
       "first three, checks they sit under the arc, caps the marker and sets it "
       "in the tray. He dusts his hands together."),

# ───────────────────────── 研究ノート・次回 ───────────────────────────────
"chuui": dict(
    mo="He closes the notebook and lays both hands on it, looks at the camera "
       "and gives a slow nod, then picks up a leaflet from the desk, holds it "
       "up briefly toward the camera, and sets it down again."),

"chuui_b": dict(cast="S1",
    sc="the public service counter seen from a few steps away, the staff member "
       "in a pale grey blazer behind it tidying a stack of leaflets, the blank "
       "sign boards above, one grey chair on the customer side, daylight from a "
       "side window",
    mo="She squares the stack of leaflets, sets a pen in its holder, looks up "
       "toward the door, and reaches across to straighten the chair on the "
       "customer side with one hand."),

"yokoku": dict(
    mo="She opens the letterbox, takes out the envelope, lets the flap fall "
       "shut, and turns the envelope over to read the front. She tucks it under "
       "her arm with the rest of her post and walks back up the path toward "
       "the house."),

"takahashi_b": dict(
    mo="She sets the envelope on the table, turns it face up, looks at it, then "
       "picks up her tea instead. She drinks, puts the cup down, and finally "
       "slides a finger under the flap and begins to open it."),

"fuyo": dict(hands="W2",
    sc="a close overhead shot of a single printed form lying on a table, ruled "
       "into boxes with faint unreadable print; a woman's hands in a "
       "mustard-yellow cardigan sleeve are smoothing it flat, a black ballpoint "
       "pen beside it, autumn light from the side",
    mo="She smooths the form flat, picks up the pen, reads down the boxes with "
       "the pen tip, then puts the pen down without writing and rests both "
       "hands on the table either side of the form."),

"hirogatta": dict(
    sc="a wide view of a quiet Japanese residential street in autumn, seen from "
       "above at a shallow angle, ginkgo trees turning yellow along the "
       "pavement; a postal worker on a small red delivery bike is stopped at "
       "the first gate, sliding a white envelope into its letterbox, more "
       "identical envelopes in the bike's carrier",
    mo="The postal worker slides the envelope into the letterbox, pushes off, "
       "and rides slowly down the street, stopping at the next gate and the one "
       "after to post an envelope at each, before riding on; leaves drift "
       "across the road."),

"mata": dict(
    mo="He closes his notebook, stands his pen in the holder, looks at the "
       "camera and gives a small bow of the head, then raises a hand in a brief "
       "wave and reaches to switch off the desk lamp; the lamp goes dark and "
       "the blue window light takes over."),
}
