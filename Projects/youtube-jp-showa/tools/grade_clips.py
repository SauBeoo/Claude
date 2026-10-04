# -*- coding: utf-8 -*-
"""grade_clips.py — hau ky cho clip AI: GIAM TRANG CHAY + TANG NET. Khong gia lap chat phim.

user 2026-09-11: "May co the bo hat di nhe. Do net tang len, y tao la phong cach video.
Chu khong phai nhung chi so do. cai trang chay thi giam di oke"

⛔ BAN DAU tao lam nham: dung bo loc gia lap 16mm (hat + lam mem + gate weave + halation)
   de "keo AI ve giong phim that" theo SO DO. Sai huong — cai user muon giong la PHONG CACH
   QUAY (may quan sat, canh nhieu lop, nguoi khong dien), thu do nam o PROMPT
   (videogen_lib STYLE/MOTION), khong nam o hau ky. Hau ky chi con 2 viec:

   1) HIGHLIGHT ROLLOFF — do duoc: canh AI ngoai troi co **9,0%** pixel > 240 (chay trang),
      phim that 0,0%. Chay trang la mat han chi tiet, khong cuu duoc o khau nao khac.
   2) TANG NET — user muon net hon, nguoc voi huong gia-lap-phim.

Do lai bang tools/measure_filmlook.py sau khi chay.

Usage:
  python tools/grade_clips.py <in.mp4> <out.mp4>
  python tools/grade_clips.py --dir <folder> --outdir <folder>
"""
import argparse, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# curves: keo diem trang 1.0 -> 0.88 nhung GIU trung gian (0.5/0.5) de anh khong bi xam.
# unsharp 5x5 amount 0.8 = net ro nhung chua tao quang vien (>1.2 la bat dau vien trang).
VF = ("curves=all='0/0 0.5/0.5 0.85/0.83 1/0.88',"
      "unsharp=5:5:0.80:5:5:0.0,"
      "scale=1920:1080:flags=lanczos")

def run(src, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", VF, "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", dst, "-y"], check=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?"); ap.add_argument("dst", nargs="?")
    ap.add_argument("--dir"); ap.add_argument("--outdir")
    a = ap.parse_args()
    if a.dir:
        os.makedirs(a.outdir, exist_ok=True)
        fs = sorted(f for f in os.listdir(a.dir) if f.endswith(".mp4"))
        for i, f in enumerate(fs, 1):
            run(os.path.join(a.dir, f), os.path.join(a.outdir, f))
            print(f"  [{i}/{len(fs)}] {f}")
        print(f"xong {len(fs)} clip -> {a.outdir}")
    else:
        run(a.src, a.dst); print("->", a.dst)
