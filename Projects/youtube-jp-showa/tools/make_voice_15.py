# -*- coding: utf-8 -*-
"""Buoc GIONG DOC rieng cho video 14 — chay TRUOC khi co SLIDES.

🔴 VI SAO PHAI CO BUOC NAY (bat 2026-09-16): `video_render.py` dong 1070 co
       if not slides_json.exists(): raise SystemExit("[LOI] Thieu config slide")
   va no nam TRUOC ca khau giong. Nhung `build_slides_14.py` lai phai doc
   `timeline.json` — thu chi co SAU khi tong hop giong. Vong tron.
   ⛔ Duong sai: dung mot SLIDES tam de lot qua — no se render ca video voi cue sai.
   ⛔ Duong sai thu hai: uoc timeline bang so ky. Da do: lech don +8,6s
      ([[feedback_timeline_phai_do_tu_wav_that]]).
   ✅ Duong dung: goi DUNG `render_audio_timeline()` cua renderer — cung ham, cung
      cache TTS, cung cach do moc — roi ghi voice.wav + timeline.json + subs.srt.
      Khong co ban thu hai nao de troi lech.
"""
import sys, json, types
from pathlib import Path

sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import channels as C
import video_render as VR

STEM = "15_haha-no-okane"
CH = "showa-b"                     # truc B — 阿井田茂/Calm/0.90, AivisSpeech port 10101 (CLAUDE.md §San xuat)
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / (STEM + "_TTS.md")
VD = ROOT / "06_VIDEO" / STEM
VD.mkdir(parents=True, exist_ok=True)

p = C.CHANNELS[CH]
# Lay THAM SO TU HO SO KENH, khong go lai bang tay — go lai la nguon lech thu hai.
args = types.SimpleNamespace(
    engine=p.get("engine", "voicevox"),
    speaker=p["speaker"], style=p.get("style"),
    speaker2=None, style2=None, voice_af=None,
    speed=p.get("speed", 0.9), intonation=p.get("intonation", 1.15),
    gap=0.6, section_gap=1.1,
    sub_style=p.get("sub_style", "outline"), sub_size=p.get("sub_size"),
    sub_marginv=None, sub_accent=None,
)
print("giong: %s / %s / speed %s / intonation %s"
      % (args.speaker, args.style, args.speed, args.intonation))

wav = VD / "voice.wav"
timeline, total = VR.render_audio_timeline(TTS, wav, args)
(VD / "timeline.json").write_text(
    json.dumps({"total": total, "lines": timeline}, ensure_ascii=False, indent=1),
    encoding="utf-8")

# phu de: dung DUNG cong thuc maxlen cua renderer, neu khong ban srt o day va ban
# renderer ghi de len nhau se khac nhau tung cue.
maxlen = VR.SUB_MAXLEN if not args.sub_size else max(24, int(VR.SUB_MAXLEN * 17 / args.sub_size))
VR.write_srt(timeline, VD / "subs.srt", maxlen)

print("\nvoice.wav    %.2f phut (%.2fs)" % (total / 60, total))
print("timeline.json %d dong" % len(timeline))
print("subs.srt      da ghi (maxlen %d)" % maxlen)
print("\nTiep: python tools\\build_slides_14.py")
