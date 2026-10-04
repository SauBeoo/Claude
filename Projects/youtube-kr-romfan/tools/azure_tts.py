# -*- coding: utf-8 -*-
"""
azure_tts.py — Render Korean TTS voice track from a _TTS.md script (youtube-kr-romfan).

Reads a plain-Korean script (one paragraph per line block), splits it into
sentences, synthesizes each sentence via Azure Speech REST (region koreacentral,
tier F0), and produces:

    03_VOICE/<slug>/voice.wav      full voice track (24kHz 16bit mono)
    03_VOICE/<slug>/subs.srt       per-sentence subtitles, synced to audio
    03_VOICE/<slug>/timeline.json  per-sentence start/end (for video render)
    03_VOICE/<slug>/segs/          cached per-sentence wav (resume-safe)

Voices (fixed for kênh 사우 오디오, chốt 2026-07-10, cập nhật 2026-07-11):
    default narration  ko-KR-SunHiNeural          (nữ chính, ngôi 나)
    [속]               ko-KR-SunHiNeural -10Hz    (nội tâm/속마음 — hạ pitch nhẹ)
    [감]               ko-KR-SunHiNeural -10Hz    (nhịp cảm xúc 정/cao trào —
                       chậm -7%, ngắt nghẹn comma 430ms, nghỉ dài +0.35s)
    [남]               ko-KR-InJoonNeural -15Hz   (nam chính, hạ tông)
    [시모]             ko-KR-SoonBokNeural        (mẹ chồng / bà lớn tuổi)
    [회장]             ko-KR-BongJinNeural        (회장님 / phát thanh viên)
    [여2]              ko-KR-SeoHyeonNeural       (nữ phụ / 백여우)
A voice tag at the start of a paragraph applies to that whole paragraph.
Default output is single-voice SunHi; [속] is expected in every script,
other tags only appear when user asked for multi-voice.

Channel-standard prosody (user chốt 2026-07-11, sau A/B rate -5/-12/-18):
    rate -12% | gap 0.35s | pgap 1.0s | comma break 250ms
These are the defaults below — run without flags to get the standard.

Usage:
    python tools/azure_tts.py 02_SCRIPTS/01_slug_TTS.md
    python tools/azure_tts.py <file> --limit 10          # quick test, first 10 sentences
    python tools/azure_tts.py <file> --rate -5 --out 03_VOICE/custom

Credentials: env AZURE_SPEECH_KEY / AZURE_SPEECH_REGION, fallback file
tools/.azure_key (line 1 = key, line 2 = region). Never commit the key.
"""
import argparse
import http.client
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

SAMPLE_RATE = 24000
OUTPUT_FORMAT = "riff-24khz-16bit-mono-pcm"

# Optional per-voice prosody knobs (emotional delivery):
#   rate_delta  : added to --rate for this voice (slower = more feeling)
#   comma_ms    : override comma <break> (None = use --comma-break)
#   prebreak_ms : leading pause before the line (a "breath in")
#   gap_bonus   : extra silence (s) appended after the line
VOICES = {
    "여":   {"name": "ko-KR-SunHiNeural",    "pitch": "0Hz"},
    "속":   {"name": "ko-KR-SunHiNeural",    "pitch": "-10Hz"},
    # [감] = nhịp cảm xúc (정/cao trào): chậm hơn, hạ tông, ngắt nghẹn, nghỉ dài
    "감":   {"name": "ko-KR-SunHiNeural",    "pitch": "-10Hz",
             "rate_delta": -7, "comma_ms": 430, "prebreak_ms": 180, "gap_bonus": 0.35},
    "남":   {"name": "ko-KR-InJoonNeural",   "pitch": "-15Hz"},
    "시모": {"name": "ko-KR-SoonBokNeural",  "pitch": "0Hz"},
    "회장": {"name": "ko-KR-BongJinNeural",  "pitch": "0Hz"},
    "여2":  {"name": "ko-KR-SeoHyeonNeural", "pitch": "0Hz"},
}
DEFAULT_VOICE = "여"

TAG_RE = re.compile(r"^\[(\S+?)\]\s*")
# sentence = run of text ending in .?!… (plus closing quote), or remainder of line
SENT_RE = re.compile(r'[^.?!…\n]+[.?!…]+["”\'』」)]?|[^.?!…\n]+$')


def get_credentials():
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    key_file = Path(__file__).resolve().parent / ".azure_key"
    if (not key or not region) and key_file.exists():
        lines = key_file.read_text(encoding="utf-8").split()
        if not key and len(lines) >= 1:
            key = lines[0]
        if not region and len(lines) >= 2:
            region = lines[1]
    if not key:
        sys.exit("ERROR: no Azure key (env AZURE_SPEECH_KEY or tools/.azure_key)")
    return key, region or "koreacentral"


def parse_script(path):
    """Return list of segments: {text, voice, par_end(bool)}."""
    raw = Path(path).read_text(encoding="utf-8")
    segments = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line == "---":
            continue
        voice = DEFAULT_VOICE
        m = TAG_RE.match(line)
        if m:
            tag = m.group(1)
            if tag in VOICES:
                voice = tag
                line = line[m.end():]
            else:
                print(f"WARN: unknown voice tag [{tag}] — read by default voice")
                line = line[m.end():]
        if not line:
            continue
        sents = [s.strip() for s in SENT_RE.findall(line) if s.strip()]
        for i, s in enumerate(sents):
            segments.append({"text": s, "voice": voice,
                             "par_end": i == len(sents) - 1})
    return segments


def xml_escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def synth(text, voice_key, rate_pct, key, region, comma_break_ms=250,
          prebreak_ms=0, max_retries=6):
    v = VOICES[voice_key]
    body = xml_escape(text)
    if comma_break_ms > 0:
        body = body.replace(",", f",<break time='{comma_break_ms}ms'/>")
    if prebreak_ms > 0:
        body = f"<break time='{prebreak_ms}ms'/>" + body
    ssml = (f"<speak version='1.0' xml:lang='ko-KR'>"
            f"<voice name='{v['name']}'>"
            f"<prosody rate='{rate_pct:+d}%' pitch='{v['pitch']}'>"
            f"{body}</prosody></voice></speak>")
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    req = urllib.request.Request(url, data=ssml.encode("utf-8"), headers={
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": OUTPUT_FORMAT,
        "User-Agent": "kr-romfan-render",
    })
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:  # F0 throttle
                wait = int(e.headers.get("Retry-After") or 0) or attempt * 5
                print(f"  429 throttled — wait {wait}s (attempt {attempt})")
                time.sleep(wait)
                continue
            body = e.read().decode("utf-8", "replace")[:300]
            raise RuntimeError(f"Azure HTTP {e.code}: {body}") from e
        except (urllib.error.URLError, TimeoutError,
                http.client.IncompleteRead, ConnectionError) as e:
            if attempt < max_retries:
                time.sleep(attempt * 3)
                continue
            raise


def wav_frames(data):
    with wave.open(io.BytesIO(data)) as w:
        assert w.getframerate() == SAMPLE_RATE and w.getnchannels() == 1
        return w.readframes(w.getnframes())


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", help="path to _TTS.md")
    ap.add_argument("--out", help="output dir (default 03_VOICE/<slug>)")
    ap.add_argument("--rate", type=int, default=-12, help="prosody rate %% (channel std -12)")
    ap.add_argument("--gap", type=float, default=0.35, help="pause between sentences (s)")
    ap.add_argument("--pgap", type=float, default=1.0, help="pause between paragraphs (s)")
    ap.add_argument("--comma-break", type=int, default=250,
                    help="break (ms) inserted at commas, 0=off (channel std 250)")
    ap.add_argument("--limit", type=int, help="render only first N sentences (test)")
    ap.add_argument("--delay", type=float, default=0.3, help="delay between API calls (s)")
    args = ap.parse_args()

    key, region = get_credentials()
    script = Path(args.script)
    slug = script.stem.replace("_TTS", "")
    out_dir = Path(args.out) if args.out else script.parent.parent / "03_VOICE" / slug
    segs_dir = out_dir / "segs"
    segs_dir.mkdir(parents=True, exist_ok=True)

    segments = parse_script(script)
    if args.limit:
        segments = segments[:args.limit]
    total_chars = sum(len(s["text"].replace(" ", "")) for s in segments)
    print(f"{len(segments)} sentences, {total_chars} hangul chars (F0 quota 500k/month)")

    # synthesize (resume: skip cached segs)
    api_chars = 0
    for i, seg in enumerate(segments):
        seg_path = segs_dir / f"seg_{i:04d}.wav"
        if seg_path.exists() and seg_path.stat().st_size > 44:
            continue
        v = VOICES[seg["voice"]]
        eff_rate = args.rate + v.get("rate_delta", 0)
        comma = v["comma_ms"] if v.get("comma_ms") is not None else args.comma_break
        audio = synth(seg["text"], seg["voice"], eff_rate, key, region,
                      comma_break_ms=comma, prebreak_ms=v.get("prebreak_ms", 0))
        seg_path.write_bytes(audio)
        api_chars += len(seg["text"])
        if (i + 1) % 20 == 0 or i == len(segments) - 1:
            print(f"  {i+1}/{len(segments)}")
        time.sleep(args.delay)

    # concat + timeline
    timeline = []
    t = 0.0
    with wave.open(str(out_dir / "voice.wav"), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(SAMPLE_RATE)
        for i, seg in enumerate(segments):
            frames = wav_frames((segs_dir / f"seg_{i:04d}.wav").read_bytes())
            dur = len(frames) / 2 / SAMPLE_RATE
            timeline.append({"i": i, "text": seg["text"], "voice": seg["voice"],
                             "start": round(t, 3), "end": round(t + dur, 3)})
            out.writeframes(frames)
            t += dur
            base = args.pgap if seg["par_end"] else args.gap
            pause_dur = base + VOICES[seg["voice"]].get("gap_bonus", 0.0)
            pause = b"\x00\x00" * int(SAMPLE_RATE * pause_dur)
            out.writeframes(pause)
            t += len(pause) / 2 / SAMPLE_RATE

    (out_dir / "timeline.json").write_text(
        json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    srt = []
    for n, e in enumerate(timeline, 1):
        srt.append(f"{n}\n{srt_time(e['start'])} --> {srt_time(e['end'])}\n{e['text']}\n")
    (out_dir / "subs.srt").write_text("\n".join(srt), encoding="utf-8")

    # quota log + speed coefficient
    log = out_dir.parent / "QUOTA.log"
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M')}\t{slug}\t{api_chars} chars sent\n")
    minutes = t / 60
    print(f"DONE {out_dir / 'voice.wav'}")
    print(f"duration {int(t//60)}m{int(t%60):02d}s | {total_chars} chars "
          f"| {total_chars/minutes:.0f} chars/min (target 220-260)")


if __name__ == "__main__":
    main()
