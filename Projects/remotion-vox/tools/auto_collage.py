# -*- coding: utf-8 -*-
"""auto_collage.py — audio (+script) → draft Vox-collage project.json.

Automates the vox-collage-video skill flow, data-driven:
  1. timestamps: subs.srt if given (each block = one scene) else Whisper local
  2. scenes → background/hero/support/tag/punch/sfx clips on tracks
  3. images: Pexels fetch per scene query (needs a PLAN file for good queries)
     → rembg cutout via the existing skill script process_cutout.py
  4. SFX: ensured via generate_sfx.py (shared public/sfx)
  5. entrance variants rotate — never the same on two consecutive scenes

The PLAN file (--plan plan.json) carries the creative choices (usually
authored by Claude in the skill): [{tag, tagColor?, splash?, punch,
punchAtSec?, heroQuery|heroFile, supportQueries?, variant?}] — matched to
scenes by index. Without a plan, a skeleton project is still produced
(scenes, tags from text, captions, voice) with no images: fill in the editor.

Usage:
  py -3 tools/auto_collage.py --audio voice.mp3 --srt subs.srt --out my-video
      [--plan plan.json] [--script script.md] [--fps 30] [--lang ja]
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SKILL_SCRIPTS = Path(r"E:\Claude\.claude\skills\vox-collage-video\scripts")
PEXELS_KEY_FILE = Path(r"E:\Claude\Projects\youtube-jp-health\tools\.pexels_key")

VARIANT_ROTATION = ["rise", "grow", "flip", "punch", "wobble", "peel", "zoom-through"]
SPLASHES = [
    ["#7CB518", "#4EC3E0"], ["#4EC3E0", "#FFE01B"], ["#FF8C42", "#B8B8D1"],
    ["#2EC46F", "#FFE01B"], ["#FF5E5B", "#4EC3E0"], ["#B388EB", "#FFE01B"],
]
TAG_COLORS = ["#FFE01B", "#4EC3E0", "#FF8C42", "#2EC46F", "#FF5E5B", "#B388EB"]
ENTRANCE_SFX = {
    "rise": "whoosh", "grow": "paper", "punch": "thud", "flip": "whoosh",
    "wobble": "boing", "peel": "paper", "zoom-through": "riser",
    "spiral": "riser", "pop": "pop",
}
SUPPORT_SLOTS = [(1400, 520, 440), (140, 600, 300), (1500, 300, 320)]


def parse_srt(path: Path):
    txt = path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", txt.strip())
    scenes = []
    ts = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")
    for b in blocks:
        m = ts.search(b)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        lines = [l for l in b.splitlines() if not ts.search(l) and not l.strip().isdigit()]
        text = " ".join(l.strip() for l in lines if l.strip())
        if text:
            scenes.append({"start": start, "end": end, "text": text})
    return scenes


def whisper_scenes(audio: Path, lang: str):
    try:
        from faster_whisper import WhisperModel  # type: ignore
        model = WhisperModel("small", compute_type="int8")
        segs, _ = model.transcribe(str(audio), language=lang)
        return [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs]
    except ImportError:
        pass
    try:
        import whisper  # type: ignore
        model = whisper.load_model("small")
        r = model.transcribe(str(audio), language=lang)
        return [{"start": s["start"], "end": s["end"], "text": s["text"].strip()}
                for s in r["segments"]]
    except ImportError:
        raise SystemExit(
            "[LOI] khong co subs.srt va khong co Whisper. Cai: pip install faster-whisper")


def pexels_fetch(query: str, dest: Path) -> bool:
    key = os.environ.get("PEXELS_API_KEY") or (
        PEXELS_KEY_FILE.read_text().strip() if PEXELS_KEY_FILE.exists() else None)
    if not key:
        print(f"  ⚠ khong co Pexels key — bo qua '{query}'")
        return False
    url = f"https://api.pexels.com/v1/search?query={urllib.request.quote(query)}&per_page=3"
    req = urllib.request.Request(url, headers={
        "Authorization": key,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # 403 without UA
    })
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        photos = data.get("photos", [])
        if not photos:
            print(f"  ⚠ Pexels 0 ket qua: '{query}'")
            return False
        src = photos[0]["src"]["large2x"]
        req2 = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        dest.write_bytes(urllib.request.urlopen(req2, timeout=60).read())
        credit = f"{dest.name}: {photos[0]['url']} (Pexels, {photos[0]['photographer']})\n"
        with open(dest.parent / "ATTRIBUTIONS.txt", "a", encoding="utf-8") as f:
            f.write(credit)
        return True
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠ Pexels loi '{query}': {e}")
        return False


def cutout(raw: Path, out: Path) -> bool:
    script = SKILL_SCRIPTS / "process_cutout.py"
    r = subprocess.run([sys.executable, str(script), str(raw), str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ⚠ cutout loi {raw.name}: {r.stderr[-200:]}")
        return False
    if "SPARSE" in (r.stdout or ""):
        print(f"  ⚠ SPARSE canh bao: {raw.name} — nen doi query nen trang")
    return True


def ensure_sfx():
    sfx_dir = ROOT / "public" / "sfx"
    if any(sfx_dir.glob("*.wav")):
        return
    sfx_dir.mkdir(parents=True, exist_ok=True)
    script = SKILL_SCRIPTS / "generate_sfx.py"
    subprocess.run([sys.executable, str(script), str(sfx_dir)], check=False)


def short_punch(text: str) -> str:
    parts = re.split(r"[、。！？,.!?]", text)
    parts = [p.strip() for p in parts if p.strip()]
    return min(parts, key=len)[:18] if parts else text[:14]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--srt", default=None)
    ap.add_argument("--script", default=None, help="script text (tham khao, khong bat buoc)")
    ap.add_argument("--plan", default=None, help="scene plan JSON (tag/punch/query per scene)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--lang", default="ja")
    ap.add_argument("--paper", default=None, help="paper texture file (optional)")
    args = ap.parse_args()

    audio = Path(args.audio)
    if not audio.exists():
        raise SystemExit(f"[LOI] khong thay audio: {audio}")

    scenes = parse_srt(Path(args.srt)) if args.srt else whisper_scenes(audio, args.lang)
    if not scenes:
        raise SystemExit("[LOI] 0 scene")
    total = scenes[-1]["end"]
    fps = args.fps
    total_frames = round(total * fps)
    print(f"{len(scenes)} scene / {total:.1f}s")

    plan = []
    if args.plan:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8-sig"))

    assets_dir = ROOT / "public" / "projects" / args.out / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = ROOT / "projects" / args.out / "_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(audio, assets_dir / f"audio{audio.suffix.lower()}")
    audio_ref = f"assets/audio{audio.suffix.lower()}"
    paper_ref = None
    if args.paper and Path(args.paper).exists():
        shutil.copy2(args.paper, assets_dir / "paper.jpg")
        paper_ref = "assets/paper.jpg"
    ensure_sfx()

    tracks = {
        "bg": {"id": "trk-bg", "name": "Background", "type": "background",
               "muted": False, "hidden": False, "locked": False, "clips": []},
        "hero": {"id": "trk-hero", "name": "Hero", "type": "sticker",
                 "muted": False, "hidden": False, "locked": False, "clips": []},
        "sup1": {"id": "trk-sup1", "name": "Support 1", "type": "sticker",
                 "muted": False, "hidden": False, "locked": False, "clips": []},
        "sup2": {"id": "trk-sup2", "name": "Support 2", "type": "sticker",
                 "muted": False, "hidden": False, "locked": False, "clips": []},
        "tag": {"id": "trk-tag", "name": "Tag", "type": "text",
                "muted": False, "hidden": False, "locked": False, "clips": []},
        "punch": {"id": "trk-punch", "name": "Punch", "type": "text",
                  "muted": False, "hidden": False, "locked": False, "clips": []},
        "voice": {"id": "trk-voice", "name": "Voice", "type": "audio",
                  "muted": False, "hidden": False, "locked": False, "clips": []},
        "sfx": {"id": "trk-sfx", "name": "SFX", "type": "audio",
                "muted": False, "hidden": False, "locked": False, "clips": []},
    }
    markers = []
    prev_variant = None

    for k, sc in enumerate(scenes):
        F = round(sc["start"] * fps)
        D = max(1, round((sc["end"] - sc["start"]) * fps))
        p = plan[k] if k < len(plan) else {}

        variant = p.get("variant")
        if not variant:
            pool = [v for v in VARIANT_ROTATION if v != prev_variant]
            variant = pool[k % len(pool)]
        prev_variant = variant

        tag = p.get("tag") or re.sub(r"[、。「」『』！？…・—―\-\s]", "", sc["text"])[:4] or f"#{k+1}"
        tag_color = p.get("tagColor") or TAG_COLORS[k % len(TAG_COLORS)]
        splash = p.get("splash") or SPLASHES[k % len(SPLASHES)]
        punch = p.get("punch") or short_punch(sc["text"])
        punch_at = round(float(p.get("punchAtSec", (sc["end"] - sc["start"]) * 0.45)) * fps)
        punch_at = min(punch_at, D - 10) if D > 20 else max(0, D - 10)

        markers.append({"id": f"scene-{k+1}", "atFrame": F, "label": tag})
        tracks["bg"]["clips"].append({
            "id": f"bg-{k+1}", "kind": "background", "from": F, "durationInFrames": D,
            "paper": paper_ref, "tint": "#F2EDE4", "tintOpacity": 0.55,
            "grid": True, "dots": True, "splash": splash,
        })

        # hero image: file given > query > none
        hero_ref = None
        if p.get("heroFile") and Path(p["heroFile"]).exists():
            dst = assets_dir / f"el_hero{k+1}.png"
            shutil.copy2(p["heroFile"], dst)
            hero_ref = f"assets/{dst.name}"
        elif p.get("heroQuery"):
            raw = raw_dir / f"raw_hero{k+1}.jpg"
            cut = assets_dir / f"el_hero{k+1}.png"
            print(f"scene {k+1}: hero '{p['heroQuery']}'")
            if pexels_fetch(p["heroQuery"], raw) and cutout(raw, cut):
                hero_ref = f"assets/{cut.name}"
        if hero_ref:
            tracks["hero"]["clips"].append({
                "id": f"hero-{k+1}", "kind": "sticker", "from": F, "durationInFrames": D,
                "asset": hero_ref,
                "layout": {"x": 420, "y": 180, "w": 1200, "rotation": 0, "opacity": 1},
                "entrance": {"variant": variant, "delayFrames": 0, "params": {}},
                "exit": None, "idle": {"amp": 6, "phase": 0}, "shadow": "lg",
            })

        for j, q in enumerate((p.get("supportQueries") or [])[:3]):
            raw = raw_dir / f"raw_sup{k+1}_{j+1}.jpg"
            cut = assets_dir / f"el_sup{k+1}_{j+1}.png"
            print(f"scene {k+1}: support '{q}'")
            if not (pexels_fetch(q, raw) and cutout(raw, cut)):
                continue
            sx, sy, sw = SUPPORT_SLOTS[j % len(SUPPORT_SLOTS)]
            delay = 12 + j * 10
            lane = tracks["sup1"] if j % 2 == 0 else tracks["sup2"]
            lane["clips"].append({
                "id": f"sup-{k+1}-{j+1}", "kind": "sticker",
                "from": F + delay, "durationInFrames": max(1, D - delay),
                "asset": f"assets/{cut.name}",
                "layout": {"x": sx, "y": sy, "w": sw,
                           "rotation": 4 if j % 2 else -5, "opacity": 1},
                "entrance": {"variant": "pop", "delayFrames": 0, "params": {}},
                "exit": None, "idle": {"amp": 4, "phase": 2.1 * (j + 1)}, "shadow": "sm",
            })

        tracks["tag"]["clips"].append({
            "id": f"tag-{k+1}", "kind": "text", "from": F + 4,
            "durationInFrames": max(1, D - 4),
            "content": tag, "preset": "tag", "color": tag_color,
            "animation": "pop-swing" if variant == "flip" else "pop",
            "animationParams": {"damping": 11, "stiffness": 180, "restDeg": -2},
            "layout": {}, "fontSize": None,
        })
        tracks["punch"]["clips"].append({
            "id": f"punch-{k+1}", "kind": "text", "from": F + punch_at,
            "durationInFrames": max(1, D - punch_at),
            "content": punch, "preset": "punch", "color": "#FFE01B",
            "animation": "pop", "animationParams": {"restDeg": -1.5},
            "layout": {}, "fontSize": None,
        })

        sfx_name = ENTRANCE_SFX.get(variant, "whoosh")
        for name, at, vol in [(sfx_name, 0, 0.45), ("pop", 6, 0.4),
                              ("click", punch_at, 0.45)]:
            tracks["sfx"]["clips"].append({
                "id": f"sfx-{k+1}-{name}-{at}", "kind": "audio",
                "from": F + at,
                "durationInFrames": min(60, max(1, total_frames - (F + at))),
                "asset": f"sfx/{name}.wav", "volume": vol, "trimStartFrames": 0,
            })

    tracks["voice"]["clips"].append({
        "id": "voice-1", "kind": "audio", "from": 0, "durationInFrames": total_frames,
        "asset": audio_ref, "volume": 1, "trimStartFrames": 0,
    })

    now = datetime.now(timezone.utc).isoformat()
    project = {
        "version": 1,
        "meta": {"name": args.out, "channel": None, "templateRef": None,
                 "fps": fps, "width": 1920, "height": 1080,
                 "createdAt": now, "modifiedAt": now},
        "timeline": {"durationInFrames": total_frames},
        "sceneMarkers": markers,
        "tracks": [tracks[k] for k in
                   ("bg", "hero", "sup1", "sup2", "tag", "punch", "voice", "sfx")],
        "captions": {"source": "srt-interpolated", "style": "outline",
                     "enabled": False, "fontSize": 44,
                     "lines": [{"text": s["text"],
                                "startMs": round(s["start"] * 1000),
                                "endMs": round(s["end"] * 1000)} for s in scenes],
                     "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F2EDE4"},
    }
    out_dir = ROOT / "projects" / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "project.json").write_text(
        json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    n_hero = len(tracks["hero"]["clips"])
    print(f"OK projects/{args.out}/project.json — {len(scenes)} scene / "
          f"{n_hero} hero / {len(tracks['sfx']['clips'])} sfx cue")
    if n_hero < len(scenes):
        print(f"⚠ {len(scenes) - n_hero} scene chua co hero — mo editor dien tay, "
              f"hoac chay lai voi --plan co heroQuery")


if __name__ == "__main__":
    main()
