# -*- coding: utf-8 -*-
r"""autofocus.py — tìm VÙNG ĐÁNG NHÌN trong ảnh, ghi vào `shot.focus` của SLIDES.json.

VÌ SAO CÓ FILE NÀY (bài học 2026-08-18, video 21)
────────────────────────────────────────────────────────────────────────────────
`make_shot.py` mode `inset`/`focus` cần biết NHÌN VÀO ĐÂU. Bản đầu để mặc định
[0.52, 0.5, 0.16] — và soi clip thật thì hỏng đúng như dự đoán:
  · clip_05: tấm inset là một mảng TƯỜNG TRẮNG TRƠN, mũi tên trỏ vào khoảng không
  · clip_07: y hệt, mảng tường xám
Ảnh cảnh hiếm khi có chủ thể nằm giữa khung ⇒ crop giữa gần như luôn trúng chỗ trống.

CÁCH ĐO: vùng "đáng nhìn" = vùng có NHIỀU CHI TIẾT nhất (độ lệch chuẩn cục bộ cao),
loại 8% mép mỗi phía. Rồi so đỉnh với trung vị:
  · đỉnh nổi trội  → giữ inset/focus, đặt tâm vào đó
  · ảnh phẳng đều  → HẠ VỀ `soft` (không có gì để khoanh thì đừng khoanh — vòng đỏ
    trỏ vào chỗ vô nghĩa tệ hơn không có vòng)

    python autofocus.py <SLIDES.json> --img-dir <folder> [--apply]
"""
import argparse, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)

EDGE = 0.17          # bỏ 17% mép mỗi phía.
#   🔴 bản đầu để 0.08 và 12/46 tâm rơi đúng y=0.08 — vùng chi tiết cao nhất của ảnh
#   phòng tắm hay là VIỀN CỬA SỔ / mép trần, tức mép khung. Crop quanh đó bị clamp
#   nên tấm inset lệch hẳn khỏi tâm đã chọn.
WIN = 33             # cửa sổ đo chi tiết (px, trên ảnh đã thu nhỏ)
FLAT = 1.55          # đỉnh/trung vị < ngưỡng này = ảnh phẳng đều → hạ về soft


def detail_map(p, w=320):
    im = Image.open(p).convert("L")
    h = max(1, int(w * im.height / im.width))
    a = np.asarray(im.resize((w, h)), dtype=np.float64)
    mean = ndimage.uniform_filter(a, WIN)
    sq = ndimage.uniform_filter(a * a, WIN)
    var = np.clip(sq - mean * mean, 0, None)
    return np.sqrt(var)


def best_spot(p):
    d = detail_map(p)
    h, w = d.shape
    ey, ex = int(h * EDGE), int(w * EDGE)
    core = d[ey:h - ey, ex:w - ex]
    if core.size == 0:
        return None
    sm = ndimage.uniform_filter(core, WIN)
    # thiên vị nhẹ về giữa: hai vùng chi tiết ngang nhau thì lấy cái gần tâm hơn,
    # vì crop quanh tâm ít bị clamp và mắt người xem cũng ở giữa khung
    hh, ww = sm.shape
    yy, xx = np.mgrid[0:hh, 0:ww]
    dist = np.sqrt(((xx / ww - .5) * 2) ** 2 + ((yy / hh - .5) * 2) ** 2) / 1.4142
    sm = sm * (1 - 0.35 * dist)
    k = int(np.argmax(sm))
    cy, cx = np.unravel_index(k, core.shape)
    peak = float(core[cy, cx])
    med = float(np.median(core)) or 1e-6
    return ((cx + ex) / w, (cy + ey) / h, peak / med)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides")
    ap.add_argument("--img-dir", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    sp = Path(a.slides)
    cfg = json.loads(sp.read_text(encoding="utf-8"))
    img_dir = Path(a.img_dir)
    n_set = n_flat = n_miss = n_alt = 0
    prev_mode = None
    print("  slot  mode    -> tâm mới        nổi trội   ảnh")
    for i, e in enumerate(cfg):
        s = e.get("shot")
        if not isinstance(s, dict) or s.get("mode") not in ("inset", "focus"):
            continue
        p = Path(s["photo"])
        if not p.is_absolute():
            p = img_dir / p
        if not p.exists():
            print(f"  {i:>4}  {s['mode']:<7} -> THIẾU ẢNH        —        {p.name}")
            n_miss += 1
            continue
        r = best_spot(p)
        if r is None:
            continue
        cx, cy, ratio = r
        if ratio < FLAT:
            s["mode"] = "soft"
            s.pop("focus", None)
            s.pop("inset_pos", None)
            n_flat += 1
            prev_mode = "soft"
            print(f"  {i:>4}  {'→soft':<7} -> ảnh phẳng đều   {ratio:.2f}x    {p.name[:34]}")
            continue
        # 🔴 KHONG hai `inset` LIEN TIEP: hai tam anh truot vao lien nhau nhin nhu mot
        #    khung duy nhat lap lai (thay ro o demo 95s dau, khung 0:50 va 1:09).
        #    Doi cai thu hai sang `focus` neu anh du noi troi, khong thi `soft`.
        if s["mode"] == "inset" and prev_mode == "inset":
            s["mode"] = "focus" if ratio >= 2.0 else "soft"
            n_alt += 1
            if s["mode"] == "soft":
                s.pop("focus", None); s.pop("inset_pos", None)
                prev_mode = "soft"
                print(f"  {i:>4}  {'inset→soft':<10} -> tranh lap                 {p.name[:30]}")
                continue
            print(f"  {i:>4}  {'inset→focus':<10} -> [{cx:.2f}, {cy:.2f}]   {ratio:.2f}x  tranh lap")
        prev_mode = s["mode"]
        s["focus"] = [round(cx, 3), round(cy, 3), 0.15]
        if s["mode"] == "inset":
            # card đặt ĐỐI DIỆN vùng nhìn để mũi tên không cắt ngang chủ thể
            s["inset_pos"] = "br" if cx < 0.5 else "bl"
        else:
            s.pop("inset_pos", None)
        n_set += 1
        print(f"  {i:>4}  {s['mode']:<7} -> [{cx:.2f}, {cy:.2f}]   {ratio:.2f}x    {p.name[:34]}")

    print(f"\nđặt tâm {n_set} · hạ về soft {n_flat} · thiếu ảnh {n_miss}")
    if a.apply:
        sp.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[OK] đã ghi {sp}")
    else:
        print("(xem trước — thêm --apply để ghi)")


if __name__ == "__main__":
    main()
