#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""check_stage_pace.py — GATE NHỊP HÌNH cho lớp SÂN KHẤU (`make_stage`).

    python check_stage_pace.py <SLIDES.json> <timeline.json> [--max-gap 9] [--max-card-per-min 6]

Bản đọc SLIDES của `check_frame_pace.py` (bản đó đọc `project.json` của Remotion).
Cùng ý đồ, **khác ĐƠN VỊ** — và cái khác đó là toàn bộ lý do file này tồn tại.

⭐ ĐỔI ĐƠN VỊ (user chốt 2026-09-06). `audience-45plus.md` §2.0b đo sàn bằng **ẢNH CHÍNH**
đổi mỗi ≤9s. Đo trên file thật của 4 video đối thủ (`~/Downloads/Video/`, 2026-09-06):

  | | đổi THẺ/hình lớn | SỰ KIỆN hình nhỏ | khe >9s |
  |---|---|---|---|
  | カメ先生 101K, 17:28 | 2,8/phút · median 19,7s · max 57,9s | **19,4/phút · median 3,0s** | **1/340** |
  | お金の保健室 190K, 29:00 | 2,2/phút · median 26,5s · max 53,7s | **20,2/phút · median 2,8s** | **0/587** |
  | nenkin 21 (bài bị chê) | 5,9/phút | — | — |

Tức hai kênh thắng **giữ một thẻ 20–58 giây** — vi phạm sàn cũ ở 95–99% thời lượng — nhưng
khung của chúng **không bao giờ chết quá 9 giây**, vì thứ đổi mỗi ~3s là: một dòng phụ đề
ngắn · **tư thế cast** · một phần tử của sơ đồ mọc thêm. Còn nenkin 21 cắt cảnh **nhiều thứ
hai** trong cả bộ mà vẫn chán nhất — vì mỗi cắt đổi *mood*, không đổi *nghĩa*.
⇒ Ý của luật cũ đúng (khung không được chết), **đơn vị thì sai**. Cùng họ với bài học
`feedback_doi_don_vi_hinh_ra_ca_lo` và `audience-45plus` §6.10 (*gate đo sai thứ nó muốn đo*).

Ba đại lượng đo ở đây:
  ① TRẦN đổi THẺ  ≤6/phút   — chống MỆT (giữ nguyên tinh thần §2 mục 1)
  ② SÀN SỰ KIỆN   ≤9,0s/khe — chống CHÁN. Sự kiện = thẻ mới · beat của `beats` ·
                              pin có `beat` · props có `t0` · **cast đổi tư thế** ·
                              dòng phụ đề mới (từ timeline)
  ③ Thẻ giữ >30s  — trần clip của `make_stage`; quá đây thì phần tử cuối KHÔNG kịp hiện

⚖️ **Cái mất, biết trước:** đơn vị mới dễ bị lách bằng sự kiện rẻ tiền (nhấp nháy một icon
cho đủ số) — đúng bệnh "rải `props` trang trí" mà gate ① của `stage-zu-layout` đã kết án.
Chống bằng cách **chỉ đếm sự kiện NEO VÀO LỜI**: props không có `t0`/`ph` thì `check_stage_card`
T9 đã chặn từ trước, và ở đây phụ đề được đếm vì nó *là* lời.

Exit 0 = sạch · 1 = có gate đỏ.
"""
from __future__ import annotations

import argparse
import io
import json
import statistics as st
import sys
from pathlib import Path

# 🔴 audience-45plus §2.0h — gate CRASH thì builder báo đỏ GIẢ trên project sạch.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_stage as M                                          # noqa: E402

CARD_SEC_MAX = 30.0     # trần clip make_stage (render_clip sec)


def card_events(st_, t0, t1):
    """Mốc GIÂY TUYỆT ĐỐI của mọi sự kiện hình trong MỘT thẻ [t0,t1).

    `beat`/`t0` trong spec là GIÂY THẬT tính từ ĐẦU THẺ (cùng đơn vị `beat` của pins) —
    không phải giây của cả video. Quên cộng t0 là đo ra một bài "sạch" hoàn toàn giả.
    """
    ev = [t0]                                        # thẻ vào = một sự kiện
    for b in (st_.get("beats") or []):
        try:
            ev.append(t0 + float(b))
        except (TypeError, ValueError):
            pass
    for p in (list(st_.get("pins") or []) + list(st_.get("pins_card") or [])):
        if isinstance(p, dict) and p.get("beat") is not None:
            ev.append(t0 + float(p["beat"]))
    for pr in (list(st_.get("props") or []) + list(st_.get("props_top") or [])):
        if isinstance(pr, dict) and pr.get("t0") is not None:
            ev.append(t0 + float(pr["t0"]))
    # ⭐ cast đổi tư thế — thứ nuôi sàn ở 2 kênh thắng
    for side_beats in (st_.get("cast_beats") or {}).values():
        for b in (side_beats or []):
            at = b[0] if isinstance(b, (list, tuple)) else b.get("at")
            if at is not None:
                ev.append(t0 + float(at))
    return [e for e in ev if t0 <= e < t1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides")
    ap.add_argument("timeline", nargs="?", help="timeline.json (để đếm dòng phụ đề)")
    ap.add_argument("--max-gap", type=float, default=9.0)
    ap.add_argument("--max-card-per-min", type=float, default=6.0)
    ap.add_argument("--no-sub", action="store_true",
                    help="KHÔNG đếm dòng phụ đề là sự kiện (đo khắt khe hơn)")
    a = ap.parse_args()

    d = json.load(io.open(a.slides, encoding="utf-8"))
    ss = d["slides"] if isinstance(d, dict) else d
    cards = [(i, c["stage"], c) for i, c in enumerate(ss) if c.get("stage")]
    if not cards:
        print("🔴 SLIDES không có thẻ `stage` nào"); sys.exit(1)

    # ── mốc thời gian từng thẻ: ưu tiên timeline.json, không có thì dùng `sec`/`match` ──
    subs = []
    tl = None
    if a.timeline and Path(a.timeline).exists():
        tl = json.load(io.open(a.timeline, encoding="utf-8"))
        subs = [(float(l["start"]), float(l["end"])) for l in tl["lines"]]
    if not subs:
        print("⚠️  không có timeline.json → suy mốc thẻ từ khoá `sec`, "
              "phụ đề KHÔNG được đếm là sự kiện (đo khắt khe hơn thực tế)")

    bounds, t = [], 0.0
    for i, stg, c in cards:
        sec = float(c.get("sec") or stg.get("sec") or 0)
        if not sec and subs:
            # chia đều theo số thẻ nếu builder chưa ghi `sec` — chỉ để gate chạy được
            sec = subs[-1][1] / len(cards)
        bounds.append((i, stg, t, t + (sec or 12.0)))
        t += (sec or 12.0)
    total = t

    ev = []
    over_card = []
    for i, stg, t0, t1 in bounds:
        if t1 - t0 > CARD_SEC_MAX:
            over_card.append((i, t1 - t0))
        ev += card_events(stg, t0, t1)
    if subs and not a.no_sub:
        ev += [s for s, _ in subs]
    ev = sorted(set(round(x, 2) for x in ev))

    gaps = [b - aa for aa, b in zip([0.0] + ev, ev + [total])]
    bad_gaps = [(round(x, 1), round(g, 1))
                for x, g in zip([0.0] + ev, gaps) if g > a.max_gap]
    cpm = len(cards) / (total / 60.0) if total else 0

    print(f"── GATE NHỊP SÂN KHẤU — {len(cards)} thẻ / {total/60:.1f} phút ──")
    print(f"   ① đổi THẺ      {cpm:.2f}/phút   (trần {a.max_card_per_min})")
    print(f"   ② SỰ KIỆN      {len(ev)/(total/60):.1f}/phút · khe median "
          f"{st.median(gaps):.1f}s · max {max(gaps):.1f}s   (sàn {a.max_gap}s)")
    print(f"      so đối thủ: カメ 19,4/phút median 3,0s · 保健室 20,2/phút median 2,8s")
    print(f"   ③ thẻ >{CARD_SEC_MAX:.0f}s   {len(over_card)}")

    red = 0
    if cpm > a.max_card_per_min:
        print(f"  🔴 ① {cpm:.2f} thẻ/phút > {a.max_card_per_min} — cắt dồn, tệp 45+ mệt")
        red += 1
    if bad_gaps:
        pct = sum(g for _, g in bad_gaps) / total * 100
        print(f"  🔴 ② {len(bad_gaps)} khe > {a.max_gap}s ({pct:.0f}% thời lượng đứng yên). "
              f"Tệ nhất: " + " · ".join(f"@{x/60:.1f}′={g}s" for x, g in
                                        sorted(bad_gaps, key=lambda z: -z[1])[:6]))
        print(f"      chữa: thêm `cast_beats` (rẻ nhất, không cần asset) → thêm beat cho "
              f"phần tử sơ đồ mọc dần → chẻ thẻ. ⛔ ĐỪNG chữa bằng cách tăng đổi THẺ (đâm vào ①)")
        red += 1
    if over_card:
        print(f"  🔴 ③ {len(over_card)} thẻ giữ > {CARD_SEC_MAX:.0f}s (trần clip make_stage): "
              + " · ".join(f"[{i:02d}]={s:.0f}s" for i, s in over_card[:8]))
        print(f"      phần tử cuối KHÔNG kịp hiện. Chẻ thẻ, hoặc --clip-sec lớn hơn.")
        red += 1
    if red:
        print(f"\n🔴 {red}/3 gate ĐỎ — SỬA XONG MỚI RENDER")
        sys.exit(1)
    print("✅ SẠCH 3/3 — được render")


if __name__ == "__main__":
    main()
