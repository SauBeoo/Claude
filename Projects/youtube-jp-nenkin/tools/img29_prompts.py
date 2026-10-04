# -*- coding: utf-8 -*-
r"""img29_prompts.py — sinh prompt ảnh cho các ô của video 29.

KHUÔN: y nguyên v27/v28 — vector phẳng clip-art công ích Nhật, nền kem #F6F1E4 một tông,
đúng 3 màu + kem, không đổ bóng. Máy móc (STYLE / style_text / _BASE) **import từ
`img28_prompts`**, không chép lại — sửa khuôn thì sửa ở đó.

⭐⭐ KHÁC v28 MỘT CHỖ QUAN TRỌNG — **KHOÁ THEO CHỈ SỐ DÒNG, KHÔNG THEO CHỈ SỐ Ô.**
`img28_prompts.py` gắn subject vào `SHOTS[15]`, `SHOTS[16]`… tức **chỉ số ô**. Chỉ số ô do
`plan*.py` sinh ra từ `timeline.json`, mà timeline đổi mỗi lần đổi khoảng nghỉ hoặc sửa một
câu ⇒ **mọi subject lệch một ô, im lặng**. Bài này khoá theo **dải chỉ số DÒNG** của
`_TTS.md` — thứ chỉ đổi khi thật sự thêm/bớt câu. Mỗi ô lấy subject của **dòng đầu tiên** của nó.
📌 Cùng họ bài học `feedback_doi_don_vi_hinh_ra_ca_lo`: đổi đơn vị thì phải rà mọi thứ neo
vào đơn vị cũ. Ở đây tránh hẳn bằng cách **đừng neo vào đơn vị dễ trôi**.

🔴 BỐN LUẬT RIÊNG CỦA BÀI 29:
  1. ⛔ **KHÔNG ô nào được có lưới lịch.** Bài nói dày đặc mốc (8月1日 · 8月2日 · 12か月 ·
     3か月 · 2年). Lịch là **vật mời gọi** — model sẽ điền số lên nó bất kể câu cấm
     (`ai-video-regen.md` §3). Mốc thời gian tả bằng **dải ngang có vạch mốc** hoặc **tờ ghi
     chú dán tường**, không bao giờ bằng lịch. STYLE đã có sẵn `NO CALENDAR GRID`.
  2. **Hai trục vật phải nhận ra xuyên bài:** ① **phong bì vàng nhạt nằm ngang** (ô của dòng
     0, 28–30, 151) ② **hai tờ giấy cỡ thẻ đặt cạnh nhau** — trái là 資格確認書, phải là
     資格情報のお知らせ. Cùng góc nhìn, cùng tỉ lệ, mọi lần xuất hiện.
  3. ⛔ **Cấm mọi chữ `blank` / `empty` / `text-free`** (`CLAUDE.md` §Prompt ảnh). Bài này nói
     về **Ô TRỐNG**, nên rất dễ dính. Cách tả đúng: *«a ruled box drawn in navy outline, the
     inside of the box the same cream as the paper around it»* — tả **cái CÓ MẶT** (đường kẻ,
     màu kem), không tả cái vắng mặt.
  4. ⛔ **Không xin SỐ ở bất kỳ ô nào** — số tiền/ngày/tỉ lệ do **font của builder** vẽ đè
     (`feedback_so_tren_hinh_phai_do_font_ve`). Chữ Nhật đọc được thì XIN (≤7 ký, danh từ).

CHẠY:  python tools/img29_prompts.py             → 3 file trong 06_VIDEO/<stem>/
       python tools/img29_prompts.py --lot 2     → chỉ in lô 2 (mỗi lô 30 ô)
"""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from img28_prompts import STYLE, style_text  # noqa: E402

# 🔴 reconfigure SAU khi import: `img28_prompts` cũng gán `sys.stdout = TextIOWrapper(...)`
# ở tầng module, nên nếu mình bọc TRƯỚC thì wrapper của mình bị thay và đóng lại
# ⇒ `ValueError: I/O operation on closed file` ở dòng print đầu tiên.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "29_shikaku-kakuninsho-8gatsu-85sai"
VD = PROJ / "06_VIDEO" / STEM
LOT = 30

# ── 原典ショット: ô rơi vào các dải này dùng ẢNH CHỤP MÀN HÌNH, không gen ────
GENTEN = {
    (35, 38): "genten_8gatsu1_mhlw.png",       # 厚労省 — 資格確認書 職権交付
    (70, 73): "genten_85sai_chiba.png",        # 千葉県広域連合 — 85歳 + 8月2日 + 6回
    (121, 124): "genten_gendogaku_hyogo.png",  # 兵庫県広域連合 — 限度区分の空欄
}

# ── CHỮ NHẬT ĐỌC ĐƯỢC trên giấy tờ: (tiêu đề, các dòng) · ≤7 ký/cụm, danh từ, KHÔNG số ──
# 「資格情報のお知らせ」 = 9 ký ⇒ vượt trần, rút còn 「資格情報」 (4 ký).
D_KAKUNIN = ("資格確認書", ["氏名", "住所", "限度区分"])
D_OSHIRASE = ("資格情報", ["氏名", "住所"])
D_HOKENSHO = ("保険証", ["氏名", "記号"])
D_RYOYOHI = ("療養費", ["領収書", "明細"])

# ── SUBJECT theo DẢI DÒNG. Mỗi mục: (lo, hi, subject) hoặc (lo, hi, subject, DOC) ──
#    hi là biên PHẢI MỞ (lo ≤ i < hi). Phải phủ kín 0..182, gate ở cuối file kiểm.
S = [
 (0, 2, "A pale yellow envelope lying flat on a wooden table, one card-sized sheet of paper "
        "sliding halfway out of it, seen from straight above."),
 (2, 5, "A hospital reception counter. An elderly Japanese man holds out one small card-sized "
        "sheet across the counter; the receptionist raises one open palm a little, stopping.",
        D_OSHIRASE),
 (5, 7, "Two stacks of coins side by side on a counter, the left stack very short and the right "
        "stack about ten times taller, a thin navy arrow pointing from the short one to the tall one."),
 (7, 9, "Two identical apartment doors side by side, each with a mailbox, and the same pale "
        "yellow envelope sticking out of both mailboxes."),
 (9, 11, "An elderly woman resting a card on a small reader on a clinic counter, and beside her "
         "on the counter a clinic card and a short stack of visit receipts held by a paperclip."),
 (11, 13, "One sheet of paper held in two hands, with a ruled box near its lower edge drawn in "
          "navy outline, the inside of that box the same cream as the paper, and a warm red "
          "circle hand-drawn around that box."),
 (13, 14, "Three things laid in a row on a counter: one printed certificate alone, one printed "
          "notice with a card lying on top of it, and one certificate with a warm red circle "
          "drawn around a ruled box near its lower edge."),
 (14, 17, "A low table with one printed municipal notice open on it, a red pen resting on the "
          "notice and a magnifying glass lying beside it."),
 (17, 19, "Two mailboxes side by side in an apartment corridor, one with a pale yellow envelope "
          "standing in it and the other holding a thinner white one."),
 (19, 21, "A pair of open upturned palms held up at chest height beside a counter, and a "
          "rubber stamp lying on the counter untouched, well away from the hands."),
 (21, 23, "An old-style health insurance card lying on a table with a broad warm red diagonal "
          "stroke drawn across it.", D_HOKENSHO),
 (23, 25, ["A postal worker handing identical pale yellow envelopes to a long line of elderly "
           "people, one envelope each.",
           "A postal worker at a gate posting one pale yellow envelope into a mailbox, more "
           "of the same envelopes visible in the shoulder bag."]),
 (25, 28, ["An elderly man at a municipal counter, both hands on the counter, speaking to a clerk "
           "who is listening with her head tilted.",
           "An elderly woman standing at a municipal counter with one hand raised slightly, "
           "a clerk behind the counter nodding."]),
 (28, 29, "A residential mailbox on a gatepost with one pale yellow envelope standing in it."),
 (29, 31, "Two pale yellow envelopes lying side by side on a table, the left one slightly faded "
          "and the right one crisp and new."),
 (31, 33, "One card-sized certificate lying alone on a cream surface, a hand sliding it forward "
          "across a counter.", D_KAKUNIN),
 (33, 35, "One card-sized notice lying alone on a cream surface, a hand resting beside it, not "
          "moving it forward.", D_OSHIRASE),
 (38, 40, "Two card-sized sheets side by side on a table: the left one with a hand pushing it "
          "forward, the right one with a card lying on top of it."),
 (40, 42, "A card-sized notice held up at reading distance, a pair of reading glasses lying on "
          "the table below it.", D_OSHIRASE),
 (42, 44, "A card-sized notice and a My Number card lying overlapped, the card resting on the "
          "lower half of the notice, both being pushed forward together by one hand."),
 (44, 46, ["A hospital reception counter. An elderly man has laid one sheet down; the "
           "receptionist points with one finger at an open space on the counter beside it.",
           "A hospital reception counter with one sheet lying on it and a receptionist "
           "holding both hands still above the counter, not taking it."]),
 (46, 47, "Two card-sized sheets lying side by side on a counter, one finger resting on the "
          "heading of the left sheet and the thumb of the same hand on the heading of the right."),
 (47, 48, "A post office sorting table with two trays on it, one tray holding a thick stack of "
          "pale yellow envelopes and the other holding a thin stack."),
 (48, 51, "An elderly man in a knitted vest standing outside the door of a flat on the fourth "
          "floor of an apartment block, one hand on the railing."),
 (51, 52, "An elderly man resting a card flat on a small reader set into a clinic counter, the "
          "reader lit with a soft teal glow."),
 (52, 54, "Two elderly neighbours standing in an apartment corridor, each holding one "
          "card-sized sheet, the two sheets clearly different from each other."),
 (54, 56, "An elderly woman in a cardigan standing in her doorway holding one card-sized "
          "certificate up in front of her, looking pleased.", D_KAKUNIN),
 (56, 58, "Two card-sized sheets on a table with their positions crossed over by two curved "
          "navy arrows that swap left for right."),
 (58, 60, "A clinic card lying on a table with six visit receipts fanned out beside it, all held "
          "together at one corner by a paperclip."),
 (60, 62, "A clerk behind a counter placing two small tokens onto one side of a simple balance "
          "scale, the pan on that side tipping down."),
 (62, 64, "A clerk at a desk looking at a reader and a stack of sheets, one hand moving the "
          "stack of sheets away to the side of the desk."),
 (64, 66, "An open wallet lying on a hall table, one card slotted inside it, seen from above."),
 (66, 69, "An elderly man standing in a corridor holding an open wallet, looking down into it, "
          "his eyebrows drawn together."),
 (69, 70, "A printed municipal leaflet lying open on a desk, one finger tracing down the page "
          "and stopping on the second paragraph."),
 (73, 75, "A queue of elderly people at a post office window, each of them holding one identical "
          "pale yellow envelope.", D_KAKUNIN),
 (75, 78, ["A printed municipal leaflet on a desk with a warm red line drawn under one single "
           "row of its text, a magnifying glass resting over that row.",
           "A printed municipal leaflet held in two hands, a warm red line under one row near "
           "the foot of the page and a finger resting beside it."]),
 (78, 81, "Two neighbouring gateposts seen from the street, the left mailbox with a pale yellow "
          "envelope standing in it, the right mailbox with its flap shut and its metal face bare."),
 (81, 83, "A post office sorting table with two trays, the left tray stacked with pale yellow "
          "envelopes and the right tray stacked with white notices."),
 (83, 85, "A simple outline map of Japan divided into regions, each region drawn in a slightly "
          "different tone of cream, navy and teal."),
 (85, 86, "Four things laid in a row on a clinic counter: a printed certificate, a printed "
          "notice, a My Number card, and an old-style health insurance card."),
 (86, 88, "One card-sized certificate lying on a counter with a large warm red circle drawn "
          "beside it.", D_KAKUNIN),
 (88, 90, "One card-sized notice lying on a counter with a large navy cross drawn beside it.",
        D_OSHIRASE),
 (90, 92, "An elderly man sitting at a low table, one hand lifted to his mouth, looking at a "
          "card-sized notice in front of him."),
 (92, 94, "A My Number card resting alone on a small reader set into a counter, the reader lit "
          "with a soft teal glow, no paper anywhere on the counter."),
 (94, 96, "A small counter reader with its screen dark and a folded paper notice propped "
          "against it."),
 (96, 98, "An old-style health insurance card lying on a counter with a large navy cross drawn "
          "beside it.", D_HOKENSHO),
 (98, 101, ["A receptionist behind a counter returning an old card to an elderly man across the "
            "counter, holding it out flat on two fingers.",
            "An elderly man at a counter putting an old card back into his wallet while the "
            "receptionist looks on."]),
 (101, 102, "An open wallet lying on a table with two cards tucked into its slots, seen from above."),
 (102, 106, ["A handwritten note pinned to a refrigerator door with a magnet, a pale yellow "
             "envelope tucked behind the same magnet.",
             "A pale yellow envelope propped against a teapot on a kitchen table, a "
             "handwritten note lying open beside it."]),
 (106, 108, "A pale yellow envelope lying on a low table beside a cup of tea, one hand reaching "
            "towards it."),
 (108, 111, ["Two identical card-sized certificates lying side by side on a table, a warm red "
             "circle drawn around the lower part of only one of them.",
             "Two identical card-sized certificates held up one in each hand, the left one "
             "tilted forward slightly."], D_KAKUNIN),
 (111, 113, "One card-sized certificate held in two hands at reading distance, tilted slightly "
            "towards the viewer.", D_KAKUNIN),
 (113, 115, "A close view of the lower part of a printed certificate, with one ruled box drawn "
            "in navy outline, the inside of that box the same cream as the paper.", D_KAKUNIN),
 (115, 118, ["An older separate certificate card lying on a desk beside a municipal counter, a "
             "hand withdrawing it into a drawer.",
             "An open desk drawer seen from above with one older certificate card lying flat "
             "inside it and a hand closing the drawer."]),
 (118, 119, "One card-sized certificate on a table with a warm red arrow curving down into a "
            "ruled navy box near its lower edge.", D_KAKUNIN),
 (119, 121, "A My Number card resting on a reader, a soft teal ring of light around it and a "
            "small navy tick mark floating just above it."),
 (124, 126, "One card-sized certificate lying on a table, a ruled navy box near its lower edge, "
            "the inside of the box the same cream as the paper around it.", D_KAKUNIN),
 (126, 128, ["A bank passbook open on a table, a warm red arrow leading away from it towards the "
             "edge of the picture and a thinner navy arrow curving back towards it.",
             "A bank passbook open on a table beside a wall clock, a warm red arrow leaving "
             "the page and a teal arrow returning to it from the far side."]),
 (128, 130, "An elderly woman on a fourth-floor apartment balcony tending morning glory vines on "
            "a bamboo trellis."),
 (130, 132, "An elderly woman sitting at a low table with a certificate in one hand and a "
            "telephone handset held to her ear with the other.", D_KAKUNIN),
 (132, 135, "A close view of the lower edge of a certificate, one ruled navy box with the inside "
            "the same cream as the paper, and a hand pointing one finger at that box."),
 (135, 138, "Two printed municipal notices stacked on a desk, the newer one laid on top and one "
            "corner of the older one showing underneath."),
 (138, 141, ["A hand holding a certificate up to a window, sunlight falling across its lower edge.",
             "A certificate propped against a teacup on a low table, its lower edge turned "
             "towards the viewer."]),
 (141, 144, "A hospital payment counter with a folded payment slip lying on it and two hands "
            "counting notes onto the counter."),
 (144, 147, ["A payment receipt and a printed statement of treatment lying overlapped on a table, "
             "a paperclip holding them together.",
             "A clear document folder on a shelf with a payment receipt and a printed "
             "statement slipped inside it, seen from the front."], D_RYOYOHI),
 (147, 150, ["A clear document folder standing on a shelf with a payment receipt and a printed "
            "statement clipped inside it, a pale yellow envelope leaning beside the folder.",
            "A payment receipt and a printed statement clipped together and slipped into the "
            "pocket of a household account book on a low table."]),
 (150, 153, "Two hands opening a pale yellow envelope over a low table, one card-sized sheet "
            "half drawn out."),
 (153, 154, "An open wallet lying on a hall table with one card being slid into a slot by a hand."),
 (154, 157, ["A close view of the lower part of a certificate with a hand holding a pen just above "
             "one ruled navy box.",
             "A municipal counter with a certificate lying on it and a clerk drawing one short "
             "navy stroke inside a ruled box near its lower edge."], D_KAKUNIN),
 (157, 158, "A municipal office counter with a simple sign board standing on it and an arrow "
            "shape pointing left, a seated clerk behind the counter."),
 (158, 161, "An open wallet on a table with a card and a folded notice stacked together in the "
            "same slot, seen from above."),
 (161, 165, ["An open notebook on a low table with a printed notice tucked between its pages, "
             "one corner of the notice showing above the page edge.",
             "An open notebook on a low table, a hand smoothing a printed notice flat across "
             "the right-hand page."]),
 (165, 168, ["An elderly woman standing in her doorway holding up one card-sized certificate "
             "towards the viewer.",
             "Two printed sheets laid side by side on a table, the left one a certificate and "
             "the right one a notice with a My Number card resting on it.",
             "A clinic card on a table with six visit receipts fanned beside it under a "
             "paperclip."]),
 (168, 171, ["A card-sized notice and a My Number card lying overlapped on a table, pushed "
             "forward together by one hand.",
             "A card-sized notice standing upright in a wallet slot with a My Number card "
             "tucked into the same slot behind it."], D_OSHIRASE),
 (171, 175, "Three things placed in a vertical column on a low table: a pale yellow envelope, a "
            "printed card-sized sheet, and an open wallet with a card in its slot."),
 (175, 178, ["An elderly couple sitting at a low table, one of them holding a pale yellow envelope "
             "and both looking at it together.",
             "An elderly man kneeling in front of a low chest of drawers, one drawer open, "
             "lifting a pale yellow envelope out of it."]),
 (178, 182, ["A pale yellow envelope and a My Number card lying side by side on a low table "
             "under warm lamplight.",
             "A pale yellow envelope standing upright against a teacup on a low table, warm "
             "light from one side."]),
]


# ⭐⭐ GATE 5 — CẤM HÌNH TRỪU TƯỢNG / FILLER (user bắt 2026-09-21, lô gen đầu tiên)
#
# Lô đầu có **23/90 ô là hình trừu tượng**: dải navy có "mốc", ô tick trống, 4 thẻ úp, "bàn làm
# việc gọn gàng". User: *"có rất nhiều ảnh không có ý nghĩa kiểu này"* — và đúng: che lời đọc đi
# thì không ô nào trong số đó nói được điều gì.
#
# 🔴 ĐÂY LÀ LỖI CỦA MỘT LỚP, KHÔNG PHẢI CỦA 4 ẢNH (`ai-video-regen.md` §0). Cơ chế sinh ra nó:
# mỗi khi lời đọc nói về một KHÁI NIỆM (đường ranh giới · đếm 6 lần · hạn 2 năm · ba việc phải
# làm), tao vẽ **ẩn dụ hình học** thay vì đi tìm VẬT THẬT. Mà gần như lần nào cũng có vật tương
# ứng 1-1, chỉ là phải chịu khó đếm:
#     4 câu hỏi ○× → 4 VẬT trên quầy (証明書・お知らせ・マイナカード・旧保険証)
#     セルフチェック 3問 → 3 VẬT xếp dọc (封筒・紙・財布)
#     「12か月に6回」 → 診察券 + 6 tờ 領収書 kẹp ghim
#     「線が二本」 → 2 khay phân loại ở bưu điện
# ⇒ Luật: **mỗi ô phải hiện một vật người 75 tuổi cầm được, hoặc một khoảnh khắc có bàn tay.**
#   Hình học chỉ được làm NỀN cho vật, không bao giờ là chủ thể.
ABSTRACT = ("navy band", "navy line", "tally stroke", "bracket drawn", "checkbox",
            "face down", "marker standing", "marker on the", "marker at its",
            "tidy desk", "desk lamp", "hatched", "cream field with")


def row_for(line_idx: int):
    """Trả (chỉ số hàng trong S, hàng) hoặc ('GENTEN', tên file)."""
    for (lo, hi), fn in GENTEN.items():
        if lo <= line_idx < hi:
            return "GENTEN", fn
    for j, row in enumerate(S):
        if row[0] <= line_idx < row[1]:
            return j, row
    return None, None


def variants_of(row):
    """subject có thể là MỘT chuỗi, hoặc LIST nhiều biến thể cho các ô cùng dải."""
    subj = row[2]
    return (list(subj) if isinstance(subj, (list, tuple)) else [subj],
            row[3] if len(row) > 3 else None)


def build_prompt(subj: str, doc) -> str:
    if doc is None:
        return STYLE + subj
    return style_text(f"「{doc[0]}」", [f"「{x}」" for x in doc[1]]) + subj


def main() -> int:
    # ── GATE 0: CẤU TRÚC hàng. 🔴 Đã dính thật 2026-09-21: viết nhiều biến thể mà quên bọc
    # trong list ⇒ biến thể thứ 2 rơi vào vị trí row[3] = DOC, và `build_prompt` đem chuỗi đó
    # đi làm tiêu đề giấy tờ (`doc[0]` = ký tự ĐẦU TIÊN) ⇒ prompt rác, cú pháp vẫn hợp lệ,
    # không gate nào kêu. Kiểm cấu trúc trước khi kiểm nội dung.
    err = [f"S[{j}] dòng {r[0]}–{r[1]}: row[3] phải là DOC (tuple), đang là {type(r[3]).__name__}"
           for j, r in enumerate(S) if len(r) > 3 and not isinstance(r[3], tuple)]
    err += [f"S[{j}]: subject phải là str hoặc list[str]" for j, r in enumerate(S)
            if not isinstance(r[2], (str, list, tuple))]
    if err:
        print("🔴 GATE cấu trúc hàng:")
        for e in err[:10]:
            print("    ", e)
        return 1
    print(f"✅ GATE cấu trúc hàng: {len(S)}/{len(S)}")

    # ── GATE 1: bảng S phải phủ KÍN 0..181, không hở không chồng ──────────
    cov = [0] * 182
    for row in S:
        for i in range(row[0], min(row[1], 182)):
            cov[i] += 1
    holes = [i for i, c in enumerate(cov) if c == 0
             and not any(lo <= i < hi for lo, hi in GENTEN)]
    dups = [i for i, c in enumerate(cov) if c > 1]
    if holes or dups:
        print(f"🔴 GATE phủ dòng: hở {holes[:12]} · chồng {dups[:12]}")
        return 1
    print(f"✅ GATE phủ dòng: 182/182 (trong đó {sum(hi-lo for lo,hi in GENTEN)} dòng dùng 原典ショット)")

    plan = VD / "plan29.json"
    if not plan.exists():
        print(f"⏳ chưa có {plan} — chạy `python tools/plan29.py` sau khi voice xong.")
        print("   (bảng S ở trên đã sẵn sàng, không phụ thuộc timeline)")
        return 0

    shots = json.loads(plan.read_text(encoding="utf-8"))["shots"]
    flow, names, blocks, n_gen = [], [], [], 0
    used, short = {}, []
    for k, sh in enumerate(shots):
        li = sh["lines"][0]
        j, row = row_for(li)
        if j == "GENTEN":
            names.append(f"o {k:03d} -> [原典ショット] {row}")
            n_gen += 1
            continue
        vs, doc = variants_of(row)
        n = used.get(j, 0)
        used[j] = n + 1
        # 🔴 GATE 4 — CẤM TRÙNG ẢNH TRONG CÙNG VIDEO
        # (`feedback_slide_khong_trung_anh_trong_video`). Hai ô rơi vào CÙNG một dải dòng sẽ
        # nhận CÙNG một prompt ⇒ cùng một ảnh. Ghi sổ để biết đúng dải nào cần viết thêm biến
        # thể, thay vì để lọt rồi mới phát hiện lúc soi contact sheet.
        if n >= len(vs):
            short.append((j, row[0], row[1], n + 1, len(vs)))
            continue
        p = build_prompt(vs[n], doc)
        flow.append(p.replace("\n", " "))
        names.append(f"dong {len(flow)} -> shot_{k:03d}.png   [dong TTS {li}]")
        blocks.append((k, li, p))

    (VD / "img29_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8", newline="\n")
    (VD / "img29_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8", newline="\n")
    md = [f"# img29 — {len(flow)} prompt ảnh ({n_gen} ô dùng 原典ショット)", ""]
    for k, li, p in blocks:
        md += [f"### shot_{k:03d}  (dòng TTS {li})", "", "```", p, "```", ""]
    (VD / "img29_BLOCKS.md").write_text("\n".join(md), encoding="utf-8", newline="\n")

    # ── GATE 2: guard CẤM phải nằm trong 15% ĐẦU prompt (ai-video-regen §2) ──
    bad = [i for i, p in enumerate(flow)
           if max(p.find("NO TEXT"), p.find("READABLE JAPANESE TEXT")) * 100 // len(p) > 15]
    # ── GATE 3: không còn từ kéo model về vẽ mảng trống ──────────────────
    # 🔴 QUÉT RIÊNG PHẦN SUBJECT, KHÔNG QUÉT CẢ PROMPT. Bản đầu quét cả prompt → báo đỏ 17 chỗ,
    # và 16/17 là **câu của khuôn chung v28** (`style_text` có
    # 'do not leave any row as an empty ruled line' — bản vá CỐ Ý của v28 chống hàng trống).
    # Gate đọc trúng văn của chính mình, đúng `ai-video-regen.md` §6 — lần thứ ba trong workspace.
    banned = [(j, w) for j, row in enumerate(S)
              for sub in (row[2] if isinstance(row[2], (list, tuple)) else [row[2]])
              for w in ("blank", "empty", "text-free") if w in sub.lower()]
    if short:
        print(f"🔴 GATE trùng ảnh: {len(short)} ô chưa có biến thể riêng —")
        for j, lo, hi, need, have in short:
            print(f"     S[{j}] dòng {lo}–{hi}: cần {need} biến thể, đang có {have}")
        print("   ⇒ đổi subject của các dải đó thành LIST nhiều biến thể rồi chạy lại.")
    # ── GATE 5: không ô nào lấy HÌNH HỌC làm chủ thể (xem khối ABSTRACT ở đầu file) ──
    abst = [(j, w) for j, row in enumerate(S)
            for sub in (row[2] if isinstance(row[2], (list, tuple)) else [row[2]])
            for w in ABSTRACT if w in sub.lower()]
    if abst:
        print(f"🔴 GATE hình trừu tượng: {len(abst)} chỗ —")
        for j, w in abst[:10]:
            print(f"     S[{j}] dòng {S[j][0]}–{S[j][1]}: «{w}»")
    print(f"{len(flow)} prompt · dài TB {sum(map(len, flow))//max(len(flow),1)} ký")
    print(f"hình trừu tượng: {len(abst)} (phải 0)")
    print(f"guard >15%: {len(bad)} (phải 0) · từ cấm: {len(banned)} (phải 0)")
    if banned:
        print("   ", banned[:6])
    print(f"→ {VD}")
    return 1 if (bad or banned or short or abst) else 0


if __name__ == "__main__":
    sys.exit(main())
