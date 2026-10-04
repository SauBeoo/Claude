# -*- coding: utf-8 -*-
"""Tai ban GOC 1280x720 (.mov) cua cac phim PD video 18 dang dung (ban mp4 cu chi 640x360).
Resume bang curl -C -. So duration voi ban mp4 cu: lech >0,5s thi bao — moc ss dang dung se khong khop."""
import subprocess, sys, urllib.parse
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_footage_pd")
ITEMS = [  # lo 2: phim MAU 720p cho cold open + o thay clip AI (user 23/09: "mau sac va net hon")
    ("USAF-11078", "USAF-11078.mov", "usaf11078_hiroshima_life_1946_hd.mov", None),
    ("USAF-11026", "342-USAF-11026 Japanese Repatriates Otake 03-09-1946.mov", "usaf11026_repatriates_otake_1946_hd.mov", None),
    ("USAF-11059", "USAF-11059.mov", "usaf11059_kyoto_home_1946_hd.mov", "usaf11059_kyoto_home_1946.mp4"),
    ("USAF-11079", "USAF-11079.mov", "usaf11079_hiroshima_life_1946_hd.mov", "usaf11079_hiroshima_life_1946.mp4"),
    ("USAF-11050", "USAF-11050.mov", "usaf11050_agri_1946_hd.mov", "usaf11050_agri_1946.mp4"),
]
def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return 0.0
bad = 0
for ident, fn, name, old in ITEMS:
    dst = OUT / name
    url = "https://archive.org/download/%s/%s" % (ident, urllib.parse.quote(fn))
    print("->", name, flush=True)
    r = subprocess.run(["curl", "-L", "-sS", "--retry", "5", "-C", "-", "-o", str(dst), url])
    d, d0 = dur(dst), (dur(OUT / old) if old and (OUT / old).exists() else None)
    ok = r.returncode in (0, 33) and d > 0 and (d0 is None or abs(d - d0) < 0.5)
    print("   curl=%s dur=%.2f (mp4 cu %s) %.0fMB %s" % (r.returncode, d, d0, dst.stat().st_size / 1e6 if dst.exists() else 0,
                                                       "OK" if ok else "⚠️ LECH/LOI"), flush=True)
    bad += 0 if ok else 1
print("DONE bad=%d" % bad)
sys.exit(1 if bad else 0)
