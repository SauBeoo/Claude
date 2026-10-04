# -*- coding: utf-8 -*-
r"""shoot_genten_31.py - chup anh 原典 THAT cho video 31 (扶養親族等申告書 domino).

Chup bang chrome-headless-shell cua Remotion, --force-device-scale-factor=2 (cat cot hep van net).
Khoanh do + cat khung lam o buoc dung hinh (make_genten_30.py, CHUA viet), khong lam o day.
CHAY: python tools/shoot_genten_31.py
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\31_fuyo-shinkokusho-hikazei-domino\genten_raw"
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")

PAGES = [
    ("raw_nenkin_r9_kami.png", "https://www.nenkin.go.jp/service/jukyu/tetsuduki/rourei/jukyu/fuyo/2027fuyoukami.html", 12000),
    ("raw_nenkin_0617.png", "https://www.nenkin.go.jp/oshirase/taisetu/kojin/2026/202606/0617.html", 12000),
    ("raw_nenkin_faq_mitei.png", "https://www.nenkin.go.jp/section/faq/jukyu/jukyushatodoke/rourei/fuyoushinkoku/teishutsu/20141022-08.html", 12000),
    ("raw_nenkin_r9_top.png", "https://www.nenkin.go.jp/service/jukyu/tuutisyo/20160822.html", 12000),
    ("raw_osaka_hikazei.png", "https://www.city.osaka.lg.jp/zaisei/page/0000384084.html", 12000),
    ("raw_osaka_kaigo.png", "https://www.city.osaka.lg.jp/fukushi/page/0000667192.html", 12000),
    ("raw_nenkin_koumoku.png", "https://www.nenkin.go.jp/denshibenri_kojin/denshibenri_rorei/denshi_fuyo/fuyokoumoku.html", 12000),
    ("raw_tama_fuyo.png", "https://www.city.tama.lg.jp/kurashi/nenkin/oshjirase/1001952.html", 12000),
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
