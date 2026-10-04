# -*- coding: utf-8 -*-
r"""_scenes21.py — SCENE PLAN ("slides") cho video 21 扶養親族等申告書・二百五万円.

Import boi `gen_flow21.py` (sinh prompt text->video) va `build_remotion_21.py`.

⭐ STYLE: **AI NGUOI THAT (photoreal)** — user chot 2026-09-04: *"tao muon dang
   AI nguoi that. Tu nay deu dung AI nguoi that het nhe"*. Khong con chon style
   theo tung video; xem `CLAUDE.md` §② khoi ⭐⭐⭐⭐.
   ⚖️ Canh AI realistic => **PHAI TICK "altered/synthetic content"** luc upload
   (`youtube-compliance.md` §2.1). Nhan vat HU CAU; cam mat nguoi that cu the.

🔴 KHAC VIDEO 20 O CACH TO CHUC FILE — co y:
   Video 20 co BA lop file (`_scenes20` anime + `_scenes20_real` + `_scenes20_human`)
   vi style bi dao hai lan trong mot ngay. Video 21 gop lai MOT file, mang san
   ba bai hoc cua lop `_human`:
     · anh tinh (`sc`) PHAI co nguoi o **the BAT DAU** cua viec do — t2v khong
       tu sinh ra nguoi khong co trong khung;
     · `mo` = MOT NGUOI LAM MOT VIEC tron 8 giay, ba nhip **toi -> lam -> dung**,
       viet nhu mot dong kich ban quay tai lieu (khong `PERFORMANCE:`, khong
       "don chuyen dong vao 4 giay dau");
     · viec phai la viec nguoi ta THUC SU lam voi vat do (nhat thu, deo kinh,
       lat mat sau, bam may tinh, tra but) — khong "anh sang dich chuyen",
       khong "bui bay", khong vat the tu bay.
   ⛔ **Khong shot nao sieu thuc.** Bai 21 day an du SO HOC (duong 158->205,
      phep cong 110+95, nguong tut ve 148) — moi an du thi hanh bang **VAT THAT
      + may quay + dien xuat**: bang trang, thuoc ke, may tinh cam tay, hai to
      giay dat canh nhau, hop ho so. Khong so tu ve tren khong, khong giay tu bay.

📐 NEO: `L` = chi so dong khong-rong trong `03_SCRIPTS/21_..._TTS.md`
   (= chi so dong trong `timeline.json`, 114 dong / 855,9s). Scene chay tu L cua
   no toi L cua scene ke tiep; cac shot trong `shots` chia deu khoang do.

🖼️ **11 SHOT `still=True` — ANH TINH, KHONG PHAI CLIP 8s** (user chot 2026-09-04:
   *"cai nay may dung hinh anh di. Chu video tao gen ra no khong ro noi dung"*).
   Do la 11 shot **bang trang** (an du so hoc: cong lai / tang len / bang nhau).
   Hai ly do:
     ① Veo **khong viet duoc chu Nhat/so co nghia** — frame 10800 ban render thu
        ra 「50 ≒ 50 0 ハ」 loang ngoang chiem ~1/4 khung;
     ② ngay khi bo chu chi ve KY HIEU, clip 8s van **khong ro noi dung** — ve
        trong 8 giay thi net ve loang ngoang theo tay, khong doc ra hinh gi.
   ⇒ Anh tinh thi user **gen nhieu ban roi CHON**, va net ve la net TINH nen doc
     ra duoc. Builder dat chung o `trk-video` (van la cat canh) + `motion: pan`.
   ⚠️ Anh AI CUNG nat chu, nen prompt anh **cung khong duoc co chu/so** — chi
     vong tron, mui tui, gach ngang, dau ＋ ＝, dau tich.

🔴 LUAT AP:
  · `audience-45plus.md` §2.0b — anh chinh doi <= 9,0s
    => `so shot >= ceil(giay_scene / 9)`. Scene `stat`/`formula` DUOC MIEN.
  · `CLAUDE.md` §② — VUNG GIUA CHO DUOC MOT THU: scene co `stat`/`formula` thi
    KHONG co anh hero (khong `shots`).
  · `CLAUDE.md` §③ — cua so **0-120s KHONG co モニター ke chuyen**: cold open
    dung `U1`/`U2` (nguoi 60-70 VO DANH, khong ten, khong tieu su). モニター co
    ten (高橋さん = M1) vao tu **L30 = 208,6s = 3:29** ✅ (gate G9 doi >= 2:00).
  · `stage-zu-layout.md` §2 / `audience-45plus.md` §2.0c — bang >= 3 dong; dong
    `*` la dong duoc NHAN.
  · YMYL: moi con so duoi day co mat NGUYEN VAN trong kich ban. Hai cong thuc
    `110+95=205` va `5+2,1%=5,105` la phep tinh lai tu so DA doc trong loi —
    khong phai so moi.

🔴 原典 — **URL CHUA VERIFY**. Bon khoi `genten` de `url=""` co y: khong co
   FACT SHEET kem link cho bai nay (`03_SCRIPTS/21_*.md` ban sach chua ton tai),
   va YMYL cam bia nguon. `gen_flow21.py` in 🔴 va exit 1 neu con `url=""`.
   Phai verify 4 trang truoc khi chup man hinh.
"""

# ══════════════════════════════════════════════════════════════════════════
# CAST — mo ta kieu "character design sheet": toc / mat / trang phuc CO DINH.
# M3 giu nguyen lock cua video 20 => 案内役 nhat quan xuyen ca kenh.
# ══════════════════════════════════════════════════════════════════════════
CAST = {
    "M1": {"who": "高橋さん 65 — case chinh, Tokyo, nguyen truong phong, nghi nam ngoai", "lock": (
        "a Japanese man of 65 with short neatly combed grey hair thinning at the "
        "crown, a squarish clean-shaven face with deep smile lines, calm tired "
        "eyes behind thin rectangular reading glasses, wearing a soft olive-grey "
        "cardigan over a pale checked shirt buttoned to the collar")},
    "W1": {"who": "奥さま 60 — vo cua 高橋さん, hien khong di lam", "lock": (
        "a Japanese woman of 60 with dark brown hair cut short and tucked behind "
        "one ear with a few grey strands at the parting, a slim gentle face and "
        "attentive eyes, wearing a plain dusty-rose knitted top under a beige apron")},
    "M3": {"who": "研究員 — nguoi dan 案内役 cua kenh (giong video 20)", "lock": (
        "a composed Japanese man in his late sixties with neat full white hair "
        "combed back, thin silver-rimmed round glasses, calm unhurried eyes, "
        "wearing a soft charcoal cardigan over a pale blue shirt")},
    "U1": {"who": "nguoi nhan phong bi o cold open — nam 68, VO DANH", "lock": (
        "a Japanese man of 68 with short white hair and a lined weathered face, "
        "slightly stooped shoulders, wearing a faded navy fleece zip-up over a "
        "grey undershirt and loose cotton trousers")},
    "U2": {"who": "nguoi 66 VO DANH — canh minh hoa chung (dai 148万, han chot)", "lock": (
        "a Japanese woman of 66 with silver-grey hair pinned back loosely, a round "
        "kind face with reading glasses on a cord around her neck, wearing a soft "
        "lilac cardigan over a white blouse")},
    "S1": {"who": "職員 quay 年金事務所 / 税務署 — nu, dau 30", "lock": (
        "a Japanese woman in her early thirties with black hair in a low neat "
        "ponytail, wearing a plain navy office jacket over a white blouse with a "
        "small blank name-holder clipped at her chest")},
}

# ban tay can canh — dung khi khung khong co mat
HANDS = {
    "H_M1": ("the hands of a Japanese man of 65 — broad and dry, short clean "
             "nails, a thin worn wedding band on the left ring finger"),
    "H_U1": ("the hands of a Japanese man of 68 — thin and sun-spotted with "
             "prominent knuckles"),
    "H_M3": ("the hands of a Japanese man in his late sixties — steady, holding "
             "a plain black fountain pen loosely"),
}

# ══════════════════════════════════════════════════════════════════════════
# PROP LOCK — tat ca la VAT CO THAT, cam duoc, quay duoc.
# 🔴 Giay to phai CHUNG CHUNG (o ke trong, chu khong doc duoc) — `media-library.md`
#    §2.10 ⑦: cam dung ban sao giay to chinh thuc; giay THAT chi o 原典ショット.
# ══════════════════════════════════════════════════════════════════════════
PROP = {
    "P_ENV": ("the SAME envelope in every shot: a plain white window envelope, "
              "long and narrow, with a pale blue printed band along one edge and "
              "no readable wording, the flap unsealed and one corner slightly bent"),
    "P_SHINKOKU": ("the SAME declaration form in every shot: one A4 sheet of pale "
                   "cream paper printed with fine grey rule lines and a column of "
                   "empty boxes down the right side, three boxes left blank, the "
                   "printing too small and soft to read"),
    "P_PAMPH": ("the SAME booklet in every shot: a thin stapled A4 leaflet with a "
                "muted blue-grey cover and plain inner pages of small indistinct "
                "print, one page turned down at the corner"),
    "P_PEN": ("the SAME pens in every shot: a slim red ballpoint with a chewed cap "
              "and a stubby wooden pencil lying beside it"),
    "P_CALC": ("the SAME calculator in every shot: a small beige desktop "
               "calculator with large grey rubber keys and a narrow display "
               "showing a few clear numerals"),
    "P_RULER": ("the SAME ruler in every shot: a short scratched aluminium ruler "
                "with worn engraved marks"),
    "P_TSUCHI": ("the SAME notice in every shot: a folded pale-green single sheet "
                 "with two horizontal fold creases and a narrow table of figures "
                 "down one side, the figures crisp and the surrounding wording soft"),
    "P_KITCHEN": ("the SAME kitchen table in every shot: a pale wooden table with "
                  "a rubbed varnish edge, a woven placemat, a chipped brown tea cup "
                  "and a small tin of tea leaves at the far corner"),
    "P_DESK": ("the SAME study desk in every shot: a dark-wood desk with a green "
               "blotter pad, a stack of unlabelled folders on the left and a small "
               "brass desk lamp with a dented shade"),
    "P_BOARD": ("the SAME whiteboard in every shot: a small A2 whiteboard on a "
                "wooden easel, its surface faintly ghosted from old wiping, a "
                "black marker resting in the tray"),
    "P_POST": ("the SAME letterbox in every shot: a weathered aluminium wall "
               "letterbox beside a frosted-glass front door, its lid worn bare "
               "at the lip"),
    "P_FILE": ("the SAME box file in every shot: a scuffed grey cardboard document "
               "box with a hand-cut blank paper label, packed with sheets"),
    "P_COUNTER": ("the SAME counter in every shot: a low pale-laminate service "
                  "counter with a clear acrylic partition, a numbered ticket stand "
                  "and a small tray for documents"),
    "P_NENPYO": ("the SAME wall calendar in every shot: a plain monthly paper "
                 "calendar hanging on a nail, its grid faint and its numerals "
                 "clear, one square marked with a red pen ring"),
    "P_TSUCHOU": ("the SAME bankbook in every shot: a slim bank passbook with a "
                  "worn navy cover and a column of printed figures inside, the "
                  "figures crisp and the bank name indistinct"),
}

# shot ma GIAY TO la chu the => phai co chu SO doc duoc + dau danh dau dung cho
# tay chi vao (`R_IMG_DOC` cua gen_flow21)
DOC_FOCUS = {
    "shinkoku_ue", "ninen_2man", "kojo_ugoku", "kigen_insatsu",
    "gonen_sakanobore", "furikomi_sa", "kakunin_hizuke", "kazoku_ran",
}


# ══════════════════════════════════════════════════════════════════════════
# SCENES — 47 scene / 855,9s = 2,88 scene/phut
#   art 35 scene · 85 clip 8s      stat 4 · formula 4 · genten 4 (9 screenshot)
# ══════════════════════════════════════════════════════════════════════════
SCENES = [

# ══════════════ COLD OPEN (L0–L11 · 0,0–74,4s) ═══════════════════════════
# ⛔ Khong モニター co ten trong cua so nay — chi U1/U2 vo danh (CLAUDE.md §③).
dict(L=0, tag="百五十八万円という記憶", kind="art", shots=[
  dict(key="kioku158", cast="U1", props=["P_KITCHEN", "P_TSUCHI", "P_PEN"],
       cam="push", lv="mid",
       # L0 年金に税金がかかりはじめるのは、年に百五十八万円から。
       sc="a Japanese man of 68 already wearing his reading glasses, sitting at "
           "his kitchen table in the late morning with a folded pale-green "
           "notice open flat in front of him, a red ballpoint and a stubby "
           "pencil lying beside the sheet, seen from the front at chest height",
       mo="He leans forward over the sheet and runs one finger slowly down the "
           "column of figures. His finger stops partway down and stays there, "
           "and he holds still, looking at that line."),
  dict(key="zure47", hands="H_U1", props=["P_TSUCHI", "P_PEN"],
       cam="push_hard", lv="peak",
       # L1–L2 その数字は、いま四十七万円ずれています。／二百五万円です。
       sc="a close overhead shot of the same pale-green notice on the wooden "
          "table, the thin sun-spotted hands of a man of 68 holding a red "
          "ballpoint just above one line of figures, the pencil pushed to the "
          "edge of frame",
       mo="He draws a red ring round one figure in a single unhurried stroke, "
          "lifts the pen away and sets it down on the table, then taps the ringed "
          "figure twice with his fingertip and leaves his hand resting there."),
]),

dict(L=3, tag="この秋、封筒が届く", kind="art", shots=[
  dict(key="shizuka_ugoku", cast="U1", props=["P_KITCHEN"], cam="static", lv="low",
       # L3 去年、静かに動きました。テレビでも、あまり取り上げられませんでした。
       sc="a Japanese man of 68 sitting at the same kitchen table with a folded "
          "newspaper open across it, a cold cup of tea at his elbow, the "
          "television dark in the room behind him, seen from the side at "
          "table height",
       mo="He turns one page of the newspaper, scans down it, then turns the next "
          "and scans that too. He folds the paper closed, pushes it away to the "
          "side of the table and sits still with one hand flat on top of it."),
  dict(key="post_aki", cast="U1", props=["P_POST", "P_ENV"], cam="push", lv="mid",
       # L4 そしてこの秋、…税務の封筒が届きます。
       sc="a Japanese man of 68 standing at his front door in the autumn morning "
          "with the aluminium wall letterbox open, one hand on its lid and a "
          "plain white window envelope already in his other hand, dry leaves on "
          "the step behind him",
       mo="He lets the letterbox lid fall shut, turns the envelope over to look "
          "at the front of it, holds it a moment at arm's length, then tucks it "
          "under his arm and steps back inside out of the cold."),
  dict(key="ippen_mo", cast="U1", props=["P_FILE", "P_DESK"], cam="parallax", lv="mid",
       # L5 年金だけで暮らしていて、所得税は一円も払っていない。
       sc="a Japanese man of 68 standing at a dark-wood desk with a scuffed grey "
          "document box open in front of him, a thick handful of old sheets "
          "lifted halfway out, a small brass lamp lit at the side",
       mo="He lifts the sheets out of the box and turns them over one at a time, "
          "looking at each for only a moment. He gets to the bottom of the pile, "
          "squares the sheets back into the box and lets the lid down on it."),
]),

dict(L=7, tag="出さないほうが損をする紙", kind="art", shots=[
  dict(key="taisho_kazoku", cast="U1", props=["P_KITCHEN", "P_ENV"],
       cam="static", lv="mid",
       # L7 対象は、年金を受け取っているかた。とくに、ご家族を扶養されているかた。
       sc="a Japanese man of 68 and a Japanese woman of 66 sitting side by side "
           "at a kitchen table with one white window envelope lying flat on the "
           "table between them, both already looking down at it, two tea cups "
           "pushed to the far edge",
       mo="She reaches out and rests two fingers on the envelope without "
           "lifting it, and they both keep looking down at it. Neither of them "
           "moves it."),
  dict(key="shinkoku_ue", hands="H_U1", props=["P_SHINKOKU", "P_ENV", "P_PEN"],
       cam="push", lv="mid",
       # L8 その封筒の中身は、扶養親族等申告書という紙です。
       sc="a close shot from above of one cream A4 form lying flat and open on "
           "the wooden table with an opened white envelope resting beside it, "
           "the thin hands of a man of 68 at the edges of the form, one red "
           "ballpoint on the table",
       mo="He smooths the form flat with the side of one hand, once, and leaves "
           "that hand resting at the edge of the page."),
  dict(key="gyaku_no_kami", cast="U1", props=["P_SHINKOKU", "P_KITCHEN"],
       cam="static", lv="mid",
       # L9 …中身は逆で、出さないほうが損をする紙なんです。
       sc="a Japanese man of 68 sitting back from the kitchen table holding the "
          "cream form up in both hands at reading distance, his brows drawn "
          "together, the table and cup soft behind it",
       mo="He reads down the form, then lowers it to the table and pushes it away "
          "from himself with one hand. He stops, draws it back toward him again "
          "and holds it there with his fingertips."),
  dict(key="ninen_2man", hands="H_U1", props=["P_CALC", "P_SHINKOKU"],
       cam="push_hard", lv="peak",
       # L10 出すか出さないかで、一年に二万円。二十年なら、四十万円ほど。
       sc="a close shot of a small beige calculator on the wooden table beside "
          "the cream form, the thin hands of a man of 68 resting on its keys with "
          "a few numerals already showing on the narrow display",
       mo="He presses three keys in turn with one finger, waits, then presses one "
          "more and lifts his hand away. He looks at the display without moving, "
          "then taps the edge of the calculator once with his knuckle."),
]),

# ══════════════ CHUONG 1 — 二百五万円の線 (L12–L29 · 74,4–208,6s) ════════
dict(L=12, tag="研究室・いちばん大きな誤解", kind="art", shots=[
  dict(key="kenkyu_hiraku", cast="M3", props=["P_DESK", "P_PAMPH"],
       cam="push", lv="mid",
       # L12 年金と老後のお金研究室です。…原典を画面で開きながら
       sc="a composed Japanese man in his late sixties standing at a dark-wood "
          "desk with two thin stapled leaflets laid open side by side on the "
          "green blotter, his hand flat on one of them, a brass lamp lit low",
       mo="He turns the leaflet on his left round to face the camera, squares it "
          "against the edge of the blotter, then draws the second leaflet up "
          "beside it and lines the two together with the flat of his hand."),
  dict(key="futatsu_narabe", hands="H_M3", props=["P_PAMPH", "P_RULER"],
       cam="static", lv="low",
       # L13 いちばん大きな誤解をひとつ、片づけておきます。
       sc="a close overhead shot of two open leaflets on a green blotter with a "
          "short scratched aluminium ruler lying across the pages and the steady "
          "hands of a man in his late sixties holding a fountain pen above them",
       mo="He slides the ruler down the page until it sits under one line, holds "
          "it there and draws the pen along its edge in one stroke, then lifts "
          "the ruler off and sets it down beside the leaflet."),
  dict(key="ooi_gokai", still=True, cast="M3", props=["P_BOARD"], cam="parallax", lv="mid",
       # L14 そう覚えていらっしゃるかたが、とても多いんです。
       sc="a composed Japanese man in his late sixties standing beside a small "
           "whiteboard on a wooden easel, a black marker in his hand, the board "
           "surface clean and empty",
       mo="He draws one large open ring on the empty board in a single sweep, "
           "steps back to look at it, then returns and draws a diagonal stroke "
           "through the ring. He caps the marker and rests it in the tray."),
  dict(key="mou_tsukawanai", still=True, cast="M3", props=["P_BOARD", "P_PAMPH"],
       cam="push_hard", lv="peak",
       # L15 その数字は、もう使われていません。
       sc="a composed Japanese man in his late sixties at the whiteboard where a "
           "single crossed-through ring is drawn, holding one open leaflet up "
           "beside the board at chest height",
       mo="He holds the leaflet up level with the crossed ring, looks from one to "
           "the other, then lowers the leaflet to his side and leaves his other "
           "hand resting on the frame of the easel."),
]),

dict(L=16, tag="原典①国税庁・二百五万円", kind="genten",
     genten=dict(url="https://www.nta.go.jp/publication/pamph/koho/kurashi/html/03_1.htm",
                 verified="2026-09-04",
                 # 🔴 SUA 2026-09-04 sau khi CHUP ANH THAT (`_genten_raw/nta_full.png`,
                 #    dai y 2126-2300). Ban dau tao lay quote tu WebFetch va no tra
                 #    ve cau rut gon cua CHO KHAC tren trang ("この額が205万円を…"),
                 #    lam tao ket luan sai rang loi doc "lech nguyen van".
                 #    ⇒ Doc tu ANH thi cau tren trang KHOP loi doc L17 gan nhu tung
                 #    chu, nen `said` da duoc BO.
                 #    📌 Bai hoc: WebFetch (model nho) TOM TAT/dien giai, no khong
                 #    phai nguon "nguyen van". Bang chung nguyen van la SCREENSHOT.
                 quote="一定の金額（65歳未満の場合は155万円、65歳以上の場合は205万円"
                       "（※））を超える公的年金等や一定の生命保険契約等に基づく年金を"
                       "受け取るときは、所得税等が源泉徴収されますが、これらについては"
                       "年末調整が行われないため、確定申告で1年間の税金を精算すること"
                       "になります。",
                 # ⭐ Cau nay TRUNG NGUYEN VAN loi doc L26 — chung minh script duoc
                 #    viet tu dung trang nay. Khoanh do luon khi chup, no la bang
                 #    chung cho ca 214万 (scene 08) chu khong rieng 205万.
                 quote3="なお令和9年分については、65歳未満の場合は164万円、"
                        "65歳以上の場合は214万円となります。",
                 mark="trang「高齢者と税（年金と税）」muc 公的年金等の源泉徴収 — "
                      "khoanh DO hai dong 155万円 va 205万円",
                 shots=3)),

dict(L=19, tag="四十七万円も上がった", kind="art", shots=[
  dict(key="yonjunana_agaru", still=True, cast="M3", props=["P_BOARD"], cam="push", lv="mid",
       # L19 百五十八万円から、四十七万円も上がりました。
       sc="a composed Japanese man in his late sixties at the small whiteboard "
           "with a short horizontal stroke drawn low on the otherwise clean board, "
           "marker in hand, seen from the side at shoulder height",
       mo="He draws a second horizontal stroke higher up the board, then draws a "
           "long arrow from the lower stroke up to the higher one in one movement. "
           "He steps back one pace and looks at the pair of strokes."),
  dict(key="riyuu_hakkiri", cast="M3", props=["P_DESK", "P_PAMPH", "P_RULER"],
       cam="static", lv="low",
       # L20 なぜ上がったのか。理由は、はっきりしています。
       sc="a composed Japanese man in his late sixties seated at the dark-wood "
          "desk with one leaflet open and the aluminium ruler in his hand, the "
          "whiteboard out of focus behind him",
       mo="He sits down, draws the leaflet toward him and lays the ruler across "
          "the page, then turns the leaflet a little so the light falls on it and "
          "leaves his hand resting at the top of the page."),
]),

dict(L=21, tag="控除だけが動いた", kind="art", shots=[
  dict(key="kojo_ugoku", hands="H_M3", props=["P_PAMPH", "P_PEN", "P_RULER"],
       cam="push", lv="mid",
       # L21 基礎控除…四十八万円から九十五万円に引き上げられました。
       sc="a close overhead shot of an open leaflet on the green blotter showing "
          "a short table of figures, the steady hands of a man in his late sixties "
          "holding a red ballpoint above one row with the ruler set under it",
       mo="He rings one figure in the row with the red pen, moves the ruler down "
          "one line and rings the figure below it as well, then lifts both hands "
          "clear of the page."),
  dict(key="kawattenai", cast="M3", props=["P_DESK", "P_FILE"], cam="parallax", lv="low",
       # L22 公的年金等控除のほうは、変わっていません。百十万円のまま。
       sc="a composed Japanese man in his late sixties standing at the desk with "
          "the grey document box open and two sheets of the same size held one in "
          "each hand, the desk lamp lit at the side",
       mo="He brings the two sheets together in front of him and holds them up so "
          "the light shows through both, looks along them, then lays them down flat "
          "and side by side on the blotter."),
  dict(key="tashizan_te", still=True, cast="M3", props=["P_BOARD"], cam="push", lv="mid",
       # L23 百十万円と、九十五万円。足すと、二百五万円。
       sc="a composed Japanese man in his late sixties at the whiteboard with two "
           "short horizontal strokes drawn one under the other on a clean board, "
           "the marker held at the board, seen from behind his shoulder",
       mo="He draws a plus sign between the two strokes, then a long line "
           "underneath them, and finally one thicker stroke below the line. He "
           "lowers the marker to his side."),
]),

dict(L=23, tag="百十万＋九十五万＝二百五万", kind="formula",
     formula="110万 ＋ 95万 ＝ 205万", peak=False),

dict(L=25, tag="来年は二百十四万円", kind="art", shots=[
  dict(key="chuuigaki", hands="H_M3", props=["P_PAMPH", "P_PEN"],
       cam="push", lv="mid",
       # L25 同じパンフレットの、注意書きの部分です。
       sc="a close overhead shot of the same leaflet turned to a page of small "
          "print with a note block at the foot, the steady hands of a man in his "
          "late sixties flattening the fold with one palm",
       mo="He smooths the crease down the middle of the page with his palm, then "
          "moves his finger to the note block at the foot of it and holds it "
          "there, and with the other hand sets the pen down beside the page."),
  dict(key="rainen_mata", still=True, cast="M3", props=["P_BOARD"], cam="static", lv="mid",
       # L26–L27 令和九年分は…二百十四万円となります。
       sc="a composed Japanese man in his late sixties at the whiteboard where "
           "two strokes and a line beneath them are drawn, marker in hand, "
           "standing to one side so the board is clear",
       mo="He draws a third stroke above the others and a short arrow up to it, "
           "then steps aside and turns to look at the whole column of marks from "
           "where he stands."),
  dict(key="mainen_minaosu", cast="M3", props=["P_NENPYO", "P_PEN"],
       cam="parallax", lv="low",
       # L28 毎年見直すところだと思っておいてください。
       sc="a composed Japanese man in his late sixties standing at a plain paper "
          "wall calendar hanging on a nail, a red pen in his raised hand, one "
          "square already ringed",
       mo="He rings a second square on the calendar, lets the sheet fall back "
          "against the wall and straightens it with two fingers, then lowers the "
          "pen and stands looking at the month."),
  dict(key="kyonen_no_joushiki", cast="M3", props=["P_DESK", "P_PAMPH", "P_FILE"],
       cam="static", lv="low",
       # L28 去年の常識で今年を判断すると、ずれます。
       sc="a composed Japanese man in his late sixties seated at the dark-wood "
          "desk with two thin leaflets lying one on top of the other in front of "
          "him, the grey document box open at his elbow",
       mo="He slides the upper leaflet off the lower one and sets it to his left, "
          "looks between the two, then puts the older one into the document box "
          "and closes the lid on it."),
]),

dict(L=29, tag="では、数字で見ていきます", kind="art", shots=[
  dict(key="kazu_de_miru", cast="M3", props=["P_DESK", "P_CALC", "P_SHINKOKU"],
       cam="push", lv="mid",
       # L29 では、その紙を出すと、何が変わるのか。数字で見ていきます。
       sc="a composed Japanese man in his late sixties seated at the dark-wood "
           "desk with a small beige calculator already squared in front of him "
           "on the green blotter and the cream form lying alongside it",
       mo="He rests both hands on the edge of the desk on either side of the "
           "calculator and looks down at it, then settles back a little in his "
           "chair."),
]),

# ══════════════ CHUONG 2 — 高橋さん (L30–L44 · 208,6–318,5s) ══════════════
# ⭐ モニター co ten vao tu day = 208,6s = 3:29 ✅ (G9 doi >= 2:00)
dict(L=30, tag="東京の高橋さん、六十五歳", kind="art", shots=[
  dict(key="takahashi_asa", cast="M1", props=["P_KITCHEN"], cam="push", lv="mid",
       # L30 東京の高橋さん、六十五歳。長く部長を務められて、去年、退職された。
       sc="a Japanese man of 65 in an olive-grey cardigan already wearing his "
           "reading glasses, seated at his own kitchen table in the morning "
           "light with a cup of tea and a folded newspaper in front of him",
       mo="He lifts the cup, takes one slow sip and sets it back down on the "
           "table, then rests both hands beside it."),
  dict(key="ekimae_sanpo", cast="M1", props=[], cam="parallax", lv="low",
       # L31 朝は必ず駅前まで歩いてから帰ってくる、という習慣
       sc="a Japanese man of 65 in an olive-grey cardigan standing on a quiet "
          "residential street in the early morning with a small station building "
          "visible far behind him, one hand in his pocket",
       mo="He stops at the corner, looks up the street toward the station for a "
          "moment, then turns and walks two steps back the way he came and slows "
          "to a stop at a low wall."),
]),

dict(L=32, tag="年末調整をしてくれる会社が、もうない", kind="art", shots=[
  dict(key="genyaku_koro", cast="M1", props=["P_KITCHEN", "P_TSUCHI"],
       cam="static", lv="mid",
       # L32 「現役のころは、税金なんて会社が全部やってくれていましたから」
       sc="a Japanese man of 65 sitting at his kitchen table with the folded "
          "pale-green notice open in front of him, both forearms resting on the "
          "table on either side of it, seen from the front at chest height",
       mo="He looks down at the notice, then lifts one hand off the table and "
          "turns it palm up for a moment before letting it fall back. He shakes "
          "his head slightly and looks away toward the window."),
  dict(key="kaisha_ga_nai", cast="M1", props=["P_FILE", "P_DESK"],
       cam="push", lv="mid",
       # L33 年末調整をしてくれる会社が、もう、ありません。
       sc="a Japanese man of 65 standing at a dark-wood desk with the grey "
          "document box open and an old empty folder held open in both hands, the "
          "shelf behind him half cleared",
       mo="He looks into the empty folder, closes it and lays it down in the box, "
          "then pushes the box a little further along the desk and stands with "
          "one hand still on its edge."),
]),

dict(L=34, tag="年二百四十万円・二百五万円を超える", kind="art", shots=[
  dict(key="tsuki20man", cast="M1", props=["P_TSUCHOU", "P_KITCHEN"],
       cam="push", lv="mid",
       # L34 年金は、月に二十万円ほど。年にすると、二百四十万円。
       sc="a Japanese man of 65 at the kitchen table with a slim navy bankbook "
          "open in one hand and his glasses on, the pale-green notice pushed to "
          "one side of the table",
       mo="He opens the bankbook wider with his thumb, runs his finger down the "
          "printed column inside, stops at one line and holds there, then closes "
          "the book over his finger to keep the place."),
  dict(key="koeteiru", hands="H_M1", props=["P_CALC", "P_TSUCHOU"],
       cam="push_hard", lv="peak",
       # L35 二百五万円を超えていますから、所得税が引かれます。
       sc="a close shot of the beige calculator on the kitchen table with the navy "
          "bankbook open beside it, the broad hands of a man of 65 resting on the "
          "keys and a figure showing on the display",
       mo="He types a figure with two fingers, presses the key at the corner and "
          "waits, then lifts both hands and sets them flat on the table on either "
          "side of the calculator."),
]),

dict(L=36, tag="奥さまは六十歳・配偶者控除", kind="art", shots=[
  dict(key="okusama_60", cast="W1", props=["P_KITCHEN"], cam="static", lv="low",
       # L36 奥さまは六十歳。いまは、お勤めをされていません。
       sc="a Japanese woman of 60 in a beige apron standing at the kitchen "
          "counter drying a cup with a cloth, the table with the notice on it "
          "visible behind her, soft light from the window",
       mo="She finishes drying the cup, sets it on the shelf and folds the cloth "
          "over the rail, then turns toward the table and stops there, looking at "
          "the sheet lying on it."),
  dict(key="haigusha_kojo", cast="M1", props=["P_SHINKOKU", "P_PEN", "P_KITCHEN"],
       cam="push", lv="mid",
       # L37 配偶者控除…使えるのは、あの紙を出したときだけです。
       sc="a Japanese man of 65 seated at the kitchen table with the cream form "
           "open in front of him and a red ballpoint held in his hand just above "
           "the column of empty boxes, a woman of 60 standing behind his "
           "shoulder out of focus",
       mo="He holds the pen tip just above one empty box without writing, then "
           "turns his head and looks up over his shoulder, keeping the pen where "
           "it is."),
]),

dict(L=38, tag="計算の式", kind="formula",
     formula="支給額 − 社会保険料 − 各種控除額 × 5.105％", peak=False),

dict(L=40, tag="配偶者の分が入る", kind="stat", stat=[
    ("ひと月あたり", "3万2,500円"),
    ("一年にすると", "39万円"),
    ("*紙を出さないと", "この行が空になる"),
]),

dict(L=42, tag="三十九万円×五・一〇五％", kind="formula",
     formula="39万 × 5.105％ ≒ 1万9,900円", peak=True),

dict(L=43, tag="紙一枚の差・二十年で四十万円", kind="art", shots=[
  dict(key="kami_ichimai", cast="M1", props=["P_SHINKOKU", "P_KITCHEN"],
       cam="push_hard", lv="peak",
       # L43 年に、二万円ほど。それが、紙一枚の差です。
       sc="a Japanese man of 65 holding the single cream form up between both "
          "hands at chest height at the kitchen table, looking at it, the "
          "calculator and cup soft behind it",
       mo="He holds the sheet up and turns it once between his hands to look at "
          "the back, then lays it down flat on the table, presses the fold out of "
          "it with his palm and leaves his hand resting on top."),
  dict(key="nijunen_40man", cast="M1", props=["P_NENPYO", "P_PEN"],
       cam="parallax", lv="mid",
       # L44 十年、二十年と受け取っていく年金です。二十年なら、およそ四十万円。
       sc="a Japanese man of 65 standing at the paper wall calendar with the red "
          "pen raised, several squares already ringed down the sheet",
       mo="He rings one more square, then runs his finger down the column of "
          "rings from the top to the bottom of the sheet and stops at the last "
          "one, and lowers his hand."),
]),

# ══════════════ CTA (L45 · 318,5–346,5s) ═════════════════════════════════
dict(L=45, tag="CTA・研究室を応援してください", kind="art", shots=[
  dict(key="cta_cha", cast="M3", props=["P_DESK", "P_PAMPH"], cam="static", lv="low",
       sc="a composed Japanese man in his late sixties seated at the dark-wood "
          "desk with the leaflets closed and stacked to one side, a cup of tea "
          "set down on the blotter, the lamp lit low",
       mo="He squares the stack of leaflets with both hands, moves it to the "
          "corner of the desk, then draws the tea cup toward him and holds it in "
          "both hands without drinking."),
  dict(key="cta_mado", cast="M3", props=[], cam="parallax", lv="low",
       sc="a composed Japanese man in his late sixties standing at a window in a "
          "quiet room, half turned away from the desk behind him, one hand resting "
          "on the frame, afternoon light on the glass",
       mo="He rests his hand on the window frame and looks out for a moment, then "
          "turns back toward the room, takes one step and stops beside the desk."),
  dict(key="cta_note", hands="H_M3", props=["P_DESK", "P_PEN"],
       cam="push", lv="low",
       sc="a close overhead shot of the green blotter with a small plain notebook "
          "open on it and the steady hands of a man in his late sixties holding a "
          "fountain pen above a blank page",
       mo="He turns to a clean page in the notebook, smooths it flat, writes two "
          "short strokes at the top of it and then caps the pen and lays it down "
          "in the gutter of the book."),
  dict(key="cta_tsuzuki", cast="M3", props=["P_DESK", "P_PAMPH"],
       cam="push", lv="mid",
       sc="a composed Japanese man in his late sixties seated at the desk drawing "
          "the stack of leaflets back toward himself, the notebook open beside "
          "him, the lamp lit",
       mo="He brings the stack back in front of him, opens the top leaflet to a "
          "marked page and flattens it with one hand, then sets his other hand at "
          "the edge of the page ready to turn it."),
]),

# ══════════════ CHUONG 3 — 税率は同じ (L46–L59 · 346,5–446,9s) ════════════
dict(L=46, tag="誤解②税率が高くなる？", kind="art", shots=[
  dict(key="gokai_zeiritsu", cast="U2", props=["P_KITCHEN", "P_SHINKOKU"],
       cam="push", lv="mid",
       # L46–L47 紙を出さないと、税率が高くなる。そう聞いたことは？
       sc="a Japanese woman of 66 in a lilac cardigan sitting at a kitchen table "
          "with the cream form in front of her, her reading glasses hanging on "
          "their cord, one hand at her chin",
       mo="She picks her glasses up off her chest and puts them on, leans in over "
          "the form and looks down it, then sits back and takes the glasses off "
          "again, holding them in her lap."),
  dict(key="sore_wa_chigau", still=True, cast="M3", props=["P_BOARD"], cam="push_hard", lv="peak",
       # L48 それは、違います。
       sc="a composed Japanese man in his late sixties standing squarely at the "
           "small whiteboard with two open rings drawn side by side on a clean "
           "board and a black marker held at the board",
       mo="He draws one line under both rings at once, then puts an equals sign "
           "between them in a single stroke, steps back half a pace and lowers the "
           "marker to his side."),
]),

dict(L=49, tag="原典②年金機構・税率に差はない", kind="genten",
     genten=dict(url="https://www.nenkin.go.jp/section/faq/jukyu/jukyushatodoke/rourei/fuyoushinkoku/teishutsu/20141022-08.html",
                 verified="2026-09-04",
                 quote="提出した場合と提出しなかった場合で、所得税率に差はありません。",
                 # ⭐ CUNG TRANG con co CA HAI cong thuc — la nguon THAT cho scene
                 #    13 (L38 計算の式) va cho L52-L53 (控除が消える). Anh thu 2 cua
                 #    khoi nay khoanh chinh hai dong do.
                 quote2="源泉徴収税額=（年金支給額−社会保険料−各種控除額（基礎控除+"
                        "配偶者控除等各種控除））×合計税率（5.105%）",
                 quote3="源泉徴収税額=（年金支給額−社会保険料−基礎控除）×合計税率"
                        "（5.105%）",
                 # ✅ SUA LOI 2026-09-04 (user chot): L49 doi tu
                 #    「こう書かれています」 sang 「要点だけまとめます」 => khong con
                 #    tuyen bo nguyen van, nen `said` bo. Chu tren anh khoanh do
                 #    van la chu THAT cua trang.
                 mark="trang FAQ「扶養親族等申告書を提出しなかった場合はどうなるの"
                      "ですか。」— anh 04 khoanh cau 所得税率…, anh 05 khoanh 2 cong thuc",
                 shots=2)),

dict(L=51, tag="控除が消える", kind="art", shots=[
  dict(key="kojo_kieru", hands="H_M3", props=["P_SHINKOKU", "P_PEN", "P_RULER"],
       cam="push", lv="mid",
       # L51–L52 控除が、消えるんです。／基礎的な控除に加えて…
       sc="a close overhead shot of two cream forms laid side by side on the green "
          "blotter, the steady hands of a man in his late sixties holding the "
          "ruler across the right-hand sheet",
       mo="He lays the ruler under one row on the right-hand sheet and draws a "
          "line along it, moves down and draws a second, then lifts the ruler away "
          "and sets it between the two sheets."),
  dict(key="dake_ni_naru", cast="M3", props=["P_SHINKOKU", "P_DESK"],
       cam="static", lv="mid",
       # L53 出さなかったかたは、基礎的な控除だけ。
       sc="a composed Japanese man in his late sixties standing at the desk "
          "holding one cream form up in each hand at chest height, the lamp lit "
          "behind them",
       mo="He holds the two sheets up level with each other, then lowers the one "
          "in his left hand to the desk and slides it away to the far edge, "
          "keeping the other raised."),
  dict(key="hiku_mae_no_gaku", still=True, cast="M3", props=["P_BOARD"], cam="push", lv="mid",
       # L54 税率が上がるのではなく、引く前の額が大きくなる。
       sc="a composed Japanese man in his late sixties at the whiteboard with two "
           "rings and an equals sign already on it, marker in hand, seen from the "
           "side",
       mo="He draws a box round the left ring, then a second larger box round the "
           "first, and taps the marker twice on the edge of the board before "
           "lowering it."),
  dict(key="hikareru_fueru", hands="H_M3", props=["P_CALC", "P_SHINKOKU"],
       cam="push", lv="mid",
       # L54 結果として、引かれる税金が増える。そういう仕組みです。
       sc="a close shot of the beige calculator on the green blotter beside one "
          "cream form, the steady hands of a man in his late sixties resting on "
          "the keys with a figure already on the display",
       mo="He presses two keys in turn, waits for the display, then presses the "
          "corner key once more and lifts his hand away, and taps the edge of the "
          "form beside it with one fingertip."),
]),

dict(L=55, tag="控除の種類", kind="stat", stat=[
    ("配偶者", "ひと月3万2,500円"),
    ("70歳以上の配偶者・家族", "ひと月4万円"),
    ("扶養家族 ひとりにつき", "ひと月3万2,500円"),
    ("障害のあるかた", "ひと月2万2,500円〜"),
    ("*家族の人数が多いほど", "紙一枚が重くなる"),
]),

dict(L=59, tag="紙一枚が重くなる", kind="art", shots=[
  dict(key="omoku_naru", cast="U2", props=["P_SHINKOKU", "P_KITCHEN"],
       cam="push", lv="mid",
       # L59 ご家族の人数が多いかたほど、この紙の一枚が重くなります。
       sc="a Japanese woman of 66 seated at the kitchen table with the cream form "
          "held flat under both hands, her glasses back on, the tea cup at her "
          "elbow",
       mo="She presses the form flat under both palms, slides it a little closer "
          "to herself, then lifts one hand and lays it over the column of boxes "
          "and holds it there."),
]),

# ══════════════ CHUONG 4 — 対象が広がる (L60–L70 · 446,9–534,6s) ══════════
dict(L=60, tag="三つ目・今年の変化", kind="art", shots=[
  dict(key="mitsume", still=True, cast="M3", props=["P_BOARD"], cam="push", lv="mid",
       # L60 そして、三つ目です。今年、何が変わったのか。
       sc="a composed Japanese man in his late sixties at the small whiteboard "
           "wiping it clear with a cloth, the marker already back in the tray",
       mo="He wipes the board clear in two passes, folds the cloth and sets it on "
           "the easel tray, then picks the marker up and draws three short ticks "
           "down the left edge of the clean board."),
  dict(key="izen_wa_205", hands="H_M3", props=["P_FILE", "P_SHINKOKU"],
       cam="static", lv="low",
       # L61 これまで、この紙が届いていたのは、二百五万円以上のかた。
       sc="a close overhead shot of the grey document box with a small stack of "
          "cream forms inside it, the steady hands of a man in his late sixties "
          "lifting the top sheet clear",
       mo="He lifts the top sheet out of the box, holds it a moment, then lays it "
          "down on the blotter beside the box and squares the remaining stack "
          "with his fingertips."),
]),

# 🔴 NGUON DA VERIFY 2026-09-04 (khong lam the 原典 vi vung giua chi cho duoc
#    MOT thu, va the chu doc ro hon screenshot voi tep 45+):
#    年金機構「令和9年分…紙の提出方法」§扶養親族等申告書の送付の対象となる条件
#    https://www.nenkin.go.jp/service/jukyu/tetsuduki/rourei/jukyu/fuyo/2027fuyoukami.html
#    Bang 送付対象となる年金額 — 65歳以上: 令和7年分まで 158万 / 令和8年分 205万 /
#    **令和9年分 148万** · 65歳未満: 108万 / 155万 / **98万**. Va cau
#    「住民税の課税対象となる可能性がある方（単身者の住民税非課税限度額の最低額以上
#    の方）にご案内をお送りしています」 = dung ly do 住民税 ma L64-L67 noi.
#    ⚠️ Dung lan voi bang 源泉徴収の対象となる年金額 tren cung site (158万→205万,
#    chieu NGUOC) — hai bang khac nhau, tao da suyt ket luan sai vi doc lan.
dict(L=62, tag="来年分からは百四十八万円以上にも", kind="stat", stat=[
    ("これまで（65歳以上）", "年金205万円以上"),
    ("来年分から（65歳以上）", "年金148万円以上"),
    ("*65歳未満は", "98万円以上"),
]),

dict(L=64, tag="住民税のためです", kind="art", shots=[
  dict(key="juuminzei_tame", still=True, cast="M3", props=["P_BOARD"], cam="push_hard", lv="peak",
       # L64–L65 住民税のためです。／税金を取りに来たのではなく…
       sc="a composed Japanese man in his late sixties standing at the whiteboard "
           "where two open rings are drawn one above the other, marker held at the "
           "board, the room quiet behind him",
       mo="He draws a long arrow from the two rings down to the foot of the board "
           "and puts a firm dot at its tip, then steps back a full pace, looks at "
           "the board and lets his hand with the marker fall to his side."),
  dict(key="kazoku_joho", hands="H_M3", props=["P_SHINKOKU", "P_PEN"],
       cam="push", lv="mid",
       # L65 …ご家族の情報が要るようになった。
       sc="a close overhead shot of one cream form on the green blotter with the "
          "column of empty boxes toward the camera and the steady hands of a man "
          "in his late sixties resting the fountain pen at the first box",
       mo="He moves the pen down the column, touching the tip lightly at the top "
          "of each empty box in turn without writing, reaches the last one and "
          "lifts the pen away from the page."),
]),

dict(L=66, tag="非課税の帯にいるかた", kind="art", shots=[
  dict(key="kakaranai_obi", cast="U2", props=["P_TSUCHOU", "P_KITCHEN"],
       cam="static", lv="mid",
       # L66 所得税はかからなくても、住民税はかかる。
       sc="a Japanese woman of 66 sitting at her kitchen table with the navy "
          "bankbook open in front of her and a small pile of unopened post beside "
          "it, glasses on, one finger on the page",
       mo="She runs her finger down the printed column in the bankbook, stops, "
          "then turns the page and looks down that one too before closing the "
          "book and setting it on top of the pile of post."),
  dict(key="taisho_hirogaru", cast="S1", props=["P_COUNTER", "P_SHINKOKU"],
       cam="parallax", lv="mid",
       # L67 だから、対象が広がりました。
       sc="a Japanese woman in her early thirties in a navy office jacket standing "
          "behind a pale service counter with a tray of cream forms on it and a "
          "numbered ticket stand at one end",
       mo="She takes a handful of forms from the tray, squares them against the "
          "counter top and sets them back down in two separate piles, then moves "
          "the tray a little closer to the front edge."),
]),

dict(L=68, tag="慌てないでください", kind="art", shots=[
  dict(key="totsuzen_todoku", cast="U1", props=["P_POST", "P_ENV"],
       cam="push", lv="mid",
       # L68 一度も受け取ったことのないかたのお宅に、突然、税金の紙が届く。
       sc="a Japanese man of 68 standing at his front door holding the white "
          "window envelope in both hands and looking down at it, the letterbox "
          "lid still open behind his shoulder",
       mo="He turns the envelope over once, looks up from it toward the house, "
          "then reaches back and closes the letterbox lid before stepping inside "
          "with the envelope held against his chest."),
  dict(key="awatenai", cast="U1", props=["P_KITCHEN", "P_ENV", "P_SHINKOKU"],
       cam="static", lv="mid",
       # L69 これは、増税の通知ではありません。控除を受けるための紙です。
       sc="a Japanese man of 68 seated at the kitchen table with the envelope open "
          "and the cream form drawn out of it lying flat, both hands resting on "
          "the table on either side",
       mo="He draws the form fully out and turns it the right way round to face "
          "him, sets the empty envelope aside, then lets his shoulders drop and "
          "sits back a little in the chair."),
  dict(key="son_ni_naru", hands="H_U1", props=["P_SHINKOKU", "P_PEN"],
       cam="push_hard", lv="peak",
       # L70 出さないほうが損になる。そういう性質の紙です。
       sc="a close overhead shot of the cream form on the kitchen table with the "
          "red ballpoint lying across one corner and the thin hands of a man of 68 "
          "at the edges of the sheet",
       mo="He picks the pen up off the corner of the form, uncaps it with one "
          "hand, then sets the cap down on the table and holds the pen above the "
          "first blank box."),
]),

# ══════════════ CHUONG 5 — 期限と救い (L71–L86 · 534,6–659,7s) ════════════
dict(L=71, tag="期限は紙に印刷されている", kind="art", shots=[
  dict(key="itsumade", cast="M3", props=["P_DESK", "P_PAMPH"], cam="static", lv="low",
       # L71–L72 いつまでに出せばいいのか。…載せていません。
       sc="a composed Japanese man in his late sixties seated at the desk with two "
          "leaflets open in front of him, turning the pages of one, the lamp lit "
          "low at his side",
       mo="He turns three pages of the leaflet one after another, looking at each "
          "briefly, then closes it and sets it down on the blotter with his hand "
          "flat on the cover."),
  dict(key="kigen_insatsu", hands="H_M3", props=["P_SHINKOKU", "P_PEN"],
       cam="push_hard", lv="peak",
       # L73 期限は、届いた紙そのものに印刷されています。
       sc="a close overhead shot of the top edge of the cream form on the green "
          "blotter where a short date line is printed, the steady hands of a man "
          "in his late sixties holding the red pen just above it",
       mo="He rings the printed date at the top of the sheet in one stroke, then "
          "taps beside the ring twice with the capped end of the pen and leaves "
          "the pen lying across the top edge of the form."),
  dict(key="gojishin_no_kami", cast="U2", props=["P_SHINKOKU", "P_KITCHEN"],
       cam="push", lv="mid",
       # L73 ですから、ご自身の紙をご覧いただくほかありません。
       sc="a Japanese woman of 66 at her kitchen table holding the cream form up "
          "toward the window light with both hands, her glasses on, head tilted "
          "slightly back",
       mo="She raises the sheet toward the window and turns it a little to catch "
          "the light on the top edge, holds it there while she reads, then lowers "
          "it to the table and keeps one finger on the line."),
]),

dict(L=74, tag="原典③機構・期限に間に合わなくても", kind="genten",
     # 🔴 DOI NGUON 2026-09-04: dung trang **令和9年分** lam chinh, vi tho 申告書
     #    ma video noi den la to 令和9年分 (gui tu 令和8年9月7日 = "この秋" cua cold
     #    open). Trang 令和8年分 giu lam anh thu 2 cho cau さかのぼって…再計算.
     genten=dict(url="https://www.nenkin.go.jp/service/jukyu/tetsuduki/rourei/jukyu/fuyo/2027fuyoukami.html",
                 url2="https://www.nenkin.go.jp/service/jukyu/tetsuduki/rourei/jukyu/fuyo/fuyokami2026.html",
                 verified="2026-09-04",
                 quote="お手元に届きましたら、内容を確認し、各種控除に該当する方は、"
                       "記載されている期限内の提出をお願いします。期限に間に合わない"
                       "場合でも、なるべく早くご提出をお願いします。",
                 # ⭐ cum 「記載されている期限内」 chung minh luon L72-L73 (期限 in tren
                 #    chinh to giay, HP khong ghi ngay) — dung cai ma bai dang noi.
                 quote2="申告書を提出いただくと、令和8年の最初の年金のお支払いまで"
                        "さかのぼって源泉徴収税額の再計算を行います。（令和8年分のページ）",
                 # ✅ SUA LOI 2026-09-04: L75 doi sang 「要点はこうです」 + dung dung
                 #    tu 「期限に間に合わなくても、なるべく早く」 cua trang.
                 mark="trang「令和8年分…扶養親族等申告書の紙の提出方法」— khoanh DO "
                      "hai cau tren; ⚠️ trang KHONG ghi ngay han cu the (dung cho "
                      "L72「締め切りの日付を、ホームページに載せていません」)",
                 shots=2)),

dict(L=76, tag="あとから出せば戻ってくる", kind="art", shots=[
  dict(key="ato_kara", cast="U2", props=["P_SHINKOKU", "P_ENV", "P_KITCHEN"],
       cam="push", lv="mid",
       # L76 出し忘れても、あとから出せば、戻ってきます。
       sc="a Japanese woman of 66 at the kitchen table sliding the filled cream "
          "form into the white window envelope, her glasses pushed up on her head",
       mo="She feeds the form into the envelope, presses the flap down flat with "
          "her thumb, then stands the envelope up against the tea cup so it faces "
          "out and leaves her hand steadying it."),
  dict(key="akiramenai", cast="U2", props=["P_POST", "P_ENV"], cam="parallax", lv="mid",
       # L76 諦めないでください。
       sc="a Japanese woman of 66 standing at the front door with the sealed "
          "envelope in one hand, the other hand on the aluminium letterbox lid, "
          "morning light through the frosted glass",
       mo="She lifts the lid, posts the envelope through it and lets the lid fall "
          "shut, then rests her hand on the closed lid for a moment before "
          "turning back into the house."),
]),

dict(L=78, tag="五年間さかのぼれる", kind="art", shots=[
  dict(key="gonen_sakanobore", hands="H_M3", props=["P_FILE", "P_PEN", "P_RULER"],
       cam="push", lv="mid",
       # L78 還付の申告は、その年の翌年一月一日から、五年間できます。
       sc="a close overhead shot of five cream sheets fanned out in a row on the "
          "green blotter, each with a short date printed at its top edge, the "
          "steady hands of a man in his late sixties laying the ruler along the row",
       mo="He straightens the fan of sheets into an even row with the edge of the "
          "ruler, then draws the ruler back along the row from the far end to the "
          "near one and lifts it clear."),
  dict(key="ima_kara_demo", cast="M3", props=["P_FILE", "P_DESK"],
       cam="static", lv="mid",
       # L79 五年前の分まで、いまからでも取り戻せる。
       sc="a composed Japanese man in his late sixties standing at the desk with "
          "the grey document box open and five sheets stacked on the blotter "
          "beside it, one hand on the stack",
       mo="He gathers the five sheets into one stack, taps their bottom edge "
          "square on the desk, then lays the stack into the box and rests his hand "
          "on the open lid."),
]),

dict(L=80, tag="落とし穴・確定申告不要制度", kind="art", shots=[
  dict(key="otoshiana", still=True, cast="M3", props=["P_BOARD"], cam="push", lv="mid",
       # L80 ここに、多くのかたが引っかかる落とし穴があります。
       sc="a composed Japanese man in his late sixties at the cleared whiteboard "
           "with the marker uncapped in his hand, standing to the left of the "
           "clean board",
       mo="He draws a wide shallow curve across the middle of the board, then a "
           "small circle sitting in the dip of the curve, and steps back one pace "
           "to look at it, holding the marker at his side."),
  dict(key="fuyou_seido", cast="U2", props=["P_PAMPH", "P_KITCHEN"],
       cam="static", lv="mid",
       # L81–L82 確定申告不要制度…この二つを両方みたすかた
       sc="a Japanese woman of 66 at her kitchen table with the thin leaflet open "
          "in front of her, glasses on, one hand holding the page flat and the "
          "other at her chin",
       mo="She reads down the open page, turns to the next and reads that too, "
          "then lays the leaflet flat and smooths the crease with her palm and "
          "keeps her hand there."),
  dict(key="benri_ni_kikoeru", cast="U2", props=["P_PAMPH"], cam="push", lv="mid",
       # L83 便利な制度に聞こえますよね。ところが、その続きが…
       sc="a Japanese woman of 66 holding the open leaflet up in both hands at "
          "reading distance, glasses on, the kitchen soft behind her",
       mo="She reads down the page, then turns the leaflet over to look at the "
          "back of it, turns it back again and lowers it slowly to the table with "
          "one hand still holding the page open."),
]),

dict(L=83, tag="原典④国税庁・還付には申告が必要", kind="genten",
     genten=dict(url="https://www.nta.go.jp/publication/pamph/koho/kurashi/html/03_1.htm",
                 verified="2026-09-04",
                 # 🔴 SUA 2026-09-04 sau khi chup anh that (nta_full dai y 2500-2600):
                 #    nguyen van la 注1 cua muc 年金所得者の確定申告不要制度, va no
                 #    KHOP loi doc L84 gan nhu tung chu => `said` da bo. WebFetch
                 #    truoc do tra ve mot cau dien giai o cho khac.
                 quote="所得税等の確定申告が必要ない場合であっても、所得税等の還付を"
                       "受けるためには、確定申告書を提出する必要があります。",
                 mark="cung trang ①, muc 源泉徴収税額を超える所得控除等がある場合 — "
                      "khoanh DO ca cau",
                 shots=3)),

dict(L=85, tag="こちらから出す", kind="art", shots=[
  dict(key="kaettekonai", cast="M3", props=["P_DESK", "P_SHINKOKU"],
       cam="static", lv="mid",
       # L85 申告しなくていい、というのは、返ってこない、ということでもある。
       sc="a composed Japanese man in his late sixties seated at the desk with one "
          "cream form lying face up on the blotter and both hands resting flat on "
          "the desk on either side of it",
       mo="He turns the form face down on the blotter, sits looking at the blank "
          "back of it, then turns it face up again and squares it against the edge "
          "of the pad."),
  dict(key="kochira_kara", cast="M3", props=["P_SHINKOKU", "P_ENV", "P_DESK"],
       cam="push_hard", lv="peak",
       # L86 戻してほしいなら、こちらから出す。
       sc="a composed Japanese man in his late sixties standing at the desk "
          "sliding the cream form into the white envelope, the lamp lit and the "
          "leaflets stacked to one side",
       mo="He feeds the form into the envelope, presses the flap flat with his "
          "thumb, then holds the envelope out toward the front of the desk and "
          "sets it down square on the blotter facing away from him."),
]),

# ══════════════ CHUONG 6 — 引かれているもの (L87–L95 · 659,7–723,0s) ══════
dict(L=87, tag="復興特別所得税", kind="art", shots=[
  dict(key="mou_hitotsu", cast="M3", props=["P_DESK", "P_PAMPH", "P_PEN"],
       cam="push", lv="low",
       # L87–L88 引かれた所得税には、復興特別所得税が上乗せされています。
       sc="a composed Japanese man in his late sixties seated at the desk opening "
          "a leaflet to a marked page, the fountain pen already in his other hand, "
          "the lamp lit low",
       mo="He opens the leaflet at the marked page, flattens it with one hand and "
          "moves the pen to a line partway down, then holds the pen there and "
          "leaves his other hand at the top of the page."),
  dict(key="uwanose", still=True, cast="M3", props=["P_BOARD"], cam="static", lv="mid",
       # L89 もとの税率が五パーセント。それに、二・一パーセント分が加わって
       sc="a composed Japanese man in his late sixties at the whiteboard with one "
           "short thick stroke drawn on a clean board, marker in hand, standing "
           "clear of the board",
       mo="He draws a much smaller stroke above and to the right of the first, "
           "then a plus sign between them and a line beneath, and lowers the "
           "marker without adding anything else."),
]),

dict(L=89, tag="五％＋二・一％分＝五・一〇五％", kind="formula",
     formula="5％ ＋ 2.1％分 ＝ 5.105％", peak=False),

dict(L=91, tag="特別徴収・引かれているもの", kind="art", shots=[
  dict(key="zeikin_dake_de_nai", cast="M3", props=["P_DESK", "P_FILE"],
       cam="push", lv="mid",
       # L91 年金から引かれているのは、税金だけではありません。
       sc="a composed Japanese man in his late sixties standing at the desk laying "
          "four separate sheets out in a row on the blotter, two already down and "
          "two in his hand",
       mo="He lays the two sheets in his hand down at the end of the row, then "
          "moves along the row squaring each one against the next, and stops with "
          "his hand on the last sheet."),
  dict(key="tokubetsu_choushuu", cast="U2", props=["P_TSUCHOU", "P_KITCHEN"],
       cam="static", lv="mid",
       # L92–L93 介護保険料…住民税。／これらが年金から直接引かれます。
       sc="a Japanese woman of 66 at her kitchen table with the navy bankbook open "
          "and a small stack of notices beside it, glasses on, one hand on the "
          "bankbook page",
       mo="She sets the bankbook down open, takes the top notice off the stack and "
          "lays it beside the book, then moves her finger from one to the other "
          "and back and leaves it resting on the bankbook."),
  dict(key="furikomi_sa", hands="H_M1", props=["P_TSUCHI", "P_TSUCHOU", "P_PEN"],
       cam="push_hard", lv="peak",
       # L94 振込通知書に書かれている金額と、実際に口座に入る金額は、違います。
       sc="a close overhead shot of the pale-green notice and the open navy "
          "bankbook lying side by side on the kitchen table, the broad hands of a "
          "man of 65 holding the red pen above them",
       mo="He rings one figure on the notice, moves the pen across and rings the "
          "matching figure in the bankbook, then draws a short line in the air "
          "between the two rings and sets the pen down between them."),
]),

dict(L=94, tag="手取りを守る第一歩", kind="art", shots=[
  dict(key="hitotsuzutsu", cast="M1", props=["P_KITCHEN", "P_TSUCHI", "P_CALC"],
       cam="push", lv="mid",
       # L95 引かれるものを、ひとつずつ確かめておく。
       sc="a Japanese man of 65 seated at the kitchen table with the pale-green "
          "notice open, the calculator beside it and his glasses on, one finger at "
          "the top of the column of figures",
       mo="He moves his finger down the column one line at a time, pressing a key "
          "on the calculator after each, reaches the foot of the column and lifts "
          "his hand, then looks at the display."),
  dict(key="tedori_mamoru", cast="M1", props=["P_KITCHEN", "P_TSUCHOU"],
       cam="static", lv="low",
       # L95 それが、手取りを守る第一歩になります。
       sc="a Japanese man of 65 at the kitchen table closing the navy bankbook "
          "with both hands, the notice folded beside him, morning light across "
          "the table",
       mo="He closes the bankbook, folds the notice in half along its crease and "
          "lays the book on top of it, then squares the small pile with both hands "
          "and leaves them resting there."),
]),

# ══════════════ 研究ノート (L96–L101 · 723,0–767,2s) ═════════════════════
# 44,2s — CO Y giu MOT bang 5 dong, khong che lam hai bang ngan
# (`audience-45plus.md` §2.0c: bang 2 dong la "nen trong"; scene so lieu duoc
#  MIEN san 9s vi build-on tung dong chinh la chuyen dong).
dict(L=96, tag="研究ノート", kind="stat", stat=[
    ("所得税が引かれる線（65歳以上）", "205万円"),
    ("来年分は", "214万円"),
    ("紙を出しても出さなくても税率は", "5.105％で同じ"),
    ("配偶者の控除だけで", "年およそ2万円"),
    ("*来年分から届くのは", "年金148万円以上"),
]),

# ══════════════ まとめ・三つの確認 (L102–L106 · 767,2–818,8s) ════════════
dict(L=102, tag="三つだけ確かめてください", kind="art", shots=[
  dict(key="kakunin_hizuke", cast="U2", props=["P_SHINKOKU", "P_KITCHEN", "P_PEN"],
       cam="push", lv="mid",
       # L103 ひとつ。封筒は届きましたか。期限の日付を、まず見てください。
       sc="a Japanese woman of 66 at the kitchen table with the cream form open in "
          "front of her and the red pen in her hand, glasses on, leaning over the "
          "top edge of the sheet",
       mo="She rings the printed date at the top of the form, sets the pen down "
          "across the corner, then slides the sheet a little away from her and "
          "looks at the ringed date from there."),
  dict(key="kazoku_ran", cast="U2", props=["P_SHINKOKU", "P_PEN"],
       cam="push", lv="mid",
       # L104 ふたつ。収入の少ないかたはいらっしゃいませんか。その欄が控除に。
       sc="a close shot from the side of the cream form on the table with the "
          "column of empty boxes toward the camera, the hands of a woman of 66 "
          "holding the pen at the first box",
       mo="She writes a short stroke in the first box, moves down and writes "
          "another in the second, then lifts the pen and runs her thumb down the "
          "edge of the column to the bottom."),
  dict(key="dashiwasure", cast="U2", props=["P_FILE", "P_DESK"],
       cam="parallax", lv="mid",
       # L105 みっつ。過去に出し忘れた年はありませんか。
       sc="a Japanese woman of 66 standing at a desk with the grey document box "
          "open and a handful of old sheets held up in one hand, the lamp lit "
          "beside her",
       mo="She turns the old sheets over one at a time, holding each up briefly, "
          "sets three of them aside on the desk and puts the rest back into the "
          "box, then rests her hand on the three she kept."),
  dict(key="gonen_inai", cast="U2", props=["P_NENPYO", "P_PEN"],
       cam="push", lv="mid",
       # L105 五年以内なら、確定申告で取り戻せます。
       sc="a Japanese woman of 66 standing at the paper wall calendar with the red "
          "pen raised and her glasses on, the calendar sheet hanging a little "
          "crooked on its nail",
       mo="She straightens the calendar sheet on its nail with one hand, then "
          "rings one square with the pen and steps back half a pace, holding the "
          "pen down at her side."),
]),

dict(L=106, tag="時点情報・ご確認ください", kind="art", shots=[
  dict(key="jiten_joho", cast="M3", props=["P_DESK", "P_PAMPH"],
       cam="static", lv="low",
       # L106 令和八年八月時点の情報です。税制は毎年改正されますし…
       sc="a composed Japanese man in his late sixties seated at the desk with the "
          "two leaflets closed and squared in front of him, both hands resting on "
          "the top cover, the lamp lit low",
       mo="He squares the two leaflets together with both hands, slides them to "
          "the centre of the blotter, then folds his hands on top of the stack and "
          "sits still."),
  dict(key="madoguchi_de", cast="S1", props=["P_COUNTER", "P_SHINKOKU"],
       cam="parallax", lv="mid",
       # L106 お近くの税務署、または年金事務所でご確認ください。
       sc="a Japanese woman in her early thirties in a navy office jacket standing "
          "behind the pale service counter, one cream form laid on the document "
          "tray in front of her and the ticket stand at the end of the counter",
       mo="She takes the form from the tray, turns it round to face the front of "
          "the counter and sets it down there, then moves the tray aside and rests "
          "one hand on the counter edge."),
  dict(key="madoguchi_te", cast="U2", props=["P_COUNTER", "P_ENV"],
       cam="push", lv="mid",
       # L106 (canh nguoi xem mang giay den quay)
       sc="a Japanese woman of 66 standing at the front of a pale service "
           "counter with one white envelope already lying on the counter in "
           "front of her, both hands resting on the counter edge, the acrylic "
           "partition beside her",
       mo="She looks down at the envelope on the counter, then lifts her eyes "
           "toward the far side of the counter and waits, hands still resting "
           "where they are."),
]),

# ══════════════ 次回予告 + 締め (L107–L113 · 818,8–855,9s) ════════════════
dict(L=107, tag="次回・未支給年金", kind="art", shots=[
  dict(key="jikai_hako", cast="M3", props=["P_DESK", "P_FILE"], cam="push", lv="mid",
       # L107–L108 次回です。…まだ受け取っていない年金が残ります。
       sc="a composed Japanese man in his late sixties standing at the desk with "
          "the grey document box closed and one unopened white envelope resting on "
          "its lid, his hand at the corner of the box",
       mo="He picks the envelope up off the lid, turns it over once in his hand, "
          "then stands it upright against the side of the box and leaves it "
          "leaning there."),
  dict(key="nikagetsu_bun", hands="H_M3", props=["P_TSUCHOU", "P_PEN"],
       cam="static", lv="mid",
       # L109 年金は、二か月分をまとめて、あとから振り込まれる仕組み。
       sc="a close overhead shot of the open navy bankbook on the green blotter "
          "showing a column of printed figures, the steady hands of a man in his "
          "late sixties with the pen held above two adjacent lines",
       mo="He brackets two adjacent lines in the bankbook with one stroke of the "
          "pen, then moves down and brackets the next two the same way, and lays "
          "the pen along the edge of the page."),
]),

dict(L=110, tag="請求しなければ渡らない", kind="art", shots=[
  dict(key="kieru_wake_denai", cast="M3", props=["P_DESK", "P_ENV"],
       cam="push_hard", lv="peak",
       # L110 そのお金は、消えるわけではありません。ご家族が、請求できます。
       sc="a composed Japanese man in his late sixties at the desk holding the "
          "white envelope upright in one hand at chest height, the closed document "
          "box behind it, the lamp lit",
       mo="He holds the envelope up and turns it so the front faces the camera, "
          "then lowers it to the blotter and sets it down flat, keeping two "
          "fingers on it."),
  dict(key="seikyuu_shinakereba", cast="M3", props=["P_DESK", "P_ENV"],
       cam="static", lv="mid",
       # L111–L112 請求しなければ、誰の手にも渡りません。／一緒に確かめます。
       sc="a composed Japanese man in his late sixties seated at the desk with the "
          "white envelope lying flat in front of him and both hands resting on the "
          "blotter on either side of it",
       mo="He slides the envelope to the centre of the blotter, straightens it "
          "square to the edge of the desk with two fingers, then folds his hands "
          "in front of it and sits still."),
]),

dict(L=113, tag="締め・また次回", kind="art", shots=[
  dict(key="shime_mata", cast="M3", props=["P_DESK"], cam="pull_out", lv="low",
       # L113 それでは、また次回の研究でお会いしましょう。
       sc="a composed Japanese man in his late sixties standing beside the "
          "dark-wood desk with the lamp lit and the leaflets and box squared away "
          "on the blotter, one hand on the back of the chair",
       mo="He pushes the chair in to the desk, rests his hand on its back for a "
          "moment, then reaches over and turns the lamp off and stands in the "
          "softer light."),
]),

]
