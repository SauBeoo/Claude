# -*- coding: utf-8 -*-
r"""ingest_c26.py — nhận lô 61 clip t2v của video 26 vào `clips/clip_<key>.mp4`.

MAP: lô này được bơm bằng ĐÚNG `vox26_FLOW.txt` theo thứ tự, nên `task_NNN` = dòng NNN.
🔴 KHÔNG tin thứ tự một cách mù quáng — bài học 13 của video 22: *"t2v KHÔNG CÓ ĐÁP ÁN
   ĐÚNG cho phép map clip→khe, máy sai 2/2 lần"*. Ở đây thứ tự đúng vì user bơm cả file
   một lượt và Flow trả về đúng số lượng (61 = 61), và đã SOI MẮT 4 mốc (dòng 1·25·40·61)
   khớp nội dung khe. Lô sau thứ tự khác ⇒ phải soi lại, đừng đổi tên mù.

🔴 GATE ĐẾM: số clip vào phải BẰNG số dòng TENFILE. Thiếu/thừa ⇒ dừng, không đổi tên gì.

Nguồn 1280×720 @24fps 8,000s → scale **1920×1080** (1,50×), giữ 24fps (ép 30 là 27% frame
lặp = judder — `feedback_fps_clip_phai_khop_renderer`). Lô t2v KHÔNG có ✦ (đã soi), nhưng
vẫn phải soi lại mỗi lô: `media-library.md` §2.10 ⑤.

RESUME theo **mtime**: clip đích cũ hơn clip nguồn thì dựng lại (`render-background.md` §2.5).

CHẠY:  python tools/ingest_c26.py --src "F:\Youtube\..." [--force]
"""
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\26_kaigo-hokenryo-dankai-setai")
DST = os.path.join(VD, "clips")
SRC_DEF = r"F:\Youtube\Dự_án_mới_4_3wpyxc8d"


def main() -> int:
    src = SRC_DEF
    if "--src" in sys.argv:
        src = sys.argv[sys.argv.index("--src") + 1]
    force = "--force" in sys.argv

    ten = [l.rstrip("\n") for l in io.open(os.path.join(VD, "vox26_TENFILE.txt"),
                                           encoding="utf-8") if l.strip()]
    keys = [re.search(r"clips/clip_([0-9a-z]+)\.mp4", t).group(1) for t in ten]
    vids = sorted(f for f in os.listdir(src) if f.lower().endswith(".mp4"))

    if len(vids) != len(keys):
        print(f"🔴 GATE ĐẾM: {len(vids)} clip nguồn ≠ {len(keys)} dòng TENFILE — "
              f"DỪNG, không đổi tên gì. Soi lại lô trước khi chạy tiếp.")
        return 1

    os.makedirs(DST, exist_ok=True)
    done = skip = 0
    for k, f in zip(keys, vids):
        s = os.path.join(src, f)
        d = os.path.join(DST, f"clip_{k}.mp4")
        if not force and os.path.exists(d) and os.path.getmtime(d) >= os.path.getmtime(s):
            skip += 1
            continue
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", s,
             "-vf", "scale=1920:1080:flags=lanczos", "-r", "24",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
             "-pix_fmt", "yuv420p", "-an", d],
            capture_output=True, text=True)
        if r.returncode:
            print(f"🔴 ffmpeg lỗi ở {f}: {r.stderr[:200]}")
            return 1
        done += 1
        print(f"  {f}  ->  clip_{k}.mp4")
    print(f"\n✓ {done} dựng mới · {skip} bỏ qua (đã mới hơn nguồn) -> {DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
