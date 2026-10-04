# -*- coding: utf-8 -*-
r"""plan32.py — SCENE PLAN cho video 32 (本人確認 2027 · 免許証の暗証番号2つ), khuôn v27–v31.

Chỉ khác `plan31.py` ở STEM + CHAPTERS + FLOW_AFTER. Cơ chế gom ô ở `plan28.py`.
🔴 Cue chương phải là TIỀN TỐ của một dòng `_TTS.md` v2 (2026-09-28); ⛔ không chứa 方.
CHẠY:  python tools/plan32.py   → 06_VIDEO/<stem>/plan32.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan28 as base  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STEM = "32_ginko-honnin-kakunin-2027"

CHAPTERS = [
    ("0", "",          "はじめに",       None),
    ("1", "警察庁の",    "チラシ",        "冒頭の場面は、どこに"),
    ("2", "今ある",      "口座は？",      "では、あなたが、いま気になっているのは"),
    ("3", "佐藤さんの",   "暗証番号",      "当研究室のモニター、仙台"),
    ("4", "忘れたときの", "3つの道",       "では、佐藤さんのように"),
    ("5", "なぜ国は",    "中を読む？",     "では、冒頭の、もう一つ"),
    ("6", "",          "研究ノート",     "それでは、今日の研究ノート"),
    ("7", "",          "セルフチェック",  "最後に、3つだけ"),
]

# 3 màn 「本日の流れ」: sau cold open · trước 3 con đường · trước câu trả lời lớn
FLOW_AFTER = ["まず、事実から", "では、佐藤さんのように", "では、冒頭の、もう一つ"]

base.STEM = STEM
base.VD = PROJ / "06_VIDEO" / STEM
base.HOLD_TARGET = 12.5
base.PLAN_NAME = "plan32.json"
base.CHAPTERS = CHAPTERS
base.FLOW_AFTER = FLOW_AFTER

if __name__ == "__main__":
    sys.exit(base.main())
