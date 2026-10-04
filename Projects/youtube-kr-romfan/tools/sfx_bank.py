# -*- coding: utf-8 -*-
"""sfx_bank.py — synth bộ SFX radio-drama cho kênh 朗読 (license sạch, không tải ngoài).
Sinh vào 06_VIDEO/_sfx/*.wav (48kHz mono, peak -3dB). Chạy 1 lần; thêm SFX = thêm entry BANK.
Dùng bởi fx_mix.py / scene_render.py (lớp <slug>_FX.json).
"""
import subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_VIDEO" / "_sfx"

# name -> (aevalsrc/anoisesrc expr hoặc noise, duration, post-filter)
# v2 2026-07-22 (user chê "hiệu ứng không rõ"): mọi tiếng đều có TẦNG MID 200-600Hz
# để nghe được trên loa laptop/điện thoại (dải <180Hz loa nhỏ không phát được).
BANK = {
    # điện thoại rung trên bàn: buzz 170Hz + rattle 480Hz (tiếng lạch cạch mặt bàn)
    "phone_buzz": (
        "aevalsrc=exprs='(0.65*sin(2*PI*170*t)+0.45*sin(2*PI*480*t)*(1+0.4*sin(2*PI*61*t)))"
        "*(1+0.5*sin(2*PI*32*t))*lt(mod(t\\,0.75)\\,0.45)':d=2.3:s=48000",
        "lowpass=f=2400,highpass=f=100"),
    # rung DỒN DẬP (着信 liên tục): chu kỳ ngắn + rattle rõ
    "phone_buzz_urgent": (
        "aevalsrc=exprs='(0.65*sin(2*PI*175*t)+0.5*sin(2*PI*500*t)*(1+0.4*sin(2*PI*63*t)))"
        "*(1+0.5*sin(2*PI*34*t))*lt(mod(t\\,0.42)\\,0.28)':d=4.2:s=48000",
        "lowpass=f=2600,highpass=f=100"),
    # tim đập: thump 58Hz + click transient 185Hz mỗi nhịp (nghe được cả trên loa nhỏ)
    "heartbeat": (
        "aevalsrc=exprs='0.85*sin(2*PI*58*t)*exp(-11*mod(t\\,0.62))"
        "+0.5*sin(2*PI*185*t)*exp(-34*mod(t\\,0.62))':d=6.2:s=48000",
        "lowpass=f=420"),
    # sting cú reveal: sub-drop 110→40Hz + tầng body 230Hz + đuôi noise tối
    "sub_drop": (
        "aevalsrc=exprs='0.75*sin(2*PI*(110-44*t)*t)*exp(-1.7*t)"
        "+0.5*sin(2*PI*230*t)*exp(-5.5*t)+0.3*sin(2*PI*345*t)*exp(-7*t)':d=1.8:s=48000",
        "lowpass=f=900"),
    # gõ cửa 2 tiếng: burst noise băng thấp-mid
    "door_knock": (
        "anoisesrc=d=0.9:c=pink:r=48000:a=0.9",
        "bandpass=f=240:w=260,aeval=exprs='val(0)*exp(-34*mod(t\\,0.38))*lt(mod(t\\,0.38)\\,0.10)'"),
    # tát khô: burst noise ngắn băng trung
    "slap": (
        "anoisesrc=d=0.22:c=white:r=48000:a=0.9",
        "bandpass=f=900:w=1600,aeval=exprs='val(0)*exp(-48*t)'"),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (src, post) in BANK.items():
        f = OUT / f"{name}.wav"
        af = f"{post},alimiter=limit=0.7,aformat=sample_fmts=s16:channel_layouts=mono"
        r = subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", src, "-af", af,
                            str(f), "-loglevel", "error"])
        print(("OK  " if r.returncode == 0 else "FAIL"), f.name)
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
