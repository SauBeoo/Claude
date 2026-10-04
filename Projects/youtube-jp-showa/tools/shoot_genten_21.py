# -*- coding: utf-8 -*-
r"""shoot_genten_21.py - chup anh 原典 THAT cho video 21 (umaredoshi-okane).

HTML -> chrome-headless-shell cua Remotion (--force-device-scale-factor=2).
PDF  -> PyMuPDF render 200 dpi.
Ra: 06_VIDEO/21_umaredoshi-okane/genten_raw/  (anh THO — cat + khoanh do o buoc sau, doc bang MAT truoc)
CHAY: python tools/shoot_genten_21.py
"""
import os, subprocess, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GT = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\21_umaredoshi-okane\genten_raw"
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")

PAGES = [  # (ten, url, budget ms, width)
    ("kokkai1963.png", "https://kokkai.ndl.go.jp/txt/104305077X00819630306/119", 9000, 1800),
    ("kokkai1966.png", "https://kokkai.ndl.go.jp/txt/105114816X02519660609/80", 9000, 1800),
    ("kokkai1972.png", "https://kokkai.ndl.go.jp/txt/106805261X01119720307/144", 9000, 1800),
    ("mext_jugyoryo.png", "https://www.mext.go.jp/b_menu/shingi/kokuritu/005/gijiroku/attach/1386502.htm", 9000, 1300),
]
PDFS = [  # (ten, url, trang can render (1-based) hoac None = tat ca)
    ("postal", "https://www.postalmuseum.jp/publication/research/research_08_09.pdf", None),
    ("soumu", "https://www.soumu.go.jp/main_content/000683792.pdf", None),
    ("ntt", "https://www.ntt-east.co.jp/databook/pdf/2024_06-10.pdf", None),
]


def shoot_html():
    os.makedirs(GT, exist_ok=True)
    for name, url, budget, w in PAGES:
        out = os.path.join(GT, name)
        cmd = [CHS, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
               "--force-device-scale-factor=2", f"--window-size={w},1400",
               f"--virtual-time-budget={budget}", f"--screenshot={out}", url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        ok = os.path.exists(out)
        print(f"{'OK ' if ok else 'FAIL'} {name:24s} {os.path.getsize(out)/1024 if ok else 0:8.0f} KB  rc={r.returncode}")
        if not ok:
            print("   stderr:", (r.stderr or "")[:300])


def shoot_pdf():
    import pymupdf
    for name, url, pages in PDFS:
        raw = os.path.join(GT, f"_{name}.pdf")
        if not os.path.exists(raw):
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as f, open(raw, "wb") as g:
                g.write(f.read())
        doc = pymupdf.open(raw)
        for i, page in enumerate(doc):
            if pages and (i + 1) not in pages:
                continue
            pix = page.get_pixmap(dpi=200)
            out = os.path.join(GT, f"{name}_p{i+1}.png")
            pix.save(out)
            print(f"OK  {name}_p{i+1}  {pix.width}x{pix.height}")


if __name__ == "__main__":
    shoot_html()
    shoot_pdf()
