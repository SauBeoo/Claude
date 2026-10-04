# -*- coding: utf-8 -*-
r"""shoot_genten_32.py - chup anh 原典 THAT cho video 32 (本人確認 2027 銀行).

Chup bang chrome-headless-shell cua Remotion, --force-device-scale-factor=2 (cat cot hep van net).
Khoanh do + cat khung lam o buoc dung hinh (make_genten_30.py, CHUA viet), khong lam o day.
CHAY: python tools/shoot_genten_32.py
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\32_ginko-honnin-kakunin-2027\genten_raw"
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")

PAGES = [
    ("raw_keishicho_ic.png", "https://www.keishicho.metro.tokyo.lg.jp/menkyo/menkyo/menkyo_annai/ic.html", 12000),
]


def main():
    os.makedirs(GT, exist_ok=True)
    for name, url, budget in PAGES:
        out = os.path.join(GT, name)
        cmd = [CHS, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
               "--force-device-scale-factor=2", "--window-size=1500,5000",
               f"--virtual-time-budget={budget}", f"--screenshot={out}", url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        ok = os.path.exists(out)
        sz = os.path.getsize(out) if ok else 0
        print(f"{'OK ' if ok else 'FAIL'} {name:28s} {sz/1024:8.0f} KB  rc={r.returncode}")


if __name__ == "__main__":
    main()
