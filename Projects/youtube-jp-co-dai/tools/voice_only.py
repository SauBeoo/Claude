# -*- coding: utf-8 -*-
r"""Chi chay KHAU VOICE cua video_render.py: voice.wav + timeline.json + subs.srt.

Vi sao co file nay: `import_pipeline.py` cua remotion-vox doi `06_VIDEO/<stem>/timeline.json`
(hop dong dong bo), nhung `video_render.py` khong co co --voice-only — chay no la render
luon ca VIDEO (~30 phut CPU) trong khi phan HINH da giao cho remotion. Wrapper nay dung
dung ham cua video_render nen timeline sinh ra GIONG HET ban render pipeline.

    python tools\voice_only.py 04_SCRIPTS\x_TTS.md --channel co-dai
"""
import argparse, io, json, sys
from pathlib import Path

# 🔴 write_through=True BAT BUOC: TextIOWrapper tu tao la BLOCK-BUFFERED, nen
#    PYTHONUNBUFFERED=1 KHONG con tac dung => log ra 0 byte suot ca lan chay
#    va nhin nhu tien trinh treo (dinh that 2026-08-16, mat mot vong truy nguyen).
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)
HT = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
sys.path.insert(0, str(HT))

import channels as CH          # noqa: E402
import video_render as VR      # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tts")
    ap.add_argument("--channel", choices=list(CH.CHANNELS), required=True)
    ap.add_argument("--reuse", action="store_true")
    a = ap.parse_args()

    prof = CH.CHANNELS[a.channel]
    tts_path = Path(a.tts).resolve()
    stem = tts_path.stem.replace("_TTS", "")
    root = tts_path.parent.parent
    vd = root / "06_VIDEO" / stem
    vd.mkdir(parents=True, exist_ok=True)

    # Namespace toi thieu ma render_audio_timeline + write_srt can, lay tu HO SO KENH
    # (channels.py la nguon su that — CLAUDE.md §Renderer co ho so kenh).
    ns = argparse.Namespace(
        engine=prof.get("engine", "voicevox"),
        speaker=prof.get("speaker", "青山龍星"),
        speed=prof.get("speed", 0.9),
        intonation=prof.get("intonation", 1.15),
        gap=prof.get("gap", 0.6),
        section_gap=prof.get("section_gap", 1.1),
        style=prof.get("style"),
        voice_af=prof.get("voice_af"),
    )
    print(f"[hồ sơ] {a.channel}: {ns.speaker} / {ns.style or 'ノーマル'} / "
          f"speed {ns.speed} / intonation {ns.intonation}")

    wav = vd / "voice.wav"
    tl = vd / "timeline.json"
    if a.reuse and tl.exists():
        d = json.loads(tl.read_text(encoding="utf-8"))
        timeline, total = d["lines"], d["total"]
        print(f"Dùng lại timeline: {len(timeline)} dòng, {total/60:.1f} phút")
    else:
        timeline, total = VR.render_audio_timeline(tts_path, wav, ns)
        tl.write_text(json.dumps({"total": total, "lines": timeline},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nVoice → {wav} ({total/60:.1f} phút)")

    sub_size = prof.get("sub_size")
    maxlen = VR.SUB_MAXLEN if not sub_size else max(24, int(VR.SUB_MAXLEN * 17 / sub_size))
    VR.write_srt(timeline, vd / "subs.srt", maxlen)
    print(f"subs.srt → {vd/'subs.srt'} (maxlen {maxlen})")
    print(f"timeline.json → {tl}  ({len(timeline)} dòng / {total/60:.2f} phút)")


if __name__ == "__main__":
    main()
