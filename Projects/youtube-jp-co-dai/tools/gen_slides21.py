# -*- coding: utf-8 -*-
r"""Sinh 21_furo-no-kabi-modoru_SLIDES.json + bo prompt anh (FLOW/NAMES).

LOP HINH = MOT DEM TRONG MOT PHONG TAM (khong phai 80 anh minh hoa roi rac).

  NEO LAP LAI (phai xuat hien dung nhu nhau moi lan):
    - GOM CAO SU (packing) co vet den : entry 0 -> giua bai -> sau khi xu ly 50 do
    - DONG HO trong phong tam         : 22h -> 23h -> 2h -> sang (truc thoi gian)
    - 3 CHAI THUOC TAY duoi bon rua   : mo bai (tu trao) -> dong bai
    - CAY GAT NUOC (wiper)            : nam im o dau bai -> thanh nhan vat o phut 19
    - CUA PHONG TAM HE MO             : me -> cau cuoi

  4 HOI theo dong ho:
    I   22:00  hoi nuoc + 9 tieng + phep thu so tuong
    II  23:00  quat hut / cua so / nap bon (short circuit)
    III 02:00  tran nha -> giot nuoc roi xuong
    IV  sang   gom cao su: mau != chet -> 50 do 90 giay -> thu tu
    V   dong tien -> quay lai 22:00 (1 phut) -> hinox/sunoko/sento -> me

Hai rang buoc ky thuat giu nguyen tu gen_slides19/20.py:
  1) moi `match` PHAI la substring DUY NHAT cua mot dong _TTS.md — sai la render gay
  2) cue chon bang luat >=58 ky/slide => ~4 doi hinh/phut (audience-45plus.md §2)
"""
import re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "21_furo-no-kabi-modoru"
VD = f"E:/Claude/Projects/youtube-jp-co-dai/06_VIDEO/{SLUG}"
DUR = 1278          # 6.498 ky / 305 ky-phut ~ 21,3 phut

L = [re.sub(r"\[[^\]]*\]", "", l).strip()
     for l in (PROJ / "03_SCRIPTS" / f"{SLUG}_TTS.md").read_text(encoding="utf-8").split("\n")]
L = [l for l in L if l and not l.startswith(("#", "TARGET_QUERY", "INTENT"))]


def P(n):
    return f"{VD}/ai_clean/{n}.jpeg"


def idx(frag):
    """Chi so dong chua `frag` — bat buoc DUY NHAT, sai la dung ngay."""
    hit = [i for i, l in enumerate(L) if frag in l]
    if len(hit) != 1:
        raise SystemExit(f"NEO KHONG DUY NHAT ({len(hit)}): {frag}")
    return hit[0]


# ══ THE VOX — moi the la mot NUT cua cau chuyen ═════════════════════════════
VOXSPEC = [
 ("そこから朝まで、9時間",
  ("stat", {"kicker": "電気を消してから", "big": "9", "unit": "時間",
            "sub": "壁が濡れたまま越す夜",
            "note": "カビは生えたのではなく、乾かなかっただけ"}, "wet_bathroom_wall_night")),

 ("手を入れられる時刻は",
  ("timeline", {"kicker": "順番でしか効かない", "title": "一晩に、手は四回",
                "marks": [["22時", "1分"], ["23時", "フタ"], ["2時", "天井"], ["朝", "熱"]],
                "note": "前でしくじると、あとは効きません"}, "bathroom_wall_clock_night")),

 ("換気扇は、空気を送り込む機械ではありません",
  ("flow", {"kicker": "窓を開けると", "head": "入口と出口が近いと、近道になる",
            "pins": [[1560, 235, "窓＝入口"], [1180, 610, "床は乾かない"]],
            "arrows": [[1500, 320, 1180, 545, 0.20]]}, "bathroom_extractor_fan")),

 ("フタを、すきまなく閉めてください",
  ("compare", {"kicker": "11時の一手", "title": "スイッチではなく、フタ",
               "left": {"label": "フタが半分", "mark": "x", "verdict": "一晩じゅう湯気"},
               "right": {"label": "すきまなく", "mark": "o", "verdict": "湯気が止まる"}},
   "bathtub_lid_half_open")),

 ("落ちた先が天井です",
  ("room", {"preset": "mix", "kicker": "真夜中の2時",
            "head": "天井で水滴が育ち、真下へ落ちてくる"}, "bathroom_ceiling_from_below")),

 ("カビ取り剤で真っ白にしたのに",
  ("compare", {"kicker": "10日でまた同じ形", "title": "白い、は、死んだ、ではない",
               "left": {"label": "色素だけ抜けた", "mark": "x", "verdict": "菌糸は生きている"},
               "right": {"label": "熱が奥まで届く", "mark": "o", "verdict": "そこで初めて死ぬ"}},
   "black_mould_on_rubber_packing")),

 ("表面のカビは、50度のお湯を5秒かければ死にます",
  ("stat", {"kicker": "薬ではなく", "big": "50", "unit": "度",
            "sub": "表面は5秒、ゴムの奥は90秒",
            "note": "樹脂の内側まで熱が通るのを待つ時間"}, "shower_head_hot_water")),

 ("先に、50度で始末してください",
  ("process", {"kicker": "順番を逆にしない", "title": "熱が先、色は翌日",
               "steps": [{"label": "50度を90秒あてる", "sub": "同じ場所に、ゆっくり"},
                         {"label": "給湯器を40度に戻す", "sub": "次に入る人のため"},
                         {"label": "翌日に漂白剤で色を抜く", "sub": "逆にすると生き残る",
                          "hot": True}]}, "bathroom_thermometer_in_basin")),

 ("乾燥に強い一部のカビでも",
  ("stat", {"kicker": "素材が濡れている時間", "big": "0.65", "unit": "",
            "sub": "水分活性、これを下回ると伸びられない",
            "note": "湿度の話ではありません"}, "water_droplet_on_tile")),

 ("まず、冷たいシャワーを、壁に一周かけてください",
  ("process", {"kicker": "夜10時の1分", "title": "9時間を20分に変える",
               "steps": [{"label": "冷たい水を壁に一周", "sub": "壁の温度を下げる"},
                         {"label": "皮脂と石けんかすを流す", "sub": "カビの食べ物"},
                         {"label": "ワイパーで上から下へ一度", "sub": "水の膜をはがす",
                          "hot": True}]}, "squeegee_on_bathroom_wall")),

 ("文部科学省がまとめたカビ対策の資料では",
  ("source", {"kicker": "出典", "org": "文部科学省 カビ対策マニュアル",
              "asof": "カビ相談センター 高鳥浩介氏／2016年6月15日 NHK",
              "quote": "よく育つのは25〜28度。50度で細胞はこわれはじめる",
              "number": "90秒",
              "note": "ゴムの奥まで熱が通るのを待つ時間"}, "official_document_on_desk")),

 ("すのこという道具も、同じ考えでできています",
  ("title", {"title": "乾かす技術",
             "sub": "道具の中ではなく、暮らしの段取りの中にありました"},
   "wooden_sunoko_slats")),
]

VOX = {}
for frag, spec in VOXSPEC:
    VOX[idx(frag)] = spec

# ══ ANH THE VOX (bat buoc MACRO — media-library.md §2.11) ═══════════════════
VOXSUBJ = {
 "wet_bathroom_wall_night": "a bathroom wall surface still beaded with water at night, droplets catching a dim light",
 "bathroom_wall_clock_night": "a simple round wall clock in a dim bathroom, hands near ten, steam haze in the air",
 "bathroom_extractor_fan": "a square ceiling extractor fan grille in a bathroom, seen from below, dust-free",
 "bathtub_lid_half_open": "a folding bathtub lid pushed halfway across a full tub, steam rising from the open gap",
 "bathroom_ceiling_from_below": "a plain bathroom ceiling panel photographed straight from below, faint condensation film",
 "black_mould_on_rubber_packing": "extreme macro of black spots embedded in white rubber sealant along a bathroom joint",
 "shower_head_hot_water": "a shower head with hot water streaming out, steam curling, macro",
 "bathroom_thermometer_in_basin": "a simple cooking thermometer standing in a basin of hot water, dial visible but numbers unreadable",
 "water_droplet_on_tile": "a single water droplet clinging to a smooth tile surface, extreme macro, backlit",
 "squeegee_on_bathroom_wall": "a rubber squeegee blade pressed against a wet bathroom wall, water sheeting off below it",
 "official_document_on_desk": "a plain stapled paper document lying on a desk under a lamp, text blurred and unreadable",
 "wooden_sunoko_slats": "a wooden slatted bath mat resting on a tiled floor, gaps between the slats, macro",
}

# ══ ANH THUONG — theo tung dong (chi so ENTRY duoc tinh sau) ════════════════
# Neo lap lai duoc dat lai dung tu ngu de model ve ra CUNG mot vat.
PACK = "white rubber sealant strip along a bathroom joint with black spots embedded in it"
BOTTLES = "three refill pouches of bathroom mould cleaner standing under a washbasin cabinet"
WIPER = "a rubber squeegee hanging on a hook in a bathroom"
DOOR = "a bathroom door left slightly ajar, warm hallway light beyond"

SUBJ = {}


def S(frag, text):
    SUBJ[idx(frag)] = text


# ── HOI I · 22:00 ──────────────────────────────────────────────────────────
S("風呂の電気を消して戸を閉めた", f"extreme macro of {PACK}")           # entry 0 = CHU THE
S("壁はまだ濡れていました", "a dark bathroom just after the light was switched off, wet wall faintly lit from the doorway")
S("数百円の一本で", "a single bathroom mould cleaner spray bottle standing on a tiled floor")
S("今夜、電気を消す前に、壁を手のひらでひとなでして", "an open palm pressed flat against a wet bathroom wall")
S("指先が濡れたら", "wet fingertips held up close, droplets on the skin, macro")
S("そこだけに黒い点が出て", "a bathroom corner where smooth tile meets rubber sealant, mould only on the rubber")
S("先に一つだけ。あの黒い点を始末する", f"extreme macro of {PACK}, lit hard from one side")
S("いちばん効くのは、夜10時の、たった1分", WIPER)
S("何度のお湯を何秒あてるのか", "a shower head resting in its holder, water not yet running")

# ── tu trao + me ───────────────────────────────────────────────────────────
S("白状しますと、私の家の風呂も", "a dim bathroom in an ordinary Japanese home, nothing special, evening")
S("洗面台の下に、カビ取り剤の詰め替えが3本", BOTTLES)
S("使い切る前に、次を買っていた", "a shopping basket holding one more bathroom cleaner refill pouch")
S("実家の母は、お客さんが来る前の日", DOOR)
S("子どもの私は、寒いのに何をしているのだろう", "a cold hallway with a bathroom door standing wide open, winter light")
S("母は、それだけ言って、また台所へ戻って", "an empty kitchen doorway seen from a hallway, someone just left the frame")
S("あの一言の意味が分かるまで", "an old family bathroom, tiles from decades ago, quiet")

# ── HOI I tiep · 22:00 ────────────────────────────────────────────────────
S("では、夜の10時に戻ります", "a bathroom full of steam right after use, mirror fogged")
S("このとき浴室は、温度がおよそ35度", "steam curling in the air of a warm bathroom, backlit")
S("窓を閉めた押し入れではありません", "a warm humid bathroom with every surface glistening")
S("そして壁も、床も、天井も", "water film covering a bathroom floor, reflecting the ceiling light")
S("カビにとって、これ以上の場所は", "extreme macro of a wet grout line, water sitting in the seam")
S("ここで、多くのご家庭が最初の一手", "a finger pressing the extractor fan switch on a bathroom wall panel")
S("理由を、先に一つだけ申し上げます", "a bathroom ceiling at night, one fat droplet hanging from it")
S("拭いたはずの壁が朝また", "a bathroom wall in morning light, faint damp patches remaining")
S("それを知らずに聞くと", WIPER)

# ── HOI II · 23:00 ────────────────────────────────────────────────────────
S("夜11時。あなたはもう、居間にいます", "a lit living room at night seen from a dark hallway, bathroom door closed")
S("つまり、10時の一手は打ってある", "an extractor fan running in a dark bathroom, faint motion blur on the blades")
S("まず一つ、うかがいます。窓は", "a small frosted bathroom window pushed open at night")
S("吸い出した分だけ", "air movement suggested by steam drifting toward a ceiling vent")
S("このとき、入口の窓が", "a bathroom window and a ceiling fan close together on the same wall")
S("入った空気は、部屋を一周してくれる", "steam drifting in a straight line from window to ceiling vent")
S("換気の分野では、これをショートサーキット", "a floor corner of a bathroom still wet while the fan runs above")
S("機械は回しています。音もしています", "an electricity meter dial turning, dim utility corner")
S("それなのに、床の隅も", "the wet lower half of a bathroom wall, tide line of dampness")
S("正しいやり方は、拍子抜けするほど地味です", "a hand pushing a frosted bathroom window firmly shut")
S("そして、浴室のドアも閉めて", "a bathroom door being pulled closed from inside")
S("ドアの下のほうに、細い羽根の並んだ", "the louvred vent slats at the bottom of a bathroom door, macro")
S("ガラリのないドアなら", "a bathroom door left open a hand's width, gap measured by fingers")
S("こうして初めて、空気は入口から", "steam drifting in a long curve across a bathroom before reaching the vent")
S("ところが、ここまでやっても乾かない", "a full bathtub of water sitting in a dark bathroom")
S("湯船に、お湯を張ったままに", "a bathtub filled to the brim, surface perfectly still")
S("洗濯に使うため", "a washing machine hose lying over the edge of a full bathtub")
S("ところが、40度の湯を200リットル", "heavy steam rising from an uncovered bathtub in a dark room")
S("換気扇一台が、その相手をする", "a ceiling extractor fan seen through drifting steam")
S("ここで申し上げたいのは、残り湯を", "a hand pulling a folding bathtub lid across the water")
S("半分だけ載せてある", "a bathtub lid covering only half the tub, steam escaping from the gap")
S("11時の一手は、スイッチではありません", "a fully closed bathtub lid, no steam anywhere, dark bathroom")

# ── HOI III · 02:00 ───────────────────────────────────────────────────────
S("ここまでで、湯気の出どころは止まりました", "a quiet dark bathroom, tub covered, window shut, nothing moving")
S("ところが、それでも真夜中に", "a bathroom at 2am, only a night light, air still")
S("今度の水は、湯船から出てきません", "condensation forming on a cold ceiling surface, macro")
S("真夜中の2時。家の中で、いちばん気温が下がる", "a wall thermometer in a dark bathroom showing a low reading")
S("ここで一度、浴室の天井を", "a plain bathroom ceiling seen from directly below, dim")
S("浴室のカビの本体は、壁でも床でもありません", "faint grey mould film spreading across a bathroom ceiling panel")
S("昼のあいだに舞い上がった胞子は", "dust motes drifting in a shaft of bathroom light")
S("落ちた先が天井です", "the underside of a bathroom ceiling, slightly rough surface, damp sheen")
S("気温が下がる2時ごろ", "a single droplet swelling on a ceiling surface, about to fall, macro")
S("育った水滴は、真下に落ちます", "a droplet caught mid-fall against a dark bathroom background")
S("眠っているあいだ、浴室の中だけ", "a bathroom floor at night with fresh droplet marks on it")
S("つまり天井は、浴室のいちばん高いところで", "a wide view of a bathroom ceiling, the highest surface in the room")
S("壁だけを何度も磨きなおしても", "a scrubbing sponge and a cleaned wall panel, still one dark spot remaining")
S("掃除の腕の問題ではありません", "a cleaning brush resting on the edge of a bathtub, unused")
S("天井の拭き方は、床用のワイパーを", "a floor wiper with a dry towel wrapped around its head")
S("乾いたタオルをワイパーの先に巻いて", "a towel-wrapped wiper held up against a bathroom ceiling")
S("水滴を落としてから", "a cloth being wiped across a ceiling panel, streak of moisture behind it")
S("ここで、ひとつだけ、してはいけない", "a spray bottle held pointing upward, warning framing, no text")
S("カビ取り剤を、天井にスプレーしないで", "fine spray mist drifting down through the air of a bathroom")
S("霧が真上から降ってきて", "a person's shoulder and a bathroom ceiling above, mist falling, no face")
S("天井は、拭く場所です", "a towel-wrapped wiper resting against a bathroom wall after use")
S("同じ理由で、もう1か所だけ", "the underside of a shampoo bottle lifted off a shelf, water ring beneath it")
S("置きっぱなしの底には水がたまり", "a wet ring of water left on a bathroom shelf, macro")
S("週に一度、底を持ち上げて", "a hand tipping a shampoo bottle to drain water from its base")

# ── HOI IV · sang ─────────────────────────────────────────────────────────
S("ところが、天井を拭いても、窓を閉めても", "a bathroom in morning light, clean except one dark line of sealant")
S("それでも消えない黒い点が", f"extreme macro of {PACK}, morning light")
S("ここだけは、乾かしても消えません", "a close view of rubber sealant with dark spots deep inside the material")
S("朝です。ゴムパッキンの、あの黒い点", "a bathroom joint seen in flat morning light, black spots along the rubber")
S("カビ取り剤で真っ白にしたのに", "a bleached white sealant strip looking perfectly clean, macro")
S("あれは、生き返ったのではありません", "the same sealant strip with faint grey shadows returning inside the rubber")
S("黒カビの黒は、メラニンに近い色素です", "extreme macro of dark pigment sunk into a porous white material")
S("菌が死んでも、この色素は残ります", "a whitened patch of sealant beside an untreated dark patch")
S("つまり、白くなったかどうかは", "a white sealant strip photographed flatly, ambiguous and plain")
S("私たちは、目に見える色を", "a cleaning cloth and a bleached bathroom joint, looking finished")
S("ゴムパッキンやコーキングは、やわらかい樹脂", "extreme macro of the porous surface of rubber sealant, tiny pits visible")
S("指先でなでるとつるりとしていますが", "a fingertip running along a rubber sealant strip, macro")
S("カビは、そのすき間に菌糸という", "microscopic-looking fine threads suggested inside a translucent material, macro")
S("根が張る、と言いますが", "a cross-section-like view of a rubber strip, dark threads running inward")
S("スプレーの液は、垂れて、乾いて", "liquid running down a vertical rubber joint and pooling below")
S("胞子から目に見える大きさに育つまで", "a tiny dark speck on white sealant, barely visible, macro")
S("では、糸の先まで届くものは", "steam rising from hot water in a bathroom, nothing else in frame")
S("答えは、薬ではありませんでした。熱です", "hot water streaming from a shower head, heavy steam")
S("私たちが、ちょうど心地よいと感じる温度", "a warm bathroom with gentle steam, comfortable and ordinary")
S("そして50度を超えたあたりから", "very hot water hitting a tiled surface, dense steam")
S("表面のカビは、50度のお湯を5秒", "a shower stream held steadily against one spot of a wall joint")
S("ゴムパッキンの奥まで熱を通すには", "a shower stream held on a single point, steam building around it")
S("この90秒は、長くかけるための", "a wall clock second hand, close up, dim bathroom light")
S("やり方は、これだけです。給湯器の温度表示", "a water heater control panel on a kitchen wall, digits blurred")
S("シャワーヘッドは近づけすぎない", "a shower head held a hand's distance from a wall joint")
S("黒い点の上から下へ", "a shower stream running slowly down a line of sealant")
S("終わったら、給湯器の設定を40度前後に戻して", "a finger pressing a button on a water heater control panel")
S("お使いの給湯器が50度まで上げられない", "a basin of steaming water on a bathroom floor")
S("そのときは、洗面器に熱めの湯を", "a cooking thermometer standing in a basin of hot water")
S("50度を指したら、その湯を", "hot water being poured slowly from a small basin onto a wall joint")
S("50度の湯は、肌にふれれば", "steam rising from very hot water, warning mood, no people")
S("浴室に誰もいない状態で", "an empty bathroom with the door closed, seen from outside")
S("小さなお子さんや、お年寄りが入る前には", "a water heater panel showing a lowered setting, hand withdrawing")
S("ここで、正直に申し上げておきます", "a bathroom joint still dark after treatment, honest and plain")
S("お湯をかけても、黒い色は消えません", "a dark sealant strip photographed unchanged, matter-of-fact")
S("試したけれど効きません", "a person's hand lowering a shower head, disappointment implied, no face")
S("死んでいるのに、黒いまま", "a dark but dead-looking sealant strip, dry and matte")
S("だから、順番があります", "a shower head and a bleach bottle placed side by side on a bathroom floor")
S("先に、50度で始末してください", "hot water hitting a sealant joint, steam rising")
S("翌日に、漂白剤で色を抜いてください", "a bleach gel bottle standing beside a clean white joint the next morning")
S("逆にすると、白い表面の下に", "a white sealant strip with faint grey shadow returning beneath the surface")
S("洗面台の下にたまっていた私の3本は", BOTTLES)

# ── HOI V · dong tien -> 22:00 -> lich su -> me ───────────────────────────
S("ところで、なぜ、こんな単純な順番が", "an empty supermarket aisle shelf, cleaning products out of focus")
S("売り物になるのは、目に見える結果です", "a spotless white bathroom joint photographed like an advertisement")
S("真っ白になったタイルは、写真になります", "a gleaming clean bathroom, bright and staged")
S("では、乾いた壁は、写真になるでしょうか", "a plain dry bathroom wall, nothing to see, flat light")
S("何も起きていないように見えるので", "an ordinary dry bathroom, unremarkable, quiet")
S("カビ取り剤の棚を思い出して", "a long shelf of mould cleaner bottles in a store, labels unreadable")
S("一年じゅう並んでいられるのは", "a store shelf being restocked with cleaning bottles")
S("よく効く薬なら、そんなに何度も", "a half-used cleaning bottle standing alone on a bathroom floor")
S("どこかの会社を責める話ではありません", "a quiet store aisle at closing time, shelves neat")
S("ただ、広まる知恵と、広まらない知恵", "a dry bathroom wall beside a shelf of bottles, direct comparison")
S("そして、乾いた壁は、誰にも売れません", "a completely dry bathroom wall in morning light, matte and plain")
S("さあ、夜の10時に帰ります", "a bathroom at night again, steam still hanging, the same room as the opening")
S("いちばん効く一手は、この時刻に", WIPER)
S("そして、同じ1分でも、朝にやったのでは", "a bathroom wall in morning light, already dry but stained")
S("天井の水滴も、パッキンの中の菌糸も", f"extreme macro of {PACK}")
S("お風呂から上がる前の、最後の1分", "a cold shower stream running down a warm bathroom wall, steam collapsing")
S("それから、水切りのワイパーで", "a squeegee drawn from top to bottom of a bathroom wall, water sheeting off")
S("なぜ、わざわざ冷たい水をかける", "cold water hitting a warm tiled wall, steam vanishing on contact")
S("一つは、温まった壁の温度を下げる", "a wall surface cooling, condensation not forming, macro")
S("もう一つは、皮脂と石けんのかす", "soap scum residue on a wall being rinsed away by water")
S("そしてワイパーは、壁に張りついた", "a thin film of water being lifted off a wall by a rubber blade, macro")
S("カビが必要としているのは、部屋の湿度", "a dry bathroom wall with no droplets at all, matte finish")
S("素材の中の水分は、水分活性という", "a bone-dry tiled wall surface, extreme macro, no moisture")
S("壁が朝まで濡れているか", "a bathroom wall completely covered in water droplets, night light, macro")
S("冒頭でお約束した、いちばん効く一手は", WIPER)

S("ここで、母の話に帰ります", "an old wooden bathroom in a Japanese house, hinoki tub, evening light")
S("檜の風呂桶はカビない", "a hinoki wooden bath tub, grain visible, dry and pale")
S("ところが、そのヒノキチオール", "a slice of pale cypress wood on a dark surface, macro")
S("つまり、昔の風呂桶が保ったのは", "an upturned wooden bath bucket drying on a stone floor")
S("では、何だったのでしょうか", "an empty old bathroom with everything stood on end to dry")
S("湯を落とし、桶を伏せ", "wooden bath boards leaned upright against a wall to dry")
S("すのこという道具も", "a wooden slatted mat lifted to show the air gap beneath it")
S("木のフタも、置きっぱなしには", "a wooden bath lid standing on its edge against a wall")
S("銭湯の天井が、あんなに高いのも", "the very high ceiling of an old public bathhouse, steam rising far above")
S("男湯と女湯を分ける壁の上が", "the open gap above a dividing wall in an old bathhouse")
S("あれは掃除ではありません", "an old bathhouse interior, empty, quiet, steam drifting")
S("昔の人は、カビを殺す薬を", "an old Japanese bathroom with no bottles at all, only wood and stone")
S("持っていたのは、順番と、習慣です", "a wooden bucket, a stool and a slatted mat all standing upright to dry")
S("乾かすという技術は、道具の中には", "an old washing area, everything stored vertically, air flowing")
S("母が、お客さんの来る前の日に", DOOR)
S("違いました。あれは、9時間を", "a bathroom door propped wide open, cold clean air, winter afternoon")
S("母は、掃除の話をしていたのでは", "a quiet home bathroom seen from the hallway, door ajar, evening")

S("正直に申し上げれば、これで一生カビが", "a north-facing bathroom with no window, dim even at noon")
S("窓のない浴室、日の差さない", "an old apartment bathroom, aged tiles and worn sealant")
S("ゴムパッキンそのものが欠けていたり", "cracked and chipped rubber sealant along a bathroom joint, macro")
S("体調に不安のある方や", "an open bathroom window with fresh air coming in, calm")
S("それでも、今日いちばんお伝えしたかった", "a shelf of cleaning bottles beside a plain dry wall")
S("問題は、洗剤が弱かったこと", "a wet bathroom wall at night, droplets everywhere")
S("私たちは、汚れと戦う道具は", BOTTLES)
S("今夜、電気を消す前に、壁を手のひらでなでて", "an open palm on a bathroom wall, testing for moisture")
S("そして10日後、あの黒い点が", f"extreme macro of {PACK}, ten days later, unchanged and clean")
S("次にお話しするのは、同じ台所で", "a cast-iron frying pan hanging on a kitchen wall, evening light")

# ── mac dinh theo doan ─────────────────────────────────────────────────────
DEF = [(30, "a dim Japanese home bathroom at night, wet surfaces"),
       (60, "a bathroom extractor fan and a covered bathtub at night"),
       (95, "a bathroom ceiling and falling condensation droplets"),
       (135, "black mould on rubber sealant and hot water treatment"),
       (999, "an old wooden Japanese bathroom, everything stood up to dry")]


def dflt(i):
    for lim, s in DEF:
        if i < lim:
            return s
    return DEF[-1][1]


# ── TONG vs BOI CANH tach doi (bai hoc gen_slides20.py) ────────────────────
STYLE_TONE = ("Photorealistic cinematic documentary still, soft natural light, cool neutral "
              "palette, muted colors, shallow depth of field, fine detail, calm quiet mood, "
              "16:9 horizontal, no text, no letters, no logos, no brand labels, no human faces, "
              "no watermark")

STYLE = (STYLE_TONE.replace("documentary still, ",
         "documentary still from a single continuous night inside one ordinary Japanese unit "
         "bathroom: pale beige wall panels, white rubber sealant joints, a folding bathtub lid, "
         "one small frosted window, "))

# Slot NGOAI phong tam => dung TONE, khong keo continuity vao
OFF_ROOM = set()
for f in ("実家の母は、お客さんが来る前の日", "子どもの私は、寒いのに", "母は、それだけ言って",
          "使い切る前に、次を買っていた", "ところで、なぜ、こんな単純な順番が",
          "売り物になるのは、目に見える結果です", "真っ白になったタイルは",
          "カビ取り剤の棚を思い出して", "一年じゅう並んでいられるのは",
          "どこかの会社を責める話ではありません", "ただ、広まる知恵と、広まらない知恵",
          "やり方は、これだけです。給湯器の温度表示", "終わったら、給湯器の設定を40度前後に戻して",
          "小さなお子さんや、お年寄りが入る前には", "ここで、母の話に帰ります",
          "檜の風呂桶はカビない", "ところが、そのヒノキチオール", "つまり、昔の風呂桶が保ったのは",
          "では、何だったのでしょうか", "湯を落とし、桶を伏せ", "木のフタも、置きっぱなしには",
          "銭湯の天井が、あんなに高いのも", "男湯と女湯を分ける壁の上が", "あれは掃除ではありません",
          "昔の人は、カビを殺す薬を", "持っていたのは、順番と、習慣です",
          "乾かすという技術は、道具の中には", "母が、お客さんの来る前の日に",
          "違いました。あれは、9時間を", "母は、掃除の話をしていたのでは",
          "次にお話しするのは、同じ台所で"):
    OFF_ROOM.add(idx(f))

STYLE_MACRO = ("Photorealistic extreme close-up macro photograph, the subject FILLS THE FRAME "
               "and is the only thing visible, tight crop, plain dark out-of-focus background, "
               "NO room, NO wall, NO sky, NO tools in view unless named. Hard directional light, "
               "high micro-detail, muted cool palette, calm documentary mood, 16:9 horizontal, "
               "no text, no letters, no logos, no brand labels, no human faces, no watermark")

MACRO = set()
for f in ("風呂の電気を消して戸を閉めた", "指先が濡れたら", "先に一つだけ。あの黒い点を始末する",
          "カビにとって、これ以上の場所は", "ドアの下のほうに、細い羽根の並んだ",
          "今度の水は、湯船から出てきません", "気温が下がる2時ごろ", "育った水滴は、真下に落ちます",
          "同じ理由で、もう1か所だけ", "置きっぱなしの底には水がたまり",
          "それでも消えない黒い点が", "ここだけは、乾かしても消えません",
          "カビ取り剤で真っ白にしたのに", "あれは、生き返ったのではありません",
          "黒カビの黒は、メラニンに近い色素です", "菌が死んでも、この色素は残ります",
          "ゴムパッキンやコーキングは、やわらかい樹脂", "指先でなでるとつるりとしていますが",
          "カビは、そのすき間に菌糸という", "根が張る、と言いますが",
          "胞子から目に見える大きさに育つまで", "この90秒は、長くかけるための",
          "死んでいるのに、黒いまま", "逆にすると、白い表面の下に",
          "天井の水滴も、パッキンの中の菌糸も", "そしてワイパーは、壁に張りついた",
          "素材の中の水分は、水分活性という", "ところが、そのヒノキチオール",
          "ゴムパッキンそのものが欠けていたり", "そして10日後、あの黒い点が",
          "一つは、温まった壁の温度を下げる"):
    MACRO.add(idx(f))

# ── chon cue: >=58 ky/slide, ep cue o dong CTA ────────────────────────────

# ẢNH "SAU" của cặp wipe — phải là CÙNG khung, CÙNG góc, chỉ khác trạng thái
WIPE_PROMPT = {
 "wipe_wall_dry.jpg": "the same bathroom wall completely dry, no droplets at all, matte surface, night light, macro",
 "wipe_packing_clean.jpg": "the same white rubber sealant strip, clean and white, no black spots at all, macro",
 "wipe_packing_after10.jpg": "the same white rubber sealant strip ten days later, still clean, no black spots returning, macro",
}

FOCUS_LINES = ("そこだけに黒い点が出て", "落ちた先が天井です", "気温が下がる2時ごろ",
               "それでも消えない黒い点が", "同じ理由で、もう1か所だけ",
               "同じ報告に、答えがあります" if False else "壁だけを何度も磨きなおしても",
               "ドアの下のほうに、細い羽根の並んだ", "半分だけ載せてある")
# wipe: dong -> anh THU HAI (duong dan tuong doi trong slides_img/, dat sau khi co anh)
WIPE_LINES = {"カビ取り剤で真っ白にしたのに": "slides_img/wipe_packing_clean.jpg",
              "壁が朝まで濡れているか": "slides_img/wipe_wall_dry.jpg",
              "そして10日後、あの黒い点が": "slides_img/wipe_packing_after10.jpg"}


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
# 🔴 SKIP: cau thoai cua me xuat hien Y HET NHAU 2 lan (phut 2 + phut 19) — khong
#    substring nao tach duoc => cue dong LIEN TRUOC va giu nguyen hinh khi thoai vang len
#    (cung cach xu ly cua gen_slides20.py voi 「いま切らんと、秋に困るとよ。」)
SKIP = {i for i, l in enumerate(L) if l.startswith("「お客さんの来る家は")}
CUE, acc = [], 0
for i, l in enumerate(L):
    if i in SKIP:
        acc += len(l)
        continue
    if i == 0 or i in VOX or i in FORCE or acc >= 58:
        CUE.append(i)
        acc = 0
    acc += len(l)

# ── san 6 giay/entry (audience-45plus.md §2 muc 2) ────────────────────────
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
              else STYLE_TONE if i in OFF_ROOM else STYLE)
        flow.append(f"{st}. {SUBJ.get(i) or dflt(i)}")
        rel = f"slides_img/slide_{idxe:02d}.jpg"
        names.append(rel)
        out.append({"match": m, "photo": False, "video": True, "shot": shot_spec(i, rel)})

# ⭐ ảnh "sau" của wipe KHÔNG nằm trong vòng lặp entry (nó là ảnh thứ hai của một
#    entry đã có) → phải xuất riêng, nếu không user gen thiếu và wipe tự hạ về soft
for _sp in [x.get("shot") for x in out]:
    if _sp and _sp.get("mode") == "wipe":
        _n = _sp["photo2"].split("/")[-1]
        flow.append(f"{STYLE_MACRO}. {WIPE_PROMPT.get(_n, 'the same scene, after state')}")
        names.append(_sp["photo2"])

S_DIR = PROJ / "03_SCRIPTS"
(S_DIR / f"{SLUG}_SLIDES.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(S_DIR / f"{SLUG}_IMG_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
(S_DIR / f"{SLUG}_IMG_NAMES.txt").write_text(
    "\n".join(f"{n+1:3d}  {p}" for n, p in enumerate(names)) + "\n", encoding="utf-8")

nv = [x["vox"]["kind"] for x in out if isinstance(x.get("vox"), dict)]
npho = sum(1 for x in out if x.get("photo") is True)
print(f"entry {len(out)} | anh thuong {npho} | vox {len(nv)} (100% co anh nen)")
print(f"doi hinh/phut {len(out)/(DUR/60):.1f} (tran 6) | giay/entry {DUR/len(out):.1f} (san 6)")
print(f"prompt {len(flow)} dong | match TRUNG/THIEU: {bad if bad else '0 - tat ca duy nhat'}")
print("kinds:", ", ".join(sorted(set(nv))))
