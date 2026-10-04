# -*- coding: utf-8 -*-
r"""_scenes20.py — SCENE PLAN ("slides") cho video 20 遺族年金・四分の三の誤解.

Import boi `gen_flow20.py` (sinh prompt anh + prompt i2v) va sau nay boi
`build_remotion_20.py`. Tach file de sua NOI DUNG khong dung co khi.

⭐ STYLE: **ANIME** (user chot 2026-09-03: *"toi muon phong cach anime nhe"*).
   Doi so voi video 19 (photoreal documentary) va 17/18 (paper collage).
   ⚖️ Compliance: anh ANIME **khong phai "realistic"** => KHONG phai tick
   altered/synthetic (`youtube-compliance.md` §2.1 chi bat canh AI realistic).
   Day la cai LOI mien phi cua viec doi sang anime — ghi ro de khoi quen.

📐 NEO: `L` = chi so dong khong-rong trong `03_SCRIPTS/20_..._TTS.md`
   (= chi so dong trong `timeline.json`). Scene chay tu L cua no toi L cua
   scene ke tiep; cac shot trong `shots` chia deu khoang do.

🔴 LUAT AP:
  · `audience-45plus.md` §2.0b — scene ANH doi hero moi <= 9,0s
    => so shot >= ceil(giay_scene / 9). Scene `stat`/`formula` DUOC MIEN.
  · `nenkin/CLAUDE.md` §② — VUNG GIUA CHO MOT THU: scene co `stat`/`formula`
    thi KHONG co anh hero.
  · `stage-zu-layout.md` §2 — bang >= 3 dong; dong `*` la dong duoc NHAN.
  · Moi con so duoi day deu co mat NGUYEN VAN trong kich ban — khong them
    mot con so nao moi (YMYL).
"""

# ══════════════════════════════════════════════════════════════════════════
# CAST — 7 nhan vat lap lai. Anime an CAST LOCK rat tot, nhung phai ta theo
# kieu "character design sheet": toc / mat / trang phuc co dinh.
# ══════════════════════════════════════════════════════════════════════════
CAST = {
    "W1": {"who": "佐藤さん 66 — case chinh, qua phu o Sendai, lam sieu thi", "lock": (
        "a Japanese woman of 66 with a kind oval face and soft round cheeks, warm "
        "hazel eyes with fine laugh lines, silver-white hair pinned back in a low "
        "neat bun with a few loose strands at the temples, small pearl stud "
        "earrings, wearing a muted grey-blue knitted cardigan over a cream blouse")},
    "M1": {"who": "亡くなったご主人 — chi trong hoi tuong / anh tho", "lock": (
        "a Japanese man in his late fifties with short neatly parted black hair "
        "greying at the temples, a calm narrow face and gentle down-turned eyes, "
        "wearing a plain charcoal salaryman suit with a navy tie")},
    "M3": {"who": "研究員 — nguoi dan 案内役 cua kenh", "lock": (
        "a composed Japanese man in his late sixties with neat full white hair "
        "combed back, thin silver-rimmed round glasses, calm unhurried eyes, "
        "wearing a soft charcoal cardigan over a pale blue shirt")},
    "W2": {"who": "高橋さん 65 — chi o 次回予告", "lock": (
        "a Japanese woman of 65 with short wavy grey hair tucked behind her ears "
        "and a slightly worried expression, wearing a warm mustard-yellow cardigan "
        "over a white collared blouse")},
    "S1": {"who": "年金事務所の窓口の職員 — nu, dau 30", "lock": (
        "a Japanese woman in her early thirties with black hair in a low ponytail "
        "and a calm polite expression, wearing a pale grey office blazer with a "
        "small plain name badge")},
    "K1": {"who": "遺族基礎年金 doan — me tre + 2 con nho", "lock": (
        "a Japanese mother in her late thirties with shoulder-length dark hair and "
        "tired gentle eyes, with two small children — a boy of about seven in a "
        "striped shirt and a girl of about four in a yellow dress")},
    "C1": {"who": "khoi CTA — vo chong gia dang xem video", "lock": (
        "an elderly Japanese couple in their seventies — the husband with thin "
        "white hair in a beige cardigan, the wife with short permed white hair in "
        "a soft lilac blouse — sitting comfortably together")},
}
HANDS = {
    "W1": ("the same 66-year-old woman's hands — slim, softly lined, a thin plain "
           "gold ring on the left hand, grey-blue knitted cardigan cuff"),
    "M3": "the same elderly man's hands, thin and steady, charcoal cardigan cuff",
    "K1": "the same young mother's hands, small and unadorned, plain cotton sleeve",
    "W2": ("the same 65-year-old woman's hands, slightly plump with short clean "
           "nails, a mustard-yellow knitted cuff"),
}

# ══════════════════════════════════════════════════════════════════════════
# PROP LOCK — vat / boi canh lap lai. Cung mot vat o nhieu shot phai cung hinh.
# ══════════════════════════════════════════════════════════════════════════
PROP = {
    "P_TSUCHI": ("the SAME notice every time: a single pale-cream A4 sheet folded "
                 "once, with faint ruled rows and small boxes of illegible printed "
                 "squiggles and one thin navy header band across the top"),
    "P_ENV":    ("the SAME envelope every time: a plain white official window "
                 "envelope with a thin navy border line and no readable writing"),
    "P_FURI":   ("the SAME notification every time: a wide pale-cream slip with a "
                 "ruled table of small illegible figures and one pale blue column "
                 "band down the left side"),
    "P_KITCHEN": ("the SAME kitchen every time: a small tidy Japanese kitchen-diner "
                  "with a pale wood table, two chairs, a cream teapot and one cup, "
                  "a low window with a white lace curtain and a potted plant on "
                  "the sill"),
    "P_HOUSE":  ("the SAME house model every time: a simple warm-toned two-storey "
                 "Japanese house drawn from the side like a neat picture-book "
                 "cutaway — a wide solid ground floor and a smaller upper floor "
                 "with a pale tiled roof, standing alone on a plain background"),
    "P_BUTSU":  ("the SAME memorial corner every time: a small dark-wood family "
                 "altar shelf with a framed portrait photograph of the late "
                 "husband, one white chrysanthemum in a slim vase and a small "
                 "brass bell"),
    "P_MADO":   ("the SAME pension office every time: a pale wood-veneer counter, "
                 "blank sign boards above it, one grey moulded chair, soft "
                 "institutional lighting and a low queue-rope stand"),
    "P_SUPER":  ("the SAME supermarket every time: a bright vegetable aisle with "
                 "wooden crates of daikon, cabbage and tomatoes, pale green blank "
                 "price cards and overhead strip lights"),
    "P_TEIKI":  ("the SAME pension statement every time: a folded pale-blue "
                 "postcard-style leaflet with faint ruled boxes of illegible "
                 "small print"),
    "P_COIN":   ("the SAME props every time: neat stacks of plain brass-coloured "
                 "coins on a pale wooden surface"),
    "P_CAL":    ("the SAME calendar every time: an ordinary cream wall-calendar "
                 "page with a seven-column grid of small date numbers, a thin navy "
                 "border, and one date ringed in red pen"),
    "P_DESK":   ("the SAME study every time: a warm wooden desk under a window, a "
                 "brass-shaded desk lamp, a stack of plain government leaflets, a "
                 "dark fountain pen and an open ruled notebook"),
    "P_LIVING": ("the SAME living room every time: a low beige fabric sofa, a small "
                 "dark-wood table, a pale ceramic teapot with two cups and a "
                 "tablet lying flat"),
    "P_STAIR":  ("the SAME staircase every time: a clean pale-stone flight of steps "
                 "rising steadily against an open sky, drawn plain and "
                 "diagram-like, with one single step that drops DOWN instead of up"),
    "P_SCHOOL": ("the SAME school things every time: a navy Japanese high-school "
                 "blazer on a hanger and a worn leather school satchel"),
    "P_SCALE":  ("the SAME balance every time: a simple brass two-pan balance scale "
                 "on a pale wooden surface"),
}

# ══════════════════════════════════════════════════════════════════════════
# SCENES — `L` = dong bat dau.  kind: art | stat | formula | genten
#   art     -> shots[] : moi shot = 1 anh + 1 clip
#   stat    -> bang so (>=3 dong; dong mo dau bang `*` la dong duoc NHAN)
#   formula -> mot phep tinh (hang sau `=` tu nhan)
#   genten  -> screenshot THAT, KHONG gen AI (phai doc duoc)
# lv: peak | mid | calm  ·  cam: static|parallax|push|push_hard|pull_out
# ══════════════════════════════════════════════════════════════════════════
SCENES = [

# ─────────────────────── COLD OPEN (L0–L13) ────────────────────────────────
dict(L=0, tag="届いたお知らせ", kind="art", shots=[
  dict(key="todoku", cast=None, props=["P_ENV"], cam="push", lv="mid",
       # L0 六十五歳の誕生月に、年金額のお知らせが届きます。
       sc="the entrance hall of a quiet Japanese house in the morning, seen from "
          "inside: a single white official envelope has just dropped through the "
          "door slot and lies alone on the polished wooden floor, one slipper by "
          "the step, soft daylight through the frosted glass door",
       mo="the envelope finishes falling and settles flat on the floor with a small "
          "bounce, then goes still; the morning light through the frosted glass "
          "brightens very slowly; a curtain edge stirs once at the side of frame"),
  dict(key="hiraku", cast="W1", props=["P_KITCHEN", "P_TSUCHI"], cam="push", lv="mid",
       # L1 ご主人を早くに亡くされた女性が、その紙を開いて、目を疑いました。
       sc="a Japanese woman of 66 sitting alone at her kitchen table in the morning, "
          "unfolding a single official notice with both hands, her reading glasses "
          "pushed up on her head, a cup of tea going cold beside her, a man's "
          "folded reading glasses left on the shelf behind her, seen from the "
          "front at chest height",
       mo="she opens the folded notice fully with both hands and lays it flat on "
          "the table, then leans in slightly over it; her shoulders lower; the "
          "steam from the cup beside her drifts slowly upward"),
  dict(key="meutagau", cast="W1", props=["P_TSUCHI"], cam="push_hard", lv="peak",
       # L2 年金が、増えるどころか、減っていたんです。
       sc="a close portrait of the same 66-year-old woman looking down at the notice "
          "in her hands, her eyes wide and unblinking, her mouth slightly open in "
          "disbelief, the paper edge catching the window light in the lower frame, "
          "the kitchen soft and out of focus behind her",
       mo="her eyes widen a fraction more and her brows draw together; she blinks "
          "once, slowly, and her hands tighten on the edges of the paper so it "
          "bends a little; nothing else in the room moves"),
]),

dict(L=3, tag="年に六十三万円", kind="stat",
     # L3 年に、六十三万円。月にすると、五万三千円ほど。
     stat=[("減った分", "年 63万円"),
           ("ひと月あたり", "5万3千円"),
           ("*それが起きたのが", "65歳の誕生月")]),

dict(L=4, tag="始まる歳なのに", kind="art", shots=[
  dict(key="hazu", cast="W1", props=["P_KITCHEN", "P_CAL", "P_TSUCHI"], cam="static", lv="mid",
       # L4 六十五歳は、年金が始まる歳です。それなのに、減る。
       sc="the same woman standing at her kitchen wall looking up at a cream wall "
          "calendar with one date ringed in red pen, the official notice hanging "
          "loosely from her other hand at her side, her expression puzzled rather "
          "than upset, morning light across the wall",
       mo="she looks up from the notice to the ringed date on the calendar and "
          "holds there; the hand holding the paper lowers a few centimetres to her "
          "side; the light on the wall shifts very slowly"),
]),

dict(L=5, tag="いつか必ず来ます", kind="art", shots=[
  dict(key="anata", cast=None, props=["P_LIVING", "P_ENV"], cam="push_hard", lv="peak",
       # L5 あなたが遺族年金を受け取っていらっしゃるなら、この段差は、いつか必ず来ます。
       sc="an empty ordinary Japanese living room at dusk with nobody in it, one "
          "white official envelope lying unopened in the middle of the low table, "
          "two cups set out but only one used, the television dark, the last "
          "daylight coming in low through the window",
       mo="the low evening light slides slowly across the table and reaches the "
          "unopened envelope, lifting it out of shadow; the sheer curtain breathes "
          "once at the window; nobody enters"),
]),

dict(L=6, tag="対象は、お勤めだったかた", kind="art", shots=[
  dict(key="taishou", cast="M1", props=[], cam="parallax", lv="calm",
       # L6 対象は、ご主人が会社にお勤めだったかた。…いま受け取っているかたも同じです。
       sc="a warm memory-toned scene at a house entrance years earlier: a Japanese "
          "man in his late fifties in a charcoal salaryman suit stepping out of the "
          "door with a briefcase, half turned back to say goodbye, the morning "
          "street bright behind him, the colours slightly faded like an old "
          "photograph",
       mo="he takes one step down out of the doorway and turns his head back over "
          "his shoulder for a moment, then faces forward again; the bright street "
          "light behind him blooms a little; his tie sways once"),
  dict(key="taishou_b", cast="W1", props=["P_ENV"], cam="static", lv="calm",
       # L6後半 これから受け取るかただけでなく、いま受け取っているかたも同じです。
       sc="the present day at the very same house entrance, the colours now normal "
          "and clear: the 66-year-old woman stands alone in the open doorway "
          "holding a white official envelope in both hands, looking out at the "
          "empty morning street where he used to walk away",
       mo="she looks out down the empty street and then down at the envelope in her "
          "hands; her thumb moves once across its edge; the morning light on the "
          "street steadies"),
]),

dict(L=7, tag="なぜ、減るのか", kind="art", shots=[
  dict(key="naze", cast="W1", props=["P_KITCHEN", "P_TSUCHI"], cam="static", lv="mid",
       # L7 なぜ、減るのか。それは今日、はっきりお話しします。
       sc="the same woman seated at the kitchen table with the notice laid flat in "
          "front of her, her chin resting on her linked hands, eyes lowered on the "
          "paper, thinking hard, the room quiet and softly lit, seen slightly from "
          "the side",
       mo="she tilts her head slowly to one side over the paper and her linked "
          "hands shift under her chin; her gaze travels once from the top of the "
          "sheet to the bottom and settles"),
  dict(key="omoichigai", cast=None, props=["P_KITCHEN", "P_TSUCHI"], cam="push", lv="mid",
       # L8 ただ、その前に。もっと大きな思い違いが、ひとつあります。
       sc="an overhead view of the kitchen table: the official notice lies flat with "
          "a pencil and a small ruled notebook beside it, and on the notebook page "
          "a simple hand-drawn shape has been sketched wrongly and crossed out with "
          "two pencil strokes, no readable writing anywhere",
       mo="a pencil is drawn slowly across the sketched shape leaving a second "
          "crossing-out stroke, then lifts away and rests on the table; the "
          "notebook page settles flat"),
]),

dict(L=9, tag="四分の三", kind="art", shots=[
  dict(key="yonbunno3", cast=None, hands="W1", props=[], cam="static", lv="mid",
       # L9 夫の年金の、四分の三。よく聞く言葉ですね。
       sc="a close overhead shot of a plain round rice cake on a pale ceramic plate "
          "cut into four equal wedges, three of the wedges already slid together to "
          "one side and the fourth left apart, an elderly woman's hands resting at "
          "the edge of the plate",
       mo="the woman's fingers slide the three wedges a little closer together into "
          "one group and withdraw; the single separated wedge stays exactly where "
          "it is; the plate does not move"),
  dict(key="nanno", cast=None, props=["P_HOUSE"], cam="push", lv="mid",
       # L10 この四分の三は、いったい、何の四分の三なのでしょうか。
       sc="the simple two-storey Japanese house drawn alone against a plain soft "
          "background, and hovering in front of it one large hand-drawn "
          "question-mark shape rendered as a plain paper cutout, no other markings",
       mo="the paper question-mark shape drifts down a few centimetres in front of "
          "the house and settles, turning very slightly; the house stays perfectly "
          "still; the light behind it warms a little"),
  dict(key="keisan", cast="W1", props=["P_KITCHEN"], cam="static", lv="calm",
       # L11 ここを取り違えたまま老後の計算をされているかたが、とても多いんです。
       sc="the same woman at the kitchen table at night under a single warm lamp, "
          "working through household figures with a small calculator and an open "
          "ruled notebook, her glasses on now, absorbed and calm",
       mo="her finger presses two keys on the calculator in turn, then she writes "
          "one short mark in the notebook and pauses with the pen resting on the "
          "page; the lamplight is steady"),
]),

dict(L=12, tag="まず、事実から", kind="art", shots=[
  dict(key="kenkyu", cast="M3", props=["P_DESK"], cam="push", lv="calm",
       # L12 まず、事実から。/ L13 年金と老後のお金研究室です。…原典を画面で開きながら
       sc="a calm Japanese man in his late sixties in a charcoal cardigan sitting at "
          "a warm wooden study desk under a window, turning a laptop screen toward "
          "the viewer, a stack of plain government leaflets and an open notebook "
          "beside him, the screen glow pale and its contents not readable",
       mo="he turns the laptop a little further toward the viewer with one hand, "
          "settles it, then rests both hands on the desk edge and looks up; the "
          "desk lamp glow steadies"),
  dict(key="kenkyu_b", cast=None, hands="M3", props=["P_DESK"], cam="push", lv="calm",
       # L13 日本年金機構の原典を画面で開きながら、一緒に確かめていきます。
       sc="a close over-the-shoulder view of the laptop on the study desk showing a "
          "plain pale official web page of ruled rows and unreadable small text, an "
          "elderly man's finger tracing along one row of it, the desk lamp warm at "
          "the edge of frame",
       mo="his fingertip travels slowly along one row of the page from left to "
          "right and stops at the end of it, resting there; the screen glow holds "
          "steady"),
]),

# ───────────────── 第1章 二階建て (L14–L25) ────────────────────────────────
dict(L=14, tag="年金は二階建て", kind="art", shots=[
  dict(key="nikaidate", cast=None, props=["P_HOUSE"], cam="pull_out", lv="mid",
       # L14 日本の年金は、二階建てだと言われます。
       sc="the simple warm-toned two-storey Japanese house standing alone in the "
          "centre of a plain pale background, drawn flat from the side like a clean "
          "picture-book diagram, both floors evenly lit, nothing else in frame",
       mo="the camera eases back a little and the house settles into the centre of "
          "frame; the light across both floors comes up evenly and steadies; "
          "nothing about the house changes shape"),
  dict(key="ikkai", cast=None, props=["P_HOUSE"], cam="static", lv="mid",
       # L15 一階が、老齢基礎年金。二十歳から六十歳まで納めた期間で決まる部分です。
       sc="the same two-storey house, but now only the wide GROUND floor is warmly "
          "lit from within while the upper floor sits in soft shadow; a row of tiny "
          "identical coin shapes runs along the ground in front of the house like a "
          "long steady line",
       mo="the warm light inside the ground floor rises to full and holds while the "
          "upper floor stays dim; the row of small coins in front brightens one "
          "after another from left to right and stops"),
  dict(key="nikai", cast=None, props=["P_HOUSE"], cam="static", lv="mid",
       # L16 二階が、老齢厚生年金。会社にお勤めだったかたが、給料に応じて上乗せされる部分。
       sc="the same house, now with only the UPPER floor warmly lit while the ground "
          "floor sits in soft shadow, and a small stack of coins resting on the "
          "upper floor's balcony ledge",
       mo="the light inside the upper floor rises to full while the ground floor "
          "stays dim, and two more coins settle gently onto the balcony stack, "
          "which sinks a fraction under them"),
  dict(key="awaseta", cast="M1", props=["P_HOUSE"], cam="parallax", lv="calm",
       # L17 ご主人が受け取っていた年金は、この一階と二階を足したものでした。
       sc="the two-storey house fully lit on both floors, and standing small in "
          "front of it the Japanese man in his charcoal suit with his back half "
          "turned, looking up at the house, warm even light",
       mo="both floors hold their full warm light while the man tilts his head "
          "slowly upward to take in the upper floor; his shoulders lower on a quiet "
          "breath"),
]),

dict(L=18, tag="どちらでしょうか", kind="art", shots=[
  dict(key="dochira", cast=None, hands="W1", props=["P_HOUSE"], cam="push", lv="mid",
       # L18 では、亡くなったあと、遺族厚生年金として四分の三になるのは、どちらでしょうか。
       sc="the two-storey house now standing empty and unlit, with an elderly "
          "woman's hand entering from the side and hovering uncertainly in the gap "
          "between the ground floor and the upper floor, not touching either",
       mo="the hovering hand drifts slowly up toward the upper floor, hesitates, "
          "drifts back down toward the ground floor and stops in between, still not "
          "touching; the house stays unlit"),
]),

dict(L=19, tag="原典①・遺族厚生年金", kind="genten",
     # L19 こちらが、日本年金機構のページです。赤で囲んだところを、ご覧ください。
     # L20 亡くなられたかたの老齢厚生年金の、報酬比例部分の、四分の三。
     # ✅ URL + cau trich DA VERIFY 2026-09-03 (WebFetch). Trang nay cho ca 3
     #    trich dan cua bai: 4分の3 · 中高齢寡婦加算 635,500円/40-65歳/20年 · 65歳の支給停止.
     genten=dict(url="https://www.nenkin.go.jp/service/jukyu/seido/izokunenkin/"
                     "jukyu-yoken/20150424.html",
                 quote="遺族厚生年金の年金額は、死亡した方の老齢厚生年金の"
                       "報酬比例部分の4分の3の額となります。",
                 mark="muc「遺族厚生年金の年金額」— khoanh DO dung cau tren",
                 shots=3)),

dict(L=21, tag="つまり、二階だけ", kind="art", shots=[
  dict(key="nikai_dake", cast=None, props=["P_HOUSE"], cam="push_hard", lv="peak",
       # L21 報酬比例部分。つまり、二階だけです。
       sc="the two-storey house with ONLY the upper floor lifted clear of the "
          "building and floating a short way above it, brightly lit and separated, "
          "while the ground floor below stays dark and untouched, plain background",
       mo="the upper floor rises a few more centimetres clear of the house in one "
          "smooth movement and stops, holding steady in the air and brightening; "
          "the dark ground floor below does not move at all"),
  dict(key="ikkai_hairanai", cast=None, props=["P_HOUSE"], cam="static", lv="mid",
       # L22 一階の老齢基礎年金は、この計算に、入っていません。
       sc="the same separated view: the floating upper floor bright at the top of "
          "frame, and the ground floor below drained of all colour to a flat pale "
          "grey with a plain paper cutout of a diagonal line laid across it",
       mo="the colour drains a little further out of the ground floor until it is "
          "flat grey, and the paper diagonal across it settles into place; the "
          "floating upper floor above keeps its warm light"),
]),

dict(L=23, tag="ゼロになります", kind="art", shots=[
  dict(key="gokai_shin", cast="M3", props=["P_DESK", "P_HOUSE"], cam="static", lv="mid",
       # L23 ここが誤解の芯にあたる部分です。ご主人の一階部分は、四分の三になるのではありません。
       sc="the researcher in the charcoal cardigan standing beside a small model of "
          "the two-storey house on his desk, one hand open toward the grey ground "
          "floor, his expression serious and level as he explains",
       mo="his open hand moves slowly down through the air to indicate the grey "
          "ground floor and holds there; he gives one small nod; the model on the "
          "desk does not move"),
  dict(key="zero", cast=None, props=["P_HOUSE"], cam="push_hard", lv="peak",
       # L24 ゼロになります。
       sc="the two-storey house with the ground floor GONE — only the upper floor "
          "remains, resting on empty air above a bare flat foundation slab, the "
          "space where the ground floor stood completely empty, cold even light",
       mo="the last of the light drains out of the empty space beneath the upper "
          "floor and the bare foundation slab is left flat and plain; a faint dust "
          "settles onto it; nothing else moves"),
  dict(key="hikitsugarenai", cast=None, props=["P_BUTSU"], cam="parallax", lv="calm",
       # L25 ご主人が亡くなられた時点で、そのかたの老齢基礎年金は、そこで終わります。
       sc="a quiet corner of a Japanese home: a small dark-wood memorial shelf with "
          "a framed portrait photograph of the late husband, one white "
          "chrysanthemum in a slim vase and a small brass bell, soft afternoon "
          "light from the side, nobody in frame",
       mo="the afternoon light moves slowly across the framed portrait and the "
          "chrysanthemum leans a fraction in a draught; a thin thread of incense "
          "smoke rises and bends"),
]),

# ───────────────── 第2章 佐藤さんの数字 (L26–L40) ─────────────────────────
dict(L=26, tag="仙台の佐藤さん", kind="art", shots=[
  dict(key="sato", cast="W1", props=["P_KITCHEN"], cam="parallax", lv="calm",
       # L26 数字で見たほうが早いですね。仙台の佐藤さん、六十六歳。
       sc="a calm half-body portrait of the 66-year-old woman standing in her tidy "
          "kitchen-diner by the low window, hands folded in front of her, a small "
          "gentle smile, warm afternoon light, the room lived-in and neat",
       mo="she draws a slow breath and her shoulders rise and settle; she turns her "
          "head a few degrees toward the window light and holds; the lace curtain "
          "moves once behind her"),
  dict(key="sato_boutou", cast="W1", props=["P_KITCHEN", "P_TSUCHI"], cam="push", lv="mid",
       # L27 冒頭で、六十五歳の通知を開いて目を疑った女性。あれが、佐藤さんです。
       sc="the exact same framing as the opening scene — the same woman at the same "
          "kitchen table holding the same official notice — but now seen calmly "
          "from a little further back, the cup beside her freshly filled and "
          "steaming again",
       mo="she lowers the notice flat to the table and rests one hand on top of it, "
          "then looks up and away toward the window; fresh steam rises from the cup"),
  dict(key="furikomi", cast=None, hands="W1", props=["P_KITCHEN", "P_FURI"], cam="push", lv="mid",
       # L28 今日は、佐藤さんが毎年受け取っている、年金振込通知書を見ながら進めます。
       sc="a close overhead shot of the elderly woman's hands smoothing a wide "
          "pale-cream pension transfer notification flat on the kitchen table, its "
          "ruled table of small illegible figures catching the light, her reading "
          "glasses folded beside it",
       mo="both hands smooth the slip outward from the centre to flatten its fold "
          "creases, then one fingertip comes to rest on the left-hand column and "
          "stays there"),
]),

dict(L=29, tag="仮に置いてみます", kind="stat",
     # L29 二階の報酬比例部分が、年に百万円。一階の基礎年金が、年に八十万円。
     # L30 合わせて、年に百八十万円。月にすると、十五万円ほどですね。
     stat=[("二階・報酬比例部分", "年 100万円"),
           ("一階・老齢基礎年金", "年 80万円"),
           ("*合わせて", "年 180万円（月15万円）")]),

dict(L=31, tag="百八十万の四分の三", kind="formula",
     # L31 この百八十万円の四分の三は、いくらでしょうか。
     # L32 百三十五万円です。月に、十一万二千五百円。/ L33 多くのかたが、この数字を思い浮かべます。
     formula="180万円 × 3/4 ＝ 135万円"),

dict(L=34, tag="実際に計算されるのは", kind="formula",
     # L34 実際に計算されるのは、二階の百万円だけ。
     # L35 その四分の三で、七十五万円。月にすると、六万二千五百円です。
     formula="100万円 × 3/4 ＝ 75万円"),

dict(L=36, tag="差は、年に六十万円", kind="formula", peak=True,
     # L36 差は、年に六十万円。/ L37 十年で、六百万円になります。
     formula=["135万円 − 75万円 ＝ 60万円", "60万円 × 10年 ＝ 600万円"]),

dict(L=38, tag="ご自身の分は、別", kind="art", shots=[
  dict(key="jibun_kiso", cast=None, hands="W1", props=["P_FURI"], cam="push", lv="mid",
       # L38 佐藤さんご自身の老齢基礎年金は、別に受け取れます。…なくなりません。
       sc="a close shot of the pension transfer notification on the table with the "
          "woman's fingertip resting on a SECOND, separate row lower down the ruled "
          "table, clearly apart from the first row, warm lamp light from the side",
       mo="her fingertip slides down from the upper row and comes to rest firmly on "
          "the lower separate row and stays; her other hand steadies the corner of "
          "the slip"),
  dict(key="mangaku", cast=None, props=["P_COIN"], cam="static", lv="mid",
       # L39 令和八年度の満額で、年に八十四万七千三百円。
       sc="a clean close shot on a pale wooden table of one full neat stack of "
          "brass-coloured coins standing by itself, evenly lit, plain soft "
          "background, nothing else in frame",
       mo="two more coins are set gently on top of the stack one after the other "
          "and the stack settles square and still; the light steadies on the brass"),
  dict(key="chigau", cast="W1", props=["P_KITCHEN"], cam="parallax", lv="calm",
       # L40 生活が成り立たなくなる、という話ではないんです。ただ、思っていた額とは違う。
       sc="the same woman at her kitchen table with the paperwork now pushed to one "
          "side, holding her teacup in both hands, her expression settled and a "
          "little rueful rather than frightened, soft afternoon light",
       mo="she lifts the cup slowly to just below her chin, breathes out over it "
          "and lowers it back to the table; her eyes drift once to the pushed-aside "
          "papers and back"),
  dict(key="chigau_b", cast=None, hands="W1", props=["P_KITCHEN"], cam="push", lv="mid",
       # L40後半 そこは、先に知っておいたほうがいい。
       sc="a close shot of the elderly woman's hands writing one short figure into a "
          "small ruled household notebook on the kitchen table, the old pencilled "
          "figure above it neatly crossed out with a single line, warm afternoon "
          "light",
       mo="her pen finishes the short figure and lifts away, and her other hand "
          "smooths the notebook page flat beside it; the pen comes to rest along "
          "the spine of the book"),
]),

# ───────────────── 第3章 遺族基礎年金 (L41–L51) ───────────────────────────
dict(L=41, tag="お子さんが小さいうちに", kind="art", shots=[
  dict(key="kodomo", cast="K1", props=[], cam="parallax", lv="calm",
       # L41 お子さんが小さいうちに、ご主人を亡くされたかた。/ L42 遺族基礎年金です。
       sc="a young Japanese mother in her late thirties at a low table in a modest "
          "living room with her two small children, a boy of about seven and a girl "
          "of about four, all three quiet together over an evening meal, a framed "
          "photograph of a man on the shelf behind them, warm lamp light",
       mo="the little girl leans against her mother's arm and the mother's hand "
          "comes up to rest on the child's head; the boy sets down his bowl; the "
          "lamp light is steady"),
  dict(key="izoku_kiso", cast=None, props=["P_HOUSE"], cam="push", lv="mid",
       # L43 お子さんがいらっしゃる配偶者か、お子さんご本人だけが対象になります。
       sc="the two-storey house with the upper floor still missing, but the GROUND "
          "floor lit up warm again from inside, and two small child-sized paper "
          "silhouette figures standing in its doorway",
       mo="warm light rises inside the ground floor until it is fully lit and "
          "holds, and the two small paper figures in the doorway settle a fraction "
          "closer together; the empty space above stays dark"),
  dict(key="izoku_kiso_b", cast=None, hands="K1", props=["P_COIN"], cam="static", lv="mid",
       # L43後半 令和八年度で、年に八十四万七千三百円。
       sc="a close shot on a pale wooden table of a young mother's hands setting one "
          "neat stack of brass-coloured coins down in front of two small "
          "child-sized paper silhouette figures standing on the table, plain soft "
          "background",
       mo="the hands lower the coin stack the last centimetre onto the table in "
          "front of the two small figures and withdraw; the stack settles square "
          "and the figures stay still"),
]),

dict(L=44, tag="子の加算", kind="stat",
     # L44 ひとり目とふたり目が、それぞれ年に二十四万三千八百円。三人目からは、八万千三百円。
     stat=[("遺族基礎年金", "年 84万7300円"),
           ("子 1人目・2人目", "各 24万3800円"),
           ("*3人目から", "8万1300円")]),

dict(L=45, tag="お子さん、という言葉", kind="art", shots=[
  dict(key="jyuhassai", cast=None, props=["P_CAL", "P_SCHOOL"], cam="push", lv="mid",
       # L45 十八歳になった年度の、三月三十一日まで。障害のあるお子さんなら、二十歳未満まで。
       sc="a cream wall calendar page hanging beside a navy Japanese high-school "
          "blazer on a hanger, with the very last date square of the grid ringed "
          "firmly in red pen, plain wall, cool clear daylight",
       mo="the red pen ring on the final date square is completed with one more "
          "steady stroke and the pen withdraws out of frame; the blazer on the "
          "hanger swings very slightly and settles"),
  dict(key="sotsugyou", cast="K1", props=["P_SCHOOL"], cam="parallax", lv="calm",
       # L46 お子さんが高校を卒業される年の春に、この一階部分は終わります。家計が変わる。
       sc="a spring graduation day outside a Japanese school gate under cherry "
          "blossom, the now grown son in his school blazer walking ahead with his "
          "certificate tube while his mother watches him from a few steps back, "
          "proud and a little uncertain, petals in the air",
       mo="the son walks two steps further away from her and she stays where she "
          "is, her hands closing together in front of her; cherry petals drift down "
          "slowly across the frame"),
  dict(key="kakei_kawaru", cast="K1", props=[], cam="static", lv="mid",
       # L46後半 そこで、家計が変わるかたが、多いんです。
       sc="the mother alone at her low table that evening after the graduation, an "
          "open ruled household account book in front of her and a calculator "
          "beside it, her son's certificate tube standing against the wall, her "
          "expression quiet and thoughtful, lamp light",
       mo="she turns one page of the account book, looks down the column and rests "
          "her fingertips on the page; her other hand moves toward the calculator "
          "and stops just short of it"),
]),

dict(L=47, tag="受け取れる条件", kind="art", shots=[
  dict(key="seikei", cast=None, props=["P_KITCHEN"], cam="static", lv="calm",
       # L47 受け取れるかどうかを分ける条件 / L48 生計を同じくしていたこと。
       sc="a quiet kitchen table laid for two people who lived together — two rice "
          "bowls, two pairs of chopsticks on their rests and one shared teapot "
          "between them, morning light across the wood, nobody in frame",
       mo="steam rises steadily from the teapot spout and drifts toward the second "
          "empty place; the light across the table warms very slowly"),
  dict(key="happyakugojuu", cast=None, hands="W1", props=["P_DESK"], cam="push", lv="mid",
       # L48後半–L49 ご自身の年収が、原則として八百五十万円未満であること。…下回る見込み
       sc="a close desk shot: an elderly woman's hands holding a plain income "
          "statement sheet with faint ruled rows, and lying across it a flat pale "
          "wooden ruler set as a clear horizontal threshold line partway down the "
          "page, warm lamp light",
       mo="the wooden ruler is slid a little way down the page to a new line and "
          "pressed flat there, and the hand holding it stays; the paper beneath "
          "flattens under the pressure"),
  dict(key="mikomi", cast=None, props=["P_DESK"], cam="static", lv="mid",
       # L49 八百五十万円を超えていても、数年のうちに下回る見込みがあるかたは、対象になる場合があります。
       sc="a clean picture-book diagram on a plain pale background: one flat pale "
          "wooden ruler lies as a horizontal threshold line, and a simple warm "
          "coloured line descends step by step from above it and crosses below the "
          "ruler at the right-hand side of frame",
       mo="the descending coloured line draws itself down step by step from the "
          "left and passes below the ruler line near the right edge, then stops; "
          "the ruler itself does not move at all"),
]),

dict(L=50, tag="受け取る順番", kind="art", shots=[
  dict(key="junban", cast=None, props=[], cam="pull_out", lv="mid",
       # L50 お子さんのいる配偶者が最初。次に、お子さん。そのあとに…父母、孫、祖父母
       sc="a clean picture-book diagram on a plain pale background: a single-file "
          "row of six simple paper-cutout family silhouettes queueing from left to "
          "right — a parent holding a child's hand, then a child, then a lone "
          "adult, then an older couple, then a small child, then two elderly "
          "figures — each one slightly smaller than the last",
       mo="the whole row shuffles forward one short step together and settles, the "
          "front figure arriving at a marked spot on the ground and stopping; the "
          "gaps between them even out"),
  dict(key="junban_b", cast=None, props=[], cam="push", lv="mid",
       # L50後半 お子さんのいる配偶者が最初。次に、お子さん。
       sc="a closer view of the front of the same paper-cutout queue: the parent "
          "figure holding a child's hand stands warmly lit on a marked spot at the "
          "front, with the lone child figure waiting one step behind, the rest of "
          "the row falling away softly out of focus",
       mo="the parent-and-child figure settles onto the marked spot and its warm "
          "light comes up; the lone child figure behind takes half a step closer "
          "and stops"),
  dict(key="saki_no_juni", cast=None, props=[], cam="static", lv="mid",
       # L51 先の順位のかたがいらっしゃると、あとの順位のかたには回りません。
       sc="the same queue of six paper silhouettes, but now the front figure is "
          "warmly lit and holding a small envelope, while every figure behind it "
          "has faded to flat pale grey and stands with empty hands",
       mo="the front figure's warm light rises and its envelope lifts slightly, "
          "while the colour drains further from the grey figures behind until they "
          "are flat; none of them move forward"),
]),

# ───────────────── CTA (L52) ──────────────────────────────────────────────
dict(L=52, tag="ひとつだけ、お願いです", kind="art", shots=[
  dict(key="cta", cast="C1", props=["P_LIVING"], cam="parallax", lv="calm",
       # L52 高評価と…シェアで、この研究室を応援していただけると嬉しいです。
       sc="an elderly Japanese couple in their seventies sitting close together on "
          "a beige sofa in a warm living room, watching a tablet propped on the low "
          "table in front of them, teacups beside it, both relaxed and smiling "
          "gently, evening lamp light",
       mo="the husband leans in a little toward the tablet and the wife nods twice "
          "slowly; her hand comes to rest on his forearm; the lamplight is warm and "
          "steady"),
  dict(key="cta_b", cast="C1", props=["P_LIVING"], cam="static", lv="calm",
       # L52 (dong 162 ky ~27s => can 3 shot cho san 9s)
       sc="a closer view of the same elderly couple on the sofa, the wife now "
          "holding the tablet up between them with both hands while the husband "
          "points at something on its screen, both of them smiling, the screen glow "
          "soft on their faces",
       mo="the wife tilts the tablet a few degrees toward the husband and he taps "
          "the air near the screen once with a fingertip, then lowers his hand; "
          "both settle back into the sofa"),
  dict(key="cta_c", cast=None, props=["P_LIVING"], cam="push", lv="calm",
       # L52 (phan cuoi: ご感想・コメント)
       sc="a close shot of the low living-room table: the tablet lying flat with a "
          "soft pale glow, two teacups beside it, a small notepad and a pen placed "
          "ready next to them, warm evening lamplight, nobody in frame",
       mo="the pale glow of the tablet screen brightens gently and steadies; a wisp "
          "of steam lifts from one teacup and drifts sideways; the pen rocks once "
          "on the notepad and stills"),
  dict(key="cta_d", cast="C1", props=["P_LIVING"], cam="static", lv="calm",
       # L52末 皆さまの声が、次の研究テーマになります。それでは、続きを見ていきましょう。
       sc="a warm close shot of the elderly husband raising a gentle thumbs-up "
          "toward the glowing tablet on the low table while his wife beside him "
          "laughs softly with a hand at her cheek, both of them at ease, evening "
          "lamp light",
       mo="his thumb comes up into a steady thumbs-up and holds there while she "
          "turns her face toward him and her shoulders lift once with a quiet "
          "laugh; the tablet glow stays even"),
]),

# ───────────────── 第4章 六十五歳の段差 (L53–L68) ─────────────────────────
dict(L=53, tag="六十五歳の段差", kind="art", shots=[
  dict(key="dansa", cast="W1", props=["P_STAIR"], cam="pull_out", lv="mid",
       # L53 もうひとつの話をします。六十五歳の段差です。
       sc="a clean diagram-like scene against an open pale sky: a flight of plain "
          "pale-stone steps rising steadily from the left, and at the top one "
          "single step that drops DOWN instead of continuing up; the 66-year-old "
          "woman stands at the edge of that dropped step looking at it",
       mo="the camera eases back to reveal the whole flight and the one dropped "
          "step; the woman shifts her weight back half a pace from the edge and "
          "holds; her cardigan hem moves once in the open air"),
  dict(key="dansa_b", cast="W1", props=["P_STAIR"], cam="push", lv="mid",
       # L54 佐藤さんは、六十五歳になった年に、年金が減りました。
       sc="a closer view of the same woman standing on the dropped step itself, now "
          "one level lower than the flight behind her, looking back up at the step "
          "she came down from, the open pale sky around her",
       mo="she looks back and up at the higher step behind her and her hand comes "
          "halfway toward its edge, then lowers again without touching it; her "
          "shoulders settle"),
]),

dict(L=55, tag="窓口まで行きました", kind="art", shots=[
  dict(key="madoguchi", cast="W1", props=["P_MADO"], cam="parallax", lv="mid",
       # L55 「通帳を持って窓口まで行きました」
       sc="the 66-year-old woman standing at a pale wood-veneer pension office "
          "counter holding a small navy bank passbook and her folded notice against "
          "her chest, a row of blank sign boards above the counter, soft "
          "institutional light, one grey chair behind her",
       mo="she steps up to the counter and sets the passbook and the folded notice "
          "down flat on the counter top with both hands, then draws her hands back "
          "and clasps them in front of her"),
  dict(key="kotae", cast="S1", props=["P_MADO"], cam="static", lv="mid",
       # L56 窓口の答えは、こうでした。手続きの漏れではありません、と。
       sc="the counter seen from the customer's side: a calm office worker in her "
          "early thirties in a pale grey blazer behind the counter, one hand open "
          "over the papers between them, explaining patiently, her expression kind "
          "and level",
       mo="the office worker's open hand moves slowly in a small horizontal sweep "
          "over the papers and comes to rest flat on the counter; she gives one "
          "small measured shake of the head"),
  dict(key="owatta", cast="W1", props=["P_MADO"], cam="push", lv="mid",
       # L57 そうではありません。制度どおりに、終わったものがあったんです。
       sc="a close portrait of the woman at the counter as she understands: her eyes "
          "lowering to the papers, her mouth closing, the tension going out of her "
          "shoulders into something quieter and heavier, the counter soft behind her",
       mo="her gaze lowers slowly from the worker to the papers on the counter and "
          "stays; her shoulders drop; she gives one very small nod"),
]),

dict(L=58, tag="中高齢寡婦加算", kind="art", shots=[
  dict(key="kafu_kasan", cast=None, hands="W1", props=["P_MADO"], cam="push", lv="mid",
       # L58 中高齢寡婦加算といいます。
       sc="a close shot on the counter of a single plain government leaflet being "
          "turned toward the viewer by an elderly woman's hands, its printed matter "
          "faint ruled boxes and unreadable small marks, one line of it lightly "
          "underlined in pencil",
       mo="the leaflet is turned the last few degrees square to the viewer and "
          "pressed flat with one fingertip beside the pencilled line, and the hands "
          "stay"),
  dict(key="yonjuu_rokujuugo", cast=None, props=[], cam="static", lv="mid",
       # L59 四十歳以上六十五歳未満で、お子さんがいらっしゃらないかた…
       sc="a clean picture-book diagram on a plain pale background: one long "
          "horizontal band running left to right like a life-line, with a warm "
          "coloured section filling only the middle portion of it and plain "
          "uncoloured band at each end, and two small plain marker posts standing "
          "at the two ends of the coloured section",
       mo="the warm colour fills the middle section of the band smoothly from left "
          "to right until it reaches the second marker post and stops there "
          "cleanly; the two posts do not move"),
  dict(key="uwanose", cast=None, props=["P_COIN"], cam="static", lv="mid",
       # L60 そういうかたに、六十五歳になるまで上乗せされる加算です。
       sc="a close shot on a pale wooden surface of one existing stack of "
          "brass-coloured coins with a second smaller stack being added directly on "
          "top of it, clearly a top-up sitting above the original, even soft light",
       mo="the smaller stack is lowered the last centimetre onto the top of the "
          "existing stack and released, and the whole column settles square; one "
          "coin edge rocks once and stills"),
]),

dict(L=61, tag="年に六十三万五千五百円", kind="stat",
     # L61 令和八年度で、年に六十三万五千五百円。月にすると、五万三千円ほど。
     # L62 決して小さくありません。そして、これが六十五歳で、すっと終わります。
     stat=[("中高齢寡婦加算", "年 63万5500円"),
           ("ひと月あたり", "約 5万3000円"),
           ("*65歳で", "終わる")]),

dict(L=63, tag="経過的寡婦加算", kind="art", shots=[
  dict(key="keikateki", cast=None, props=[], cam="static", lv="calm",
       # L63 経過的寡婦加算という形で一部が続くこともありますが、額は下がります。
       sc="the same clean diagram band on a plain background: the thick warm "
          "coloured section ends at its marker post, and beyond that post the band "
          "continues as a much THINNER strip of the same warm colour, clearly "
          "reduced but not gone",
       mo="the thinner strip beyond the marker post draws itself out to the right a "
          "short way and stops; the thick section before the post stays exactly as "
          "it is"),
  dict(key="keikateki_b", cast=None, props=["P_CAL"], cam="push", lv="calm",
       # L63後半 昭和三十一年四月一日より前にお生まれのかたが対象です。
       sc="a close shot of an old cream calendar page from decades ago lying on a "
          "wooden desk, its paper yellowed with age, with a single firm vertical "
          "pencil line ruled straight down between two of its date columns, "
          "dividing the page in two",
       mo="the pencil finishes drawing the vertical dividing line down the page and "
          "lifts away out of frame; the aged paper settles flat and one corner "
          "curls slightly"),
]),

dict(L=64, tag="二十年の壁", kind="art", shots=[
  dict(key="mikkosare", cast="M3", props=["P_DESK"], cam="push", lv="mid",
       # L64 この加算には、見落とされやすい条件がひとつあります。
       sc="the researcher at his desk holding a magnifying glass down over the fine "
          "lower part of a plain leaflet, his eyes narrowed behind his glasses, the "
          "lamp throwing a small bright circle onto the page",
       mo="he lowers the magnifying glass the last few centimetres to the page and "
          "the bright circle sharpens on one line; he goes very still, then his "
          "brows lift slightly"),
  dict(key="nijuunen", cast=None, props=[], cam="push_hard", lv="peak",
       # L65 ご主人の厚生年金の加入期間が、二十年以上あったかどうかで
       # L66 二十年に足りないと、この六十三万円は、つきません。
       sc="a clean picture-book diagram on a plain pale background: two horizontal "
          "bars of the same warm colour drawn one above the other running toward a "
          "single vertical marker line — the upper bar reaches past the marker, the "
          "lower bar stops clearly SHORT of it, leaving a visible gap",
       mo="both bars extend to the right at the same steady speed; the upper one "
          "crosses the vertical marker and stops just past it, the lower one halts "
          "before reaching it and the gap stays open; the marker line does not move"),
  dict(key="tsukanai", cast=None, hands="W1", props=["P_COIN"], cam="static", lv="mid",
       # L66前半 二十年に足りないと、この六十三万円は、つきません。
       sc="a close shot on a pale wooden surface: one plain stack of brass-coloured "
          "coins stands alone, and a second smaller stack is being drawn back and "
          "away from it by a hand instead of being added on top, leaving a clear "
          "empty gap above the first stack",
       mo="the hand carries the smaller stack steadily away from the first one and "
          "out of frame; the first stack is left standing alone with clear empty "
          "space above it and does not move"),
  dict(key="kekka_kawaru", cast=None, props=["P_BUTSU"], cam="static", lv="mid",
       # L66後半 同じように四十代で夫を亡くされても、勤め先での年数で、結果が変わってしまう。
       sc="two identical quiet memorial corners side by side in one frame, each with "
          "the same framed portrait and white chrysanthemum — but the left one is "
          "warmly lit and the right one is drained to flat pale grey, plain wall "
          "between them",
       mo="the warm light on the left corner rises a little while the colour drains "
          "further from the right corner until it is flat grey; the two "
          "chrysanthemums lean the same way in the same draught"),
]),

dict(L=67, tag="ねんきん定期便で確かめる", kind="art", shots=[
  dict(key="teikibin", cast="W1", props=["P_KITCHEN", "P_TEIKI"], cam="push", lv="mid",
       # L67 ねんきん定期便やねんきんネットで、ご主人の加入月数を確かめるのが早道です。
       sc="the 66-year-old woman at her kitchen table unfolding a pale-blue "
          "postcard-style pension statement leaflet with both hands, her glasses "
          "on, a tablet lying beside it, clear daylight from the window",
       mo="she unfolds the leaflet fully open with both hands and flattens the "
          "crease with her thumb, then leans in over one boxed section of it"),
  dict(key="riyuu", cast="W1", props=["P_KITCHEN", "P_TEIKI"], cam="static", lv="mid",
       # L68 六十五歳で年金が減った。その理由の多くは、ここにあります。
       sc="a close shot of the woman's face as she finds the answer on the leaflet — "
          "her eyebrows lifting, her lips parting slightly, recognition rather than "
          "shock, the pale leaflet edge lit in the lower frame",
       mo="her eyes stop moving and fix on one point, then her chin lifts a little "
          "and she breathes out; one fingertip comes up into frame and rests on the "
          "spot she has found"),
]),

# ───────────────── 第5章 働いても増えない (L69–L84) ───────────────────────
dict(L=69, tag="三つ目です", kind="art", shots=[
  dict(key="mittsume", cast="M3", props=["P_DESK"], cam="static", lv="mid",
       # L69 そして、三つ目です。ここがいちばん、知られていないところかもしれません。
       sc="the researcher at his desk turning a page of his open ruled notebook to a "
          "fresh blank spread and resting his pen at the top of it, looking up "
          "toward the viewer with a level, slightly grave expression",
       mo="he turns one page over with his fingertips and smooths it flat, sets the "
          "pen down at the top of the fresh page and looks up; the lamp glow holds"),
  dict(key="super", cast="W1", props=["P_SUPER"], cam="parallax", lv="calm",
       # L70 佐藤さんは、六十六歳のいまも、スーパーでお仕事を続けていらっしゃいます。野菜の売り場です。
       sc="the same 66-year-old woman in a supermarket staff apron and cap arranging "
          "daikon and cabbages in a wooden crate in a bright vegetable aisle, "
          "working steadily with a small comfortable smile, overhead strip lights, "
          "pale green blank price cards on the shelf edge",
       mo="she lifts one daikon from the crate, turns it to sit the right way round "
          "and sets it back down into the row, then reaches for the next; her cap "
          "shifts a fraction as she leans"),
]),

dict(L=71, tag="増えるはずが", kind="art", shots=[
  dict(key="fueru", cast=None, hands="W1", props=["P_COIN"], cam="static", lv="mid",
       # L71 働いた分、ご自身の老齢厚生年金も、少しずつ増えていきます。
       sc="a close shot on a pale wooden surface of an elderly woman's hand placing "
          "brass-coloured coins one at a time onto a small growing stack, an apron "
          "corner visible at the edge of frame, warm even light",
       mo="the hand sets one coin onto the stack, withdraws, and sets a second coin "
          "on top of it; the stack rises a little each time and settles square"),
  dict(key="tedori", cast="W1", props=["P_KITCHEN"], cam="parallax", lv="calm",
       # L72 増えた分は、そのまま手取りが増える。そう思われますよね。
       sc="the woman at her kitchen table in the evening, still in her work apron, "
          "looking up and away with a small hopeful smile as she imagines it, a "
          "small household notebook open in front of her, warm lamp light",
       mo="she looks up from the notebook toward the middle distance and a small "
          "smile forms; her pen taps the page twice, lightly, and stops"),
  dict(key="naranai", cast="W1", props=["P_KITCHEN"], cam="push_hard", lv="peak",
       # L73 ところが、そうならないんです。
       sc="the same framing a moment later: the small hopeful smile gone, the woman "
          "looking straight down at the notebook again, the pen stopped still on "
          "the page, the room a shade cooler and quieter",
       mo="her smile fades and her gaze drops back to the page; the pen stops dead "
          "and stays; she does not move again"),
]),

dict(L=74, tag="二つの計算で比べます", kind="stat",
     # L74–L77 二つの計算 → 大きいほうが、遺族厚生年金の額になります。
     stat=[("① 報酬比例部分の", "3/4"),
           ("② その3/4の2/3 ＋ 自分の老齢厚生年金の", "1/2"),
           ("*大きいほうが", "遺族厚生年金の額")]),

dict(L=78, tag="原典②・併給の調整", kind="genten",
     # L78 日本年金機構のページ、赤で囲んだところです。
     # L79 老齢厚生年金は全額支給となり、遺族厚生年金は、老齢厚生年金に相当する額が支給停止。
     # ✅ CUNG MOT TRANG voi 原典①, nhung KHAC MUC / khac vi tri cuon.
     #    ⚠️ Hai lo screenshot phai NHIN RA la khac nhau — dung chup trung khung.
     genten=dict(url="https://www.nenkin.go.jp/service/jukyu/seido/izokunenkin/"
                     "jukyu-yoken/20150424.html",
                 quote="65歳以上で遺族厚生年金と老齢厚生年金を受ける権利がある方は、"
                       "老齢厚生年金は全額支給となり、遺族厚生年金は老齢厚生年金に"
                       "相当する額の支給が停止となります。",
                 mark="muc「65歳以上の方の取扱い」— khoanh DO dung cau tren",
                 shots=2)),

dict(L=80, tag="合計は、変わりません", kind="stat", peak=True,
     # L80 ご自身の厚生年金が一万円増えたら、遺族厚生年金が一万円止まる。
     # L81 合計は、変わりません。
     stat=[("自分の厚生年金", "＋1万円"),
           ("遺族厚生年金", "−1万円"),
           ("*合計は", "変わらず")]),

dict(L=82, tag="そっくり相殺される", kind="art", shots=[
  dict(key="sousai", cast=None, props=["P_SCALE", "P_COIN"], cam="push", lv="mid",
       # L82 働いて増やしたはずの分が、そっくり相殺される。
       sc="a close shot of a simple brass two-pan balance on a pale wooden surface "
          "holding coins, perfectly level: coins are stacked higher in the left pan "
          "and lower in the right, yet the beam sits dead flat and unmoved, plain "
          "soft background",
       mo="two more coins are placed into the left pan and at the same moment two "
          "are lifted out of the right pan; the beam does not tip at all and stays "
          "perfectly level throughout"),
  dict(key="shirazu", cast="W1", props=["P_SUPER"], cam="static", lv="mid",
       # L83 ここを知らないまま、年金を増やすつもりで働きかたを決めると
       sc="the woman in her supermarket apron standing at a staff notice board in a "
          "back corridor with a small pencil, about to write her hours on a plain "
          "ruled roster sheet, her expression thoughtful and determined",
       mo="she raises the pencil to the roster sheet, holds it hovering above one "
          "row for a beat, then lowers it and writes one short mark; her other hand "
          "steadies the board"),
]),

dict(L=84, tag="税金は、かかりません", kind="art", shots=[
  dict(key="zeikin", cast="W1", props=["P_KITCHEN"], cam="parallax", lv="calm",
       # L84 遺族年金そのものには、所得税も相続税もかかりません。…安心していただいて大丈夫です。
       sc="the woman at her kitchen table setting a plain government leaflet down "
          "and letting her shoulders come down, both hands flat and relaxed on the "
          "table on either side of it, a genuinely relieved small smile, bright "
          "clear daylight filling the room",
       mo="she lays the leaflet down flat, lets both hands settle open on the table "
          "and breathes out; her shoulders drop and the small smile reaches her "
          "eyes; the daylight brightens gently"),
  dict(key="zeikin_b", cast=None, props=["P_COIN"], cam="static", lv="calm",
       # L84後半 国税庁が、そう示しています。ここは、安心していただいて大丈夫です。
       sc="a clean close shot on a pale wooden table of one whole untouched stack of "
          "brass-coloured coins standing complete, with a plain government leaflet "
          "lying flat beside it and nothing taken away from the stack, calm even "
          "daylight",
       mo="the daylight across the table brightens gently and steadies on the "
          "complete coin stack; the leaflet's raised corner settles flat; nothing "
          "is added to or taken from the stack"),
]),

# ───────────────── 第6章 改正 (L85–L92) ───────────────────────────────────
dict(L=85, tag="改正の話", kind="art", shots=[
  dict(key="kaisei", cast=None, props=["P_DESK", "P_CAL"], cam="push", lv="mid",
       # L85 最後に、改正の話にも触れておきます。/ L86 施行は、令和十年の四月です。
       sc="a close desk shot of a plain bound booklet of statutes lying open beside "
          "a cream wall calendar leaning against the wall, one month square on the "
          "calendar ringed in red pen, the desk lamp warm on both",
       mo="a hand turns one page of the open booklet and smooths it flat, then "
          "withdraws; the calendar leaning behind rocks once against the wall and "
          "settles"),
  dict(key="ochitsuite", cast="M3", props=["P_DESK"], cam="static", lv="calm",
       # L87 ただし、ここは落ち着いて聞いてください。
       sc="the researcher looking directly toward the viewer with both hands raised "
          "low and open in a calming, steadying gesture, his expression warm and "
          "unhurried, the study softly lit behind him",
       mo="both his open hands lower slowly through a small calming arc and come to "
          "rest on the desk; he gives one slow reassuring nod"),
]),

dict(L=88, tag="影響を受けません", kind="art", shots=[
  dict(key="eikyou_nashi", cast=None, props=[], cam="pull_out", lv="mid",
       # L88 いま受け取っていらっしゃるかたは、影響を受けません。/ L89 これまでどおりです。
       sc="a clean picture-book diagram on a plain pale background: a group of warm "
          "paper-cutout figures — an older woman, an older man, a parent with two "
          "children — standing together on a solid unbroken pale platform, with a "
          "wide calm arc drawn over them like a sheltering roof",
       mo="the sheltering arc above the group settles firmly into place and the "
          "platform beneath them holds perfectly steady; the figures do not move; "
          "the light on them warms evenly"),
  dict(key="korekara", cast=None, props=[], cam="static", lv="mid",
       # L89 六十歳を過ぎて権利が発生するかたも、これまでどおりです。お子さんを育てているかたも、変わりません。
       sc="the same picture-book diagram: the solid pale platform under the wide "
          "sheltering arc, with two further warm paper-cutout groups — an older "
          "man on his own and a young parent with two small children — now "
          "standing on the same platform alongside the first group, plain pale "
          "background",
       mo="the two further paper groups settle into place on the platform beside "
          "the first and their warm colour comes up to match; the sheltering arc "
          "above widens very slightly to cover them all and holds"),
]),

dict(L=90, tag="新しく五年の期限", kind="stat",
     # L90 施行の時点で四十歳より若い、お子さんのいない女性のかた。年に二百五十人ほど。
     # L91 男性のかたは、これまで五十五歳未満だと受け取れませんでしたが、そこが広がります。
     stat=[("新しく5年の期限がつくのは", "施行時40歳未満・子のいない女性"),
           ("見込み人数", "年 およそ250人"),
           ("*男性は", "55歳未満にも広がる")]),

# ───────────────── 研究ノート・確かめる三つ (L93–L103) ────────────────────
dict(L=93, tag="今日の研究ノート", kind="stat",
     # L93–L98 一〜五
     stat=[("一 4分の3になるのは", "夫の二階だけ"),
           ("二 自分の老齢基礎年金は", "まるごと別に"),
           ("三 中高齢寡婦加算は", "65歳で終わる"),
           ("四 自分の厚生年金が増えた分", "遺族厚生年金が止まる"),
           ("*五 遺族年金に", "税金はかからない")]),

dict(L=99, tag="確かめる三つ", kind="stat",
     # L99–L102 ひとつ／ふたつ／みっつ
     stat=[("ひとつ 年金振込通知書の", "「年金の種類」の欄"),
           ("ふたつ 夫の厚生年金は", "20年以上あったか"),
           ("*みっつ 自分の老齢厚生年金を", "請求してあるか")]),

dict(L=103, tag="ご判断の前に", kind="art", shots=[
  dict(key="chuui", cast="M3", props=["P_DESK"], cam="static", lv="calm",
       # L103 令和八年八月時点の情報です。…必ず年金事務所でご確認ください。
       sc="the researcher closing his ruled notebook gently with both hands and "
          "resting them on top of it, looking toward the viewer with a calm, "
          "honest, slightly cautioning expression, the study lamp warm behind him",
       mo="he closes the notebook cover the last few centimetres and lays both "
          "hands flat on it, then lifts his eyes to the viewer and holds; the "
          "lamplight stays even"),
  dict(key="chuui_b", cast=None, props=["P_MADO"], cam="push", lv="calm",
       # L103後半 ご判断の前に、必ず年金事務所でご確認ください。
       sc="the quiet pension office counter seen from a few steps away with nobody "
          "at it yet, the blank sign boards above, one grey chair drawn neatly up "
          "to the counter and clear daylight from a window off to one side",
       mo="the daylight from the side window strengthens slowly across the empty "
          "counter top; the grey chair stays exactly where it is; nothing else "
          "moves"),
]),

# ───────────────── 次回予告 (L104–L109) ───────────────────────────────────
dict(L=104, tag="次回・扶養親族等申告書", kind="art", shots=[
  dict(key="yokoku", cast="W2", props=["P_ENV"], cam="parallax", lv="mid",
       # L104 さて、次回です。/ L105 東京の高橋さん、六十五歳。秋になると、一通の封筒が届く。
       sc="a Japanese woman of 65 in a mustard-yellow cardigan standing at her front "
          "gate in autumn taking a single white official envelope out of the "
          "letterbox, yellow ginkgo leaves on the ground and in the air, a Tokyo "
          "residential street soft behind her",
       mo="she draws the envelope fully out of the letterbox and lets the flap fall "
          "shut; she turns the envelope over once in her hands; ginkgo leaves drift "
          "down slowly behind her"),
  dict(key="takahashi_b", cast="W2", props=["P_KITCHEN", "P_ENV"], cam="push", lv="mid",
       # L105後半 毎年、秋になると、一通の封筒が届くかたです。
       sc="the 65-year-old woman in the mustard-yellow cardigan now sitting at her "
          "own table indoors, turning the white official envelope over in her hands "
          "and looking at it with a small resigned frown, warm autumn light through "
          "the window behind her",
       mo="she turns the envelope over once more in her hands and sets it down flat "
          "on the table, then rests her fingertips on top of it without opening "
          "it; the autumn light shifts slowly"),
  dict(key="fuyo", cast=None, props=["P_KITCHEN"], cam="push", lv="mid",
       # L106 扶養親族等申告書。この紙を出すか出さないかで、年金から引かれる税金が変わります。
       sc="a close overhead shot of a single official declaration form lying alone "
          "on a table with a black ballpoint pen resting across one corner, the "
          "form ruled into boxes with faint unreadable print, autumn light from "
          "the side",
       mo="the pen is lifted off the form and set down again beside it, and the "
          "form's raised corner is pressed flat by one fingertip; nothing is "
          "written on it"),
  dict(key="hirogatta", cast=None, props=["P_ENV"], cam="pull_out", lv="mid",
       # L107 この紙が届く人の範囲が、大きく広がりました。…受け取ったことのないかたにも
       sc="a wide gentle view of a quiet Japanese residential street in autumn seen "
          "from above at a shallow angle, with an identical white official envelope "
          "waiting in the letterbox of house after house all the way down the "
          "street, ginkgo trees turning yellow along the pavement",
       mo="the camera eases slowly back and up so more and more houses come into "
          "frame, each with the same white envelope waiting in its letterbox; "
          "leaves drift down across the street"),
  dict(key="mata", cast="M3", props=["P_DESK"], cam="static", lv="calm",
       # L108 次回の研究で、一緒に確かめます。/ L109 また次回の研究でお会いしましょう。
       sc="the researcher at his desk in the evening, the lamp warm, one hand raised "
          "in a small quiet farewell toward the viewer, his notebook closed in "
          "front of him, the window behind him dark blue with dusk",
       mo="his raised hand gives one small unhurried wave and lowers to the desk; "
          "he inclines his head slightly; the desk lamp glow holds steady as the "
          "window behind darkens"),
]),
]
