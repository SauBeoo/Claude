# -*- coding: utf-8 -*-
r"""INGEST clip AI cho video 29: doi ten task_NNN -> ten trong TENFILE, kiem du bo.

Chay SAU khi `_media_library/retime_clips.py` da retime + crop vao `_clips_stage/`.

    python tools\ingest_clips29.py                 # kiem, khong doi gi
    python tools\ingest_clips29.py --apply         # doi ten -> clips/

BAY: extension xuat theo THU TU BOM (task_001, task_002...), khong theo ten canh.
Neu bom FLOW2.txt truoc thi task_001 = clip 42. Script doc co --offset de khai bao.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = Path(r"E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\29_hocho-togi-mennaoshi")


def load_map(tenfile: Path):
    """doc '<so> -> <ten>.mp4  | <cau thoai>' -> {so: (ten, thoai)}"""
    m = {}
    for line in tenfile.read_text(encoding="utf-8").splitlines():
        g = re.match(r"^\s*(\d+)\s*->\s*(\S+\.mp4)\s*\|?\s*(.*)$", line)
        if g:
            m[int(g.group(1))] = (g.group(2), g.group(3).strip())
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default=str(VD / "_clips_stage"))
    ap.add_argument("--out", default=str(VD / "clips"))
    ap.add_argument("--tenfile", default=str(VD / "video_prompts_TENFILE2.txt"))
    ap.add_argument("--offset", type=int, default=42,
                    help="task_001 ung voi clip so may (lo 2 bat dau tu 42)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    stage, out = Path(a.stage), Path(a.out)
    if not stage.is_dir():
        print(f"🔴 chua co {stage} — chay retime_clips.py truoc"); return 1
    mp = load_map(Path(a.tenfile))
    if not mp:
        print(f"🔴 khong doc duoc map tu {a.tenfile}"); return 1

    srcs = sorted(stage.glob("task_*.mp4"))
    print(f"── {len(srcs)} clip trong stage · map co {len(mp)} dong · offset={a.offset}")

    plan, miss = [], []
    for p in srcs:
        g = re.search(r"task_(\d+)", p.name)
        if not g:
            continue
        idx = int(g.group(1)) + a.offset - 1        # task_001 -> clip <offset>
        if idx not in mp:
            miss.append((p.name, idx)); continue
        plan.append((p, out / mp[idx][0], idx, mp[idx][1]))

    for src, dst, idx, line in plan[:5]:
        print(f"  {src.name}  ->  clip {idx:3d}  {dst.name:38s} | {line[:34]}")
    if len(plan) > 5:
        print(f"  … con {len(plan)-5} file nua")

    have = {i for _, _, i, _ in plan}
    want = set(range(1, 113))
    lack = sorted(want - have)
    print(f"\n── DU BO: co {len(have)}/112 clip")
    if lack:
        rng = []
        s = e = lack[0]
        for x in lack[1:]:
            if x == e + 1: e = x
            else: rng.append((s, e)); s = e = x
        rng.append((s, e))
        print("🔴 THIEU:", " · ".join(f"{s}-{e}" if s != e else str(s) for s, e in rng),
              f"  (tong {len(lack)} clip)")
        print("   -> chua du asset, KHONG duoc render video (render-background.md §1.5)")
    if miss:
        print(f"⚠️ {len(miss)} file khong co trong map:", [m[0] for m in miss][:5])

    if not a.apply:
        print("\n(chay lai voi --apply de doi ten)")
        return 0

    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for src, dst, _, _ in plan:
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        shutil.copy2(src, dst)
        n += 1
    print(f"\n✅ da dat {n} clip vao {out}  (tong {len(list(out.glob('*.mp4')))} file)")
    return 1 if lack else 0


if __name__ == "__main__":
    sys.exit(main())
