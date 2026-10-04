# -*- coding: utf-8 -*-
"""
Sinh 34 prompt t2v cho TẬP 01 「塔のふもとの一日」 — kênh youtube-jp-retrofuture.

Nguồn: `03_SCRIPTS/ep01_tou-no-fumoto.md` (storyboard) + `tools/blocks_s100.py` (mọi khối luật).
⛔ KHÔNG chép khối vào đây — hai bản khối = hai luật, đúng bệnh `_sig` của workspace.

Chạy:  python tools/gen_prompts_ep01.py
Xuất:  06_VIDEO/01_tou-no-fumoto/videogen_FLOW.txt     (1 prompt/dòng — bơm extension)
       06_VIDEO/01_tou-no-fumoto/videogen_TENFILE.txt  (thứ tự dòng ↔ tên clip ↔ vai trong mạch)

🔴 GATE PHÂN LOẠI CẢNH — sửa HAI LẦN trong lượt này, cả hai đều vì gate QUÁ CHẶT:
   ① bản 3-cảnh-thử kiểm `emo XOR (crowd=="none")` ⇒ chấm oan cảnh **mẹ đan một mình** (22/32/33):
      cảm xúc thật mà không có người khác trong khung. "Cảnh thở" = không có NGƯỜI NÀO, không phải
      "không có đám đông" ⇒ thêm cờ `breath`.
   ② bản `emo XOR breath` ⇒ chấm oan **9 cảnh CHUYỂN** (đi học · bến xe · vào arcade · tính tiền ·
      về nhà · ăn tối · rửa bát): có người, không phải khoảnh khắc, không phải cảnh thở.
   ⇒ **BA loại cảnh**, mỗi cảnh đúng một loại, + hai gate CẢ LÔ:
      · cảnh CHUYỂN ≤30% — thừa là quay về đúng bệnh vòng 1 "phong cảnh có người đi lại"
      · KHOẢNH KHẮC ≥30% — thiếu là video không có cảm xúc
   Cùng bài học `feedback_gate_phai_qua_duoc_mau_no_hoc_tu`: gate đánh trượt chính thứ nó phải
   phục vụ thì **gate sai**, không phải nội dung sai.
"""
import io, re, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from blocks_s100 import (ALIVE, HEAD, REAL, PEOPLE, POV, TOWN, MEGACITY, RETRO_TECH, GREEN, MATERIALS,
                         WALK, STAND, SIT, HANDHELD, PACE, PACE_MEASURED, SLOW_STAND, GROUND,
                         EASE, CALM, MOMENT, AVOID, NO_TEXT_NUM, SKY, LIGHT, OPTICS,
                         CROWD, TAIL, TAIL_SIGN, CAST, POSE_BLOCK)

S = lambda **k: k

# ─────────────────────────────────────────────────────────────────────────────
# 34 CẢNH — khớp storyboard `03_SCRIPTS/ep01_tou-no-fumoto.md` §4
#   pose stand|walk · pace creep|stroll · emo=khoảnh khắc · breath=không người nào
#   mega=có tháp xoắn trong khung · thread=vai trong sợi chỉ của vật (len → áo)
# ─────────────────────────────────────────────────────────────────────────────
SCENES = [
# ══ A · PHỐ THỨC ═══════════════════════════════════════════════════════════
 S(id="01_yoake", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="none",
   cast=[], mega=True, emo=False, breath=True, thread="",
   you="standing in the narrow back lane before anyone else is up",
   set="A view down a narrow back lane still in the blue of before-dawn, the shopfronts shuttered "
       "close on both sides, a street lamp with a fluted glass shade still burning above you and its "
       "filament visible inside, a bundle of pneumatic message tubes running along the shopfronts, "
       "potted plants crowding every doorstep. At the far end of the lane, beyond the roofs, the "
       "spiralling tiered towers of the great city stand up into the sky.",
   act="Nobody is out. A thin wisp of white steam leaks from a joint in the pneumatic tubes and drifts "
       "up. The street lamp fades out as the sky lightens. High above, the tops of the towers catch the "
       "first sun long before it reaches the ground.",
   cam="the view holds steady down the lane with the lit towers above the far roofs"),

 S(id="02_hoshimono", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="none",
   cast=[], mega=True, emo=False, breath=True, thread="",
   you="standing at the concrete parapet at the top of the worn steps above the roofs",
   set="A view out over the tiled and corrugated-steel roofs of the little streets packed close "
       "together below you, their aerials and water tanks and washing lines, a big old tree leaning "
       "over them, ivy climbing the parapet in a broad sheet at the left edge of the frame. Beyond the "
       "roofs stand the spiralling tiered towers of the great city.",
   act="Nobody is in the shot. Last night's washing still hangs on the lines, damp and heavy, barely "
       "moving. A crow walks along the top of a water tank. The shadow of the nearest tower lies right "
       "across the whole town.",
   cam="the view holds steady out over the roofs with the towers beyond"),

 S(id="03_shutter", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="few",
   cast=[], mega=True, emo=True, breath=False, thread="",
   you="standing in the lane a few steps from the shopfront as it opens",
   set="A view of a shopfront in the lane, its wooden shutter still down, a plain painted board above "
       "the doorway with nothing written on it, a canvas awning rolled up, bicycles against the wall "
       "beside a red cylindrical post box, and a brass and glass vending stand with a pressure dial on "
       "its front standing at the kerb in the near foreground.",
   act="The shopkeeper, a man in his sixties in shirtsleeves seen mostly from behind, pushes the "
       "wooden shutter up its runners, props it, and then stands still in his own doorway for a moment "
       "looking out down the lane before he turns and goes in.",
   cam="the view holds steady on the shopfront with the lane running away beside it"),

 S(id="04_asagohan", pose="stand", pace="creep", sky="window", light="interior", crowd="none",
   cast=["mother", "daughter"], mega=False, emo=True, breath=False,
   thread="⭐ GIEO — lỗ sờn ở khuỷu áo cũ",
   you="sitting at the low table in your own front room with the window open on the morning",
   set="A view across a low wooden table in a small front room: worn tatami, a glass globe lamp in a "
       "cage of brass ribs above it, a small electric fan with a brass cage on the shelf, a bonsai in a "
       "glazed pot in the alcove, and a square wooden-framed window standing open onto the bright lane "
       "with the roofs beyond.",
   act="The mother sets a glazed bowl down in front of the girl. The girl leans forward and props both "
       "elbows on the table — and the elbow of her old knitted cardigan is worn right through, the wool "
       "gone thin and pale and open in a small hole. The mother's eyes rest on it for exactly one beat, "
       "then she turns away to fetch another bowl. Neither of them says anything.",
   cam="the view holds steady across the table with the open window beyond them"),

 S(id="05_tsuugaku", pose="walk", pace="creep", sky="day", light="day", crowd="some",
   cast=["daughter"], mega=True, emo=False, breath=False, thread="lỗ sờn nhắc lại",
   you="walking a few paces behind the girl on her way to school",
   set="A view along the lane in the morning sun, shopfronts open on both sides with their goods "
       "stacked out to the kerb, cloth noren in the doorways, bicycles against every wall, tangled "
       "overhead wires crossing above, and at the far end the spiralling tiered towers of the great "
       "city with a slim monorail threading between them.",
   act="The girl walks ahead of you with her satchel on her back, unhurried. She puts one hand up on "
       "the stair rail as she goes, and the worn-through elbow of her cardigan turns towards you.",
   cam="the shot begins framed on the lane with the girl a little way ahead, the camera then edges "
       "forward barely at all, and the shot ends with her still ahead of you and a little more of the "
       "lane opened out"),

 S(id="06_basutei", pose="stand", pace="creep", sky="day", light="day", crowd="some",
   cast=[], mega=True, emo=False, breath=False, thread="",
   you="standing at the bus stop at the end of the street among the other people waiting",
   set="A view at a bus stop at the end of the street: a timber shelter, a plain unlettered enamel "
       "sign on a post, a bundle of pneumatic tubes turning the corner of the building behind with "
       "brass caps at the bend, potted plants along the kerb, and the little shops of the street "
       "running away beyond.",
   act="Eight or ten people wait, all of them turned the same way looking off down the road, seen from "
       "behind or from the side. A small three-wheeled delivery truck with a riveted boiler goes past "
       "and leaves a thin plume of steam across the frame.",
   cam="the view holds steady on the shelter and the waiting people with the street beyond"),

 S(id="07_asa_hikari", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   cast=[], mega=True, emo=False, breath=True, thread="",
   you="standing in the lane now that the morning sun has reached the ground",
   set="A view straight down the lane with the sun now down on the road surface, shopfronts and "
       "awnings on both sides, a red post box, bicycles, dozens of potted plants, tangled overhead "
       "wires, and beyond the roofs the spiralling tiered towers with a slender monorail rail on "
       "concrete piers running just above the rooftops.",
   act="Nobody is near. A single riveted monorail carriage slides along the rail above the roofs and "
       "out of frame. The shadow of the tower has begun to shorten. Dust turns in the bar of sunlight.",
   cam="the view holds steady down the lane with the monorail above the roofs"),

# ══ B · LỖ SỜN ═════════════════════════════════════════════════════════════
 S(id="08_tabako", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   cast=[], mega=True, emo=True, breath=False, thread="",
   you="standing in the lane beside the tobacconist's little window, where people stop a moment on "
       "their way through",
   set="A view of the tiny tobacconist's on the left of the lane: a small sliding window open onto the "
       "street, its counter crowded with boxes, an electric fan with a brass cage turning slowly on the "
       "counter, and an old woman sitting just inside it. On the right a bicycle leans against a "
       "glazed-tile wall beside a red post box; at the far end of the lane the tiered towers stand up "
       "into the sky.",
   act="The old woman in the window has her head down over her knitting. She comes to the end of a "
       "row, stops, and holds the work out at arm's length to look at it — her eyes go first and crease "
       "into two slits, the cheeks pushing up, the mouth barely opening at all — then she lowers it "
       "back into her lap and her hands start again.",
   cam="the view holds steady on the open window with the lane and the far towers beyond it"),

 S(id="09_keito_tarinai", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   cast=["mother"], mega=True, emo=True, breath=False,
   thread="⭐ cuộn len còn lại — KHÔNG ĐỦ",
   you="standing on the lane outside your own door as she finishes sweeping",
   set="A view of the doorstep of a small house on the lane: potted plants crowding the step in their "
       "dozens, a copper rainwater pipe running down the wall polished warm where hands have touched "
       "it, a broom leaning against the timber, a street lamp with a fluted glass shade above, and a "
       "wicker knitting basket set down on the step.",
   act="The mother finishes sweeping, sets the broom against the wall and sits down on the step. She "
       "lifts the wicker basket onto her lap and turns over the last small ball of cream wool in it, "
       "weighing it in the flat of her hand — then sets it back down and looks at it. It is not enough.",
   cam="the view holds steady on the doorstep with her and the basket and the lane beside"),

 S(id="10_kago", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   cast=[], mega=False, emo=False, breath=True, thread="tay áo đan được nửa",
   you="standing on the lane looking at the basket she has left on the step",
   set="A close view of the wicker knitting basket alone on the timber doorstep, the half-made sleeve "
       "of a child's jumper hanging out of it in cream wool with both needles still pushed through the "
       "stitches, potted plants crowding around it, the copper pipe and the glazed tile of the wall "
       "behind, the lane soft and bright beyond.",
   act="Nobody is in the shot. The wind turns one loop of the wool over and then lets it be. The "
       "shadow of a leaf moves across the timber.",
   cam="the view holds steady on the basket and the sleeve on the step"),

 S(id="11_dekakeru", pose="walk", pace="creep", sky="day", light="day", crowd="few",
   cast=["mother"], mega=True, emo=False, breath=False, thread="mang giỏ đi",
   you="walking out of the lane towards the main street a little way behind her",
   set="A view along the lane towards where it opens onto the main street, shopfronts close on both "
       "sides, a bundle of pneumatic message tubes running along the frontages with brass caps at the "
       "bends, bicycles, awnings, dozens of potted plants, tangled wires above.",
   act="The mother walks ahead of you with the wicker basket on her arm. As she passes the tubes one "
       "of them thumps softly and something runs away inside it along the wall.",
   cam="the shot begins framed on the lane with her a little way ahead, the camera then edges forward "
       "barely at all, and the shot ends with her still ahead and the bright opening of the main street "
       "a little nearer"),

 S(id="12_denki", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   cast=[], mega=False, emo=True, breath=False, thread="",
   you="standing on the pavement outside the electrical shop",
   set="A view of the electrical shop's window: a television in a timber cabinet on thin splayed legs "
       "with a deeply curved glass screen, glass bulbs and coils of flex crowded around it, a plain "
       "unlettered board above, a canvas awning low over the glass, bicycles and potted plants at the "
       "kerb in the near foreground.",
   act="An old man stands at the window with both hands behind his back, watching the curved screen, "
       "which shows nothing but soft grey static. He shifts his weight from one foot to the other and "
       "goes on watching.",
   cam="the view holds steady on the window with him at the edge of the frame"),

 S(id="13_mahiru", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   cast=[], mega=True, emo=False, breath=True, thread="",
   you="standing at the junction in the middle of the day",
   set="A view at a junction of two narrow streets under the high midday sun, glazed tile and painted "
       "concrete walls, a red post box, a street lamp, potted plants, and beyond the roofs the "
       "spiralling tiered towers rising tier above tier into the sky.",
   act="Nobody is near. The shadow of the tower is at its shortest of the whole day, folded in tight "
       "at the foot of the wall. Heat shivers up off the road surface. A cat lies in the strip of shade.",
   cam="the view holds steady on the junction with the towers above the roofs"),

# ══ C · ĐI TÌM LEN ═════════════════════════════════════════════════════════
 S(id="14_shoutengai", pose="walk", pace="creep", sky="window", light="interior", crowd="busy",
   cast=[], mega=False, emo=False, breath=False, thread="",
   you="walking very slowly into the covered shopping arcade",
   set="A view down the middle of a covered shopping street: a translucent corrugated roof high "
       "overhead letting the daylight down in long pale bars, shopfronts opening onto the walkway on "
       "both sides with their goods stacked out to the edge, plain unlettered painted boards above the "
       "frontages, cloth noren and canvas awnings hanging low, paper lanterns strung along above, "
       "bicycles parked in rows against the pillars, and a brass and glass vending stand with a "
       "pressure dial standing at the near corner.",
   act="The crowd moves both ways along the arcade, nobody hurrying, nearly all of them seen from "
       "behind or from the side.",
   cam="the shot begins framed down the arcade with the far end soft and bright, the camera then edges "
       "forward barely at all, and the shot ends with only a little more of the arcade opened out"),

 S(id="15_yaoya", pose="stand", pace="creep", sky="window", light="interior", crowd="busy",
   cast=[], mega=False, emo=True, breath=False, thread="",
   you="standing at the greengrocer's stand in the arcade",
   set="A view of a grocer's sloping stand of vegetables in wooden crates under the arcade roof, a "
       "plain painted board above it, a canvas awning, paper lanterns overhead, bicycles against the "
       "pillar beside, and a mechanical cash register with rows of round keys on the counter at the end "
       "of the stand.",
   act="The grocer, a broad man in his fifties with a towel round his neck, holds a wrapped parcel out "
       "to a customer with both hands; she takes it, and his hands are already reaching back behind him "
       "for the next parcel before she has finished bowing her head over it.",
   cam="the view holds steady on the stand with the two of them at it"),

 S(id="16_hanbaiki", pose="stand", pace="creep", sky="window", light="interior", crowd="some",
   cast=[], mega=False, emo=True, breath=False, thread="",
   you="standing beside the vending stand in the arcade",
   set="A view of a tall brass and glass vending stand under the arcade roof, a round pressure dial on "
       "its front and copper piping running down its side, polished where hands have touched it, with "
       "the shopfronts and hanging lanterns of the arcade behind and bicycles in a row against the "
       "pillar.",
   act="A small boy stops dead in front of the dial and tips his head right back to look up at it, his "
       "mouth open. His mother's hand comes into the frame and rests on the top of his head and steers "
       "him away — and he goes, still looking back over his shoulder at it.",
   cam="the view holds steady on the vending stand with the boy in front of it"),

 S(id="17_keitoya", pose="stand", pace="creep", sky="window", light="interior", crowd="few",
   cast=["mother"], mega=False, emo=True, breath=False,
   thread="⭐ chọn cuộn len kem — so với tay áo đang đan",
   you="standing just inside the little wool shop",
   set="A view inside a small wool shop: wooden trays on the shelves stacked with balls of wool in "
       "soft colours, thread and buttons and folded cloth, one lamp with a fluted glass shade lit above "
       "the counter, a plain unlettered board over it, and the bright doorway onto the arcade behind.",
   act="The mother picks a ball of cream wool out of the tray and holds it up beside the half-made "
       "sleeve she has brought with her in the basket, turning it towards the light from the doorway to "
       "compare them. Her fingers stay on the wool a beat longer than she needs. Then she keeps it.",
   cam="the view holds steady on the trays of wool with her beside them"),

 S(id="18_kaikei", pose="stand", pace="creep", sky="window", light="interior", crowd="few",
   cast=["mother"], mega=False, emo=False, breath=False, thread="gói giấy",
   you="standing at the counter of the wool shop",
   set="A view of the wool shop counter: a mechanical cash register with rows of round keys and a "
       "brass crank, a roll of brown paper, a ball of string on a spike, the lamp with its fluted glass "
       "shade above, and the trays of coloured wool on the shelves behind.",
   act="The shopkeeper, a woman in her sixties, wraps the ball of wool in a square of brown paper and "
       "twists the two ends closed, then presses one key on the register with the flat of her finger "
       "and the drawer comes out with a soft knock.",
   cam="the view holds steady on the counter with the parcel and the register"),

 S(id="19_arcade_oku", pose="stand", pace="creep", sky="window", light="interior", crowd="none",
   cast=[], mega=False, emo=False, breath=True, thread="",
   you="standing in the arcade looking towards the bright far end of it",
   set="A view down the length of the covered arcade towards the white opening at the far end, the "
       "translucent roof letting the light down in long pale bars, paper lanterns strung overhead, "
       "plain painted boards and low awnings on both sides, bicycles in rows against the pillars, a "
       "bundle of pneumatic tubes running along above the shopfronts.",
   act="Nobody is near you. The paper lanterns overhead sway very slightly. A thin curl of steam drifts "
       "across the bright opening at the far end and is gone.",
   cam="the view holds steady down the arcade towards the bright far end"),

 S(id="20_kouri", pose="stand", pace="creep", sky="day", light="day", crowd="some",
   cast=[], mega=True, emo=True, breath=False, thread="",
   you="standing on the pavement by the ice stall just outside the arcade",
   set="A view of a small ice stall at the kerb: a brass and glass machine with a pressure dial, one "
       "small board above it carrying the single word 氷 in large clean brush strokes, a canvas awning "
       "over it, potted plants and bicycles along the kerb, and the shopfronts of the street behind.",
   act="Two schoolgirls sit on the kerb sharing one paper cup of shaved ice between them. The one "
       "holding it turns the cup round in her hands so that the side that has not been eaten yet is "
       "facing the other girl, and holds it out.",
   cam="the view holds steady on the two of them on the kerb with the stall behind"),

 S(id="21_kaeri", pose="walk", pace="creep", sky="day", light="day", crowd="some",
   cast=["mother"], mega=True, emo=False, breath=False, thread="mang len về",
   you="walking home behind her out of the arcade and into the street",
   set="A view along the street away from the arcade in the early afternoon, shopfronts and awnings on "
       "both sides, a red post box, dozens of potted plants, ivy climbing a concrete wall in a broad "
       "healthy sheet, tangled wires above, and beyond the roofs the spiralling tiered towers standing "
       "in the light.",
   act="The mother walks ahead of you with the brown paper parcel in the basket on her arm. The light "
       "on the walls has begun to lean.",
   cam="the shot begins framed on the street with her a little way ahead, the camera then edges forward "
       "barely at all, and the shot ends with her still ahead and a little more of the street opened out"),

# ══ D · ĐAN ════════════════════════════════════════════════════════════════
 S(id="22_amu", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   cast=["mother"], mega=True, emo=True, breath=False, thread="⭐ đan trên hiên",
   you="sitting on the timber veranda a little way along from her",
   set="A view along a narrow timber veranda at the front of the house, the wicker basket on her lap, "
       "potted plants crowding the edge of the boards, a copper pipe polished warm on the wall, an "
       "electric fan with a brass cage turned off in the corner, and the bright lane beyond the rail.",
   act="The mother sits knitting, the needles going evenly. Halfway along a row she stops with the work "
       "still in her hands and looks out at the lane for one beat, not at anything — then her hands "
       "start again and she goes on.",
   cam="the view holds steady along the veranda with her and the basket"),

 S(id="23_monohoshi", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   cast=[], mega=True, emo=False, breath=True, thread="",
   you="standing on the veranda beside the washing line",
   set="A close view of a washing line strung between two timber posts at the edge of the veranda, one "
       "cloth hanging on it, the glazed-tile wall and the copper pipe behind, potted plants along the "
       "boards, and the roofs of the lane soft beyond.",
   act="Nobody is in the shot. The cloth on the line fills out with the wind and then falls slack "
       "again, and fills again. The light on the wall behind it has turned the colour of honey.",
   cam="the view holds steady on the line and the cloth with the wall behind"),

 S(id="24_kage_gyaku", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   cast=[], mega=True, emo=False, breath=True,
   thread="⭐ bóng tháp đã đổ ngược so với cảnh 02",
   you="standing at the concrete parapet above the roofs again, late in the afternoon",
   set="A view out over the same roofs as the morning, the aerials and water tanks and washing lines, "
       "the big old tree, the ivy on the parapet at the left edge — and beyond them the spiralling "
       "tiered towers, tier widening above tier, their terraces planted green, joined by slender "
       "bridges and elevated roadways high in the air.",
   act="Nobody is in the shot. The shadow of the tower now lies the opposite way across the town from "
       "where it lay in the morning. A single monorail carriage moves slowly between the tiers. A thin "
       "plume of white steam rises from somewhere among the roofs and leans away on the wind.",
   cam="the view holds steady out over the roofs with the towers and the piled white cumulus above them"),

 S(id="25_miageru", pose="stand", pace="creep", sky="dusk", light="dusk", crowd="few",
   cast=[], mega=True, emo=True, breath=False, thread="",
   you="standing at the mouth of the lane in the late afternoon",
   set="A view at the mouth of the lane with the low sun coming in flat along the road, shopfronts "
       "thrown into long bars of light and shade, a red post box, bicycles, potted plants, a street "
       "lamp with a fluted glass shade not yet lit, and beyond the roofs the tiered towers going gold "
       "at their tops.",
   act="A man stops in the middle of the lane with his shopping bag still in his hand and tips his head "
       "back to look up at the towers, the way people look at weather — he stands like that for a "
       "moment, then his head comes down and he walks on.",
   cam="the view holds steady on the mouth of the lane with the towers above"),

 S(id="26_kaerimichi", pose="walk", pace="creep", sky="dusk", light="dusk", crowd="few",
   cast=["daughter"], mega=True, emo=False, breath=False, thread="",
   you="walking home along the lane a little way behind the girl",
   set="A view along the lane in the last of the sun, the shopfronts warm on one side and in shadow on "
       "the other, paper lanterns not yet lit under the eaves, bicycles, potted plants, the drain "
       "grates and worn kerbstones underfoot.",
   act="The girl comes home with her satchel, slower than she went in the morning. She stops once and "
       "looks down through the grating of a drain, then goes on.",
   cam="the shot begins framed on the lane with her a little way ahead, the camera then edges forward "
       "barely at all, and the shot ends with her nearer her own door"),

 S(id="27_kakusu", pose="stand", pace="creep", sky="dusk", light="interior", crowd="none",
   cast=["mother", "daughter"], mega=False, emo=True, breath=False,
   thread="⭐ mẹ giấu giỏ len",
   you="standing just inside your own doorway as she comes in",
   set="A view of the inside of the doorway of a small house: shoes lined up on the step, a paper "
       "lantern lit over the door, the wicker knitting basket on the timber floor beside her, the "
       "glass globe lamp in its brass cage further in, and the bright doorway onto the lane behind.",
   act="The mother hears the step outside. She pushes the wicker basket behind her out of sight with "
       "the back of her hand, then turns and lifts the satchel off the girl's shoulder as she comes in. "
       "The girl goes past her into the dim room without looking at anything.",
   cam="the view holds steady on the doorway with both of them in it"),

# ══ E · XONG ═══════════════════════════════════════════════════════════════
 S(id="28_yuushoku", pose="stand", pace="creep", sky="night", light="interior_night", crowd="none",
   cast=["mother", "daughter"], mega=False, emo=False, breath=False,
   thread="vẫn cái áo cũ, vẫn cái lỗ",
   you="sitting at the low table with them",
   set="A view across the low wooden table in the front room at night, the glass globe lamp in its "
       "cage of brass ribs lit warm above it, bowls on the wood, the window a dark blue rectangle, the "
       "television in its timber cabinet dark in the corner.",
   act="The mother and the girl eat together, neither of them talking. The girl props her elbows on the "
       "table again — still the old cardigan, still the worn-through hole at the elbow.",
   cam="the view holds steady across the table with both of them and the dark window"),

 S(id="29_terebi", pose="stand", pace="creep", sky="night", light="interior_night", crowd="none",
   cast=[], mega=False, emo=False, breath=True, thread="",
   you="sitting on the tatami in the corner of the room",
   set="A close view of the television in its timber cabinet on thin splayed legs in the corner of the "
       "room, its deeply curved glass screen showing soft grey static, a three-bladed electric fan with "
       "a brass cage turning slowly beside it, the hem of the cloth on the low table lifting, a glass "
       "globe lamp warm further off.",
   act="Nobody is in the shot. The static moves on the curved glass. The fan comes round to the end of "
       "its arc and the cloth on the table lifts and settles.",
   cam="the view holds steady on the cabinet and the fan and the corner of the tatami"),

 S(id="30_arai", pose="stand", pace="creep", sky="night", light="interior_night", crowd="none",
   cast=["mother"], mega=False, emo=False, breath=False, thread="",
   you="standing in the kitchen doorway",
   set="A view of a small kitchen at night, one lamp with a fluted glass shade over the sink, a "
       "spherical steel rice cooker cold on the counter beside it, copper pipe running up the wall, a "
       "draining rack, and the window black above the sink.",
   act="The mother washes the bowls at the sink with her back to you, unhurried, and stacks them one at "
       "a time on the rack.",
   cam="the view holds steady on the sink with her at it and the black window above"),

 S(id="31_yoru_no_machi", pose="stand", pace="creep", sky="night", light="night", crowd="none",
   cast=[], mega=True, emo=False, breath=True, thread="",
   you="standing on the veranda late at night",
   set="A view from the veranda out over the dark lane, an oil lantern set down on the timber boards "
       "in the near foreground, the shopfronts shut and only one or two paper lanterns burning under "
       "the eaves, potted plants black shapes along the boards — and beyond the roofs the spiralling "
       "tiered towers standing dark with thousands of tiny lit windows scattered up them into the sky.",
   act="Nobody is in the shot. A thin wisp of steam still leaks from the joint in the pneumatic tubes "
       "along the wall and the lantern light catches it. One monorail carriage crosses between the "
       "towers, lit from inside.",
   cam="the view holds steady out over the dark lane with the lit towers above"),

 S(id="32_kiru", pose="stand", pace="creep", sky="night", light="night", crowd="none",
   cast=["mother"], mega=True, emo=True, breath=False,
   thread="⭐ đan nốt — CẮT SỢI CHỈ",
   you="sitting on the veranda boards a little way along from her",
   set="A view along the timber veranda at night, an oil lantern set down on the boards beside her "
       "throwing a small warm circle, the finished jumper across her knees in cream wool, a small pair "
       "of scissors on the boards, potted plants black beyond the lantern light, the dark lane past the "
       "rail.",
   act="The mother works the last few stitches. Then she holds the jumper out at arm's length towards "
       "the lantern and her eyes go from one elbow to the other and back. She lowers it into her lap, "
       "picks up the small scissors, and cuts the thread.",
   cam="the view holds steady along the veranda with her and the lantern"),

 S(id="33_makuramoto", pose="stand", pace="creep", sky="night", light="interior_night", crowd="none",
   cast=["mother", "daughter"], mega=False, emo=True, breath=False,
   thread="⭐⭐ TRẢ — áo mới đặt cạnh gối",
   you="standing in the doorway of the small back room",
   set="A view into a small back room at night: a futon on the worn tatami, one low lamp with a fluted "
       "glass shade turned down in the corner, a folded cloth, the paper of the sliding screen faintly "
       "lit from the next room.",
   act="The girl is asleep on the futon. Her old cardigan lies folded at the foot of it with the "
       "worn-through elbow turned face up. The mother comes in with the new jumper folded square in "
       "both hands, sets it down on the tatami beside the girl's pillow, straightens it once with two "
       "fingers, and stands up. Nobody sees her do it.",
   cam="the view holds steady into the room with the futon and the two folded jumpers"),

 S(id="34_kieru_akari", pose="stand", pace="creep", sky="night", light="night", crowd="none",
   cast=[], mega=True, emo=False, breath=True, thread="đèn tắt",
   you="standing out in the lane looking back at the front of your own house",
   set="A view of the front of a small house from the dark lane, one small square window still lit warm "
       "yellow among the dark timber and glazed tile, a paper lantern burning by the door, potted plants "
       "black along the step, the copper pipe running down the wall — and above the roofs the tiered "
       "towers standing dark with their thousands of lit windows going up into the night sky.",
   act="Nobody is in the shot. The lit window holds for a moment. Then it goes out, and only the "
       "lantern by the door is left burning — and above, the windows of the towers, still lit, all "
       "night.",
   cam="the view holds steady on the front of the house with the towers above the roofs"),
]

# ── POV hoá (làm ở TẦNG HÀM — replace trên source Python đã trượt 3 lần) ──
_POVIFY = [
    (r"the camera then edges",  "you then move"),
    (r"the camera then drifts", "you then draw"),
    (r"the camera then lifts",  "you then raise your eyes"),
    (r"the camera then turns",  "you then turn your head"),
    (r"the camera then",        "you then"),
    (r"the camera",             "you"),
]


def povify(t):
    for a, b in _POVIFY:
        t = re.sub(a, b, t)
    return t


def build(sc):
    # ⭐ THU TU KHOI = thu quyet dinh (04_VIDEOGEN_STYLE_S100.md §CONG THUC DA CHOT §1):
    #   HEAD 0% → MEGACITY 7% → RETRO_TECH → NO_TEXT_NUM → REAL/POV → MOMENT → AVOID cuoi.
    P = [HEAD]
    if sc["mega"]:
        P.append(MEGACITY)
    P += [RETRO_TECH, NO_TEXT_NUM, REAL, POV, ALIVE]
    for c in sc["cast"]:
        P.append(CAST[c])
    P.append("You are " + sc["you"] + ", and this is what you see.")
    P.append(sc["set"])
    if sc["emo"]:
        P.append(MOMENT)
    P.append(sc["act"])
    if CROWD[sc["crowd"]]:
        P.append(CROWD[sc["crowd"]])
    P.append(CALM)

    pace = PACE[sc["pace"]]
    if sc["pose"] == "walk":
        P.append("Your movement, the only one in this shot: " + povify(sc["cam"]) + "; " + EASE
                 + ". " + pace + " " + GROUND + " " + WALK)
    else:
        P.append("The framing does not change at all from the first frame to the last: the shot holds "
                 "one single unmoving view for the whole eight seconds and the viewpoint never pushes "
                 "in, never pulls back, never pans and never drifts — " + povify(sc["cam"]) +
                 " for the whole shot. What changes is only what happens inside that unmoving frame. "
                 + SLOW_STAND + " " + POSE_BLOCK[sc["pose"]])

    # HANDHELD tung BI MAT o ca hai tool: no nam trong list dau `P = [...]`, va luc sap lai
    # thu tu khoi tao viet lai list do nen no roi ra ngoai — do duoc 0/3 va 0/34 prompt co no.
    # Dat canh khoi tu the vi no noi ve MAY, va de lan sau sap lai thu tu thi no di theo.
    P.append(HANDHELD)
    P.append(TOWN)
    P.append(GREEN)
    P.append(MATERIALS)
    P.append(PEOPLE)
    P.append(AVOID)
    if SKY[sc["sky"]]:
        P.append(SKY[sc["sky"]])
    P.append(LIGHT[sc["light"]])
    P.append(OPTICS)
    has_sign = bool(re.search(r"[぀-ヿ一-鿿]", sc["set"] + sc["act"]))
    P.append(TAIL_SIGN if has_sign else TAIL)
    return " ".join(x.strip() for x in P if x.strip())


JP_OK = tuple("ゆ氷たばこパンさかな")


def _at(lo, p, key, limit, label):
    """Tra (ten_gate, dat) — ten SINH TU nguong nen khong the lech voi phep kiem.
    🔴 Da dinh: doi ten thanh '<=20%' ma bieu thuc con '<= 12' => bao do kem thong tin SAI."""
    i = lo.find(key)
    pct = i * 100 // len(p) if i >= 0 else 999
    return (f"{label}<={limit}%", pct <= limit)


def gate(prompts):
    bad = ["35mm", "16mm", "respectful distance", "hands only", "feet only", "pedestal",
           "crane down", "sink down", "floating island", "hovering city",
           "rock pillar", "sea of cloud", "suspension bridge", "treehouse", "16:9", "1920x1080"]
    fails = 0
    for i, (sc, p) in enumerate(prompts, 1):
        lo = p.casefold()
        scan = lo
        for kill in ("it is not a cyberpunk city: no neon, no holograms, no glass towers, no glowing "
                     "signs, no flying cars, nothing hovering",
                     "never electronic, never a screen with an image on it, never neon, never a "
                     "hologram, and nothing hovers or floats",
                     "and it is not a modern city of glass office towers"):
            scan = scan.replace(kill, "")
        anim = [m.group(0) for m in re.finditer(r"(?<!not )(?<!never )anim\w*", lo)]
        chk = dict([
            _at(lo, p, "impossible spiralling ziggurats", 12, "THAP-XOAN") if sc["mega"]
                else ("THAP-XOAN<=12%", True),
            _at(lo, p, "right here in the foreground within arm's reach", 22, "VT-TIEN-CANH"),
            _at(lo, p, "no distorted, melted or asymmetric faces", 10, "CAM-MAT"),
            _at(lo, p, "most of the shop signboards", 28, "CAM-CHU"),
            _at(lo, p, "live-action photography, shot on a real camera", 36, "REAL"),
            _at(lo, p, "first-person point of view", 40, "POV"),
            _at(lo, p, "colossal city stacked in layers", 4, "THE-GIOI"),
            _at(lo, p, "not quite ours", 8, "VT-HEAD"),
        ])
        chk.update({
            "cam-than-nguoi-xem": "no part of the viewer's own body" in lo,
            "khong-nhin-tay":     "you never look down at your own hands or feet" in lo,
            "khai-cho-dung":      "and this is what you see" in lo,
            "khong-xin-anime":    not anim,
            "lop-gan-chat":       "there is no empty wall anywhere" in lo,
            "bien-tron":          "at most two signs anywhere in the frame carry any writing" in lo,
            "cam-do-hien-dai":    "no face masks on anyone" in lo,
            # Do lo 40 clip: 43,5% khung dung yen tuyet doi (mau 3,0-3,8%), 4 clip 97-100%.
            # May tinh + vat dong = tinh lang. May tinh + vat tinh = ANH CHET.
            "khung-phai-song":    "something in the frame is always moving" in lo,
            # 🔴 SKY va LIGHT phai CUNG BUOI. Da dinh: sky="dawn" + light="day" => mot prompt vua
            #    noi "low sun, last of the night" vua noi "sun high and strong".
            "troi-va-sang-cung-buoi":
                (sc["light"] == "interior" and sc["sky"] != "night")       # noi that BAN NGAY
                or (sc["light"] == "interior_night" and sc["sky"] == "night")
                or (sc["sky"] == "window" and sc["light"] == "interior")
                or (sc["sky"] == sc["light"]),
            # Canh NGOAI TROI ma khong khai hau canh = de model TU DIEN => no ve thanh pho
            # hien dai, dung cai da hong 2/3 o vong 1. Mien canh NOI THAT va 2 canh CAN that.
            "ngoai-troi-phai-khai-hau-canh":
                sc["mega"] or sc["light"].startswith("interior") or sc["id"] in ("10_kago", "12_denki"),
            # 🔴 SUA HAI LAN, ghi ca hai vi ca hai deu la gate QUA CHAT:
            #  ① ban 3-canh-thu kiem `emo XOR crowd=="none"` => cham oan canh me dan MOT MINH
            #     (canh tho = khong co NGUOI NAO, khong phai "khong co dam dong").
            #  ② ban XOR `emo/breath` => cham oan 9 CANH CHUYEN (di hoc · ben xe · vao arcade ·
            #     tinh tien · ve nha · an toi · rua bat). Chung co nguoi, khong phai khoanh khac,
            #     khong phai canh tho. Tap thuc te can LOAI THU BA.
            # => 3 loai, moi canh dung mot loai; va CANH CHUYEN co TRAN (xem gate duoi),
            #    vi thua canh chuyen la quay ve dung benh vong 1: "phong canh co nguoi di lai".
            "dung-mot-loai":      (sc["emo"] + sc["breath"]) <= 1,
            "co-viec-xay-ra":     len(sc["act"]) > 80,
            "tho-thi-khong-cast": (not sc["cast"] and sc["crowd"] == "none") if sc["breath"] else True,
            "emo-thi-may-dung":   (sc["pose"] == "stand") if (sc["emo"] and sc["crowd"] != "busy") else True,
            "co-vong-cung":       ("three beats and the middle one is the peak" in lo) if sc["emo"] else True,
            "mot-muc-pace":       (sum(v.casefold()[:60] in lo for v in PACE.values()) == 1)
                                  if sc["pose"] == "walk" else ("you are completely still" in lo),
            "hai-moc": ("the shot begins" in lo and "the shot ends" in lo) if sc["pose"] == "walk"
                       else ("the framing does not change at all" in lo),
            "khoang-lang":      "nothing else happens in it" in lo,
            "cam-mat-dam-dong": "if a background face cannot be rendered cleanly" in lo,
            "khong-tu-cam":     not [b for b in bad if b in scan],
            "chu-chi-tu-quen":  all(ch in JP_OK for ch in re.findall(r"[぀-ヿ一-鿿]", p)),
            "cam-so-goc":       "no timestamps, no counters" in lo,
        })
        f = [k for k, v in chk.items() if not v]
        if f:
            fails += 1
            print(f"  🔴 {i:02d} {sc['id']:<18} {f}")

    # ── gate CA LO: tran canh chuyen ───────────────────────────────────────
    n = len(prompts)
    link = [sc for sc, _ in prompts if not sc["emo"] and not sc["breath"]]
    emo  = sum(1 for sc, _ in prompts if sc["emo"])
    pct = len(link) * 100 // n
    print(f"  ⓘ phan loai canh: {emo} khoanh khac · {sum(1 for sc,_ in prompts if sc['breath'])} tho"
          f" · {len(link)} chuyen ({pct}%)")
    if pct > 30:
        fails += 1
        print(f"  🔴 CANH CHUYEN {pct}% > tran 30% — them khoanh khac hoac ha xuong canh tho."
              f" Thua canh chuyen = 'phong canh co nguoi di lai', dung benh vong 1.")
        print("     " + ", ".join(sc["id"] for sc in link))
    if emo * 100 // n < 30:
        fails += 1
        print(f"  🔴 KHOANH KHAC chi {emo*100//n}% < san 30% — video se khong co cam xuc.")
    return fails


def main():
    prompts = [(sc, build(sc)) for sc in SCENES]
    vd = os.path.join(ROOT, "06_VIDEO", "01_tou-no-fumoto")
    os.makedirs(vd, exist_ok=True)
    os.makedirs(os.path.join(vd, "clips"), exist_ok=True)
    flow = os.path.join(vd, "videogen_FLOW.txt")
    tenf = os.path.join(vd, "videogen_TENFILE.txt")
    with io.open(flow, "w", encoding="utf-8") as fh:
        fh.write("\n\n".join(p for _, p in prompts) + "\n")
    with io.open(tenf, "w", encoding="utf-8") as fh:
        fh.write("# TAP 01 「塔のふもとの一日」 — 34 canh x 8s = 4:32\n")
        fh.write(f"# moc toc do do tu mau: {PACE_MEASURED}\n#\n")
        for i, (sc, _) in enumerate(prompts, 1):
            fh.write(f"{i:02d}\tep01_{sc['id']}.mp4\t{sc['pose']}/{sc['pace']} · "
                     f"{sc['sky']}/{sc['light']} · crowd={sc['crowd']} · "
                     f"{'THAP ' if sc['mega'] else ''}"
                     f"{'EMO ' if sc['emo'] else ''}{'THO ' if sc['breath'] else ''}"
                     f"cast={','.join(sc['cast']) or '-'}"
                     f"{'  ← ' + sc['thread'] if sc['thread'] else ''}\n")

    L = [len(p) for _, p in prompts]
    from collections import Counter
    n = len(prompts)
    print(f"\n《塔のふもとの一日》  {n} canh x 8s = {n*8//60}:{n*8%60:02d}")
    print(f"prompt: {min(L)}–{max(L)} ky, TB {sum(L)//n}")
    print(f"tu the : {dict(Counter(s['pose'] for s in SCENES))}")
    print(f"troi   : {dict(Counter(s['sky'] for s in SCENES))}")
    print(f"dam dong: {dict(Counter(s['crowd'] for s in SCENES))}")
    print(f"THAP xoan: {sum(s['mega'] for s in SCENES)}  ·  KHOANH KHAC: {sum(s['emo'] for s in SCENES)}"
          f"  ·  canh THO: {sum(s['breath'] for s in SCENES)}")
    print(f"cast     : {dict(Counter(c for s in SCENES for c in s['cast']))}")
    print("\nSOI CHI CUA VAT (luat ① ke khong loi):")
    for sc in SCENES:
        if sc["thread"]:
            print(f"   {sc['id']:<18} {sc['thread']}")
    print("\nGATE:")
    bad = gate(prompts)
    print(f"  ✅ SACH {n}/{n}" if not bad else f"  🔴 {bad} canh LOI")
    print(f"\n-> {flow}\n-> {tenf}")
    print("\n⭐ GEN 3 CANH DAI DIEN TRUOC (dong 4 · 24 · 33), soi bang"
          "\n   check_test_world.py roi moi gen ca tap — 3 canh do la 3 thu khac nhau ca tap dua vao.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
