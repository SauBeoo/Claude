# -*- coding: utf-8 -*-
"""Dat 101 anh MOI (tu Downloads) vao slides_img/ + cat watermark, roi build lai 132 anh
ten-tran (slide_NN.jpg) theo dung thu tu TENFILE.txt moi (ban 4, nhip 6s/khung)."""
import json, shutil
from pathlib import Path
from PIL import Image

SRC = Path(r"C:\Users\tuana\Downloads\download (14)")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\04_showa45-asa")
IMG = VD / "slides_img"
BAK = VD / "_wm_orig"
CUT_X = 0.915

AUTO_MAP = json.load(open(VD / "_auto_map.json", encoding="utf-8"))

# 9 ghi de tay (auto-match diem thap hoac sai)
OVERRIDE = {
    "i10_02_senaka": "Commuters_standing_on_train_plat…_202608250204.jpeg",
    "i12_03_shashin_bokeh": "Aged_hands_holding_newspaper_202608250221.jpeg",
    "i12_06_gunshuu_close": "Crowd_in_Showa_era_lane_202608250221.jpeg",
    "i12_07_tou_hitori": "Tower_in_Showa-era_lane_202608250221.jpeg",
    "i12_08_hitori_senaka": "Figure_walking_in_residential_lane_202608250221.jpeg",
}
# Khong co anh rieng duoc gen dung - TAI SU DUNG anh ngan hang (khong copy tu Downloads)
REUSE_BANK = {
    "i12_12_yane_sora": "24_ie_zentai_asa",
    "i12_17_memo_yure": "25b_anpi_kakunin",
    "i12_18_roka": "25_gyunyu_kamipakku_ima",
    "i12_26_ie_sora": "24_ie_zentai_asa",
}
AUTO_MAP.update(OVERRIDE)


def crop_wm(im):
    W, H = im.size
    nw = int(W * CUT_X)
    nh = min(H, int(round(nw * 9 / 16)))
    return im.crop((0, 0, nw, nh)).resize((1376, 768), Image.LANCZOS)


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    BAK.mkdir(parents=True, exist_ok=True)
    placed, reused, missing = 0, 0, []

    for name, src_name in AUTO_MAP.items():
        if name in REUSE_BANK:
            continue
        src = SRC / src_name
        if not src.exists():
            missing.append((name, src_name))
            continue
        im = Image.open(src).convert("RGB")
        im.save(BAK / f"{name}.jpg", quality=95)
        cropped = crop_wm(im)
        dst = IMG / f"i_{name}.jpg"
        cropped.save(dst, quality=95)
        placed += 1

    for name, bank_key in REUSE_BANK.items():
        # tim file ngan hang co san (dang slide_NN_<bank_key>.jpg)
        cands = list(IMG.glob(f"slide_*_{bank_key}.jpg"))
        if not cands:
            missing.append((name, f"BANK:{bank_key} khong thay"))
            continue
        shutil.copy2(cands[0], IMG / f"i_{name}.jpg")
        reused += 1

    print(f"OK: dat {placed} anh moi (da cat wm) + tai su dung {reused} anh ngan hang")
    if missing:
        print(f"[LOI] thieu {len(missing)}:")
        for n, s in missing:
            print("  ", n, "<-", s)


if __name__ == "__main__":
    main()
