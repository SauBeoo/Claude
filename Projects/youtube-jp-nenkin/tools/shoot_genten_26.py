# -*- coding: utf-8 -*-
r"""shoot_genten_26.py - chup anh 原典 THAT cho video 26.

3 trang HTML chup bang chrome-headless-shell cua Remotion (buoc 6.7 CLAUDE.md) +
1 trang PDF render bang PyMuPDF (con so 6,225 nam trong PDF, khong o HTML).

--force-device-scale-factor=2 => glyph co gap doi => cat cot hep van net.
CHAY: python tools/shoot_genten_26.py
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\26_kaigo-hokenryo-dankai-setai\genten_raw"
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")

PAGES = [
    ("raw_shinjuku_dankai.png",
     "https://www.city.shinjuku.lg.jp/fukushi/file07_02_00006.html", 9000),
    ("raw_shinjuku_9ki.png",
     "https://www.city.shinjuku.lg.jp/fukushi/file07_02_00002.html", 9000),
    ("raw_joetsu_dankai.png",
     "https://www.city.joetsu.niigata.jp/site/kaigo/hokenryou.html", 12000),
]
PDF = ("raw_kaigo.png", "https://www.mhlw.go.jp/content/12303500/001253798.pdf")


def shoot_html():
    os.makedirs(GT, exist_ok=True)
    for name, url, budget in PAGES:
        out = os.path.join(GT, name)
        cmd = [CHS, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
               "--force-device-scale-factor=2", "--window-size=1500,5000",
               f"--virtual-time-budget={budget}", f"--screenshot={out}", url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        ok = os.path.exists(out)
        sz = os.path.getsize(out) if ok else 0
        print(f"{'OK ' if ok else 'FAIL'} {name:32s} {sz/1024:8.0f} KB  rc={r.returncode}")
        if not ok:
            print("   stderr:", (r.stderr or "")[:300])


def shoot_pdf():
    import urllib.request
    import pymupdf
    raw = os.path.join(GT, "_kaigo.pdf")
    if not os.path.exists(raw):
        req = urllib.request.Request(PDF[1], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as f, open(raw, "wb") as g:
            g.write(f.read())
    doc = pymupdf.open(raw)
    print(f"PDF {len(doc)} trang")
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        out = os.path.join(GT, f"raw_kaigo_p{i+1}.png")
        pix.save(out)
        print(f"OK  p{i+1}  {pix.width}x{pix.height}  {os.path.getsize(out)/1024:.0f} KB")


if __name__ == "__main__":
    shoot_html()
    shoot_pdf()
