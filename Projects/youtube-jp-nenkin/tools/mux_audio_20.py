# -*- coding: utf-8 -*-
r"""mux_audio_20.py — tron + chuan hoa tieng cho video 20, LOUDNORM HAI LUOT.

🔴 VI SAO PHAI HAI LUOT (do duoc 2026-09-04):
   `loudnorm` chay MOT LUOT la che do dong, no **khong tra dung dich**:
     lan 1 (I=-14) -> do lai duoc **-15,8 LUFS**
     lan 2 (I=-14) -> do lai duoc **-15,2 LUFS**   (van thieu 1,2 LU)
   Cach dung la lay so do that o luot 1 (`print_format=json`) roi bom vao luot 2
   qua `measured_I/TP/LRA/thresh/offset`. Luc do no thanh che do TUYEN TINH va
   ban trung dich.

🔴 VA QUAY VE NGUON, khong va tiep len file da xong:
   moi lan "sua tieng" tren `video_final.mp4` la them MOT doi nen AAC. Chuoi cu
   da la wav -> AAC -> AAC. Script nay dung `video_mute.mp4` (video thuan, chua
   tung co tieng) + `voice_full.wav` goc => dung MOT doi nen AAC duy nhat.

CHAY:  python tools/mux_audio_20.py
"""
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "20_izoku-nenkin-yonbunno-san")
RV = os.path.join(os.path.dirname(PROJ), "remotion-vox")
VOICE = os.path.join(VD, "voice_full.wav")
BGM = os.path.join(RV, "public", "projects", "nenkin-20", "assets", "bgm.mp3")
MUTE = os.path.join(VD, "video_mute.mp4")
MIX = os.path.join(VD, "_mix.wav")
OUT = os.path.join(VD, "video_final.mp4")

# BGM -40 dB = 10^(-40/20) = 0,01 (channels.py, nenkin)
MIXF = ("[1:a]aloop=loop=-1:size=2e9,volume=0.01[b];"
        "[0:a][b]amix=inputs=2:duration=first:dropout_transition=0[a]")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def main():
    # ── 1) tron voice + bgm ra wav 48k stereo ──────────────────────────────
    print("1/3 tron voice + bgm ...", flush=True)
    if os.path.exists(BGM):
        r = sh(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-i", BGM,
                "-filter_complex", MIXF, "-map", "[a]",
                "-ar", "48000", "-ac", "2", MIX])
    else:
        r = sh(["ffmpeg", "-v", "error", "-y", "-i", VOICE,
                "-ar", "48000", "-ac", "2", MIX])
    if r.returncode:
        print("tron GAY:", r.stderr[-400:])
        return 2

    # ── 2) loudnorm LUOT 1: DO ────────────────────────────────────────────
    print("2/3 loudnorm luot 1 (do) ...", flush=True)
    r = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", MIX,
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
            "-f", "null", "-"])
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        print("khong doc duoc so do loudnorm:", r.stderr[-500:])
        return 3
    d = json.loads(m[-1])
    print(f"   do duoc: I={d['input_i']} TP={d['input_tp']} "
          f"LRA={d['input_lra']} thresh={d['input_thresh']}")

    # ── 3) loudnorm LUOT 2 (tuyen tinh) + mux ─────────────────────────────
    print("3/3 loudnorm luot 2 + mux ...", flush=True)
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:"
          f"measured_I={d['input_i']}:measured_TP={d['input_tp']}:"
          f"measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:"
          f"offset={d['target_offset']}:linear=true:print_format=summary")
    r = sh(["ffmpeg", "-v", "error", "-y", "-i", MUTE, "-i", MIX,
            "-af", af, "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-shortest", OUT])
    if r.returncode:
        print("mux GAY:", r.stderr[-400:])
        return 4
    os.remove(MIX)
    print("XONG:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
