# -*- coding: utf-8 -*-
r"""ingest_clips_25.py — nhận lô clip t2v của video 25 từ Google Flow về `clips/`.

CHẠY:
    python tools/ingest_clips_25.py --src "F:\Youtube\<thu muc Flow>"          # xem truoc
    python tools/ingest_clips_25.py --src "F:\Youtube\<thu muc Flow>" --go     # lam that

🔴 BA BÀI HỌC CỦA LƯỢT t2v VIDEO 22 — ĐÃ CÀI THÀNH GATE, ĐỪNG GỠ:

 ① **Flow KHÔNG trả 1 clip / 1 prompt.** Ở video 22: gửi 25 prompt, nhận 25 clip nhưng
    **thừa 2 + thiếu 2** (hai bản thừa là biến thể của cùng một prompt). ⇒ Tuyệt đối không
    đổi tên mù theo thứ tự. Tool **DỪNG** khi số clip ≠ số prompt của lô và bắt khai
    `--map` bằng tay.

 ② **Map clip→khe bằng máy đã SAI 2/2 lần ở t2v** (i2v thì được, vì có ảnh start-frame khớp
    MD5). t2v không có mỏ neo nào: 19/82 khe của bài này cùng khuôn SCREEN/DESK nên caption
    Flow trả về gần như giống hệt. ⇒ Thứ tự mặc định chỉ là GIẢ ĐỊNH; phải soi sheet mắt
    (`--sheet`) rồi mới `--go`.

 ③ **Kiểm ✦ watermark theo TỪNG LÔ, đừng tin hằng số.** Lô t2v video 22 **không có** ✦
    (soi 1:1 bốn góc 12 clip nền sáng nhất), lô i2v thì có và lệch tới 45px giữa các clip.
    Tool in cảnh báo, không tự cắt.

⚠️ Clip Flow là **8,000s @ 24fps**. Builder tự hạ `speed` cho khớp khe; đừng resample ở đây.
"""
import argparse
import io
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = r"E:\Claude\Projects\youtube-jp-nenkin"
VD = os.path.join(PROJ, r"06_VIDEO\25_nenkin-tenbiki-tetori-6man2sen")
CLIPS = os.path.join(VD, "clips")
TENFILE = os.path.join(VD, "vox25_TENFILE.txt")


def want_keys():
    """Đọc sổ tên: dòng N -> clips/clip_<key>.mp4"""
    out = []
    for l in io.open(TENFILE, encoding="utf-8"):
        m = re.search(r"clips/(\S+?\.mp4)", l)
        if m:
            out.append(m.group(1))
    return out


def probe(p):
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", p],
            capture_output=True, text=True, timeout=30)
        v = [x for x in r.stdout.split() if x]
        return f"{v[0]}x{v[1]} {v[2]} {float(v[3]):.2f}s" if len(v) >= 4 else "?"
    except Exception:
        return "?"


def sheet(src, files):
    """Xuất sheet 3 frame/clip để SOI MẮT trước khi đổi tên (gate ②)."""
    import cv2
    import numpy as np
    os.makedirs(os.path.join(VD, "_ingest_sheet"), exist_ok=True)
    for i, f in enumerate(files, 1):
        cap = cv2.VideoCapture(os.path.join(src, f))
        fr = []
        for t in (300, 4000, 7600):
            cap.set(cv2.CAP_PROP_POS_MSEC, t)
            ok, im = cap.read()
            if ok:
                fr.append(cv2.resize(im, (420, 236)))
        cap.release()
        if fr:
            cv2.imwrite(os.path.join(VD, "_ingest_sheet", f"{i:03d}_{f[:26]}.png"),
                        np.hstack(fr))
    print(f"  → sheet: {os.path.join(VD, '_ingest_sheet')}  ({len(files)} clip)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="thu muc Flow tra clip ve")
    ap.add_argument("--first", type=int, default=1, help="dong dau cua lo (1-based)")
    ap.add_argument("--go", action="store_true", help="lam that (mac dinh chi xem truoc)")
    ap.add_argument("--sheet", action="store_true", help="xuat sheet 3 frame/clip de soi mat")
    ap.add_argument("--map", default="", help="ep map tay: 'file.mp4=clip_0a.mp4,...'")
    a = ap.parse_args()

    keys = want_keys()
    files = sorted(f for f in os.listdir(a.src) if f.lower().endswith(".mp4"))
    if not files:
        print(f"🔴 khong thay .mp4 nao trong {a.src}")
        return 1
    print(f"kho dich : {CLIPS}")
    print(f"so prompt: {len(keys)}  ·  clip trong thu muc: {len(files)}")

    if a.sheet:
        sheet(a.src, files)
        return 0

    pairs = []
    if a.map:
        tbl = dict(x.split("=") for x in a.map.split(",") if "=" in x)
        for f, k in tbl.items():
            pairs.append((f.strip(), k.strip()))
    else:
        seg = keys[a.first - 1: a.first - 1 + len(files)]
        # ── GATE ①: so luong phai khop, neu khong DUNG ────────────────────
        if len(seg) != len(files):
            print(f"🔴 GATE: lo co {len(files)} clip nhung so ghi {len(seg)} khe "
                  f"(tu dong {a.first}). Flow hay tra thua/thieu — khai tay bang --map.")
            return 1
        pairs = list(zip(files, seg))
        print("⚠️  Dang map THEO THU TU — day chi la GIA DINH (gate ②).")
        print("    Chay --sheet va soi mat truoc khi --go.")

    os.makedirs(CLIPS, exist_ok=True)
    for f, k in pairs:
        s = os.path.join(a.src, f)
        d = os.path.join(CLIPS, k)
        print(f"  {f[:44]:<46} -> {k:<16} {probe(s)}")
        if a.go:
            shutil.copyfile(s, d)
    print(f"\n{'DA CHEP' if a.go else 'XEM TRUOC (them --go de lam that)'}: {len(pairs)} clip")
    if a.go:
        print("⚠️  GATE ③: soi 1:1 BON GOC vai clip nen sang nhat xem co dau ✦ khong "
              "(lo t2v cua video 22 khong co, nhung phai kiem tung lo).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
