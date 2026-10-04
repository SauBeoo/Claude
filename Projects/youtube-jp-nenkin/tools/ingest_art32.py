# -*- coding: utf-8 -*-
r"""ingest_art32.py — gom ảnh video 32 từ lô Flow, xoá ✦, ghi art_final/shot_KKK.png.

Chép cơ chế `ingest_art31.py` (đọc docstring ở đó).
LÔ:
  · lô 1 `Tháng 9 29 - 10_35.zip` (61/63 ảnh, 1376×768) — ghép Hungarian trên SUBJECT của
    `img32_FLOW.txt` ↔ token tên file. ⛔ Điểm token là PHỎNG ĐOÁN ⇒ sheet `_verify/` bắt buộc soi mắt;
    ô sai ghép thì chốt tay ở FIX (dòng FLOW → tên file), rồi đóng băng thành `art_map32_lot1.json`.
✦: đo 1:1 cả 61 ảnh (2026-09-29) — cố định ở (0,930W · 0,874H) ⇒ CẮT 0,905W + trim 16:9 chia đôi.
⚠️ CHỈNH TAY SAU INGEST (2026-09-29): ô 40 (「2つ目 マイナカード」) mở bằng câu đuôi của bước 1 nên ăn nhầm ảnh F31
   (cảnh sát ngồi máy tính) ⇒ dời F31 sang `art_final/rejected/unused_shot_040_police_F31.png`, chép ảnh F32 (thẻ マイナ +
   điện thoại) vào shot_040; ô 41 do `make_genten_32.py` ghi thẻ 原典 デジタル庁 đè lên. Chạy lại tool này với zip lô 1
   thì PHẢI làm lại bước tay này.
CHẠY:  python tools/ingest_art32.py            → art_final/ + art_map32.json + _verify/verify_NN.png
"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.optimize import linear_sum_assignment

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
STEM = "32_ginko-honnin-kakunin-2027"
VD = PROJ / "06_VIDEO" / STEM
ART = VD / "art_final"
LOT1 = Path(r"C:\Users\tuana\Downloads") / "Tháng 9 29 - 10_35.zip"
LOT2 = Path(r"C:\Users\tuana\Downloads") / "Tháng 9 29 - 14_40.zip"
# Lô REDO1 (4 ảnh) — tên file đọc rõ nghĩa ⇒ ghép TAY, soi mắt xác nhận.
MAP2 = {
    12: "Bank_passbook_on_table_20260929144139.jpg",
    25: "Woman_walking_past_police_box_20260929144139.jpg",
    35: "Man_handing_licence_at_counter_20260929144139.jpg",
    45: "Elderly_woman_walking_to_station_20260929144139.jpg",
}
MAP1 = VD / "art_map32_lot1.json"   # bản ghép lô 1 ĐÃ SOI MẮT — dùng khi zip lô 1 không còn
CUT = 0.905
WM = (0.930, 0.874)
N_SHOTS = 77  # plan32: 63 ô AI + 14 ô 原典
STOP = set("a an the of on in at to and with one two three four its it them their by from for "
           "same other side lying laid seen held resting beside is are into under over his her "
           "small only just".split())
# Chốt tay sau khi soi sheet: {dòng FLOW: tên file trong zip}. Rỗng = tin Hungarian.
FIX = {
    7: "Padlock_on_driving_licence_card_20260929142713.jpg",      # khoá trên thẻ, nền tối
    42: "Padlock_resting_on_driving_licence_20260929142713.jpg",  # khoá phát sáng
    56: "Padlock_resting_on_card_20260929142713.jpg",             # khoá + điện thoại gạch đỏ
}
# Soi 1:1 lô 1 (2026-09-29) — LOẠI, gen lại ở img32_FLOW_REDO1.txt (lý do: img32_prompts.REDO1_WHY)
REJECT_FILES = {
    "Passbook_with_glasses_and_tea_20260929142713.jpg",   # F12: sổ vẽ thành máy tính xách tay
    "Woman_walking_up_stairs_20260929142713.jpg",         # cổng đỏ-trắng đọc ra cổng ĐỀN
}


def toks(s):
    out = set()
    for w in re.findall(r"[a-z]+", s.lower()):
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if w not in STOP and len(w) > 2:
            out.add(w)
    return out


def cut(im):
    W, H = im.size
    x1 = int(W * CUT)
    h2 = int(x1 / 16 * 9)
    dy = (H - h2) // 2
    return im.crop((0, dy, x1, dy + h2)).resize((1920, 1080), Image.LANCZOS)


def lost_ink(im):
    """% pixel KHÁC NỀN trong dải bị cắt (trừ ô ✦). >0,5% ⇒ nội dung bị cắt, soi mắt."""
    a = np.asarray(im).astype(int)
    H, W = a.shape[:2]
    bg = a[6, 6]
    s = a[:, int(W * CUT):]
    d = np.abs(s - bg).sum(2) > 90
    wx, wy = int(W * WM[0]) - int(W * CUT), int(H * WM[1])
    d[max(0, wy - 60):wy + 60, max(0, wx - 60):wx + 60] = False
    return 100 * d.mean()


def font(sz):
    for f in (r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\msgothic.ttc"):
        if Path(f).exists():
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def main() -> int:
    ten = [l for l in open(VD / "img32_TENFILE.txt", encoding="utf-8") if l.startswith("dong ")]
    shot_of = {int(m.group(1)): int(m.group(2)) for l in ten
               for m in [re.match(r"dong (\d+) -> shot_(\d+)\.png", l)] if m}
    flow = [l.rstrip("\n") for l in open(VD / "img32_FLOW.txt", encoding="utf-8")]
    subs = [l.split("SUBJECT:", 1)[1].strip() if "SUBJECT:" in l else l for l in flow]
    ART.mkdir(parents=True, exist_ok=True)
    rows, warn, weak = [], [], []
    if not LOT1.exists():
        # zip lô 1 đã bị dời/xoá khỏi Downloads ⇒ GIỮ 59 ảnh đã cắt, đọc lại bản ghép đã duyệt
        rows = [r for r in json.loads(MAP1.read_text(encoding="utf-8")) if r["lot"] == 1]
        print(f"lô 1: zip không còn — giữ {len(rows)} ô đã cắt theo {MAP1.name}")
    else:
        z = zipfile.ZipFile(LOT1)
        names = [i.filename for i in z.infolist() if i.filename.lower().endswith((".jpg", ".jpeg", ".png"))]
        print(f"lô 1: {LOT1.name} · {len(names)} ảnh / {len(flow)} dòng FLOW")

        nt = [toks(re.sub(r"_\d{14}(_\d)?\.(jpe?g|png)$", "", n).replace("_", " ")) for n in names]
        M = np.array([[len(toks(s) & b) / max(1, len(b)) for b in nt] for s in subs])
        fixed_d = {d for d in FIX}
        fixed_n = set(FIX.values())
        sys.path.insert(0, str(PROJ / "tools"))
        from img32_prompts import REDO1_WHY
        rows_idx = [i for i in range(len(flow)) if (i + 1) not in fixed_d and (i + 1) not in REDO1_WHY]
        cols_idx = [j for j, n in enumerate(names) if n not in fixed_n and n not in REJECT_FILES]
        sub_M = M[np.ix_(rows_idx, cols_idx)]
        r, c = linear_sum_assignment(-sub_M)
        pairs = {rows_idx[i] + 1: (names[cols_idx[j]], float(sub_M[i, j])) for i, j in zip(r, c)}
        for d, n in FIX.items():
            pairs[d] = (n, -1.0)

        for d in sorted(pairs):
            n, sc = pairs[d]
            im = Image.open(io.BytesIO(z.read(n))).convert("RGB")
            li = lost_ink(im)
            if li > 0.5:
                warn.append((d, shot_of[d], n[:44], li))
            if 0 <= sc < 0.34:
                weak.append((d, shot_of[d], n[:44], sc))
            cut(im).save(ART / f"shot_{shot_of[d]:03d}.png")
            rows.append(dict(flow=d, shot=shot_of[d], lot=1, file=n, score=round(sc, 2), lost_ink=round(li, 2)))
    if LOT2.exists():
        z2 = zipfile.ZipFile(LOT2)
        for d, n in MAP2.items():
            im = Image.open(io.BytesIO(z2.read(n))).convert("RGB")
            li = lost_ink(im)
            if li > 0.5:
                warn.append((d, shot_of[d], n[:44], li))
            cut(im).save(ART / f"shot_{shot_of[d]:03d}.png")
            rows.append(dict(flow=d, shot=shot_of[d], lot=2, file=n, score=-1.0, lost_ink=round(li, 2)))
        rows.sort(key=lambda r: r["flow"])
        print(f"lô 2 (REDO1): {LOT2.name} · {len(MAP2)} ảnh ghép tay")
    (VD / "art_map32.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── sheet đối chiếu: ảnh (sau cắt) + SUBJECT prompt, 3×3 mỗi trang ──
    vdir = VD / "_verify"
    vdir.mkdir(exist_ok=True)
    f1, cw, ch = font(22), 640, 360
    for p in range(0, len(rows), 9):
        sheet = Image.new("RGB", (cw * 3, (ch + 120) * 3), (255, 255, 255))
        dr = ImageDraw.Draw(sheet)
        for i, rw in enumerate(rows[p:p + 9]):
            x, y = (i % 3) * cw, (i // 3) * (ch + 120)
            sheet.paste(Image.open(ART / f"shot_{rw['shot']:03d}.png").resize((cw, ch)), (x, y))
            t = f"F{rw['flow']} shot_{rw['shot']:03d} s={rw['score']}  " + subs[rw["flow"] - 1][:150]
            for k in range(4):
                dr.text((x + 6, y + ch + 4 + k * 28), t[k * 52:(k + 1) * 52], font=f1, fill=(20, 20, 20))
        sheet.save(vdir / f"verify_{p // 9:02d}.png")

    print(f"ô ảnh AI: {len(rows)} · ảnh bị dùng lại: {len(rows) - len({r['file'] for r in rows})}")
    print(f"✦: cắt {CUT}W + trim 16:9 → 1920×1080")
    print(f"⚠️ ô có mực trong dải bị cắt (>0,5%) — SOI MẮT: {len(warn)}")
    for w in warn:
        print("    FLOW %2d · shot_%03d · %s · %.2f%%" % w)
    print(f"⚠️ ô ghép token YẾU (<0,34) — SOI MẮT đúng ô: {len(weak)}")
    for w in weak:
        print("    FLOW %2d · shot_%03d · %s · %.2f" % w)
    got = {r["flow"] for r in rows}
    for d in sorted(set(shot_of) - got):
        print(f"🔴 dòng FLOW {d} (shot_{shot_of[d]:03d}) chưa có ảnh — {subs[d - 1][:90]}")
    miss = [k for k in range(N_SHOTS) if not (ART / f"shot_{k:03d}.png").exists()]
    print(f"ô chưa có ảnh trong art_final (gồm 14 ô 原典 chưa dựng): {len(miss)} {miss}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
