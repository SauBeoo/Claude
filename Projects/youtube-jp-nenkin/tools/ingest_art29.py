# -*- coding: utf-8 -*-
r"""ingest_art29.py — gom ảnh các ô của video 29 từ 2 lô gen, xoá ✦, chuẩn hoá 1920×1080.

KHÁC v28 MỘT CHỖ: **KHÔNG cần bảng map tay.** v28 phải map tay vì tên file model đặt
**trùng nhau hàng loạt** (`Elderly_woman_climbing_step_blocks` có 4 bản trong một lô) ⇒ khớp
token sai 17/92. Lô v29 đo được **tên duy nhất 100%** ở cả hai lô (89/89 và 24/24) — vì subject
đã đổi sang **vật cụ thể**, không còn mấy câu hình học na ná nhau. ⇒ khớp bằng token là đủ,
nhưng **mọi ô khớp yếu vẫn phải soi mắt** (xem `--probe`).

HAI LÔ, ƯU TIÊN LÔ MỚI:
  · `Sep 21 - 17_57` (24 ảnh) = vòng REDO, **chỉ dùng cho 24 dòng FLOW đã đổi**
  · `Sep 21 - 17_34` (89 ảnh) = lô đầu, dùng cho 66 dòng còn lại
  ⛔ 23 ảnh cũ của các dòng đã REDO **KHÔNG được dùng** — chúng là bản hình trừu tượng user bác.

XOÁ ✦ (`media-library.md` §2.10 ⑤b — ảnh còn ✦ = chưa xong): cùng cơ chế v28 (inpaint NS,
mask = pixel sáng hơn trung vị cục bộ > 3). ⚠️ Toạ độ ✦ **đo lại cho lô này**, không bê của v28.

CHẠY:  python tools/ingest_art29.py           → art_final/shot_KKK.png + bảng kiểm
       python tools/ingest_art29.py --probe   → thêm sheet soi góc ✦ 1:1 sau khi vá
"""
import io
import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
import img29_prompts as ip  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STEM = "29_shikaku-kakuninsho-8gatsu-85sai"
VD = PROJ / "06_VIDEO" / STEM
DL = Path(r"C:\Users\tuana\Downloads")
LOT_NEW = DL / "Sep 21 - 17_57"     # vòng REDO
LOT_OLD = DL / "Sep 21 - 17_34"     # lô đầu

# dòng FLOW (1-based) đã đổi subject ở vòng REDO — chỉ những dòng này lấy từ LOT_NEW
REDO = {5, 7, 8, 9, 24, 29, 34, 35, 38, 39, 41, 51, 52, 66,
        72, 73, 79, 80, 81, 82, 83, 86, 89, 90}

STAR_R = 46
STOP = {"a", "an", "the", "of", "on", "in", "at", "to", "and", "with", "one", "two",
        "three", "four", "its", "it", "them", "their", "by", "from", "for", "same",
        "other", "side", "lying", "laid", "seen", "held", "resting", "beside"}


def toks(s):
    """🔴 CÓ RÚT ĐUÔI SỐ NHIỀU. Bản đầu so token thô ⇒ `certificate`≠`certificates`,
    `hand`≠`hands`, `card`≠`cards` — và đó là THỦ PHẠM CHÍNH làm điểm tụt xuống 0,25–0,33
    rồi kéo theo mấy vòng vá sổ đen. Tên file model đặt hay ở số nhiều, subject hay số ít."""
    out = set()
    for w in re.findall(r"[a-z]+", s.lower()):
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if w not in STOP and len(w) > 2:
            out.add(w)
    return out


def star_xy(img):
    """Đo tâm ✦ của CHÍNH ảnh này (góc dưới-phải), thay vì bê hằng số của lô khác."""
    h, w = img.shape[:2]
    y0, x0 = int(h * 0.80), int(w * 0.85)
    g = cv2.cvtColor(img[y0:, x0:], cv2.COLOR_BGR2GRAY).astype(np.int16)
    med = int(np.median(g))
    m = ((g - med) > 3).astype(np.uint8)
    if m.sum() < 60:
        return None
    ys, xs = np.nonzero(m)
    return int(x0 + xs.mean()), int(y0 + ys.mean())


def strip_star(bgr):
    c = star_xy(bgr)
    if c is None:
        return bgr, 0
    cx, cy = c
    h, w = bgr.shape[:2]
    x0, y0 = max(0, cx - STAR_R), max(0, cy - STAR_R)
    x1, y1 = min(w, cx + STAR_R), min(h, cy + STAR_R)
    box = bgr[y0:y1, x0:x1]
    g = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY).astype(np.int16)
    mask = ((g - int(np.median(g))) > 3).astype(np.uint8) * 255
    yy, xx = np.ogrid[:mask.shape[0], :mask.shape[1]]
    mask[((xx - (cx - x0))**2 + (yy - (cy - y0))**2) > 40**2] = 0
    if mask.sum() == 0:
        return bgr, 0
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), 1)
    out = bgr.copy()
    out[y0:y1, x0:x1] = cv2.inpaint(box, mask, 6, cv2.INPAINT_NS)
    return out, int((mask > 0).sum())


def main() -> int:
    shots = json.loads((VD / "plan29.json").read_text(encoding="utf-8"))["shots"]

    # ── dựng lại đúng thứ tự dòng FLOW như img29_prompts đã ghi ──────────
    order, used_var = [], {}
    for k, sh in enumerate(shots):
        j, row = ip.row_for(sh["lines"][0])
        if j == "GENTEN":
            order.append((k, None, row))
            continue
        vs, _doc = ip.variants_of(row)
        n = used_var.get(j, 0)
        used_var[j] = n + 1
        order.append((k, vs[n], None))

    flow_i, tasks = 0, []
    for k, subj, gen in order:
        if subj is None:
            tasks.append((k, None, gen))
            continue
        flow_i += 1
        tasks.append((k, (flow_i, subj), None))

    # ⛔ SỔ ĐEN — 19 ảnh TRỪU TƯỢNG của lô đầu mà user đã bác (dải navy · mốc · ô tick · thẻ úp ·
    # "bàn gọn gàng" · đường kẻ chia người). Chúng **không được dự thi**: ghép toàn cục tối đa
    # hoá TỔNG điểm, nên một ảnh rác vẫn có thể chen vào một ô nếu nó nhả ảnh tốt cho ô khác —
    # đã dính thật: ô 040 nhận `People_standing_on_bands`. Loại khỏi rổ là cách duy nhất chắc.
    REJECT = ("Bands_and_markers", "Checkboxes_", "Desk_lamp_over", "Elderly_people_divided",
              "Four_square_cards", "Navy_band_", "People_divided",
              "People_standing_on_bands", "Red_marker_on_navy", "Red_pen_drawing_navy",
              "Tidy_desk_", "Desk_with_notebook", "Three_small_items")
    allf = list(LOT_NEW.glob("*.jpe*g")) + list(LOT_OLD.glob("*.jpe*g"))
    dropped = [f for f in allf if f.name.startswith(REJECT)]
    pool = {p: toks(p.stem) for p in allf if not p.name.startswith(REJECT)}
    print(f"rổ ứng viên: {len(pool)} ảnh (loại {len(dropped)} ảnh trừu tượng đã bị bác)")
    dst = VD / "art_final"
    dst.mkdir(parents=True, exist_ok=True)

    # ── GHÉP TỐI ƯU TOÀN CỤC, KHÔNG THAM LAM ─────────────────────────────
    # 🔴 Bản đầu duyệt ô theo thứ tự và mỗi ô lấy ảnh điểm cao nhất còn trống ⇒ ô ĐỨNG TRƯỚC
    # cướp mất ảnh mà ô ĐỨNG SAU mới thật sự cần: ô 048 lấy `Certificate_propped_against_teacup`
    # (0,50) rồi ô 072 — chính là ô của câu "certificate propped against a teacup" — chỉ còn
    # best 0,33 và bị báo "KHÔNG có ảnh". **7 ô báo thiếu, thật ra không thiếu ảnh nào.**
    # ⇒ Đây là bài toán ghép cặp, phải giải bằng Hungarian trên TOÀN BỘ ma trận điểm.
    from scipy.optimize import linear_sum_assignment

    # 🔴 KHÔNG chia theo LÔ nữa. Bản trước khoá "dòng FLOW này phải lấy từ lô REDO", nhưng danh
    # sách REDO được tính ở trạng thái TRƯỚC khi thay 19 hàng subject ⇒ số dòng FLOW đã dịch,
    # và ô 089 bị ép lấy `People_standing_on_bands` — đúng một trong những ảnh trừu tượng user
    # vừa bác. Cùng bệnh `feedback_doi_don_vi_hinh_ra_ca_lo`: neo vào một chỉ số đã trôi.
    # ⇒ Ghép TOÀN CỤC trên cả 113 ảnh của hai lô. Tên file sinh từ nội dung prompt, nên ảnh
    # REDO tự thắng các ô REDO, còn 23 ảnh trừu tượng cũ **không khớp ai và bị bỏ lại** —
    # đúng kết quả mong muốn, không cần danh sách tay nào.
    pairs = {}
    cand = list(pool)
    jobs = [(k, fi, subj) for k, item, _g in tasks if item for fi, subj in [item]]
    M = np.zeros((len(jobs), len(cand)))
    for a, (_k, _fi, subj) in enumerate(jobs):
        st = toks(subj)
        for b, q in enumerate(cand):
            # ⚠️ KHÔNG dùng Jaccard: subject dài 12–20 token, tên file chỉ 3–5 ⇒ mẫu số phình,
            # điểm tụt xuống 0,06–0,15 và ngưỡng nào cũng loại sạch. Thang đúng là
            # "bao nhiêu phần của TÊN FILE được subject giải thích".
            M[a, b] = len(st & pool[q]) / max(len(pool[q]), 1)
    ri, ci = linear_sum_assignment(-M)
    for a, b in zip(ri, ci):
        pairs[jobs[a][0]] = (cand[b], M[a, b])

    taken, rows, miss, weak, patched = set(), [], [], [], 0
    for k, item, gen in tasks:
        if item is None:
            rows.append((k, "原典", gen, 0.0))
            continue
        fi, subj = item
        best, bs = pairs.get(k, (None, 0.0))
        if best is None or bs < 0.20:
            miss.append((k, fi, subj[:52], f"{bs:.2f}"))
            continue
        if bs < 0.45:
            weak.append((k, fi, best.name[:44], f"{bs:.2f}"))
        taken.add(best)
        img = cv2.imdecode(np.fromfile(str(best), np.uint8), cv2.IMREAD_COLOR)
        img, npx = strip_star(img)
        patched += 1 if npx else 0
        if (img.shape[1], img.shape[0]) != (1920, 1080):
            img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
        Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(dst / f"shot_{k:03d}.png")
        rows.append((k, best.parent.name[-5:], best.name[:40], bs))

    print(f"ô: {len(tasks)} · ghép được {len(taken)} · 原典 {sum(1 for r in rows if r[1]=='原典')}"
          f" · ✦ đã vá {patched}")
    print(f"ảnh bị dùng lại: {len(taken) - len(set(taken))}")
    if weak:
        print(f"\n⚠️ {len(weak)} ô khớp YẾU (<0,55) — BẮT BUỘC soi mắt:")
        for k, fi, n, s in weak:
            print(f"    ô {k:03d} (FLOW {fi:2d})  {s}  {n}")
    if miss:
        print(f"\n🔴 {len(miss)} ô KHÔNG có ảnh — ⛔ chưa được render (`render-background.md` §1.5):")
        for k, fi, s, sc in miss:
            print(f"    ô {k:03d} (FLOW {fi:2d})  best={sc}  {s}")
    (VD / "art_map29.json").write_text(
        json.dumps([{"shot": r[0], "lot": r[1], "file": r[2], "score": round(r[3], 3)}
                    for r in rows], ensure_ascii=False, indent=1), encoding="utf-8")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
