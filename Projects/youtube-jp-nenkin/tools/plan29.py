# -*- coding: utf-8 -*-
r"""plan29.py — SCENE PLAN cho video 29 (khuôn v27/v28, không đổi cơ khí).

Chỉ khác `plan28.py` ở **STEM + bảng CHAPTERS + FLOW_AFTER**. Cơ chế gom ô, chip chương,
màn 「本日の流れ」 giữ nguyên — đừng sửa ở đây, sửa thì sửa `plan28.py` rồi port sang.

🔴 CUE PHẢI LÀ VĂN BẢN SAU KHI ĐỔI SỐ. `make_tts` đổi 漢数字 → Ả Rập (七十五歳 → 75歳,
八月 → 8月) và 方(ほう) → かた, nên cue viết bằng kanji-số sẽ TRƯỢT hết. Cả 8 cue dưới đây
đã đối chiếu 1-1 với `_TTS.md` (mỗi cue khớp ĐÚNG 1 dòng) trước khi chốt.

⚠️ Chương 7 KHÔNG mở bằng 「一つ。」 — `make_tts` tách câu ở 。 nên 「1つ。」 đứng riêng rồi bị
gộp ngược vào dòng trước; dòng thật bắt đầu bằng 「7月に届いた封筒を、」. Đây là lý do phải
đối chiếu cue với `_TTS.md`, không đoán từ bản `.md`.

CHẠY:  python tools/plan29.py            → in bảng plan + ghi 06_VIDEO/<stem>/plan29.json
       python tools/plan29.py --prompts  → thêm bảng gợi ý nội dung ảnh từng ô
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan28 as base  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STEM = "29_shikaku-kakuninsho-8gatsu-85sai"

# ── 8 CHƯƠNG — chip ≤12 ký full-width (góc trên-trái, không đè nội dung) ─────
CHAPTERS = [
    ("0", "",            "はじめに",       None),
    ("1", "8月1日",       "何が終わった",   "75歳以上のかたは"),
    ("2", "一本目の線",    "6回",           "では、どちらが届くのか"),
    ("3", "二本目の線",    "85歳",          "もう一本、年齢の線"),
    ("4", "○×クイズ",     "4問",           "では、ここで四問だけ"),
    ("5", "限度区分",      "空欄の罠",       "冒頭で、もう一つ申し上げ"),
    ("6", "使えなかった日", "10割と2年",     "もし、当日にどうにも"),
    ("7", "やること",      "封筒と欄",       "7月に届いた封筒を"),
    ("8", "",            "研究ノート",     "それでは、今日の研究ノート"),
]

# 3 màn 「本日の流れ」: sau cold open · trước ○×クイズ · trước khối lối thoát
FLOW_AFTER = ["まず、事実から", "では、ここで四問だけ", "もし、当日にどうにも"]

base.STEM = STEM
base.VD = PROJ / "06_VIDEO" / STEM
# 16:34 ÷ 10,0s = 96 ô = 6,0 đổi/phút — CHẠM trần 6,0 của `audience-45plus.md` §2 mục 1.
# 10,8s ⇒ ~89 ô ⇒ ~5,6/phút, vẫn trên sàn "giữ hình ≥3,0s" của §2.0-quater.
base.HOLD_TARGET = 13.0   # v2 2026-09-24: 16:36 -> <=95 o de ghep du bo anh v1
base.PLAN_NAME = "plan29.json"
base.CHAPTERS = CHAPTERS
base.FLOW_AFTER = FLOW_AFTER

if __name__ == "__main__":
    sys.exit(base.main())
