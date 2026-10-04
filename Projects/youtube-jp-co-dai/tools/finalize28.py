# -*- coding: utf-8 -*-
r"""Nghiem thu + dong goi video 28 sau khi render chunk xong.

Chay MOT lenh, lam du 4 viec cua `render-background.md` §1 muc 3 + dong goi:
  1. so duration mp4 vs subs.srt vs timeline.json  (lech >1s = FAIL)
  2. trich 12 frame rai deu -> sheet de soi mat
  3. copy mp4 ve 06_VIDEO/<slug>/
  4. chay upload_pack --force

    python tools\finalize28.py
"""
import io
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True, write_through=True)

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
RV = Path(r"E:\Claude\Projects\remotion-vox")
STEM = "28_dannetsu-tenjo-alumi"
SRC = RV / "out" / "co-dai-28.mp4"
VD = PROJ / "06_VIDEO" / STEM


def probe(p):
    j = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(p)],
        capture_output=True, text=True).stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in j["streams"] if s["codec_type"] == "audio"]
    return float(j["format"]["duration"]), v, bool(a)


def main():
    if not SRC.exists():
        print("🔴 chua co", SRC)
        sys.exit(1)
    dur, v, has_a = probe(SRC)
    print("mp4: %dx%s %s | %.2fs = %d:%02d | audio=%s | %.1f MB"
          % (v["width"], v["height"], v["r_frame_rate"], dur,
             int(dur) // 60, int(dur) % 60, has_a, SRC.stat().st_size / 1048576))

    bad = []
    if not has_a:
        bad.append("KHONG CO AUDIO")
    if (v["width"], v["height"]) != (1920, 1080):
        bad.append("khong phai 1920x1080")

    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
    if abs(dur - tl["total"]) > 1.0:
        bad.append("lech timeline.json %.2fs (mp4 %.2f vs %.2f)" % (dur - tl["total"], dur, tl["total"]))
    else:
        print("✅ khop timeline.json (lech %.2fs)" % (dur - tl["total"]))

    srt = VD / "subs.srt"
    if srt.exists():
        ts = re.findall(r"(\d\d):(\d\d):(\d\d),(\d+)\s*-->", srt.read_text(encoding="utf-8"))
        if ts:
            h, m, s, ms = ts[-1]
            last = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
            print("srt cuoi %.2fs | mp4 %.2fs | lech %.2fs" % (last, dur, dur - last))
            if dur < last:
                bad.append("mp4 NGAN HON srt %.2fs" % (last - dur))

    out = RV / "out" / "c28fin"
    out.mkdir(parents=True, exist_ok=True)
    times = [int(dur * i / 13) for i in range(1, 13)]
    for t in times:
        o = out / ("t%04d.jpg" % t)
        if not o.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(SRC),
                            "-frames:v", "1", "-q:v", "4", "-vf", "scale=460:-1", "-y", str(o)],
                           check=False)
    try:
        from PIL import Image, ImageDraw
        CW, CH = 460, 259
        sh = Image.new("RGB", (CW * 2 + 15, (CH + 20) * 6 + 5), (18, 20, 26))
        d = ImageDraw.Draw(sh)
        for k, t in enumerate(times):
            f = out / ("t%04d.jpg" % t)
            if f.exists():
                x, y = 5 + (k % 2) * (CW + 5), 5 + (k // 2) * (CH + 20)
                sh.paste(Image.open(f).convert("RGB").resize((CW, CH)), (x, y))
                d.text((x + 5, y + CH + 3), "%d:%02d" % (t // 60, t % 60), fill=(255, 210, 0))
        sh.save(out / "sheet.jpg", quality=88)
        print("sheet:", out / "sheet.jpg")
    except Exception as e:
        print("(bo qua sheet:", e, ")")

    if bad:
        print("🔴 NGHIEM THU FAIL:" + chr(10) + chr(10).join("   " + b for b in bad))
        sys.exit(1)

    dst = VD / f"{STEM}.mp4"
    subprocess.run(["cmd", "/c", "copy", "/Y", str(SRC), str(dst)], capture_output=True)
    print("da copy ->", dst.name)

    r = subprocess.run([sys.executable,
                        r"E:\Claude\Projects\youtube-jp-chouhen\tools\upload_pack.py",
                        STEM, "--channel", "co-dai", "--force"],
                       cwd=str(PROJ), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print((r.stdout or "")[-1200:])
    if r.returncode != 0:
        print("🔴 upload_pack rc=%s" % r.returncode, (r.stderr or "")[-400:])
        sys.exit(1)
    print("✅ XONG — soi sheet.jpg roi kiem _upload/")


if __name__ == "__main__":
    main()
