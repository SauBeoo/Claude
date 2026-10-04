# -*- coding: utf-8 -*-
r"""plan27.py — SCENE PLAN cho video 27 (khuôn mới sau mổ 3 kênh 2026-09-17).

KHÁC BUILDER CŨ Ở ĐÂU (đọc trước khi sửa):
  · **0 clip AI** — v26 có 61 clip × 8,000s = 62% thời lượng, MAD từng clip 3,83–8,35.
    Từ v27 lớp hình là ẢNH TĨNH, style phẳng いらすとや (user chốt 2026-09-17).
  · Mỗi ô hình giữ ~10s ⇒ nhịp ≈ 5,8 đổi/phút, đúng mốc 完全攻略 (445K view/video) và
    dưới trần 6/phút của `audience-45plus.md` §2 mục 1.
  · 5 CHƯƠNG có chip đánh số + 3 màn 「本日の流れ」 (thanh tiến độ ✅).

CHẠY:  python tools/plan27.py            → in bảng plan + ghi 06_VIDEO/<stem>/plan27.json
       python tools/plan27.py --prompts  → thêm bảng gợi ý nội dung ảnh từng ô
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "27_nenkin-tsuchisho-nai-okane-5tsu"
VD = PROJ / "06_VIDEO" / STEM

HOLD_TARGET = 10.0     # giây/ô hình. 16,35′ ÷ 10s ≈ 98 ô ≈ 5,8 đổi/phút (mốc 完全攻略)

# ── 5 CHƯƠNG — mốc nhận bằng câu MỞ CHƯƠNG trong lời đọc ─────────────────────
# chip ≤12 ký full-width để lọt góc trên-trái mà không đè nội dung
CHAPTERS = [
    ("0", "",                   "はじめに",           None),
    ("1", "60代前半",            "特別支給",           "一つ目。六十代の前半に来るお金"),
    ("2", "65歳",               "加給年金",           "二つ目。六十五歳になったときのお金"),
    ("3", "配偶者65歳",          "振替加算",           "三つ目。配偶者が六十五歳になった月"),
    ("4", "毎年",               "支援給付金",         "四つ目。毎年くり返し来るお金"),
    ("5", "そのあと",            "未支給年金",         "そして五つ目。これだけは、ご自身では"),
    ("6", "",                   "研究ノート",         "それでは、今日の研究ノートです"),
]

# 3 màn 「本日の流れ」: sau cold open · giữa bài · trước kết
FLOW_AFTER = ["まず、事実から", "ここまでの二つが、今日いちばん大きい金額", "四つ目。毎年くり返し"]


def load_lines():
    d = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
    return d["lines"], float(d["total"])


def chapter_of(lines):
    """Gán số chương cho từng dòng bằng câu mở chương (khớp tiền tố, bỏ dấu câu)."""
    marks = {}
    for num, chip_l, chip_r, cue in CHAPTERS:
        if not cue:
            continue
        for i, ln in enumerate(lines):
            if ln["text"].startswith(cue[:14]):
                marks[i] = num
                break
        else:
            print(f"  ⚠️ KHÔNG tìm thấy câu mở chương {num}: 「{cue[:18]}」")
    out, cur = [], "0"
    for i, _ in enumerate(lines):
        cur = marks.get(i, cur)
        out.append(cur)
    return out, marks


def main() -> int:
    lines, total = load_lines()
    chaps, marks = chapter_of(lines)

    # ── gom dòng thành Ô HÌNH ~HOLD_TARGET giây, KHÔNG cho ô vắt qua ranh giới chương
    shots, cur = [], None
    for i, ln in enumerate(lines):
        new_chap = i in marks
        if cur is None or new_chap or (ln["end"] - cur["t0"]) >= HOLD_TARGET:
            if cur:
                shots.append(cur)
            cur = dict(t0=ln["start"], t1=ln["end"], chap=chaps[i], lines=[i], text=ln["text"])
        else:
            cur["t1"] = ln["end"]
            cur["lines"].append(i)
            cur["text"] += ln["text"]
    if cur:
        shots.append(cur)

    # ── VÁ 1: ô <6s (sinh ở ranh giới chương, khi câu mở chương ngắn) → gộp với ô SAU
    #    cùng chương. `audience-45plus.md` §2 mục 2: không entry nào <6 giây.
    merged, i = [], 0
    while i < len(shots):
        s = shots[i]
        if (s["t1"] - s["t0"]) < 6.0 and i + 1 < len(shots) and shots[i + 1]["chap"] == s["chap"]:
            n = shots[i + 1]
            s = dict(t0=s["t0"], t1=n["t1"], chap=s["chap"],
                     lines=s["lines"] + n["lines"], text=s["text"] + n["text"])
            i += 2
        else:
            i += 1
        merged.append(s)
    shots = merged

    # ── VÁ 1b: ô <6s còn sót ở CUỐI chương (không có ô sau cùng chương để gộp)
    #    → gộp ngược vào ô TRƯỚC cùng chương. Nếu cả trước lẫn sau đều khác chương thì để yên:
    #    ô đó là cả một chương ngắn, gộp sẽ làm ô vắt qua hai chương ⇒ chip chương sai.
    back, k = [], 0
    for s in shots:
        if (s["t1"] - s["t0"]) < 6.0 and back and back[-1]["chap"] == s["chap"]:
            back[-1]["t1"] = s["t1"]
            back[-1]["lines"] += s["lines"]
            back[-1]["text"] += s["text"]
        else:
            back.append(dict(s))
    shots = back

    # ── VÁ 2: ô >18s (một DÒNG dài, ví dụ khối CTA 27s) → chẻ đều để hình không đứng quá lâu.
    #    ⚠️ Chẻ theo THỜI GIAN, không theo dòng — ô này vốn chỉ có 1 dòng nên không cắt lời được.
    split = []
    for s in shots:
        d = s["t1"] - s["t0"]
        if d > 18.0:
            n = int(d // 10.0) + (1 if d % 10.0 > 4 else 0)
            n = max(2, n)
            step = d / n
            for j in range(n):
                split.append(dict(t0=s["t0"] + j * step, t1=s["t0"] + (j + 1) * step,
                                  chap=s["chap"], lines=s["lines"] if j == 0 else [],
                                  text=s["text"] if j == 0 else ""))
        else:
            split.append(s)
    shots = split

    # ── PAN CHẬM (user chốt 2026-09-17 "tĩnh + pan chậm") ───────────────────────
    # Đo thật trên ảnh 1920x1080, ô 10s (scratchpad/pan*.mp4):
    #   pan 0% -> MAD 0,00 / 100% frame đứng yên     pan 3% -> MAD 0,71 / 59%
    #   pan 2% -> MAD 0,46 /  74%                     pan 6% -> MAD 1,29 / 15%
    # => Pan MỘT MÌNH rất rẻ về MAD (trần 5,0), NHƯNG ăn mạnh vào "% frame đứng yên" —
    #   chỉ số mà 3 kênh thắng đều giữ 89-92%. Nên CHỈ pan ~33% số ô:
    #   0,67x100% + 0,33x59% ~ 86% đứng yên (sát ngách), MAD ~ cắt-cảnh 1,6 + 0,24 ~ 1,9.
    # 🔴 KHÔNG pan ô có SƠ ĐỒ/BẢNG/CHỮ LỚN — chữ trôi thì tệp 65+ đọc không kịp; và
    #   `feedback_video_no_motion_mot_giong` đã kết án Ken Burns. Pan ở đây là DỊCH KHUNG
    #   biên độ 3%, zoom CỐ ĐỊNH (Ken Burns = zoom đổi liên tục, khác hẳn).
    PAN_PCT, PAN_EVERY = 3, 3
    PAN_DIRS = ["lr", "tb", "rl", "bt"]
    for k, s in enumerate(shots):
        s["pan"] = (dict(pct=PAN_PCT, dir=PAN_DIRS[(k // PAN_EVERY) % 4])
                    if k % PAN_EVERY == 1 else None)

    # ── màn 「本日の流れ」
    flow_at = []
    for cue in FLOW_AFTER:
        for k, s in enumerate(shots):
            if cue[:12] in s["text"]:
                flow_at.append(k)
                break

    per_min = len(shots) / (total / 60.0)
    holds = [s["t1"] - s["t0"] for s in shots]
    holds_sorted = sorted(holds)
    med = holds_sorted[len(holds_sorted) // 2]

    print(f"\n=== PLAN 27 — {total/60:.2f} phút · {len(lines)} dòng ===")
    print(f"  ô hình      : {len(shots)}   (đổi {per_min:.1f}/phút — trần ≤6 · mốc 完全攻略 5,8)")
    print(f"  giữ mỗi ô   : trung vị {med:.1f}s · min {min(holds):.1f}s · max {max(holds):.1f}s")
    print(f"  màn 本日の流れ: {len(flow_at)} màn tại ô {flow_at}")
    npan = sum(1 for s in shots if s.get("pan"))
    print(f"  pan chậm    : {npan}/{len(shots)} ô ({npan/len(shots)*100:.0f}%) · biên độ 3% · "
          f"ước MAD ~1,9 · ước dứng yên ~{100 - npan/len(shots)*41:.0f}%")
    print(f"  clip AI     : 0   ⭐ (v26 có 61 clip = 62% thời lượng)\n")

    print(f"  {'chương':<22} {'ô':>4} {'giây':>8}  chip")
    for num, cl, cr, _ in CHAPTERS:
        sel = [s for s in shots if s["chap"] == num]
        if not sel:
            continue
        secs = sum(s["t1"] - s["t0"] for s in sel)
        chip = f"{num}. {cl} {cr}".strip() if cl else cr
        print(f"  {cr:<22} {len(sel):>4} {secs:>7.0f}s  {chip}")

    warn = []
    if per_min > 6.0:
        warn.append(f"nhịp {per_min:.1f}/phút VƯỢT trần 6,0 — tăng HOLD_TARGET")
    if med < 3.0:
        warn.append(f"trung vị giữ ô {med:.1f}s < 3,0s (gate check_motion ②)")
    if len(flow_at) < 2:
        warn.append(f"chỉ {len(flow_at)} màn 本日の流れ — cần ≥2")
    for w in warn:
        print(f"  🔴 {w}")

    out = dict(stem=STEM, total=total, hold_target=HOLD_TARGET, per_min=round(per_min, 2),
               hold_median=round(med, 2), flow_at=flow_at,
               chapters=[dict(num=n, chip_l=cl, chip_r=cr) for n, cl, cr, _ in CHAPTERS],
               shots=[dict(k=k, t0=round(s["t0"], 3), t1=round(s["t1"], 3),
                           chap=s["chap"], lines=s["lines"], text=s["text"],
                           pan=s.get("pan"))
                      for k, s in enumerate(shots)],
               pan=dict(pct=PAN_PCT, every=PAN_EVERY,
                        n=sum(1 for s in shots if s.get("pan"))))
    (VD / "plan27.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {VD / 'plan27.json'}")

    if "--prompts" in sys.argv:
        print(f"\n=== NỘI DUNG ẢNH TỪNG Ô (rút từ lời đọc) ===")
        for k, s in enumerate(shots):
            t = re.sub(r"\s+", "", s["text"])[:46]
            print(f"  {k:>3} ch{s['chap']} {s['t0']:>7.1f}–{s['t1']:>7.1f}s  {t}")
    return 0 if not warn else 1


if __name__ == "__main__":
    sys.exit(main())
