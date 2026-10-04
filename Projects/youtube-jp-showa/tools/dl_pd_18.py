# -*- coding: utf-8 -*-
"""Tai lo phim PD moi cho video 18 (danh sach tu SOURCES_FILMS_2026-09-23.md). Resume bang curl -C -."""
import subprocess, sys, urllib.parse
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_footage_pd")
ITEMS = [  # (identifier, file tren archive.org, ten luu)
    ("USAF11022", "342-USAF-11022 Japanese Industrial Life 02-19-1946 - 04-04-1946.mp4", "usaf11022_industrial_life_1946.mp4"),
    ("gov.archives.arc.1991037", "gov.archives.arc.1991037.mp4", "nsc1991037_japan_democracy_1949.mp4"),
    ("1946-06-20_Japan_Today", "1946-06-20_Japan_Today.mp4", "univ_japan_today_1946.mp4"),
    ("NPC-14671", "NPC-14671.mp4", "npc14671_ruins_tokyo_1945.mp4"),
    ("NPC-14672", "NPC-14672.mp4", "npc14672_street_tokyo_1945.mp4"),
    ("USAF11018", "USAF11018.mp4", "usaf11018_way_of_life_tokyo_1945.mp4"),
    ("USAF-11067", "342-USAF-11067 Black Market Kyoto 05-28-1946.mp4", "usaf11067_black_market_kyoto_1946.mp4"),
    ("gov.archives.arc.2569464", "gov.archives.arc.2569464_512kb.mp4", "bigpic2569464_operation_rollup.mp4"),
]
bad = 0
for ident, fn, name in ITEMS:
    url = "https://archive.org/download/%s/%s" % (ident, urllib.parse.quote(fn))
    dst = OUT / name
    print("->", name, flush=True)
    r = subprocess.run(["curl", "-L", "-sS", "--retry", "5", "-C", "-", "-o", str(dst), url])
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dst)],
                       capture_output=True, text=True)
    ok = r.returncode in (0, 33) and p.stdout.strip()
    print("   curl=%s dur=%s size=%.1fMB" % (r.returncode, p.stdout.strip(), dst.stat().st_size / 1e6 if dst.exists() else 0), flush=True)
    bad += 0 if ok else 1
print("DONE bad=%d" % bad)
sys.exit(1 if bad else 0)
