# -*- coding: utf-8 -*-
"""import_pipeline.py — import a channel-pipeline video into remotion-vox.

Reads the pipeline's sync contract (06_VIDEO/<stem>/timeline.json), the
<stem>_SLIDES*.json cue file and channels.py profile, and produces
projects/<out>/project.json + copies assets into public/projects/<out>/assets/.

Timing reproduces video_render.py exactly: slide i starts at the timeline
line whose text contains `match` (+offset); entries sorted by start; first
forced to t=0; duration fills to the next start (min 0.5s); last runs to total.

Asset copies are content-aware: assets_manifest.json stores sha1 per file,
re-runs only copy files whose hash changed (workspace rule §2.5 — never
existence-only).

Usage:
  py -3 tools/import_pipeline.py --stem 34_cabbage-asa-yoru --channel health
      [--out <project-name>] [--fps 30]
"""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CHANNELS_TOOLS = Path(r"E:\Claude\Projects\youtube-jp-health\tools")


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rgb_hex(t) -> str:
    return "#{:02X}{:02X}{:02X}".format(*t)


def find_slides_json(scripts_dirs, stem: str) -> Path:
    # exact _SLIDES.json first, then variants (_SLIDES_photo / _SLIDES_video)
    for d in scripts_dirs:
        p = d / f"{stem}_SLIDES.json"
        if p.exists():
            return p
    for d in scripts_dirs:
        hits = sorted(d.glob(f"{stem}_SLIDES*.json"))
        if hits:
            return hits[0]
    raise SystemExit(f"[LOI] khong tim thay {stem}_SLIDES*.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stem", required=True)
    ap.add_argument("--channel", required=True)
    ap.add_argument("--out", default=None, help="project name (default: stem)")
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    sys.path.insert(0, str(CHANNELS_TOOLS))
    import channels as CH  # noqa: E402

    prof = CH.get(args.channel)
    pal = CH.palette(args.channel)
    proj_dir = CH.project_dir(args.channel)
    video_dir = proj_dir / prof["video_dir"] / args.stem
    img_dir = Path(CH.img_dir(args.channel, args.stem))
    clips_dir = Path(CH.clips_dir(args.channel, args.stem))
    scripts_dirs = sorted(proj_dir.glob("0*_SCRIPTS"))

    timeline_path = video_dir / "timeline.json"
    if not timeline_path.exists():
        raise SystemExit(f"[LOI] khong co {timeline_path} — video chua render voice")
    tl = json.loads(timeline_path.read_text(encoding="utf-8-sig"))
    total = float(tl["total"])
    lines = tl["lines"]

    slides_path = find_slides_json(scripts_dirs, args.stem)
    entries = json.loads(slides_path.read_text(encoding="utf-8-sig"))
    print(f"timeline: {total:.1f}s / {len(lines)} dong · slides: {slides_path.name} ({len(entries)} entry)")

    fps = args.fps
    out_name = args.out or args.stem
    total_frames = round(total * fps)

    # ---- timing: reproduce video_render.py ---------------------------------
    timed = []
    for i, e in enumerate(entries):
        match = e.get("match")
        if not match:
            raise SystemExit(f"[LOI] entry {i} khong co 'match'")
        line = next((l for l in lines if match in l["text"]), None)
        if line is None:
            raise SystemExit(f"[LOI] entry {i}: match khong khop dong nao: {match[:40]}")
        start = float(line["start"]) + float(e.get("offset", 0.0))
        timed.append((start, i, e))
    timed.sort(key=lambda t: (t[0], t[1]))

    starts = [t[0] for t in timed]
    if starts:
        starts[0] = 0.0
    frames = []
    for k in range(len(timed)):
        s = starts[k]
        nxt = starts[k + 1] if k + 1 < len(timed) else total
        dur = max(0.5, nxt - s)
        frames.append((round(s * fps), max(1, round(dur * fps))))

    # ---- assets: copy with sha1 manifest -----------------------------------
    assets_dir = ROOT / "public" / "projects" / out_name / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / "projects" / out_name / "assets_manifest.json"
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    copied = [0]

    def bring(src: Path, dest_name: str) -> str:
        dest = assets_dir / dest_name
        digest = sha1_file(src)
        if manifest.get(dest_name) != digest or not dest.exists():
            shutil.copy2(src, dest)
            manifest[dest_name] = digest
            copied[0] += 1
        return f"assets/{dest_name}"

    # ---- build clips --------------------------------------------------------
    footage_clips = []
    markers = []
    prev_rank = object()
    missing = []
    for k, ((start_f, dur_f), (s, i, e)) in enumerate(zip(frames, timed)):
        asset_ref = None
        motion = "none"
        clip_mp4 = clips_dir / f"clip_{i:02d}.mp4"
        if e.get("video") and clip_mp4.exists():
            asset_ref = bring(clip_mp4, f"clip_{i:02d}.mp4")
        else:
            for ext in ("jpg", "jpeg", "png"):
                p = img_dir / f"slide_{i:02d}.{ext}"
                if p.exists():
                    asset_ref = bring(p, p.name)
                    break
            if asset_ref and e.get("photo") and not e.get("static"):
                motion = "pan"
        if asset_ref is None:
            missing.append(i)
            continue
        # dissolve theo hồ sơ kênh (audience-45plus §2: dissolve ≥0.4s):
        # clip sau chớm sớm `fade` frame và fade-in đè lên clip trước
        fade = 0
        if len(footage_clips) > 0 and prof.get("transition", "dissolve") == "dissolve":
            fade = max(1, round(float(prof.get("transition_dur", 0.4)) * fps))
            fade = min(fade, start_f)  # không âm frame
        footage_clips.append({
            "id": f"slide-{i}", "kind": "video",
            "from": start_f - fade, "durationInFrames": dur_f + fade,
            "asset": asset_ref, "trimStartFrames": 0,
            "fit": "cover", "layout": {}, "motion": motion, "volume": 0,
            "fadeInFrames": fade,
        })
        rank = e.get("rank")
        if rank and rank != prev_rank:
            markers.append({"id": f"m-{i}", "atFrame": start_f, "label": str(rank)})
            prev_rank = rank

    voice_src = video_dir / "voice.wav"
    voice_ref = bring(voice_src, "voice.wav") if voice_src.exists() else None

    captions_lines = [
        {"text": l["text"], "startMs": round(float(l["start"]) * 1000),
         "endMs": round(float(l["end"]) * 1000)}
        for l in lines if l.get("text", "").strip()
    ]

    sub_size = prof.get("sub_size") or 22
    tracks = [
        {"id": "trk-slides", "name": "Slides", "type": "video",
         "muted": False, "hidden": False, "locked": False, "clips": footage_clips},
    ]
    if voice_ref:
        tracks.append({
            "id": "trk-voice", "name": "Voice", "type": "audio",
            "muted": False, "hidden": False, "locked": False,
            "clips": [{"id": "voice-1", "kind": "audio", "from": 0,
                       "durationInFrames": total_frames, "asset": voice_ref,
                       "volume": 1, "trimStartFrames": 0}],
        })

    now = datetime.now(timezone.utc).isoformat()
    project = {
        "version": 1,
        "meta": {"name": out_name, "channel": args.channel,
                 "templateRef": args.channel, "fps": fps,
                 "width": 1920, "height": 1080,
                 "createdAt": now, "modifiedAt": now},
        "timeline": {"durationInFrames": total_frames},
        "sceneMarkers": markers,
        "tracks": tracks,
        "captions": {"source": "srt-interpolated", "style": "outline",
                     "enabled": True, "fontSize": sub_size * 2,
                     "lines": captions_lines, "words": []},
        "theme": {
            "palette": {"bgTop": rgb_hex(pal["bg_top"]),
                        "bgBottom": rgb_hex(pal["bg_bottom"]),
                        "accent": rgb_hex(pal["accent"])},
            "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
            "canvasColor": rgb_hex(pal["bg_top"]),
        },
    }

    out_dir = ROOT / "projects" / out_name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "project.json").write_text(
        json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"OK projects/{out_name}/project.json — {len(footage_clips)} slide clip / "
          f"{len(markers)} marker / {len(captions_lines)} dong phu de / "
          f"{copied[0]} asset copy moi")
    if missing:
        print(f"⚠ {len(missing)} entry KHONG co anh/clip (index: {missing[:10]}...)"
              if len(missing) > 10 else f"⚠ entry thieu asset: {missing}")


if __name__ == "__main__":
    main()
