# -*- coding: utf-8 -*-
r"""plan31.py — SCENE PLAN cho video 31 (扶養親族等申告書 → 非課税世帯 domino), khuôn v27–v30.

Chỉ khác `plan30.py` ở **STEM + bảng CHAPTERS + FLOW_AFTER**. Cơ chế gom ô, chip chương,
màn 「本日の流れ」 giữ nguyên ở `plan28.py`.

🔴 Cue chương phải là TIỀN TỐ của một dòng `_TTS.md` v2 (2026-09-26) sau khi đổi số; ⛔ không chứa 方.

CHẠY:  python tools/plan31.py            → in bảng plan + ghi 06_VIDEO/<stem>/plan31.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan28 as base  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STEM = "31_fuyo-shinkokusho-hikazei-domino"

# ── CHƯƠNG — chip ≤12 ký full-width (góc trên-trái) ─────────────────────────
CHAPTERS = [
    ("0", "",          "はじめに",       None),
    ("1", "所得税の紙が", "住民税の紙に",   "所得税のかからない人にまで"),
    ("2", "148万円",    "線は家族で動く", "では、148万円という数字"),
    ("3", "木村さん",    "ご夫妻",        "冒頭の、通知が二通"),
    ("4", "封筒から",    "通帳までの2年",  "では、もしこの封筒が"),
    ("5", "損をするのは", "だれ？",        "では、冒頭の、もう一つ"),
    ("6", "",          "研究ノート",     "それでは、今日の研究ノート"),
    ("7", "",          "○×クイズ",      "最後に、○×で"),
]

# 3 màn 「本日の流れ」: sau cold open · trước hành trình 2 năm · trước câu trả lời lớn
FLOW_AFTER = ["まず、事実から", "では、もしこの封筒が", "では、冒頭の、もう一つ"]

base.STEM = STEM
base.VD = PROJ / "06_VIDEO" / STEM
base.HOLD_TARGET = 12.5   # 15,5′: 11,5 ra 6,0/phút (chạm trần) → 12,5
base.PLAN_NAME = "plan31.json"
base.CHAPTERS = CHAPTERS
base.FLOW_AFTER = FLOW_AFTER

if __name__ == "__main__":
    sys.exit(base.main())
