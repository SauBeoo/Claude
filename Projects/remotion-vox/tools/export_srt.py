# -*- coding: utf-8 -*-
"""export_srt.py — clean subs.srt from a project's captions.lines.

The UPLOADED srt must stay CLEAN (workspace rule youtube-upload-seo §1.2):
no style tags ever — styling lives only in the burned render.

Usage: py -3 tools/export_srt.py --project cabbage-34 [--out path/subs.srt]
"""

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def fmt(ms: int) -> str:
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, milli = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{milli:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    proj = json.loads((ROOT / "projects" / args.project / "project.json")
                      .read_text(encoding="utf-8"))
    lines = proj.get("captions", {}).get("lines", [])
    if not lines:
        raise SystemExit("[LOI] khong co captions.lines")

    out = Path(args.out) if args.out else ROOT / "out" / f"{args.project}_subs.srt"
    out.parent.mkdir(parents=True, exist_ok=True)
    blocks = []
    for i, l in enumerate(lines, 1):
        blocks.append(f"{i}\n{fmt(l['startMs'])} --> {fmt(l['endMs'])}\n{l['text']}\n")
    out.write_text("\n".join(blocks), encoding="utf-8")
    print(f"OK {out} — {len(lines)} cue (SACH, khong tag)")


if __name__ == "__main__":
    main()
