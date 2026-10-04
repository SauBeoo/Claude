# -*- coding: utf-8 -*-
r"""shoot_genten_30.py - chup anh 原典 THAT cho video 30 (10月15日 直前チェック).

Chup bang chrome-headless-shell cua Remotion, --force-device-scale-factor=2 (cat cot hep van net).
Khoanh do + cat khung lam o buoc dung hinh (make_genten_30.py, CHUA viet), khong lam o day.
CHAY: python tools/shoot_genten_30.py
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\30_nenkin-furikomi-10gatsu-fueru-hito\genten_raw"
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")

PAGES = [
    # shot 1 (~1:40): kariChoushu = zennendo 2gatsu
    ("raw_setagaya_kari.png", "https://www.city.setagaya.lg.jp/02061/2286.html", 9000),
    # shot 2 (~3:40): Niigata-shi dankai table dai2 33,000 / dai3 53,700
    ("raw_niigata_dankai.png", "https://www.city.niigata.lg.jp/iryo/kaigo/kaigoindex/hokenryou.html", 12000),
    # shot 3 (~10:30): minashi kazei (R8 only)
    ("raw_niigata_minashi.png", "https://www.city.niigata.lg.jp/iryo/kaigo/kaigoindex/R8kaigohokenryo.html", 12000),
    # phu: Nerima rei 2 (kyuyo 110man) + Niigata juminzei kari/hon + nenkin kikou yoteigaku
    ("raw_nerima_rei2.png", "https://www.city.nerima.tokyo.jp/hokenfukushi/kaigohoken/hokenryo/R7hokenryosantei.html", 12000),
    ("raw_niigata_juminzei.png", "https://www.city.niigata.lg.jp/kurashi/zei/siraberu/kojin/sinkoku_nouzei.html", 12000),
    ("raw_nenkin_yoteigaku.png", "https://www.nenkin.go.jp/service/jukyu/tuutisyo/gakukaitei/0601-02.html", 12000),
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
