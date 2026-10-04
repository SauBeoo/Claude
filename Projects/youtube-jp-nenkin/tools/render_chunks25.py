# -*- coding: utf-8 -*-
r"""render_chunks25.py — render video 25 (`nenkin-25`, vox paper-collage) theo CHUNK + loudnorm -14 LUFS.

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

    python tools\render_chunks23.py             # render + noi + loudnorm
    python tools\render_chunks23.py --check     # chi in trang thai
    python tools\render_chunks23.py --only 3,7  # render lai vai chunk roi noi lai
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
NAME = "nenkin-25"
PROPS = f"projects/{NAME}/project.json"
OUTDIR = RV / "out" / "n25chunks"
RAW = RV / "out" / "n25" / "raw.mp4"
FINAL = RV / "out" / "n25" / "final.mp4"
FPS = 24
# 🔴 1600 (khong phai 2400): lan chay dau conc=2 / chunk 2400 bi harness KILL vi het
#    RAM ngay trong CHUNK DAU (0/10 mieng xong). Doi luc **chua co mieng nao** thi doi
#    CHUNK la MIEN PHI — luat 'dung doi CHUNK' o duoi chi ap khi da co mieng render roi.
CHUNK = 1600          # ~67s video / chunk -> moi lan chay ngan hon, it trung spike RAM

# ══════════════════════════════════════════════════════════════════════════════
# 🔴🔴 HAI THU LAM CHET 3 LUOT RENDER DAU, CA HAI **DO DUOC**, khong phai suy doan:
#
#  ① RO BO NHO THEO SO FRAME — do bang `tools/probe25.py` (200 frame, conc=1):
#       frame   0 -> render   464 MB        frame 150 -> render 3.305 MB
#       frame  80 -> render 2.057 MB        frame 200 -> render 3.737 MB
#     ~**16 MB/frame, leo DEU, khong chung**. Suy ra chunk 1600 can ~26 GB va chunk 2400
#     can ~38 GB tren mot may 23,9 GB => hai luot dau chet la tat yeu, va **ha
#     `--concurrency` khong the cuu** vi cai leo khong phai so worker (luot 2 da chay
#     conc=1 va van chet).
#     ⇒ Thu pham: Remotion cache khung VIDEO da giai ma theo mot phan RAM may. Project nay
#       co **67 clip**, cang chay cang gom them clip vao cache. Video 23 nhe hon nen chua vo.
#     ⇒ Vá: ep TRAN cache. Do lai voi tran 256 MB: RAM **chung o ~2,3-2,6 GB** thay vi leo.
#
#  ② TIEN TRINH MO COI SAU MOI LAN BI KILL — thu that su giet luot ke tiep:
#       sau 3 luot bi kill, con **remotion 4.636 MB + chrome-headless-shell 1.080 MB +
#       ffmpeg 598 MB** nam lai; RAM trong tut 10,6 GB -> 4,8 GB. Don xong ve lai 11,1 GB.
#     ⇒ Moi lan harness kill la ngan sach RAM cua luot sau bi an mat ~6 GB, nen luot sau
#       chet SOM HON luot truoc — nhin ra thi tuong "cang ngay cang te", that ra la rac.
#     ⇒ Vá: don mo coi TRUOC MOI CHUNK (`_kill_orphans`), khong cho rac tich luy.
# ══════════════════════════════════════════════════════════════════════════════
CACHE_CAP = ["--offthreadvideo-cache-size-in-bytes=268435456",
             "--media-cache-size-in-bytes=268435456"]
ORPHANS = ("remotion.exe", "chrome-headless-shell.exe")


def _kill_orphans():
    """Giet tien trinh render con sot lai tu luot truoc.

    ⚠️ CHI giet `remotion.exe` va `chrome-headless-shell.exe` — hai cai nay CHI do Remotion
    sinh ra. ⛔ KHONG dung `node.exe` (user co the dang chay viec khac) va tuyet doi khong
    dung `chrome.exe` (do la Chrome cua user). `ffmpeg.exe` cung khong dung o day vi buoc
    concat/loudnorm cua chinh tool nay dung no.
    """
    n = 0
    for p in ORPHANS:
        r = subprocess.run(["taskkill", "/F", "/IM", p], capture_output=True, text=True)
        n += r.stdout.count("SUCCESS")
    return n


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
# Video 25 chua co chunk nao bi kill => khong che nho san. Chunk nao chet LAP LAI thi
# them vao day (vd {8: 3}), DUNG doi `CHUNK` — doi la ca luoi chunk lech, moi mieng
# da render thanh vo dung.
SPLIT = {}


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
    # 🔴 MAC DINH 1 cho video 25: conc=2 chet ngay chunk dau tren may nay (11 GB trong,
    #    PhpStorm dang giu 1,9 GB). Mot worker Chrome it RAM hon han; cham hon ~40%.
    ap.add_argument("--conc", type=int, default=1, help="concurrency cua remotion (mac dinh 1)")
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
        nk = _kill_orphans()
        print("[%2d/%d] %s  frame %d-%d  (conc=%d%s) ..."
              % (k + 1, len(cs), name, f0, f1, a.conc,
                 ", don %d mo coi" % nk if nk else ""))
        r = subprocess.run(
            ["npx.cmd", "remotion", "render", "VoxProject", f"--props={PROPS}",
             f"--frames={f0}-{f1}", f"--concurrency={a.conc}", *CACHE_CAP, str(o)],
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
