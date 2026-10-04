# -*- coding: utf-8 -*-
r"""sticker_prompts_collage.py — prompt gen STICKER CUTOUT rời (từng VẬT một) cho lớp
Remotion kiểu `okura-demo`, giữ style paper-collage của kênh nenkin.

⭐ VÌ SAO CÓ TOOL NÀY (user chốt 2026-08-26, lần 4): *"toàn bộ frame đều là ảnh hết, vẫn
giữ khung 2 nhân vật 2 bên, làm remotion giống okura-demo"*.
Khuôn tham chiếu: `E:\Claude\Projects\remotion-vox\projects\okura-demo` — nền giấy kem +
**sticker cutout ảnh thật** (1 hero to + 2–3 sup nhỏ) + tag chữ khối màu + dải punch đen-vàng.
Mọi frame là ẢNH, KHÔNG có card chữ.

🔴 VÌ SAO PHẢI GEN RIÊNG TỪNG VẬT — đã đo, không phải phỏng đoán (2026-08-26):
thử `rembg` trên chính ảnh collage scene đã có (`art_denwa_furueru.png`) → nó cắt ra
**cả mảng giấy** (bàn + điện thoại + cốc + báo dính liền), bbox (0,4)–(984,768). Ảnh collage
là MỘT khối giấy liền, không có ranh giới alpha giữa các vật ⇒ **không thể tách sticker từ
ảnh scene**. Muốn sticker rời thì phải gen từng vật một, trên nền tách được.

🎨 NỀN MAGENTA `#FF00FF`, KHÔNG nền trắng — luật đã có ở `media-library.md` §2.10 ⑨ ①:
vật của kênh này hay là **giấy kem / tóc bạc / áo trắng**, tách theo ngưỡng sáng là ăn mất.
Magenta không bao giờ có trong palette collage ⇒ tách bằng khoảng cách màu, sạch tuyệt đối.
Cắt nền bằng `tools/cutout_sticker.py` (co mask vào 3px theo §2.10 ⑨ ②, giữ viền giấy trắng).

CHẠY:  python tools/sticker_prompts_collage.py <slug>
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]

# Khối STYLE — CHÉP NGUYÊN từ `art_prompts_collage.py` để sticker và ảnh nền cùng một phim.
STYLE = (
    "Vintage newsprint editorial paper collage in the style of a mid-century JAPANESE "
    "front-page news feature: heavy halftone print dots, aged newsprint texture with slight "
    "ink misregistration. Palette: cream white, deep navy ink, deep red, mustard yellow, "
    "charcoal black."
)

# Cơ chế riêng của STICKER: một vật, viền giấy trắng dày, không bối cảnh.
CUTOUT = (
    "ONE SINGLE OBJECT only, centred, filling most of the frame, cut out as a hand-cut paper "
    "sticker with a THICK WHITE TORN-PAPER BORDER all the way around it and a soft paper drop "
    "shadow. The object is a PRINTED / illustrated halftone cut-out, NOT CGI, NOT a 3D render "
    "— keep print grain and paper imperfections."
)

# 🔴 Nền magenta — lý do ở docstring. Phải nói NHIỀU LẦN, model rất hay trả nền trắng.
BG = (
    "The background is a COMPLETELY FLAT, UNIFORM, SOLID MAGENTA #FF00FF chroma-key screen — "
    "pure magenta, edge to edge, with absolutely nothing else in it: no table, no room, no "
    "floor, no shadow cast onto the background, no gradient, no texture, no other colour. "
    "Only the single object and its white paper border sit on top of the magenta."
)

NOTEXT = (
    "All paper surfaces on the object are BLANK and unprinted. No text, no letters, no "
    "numbers, no logo, no watermark anywhere in the image."
)

PEOPLE = (
    "The person is JAPANESE and elderly (60s-70s), in modest everyday Japanese clothing — "
    "not Western, not American, not 1950s retro fashion."
)


def compose(obj, person=False):
    parts = [STYLE, f"SUBJECT: {obj.strip().rstrip('.')}.", CUTOUT]
    if person:
        parts.append(PEOPLE)
    parts += [BG, NOTEXT]
    return " ".join(parts)


# ══════════════════════════════════════════════════════════════════════════════
# LÔ 1 — video 17 (詐欺). Mỗi scene cần 1 HERO + 2–3 SUP (khuôn okura-demo).
# Vật lặp lại giữa các scene (điện thoại, sổ 通帳) chỉ gen MỘT LẦN rồi dùng lại —
# đó là cái rẻ của lớp sticker so với gen cả scene.
# ══════════════════════════════════════════════════════════════════════════════
SPEC = [
    # ── scene 1: cold open「電話が震える」
    ("el_smartphone.png",   "a modern smartphone lying at a slight angle, screen blank and pale", False),
    ("el_teacup.png",       "a Japanese green-tea cup on a small saucer, seen from slightly above", False),
    ("el_newspaper.png",    "a folded morning newspaper, blank columns, no printed words", False),
    # ── scene 2: giọng máy「支給停止」
    ("el_speaker_robot.png", "an old desk telephone handset with three curved sound-wave arcs "
                             "cut from paper radiating out of the earpiece", False),
    ("el_calendar.png",     "a torn-off desk calendar page showing an empty date grid", False),
    # ── scene 3: 4 câu hỏi leo thang
    ("el_passbook.png",     "a closed Japanese bank passbook, plain navy cover, no lettering", False),
    ("el_mynumber_card.png", "a blank plastic ID card the size of a credit card, rounded corners, "
                             "completely empty surface with only faint empty boxes", False),
    # ── scene 4: CAO TRÀO「手が止まった」
    ("el_hand_stop.png",    "an elderly Japanese man's hand, palm down, fingers spread and frozen "
                            "in mid-air as if stopping just short of touching something", True),
    ("el_burst_red.png",    "a jagged starburst shape cut from deep red paper, like a comic impact "
                            "flash, nothing inside it", False),
    # ── scene 5: 年金手帳 + gọi lại
    ("el_nenkin_techo.png", "a small slim booklet held half-open, plain cover, blank pages", False),
    ("el_senior_phone.png", "an elderly Japanese man in a dark cardigan pressing an old telephone "
                            "handset to his ear, calm expression, upper body only", True),
    # ── scene 6: số liệu 警察庁
    ("el_police_badge.png", "a simple round official-looking emblem cut from mustard paper, plain "
                            "rim, empty centre", False),
    ("el_coin_stack.png",   "a tall stack of Japanese coins seen from the side", False),
    ("el_chart_up.png",     "a rising bar chart of four bars cut from red and mustard paper with a "
                            "steep arrow climbing over them", False),
    # ── scene 7: 釣り (beat chất người)
    ("el_two_anglers.png",  "two elderly Japanese men sitting side by side on low stools, each "
                            "holding a long fishing rod angled out of frame", True),
]

# ══════════════════════════════════════════════════════════════════════════════
# SPEC18 — 6 sticker MỚI cho video 18 (60歳繰上げ｜窓口の一言), để giảm lặp.
# Lý do có lô riêng: 15 sticker cũ của video 17 chỉ 8 cái hợp chủ đề tuổi-nhận-lương-hưu;
# dùng đúng 8 cái đó cho 24 lượt sticker ⇒ 1 file lặp tới 4 lần. Lô này KHÔNG lặp tên với
# 15 file cũ — chạy `cutout_sticker.py` xong là gộp thẳng vào `sticker/` cùng thư mục.
# ══════════════════════════════════════════════════════════════════════════════
SPEC18 = [
    ("el_magnifying_glass.png", "a magnifying glass with a dark wooden handle, held at a slight "
                                "angle as if examining something", False),
    ("el_house_bills.png",   "three small utility bill slips fanned out slightly, each a plain "
                             "blank rectangle of paper, stacked like a hand of cards", False),
    ("el_heart_pulse.png",   "a simple paper heart shape with a jagged pulse-line cut through "
                             "its centre, like an ECG heartbeat line", False),
    ("el_medicine_bottle.png", "a small amber medicine bottle with a white cap, one blank round "
                               "pill resting beside it", False),
    ("el_signpost.png",      "a wooden signpost post with three blank arrow-shaped signs "
                             "pointing in three different directions from the same post", False),
    ("el_percent_badge.png", "a torn-paper circular badge shape with a bold percent symbol "
                             "(%) cut out of its centre", False),
]




# ══════════════════════════════════════════════════════════════════════════════
# SPEC24 — 3 sticker MỚI cho video 24 (年金生活者支援給付金・9月の緑の封筒). Vật trung
# tâm của bài (phong bì xanh / はがき / tem) không có trong POOL 21 file tái dùng từ v19.
# ══════════════════════════════════════════════════════════════════════════════
SPEC24 = [
    ("el_green_envelope.png", "a plain GREEN envelope, thin and slightly bent as if it has "
                              "just been pulled from a mailbox, one corner lifted", False),
    ("el_hagaki.png",        "a single BLANK postcard-style government form, a few empty "
                              "ruled boxes visible on its surface, lying flat", False),
    ("el_stamp.png",         "one loose Japanese postage stamp, plain and unprinted, seen at "
                              "a slight angle as if about to be pressed onto paper", False),
]


def main18b_spec24(vdir):
    """Lô 3 sticker MỚI riêng cho video 24 (xem SPEC24)."""
    flow, ten, blocks = [], [], []
    blocks.append(f"# Prompt STICKER CUTOUT — paper-collage · video 24 (lô mới, 3 vật)\n\n")
    for i, (fn, obj, person) in enumerate(SPEC24, 1):
        p = compose(obj, person)
        flow.append(p)
        ten.append(f'{fn:<26}<- dòng {i} FLOW')
        blocks.append(f"\n## {i}. `{fn}`\n\n```\n{p}\n```\n")
    (vdir / "sticker_prompts_v24_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (vdir / "sticker_prompts_v24_BLOCKS.md").write_text("".join(blocks), encoding="utf-8")
    (vdir / "sticker_prompts_v24_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")
    ln = [len(x) for x in flow]
    print(f"✓ {len(flow)} prompt sticker MỚI (video 24) → {vdir}")
    print(f"   độ dài: min {min(ln)} · TB {sum(ln)//len(ln)} · max {max(ln)} ký")
    print(f"   (21 sticker khác đã COPY từ video 19, không cần gen lại)")
    return 0


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    if not slug:
        print("dùng: python tools/sticker_prompts_collage.py <slug> [--v18|--v19|--v24]")
        return 1
    vdir = PROJ / "06_VIDEO" / slug
    vdir.mkdir(parents=True, exist_ok=True)
    if "--v24" in sys.argv:
        return main18b_spec24(vdir)
    if "--v19" in sys.argv:
        from _stick19 import main19
        return main19(vdir, compose)
    if "--v18" in sys.argv:
        return main18(vdir)

    flow, ten, blocks = [], [], []
    blocks.append(f"# Prompt STICKER CUTOUT — paper-collage · {slug}\n\n")
    blocks.append(
        "Khuôn: `tools/sticker_prompts_collage.py`. Đây là lớp cho **Remotion kiểu "
        "`okura-demo`** — mọi frame là ẢNH, ghép từ sticker rời.\n\n"
        "🔴 **NỀN PHẢI LÀ MAGENTA `#FF00FF` THUẦN.** Ảnh nào gen ra nền trắng / có bàn / có "
        "bóng đổ xuống nền ⇒ **loại, gen lại** — nền trắng thì không tách nổi giấy kem, tóc "
        "bạc, áo trắng (`media-library.md` §2.10 ⑨ ①).\n\n"
        "🔴 **ĐÚNG MỘT VẬT / ảnh.** Hai vật trong một ảnh là không tách rời được, tức mất "
        "hẳn cái lợi của lớp sticker.\n\n"
        "Cắt nền: `python tools/cutout_sticker.py <slug>` (tách theo khoảng cách màu + co "
        "mask 3px để giữ viền giấy trắng).\n"
    )
    for i, (fn, obj, person) in enumerate(SPEC, 1):
        p = compose(obj, person)
        flow.append(p)
        ten.append(f'{fn:<26}<- dòng {i} FLOW{"  [người]" if person else ""}')
        blocks.append(f"\n## {i}. `{fn}`{'  · CÓ NGƯỜI' if person else ''}\n\n```\n{p}\n```\n")

    (vdir / "sticker_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (vdir / "sticker_prompts_BLOCKS.md").write_text("".join(blocks), encoding="utf-8")
    (vdir / "sticker_prompts_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")

    ln = [len(x) for x in flow]
    print(f"✓ {len(flow)} prompt sticker → {vdir}")
    print(f"   độ dài: min {min(ln)} · TB {sum(ln)//len(ln)} · max {max(ln)} ký")
    print(f"   {sum(1 for _,_,p in SPEC if p)} ảnh có người · {sum(1 for _,_,p in SPEC if not p)} ảnh vật")
    return 0


def main18(vdir):
    """Lô 6 sticker MỚI riêng cho video 18 — giảm lặp (xem SPEC18)."""
    flow, ten, blocks = [], [], []
    blocks.append("# Prompt STICKER CUTOUT — paper-collage · video 18 (lô GIẢM LẶP)\n\n")
    blocks.append(
        "6 sticker MỚI, không trùng tên với 15 file cũ tái dùng từ video 17. Cắt nền xong "
        "thì bỏ THẲNG vào `06_VIDEO/18_.../sticker/` cùng chỗ với 10 file cũ đang dùng — "
        "builder tự nhặt theo tên khai trong `sup=[...]`.\n\n"
        "🔴 Nền phải MAGENTA thuần `#FF00FF`, đúng 1 vật/ảnh (xem docstring đầu file).\n"
        "Cắt nền: `python tools/cutout_sticker.py 18_nenkin-60sai-kuriage-tsuki4man3sen`\n"
    )
    for i, (fn, obj, person) in enumerate(SPEC18, 1):
        p = compose(obj, person)
        flow.append(p)
        ten.append(f'{fn:<26}<- dòng {i} FLOW')
        blocks.append(f"\n## {i}. `{fn}`\n\n```\n{p}\n```\n")

    (vdir / "sticker_prompts_v18_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (vdir / "sticker_prompts_v18_BLOCKS.md").write_text("".join(blocks), encoding="utf-8")
    (vdir / "sticker_prompts_v18_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")

    ln = [len(x) for x in flow]
    print(f"✓ {len(flow)} prompt sticker MỚI → {vdir}")
    print(f"   độ dài: min {min(ln)} · TB {sum(ln)//len(ln)} · max {max(ln)} ký")
    return 0


if __name__ == "__main__":
    sys.exit(main())

