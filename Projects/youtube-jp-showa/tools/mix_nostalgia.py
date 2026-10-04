# -*- coding: utf-8 -*-
"""Mix lop am hoai niem vao video da render, bam theo subs.srt:
- school_chime sau cau hoi mo man (to) + sau cau 校庭 cuoi bai (xa, nho)
- pa_chime sau cau お昼の放送
- film_bed rat khe toan bai
Usage: python mix_nostalgia.py <video_dir>
"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

D = sys.argv[1]
SFX = os.path.join(D, "_sfx")

def srt_cues(path):
    txt = open(path, encoding="utf-8").read()
    cues = []
    for m in re.finditer(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)\n(.+?)(?:\n\n|\Z)", txt, re.S):
        h1,m1,s1,ms1,h2,m2,s2,ms2 = map(int, m.groups()[:8])
        end = h2*3600+m2*60+s2+ms2/1000
        cues.append((end, m.group(9).replace("\n","")))
    return cues

cues = srt_cues(os.path.join(D, "subs.srt"))
def find_end(sub):
    for end, text in cues:
        if sub in text:
            return end
    raise SystemExit(f"[LOI] khong thay cue: {sub}")

events = [
    (find_end("この揚げパン、覚えていますか") + 0.2, "school_chime.wav", 0.34),
    (find_end("お昼の放送が流れていました") + 0.25, "pa_chime.wav", 0.40),
    (find_end("校庭へ") + 0.3, "school_chime.wav", 0.14),
]
print("SFX events:", [(round(t,1), f, v) for t, f, v in events])

src = os.path.join(D, "01_kyushoku_pre_atm.mp4")
if not os.path.exists(src):
    os.rename(os.path.join(D, "01_kyushoku.mp4"), src)
inputs = ["-i", src]
fparts, mixins = [], ["[0:a]"]
for i, (t, f, vol) in enumerate(events, start=1):
    inputs += ["-i", os.path.join(SFX, f)]
    ms = int(t*1000)
    fparts.append(f"[{i}:a]adelay={ms}|{ms},volume={vol}[s{i}]")
    mixins.append(f"[s{i}]")
bed_idx = len(events) + 1
inputs += ["-stream_loop", "-1", "-i", os.path.join(SFX, "film_bed.wav")]
fparts.append(f"[{bed_idx}:a]volume=0.05[bd]")
mixins.append("[bd]")
fc = ";".join(fparts) + f";{''.join(mixins)}amix=inputs={len(mixins)}:duration=first:normalize=0[a]"
out = os.path.join(D, "01_kyushoku.mp4")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error"] + inputs +
               ["-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out, "-y"], check=True)
print("MIX XONG ->", out)
