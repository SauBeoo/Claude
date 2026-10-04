# -*- coding: utf-8 -*-
"""gen_prompts_18 — prompt anh AI (STILL) + clip AI (MOTION) cho video 18 「働く人とお金」 (REAL-FIRST v3).

Doc 06_VIDEO/18_hataraku-okane/clips/_PLAN.json (build_slides_v3.py). Chi sinh cho o `aistill` + `ai`:
  aistill -> STILL (Nano Banana, che do Image)                 -> user luu cells_in/NN.png
  ai      -> STILL -> ⋮ Animate -> MOTION (Veo)                  -> user luu cells_in/NN.mp4
O `film` = phim PD (USAF/NPC/Universal — dokkoi da BO 23/09 vi ban quyen), KHONG sinh prompt.

🔑 CANH NEO THEO CHUOI LOI (SH), khong theo so o: timeline that ve thi so o doi, chuoi loi khong doi.
   Dong nao bi chia nhieu o -> list nhieu canh, lay theo thu tu xuat hien.
🎭 Dan mat C: mot gia dinh 5 nguoi, MAT khong doi suot video, DO doi theo thoi ky. Gate:
   python tools/check_cast_unique.py 18   (roi --write)
⛔ Khong chu so trong prompt (gate_prompt bat) — model hay in so len hinh; so lieu do FONT ve luc dung.
⛔ Khong dung mat dien vien 「どっこい生きてる」 — gia dinh nay la nguoi KHAC hoan toan.

Chay:  python tools/gen_prompts_18.py
Xuat:  06_VIDEO/18_hataraku-okane/prompts18_{STILL,MOTION}_FLOW.txt · _TENFILE.txt · _BLOCKS.md
"""
import io, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_media_library"))
from realism_blocks import build_pair, gate_prompt, gate_action, HOLD_CLAUSE, LIMIT_SHOWA  # noqa: E402

VD = HERE.parent / "06_VIDEO" / "18_hataraku-okane"

# ------------------------------------------------------------------ DAN MAT (MAT co dinh · DO theo thoi ky)
C = {
 "haha": "the mother: a slim Japanese woman with a narrow oval face, high flat cheekbones, thin arched eyebrows, a small straight nose, a small mole under her left eye, dark hair pulled back into a low plain bun",
 "chichi": "the father: a lean Japanese man with a long bony face, deep-set narrow eyes under heavy brows, a crooked nose that was once broken, a wide thin-lipped mouth, close-cropped hair",
 "ani": "the elder son: a thin Japanese boy of fifteen with a round face, thick straight eyebrows, slightly protruding ears, a short buzz cut",
 "ane": "the daughter: a Japanese girl of fifteen with a soft round face, dimpled cheeks, single-lidded eyes, a small chin, black hair in two short braids",
 "sue": "the youngest son as a child: a small Japanese boy with big ears, a wide forehead, a gap in his front teeth, a straight bowl haircut",
 "sue_old": "the youngest son today: a Japanese man in his late sixties with a wide forehead, big ears, thinning grey hair combed back, heavy-framed reading glasses",
}

# ------------------------------------------------------------------ THE GIOI theo thoi ky (showa = co dien, khong vien tuong)
W = {
 "now": "Present-day Japan, an old wooden farmhouse in a quiet Tohoku village: worn tatami, sliding paper doors, dark cedar beams, a Buddhist altar with white chrysanthemums, nothing modern in view except one plain electric lamp.",
 "p49": "Tokyo just after the war, the late nineteen-forties: bomb-damaged neighbourhoods, wooden barracks and rubble, people in patched clothes, army-surplus jackets and cloth caps.",
 "v60": "Japan in the early nineteen-sixties, a farming village in Tohoku: tin- and thatch-roofed farmhouses, rice fields, wooden utility poles, everyone in plain working clothes of the period.",
 "t60": "Japan in the early nineteen-sixties: a steam-age railway, wooden station platforms, everyone in the clothes of the period, school uniforms with stand-up collars and peaked caps.",
 "m60": "Japan in the mid nineteen-sixties, a cotton spinning mill: long rows of spinning frames, wooden floors, tall windows, young women workers in white triangular headscarves and white aprons.",
 "f60": "Japan in the nineteen-sixties, a small machine workshop in the Tokyo backstreets: lathes, oily wooden floors, bare bulbs, men in worn work jackets.",
 "c70": "Japan in the early nineteen-seventies, a Tokyo construction site for an elevated expressway: steel frames, wooden scaffolding, labourers in work jackets and cloth headbands.",
 "v70": "Japan in the early nineteen-seventies, a snowy farming village in Tohoku: deep snow on the roofs, a small wooden station, everyone in heavy winter clothes of the period.",
 "s74": "Japan in the mid nineteen-seventies, a small country town in Tohoku in spring: a wooden high school building, cherry trees in blossom, students in dark uniforms.",
 "none": "",
}

BW = "Black-and-white photograph, like a documentary still of the period."
TIN = "an old rectangular biscuit tin with a faded painted floral lid carrying no lettering"
ENV = "old brown paper envelopes, soft and creased, their faces turned away so that no writing shows"
NOTES = "two old hundred-yen banknotes folded in half so that no printing can be read"

# ------------------------------------------------------------------ CANH theo chuoi loi
# moi canh: w (the gioi) · light · still (mo ta anh) · [ai:] where/height/cam/act/alive
S = {
 # ---- HOOK (hien tai) ----
 "中には、郵便局の封筒が": [dict(w="now", light="night",
   still=f"{C['sue_old']}, in a black mourning suit, kneels on the tatami in front of an open closet at night; on the floor before him sits {TIN}, its lid just lifted, the inside packed tight with {ENV}.",
   where="a relative kneeling a little behind him on the tatami", height="seated eye height on the floor", cam="locked",
   act="the man lifts the lid of the tin the rest of the way with both hands and sets it down on the tatami beside him, then keeps his hands on his knees and looks inside.",
   alive="The lamp flame of the altar behind him flickers very slightly.")],
 "缶の底には、使われないままの": [dict(w="now", light="night",
   still=f"Looking down into {TIN} held open on a lap: the envelopes pushed to one side, and at the very bottom lie {NOTES}, flat and pale with age. Seen over the shoulder of {C['sue_old']}.")],
 "三人のうち、封筒がいちばん多かったのは、誰なのか": [dict(w="now", light="night",
   still=f"{C['sue_old']} sits back on his heels on the tatami beside the open tin; the envelopes are spread in three loose piles in front of him; he looks down at them without touching them.",
   where="a relative sitting at the far side of the low table", height="seated eye height on the floor", cam="drift",
   act="he sits very still, both hands resting on his knees, and looks from one pile of envelopes to the next; only his shoulders rise and fall with one long breath.",
   alive="Incense smoke from the altar drifts slowly across the back of the room.")],
 "答えは、缶の、最後の一枚に": [dict(w="now", light="night",
   still=f"Close view of {TIN} on the tatami: under the last envelopes, the corner of a single folded paper that is plainly not an envelope, stiffer and whiter than the rest, only its blank edge showing. Nobody is in the picture, no hands, no people; the tin sits in the upper half of the frame, the lower third is plain dark tatami.")],
 "この家族は、昭和の東北によくあった": [dict(w="v60", light="day",
   still=f"A family of five stands in front of a tin-roofed farmhouse for a photograph in summer: {C['chichi']} in a work shirt, {C['haha']} in a plain cotton kimono and apron, {C['ani']}, {C['ane']}, and {C['sue']} held by the hand; rice fields behind them.")],
 # ---- MUC 1 (den trang, 1949) ----
 "一点目。日当は": [dict(w="p49", light="dawn", bw=True,
   still=f"Before sunrise, a long line of men in caps and patched jackets waits outside a wooden employment office in a bomb-damaged Tokyo street; near the front stands {C['chichi']}, younger, in an army-surplus jacket, hands in his pockets, breath visible in the cold.")],
 "百円札が二枚と、十円札が四枚": [dict(w="p49", light="dusk", bw=True,
   still=f"At dusk, across a rough wooden counter, a clerk in a cap holds out a few folded banknotes towards {C['chichi']}, who reaches for them with both hands; other labourers wait behind him.",
   where="the next labourer waiting in line just behind him", height="standing eye height", cam="locked",
   act=f"the clerk's hand holds the folded notes out across the counter and the man takes them in both hands and draws them to his chest. {HOLD_CLAUSE}",
   alive="A bare bulb above the counter sways a little in the wind.")],
 "この家の、最初のお金です": [dict(w="p49", light="night", bw=True,
   still=f"In a bare barracks room at night, {C['haha']}, young, in a worn kimono jacket, kneels by a small low table and places {NOTES} into {TIN}; a bowl of rice sits beside it.")],
 "そして、この仕組みが終わったのは": [dict(w="p49", light="day", bw=True,
   still="A row of men with shovels and wheelbarrows repairs a cracked street between burnt-out buildings in post-war Tokyo, working in a line, seen from a little distance.")],
 "今は、給料は月に一度": [dict(w="p49", light="interior", bw=True,
   still=f"Close view of two work-hardened hands, one resting over the other on a knee, holding {NOTES}; behind them, out of focus, a wooden room lit from a window.")],
 # ---- MUC 2 (1962) ----
 "二点目。中学を出たら": [dict(w="v60", light="day",
   still=f"On a spring morning in a farming village, {C['ani']}, in a new black school uniform with a peaked cap, stands at the edge of a rice field with a small cloth-wrapped bundle, looking along the road that leads to the station.")],
 "発車のベルが鳴ると": [dict(w="t60", light="day",
   still=f"At a crowded wooden station platform, a steam train stands ready; {C['ani']} leans out of an open carriage window in his school uniform; below him {C['haha']} in a plain wool kimono reaches up; around them other mothers stand still, looking up at other windows.",
   where="another mother standing on the platform just behind her", height="standing eye height", cam="locked",
   act="the mother reaches up towards the window, and the boy's hand comes down and holds hers; neither of them lets go.",
   alive="Steam drifts slowly along the platform past the carriages.")],
 "最初の給料の、半分が": [dict(w="v60", light="interior",
   still=f"In a farmhouse kitchen, {C['haha']} in a white kappogi apron kneels at the edge of the wooden floor and holds a single envelope in both hands, looking at it without opening it; the sliding door behind her open to bright daylight.")],
 "文部科学省の学校基本調査では": [dict(w="v60", light="day",
   still="A small wooden village junior high school in the early sixties, pupils in dark uniforms crossing the dirt schoolyard after the graduation ceremony, some carrying rolled certificates tied with ribbon.")],
 "若くて、よく働いて": [dict(w="f60", light="interior",
   still="In a small Tokyo workshop, a row of teenage boys in new work clothes stands at attention on their first morning while the owner, an older man in a cardigan, looks them over.")],
 "学校教育法ができたのは": [dict(w="v60", light="interior",
   still="An empty wooden classroom in a village school, rows of small desks, a blackboard wiped clean, spring light coming through tall windows onto the floorboards.")],
 "昭和四十年度には": [dict(w="t60", light="day",
   still="A group of fifteen-year-old boys and girls in school uniforms stands with small suitcases and bundles on a station platform, a teacher beside them, waiting for the train, seen from a little distance.")],
 "十五の子が送ってくる封筒": [dict(w="v60", light="night",
   still=f"By the light of one low lamp, {C['haha']} kneels at a low table and smooths an empty envelope flat with her palm before laying it into {TIN}; the tin already holds a small neat stack.")],
 # ---- MUC 3 (1964, xuong det — 100% AI) ----
 "三つ目の封筒は、薄いものばかり": [dict(w="m60", light="interior",
   still=f"In a mill dormitory room with rows of futons, {C['ane']}, in a white headscarf, sits by the window and writes a letter on a low table, a thin envelope ready beside her hand.")],
 "機械の前に立つと、プツンと": [dict(w="m60", light="interior",
   still=f"A long aisle between two rows of spinning frames; {C['ane']}, in a white triangular headscarf and white apron, stands at the frame and watches the spindles; cotton dust hangs in the shafts of window light.",
   where="another mill girl standing at the next frame down the aisle", height="standing eye height", cam="drift",
   act="the girl walks slowly along the frame, stops, and looks up at one spindle; around her the rows of spindles keep turning steadily.",
   alive="Cotton dust floats slowly through the beams of light from the tall windows.")],
 "切れた糸を、指先で": [dict(w="m60", light="interior",
   still=f"Seen from the side, {C['ane']} leans in towards a spinning frame, both hands raised to the threads; beside and behind her, a line of other girls in white headscarves at the same frame, all bent to the same work.")],
 "姉の手紙には、いつもその一行が": [dict(w="v60", light="interior",
   still=f"{C['haha']} sits on the step of the farmhouse entrance reading a handwritten letter held close to her face, a thin envelope on her knee; the paper turned so that its writing cannot be read.")],
 "男性を百とすると": [dict(w="m60", light="interior",
   still="Payday at the mill: a line of young women in white headscarves waits at a wooden office window; beyond the glass, a clerk hands out small pay envelopes; seen from the end of the line.")],
 "女性だからという理由で": [dict(w="m60", light="interior",
   still="Two young mill workers in white headscarves sit side by side on a dormitory step comparing two small pay envelopes held in their laps, one noticeably thinner than the other.")],
 "労働基準法の、第四条です": [dict(w="m60", light="interior",
   still="A bare mill office wall in the sixties with an empty wooden notice board, a wall clock with no numerals and a row of hooks with worn aprons; nobody in the frame.")],
 "法律が禁じたのは": [dict(w="m60", light="interior",
   still="Across the spinning floor, young women tend the machines in the foreground while, far behind them, a few men in shirt sleeves stand at a supervisor's desk by the window.")],
 "同じ昭和三十九年、ひとつの会社に": [dict(w="v60", light="day",
   still=f"A simple country wedding: {C['ane']}, a few years older, in a plain white bridal kimono, walks beside her groom along a village road, relatives following behind.")],
 "昭和六十年、男女雇用機会均等法": [dict(w="none", light="interior",
   still="Japan in the mid nineteen-eighties, a bright office floor: young women and men in suits working side by side at grey steel desks, seen from a little distance.")],
 "統計の取り方は途中で変わって": [dict(w="none", light="day",
   still="Present-day Japan, a quiet morning street: women and men of all ages walking to work past a small station, seen from a little distance.")],
 "ただ、「同じだけ働いてるのにね」": [dict(w="v60", light="night",
   still=f"By the light of one low lamp, {C['haha']} folds a letter back into its thin envelope and holds it against her chest for a moment, eyes lowered.")],
 # ---- CTA (hai o) ----
 "ここで、ひとつだけお願いです": [
   dict(w="v60", light="day", still="A tin-roofed farmhouse in Tohoku in late summer, its sliding doors open to the veranda, laundry drying on a pole, rice fields beyond; nobody in view."),
   dict(w="v60", light="interior", still=f"Close view of {TIN} standing on a wooden shelf in a farmhouse kitchen, a little dust on its lid, a folded cloth beside it.")],
 # ---- MUC 4 (xuong may — cho USAF-11068 thay bot) ----
 "四点目。けがをするのは": [dict(w="f60", light="interior",
   still=f"In a small Tokyo workshop, {C['ani']}, a little older, in a worn work jacket, stands at a lathe with his back half to the camera, the machine running, metal shavings curling onto the oily floor.")],
 "「指を少し、機械にとられました": [dict(w="v60", light="interior",
   still=f"{C['haha']} kneels by the farmhouse doorway holding a short letter in both hands, her face tight; the paper is turned so that its writing cannot be read.")],
 "兄の封筒を順に並べていくと": [dict(w="now", light="night",
   still=f"{C['sue_old']} has laid a long row of envelopes side by side on the tatami in order; near the middle of the row there is a clear empty gap where two are missing; he looks at the gap.")],
 "兄の鉄工所では、朝から晩まで": [dict(w="f60", light="interior",
   still=f"Seen from behind and to one side, {C['ani']}, a little older, in a worn work jacket and cap, bends over a running lathe in a cramped Tokyo workshop, bright curls of metal shavings spinning off the cutting tool, a bare bulb above him.")],
 "工場の先輩は、指を一本": [dict(w="f60", light="interior",
   still="An older machinist in a stained work jacket stands at his lathe in profile, one hand resting on the machine's handwheel; the workshop behind him dim, belts running up to the ceiling shafts.")],
 "指先には、いつも小さな切り傷": [dict(w="f60", light="interior",
   still=f"At a workbench, {C['ani']} wraps a strip of white gauze around one finger over his cotton work glove, his face lowered; tools and metal parts on the bench.")],
 "そう言って、笑っていたそうです": [dict(w="f60", light="interior",
   still="Two machinists in work jackets take a break on upturned crates by the workshop door, drinking tea from tin cups; the older one holds up his hand, one finger missing, and grins.")],
 "早く、安く、たくさん作る": [dict(w="f60", light="interior",
   still="A cramped workshop floor with five lathes in a row, each worked by a man bent close to the spinning chuck, belts running to the ceiling shafts, sparks and shavings, no guards on the machines.")],
 "機械の覆いは": [dict(w="f60", light="interior",
   still="Close view of a metal safety guard left leaning against the workshop wall, removed from the lathe beside it; the lathe runs uncovered, its belt and gears exposed.")],
 "翌年の昭和四十一年には": [dict(w="c70", light="day",
   still="High on wooden scaffolding at a building site, labourers in cloth headbands carry steel rods along narrow planks with no safety rails, the city spread out far below.")],
 "労働安全衛生法という法律ができて": [dict(w="c70", light="day",
   still="Workers at a construction site in the early seventies line up in the morning wearing new white helmets and safety belts while a foreman stands in front of them.")],
 "亡くなる人は、昭和四十九年に": [dict(w="c70", light="day",
   still="A construction site with green safety netting hung along the scaffolding and a row of helmeted workers climbing a proper ladder, seen from a little distance.")],
 "二か月、封筒が来なかった": [dict(w="v60", light="night",
   still=f"At night, {C['haha']} sits alone at the low table with {TIN} closed in front of her, both hands resting on its lid, looking at the dark doorway.")],
 # ---- MUC 5 (1970s, de-kasegi) ----
 "最後の束は、父の封筒です": [dict(w="v70", light="interior",
   still=f"A bundle of envelopes tied with string on the tatami beside {TIN}; beside it, a worn cloth work cap; winter light from a snowy window.")],
 "駅まで見送るのは、母と": [dict(w="v70", light="dawn",
   still=f"On a small snowy country station platform before dawn, {C['chichi']}, older, greying, in a heavy work coat with a canvas bag, stands beside {C['sue']} and {C['haha']} in a winter shawl; a steam train waits.",
   where="a neighbour standing a few steps behind them on the platform", height="standing eye height", cam="locked",
   act="the father lifts his bag onto his shoulder and rests his free hand on the boy's head; the boy keeps looking at the train.",
   alive="Snow falls slowly and steam drifts from the locomotive.")],
 "飯場と呼ばれる宿舎で": [dict(w="c70", light="night",
   still="A crowded workers' bunkhouse at night: a dozen futons in rows on a plank floor, men in undershirts sitting and lying, a kerosene stove glowing in the middle, work gloves hanging from a line by the window.")],
 "春が来て、父が帰ってくる": [
   dict(w="v70", light="day",
   still=f"The sliding door of a farmhouse entrance opens onto a spring day; {C['chichi']} stands in the doorway with a paper shopping bag held against his chest; inside, {C['sue']} sits on the step looking up.",
   where="the mother standing inside by the kitchen doorway", height="standing eye height", cam="locked",
   act="the father steps in over the threshold holding the paper bag, and the small boy stands up from the step and looks at the bag.",
   alive="Blossom petals drift in through the open door behind him."),
   dict(w="v70", light="interior",
   still=f"{C['sue']} kneels on the tatami holding a boxed Tokyo sweet in both hands, grinning, while {C['chichi']} sits beside him taking off his work socks.")],
 "さらに昭和四十年代の半ばからは": [dict(w="v70", light="day",
   still="A Tohoku rice field left fallow in late summer, overgrown with grass, next to fields still green with rice; an old farmer stands at the boundary looking at it.")],
 "出身地でいちばん多いのは青森県": [dict(w="v70", light="dawn",
   still="A crowded night-train platform in a snowy northern station, men in winter work coats with canvas bags boarding the train, seen from a little distance.")],
 "出稼ぎは、この年を境に": [dict(w="v70", light="day",
   still="An empty snowy country station platform in late winter, a single wooden bench, the tracks running away into the white fields; nobody waiting.")],
 "あの冬、末の息子が待っていたのは": [dict(w="v70", light="night",
   still=f"At night in a snowy farmhouse, {C['sue']} sits on the entrance step in his pyjamas, knees drawn up, watching the closed sliding door.")],
 # ---- KET ----
 "三人のうち、封筒がいちばん多かったのは、誰だったのか": [dict(w="now", light="night",
   still=f"{C['sue_old']} kneels over the three piles of envelopes on the tatami, one pile clearly larger than the other two; he rests his hand beside it without touching it.")],
 "姉です。": [dict(w="m60", light="interior",
   still=f"{C['ane']} in her white headscarf stands at the dormitory window after work with a thin envelope in her hand, the evening light on her face, a small tired smile.")],
 "そして、この缶のお金は、最後に": [dict(w="now", light="night",
   still=f"{C['sue_old']} lifts the last folded paper from the bottom of {TIN}; it is a stiff white sheet, still folded, its writing on the inside.")],
 "昭和四十九年、県立高校の": [dict(w="s74", light="interior",
   still="An old stiff white paper receipt with a red school seal, worn at the folds, lying open on dark tatami; its printed lines too blurred and soft with age to read.")],
 "名前は、末の息子。缶を見つけた": [dict(w="now", light="night",
   still=f"{C['sue_old']} holds the unfolded receipt in both hands and lowers his head, his glasses pushed up onto his forehead; the open tin in his lap.")],
 "兄も、姉も、乗った夜の列車に": [dict(w="s74", light="day",
   still=f"On a spring morning, {C['sue']}, now fifteen, in a new dark high school uniform, walks through the wooden gate of a country high school under cherry blossom; {C['haha']}, older, in a plain coat, stands a few steps behind him.",
   where="a parent standing a few steps behind the mother by the gate", height="standing eye height", cam="drift",
   act="the boy walks slowly through the gate and away along the path; his mother stops at the gatepost and watches him go.",
   alive="Cherry petals drift slowly down across the path.")],
 "母が最後まで使わなかったのは": [dict(w="now", light="night",
   still=f"{C['sue_old']} sits on the tatami with {TIN} in his lap, tilting it slightly towards the lamp; inside, at the bottom, lie {NOTES}.",
   where="a relative kneeling a little behind him on the tatami", height="seated eye height on the floor", cam="locked",
   act="he tilts the tin a little towards the lamp and looks into it for a long moment, then slowly lowers it back onto his lap; he does not take anything out.",
   alive="The candle on the altar behind him flickers slightly.")],
 "この家のお金は、全部、あの二枚から": [dict(w="now", light="night",
   still=f"The closed {TIN} set on the Buddhist altar beside a small framed photograph of an old woman and white chrysanthemums; one candle burning; nobody in the frame.")],
 "でも、あの時代を働いた人たちは": [dict(w="c70", light="day",
   still="A long line of labourers in headbands and work jackets walks home along an elevated expressway under construction at the end of the day, their tools on their shoulders, the city behind them.")],
 "あなたの家にも、こんな缶は": [dict(w="now", light="interior",
   still=f"Close view of {TIN} on a wooden table by a window, its lid off, a few old envelopes inside, soft daylight.")],
 "覚えていることを、コメントで": [dict(w="v60", light="day",
   still="A country road through rice fields in Tohoku in summer, a small wooden station in the distance, the road empty.")],
 "次のページで、またお会いしましょう": [dict(w="now", light="day",
   still=f"The old farmhouse veranda in afternoon light, {TIN} placed on the wooden floor beside a cup of tea; nobody in the frame.")],
    # ---- 6 o chuyen tu phim dokkoi sang AI (23/09) ----
 "十五で東京へ出た兄": [
   dict(w="t60", light="day",
   still=f"On a wooden station platform in the early sixties, {C['ani']}, in a black school uniform with a peaked cap, stands with a small cloth-wrapped bundle beside a steam train, looking straight ahead, other boys in the same uniform around him."),
   dict(w="m60", light="interior",
   still=f"At the gate of a cotton spinning mill, {C['ane']}, in a white triangular headscarf, stands among a group of new mill girls holding a small suitcase, looking up at the tall brick building.")],
 "前の晩、母が、柳行李": [dict(w="v60", light="night",
   still=f"By one low lamp in a farmhouse room, {C['haha']} kneels beside an open wicker travel trunk and lays a neatly folded white undershirt into it; a small cloth amulet pouch rests on top of the other clothes.")],
 "「体にだけは、気をつけるんだよ」": [dict(w="t60", light="day",
   still=f"Close view on a crowded station platform: {C['haha']}, in a plain wool kimono, holds the hands of {C['ani']} in both of hers, looking up at his face; he looks down at their hands.")],
 "十五で親元を離れることも": [dict(w="t60", light="dusk",
   still="Seen from behind at dusk, a line of fifteen-year-olds in school uniforms with small bundles walks along a wooden station platform towards a waiting steam train, the lamps just lit.")],
 "自分の稼いだお金で": [dict(w="v60", light="day",
   still=f"In a farmhouse room, {C['sue']} and a little sister in school clothes kneel at a low table doing homework with pencils, new school bags beside them, while {C['haha']} sets down a pot of tea; bright daylight through the paper doors.")],
}


def scene_of(text, used):
    """Tim canh cho mot o theo chuoi loi; dong bi chia nhieu o -> lay canh ke tiep trong list."""
    hits = [k for k in S if k in text]
    if not hits:
        return None, None
    k = max(hits, key=len)                       # chuoi dai nhat = cu the nhat
    i = used.get(k, 0); used[k] = i + 1
    lst = S[k]
    return k, lst[min(i, len(lst) - 1)]


def main():
    plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
    used, rows, rows_v, still_out, vid_out, mot_out, blocks, bad = {}, [], [], [], [], [], [], 0
    for r in plan:
        if r["layer"] not in ("aistill", "ai"):
            continue
        k, sc = scene_of(r["text"], used)
        if sc is None:
            print("🔴 o %02d KHONG co canh: %s" % (r["idx"], r["text"][:30])); bad += 1; continue
        world = W[sc["w"]]
        if r.get("bw") or sc.get("bw"):
            world = (BW + " " + world).strip()
        full = dict(where=sc.get("where", "a person standing nearby"), height=sc.get("height", "standing eye height"),
                    cam=sc.get("cam", "locked"), light=sc["light"], still=sc["still"], act=sc.get("act", "."),
                    alive=sc.get("alive", ""))
        still, motion, _ = build_pair(full, world)
        probs = gate_prompt("still", still, LIMIT_SHOWA)
        if r["layer"] == "ai":
            probs += gate_prompt("motion", motion, LIMIT_SHOWA)
            probs += [m for _, m in gate_action(sc["act"]) if "HOLD_CLAUSE" not in m]
        if probs:
            print("⚠️ o %02d %s" % (r["idx"], probs)); bad += 1
        if r["layer"] == "ai":      # anh lam FRAME DAU cho clip -> file rieng, di cung MOTION
            vid_out.append(still); mot_out.append(motion)
            rows_v.append("%d\tanh -> cells_in/%02d.png  |  MOTION dong %d -> cells_in/%02d.mp4\t%s"
                          % (len(vid_out), r["idx"], len(mot_out), r["idx"], r["text"][:30]))
        else:                       # anh tinh thuan (hoa dong cuc bo bang make_cells_v3)
            still_out.append(still)
            rows.append("%d\tcells_in/%02d.png\t%s" % (len(still_out), r["idx"], r["text"][:30]))
        blocks.append("### o %02d · %s · %s\n> %s\n\n**STILL**\n```\n%s\n```\n%s" % (
            r["idx"], r["layer"], "BW" if "Black-and-white" in world else "mau", r["text"],
            still, ("\n**MOTION**\n```\n%s\n```\n" % motion) if r["layer"] == "ai" else ""))
    # 🗂 TACH HAI VIEC (user 2026-09-23): anh AI TINH thuan · anh+clip cho VIDEO — moi viec mot bo file
    def w_(name, xs):
        io.open(VD / name, "w", encoding="utf-8", newline="\n").write("\n".join(xs) + "\n")
    w_("prompts18_ANH_TINH_FLOW.txt", still_out)
    w_("prompts18_ANH_TINH_TENFILE.txt", [
        "# ANH AI TINH — che do Image (Nano Banana). Dong i cua ANH_TINH_FLOW -> luu ten ben duoi.",
        "# Thu muc: 06_VIDEO/18_hataraku-okane/cells_in/  (make_cells_v3 tu cat ✦ + hoa dong nhe)",
        "# NN = so o trong _PLAN.json. ⚠️ timeline THAT ve thi so o co the doi -> chay lai tool nay truoc khi luu"] + rows)
    w_("prompts18_VIDEO_ANH_FLOW.txt", vid_out)
    w_("prompts18_VIDEO_MOTION_FLOW.txt", mot_out)
    w_("prompts18_VIDEO_TENFILE.txt", [
        "# CLIP AI — B1: che do Image, dan dong i cua VIDEO_ANH_FLOW -> chon anh -> luu .png",
        "#           B2: ⋮ Animate tren anh do, dan dong i cua VIDEO_MOTION_FLOW -> luu .mp4 CUNG SO O",
        "# (dong i cua hai file la CUNG mot o)"] + rows_v)
    io.open(VD / "prompts18_BLOCKS.md", "w", encoding="utf-8").write(
        "# Video 18 — prompt anh/clip AI (ban nguoi doc)\n\n" + "\n\n".join(blocks) + "\n")
    # 🆕 file RIENG cho cac o can anh MOI (sau khi bo dokkoi) — user chi gen phan nay
    rm = VD / "_src_flow" / "remap_dokkoi.json"
    if rm.exists():
        need = {n[0] for n in json.loads(rm.read_text(encoding="utf-8"))["need"]}
        pairs = [(row, st) for row, st in zip(rows, still_out) if int(row.split("/")[1][:2]) in need]
        w_("prompts18_ANH_MOI_FLOW.txt", [st for _, st in pairs])
        w_("prompts18_ANH_MOI_TENFILE.txt", ["# CHI %d anh MOI (o tung la phim dokkoi). Dong i -> luu ten ben duoi vao cells_in/" % len(pairs)]
           + ["%d	%s" % (i + 1, row.split("	", 1)[1]) for i, (row, _) in enumerate(pairs)])
    print("ANH TINH %d · VIDEO %d (anh + motion) · canh bao %d" % (len(still_out), len(vid_out), bad))
    print("-> %s/prompts18_ANH_TINH_* · prompts18_VIDEO_* · prompts18_BLOCKS.md" % VD)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
