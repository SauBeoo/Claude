# -*- coding: utf-8 -*-
"""SPEC19 + main19 — 5 sticker MỚI của video 19.
21 sticker cũ của video 17/18 đã được dùng lại (CLAUDE.md §②: "Sticker thì TÁI DÙNG"),
chỉ 5 vật dưới đây là mới. Gọi: python tools/sticker_prompts_collage.py <slug> --v19
"""

SPEC19 = [
    ("el_kyuryo_meisai.png",
     "a single monthly payslip sheet held slightly curled, showing empty ruled columns and "
     "blank boxes, no characters written anywhere on it", False),
    ("el_chart_down.png",
     "a small bar chart of four descending bars with a bold arrow sloping downward across "
     "them, cut from paper", False),
    ("el_shashou.png",
     "a small round metal company lapel pin with a plain unmarked enamel face and a pin "
     "clasp behind it, slightly worn at the edge", False),
    ("el_two_men_desk.png",
     "two simple seated figures of older men side by side at one long desk, seen from the "
     "front, plain shirts, no facial detail", False),
    ("el_zero_stamp.png",
     "a red rubber-stamp impression of a single large circle shaped like the digit zero, "
     "slightly smudged at one edge, on a small torn paper scrap", False),
]

_HEAD = (
    "21 sticker cũ của video 17/18 **đã được dùng lại**, không cần gen. "
    "Chỉ 5 vật dưới đây là mới.\n\n"
    "🔴 **Nền phải là MAGENTA `#FF00FF` thuần** — nền trắng thì không tách nổi giấy kem, "
    "tóc bạc, áo trắng (`media-library.md` §2.10 ⑨ ①).\n"
    "🔴 **Đúng MỘT vật / ảnh.** Hai vật trong một ảnh là không tách rời được.\n\n"
    "Cắt nền: `python tools/cutout_sticker.py 19_kounenrei-koyou-keizoku-kyufu --v19`\n"
)


def main19(vdir, compose):
    nl = chr(10)
    flow, ten, blocks = [], [], []
    blocks.append("# Prompt STICKER — video 19 (lô 5 vật MỚI)" + nl * 2)
    blocks.append(_HEAD)
    for i, (fn, obj, person) in enumerate(SPEC19, 1):
        p = compose(obj, person)
        flow.append(p)
        ten.append(f"{fn:<26}<- dòng {i} FLOW")
        blocks.append(nl * 2 + f"## {i}. `{fn}`" + nl * 2 + "```" + nl + p + nl + "```" + nl)
    (vdir / "sticker_prompts_v19_FLOW.txt").write_text(nl.join(flow) + nl, encoding="utf-8")
    (vdir / "sticker_prompts_v19_BLOCKS.md").write_text("".join(blocks), encoding="utf-8")
    (vdir / "sticker_prompts_v19_TENFILE.txt").write_text(nl.join(ten) + nl, encoding="utf-8")
    ln = [len(x) for x in flow]
    print(f"✓ {len(flow)} prompt sticker MỚI → {vdir}")
    print(f"   độ dài: min {min(ln)} · TB {sum(ln)//len(ln)} · max {max(ln)} ký")
    for fn, _, _ in SPEC19:
        print("   -", fn)
    return 0
