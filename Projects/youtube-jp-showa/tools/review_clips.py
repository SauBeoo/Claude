# -*- coding: utf-8 -*-
"""review_clips — NGHIEM THU BANG MAT cho MOI clip AI truoc khi crop/stretch/render.

Gop 2 tool viet o video 10: check_hands.py (sheet 4 frame/clip) + sheet_corners.py (sheet dai mep).
Vi sao bat buoc: contact sheet 1 frame giua khung da CHO QUA 24 clip loi hanh dong va 120 clip
khung phim. Loi hanh dong chi thay khi xep 4 frame NGANG (dien bien), loi vien chi thay o MEP.

  py tools/review_clips.py <folder clip> [--out _sheets] [--edges]
     <folder clip>  : clips/ (ten mo ta) hoac clips_raw/
     --edges        : them sheet DAI MEP (soi vien phim). Mac dinh chi sheet 4-frame.
Doc sheet 4-frame: moi HANG = 1 clip, 4 cot = 0,8s · 3,0s · 5,2s · 7,4s. Ten clip in o mep trai.
Loi hay gap: tay/chan lo lung khong than · vat doi hinh giua hang · nguoi bien mat · nguoi quay mat lai
· khoang cach nhay (gan-xa-gan) · chu Latin tren vat · vien den/lo rang o mep.
"""
import sys, os, glob, io, subprocess, argparse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image, ImageDraw

def frame(path, ss, w):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", path, "-frames:v", "1",
                        "-vf", f"scale={w}:-1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert("RGB") if r.stdout else None

def sheet_motion(fs, out, per=11, W=300, H=169):
    n = 0
    for p in range((len(fs) + per - 1) // per):
        chunk = fs[p*per:(p+1)*per]
        sh = Image.new("RGB", (W*4 + 90, H*len(chunk)), (12, 12, 12))
        d = ImageDraw.Draw(sh)
        for r, f in enumerate(chunk):
            for c, ss in enumerate(("0.8", "3.0", "5.2", "7.4")):
                im = frame(f, ss, W)
                if im: sh.paste(im.resize((W, H)), (90 + c*W, r*H))
            nm = os.path.basename(f).replace("clip_", "").replace(".mp4", "")
            for i in range(0, len(nm), 12): d.text((4, r*H + 6 + 11*(i//12)), nm[i:i+12], fill=(255, 220, 90))
        o = os.path.join(out, f"review_{p+1}.jpg"); sh.save(o, quality=90); n += 1
        print("da ghi", o, "|", " ".join(os.path.basename(x)[5:-4][:6] for x in chunk))
    return n

def sheet_edges(fs, out, strip=70, cw=150, ch=150, cols=11):
    per = cols * cols; n = 0
    for p in range((len(fs) + per - 1) // per):
        chunk = fs[p*per:(p+1)*per]
        sh = Image.new("RGB", (cols*cw, cols*ch), (0, 0, 0))
        for i, f in enumerate(chunk):
            im = frame(f, "4", 1920)
            if not im: continue
            Wd, Hd = im.size
            left = im.crop((0, 0, strip, Hd)).resize((cw//2, ch), Image.LANCZOS)
            top  = im.crop((0, 0, Wd, strip)).resize((cw//2, ch), Image.LANCZOS)
            cell = Image.new("RGB", (cw, ch), (20, 20, 20)); cell.paste(left, (0, 0)); cell.paste(top, (cw//2, 0))
            sh.paste(cell, ((i % cols)*cw, (i // cols)*ch))
        o = os.path.join(out, f"edges_{p+1}.jpg"); sh.save(o, quality=92); n += 1
        print("da ghi", o, f"({len(chunk)} clip) — moi o: NUA TRAI = dai mep TRAI, NUA PHAI = dai mep TREN")
    return n

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder"); ap.add_argument("--out", default="_sheets"); ap.add_argument("--edges", action="store_true")
    a = ap.parse_args()
    fs = sorted(glob.glob(os.path.join(a.folder, "*.mp4")))
    if not fs: sys.exit(f"khong co mp4 trong {a.folder}")
    os.makedirs(a.out, exist_ok=True)
    print("clip:", len(fs))
    sheet_motion(fs, a.out)
    if a.edges: sheet_edges(fs, a.out)
    print("\nDUYET MAT: mo tung review_N.jpg, danh dau clip loi theo ten o mep trai. Xong roi moi crop/stretch/render.")
