# -*- coding: utf-8 -*-
"""
brand2_prompts.py — sinh prompt LOGO + MASCOT bản 2 cho kênh nenkin (user chốt 2026-09-10:
*"logo góc trên phải gen cái khác đi · video ông già góc dưới phải gen lại cái khác rồi cắt lại"*).

Xuất 3 file (khuôn 4-file của `ab-3title-3thumb.md` §3 Bước 4, bỏ PLATE vì đây không phải
thumbnail bake chữ):
  `_BRAND2_logo_FLOW.txt`    — 3 prompt LOGO, mỗi prompt 1 DÒNG
  `_BRAND2_mascot_FLOW.txt`  — 3 prompt MASCOT (video 8s), mỗi prompt 1 DÒNG
  `_BRAND2_prompts_TENFILE.txt` — dòng ↔ tên file đích
Bản người đọc: `_BRAND2_prompts_BLOCKS.md`.

🔴 BỐN CHỖ CỐ Ý KHÁC bộ prompt cũ, mỗi chỗ bịt một lỗi ĐÃ DÍNH THẬT:
  ① **`no glow and no light flare around the badge`** — logo cũ có quầng sáng hồng ở rìa
     trái, và chính nó là thứ sống sót qua phép tách magenta (quầng hồng nhạt có `b−g`≈20
     nên lọt ngưỡng). Chặn từ prompt rẻ hơn vá sau.
  ② **`the camera is locked off … stays in exactly the same spot`** — `mascot_chroma.py`
     crop theo **HỢP bbox mọi frame**; nhân vật đi lại thì bbox phình và mascot co bé tí.
  ③ **`surfaces are plain and unmarked`** thay cho `no text` — mô tả TÍCH CỰC, model đọc
     TỪ KHOÁ chứ không đọc chữ "no" (`_policy20.py` §①). Riêng `no watermark` thì GIỮ
     nguyên dạng phủ định vì `ab-3title-3thumb.md` §3 mục 8 ⑥ bắt buộc câu đó.
  ④ **ép cỡ bằng MÉP KHUNG** (`almost touching the top edge`), không bằng phần trăm —
     model nghe VỊ TRÍ, không nghe TỈ LỆ (`media-library.md` §2.10 ⑥).
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"

# ── LOGO ─────────────────────────────────────────────────────────────────────
LOGO_HEAD = (
    "a circular emblem badge icon, flat vector illustration with thick clean outlines and "
    "soft cel shading, a wide gold ring border around a deep navy blue interior, one single "
    "bold symbol centred inside, very high contrast so it stays readable at a tiny size"
)
LOGO_FRAME = (
    "the badge is centred and fills the whole height of the frame, the top of the gold ring "
    "almost touching the top edge and the bottom of the ring almost touching the bottom edge, "
    "seen straight on"
)
LOGO_BG = (
    "the background is a completely flat uniform magenta screen, pure saturated magenta, "
    "evenly lit, no gradient and no texture, the badge casts no shadow on the background, "
    "no glow and no light flare around the badge, the edge of the gold ring is crisp"
)
TAIL = "surfaces are plain and unmarked. no watermark, no signature, no lettering of any kind"

LOGOS = [
    ("logo_tsucho.png",
     "the symbol is an open bank passbook booklet in cream and white with ruled lines, and a "
     "single gold coin resting against its lower right corner"),
    ("logo_flask.png",
     "the symbol is a glass laboratory beaker with a wide base, three gold coins stacked "
     "inside the bottom of the beaker"),
    ("logo_fukurou.png",
     "the symbol is a plump golden owl perched on one large gold coin, its two big round eyes "
     "facing forward"),
]

# ── MASCOT ───────────────────────────────────────────────────────────────────
MAS_FRAME = (
    "the character is centred and fills the whole height of the frame, the top of its head "
    "almost touching the top edge and its feet almost touching the bottom edge, filmed "
    "straight on at eye level, the camera is locked off and does not move, no zoom and no pan, "
    "the character stays in exactly the same spot for the whole shot"
)
MAS_BG = (
    "the background is a completely flat uniform chroma key green screen, pure green, evenly "
    "lit, no gradient and no texture, the character casts no shadow on the background, there "
    "is no floor and no props, the character is lit evenly from the front"
)
# ⛔ Tư thế idle CHỈ được có một việc: 8 giây một hành động (CLAUDE.md §② khối Veo).
IDLE = ("the character stands calmly and breathes, its shoulders rising and falling gently, "
        "it blinks a few times and tilts its head slightly to one side, a warm friendly "
        "expression")

MASCOTS = [
    ("m2_obaa_idle.mp4",
     "a cheerful elderly Japanese woman mascot, chibi proportions about three heads tall, soft "
     "rounded 3D animation style with thick clean outlines, silver-white hair in a neat bun, "
     "round gold-rimmed glasses, a teal knit vest over a cream blouse, a long dark skirt, "
     "brown shoes, a small closed notebook held in one hand"),
    ("m2_neko_idle.mp4",
     "a friendly calico cat mascot, chibi proportions about three heads tall, soft rounded 3D "
     "animation style with thick clean outlines, white fur with orange and black patches, "
     "round gold-rimmed glasses, a small navy bow tie, standing upright on its hind legs"),
    ("m2_fukurou_idle.mp4",
     "a friendly brown and cream owl mascot, chibi proportions about three heads tall, soft "
     "rounded 3D animation style with thick clean outlines, large round amber eyes, round "
     "gold-rimmed glasses resting on its beak, a small navy bow tie, standing upright with "
     "its wings tucked at its sides"),
]


def one_line(s: str) -> str:
    return " ".join(s.split())


def main() -> int:
    logo_rows = [(f, one_line(f"{LOGO_HEAD}. {sym}. {LOGO_FRAME}. {LOGO_BG}. {TAIL}"))
                 for f, sym in LOGOS]
    mas_rows = [(f, one_line(f"{char}. {IDLE}. {MAS_FRAME}. {MAS_BG}. {TAIL}"))
                for f, char in MASCOTS]

    for name, rows in (("_BRAND2_logo_FLOW.txt", logo_rows),
                       ("_BRAND2_mascot_FLOW.txt", mas_rows)):
        p = os.path.join(OUT, name)
        io.open(p, "w", encoding="utf-8").write("\n".join(r[1] for r in rows) + "\n")
        print(f"✅ {name}  ({len(rows)} prompt)")

    ten = os.path.join(OUT, "_BRAND2_prompts_TENFILE.txt")
    with io.open(ten, "w", encoding="utf-8") as fh:
        fh.write("# _BRAND2_logo_FLOW.txt  (anh, nen MAGENTA)\n")
        for i, (f, _) in enumerate(logo_rows, 1):
            fh.write(f"dong {i} -> {f}\n")
        fh.write("\n# _BRAND2_mascot_FLOW.txt  (video 8s, nen XANH chroma)\n")
        for i, (f, _) in enumerate(mas_rows, 1):
            fh.write(f"dong {i} -> {f}\n")
    print(f"✅ _BRAND2_prompts_TENFILE.txt")

    # ── gate: độ dài + không được có ký tự xuống dòng lọt vào giữa prompt ────
    bad = 0
    for tag, rows in (("logo", logo_rows), ("mascot", mas_rows)):
        for f, s in rows:
            flag = ""
            if len(s) > 1500:                       # trần mềm của kênh, ab-3title §3.1 Bước 3
                flag = "  🔴 dài > 1500 ký"
                bad += 1
            if "\n" in s:
                flag += "  🔴 có newline giữa prompt"
                bad += 1
            print(f"   {tag:<7} {f:<22} {len(s):>5} ký{flag}")
    if bad:
        print(f"\n🔴 {bad} prompt vi phạm")
        return 1
    print("\n✓ gate sạch — bơm `_BRAND2_logo_FLOW.txt` và `_BRAND2_mascot_FLOW.txt` "
          "vào extension. Đọc `_BRAND2_prompts_BLOCKS.md` trước khi gen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
