# -*- coding: utf-8 -*-
r"""img31_prompts.py — sinh prompt ảnh cho các ô của video 31 (扶養親族等申告書 → 非課税世帯 domino).

KHUÔN: y nguyên v27–v30 — vector phẳng clip-art công ích Nhật, nền kem một tông, đúng 3 màu + kem,
không đổ bóng. STYLE / style_text **import từ `img28_prompts`**. Cơ chế (khoá theo CUE văn bản,
gate cue/phủ/guard/từ cấm) chép từ `img30_prompts.py` — đọc docstring ở đó trước khi sửa.

LUẬT RIÊNG BÀI 31:
  1. **Ba mô-típ xuyên bài** (mạch hình khớp mạch lời):
     ① PHONG BÌ kẹp dưới DÂY BUỘC BÓ BÁO CŨ (nguyên nhân, xuất hiện ở hook và được rút ra ở 第4章)
     ② BỐN KHỐI GỖ navy đứng thành hàng rồi đổ lần lượt (4 quân domino = 4 mốc của 2 năm).
        ⛔ khối trơn, KHÔNG chấm/pips — chấm domino là vật mời gọi số (`ai-video-regen.md` §3)
     ③ TÚI お年玉 của bà (đỏ-trắng, không chữ) — cái bị mất ở tháng 12 và được giữ lại ở cảnh cuối.
  2. **Cast:** 木村 chồng = ông cụ tóc xám ngắn, kính tròn, gile len navy · 木村 vợ = bà cụ tóc xám
     búi thấp, cardigan teal, tạp dề hoa đỏ nhỏ (trong palette 3 màu — bài học v30: màu ngoài palette
     bị model đổi thành teal). Cặp đôi đứng cạnh nhau phải phân biệt ngay.
  3. ⛔ Không lịch/đồng hồ (mùa vẽ bằng cây: hoa anh đào xuân · quạt tay hè · lá phong thu · tuyết đông).
  4. ⛔ Không xin SỐ ở bất kỳ ô nào. Chữ Nhật đọc được: ≤7 ký, danh từ, chỉ ở ô có giấy tờ.
  5. ⛔ Cấm `blank` / `empty` / `text-free` trong subject.

CHẠY:  python tools/img31_prompts.py   → img31_FLOW.txt · img31_TENFILE.txt · img31_BLOCKS.md
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from img28_prompts import STYLE, style_text  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "31_fuyo-shinkokusho-hikazei-domino"
VD = PROJ / "06_VIDEO" / STEM

KM = ("an elderly Japanese man with short grey hair and small round glasses, in a navy knitted "
      "vest over a white shirt")
KW = ("an elderly Japanese woman with grey hair tied in a low bun, in a teal cardigan and a small "
      "red-flower apron")
KB = ("a bundle of old newspapers tied with white string for paper recycling, a long envelope "
      "tucked under the string")
BLOCKS = "four plain navy wooden blocks standing on end in one row like dominoes, with no dots or marks"
X = ("a navy card bearing one big bold batsu mark made of two thick bars crossing DIAGONALLY at 45 degrees like a saltire, never an upright plus sign and never a religious cross")
R = "a red card bearing one big bold ring, a thick circle open in the middle"

D_FUYO = ("申告書", ["扶養親族等", "配偶者"])
D_FUYO1 = ("申告書", ["配偶者"])
D_KAISEI = ("税制改正", ["住民税"])
D_JUMIN = ("住民税", ["課税"])
D_KAIGO = ("決定通知書", ["介護保険料", "段階"])
D_NENMATSU = ("年末調整", ["配偶者"])
D_NOTE = ("研究ノート", ["非課税世帯"])

GENTEN = [  # (cue mở, cue kết — dòng KẾT không thuộc 原典, file)
    ("こちらが、日本年金機構のページ", "今年から、この帯のかたにも", "genten_r9"),
    ("こちらが、大阪市の、住民税が課税されない", "では、家族を1人数えるかどうか", "genten_hikazei"),
    ("同じページには、寡婦", "夫を亡くされた女性なら", "genten_kafu"),
    ("年金機構のよくある質問には", "奥さまを数えてもらえない", "genten_mitei"),
    ("こちらが、大阪市の、介護保険料の表", "一通目は、ご主人の分", "genten_kaigo"),
    ("年金生活者支援給付金の条件の一つは", "ご主人が課税になった年", "genten_shien"),
]

# (cue, subject | [biến thể…], DOC?)
S = [
 # ── 0 はじめに ─────────────────────────────────────────────────────────
 ("再来年の7月。", [
    "Two long municipal envelopes lying side by side on a doormat under a mail slot of a Japanese "
    "front door, a round paper fan hanging on the wall above, summer light.",
    "An elderly couple, " + KM + " and " + KW + ", each opening a long envelope at the same kitchen "
    "table, a round paper fan lying between them."]),
 ("二通とも、上がっています", KM + " and " + KW + " each holding an opened notice, both leaning back "
                         "in surprise, two cups of barley tea on the table."),
 ("12月の通帳には", [
    KW + " in a winter coat at a passbook machine in a small post office, frowning at her open "
    "passbook, snow visible through the door.",
    "An open passbook held in two elderly hands in a winter coat, one finger stopped just below the "
    "last printed row."]),
 ("合わせて、年に15万円あまり", "Two notices and an open passbook laid in a row on a table, a pair "
                            "of reading glasses resting on the passbook."),
 ("どの通知にも、理由は", KM + " and " + KW + " looking at three notices spread on their table, "
                        "both puzzled, one hand scratching the back of his head."),
 ("原因は、2年前の秋に", [KB + ", standing by a Japanese front door, a red maple leaf lying on the "
                        "step beside it.",
                        "Close view of " + KB + ", the envelope's corner sticking out."]),
 ("いま届いている、扶養親族", ["An elderly hand taking a long envelope out of a red mailbox at a house "
                          "gate in autumn.",
                          "A long envelope and the document inside it lying on a table."], D_FUYO),
 ("所得税がかからないからと", KM + " kneeling by his front door tying a bundle of old newspapers with "
                          "white string, an envelope slipping in between the papers."),
 ("ところが、この紙が決めるのは", ["A small Japanese two-storey house seen from the street, "
                                  "warm light in the window, an elderly couple visible inside.",
                                  KM + " and " + KW + " standing together at the door of their "
                                  "small house."]),
 ("税金のかからない紙一枚が", "A single long envelope on a table and a bank passbook lying beside it, "
                          "a thin dotted navy line curving from the envelope to the passbook."),
 ("そして、なぜ損をするのは", KW + " cooking at the stove in the foreground, unaware, while " + KM +
                          " stands in the doorway behind her holding a long envelope."),
 ("当研究室は", ["A tidy desk with an open research notebook, a pencil and a small stack of notices "
               "held by a clip, a magnifying glass resting on the notebook.",
               "An elderly couple and an elderly widow walking along the same quiet street, each "
               "carrying a long envelope."]),
 # ── 1 所得税の紙が住民税の紙に ──────────────────────────────────────────
 ("所得税のかからない人にまで", [KM + " reading a document at his table with a puzzled look.",
                            "A document lying on a table beside its long envelope, a pencil on "
                            "top."], D_FUYO),
 ("この紙は、もともと", "A document with a ballpoint pen lying across it on a wooden desk.", D_FUYO1),
 ("変わったのは、令和8年度", ["An official document with a round red seal lying on a wooden desk in "
                          "a government office.",
                          "A clerk in a government office stamping a document."], D_KAISEI),
 ("今年から、この帯のかたにも", ["A postman on a bicycle handing a long envelope to an elderly woman at "
                            "her gate.",
                            "A row of small houses along a street, a postman putting envelopes "
                            "into several of the mailboxes."]),
 ("去年の送り先は", "Two neighbouring house mailboxes on a street: the left one with a long envelope "
                   "sticking out, the right one closed with a small potted plant beside it."),
 ("つまり、税金の紙が来なかった", KW + " at her gate receiving a long envelope for the first time, "
                            "holding it with both hands and looking at it curiously."),
 # ── 2 148万円の線 ───────────────────────────────────────────────────────
 ("では、148万円という", "A magnifying glass held over a long envelope lying on a table."),
 ("年金機構は、単身者の", "An elderly man sitting alone at a small table with a single teacup."),
 ("単身者の、です。", "A single teacup and a single pair of chopsticks on a small table for one."),
 ("なぜ、わざわざ、ひとり暮らし", ["The same small table now with two teacups and two pairs of "
                              "chopsticks, two chairs pulled up.",
                              "An elderly couple sitting down together at a small table with two "
                              "teacups."]),
 ("では、家族を1人数えるかどうか", ["Two panels side by side: on the left an elderly man standing "
                               "alone, on the right the same man standing with his wife, a navy "
                               "line drawn higher above the couple than above the single man.",
                               "A short wooden fence beside a single elderly man and a taller "
                               "fence beside an elderly couple."]),
 ("夫を亡くされた女性なら", [
    "An elderly Japanese widow at a small home altar with a framed photograph and flowers, holding a "
    "document in her hands.",
    "An elderly widow at her table filling in a document with a pen, a small photo frame beside "
    "her."], D_FUYO),
 ("年金の場合、65歳以上なら", ["An elderly hand holding a pencil over a notepad, a small hand "
                          "calculator lying beside it.",
                          "Two small stacks of coins on a table, a pencil laid between them like a "
                          "dividing line."]),
 ("あなたの年金から、110万円を", ["An elderly person pressing the keys of a hand calculator at a "
                               "kitchen table, a notepad beside it.",
                               "Reading glasses, a pencil and a hand calculator on a notepad."]),
 ("その数字が45万円を超えていて", KM + " and " + KW + " leaning over one document together at their "
                            "table.", D_FUYO),
 ("反対に、この紙で受けられる", "An elderly woman living alone reading a document calmly at her table "
                           "and nodding, a cup of tea beside her.", D_FUYO1),
 ("では、線の下に入るお宅で", "A quiet residential street of small Japanese houses, one house in the "
                          "middle with a long envelope in its mailbox."),
 # ── 3 木村さんご夫妻 ─────────────────────────────────────────────────────
 ("冒頭の、通知が二通届いた", [KM + " and " + KW + " standing at the front door of their small house "
                          "in an Osaka side street, greeting the viewer with a small bow.",
                          KM + " and " + KW + " sitting side by side on their veranda."]),
 ("印刷会社を定年まで", [KM + " at his dining table, a framed picture of an old printing press on the "
                      "wall behind him.",
                      KM + " reading a newspaper in his armchair."]),
 ("国民年金を400か月", KW + " in her kitchen, smiling, drying a bowl with a cloth."),
 ("それに、年金生活者支援給付金を", KW + " at a small post office counter, putting her passbook back "
                              "into her handbag with a satisfied look."),
 ("その給付金が振り込まれる12月", [KW + " at a small post office in winter choosing small red-and-white "
                              "gift envelopes from a rack, with no writing on them.",
                              KW + " at home holding a fan of small red-and-white gift envelopes, "
                              "smiling, a grandchild's drawing pinned on the wall."]),
 ("では、ご主人の所得は", KM + " doing a sum with a pencil on a notepad at his table, a hand "
                        "calculator beside him."),
 ("奥さまを家族に数えれば", KM + " and " + KW + " standing side by side, both smiling calmly, a "
                         "navy line drawn well above their heads."),
 ("数えなければ、線は45万円", KM + " standing alone, a navy line drawn just above his shoulders, his "
                          "wife's chair pushed in under the table behind him."),
 ("同じ年金で、紙を出したかどうか", ["Two identical small houses side by side: in front of the left one "
                               "a hand drops an envelope into a red postbox, in front of the right "
                               "one " + KB + ".",
                               "Two identical envelopes side by side, one going into a red postbox, "
                               "the other under the string of a newspaper bundle."]),
 ("以前の研究でお話しした東京の高橋", "An elderly Japanese man in a grey cardigan posting a long "
                                "envelope into a red postbox on a Tokyo street."),
 ("では、木村さんのご主人は", KM + " holding a long envelope and shrugging with a relaxed smile."),
 ("だからこそ、この紙を", "Close view of " + KB + ", by a doorstep."),
 ("この話をしたとき", KM + " sitting at his table looking down at his hands, a little embarrassed."),
 ("「税金かからんのやから", KM + " pointing with a sheepish smile at " + KB + " by his front door."),
 ("封筒は、古紙回収に出す", "A paper recycling collection point on a street corner with several "
                        "bundles of newspapers, one of them with a long envelope under its string."),
 ("会社勤めのころを", ["A 1980s Japanese office with rows of grey steel desks, a woman from the "
                     "general affairs section walking between them handing out forms.",
                     "A young office worker at a steel desk receiving a form from a colleague."]),
 ("配偶者の欄に、奥さまの名前を書いて", "A young Japanese office worker in a white shirt and tie writing on a "
                            "form at his desk, a small round personal seal and red ink pad beside "
                            "it.", D_NENMATSU),
 ("あの紙は、会社が", "A general affairs clerk collecting forms into a wire tray on a desk in a 1980s "
                     "office."),
 ("年金暮らしになると", KM + " at home alone at the doorway, looking out at a quiet street with "
                       "nobody coming."),
 # ── 4 封筒から通帳までの2年 ───────────────────────────────────────────────
 ("では、もしこの封筒が", ["A paper recycling truck collecting newspaper bundles at a street corner.",
                        "A newspaper bundle with an envelope under its string being lifted by a "
                        "recycling worker's gloved hands."]),
 ("来年から、順番に", BLOCKS + ", on a low wooden table."),
 ("ご主人の年金からは、所得税が", KM + " at a passbook machine, calm, looking at his passbook, cherry "
                            "blossoms outside the bank window."),
 ("紙を出さなかった年には", [KM + " and " + KW + " drinking tea on their veranda in spring, relaxed.",
                         BLOCKS + ", all still standing, a teacup beside them."]),
 ("何も起きないから", "A windowsill through the seasons: cherry blossoms outside, a small pot of "
                     "morning glories, the room quiet and tidy."),
 ("奥さまを数えてもらえない", KM + " opening a municipal notice at his table, eyebrows raised in "
                          "surprise.", D_JUMIN),
 ("ところが、住民税そのものの額", BLOCKS + ", the first block tipping forward onto the second."),
 ("本当に重いのは", "The small house of the couple seen from the street, a navy wooden block leaning "
                   "against its front wall."),
 ("ここで、ひとつだけお願い", ["A small wooden community notice board with a hand-written thank-you "
                            "card pinned to it.",
                            "Two elderly neighbours chatting over a low garden hedge, one handing "
                            "the other a folded leaflet."]),
 ("続いて、再来年の7月", ["Two long envelopes lying on a doormat in summer, a round paper fan on the "
                        "floor beside them.",
                        KM + " and " + KW + " each holding an envelope, standing in the hallway."]),
 ("一通目は、ご主人の分", [KM + " reading a notice at the table, fanning himself with a round paper fan.",
                        KM + " holding a notice close to his glasses.",
                        KM + " laying his notice down next to a tall stack of coins."], D_KAIGO),
 ("ご主人の分だけで", KM + " wiping his forehead with a small towel, a notice in his other hand, "
                     "summer light."),
 ("二通目は、奥さまの分", KW + " opening her own notice at the kitchen table.", D_KAIGO),
 ("奥さまご自身の住民税は", KW + " holding her notice in one hand and pointing at herself with the "
                         "other, puzzled."),
 ("それなのに、第2段階", "A notice lying on a table with a tall stack of coins beside it, and a much "
                       "smaller stack of coins beside that."),
 ("奥さまの保険料は、2倍半", KW + " sitting heavily on a kitchen chair, one hand on her cheek."),
 ("そして最後が、再来年の12月", [KW + " in a winter coat entering a small post office, snow on the "
                             "ground.",
                             "A small post office with snow on its roof and a red mailbox in "
                             "front."]),
 ("ご主人が課税になった年の10月分", BLOCKS + ", the third block falling onto the fourth, the first two "
                               "already fallen."),
 ("奥さまの、年に5万6千196円", KW + " holding the small red-and-white gift envelopes with no writing "
                            "on them, looking down at them sadly."),
 ("では、2年間で倒れたものを", BLOCKS + ", all four lying fallen in a row on a low wooden table."),
 ("年に、15万9千415円。", KM + " and " + KW + " sitting at opposite ends of their table in silence, "
                        "two notices and a passbook between them."),
 ("冒頭の、15万円あまり", "A long envelope in the foreground of a table and four fallen navy wooden "
                        "blocks behind it."),
 ("今日の計算は、今の大阪市の表", "A municipal office counter with a small bell and a neat stack of "
                            "leaflets."),
 ("ですが、非課税世帯から外れれば", "A small wooden staircase model on a table, a tiny navy wooden "
                               "figure standing one step higher than before."),
 # ── 5 損をするのはだれ ────────────────────────────────────────────────────
 ("では、冒頭の、もう一つの問い", KW + " in the foreground peeling a mandarin orange, " + KM +
                            " behind her holding the long envelope."),
 ("15万9千415円のうち", ["Two piles of coins on a dining table: a small one on the husband's side and a "
                      "much larger one on the wife's side, two teacups marking the two places.",
                      KW + " looking at the larger pile of coins on her side of the table."]),
 ("損の7割は", KW + " alone at the kitchen table with two notices and her gift envelopes in front of "
               "her."),
 ("介護保険料も、給付金も", "A small house drawn as one roof sheltering an elderly husband and wife "
                        "standing side by side under it."),
 ("ご主人の紙一枚が決めていたのは", "A single long envelope resting on the roof of a small model house "
                              "on a table."),
 ("そして、届いた通知のどれにも", "Three notices laid on a table, and far to the side a newspaper "
                            "bundle with an envelope under its string."),
 ("ご主人は、保険料が上がった", KM + " at a supermarket shelf looking at a vegetable price tag, "
                           "sighing."),
 ("奥さまは、給付金が止まった", KW + " on the home telephone, puzzled, her passbook open in her other "
                           "hand."),
 ("では、本当の理由は", "Close view of " + KB + ", the white string pressing the envelope flat."),
 ("木村さんのご主人は、その封筒を", KM + " pulling a long envelope out from under the white string of a "
                              "newspaper bundle."),
 ("食卓で、老眼鏡をかけて", KM + " at the dining table with reading glasses on, carefully writing on "
                         "a document with a pen.", D_FUYO1),
 ("「妻の名前を書くのは", KM + " smiling softly as he writes, his pen stopped for a moment."),
 ("奥さまは、その横で", KW + " quietly pouring green tea into his cup beside him at the table."),
 ("再来年の12月も、お年玉袋", KW + " at the post office in winter happily choosing small red-and-white "
                          "gift envelopes with no writing on them."),
 ("では、もう封筒を捨ててしまって", ["An elderly woman calmly searching through a stack of papers by "
                                "the door.",
                                "An elderly man at home on the telephone, relaxed, a notepad in his "
                                "hand."]),
 ("期限に間に合わない場合でも", "An elderly hand dropping a long envelope into a red postbox."),
 ("それも過ぎてしまったときは", ["A municipal tax counter with a clerk explaining a document to an "
                            "elderly man, pointing with a pen.",
                            "An elderly couple sitting at a municipal consultation counter."]),
 # ── 6 研究ノート ─────────────────────────────────────────────────────────
 ("それでは、今日の研究ノート", [
    "An open research notebook on a desk with a pencil and a small stack of notices.",
    "An elderly hand turning a page of an open research notebook.",
    "An open research notebook with a small red check drawn beside a line.",
    "A research notebook closed on top of a long envelope, a pencil lying across it.",
    "An open research notebook beside four small navy wooden blocks standing in a row."], D_NOTE),
 # ── 7 ○×クイズ ───────────────────────────────────────────────────────────
 ("最後に、○×で", [
    # ⛔ "cross-shaped" ra dấu +/thánh giá (REDO1, 5/5 ô) ⇒ tả × bằng HÌNH HỌC (X/R ở dưới).
    "A researcher's hand holding up two cards side by side: " + R + ", and " + X + ".",
    "On a desk, " + X + ", lying beside a long envelope.",
    X[0].upper() + X[1:] + ", propped against a newspaper bundle tied with string.",
    X[0].upper() + X[1:] + ", standing in front of a red postbox.",
    "Three cards laid in a row on a desk beside a research notebook, each one " + X + "."]),
 ("三問とも×だった", "A long envelope placed in the middle of a dining table beside a teacup, "
                    "morning light."),
 ("次の年金支給日", ["A bank passbook and a long envelope on a low table beside a small winter "
                    "mandarin orange.",
                    "A pension passbook propped against a teapot on a winter kotatsu."]),
 # ⛔ bản cũ chép gần y ô 「今日の計算は」(quầy + chuông) và ô CTA (trà + thư bên cửa sổ) — trùng
 # hình trong cùng video (`media-library.md` §2 mục 4) ⇒ đổi bố cục.
 ("なお、今日お伝えした", ["An elderly couple bowing slightly at a municipal office counter as a "
                        "clerk hands them a leaflet.",
                        "An elderly couple at home in the evening putting a folded notice away "
                        "in a drawer of a wooden cabinet."]),
]

ABSTRACT = ("tally stroke", "checkbox", "hatched", "calendar", "clock", "pips", "dice")


# Lô 1 (`Tháng 9 27 - 17_50.zip`, 76/81 ảnh) — soi 1:1 2026-09-27. FLOW dòng → lý do gen lại.
REDO1_WHY = {
    40: "thieu anh trong lo 1",
    41: "thieu anh trong lo 1 + doi bo cuc (trung o F81)",
    73: "LOAI: dau + thay vi x",
    74: "LOAI: thanh gia Latin thay vi x",
    75: "LOAI: dau + thay vi x",
    76: "LOAI: dau + thay vi x",
    77: "LOAI: dau + thay vi x",
    78: "thieu anh trong lo 1",
    80: "thieu anh trong lo 1 + doi bo cuc (trung o F53)",
    81: "thieu anh trong lo 1 + doi bo cuc (trung o F41)",
}
# CỐ Ý NHẬN (lô 1): F20/shot_025 chữ 申告書 xoay 180° vì tờ giấy quay về phía bà — đúng vật lý,
# nét đủ. F28/shot_033 bàn tay bỏ thư thành cậu bé — không lệch nghĩa câu. F56/shot_065 dải trắng
# ngang khung → tô lại ở ingest_art31.BAND. F61/shot_070 bó báo sát mép → VÁ ✦ (ingest PATCH).


def build_prompt(subj, doc):
    if doc is None:
        return STYLE + subj
    return style_text(f"「{doc[0]}」", [f"「{x}」" for x in doc[1]]) + subj


def main():
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    txt = [re.sub(r"^(?:\[[^\]]*\])+", "", ln["text"]).strip() for ln in tl]

    def find(cue):
        # dòng TRÙNG KHÍT cue thắng (dòng mở bài 「再来年の7月。」 cũng là chuỗi con của dòng 88)
        ex = [i for i, t in enumerate(txt) if t == cue]
        return ex or [i for i, t in enumerate(txt) if cue in t]

    bad, starts = [], []
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
    print(f"✅ GATE cue: {len(S)} mục + {len(GENTEN)} dải 原典, mỗi cue đúng 1 dòng")

    def entry_of(li):
        for a, b, fn in gz:
            if a <= li < b:
                return "GENTEN", fn
        cur = None
        for s0, e in starts:
            if s0 <= li:
                cur = e
        return "S", cur

    shots = json.loads((VD / "plan31.json").read_text(encoding="utf-8"))["shots"]
    flow, names, blocks, used, short, prev = [], [], [], {}, [], None
    for k, sh in enumerate(shots):
        li = sh["lines"][0] if sh["lines"] else prev
        prev = li
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
        blocks.append((k, li, p))

    (VD / "img31_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8", newline="\n")
    (VD / "img31_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8", newline="\n")
    md = [f"# img31 — {len(flow)} prompt ảnh ({len(shots) - len(flow) - len(short)} ô dùng 原典ショット)", ""]
    for k, li, p in blocks:
        md += [f"### shot_{k:03d}  (dòng timeline {li})", "", "```", p, "```", ""]
    (VD / "img31_BLOCKS.md").write_text("\n".join(md), encoding="utf-8", newline="\n")

    guard = [i for i, p in enumerate(flow)
             if max(p.find("NO TEXT"), p.find("READABLE JAPANESE TEXT")) * 100 // len(p) > 15]
    subs = [s for e in S for s in (e[1] if isinstance(e[1], list) else [e[1]])]
    banned = [w for s in subs for w in ("blank", "empty", "text-free") if w in s.lower()]
    abst = [w for s in subs for w in ABSTRACT if w in s.lower()]
    labels = [x for e in S if len(e) > 2 for x in [e[2][0]] + e[2][1]]
    long_lab = [x for x in labels if len(x) > 7 or re.search(r"[0-9０-９]", x)]
    dup = len(flow) - len(set(flow))
    unused = [e[0] for e in S if used.get(e[0], 0) == 0]
    print(f"ô {len(shots)} · prompt {len(flow)} · dài TB {sum(map(len, flow)) // max(1, len(flow))} ký")
    print(f"thiếu biến thể: {len(short)} {short[:8]}")
    print(f"cue không ô nào dùng (bị ô khác nuốt): {len(unused)} {unused[:8]}")
    print(f"prompt trùng nhau: {dup} (phải 0) · guard >15%: {len(guard)} · từ cấm: {len(banned)} · "
          f"lịch/đồng hồ/xúc xắc: {len(abst)} {abst[:4]} · nhãn >7 ký hoặc có số: {long_lab}")
    print(f"→ {VD}")

    # ── REDO1: file riêng, không đè FLOW gốc. Lý do từng dòng ghi ở REDO1_WHY ─────────────
    rflow = [flow[d - 1] for d in sorted(REDO1_WHY)]
    shot_by_line = {int(n.split()[1]): n.split(" -> ")[1].split()[0]
                    for n in names if n.startswith("dong ")}
    rnames = [f"redo dong {i + 1} -> thay FLOW dong {d} -> {shot_by_line[d]}   [{REDO1_WHY[d]}]"
              for i, d in enumerate(sorted(REDO1_WHY))]
    (VD / "img31_FLOW_REDO1.txt").write_text("\n".join(rflow) + "\n", encoding="utf-8",
                                             newline="\n")
    (VD / "img31_TENFILE_REDO1.txt").write_text("\n".join(rnames) + "\n", encoding="utf-8",
                                                newline="\n")
    rbad = [d for d in REDO1_WHY if "cross-shaped" in flow[d - 1]]
    print(f"REDO1: {len(rflow)} prompt · còn 'cross-shaped': {rbad}")
    return 1 if (short or guard or banned or abst or dup or long_lab or rbad) else 0


if __name__ == "__main__":
    sys.exit(main())
