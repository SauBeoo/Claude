# -*- coding: utf-8 -*-
"""_motion19.py — MOTION viet lai THEO LOI DOC, cho 74 shot cua video 19.

User bat 2026-09-02: *"mày có dựa theo script để tạo animation không thế. Sao tao
thấy animation sinh ra tù thế"*. Cau tra loi that: **KHONG**. Ban truoc lay nguyen
`element_motion` co san trong `beats.json` roi boc khuon, khong he mo `_TTS.md` /
`timeline.json` de xem giay do LOI dang noi gi.

So do cua ban cu (do bang may):
  motion_style=calm · constraints=strict · camera 56/74 static
  60/74 shot dung dong tu YEU (slides/settles/tilts/drifts/sways), 4/74 manh
  bien do ghi thang trong chu: "a millimetre" · "a few degrees" · "a pixel or two"
  roi khuon lai chong them "Calm restrained amplitude" o MOI shot, ke ca peak.

Ba scene dat nhat, dat canh loi:
  「五年間で、およそ八十四万円」  -> "settles one notch, drifts a pixel or two"
  「一円も、出ません」            -> "palm closes halfway and opens again"
  「戻りません」                  -> "pushed a few degrees, catches"

⚠️ `E:\\vox-director\\SKILL.md` noi nguoc lai dung cho nay: *"element_motion - where
the ENERGY LIVES; AI writes it per beat to fit that scene (not a template). Make it
RICH (several elements moving) - be bold"*, va camera bold `{orbit, dolly_zoom, roll,
whip}` la *"available, NOT banned"*.

🔴 CHO AP SAI LUAT: `audience-45plus.md` §2 bat nhip dung cham cho tep 45+, nhung no
   noi ve **NHIP CAT** (<=6 doi hinh/phut), KHONG noi ve **BIEN DO CHUYEN DONG TRONG
   MOT SHOT**. Dung cai loi ma §2.0 cua chinh rule do da ghi: *gate co TRAN ma khong
   co SAN* - va o day hai dai luong bi gop lam mot. Mot shot co the dong manh ma van
   khong cat nhanh.

BA HANG NANG LUONG (khoa `lv`):
  "peak" — cau don / so mat mat / reveal / chan cung. Bien do LON, co **1 hero
           element bay-xe-do qua khung**, camera push manh. Bo phanh "restrained".
  "mid"  — dien giai co dong luc. 3-4 element dong ro rang, camera parallax/push nhe.
  "calm" — doan gioi thieu / dinh chinh / CTA / disclaimer / 予告. Giu nhe - day la
           cho tep 45+ can nghi, va la cho lam cho peak noi bat.

Phan hang lay tu NOI DUNG cau, khong theo cam giac. 74 shot: 26 peak · 27 mid · 21 calm.

🔴 SUA 2026-09-03: 4 motion co chu "banknotes" khien model ve **do la My**
   (chan dung Franklin, so 100) — thay ro o cold open va callback `futari`.
   Kenh Nhat noi ve 円 (`feedback_jp_script_yen_only`). Da ta ro tien NHAT +
   cam tuong minh USD. Cung loi da sua o `gen_flow19.py::PROP["P_MONEY"]`.
"""

# lv: peak | mid | calm      cam: static | parallax | push | push_hard | whip
# m : chuyen dong, viet theo NGHIA cua cau loi dang doc o giay do
M = {

# ══ COLD OPEN ═══════════════════════════════════════════════════════════════
# [0-10s] 「六十歳を過ぎても、いまも働いているかた」「あなたが五年で受け取り損ねるのは、およそ百六十八万円です」
# -> SO DAU TIEN cua bai. Phai DAM, khong duoc "settles a millimetre".
"hataraku": dict(lv="peak", cam="push", m=(
    "the man keeps working steadily - he lifts a box onto the shelf and turns back for "
    "the next one - while BEHIND HIM a wide fan of plain kraft-brown pay envelopes, each "
    "one fat with folded paper, peels off the wall of boxes one after another and sails "
    "away out of the top of the frame, going where he cannot see; he never looks up, the "
    "daylight from the high window flares brighter as each envelope leaves")),
"hataraku_b": dict(lv="peak", cam="push", m=(
    "the gloved hands push the box the rest of the way onto the shelf and pat it flat - "
    "the work is done right - and as they do, two more plain kraft-brown pay envelopes "
    "slip out from between the boxes and flutter up past the hands and out of frame; the "
    "fingertips never notice, the paper dust in the window light swirls where they passed")),

# [10-23s] 「減らされるのではなく、もらえるはずのお金を、もらわないまま終わるのです」
# -> KHONG bi cat, ma la KHONG BAO GIO DEN. Cho o thu do TRONG.
"kyuryo_meisai": dict(lv="mid", cam="parallax", m=(
    "the hands lift the payslip up into the light and turn it toward us, searching it; "
    "one line on the sheet sits completely empty and a soft glow pulses in that blank "
    "line as if something should have been there; the reading glasses beside them rock "
    "once, the calculator's shadow creeps across the table")),
"kyuryo_meisai_b": dict(lv="mid", cam="static", m=(
    "still searching the same sheet: the paper is laid back down and smoothed flat with "
    "one sweep, the coffee ring stain darkening as the cup's shadow passes over it, and "
    "the one empty line glows once more and fades; the folded glasses beside it stay shut")),

# [36-49s] 「対象は、六十歳から六十五歳の、働いているかた…逆で、働いていないかたには出ません」
# -> DIEU KIEN: dang lam viec thi VAO, khong lam thi BI GAT RA.
"hataraku_c": dict(lv="mid", cam="static", m=(
    "the hand drives the blank time card into the wall clock and it stamps home with a "
    "hard mechanical snap that shakes the whole machine; the card springs back up a "
    "centimetre and is caught; a small burst of paper flecks jumps off the slot")),
"hatena": dict(lv="mid", cam="parallax", m=(
    "the seated man's head turns from one envelope to the next along the fan, and as his "
    "gaze passes each one that envelope lifts an inch off the desk and drops back; the "
    "last one in the row slides right out of the fan and off the far edge of the desk, "
    "gone; his hand half rises to stop it and does not make it")),

# [49-59s] 「確かめる数字は、三つ。順番に見ていきます」「いくら下がれば…なぜ去年、額が減ったのか」
# -> OPEN LOOP: ba cau hoi treo len.
"hatena_b": dict(lv="mid", cam="push", m=(
    "the three envelopes snap apart from the fan and space themselves evenly across the "
    "frame in three quick beats, one - two - three, each landing with a small paper thud "
    "that rocks the desk lamp; the lamp light swings and three long shadows fan out "
    "beneath them")),
"hatena_c": dict(lv="mid", cam="static", m=(
    "he flips one of those three envelopes over and back, over and back, hunting for "
    "something written on it and finding nothing; his frown deepens; the other two "
    "envelopes wait in the blur behind his hands, still unopened")),

# [59-68s] 「しかも、この二万八千円を受け取ると、年金が止まります」「まず、事実から」
# -> CANH BAO: mot thu DUNG LAI.
"kenkyu": dict(lv="peak", cam="push", m=(
    "the small brass desk clock in the middle of the tidy desk is ticking - then its "
    "second hand JAMS dead mid-sweep and the whole desk jolts with it; the stacked "
    "leaflets slide a hand's width sideways, the fountain pen rolls off its rest and "
    "stops against the clock, and everything goes completely still")),

# [68-75s] 「年金と老後のお金研究室です。原典を開いて、あなたの数字を計算していきます」
# -> Gioi thieu kenh: DIEM DAM. Day la cho nghi.
"kenkyu_b": dict(lv="calm", cam="parallax", m=(
    "the magnifying glass is drawn slowly across the open leaflet and the paper fibres "
    "swell and sharpen as it passes; the linen cloth beneath breathes; the page's free "
    "corner turns over by itself, unhurried, and lies flat")),

# ══ 第1章 ══════════════════════════════════════════════════════════════════
# [75-91s] 「給料が下がった。その下がった分を、雇用保険から補う」
# -> BU VAO: tien chay VE PHIA nguoi xem.
"koyou_hoken": dict(lv="mid", cam="push", m=(
    "the uniformed hands lay note after note onto the older palm in a quick steady rhythm "
    "and the stack visibly grows taller in the frame; with each note the older hand dips "
    "under the weight and lifts again; one note catches the air and spins flat onto the "
    "top of the pile")),
"koyou_hoken_b": dict(lv="mid", cam="static", m=(
    "the same giving keeps going, right up close: two more notes drop onto the stack and "
    "the whole pile springs slightly under them; the palm's fingers curl up around the "
    "edges to hold it all in; the giving hand withdraws out of frame")),

# [114-124s] 「少し下がった、では出ません。四分の三を、はっきり下回る必要があります」
# -> NGUONG: phai TUT HAN xuong duoi soi chi.
"75percent": dict(lv="mid", cam="push", m=(
    "the stack of coins beside the measuring stick sinks - coin by coin the pile drops "
    "lower, stops just under the taut red thread, then settles one coin lower still so it "
    "is clearly beneath the line; the red thread hums and stays dead level")),
"75percent_b": dict(lv="mid", cam="static", m=(
    "extremely close on the same thread: it snaps taut and vibrates hard once across the "
    "frame while the wooden stick's markings sharpen behind it; a single grain of paper "
    "dust is knocked off the thread and drifts down")),

# ══ 第2章 松本さん ═════════════════════════════════════════════════════════
# [144-170s] 「千葉県の松本さん、六十歳…机の引き出しに、入社の年に配られた社章がまだ入っている」
# -> BEAT TINH CAM. Nhe la DUNG - va no lam peak sau do noi bat.
"matsumoto": dict(lv="calm", cam="parallax", m=(
    "the drawer glides open the whole way and stops; his eyes travel down to the lapel pin "
    "lying inside and stay there; his shoulders come down a notch; the lamp behind him "
    "brightens a shade as the drawer's shadow retreats")),
"matsumoto_b": dict(lv="calm", cam="static", m=(
    "the open palm tilts slowly and the warm lamp light slides all the way across the "
    "plain enamel face of the pin and off its edge; the fingers close in around it a "
    "little; a thumb brushes the surface once")),
"matsumoto_c": dict(lv="calm", cam="static", m=(
    "closing the beat: the drawer is pushed shut in one slow continuous push until it "
    "seats with a soft knock; he keeps looking down at where it was; the lamp behind him "
    "holds steady and the room goes quiet")),

# [187-216s] 「ひとつ落とし穴があります…上限が決められています。五十二万二千円」
# -> BAY: bi CHAN CUNG khong cho cao them. PEAK.
"jougen": dict(lv="peak", cam="push_hard", m=(
    "the tall coin stack is still rising when the flat wooden ruler SLAMS down flat across "
    "its top and pins it - the whole stack shudders, the desk jumps, and three coins are "
    "knocked clean off the side and skid away out of frame; the ruler does not lift")),
"jougen_b": dict(lv="peak", cam="static", m=(
    "extremely close on the pinned top coin: the ruler presses down harder and the coin "
    "beneath it visibly compresses and grinds sideways a fraction; the hard side light "
    "flares on the ruler's edge; nothing gives")),
"jougen_c": dict(lv="mid", cam="static", m=(
    "the coins that were knocked off wobble on their rims one after another and topple "
    "flat, rolling to a stop apart from each other; behind them the capped stack sits "
    "clamped and motionless in the blur")),
"jougen_d": dict(lv="peak", cam="push", m=(
    "closing the trap: the hand carries one last coin down toward the top of the stack, "
    "meets the ruler, presses against it twice - and cannot get through; the hand hangs "
    "there holding the coin it is not allowed to place, then goes still")),

# [234-259s] 「二万八千円。これが、松本さんが毎月受け取れる額です」「五年で、百六十八万円」
# -> DUOC NHAN: am, nhe nhom.
"28000": dict(lv="mid", cam="parallax", m=(
    "he leans in over the passbook and his smile widens as he reads; his finger comes down "
    "onto a line and taps it twice; steam curls up off the tea beside him and the warm "
    "afternoon light swells across the table")),
"28000_b": dict(lv="mid", cam="static", m=(
    "extremely close on the same page: the finger slides down the ruled lines, one line "
    "after another, and each line it touches lights up faintly and fades behind it; the "
    "page's edge lifts and settles as his hand moves")),
"28000_c": dict(lv="calm", cam="parallax", m=(
    "closing the beat from above: the steam from the teacup rises and leans, the passbook's "
    "pages breathe once and lie flat, the reading glasses' shadow creeps a little further "
    "across the table, and everything comes to rest")),

# [259-272s] 「ここからが、今日の本題です」「この十パーセント、去年の春まで、十五パーセントでした」
# -> CU LAT. Phong bat dau toi lai.
"hondai": dict(lv="peak", cam="push_hard", m=(
    "the turned-up corner of the leaflet peels back further and FLIPS the page right over "
    "with a snap; the pen laid across it is thrown off and clatters away; the desk lamp "
    "swings hard on its arm so the shadows sweep across the whole desk and the dark room "
    "behind closes in")),
"hondai_b": dict(lv="peak", cam="push", m=(
    "extremely close: the narrow beam of lamp light contracts fast to a slit while the "
    "page's edge keeps curling up into it, and the rest of the sheet drops away into black; "
    "one paper fibre lifts off the torn edge and vanishes into the dark")),

# [299-310s] 「五年間で、およそ八十四万円」「同じ会社で、同じ仕事をして、同じだけ給料が下がっても、です」
# -> PEAK CAO NHAT CUA BAI. Mat 840.000 yen.
"84man": dict(lv="peak", cam="push_hard", m=(
    "a whole slab of the stack of JAPANESE banknotes (warm pale gold and soft brown, blank faces, no portraits, no numerals, NOT green US dollars) is TORN AWAY - the paper rips across the frame in "
    "one fast pull, the ragged edge bursting loose fibres into the air - and the torn-off "
    "portion is carried up and clean out of the top of the frame; the stack that is left "
    "rocks back, suddenly much shorter, and the hard light glares off the raw torn edge")),
"84man_b": dict(lv="peak", cam="push", m=(
    "the torn-away slab lands apart on the dark table and slides further away, opening the "
    "gap wider and wider until it is unmistakable; loose paper fibres rain down between the "
    "two pieces; the remaining stack does not move at all")),

# [310-339s] 「分かれ目になるのは…あなたが、六十歳になった日です」「一日の違いで、五年分の八十四万円が変わる」
# -> MOT NGAY DINH MENH. PEAK.
"tanjoubi": dict(lv="peak", cam="push", m=(
    "the red marker drives the circle closed in one hard stroke that overshoots and scores "
    "past itself, then lifts clear; the whole calendar page snaps taut against the wall and "
    "flutters; a fine spray of red ink flecks is thrown off the tip and lands across the "
    "blank squares nearby")),
"tanjoubi_b": dict(lv="peak", cam="static", m=(
    "extremely close: the wet red ink bleeds outward through the paper fibres, creeping "
    "visibly past the circle's edge and staining into the squares on either side; the paper "
    "dimples slightly under the wet ink")),
"tanjoubi_c": dict(lv="peak", cam="push", m=(
    "the two calendar pages laid side by side begin to SEPARATE - the unmarked right-hand "
    "page slides steadily away from the circled left one, opening a widening gap of bare "
    "desk between them, and lifts its far edge as it goes; the circled page stays nailed "
    "flat where it is")),
"tanjoubi_d": dict(lv="mid", cam="static", m=(
    "closing the beat: the uncapped marker rolls across the desk, knocks against the "
    "calendar and stops dead; its cap, resting apart, is nudged by the shock and rocks; the "
    "red ink on the tip catches the light and dulls")),

# [370-376s] 「この「割合」というのが、思っている以上に厳しいんです」
"wariai": dict(lv="mid", cam="push", m=(
    "the brass balance tips further and further as the coin pan sinks, until the folded "
    "payslip on the other pan is thrown high and hangs there; the beam bounces hard against "
    "its stop twice and the whole scale rings; the pans swing on, refusing to level")),

# ══ 第3章 同僚 ═════════════════════════════════════════════════════════════
# [376-402s] 「同僚のかた…四十万円になったそうです」「多いほうが、恵まれているように見えますね」
"douryou": dict(lv="mid", cam="parallax", m=(
    "he lifts the payslip up to eye level, looks at it, and the wry smile pulls further "
    "across his face and holds; his other hand comes up and drops back onto his knee; the "
    "vending machine's light behind him flickers over and over")),
"douryou_b": dict(lv="mid", cam="static", m=(
    "close on the same sheet: the fingers tighten and tighten until the paper folds and "
    "crumples visibly under them, one crease running right across the ruled lines; the "
    "blurred break room behind stays flat and still")),
"douryou_c": dict(lv="mid", cam="static", m=(
    "closing the beat: the folded sheet is pushed back down into the brown envelope in one "
    "long slow slide until it disappears; the flap is pressed shut with a thumb; he keeps "
    "looking down and does not lift his head")),

# [415-425s] 「このかたは、対象外です。一円も、出ません」「十五万円も給料が下がったのに、です」
# -> PEAK kieu RONG. Khong co gi de dong - va cai TRONG phai duoc dien to.
"zero": dict(lv="peak", cam="push_hard", m=(
    "the empty palm is held out flat and WAITS, and nothing comes - then the empty envelope "
    "beside it is lifted by the air, flips over once showing both blank sides, and slides "
    "off the far edge of the desk out of frame; the palm stays open on nothing, and the cold "
    "flat light hardens across it")),
"zero_b": dict(lv="peak", cam="push", m=(
    "the lone envelope on the bare desk has its flap thrown wide open by the air, showing "
    "the empty inside right at us, and it is pushed a long way across the bare wood until "
    "it fetches up against nothing at all; the desk around it is completely empty")),

# [425-454s] 「冒頭の、ふたりの男性。あれが、このおふたりです」「百六十八万円と、ゼロに分かれました」
# -> CALLBACK + CHIA DOI SO PHAN. PEAK.
"futari": dict(lv="peak", cam="push", m=(
    "the two men are standing shoulder to shoulder when the floor between them SPLITS "
    "them apart - they are drawn steadily away from each other to opposite sides of the "
    "frame, the uneasy one turning his head to watch the calm one go; the calm man's "
    "kraft-brown envelope swells visibly fat with folded paper and its flap lifts, while "
    "the other man's envelope stays flat and empty and caves in on itself")),
"futari_b": dict(lv="peak", cam="push", m=(
    "close on the two envelopes side by side: the tightly gripped one creases and folds in "
    "on itself in the fist, showing it is completely flat and empty inside, while "
    "the other is held dead level and swells thick with folded paper until its flap "
    "springs open; the two hands keep drawing apart")),
"futari_c": dict(lv="peak", cam="push_hard", m=(
    "the man who stopped to read stands frozen while the other walks on and on toward the "
    "far door, getting smaller and blurring away, until the corridor between them is long "
    "and empty; the sheet of paper drops from the reading man's hand and drifts to the floor")),
"futari_d": dict(lv="mid", cam="static", m=(
    "closing the callback: the folded work jacket between the two closed lockers swings "
    "wider and wider on its hook and knocks against one metal door, then the other, before "
    "hanging still; the fluorescent light stutters twice; both doors stay shut")),

# [513-541s] CTA 「ここで、ひとつだけお願いです…」
# -> CALM. Day la cho nghi, khong phai cho dien.
"cta": dict(lv="calm", cam="parallax", m=(
    "the two of them lean in together over the tablet and both smiles widen; the husband's "
    "hand comes to rest on the wife's; steam rises from the two cups on the low table and "
    "leans toward them in the warm light")),
"cta_b": dict(lv="calm", cam="static", m=(
    "close on their hands: the tablet is tilted slowly toward us and the blank pale screen "
    "catches the room light and glows brighter across its whole face; the fingers around the "
    "edges settle into a firmer hold")),
"cta_c": dict(lv="calm", cam="static", m=(
    "the teapot pours a long steady stream into the second cup until it is full and lifts "
    "away; the steam climbs and bends; a ring of light spreads on the surface of the tea")),
"cta_d": dict(lv="calm", cam="parallax", m=(
    "closing the beat: the two of them turn to look at each other and hold it, both smiles "
    "settling; the tablet lies face-down and forgotten on the table; the evening light "
    "deepens a shade across the sofa")),

# ══ 第4章 二つ目の窓口 ═════════════════════════════════════════════════════
# [541-559s] 「もうひとつの窓口に移ります…年金のほうが、止まります」
"madoguchi2": dict(lv="mid", cam="push", m=(
    "the man standing between the two counters turns from one to the other and back, twice, "
    "unable to choose; the blank sign above the left counter swings on its chains and the "
    "right one answers; his bag slips down off his shoulder to his elbow")),
"madoguchi2_b": dict(lv="mid", cam="static", m=(
    "straight on at the second counter: the empty chair in front of it is drawn back from "
    "the counter a long way, as if by someone leaving, and stops turned aside; the blank "
    "sign above it steadies; the daylight across the counter cools")),

# [587-608s] 「ここは正確に申し上げます…松本さんは、まだ年金を受け取っていません」
# -> DINH CHINH. Phai DIEM DAM - noi dung la "dung hieu sai", khong phai cu don.
"tadashi": dict(lv="calm", cam="static", m=(
    "the raised palm comes up a little further into the 'wait a moment' hold and stays "
    "there, perfectly steady; his head tilts a few degrees toward us; the even light across "
    "the desk does not change")),
"tadashi_b": dict(lv="calm", cam="static", m=(
    "close on the same raised palm: the fingers spread slowly apart and relax again, once; "
    "the soft shadow behind the hand widens and narrows with them; the pale background stays "
    "flat")),
"tadashi_c": dict(lv="calm", cam="parallax", m=(
    "closing the beat: he pushes his reading glasses up his nose with one finger and lowers "
    "his eyes back to the document; his other hand smooths the page flat; he settles and "
    "does not hurry")),

# [608-630s] 「繰上げ受給です…月に四万三千円減ったまま、一生続く」
"kuriage": dict(lv="mid", cam="push", m=(
    "the hourglass, already tipped on its side, is nudged over further and its sand pours "
    "out onto the desk in a steady stream, the spilled pile growing wider while the glass "
    "empties; the pension handbook beside it is pushed aside by the spreading sand")),
"kuriage_b": dict(lv="mid", cam="static", m=(
    "extremely close on the spilled pile: fresh sand keeps arriving and the pile slumps and "
    "spreads, sending grains skating away across the dark desk in every direction; the base "
    "of the glass is slowly buried")),
"kuriage_c": dict(lv="mid", cam="static", m=(
    "closing the beat: the hourglass is set upright again and it is plainly less than half "
    "full - the last grains inside run down and stop; the loose sand left on the desk "
    "outside it is not swept up; nothing refills")),

# [630-654s] 「減ったあとの年金から、さらに一万一千二百円が止まる」「二重に、削られます」
# -> CAT HAI LAN. PEAK.
"nijuu": dict(lv="peak", cam="push_hard", m=(
    "the scissors bite through the sheet a SECOND time - a strip is sliced off and thrown "
    "clear across the frame to land beside the first one, and the sheet left behind is now "
    "visibly narrower than it started; the two cut strips curl up at their ends; the hard "
    "light glares on the blades")),
"nijuu_b": dict(lv="peak", cam="static", m=(
    "close on the open scissors: the blades scissor shut hard once more and the fresh strip "
    "springs away from the cut edge, the crisp edge lifting; a shiver runs down the length "
    "of the remaining sheet")),
"nijuu_c": dict(lv="mid", cam="push", m=(
    "closing the beat: the two narrow strips are drawn apart from each other and further "
    "from the sheet they came out of, until all three lie clearly separate; what is left of "
    "the sheet lies alone and thin under the even light")),

# [673-694s] 「あとから給付金の申請をやめても、年金の停止だけは、戻りません」「順番が、大事だ」
# -> CHAN CUNG, MOT CHIEU. PEAK kieu KHOA.
"modoranai": dict(lv="peak", cam="push_hard", m=(
    "the hand pushes the turnstile's barred arm forward and it swings freely through - then "
    "the hand tries to bring it BACK the other way and it stops dead against its lock and will not budge; "
    "the gate does not give at all; the hand pulls again and it holds "
    "absolutely fast")),
"modoranai_b": dict(lv="peak", cam="static", m=(
    "extremely close on the lock: the mechanism is pressed backward, the pawl rides up over "
    "the tooth and settles down firmly, again and again, never releasing; a fleck of metal dust "
    "jumps off it; the cold light is unmoving")),
"modoranai_c": dict(lv="mid", cam="push", m=(
    "closing the beat: beyond the gate the far corridor stretches away completely empty and "
    "the light down it dims from the far end toward us; the out-of-focus gate in the "
    "foreground stays locked across the way back")),

# ══ 第5章 確かめる三つ ═════════════════════════════════════════════════════
# [708-726s] 「給料明細に、この給付金が反映されているかどうか…そこを見てください」
"meisai_check": dict(lv="mid", cam="push", m=(
    "the finger runs down the column of the payslip line by line, the magnifying glass "
    "travelling with it and each line swelling huge under the lens as it passes, until both "
    "stop on one line and press against it; the paper dents under the fingertip")),
"meisai_check_b": dict(lv="mid", cam="static", m=(
    "closing the beat: the magnifying glass is set down beside the sheet and rocks flat on "
    "its rim, its lens throwing a bright disc of light onto the paper; the hand withdraws "
    "out of frame and the sheet's edge lifts once behind it")),

# [726-746s] 「四か月以内」「過ぎてしまうと、その月の分は戻りません」
# -> HAN CHOT DANG BOC DI. PEAK.
"4kagetsu": dict(lv="peak", cam="push", m=(
    "the four calendar pages laid side by side begin to go: the first curls up hard and is "
    "peeled off and carried out of frame, then the next, and the next, in quick succession, "
    "leaving bare desk behind them; the red marker resting on top is thrown off as the last "
    "page lifts")),
"4kagetsu_b": dict(lv="peak", cam="static", m=(
    "extremely close on the last page's corner: it curls further and further back on itself, "
    "the paper fibres straining and whitening along the fold until they begin to give; the "
    "shallow focus behind it goes soft")),
"4kagetsu_c": dict(lv="peak", cam="push_hard", m=(
    "the hand pulls the page away from the calendar in one long steady motion - the sheet comes free "
    "with a ragged edge and is swung right out of the frame, and a scatter of torn paper "
    "flecks is thrown into the air; the pages left behind snap flat against the wall")),

# [746-764s] 「同じ月の、同じあなたの、二つの窓口です。片方だけ見て決めると、もう片方で削られます」
"futatsu_mado": dict(lv="mid", cam="parallax", m=(
    "he looks down at the left document, then the right, then the left again, faster each "
    "time; as he looks at one, the other lifts its near edge off the desk behind his "
    "attention and settles back; his hands press down on both to hold them still")),
"futatsu_mado_b": dict(lv="mid", cam="static", m=(
    "closing the beat, from above: the two flat hands press down on the two documents at "
    "once and both papers flatten and go still under them; the ruled lines sharpen; neither "
    "hand lifts")),

# ══ CLOSING ════════════════════════════════════════════════════════════════
# [843-865s] Disclaimer 「令和八年八月時点の情報です…必ずご確認ください」
# -> CALM. Institutional, trong.
"chuui": dict(lv="calm", cam="parallax", m=(
    "the information desk waits with nobody at it: the blank leaflets in their stand lean a "
    "little further over, the neutral daylight moves slowly across the clean counter, and "
    "the empty chair's shadow lengthens")),
"chuui_b": dict(lv="calm", cam="static", m=(
    "close on the leaflet stand: the pale leaflets fan apart a fraction and settle back "
    "against each other; the top one's corner lifts in the moving air and lies down; the "
    "soft light holds even")),
"chuui_c": dict(lv="calm", cam="static", m=(
    "closing the beat: the single empty chair in front of the counter turns a few degrees "
    "further aside on its own and stops; the daylight across it cools; nobody comes")),

# [865-899s] 次回予告 「仙台の佐藤さん、六十六歳…四分の三になるのは、年金の、どの部分でしょうか」
# -> CALM-am, mo mot cau hoi cho tap sau.
"yokoku": dict(lv="calm", cam="parallax", m=(
    "she raises the notice sheet in both hands into the lamplight and reads down it, her "
    "head tilting slowly; the sheet's lower corner turns over toward us; the lamp glow "
    "swells warmer across the low table beside her")),
"yokoku_b": dict(lv="calm", cam="static", m=(
    "close on her hands and the sheet: the ruled table on the paper sharpens as she brings "
    "it nearer, and one row of it glows faintly and fades, then a different row does - as "
    "if the answer were somewhere in there; her thumbs shift their grip")),
"yokoku_c": dict(lv="calm", cam="static", m=(
    "the reading glasses are set down beside the folded sheet and rock to rest; the steam "
    "from the teacup rises and leans away; the warm lamplight settles over the three of them "
    "on the low table")),
"yokoku_d": dict(lv="calm", cam="parallax", m=(
    "closing the film: her silhouette beside the floor lamp breathes once and stills; the "
    "warm pool of light around her widens very slowly into the dusk of the room; nothing "
    "else moves")),
}
