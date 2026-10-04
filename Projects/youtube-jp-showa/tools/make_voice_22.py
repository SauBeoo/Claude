# -*- coding: utf-8 -*-
"""Buoc GIONG DOC rieng cho video 22 — chay TRUOC khi co SLIDES.

Port tu `make_voice_16.py`, doi DUNG HAI THU: STEM va CH.
  16 = truc A (showa      / VOICEVOX     :50021 / 東北イタコ)
  17 = truc B (showa-b    / AivisSpeech  :10101 / 阿井田 茂 / Calm)   <- bai nay la tien+che do

🔴 VI SAO PHAI CO BUOC NAY (giu nguyen ghi chu cua ban 16):
   `video_render.py` doi co SLIDES truoc ca khau giong, nhung `build_slides_*.py`
   lai phai doc `timeline.json` — thu chi co SAU khi tong hop giong. Vong tron.
   ⛔ Duong sai: SLIDES tam cho lot qua -> render ca video voi cue sai.
   ⛔ Duong sai thu hai: uoc timeline bang so ky -> da do lech don +8,6s
      ([[feedback_timeline_phai_do_tu_wav_that]]).
   ✅ Duong dung: goi DUNG `render_audio_timeline()` cua renderer.
"""
import sys, json, types
from pathlib import Path

sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import channels as C
import video_render as VR

STEM = "22_kieta-shigoto"
CH = "showa-b"                      # truc B — 阿井田 茂/Calm/0.90, AivisSpeech :10101 (CLAUDE.md §San xuat)
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / (STEM + "_TTS.md")
VD = ROOT / "06_VIDEO" / STEM
VD.mkdir(parents=True, exist_ok=True)

p = C.CHANNELS[CH]
args = types.SimpleNamespace(
    engine=p.get("engine", "voicevox"),
    speaker=p["speaker"], style=p.get("style"),
    speaker2=None, style2=None, voice_af=None,
    speed=p.get("speed", 0.9), intonation=p.get("intonation", 1.15),
    gap=0.6, section_gap=1.1,
    sub_style=p.get("sub_style", "outline"), sub_size=p.get("sub_size"),
    sub_marginv=None, sub_accent=None,
)
print("engine: %s | giong: %s / %s / speed %s / intonation %s"
      % (args.engine, args.speaker, args.style, args.speed, args.intonation))

wav = VD / "voice.wav"
timeline, total = VR.render_audio_timeline(TTS, wav, args)
(VD / "timeline.json").write_text(
    json.dumps({"total": total, "lines": timeline}, ensure_ascii=False, indent=1),
    encoding="utf-8")

maxlen = VR.SUB_MAXLEN if not args.sub_size else max(24, int(VR.SUB_MAXLEN * 17 / args.sub_size))
VR.write_srt(timeline, VD / "subs.srt", maxlen)

print("\nvoice.wav     %.2f phut (%.2fs)" % (total / 60, total))
print("timeline.json %d dong" % len(timeline))
print("subs.srt      da ghi (maxlen %d)" % maxlen)
print("\n⚠️ DAI THAT chi duoc doc tu day, khong tu so ky. Dai chuan kenh: 14,5-18,0 phut.")
print("Tiep: python tools\\plan_22.py --fetch  ->  build SLIDES v08")
