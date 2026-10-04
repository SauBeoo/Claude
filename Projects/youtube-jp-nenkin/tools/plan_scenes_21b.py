# -*- coding: utf-8 -*-
r"""plan_scenes_21b.py — sinh SCENE PLAN cho v21 theo luật "footage không được đứng ở dòng có SỐ".

🔴 VÌ SAO PHẢI SINH BẰNG MÁY, KHÔNG XẾP TAY. `_scenes21.py` neo scene bằng **chỉ số dòng
`L`** của `_TTS.md`. Lời v21 vừa viết lại (114 → 111 dòng, đảo thứ tự, cắt 復興税, thêm case
山田) ⇒ **mọi neo L đã vỡ**, và vỡ IM LẶNG: builder vẫn chạy, clip vẫn đủ giây, chỉ có hình
rơi vào sai câu. Đúng bẫy `feedback_builder_neo_dong_kiem_timeline_truoc`.

LUẬT THI HÀNH (đo trên chính script, xem `check_footage_ratio.py`):
    Dòng CÓ số  → thẻ (stat / formula / genten)
    Dòng KHÔNG số → footage được phép
v21 cũ: footage 74,0% trong khi lời không-số chỉ 52,2% ⇒ tràn 21 điểm, và **35 dòng có số
bị đặt lên footage** — trong đó 18 dòng so sánh ≥2 số. Dòng tệ nhất: 「百十万円と、九十五万円。
足すと、二百五万円。」 — phương trình trung tâm của cả video, đọc trên khung không một chữ số.

CHẠY:  python tools/plan_scenes_21b.py [--max-scene 30]
       → in bảng scene + ghi `06_VIDEO/<stem>/scenes_plan.json`
"""
import argparse
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)

RE_NUM = re.compile(r"(?:[0-9０-９]+(?:[,，][0-9０-９]+)*|[一二三四五六七八九十百千万億〇]{1,})"
                    r"\s*(?:円|万|パーセント|％|割|年|歳|日|月|人|件|回|倍|分)")
# Câu trích NGUYÊN VĂN từ 原典 → thẻ 原典 (ảnh chụp), không phải thẻ số
GENTEN_CUE = ("赤で囲んだ", "パンフレットです", "要点はこうです", "要点だけまとめます",
              "その続きが書いてあります")
GENTEN_QUOTE = ("源泉徴収されます", "差はありません", "計算しなおしてもらえます",
                "提出する必要があります")
# Dòng có ≥2 cụm số → BẮT BUỘC thẻ, footage ở đây là khung trống
CMP_MIN = 2


# 🔴 MỐC LỊCH ≠ SỐ TIỀN. 「令和八年八月時点」 khớp RE_NUM ba lần (八年・八月・…) nên dòng
# disclaimer bị chấm là "công thức" và đòi một thẻ số cho một câu miễn trừ trách nhiệm.
# Cùng lỗi mà `check_pace.RE_STAKE` đã phải chặn từ trước bằng lookbehind 月/\d.
RE_DATE = re.compile(r"(?:令和|平成|昭和)?[0-9０-９一二三四五六七八九十]+年"
                     r"(?:[0-9０-９一二三四五六七八九十]+月)?(?:[0-9０-９一二三四五六七八九十]+日)?時点")
TAIL_CUE = "時点の情報です"          # từ đây trở đi là ĐOẠN KẾT: disclaimer + CTA + 次回


def kind_of(text):
    n = len(RE_NUM.findall(RE_DATE.sub("", text)))
    if any(c in text for c in GENTEN_QUOTE):
        return "genten", n
    if any(c in text for c in GENTEN_CUE):
        return "genten", n
    if n >= CMP_MIN:
        return "formula", n
    if n >= 1:
        return "stat", n
    return "art", n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-scene", type=float, default=30.0)
    a = ap.parse_args()
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))
    lines, total = tl["lines"], tl["total"]

    # ĐOẠN KẾT không phải chỗ của thẻ số: disclaimer + CTA đăng ký + 次回予告 + chữ ký
    # là lời nói với người xem, không phải dữ kiện. Ép thẻ vào đó là lặp lại đúng bệnh
    # "thẻ để lấp chỗ" mà cả bài này đang chữa.
    i_tail = next((i for i, l in enumerate(lines) if TAIL_CUE in l["text"]), len(lines))
    marked = []
    for i, l in enumerate(lines):
        k, n = kind_of(l["text"])
        if i >= i_tail:
            k, n = "art", 0
        marked.append((i, l["start"], l["end"], k, n, l["text"], l.get("spk", "s1")))

    # gộp dòng liền nhau CÙNG loại thành scene; chẻ khi vượt trần
    scenes = []
    for i, st, en, k, n, txt, spk in marked:
        if scenes and scenes[-1]["kind"] == k and (en - scenes[-1]["start"]) <= a.max_scene:
            s = scenes[-1]
            s["to"] = i
            s["end"] = en
            s["n"] = s["n"] + n
            s["lines"].append(txt)
        else:
            scenes.append({"from": i, "to": i, "start": st, "end": en, "kind": k,
                           "n": n, "lines": [txt]})

    # gộp scene <6s vào hàng xóm — `audience-45plus.md` §2 mục 2 cấm entry <6 giây.
    # Gộp về phía có CÙNG loại nếu được, không thì về scene TRƯỚC (giữ mốc mở scene).
    MIN = 6.0
    merged = []
    for sc in scenes:
        if merged and (sc["end"] - sc["start"]) < MIN:
            m = merged[-1]
            m["to"], m["end"] = sc["to"], sc["end"]
            m["n"] += sc["n"]
            m["lines"] += sc["lines"]
            if sc["n"] and m["kind"] == "art":
                m["kind"] = "formula" if sc["n"] >= CMP_MIN else "stat"
        else:
            merged.append(sc)
    scenes = merged

    foot = sum(s["end"] - s["start"] for s in scenes if s["kind"] == "art")
    card = sum(s["end"] - s["start"] for s in scenes if s["kind"] != "art")
    span = foot + card
    n_shot = sum(max(1, int((s["end"] - s["start"]) // 9) + 1)
                 for s in scenes if s["kind"] == "art")

    print(f"── SCENE PLAN v21b — {len(scenes)} scene / {total/60:.1f}′ ──")
    for s in scenes:
        d = s["end"] - s["start"]
        tag = {"art": "footage", "stat": "THẺ SỐ", "formula": "CÔNG THỨC", "genten": "原典"}[s["kind"]]
        print(f"  [{s['from']:03d}-{s['to']:03d}] {int(s['start'])//60}:{int(s['start'])%60:02d} "
              f"+{d:5.1f}s  {tag:9s} {s['n']:2d} số  {s['lines'][0][:34]}")
    print()
    print(f"  footage {foot/span*100:5.1f}%  ({foot:.0f}s → ~{n_shot} shot 8s)")
    print(f"  thẻ     {card/span*100:5.1f}%  ({card:.0f}s)")
    print(f"  (v21 CŨ: footage 74,0% / thẻ 26,0% — bản user chê 'ảnh vô nghĩa')")

    io.open(os.path.join(VD, "scenes_plan.json"), "w", encoding="utf-8").write(
        json.dumps(scenes, ensure_ascii=False, indent=1))
    print(f"→ {os.path.join(VD, 'scenes_plan.json')}")


if __name__ == "__main__":
    main()
