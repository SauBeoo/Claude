# -*- coding: utf-8 -*-
r"""Sinh 24_kamemushi-3mm-sukima_SLIDES.json + bo prompt anh (FLOW/NAMES).

LOP HINH = MOT CAI CUA SO NHOM TRANG, tu dem mua dong den chieu thu.

  NEO LAP LAI (ve ra CUNG mot vat moi lan):
    - 1 CON KAMEMUSHI nau hinh khien: tren tuong (mo bai) -> trong khe (giua) -> tren la (cuoi)
    - CUA SO NHOM TRANG truot + luoi: khe doc ho -> khung chong nhau (het khe)
    - CARTEN co nep gap: tu thu dau bai -> loi moi cuoi bai
    - MAI TRAN (yaneura) toi: nha bac trong le
    - AMADO go (sepia): song 6
    - GA TRANG tren day phoi: song 5

  6 SONG:
    I   dem mua dong: 1 con tren tuong -> "khong tu ngoai vao" -> ten no + 1000 con
    II  dong ho: 15 do -> 6 tuan -> "som qua muon qua deu vo nghia"
    III danh thuc: 20 do -> kotatsu -> nghich ly thang 9 vs thang 12
    IV  duong vao: 1.15 vs 3 mm -> JSMA -> mo het + to xe -> 3 lo con lai
    V   mau trang + khong duoc dap (tuyen mui)
    VI  amado = lop ngoai da mat -> dong tien -> mo ben nao (3 giay)
"""
import re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "24_kamemushi-3mm-sukima"
VD = f"E:/Claude/Projects/youtube-jp-co-dai/06_VIDEO/{SLUG}"
DUR = 1104          # 5.623 ky / 305,4 ky-phut = 18,4 phut

L = [re.sub(r"\[[^\]]*\]", "", l).strip()
     for l in (PROJ / "03_SCRIPTS" / f"{SLUG}_TTS.md").read_text(encoding="utf-8").split("\n")]
L = [l for l in L if l and not l.startswith(("#", ">", "TARGET_QUERY", "INTENT"))]


def P(n):
    return f"{VD}/ai_clean/{n}.jpeg"


def idx(frag):
    hit = [i for i, l in enumerate(L) if frag in l]
    if len(hit) != 1:
        raise SystemExit(f"NEO KHONG DUY NHAT ({len(hit)}): {frag}")
    return hit[0]


# == THE VOX ==================================================================
VOXSPEC = [
 ("あれは、外から入ってきたのではありません",
  ("title", {"title": "侵入ではなく、越冬",
             "sub": "去年の秋から、ずっと家の中にいた1匹"}, "bug_on_white_wall_winter")),

 ("岡山県立図書館が、専門書をもとに",
  ("collage", {"kicker": "冬を越す場所が、種でちがう", "title": "家を選ぶのは、3種のうち1種だけ",
               "items": [{"label": "チャバネアオ", "mark": "x"},
                         {"label": "ツヤアオ", "mark": "x"},
                         {"label": "クサギ", "mark": "o"}],
               "note": "チャバネアオは落葉の下、ツヤアオは常緑樹の葉、クサギカメムシだけが家屋の隙間",
               "source": "岡山県立図書館 レファレンス協同データベース"},
   "three_stinkbugs_row")),

 ("同じ記録に、もう一行あります",
  ("stat", {"kicker": "成虫で冬を越すとき", "big": "1000", "unit": "匹超",
            "sub": "1か所に集まることもある",
            "note": "屋根裏、壁の中、押し入れ、カーテンの裏",
            "source": "岡山県立図書館 レファレンス協同データベース"},
   "dark_attic_beam")),

 ("この虫にとって、家は隠れ場所ではありません",
  ("collage", {"kicker": "家の中の越冬場所", "title": "隠れ場所ではなく、寝室です",
               "items": [{"label": "屋根裏", "mark": "o"},
                         {"label": "壁の中", "mark": "o"},
                         {"label": "押し入れ", "mark": "o"},
                         {"label": "カーテンの裏", "mark": "o"}],
               "note": "どれも、暖かくて、狭くて、暗い"},
   "closet_shelf_folded_cloth")),

 ("千葉県農林総合研究センターが5月に出した注意報では",
  ("bar", {"kicker": "5月のわなにかかった数", "title": "今年は、平年のちょうど2倍",
           "bars": [["今年", 9], ["平年", 4.5]], "hot": 0,
           "source": "千葉県農林総合研究センター 2026年5月27日"},
   "pear_orchard_trap")),

 ("外の気温が15度を下回ると",
  ("timeline", {"kicker": "1年の予定表", "title": "入るのも、出るのも、決まっている",
                "marks": [["9月下旬", "入る"], ["11月", "入り終わる"],
                          ["12〜3月", "眠る"], ["春", "出てくる"]],
                "note": "外気が15度を下回ると、越冬場所を探しはじめる"},
   "autumn_house_wall_evening")),

 ("つまり、防げる期間は、だいたい6週間しかありません",
  ("stat", {"kicker": "隙間をふさぐ意味がある期間", "big": "6", "unit": "週間",
            "sub": "9月の終わりから、11月まで",
            "note": "早すぎても、遅すぎても、効きません"},
   "calendar_on_kitchen_wall")),

 ("部屋の温度が20度を超えると",
  ("stat", {"kicker": "起こしているのは春ではない", "big": "20", "unit": "度",
            "sub": "室温がここを超えると、春が来たと勘違いする",
            "note": "こたつ、ストーブ、暖房の入った部屋"},
   "kotatsu_warm_room")),

 ("同じ行いが、9月なら守りになり",
  ("compare", {"kicker": "同じ行い、反対の結果", "title": "ふさぐ時期で、意味が裏返る",
               "left": {"label": "9月にふさぐ", "mark": "o", "verdict": "入れない"},
               "right": {"label": "12月にふさぐ", "mark": "x", "verdict": "出られない"}},
   "hand_taping_window_gap")),

 ("数字を並べます。よく使われている18メッシュ",
  ("bar", {"kicker": "通り道の大きさ", "title": "網の目より、その横のほうが大きい",
           "bars": [["網の目", 1.15], ["最も細かい網", 0.67], ["横の隙間", 3]], "hot": 2,
           "note": "単位はミリ。網を細かくする勝負は、とうに終わっている"},
   "screen_mesh_macro")),

 ("日本サッシ協会が、はっきり書いています",
  ("source", {"kicker": "出典", "org": "一般社団法人 日本サッシ協会",
              "asof": "網戸からの虫の侵入",
              "quote": "軽快に開閉するため、枠やレールとの間にある程度のすきまを設けた構造",
              "number": "3ミリ",
              "note": "モヘアやパッキンを入れても、完全には防げない"},
   "sliding_window_frame_seam")),

 ("戸車の横に小さなねじが一つあります",
  ("process", {"kicker": "0円でできる3つ", "title": "今夜、窓の前でやること",
               "steps": [{"label": "網戸をいっぱいまで寄せる", "sub": "枠と枠を重ねる"},
                         {"label": "枠が重なる側の窓を開ける", "sub": "縦の線が消える"},
                         {"label": "戸車のねじを回す", "sub": "斜めの三角をなくす", "hot": True}]},
   "screen_door_roller_screw")),

 ("この3か所は、隙間テープで足ります",
  ("collage", {"kicker": "窓を直しても残る入口", "title": "数えると、たいてい3か所",
               "items": [{"label": "給気口", "mark": "x"},
                         {"label": "エアコンの穴", "mark": "x"},
                         {"label": "玄関ドアの下", "mark": "x"}],
               "note": "隙間テープなら数百円。一冬もちます"},
   "wall_air_vent_round")),

 ("家の網は1.15ミリ。畑の網は9ミリ",
  ("stat", {"kicker": "畑で使う網の目合い", "big": "8", "unit": "倍粗い",
            "sub": "それでも、畑では足りている",
            "note": "差は網ではありません。網の横にあるものです",
            "source": "千葉県農林総合研究センター 2026年5月27日"},
   "orchard_net_wide_mesh")),

 ("ですから、やることは2つだけです",
  ("process", {"kicker": "洗濯物でやること", "title": "白は内側、そして日が傾く前",
               "steps": [{"label": "白いものを内側に干す", "sub": "色のあるものを外側に"},
                         {"label": "日が傾く前に取り込む", "sub": "いちばん飛ぶ時間を避ける",
                          "hot": True}]},
   "white_sheet_on_line")),

 ("つまり、よく言われる、潰すと仲間が呼ばれる",
  ("compare", {"kicker": "同じ匂い、逆の意味", "title": "濃さで、役目が入れ替わる",
               "left": {"label": "濃い匂い", "mark": "o", "verdict": "警報 → 逃げる"},
               "right": {"label": "薄い匂い", "mark": "x", "verdict": "集まる合図"},
               "note": "主成分はトランス2ヘキセナール。潰すと、薄まる途中を家の中に作る"},
   "stinkbug_leg_macro")),

 ("つまり、ひと季節に2回か3回、買い直す形になります",
  ("bar", {"kicker": "単位は、か月", "title": "効果が切れても、まだ飛んでいる",
           "bars": [["忌避剤", 2], ["飛ぶ時期", 3]], "hot": 1,
           "note": "表示は約1〜2か月。飛来は9月下旬から11月"},
   "repellent_spray_on_screen")),

 ("今夜、窓の前に立って",
  ("title", {"title": "開ける側を、見るだけ",
             "sub": "網戸のある側のガラス戸を開ける。3秒、0円"},
   "window_at_night_from_inside")),
]

VOX = {}
for frag, spec in VOXSPEC:
    VOX[idx(frag)] = spec

VOXSUBJ = {
 "bug_on_white_wall_winter": "one brown shield-shaped stink bug on a pale interior wall, cold winter light, macro",
 "three_stinkbugs_row": "three brown and green shield-shaped stink bugs resting apart on a plain surface, macro",
 "dark_attic_beam": "the underside of a dark wooden attic beam, dusty and dim, macro",
 "closet_shelf_folded_cloth": "folded cloth stacked on a dim closet shelf, deep shadow between the folds, macro",
 "pear_orchard_trap": "a simple insect trap hanging from a pear branch in an orchard, macro",
 "autumn_house_wall_evening": "a sunlit house wall in late autumn afternoon, long shadows, plain",
 "calendar_on_kitchen_wall": "a plain paper wall calendar hanging in a kitchen, dates blurred and unreadable",
 "kotatsu_warm_room": "a low table with a warm quilt in a dim tatami room, soft orange light",
 "hand_taping_window_gap": "a hand pressing draught tape along a window frame edge, no face, macro",
 "screen_mesh_macro": "extreme macro of a fine insect screen mesh, individual wires visible",
 "sliding_window_frame_seam": "extreme macro of the seam where an insect screen frame meets a glass door frame",
 "screen_door_roller_screw": "extreme macro of the small adjusting screw beside a screen door roller",
 "wall_air_vent_round": "a round white air supply vent on an interior wall, macro",
 "orchard_net_wide_mesh": "extreme macro of a wide-mesh orchard netting against a bright sky",
 "white_sheet_on_line": "a white cotton sheet hanging on an outdoor line in bright afternoon sun",
 "stinkbug_leg_macro": "extreme macro of the underside joint of a brown shield-shaped insect, plain dark background",
 "repellent_spray_on_screen": "an aerosol can standing beside a window screen, label unreadable, plain",
 "window_at_night_from_inside": "a white aluminium sliding window seen from inside a dark room at night",
}

# == ANH THUONG ===============================================================
BUG_WALL = "one brown shield-shaped stink bug on a pale interior wall, calm and clean, not gruesome"
WIN_HALF = "a white aluminium sliding window with the insect screen slid only halfway, a thin vertical gap where the frames fail to overlap"
WIN_FULL = "a white aluminium sliding window with the insect screen slid fully across, the screen frame overlapping the glass frame, no gap"
CURTAIN = "a pale curtain hanging in folds by a window, quiet room, nobody present"
AMADO_OPEN = "a wooden storm shutter standing open beside a veranda at dusk, sepia warm tones"
AMADO_SHUT = "a wooden storm shutter closed across a veranda at dusk, sepia warm tones"
ATTIC = "a dim attic space with bare wooden beams, dust in the air"
SHEET = "a white cotton sheet hanging on an outdoor washing line in strong afternoon light"

SUBJ = {}


def S(frag, text):
    SUBJ[idx(frag)] = text


# -- SONG I -------------------------------------------------------------------
S("真冬の夜に、壁を這うカメムシを", BUG_WALL)
S("外は雪。窓は閉めきっている", "a dark window pane at night with snow outside, seen from a warm room")
S("去年の秋から、ずっと家の中にいたのです", "a pale interior wall in winter light, one small dark shape near the ceiling corner")
S("ですから、やることは今月です", WIN_FULL)
S("網の目は1.15ミリ。あの虫が通るのは", "extreme macro of insect screen mesh beside the frame edge, the gap visible")
S("ところが、時期を過ぎてから隙間をふさぐと", "a roll of draught tape lying on a window sill")
S("いちばん効く一手は、いちばん最後に", "a white aluminium sliding window seen straight on, curtains drawn back")
S("お住まいの地域では、春になると", "a spring window with soft light, a small dark shape on the sill")
S("先に、白状します", CURTAIN)
S("私は去年の三月、カーテンを洗おうとして", "hands opening the folds of a pale curtain, no face, soft light")
S("2匹、落ちてきました", "two small brown shield-shaped insects on a wooden floor beneath a curtain")
S("窓は冬のあいだ、ほとんど開けていません", "a closed window in a quiet room, winter light, nobody present")
S("答えは、入っていなかった、です", CURTAIN)
S("さて、その1匹には、名前があります", BUG_WALL)
S("今年、各県が出した注意報に並んでいるのは三種類", "three shield-shaped insects of slightly different colour on a plain pale surface")
S("じつは、この三種類は、冬を越す場所が", "fallen autumn leaves, an evergreen branch and a house wall in one quiet frame")
S("チャバネアオカメムシは、落ち葉の下", "a layer of damp fallen leaves on the ground, macro")
S("ツヤアオカメムシは、常緑樹の葉の上", "glossy evergreen leaves in soft daylight, macro")
S("そして、クサギカメムシは、家屋の隙間です", "extreme macro of a narrow gap in a house wall board, dark inside")
S("つまり、三種類のうち、家を選ぶのは", "a plain house exterior wall with a narrow shadowed seam running down it")
S("あなたが真冬に壁で見たあの1匹には", BUG_WALL)
S("屋根裏、壁の中、押し入れ、カーテンの裏", ATTIC)
S("それから、今年の数字も見ておきます", "a pear orchard in early summer, young fruit on the branches")
S("兵庫県も、平年を大幅に上回る", "a plain official notice sheet on a desk, text blurred and unreadable")

# -- SONG II ------------------------------------------------------------------
S("では、その入居は、いつ行われるのでしょうか", "a house wall in late afternoon autumn sun, warm and still")
S("ここが、今日いちばん大事なところです", "a paper calendar page on a wall, dates unreadable, autumn light")
S("早すぎても、遅すぎても、意味がありません", "an open window with cool autumn air, curtains barely moving")
S("今日は8月の終わりです", "late summer light on a house wall, cicada-season haze")
S("秋に売り場が広がるのも", "a shop shelf of household aerosol cans, labels unreadable, bright store light")

# -- SONG III -----------------------------------------------------------------
S("では、なぜ、真冬に出てくるのでしょうか", "a dim winter room with a warm glow from a heater, nobody present")
S("ここが、この虫のいちばん奇妙なところです", "a pale wall lit by warm indoor light in winter")
S("起こしているのは、春ではありません。暖房です", "an old kerosene stove burning quietly in a tatami room")
S("12月に、こたつを出す", "a low table with a warm quilt being set up in a tatami room, winter")
S("あの1匹は、侵入してきたのではありません", "one brown shield-shaped insect walking on a warm interior wall")
S("じつは、私の家の三月のカーテンも", CURTAIN)
S("近所で30年、梨をやっているかたに", "a pear orchard in autumn with a farmhouse roof behind the trees")
S("「うちは屋根裏だからね", ATTIC)
S("落ちてくる、という言い方でした", "looking up at a dark attic hatch in a ceiling, dim light")
S("そして、ここから、今日いちばん申し上げたい一行", "a narrow gap in a window frame, half covered with tape")
S("隙間をふさぐのは、正しい対策です", "a hand pressing draught tape into a window frame gap, no face")
S("出口をふさぐことになるからです", "a taped-over gap seen from inside, the room dim behind it")
S("中で冬を越している数百の個体は", ATTIC)
S("ですから、遅れてしまった年は", "a window left slightly ajar in a cold room, faint daylight")
S("では、その6週間のうちに、どこをふさげばいいのか", WIN_HALF)

# -- SONG IV ------------------------------------------------------------------
S("まず、多くの方が最初に考えることを", "a rolled bundle of new insect screen mesh leaning against a wall")
S("網戸を、目の細かいものに張り替える", "hands stretching new screen mesh over an aluminium frame, no face")
S("いちばん細かい30メッシュでも", "extreme macro of very fine insect screen mesh, wires almost touching")
S("どれも、もう2ミリを大きく下回っています", "extreme macro comparison feel: fine mesh filling the frame, sharp detail")
S("金鳥の解説では、カメムシは2ミリから3ミリの隙間", "extreme macro of a narrow gap between two aluminium frame edges")
S("網の目は1ミリを切っているのに", "extreme macro where fine mesh ends and a bare frame gap begins")
S("では、その3ミリはどこにあるのか", WIN_HALF)
S("モヘアやパッキンを入れても", "extreme macro of a grey mohair brush strip along a window frame edge")
S("不良品の話ではありません", "a hand sliding a screen door smoothly along its rail, no face")
S("そして、その隙間の大きさは、家ではなく", WIN_HALF)
S("引違いの窓は、ガラスの戸が2枚", "a white aluminium sliding window seen straight on, two glass panels offset")
S("網戸を半分だけ開けて止めると", WIN_HALF)
S("その重ならない線が、そのまま縦の入口に", "extreme macro of a thin vertical gap running down between two window frames")
S("網戸をいっぱいまで開けて寄せると", WIN_FULL)
S("それから、網戸の下の車輪、戸車です", "the bottom rail of a screen door showing a small plastic roller, macro")
S("10年、20年使った網戸は", "an old screen door sitting slightly crooked in its frame, gap at the top")
S("ところが、窓を直しても", "an interior wall with a round air vent and an air conditioner pipe cover")
S("数えると、たいてい3か所です", "a plain interior wall with a round vent, quiet room")
S("一つ目は、壁についている丸い給気口", "a round white air supply vent on an interior wall, cover open, macro")
S("二つ目は、エアコンの配管が壁を抜けるところ", "an air conditioner pipe passing through a wall, putty around the hole, macro")
S("そのパテは10年、15年で縮みます", "extreme macro of dried cracked putty shrunk away from a pipe in a wall hole")
S("三つ目は、玄関ドアの下", "the narrow gap under a Japanese front door seen from inside, dim hallway")
S("ここで、面白い数字を一つ並べておきます", "a wide-mesh orchard net stretched over pear trees, bright sky")
S("先ほどの千葉県の注意報には", "wide orchard netting seen close, large square openings, macro")
S("飛んでくる成虫を、木に近づけないためだけの網", "an orchard covered with netting, seen from outside, calm daylight")
S("家のほうは、目が8倍細かいのに", "extreme macro of fine house screen mesh, dense and tight")

# -- SONG V -------------------------------------------------------------------
S("ところが、隙間をふさいでも", SHEET)
S("白です", SHEET)
S("金鳥も、白っぽい光に呼び寄せられる", "a bright white wall lit by low afternoon sun, plain")
S("寒さが苦手な虫ですから", "a white sheet on a line with two small brown insects resting on it, macro")
S("そして、日が傾く前に取り込んでください", "laundry being taken in from a line at dusk, hands only, no face")
S("じつは、これは新しい知恵ではありません", "an old Japanese house at dusk with laundry poles empty, sepia warm tones")
S("理由は虫ではなく、夜露です", "damp evening air over a garden at dusk, dew forming on a railing, macro")
S("虫を避けるつもりのなかった習慣が", "an empty washing line at dusk against a dimming sky")
S("そして、いちばんやってはいけない一手は", "one brown shield-shaped insect on a pale wall, seen from close")
S("潰さないでください", "one brown shield-shaped insect on a wall, a folded sheet of paper approaching it")
S("あの匂いは、脚の付け根にある臭腺", "extreme macro of the leg joint of a brown shield-shaped insect")
S("この匂いには、役目が二つあります", "extreme macro of a brown shield-shaped insect from above, plain background")
S("濃い匂いは、まわりの仲間に危険を", "two brown shield-shaped insects moving apart on a plain surface, macro")
S("ところが、群れをつくる種類では", "several brown shield-shaped insects gathered close on a wall corner, macro")
S("濃いあいだは逃げ、薄まっていくにつれて", "a plain pale wall with faint marks, quiet and empty")
S("潰すというのは、その薄まっていく途中を", "a faint smear on a pale wall surface, macro, nothing else")
S("取るときは、空き瓶かペットボトルを1本", "an empty glass jar and a plastic bottle standing on a window sill")
S("紙を1枚、虫の下に差し入れて", "a folded sheet of paper being slid under an insect on a sill, no face, macro")
S("掃除機は使わないでください", "a vacuum cleaner nozzle resting on a floor beside a wall, plain")

# -- SONG VI ------------------------------------------------------------------
S("では、昔の家は、この6週間を", AMADO_OPEN)
S("昔の日本の家は、今の家よりずっと隙間が多い", "an old Japanese house interior with wooden boards, paper screens and a veranda, sepia")
S("ところが、秋にこの虫が寝床にしていたのは", "the back of a weathered wooden board on an old house exterior, sepia, macro")
S("理由は1つです。網戸の外に、もう1枚", AMADO_OPEN)
S("雨戸です", AMADO_SHUT)
S("日が傾くと、家じゅうの雨戸を閉めていました", "hands sliding a wooden storm shutter closed at dusk, sepia, no face")
S("閉めた理由は、風と雨と、そして戸締り", "a wooden storm shutter latched shut from inside, sepia warm tones")
S("この形は、今でも半分は使えます", "a modern metal shutter half lowered over a window at dusk")
S("無い場合は、夕方だけカーテンを引いて", "a curtain being drawn across a window at dusk, warm room light behind")
S("ところが、その1枚を失った家に", "a plain modern house exterior at dusk, no shutters, windows glowing")
S("忌避剤です。網戸や窓枠に吹きつけて", "an aerosol can held up to a window screen, no face, label unreadable")
S("効かないという話ではありません", "a small printed label on a spray can, text deliberately blurred")
S("飛んでくる時期は、9月の終わりから11月", "an autumn house wall in low sun, leaves scattered on the ground")
S("誰かを責める話ではありません", "a shop shelf of household sprays, bright and uniform, labels unreadable")
S("一方で、網戸をいっぱいまで寄せることと", WIN_FULL)
S("そして、いちばん最後に置いておいた", "a white aluminium sliding window seen from inside at night, dark outside")
S("網戸をいっぱいに開けても", WIN_HALF)
S("開ける側を、間違えているときです", "a white sliding window with the screen and glass panels on opposite sides")
S("引違いの窓には、右のガラス戸と", "a white aluminium sliding window seen straight on, both panels visible")
S("網戸のある側のガラス戸を開ければ", WIN_FULL)
S("反対側を開けると、網戸をいっぱいに寄せても", "extreme macro of a thin vertical gap remaining between two window frames")
S("道具も、薬も、お金も要りません", "a bare hand resting on a window latch, no face, evening light")
S("そして、もし今このあと時間があれば", CURTAIN)
S("何も落ちてこなければ、この秋はまだ間に合います", "an open curtain fold with clean floor beneath it, nothing there, soft light")

S("もちろん、万能ではありません", "an old wooden house exterior with many small gaps and worn boards")
S("古い木造のお宅は、隙間が多すぎて", "a weathered wooden wall with visible cracks between the boards, macro")
S("それから、あの匂いの成分は、目に入ると", "a running tap of clear water over cupped hands, no face")
S("肌が赤くなるかたや、匂いで気分が悪くなる", "a plain glass of water on a counter, quiet kitchen")
S("今日の話で、いちばん申し上げたかったのは", WIN_FULL)
S("この虫との勝負は、秋の6週間で", "an autumn house wall at golden hour, quiet and still")
S("春に出てくる1匹は、春の問題ではありません", "a spring window sill with soft light and one small brown insect")
S("昔の家は隙間だらけでした", AMADO_SHUT)
S("今の家は、隙間がずっと少ない", "a modern sealed window seen from outside at dusk, no shutters")
S("失った1枚の分を、私たちはいま", "a shop shelf of insect repellent cans, bright store light, labels unreadable")
S("よろしければ、教えてください", ATTIC)
S("次の話も、今の家から消えてしまった", "an old veranda at dusk with one wooden shutter half closed, sepia")

DEF = [(24, BUG_WALL),
       (48, "an autumn house wall in low afternoon sun, quiet"),
       (72, WIN_HALF),
       (100, "a white aluminium sliding window and a pale interior wall, plain"),
       (999, AMADO_SHUT)]


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
         "documentary still from a single continuous story in one ordinary Japanese house: "
         "a white aluminium sliding window, a pale plaster wall, a wooden veranda, "))

STYLE_MACRO = ("Photorealistic extreme close-up macro photograph, the subject FILLS THE FRAME "
               "and is the only thing visible, tight crop, plain dark out-of-focus background, "
               "NO room, NO wall, NO sky, NO tools in view unless named. Hard directional light, "
               "high micro-detail, muted warm palette, calm documentary mood, 16:9 horizontal, "
               "no text, no letters, no logos, no brand labels, no human faces, no watermark")

STYLE_SEPIA = (STYLE_TONE.replace("Photorealistic cinematic documentary still, ",
               "Photorealistic archival photograph of an old Japanese house, faded sepia and "
               "warm brown tones, gentle grain, "))

# canh KHONG o trong nha -> bo neo "one ordinary Japanese house"
OFF_HOUSE = set()
for f in ("それから、今年の数字も見ておきます", "兵庫県も、平年を大幅に上回る",
          "近所で30年、梨をやっているかたに", "ここで、面白い数字を一つ並べておきます",
          "先ほどの千葉県の注意報には", "飛んでくる成虫を、木に近づけないためだけの網",
          "秋に売り場が広がるのも", "誰かを責める話ではありません",
          "失った1枚の分を、私たちはいま", "まず、多くの方が最初に考えることを",
          "効かないという話ではありません"):
    OFF_HOUSE.add(idx(f))

# canh XUA -> sepia
SEPIA = set()
for f in ("では、昔の家は、この6週間を", "昔の日本の家は、今の家よりずっと隙間が多い",
          "ところが、秋にこの虫が寝床にしていたのは", "理由は1つです。網戸の外に、もう1枚",
          "雨戸です", "日が傾くと、家じゅうの雨戸を閉めていました",
          "閉めた理由は、風と雨と、そして戸締り", "じつは、これは新しい知恵ではありません",
          "昔の家は隙間だらけでした", "次の話も、今の家から消えてしまった"):
    SEPIA.add(idx(f))

MACRO = set()
for f in ("真冬の夜に、壁を這うカメムシを", "網の目は1.15ミリ。あの虫が通るのは",
          "そして、クサギカメムシは、家屋の隙間です", "チャバネアオカメムシは、落ち葉の下",
          "ツヤアオカメムシは、常緑樹の葉の上", "いちばん細かい30メッシュでも",
          "どれも、もう2ミリを大きく下回っています",
          "金鳥の解説では、カメムシは2ミリから3ミリの隙間", "網の目は1ミリを切っているのに",
          "モヘアやパッキンを入れても", "その重ならない線が、そのまま縦の入口に",
          "それから、網戸の下の車輪、戸車です", "一つ目は、壁についている丸い給気口",
          "二つ目は、エアコンの配管が壁を抜けるところ", "そのパテは10年、15年で縮みます",
          "先ほどの千葉県の注意報には", "家のほうは、目が8倍細かいのに",
          "あの匂いは、脚の付け根にある臭腺", "この匂いには、役目が二つあります",
          "濃い匂いは、まわりの仲間に危険を", "ところが、群れをつくる種類では",
          "潰すというのは、その薄まっていく途中を", "紙を1枚、虫の下に差し入れて",
          "ところが、秋にこの虫が寝床にしていたのは", "反対側を開けると、網戸をいっぱいに寄せても",
          "古い木造のお宅は、隙間が多すぎて", "寒さが苦手な虫ですから",
          "2匹、落ちてきました", "理由は虫ではなく、夜露です"):
    MACRO.add(idx(f))

FOCUS_LINES = ("網の目は1.15ミリ。あの虫が通るのは", "その重ならない線が、そのまま縦の入口に",
               "網戸をいっぱいまで開けて寄せると", "網戸のある側のガラス戸を開ければ",
               "そのパテは10年、15年で縮みます", "紙を1枚、虫の下に差し入れて",
               "家のほうは、目が8倍細かいのに", "10年、20年使った網戸は",
               "反対側を開けると、網戸をいっぱいに寄せても")

# wipe = doi trang thai (khe ho -> khe mat / amado mo -> dong). Anh "SAU" xuat RIENG.
# 🔴 WIPE DA BO (2026-08-25, sau khi soi 78 anh ve): khong mot cap nao co CUNG BO CUC.
# Generator khong lam duoc "cung goc may, chi doi mot thu" tu prompt chu — cung ho gioi han
# da ghi o media-library.md §2.10⑥ (prompt dieu khien duoc VI TRI, khong dieu khien duoc TI LE).
# Wipe giua 2 bo cuc khac nhau doc thanh CAT CANH, te hon `focus` sach. Doi ca 3 sang focus.
WIPE_LINES = {}
WIPE_SUBJ = {}


# == LOP CHUYEN DONG BANG HINH (make_shot.py) ================================
SHOT_FOCUS = set()
for f in FOCUS_LINES:
    SHOT_FOCUS.add(idx(f))
SHOT_WIPE = {}
for f, second in WIPE_LINES.items():
    SHOT_WIPE[idx(f)] = second

_shot_n = [0]


def shot_spec(i, img_rel):
    """VAI THEO ANH: macro -> focus (khoanh); canh -> inset (2/3 lan), lan 3 de soft."""
    if i in SHOT_WIPE:
        return {"mode": "wipe", "photo": img_rel, "photo2": SHOT_WIPE[i]}
    if i in SHOT_FOCUS or i in MACRO:
        return {"mode": "focus", "photo": img_rel, "focus": [0.54, 0.48, 0.17]}
    _shot_n[0] += 1
    if _shot_n[0] % 3 == 0:
        return {"mode": "soft", "photo": img_rel}
    fx = 0.34 if (_shot_n[0] % 2 == 0) else 0.66
    return {"mode": "inset", "photo": img_rel, "focus": [fx, 0.5, 0.16],
            "inset_pos": "br" if fx < 0.5 else "bl"}


FORCE = ({idx("ここまでご覧いただき、ありがとうございます"),
          # dong VAO BAI (O1) phai co khung rieng — demo 95s bat duoc loi nay
          idx("ですから、やることは今月です")}
         | set(SHOT_WIPE))
CUE, acc = [], 0
for i, l in enumerate(L):
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
        # 🔴 `collage` ve title bang MUC DEN va KHONG co dai vang (k_collage goi head_line()
        #    thieu highlight=True) => chu chim tren anh SANG, va cung chim tren anh TOI.
        #    Duotone khong cuu duoc. => cho collage ve NEN PHANG (no rat dep o ban nen phang).
        #    ⚠️ Chua duoc >50% the vox: 15/18 = 83% van co anh that, X2 PASS.
        #    Sua dung tang la them highlight=True vao k_collage trong make_vox.py, nhung do la
        #    TOOL DUNG CHUNG (nenkin/kaigo/akiya) — khong tu sua.
        if kind != "collage":
            v["bg"] = "photo"
            v["photo"] = P(sub)
            # DUOTONE cho kind ve kicker/title TRAN tren anh (timeline/source)
            v["photo_style"] = "duotone:ink" if kind in ("timeline", "source") else "darken"
        flow.append(f"{STYLE_MACRO}. {VOXSUBJ[sub]}")
        names.append(f"ai_clean/{sub}.jpeg")
        out.append({"match": m, "photo": False, "video": True, "vox": v})
    else:
        idxe = len(out)
        st = (STYLE_MACRO if i in MACRO
              else STYLE_SEPIA if i in SEPIA
              else STYLE_TONE if i in OFF_HOUSE else STYLE)
        flow.append(f"{st}. {SUBJ.get(i) or dflt(i)}")
        rel = f"slides_img/slide_{idxe:02d}.jpg"
        names.append(rel)
        out.append({"match": m, "photo": False, "video": True, "shot": shot_spec(i, rel)})

# anh "SAU" cua wipe KHONG nam trong vong lap -> xuat rieng (pipeline muc 4.3)
for rel, prompt in WIPE_SUBJ.items():
    flow.append(prompt)
    names.append(rel)

S_DIR = PROJ / "03_SCRIPTS"
(S_DIR / f"{SLUG}_SLIDES.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(S_DIR / f"{SLUG}_IMG_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
(S_DIR / f"{SLUG}_IMG_NAMES.txt").write_text(
    "\n".join(f"{n+1:3d}  {p}" for n, p in enumerate(names)) + "\n", encoding="utf-8")

nv = [x["vox"]["kind"] for x in out if isinstance(x.get("vox"), dict)]
modes = [x["shot"]["mode"] for x in out if isinstance(x.get("shot"), dict)]
print(f"entry {len(out)} | vox {len(nv)} | shot {len(modes)}")
print(f"doi hinh/phut {len(out)/(DUR/60):.1f} (tran 6) | giay/entry {DUR/len(out):.1f} (san 6)")
print(f"prompt {len(flow)} dong (gom {len(WIPE_SUBJ)} anh SAU cua wipe)")
print(f"match TRUNG/THIEU: {bad if bad else '0 - tat ca duy nhat'}")
print("vox kinds:", ", ".join(f"{k}x{nv.count(k)}" for k in sorted(set(nv))))
print("shot modes:", ", ".join(f"{k}x{modes.count(k)}" for k in sorted(set(modes))))
