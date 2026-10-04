# -*- coding: utf-8 -*-
r"""render19real_parts.py — render video 19 REAL theo DOAN + RESUME, roi ghep.

🔴 VI SAO KHONG RENDER MOT MACH: may nay hay kill tien trinh dai (CLAUDE.md ghi
   san: *"May hay tu kill tien trinh dai -> co che resume tung chunk"*), va
   Remotion **khong co resume**. Da mat 2 luot:
     · luot 1: chet that o frame 2765 (CSS blur -> Chrome treo) — da sua
     · luot 2: bi KILL tu ngoai o frame 8000/26974 (~30%), khong EXITCODE,
               khong ra file. Mat ~35 phut.
   Chia thanh doan ~4500 frame (150s): moi doan ~18 phut, bi kill thi mat 1 doan,
   va lan chay sau TU BO QUA doan da xong.

⚠️ RESUME DUNG CACH (`render-background.md` §2.5): bo qua doan chi khi file da co
   **VA moi hon project.json** — khong chi `exists()`. Doi project roi chay lai
   thi cac doan cu tu dung lai.

GHEP: ffmpeg concat demuxer `-c copy` (khong re-encode, khong mat chat).
   Moi doan cung codec/GOP nen concat sach.

CHAY:  python tools/render19vox_parts.py            # render + ghep
       python tools/render19vox_parts.py --concat   # chi ghep (doan da du)
"""
import io
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

RV = os.path.join("E:" + os.sep, "Claude", "Projects", "remotion-vox")
NAME = "nenkin-19real"
PJ = os.path.join(RV, "projects", NAME, "project.json")
OUT = os.path.join(RV, "out", "n19real")
PARTS = os.path.join(OUT, "parts")
FINAL = os.path.join(OUT, "nenkin-19real.mp4")
STEP = 4500          # frame moi doan (~150s @30fps)


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          errors="replace")


def main():
    os.makedirs(PARTS, exist_ok=True)
    dur = json.load(io.open(PJ, encoding="utf-8"))["timeline"]["durationInFrames"]
    pj_mtime = os.path.getmtime(PJ)
    segs = [(a, min(a + STEP - 1, dur - 1)) for a in range(0, dur, STEP)]
    print(f"tong {dur} frame -> {len(segs)} doan x {STEP} frame (~{STEP/30:.0f}s)")

    if "--concat" not in sys.argv:
        for i, (a, b) in enumerate(segs):
            p = os.path.join(PARTS, f"p{i:02d}.mp4")
            if os.path.exists(p) and os.path.getmtime(p) >= pj_mtime:
                print(f"  [{i+1}/{len(segs)}] doan {a}-{b}: SKIP (da co, moi hon project)")
                continue
            print(f"  [{i+1}/{len(segs)}] doan {a}-{b} ...", end="", flush=True)
            t0 = time.time()
            r = run(["cmd", "/c", "npx", "remotion", "render", "VoxProject",
                     f"--props=projects/{NAME}/project.json",
                     "--public-dir=public_n19r", f"--frames={a}-{b}",
                     "--crf=18", "--concurrency=4", p], cwd=RV)
            if r.returncode or not os.path.exists(p):
                print(f" 🔴 LOI (exit {r.returncode})")
                print((r.stdout or "")[-800:])
                print((r.stderr or "")[-800:])
                sys.exit(1)
            print(f" xong {time.time()-t0:.0f}s")

    # ── ghep ──────────────────────────────────────────────────────────────
    missing = [i for i in range(len(segs))
               if not os.path.exists(os.path.join(PARTS, f"p{i:02d}.mp4"))]
    if missing:
        print(f"🔴 thieu doan: {missing}")
        sys.exit(1)
    lst = os.path.join(PARTS, "list.txt")
    io.open(lst, "w", encoding="utf-8", newline="\n").write(
        "".join(f"file 'p{i:02d}.mp4'\n" for i in range(len(segs))))
    print("ghep bang concat -c copy ...", end="", flush=True)
    r = run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
             "-i", "list.txt", "-c", "copy", FINAL], cwd=PARTS)
    if r.returncode:
        print(" 🔴 LOI concat"); print((r.stderr or "")[:600]); sys.exit(1)
    d = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", FINAL]).stdout.strip()
    print(f" xong\nOK  {FINAL}\n    duration {d}s (can {dur/30:.3f}s)")


if __name__ == "__main__":
    main()
