# -*- coding: utf-8 -*-
r"""build_demo21b.py — SLIDES cho DEMO 60–90s của công thức "SÂN KHẤU SƠ ĐỒ" (v3).

Đây là **Cổng 1 mục 2** của plan: dựng 1 khối ngắn để user duyệt bằng mắt TRƯỚC khi
làm cả bài. Khối chọn = 税率 của video 21, viết lại theo B3 (61,7s giải thích chay →
3 câu hỏi của 聞き手 cách nhau ≤20s). Tiếng đã có sẵn: `06_VIDEO/_demo_2voice/`.

Thẻ bám đúng 5 luật mới:
  · mỗi thẻ MỘT sơ đồ chở số (T1) — compare · art+pins · big · compare · bars
  · sơ đồ ≥50% (T3): 3/5 = 60%
  · thẻ có số ⇒ có `src` (T6)
  · `cast_beats` để khe sự kiện ≤9s (sàn đơn vị MỚI) — thẻ giữ 12–17s vẫn sạch
  · 原典 = ảnh chụp + `frame` mọc dần + `quote` trích 《》 đỏ (không vẽ khoanh vào ảnh)

CHẠY:  python tools/build_demo21b.py
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO = os.path.join(PROJ, "06_VIDEO", "_demo_2voice")
GB = json.load(io.open(os.path.join(PROJ, "06_VIDEO",
                                    "21_fuyo-shinkokusho-205man",
                                    "genten_boxes.json"), encoding="utf-8"))
TL = json.load(io.open(os.path.join(DEMO, "timeline.json"), encoding="utf-8"))["lines"]
NL = "\n"
SRC_FAQ = "日本年金機構「扶養親族等申告書」FAQ（令和8年8月時点）"

# ── mốc thẻ theo timeline THẬT (dòng nào → thẻ nào) ─────────────────────────────
# 🔴 Lấy giây từ timeline, KHÔNG ước: `feedback_timeline_phai_do_tu_wav_that`.
SPAN = [(0, 1), (2, 2), (3, 4), (5, 6), (7, 8)]     # (dòng đầu, dòng cuối) mỗi thẻ


def sec(i0, i1):
    return round(TL[i1]["end"] - TL[i0]["start"], 2), round(TL[i0]["start"], 2)


g4 = GB["genten21b_04"]

CARDS = [
    # ── 0 · phản bác định kiến. Hai lối, CÙNG một con số ⇒ chính nó là sơ đồ ──
    dict(layout="compare", title="税率は、同じです",
         panels=[{"cap": "出した" + NL + "５.１０５％", "icon": "doc"},
                 {"cap": "出さなかった" + NL + "５.１０５％", "icon": "doc"}],
         rows=["変わるのは、税率ではありません"],
         src=SRC_FAQ,
         left="sensei_serious", right="kikite_worried",
         beats=[0.4, 0.9, 5.9],
         cast_beats={"right": [[0, "kikite_worried"], [5.6, "kikite_think"]],
                     "left": [[0, "sensei_serious"], [5.6, "sensei_explain"]]}),

    # ── 1 · 原典: ảnh chụp thật + khoanh MỌC DẦN + trích 《》 đỏ ──────────────
    dict(layout="art", title="年金機構は、こう書いています",
         img=g4["img"],
         src=g4["src"],
         left="sensei_point", right="kikite_listen",
         beats=[0.3],
         pins=[{"kind": "frame", "box": g4["boxes"][0], "beat": 3.2, "w": 9},
               {"kind": "quote", "at": [0.50, 0.86], "w": 0.94, "size": 42,
                "beat": 6.4, "t": g4["quote"]}],
         cast_beats={"right": [[0, "kikite_listen"], [3.2, "kikite_think"],
                               [7.0, "kikite_nod"]],
                     "left": [[0, "sensei_point"], [6.4, "sensei_explain"]]}),

    # ── 2 · chốt cái ĐỔI ─────────────────────────────────────────────────────
    dict(layout="big", title="変わるのは、こちら", value="控除", unit="",
         cap="引ける控除が、消えます", pop=True,
         src=SRC_FAQ,
         left="sensei_explain", right="kikite_surprised",
         beats=[0.5],
         cast_beats={"right": [[0, "kikite_surprised"], [3.0, "kikite_think"]]}),

    # ── 3 · hai cột: cái gì còn, cái gì mất ──────────────────────────────────
    dict(layout="compare", title="引ける控除の、中身",
         panels=[{"cap": "出した", "icon": "doc"},
                 {"cap": "出さなかった", "icon": "doc"}],
         rows=["基礎的な控除　　　　両方あります",
               "配偶者・扶養の分　　出した人だけ",
               "障害のあるかたの分　出した人だけ"],
         src=SRC_FAQ,
         left="sensei_explain", right="kikite_listen",
         beats=[0.4, 0.9, 2.2, 6.0, 10.5],
         cast_beats={"right": [[0, "kikite_listen"], [5.0, "kikite_think"],
                               [11.0, "kikite_worried"]],
                     "left": [[0, "sensei_explain"], [8.0, "sensei_point"]]}),

    # ── 4 · số đắt nhất, và nó ĐƯỢC TÍNH RA chứ không rơi từ trời ────────────
    dict(layout="bars", title="高橋さんの場合",
         label_w=380,
         rows=[["出した", 168000, "ok", "16万8千円"],
               ["出さなかった", 188000, "bad", "18万8千円"]],
         src=SRC_FAQ,
         left="sensei_conclude", right="kikite_surprised",
         beats=[0.5, 1.6, 3.0],
         pins_card=[{"kind": "num", "t": "差は 年２万円", "at": [0.50, 0.78],
                     "size": 104, "w": 0.56, "beat": 8.6}],
         cast_beats={"right": [[0, "kikite_listen"], [3.0, "kikite_surprised"],
                               [9.0, "kikite_down"]],
                     "left": [[0, "sensei_explain"], [8.6, "sensei_conclude"]]}),
]

slides = []
for k, (i0, i1) in enumerate(SPAN):
    d, s0 = sec(i0, i1)
    st = dict(CARDS[k])
    st["sub"] = None
    slides.append({"index": k, "video": True, "sec": d, "start": s0,
                   "match": TL[i0]["text"][:18], "stage": st})

out = os.path.join(PROJ, "03_SCRIPTS", "demo21b_SLIDES.json")
io.open(out, "w", encoding="utf-8").write(
    json.dumps(slides, ensure_ascii=False, indent=1))
tot = sum(s["sec"] for s in slides)
print(f"→ {out}")
for s in slides:
    print(f"  [{s['index']:02d}] {s['stage']['layout']:8s} {s['start']:6.2f}s +{s['sec']:5.2f}s "
          f"| {s['match']}")
print(f"tổng {tot:.2f}s · {len(slides)} thẻ = {len(slides)/(tot/60):.2f} thẻ/phút")
