# -*- coding: utf-8 -*-
r"""Render video 28 theo CHUNK — chong mat tien do khi bi kill.

VI SAO: render mot mach 33.537 frame bi kill HAI lan (frame 11.180 va 1.061), khong
EXITCODE, khong traceback, RAM con 10GB => khong phai loi noi dung, cung khong phai
OOM. Remotion KHONG co resume, nen moi lan kill la mat sach. Chia chunk thi mat toi
da MOT chunk.

⚠️ concurrency=4 da thu va CHAM HON 2 (uoc 1h22 vs 1h09) — 4 worker tranh CPU/IO tren
   may 6 nhan. Giu 2.

🔴 RESUME dung luat `render-background.md` §2.5: chunk duoc BO QUA chi khi no MOI HON
   project.json — khong phai "co file thi bo qua". Doi noi dung roi render lai ma van
   ra hang cu la bay da dinh 6 lan trong workspace.

    python tools\render_chunks28.py            # render + noi
    python tools\render_chunks28.py --check     # chi in trang thai
"""
import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True, write_through=True)

RV = Path(r"E:\Claude\Projects\remotion-vox")
NAME = "co-dai-28"
PROPS = f"projects/{NAME}/project.json"
OUTDIR = RV / "out" / "c28chunks"
FINAL = RV / "out" / "co-dai-28.mp4"
CHUNK = 3000          # ~100s video / chunk -> ~8 phut render


def chunks(total):
    out, a = [], 0
    while a < total:
        b = min(a + CHUNK - 1, total - 1)
        out.append((a, b))
        a = b + 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    # ⭐ --only 0,3  : chi render lai CAC CHUNK CHI DINH roi noi lai.
    #    Dung khi chi doi MOT vai clip (vd thay clip dau) — cac chunk khac van dung,
    #    render lai het 12 chunk la phi ~90 phut. Day chinh la loi cua viec chia chunk.
    #    ⚠️ Chi dung khi CHAC thay doi nam gon trong cac chunk do. Doi hang so toan
    #    cuc (FADE, SPEED_MIN, layout bang) thi KHONG duoc dung — phai render lai het.
    ap.add_argument("--only", default="", help="vd: 0 hoac 0,5,11")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x.strip()} if a.only else None

    pj = RV / "projects" / NAME / "project.json"
    total = json.loads(pj.read_text(encoding="utf-8"))["timeline"]["durationInFrames"]
    pj_m = pj.stat().st_mtime
    OUTDIR.mkdir(parents=True, exist_ok=True)
    cs = chunks(total)
    print("tong %d frame -> %d chunk x %d" % (total, len(cs), CHUNK))

    done = []
    for k, (f0, f1) in enumerate(cs):
        o = OUTDIR / f"c{k:02d}.mp4"
        fresh = o.exists() and o.stat().st_mtime >= pj_m
        if only is not None:                    # che do chi render chunk chi dinh
            fresh = o.exists() and k not in only
        if a.check:
            print("  c%02d  %6d-%-6d  %s" % (k, f0, f1,
                                             "OK" if fresh else
                                             ("CU HON project.json -> render lai" if o.exists() else "chua co")))
            if fresh:
                done.append(o)
            continue
        if fresh:
            print("[%2d/%d] c%02d da co va moi hon project.json -> bo qua" % (k + 1, len(cs), k))
            done.append(o)
            continue
        print("[%2d/%d] c%02d  frame %d-%d ..." % (k + 1, len(cs), k, f0, f1))
        r = subprocess.run(
            ["npx.cmd", "remotion", "render", "VoxProject", f"--props={PROPS}",
             f"--frames={f0}-{f1}", "--concurrency=2", str(o)],
            cwd=str(RV), capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0 or not o.exists():
            print("🔴 CHUNK %d FAIL (rc=%s)" % (k, r.returncode))
            print((r.stderr or r.stdout or "")[-800:])
            sys.exit(1)
        done.append(o)

    if a.check:
        print("san sang noi: %d/%d chunk" % (len(done), len(cs)))
        return

    lst = OUTDIR / "list.txt"
    lst.write_text("".join("file '%s'\n" % p.as_posix() for p in done), encoding="utf-8")
    print("noi %d chunk -> %s" % (len(done), FINAL.name))
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-c", "copy", str(FINAL)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("🔴 CONCAT FAIL:", r.stderr[-600:])
        sys.exit(1)
    j = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", str(FINAL)],
        capture_output=True, text=True).stdout)
    d = float(j["format"]["duration"])
    print("XONG: %.2fs = %d:%02d | %.1f MB" % (d, int(d) // 60, int(d) % 60,
                                               FINAL.stat().st_size / 1048576))
    exp = total / 30
    if abs(d - exp) > 1.0:
        print("🔴 duration lech %.2fs so voi project (%.2fs)" % (d - exp, exp))
        sys.exit(1)
    print("✅ duration khop project.json")


if __name__ == "__main__":
    main()
