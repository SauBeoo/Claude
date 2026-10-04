# -*- coding: utf-8 -*-
"""
gen_cta_sfx.py — synth 3 SFX cho hieu ung CTA (tu tao bang ffmpeg, khong dinh license):
  whoosh.wav — gio nhe khi card truot len (pink noise bandpass + fade)
  pop.wav    — tieng "bup" mem khi bam nut (sine sweep + hai am + echo nhe)
  bell.wav   — chime 2 not "ding-dong" khi bam subscribe (partials + shimmer echo)

Usage: python gen_cta_sfx.py --out <dir>
Timing ghep: xem SFX_EVENTS trong gen_cta_overlay.py.
Mix vao video: adelay tung event + amix; gain goi y -8..-12dB duoi giong doc.
"""
import argparse
import os
import re
import subprocess

PEAK_TARGET = -3.0  # dBFS sau normalize

SFX = {
    # gio nhe: pink noise loc bandpass, fade in/out
    "whoosh": (
        "anoisesrc=d=0.6:c=pink:a=0.45:s=44100",
        "bandpass=f=850:w=700,afade=t=in:d=0.12,afade=t=out:st=0.25:d=0.35,volume=0.5",
    ),
    # pop mem: sweep 900->220Hz + hai am 2f, decay nhanh, echo phong rat nhe
    "pop": (
        "aevalsrc=0.75*sin(2*PI*(220+680*exp(-t*30))*t)*exp(-t*18)"
        "+0.15*sin(2*PI*2*(220+680*exp(-t*30))*t)*exp(-t*24):d=0.45:s=44100",
        "highpass=f=120,lowpass=f=4200,aecho=0.5:0.35:28:0.22,"
        "afade=t=in:d=0.004,volume=0.9",
    ),
    # chime 2 not: A5 roi E6 (partials hoi detune cho am chuong), shimmer echo
    "bell": (
        "aevalsrc=0.30*(sin(2*PI*880*t)+0.40*sin(2*PI*1764*t)+0.18*sin(2*PI*2652*t))"
        "*exp(-t*6)"
        "+gt(t\\,0.12)*0.34*(sin(2*PI*1318.5*(t-0.12))+0.45*sin(2*PI*2642*(t-0.12))"
        "+0.20*sin(2*PI*3968*(t-0.12)))*exp(-(t-0.12)*3.5):d=2.2:s=44100",
        "lowpass=f=9000,aecho=0.55:0.45:60|110:0.26|0.16,"
        "afade=t=in:d=0.004,afade=t=out:st=1.7:d=0.5,volume=0.85",
    ),
}


def peak_db(path):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for name, (src, af) in SFX.items():
        path = os.path.join(a.out, f"{name}.wav")
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", src, "-af", af,
                        path, "-loglevel", "error"], check=True)
        # normalize peak ve PEAK_TARGET (cong thuc synth co the tu triet tieu nang luong)
        gain = PEAK_TARGET - peak_db(path)
        if abs(gain) > 0.5:
            tmp = path + ".tmp.wav"
            subprocess.run(["ffmpeg", "-y", "-i", path, "-af", f"volume={gain:.1f}dB",
                            tmp, "-loglevel", "error"], check=True)
            os.replace(tmp, path)
        print(f"  {name}.wav peak -> {peak_db(path):.1f} dB")
    print(f"OK: whoosh.wav + pop.wav + bell.wav -> {a.out}")


if __name__ == "__main__":
    main()
