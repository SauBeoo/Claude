# -*- coding: utf-8 -*-
"""Tai file lon tu archive.org bang N luong range song song (server bop 1 luong ~18KB/s).
python dl_parallel.py <url> <dest> [threads=8]
"""
import sys, io, urllib.request, threading, os
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ShowaChannel/1.0"}
url, dest = sys.argv[1], Path(sys.argv[2])
N = int(sys.argv[3]) if len(sys.argv) > 3 else 8

req = urllib.request.Request(url, headers=UA, method="HEAD")
with urllib.request.urlopen(req, timeout=60) as r:
    total = int(r.headers["Content-Length"]); final = r.geturl()
print("size", total, "url", final, flush=True)
part = total // N
lock = threading.Lock(); done = [0]

def worker(i):
    a = i * part; b = total - 1 if i == N - 1 else (i + 1) * part - 1
    p = dest.with_suffix(f".part{i}")
    have = p.stat().st_size if p.exists() else 0
    if have >= b - a + 1: return
    rq = urllib.request.Request(final, headers={**UA, "Range": f"bytes={a+have}-{b}"})
    with urllib.request.urlopen(rq, timeout=120) as r, open(p, "ab") as f:
        while True:
            c = r.read(1 << 18)
            if not c: break
            f.write(c)
            with lock:
                done[0] += len(c)

ts = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
[t.start() for t in ts]
import time
while any(t.is_alive() for t in ts):
    time.sleep(10)
    print(f"  {done[0]/1e6:7.1f} MB", flush=True)
[t.join() for t in ts]
missing = []
for i in range(N):
    a = i * part; b = total - 1 if i == N - 1 else (i + 1) * part - 1
    p = dest.with_suffix(f".part{i}")
    have = p.stat().st_size if p.exists() else 0
    if have < b - a + 1:
        missing.append((i, have, b - a + 1))
if missing:
    print("INCOMPLETE parts (chay lai lenh de resume):", missing, flush=True)
    sys.exit(2)
with open(dest, "wb") as out:
    for i in range(N):
        p = dest.with_suffix(f".part{i}")
        out.write(p.read_bytes()); p.unlink()
print("DONE", dest.stat().st_size, flush=True)
