# -*- coding: utf-8 -*-
"""import_caption_job.py — caption-only project: 1 video clip + caption track.

Use when the only job is burning styled captions onto an existing video.
Word-level timing (karaoke): pass --whisper-words to align words locally,
otherwise captions stay line-level (still styled, no karaoke highlight).

Usage:
  py -3 tools/import_caption_job.py --video x.mp4 --srt subs.srt --out my-captions
      [--whisper-words] [--lang ja] [--style outline|box|karaoke] [--fps 30]
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from auto_collage import parse_srt  # noqa: E402


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def whisper_words(audio: Path, lang: str, lines):
    """Word timestamps via faster-whisper, bucketed into the srt lines."""
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError:
        raise SystemExit("[LOI] --whisper-words can: pip install faster-whisper")
    model = WhisperModel("small", compute_type="int8")
    segs, _ = model.transcribe(str(audio), language=lang, word_timestamps=True)
    words = []
    for seg in segs:
        for w in seg.words or []:
            mid = (w.start + w.end) / 2
            li = next((i for i, l in enumerate(lines)
                       if l["start"] <= mid <= l["end"]), None)
            if li is None:
                continue
            words.append({"text": w.word, "startMs": round(w.start * 1000),
                          "endMs": round(w.end * 1000), "lineIndex": li})
    return words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--whisper-words", action="store_true")
    ap.add_argument("--lang", default="ja")
    ap.add_argument("--style", default="outline")
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    video = Path(args.video)
    lines = parse_srt(Path(args.srt))
    if not lines:
        raise SystemExit("[LOI] srt rong")
    dur = probe_duration(video)
    fps = args.fps
    total_frames = round(dur * fps)

    assets_dir = ROOT / "public" / "projects" / args.out / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    dest = assets_dir / f"source{video.suffix.lower()}"
    if not dest.exists() or dest.stat().st_size != video.stat().st_size:
        shutil.copy2(video, dest)

    words = whisper_words(video, args.lang, lines) if args.whisper_words else []

    now = datetime.now(timezone.utc).isoformat()
    project = {
        "version": 1,
        "meta": {"name": args.out, "channel": None, "templateRef": None,
                 "fps": fps, "width": 1920, "height": 1080,
                 "createdAt": now, "modifiedAt": now},
        "timeline": {"durationInFrames": total_frames},
        "sceneMarkers": [],
        "tracks": [
            {"id": "trk-src", "name": "Video", "type": "video",
             "muted": False, "hidden": False, "locked": False,
             "clips": [{"id": "src-1", "kind": "video", "from": 0,
                        "durationInFrames": total_frames,
                        "asset": f"assets/{dest.name}", "trimStartFrames": 0,
                        "fit": "cover", "layout": {}, "motion": "none",
                        "volume": 1, "fadeInFrames": 0}]},
        ],
        "captions": {
            "source": "whisper" if words else "srt-interpolated",
            "style": args.style, "enabled": True, "fontSize": 44,
            "lines": [{"text": l["text"], "startMs": round(l["start"] * 1000),
                       "endMs": round(l["end"] * 1000)} for l in lines],
            "words": words,
        },
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#000000"},
    }
    out_dir = ROOT / "projects" / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "project.json").write_text(
        json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK projects/{args.out}/project.json — {len(lines)} dong / {len(words)} tu")


if __name__ == "__main__":
    main()
