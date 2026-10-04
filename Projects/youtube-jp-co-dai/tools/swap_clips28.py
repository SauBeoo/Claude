# -*- coding: utf-8 -*-
r"""Thay 3 clip cua video 28 bang ban gen moi (lo Du_an_moi_8_349x1q6v).

  task_001 -> v_A4_window-black-night   (ban cu LOI TRIPOD o goc phai)
  task_002 -> v_A1_fan-curtain-still    (frame DAU: tran chiem nua khung = chu the bai)
  task_003 -> v_D1_foil-macro           (ban cu chay trang, 120px khong ro la nhom)

Chuan hoa 1920x1080 / 30fps / bo audio giong `ingest_clips28.py`, ghi de vao clips/
va copy sang public cua remotion. Sau do chi can:

    python tools\build_remotion_28.py
    python tools\render_chunks28.py --only 0,3
"""
import io
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True, write_through=True)

SRC = Path(r"F:\Youtube\Dự_án_mới_8_349x1q6v")
VD = Path(r"E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\28_dannetsu-tenjo-alumi")
PUB = Path(r"E:\Claude\Projects\remotion-vox\public\projects\co-dai-28\assets")
BAK = VD / "clips" / "_replaced"

MAP = {
    "task_001_1_1080p.mp4": "v_A4_window-black-night",
    "task_002_1_1080p.mp4": "v_A1_fan-curtain-still",
    "task_003_1_1080p.mp4": "v_D1_foil-macro",
}

BAK.mkdir(parents=True, exist_ok=True)
for src_name, dst_stem in MAP.items():
    s = SRC / src_name
    if not s.exists():
        print("🔴 thieu nguon:", s)
        sys.exit(1)
    dst = VD / "clips" / f"{dst_stem}.mp4"
    if dst.exists():                       # giu ban cu de con so sanh / hoan tac
        b = BAK / f"{dst_stem}.mp4"
        if not b.exists():
            shutil.copy(dst, b)
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(s),
                        "-vf", "fps=30", "-an", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "18", "-pix_fmt", "yuv420p", str(dst)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("🔴 ffmpeg FAIL", dst_stem, r.stderr[-300:])
        sys.exit(1)
    shutil.copy(dst, PUB / f"{dst_stem}.mp4")
    print("✅ %-30s <- %s  (%.1f MB)" % (dst_stem, src_name, dst.stat().st_size / 1048576))

print("\nban cu luu o:", BAK)
print("tiep: python tools\\build_remotion_28.py  roi  python tools\\render_chunks28.py --only 0,3")
