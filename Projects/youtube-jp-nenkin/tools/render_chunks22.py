# -*- coding: utf-8 -*-
r"""render_chunks22.py — render video 22 (`nenkin-22full`) theo CHUNK + loudnorm -14 LUFS.

VI SAO CHIA CHUNK: render mot mach 19.881 frame bi **harness KILL o frame 15.306 (77%)**
vi may het RAM — `RENDER_EXIT=1`, khong co file nao. Remotion **KHONG co resume**, nen mot
mach bi kill la mat sach 44 phut. Chia chunk thi mat toi da MOT chunk (~10 phut).
📌 Cung bai hoc da ghi cho co-dai 28 (`tools/render_chunks28.py`) va cho pipeline cu
   (`project_co_dai_health_render_resume`): may nay tu kill tien trinh dai, phai co resume.

⚠️ concurrency=2, KHONG 4: ban 4 vua bi kill vi RAM. O co-dai do duoc 2 con **nhanh hon** 4
   tren may 6 nhan (4 worker tranh CPU/IO).

🔴 RESUME dung luat `render-background.md` §2.5: chunk duoc BO QUA **chi khi no MOI HON
   project.json** — khong phai "co file thi bo qua". Doi noi dung roi render lai ma van ra
   hang cu la bay da dinh 6 lan trong workspace.

🔴 fps = **24** (khong phai 30 nhu ban co-dai): clip Veo la 24fps. Phep kiem duration cuoi
   chia cho 24 — bê hang so 30 sang la bao lech 20%.

⛔ KHONG chay `cta_inject` — duong Remotion lam mat lop anh (`render-background.md` §2.6 ⑧).

    python tools\render_chunks22.py             # render + noi + loudnorm
    python tools\render_chunks22.py --check     # chi in trang thai
    python tools\render_chunks22.py --only 3,7  # render lai vai chunk roi noi lai
"""
import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

pj = None            # gan trong main(), asset_mtimes() doc lai

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True, write_through=True)

RV = Path(r"E:\Claude\Projects\remotion-vox")
NAME = "nenkin-22full"
PROPS = f"projects/{NAME}/project.json"
OUTDIR = RV / "out" / "n22chunks"
RAW = RV / "out" / "n22full" / "raw.mp4"
FINAL = RV / "out" / "n22full" / "final.mp4"
FPS = 24
CHUNK = 2400          # 100s video / chunk -> ~10 phut render

# -14 LUFS chuan kenh (`project_loudness_14_lufs`): nen truoc roi loudnorm
AF = ("acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=2,"
      "loudnorm=I=-14:TP=-1.5:LRA=9")


def asset_mtimes(pj_data):
    """(mtime toan cuc, [(f0, f1, mtime)]) — de resume so theo TUNG CHUNK.

    🔴🔴 VI SAO KHONG CHI SO VOI `project.json`: doi CLIP ma khong doi project.json thi
       mtime cua project.json **khong nhich**, nen chunk cu duoc coi la "moi hon" va bi BO
       QUA => render lai ma van ra HANG CU. Day dung la bay `render-background.md` §2.5, chi
       o mot tang moi: bay cu la "co file thi bo qua", bay nay la "moi hon project.json thi
       bo qua". Ca hai deu hoi SAI CAU.
       Da suyt dinh that: lo GEN LAI vong 2 thay 10 clip ma project.json khong doi mot byte.
    ⇒ Chunk chi duoc bo qua khi no moi hon **CA project.json LAN moi asset xuat hien trong
      dung khoang frame cua chunk do**. Nho vay doi 3 clip thi chi 1-2 chunk phai render lai,
      khong phai ca 9 (=90 phut).
    """
    root = RV / "public" / "projects" / NAME
    glob_m = pj.stat().st_mtime
    # asset dan CUNG len moi frame (logo · mascot · voice) => vao mtime TOAN CUC
    for rel in ("assets/brand_logo.png", "assets/voice.wav"):
        f = root / rel
        if f.exists():
            glob_m = max(glob_m, f.stat().st_mtime)
    for d in (root / "assets").glob("*/"):
        if d.is_dir():
            for f in d.iterdir():
                glob_m = max(glob_m, f.stat().st_mtime)
    spans = []
    for tr in pj_data.get("tracks", []):
        for c in tr.get("clips", []):
            a = c.get("asset")
            if not a:
                continue
            f = root / a
            if not f.exists():
                continue
            spans.append((c["from"], c["from"] + c["durationInFrames"], f.stat().st_mtime))
    return glob_m, spans


def need_m(f0, f1, glob_m, spans):
    """mtime toi thieu ma chunk [f0,f1] phai co de duoc coi la con moi."""
    m = glob_m
    for a, b, t in spans:
        if a < f1 + 1 and b > f0:                 # giao nhau voi khoang chunk
            m = max(m, t)
    return m


# 🔴 CHUNK bi kill LAP LAI thi che nho HON, dung o day — dung doi `CHUNK` (doi la ca luoi
#    chunk lech, 8 chunk da render thanh vo dung). `c08` chet 3 lan (frame 495/681 · 375/681
#    · ngay dau o conc=1) trong khi c00-c07 (2400 frame, conc=2) qua het => khong phai do
#    do dai chunk, ma do may dang thieu RAM ngay luc do (Chrome cua user giu 8,5/23,9 GB).
#    Che nho lam moi lan render ngan hon, giam kha nang trung voi mot cu spike.
SPLIT = {8: 3}


def chunks(total):
    """[(f0, f1, ten)] — ten de dat file, co the la 'c08a' khi chunk bi che nho."""
    out, a, k = [], 0, 0
    while a < total:
        b = min(a + CHUNK - 1, total - 1)
        n = SPLIT.get(k, 1)
        if n == 1:
            out.append((a, b, "c%02d" % k))
        else:
            span = b - a + 1
            step = -(-span // n)                     # ceil
            x = a
            for j in range(n):
                y = min(x + step - 1, b)
                out.append((x, y, "c%02d%s" % (k, "abcdefgh"[j])))
                x = y + 1
                if x > b:
                    break
        a = b + 1
        k += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", default="", help="vd: 3 hoac 3,7")
    # 🔴 May nay bi harness KILL vi het RAM o ca concurrency=2 (chunk c08 chet 2 lan o
    #    frame 375-495/681). --conc 1 la duong lui: cham hon ~40% nhung mot worker Chrome
    #    it RAM hon han. Dung khi mot chunk chet lap lai.
    ap.add_argument("--conc", type=int, default=2, help="concurrency cua remotion (mac dinh 2)")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x.strip()} if a.only else None

    global pj
    pj = RV / "projects" / NAME / "project.json"
    pj_data = json.loads(pj.read_text(encoding="utf-8"))
    total = pj_data["timeline"]["durationInFrames"]
    glob_m, spans = asset_mtimes(pj_data)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    cs = chunks(total)
    print("tong %d frame (%.1fs @ %dfps) -> %d mieng (chunk %d, SPLIT %s)"
          % (total, total / FPS, FPS, len(cs), CHUNK, SPLIT or "khong"))

    done = []
    for k, (f0, f1, name) in enumerate(cs):
        o = OUTDIR / f"{name}.mp4"
        nm = need_m(f0, f1, glob_m, spans)
        fresh = o.exists() and o.stat().st_mtime >= nm
        if only is not None:
            fresh = o.exists() and k not in only
        if a.check:
            st = "OK" if fresh else ("CU HON asset/project -> render lai" if o.exists()
                                     else "chua co")
            print("  %-5s %6d-%-6d  %s" % (name, f0, f1, st))
            if fresh:
                done.append(o)
            continue
        if fresh:
            print("[%2d/%d] %s da co va moi hon moi asset trong khoang -> bo qua"
                  % (k + 1, len(cs), name))
            done.append(o)
            continue
        print("[%2d/%d] %s  frame %d-%d  (conc=%d) ..."
              % (k + 1, len(cs), name, f0, f1, a.conc))
        r = subprocess.run(
            ["npx.cmd", "remotion", "render", "VoxProject", f"--props={PROPS}",
             f"--frames={f0}-{f1}", f"--concurrency={a.conc}", str(o)],
            cwd=str(RV), capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0 or not o.exists():
            print("GATE DO: %s FAIL (rc=%s)" % (name, r.returncode))
            print((r.stderr or r.stdout or "")[-900:])
            return 1
        done.append(o)

    if a.check:
        print("san sang noi: %d/%d mieng" % (len(done), len(cs)))
        return 0

    lst = OUTDIR / "list.txt"
    lst.write_text("".join("file '%s'\n" % p.as_posix() for p in done), encoding="utf-8")
    print("noi %d mieng -> raw.mp4" % len(done))
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-c", "copy", str(RAW)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("GATE DO: CONCAT FAIL:", (r.stderr or "")[-700:])
        return 1

    print("loudnorm -14 LUFS -> final.mp4")
    # 🔴 PHAI ep `-ar 48000`: `loudnorm` resample noi bo len 192 kHz, va neu khong chi dinh
    #    thi encoder aac chon **96 kHz** — do duoc tren ban dau. 96k la hop le nhung phi
    #    (nguon voice.wav chi 24 kHz mono) va lech chuan upload 48 kHz.
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(RAW),
                        "-c:v", "copy", "-af", AF, "-c:a", "aac", "-b:a", "192k",
                        "-ar", "48000", "-ac", "2",
                        str(FINAL)], capture_output=True, text=True)
    if r.returncode != 0:
        print("GATE DO: LOUDNORM FAIL:", (r.stderr or "")[-700:])
        return 1

    j = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", str(FINAL)],
        capture_output=True, text=True).stdout)
    d = float(j["format"]["duration"])
    print("XONG: %.2fs = %d:%02d | %.1f MB"
          % (d, int(d) // 60, int(d) % 60, FINAL.stat().st_size / 1048576))
    exp = total / FPS
    if abs(d - exp) > 1.0:
        print("GATE DO: duration lech %.2fs so voi project (%.2fs)" % (d - exp, exp))
        return 1
    print("ok duration khop project.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
