# -*- coding: utf-8 -*-
r"""plan30.py — SCENE PLAN cho video 30 (khuôn v27/v28/v29, không đổi cơ khí).

Chỉ khác `plan29.py` ở **STEM + bảng CHAPTERS + FLOW_AFTER**. Cơ chế gom ô, chip chương,
màn 「本日の流れ」 giữ nguyên ở `plan28.py`.

🔴 CUE PHẢI LÀ VĂN BẢN SAU KHI ĐỔI SỐ (`make_tts` đổi 漢数字 → Ả Rập) và phải khớp ĐÚNG 1 dòng
của `_TTS.md`. Cả 9 cue dưới đã đối chiếu với `_TTS.md` v2 (2026-09-24).

CHẠY:  python tools/plan30.py            → in bảng plan + ghi 06_VIDEO/<stem>/plan30.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan28 as base  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STEM = "30_nenkin-furikomi-10gatsu-fueru-hito"

# ── CHƯƠNG — chip ≤12 ký full-width (góc trên-trái) ─────────────────────────
CHAPTERS = [
    ("0", "",          "はじめに",       None),
    ("1", "3つの容疑者", "を消す",         "一つ目の容疑者は"),
    ("2", "減る側",      "中村さん",       "では、この精算で"),
    ("3", "増える側",    "加藤さん",       "では、反対に増える側"),
    ("4", "あなたの紙",  "3つの場所",      "では、あなたは、どちらの側"),
    ("5", "今年だけ",    "みなし課税",     "冒頭でお約束した"),
    ("6", "来年の10月",  "もう一度驚く",   "では最後に、冒頭の"),
    ("7", "",          "研究ノート",     "それでは、今日の研究ノート"),
    ("8", "",          "やること3つ",    "今日から、三つだけ"),
]

# 3 màn 「本日の流れ」: sau cold open · trước 「あなたの紙」 · trước みなし課税
FLOW_AFTER = ["まずは、疑わしいものを", "では、あなたは、どちらの側", "冒頭でお約束した"]

base.STEM = STEM
base.VD = PROJ / "06_VIDEO" / STEM
base.HOLD_TARGET = 13.0   # 17′ ÷ 11,6s ≈ 5,6 đổi/phút, dưới trần 6,0
base.PLAN_NAME = "plan30.json"
base.CHAPTERS = CHAPTERS
base.FLOW_AFTER = FLOW_AFTER

if __name__ == "__main__":
    sys.exit(base.main())
