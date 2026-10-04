# -*- coding: utf-8 -*-
"""vv_word_timing.py — karaoke word timing from VOICEVOX mora lengths. $0, exact.

For each caption line already in the project (timed by timeline.json), call
VOICEVOX /audio_query on the line text and read accent_phrases[].moras[]
consonant/vowel lengths. Mora-duration FRACTIONS are speed-invariant, so we
scale them into the line's real [startMs..endMs] window — no re-synthesis.
Original characters are distributed across accent phrases proportionally to
mora count (kanji have no 1:1 mora mapping; proportional runs read perfectly
as karaoke highlights).

Queries are cached by sha1(engine+style+text) in %TTS_CACHE_DIR% (same dir as
the pipeline's wav cache, "aq_" prefix) — reruns are instant.

Usage:
  py -3 tools/vv_word_timing.py --project cabbage-34 --channel health
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CHANNELS_TOOLS = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
CACHE_DIR = Path(os.environ.get("TTS_CACHE_DIR", r"E:\Claude\Projects\_tts_cache"))

BASES = {"voicevox": "http://127.0.0.1:50021", "aivis": "http://127.0.0.1:10101"}


def api_json(base, method, path, params=None, body=None, timeout=60):
    url = base + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method=method,
                                 data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def audio_query_cached(base, engine, style_id, text):
    key = hashlib.sha1(f"{engine}|{style_id}|{text}".encode("utf-8")).hexdigest()
    cache = CACHE_DIR / f"aq_{key}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    q = api_json(base, "POST", "/audio_query", {"text": text, "speaker": style_id})
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = cache.with_suffix(".part")
    tmp.write_text(json.dumps(q, ensure_ascii=False), encoding="utf-8")
    tmp.replace(cache)
    return q


def phrase_fractions(query):
    """[(mora_count, duration)] per accent phrase; duration at speedScale=1."""
    out = []
    for ap in query.get("accent_phrases", []):
        d = 0.0
        for m in ap.get("moras", []):
            d += (m.get("consonant_length") or 0.0) + (m.get("vowel_length") or 0.0)
        pm = ap.get("pause_mora")
        pause = ((pm.get("consonant_length") or 0.0) + (pm.get("vowel_length") or 0.0)) if pm else 0.0
        out.append((len(ap.get("moras", [])), d, pause))
    return out


def split_line_words(text, phrases, start_ms, end_ms):
    """Distribute original chars across accent phrases ∝ mora count; time by duration."""
    total_moras = sum(p[0] for p in phrases) or 1
    total_dur = sum(p[1] + p[2] for p in phrases) or 1.0
    n = len(text)
    # char allocation ∝ moras, fixed to sum n
    alloc = [max(1, round(n * p[0] / total_moras)) if p[0] else 0 for p in phrases]
    while sum(alloc) > n:
        alloc[alloc.index(max(alloc))] -= 1
    while sum(alloc) < n and alloc:
        alloc[alloc.index(max(alloc))] += 1
    words = []
    ci = 0
    t = float(start_ms)
    span = end_ms - start_ms
    for (moras, dur, pause), take in zip(phrases, alloc):
        seg = text[ci:ci + take]
        ci += take
        w_ms = span * (dur / total_dur)
        p_ms = span * (pause / total_dur)
        if seg:
            words.append({"text": seg, "startMs": round(t), "endMs": round(t + w_ms)})
        t += w_ms + p_ms
    if ci < n and words:
        words[-1]["text"] += text[ci:]
        words[-1]["endMs"] = end_ms
    return words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--channel", required=True)
    args = ap.parse_args()

    sys.path.insert(0, str(CHANNELS_TOOLS))
    import channels as CH  # noqa: E402
    import tts_render as TR  # noqa: E402

    prof = CH.get(args.channel)
    engine = prof.get("engine", "voicevox")
    base = BASES.get(engine, BASES["voicevox"])
    try:
        api_json(base, "GET", "/version")
    except Exception:
        raise SystemExit(
            f"[LOI] engine {engine} chua chay o {base} — mo VOICEVOX (E:\\VOICEVOX) roi chay lai")
    speakers = api_json(base, "GET", "/speakers")
    _sp, _st, style_id = TR.resolve_style(speakers, prof["speaker"], prof.get("style"))

    proj_path = ROOT / "projects" / args.project / "project.json"
    project = json.loads(proj_path.read_text(encoding="utf-8"))
    lines = project.get("captions", {}).get("lines", [])
    if not lines:
        raise SystemExit("[LOI] project khong co captions.lines — import truoc da")

    all_words = []
    for i, line in enumerate(lines):
        text = re.sub(r"\s+", "", line["text"])
        if not text:
            continue
        try:
            q = audio_query_cached(base, engine, style_id, text)
        except Exception as e:  # noqa: BLE001
            print(f"  ⚠ dong {i}: audio_query loi ({e}) — bo qua")
            continue
        phrases = phrase_fractions(q)
        if not phrases:
            continue
        for w in split_line_words(text, phrases, line["startMs"], line["endMs"]):
            w["lineIndex"] = i
            all_words.append(w)
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(lines)} dong…")

    project["captions"]["words"] = all_words
    project["captions"]["source"] = "voicevox-mora"
    proj_path.write_text(json.dumps(project, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"OK — {len(all_words)} tu karaoke cho {len(lines)} dong "
          f"(engine {engine}, style {style_id})")


if __name__ == "__main__":
    main()
