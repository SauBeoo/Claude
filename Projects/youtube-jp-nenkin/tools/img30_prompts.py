# -*- coding: utf-8 -*-
r"""img30_prompts.py — sinh prompt ảnh cho các ô của video 30 (10月15日の年金振込).

KHUÔN: y nguyên v27/v28/v29 — vector phẳng clip-art công ích Nhật, nền kem một tông, đúng 3 màu
+ kem, không đổ bóng. STYLE / style_text **import từ `img28_prompts`**, không chép lại.

⭐⭐ KHÁC v29 MỘT CHỖ — **KHOÁ THEO CUE VĂN BẢN, KHÔNG THEO CHỈ SỐ DÒNG.**
v29 khoá theo dải chỉ số dòng `_TTS.md`. Nhưng `make_timeline_exact` **bỏ dòng chú thích**
`<!-- PAYOFF -->` ⇒ chỉ số timeline lệch 1–2 so với chỉ số `_TTS.md` sau mỗi marker (v30: 188
dòng TTS → 186 dòng timeline). Khoá bằng một mẩu lời đọc thì không trôi dù thêm/bớt câu hay
marker. Mỗi mục phủ từ dòng chứa cue của nó tới trước dòng chứa cue của mục kế.

LUẬT RIÊNG BÀI 30:
  1. ⛔ **KHÔNG LỊCH, KHÔNG ĐỒNG HỒ** dù bài nói 「犯人は、カレンダー」 — lịch là vật mời gọi số
     (`ai-video-regen.md` §3). Nửa năm trước / nửa năm sau vẽ bằng **hai phong bì quỹ tiết kiệm:
     một gắn cành hoa xuân, một gắn lá phong đỏ** — trục vật xuyên bài. 「カレンダーに書き込む」
     vẽ bằng **mảnh giấy ghi chú dán trên tủ lạnh**.
  2. **Cast cố định trong bài:** 中村 = bà cụ tóc xám cắt ngắn, áo len màu mù tạt · 加藤 = ông cụ
     tóc bạc thưa, áo sơ mi xanh da trời (khớp thumbnail v30). Khác giới để 2 người đứng cạnh
     nhau vẫn phân biệt ngay.
  3. ⛔ Không xin SỐ ở bất kỳ ô nào — số do font builder vẽ. Chữ Nhật đọc được: ≤7 ký, danh từ.
  4. ⛔ Cấm `blank` / `empty` / `text-free` trong subject.

CHẠY:  python tools/img30_prompts.py   → img30_FLOW.txt · img30_TENFILE.txt · img30_BLOCKS.md
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from img28_prompts import STYLE, style_text  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "30_nenkin-furikomi-10gatsu-fueru-hito"
VD = PROJ / "06_VIDEO" / STEM

NAKA = ("an elderly Japanese woman with short grey hair in a bob, in a mustard-yellow cardigan "
        "over a white blouse")
KATO = ("an elderly Japanese man with thinning white hair, in a light sky-blue collared shirt")
ENV2 = ("two paper savings envelopes lying side by side, the left one tied with a small sprig of "
        "pink spring blossom, the right one with a single red maple leaf tucked under its flap")

D_TSUCHI = ("決定通知書", ["介護保険料", "段階", "課税"])
D_DANKAI = ("決定通知書", ["段階"])
D_KAZEI = ("決定通知書", ["課税"])
D_FURI = ("振込通知書", ["年金", "振込額"])
D_KAIGO = ("介護保険料", ["年金から"])
D_KYUYO = ("給与明細", ["支給", "控除"])
D_SEKOU = ("施行令", ["介護保険"])
D_NOTE = ("研究ノート", ["介護保険料"])

GENTEN = [  # (cue mở, cue kết — dòng KẾT không thuộc 原典, file)
    ("こちらが、日本年金機構のページ", "つまり、6月の紙の10月の欄", "genten_yoteigaku_nenkin.png"),
    ("こちらが、世田谷区の", "つまり、4月から8月まで", "genten_kari_setagaya.png"),
    ("こちらが、新潟市の、介護保険料の表", "ところが、春から夏まで", "genten_dankai_niigata.png"),
    ("こちらが、新潟市のページです", "住民税は下がったのに", "genten_minashi_niigata.png"),
]

# (cue, subject | [biến thể…], DOC?)
S = [
 ("10月15日の朝。", [
    "A bank passbook-update machine in the corner of a bank lobby, an elderly hand feeding an "
    "open passbook into its slot.",
    "An open bank passbook held in two elderly hands, the thumb pressing just below the last "
    "printed row, the fingers tense."]),
 ("年金が、こっそり", [
    "Three things laid in a row on a table under a round magnifying glass: a thick pension "
    "booklet, a postcard, and a telephone handset lying on its side.",
    "An elderly woman at her kitchen table holding a telephone receiver half raised, "
    "hesitating, a postcard lying in front of her."]),
 ("しかも同じ朝", KATO + " at a small dining table, smiling down at an open bank passbook, one "
                  "hand resting relaxed on the table."),
 ("ところが、そのほっとした", KATO + " at the same table, his smile tightening as a single red "
                         "maple leaf drifts past the window behind him."),
 ("答えは、7月ごろ", ["An A4 municipal notice lying on a table with three places on it circled "
                     "in warm red marker, a pencil beside it.",
                     "An elderly hand pulling an A4 folded notice out of a long envelope.",
                     "An A4 notice lying beside its opened long envelope on a table, the flap "
                     "torn neatly along the top."],
  D_TSUCHI),
 ("当研究室は", "A tidy desk with an open research notebook, a pencil and a small stack of "
               "municipal notices held by a clip, a magnifying glass resting on the notebook."),
 ("一つ目の容疑者", ["A thick pension booklet lying closed on a table, an elderly hand resting "
                    "flat on its cover, a cup of green tea beside it.",
                    "An elderly man turning the pages of a pension booklet with a puzzled look."]),
 ("二つ目の容疑者", ["A pension postcard held up at reading distance in two hands, a pair of "
                    "reading glasses lying on the table below.",
                    "A pension postcard standing against a teapot on a low table."], D_FURI),
 ("つまり、6月の紙の10月の欄", [
    "A pension postcard lying flat, one column of it lightly traced over with a pencil, the "
    "pencil still resting on the card.",
    "A postman at a gate handing a new postcard to an elderly woman, who takes it with both "
    "hands."]),
 ("では、本当の犯人は", ["An elderly man holding a pension slip in one hand and a small "
                        "premium notice in the other, looking from one to the other.",
                        "A small premium notice lying on top of a pension postcard, a hand "
                        "sliding the notice up to reveal it."], D_KAIGO),
 ("介護保険料は、1年を", [ENV2 + ", on a low wooden table.",
                         ENV2 + ", an elderly hand lifting the spring one."]),
 ("つまり、4月から8月まで", [
    "A faded savings envelope from last year being reused, an elderly hand putting coins into "
    "it, the paper worn soft at the corners.",
    "Three identical faded envelopes lined up in a row, each tied with a pink spring sprig."]),
 ("町内のバス旅行", [
    "A neighbourhood organiser, an elderly woman in an apron, standing at a front door holding "
    "a bundle of small envelopes, a sightseeing bus drawn small in the distance behind her.",
    "A low table in a community hall covered with small savings envelopes, coins and a "
    "sightseeing-bus pamphlet."]),
 ("介護保険料の10月は", [
    "Two hands over an open envelope, one hand adding coins, the other taking a few coins back "
    "out.",
    ENV2 + ", a pencil lying across the maple-leaf envelope."]),
 ("では、この精算で", [NAKA + ", sitting alone at a kotatsu table in a small room, a window "
                      "behind her showing a snowy Japanese town.",
                      NAKA + " reading a notice at a kotatsu table, one hand on her cheek."]),
 ("今年から住民税が", [
    "Six small envelopes in a row, the first three flat, the last three bowed under a tall "
    "stack of coins.",
    NAKA + " looking at three heavy envelopes on the table in front of her, her shoulders "
    "dropped."]),
 ("8月の振込は、およそ", [NAKA + " at a bank passbook machine, frowning at her open passbook.",
                         NAKA + " holding her passbook close to her face, lips pressed "
                         "together."]),
 ("冒頭でお話しした数字", "Two bank passbooks lying open side by side on a table, a finger "
                         "resting on the lower passbook."),
 ("同じ新潟県の新潟市に", [KATO + " sitting at his dining table in a tidy house, a rice field "
                         "visible through the window.",
                         KATO + " greeting the viewer with a small bow at his front door."]),
 ("この春まで", [KATO + " waving at his front door as his adult son in a suit walks away pulling "
                "a suitcase, moving boxes stacked in the hallway.",
                "A hallway with two taped moving boxes and a suitcase by the door, a pair of "
                "business shoes on the step."]),
 ("いまでも、ご飯", "A rice cooker on a kitchen counter beside several small portions of rice "
                   "wrapped in cling film ready for the freezer."),
 ("次男が出ていくと", [KATO + " alone at a dining table set for one, a second chair pushed in "
                      "neatly.",
                      "An elderly man handing a residence form across a municipal counter to "
                      "a clerk."]),
 ("去年度は、住民税を払う", [
    "An A4 notice held in two hands, one row near the middle circled in red marker.",
    "Two A4 notices side by side, the left one with a row circled high up, the right one with "
    "a row circled lower down."], D_DANKAI),
 ("ところが、春から夏まで", [
    "Three identical envelopes tied with pink spring sprigs lined up on a table, each with the "
    "same neat stack of coins in front of it.",
    KATO + " looking at three equal stacks of coins on his table, puzzled."]),
 ("では、10月には", [
    "Two pension slips lying side by side on a table, the left one with a pink spring-blossom "
    "sticker in its corner, the right one with a red maple-leaf sticker.",
    "A hand laying the maple-leaf slip down next to the blossom slip.",
    "Two pension slips pinned side by side on a cork board, a pink blossom sticker on the left "
    "one and a red maple-leaf sticker on the right one."]),
 ("8月より、9千600円、多く", KATO + " at the passbook machine, pleasantly surprised, a small "
                        "open-mouthed smile."),
 ("「息子がいなくなって", [KATO + " on the telephone at home, smiling and a little bewildered, "
                          "his free hand holding a notice.",
                          KATO + " sitting back in his chair with the notice on his knee, "
                          "looking out of the window."]),
 ("では、年金は上がった", [
    "A pension booklet lying unchanged on the table, and beside it three small envelopes with "
    "maple leaves, each with the same small stack of coins.",
    "An elderly hand placing a small stack of coins on the third maple-leaf envelope."]),
 ("同じ新潟県で、同じ10月15日", [
    "Two panels side by side: on the left " + NAKA + " frowning at her passbook, on the right "
    + KATO + " smiling at his.",
    "Two bank passbooks lying open on a table, one on each side of a thin navy divider."]),
 ("ただ、この話には", [KATO + " smiling over his tea, and a single red maple leaf resting on "
                      "the window sill behind him.",
                      "A single red maple leaf lying beside a teacup on a dining table, an elderly "
                      "hand just about to pick it up."]),
 ("今日は、介護保険料だけで", "Several different notices fanned out on a table, one pulled "
                            "forward, the others pushed a little to the side."),
 ("では、あなたは、どちらの側", ["An elderly hand pulling an A4 folded notice out of a long "
                               "envelope at a kitchen table.",
                               "An A4 notice unfolded on a table, a pair of reading glasses "
                               "placed on top of it."], D_TSUCHI),
 ("一つ目の場所は", ["An A4 notice with a small monthly table, one finger resting on a single "
                    "column of the table.",
                    "Two fingers resting on two neighbouring columns of a small table printed "
                    "on a notice."], D_TSUCHI),
 ("減る側だと分かった", NAKA + " breathing out with one hand on her chest, relieved, the notice "
                       "lying calmly on the table."),
 ("その差が、そのまま", ["Three different notices laid out in a row with a pencil resting on "
                        "the middle one.",
                        "An elderly hand writing a short note in the margin of a notice with a "
                        "pencil."]),
 ("二つ目の場所は", ["An A4 notice with one line circled in red marker and a hand pointing at it.",
                    "A magnifying glass held over one line of an A4 notice."], D_DANKAI),
 ("そして、三つ目の場所が", ["A magnifying glass held over a small box near the bottom of an A4 "
                            "notice.",
                            "An elderly couple leaning over one notice together at a table."],
  D_KAZEI),
 ("ここで、ひとつだけお願い", ["A small wooden community notice board with a hand-written "
                              "thank-you card pinned to it.",
                              "A cup of tea and a folded letter on a small table by a window."]),
 ("冒頭でお約束した", "A magnifying glass lying on an A4 notice, just beside one small box near "
                     "its lower edge.", D_KAZEI),
 ("パートなどの給料から", ["A middle-aged Japanese woman in a supermarket apron at a checkout "
                          "counter, smiling at a customer.",
                          "A pay envelope and a pay slip lying on a kitchen table beside a "
                          "handbag."]),
 ("ところが、介護保険料は、3年", ["Three account books standing upright in a row on a shelf, "
                                "held between two bookends.",
                                "Three account books on a table, the third one open with a "
                                "pencil in it."]),
 ("そこで国は", ["An official document with a round red seal lying on a wooden desk in a "
                "government office.",
                "A clerk in a government office stamping a document."], D_SEKOU),
 ("東京都の練馬区が出している", [
    "A pay slip lying on a table with a pencil and a small hand calculator beside it.",
    "Two pay slips side by side on a table, a hand holding a pencil above them.",
    "A middle-aged woman in a shop apron holding a pay slip up to read it by the window."], D_KYUYO),
 ("住民税は下がったのに", [NAKA + " holding two notices, one in each hand, looking at the "
                          "heavier one with surprise.",
                          "Two notices on a table: a thin one on the left and a thicker one "
                          "on the right held down by a hand."]),
 ("ご自分は年金だけで", "An elderly mother at a dining table and her adult daughter in a "
                       "part-time shop apron standing behind her chair, both looking at one "
                       "notice."),
 ("ここで、救いが一つ", ["An elderly couple smiling at a notice on their table, the wife patting "
                        "her husband's arm.",
                        "A municipal clerk handing back a notice with a friendly nod to an "
                        "elderly woman.",
                        "An elderly woman smiling with relief as she slides a notice back into "
                        "its envelope."]),
 ("そして、この扱いは", ["A municipal counter with a clerk explaining a notice to an elderly "
                        "man, pointing with a pen.",
                        "An elderly man walking out of a municipal office, a notice folded "
                        "in his hand."]),
 ("では最後に、冒頭の", [KATO + " at his table with the two savings envelopes in front of him, "
                        "the blossom one and the maple-leaf one.",
                        KATO + " picking up the maple-leaf envelope and looking at it "
                        "thoughtfully."]),
 ("前半の3回は、今年の2月", ["Three envelopes with pink spring sprigs, each with only a small thin stack of "
                "coins in front of it.",
                KATO + " smiling a little at his passbook in spring, blossom outside the "
                "window."]),
 ("では、来年も", ["Six envelopes in a row, the three blossom ones light, the three maple-leaf "
                 "ones heavy with tall stacks of coins.",
                 KATO + " looking at three heavy maple-leaf envelopes."]),
 ("来年の10月の振込は", [KATO + " at the passbook machine in autumn, surprised and frowning, "
                        "red maple leaves outside the bank window.",
                        KATO + " holding his passbook with both hands, his mouth slightly "
                        "open."]),
 ("1年分で見れば", ["Two cupped elderly hands passing the same pile of coins from one hand to "
                   "the other.",
                   ENV2 + ", a single pile of coins sitting exactly between them."]),
 ("では、加藤さんは", [KATO + " writing with a pencil on a small paper note stuck to his fridge "
                      "door.",
                      "A small paper note held on a fridge door by a round magnet, a pencil "
                      "hanging beside it on a string."]),
 ("「年金が増えたんじゃなくて", [KATO + " sitting calmly by the window with a cup of tea in the "
                               "morning light.",
                               KATO + " folding his notice neatly and putting it back in its "
                               "envelope, smiling."]),
 ("それでは、今日の研究ノート", [
    "An open research notebook on a desk with a pencil and a small stack of notices.",
    "An elderly hand turning a page of an open research notebook.",
    "An open research notebook with a small red check drawn beside a line.",
    "A research notebook closed on top of a notice, a pencil lying across it.",
    "An open research notebook beside two small savings envelopes, one with a pink blossom "
    "sprig and one with a red maple leaf."], D_NOTE),
 ("今日から、三つだけ", [
    "An elderly hand writing in the margin of a notice with a pencil.",
    "A magnifying glass held over the lower part of a notice.",
    "An elderly man sticking a small paper note onto his fridge door with a magnet."]),
 ("10月15日の朝、通帳の", "An open bank passbook and a notice lying side by side on a table, "
                         "a cup of tea beside them, calm morning light."),
 ("次の年金支給日", ["A bank passbook and a long envelope on a low table beside a small winter "
                    "mandarin orange.",
                    "A pension postcard propped against a teapot on a winter kotatsu."]),
 ("なお、今日お伝えした", ["A municipal counter with a small bell and a stack of leaflets.",
                          "A cup of green tea and a folded notice on a small table by a "
                          "window."]),
]

ABSTRACT = ("navy band", "navy line", "tally stroke", "bracket drawn", "checkbox", "hatched",
            "cream field with", "calendar", "clock")


# ── REDO vòng 1 (soi lô `Tháng 9 24 - 18_19`, 92 ảnh, 2026-09-25) ─────────────────────
# Khoá theo SỐ DÒNG FLOW (1-based) của img30_FLOW.txt — chỉ những dòng này gen lại.
# «một clip hay một lớp?» — 3 lớp + 3 lỗi lẻ:
#   LỚP A — kính lúp soi «ô nhỏ» (d50, d53): ô không có gì tên gọi ⇒ model bịa ký tự giả
#           (「01」「α」) hoặc nhét một hộp các-tông vào trong kính. d49/d86 ĐẠT vì trong kính là
#           CHÍNH nhãn đã khai. ⇒ kính lúp phải soi đúng dòng nhãn, gọi tên nó.
#   LỚP B — «các tờ thông báo khác nhau» KHÔNG kèm doc (d41, d46): model lấp mặt giấy bằng icon
#           (bóng đèn, bánh răng, bắt tay, địa cầu) và glyph giống số (「2」). ⇒ kèm D_TSUCHI cho
#           tờ chính, các tờ còn lại tả bằng dòng kẻ mảnh.
#   LỚP C — thêm người/đồ không xin (d37: 3 phụ nữ; d48: biểu đồ cột + cân + nhân viên).
#           ⇒ tả khung bằng quan hệ với MÉP KHUNG (vật lấp khung), không bằng câu cấm.
#   lẻ — d3 sổ ngân hàng thành laptop có biểu đồ · d21 中村 mặt trống · d22 中村 sai tóc/áo ·
#        d23 chỉ 1 chồng xu thay vì 3 (d72 cùng ý ĐẠT → chép cấu trúc d72).
# CỐ Ý NHẬN (ghi sổ để lượt sau khỏi gen lại): 加藤 áo teal thay vì xanh da trời ở d4/26/27/28/
#   32/36/68/69/71/74/75 — palette 3 màu không có xanh da trời, tóc bạc thưa + nam vẫn nhận ra ·
#   中村 áo teal d24/d45 (cùng lý do) · d14 nhãn phụ li ti 「年金分」「見積の知らせ」 ở rìa ·
#   d31 cành xanh thay vì hoa hồng · d64 hai cột trang trí không số · d47/d51 nét viết nguệch
#   ngoạc không đọc được · lá phong kiểu cờ Canada d37/d69.
NAKA_LOCK = ("the SAME woman in every picture: short grey hair cut in a bob, a mustard-yellow "
             "cardigan over a white blouse, her face drawn with eyes, eyebrows and a small mouth "
             "like every other character")
REDO = {
    3: (KATO + " at a small dining table, smiling down at a small hand-sized bank passbook "
        "booklet with a navy cover, opened flat in his hands like a tiny book with two pages of "
        "fine grey ruled lines, one hand resting relaxed on the table.", None),
    21: ("An elderly Japanese woman, " + NAKA_LOCK + ", sitting alone at a kotatsu table in a "
         "small room, her face calm and a little tired, a window behind her showing a snowy "
         "Japanese town.", None),
    22: ("An elderly Japanese woman, " + NAKA_LOCK + ", reading a notice at a kotatsu table, "
         "one hand on her cheek.", None),
    23: ("Six small envelopes standing in one row: the three on the left each have nothing in "
         "front of them, the three on the right each have their own tall stack of coins in front "
         "of them, so the row reads light, light, light, heavy, heavy, heavy.", None),
    37: ("Seen from directly above, a table top filling the whole frame edge to edge: a closed "
         "pension booklet on the left, and three small envelopes with a red maple leaf on each, "
         "each envelope with the same short stack of coins beside it. Objects only.", None),
    41: ("Four A4 notices fanned out on a table like a hand of cards, the front one pulled "
         "forward and fully visible, the three behind it showing only fine grey ruled lines.",
         D_TSUCHI),
    46: ("Three A4 notices laid out in a row on a table, the middle one printed with the words "
         "below, the left and right ones showing only fine grey ruled lines, a pencil resting "
         "on the middle one.", D_TSUCHI),
    48: ("An A4 notice filling most of the frame from top edge to bottom edge, its one printed "
         "row circled in red marker, an elderly hand coming in from the lower right with the "
         "index finger pointing at the circled row. Only the notice and the hand.", D_DANKAI),
    50: ("A round magnifying glass held over the printed word near the bottom of an A4 notice, "
         "the word seen enlarged and sharp inside the lens.", D_KAZEI),
    53: ("A round magnifying glass lying flat on an A4 notice, its lens resting just beside the "
         "printed word near the lower edge, the word still fully visible next to the lens.",
         D_KAZEI),
}


def build_prompt(subj, doc):
    if doc is None:
        return STYLE + subj
    return style_text(f"「{doc[0]}」", [f"「{x}」" for x in doc[1]]) + subj


def main():
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    txt = [re.sub(r"^(?:\[[^\]]*\])+", "", ln["text"]).strip() for ln in tl]

    def find(cue):
        return [i for i, t in enumerate(txt) if cue in t]

    # ── GATE 1: mỗi cue khớp ĐÚNG 1 dòng timeline ─────────────────────────
    bad = []
    starts = []
    for e in S:
        h = find(e[0])
        if len(h) != 1:
            bad.append((e[0], h))
        else:
            starts.append((h[0], e))
    gz = []
    for a, b, fn in GENTEN:
        ha, hb = find(a), find(b)
        if len(ha) != 1 or len(hb) != 1:
            bad.append((a + " / " + b, ha + hb))
        else:
            gz.append((ha[0], hb[0], fn))
    if bad:
        print("🔴 GATE cue: khớp 0 hoặc >1 dòng —")
        for c, h in bad:
            print(f"     «{c}» -> {h}")
        return 1
    starts.sort(key=lambda x: x[0])
    if starts[0][0] != 0:
        print(f"🔴 GATE phủ: mục đầu bắt đầu ở dòng {starts[0][0]}, phải là 0")
        return 1
    print(f"✅ GATE cue: {len(S)} mục + {len(GENTEN)} 原典, mỗi cue đúng 1 dòng")

    def entry_of(li):
        for a, b, fn in gz:
            if a <= li < b:
                return "GENTEN", fn
        cur = None
        for s0, e in starts:
            if s0 <= li:
                cur = e
        return "S", cur

    plan = VD / "plan30.json"
    shots = json.loads(plan.read_text(encoding="utf-8"))["shots"]
    flow, names, blocks, used, short, prev = [], [], [], {}, [], None
    names_by_flow = []
    for k, sh in enumerate(shots):
        li = sh["lines"][0] if sh["lines"] else prev
        prev = li
        # 原典 thắng nếu BẤT KỲ dòng nào của ô thuộc dải 原典 — câu dẫn 「こちらが…赤で囲んだ」 hay
        # rơi vào GIỮA ô (v30 ô 65: ảnh phiếu lương đè lên đúng lúc đọc câu dẫn 原典 của đỉnh bài)
        gk = [entry_of(x) for x in sh["lines"] if entry_of(x)[0] == "GENTEN"]
        kind, e = gk[0] if gk else entry_of(li)
        if kind == "GENTEN":
            names.append(f"o {k:03d} -> [原典ショット] {e}")
            continue
        vs = e[1] if isinstance(e[1], list) else [e[1]]
        doc = e[2] if len(e) > 2 else None
        n = used.get(e[0], 0)
        used[e[0]] = n + 1
        if n >= len(vs):
            short.append((e[0], n + 1, len(vs)))
            continue
        p = build_prompt(vs[n], doc).replace("\n", " ")
        flow.append(p)
        names.append(f"dong {len(flow)} -> shot_{k:03d}.png   [dong timeline {li}]")
        names_by_flow.append(f"shot_{k:03d}.png")
        blocks.append((k, li, p))

    (VD / "img30_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8", newline="\n")
    (VD / "img30_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8", newline="\n")
    md = [f"# img30 — {len(flow)} prompt ảnh ({len(shots) - len(flow) - len(short)} ô dùng 原典ショット)", ""]
    for k, li, p in blocks:
        md += [f"### shot_{k:03d}  (dòng timeline {li})", "", "```", p, "```", ""]
    (VD / "img30_BLOCKS.md").write_text("\n".join(md), encoding="utf-8", newline="\n")

    guard = [i for i, p in enumerate(flow)
             if max(p.find("NO TEXT"), p.find("READABLE JAPANESE TEXT")) * 100 // len(p) > 15]
    subs = [s for e in S for s in (e[1] if isinstance(e[1], list) else [e[1]])]
    banned = [w for s in subs for w in ("blank", "empty", "text-free") if w in s.lower()]
    abst = [w for s in subs for w in ABSTRACT if w in s.lower()]
    dup = len(flow) - len(set(flow))
    print(f"ô {len(shots)} · prompt {len(flow)} · dài TB {sum(map(len, flow)) // max(1, len(flow))} ký")
    print(f"thiếu biến thể: {len(short)} {short[:8]}")
    print(f"prompt trùng nhau: {dup} (phải 0) · guard >15%: {len(guard)} · từ cấm: {len(banned)} · "
          f"lịch/đồng hồ/hình học: {len(abst)} {abst[:4]}")
    print(f"→ {VD}")

    # ── REDO: file riêng, không đè FLOW gốc ─────────────────────────────────────
    rflow, rnames = [], []
    for d in sorted(REDO):
        subj, doc = REDO[d]
        p = build_prompt(subj, doc).replace("\n", " ")
        rflow.append(p)
        rnames.append(f"redo dong {len(rflow)} -> thay FLOW dong {d} -> {names_by_flow[d - 1]}")
    (VD / "img30_FLOW_REDO1.txt").write_text("\n".join(rflow) + "\n", encoding="utf-8", newline="\n")
    (VD / "img30_TENFILE_REDO1.txt").write_text("\n".join(rnames) + "\n", encoding="utf-8",
                                                newline="\n")
    rguard = [i for i, p in enumerate(rflow)
              if max(p.find("NO TEXT"), p.find("READABLE JAPANESE TEXT")) * 100 // len(p) > 15]
    rban = [w for s, _ in REDO.values() for w in ("blank", "empty", "text-free") if w in s.lower()]
    rabst = [w for s, _ in REDO.values() for w in ABSTRACT if w in s.lower()]
    print(f"REDO1: {len(rflow)} prompt · guard >15%: {len(rguard)} · từ cấm: {len(rban)} · "
          f"lịch/đồng hồ: {len(rabst)}")
    return 1 if (short or guard or banned or abst or dup or rguard or rban or rabst) else 0


if __name__ == "__main__":
    sys.exit(main())
