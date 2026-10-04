# -*- coding: utf-8 -*-
r"""img32_prompts.py — sinh prompt ảnh cho các ô của video 32 (本人確認 2027 · 免許証の暗証番号2つ).

KHUÔN: y nguyên v27–v31 — vector phẳng clip-art công ích Nhật, nền kem một tông, đúng 3 màu + kem,
không đổ bóng. STYLE / style_text import từ `img28_prompts`. Cơ chế (khoá theo CUE văn bản, gate
cue/phủ/guard/từ cấm) chép từ `img31_prompts.py`.

LUẬT RIÊNG BÀI 32:
  1. **Ba mô-típ xuyên bài** (mạch hình khớp mạch lời):
     ① MÁY ĐỌC THẺ nhỏ màu xám trên quầy (cold open → câu đóng 「あの機械の前で」)
     ② TÚI CARDIGAN ĐỎ của 佐藤 với bằng lái + phiếu giảm giá (第2章 → cảnh cuối)
     ③ CHIẾC KHOÁ nhỏ màu teal đặt trên thẻ (「名前を守る鍵」 ở 第4章)
  2. 🔴 MÁY ĐỌC THẺ / BÀN PHÍM: ⛔ không chữ số trên nút — tả 「plain square buttons without any
     markings」. Bàn phím là vật mời gọi số (`ai-video-regen.md` §3) ⇒ gate ABSTRACT chặn 「keypad digits」.
  3. 「あなた」 ở cold open = khách hàng **nhìn từ sau vai** (tóc bạc + vai), không lộ giới tính.
  4. ⛔ Không lịch/đồng hồ. ⛔ Không xin SỐ ở bất kỳ ô nào (kể cả #9110 — do font vẽ).
     Chữ Nhật đọc được: ≤7 ký, danh từ, chỉ ở ô có giấy tờ.
  5. ⛔ Cấm `blank` / `empty` / `text-free` trong subject. ⛔ Không logo/màu nhận diện bưu điện/JA.

CHẠY:  python tools/img32_prompts.py   → img32_FLOW.txt · img32_TENFILE.txt · img32_BLOCKS.md
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from img28_prompts import STYLE, style_text  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "32_ginko-honnin-kakunin-2027"
VD = PROJ / "06_VIDEO" / STEM

YOU = ("an elderly customer seen from behind the shoulder, only short grey hair and the shoulders of a "
       "navy jacket visible")
SATO = ("an elderly Japanese woman with short grey permed hair, in a red cardigan with two front "
        "pockets over a white blouse and navy trousers")
KOBA = ("an elderly Japanese man with white hair only at the sides, in a navy cardigan, holding a "
        "wooden walking cane")
SON = "a Japanese man in his forties in a navy suit talking on a mobile phone"
TELLER = "a young Japanese bank teller in a teal uniform vest"
READER = ("a small grey card reader box with a flat reading pad and a row of plain square buttons "
          "without any markings")
LIC = "a pale blue driving licence card with a small portrait photo area"
MYNA = "a white plastic ID card with a small portrait photo area"
LOCK = "a small teal padlock"

D_NOTE = ("研究ノート", ["暗証番号", "警察署"])
D_TECHO = ("手帳", ["暗証番号"])
D_SHIKAKU = ("資格確認書", ["健康保険"])
D_KEIREKI = ("運転経歴証明書", ["写真付き"])

GENTEN = [  # (cue mở, cue kết — dòng KẾT không thuộc 原典, file)
    ("こちらが、警察庁のチラシ", "これまでは、窓口の人が", "genten_chirashi_top"),
    ("そして、小さな字で", "お使いの銀行によっては", "genten_chirashi_senko"),
    ("こちらは、警察庁の、法律の概要", "つまり、今お使いの口座は", "genten_gaiyou_zumi"),
    ("こちらは、東京の警視庁", "覚えていないのは", "genten_keishicho_pin"),
    ("同じページには、暗証番号を3回", "佐藤さんは、ご主人の誕生日", "genten_keishicho_3kai"),
    ("警視庁のページには、暗証番号を忘れた", "この一行は、あとで", "genten_keishicho_denwa"),
    ("この仕組みは、カードの表に", "お客さんが、暗証番号を打つ", "genten_digital_app"),
    ("警察庁の質問と回答の資料", "ただし、見せたうえで", "genten_qa_keireki"),
    ("同じ警視庁のページの", "中の情報は、真似が", "genten_keishicho_gizou"),
    ("こちらは、金融庁の発表", "狙われているのは", "genten_fsa"),
]

# (cue, subject | [biến thể…], DOC?)
S = [
 # ── 0 はじめに ─────────────────────────────────────────────────────────
 ("2027年の春。", [
    "A small Japanese credit union branch seen from the street in spring, a cherry tree in bloom by "
    "the entrance, an elderly person stepping inside.",
    YOU + ", seated at a bank counter across from " + TELLER + ", cherry blossom visible through "
    "the window."]),
 ("免許証を出すと、机に", [
    TELLER + " placing " + READER + " on the counter in front of " + YOU + ".",
    "Close view of an elderly hand laying " + LIC + " on a bank counter next to " + READER + "."]),
 ("「4桁の暗証番号を", TELLER + " politely gesturing toward " + READER + ", " + YOU +
  " leaning forward, one finger hovering above the buttons."),
 ("口座を作るとき、200万円", [
    "A bank counter with an account opening form, a pen and " + LIC + " laid on it, a stack of "
    "banknote bundles wrapped in paper bands at the side.",
    "A calm bank lobby with a row of counters and a waiting sofa, cherry blossom through the "
    "window."]),
 ("後ろでは、番号札を", "A row of people waiting on a sofa in a bank lobby holding small paper "
                     "queue tickets, seen past the back of " + YOU + "."),
 ("誕生日を打ちます", "Close view of an elderly finger pressing one of the plain square buttons of "
                    + READER + ", a small red warning lamp lit on the box."),
 ("電話番号の、下4桁", YOU + " pausing with a hand raised above " + READER + ", the red lamp lit "
                     "again, the teller waiting quietly."),
 ("3回続けて間違えると、免許証の中", [LIC + " lying on a counter with a big red warning ring drawn around it and "
                        + READER + " beside it, its red lamp glowing.",
                        YOU + " sitting frozen at the counter, one hand on the forehead."]),
 ("いま、ゆうちょや農協", [
    "Several elderly people at home each looking worriedly at a smartphone screen showing a large "
    "red warning triangle, a tea cup on the table.",
    "A street of small houses at evening, speech bubbles containing red warning triangles "
    "floating from window to window."]),
 ("国の資料を、読み比べました", "A research desk with three official booklets laid side by side, "
                              "a magnifying glass and a pencil resting on them."),
 ("本当に起きるのは", "The bank counter scene again seen from the side: " + YOU + " in front of " +
                    READER + ", the teller across the counter."),
 ("その番号を、あなたは", [LIC + " held up in two elderly fingers against a soft light, a large navy "
                        "question mark floating above it.",
                        "A drawer full of old wallets, cards and papers pulled open, an elderly "
                        "hand searching through it."]),
 ("そして、なぜ国は", [LIC + " with " + LOCK + " resting on top of it, lying on a counter.",
                     "An old black telephone on a small wooden stand in a Japanese hallway, its "
                     "receiver off the hook."]),
 ("当研究室は", "A tidy desk with an open research notebook, a pencil and a small stack of official "
              "booklets held by a clip, a magnifying glass resting on the notebook."),
 # ── 1 警察庁のチラシ ─────────────────────────────────────────────────────
 ("冒頭の場面は、どこに", "A magnifying glass held over a flyer pinned to a notice board in a "
                       "police station lobby."),
 ("警察庁が、この6月に", "A single flyer lying on a wooden table beside a cup of green tea, "
                      "early summer light."),
 ("これまでは、窓口の人が", TELLER + " holding " + LIC + " and comparing it with the customer's face "
                        "by eye, the customer seen from behind."),
 ("これからは、カードの中", LIC + " laid flat on the reading pad of " + READER + ", three small "
                        "curved signal arcs rising from the pad."),
 ("郵送で手続きするときは", ["An elderly hand sliding a paper copy of an ID card into a long envelope "
                          "at a kitchen table, a large red cross-out ring over the copy.",
                          "A red street post box with a long envelope half inside the slot."]),
 ("お使いの銀行によっては", "Three different small bank buildings standing side by side along a "
                        "street, one of them with a small navy flag by the door."),
 # ── 2 今ある口座は ───────────────────────────────────────────────────────
 ("では、あなたが、いま気になって", "An open bank passbook lying on a kitchen table beside a pair "
                                 "of reading glasses and a cup of tea."),
 ("つまり、今お使いの口座は", ["An open bank passbook with a big teal ring drawn around it, lying on "
                           "a table in morning light.",
                           "An elderly couple smiling with relief at their kitchen table, a bank "
                           "passbook between them."]),
 ("年金が振り込まれる口座も", "An elderly person at an automatic teller machine in a bank corner, "
                          "calmly taking out a passbook."),
 ("冒頭の場面が起きるのは", ["A bank branch with a paper sign-shaped board on its closed shutter, an "
                          "elderly person reading it on the pavement.",
                          "An elderly person walking into a different, unfamiliar bank branch "
                          "down the street."]),
 ("では、あなたは、その2つを", LIC + " lying on a table under a desk lamp, two small navy question "
                            "marks floating above it."),
 # ── 3 佐藤さんの暗証番号 ─────────────────────────────────────────────────
 ("当研究室のモニター、仙台", [SATO + " standing beside a small white light car in a supermarket "
                           "staff car park, a supermarket apron over her arm.",
                           SATO + " arranging vegetables at a supermarket produce counter."]),
 ("先日、東京にいる息子さん", [SON + " at an office window with city buildings outside.",
                          SATO + " at home answering an old corded telephone, surprised."]),
 ("「口座が止まるって", SATO + " on the telephone in her small living room, one hand pressed to her "
                      "cheek, frowning."),
 ("佐藤さんは、カーディガン", ["Close view of " + LIC + " and a small paper discount coupon being "
                           "pulled out of the pocket of a red cardigan.",
                           SATO + " looking at her driving licence in her palm."]),
 ("そして、暗証番号の話を聞いて", SATO + " laughing awkwardly with one hand over her mouth, the "
                                "driving licence in her other hand."),
 ("免許の更新の日を", "A driving licence centre waiting room with rows of orange plastic chairs "
                    "and people waiting quietly, seen from the back row."),
 ("待合室の、長いすを", "Rows of long plastic benches in a licence centre waiting room, a few "
                     "elderly people sitting with folded hands."),
 ("講習のビデオと", ["A safety lecture room where a television screen shows a simple car and "
                  "pedestrian crossing picture, elderly people watching.",
                  "An eye test chart made of rings with small gaps, printed in navy on a white "
                  "board, a black eye cover paddle hanging beside it."]),
 ("写真を撮るときの", "A photo booth at a licence centre where an elderly person sits upright "
                    "facing a camera on a stand, a clerk behind the camera."),
 ("その番号は、いつ、決めた", "A clerk at a licence centre counter handing a new driving licence "
                          "card to an elderly person, a small grey box with plain buttons on the "
                          "counter between them."),
 ("覚えていないのは", ["A cash card and " + LIC + " lying side by side on a table, a thin navy "
                     "line separating them.",
                     SATO + " shaking her head with a small smile, the licence in her hand."]),
 ("では、思い出せないとき", YOU + " at the counter with a finger hesitating above " + READER + "."),
 ("佐藤さんは、ご主人の誕生日", ["An old framed photograph of a smiling middle-aged Japanese couple "
                           "on a small household altar shelf, a single flower in a vase.",
                           SATO + " putting the licence back in her cardigan pocket, deciding "
                           "not to try."]),
 ("代わりに、次の平日の朝", SATO + " walking toward a small neighbourhood police station building "
                        "in the morning, a red lamp above its door."),
 ("ただし、ここに、もう一行", "An old black telephone on a small wooden stand with a large red "
                          "cross-out ring drawn over it."),
 ("受付の曜日や時間は", "An elderly person reading a notice board at the entrance of a police "
                     "station, a bicycle parked by the wall."),
 ("ここで、ひとつだけお願い", ["An elderly couple on a sofa showing a tablet to their grown-up "
                          "daughter, all three smiling.",
                          "A handwritten letter and a cup of tea on a table by a window."]),
 # ── 4 忘れたときの3つの道 ────────────────────────────────────────────────
 ("では、佐藤さんのように", ["Three paths branching from one point in a small park, each leading "
                         "toward a different small building.",
                         "Three signposts at a fork in a country road, each with a different "
                         "symbol: a police cap, a card, an envelope."]),
 ("一つ目は、今お話しした", [SATO + " at a police station counter handing her driving licence to a "
                         "uniformed officer.",
                         "A uniformed police officer at a counter looking up information on a "
                         "computer screen turned away from the viewer."]),
 ("二つ目は、マイナンバーカード", [MYNA + " lying on a bank counter next to a smartphone on a small "
                             "stand.",
                             TELLER + " holding a smartphone on a stand over " + MYNA + "."]),
 ("お客さんが、暗証番号を打つ", YOU + " sitting relaxed with hands folded in the lap while the teller "
                            "holds a smartphone camera over the ID card."),
 ("作るかどうか迷ったかたも", ["An elderly person at a municipal office counter receiving " + MYNA +
                          " from a clerk, looking uncertain.",
                          MYNA + " and " + LIC + " side by side on a table, a small navy question "
                          "mark between them."]),
 ("三つ目は、中にICチップ", ["A handful of photo ID cards and booklets fanned out on a table.",
                          "An elderly hand holding a card with a portrait photo, no chip "
                          "visible."], D_KEIREKI),
 ("埼玉県川口市の小林さん", [KOBA + " standing in front of a small house with a potted plant, "
                         "smiling.",
                         KOBA + " at a police station counter handing over a driving licence, "
                         "bowing slightly."]),
 ("ただし、見せたうえで", ["A postman on a bicycle handing a long envelope to " + KOBA + " at his "
                        "front gate.",
                        KOBA + " opening a long envelope at his kitchen table."]),
 ("小林さんに、二つ目の道", KOBA + " laughing and tapping the side of his head, a white ID card "
                        "in his other hand."),
 ("健康保険の資格確認書は", ["A health insurance document lying on a table beside a long envelope."],
  D_SHIKAKU),
 ("あなたの財布に入っている", "An open elderly person's wallet on a table with several cards "
                          "tucked in its pockets, one card half pulled out."),
 # ── 5 なぜ国は ───────────────────────────────────────────────────────────
 ("では、冒頭の、もう一つ", LIC + " under a magnifying glass on a navy background, the photo area "
                        "and the chip area enlarged."),
 ("中の情報は、真似が", ["Two driving licence cards side by side, the right one drawn with a crooked "
                       "outline and a red cross-out ring over it.",
                       "A shady figure in a hat at a bank counter holding out a card, the teller "
                       "holding it over " + READER + " whose red lamp is lit."]),
 ("あなたの名前で、誰かが", [LIC + " with " + LOCK + " resting on top of it, glowing softly.",
                         "An elderly person's hand closing " + LOCK + " on a small wooden box "
                         "holding a passbook."]),
 ("では、止められる口座は", "Two bank passbooks on a table: one ordinary, one wrapped in yellow "
                        "caution tape."),
 ("狙われているのは", "A maze-like drawing of paths where coins flow through one narrow passage "
                    "that is blocked by a navy barrier."),
 ("そして、第2章で", "An old black telephone ringing on a stand in a dim hallway, an elderly hand "
                   "hesitating above it."),
 ("本人が、免許証を持って", SATO + " walking up the steps of a police station with her licence in "
                        "hand."),
 ("ですから、口座が止まる前に", ["An elderly person holding a telephone receiver slightly away from "
                            "the ear, suspicious.",
                            "An elderly person hanging up a telephone firmly."]),
 ("少しでもおかしいと思ったら", "An elderly person dialling a telephone calmly at home, a small "
                            "police cap icon floating in a speech bubble beside it."),
 ("次の平日、佐藤さんは", SATO + " at a police station counter while a kindly officer writes on a "
                       "slip of paper."),
 ("その4桁は、何だったと", SATO + " holding a small folded slip of paper, a soft surprised smile."),
 ("ご主人と暮らした、最初の団地", ["A row of old four-storey Japanese apartment blocks from the "
                              "1970s in warm evening light, laundry on the balconies.",
                              "A young Japanese couple in 1970s clothes carrying boxes up the "
                              "stairs of an apartment block."]),
 ("その番号は、手帳に書いて", ["A small notebook being placed at the back of a kitchen drawer by an "
                           "elderly hand.",
                           "A small notebook lying open on a kitchen table next to a pair of reading glasses and a "
                           "pencil."], D_TECHO),
 ("免許証は、また、カーディガン", SATO + " slipping her licence back into her red cardigan pocket "
                             "at her front door, smiling."),
 ("来年の春、あの機械の前で", [SATO + " seated confidently at a bank counter in spring, pressing "
                          "the plain buttons of " + READER + ", the teller smiling.",
                          "The same small credit union branch with a cherry tree in bloom, " +
                          SATO + " walking out of the door."]),
 # ── 6 研究ノート ─────────────────────────────────────────────────────────
 ("それでは、今日の研究ノート", ["An open research notebook with a pencil on a tidy desk."], D_NOTE),
 ("一つ目は、2027年4月1日", [READER + " on a counter beside " + LIC + ".",
                          "A research notebook open beside " + READER + "."]),
 ("三つ目は、免許証の暗証番号", [LIC + " and a small notebook side by side, a pencil between them.",
                            "Two small navy question marks hovering over " + LIC + "."]),
 ("四つ目は、思い出せなければ", "Three small icons in a row on a cream table: a police cap, a white "
                            "ID card, a long envelope."),
 ("五つ目は、この決まりは", LOCK + " resting on a driving licence card beside an old black "
                        "telephone with a red cross-out ring."),
 # ── 7 セルフチェック ─────────────────────────────────────────────────────
 ("最後に、3つだけ", [SATO + " at her kitchen table with her licence and a notebook, pencil in hand.",
                    "A small checklist card with three navy ring marks on a table."]),
 ("お財布の身分証は", "An elderly hand choosing one card from an open wallet on a table."),
 ("番号を確認させてください、という電話が来たら", "An elderly person holding a telephone and shaking the head firmly."),
 ("次の年金支給日の前にも", "An elderly couple at home watching a television together, a cup of tea "
                        "on the low table."),
 ("なお、今日お伝えした", ["An elderly person at a bank counter asking a teller a question, the "
                        "teller explaining with an open pamphlet.",
                        "An elderly couple at home in the evening putting a small notebook away in "
                        "a drawer of a wooden cabinet."]),
]

ABSTRACT = ("tally stroke", "checkbox", "hatched", "calendar", "clock", "pips", "dice", "keypad digits")


# Lô 1 (`Tháng 9 29 - 10_35.zip`, 61/63 ảnh) — soi 1:1 2026-09-29. FLOW dòng → lý do gen lại + subject mới.
REDO1_WHY = {
    12: "LOAI: so ngan hang ve thanh may tinh xach tay",
    25: "LOAI: cong do-trang doc ra cong DEN (anh cua F45)",
    35: "thieu anh trong lo 1",
    45: "thieu anh trong lo 1",
}
REDO1_SUBJ = {
    12: ("A Japanese bank passbook, a small hand-sized booklet with a plain navy cover, opened flat to "
         "show ruled pages, lying on a kitchen table beside a pair of reading glasses and a cup of tea. "
         "It is a paper booklet, never a laptop, never a screen, never a keyboard."),
    25: (SATO + " walking along a quiet street in the morning toward a small square neighbourhood "
         "police box with a navy roof and one round red lamp above its door, a bicycle parked beside "
         "it. No shrine, no temple gate, no red pillars."),
    35: (KOBA + " at a police station counter handing over a driving licence to a uniformed officer, "
         "bowing slightly."),
    45: (SATO + " walking up three low grey concrete steps toward the glass doors of a plain modern "
         "police station building, her driving licence in her hand. No shrine, no temple gate, no red "
         "pillars, no torii."),
}


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

    shots = json.loads((VD / "plan32.json").read_text(encoding="utf-8"))["shots"]
    flow, names, blocks, used, short, prev = [], [], [], {}, [], None
    for k, sh in enumerate(shots):
        # v32: ô KHÔNG có dòng (nửa sau của ô bị chẻ) ⇒ theo dòng CUỐI của ô trước, không phải dòng đầu
        li = sh["lines"][0] if sh["lines"] else prev
        prev = sh["lines"][-1] if sh["lines"] else li
        # v32: ô là 原典 chỉ khi DÒNG ĐẦU nằm trong dải (v31 tính cả ô chỉ chạm câu dẫn ở cuối ⇒ 19/77 ô)
        gk = [entry_of(x) for x in sh["lines"][:1] if entry_of(x)[0] == "GENTEN"]
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

    (VD / "img32_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8", newline="\n")
    (VD / "img32_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8", newline="\n")
    md = [f"# img31 — {len(flow)} prompt ảnh ({len(shots) - len(flow) - len(short)} ô dùng 原典ショット)", ""]
    for k, li, p in blocks:
        md += [f"### shot_{k:03d}  (dòng timeline {li})", "", "```", p, "```", ""]
    (VD / "img32_BLOCKS.md").write_text("\n".join(md), encoding="utf-8", newline="\n")

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

    rflow = [build_prompt(REDO1_SUBJ[d], None).replace(chr(10), " ") for d in sorted(REDO1_WHY)]
    shot_by_line = {int(n.split()[1]): n.split(" -> ")[1].split()[0]
                    for n in names if n.startswith("dong ")}
    rnames = [f"redo dong {i + 1} -> thay FLOW dong {d} -> {shot_by_line[d]}   [{REDO1_WHY[d]}]"
              for i, d in enumerate(sorted(REDO1_WHY))]
    (VD / "img32_FLOW_REDO1.txt").write_text(chr(10).join(rflow) + chr(10), encoding="utf-8", newline=chr(10))
    (VD / "img32_TENFILE_REDO1.txt").write_text(chr(10).join(rnames) + chr(10), encoding="utf-8", newline=chr(10))
    print(f"REDO1: {len(rflow)} prompt → img32_FLOW_REDO1.txt")
    return 1 if (short or guard or banned or abst or dup or long_lab) else 0


if __name__ == "__main__":
    sys.exit(main())
