#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""check_footage_ratio.py — GATE CHỐNG "ẢNH VÔ NGHĨA" cho đường FOOTAGE AI.

    python check_footage_ratio.py <_TTS.md> <project.json|SCENES.json> [--max-footage 52]

🔴 VÌ SAO CÓ FILE NÀY. User xem video 21 (footage AI người thật toàn khung) và nói:
*"Các ảnh được thêm vào tôi thấy hơi vô nghĩa"*. Chẩn đoán bằng máy trên chính script đó:

  · dòng lời **CÓ số** (≥1 cụm số + đơn vị)      **35,2%** (317s/901s)
  · trong đó **so sánh ≥2 số** trong một dòng     **18,4%** (166s)
  · dòng **KHÔNG số**                             **52,2%** (470s)
  · nhưng footage thực dùng                       **73,1%**  ← tràn 21 điểm

⇒ **Bệnh không phải "footage". Bệnh là footage TRÀN sang những câu đang nói về TIỀN.**
Veo không viết được chữ (CLAUDE.md §②), nên đặt footage lên một câu so sánh 158万↔205万
là để **khung trống** đúng lúc người xem cần thấy con số. Đo được ở v21: mọi chỗ lời so
sánh hai số (158↔205 · 240↔205 · 205↔148) hình đều bỏ trống, và con số trung tâm 205万円
chỉ đọc được ở **5/29 frame**.

Luật, một câu:
    **Footage chỉ được đứng ở dòng KHÔNG có số. Mọi dòng có số → thẻ.**

Gate đo hai thứ:
  ① dòng CÓ SỐ mà rơi vào scene footage  → 🔴 liệt kê từng dòng
  ② tổng thời lượng footage > trần        → 🔴

⚖️ Trần 52% KHÔNG phải con số thẩm mỹ: nó là **tỉ lệ dòng không-số của chính bài đó**.
Bài nào ít số hơn thì trần tự nới, bài nào dày số thì tự siết — tool tính lại mỗi lần chạy,
`--max-footage` chỉ là chặn trên tuyệt đối.

Exit 0 = sạch · 1 = có lỗi.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Cùng một regex với `youtube-jp-nenkin/tools/check_pace.py::RE_NUM` — CỐ Ý trùng:
# hai gate phải đồng ý với nhau về "thế nào là một con số", nếu không sẽ có bài
# qua gate này mà rớt gate kia vì hai định nghĩa khác nhau.
RE_NUM = re.compile(r"(?:[0-9０-９]+(?:[,，][0-9０-９]+)*|[一二三四五六七八九十百千万億〇]{1,})"
                    r"\s*(?:円|万|パーセント|％|割|年|歳|日|月|人|件|回|倍|分)")
CPS = 5.72          # ký/giây của giọng kênh (雀松朱司 speed 0.9)
GAP = 0.45


def read_timeline(tlp):
    """→ [(t0, giây, chữ, số_cụm_số)] lấy từ `timeline.json` — ĐO TỪ WAV THẬT.

    🔴 VÌ SAO PHẢI ƯU TIÊN CÁI NÀY (vá 2026-09-07). `read_lines()` dưới đây ƯỚC thời
    điểm mỗi dòng bằng `len/5,72 + 0,45`. Ước thì lệch DỒN: đo trên v21 bản mới, ước
    ra 14:22 còn wav thật 13:29 — **lệch ~50 giây ở đuôi**. Gate đem mốc ƯỚC so với
    mốc THẬT của clip ⇒ càng về cuối càng chấm sai, và nó báo oan đúng những dòng
    ĐANG có thẻ hiện trên màn (3:25 令和九年分・214万 · 12:21 研究ノート①…).
    Cùng bài học `feedback_timeline_phai_do_tu_wav_that`: có số đo thật thì đừng ước.
    """
    d = json.load(io.open(tlp, encoding="utf-8"))
    out = []
    for l in d["lines"]:
        txt = l["text"]
        out.append((float(l["start"]), float(l["end"]) - float(l["start"]),
                    txt, len(RE_NUM.findall(txt))))
    return out, float(d.get("total") or (out[-1][0] + out[-1][1]))


def read_lines(tts):
    """→ [(t_bắt_đầu, giây, chữ, số_cụm_số)] — ƯỚC, chỉ dùng khi KHÔNG có timeline.json."""
    t, out = 0.0, []
    for raw in Path(tts).read_text(encoding="utf-8").splitlines():
        if raw.lstrip().startswith(("<!--", "#", ">")):
            continue
        line = re.sub(r"^(\[[^\]]*\])+", "", raw).strip()
        if not line:
            t += 1.0
            continue
        d = len(line) / CPS + GAP
        out.append((t, d, line, len(RE_NUM.findall(line))))
        t += d
    return out, t


def scene_kind_at(scenes, t):
    """Loại hình người xem THẤY ở giây t. `scenes` = [(t0, t1, kind)].

    🔴 THẺ THẮNG KHI CHỒNG LẤN (vá 2026-09-07). Builder kéo clip footage dài thêm
    ~0,6s để cross-dissolve, nên footage **chồng lấn đầu thẻ**. Bản đầu trả về range
    bắt đầu SỚM hơn ⇒ chấm là footage, và báo oan 19 dòng — trong đó có dòng
    「令和九年分は…二百十四万円」 mà thực tế ĐANG có thẻ số hiện trên màn.
    Remotion vẽ `trk-stat`/`trk-formula`/`trk-genten` **SAU** `trk-video` trong mảng
    tracks ⇒ thẻ nằm TRÊN. Gate phải đo cái người xem thấy, không đo cái bắt đầu trước.
    """
    hit = [k for a, b, k in scenes if a <= t < b]
    if not hit:
        return None
    return "card" if "card" in hit else "footage"


def load_scenes(path):
    """Đọc project.json (Remotion) HOẶC SLIDES/SCENES json → [(t0,t1,kind)].

    Remotion: suy từ TRACK — `trk-video` = footage · `trk-genten`/`trk-stat`/`trk-formula`
    = thẻ. 🔴 Tên track phải đúng (`feedback_gate_va_builder_phai_cung_ten`): builder gộp
    hết thẻ chữ vào một `trk-text` là gate này mù y như `check_frame_pace` đã từng mù.
    """
    d = json.load(io.open(path, encoding="utf-8"))
    fps = d.get("fps", 30)
    out = []
    if "tracks" in d:
        for tr in d["tracks"]:
            tid = tr.get("id", "")
            if tid.startswith("trk-video"):
                kind = "footage"
            elif tid.startswith(("trk-genten", "trk-stat", "trk-formula")):
                kind = "card"
            else:
                continue
            for c in tr.get("clips", []):
                f = c.get("from", 0)
                n = c.get("durationInFrames", 0)
                out.append((f / fps, (f + n) / fps, kind))
    else:
        ss = d["slides"] if isinstance(d, dict) else d
        t = 0.0
        for e in ss:
            sec = float(e.get("sec") or 0) or 12.0
            st = e.get("stage") or {}
            kind = "footage" if (e.get("art") or st.get("layout") == "art") else "card"
            out.append((t, t + sec, kind))
            t += sec
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tts")
    ap.add_argument("scenes")
    ap.add_argument("--max-footage", type=float, default=52.0)
    ap.add_argument("--timeline", help="timeline.json (mốc ĐO TỪ WAV — luôn ưu tiên)")
    a = ap.parse_args()

    # tự tìm timeline.json cạnh _TTS.md → 06_VIDEO/<stem>/timeline.json
    tlp = a.timeline
    if not tlp:
        stem = Path(a.tts).name.replace("_TTS.md", "")
        cand = Path(a.tts).parent.parent / "06_VIDEO" / stem / "timeline.json"
        if cand.exists():
            tlp = str(cand)
    if tlp:
        lines, total = read_timeline(tlp)
        print(f"   (mốc dòng: timeline.json — ĐO TỪ WAV)")
    else:
        lines, total = read_lines(a.tts)
        print(f"   ⚠️  không thấy timeline.json → mốc dòng là ƯỚC, lệch dồn tới ~50s ở đuôi")
    # ⛔ MIỄN ĐOẠN KẾT, giống `check_pace` G13 và `plan_scenes_21b`: từ dòng disclaimer
    #    「…時点の情報です」 trở đi là disclaimer + CTA + 次回予告 + chữ ký. Đó là lời nói
    #    với người xem, không phải dữ kiện — ép thẻ số vào đó là lặp lại đúng bệnh
    #    "thẻ để lấp chỗ" mà cả lượt này đang chữa. Ba chỗ phải MIỄN CÙNG MỘT MỐC,
    #    nếu không planner và gate sẽ đánh nhau vĩnh viễn.
    t_tail = next((t for t, d, l, k in lines if "時点の情報です" in l), None)
    scenes = load_scenes(a.scenes)
    if not scenes:
        print("🔴 không đọc được scene nào — sai file hoặc track sai tên "
              "(cần trk-video / trk-genten / trk-stat / trk-formula)")
        sys.exit(1)

    body = [r for r in lines if t_tail is None or r[0] < t_tail]
    s_num = sum(d for _, d, _, k in body if k >= 1)
    s_cmp = sum(d for _, d, _, k in body if k >= 2)
    s_non = sum(d for _, d, _, k in body if k == 0)
    foot = sum(b - x for x, b, k in scenes if k == "footage")
    card = sum(b - x for x, b, k in scenes if k == "card")
    span = foot + card or 1

    # ① dòng CÓ SỐ nằm trên footage
    bad = []
    for t, d, line, nk in lines:
        if nk < 1:
            continue
        if t_tail is not None and t >= t_tail:
            continue
        if scene_kind_at(scenes, t + d / 2) == "footage":
            bad.append((t, nk, line))

    t_body = sum(d for _, d, _, _ in body) or total
    trần = min(a.max_footage, s_non / t_body * 100)
    print(f"── GATE FOOTAGE vs SỐ — lời {total/60:.1f}′ · hình {span/60:.1f}′ ──")
    print(f"   lời CÓ số        {s_num/t_body*100:5.1f}%   (so sánh ≥2 số: {s_cmp/t_body*100:.1f}%)")
    print(f"   lời KHÔNG số     {s_non/t_body*100:5.1f}%   ← trần tự nhiên của footage"
          + (f"  [bỏ đoạn kết từ {int(t_tail//60)}:{int(t_tail%60):02d}]" if t_tail else ""))
    print(f"   footage thực     {foot/span*100:5.1f}%   · thẻ {card/span*100:.1f}%")
    print(f"   (v21 gốc: footage 73,1% / thẻ 26,9% — bản bị user chê)")

    red = 0
    if foot / span * 100 > trần:
        print(f"  🔴 ② footage {foot/span*100:.1f}% > trần {trần:.1f}% — nó đang tràn sang "
              f"những câu nói về TIỀN, đúng chỗ Veo không viết được chữ")
        red += 1
    if bad:
        cmp_bad = [b for b in bad if b[1] >= 2]
        print(f"  🔴 ① {len(bad)} dòng CÓ SỐ đang nằm trên footage "
              f"({len(cmp_bad)} dòng so sánh ≥2 số — nặng nhất):")
        for t, nk, line in sorted(bad, key=lambda z: -z[1])[:8]:
            print(f"       {int(t//60)}:{int(t%60):02d}  [{nk} số] {line[:46]}")
        red += 1
    if red:
        print(f"\n🔴 {red}/2 gate ĐỎ — đổi những dòng đó sang thẻ số/công thức rồi chạy lại")
        sys.exit(1)
    print("✅ SẠCH 2/2 — mọi con số đều có khung chở")


if __name__ == "__main__":
    main()
