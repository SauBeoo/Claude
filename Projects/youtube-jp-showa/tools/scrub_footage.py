# -*- coding: utf-8 -*-
"""Cat frame moi N giay tu 1 phim tu lieu -> contact sheet de soi mat tim canh dung.
python scrub_footage.py <video> <out_dir> [step=15]
Xuat: out_dir/f_XXXX.jpg (thumbnail 320px) + sheet_NN.jpg (6 cot x 8 hang = 48 frame/sheet, ghi timestamp).
"""
import sys, io, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

vid, out = Path(sys.argv[1]), Path(sys.argv[2])
step = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0
out.mkdir(parents=True, exist_ok=True)
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(vid)],capture_output=True,text=True).stdout.strip())
print("duration", dur)
# 1 lenh ffmpeg: fps=1/step, scale 320
subprocess.run(["ffmpeg","-v","error","-y","-i",str(vid),"-vf",f"fps=1/{step},scale=320:-2","-q:v","5",str(out/"f_%04d.jpg")],check=True)
frames = sorted(out.glob("f_*.jpg"))
print("frames", len(frames))
W,H = 320, int(Image.open(frames[0]).size[1])
COLS, ROWS = 6, 8
for s in range(0, len(frames), COLS*ROWS):
    chunk = frames[s:s+COLS*ROWS]
    sheet = Image.new("RGB",(W*COLS, H*ROWS),"black"); d = ImageDraw.Draw(sheet)
    for i,f in enumerate(chunk):
        im = Image.open(f).convert("RGB"); sheet.paste(im,((i%COLS)*W,(i//COLS)*H))
        t = (s+i)*step; d.rectangle(((i%COLS)*W,(i//COLS)*H,(i%COLS)*W+70,(i//COLS)*H+14),fill="black")
        d.text(((i%COLS)*W+3,(i//COLS)*H+2),f"{int(t//60):02d}:{int(t%60):02d}",fill="yellow")
    sheet.save(out/f"sheet_{s//(COLS*ROWS):02d}.jpg",quality=80)
print("sheets", (len(frames)+COLS*ROWS-1)//(COLS*ROWS))
