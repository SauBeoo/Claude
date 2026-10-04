# -*- coding: utf-8 -*-
r"""render_remotion_chunks.py — render project Remotion kinishinai theo CHUNK (khuon youtube-jp-nenkin/tools/render_chunks26.py).

Vi sao chunk: render mot mach demo 3450 frame -> browser/compositor SAP o frame 969 = het RAM
(render-background.md §2.6 ⑩). Remotion KHONG co resume.
- chunk ngan (mac dinh 500 frame) · --concurrency=1 · tran cache 256 MB (offthread + media)
- don remotion.exe + chrome-headless-shell.exe MO COI truoc moi chunk (khong dung node/chrome/ffmpeg)
- resume: chunk bo qua CHI KHI moi hon project.json VA ban bundle (render-background.md §2.5)
- ⚡ BUNDLE MOT LAN (2026-10-02): ban cu de moi chunk tu bundle + chep public -> 1-2 phut thua x 8 chunk.
  Gio `remotion bundle` 1 lan ra out/<name>_bundle, chi bundle lai khi src/ hoac public gon MOI hon ban bundle.
- 🔴 LOG DAY DU tung chunk (out/<name>_chunks/cNN.log) — ban cu `--log=error` lam chunk 0 "loi im lang" 2 lan.
  Chunk loi -> don mo coi -> THU LAI 1 lan -> van loi thi dung, in 20 dong cuoi log.
- --preview: --scale=0.5 (540p; 0,6667 ra 720,036 khong nguyen) de duyet nhanh nhip/chuyen dong; ban giao luon 1080p.
- noi: HINH concat + danh so lai frame (setpts=N/fps) + gan LAI assets/audio.wav (concat -c copy lech 0,35s).
    python tools\render_remotion_chunks.py kinishinai-01yawa --public-dir public_k01yawa --out <file.mp4> [--preview]
"""
import argparse, io, json, subprocess, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
RV = Path(r"E:\Claude\Projects\remotion-vox")
NPX = "npx.cmd"


def kill_orphans():
    for exe in ("remotion.exe", "chrome-headless-shell.exe"):
        subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)


def newest(*roots):
    m = 0.0
    for r in roots:
        for p in Path(r).rglob("*"):
            if p.is_file():
                m = max(m, p.stat().st_mtime)
    return m


def ensure_bundle(name, public_dir):
    out = RV / "out" / f"{name}_bundle"
    stamp = out / "index.html"
    src_m = newest(RV / "src", RV / public_dir)
    if stamp.exists() and stamp.stat().st_mtime > src_m:
        print("bundle con moi, dung lai:", out); return out
    print("bundle 1 lan ->", out)
    log = RV / "out" / f"{name}_bundle.log"
    with open(log, "w", encoding="utf-8") as lf:
        r = subprocess.run([NPX, "remotion", "bundle", f"--public-dir={public_dir}", f"--out-dir={out}"],
                           cwd=RV, stdout=lf, stderr=subprocess.STDOUT)
    if r.returncode or not stamp.exists():
        print(f"🔴 bundle LOI (exit {r.returncode}) — xem {log}"); sys.exit(1)
    return out


def render_chunk(bundle, name, o, f0, f1, conc, scale):
    log = o.with_suffix(".log")
    cmd = [NPX, "remotion", "render", str(bundle), "VoxProject", f"--props=projects/{name}/project.json", str(o),
           f"--frames={f0}-{f1}", f"--concurrency={conc}", "--offthreadvideo-cache-size-in-bytes=268435456",
           "--media-cache-size-in-bytes=268435456"] + ([f"--scale={scale}"] if scale else [])
    for attempt in (1, 2):
        kill_orphans()
        with open(log, "w", encoding="utf-8") as lf:
            r = subprocess.run(cmd, cwd=RV, stdout=lf, stderr=subprocess.STDOUT)
        if r.returncode == 0 and o.exists():
            return True
        print(f"   lan {attempt} loi (exit {r.returncode})" + (" — thu lai" if attempt == 1 else ""))
    tail = log.read_text(encoding="utf-8", errors="replace").splitlines()[-20:]
    print("\n".join("   | " + t for t in tail))
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name"); ap.add_argument("--public-dir", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--chunk", type=int, default=500); ap.add_argument("--conc", type=int, default=3)   # do 2026-10-02: 1 luong chi an ~7,5% CPU (cho tuan tu), RAM du cho 3
    ap.add_argument("--preview", action="store_true", help="540p (--scale=0.5) de duyet nhanh")
    a = ap.parse_args()
    props = RV / "projects" / a.name / "project.json"
    pj = json.loads(props.read_text(encoding="utf-8"))
    total, fps = pj["timeline"]["durationInFrames"], pj["meta"]["fps"]
    scale = 0.5 if a.preview else None      # 0,6667 x 1080 = 720,036 -> Remotion tu choi (phai so nguyen)
    bundle = ensure_bundle(a.name, a.public_dir)
    od = RV / "out" / f"{a.name}_chunks{'_720' if a.preview else ''}"; od.mkdir(parents=True, exist_ok=True)
    gate = max(props.stat().st_mtime, (bundle / "index.html").stat().st_mtime)
    parts = []
    for k, f0 in enumerate(range(0, total, a.chunk)):
        f1 = min(f0 + a.chunk, total) - 1
        o = od / f"c{k:02d}.mp4"; parts.append(o)
        if o.exists() and o.stat().st_mtime > gate:
            print(f"chunk {k:02d} {f0}-{f1} co roi, bo qua"); continue
        print(f"chunk {k:02d} {f0}-{f1} ...")
        if not render_chunk(bundle, a.name, o, f0, f1, a.conc, scale):
            print(f"🔴 chunk {k:02d} LOI 2 lan — log: {o.with_suffix('.log')}"); return 1
    kill_orphans()
    lst = od / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    aud = RV / a.public_dir / "projects" / a.name / "assets" / "audio.wav"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(aud),
                        "-map", "0:v", "-map", "1:a", "-vf", f"setpts=N/{fps}/TB", "-r", str(fps), "-c:v", "libx264",
                        "-crf", "17", "-preset", "fast", "-c:a", "aac", "-b:a", "192k",
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.84:level=disabled", "-ar", "48000",
                        "-t", f"{total / fps:.3f}", "-movflags", "+faststart", a.out])
    print("OK ->", a.out if r.returncode == 0 else f"LOI noi {r.returncode}")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
