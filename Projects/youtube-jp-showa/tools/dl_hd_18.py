# -*- coding: utf-8 -*-
"""Tai ban GOC 1280x720 (.mov) cua cac phim PD video 18 dang dung (ban mp4 cu chi 640x360).
Resume bang curl -C -. So duration voi ban mp4 cu: lech >0,5s thi bao — moc ss dang dung se khong khop."""
import subprocess, sys, urllib.parse
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_footage_pd")
ITEMS = [  # (identifier, file goc, ten luu, ban mp4 dang dung)
    ("USAF11022", "342-USAF-11022 Japanese Industrial Life 02-19-1946 - 04-04-1946.mov", "usaf11022_industrial_life_1946_hd.mov", "usaf11022_industrial_life_1946.mp4"),
    ("NPC-14671", "NPC-14671.mov", "npc14671_ruins_tokyo_1945_hd.mov", "npc14671_ruins_tokyo_1945.mp4"),
    ("NPC-14672", "NPC-14672.mov", "npc14672_street_tokyo_1945_hd.mov", "npc14672_street_tokyo_1945.mp4"),
    ("USAF11018", "USAF11018.mov", "usaf11018_way_of_life_tokyo_1945_hd.mov", "usaf11018_way_of_life_tokyo_1945.mp4"),
    ("USAF-11068", "USAF-11068.mov", "usaf11068_industry_1946_hd.mov", "usaf11068_industry_1946.mp4"),
    ("USAF-11069", "USAF-11069.mov", "usaf11069_transport_1946_hd.mov", "usaf11069_transport_1946.mp4"),
    ("1946-06-20_Japan_Today", "1946-06-20_Japan_Today.mpeg", "univ_japan_today_1946_hd.mpeg", "univ_japan_today_1946.mp4"),
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
    d, d0 = dur(dst), dur(OUT / old)
    ok = r.returncode in (0, 33) and d > 0 and abs(d - d0) < 0.5
    print("   curl=%s dur=%.2f (mp4 cu %.2f) %.0fMB %s" % (r.returncode, d, d0, dst.stat().st_size / 1e6 if dst.exists() else 0,
                                                       "OK" if ok else "⚠️ LECH/LOI"), flush=True)
    bad += 0 if ok else 1
print("DONE bad=%d" % bad)
sys.exit(1 if bad else 0)
