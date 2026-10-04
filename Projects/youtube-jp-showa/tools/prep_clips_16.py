# -*- coding: utf-8 -*-
r"""Chuan bi 220 clip cua video 16: scale 720p -> 1080p + grade phim + doi ten theo INDEX.

    python tools\prep_clips_16.py                 # chay day du
    python tools\prep_clips_16.py --no-grade      # chi scale (de so sanh)

BA VIEC, theo dung thu tu:
 1. **Doi ten theo SLOT** — renderer doc `clips/clip_{i:02d}.mp4` THEO SO THU TU SLOT
    (`video_render.py` dong 126), khong doc theo ten mo ta. Dat ten mo ta => renderer coi
    nhu KHONG CO CLIP NAO va am tham fallback anh tinh, trong khi preflight van in "✓ clip
    đều ổn" (CLAUDE.md §Visual). Ten mo ta giu o `clips_named/` + so tra `clips/_MAP.txt`.
 2. **Scale 1280x720 -> 1920x1080** — lo nay gen ra 720p.
 3. **Grade `showa70`** cho canh QUA KHU. Do bang may trên chinh lo nay (7 clip mau):
    luma 107.2 · contrast 71.8 · grain 2.60 · den 23.4%
    phim that 1959: luma 66.3 · contrast 50.1 · grain 17.76 · den 14.7%
    => clip la DIGITAL SACH, gan nhu khong hat. Grade la de keo ve phia phim, dung nhu
    video 15 (user chot 2026-09-17: "mau phim hoai co hon").

🔴 **CANH THOI NAY (`ima_ie`) KHONG GRADE** — do la chu y cua kich ban: qua khu ngả phim,
   hien tai sach va that. Video 15 da lam dung the; o day preset doc tu ten file trong
   `videogen16_TENFILE.txt` (dang `clip_<id>_<khoi>_<preset>.mp4`).

⚠️ KHONG crop vien. Lo nay soi 5 frame khong thay vien phim — guard dat o 2% dau prompt da
   an (video 15 lo dau guard nam o 70% thi 5/10 clip co vien, phai crop).
"""
import argparse, io, os, re, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SRC = Path(r"F:\Youtube\Dự_án_mới_18_6bbvrq6n")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "16_omiai-kekkon"
TEN = VD / "videogen16_TENFILE.txt"

SCALE = "scale=1920:1080:flags=lanczos"
# preset mau lay NGUYEN VAN tu tools/grade_showa.py (khong chep so, de hai cho khoi troi)
sys.path.insert(0, str(ROOT / "tools"))
from grade_showa import PRESETS  # noqa: E402

NO_GRADE_PRESETS = {"ima_ie"}     # canh thoi NAY


def names():
    """[(index0, ten_mo_ta, preset)] doc tu TENFILE — thu tu dong = thu tu slot."""
    out = []
    for line in io.open(TEN, encoding="utf-8"):
        m = re.match(r"\s*(\d+)\s+(clip_\S+\.mp4)", line)
        if not m:
            continue
        i, nm = int(m.group(1)) - 1, m.group(2)
        # 🔴 preset CO GACH DUOI (`ima_ie`, `office_rouka`) nen KHONG duoc lay token cuoi.
        #    Ten file la clip_<sid>_<khoi>_<preset>.mp4 => preset = tu token thu 3 tro di.
        #    Bug ban dau: split("_")[-1] tra "ie" => 42 clip THOI NAY bi grade phim,
        #    dung cai lop phai giu sach. Bat duoc truoc khi render (dem theo boi canh).
        preset = "_".join(nm[:-4].split("_")[3:])
        out.append((i, nm, preset))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", default="showa70")
    ap.add_argument("--no-grade", action="store_true")
    ap.add_argument("--only", help="vd 0,5,17 — chi lam may slot nay")
    a = ap.parse_args()

    rows = names()
    if not rows:
        sys.exit("[LOI] khong doc duoc %s" % TEN)
    only = {int(x) for x in a.only.split(",")} if a.only else None

    out = VD / "clips"
    named = VD / "clips_named"
    out.mkdir(parents=True, exist_ok=True)
    named.mkdir(parents=True, exist_ok=True)

    missing, done, skip = [], 0, 0
    maplines = []
    for i, nm, preset in rows:
        src = SRC / ("task_%03d_1_720p.mp4" % (i + 1))
        dst = out / ("clip_%02d.mp4" % i)
        maplines.append("%3d  %-44s %-12s %s" % (i, nm, preset, src.name))
        if not src.exists():
            missing.append((i, src.name))
            continue
        if only is not None and i not in only:
            continue
        # resume theo mtime, khong theo "da ton tai" (`render-background.md` §2.5)
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            skip += 1
            continue
        grade = (not a.no_grade) and preset not in NO_GRADE_PRESETS
        vf = SCALE + ("," + PRESETS[a.preset] if grade else "")
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", vf,
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", "-an", str(dst)]
        r = subprocess.run(cmd)
        if r.returncode != 0:
            sys.exit("[LOI] ffmpeg gay o slot %d (%s)" % (i, src.name))
        # ban co TEN MO TA: hardlink, 0 byte them
        ln = named / nm
        if ln.exists():
            ln.unlink()
        try:
            os.link(dst, ln)
        except OSError:
            pass
        done += 1
        if done % 20 == 0:
            print("  ... %d/%d" % (done + skip, len(rows)), flush=True)

    io.open(out / "_MAP.txt", "w", encoding="utf-8").write(
        "slot  ten mo ta                                    preset       nguon\n"
        + "\n".join(maplines) + "\n")

    print("=" * 60)
    print("nguon      : %s" % SRC)
    print("dung/bo qua: %d dung moi · %d da co (bo qua theo mtime)" % (done, skip))
    print("grade      : %s  (canh %s KHONG grade)"
          % ("KHONG" if a.no_grade else a.preset, "/".join(sorted(NO_GRADE_PRESETS))))
    n_ok = len(list(out.glob("clip_*.mp4")))
    print("clip trong clips/: %d / %d" % (n_ok, len(rows)))
    if missing:
        print("🔴 THIEU %d clip nguon: %s" % (len(missing), missing[:6]))
        return 1
    print("KET QUA: %s" % ("DU CLIP" if n_ok == len(rows) else "CHUA DU"))
    return 0 if n_ok == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
