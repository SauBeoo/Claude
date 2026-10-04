# -*- coding: utf-8 -*-
r"""probe25.py — render MOT chunk cua nenkin-25 va DO RAM trong luc chay.

VI SAO CAN: `render_chunks25.py` bi harness KILL "low memory" **hai lan, o ngay chunk dau**,
ca khi da ha xuong `--conc 1` + chunk 1600 frame. Hai bien do la hai duong chua duoc ghi
san trong `render-background.md` §2.6 ⑨, va ca hai deu KHONG an => gia thuyet sai, phai do.

Doi chung da co: **14 luot `remotion still` chay sach** tren cung project, cung `public/`
4,2 GB => khau bundle/nap asset KHONG phai thu pham.

Doc ket qua:
  · RAM leo DEU roi vo            -> ro bo nho luc encode; ha conc khong cuu, phai chia nho hon
  · RAM nhay VOT mot phat luc dau -> nap asset; duong chua la don bot `public/projects/`
  · RAM dung yen ma van bi kill   -> nguong cua harness, khong phai cua may

CHAY:  python tools/probe25.py [--frames 0-199]
"""
import argparse
import os
import subprocess
import sys
import threading
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RV = r"E:\Claude\Projects\remotion-vox"
VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\25_nenkin-tenbiki-tetori-6man2sen")
NAMES = ("chrome-headless-shell.exe", "node.exe", "ffmpeg.exe")


def sample():
    """(RAM trong MB, RAM cua tien trinh render MB) — chi dung tool co san cua Windows."""
    free = -1
    try:
        out = subprocess.run(["wmic", "OS", "get", "FreePhysicalMemory", "/value"],
                             capture_output=True, text=True, timeout=10).stdout
        for ln in out.splitlines():
            if "=" in ln:
                free = int(ln.split("=")[1].strip()) // 1024
    except Exception:
        pass
    tot = 0
    for n in NAMES:
        try:
            out = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {n}", "/FO", "CSV",
                                  "/NH"], capture_output=True, text=True, timeout=10).stdout
            for ln in out.splitlines():
                p = ln.strip().strip('"').split('","')
                if len(p) >= 5 and p[0].lower() == n:
                    tot += int(p[4].replace(",", "").replace(" K", "").strip()) // 1024
        except Exception:
            pass
    return free, tot


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="0-199")
    ap.add_argument("--conc", type=int, default=1)
    ap.add_argument("--extra", default="", help="co them cho remotion, cach nhau bang dau cach")
    a = ap.parse_args()

    log = os.path.join(VD, "mem.log")
    stop = threading.Event()
    rows = []

    def loop():
        while not stop.is_set():
            fr, tt = sample()
            rows.append((time.strftime("%H:%M:%S"), fr, tt))
            with open(log, "w", encoding="ascii") as f:
                for t, x, y in rows:
                    f.write(f"{t} free={x}MB render={y}MB\n")
            stop.wait(5)

    th = threading.Thread(target=loop, daemon=True)
    th.start()
    print(f"render frames {a.frames} (conc={a.conc}) — do RAM moi 5s -> {log}")
    t0 = time.time()
    r = subprocess.run(
        ["npx.cmd", "remotion", "render", "VoxProject",
         "--props=projects/nenkin-25/project.json", f"--frames={a.frames}",
         f"--concurrency={a.conc}", *[x for x in a.extra.split(" ") if x],
         os.path.join(RV, "out", "n25chunks", "probe.mp4")],
        cwd=RV, capture_output=True, text=True, encoding="utf-8", errors="replace")
    stop.set()
    th.join(timeout=8)
    dt = time.time() - t0
    print(f"rc={r.returncode} · {dt:.0f}s")
    if r.returncode:
        print((r.stderr or r.stdout or "")[-1200:])
    if rows:
        fr = [x for _t, x, _y in rows if x > 0]
        rn = [y for _t, _x, y in rows]
        print(f"RAM trong: dau {fr[0] if fr else '?'}MB · min {min(fr) if fr else '?'}MB · "
              f"cuoi {fr[-1] if fr else '?'}MB")
        print(f"RAM render: max {max(rn)}MB · cuoi {rn[-1]}MB · {len(rows)} mau")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
