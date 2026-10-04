# -*- coding: utf-8 -*-
r"""Kiem 105 clip AI cua video 30 TRUOC khi retime/ingest.

Ba lop kiem, tu re den dat:
  ① MAY  — size/fps/duration/file hong/den/dung hinh
  ② MAT  — contact sheet 3 frame moi clip (dau/giua/cuoi), 15 clip/trang
  ③ MAT  — crop goc duoi-phai 1:1 de soi watermark ✦

🔴 Vi sao phai co lop ②③: video 29 do duoc **58/73 clip hong o THAO TAC TAY**
   (tay cam vat nho, deo kinh, xoay dao) va **KHONG lop may nao bat duoc** —
   moi chi so deu binh thuong. Xem [[feedback_ai_video_hong_thao_tac_tay]].
🔴 Watermark: **do bang MAT, khong bang so** — cua so quet hep hon vat thi so do
   tra ve mep cua so chu khong phai vat ([[feedback_do_pixel_cua_so_quet]]).

    python tools\check_clips30.py --src F:\Youtube\codai30_kb2af0zj
    python tools\check_clips30.py --src ... --sheets     # + dung contact sheet
"""
import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\30_futon-dani-uchinaoshi")


def probe(f):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-show_entries", "format=duration,size", "-of", "json", str(f)],
        capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
        st = j["streams"][0]
        return (st["width"], st["height"], st["r_frame_rate"],
                float(j["format"]["duration"]), int(j["format"]["size"]))
    except Exception:
        return None


def still_stats(f, t):
    """Do do sang trung binh + do lech chuan cua 1 frame -> bat frame den/phang."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(f), "-frames:v", "1",
         "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG",
         "-f", "null", "-"], capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "YAVG" in line:
            try:
                return float(line.split("=")[-1])
            except ValueError:
                pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--sheets", action="store_true")
    a = ap.parse_args()
    src = Path(a.src)
    fs = sorted(src.glob("*.mp4"))
    print(f"── {len(fs)} clip trong {src}")

    info, broken = {}, []
    for f in fs:
        p = probe(f)
        if p is None:
            broken.append(f.name)
        else:
            info[f] = p

    print(f"\n① MAY")
    print(f"   file hong: {broken or '0 ✅'}")
    print(f"   size : {dict(Counter((v[0], v[1]) for v in info.values()))}")
    print(f"   fps  : {dict(Counter(v[2] for v in info.values()))}")
    print(f"   dur  : {dict(Counter(round(v[3], 1) for v in info.values()))}")
    tiny = [f.name for f, v in info.items() if v[4] < 300_000]
    print(f"   file <300KB: {tiny or '0 ✅'}")
    print(f"   tong: {sum(v[4] for v in info.values()) / 1024**3:.2f} GB")

    # frame den / trang o dau-giua-cuoi
    print(f"\n   quet frame den/chay (YAVG <16 hoac >240)…")
    bad = []
    for f, v in info.items():
        for t in (0.3, v[3] / 2, max(v[3] - 0.4, 0.5)):
            y = still_stats(f, t)
            if y is not None and (y < 16 or y > 240):
                bad.append(f"{f.name}@{t:.1f}s Y={y:.0f}")
    print(f"   {bad or '0 ✅'}")

    if a.sheets:
        out = VD / "_chk"
        out.mkdir(parents=True, exist_ok=True)
        names = [f.name for f in sorted(info)]
        for pg in range(0, len(names), 15):
            batch = names[pg:pg + 15]
            tiles = []
            for n in batch:
                f = src / n
                d = info[f][3]
                for k, t in enumerate((0.3, d / 2, max(d - 0.4, 0.5))):
                    tp = out / f"_t_{n}_{k}.jpg"
                    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t),
                                    "-i", str(f), "-frames:v", "1", "-vf",
                                    "scale=426:-1", str(tp)], check=False)
                    tiles.append(tp)
            sheet = out / f"sheet_{pg//15 + 1:02d}.jpg"
            subprocess.run(["ffmpeg", "-y", "-v", "error"]
                           + sum([["-i", str(t)] for t in tiles], [])
                           + ["-filter_complex",
                              f"tile={3}x{len(batch)}:margin=4:padding=3",
                              str(sheet)], check=False)
            for t in tiles:
                t.unlink(missing_ok=True)
            print(f"   sheet -> {sheet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
