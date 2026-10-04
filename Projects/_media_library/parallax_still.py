# -*- coding: utf-8 -*-
"""parallax_still.py — bien MOT anh tinh thanh clip 2.5D (parallax theo do sau), KHONG can GPU / khong can gen video.

Vi sao (kinishinai 2026-10-02): kenh thang dung tranh CO CHUYEN DONG (clip AI anh->video); user khong gen duoc
video. still_kb (truot phang ca anh) nhin ra "anh phang". Parallax: canh GAN troi nhieu hon canh XA -> cam giac
may quay luot qua that, ma net ve giu nguyen 100%.
- do sau: Depth-Anything V2 Small (ONNX, CPU) -> models/depth_anything_v2_small.onnx, 1 lan/anh (~1-3s)
- dung khung: luoi anh xa (remap) theo do sau: offset = cam_dx * (depth - 0.5) * strength, cong zoom nhe theo do sau
- lap lo (vung bi lo khi canh gan dich) bang cach PHONG to toan anh 1,06 truoc -> mep khong bao gio lo
- chuyen dong: ease in-out, 1 huong / clip (pr | pl | zin | zout), bien do nho (tep 60+, khong lac dau)
    python parallax_still.py <anh> <out.mp4> --dur 9.5 --mode pr [--strength 28] [--fps 30]
"""
import argparse, math, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

MODEL = Path(__file__).with_name("models") / "depth_anything_v2_small.onnx"
W, H = 1920, 1080


def depth_of(img):
    import onnxruntime as ort
    s = ort.InferenceSession(str(MODEL), providers=["CPUExecutionProvider"])
    x = cv2.resize(img, (518, 294))[:, :, ::-1].astype(np.float32) / 255.0
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    d = s.run(None, {"pixel_values": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    d = cv2.resize(d, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
    d = (d - np.percentile(d, 2)) / max(np.percentile(d, 98) - np.percentile(d, 2), 1e-6)
    d = np.clip(d, 0, 1)                                 # 1 = GAN
    return cv2.GaussianBlur(d, (0, 0), 6).astype(np.float32)   # mem bien -> khong xe vien nhan vat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("img"); ap.add_argument("out")
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--mode", default="pr", choices=["pr", "pl", "zin", "zout"])
    ap.add_argument("--strength", type=float, default=28.0, help="px dich lon nhat cua canh GAN nhat")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    im = cv2.imdecode(np.fromfile(a.img, np.uint8), cv2.IMREAD_COLOR)
    im = cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4)
    dep = depth_of(im)
    Z = 1.06                                              # phong truoc de mep khong lo
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, H / 2
    n = int(round(a.dur * a.fps))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(a.fps), "-i", "-", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                            "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
    for i in range(n):
        p = i / max(1, n - 1); e = 0.5 - 0.5 * math.cos(math.pi * p)
        t = (e - 0.5) * 2                                 # -1 .. 1
        dx = dy = 0.0; zk = 0.0
        if a.mode == "pr": dx = -t
        if a.mode == "pl": dx = t
        if a.mode == "zin": zk = e
        if a.mode == "zout": zk = 1 - e
        # canh gan (dep~1) dich nhieu, canh xa (dep~0) gan nhu dung yen
        sx = (xx - cx) / Z + cx - dx * a.strength * (dep - 0.15)
        sy = (yy - cy) / Z + cy - dy * a.strength * (dep - 0.15)
        if zk:
            k = 1 + 0.035 * zk * (0.4 + dep)              # canh gan phong nhanh hon
            sx = (sx - cx) / k + cx; sy = (sy - cy) / k + cy
        fr = cv2.remap(im, sx, sy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    sys.exit(enc.returncode)


if __name__ == "__main__":
    main()
