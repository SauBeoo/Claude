# -*- coding: utf-8 -*-
"""Noi them duoi video cho cau phu de CUOI khong bi cat.

Ca goc (video 13, 2026-09-14): video dai 890,20s nhung dong phu de cuoi cua subs.srt
ket thuc o 890,63s => cau 「それでは、また次のページで、お会いしましょう」 bi cat mat 0,43s.
Voice.wav cung dai hon video 0,13s.

🔴 KHONG re-encode ca video de vá 0,43 giay — mat mot the he nen. Cach dung: dung mot doan
   DONG BANG tu frame cuoi (cung codec/tham so) roi `concat -c copy`. Phu de da chay san vao
   khung nen dong bang frame cuoi = keo dai luon cau phu de dang hien.
"""
import os, re, sys, json, subprocess, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = Path(__file__).resolve().parent.parent / "06_VIDEO" / "13_kosodate-joushiki"
MP4 = VD / "13_kosodate-joushiki.mp4"
SRT = VD / "subs.srt"
PAD_EXTRA = 0.35            # du ra sau moc phu de cuoi


def probe(p, ent):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", ent, "-of", "json", str(p)],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def srt_end(p):
    t = p.read_text(encoding="utf-8", errors="replace")
    ms = re.findall(r"-->\s*(\d\d):(\d\d):(\d\d),(\d\d\d)", t)
    h, m, s, f = ms[-1]
    return int(h) * 3600 + int(m) * 60 + int(s) + int(f) / 1000


if not MP4.exists():
    print("[CHAN] chua co", MP4.name); sys.exit(1)

dur = float(probe(MP4, "format=duration")["format"]["duration"])
end = srt_end(SRT)
need = end + PAD_EXTRA - dur
print("video %.2fs | phu de cuoi ket thuc %.2fs | thieu %.2fs" % (dur, end, need))
if need <= 0.05:
    print("khong can va — bo qua"); sys.exit(0)

v = probe(MP4, "stream=codec_name,width,height,r_frame_rate,pix_fmt,profile,level")["streams"]
vs = [s for s in v if s.get("width")][0]
fps = eval(vs["r_frame_rate"])
tmp = VD / "_tail"
tmp.mkdir(exist_ok=True)
last = tmp / "last.png"
tail = tmp / "tail.mp4"
lst = tmp / "concat.txt"
out = VD / "_padded.mp4"

# 1. frame cuoi (lui 1 frame de chac chan con hinh)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.5",
                "-i", str(MP4), "-frames:v", "1", "-update", "1", str(last)], check=True)
if not last.exists():
    print("[CHAN] khong rut duoc frame cuoi"); sys.exit(1)

# 2. doan dong bang, CUNG tham so codec + audio im lang cung sample rate
a = [s for s in probe(MP4, "stream=codec_type,sample_rate,channels")["streams"]
     if s.get("codec_type") == "audio"]
sr = a[0].get("sample_rate", "48000") if a else "48000"
ch = int(a[0].get("channels", 2)) if a else 2
print("audio: %s Hz, %d kenh" % (sr, ch))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(fps), "-i", str(last),
                "-f", "lavfi", "-i", "anullsrc=r=%s:cl=%s" % (sr, "stereo" if ch == 2 else "mono"),
                "-t", "%.3f" % need, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-pix_fmt", vs.get("pix_fmt", "yuv420p"), "-c:a", "aac", "-b:a", "192k",
                "-shortest", str(tail)], check=True)

# 3. noi KHONG re-encode
lst.write_text("file '%s'\nfile '%s'\n" % (MP4.as_posix(), tail.as_posix()), encoding="utf-8")
r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(out)])
if r.returncode != 0 or not out.exists():
    print("[CHAN] concat -c copy that bai — giu nguyen video goc"); sys.exit(1)

new = float(probe(out, "format=duration")["format"]["duration"])
print("sau khi va: %.2fs (can >= %.2fs)" % (new, end))
if new < end:
    print("[CHAN] van ngan hon phu de — giu nguyen video goc"); out.unlink(); sys.exit(1)

bak = VD / "13_kosodate-joushiki_chua-va-duoi.mp4"
if bak.exists():
    bak.unlink()
shutil.move(str(MP4), str(bak))
shutil.move(str(out), str(MP4))
shutil.rmtree(tmp, ignore_errors=True)
print("XONG — ban cu giu o", bak.name)
