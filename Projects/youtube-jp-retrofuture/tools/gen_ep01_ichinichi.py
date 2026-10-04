# -*- coding: utf-8 -*-
"""
TẬP 01「塔のふもとの一日」— BẢN Ⓑ: BÁN KHÔNG KHÍ, KHÔNG KỂ CHUYỆN (user chốt 2026-09-22).

⛔ Thay `gen_prompts_ep01.py` (bản có mạch truyện mẹ-đan-áo). File cũ giữ lại để tra, KHÔNG dùng.

VÌ SAO ĐỔI — đo được trên bản render 40 clip:
  🔴 Cảnh GIEO (mẹ đặt bát, lỗ sờn ở khuỷu áo con) **KHÔNG CÓ CÁI LỖ**. Con bé mặc áo lành lặn.
     Mắt xích đầu không tồn tại trên màn hình ⇒ 33 cảnh sau chỉ là người đi lại trong một thị
     trấn đẹp. Đó chính là "xem chả có cảm xúc gì".
  🔴 Nguyên nhân KHÔNG sửa được bằng prompt: **t2v không vẽ được chi tiết nhỏ có chủ đích**.
     Lỗ thủng trên khuỷu áo ở cỡ medium shot là vài chục pixel — model bỏ qua.
     Cùng họ `feedback_ai_video_hong_thao_tac_tay` và luật "số phải do FONT vẽ".
  🔴 Và video mẫu (PUotm8YDbKM) **vốn không kể chuyện** — nó bán KHÔNG KHÍ: một ngày ở thị trấn,
     không nhân vật chính, không mắt xích. Nhét truyện ngắn có gieo-và-trả vào format đó, bằng
     một công cụ không vẽ nổi manh mối, là sai ở tầng thiết kế chứ không phải tầng thi hành.

⭐ CÁI ĐƯỢC của bản Ⓑ, ngoài việc hết lỗi trên:
  · **Bỏ hẳn CAST_LOCK** — không còn nhân vật xuyên suốt nên không phải khoá danh tính, thứ t2v
    vốn không làm được (`feedback_nhan_vat_dong_nhat_va_noi_lien`: 34/41 clip trôi mặt).
  · Mỗi cảnh TỰ ĐỦ ⇒ gen lại một cảnh không ảnh hưởng cảnh nào khác.
  · Hỏng một cảnh thì bỏ, không sập mạch.

CÁI GIỮ NGUYÊN (đã đo là đúng): thế giới v3 · tốc độ creep · ALIVE · khoảnh khắc 3 nhịp ·
chữ XIN-đừng-CẤM · thứ tự khối.

CÁI THAY THẾ MẠCH TRUYỆN: **nhịp một ngày** (tinh mơ → sáng → trưa → chiều → tối) + mỗi cảnh
phải có MỘT thứ đáng nhìn. Không có gieo, không có trả, không có sợi chỉ của vật.

Chạy:  python tools/gen_ep01_ichinichi.py
Xuất:  06_VIDEO/01_tou-no-fumoto/videogen_FLOW.txt  ·  videogen_TENFILE.txt
"""
import io, re, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from blocks_s100 import (ALIVE, HEAD, REAL, PEOPLE, POV, TOWN, MEGACITY, RETRO_TECH, GREEN,
                         MATERIALS, WALK, STAND, HANDHELD, PACE, PACE_MEASURED, SLOW_STAND,
                         GROUND, EASE, CALM, MOMENT, AVOID, NO_TEXT_NUM, SKY, LIGHT, OPTICS,
                         CROWD, TAIL, TAIL_SIGN, POSE_BLOCK)

S = lambda **k: k

# ─────────────────────────────────────────────────────────────────────────────
# 34 CẢNH — MỘT NGÀY Ở THỊ TRẤN. Mỗi cảnh TỰ ĐỦ, không cảnh nào cần cảnh khác.
#   emo   = có khoảnh khắc người (3 nhịp, tả bằng cơ thể)
#   breath= cảnh thở, không người nào trong khung
#   link  = cảnh chuyển: có người nhưng không phải khoảnh khắc (trần 30%)
#   ⛔ KHÔNG có cast lock, KHÔNG có thread — đó là điểm khác cốt lõi của bản Ⓑ
# ─────────────────────────────────────────────────────────────────────────────
SCENES = [
# ══ TINH MƠ ════════════════════════════════════════════════════════════════
 S(id="01_yoake", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="none",
   mega=True, emo=False, breath=True,
   you="standing in the narrow back lane before anyone else is up",
   set="A view down a narrow back lane still blue with before-dawn, the shopfronts shuttered close on "
       "both sides, a street lamp with a fluted glass shade still burning above you with its filament "
       "visible inside, a bundle of pneumatic message tubes running along the frontages with brass caps "
       "at the bends, potted plants crowding every doorstep. At the far end, beyond the roofs, the "
       "spiralling tiered towers of the great city stand up into the sky.",
   act="Nobody is out. A thin wisp of white steam leaks from a joint in the tubes and drifts up and "
       "away. The street lamp fades as the sky lightens. Far above, the tops of the towers catch the "
       "first sun long before it reaches the ground.",
   cam="the view holds steady down the lane with the lit towers above the far roofs"),

 S(id="02_hoshimono", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="none",
   mega=True, emo=False, breath=True,
   you="standing at the concrete parapet at the top of the worn steps above the roofs",
   set="A view out over the tiled and corrugated-steel roofs of the little streets packed close below "
       "you, their aerials and water tanks and washing lines, a big old tree leaning over them, ivy "
       "climbing the parapet in a broad sheet at the left edge. Beyond the roofs stand the spiralling "
       "tiered towers.",
   act="Nobody is in the shot. Last night's washing hangs damp and heavy and stirs in the cold air. A "
       "crow walks along the top of a water tank and drops out of sight. The shadow of the nearest "
       "tower lies right across the whole town.",
   cam="the view holds steady out over the roofs with the towers beyond"),

 S(id="03_pan", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="few",
   mega=False, emo=True, breath=False,
   you="standing in the lane outside the bakery where the light is already on",
   set="A view of a small bakery in the dark lane, the only lit shopfront on the street: warm light "
       "spilling out over the wet kerbstones, a canvas awning, one small board above the door carrying "
       "the single word パン in large clean brush strokes, bicycles against the tiled wall, potted "
       "plants along the step, and steam rising from a vent at the side of the building.",
   act="The baker, a heavy man in his fifties with a towel round his neck, carries a wooden tray out "
       "from the back and sets it on the counter inside the window; the steam comes off the tray and up "
       "past his face, and he stands in it a moment with his hands on the counter before he turns back.",
   cam="the view holds steady on the lit shopfront with the dark lane around it"),

 S(id="04_shutter", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="few",
   mega=False, emo=True, breath=False,
   you="standing a few steps from the shopfront as it opens for the day",
   set="A view of a shopfront in the lane, its wooden shutter still down, a plain painted board above "
       "the doorway with nothing written on it, a rolled canvas awning, bicycles against the wall "
       "beside a red cylindrical post box, and a brass and glass vending stand with a pressure dial "
       "standing at the kerb in the near foreground.",
   act="The shopkeeper, a man in his sixties in shirtsleeves seen mostly from behind, pushes the "
       "shutter up its runners and props it; then he stands in his own doorway looking out down the "
       "lane, rubs the back of his neck once, and turns and goes in.",
   cam="the view holds steady on the shopfront with the lane running away beside it"),

 S(id="05_kiri", pose="stand", pace="creep", sky="dawn", light="dawn", crowd="none",
   mega=True, emo=False, breath=True,
   you="standing at the mouth of the lane as the mist comes up the street",
   set="A view straight down the lane, shopfronts close on both sides with awnings and cloth noren, a "
       "red post box, bicycles against glazed tile, dozens of potted plants, a street lamp with a "
       "fluted glass shade still lit, tangled overhead wires crossing above, and the tiered towers at "
       "the far end.",
   act="Nothing happens but the mist. It comes up the lane from the far end, pouring low between the "
       "kerbstones and around the potted plants until the far shopfronts go soft and then vanish in it "
       "and the street lamps become pale discs; the towers fade to faint outlines and then to nothing. "
       "Only the nearest eaves stay sharp.",
   cam="the view holds steady down the lane with the towers at the far end"),

# ══ SÁNG ═══════════════════════════════════════════════════════════════════
 S(id="06_tsuugaku", pose="walk", pace="creep", sky="day", light="day", crowd="some",
   mega=True, emo=False, breath=False,
   you="walking down the lane in the middle of the morning traffic of people",
   set="A view along the lane in the morning sun, shopfronts open on both sides with their goods "
       "stacked out to the kerb, cloth noren in the doorways, bicycles against every wall, tangled "
       "wires crossing above, and at the far end the spiralling tiered towers with a slim monorail "
       "threading between them.",
   act="Schoolchildren in uniform go past in twos and threes, satchels on their backs, all of them "
       "seen from behind or from the side; a woman with a shopping basket comes the other way and they "
       "part around her without anyone looking up.",
   cam="the shot begins framed down the lane with the people ahead of you, the camera then edges "
       "forward barely at all, and the shot ends a little further in with the lane opened out"),

 S(id="07_basutei", pose="stand", pace="creep", sky="day", light="day", crowd="some",
   mega=False, emo=True, breath=False,
   you="standing at the bus stop at the end of the street among the people waiting",
   set="A view at a bus stop: a timber shelter, a plain unlettered enamel sign on a post, a bundle of "
       "pneumatic tubes turning the corner of the building behind with brass caps at the bend, potted "
       "plants along the kerb, and the little shops of the street running away beyond.",
   act="An old woman on the bench has a furoshiki bundle on her knees. She works the knot loose, looks "
       "into it, folds it closed again and pats it flat with the palm of her hand — and only then does "
       "she look up the road with everyone else.",
   cam="the view holds steady on the shelter and the waiting people with the street beyond"),

 S(id="08_tabako", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   mega=True, emo=True, breath=False,
   you="standing in the lane beside the tobacconist's little window",
   set="A view of a tiny tobacconist's on the left of the lane: a small sliding window open onto the "
       "street, its counter crowded with boxes, an electric fan with a brass cage turning slowly on the "
       "counter, one small board above it carrying the single word たばこ in large clean brush strokes, "
       "and an old woman sitting just inside. On the right a bicycle leans against a glazed-tile wall "
       "beside a red post box; at the far end of the lane the tiered towers stand up into the sky.",
   act="The old woman in the window has her head down over her knitting. She comes to the end of a row, "
       "stops, and holds the work out at arm's length — her eyes go first and crease into two slits, "
       "the cheeks pushing up, the mouth barely opening — then she lowers it back into her lap and her "
       "hands start again.",
   cam="the view holds steady on the open window with the lane and the far towers beyond it"),

 S(id="09_mizumaki", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   mega=False, emo=True, breath=False,
   you="standing on the pavement outside a shop as the water goes down",
   set="A view of a shopfront with the pavement dry and dusty in front of it, potted plants crowding "
       "the step, a copper pipe polished warm running down the wall, a canvas awning, bicycles against "
       "the tile, and a shallow tin bucket on the kerb.",
   act="A woman in an apron throws water across the pavement from the bucket in one flat arc; the dust "
       "goes dark where it lands and the air above it turns cool and hazy for a second. She looks at "
       "the wet stone, tips the last of it out at the foot of the plants, and goes back in.",
   cam="the view holds steady on the shopfront and the wet pavement in front of it"),

 S(id="10_ichiba", pose="walk", pace="creep", sky="day", light="day", crowd="busy",
   mega=True, emo=False, breath=False,
   you="walking slowly into the market street at its busiest",
   set="A view down a packed market street, sloping stands of vegetables in wooden crates on both "
       "sides, plain unlettered painted boards above them, canvas awnings low overhead, paper lanterns "
       "strung along, bicycles parked against the pillars, a brass and glass vending stand with a "
       "pressure dial at the near corner, and the tiered towers beyond the roofs at the far end.",
   act="The crowd moves both ways along the stands, nobody hurrying, nearly all seen from behind or "
       "from the side; a shopkeeper leans out over his crates to hand something down and is hidden "
       "again by the people passing.",
   cam="the shot begins framed down the market street, the camera then edges forward barely at all, "
       "and the shot ends a little deeper in with the stands opened out on either side"),

 S(id="11_yaoya", pose="stand", pace="creep", sky="day", light="day", crowd="busy",
   mega=False, emo=True, breath=False,
   you="standing at the greengrocer's stand in the market street",
   set="A view of a grocer's sloping stand of vegetables in wooden crates, a plain painted board above "
       "it, a canvas awning, paper lanterns overhead, bicycles against the pillar beside, and a "
       "mechanical cash register with rows of round keys at the end of the counter.",
   act="The grocer, a broad man in his fifties with a towel round his neck, holds a wrapped parcel out "
       "to a customer with both hands; she takes it, and his hands are already reaching back behind him "
       "for the next parcel before she has finished bowing her head over it.",
   cam="the view holds steady on the stand with the two of them at it"),

 S(id="12_hanbaiki", pose="stand", pace="creep", sky="day", light="day", crowd="some",
   mega=False, emo=True, breath=False,
   you="standing beside the vending stand at the corner",
   set="A view of a tall brass and glass vending stand at a street corner, a round pressure dial on its "
       "front and copper piping down its side polished where hands have touched it, with the shopfronts "
       "and hanging lanterns of the street behind and bicycles in a row against the pillar.",
   act="A small boy stops dead in front of the dial and tips his head right back to look up at it, his "
       "mouth open. His mother's hand comes into the frame and rests on the top of his head and steers "
       "him away — and he goes, still looking back over his shoulder at it.",
   cam="the view holds steady on the vending stand with the boy in front of it"),

# ══ TRƯA ═══════════════════════════════════════════════════════════════════
 S(id="13_mahiru", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   mega=True, emo=False, breath=True,
   you="standing at the junction in the middle of the day",
   set="A view at a junction of two narrow streets under the high midday sun, glazed tile and painted "
       "concrete walls, a red post box, a street lamp, dozens of potted plants, and beyond the roofs "
       "the spiralling tiered towers rising tier above tier into the sky.",
   act="Nobody is near. The shadow of the tower is at its shortest of the day, folded in tight at the "
       "foot of the wall. Heat shivers up off the road surface. A cat lies stretched in the strip of "
       "shade and its tail moves once.",
   cam="the view holds steady on the junction with the towers above the roofs"),

 S(id="14_shokudou", pose="stand", pace="creep", sky="window", light="interior", crowd="some",
   mega=False, emo=True, breath=False,
   you="sitting at the counter of a small eating house at lunchtime",
   set="A view along the worn timber counter of a small eating house: jars and bottles crowding the "
       "shelves behind, a glass globe lamp in a cage of brass ribs above, narrow paper strips along the "
       "wall with nothing legible on them, an electric fan with a brass cage turning at the end of the "
       "counter, and the bright doorway onto the street beyond.",
   act="The owner, a woman in her forties in a green apron, sets a bowl of noodles down in front of a "
       "man in shirtsleeves who sits with his back to you; the steam comes straight up off it into his "
       "face and he leans back from it, then leans in again and picks up his chopsticks.",
   cam="the view holds steady along the counter with the two of them and the bright doorway beyond"),

 S(id="15_hirune", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   mega=False, emo=True, breath=False,
   you="standing in the lane outside a shop in the dead hour of the afternoon",
   set="A view of a shopfront in the early afternoon, the awning throwing a hard bar of shade across "
       "the step, potted plants crowding the doorway, a bicycle against the tile, a cat on the warm "
       "stone, and a low stool just inside the shade.",
   act="An old man sits on the stool inside the shade with a folded newspaper on his knee and his chin "
       "gone down onto his chest. The paper slides off his knee onto the step; he comes half awake, "
       "puts a hand down for it without opening his eyes, and settles again.",
   cam="the view holds steady on the shopfront with him in the bar of shade"),

 S(id="16_kouri", pose="stand", pace="creep", sky="day", light="day", crowd="some",
   mega=False, emo=True, breath=False,
   you="standing on the pavement by the ice stall",
   set="A view of a small ice stall at the kerb: a brass and glass machine with a pressure dial, one "
       "small board above it carrying the single word 氷 in large clean brush strokes, a canvas awning "
       "over it, potted plants and bicycles along the kerb, and the shopfronts of the street behind.",
   act="Two schoolgirls sit on the kerb sharing one paper cup of shaved ice. The one holding it turns "
       "the cup round in her hands so that the side that has not been eaten yet faces the other girl, "
       "and holds it out without saying anything.",
   cam="the view holds steady on the two of them on the kerb with the stall behind"),

 S(id="17_denki", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   mega=False, emo=True, breath=False,
   you="standing outside the window of the electrical shop",
   set="A view of an electrical shop window: a television in a timber cabinet on thin splayed legs "
       "with a deeply curved glass screen, glass bulbs and coils of flex crowded around it, a plain "
       "unlettered board above, a low canvas awning, bicycles and potted plants at the kerb in the near "
       "foreground.",
   act="An old man stands at the window with both hands behind his back watching the curved screen, "
       "which shows nothing but soft grey static. A boy stops beside him, looks at the screen, looks up "
       "at the old man's face, and then looks back at the screen and stands the same way.",
   cam="the view holds steady on the window with the two of them at the edge of the frame"),

 S(id="18_rojiura", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   mega=False, emo=False, breath=True,
   you="standing in a back alley barely wider than your shoulders",
   set="A close view along a back alley between two buildings, glazed tile and painted concrete on both "
       "sides within arm's reach, a copper pipe running down one wall, ivy in a broad healthy sheet "
       "over the other, crates stacked against the wall, a bicycle, and a strip of bright sky far above "
       "between the roofs.",
   act="Nobody is in the alley. Washing hangs on a line strung across it high up and moves in the "
       "draught; water drips steadily from a pipe joint into a bucket; a moth turns in the one bar of "
       "sun that reaches down between the walls.",
   cam="the view holds steady along the alley with the strip of sky far above"),

 S(id="19_arcade", pose="walk", pace="creep", sky="window", light="interior", crowd="busy",
   mega=False, emo=False, breath=False,
   you="walking very slowly into the covered shopping arcade",
   set="A view down the middle of a covered shopping street: a translucent corrugated roof high "
       "overhead letting the daylight down in long pale bars, shopfronts opening onto the walkway with "
       "their goods stacked out to the edge, plain unlettered boards above the frontages, cloth noren "
       "and canvas awnings hanging low, paper lanterns strung above, bicycles in rows against the "
       "pillars.",
   act="The afternoon crowd moves both ways under the roof, unhurried, nearly all seen from behind; "
       "a shopkeeper sweeps the strip of walkway in front of his own doorway and steps back to let "
       "people through without stopping.",
   cam="the shot begins framed down the arcade with the far end soft and bright, the camera then edges "
       "forward barely at all, and the shot ends with only a little more of the arcade opened out"),

# ══ CHIỀU ══════════════════════════════════════════════════════════════════
 S(id="20_shagekou", pose="stand", pace="creep", sky="day", light="day", crowd="some",
   mega=True, emo=False, breath=False,
   you="standing at the mouth of the lane as the sun goes low along the street",
   set="A view along the lane with the low afternoon sun coming in flat, the shopfronts thrown into "
       "long bars of light and shade, a red post box, bicycles, dozens of potted plants, a street lamp "
       "with a fluted glass shade not yet lit, and beyond the roofs the tiered towers going gold at "
       "their tops.",
   act="People come and go along the lane, seen mostly from behind, their shadows running long ahead of "
       "them across the stone; a three-wheeled delivery truck with a riveted boiler goes past and its "
       "steam turns gold where the light catches it.",
   cam="the view holds steady down the lane with the low sun along it"),

 S(id="21_sentou", pose="stand", pace="creep", sky="dusk", light="dusk", crowd="some",
   mega=False, emo=True, breath=False,
   you="standing outside the bathhouse as the evening starts",
   set="A view of a bathhouse entrance, a cloth noren hanging in the doorway with the single word ゆ on "
       "it in large clean brush strokes, steam drifting out along the pavement under it, a rack of "
       "wooden clogs to one side, bicycles against the tiled wall, potted plants along the step, and "
       "the lamps of the street coming on behind.",
   act="An old man comes out through the noren with a towel on his head and his face still red from the "
       "heat; he stops on the step, lets his breath all the way out, and stands there a moment in the "
       "cool air before he starts down the street.",
   cam="the view holds steady on the bathhouse entrance with the steam coming out under the noren"),

 S(id="22_kouen", pose="stand", pace="creep", sky="dusk", light="dusk", crowd="few",
   mega=True, emo=True, breath=False,
   you="standing at the edge of a small square between the houses",
   set="A view of a small stone square between the buildings, a big old tree leaning over it, a timber "
       "bench, potted plants along the walls, a street lamp with a fluted glass shade just coming on, "
       "and beyond the roofs the tiered towers with the last of the sun on their upper levels.",
   act="Three children crouch in a ring over a game of marbles on the flat stone. One of them flicks, "
       "the others lean in together over the same small patch of ground, and then all three heads go "
       "back at once at what happened.",
   cam="the view holds steady on the square with the children and the tree"),

 S(id="23_monohoshi", pose="stand", pace="creep", sky="dusk", light="dusk", crowd="none",
   mega=False, emo=False, breath=True,
   you="standing on a narrow timber veranda as the light goes",
   set="A close view of a washing line strung between two timber posts at the edge of a veranda, cloths "
       "hanging on it, the glazed-tile wall and a copper pipe behind, potted plants along the boards, "
       "and the roofs of the lane soft beyond.",
   act="Nobody is in the shot. The cloths fill out with the wind and fall slack and fill again. The "
       "light on the wall behind them has turned the colour of honey and is climbing slowly up it as "
       "the sun drops.",
   cam="the view holds steady on the line and the cloths with the wall behind"),

 S(id="24_kage_gyaku", pose="stand", pace="creep", sky="dusk", light="dusk", crowd="none",
   mega=True, emo=False, breath=True,
   you="standing at the concrete parapet above the roofs again at the end of the day",
   set="A view out over the same roofs as the morning, the aerials and water tanks and washing lines, "
       "the big old tree, the ivy on the parapet at the left edge — and beyond them the spiralling "
       "tiered towers, tier widening above tier, their terraces planted green, joined by slender "
       "bridges and elevated roadways high in the air.",
   act="Nobody is in the shot. The shadow of the tower now lies the opposite way across the town from "
       "where it lay in the morning. A single monorail carriage moves slowly between the tiers. A thin "
       "plume of white steam rises from among the roofs and leans away on the wind.",
   cam="the view holds steady out over the roofs with the towers and the piled cloud above them"),

 S(id="25_hi_wo_ireru", pose="stand", pace="creep", sky="dusk", light="dusk", crowd="few",
   mega=False, emo=True, breath=False,
   you="standing under the eaves as the lanterns are lit along the street",
   set="A close view of a paper lantern hanging under an eave against the deep blue of dusk, the timber "
       "and glazed tile of the shopfront behind it, potted plants below, a bicycle against the wall, "
       "and the lit windows of the street soft in the distance.",
   act="A hand comes up from below with a taper. The wick catches and the paper comes up warm and the "
       "whole lantern turns a few degrees on its cord; the hand and the taper withdraw out of the frame "
       "and the lantern goes on turning by itself, slower and slower.",
   cam="the view holds steady on the lantern with the dusk street behind it"),

 S(id="26_kaerimichi", pose="walk", pace="creep", sky="dusk", light="dusk", crowd="some",
   mega=True, emo=False, breath=False,
   you="walking home along the lane with everyone else at the end of the day",
   set="A view along the lane as the lamps come on, the shopfronts warm on one side and in shadow on "
       "the other, paper lanterns lit under the eaves, bicycles, potted plants, the drain grates and "
       "worn kerbstones underfoot, and the tiered towers standing beyond the roofs with their first "
       "lit windows.",
   act="People go home along the lane, all of them walking away from you, a few carrying parcels; a "
       "woman stops at a doorway and calls in, and a child comes out and goes with her without a word.",
   cam="the shot begins framed down the lit lane, the camera then edges forward barely at all, and the "
       "shot ends a little deeper in with the lit shopfronts opened out on either side"),

# ══ TỐI ════════════════════════════════════════════════════════════════════
 S(id="27_yuushoku", pose="stand", pace="creep", sky="night", light="interior_night", crowd="none",
   mega=False, emo=True, breath=False,
   you="sitting at a low table in a front room where the family is eating",
   set="A view across a low wooden table in a small front room at night, a glass globe lamp in a cage "
       "of brass ribs lit warm above it, bowls on the wood, worn tatami, the window a flat black "
       "rectangle, a television in a timber cabinet dark in the corner.",
   act="A woman and an old man eat together at the table without talking. She reaches across and moves "
       "the dish nearer to him without looking up from her own bowl; he takes from it, and only "
       "afterwards does he glance at her and go back to eating.",
   cam="the view holds steady across the table with both of them and the dark window"),

 S(id="28_terebi", pose="stand", pace="creep", sky="night", light="interior_night", crowd="none",
   mega=False, emo=False, breath=True,
   you="sitting on the tatami in the corner of a room at night",
   set="A close view of a television in a timber cabinet on thin splayed legs, its deeply curved glass "
       "screen showing soft grey static, a three-bladed electric fan with a brass cage turning slowly "
       "beside it, the hem of a cloth on a low table lifting, a glass globe lamp warm further off.",
   act="Nobody is in the shot. The static moves on the curved glass. The fan comes round to the end of "
       "its arc and the cloth on the table lifts and settles, and the light of the screen goes over the "
       "wall behind it.",
   cam="the view holds steady on the cabinet and the fan and the corner of the tatami"),

 S(id="29_yatai", pose="stand", pace="creep", sky="night", light="night", crowd="some",
   mega=False, emo=True, breath=False,
   you="standing at a food stall on the corner late in the evening",
   set="A view of a small food stall under a canvas awning at night, steam pouring up off the pot into "
       "the cold air, a paper lantern lit above it, bottles and jars along the ledge, stools along the "
       "front, and the dark street with a few lit windows behind.",
   act="The stall keeper lifts the lid off the pot and the steam goes straight up and blots out his "
       "face for a moment; the two men on the stools lean back from it, and one of them laughs at "
       "something and puts his hand flat on the counter.",
   cam="the view holds steady on the stall with the steam coming up off the pot"),

 S(id="30_arai", pose="stand", pace="creep", sky="night", light="interior_night", crowd="none",
   mega=False, emo=True, breath=False,
   you="standing in a kitchen doorway at night",
   set="A view of a small kitchen at night, one lamp with a fluted glass shade over the sink, a "
       "spherical steel rice cooker cold on the counter, copper pipe running up the wall, a draining "
       "rack, and the window black above the sink.",
   act="A woman washes bowls at the sink with her back to you. She stops with her hands still in the "
       "water and turns her head towards the window as if she heard something outside, waits, and then "
       "goes back to it and stacks the next bowl on the rack.",
   cam="the view holds steady on the sink with her at it and the black window above"),

 S(id="31_yomichi", pose="walk", pace="creep", sky="night", light="night", crowd="few",
   mega=True, emo=False, breath=False,
   you="walking down the lit lane late at night",
   set="A view along the lane late at night, the shops shut and only the paper lanterns burning under "
       "the eaves, the stone wet with mist, potted plants black along the walls, a bicycle, a bundle of "
       "pneumatic tubes along the frontages — and beyond the roofs the tiered towers standing dark with "
       "thousands of tiny lit windows scattered up them.",
   act="One man walks away from you down the middle of the lane, small and seen from behind, and turns "
       "off at the far end; the lanterns turn slightly as he passes under them.",
   cam="the shot begins framed down the lit lane, the camera then edges forward barely at all, and the "
       "shot ends with the far end of the lane and the dark beyond it"),

 S(id="32_hotaru", pose="stand", pace="creep", sky="night", light="night", crowd="none",
   mega=False, emo=False, breath=True,
   you="standing at a rail at the edge of the town looking down at the bank",
   set="A close view of a wet ivy-covered bank below a timber rail at night, ferns and weeds green in "
       "the lamp light, a copper pipe running down through them, water running somewhere out of sight, "
       "and the lit windows of the town soft and far behind.",
   act="Nobody is in the shot. Fireflies drift along the bank, a few of them rising slowly up past the "
       "rail and out of the top of the frame, and the wet leaves move where the water runs under them.",
   cam="the view holds steady on the bank and the rail with the town lights behind"),

 S(id="33_machi_yoru", pose="stand", pace="creep", sky="night", light="night", crowd="none",
   mega=True, emo=False, breath=True,
   you="standing at the parapet above the roofs one last time",
   set="A wide view out over the whole town at night from the concrete parapet: the roofs black, the "
       "windows and paper lanterns scattered warm across them, the big old tree a dark shape, the ivy "
       "on the parapet at the near edge — and beyond, the spiralling tiered towers standing enormous "
       "and dark with thousands of lit windows going up into the night sky.",
   act="Nobody is in the shot. A lit monorail carriage crosses slowly between the tiers, small and "
       "bright. One window low in the town goes out. Steam drifts up somewhere among the roofs and "
       "catches the light from below.",
   cam="the view holds steady out over the dark town with the lit towers above"),

 S(id="34_saigo_no_mado", pose="stand", pace="creep", sky="night", light="night", crowd="none",
   mega=True, emo=False, breath=True,
   you="standing in the lane looking back at the last lit window",
   set="A view of the front of a small house from the dark lane, one small square window still lit warm "
       "yellow among the dark timber and glazed tile, a paper lantern burning by the door, potted "
       "plants black along the step, a copper pipe running down the wall — and above the roofs the "
       "tiered towers with their thousands of lit windows going up into the night.",
   act="Nobody is in the shot. The lit window holds. A shadow crosses it once from inside. Then the "
       "light goes out, and only the lantern by the door is left burning — and above it, the windows "
       "of the towers, still lit, all night.",
   cam="the view holds steady on the front of the house with the towers above the roofs"),
]

_POVIFY = [(r"the camera then edges", "you then move"), (r"the camera then drifts", "you then draw"),
           (r"the camera then", "you then"), (r"the camera", "you")]


def povify(t):
    for a, b in _POVIFY:
        t = re.sub(a, b, t)
    return t


def build(sc):
    P = [HEAD]
    if sc["mega"]:
        P.append(MEGACITY)
    P += [RETRO_TECH, NO_TEXT_NUM, REAL, POV, ALIVE]
    P.append("You are " + sc["you"] + ", and this is what you see.")
    P.append(sc["set"])
    if sc["emo"]:
        P.append(MOMENT)
    P.append(sc["act"])
    if CROWD[sc["crowd"]]:
        P.append(CROWD[sc["crowd"]])
    P.append(CALM)
    if sc["pose"] == "walk":
        P.append("Your movement, the only one in this shot: " + povify(sc["cam"]) + "; " + EASE + ". "
                 + PACE[sc["pace"]] + " " + GROUND + " " + WALK)
    else:
        P.append("The framing does not change at all from the first frame to the last: the shot holds "
                 "one single unmoving view for the whole eight seconds and the viewpoint never pushes "
                 "in, never pulls back, never pans and never drifts — " + povify(sc["cam"]) +
                 " for the whole shot. What changes is only what happens inside that unmoving frame. "
                 + SLOW_STAND + " " + POSE_BLOCK[sc["pose"]])
    P += [HANDHELD, TOWN, GREEN, MATERIALS, PEOPLE, AVOID]
    if SKY[sc["sky"]]:
        P.append(SKY[sc["sky"]])
    P.append(LIGHT[sc["light"]])
    P.append(OPTICS)
    has_sign = bool(re.search(r"[぀-ヿ一-鿿]", sc["set"] + sc["act"]))
    P.append(TAIL_SIGN if has_sign else TAIL)
    return " ".join(x.strip() for x in P if x.strip())


JP_OK = tuple("ゆ氷たばこパンさかな")


def _at(lo, p, key, limit, label):
    i = lo.find(key)
    return (f"{label}<={limit}%", (i * 100 // len(p) if i >= 0 else 999) <= limit)


def gate(prompts):
    bad = ["35mm", "16mm", "hands only", "feet only", "pedestal", "crane down", "floating island",
           "rock pillar", "sea of cloud", "suspension bridge", "16:9", "1920x1080"]
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
        chk = dict([
            _at(lo, p, "impossible spiralling ziggurats", 12, "THAP") if sc["mega"] else ("THAP<=12%", True),
            _at(lo, p, "right here in the foreground within arm's reach", 22, "VT-TIEN-CANH"),
            _at(lo, p, "no distorted, melted or asymmetric faces", 10, "CAM-MAT"),
            _at(lo, p, "most of the shop signboards", 28, "CAM-CHU"),
            _at(lo, p, "this is a moving picture, not a photograph: something", 8, "ALIVE-HEAD"),
        ])
        chk.update({
            "cam-than-nguoi-xem": "no part of the viewer's own body" in lo,
            "khong-xin-anime": not [m for m in re.finditer(r"(?<!not )(?<!never )anim\w*", lo)],
            "lop-gan-chat":  "there is no empty wall anywhere" in lo,
            "bien-tron":     "at most two signs anywhere in the frame carry any writing" in lo,
            "khung-phai-song": "something in the frame is always moving" in lo,
            "cam-do-hien-dai": "no face masks on anyone" in lo,
            "dung-mot-loai":   (sc["emo"] + sc["breath"]) <= 1,
            "tho-thi-khong-nguoi": (sc["crowd"] == "none") if sc["breath"] else True,
            "emo-thi-may-dung":    (sc["pose"] == "stand") if sc["emo"] else True,
            "co-vong-cung":  ("three beats and the middle one is the peak" in lo) if sc["emo"] else True,
            "troi-va-sang-cung-buoi":
                (sc["light"] == "interior" and sc["sky"] != "night")
                or (sc["light"] == "interior_night" and sc["sky"] == "night")
                or (sc["sky"] == "window" and sc["light"] == "interior")
                or (sc["sky"] == sc["light"]),
            # Canh NGOAI TROI ma khung CO TROI thi phai khai hau canh, khong thi model tu dien
            # thanh pho hien dai. Canh CAN (mat tiem, quay, day phoi) khong thay troi => mien.
            # ⛔ KHONG liet ke id bang tay — suy tu chinh mo ta canh, khong thi sua canh la lech.
            "ngoai-troi-phai-khai-hau-canh":
                sc["mega"] or sc["light"].startswith("interior")
                or not re.search(r"sky|towers?|horizon", sc["set"], re.I),
            "khong-tu-cam":  not [b for b in bad if b in scan],
            "chu-chi-tu-quen": all(ch in JP_OK for ch in re.findall(r"[぀-ヿ一-鿿]", p)),
            "cam-so-goc":    "no timestamps, no counters" in lo,
        })
        f = [k for k, v in chk.items() if not v]
        if f:
            fails += 1
            print(f"  🔴 {i:02d} {sc['id']:<18} {f}")

    n = len(prompts)
    emo = sum(1 for sc, _ in prompts if sc["emo"])
    bre = sum(1 for sc, _ in prompts if sc["breath"])
    link = n - emo - bre
    print(f"  ⓘ {emo} khoanh khac · {bre} tho · {link} chuyen ({link*100//n}%)")
    if link * 100 // n > 30:
        fails += 1; print(f"  🔴 CANH CHUYEN {link*100//n}% > tran 30%")
    if emo * 100 // n < 30:
        fails += 1; print(f"  🔴 KHOANH KHAC {emo*100//n}% < san 30% — video se khong co cam xuc")
    return fails


def main():
    prompts = [(sc, build(sc)) for sc in SCENES]
    vd = os.path.join(ROOT, "06_VIDEO", "01_tou-no-fumoto")
    os.makedirs(vd, exist_ok=True)
    flow = os.path.join(vd, "videogen_FLOW.txt")
    tenf = os.path.join(vd, "videogen_TENFILE.txt")
    with io.open(flow, "w", encoding="utf-8") as fh:
        fh.write("\n\n".join(p for _, p in prompts) + "\n")
    with io.open(tenf, "w", encoding="utf-8") as fh:
        fh.write("# TAP 01 「塔のふもとの一日」 — BAN B: BAN KHONG KHI, KHONG KE CHUYEN\n")
        fh.write("# 34 canh x 8s = 4:32 · moi canh TU DU, gen lai mot canh khong anh huong canh nao\n#\n")
        for i, (sc, _) in enumerate(prompts, 1):
            fh.write(f"{i:02d}\tep01_{sc['id']}.mp4\t{sc['pose']} · {sc['sky']}/{sc['light']} · "
                     f"crowd={sc['crowd']}"
                     f"{' · THAP' if sc['mega'] else ''}"
                     f"{' · EMO' if sc['emo'] else ''}{' · THO' if sc['breath'] else ''}\n")

    L = [len(p) for _, p in prompts]
    from collections import Counter
    n = len(prompts)
    print(f"\n《塔のふもとの一日》 BAN B — {n} canh x 8s = {n*8//60}:{n*8%60:02d}")
    print(f"prompt: {min(L)}–{max(L)} ky, TB {sum(L)//n}")
    print(f"tu the : {dict(Counter(s['pose'] for s in SCENES))}")
    print(f"troi   : {dict(Counter(s['sky'] for s in SCENES))}")
    print(f"THAP   : {sum(s['mega'] for s in SCENES)}")
    print("\nGATE:")
    bad = gate(prompts)
    print(f"  ✅ SACH {n}/{n}" if not bad else f"  🔴 {bad} loi")
    print(f"\n-> {flow}\n-> {tenf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
