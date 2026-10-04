# -*- coding: utf-8 -*-
r"""img27_prompts.py — sinh prompt ảnh cho 86 ô của video 27.

KHUÔN ĐÃ DUYỆT (lô thử 7 ảnh, user gật 2026-09-17):
  · vector phẳng kiểu clip-art công ích Nhật · nền kem #F6F1E4 MỘT TÔNG
  · đúng 3 màu + kem: navy #1F3864 · đỏ ấm #C0392B · teal #3E7C78
  · nét đều, bo tròn, KHÔNG đổ bóng, KHÔNG vân giấy
  · 🔴 guard CẤM CHỮ đặt ở ~10% đầu prompt (`ai-video-regen.md` §2: cấm gì phải cấm ở đầu)

🔴 KHÁC LÔ THỬ MỘT CHỖ — ĐỌC TRƯỚC KHI GEN:
lô thử xin `generous empty cream space on the right third` vì lúc đó tao định để ảnh phủ kín
khung và viết chữ đè lên. Layout đã chốt (demo27e) thì **chữ nằm ở cột TRÁI trên canvas, ảnh
nằm gọn trong ô 45% bên phải** ⇒ ảnh KHÔNG cần chừa chỗ, mà phải **lấp đầy khung của nó**,
nếu không chủ thể bị nhỏ như hạt đậu. Đó là lý do khối composition ở đây đổi thành
`subject fills the frame`.

7 ẢNH LÔ THỬ đã khớp sẵn 7 ô (không gen lại):
  ô 0 cụ ông cầm giấy trắng · ô 1 bốn icon khoản trừ · ô 19 佐藤 ở bãi xe ·
  ô 33 vợ chồng 山田 + cơm đỏ · ô 43 đối chứng hai bà · ô 55 伊藤 + bảng đen · ô 71 phong bì nâu

CHẠY:  python tools/img27_prompts.py           → 3 file trong 06_VIDEO/<stem>/
       python tools/img27_prompts.py --lot 2   → chỉ in lô 2 (ô 6–31)
"""
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "27_nenkin-tsuchisho-nai-okane-5tsu"
VD = PROJ / "06_VIDEO" / STEM

# 🔴🔴 HAI STYLE, KHÔNG PHẢI MỘT — sửa 2026-09-17 sau khi user soi lô 79 ảnh:
#   *"tao thấy nhiều ảnh không có chữ như này. Tao muốn sách, giấy phải có chữ chứ.
#     Nhiều ảnh nhìn chả hiểu để làm gì không có text gì cả?"*
# Bản đầu cấm chữ TOÀN CỤC vì sợ kanji gen nát. Hậu quả: tờ 通知書 trắng trơn không còn là
# thông báo, sổ ngân hàng trắng trơn không còn là sổ, checklist trắng trơn không còn là
# checklist — **vật mất lý do tồn tại**, và người xem không hiểu ảnh nói gì.
# ⇒ Tách đúng hai loại chữ, y như `ai-video-regen.md` §1 đã phân:
#     ❌ LOẠI: chữ/số ĐỌC RA ĐƯỢC (kanji gen nát + số sai là vi phạm YMYL)
#     ✅ NHẬN: chữ TEXTURE li ti không đọc nổi — thứ làm vật trông như vật thật
# Số liệu thật vẫn do FONT của builder vẽ đè lên, không nhờ AI.
_BASE = ("Flat vector illustration in the style of Japanese public-information clip art. "
         "Plain flat cream background #F6F1E4, single tone, no gradient, no vignette, "
         "no drop shadows. Only three colors plus cream: navy #1F3864, warm red #C0392B, "
         "muted teal #3E7C78. Even line weight, rounded shapes, simple faces. "
         "Composition: subject centered and filling most of the frame, small even cream "
         "margin on all four sides. 16:9. SUBJECT: ")

# ── ảnh KHÔNG có vật in ấn: cấm chữ tuyệt đối
STYLE = ("NO TEXT, NO LETTERS, NO NUMBERS, NO SIGNAGE, NO CALENDAR GRID, NO CLOCK FACE "
         "anywhere in the image. " + _BASE)

# ── ảnh CÓ giấy tờ/sổ/biểu mẫu: BẮT BUỘC có chữ texture, cấm chữ đọc được
STYLE_PRINT = (
    "Every sheet of paper, form, book, bankbook, postcard, notice and document in this image "
    "MUST LOOK PRINTED AND FILLED IN: cover them with FINE ILLEGIBLE TEXT TEXTURE — many rows "
    "of tiny faint grey marks suggesting Japanese characters, far too small to read — plus "
    "faint ruled lines, a few small boxes and a column of tiny marks along one edge. "
    "A blank white sheet is WRONG. But NO large readable words, NO readable numbers, "
    "NO headline text, NO signage, NO logos, NO calendar grid, NO clock face. " + _BASE)

# ô có vật IN ẤN ⇒ dùng STYLE_PRINT
PRINT = {2, 7, 8, 9, 12, 17, 20, 21, 22, 27, 28, 30, 31, 32, 34, 36, 40, 47, 48, 50, 51,
         59, 60, 61, 62, 63, 65, 66, 67, 68, 72, 74, 75, 76, 77, 78, 79, 80, 83, 85}

# ── ĐÃ CÓ ẢNH (lô thử) — không gen lại ────────────────────────────────────────
HAVE = {0: "Elderly_man_holding_blank_paper", 1: "Four_deduction_icons_in_row",
        19: "Woman_holding_envelope_in_parkin", 33: "Elderly_couple_holding_rice_bowl",
        43: "Two_women_comparing_coin_holdings", 55: "Man_wiping_cup_in_cafe",
        71: "Elderly_woman_viewing_paper_enve"}

# ── CHỦ THỂ TỪNG Ô. Rút từ lời đọc của chính ô đó; ô trống (do chẻ ô dài) lấy
#    hình TIẾP NỐI ý của ô trước, KHÔNG dùng lại ảnh (cấm trùng ảnh trong cùng video).
SUBJ = {
    2: "a single large envelope lying flat, closed, seen from directly above, one elderly hand resting beside it",
    3: "an elderly man seated at a low table, both hands raised in a small helpless shrug, an open drawer beside him showing a few loose papers",
    4: "one elderly woman standing alone on the left and a married couple standing on the right, a thin vertical divider line between them",
    5: "a large simple mailbox with its flap closed, and a small elderly figure standing beside it looking up at it",
    6: "five simple milestone markers arranged along a gentle rising path from left to right, each a plain rounded post",
    7: "a laboratory flask and a notebook on a desk, an elderly researcher figure in a plain coat standing behind, calm expression",
    8: "a wide desk seen from above with one open folder of printed papers in the center, the top sheet dense with fine illegible print, and a pen beside it",
    9: "an elderly man in his early sixties holding up a printed notice sheet densely covered in fine illegible print, reading it closely",
    10: "two elderly figures standing side by side, one man and one woman, a thin horizontal timeline line running behind them",
    11: "a government office counter with a clerk figure on the far side, an elderly visitor standing before it",
    12: "a hand pointing at a large printed document pinned to a board, the sheet dense with fine illegible print, one red circle drawn around a small area of it",
    13: "an hourglass standing on a plain surface with sand nearly run out, an elderly hand reaching toward it",
    14: "a bar shrinking from tall to short across the frame, an elderly figure watching it from the side",
    15: "an elderly woman in an apron arranging vegetables at a supermarket produce shelf",
    16: "the same supermarket produce shelf seen closer, hands placing a crate of vegetables, no person's face",
    17: "an elderly woman sitting alone at a kotatsu table with a tall stack of unopened envelopes in an open drawer",
    18: "an elderly woman looking down at an envelope in her hands with a startled expression, one hand at her mouth",
    20: "a large closed envelope in the center with a thin red diagonal line crossing it, an elderly figure small in the corner",
    21: "a postcard held up against the light, its surface covered in rows of fine illegible print, an elderly hand holding it",
    22: "a checklist board whose rows are filled with fine illegible print, the first row checked off by a red mark",
    23: "an elderly married couple standing together, the husband slightly older, a small plus sign shape floating between them",
    24: "two stacked coin piles of different heights side by side, an elderly couple looking at them",
    25: "a single tall stack of coins with a small elderly figure standing beside it, looking up",
    26: "an elderly man in a work vest carrying a small bag, walking out of a house door, his wife waving from inside",
    27: "an official printed form lying on a desk, dense with fine print and small boxes, a pen placed on top and a stamp beside it",
    28: "a hand placing a filled-in printed form into a document tray on an office counter",
    29: "an elderly couple looking puzzled, two large question marks floating above their heads",
    30: "a filing cabinet with one drawer open showing folders, and beside it a closed mailbox, a thin line connecting them",
    31: "a checklist board whose rows are filled with fine illegible print, the first two rows checked off by red marks",
    32: "a printed notice sheet being turned by a hand, its surface dense with fine print, an elderly couple watching from the side",
    34: "an elderly man holding a bankbook open with both hands, eyebrows raised, a small downward arrow beside it",
    35: "two pension symbols side by side, the left one fading out and the right one appearing, an elderly couple below",
    36: "an official printed document on a stand, dense with fine print, a red rectangle drawn around one small block of it, a pointer beside it",
    37: "a small coin dropping into an open palm of an elderly woman, a gentle smile",
    38: "an elderly woman in a cardigan seated calmly, a small single coin resting on the table before her",
    39: "a very large coin on the left and a very small coin on the right with a wide gap between them",
    40: "a printed statement sheet with one small area circled in red, an elderly woman beside it",
    41: "an elderly couple in a Tokyo apartment doorway, the wife slightly younger, both looking toward the viewer",
    42: "a thin vertical dividing line with an elderly woman just to its left and another just to its right, one inside a shaded band",
    44: "a straight ruled line drawn firmly across the frame, two elderly figures standing on opposite sides of it",
    45: "an elderly couple smiling gently toward the viewer with open palms, a heart shape floating above",
    46: "two neighbouring houses side by side, one with a small coin above it and one without",
    47: "a pair of hands holding a printed slip dense with fine illegible print, seen from above on a table",
    48: "an elderly woman at a desk with an open folder of printed papers, relieved expression, one hand on her chest",
    49: "a signpost with two arrows pointing in different directions, an elderly couple standing at the fork",
    50: "a checklist board whose rows are filled with fine illegible print, one row marked with a red triangle",
    51: "a stack of twelve small identical printed envelopes arranged in a row, each showing a faint address block of fine illegible print",
    52: "a low horizontal line with a small elderly figure standing just below it and a coin above the line",
    53: "an open palm receiving a small stack of coins, plain background",
    54: "an elderly man in an apron standing behind a small cafe counter with a coffee siphon",
    56: "a cafe interior with three customers seated at small tables, the owner behind the counter",
    57: "a quiet cafe at closing time, chairs turned up on the tables, one figure wiping a table",
    58: "an elderly man in an apron looking down at his own open palm with a puzzled expression",
    59: "a hand placing a printed application slip, dense with fine print, into a post box slot",
    60: "a postman figure holding out a printed postcard to an elderly hand at a doorway, the postcard covered in fine print",
    61: "an elderly man dropping a printed postcard into a waste basket, slight frown",
    62: "a plain closed envelope resting on a small household altar shelf, no decoration",
    63: "two identical small envelopes side by side connected by a thin line, plain background",
    64: "an elderly woman in her early seventies in a school-kitchen apron standing beside a large cooking pot",
    65: "an elderly woman seated alone at a low table with a bankbook open before her",
    66: "a family of three standing together with an envelope passing from one hand to another",
    67: "a government building on the left and a house on the right connected by a thin line with a small card icon on it",
    68: "a hand reaching toward an envelope that stays just out of reach on a table",
    69: "two arrows side by side, one curving down automatically and one pushed by a hand",
    70: "an elderly woman sitting quietly with both hands in her lap, eyes lowered, gentle sad expression",
    72: "a checklist board with five printed rows, four marked with red circles and one marked with a red triangle",
    73: "an elderly couple standing beside a signpost with two arrows, one arrow slightly raised",
    74: "two hands holding up a single printed notice sheet, its surface covered in rows of fine illegible print and faint ruled lines",
    75: "an open notebook on a desk, five ruled rows filled with fine illegible handwriting, a pen resting on it",
    76: "an hourglass beside a small printed document dense with fine print",
    77: "a printed official form dense with fine print and small boxes, a pen lying diagonally across it",
    78: "a printed statement sheet with one small area circled in red and a small coin beside it",
    79: "an elderly woman handing a printed slip to a younger family member",
    80: "a hand pulling a printed slip, dense with fine print, out of a wooden drawer",
    81: "two elderly faces side by side with a thin vertical line between them, one slightly shaded",
    82: "an elderly hand holding a telephone receiver, a simple desk phone on the table",
    83: "a notice board with a printed sheet pinned to it, dense with fine illegible print, a small elderly figure looking at it",
    84: "a bell shape with gentle motion lines beside it, an elderly couple looking up toward it",
    85: "a bankbook open at a page of printed rows and columns of fine illegible figures, a small coin resting on it",
}


def main() -> int:
    plan = json.loads((VD / "plan27.json").read_text(encoding="utf-8"))
    shots = plan["shots"]
    lot = None
    if "--lot" in sys.argv:
        lot = int(sys.argv[sys.argv.index("--lot") + 1])
    lots = {2: range(2, 32), 3: range(32, 62), 4: range(62, 86)}

    miss = [s["k"] for s in shots if s["k"] not in SUBJ and s["k"] not in HAVE]
    if miss:
        print(f"🔴 THIẾU chủ thể cho ô: {miss}")
        return 1

    flow, names, blocks = [], [], []
    for s in shots:
        k = s["k"]
        if k in HAVE:
            names.append(f"# ô {k:>3}  [ĐÃ CÓ] art/{HAVE[k]}*.png")
            continue
        if lot and k not in lots[lot]:
            continue
        if "--redo-print" in sys.argv and k not in PRINT:
            continue
        flow.append((STYLE_PRINT if k in PRINT else STYLE) + SUBJ[k] + ".")
        fn = f"img27_{k:03d}.png"
        names.append(f"dòng {len(flow):>3} -> {fn}   (ô {k}, ch{s['chap']}, {s['t0']:.0f}s)")
        blocks.append(f"## ô {k} · chương {s['chap']} · {s['t0']:.0f}s\n"
                      f"lời: {s['text'][:60]}\n{SUBJ[k]}\n")

    # 🔴 --redo-print xuất ra FILE RIÊNG, không ghi đè FLOW gốc (user chốt 2026-09-17):
    # lô gen lại và lô đầy đủ phải nằm cạnh nhau để còn đối chiếu ảnh nào thuộc lượt nào.
    tag = "_REDO" if "--redo-print" in sys.argv else (f"_LOT{lot}" if lot else "")
    (VD / f"img27_FLOW{tag}.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / f"img27_TENFILE{tag}.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    (VD / f"img27_BLOCKS{tag}.md").write_text("\n".join(blocks), encoding="utf-8")

    n = len(flow)
    L = [len(x) for x in flow]
    npr = sum(1 for s in shots if s["k"] in PRINT and s["k"] not in HAVE
              and (not lot or s["k"] in lots[lot]))
    print(f"→ {n} prompt · {min(L)}–{max(L)} ký · {npr} ô dùng STYLE_PRINT (giấy tờ CÓ chữ texture)")
    print(f"  {VD / f'img27_FLOW{tag}.txt'}")
    print(f"  {VD / f'img27_TENFILE{tag}.txt'}")
    print(f"  {VD / f'img27_BLOCKS{tag}.md'}")
    print(f"  ({len(HAVE)} ô đã có ảnh từ lô thử, không gen lại)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
