# -*- coding: utf-8 -*-
r"""Sinh 22_furaipan-kuttsuku_SLIDES.json + bo prompt anh (FLOW/NAMES).

LOP HINH = MOT CAI CHAO, tu sang hom nay den bep cua me.

  NEO LAP LAI (ve ra CUNG mot vat moi lan):
    - CHAO SAT: xin/lom dom (mo bai) -> den bong (cuoi bai)
    - GIOT NUOC lan tron tren mat chao nong (phep thu — 3 lan: mo, thao tac, ket)
    - TRUNG dinh nua vao chao (cau dam cua cold open)
    - MUONG CANH DAU + giay lau (thao tac)
    - BEP CUA ME: cua bep, tay me, KHONG BAO GIO CO MAT

  5 HOI:
    I   sang nay: trung dinh -> "khong phai tay ban" -> giot nuoc
    II  1977:焼き付き -> ma sat -> mang KHONG phai dau (金属石けん)
    III thu tu: 空焼き -> dau -> nhiet; nuoc va nhiet do khong deu cat mang
    IV  rua: 30 giay khong sao, co manh moi giet; mang moc lai
    V   テフロン nguoc chieu -> dong tien -> 10 phut cuu chao -> me
"""
import re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "22_furaipan-kuttsuku"
VD = f"E:/Claude/Projects/youtube-jp-co-dai/06_VIDEO/{SLUG}"
DUR = 1262          # 6.415 ky / 305 ky-phut ~ 21,0 phut

L = [re.sub(r"\[[^\]]*\]", "", l).strip()
     for l in (PROJ / "03_SCRIPTS" / f"{SLUG}_TTS.md").read_text(encoding="utf-8").split("\n")]
L = [l for l in L if l and not l.startswith(("#", "TARGET_QUERY", "INTENT"))]


def P(n):
    return f"{VD}/ai_clean/{n}.jpeg"


def idx(frag):
    hit = [i for i, l in enumerate(L) if frag in l]
    if len(hit) != 1:
        raise SystemExit(f"NEO KHONG DUY NHAT ({len(hit)}): {frag}")
    return hit[0]


# ══ THE VOX ════════════════════════════════════════════════════════════════
VOXSPEC = [
 ("落ちたのは、腕ではありません",
  ("title", {"title": "腕ではありません",
             "sub": "はがれたのは、目に見えない膜が1枚"}, "iron_pan_dull_surface")),

 ("玉になって、すべるように転がったら",
  ("process", {"kicker": "入れどきの見分け方", "title": "水を一滴、落とすだけ",
               "steps": [{"label": "空のまま中火で1分", "sub": "何も入れない"},
                         {"label": "水を一滴おとす", "sub": "ジュッと消えたら、まだ冷たい"},
                         {"label": "玉になって転がる", "sub": "そこが油を入れる合図", "hot": True}]},
   "water_droplet_rolling_on_pan")),

 ("そこで使われた言葉が、焼き付きでした",
  ("compare", {"kicker": "1977年・家政学雑誌", "title": "台所の話ではなく、機械の話",
               "left": {"label": "油膜がある", "mark": "o", "verdict": "すべる"},
               "right": {"label": "油膜が切れる", "mark": "x", "verdict": "金属と噛み合う"},
               "source": "平野美那世（お茶の水女子大学）"}, "machine_bearing_metal")),

 ("カルボン酸鉄塩。かみくだいて言えば",
  ("stat", {"kicker": "膜が生まれる温度帯", "big": "200", "unit": "〜300度",
            "sub": "この帯で、油の脂肪酸が鉄と反応する",
            "note": "できたのは油ではなく、金属石けん",
            "source": "家政学雑誌 28巻6号（1977）"}, "oil_film_on_hot_iron")),

 ("鉄のフライパンに要るのは、後者でした",
  ("compare", {"kicker": "同じ油でも", "title": "敷くのか、反応させるのか",
               "left": {"label": "冷たい鍋に敷く", "mark": "x", "verdict": "ただの液体のまま"},
               "right": {"label": "熱してから焼きつける", "mark": "o", "verdict": "膜になる"}},
   "oil_poured_into_cold_pan")),

 ("摩擦がいちばん小さかったのは、最後の一枚でした",
  ("collage", {"kicker": "1977年・4枚の鉄板", "title": "順番を変えただけで、こうなる",
               "items": [{"label": "何もしない", "mark": "x"},
                         {"label": "空焼きだけ", "mark": "x"},
                         {"label": "油を塗って加熱", "mark": "o"},
                         {"label": "空焼き→油→加熱", "mark": "o"}],
               "note": "摩擦がいちばん小さいのは最後の一枚。20往復でも油切れなし",
               "source": "家政学雑誌 28巻6号（1977）"}, "four_iron_test_plates")),

 ("熱で先に追い出してから、油を入れる",
  ("process", {"kicker": "台所での手順", "title": "空焼き、油、そして拭き取る",
               "steps": [{"label": "空のまま中火", "sub": "水滴が転がるまで"},
                         {"label": "火を弱めて油を大さじ1杯", "sub": "縁まで回す"},
                         {"label": "1〜2分で火を止め、拭き取る", "sub": "膜はうすいほど強い",
                          "hot": True}]}, "oil_wiped_with_paper")),

 ("火が弱いからくっついたのではありません",
  ("stat", {"kicker": "濡れた肉を置いた瞬間", "big": "100", "unit": "度",
            "sub": "水が蒸発しきるまで、そこから上がらない",
            "note": "湧いた水蒸気が、膜の上の油を押しのける"}, "wet_meat_on_hot_pan")),

 ("2013年の日本調理科学会誌によれば",
  ("bar", {"kicker": "熱の伝わりやすさ", "title": "同じ火でも、広がり方が5倍ちがう",
           "bars": [["鉄", 80], ["ステンレス", 16]], "hot": 0,
           "source": "日本調理科学会誌 46巻4号（2013）"}, "pan_bottom_uneven_heat")),

 ("ところが、空焼きしてから油を焼きつけた板は",
  ("timeline", {"kicker": "洗剤で煮洗いした時間", "title": "30秒では、落ちません",
                "marks": [["30秒", "変化なし"], ["1分", "わずか"], ["10分", "それでも差"]],
                "note": "膜を断つのは洗剤ではなく、こする力でした",
                "source": "家政学雑誌 28巻6号（1977）"}, "sponge_and_hot_water")),

 ("日本弗素樹脂工業会の取扱マニュアルによれば",
  ("timeline", {"kicker": "フッ素樹脂の門限", "title": "余白は、思っているより狭い",
                "marks": [["230度", "揚げ物"], ["260度", "上限"], ["430度", "分解"]],
                "note": "鉄は300度で頭打ち。樹脂は門限の向こう側へ",
                "source": "ふっ素樹脂取扱マニュアル 第11版"}, "empty_pan_on_high_flame")),

 ("そして、その販売元があとからホームページに書き足した",
  ("source", {"kicker": "出典", "org": "国民生活センター 商品テスト No.100",
              "asof": "2016年8月18日 公表",
              "quote": "販売元は後日「初回と定期的に、油で処理を」と追記した",
              "number": "5回",
              "note": "油なしでも焦げ付かない、と受け取れる表示だった"},
   "consumer_report_paper")),

 ("理由を一つも説明できないまま、40年",
  ("title", {"title": "買う膜と、育てる膜",
             "sub": "母は理由を知らないまま、40年、正しいほうを続けていた"},
   "mother_hand_wiping_pan")),
]

VOX = {}
for frag, spec in VOXSPEC:
    VOX[idx(frag)] = spec

VOXSUBJ = {
 "iron_pan_dull_surface": "extreme macro of a dull grey cast-iron pan surface, patchy and worn",
 "water_droplet_rolling_on_pan": "a single water droplet beading and rolling on a hot dark iron surface, macro",
 "machine_bearing_metal": "extreme macro of a metal bearing surface with a thin film of oil, industrial",
 "oil_film_on_hot_iron": "a thin sheen of oil shimmering on a hot dark iron surface, faint smoke, macro",
 "oil_poured_into_cold_pan": "cooking oil pooling in the centre of a cold iron pan, macro",
 "four_iron_test_plates": "four small flat steel plates lying in a row on a plain surface, each a different shade of dark",
 "oil_wiped_with_paper": "a folded paper towel wiping a thin film of oil across a dark iron surface, macro",
 "wet_meat_on_hot_pan": "a wet piece of raw meat just placed on a hot iron surface, steam bursting around it",
 "pan_bottom_uneven_heat": "the underside of a frying pan showing an uneven ring of heat discolouration, macro",
 "sponge_and_hot_water": "a soft sponge pressed on a dark iron surface under running hot water, macro",
 "empty_pan_on_high_flame": "an empty pan sitting on a high gas flame, faint haze rising, macro of the flame edge",
 "consumer_report_paper": "a plain stapled paper report lying on a desk under a lamp, text blurred and unreadable",
 "mother_hand_wiping_pan": "an older woman's hand wiping a dark iron pan with a cloth, no face, warm kitchen light",
}

# ══ ANH THUONG ═════════════════════════════════════════════════════════════
PAN_DULL = "a cast-iron frying pan with a dull grey patchy surface, food residue stuck in the centre"
PAN_GOOD = "a cast-iron frying pan with a deep black glossy surface reflecting the light"
DROP = "a single water droplet beading up and rolling on a hot dark iron surface"
MOTHER = "an older woman's hands at a kitchen sink, no face, warm evening light"

SUBJ = {}


def S(frag, text):
    SUBJ[idx(frag)] = text


# ── HOI I ─────────────────────────────────────────────────────────────────
S("今朝、フライ返しを差し込んだら", "extreme macro of a fried egg torn in half, the white still stuck to a dark iron pan")
S("あの、めりめり、という音", "a spatula lifting a broken fried egg, ragged edges, macro")
S("私の腕が落ちたのだろうか", "an ordinary Japanese kitchen in the morning, a pan on the stove, quiet")
S("今から台所へ行って、空のまま火にかけて", "an empty iron pan heating on a gas flame, nothing in it")
S("ジュッと音を立てて消えたら", "a water droplet hitting a warm pan and instantly vanishing into steam, macro")
S("ところが、今日の話が妙なのはここからで", PAN_DULL)
S("焦げついた鉄のフライパンを、10分で戻す", "a worn iron pan lying on a kitchen counter beside a bottle of oil")
S("白状しますと、私は鉄のフライパンを2枚", "two discarded iron pans in a rubbish area, rusty and abandoned")
S("くっつくようになったから、寿命が来た", "a hand holding an old pan over a bin, hesitating, no face")
S("2枚目を捨てた日、母が台所に立っていて", MOTHER)
S("私は、はいはい、と聞き流しました", "a kitchen doorway seen from a hallway, someone just out of frame")
S("今日の話は、この一言が", "an old iron pan hanging on a kitchen wall, decades of use visible")

# ── HOI II ────────────────────────────────────────────────────────────────
S("さて、そもそも「くっつく」とは", "an egg sticking hard to a pan surface, close up")
S("油が足りないから。汚れが残っているから", "a bottle of cooking oil and a scrubbing brush on a counter")
S("ところが、この現象をまじめに測った", "an old scientific journal lying open on a desk, text unreadable")
S("1977年、お茶の水女子大学の平野美那世", "a stack of old academic journals on a library shelf")
S("機械の軸受けは、油の膜が切れて", "extreme macro of a worn metal bearing, scored surface")
S("あなたのフライパンの上で起きていたのも", "extreme macro of a pan surface where food has welded itself to the metal")
S("卵が触れているつもりの相手は", "macro cross-section feel: egg white pressed against bare dark metal")
S("そして、タンパク質は熱い金属と出会うと", "protein browning hard against a hot metal surface, macro")
S("めりめり、と鳴ったあの音は", "a spatula edge forcing under stuck egg white, macro")
S("だからこの研究は、焦げつきやすさを", "a small weighted rod resting on a flat steel plate, laboratory feel")
S("鉄の板に重りを載せた棒をすべらせて", "a laboratory bench with steel test plates and a measuring rig, plain")
S("そして最後に、その板でホットケーキを", "a pancake cooking on a flat steel plate, evenly browned")
S("ところが、ここからが今日の核心です", "extreme macro of a thin dark film on an iron surface, faint sheen")
S("摩擦の小さかった板の表面には", PAN_GOOD)
S("この研究は、膜の正体を赤外線で調べています", "an infrared spectrometer readout on paper, curves only, no readable text")
S("大豆油を塗って、200度、あるいは300度に", "a thin layer of oil smoking gently on a hot iron plate")
S("油の中の脂肪酸が、鉄と反応して", "extreme macro of a hardened dark polymerised oil layer on iron")
S("つまり、鉄のフライパンの「くっつかない面」は", PAN_GOOD)
S("ここが、多くの台所で取り違えられている", "a bottle of oil tipped over a cold pan, oil pooling")
S("油を敷く、という言い方をします", "a cloth laid loosely over a metal surface, wrinkles visible")
S("焼き付ける、という言い方もあります", "a baked enamel coating on metal, glossy and bonded, macro")
S("そして、その反応が起きるのは", "an infrared thermometer pointed at a hot pan, digits blurred")
S("同じ報告の予備の実験では", "a thermocouple probe touching the surface of a hot iron pan")
S("鉄というのは、膜が育つ温度の帯から", "an iron pan glowing faintly with heat haze above it")

# ── HOI III ───────────────────────────────────────────────────────────────
S("ところが、同じように油を塗って焼いても", "two iron plates side by side, one dull, one glossy")
S("冷たいフライパンに、油をひく", "cold oil poured into a cold pan, thick and still")
S("おそらく、いちばん多くの家でされている手順です", "an ordinary kitchen counter with a pan, oil bottle and salt")
S("先ほどの研究は、鉄の板を4通りに", "four small steel test plates lined up, subtly different surfaces")
S("何もしない板。空焼きだけした板", "a bare untreated steel plate, matte grey, macro")
S("なぜ、先に空焼きなのでしょうか", "an empty pan on a flame with faint smoke rising from its surface")
S("鉄の面には、目に見えない水気と", "extreme macro of a metal surface with microscopic pits and residue")
S("台所での手順にすると、こうなります", "an iron pan, a tablespoon of oil and a folded paper towel laid out on a counter")
S("まず、何も入れないフライパンを中火に", "an empty iron pan over a medium gas flame")
S("いったん火を弱めて、油を大さじ1杯", "a tablespoon of oil being poured into a hot pan, oil spreading fast")
S("弱火のまま、1分から2分", "thin wisps of smoke rising from an oiled pan on low flame")
S("そして、余った油を、たたんだ紙で拭き取って", "a folded paper towel wiping excess oil from a hot pan, held with tongs")
S("膜は、うすいほど強い", "an extremely thin oil sheen on dark iron, almost invisible, macro")
S("それでも、膜を作った翌日に", "a seasoned pan sitting on a stove the next morning, looking fine")
S("相手は、同じ台所にいます。冷蔵庫の中です", "a refrigerator door standing open in a dim kitchen, cold light spilling out")
S("冷蔵庫から出したばかりの肉を", "raw meat straight from the fridge on a plate, surface visibly wet")
S("表面には、目に見えない水が残っています", "extreme macro of tiny water droplets on the surface of raw meat")
S("200度に上がっていた鉄が", "steam bursting violently from meat the moment it touches a hot pan")
S("ですから、肉や魚は、焼く前に紙で押さえて", "a paper towel pressed onto raw meat to blot the surface dry")
S("そして、もう一つだけ。あなたのフライパンは", "the underside of a pan showing a ring of heat discolouration")
S("同じ火にかけても、熱が広がらない鍋では", "a thin stainless pan on a flame, one bright hot spot in the centre")
S("真ん中だけが茶色くなるフライパン", "a pancake browned dark in the centre and pale at the edges")

# ── HOI IV ────────────────────────────────────────────────────────────────
S("ここまでで、膜の作り方と、守り方までは", PAN_GOOD)
S("さて、母の一言に戻ります。鉄に洗剤を", "a bottle of dish soap standing beside an iron pan in a sink")
S("先ほどの1977年の報告は、洗う実験も", "steel test plates simmering in a pot of soapy water, laboratory feel")
S("台所用の合成洗剤の1パーセントの液で", "soapy water simmering in a plain pot, bubbles at the surface")
S("何もしていない板は、10分の煮洗いで", "a bare steel plate lifted from soapy water, completely dull")
S("つまり、食事のあとに数十秒", "a sponge wiping a dark iron pan under running water")
S("洗剤を怖がって、べたついた油ごと", "extreme macro of sticky brown oil residue coating an iron surface")
S("では、膜を本当に断ち切っているのは", "a steel wool scourer lying on a kitchen sink edge")
S("同じ報告に、答えがあります。地金が出るまで", "extreme macro of bare metal exposed where a dark layer has been scoured away")
S("金だわしで、力いっぱい", "a hand scrubbing hard at a pan with steel wool, no face")
S("ですから、洗い方はこうしてください", "a soft brush and hot water at a sink, an iron pan waiting")
S("食べ終わったら、まだ温かいうちに", "hot water poured into a still-warm iron pan in a sink, steam rising")
S("どうしても取れない焦げのときだけ", "a pan filled with hot water soaking, burnt residue loosening")
S("洗い終わったら、水気を拭いて", "an iron pan set back on a low flame, last droplets steaming away")
S("そして、ごく薄く油をなじませて", "a cloth wiping a trace of oil onto a warm dark pan")
S("ところで、削られた板は、それで終わり", "a scoured dull steel plate placed back over a flame")
S("同じ実験で、強くこすった板にもう一度", "a dull plate regaining a dark sheen after oil and heat, macro")
S("これが、鉄という道具のいちばん妙なところです", PAN_GOOD)

# ── HOI V ─────────────────────────────────────────────────────────────────
S("では、フッ素樹脂の、いわゆるテフロンの", "a black non-stick coated frying pan, factory-smooth surface")
S("あちらの膜は、工場で貼られて出てきます", "a brand new non-stick pan still in its packaging film")
S("逆に鉄は、買った日がいちばん悪い日で", "an old iron pan and a new non-stick pan side by side on a counter")
S("同じ「くっつかない面」なのに", "a worn non-stick pan with the coating flaking at the centre, macro")
S("しかも、あちらの膜には門限があります", "an empty non-stick pan sitting on a high flame, unattended")
S("炒め物や揚げ物の温度が", "a cooking thermometer in a pan of hot oil, dial blurred")
S("そして空のまま火にかければ", "an empty pan on a strong flame, heat shimmer rising")
S("この帯まで上がった空気を吸うと", "a kitchen filled with faint haze near the ceiling, window shut")
S("2016年の気管支学という専門誌には", "a stapled medical case report lying on a desk, text unreadable")
S("念のために申し添えますと", "a pan cooking normally on a moderate flame, calm kitchen")
S("そしてもう一つ、面白い記録があります", "a plain office desk with a consumer test report and a pan")
S("2016年、国民生活センターが", "a stapled report and a new frying pan side by side on a desk")
S("油を使わなくても焦げつかない、と受け取れる", "a shop shelf of frying pans, boxes unreadable, bright store light")
S("テストの結果、汚れは重曹で処理しても", "a pan with stubborn brown staining that will not come off, macro")
S("くっつかない、という言葉は", "a supermarket aisle of cookware, shelves receding into the distance")
S("そして最後には、手入れとして返ってきた", "a small bottle of oil standing alone on a plain counter")
S("ここに、この話のいちばん現実的な部分があります", "a shelf of new frying pans stacked high in a store")
S("膜を育てる技術は、売り物になりません", "an old iron pan on a worn wooden table, nothing else")
S("反対に、膜の寿命が来て買い替えて", "several discarded non-stick pans piled at a rubbish collection point")
S("私たちが手放したのは、道具ではありませんでした", "an empty kitchen counter at night, one pan hanging on the wall")

S("さて、いちばん最後に置いておいた", "a worn iron pan carried to the stove, sleeves rolled up, no face")
S("まず、洗剤とたわしで、表面のべたついた", "a scrubbing brush working at sticky old oil on an iron pan")
S("次に、何も入れないまま中火にかけます", "an empty pan on a medium flame, faint smoke starting to rise")
S("火を止めて、少し冷まします", "a pan resting off the heat, thin smoke trailing off")
S("そこへ油を大さじ1杯", "a tablespoon of oil poured into a hot pan, spreading instantly")
S("弱火で2分。火を止めて", "an oiled pan on low flame, surface starting to darken")
S("これで、あの1977年の実験でいちばん摩擦が", "the fourth test plate, darkest and glossiest of the four")
S("買い替えようとしていた3000円は", "a restored glossy black iron pan beside a tablespoon of oil")

S("正直に申し上げれば、これは万能ではありません", "a non-stick pan with its coating peeled away, beyond saving")
S("フッ素樹脂がはがれてしまったフライパンは", "a flaking non-stick surface, macro, clearly damaged")
S("アルミやステンレスの多層鍋も", "a multi-layer stainless pan with a bright polished base")
S("油を焼きつけるときは、少し煙が出ます", "a kitchen window opened and an extractor fan running above a stove")

S("最後に、母の一言に帰ります", MOTHER)
S("半分は、当たっていました", "a hand holding steel wool over an iron pan, about to scrub, no face")
S("ところが半分は、外れていました", "a soft sponge and dish soap beside a dark iron pan")
S("そして母が本当に守っていたのは", "an iron pan set back on a low flame right after washing, droplets steaming")
S("拭いて、火にかけて、薄く油をひく", "a cloth wiping a trace of oil onto a warm pan, evening kitchen light")
S("母は、金属石けんという言葉を知りません", "an old kitchen with worn wooden shelves and a single hanging pan")
S("姑にそう言われたから", "an old family kitchen at dusk, one pan on the stove, quiet")
S("岩手の南部鉄器には、金気止めという", "a cast-iron kettle sitting on charcoal embers, dark and heavy")
S("膜を貼るのではなく、膜を生ませる", "extreme macro of the black oxide surface of an old cast-iron kettle")
S("私たちは、くっつかない面を、買えるように", "a store shelf of non-stick pans, bright and uniform")
S("今夜、水を一滴だけ落としてみてください", DROP)
S("そしてもし、お母さまやお祖母さまから", "an old kitchen notebook and a worn pan on a table, evening light")
S("次にお話しするのは、鉄と同じように", "a worn wooden-handled tool hanging on a kitchen wall, evening light")

DEF = [(30, "an ordinary Japanese kitchen in the morning, an iron pan on the stove"),
       (60, "a dark iron pan surface and a thin film of oil, macro"),
       (95, "an iron pan, oil and paper towel on a kitchen counter"),
       (130, "a sink, a sponge and a dark iron pan"),
       (999, "an old kitchen at dusk with a single iron pan")]


def dflt(i):
    for lim, s in DEF:
        if i < lim:
            return s
    return DEF[-1][1]


STYLE_TONE = ("Photorealistic cinematic documentary still, soft natural light, warm neutral "
              "palette, muted colors, shallow depth of field, fine detail, calm quiet mood, "
              "16:9 horizontal, no text, no letters, no logos, no brand labels, no human faces, "
              "no watermark")

STYLE = (STYLE_TONE.replace("documentary still, ",
         "documentary still from a single continuous story in one ordinary Japanese home "
         "kitchen: a pale wooden counter, a gas stove, one cast-iron frying pan, "))

OFF_KITCHEN = set()
for f in ("1977年、お茶の水女子大学の平野美那世", "機械の軸受けは、油の膜が切れて",
          "だからこの研究は、焦げつきやすさを", "鉄の板に重りを載せた棒をすべらせて",
          "この研究は、膜の正体を赤外線で調べています", "先ほどの研究は、鉄の板を4通りに",
          "2016年の気管支学という専門誌には", "そしてもう一つ、面白い記録があります",
          "2016年、国民生活センターが", "油を使わなくても焦げつかない、と受け取れる",
          "くっつかない、という言葉は", "ここに、この話のいちばん現実的な部分があります",
          "反対に、膜の寿命が来て買い替えて", "私たちは、くっつかない面を、買えるように",
          "岩手の南部鉄器には、金気止めという", "ところが、この現象をまじめに測った"):
    OFF_KITCHEN.add(idx(f))

STYLE_MACRO = ("Photorealistic extreme close-up macro photograph, the subject FILLS THE FRAME "
               "and is the only thing visible, tight crop, plain dark out-of-focus background, "
               "NO room, NO wall, NO sky, NO tools in view unless named. Hard directional light, "
               "high micro-detail, muted warm palette, calm documentary mood, 16:9 horizontal, "
               "no text, no letters, no logos, no brand labels, no human faces, no watermark")

MACRO = set()
for f in ("今朝、フライ返しを差し込んだら", "あの、めりめり、という音", "ジュッと音を立てて消えたら",
          "ところが、今日の話が妙なのはここからで", "あなたのフライパンの上で起きていたのも",
          "卵が触れているつもりの相手は", "そして、タンパク質は熱い金属と出会うと",
          "めりめり、と鳴ったあの音は", "ところが、ここからが今日の核心です",
          "油の中の脂肪酸が、鉄と反応して", "焼き付ける、という言い方もあります",
          "鉄の面には、目に見えない水気と", "膜は、うすいほど強い",
          "表面には、目に見えない水が残っています", "200度に上がっていた鉄が",
          "そして、もう一つだけ。あなたのフライパンは", "洗剤を怖がって、べたついた油ごと",
          "同じ報告に、答えがあります。地金が出るまで", "同じ実験で、強くこすった板にもう一度",
          "同じ「くっつかない面」なのに", "テストの結果、汚れは重曹で処理しても",
          "膜を貼るのではなく、膜を生ませる", "今夜、水を一滴だけ落としてみてください",
          "何もしない板。空焼きだけした板", "機械の軸受けは、油の膜が切れて"):
    MACRO.add(idx(f))


FOCUS_LINES = ("あの、めりめり、という音", "卵が触れているつもりの相手は",
               "同じ報告に、答えがあります。地金が出るまで", "膜は、うすいほど強い",
               "同じ「くっつかない面」なのに", "テストの結果、汚れは重曹で処理しても",
               "そして、もう一つだけ。あなたのフライパンは")
WIPE_LINES = {"これが、鉄という道具のいちばん妙なところです": "slides_img/wipe_pan_glossy.jpg",
              "買い替えようとしていた3000円は": "slides_img/wipe_pan_restored.jpg",
              "同じ実験で、強くこすった板にもう一度": "slides_img/wipe_plate_reborn.jpg"}


# ══ LỚP CHUYỂN ĐỘNG BẰNG HÌNH (make_shot.py) ═══════════════════════════════
# user 2026-08-18: "chuyển động kiểu gần như nenkin, nhưng chuyển động bằng hình ảnh".
# Mọi entry ảnh thường -> clip build-on: nền ảnh đứng yên, thứ HIỆN DẦN là hình.
#   soft  : chỉ thở  (câu kể — mặc định, để vòng đỏ không lặp 60 lần)
#   inset : tấm ảnh macro trượt vào + mũi tên (câu phóng to chi tiết = dòng MACRO)
#   focus : vòng khoanh đỏ vẽ dần (câu chỉ đích danh — chọn TAY, ít thôi)
#   wipe  : ảnh B lộ dần đè ảnh A (câu đổi trạng thái — cần 2 ảnh)
SHOT_FOCUS = set()
for f in FOCUS_LINES:
    SHOT_FOCUS.add(idx(f))
SHOT_WIPE = {}
for f, second in WIPE_LINES.items():
    SHOT_WIPE[idx(f)] = second


_shot_n = [0]


def shot_spec(i, img_rel):
    """🔴 VAI THEO ẢNH, không theo thứ tự:
       ảnh ĐÃ MACRO  -> `focus` (khoanh vào chi tiết; phóng to nữa thì vỡ hạt)
       ảnh CẢNH      -> `inset` (cắt một mảnh của chính nó, phóng lên) — 2 trong 3 lần,
                        lần thứ ba để `soft` cho mắt nghỉ (nhịp thở, không phải tiết kiệm)."""
    if i in SHOT_WIPE:
        return {"mode": "wipe", "photo": img_rel, "photo2": SHOT_WIPE[i]}
    if i in SHOT_FOCUS or i in MACRO:
        return {"mode": "focus", "photo": img_rel, "focus": [0.54, 0.48, 0.17]}
    _shot_n[0] += 1
    if _shot_n[0] % 3 == 0:
        return {"mode": "soft", "photo": img_rel}
    # card đặt ĐỐI DIỆN vùng nhìn: mũi tên đi từ card sang chủ thể, không cắt ngang nó
    fx = 0.34 if (_shot_n[0] % 2 == 0) else 0.66
    return {"mode": "inset", "photo": img_rel, "focus": [fx, 0.5, 0.16],
            "inset_pos": "br" if fx < 0.5 else "bl"}

# wipe (trước→sau) là mode kể chuyện đắt nhất — ép thành cue, nếu không nó bị
# luật gom 58 ký nuốt mất (đã dính: #21 khai 3 wipe mà ra 0)
FORCE = {idx("ここまでご覧いただき、ありがとうございます")} | set(SHOT_WIPE)
# 🔴 SKIP: cau thoai cua me lap Y HET NHAU 2 lan (phut 2 + phut 17) — khong substring
#    nao tach duoc => cue dong LIEN TRUOC, hinh giu nguyen khi thoai vang len
SKIP = {i for i, l in enumerate(L) if l.startswith("「その鍋はね")}
CUE, acc = [], 0
for i, l in enumerate(L):
    if i in SKIP:
        acc += len(l)
        continue
    if i == 0 or i in VOX or i in FORCE or acc >= 58:
        CUE.append(i)
        acc = 0
    acc += len(l)

TOT = sum(len(x) for x in L)
CPS = TOT / DUR
MIN_CH = int(6 * CPS) + 1
_pos, _a = {}, 0
for i, l in enumerate(L):
    _pos[i] = _a
    _a += len(l)
_keep = []
for k, i in enumerate(CUE):
    if k + 1 < len(CUE) and _pos[CUE[k + 1]] - _pos[i] < MIN_CH:
        if i not in VOX and i != 0:
            continue
    _keep.append(i)
CUE = _keep


def uniq_key(i):
    for n in (16, 24, 34, 48):
        m = L[i][:n]
        if sum(1 for x in L if m in x) == 1:
            return m
    return None


out, flow, names, bad = [], [], [], []
for i in CUE:
    m = uniq_key(i)
    if m is None:
        bad.append((i, L[i][:20]))
        continue
    if i in VOX:
        kind, spec, sub = VOX[i]
        v = {"kind": kind}
        v.update(spec)
        v["bg"] = "photo"
        v["photo"] = P(sub)
        v["photo_style"] = "darken"
        flow.append(f"{STYLE_MACRO}. {VOXSUBJ[sub]}")
        names.append(f"ai_clean/{sub}.jpeg")
        out.append({"match": m, "photo": False, "video": True, "vox": v})
    else:
        idxe = len(out)
        st = (STYLE_MACRO if i in MACRO
              else STYLE_TONE if i in OFF_KITCHEN else STYLE)
        flow.append(f"{st}. {SUBJ.get(i) or dflt(i)}")
        rel = f"slides_img/slide_{idxe:02d}.jpg"
        names.append(rel)
        out.append({"match": m, "photo": False, "video": True, "shot": shot_spec(i, rel)})

S_DIR = PROJ / "03_SCRIPTS"
(S_DIR / f"{SLUG}_SLIDES.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(S_DIR / f"{SLUG}_IMG_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
(S_DIR / f"{SLUG}_IMG_NAMES.txt").write_text(
    "\n".join(f"{n+1:3d}  {p}" for n, p in enumerate(names)) + "\n", encoding="utf-8")

nv = [x["vox"]["kind"] for x in out if isinstance(x.get("vox"), dict)]
npho = sum(1 for x in out if x.get("photo") is True)
print(f"entry {len(out)} | anh thuong {npho} | vox {len(nv)}")
print(f"doi hinh/phut {len(out)/(DUR/60):.1f} (tran 6) | giay/entry {DUR/len(out):.1f} (san 6)")
print(f"prompt {len(flow)} dong | match TRUNG/THIEU: {bad if bad else '0 - tat ca duy nhat'}")
print("kinds:", ", ".join(sorted(set(nv))))
