# -*- coding: utf-8 -*-
r"""videogen_nenkin.py — HỒ SƠ KÊNH nenkin cho công thức clip AI của `youtube-jp-showa`.

⛔ **KHÔNG viết công thức mới.** Khuôn 6 khối, danh sách FRAMING đóng, và toàn bộ gate đều
lấy từ `youtube-jp-showa/tools/videogen_lib.py` — bản đã có **số chứng minh**: cùng một lô
22 clip, v1 = **22/22 lỗi**, v2 = **2/22 lỗi** (`showa/04_VIDEOGEN_PROMPTS.md` §10).
File này chỉ đổi ba khối mà kênh khác nhau thật: STYLE (Nhật HIỆN ĐẠI, không phim 8mm),
AVOID, và thêm gate cho **đúng những cơ chế đã làm hỏng clip nenkin v21**.

## Ba cơ chế hỏng của v21, đo được — và luật chặn từng cái

| đo được ở v21 | luật ở đây |
|---|---|
| **kính đeo lên rồi BIẾN MẤT khỏi mặt** (ca tệ nhất) | `G_GLASS`: cấm mọi động từ đeo/tháo kính. Nhân vật **đeo sẵn từ đầu**, và mô tả kính nằm trong CAST |
| **58/73 clip có thao tác tay với vật nhỏ; 4/6 soi kỹ hỏng** — nắp hộp thư đóng rồi mở lại, phong bì biến mất, bút đỏ nhân đôi, thao tác chạy ngược thứ tự | `G_STATE`: cấm động từ **ĐỔI TRẠNG THÁI VẬT** (mở/gấp/đeo/tháo/nhặt lên/đặt xuống/viết thêm nét). Vật phải ở **tư thế CUỐI** ngay từ frame đầu. Beat nào bắt buộc phải đổi trạng thái ⇒ **ảnh tĩnh**, không clip |
| **11/84 shot có người VIẾT SỐ/CHỮ → chữ nát vô nghĩa** (frame 10800 ra 「50 ≒ 50 0 ハ」 chiếm ¼ khung) | `G_TEXT`: cấm động từ viết + cấm tả chữ trên giấy. Mặt giấy/bảng **để TRỐNG**; hành động chuyển sang **KÝ HIỆU** (vòng tròn · gạch ngang · mũi tên · dấu ＋ ＝ · ✓). Con số do **thẻ** chở — nay thẻ chiếm 49,9% video |

🔴 Và luật gốc của showa vẫn thắng ở chỗ nó đã trả giá để học: **cấm mọi framing không có
THÂN người** (14/21 clip `hands only` của showa hỏng). Cận vật ⇒ dùng `ots`/`medium`.

⚠️ Mô tả **TÍCH CỰC**, đừng viết phủ định vào ACT: bộ lọc Google đọc TỪ KHOÁ chứ không đọc
phủ định (`_policy20.py` §①). Nên viết `the board surface is clean and empty`, KHÔNG viết
`no text on the board`. Phủ định chỉ nằm trong khối `AVOID` cuối prompt.
"""
import os
import re
import sys

sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
from videogen_lib import (build, gate, write_outputs, FRAMINGS,   # noqa: E402
                          bad_framing, expand)                    # noqa: F401

# ═════════════════════════════════════════════════════════════════════════════
# STYLE LOCK — Nhật HIỆN ĐẠI, photoreal. Không một chữ nào nhắc tới phim nhựa:
# showa đo được rằng model gắn dải phim + chữ FUJI vào *khái niệm* "8mm film" ở
# tầng sâu hơn chữ nghĩa (22/22 clip vẫn có viền dù đã cấm đích danh). Không nhắc
# thì không có viền ⇒ nenkin KHÔNG cần bước crop viền của showa.
# ═════════════════════════════════════════════════════════════════════════════
STYLE = ("present-day Japan, photorealistic documentary video, natural available light, "
         "calm muted colors, shallow depth of field, unremarkable everyday surroundings, "
         "the image fills the entire frame edge to edge, 16:9")

MOTION = ("slow deliberate natural human motion, continuous single take, no cuts, "
          "the subject remains in frame for the whole shot, no reversing, "
          "every object keeps the same shape, color and position for the whole shot")
MOTION_EXIT = ("slow deliberate natural human motion, continuous single take, no cuts, no reversing, "
               "every object keeps the same shape, color and position for the whole shot")

# AVOID — cấm ĐÍCH DANH. Bài học showa: negative chung (`readable text`) không chặn nổi thứ
# model coi là thành phần của cảnh; phải gọi tên VẬT + VỊ TRÍ.
# 🔴 SUA 2026-09-06 sau lo 54 clip: ban dau cam "letters, words, numbers, kanji ... on any
# PAPER, FORM" => model bo luon ca LUOI O KE, tra ve giay TRANG TRON. Do bang mat: chi
# **5-7 trong ~33 shot co giay** hien duoc net ke. Dung co che showa da do: model gan thu
# bi cam vao *khai niem* sau hon chu nghia — cam "chu tren giay" thanh "giay khong co gi".
# ⇒ Bo `paper, form` khoi cum nay; cam DICH DANH chu VIET/IN chu khong cam moi net muc.
#   Luoi o ke duoc mo ta TICH CUC ben ACT (prop `youshi`), dat o DAU cum danh tu.
AVOID = ("Avoid: kanji, japanese characters, handwriting, printed words, sentences or logos "
         "on the form, envelope, whiteboard, screen or sign, "
         "eyeglasses appearing or disappearing, glasses being put on or taken off, a second pair of glasses, "
         "objects appearing or vanishing, duplicated objects, a second pen or a second envelope, "
         "lids or flaps opening or closing, paper being folded or unfolded, "
         "disembodied hands, floating limbs, extra fingers, morphing objects, objects changing shape or color, "
         "reversing motion, walking backwards, turning to face the camera, looking at the camera, "
         "anime style, illustration, cartoon, oversaturated colors, HDR look, fast cuts, camera shake, "
         "text overlays, captions, subtitles, watermarks, on-screen graphics")

PROF = {"STYLE": STYLE, "MOTION": MOTION, "MOTION_EXIT": MOTION_EXIT, "AVOID": AVOID}

# ═════════════════════════════════════════════════════════════════════════════
# GATE riêng của nenkin — ba cơ chế hỏng đã đo được
# ═════════════════════════════════════════════════════════════════════════════
# ① KÍNH: ca tệ nhất của v21. Kính phải ĐEO SẴN, mô tả trong CAST.
G_GLASS = re.compile(r"\b(put(?:s|ting)?|take(?:s|n)?|remov\w*|slid\w*|push\w*|lift\w*|lower\w*|adjust\w*)"
                     r"\s+(?:\w+\s+){0,3}(glasses|spectacles|eyeglasses)\b|"
                     r"\b(glasses|spectacles)\s+(?:on|off)\b", re.I)
# ② ĐỔI TRẠNG THÁI VẬT: 58/73 clip v21 dính, 4/6 soi kỹ hỏng.
G_STATE = re.compile(r"\b(open(?:s|ing)?|clos(?:e|es|ing)|shut(?:s|ting)?|unfold(?:s|ing)?|fold(?:s|ing)?|"
                     r"tear(?:s|ing)?|rip(?:s|ping)?|seal(?:s|ing)?|unseal\w*|"
                     r"pick(?:s|ing)? up|put(?:s|ting)? down|set(?:s|ting)? down|take(?:s|ing)? out|"
                     r"pull(?:s|ing)? out|insert(?:s|ing)?|slide(?:s|ing)? (?:in|out)|"
                     r"flip(?:s|ping)?|turn(?:s|ing)? over|turn(?:s|ing)? the page)\b", re.I)
# ③ VIẾT CHỮ: 11/84 shot v21 ra chữ nát. Ký hiệu thì được, chữ/số thì không.
G_TEXT = re.compile(r"\b(writ\w+|write|writes|fills? in|fill(?:s|ing)? out|sign(?:s|ing)?|"
                    r"jots?|notes? down|prints?|types?)\b|"
                    r"\b(number|numbers|digit|digits|word|words|kanji|text|figure of)\b\s+(?:on|onto|in)\b", re.I)
# Ký hiệu ĐƯỢC PHÉP — có mặt thì G_TEXT không báo oan
SYMBOL_OK = re.compile(r"\b(circle|circles|circling|underlin\w+|arrow|tick|check ?mark|cross|"
                       r"plus sign|equals sign|line under|red ring|red circle)\b", re.I)


def gate_nenkin(S, C, quiet=False):
    """Ba gate riêng nenkin. Trả về số 🔴. Chạy CÙNG `videogen_lib.gate`, không thay nó."""
    red = 0
    for sid, blk, act, preset, cam, tier in S:
        a = expand(act, C)
        def R(msg):
            nonlocal red
            red += 1
            if not quiet:
                print(f"  🔴 [{sid}] {msg}")
        if G_GLASS.search(a):
            R("ĐỘNG TỪ ĐEO/THÁO KÍNH — ca hỏng tệ nhất của v21 (kính biến mất khỏi mặt). "
              "Cho nhân vật ĐEO SẴN, tả kính trong CAST, bỏ hành động này")
        m = G_STATE.search(a)
        if m:
            R(f"ĐỔI TRẠNG THÁI VẬT 「{m.group(0)}」 — 58/73 clip v21 dính, 4/6 soi kỹ hỏng "
              f"(nắp mở lại, phong bì biến mất, bút nhân đôi). Cho vật ở TƯ THẾ CUỐI ngay từ "
              f"frame đầu, hoặc dùng ẢNH TĨNH cho beat này")
        m = G_TEXT.search(a)
        if m and not SYMBOL_OK.search(a):
            R(f"VIẾT CHỮ/SỐ 「{m.group(0)}」 — Veo trả về chữ nát (11/84 shot v21). "
              f"Đổi sang KÝ HIỆU: vòng tròn · gạch chân · mũi tên · dấu ＋ ＝ · ✓. "
              f"Con số để THẺ chở")
        if cam not in FRAMINGS:
            R(f"FRAMING 「{cam}」 ngoài danh sách đóng — dùng khoá: {', '.join(FRAMINGS)}")
    if not quiet:
        print(f"── gate nenkin: {red} 🔴 trên {len(S)} shot ──")
    return red


def build_n(S, P, C):
    return build(S, P, C, prof=PROF)


def gate_n(rows, S, P, C, **kw):
    kw.setdefault("prof", PROF)
    n_red, warn = gate(rows, S, P, C, **kw)
    return n_red + gate_nenkin(S, C), warn


def write_n(rows, outdir=".", prefix="flow21b", only=None):
    return write_outputs(rows, outdir, prefix, only, prof=PROF)


if __name__ == "__main__":
    # selftest: ba ACT hỏng CỐ Ý — mỗi cái phải bị đúng một gate bắt
    C = {"m1": "a man in his sixties in a plain grey cardigan wearing thin metal-rimmed glasses"}
    S = [
        ("T1", "x", "A_M1 puts on his glasses, then looks down, then nods", "p", "medium", "Q"),
        ("T2", "x", "A_M1 opens the envelope, then pulls out the form, then sets it down", "p", "ots", "Q"),
        ("T3", "x", "A_M1 writes the number on the form, then pauses, then looks at it", "p", "ots", "Q"),
        ("T4", "x", "A_M1 draws a red circle around one line, then taps it twice, then sits back", "p", "ots", "Q"),
        ("T5", "x", "A_M1 rests both hands on the table, then shifts weight, then looks aside", "p", "hands only", "Q"),
    ]
    n = gate_nenkin(S, C)
    ok = n == 4          # T1 kính · T2 trạng thái · T3 viết chữ · T5 framing; T4 phải SẠCH
    print(("SELFTEST PASS" if ok else f"SELFTEST FAIL (bắt {n}, kỳ vọng 4)"))
    sys.exit(0 if ok else 1)
