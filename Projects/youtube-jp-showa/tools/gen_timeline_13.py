# -*- coding: utf-8 -*-
"""Chi dung VOICE + timeline.json + subs.srt cho video 12 (KHONG dung video).

Vi sao can buoc rieng: SLIDES cue-cung can GIAY THAT cua tung dong, ma
video_render.py doi co SLIDES.json truoc khi chay voice (preflight) => vong tron.
CLAUDE.md §San xuat: "moi gate thoi gian chi chot tu timeline.json SAU render".
"""
import sys, json, types
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HEALTH = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
sys.path.insert(0, str(HEALTH))
import video_render as VR          # noqa: E402
import channels as CH              # noqa: E402

STEM = "13_kosodate-joushiki"
SHOWA = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = SHOWA / "03_SCRIPTS" / (STEM + "_TTS.md")
OUT = SHOWA / "06_VIDEO" / STEM
OUT.mkdir(parents=True, exist_ok=True)

prof = CH.get("showa")
args = types.SimpleNamespace(
    engine=prof["engine"], speaker=prof["speaker"], style=prof["style"],
    speed=prof["speed"], intonation=prof["intonation"],
    gap=0.6, section_gap=1.1, speaker2=None, style2=None, voice_af=None,
)

print("[VOICE] %s | %s/%s/%s" % (STEM, prof["speaker"], prof["style"], prof["speed"]))
timeline, total = VR.render_audio_timeline(TTS, OUT / "voice.wav", args)
(OUT / "timeline.json").write_text(
    json.dumps({"total": total, "lines": timeline}, ensure_ascii=False, indent=1),
    encoding="utf-8")

# phu de: outline + sub_size 22 => maxlen theo dung cong thuc cua video_render
maxlen = max(24, int(VR.SUB_MAXLEN * 17 / prof["sub_size"]))
VR.write_srt(timeline, OUT / "subs.srt", maxlen)

print("\n=== XONG ===")
print("dong        : %d" % len(timeline))
print("tong thoi luong: %.1fs = %.2f phut" % (total, total / 60))
print("timeline    : %s" % (OUT / "timeline.json"))
