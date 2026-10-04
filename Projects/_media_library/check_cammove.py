# -*- coding: utf-8 -*-
"""check_cammove.py — GATE HẬU GEN cho CLIP AI: máy quay có DI CHUYỂN THẬT không?

VÌ SAO CÓ TOOL NÀY (đọc trước khi sửa ngưỡng):
`check_motion.py` đo **MAD** = tổng lượng chuyển động trong khung. Nó **không phân biệt được**
"máy đứng yên, người cử động" với "máy dolly qua phòng". Đo thật trên 7 clip demo của video 16
showa: cả 7 clip đều **%khung đứng yên = 0,0** và MAD 7,2–15,0 (đều trông "có động"), nhưng
3 trong số đó **máy không hề tiến/lùi** — `scale` frame-đầu↔frame-cuối chỉ 0,995–1,021.
User nhìn ra ngay: *"góc di chuyển cam không rõ ràng lắm"*.

⇒ Đại lượng đúng để hỏi "máy có DI không" là **biến đổi affine giữa frame đầu và frame cuối**:
   · `scale` đổi  ⇒ máy tiến/lùi (dolly)     · `dịch`  ⇒ máy lia/track ngang-dọc
   Hai gate KHÔNG thay nhau: `check_motion` chặn *khung chết*, tool này chặn *máy chết*.

⚠️ BẮT BUỘC dùng `MOTION_AFFINE`, KHÔNG dùng `MOTION_EUCLIDEAN` — Euclidean không có tham số
   scale nên mọi cú dolly/zoom bị chấm thành "không di chuyển" (cùng bẫy đã ghi ở
   `audience-45plus.md` §2.0-ter khi phân loại ảnh tĩnh/động).

CHẠY:  python Projects/_media_library/check_cammove.py <clip.mp4 | thư mục> [--json]
Luật:  `.claude/rules/camera-language.md` §8.2
Exit 1 khi có clip rớt.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

try:
    import cv2
except ImportError:
    sys.exit("⛔ cần opencv: pip install opencv-python")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # §2.0h: gate crash = báo đỏ giả
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── NGƯỠNG — hiệu chuẩn 2026-09-21 trên 7 clip demo video 16 ────────────────────────────
#            clip           scale   dịch px   đọc
#   D1 office_cha           1.133     24.2    ✅ dolly chạy
#   D2 office_futari        1.207     77.7    ✅
#   D3 soubetsu             1.469     54.7    ✅ mạnh
#   D8 wave                 0.789     79.0    ✅ dolly out
#   D4 yakusho              0.999     10.4    🔴 "sink down" KHÔNG chạy
#   D5 chanoma              1.021     23.5    🔴 "travel backward in" KHÔNG chạy
#   D6 omiai                0.995      5.1    🔴🔴 máy đứng yên
#   ⇒ Bốn cú tiến/lùi/ngang đều ≥13% scale; ba cú trục DỌC đều <2,1%. Ngưỡng đặt ở giữa
#     hai cụm, lệch về phía thấp để không đánh trượt cú track thuần (scale không đổi).
SCALE_MIN = 0.05      # |scale − 1| ≥ 5% ⇒ có dolly thật
SHIFT_MIN = 8.0       # dịch ≥ 8px @320 ⇒ có track/lia thật
W, H, FPS = 320, 180, 2


def _frames(p: Path, fps=FPS):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(p), "-vf",
         f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
        capture_output=True).stdout
    n = len(raw) // (W * H)
    if n < 3:
        return None
    return np.frombuffer(raw, np.uint8)[:n * W * H].reshape(n, H, W)


def _affine(a, b):
    """🔴 ECC KHONG HOI TU != MAY KHONG DI — thuong la nguoc lai: cu di QUA LON.
    Do that o lo clip v8: task_001 va task_004 bao "khong hoi tu", trong khi cac clip cung lo
    do duoc scale 1,09-1,96. Ban dau cua tool nay dem chung vao cot ROT => bao do GIA, va no
    du nguoi ta di sua NOI DUNG cho mot loi nam o CONG CU (dung benh audience-45plus §2.0h/i).
    ⇒ Thang xuong do phan giai thap dan (ECC de hoi tu hon khi anh nho), va neu van truot thi
      tra ve None de goi la KHONG DO DUOC — khong phai ROT."""
    for scale in (1.0, 0.5, 0.25):
        aa, bb = a, b
        if scale < 1.0:
            aa = cv2.resize(a, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            bb = cv2.resize(b, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        wm = np.eye(2, 3, dtype=np.float32)
        try:
            cv2.findTransformECC(aa.astype(np.float32) / 255., bb.astype(np.float32) / 255., wm,
                                 cv2.MOTION_AFFINE,
                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 500, 1e-6),
                                 None, 5)
        except cv2.error:
            continue
        wm[0, 2] /= scale                      # dua dich ve thang do goc
        wm[1, 2] /= scale
        return wm
    return None


def measure(p: Path) -> dict:
    f = _frames(p)
    if f is None:
        return dict(err="không đọc được khung hình")
    wm = _affine(f[0], f[-1])
    if wm is None:
        # khong do duoc bang affine -> do THO bang phase correlation (chi ra dich, khong ra scale)
        sh = cv2.phaseCorrelate(f[0].astype(np.float64), f[-1].astype(np.float64))[0]
        return dict(err="ECC không hội tụ (cú di quá lớn) — đo thô",
                    shift=float(np.hypot(*sh)), scale=None, path=None)
    sc = (np.hypot(wm[0, 0], wm[1, 0]) + np.hypot(wm[0, 1], wm[1, 1])) / 2
    net = float(np.hypot(wm[0, 2], wm[1, 2]))
    path = 0.0
    for i in range(len(f) - 1):
        w = _affine(f[i], f[i + 1])
        if w is not None:
            path += float(np.hypot(w[0, 2], w[1, 2]))
    return dict(scale=float(sc), shift=net, path=path)


def report(p: Path, m: dict) -> bool:
    if "err" in m:
        # KHONG tinh la ROT: day la gioi han cua phep do, khong phai ket luan ve clip
        extra = f"  dịch thô {m['shift']:.0f}px" if m.get("shift") is not None else ""
        print(f"  ⚠️ {p.name:<30} {m['err']}{extra}  → soi MẮT, đừng chấm rớt")
        return True
    dsc = abs(m["scale"] - 1)
    dolly, track = dsc >= SCALE_MIN, m["shift"] >= SHIFT_MIN
    ok = dolly or track
    kind = " + ".join(([f"DOLLY {(m['scale']-1)*100:+.0f}%"] if dolly else [])
                      + ([f"TRACK {m['shift']:.0f}px"] if track else [])) or "MÁY KHÔNG DI"
    print(f"  {'✅' if ok else '🔴'} {p.name:<30} scale {m['scale']:.3f}  dịch {m['shift']:5.1f}px  "
          f"đường đi {m['path']:6.1f}px   {kind}")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", type=Path, nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    clips = []
    for t in a.target:
        clips += sorted(t.glob("*.mp4")) if t.is_dir() else [t]
    if not clips:
        sys.exit("⛔ không thấy clip nào")
    print(f"\nGATE MÁY QUAY — {len(clips)} clip  (chuẩn: |scale−1| ≥ {SCALE_MIN:.0%} HOẶC dịch ≥ {SHIFT_MIN:.0f}px)")
    print("-" * 104)
    out, bad = {}, 0
    for c in clips:
        m = measure(c)
        out[c.name] = m
        bad += not report(c, m)
    print("-" * 104)
    print("  ⓘ scale = máy tiến/lùi (dolly) · dịch = máy lia/track. Cú track THUẦN thì scale ≈ 1 —")
    print("    đó là lý do gate lấy ĐIỀU KIỆN HOẶC, không phải VÀ.")
    print(f"\n{'✅ SACH ' + str(len(clips)) + '/' + str(len(clips)) if not bad else '🔴 ' + str(bad) + ' CLIP MÁY KHÔNG DI'}")
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
