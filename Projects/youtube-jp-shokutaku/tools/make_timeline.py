# -*- coding: utf-8 -*-
r"""Sinh 06_VIDEO/<stem>/timeline.json + subs.srt tu file _TTS.md, KHONG render video.

    python tools\make_timeline.py 20_nokosoku-kasabuta

Vi sao co tool nay (2026-08-25): pipeline remotion-vox can `timeline.json`
(sync contract) nhung chi `video_render.py` sinh no — va chay video_render thi
no render CA VIDEO, trong khi anh minh hoa chua gen xong. `tts_render.py` thi
chi xuat voice.wav, khong co timeline.

Tool nay goi dung ham `render_audio_timeline` cua video_render.py nen timing
GIONG HET ban render that. Cache TTS theo noi dung (Projects\_tts_cache) khien
lan chay thu hai gan nhu tuc thi — khong synth lai.

Thu tu dung trong pipeline kenh:
    1. tools\build_slides_NN.py            -> SLIDES.json + prompt
    2. run_voiceNN.cmd (nen)               -> voice.wav
    3. tools\make_timeline.py <stem>       -> timeline.json + subs.srt   <-- day
    4. ...\remotion-vox\tools\import_pipeline.py --stem <stem> --channel shokutaku
"""
import argparse
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
HEALTH_TOOLS = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
sys.path.insert(0, str(HEALTH_TOOLS))

import video_render as VR  # noqa: E402


def srt_time(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem", help="vd 20_nokosoku-kasabuta")
    ap.add_argument("--engine", default="voicevox")
    ap.add_argument("--speaker", default="青山龍星")
    ap.add_argument("--speed", type=float, default=0.8)
    ap.add_argument("--intonation", type=float, default=1.15)
    ap.add_argument("--gap", type=float, default=0.6)
    ap.add_argument("--section-gap", type=float, default=1.1)
    ap.add_argument("--style", default=None)
    ap.add_argument("--voice-af", default=None)
    a = ap.parse_args()

    tts = ROOT / "04_SCRIPTS" / f"{a.stem}_TTS.md"
    if not tts.exists():
        raise SystemExit(f"[LOI] khong thay {tts}")
    vd = ROOT / "06_VIDEO" / a.stem
    vd.mkdir(parents=True, exist_ok=True)
    wav = vd / "voice.wav"

    timeline, total = VR.render_audio_timeline(tts, wav, a)
    (vd / "timeline.json").write_text(
        json.dumps({"total": total, "lines": timeline}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    # subs.srt — cat cue theo dung luat kenh (<=2 dong, SUB_MAXLEN cua video_render)
    cues = VR.build_subs(timeline, VR.SUB_MAXLEN) if hasattr(VR, "build_subs") else None
    if cues is None:
        cues = [(c["start"], c["end"], c["text"]) for c in timeline]
    out = []
    for i, c in enumerate(cues, 1):
        st, en, tx = (c if isinstance(c, tuple) else (c["start"], c["end"], c["text"]))
        out.append(f"{i}\n{srt_time(st)} --> {srt_time(en)}\n{tx}\n")
    (vd / "subs.srt").write_text("\n".join(out), encoding="utf-8")

    print(f"OK  timeline {len(timeline)} dong | {int(total)//60}'{int(total)%60:02d}")
    print(f"    -> {(vd / 'timeline.json').relative_to(ROOT)}")
    print(f"    -> {(vd / 'subs.srt').relative_to(ROOT)}  ({len(out)} cue)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
