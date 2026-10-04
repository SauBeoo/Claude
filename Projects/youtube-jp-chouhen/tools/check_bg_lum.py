# -*- coding: utf-8 -*-
"""check_bg_lum.py — GATE độ sáng/tương phản của pool clip nền, ĐO ĐÚNG ĐOẠN renderer dùng.

🔴 Vì sao có tool này (bài học 2026-08-08, video 20):
Quy trình duyệt cũ dựng contact sheet bằng **1 frame giữa clip**. Clip
`morning-sunl_15671645.mp4` đo ở giữa ra sáng 54,9/255 → duyệt PASS. Nhưng renderer
cắt clip thành các TAKE (0–20s, 20–27,6s) và hai đoạn đó vốn tối, cộng thêm lớp
`eq brightness -0.08` + vignette ⇒ **13 cảnh trong bản render là ô ĐEN TRƠN có phụ đề**,
tức 10% thời lượng video không nhìn thấy gì. Phát hiện sau khi đã render xong 32 phút.

→ Gate này đo **từng take, 3 mốc (đầu / giữa / cuối)** thay vì 1 frame giữa clip, và
dùng **độ lệch chuẩn (tương phản)** làm tiêu chí chính, không dùng độ sáng:
  · mean thấp + std thấp  = đen trơn, KHÔNG có gì để xem  → LOẠI
  · mean thấp + std cao   = tối nhưng có điểm sáng (đèn lồng, nến) → GIỮ, đúng mood kênh
Ngưỡng std mặc định 12 hiệu chỉnh từ ca thật: `japanese-pap` (đèn lồng, giữ được) vs
`morning-sunl` (đen trơn, phải loại).

    python tools/check_bg_lum.py <slug> [--bg-only <file>] [--min-std 12] [--scene-max 20] [--scene-min 6]
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageStat

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]


def dur(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()
    return float(o) if o else 0.0


def takes_of(d, smax, smin):
    """Bản sao logic chia take của scene_render.plan_scenes_clip — phải khớp."""
    out, off = [], 0.0
    while d - off >= smin:
        du = min(smax, d - off)
        if 0 < d - off - du < smin:
            du = min(d - off, smax + smin)
        out.append((off, du))
        off += du
    return out


def sample(p, t, tmp):
    """Trích 1 frame và mô phỏng lớp hạ sáng của renderer (eq brightness -0.08)."""
    f = tmp / "f.jpg"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(p),
                    "-frames:v", "1", "-vf", "eq=brightness=-0.08,scale=320:180", str(f)],
                   check=True)
    st = ImageStat.Stat(Image.open(f).convert("L"))
    return st.mean[0], st.stddev[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--bg-only", help="file danh sách tên clip (như scene_render --bg-only)")
    ap.add_argument("--min-std", type=float, default=12.0, help="sàn độ lệch chuẩn (tương phản)")
    ap.add_argument("--scene-max", type=float, default=20.0)
    ap.add_argument("--scene-min", type=float, default=6.0)
    a = ap.parse_args()

    bg = PROJ / "06_VIDEO" / "_bg"
    if a.bg_only:
        names = [l.strip() for l in Path(a.bg_only).read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.strip().startswith("#")]
    else:
        names = sorted(p.name for p in bg.glob("*.mp4"))

    bad = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for n in names:
            p = bg / n
            d = dur(p)
            for ti, (off, du) in enumerate(takes_of(d, a.scene_max, a.scene_min)):
                vals = [sample(p, off + du * r, tmp) for r in (0.1, 0.5, 0.9)]
                mean = sum(v[0] for v in vals) / 3
                std = sum(v[1] for v in vals) / 3
                worst = min(v[1] for v in vals)
                mark = ""
                if worst < a.min_std:
                    mark = f"  <-- PHANG, khong co gi de xem (std thap nhat {worst:.1f})"
                    bad.append((n, ti, worst))
                print(f"{n[:30]:30s} take{ti} @{off:5.1f}s+{du:4.1f}s  "
                      f"sang={mean:5.1f} tuong-phan={std:5.1f}{mark}")

    print()
    if bad:
        print(f"🔴 GATE FAIL: {len(bad)} take PHANG/den tron (tuong phan < {a.min_std}) — "
              f"loai clip roi chay lai:")
        for n, ti, w in bad:
            print(f"   {n} (take{ti}, std {w:.1f})")
        sys.exit(1)
    print(f"✅ GATE PASS: {len(names)} clip, moi take deu co tuong phan >= {a.min_std}")


if __name__ == "__main__":
    main()
