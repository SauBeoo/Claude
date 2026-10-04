# -*- coding: utf-8 -*-
r"""Doi ten clip AI (task_NNN.mp4 / bat ky) -> ten trong TENFILE cua video 30.

Extension bom prompt theo THU TU dong trong FLOW.txt, nen file tai ve cung theo
thu tu do. Tool nay sap file nguon theo mtime roi gan ten theo TENFILE.

    python tools\ingest_clips30.py --src ~/Downloads --offset 1

MOT FILE prompt duy nhat (user chot 2026-09-06). Gen het 105 clip roi chay 1 lan
voi --offset 1. Neu gen lam nhieu dot thi --offset = so clip DAU cua dot do.

⚠️ TRUOC KHI CHAY: retime 8s -> 10s + crop watermark + chuan hoa size
    python E:\Claude\Projects\_media_library\retime_clips.py <src> <dst> \
        --factor 1.25 --crop 0.08 --size 1920x1080
   Crop 0.08 (8%) chot BANG MAT — video 29 thu 3,2% thi con lo rang phim + so hieu
   phim mau cam; phep do may tra 12,5% vi CHAM MEP cua so quet 60 cot
   (`media-library.md` §2.10 ⑤ · `feedback_do_pixel_cua_so_quet`).
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = Path(r"E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\30_futon-dani-uchinaoshi")


def tenfile():
    m = {}
    for f in ("video_prompts_TENFILE.txt",):
        p = VD / f
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            g = re.match(r"^\s*(\d+)\s*->\s*(\S+\.mp4)", line)
            if g:
                m[int(g.group(1))] = g.group(2)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(Path.home() / "Downloads"))
    ap.add_argument("--offset", type=int, required=True,
                    help="so clip dau tien cua dot gen (gen het 1 lan thi = 1)")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    m = tenfile()
    src = Path(a.src).expanduser()
    files = sorted(src.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
    if not files:
        print(f"🔴 khong thay .mp4 nao trong {src}")
        return 1

    dst_dir = VD / "clips"
    dst_dir.mkdir(parents=True, exist_ok=True)
    n, miss = 0, []
    for k, f in enumerate(files):
        no = a.offset + k
        if no not in m:
            print(f"   ⚠️ clip {no} khong co trong TENFILE — bo qua {f.name}")
            continue
        dst = dst_dir / m[no]
        print(f"   {no:3d}  {f.name:34s} -> {m[no]}")
        if not a.dry:
            shutil.copy2(f, dst)
        n += 1

    want = [no for no in m if a.offset <= no < a.offset + len(files)]
    got = a.offset + len(files) - 1
    print(f"\n✅ {n} clip -> {dst_dir}")
    print(f"   lo nay dang ky {a.offset}..{got}")
    thieu = [no for no in sorted(m) if not (dst_dir / m[no]).exists()]
    if thieu:
        print(f"🔴 CON THIEU {len(thieu)}/{len(m)} clip: {thieu[:12]}"
              f"{' ...' if len(thieu) > 12 else ''}")
        print("   -> chua duoc render (render-background.md §1.5)")
    else:
        print(f"   ✅ du ca {len(m)} clip — chay: python tools\\gen_slides30.py --place")
    return 0


if __name__ == "__main__":
    sys.exit(main())
