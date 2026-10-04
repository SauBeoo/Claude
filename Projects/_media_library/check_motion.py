# -*- coding: utf-8 -*-
"""check_motion.py — GATE HẬU RENDER: đo lớp hình của bản mp4 đã dựng.

VÌ SAO CÓ TOOL NÀY (đọc trước khi sửa ngưỡng):
`check_frame_pace.py` đọc `project.json` TRƯỚC render và đếm *"có sự kiện hình không"*. Nó
**không thể** thấy tổng lượng chuyển động thật — animation bên trong một clip, số đếm tăng dần,
sticker trượt, zoom-punch đều nằm ngoài tầm nó. Kết quả đo được ở nenkin v26: mọi gate trước
render xanh, mà bản render có **MAD 9,97** trong khi 3 kênh đang thắng ngách đo **1,06 / 1,94 /
4,28** — khung động gấp 2,3–9,4 lần. Bằng chứng: `youtube-jp-nenkin/CHANNEL_BENCHMARK_3video_2026-09-17.md`,
luật: `.claude/rules/audience-45plus.md` §2.0-quater.

⇒ Hai gate KHÔNG thay nhau được: `check_frame_pace` chặn *khung chết*, tool này chặn *khung loạn*.

CHẠY:  python Projects/_media_library/check_motion.py <video.mp4> [--json]
Exit 1 khi có mục rớt.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # bài học §2.0h: gate crash = báo đỏ giả
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── NGƯỠNG — HIỆU CHUẨN 2026-09-17 trên 4 video, và bản ĐẦU TIÊN đã SAI ────────────────
# 🔴 Bản đầu đặt MAD 2,0–4,0 và hold 6–9s theo kiểu "lấy khoảng giữa hai kênh". Chạy thử thì
# nó ĐÁNH TRƯỢT CẢ BA kênh đang thắng (完全攻略 rớt MAD 1,94 · なぎさ rớt 4 mục · ひろと rớt 3).
# Gate đánh trượt chính mẫu nó học từ = gate sai (memory `feedback_gate_phai_qua_duoc_mau_no_hoc_tu`).
# Ngưỡng dưới đây đặt lại theo đúng DẢI đo được, sao cho 3/3 kênh thắng QUA và v26 RỚT:
#
#            | yHQ 445K | なぎさ 64K | ひろと 62K | v26 mình |  ngưỡng
#   MAD      |   1,94   |   1,06    |   4,28    |  9,97 🔴 |  ≤5,0   (chỉ TRẦN)
#   giữ hình |   9,0s   |   16,5s   |   4,0s    |  0,5s 🔴 |  ≥3,0s  (chỉ SÀN)
#   sáng nền |    201   |    214    |    223    |   175 🔴 |  ≥195
#   lệch nền |    8,0   |   33,1    |   23,1    |  43,4 🔴 |  ≤36
#   peak     |  −6,3    |  −5,4     |  −5,4     |  −1,2 🔴 |  ≤−3
#
# ⚠️ KHÔNG đặt sàn cho MAD và KHÔNG đặt trần cho "giữ hình": ba kênh thắng trải 1,06–4,28 và
# 4,0–16,5s ⇒ ở hai đại lượng này ngách KHÔNG có tín hiệu, chỉ có vùng an toàn một phía.
# "Khung chết" đã có gate riêng đo đúng hơn: `check_frame_pace.py` ③ (scene không có gì ở giữa).
MAD_MAX = 5.0                    # trần độ động. v26 = 9,97 (gấp 2,3–9,4 lần 3 kênh thắng)
HOLD_MIN = 3.0                   # sàn giữ hình (trung vị). v26 = 0,5s
BRIGHT_MIN = 195.0               # sáng TB cả bài
BRIGHT_STD_MAX = 36.0            # độ lệch nền giữa các cảnh
PEAK_MAX = -3.0                  # dBTP

W, H, FPS = 160, 90, 2           # 2fps đủ bắt đổi hình; 160×90 đủ đo MAD và độ sáng
SUB_KEEP = 0.78                  # bỏ dải phụ đề dưới khi đếm đổi hình
CUT_TH = 8                       # ngưỡng MAD coi là "đổi hình" (đã hiệu chuẩn 4/6/8/12/18)


def _gray(path: Path, w=W, h=H, fps=FPS) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path),
         "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
        capture_output=True).stdout
    n = len(raw) // (w * h)
    if n < 4:
        sys.exit(f"⛔ không đọc được khung hình từ {path}")
    return np.frombuffer(raw, np.uint8)[:n * w * h].reshape(n, h, w).astype(np.float32)


def _duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip())


def _true_peak(path: Path):
    """⚠️ `ebur128` in ở mức log INFO — KHÔNG hạ log level, nếu không hàm này trả None
    (bẫy đã ghi ở render-background.md §2.7 ②)."""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                          "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    peak = None
    for line in err.splitlines():
        s = line.strip()
        if s.startswith("Peak:"):
            try:
                peak = float(s.split()[1])
            except (IndexError, ValueError):
                pass
    return peak


# 🔴 GATE "vật cố định ở viền" ĐÃ BỊ XOÁ (2026-09-17) — nó ĐO SAI THỨ NÓ MUỐN ĐO.
# Ý đồ: đếm watermark/mascot/cast 2 mép (v26 có 3, mắt thấy rõ). Cách đo: pixel có std theo
# thời gian < 3 và lệch khỏi nền > 25. Kết quả thực tế:
#     v26 (mắt thấy 3 vật: SUBSCRIBE đỏ + mascot cú + cast 2 mép)  →  tool trả **0**
#     なぎさ (mắt thấy 1 mascot)                                    →  tool trả **2**
# Lý do hỏng: mấy vật đó KHÔNG đứng yên — cast đổi tư thế theo đoạn, SUBSCRIBE nhấp nháy,
# mascot có animation nhẹ ⇒ std cao ⇒ lọt lưới "tĩnh"; còn dải viền trang trí của なぎさ thì
# lại bị đếm thành vật. Giữ một phép đo sai trong gate còn hại hơn không có nó: nó dụ người
# ta đi sửa NỘI DUNG cho một lỗi nằm ở CÔNG CỤ (cùng bệnh `audience-45plus.md` §2.0h/§2.0i).
# ⇒ "≤1 vật cố định" chuyển sang **duyệt bằng MẮT** (§2.0-quater mục 4). Muốn cài lại thì phải
# đo bằng cách khác — ví dụ so vị trí cố định qua nhiều cảnh KHÁC NHAU, không dựa vào độ tĩnh.


def measure(path: Path) -> dict:
    dur = _duration(path)
    a = _gray(path)
    full = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    top = np.abs(np.diff(a[:, :int(H * SUB_KEEP), :], axis=0)).mean(axis=(1, 2))
    idx = np.where(top > CUT_TH)[0]
    hold = np.diff(idx) / FPS if len(idx) > 1 else np.array([dur])
    bright = a.mean(axis=(1, 2))
    return dict(dur=dur, mad=float(full.mean()), hold=float(np.median(hold)),
                cuts=float(len(idx) / (dur / 60.0)), bright=float(bright.mean()),
                bright_std=float(bright.std()), peak=_true_peak(path))


def report(path: Path, m: dict) -> bool:
    print(f"\n=== {path.name} — {m['dur']/60:.1f} phút ===")
    rows = [
        ("① MAD (độ động khung)", f"{m['mad']:.2f}", m["mad"] <= MAD_MAX,
         f"≤{MAD_MAX}  (3 kênh thắng 1,06–4,28 · v26 cũ 9,97)"),
        ("② giữ mỗi hình (trung vị)", f"{m['hold']:.1f}s", m["hold"] >= HOLD_MIN,
         f"≥{HOLD_MIN:.0f}s  (3 kênh thắng 4,0–16,5s · v26 cũ 0,5s)"),
        ("③ nền — sáng TB", f"{m['bright']:.0f}", m["bright"] >= BRIGHT_MIN,
         f"≥{BRIGHT_MIN:.0f}  (3 kênh thắng 201–223 · v26 cũ 175)"),
        ("④ nền — độ lệch giữa cảnh", f"{m['bright_std']:.1f}", m["bright_std"] <= BRIGHT_STD_MAX,
         f"≤{BRIGHT_STD_MAX:.0f}  (3 kênh thắng 8,0–33,1 · v26 cũ 43,4)"),
    ]
    if m["peak"] is not None:
        rows.append(("⑤ true peak", f"{m['peak']:.1f} dBTP", m["peak"] <= PEAK_MAX,
                     f"≤{PEAK_MAX:.0f} dBTP  (họ −5,4…−6,3 · v26 cũ −1,2)"))
    bad = 0
    for name, val, ok, std in rows:
        print(f"  {'✅' if ok else '🔴'} {name:<28} {val:>10}   (chuẩn {std})")
        bad += not ok
    print(f"\n  ⓘ tham khảo: {m['cuts']:.1f} lần đổi hình/phút (trần ≤6, `audience-45plus.md` §2 mục 1)")
    print(f"\n{'✅ SACH ' + str(len(rows)) + '/' + str(len(rows)) if not bad else '🔴 ' + str(bad) + ' MỤC RỚT'}")
    return bad == 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    allok, out = True, {}
    for v in a.video:
        if not v.exists():
            sys.exit(f"⛔ không thấy {v}")
        m = measure(v)
        out[v.name] = m
        allok &= report(v, m)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
