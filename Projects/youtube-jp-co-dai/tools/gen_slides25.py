# -*- coding: utf-8 -*-
r"""Sinh 25_mizugame-suyaki-tarai_SLIDES.json + bo prompt anh (FLOW/NAMES).

LOP HINH = MOT CAI CHUM GOM (mizugame), tu bep ba den san nha.

  NEO LAP LAI (ve ra CUNG mot vat moi lan):
    - CHUM GOM 素焼き: kho rao (mo bai) -> dong giot nuoc (sau khi giai thich co che)
    - GIOT NUOC / do am dong tren be mat dat nung (phep thu co che)
    - CHAU HOA DIY: 2 chau long vao nhau, cat uot o giua
    - TARAI (chau go/kim loai) tren hien nha - vat thu hai
    - BA (khong bao gio co mat): tay gia, ao trang, no cuoi

  5 doan chinh:
    I   cold open: 100 nguoi chet vi nong, da so trong nha ban dem > ban ngay
        -> tu trao tu lanh nuoc am -> cham voi nuoc
    II  co che 素焼き: lo chan long -> ri nuoc -> boc hoi -> hut nhiet (khi hoa nhiet)
        -> DIY 2 chau hoa -> phan truc giac men bong KHONG mat
    III quoc te: Nigeria (Mohammed Bah Abba) 3 ngay -> 27 ngay, An Do/Trung Dong
        -> lich su Shigaraki/Tokoname, lu khach Edo, ky uc ba
    IV  NANG STAKE: 水がめ chi cuu con khat -> hanh dong khan cap = 行水盥/たらい
        -> lich su 行水 -> so cuu 熱中症 hien dai TRUNG mot nguyen ly
    V   dong tien: tu lanh pho cap 1957->1970, 三種の神器 -> ket 3 lop
"""
import re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "25_mizugame-suyaki-tarai"
VD = f"E:/Claude/Projects/youtube-jp-co-dai/06_VIDEO/{SLUG}"
DUR = 912          # 5.126 ky / 337,5 ky-phut ~ 15,2 phut (header .md)

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
 ("そのうち97人は、屋内で亡くなっています。夜間39人、日中33人",
  ("bar", {"kicker": "屋内で亡くなった97人", "title": "夜のほうが、多かった",
           "bars": [["夜間", 39], ["日中", 33]], "hot": 0,
           "source": "東京都監察医務院／東京新聞"}, "night_dark_room_no_ac")),

 ("素焼きの壁には、目に見えないほど小さな穴が、無数に空いています",
  ("process", {"kicker": "素焼きの甕の仕組み", "title": "小さな穴が、涼しさの正体",
               "steps": [{"label": "小さな穴が無数に空いている", "sub": "素焼き＝うわぐすりなし"},
                         {"label": "水が少しずつにじみ出る", "sub": "甕の外側の表面へ"},
                         {"label": "外側で蒸発、熱を奪う", "sub": "気化熱で内側が冷える", "hot": True}]},
   "unglazed_clay_wall_pores_macro")),

 ("食品メーカーが行った実験では、この方法で、まわりより2度から6度",
  ("stat", {"kicker": "食品メーカーの実験", "big": "2〜6", "unit": "度",
            "sub": "周囲の温度より水温が下がった", "note": "電気を一切使わずに",
            "source": "ニチレイ「エコ冷蔵庫」実験"}, "thermometer_in_clay_pot_water")),

 ("大きさの違う、素焼きの植木鉢を二つ、用意してください",
  ("process", {"kicker": "自宅でできる実験", "title": "今日から確かめられます",
               "steps": [{"label": "素焼きの植木鉢を二つ用意", "sub": "大きさ違いのもの"},
                         {"label": "小さいほうにボトルや果物", "sub": "冷やしたい物を入れる"},
                         {"label": "鉢のあいだに濡れた砂か布", "sub": "風通しのいい日陰へ", "hot": True}]},
   "two_terracotta_flowerpots_diy")),

 ("表面につやのある、美しい壺ほど、この冷たさは生まれません",
  ("compare", {"kicker": "見た目と涼しさ", "title": "美しい壺ほど、冷えない",
               "left": {"label": "素焼き（つやなし）", "mark": "o", "verdict": "穴が空いて冷える"},
               "right": {"label": "施釉（つやあり）", "mark": "x", "verdict": "穴がふさがり冷えない"}},
   "glazed_vs_unglazed_pottery_pair")),

 ("ところが、素焼きの壺を二重にして、湿った砂を挟んだだけで、なすは27日ももちました",
  ("compare", {"kicker": "ナイジェリアの教師・2001年", "title": "壺一つで、村が変わった",
               "left": {"label": "収穫から3日", "mark": "x", "verdict": "なすが傷む"},
               "right": {"label": "二重の壺＋湿った砂", "mark": "o", "verdict": "なすが27日もつ"},
               "source": "Mohammed Bah Abba／Rolex Award 2001"}, "nigerian_pot_in_pot_eggplants")),

 ("国の資料でも、首すじや、わきの下、太もものつけ根など、太い血管が皮膚の近くを通る場所を",
  ("source", {"kicker": "出典", "org": "環境省 熱中症環境保健マニュアル",
              "asof": "最新版",
              "quote": "首すじ・わきの下・太もものつけ根など、太い血管が皮膚の近くを通る場所を集中して冷やす",
              "number": "3か所",
              "note": "濡れタオル＋送風で水分を蒸発させる応急処置"}, "wet_towel_neck_cooling_firstaid")),

 ("1957年、電気冷蔵庫を持つ家庭は、100軒のうち、わずか3軒ほどでした",
  ("timeline", {"kicker": "電気冷蔵庫の普及率", "title": "わずか13年で、当たり前に",
                "marks": [["1957年", "3軒／100軒"], ["1970年", "89軒／100軒"]],
                "note": "「三種の神器」と呼ばれた時代", "source": "内閣府男女共同参画局"},
   "1950s_japanese_kitchen_new_fridge")),
]

VOX = {}
for frag, spec in VOXSPEC:
    VOX[idx(frag)] = spec

VOXSUBJ = {
 "night_dark_room_no_ac": "a dim Japanese room at night, moonlight through a window, no visible air conditioner unit, still humid air, quiet documentary mood",
 "unglazed_clay_wall_pores_macro": "extreme macro of the rough unglazed surface of terracotta clay, countless microscopic pores visible under raking light, dry matte texture",
 "thermometer_in_clay_pot_water": "a simple analog thermometer dipped into water inside an unglazed terracotta pot, macro, condensation beading on the outer clay",
 "two_terracotta_flowerpots_diy": "two unglazed terracotta flowerpots of different sizes nested together with wet sand between them, a drink bottle inside the smaller one, simple DIY setup on a wooden table",
 "glazed_vs_unglazed_pottery_pair": "two ceramic jars side by side, one with a smooth glossy glaze reflecting light, the other rough matte unglazed clay, studio still life, plain background",
 "nigerian_pot_in_pot_eggplants": "a rustic pot-in-pot cooling device made of two nested clay pots with damp sand between them, fresh eggplants and tomatoes stored inside, warm dry village light",
 "wet_towel_neck_cooling_firstaid": "a damp folded white towel held against the side of a neck, first-aid cooling technique, clinical but warm soft lighting, no face visible",
 "1950s_japanese_kitchen_new_fridge": "a nostalgic 1950s-60s Japanese kitchen with a brand new white refrigerator standing proudly beside an old terracotta water jar, warm sepia-tinted documentary light",
}

# ══ ANH THUONG ═════════════════════════════════════════════════════════════
JAR_DRY = "a large rough unglazed terracotta water jar sitting dry in a dim kitchen corner"
JAR_WET = "a large rough unglazed terracotta water jar covered in beads of condensation, warm afternoon light"
JAR_HAND = "an older woman's hand resting on the cool wet surface of a terracotta water jar, no face"
TARAI_SCENE = "a round wooden tarai washtub on a traditional Japanese engawa veranda, garden light, quiet"
KITCHEN_TAP = "a kitchen tap and a half-drunk glass of water on a pale counter, ordinary Japanese home"

SUBJ = {}


def S(frag, text):
    SUBJ[idx(frag)] = text


# ── I. COLD OPEN ─────────────────────────────────────────────────────────
S("ある夏、都内だけで、暑さがきっかけで", JAR_WET)  # entry 0 = chu the, dung media-library.md 2.0
S("亡くなった方の多くは、エアコンが備わっていない", "an air conditioner unit mounted on a wall, switched off, dim room")
S("今すぐ、水道の蛇口をひねって、手の甲に水をかけてみてください", KITCHEN_TAP)
S("古代の秘訣へようこそ。今日もまた", "an old terracotta water jar sitting quietly in a sunlit corner, establishing shot")
S("白状しますと、私も先週、真夏の台所で冷蔵庫を開けて", "a refrigerator door standing open in a dim kitchen, cold blue light spilling out, a plastic barley-tea bottle inside")
S("あなたの家には、暑い日、いつでもコップ一杯の冷たい水を", "a glass of water on a kitchen counter, condensation-free, ordinary daylight")
S("じつは、冷蔵庫は「冷やす道具」であって", "a refrigerator's digital display glowing faintly in a dark kitchen at night")
S("では、祖母の家の甕は、電気もないのに", JAR_DRY)
S("あの甕は、素焼きでした。うわぐすりを掛けていない", "extreme macro of the rough matte surface of an unglazed terracotta jar")

# ── II. CO CHE + DIY ─────────────────────────────────────────────────────
S("正直、最初は半信半疑でした。植木鉢に水をかけただけで", "a hand about to pour water over a small unglazed terracotta flowerpot on a wooden table")
S("大切なのは、風です。空気が動かなければ", "a light breeze moving a thin cloth wrapped loosely around a terracotta pot, outdoor daylight")
S("植木鉢は、ホームセンターで、大きいほうも小さいほうも", "a home-improvement store shelf lined with plain unglazed terracotta flowerpots, price tags blurred")
S("日本の中でも、湿気の少ない内陸の地域や", "a dry sunlit inland Japanese landscape, clear sky, low humidity feel")
S("じつは、この仕組みをいちばん本気で使いこなしているのは", "a dry arid landscape under strong sun, cracked earth, warm dusty light")
S("キャンプや停電のときにも、この仕組みは役に立ちます", "a small cooler box beside an unglazed clay pot with a bottle inside, outdoor camping setting")

# ── III. LICH SU + BA ────────────────────────────────────────────────────
S("信楽や常滑など、焼き物の産地では", "a traditional Japanese pottery workshop, unglazed clay jars and flowerpots drying on wooden shelves")
S("江戸時代、旅人や行商人も、素焼きの徳利や瓶に水を入れて", "an Edo-period traveler's back with a small unglazed clay water flask tied to a wicker basket, dusty road, sepia-warm tone")
S("祖母が生きていたころ、私は子どもで、直径30センチほどの", "a large old terracotta water jar in a traditional Japanese kitchen corner, a wooden ladle resting on its rim")
S("柄杓で水面を割ると、こん、と乾いた土の音がしました", "a wooden ladle dipping into a large terracotta water jar, ripples on the water surface, macro")
S("「井戸まで走らんでも、ここにあるやろ」祖母は、そう言って", "an older woman's hand resting on a terracotta jar's rim, warm kitchen light, no face, gentle")
S("白い割烹着の袖をまくり上げ、汗ばんだ額をぬぐいながら", "an older woman's hands in a white apron sleeve, wiping a brow with the back of a hand, no face, warm evening kitchen light")

# ── IV. NANG STAKE + TARAI ───────────────────────────────────────────────
S("けれど、水がめが救えるのは、喉の渇きだけです", JAR_HAND)
S("もし今、あなたの家族の誰かが、顔を真っ赤にして", "an empty chair in a warm dim room, a fallen fan on the floor beside it, urgent quiet mood")
S("そんなときのために、今の家からは消えてしまった", "an old wooden tarai washtub tucked in the corner of a traditional engawa veranda")
S("縁側や庭先に置かれていた、行水盥です", TARAI_SCENE)
S("じつは「行水」という言葉は、もともと仏教の言葉でした", "an old wooden temple ladle and a stone water basin, quiet Japanese temple courtyard")
S("じつは、扇風機で部屋の空気を冷やすより", "an electric fan spinning indoors beside a window, ordinary Japanese room")
S("汗ばんだ肌に、たらいの水をひとすくいかけてみてください", "a wooden ladle scooping water from a tarai washtub, droplets catching sunlight")
S("けれど、注意も一つ、お伝えしておきます", "a tarai washtub filled with lukewarm water in dappled afternoon shade")
S("じつは、この「肌を濡らして、風を当てる」という方法は", "a folded wet towel and a small electric fan on a table, first-aid setting, calm daylight")
S("じつは、昭和のころ、行水は、まだお風呂のない家がほとんどだった", "a Showa-era Japanese wooden house exterior, tarai washtub outside the door, nostalgic warm tone")
S("近所には、麦わら帽子をかぶったおじさんが、行水を終えて", "a straw hat resting on an engawa veranda railing at dusk, warm golden light, uchiwa fan beside it")
S("うちわの音と、蚊取り線香のにおいが、あの時間の記憶と", "a coiled mosquito incense burning faintly beside an uchiwa paper fan, warm dusk light, engawa veranda")
S("たらい一杯のぬるま湯だけで、家族の暑い一日が", "a calm engawa veranda at dusk, tarai washtub empty and quiet, warm fading light")

# ── V. DONG TIEN + KET ───────────────────────────────────────────────────
S("もう一つだけ、行水盥にまつわる話があります", TARAI_SCENE)
S("ここまでご覧いただき、ありがとうございます", JAR_WET)
S("ところが、ここでもう一つ、奇妙なことが起きました", "an old tarai washtub standing unused in a modern garden corner")
S("今の家にも、よく似た形の道具があります", "a bright plastic children's inflatable pool in a small modern Japanese garden, sunny day")
S("では、なぜ、あの便利な道具たちは、私たちの家から消えて", "an empty traditional Japanese kitchen corner, no jar, plain tile wall, quiet")
S("同じころ、水道も各家庭に届くようになりました", "an old kitchen tap fixture from the mid-20th century, plain and functional")
S("じつは、この道具たちが消えたことは、小さくない意味を", "a modern kitchen sink with a full glass of tap water, ordinary daylight")
S("保冷剤や、家庭用の冷房まわりの市場は、今も、年々広がり", "a store aisle stocked with cooling gel packs and portable fans, bright retail lighting")
S("しかも、ここ数年、電気代そのものが、じわじわと上がり続けて", "a household electricity meter dial, close but not too tight, plain wall")
S("じつは今も、信楽など焼き物の産地では、この素焼きの甕を", "a modern artisan pottery workshop shelf with newly made unglazed terracotta jars, warm studio light")
S("もちろん、甕もたらいも、冷蔵庫や冷房の代わりにはなりません", "a terracotta jar and a modern refrigerator standing side by side in a bright kitchen, both in soft focus")
S("さきほど、最後に置いておいた、あの確かめ方の答えです", KITCHEN_TAP)
S("それでも、台所の隅に、小さな素焼きの甕を一つ置いてみる", JAR_DRY)
S("大切なのは、どちらか一方を選ぶことではありません", "a terracotta jar and an electric fan both visible in one warm sunlit room, balanced composition")
S("お住まいのご実家には、こうした甕や、たらいの記憶が残って", "a quiet traditional Japanese engawa at golden hour, an old terracotta jar and a wooden tarai side by side")
S("古代の秘訣は、これからも暮らしの中に眠る宝を", JAR_WET)

DEF = [(6, KITCHEN_TAP),
       (14, JAR_DRY),
       (24, "a wooden table with an unglazed terracotta pot and a small bottle of water"),
       (36, TARAI_SCENE),
       (999, JAR_WET)]


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
         "documentary still from a single continuous story of one traditional Japanese home: "
         "a rough unglazed terracotta water jar in the kitchen, a wooden engawa veranda and "
         "garden with a tarai washtub, warm natural light, "))

OFF_KITCHEN = set()
for f in ("日本の中でも、湿気の少ない内陸の地域や", "じつは、この仕組みをいちばん本気で使いこなしているのは",
          "同じころ、水道も各家庭に届くようになりました",
          "じつは、この道具たちが消えたことは、小さくない意味を",
          "保冷剤や、家庭用の冷房まわりの市場は、今も、年々広がり",
          "しかも、ここ数年、電気代そのものが、じわじわと上がり続けて",
          "じつは「行水」という言葉は、もともと仏教の言葉でした"):
    OFF_KITCHEN.add(idx(f))

STYLE_MACRO = ("Photorealistic extreme close-up macro photograph, the subject FILLS THE FRAME "
               "and is the only thing visible, tight crop, plain dark out-of-focus background, "
               "NO room, NO wall, NO sky, NO tools in view unless named. Hard directional light, "
               "high micro-detail, muted warm palette, calm documentary mood, 16:9 horizontal, "
               "no text, no letters, no logos, no brand labels, no human faces, no watermark")

MACRO = set()
for f in ("あの甕は、素焼きでした。うわぐすりを掛けていない",
          "柄杓で水面を割ると、こん、と乾いた土の音がしました",
          "汗ばんだ肌に、たらいの水をひとすくいかけてみてください",
          "うちわの音と、蚊取り線香のにおいが、あの時間の記憶と"):
    MACRO.add(idx(f))

FOCUS_LINES = ("あの甕は、素焼きでした。うわぐすりを掛けていない",
               "「井戸まで走らんでも、ここにあるやろ」祖母は、そう言って",
               "うちわの音と、蚊取り線香のにおいが、あの時間の記憶と")
WIPE_LINES = {"けれど30分後、鉢に触れた指先が、ひんやりとしていました": "slides_img/wipe_pot_condensation.jpg",
              "たらい一杯のぬるま湯だけで、家族の暑い一日が": "slides_img/wipe_evening_calm.jpg"}


# ══ LỚP CHUYỂN ĐỘNG BẰNG HÌNH (make_shot.py) ═══════════════════════════════
SHOT_FOCUS = set()
for f in FOCUS_LINES:
    SHOT_FOCUS.add(idx(f))
SHOT_WIPE = {}
for f, second in WIPE_LINES.items():
    SHOT_WIPE[idx(f)] = second


_shot_n = [0]


def shot_spec(i, img_rel):
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

FORCE = {idx("ここまでご覧いただき、ありがとうございます")} | set(SHOT_WIPE)
SKIP = set()
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
