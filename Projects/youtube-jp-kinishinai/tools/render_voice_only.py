# -*- coding: utf-8 -*-
"""render_voice_only.py — chi render VOICE + timeline.json + subs.srt, chua dung hinh.

Vi sao: video_render.py chan o preflight (thieu anh) TRUOC khau voice. Can voice truoc de:
do moc giay THAT cho SLIDES, dung clip chu hien dan (make_cards_k.py can times + _dur).
Goi dung ham cua renderer (render_audio_timeline / write_srt) + ho so kenh trong channels.py,
nen timeline.json cung dinh dang => video_render.py --channel kinishinai --reuse doc lai duoc.
Chay: python tools/render_voice_only.py 01_kuchiguse-hitonome
"""
import sys, io, json, argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
TOOLS = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
sys.path.insert(0, str(TOOLS))
import channels as CH          # noqa: E402
import video_render as VR       # noqa: E402


def main():
    stem = sys.argv[1]
    prof = CH.get("kinishinai")
    a = argparse.Namespace(engine=prof["engine"], speaker=prof["speaker"], style=prof.get("style"),
                           speed=prof["speed"], intonation=prof["intonation"], gap=0.6, section_gap=1.1,
                           speaker2=None, style2=None)
    tts = PROJ / "03_SCRIPTS" / f"{stem}_TTS.md"
    vd = PROJ / "06_VIDEO" / stem
    vd.mkdir(parents=True, exist_ok=True)
    print(f"[KENH] {prof['name']} · {a.speaker}/{a.style} · speed {a.speed} · intonation {a.intonation}")
    timeline, total = VR.render_audio_timeline(tts, vd / "voice.wav", a)
    (vd / "timeline.json").write_text(json.dumps({"total": total, "lines": timeline}, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    maxlen = max(24, int(VR.SUB_MAXLEN * 17 / prof["sub_size"])) if prof.get("sub_size") else VR.SUB_MAXLEN
    VR.write_srt(timeline, vd / "subs.srt", maxlen)
    print(f"\nVoice -> {vd/'voice.wav'} ({total/60:.2f} phut) · {len(timeline)} dong · subs.srt")


if __name__ == "__main__":
    main()
