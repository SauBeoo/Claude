#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""GATE BỐ CỤC lớp `zu` — chạy TRƯỚC mọi lượt render video.

    python check_zu_layout.py <SLIDES.json> [--probe <thư mục PNG đã dựng>]

Kiểm 13 lớp lỗi của `.claude/rules/stage-zu-layout.md`:
  · 10 lớp HÌNH HỌC + VỊ TRÍ → gọi thẳng `make_stage.zu_check()` (builder cũng gọi hàm này,
    nên không có hai bản số lệch nhau — bài học `_sig`).
  · 3 lớp CÂN ĐỐI mà `zu_check` không đo: khoảng trống dọc · phủ ngang · mực sát mép ảnh thật.

🔴 VÌ SAO PHẢI LÀ FILE CHỨ KHÔNG PHẢI THÓI QUEN: cả 13 lớp lỗi này đều được phát hiện bởi
**user soi ảnh full-size**, sau khi tao đã duyệt contact sheet và cho qua. Trong một buổi user
phải chỉ **6 lượt** mới hết. Lần sau không được lặp lại — chạy lệnh này, đọc số.

Exit 0 = sạch · 1 = có lỗi.
"""
import io
import sys
import json
import glob
import argparse
from pathlib import Path

# 🔴 audience-45plus §2.0h — thiếu dòng này thì console cp1252 KHÔNG in nổi 🔴/✅ ⇒ gate
# CRASH giữa chừng ⇒ exit ≠ 0 ⇒ builder báo "GATE ĐỎ" trên một project SẠCH. Báo đỏ giả
# nguy hiểm hơn gate im lặng: nó dụ người ta đi sửa NỘI DUNG cho lỗi nằm ở CÔNG CỤ.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_stage as M                                          # noqa: E402

VOID_MAX = 150      # khoảng trống dọc ĐƠN tối đa (px) — §2 luật BA KHỐI
COVER_MIN = 0.85    # tỉ lệ phủ ngang tối thiểu của khối nội dung
EDGE_INK = 40       # ngưỡng pixel mực trong dải sát mép card


def check_spec(ss):
    """→ (dict lỗi theo số thẻ, số thẻ `zu` đã kiểm)."""
    bad, n = {}, 0
    Y0 = M.CARD_Y0 + 74 + 62 + 34
    Y1 = M.CARD_Y1 - 44
    BX0, BX1 = M.ZU_CAST_L + 12, M.ZU_CAST_R - 20
    for k, c in enumerate(ss):
        st = c.get("stage") or {}
        if st.get("layout") != "zu":
            continue
        n += 1
        out = list(M.zu_check(st))                # ⬅ 10 lớp: một phép đo, dùng chung với builder
        pos = M._zu_place(st)
        # ── ② khoảng trống dọc. Khe có EDGE chạy qua thì là NỘI DUNG, không phải trống.
        cross = [tuple(sorted((pos[e["from"]][1], pos[e["to"]][1])))
                 for e in st.get("edges", []) if e["from"] in pos and e["to"] in pos]
        segs = sorted((sum(pos[m["id"]][1] for m in r) / len(r) - M._zu_rowh(r)[0],
                       sum(pos[m["id"]][1] for m in r) / len(r) + M._zu_rowh(r)[1])
                      for r in M._zu_rows(st))
        gaps = ([("ĐỈNH", Y0, segs[0][0])]
                + [("giữa", segs[i][1], segs[i + 1][0]) for i in range(len(segs) - 1)]
                + [("ĐÁY", segs[-1][1], Y1)])
        for nm_, a, b in gaps:
            if any(lo - 60 <= (a + b) / 2 <= hi + 60 for lo, hi in cross):
                continue
            if b - a > VOID_MAX:
                out.append(f"khoảng trống {nm_} {b - a:.0f}px > {VOID_MAX} ⇒ thẻ rỗng. "
                           f"Thêm KHỐI THỨ BA (dải chốt đáy), đừng dời hai khối cũ")
        # ── ③ phủ ngang
        body = [m for m in st["nodes"]
                if m.get("kind", "circle") not in ("banner", "ribbon")]
        if len(body) >= 2:
            L = min(pos[m["id"]][0] - M._zu_box(m)[0] for m in body)
            R = max(pos[m["id"]][0] + M._zu_box(m)[0] for m in body)
            cov = (R - L) / (BX1 - BX0)
            if cov < COVER_MIN:
                out.append(f"phủ ngang {cov * 100:.0f}% < {COVER_MIN * 100:.0f}% ⇒ nội dung "
                           f"dồn một nửa khung. Giãn `at[0]` ra hai mép (hàng `fix` thì gõ tay)")
        if out:
            bad[k] = out
    return bad, n


def check_png(probe):
    """⑨ Mực sát 4 mép card, đo trên ẢNH THẬT. Dải ngang 560–1470 để tránh 2 nhân vật."""
    from PIL import Image
    hit = {}
    for f in sorted(glob.glob(str(Path(probe) / "clip_*.png"))):
        px = Image.open(f).convert("RGB").load()

        def ink(x0, x1, y0, y1, step=2):
            return sum(1 for y in range(y0, y1) for x in range(x0, x1, step)
                       if px[x, y][0] < 150 and px[x, y][1] < 150)
        w = [nm for nm, v in (("ĐÁY", ink(560, 1470, 884, 900)),
                              ("ĐỈNH", ink(560, 1470, 58, 76)),
                              ("TRÁI", ink(276, 290, 70, 360, 1)),
                              ("PHẢI", ink(1630, 1644, 70, 360, 1))) if v > EDGE_INK]
        if w:
            hit[Path(f).stem] = w
    return hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides")
    ap.add_argument("--probe", help="thư mục PNG đã dựng (--still) để kiểm lớp ⑨")
    a = ap.parse_args()
    d = json.load(io.open(a.slides, encoding="utf-8"))
    ss = d["slides"] if isinstance(d, dict) else d
    bad, n = check_spec(ss)
    print(f"── GATE BỐ CỤC `zu` — {n} thẻ ──")
    for k in sorted(bad):
        for m in bad[k]:
            print(f"  🔴 [{k:02d}] {m}")
    png = check_png(a.probe) if a.probe else {}
    for f, w in png.items():
        print(f"  🔴 {f}: mực sát mép {'/'.join(w)}")
    if bad or png:
        print(f"\n🔴 {len(bad)} thẻ lỗi spec · {len(png)} ảnh lỗi mép — SỬA XONG MỚI RENDER")
        sys.exit(1)
    print("✅ SẠCH 13/13 lớp — được render")


if __name__ == "__main__":
    main()
