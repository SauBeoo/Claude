# -*- coding: utf-8 -*-
r"""Render mot project remotion-vox THEO KHOI roi noi lai.

Vi sao: may nay 6 luong / 24GB, render mot mach 34.215 frame thi compositor phinh
cache video off-thread roi CHET giua duong:
    Compositor exited with code 3221226505: memory allocation of 6220800 bytes failed
(6.220.800 byte = dung MOT frame RGB 1920x1080 — tuc khong xin noi 1 frame).
Da dinh that 2026-08-16 o frame 10.285/34.215 (30%).

Chia khoi = moi khoi MOT tien trinh rieng => RAM duoc tra ve giua cac khoi, va khoi
nao chet thi chi chay lai khoi do. Cung cach ma pipeline co-dai/health da giai bai
toan y het (CHUNK=4 + finalize.py, xem memory project_co_dai_health_render_resume).

    python tools\render_chunks.py --project codai-20-sentei --chunk 5000

Khoi da co file va DU frame thi BO QUA (resume). ⚠️ Kiem bang SO FRAME THAT (ffprobe),
khong phai "file co ton tai khong" — luat render-background.md §2.5.
"""
import argparse, io, json, os, subprocess, sys, time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)
ROOT = Path(__file__).resolve().parent.parent


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), cwd=str(ROOT), **kw)


def nframes(p: Path):
    if not p.exists():
        return -1
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-count_frames", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    # 🔴 ffprobe -of csv=p=0 tra ve "5000," — CO DAU PHAY DUOI. int("5000,") nem
    #    ValueError => ham tra -1 => khoi render THANH CONG bi cham la hong (dinh that
    #    2026-08-17: khoi 0 co du 182MB/5000 frame ma van bao [LOI] frame=-1/5000).
    txt = r.stdout.strip().strip(",").split(",")[0].strip()
    try:
        return int(txt)
    except ValueError:
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--chunk", type=int, default=5000)
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--cache-mb", type=int, default=512,
                    help="tran cache video off-thread — chinh cho nay la cho da no")
    a = ap.parse_args()

    props = ROOT / "projects" / a.project / "project.json"
    total = json.loads(props.read_text(encoding="utf-8"))["timeline"]["durationInFrames"]
    outdir = ROOT / "out" / f"_chunks_{a.project}"
    outdir.mkdir(parents=True, exist_ok=True)

    spans = [(s, min(s + a.chunk, total) - 1) for s in range(0, total, a.chunk)]
    print(f"tong {total} frame · {len(spans)} khoi · concurrency {a.concurrency} · "
          f"cache {a.cache_mb}MB")

    parts = []
    for k, (s, e) in enumerate(spans):
        f = outdir / f"part_{k:02d}.mp4"
        parts.append(f)
        want = e - s + 1
        have = nframes(f)
        # render-background.md §2.5: khoi CU HON project.json = hang hong, du frame cung render lai
        if have == want and f.stat().st_mtime < props.stat().st_mtime:
            print(f"[{k+1}/{len(spans)}] {s}-{e}: CU HON project.json -> render lai")
            have = 0
        if have == want:
            print(f"[{k+1}/{len(spans)}] {s}-{e}: da co du {have} frame — bo qua")
            continue
        if have > 0:
            print(f"[{k+1}/{len(spans)}] {s}-{e}: co {have}/{want} frame — DUNG, render lai")
        t0 = time.time()
        # ⚠️ KHONG taskkill theo ten tien trinh o day: may co the co phien khac dang render
        #    Remotion (2026-10-01 dung do kinishinai) — giet theo ten la giet luon render cua ho.
        cmd = ["npx.cmd", "remotion", "render", "VoxProject",
               f"--props={props}", str(f),
               f"--frames={s}-{e}",
               f"--concurrency={a.concurrency}",
               f"--offthreadvideo-cache-size-in-bytes={a.cache_mb*1024*1024}",
               f"--media-cache-size-in-bytes={a.cache_mb*1024*1024}",
               "--overwrite", "--log=error"]
        r = sh(cmd)
        got = nframes(f)
        if r.returncode != 0 or got != want:
            print(f"[LOI] khoi {k} exit={r.returncode} frame={got}/{want}")
            return 1
        print(f"[{k+1}/{len(spans)}] {s}-{e}: OK {got} frame · {time.time()-t0:.0f}s")

    lst = outdir / "concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    final = ROOT / "out" / f"{a.project}.mp4"
    print("noi khoi ->", final)
    r = sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
            "-i", str(lst), "-c", "copy", str(final)])
    if r.returncode != 0:
        print("[LOI] concat that bai")
        return 1
    got = nframes(final)
    print(f"XONG: {final} · {got}/{total} frame")
    return 0 if got == total else 1


if __name__ == "__main__":
    sys.exit(main())
