# -*- coding: utf-8 -*-
"""lipsync_retime.py — dung clip Veo NHEP MIENG nhung TIENG la VOICEVOX cua minh.

Veo noi DUNG cau trong kich ban (nhep khop tieng cua no) -> tat tieng Veo -> co gian TUNG DOAN hinh
cho moc tieng Veo trung moc tieng VOICEVOX -> mieng mo dung luc giong minh noi.
Ban do moc: danh sach (veo_a, veo_b, vv_a, vv_b) — cum NOI <-> cum NOI, cho NGHI <-> cho NGHI.
veo_a == veo_b = giu khung (VOICEVOX nghi o dau 「、」 ma Veo noi lien).
Lay moc: faster-whisper word_timestamps + silencedetect -35dB tren CA HAI file (xem ghi so trong MAPS).
Frame trung gian = tron 2 frame Veo ke nhau (tranh judder khi gian 24 -> 30fps).
Cat watermark: --cut-bottom (ti le chieu cao bo o day, vd 0.10 cho chu "Dola AI") roi trim 16:9 bo ben TRAI
(nguoi dan ngoi lech phai).
Chay: python tools/lipsync_retime.py <veo.mp4> <voicevox.wav|mp3> <out.mp4> --map demo01 [--cut-bottom 0.10]
"""
import sys, io, argparse, subprocess
import numpy as np
import cv2

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
W, H, FPS = 1920, 1080, 30

MAPS = {
    # 「私は、ずっと、そうでした。デパートの売り場で三十四年、一日に何十回も、頭を下げてきた人間です。」
    # Veo 動画生成.mp4 (2026-10-01) <-> demo_01_jikoshoukai.mp3
    "demo01": [(0.00, 0.26, 0.00, 0.28), (0.26, 0.89, 0.28, 0.88), (0.89, 1.26, 0.88, 1.35),
               (1.26, 1.74, 1.35, 1.90), (1.74, 1.74, 1.90, 2.40), (1.74, 2.67, 2.40, 3.14),
               (2.67, 4.03, 3.14, 3.60), (4.03, 5.90, 3.60, 5.91), (5.90, 6.50, 5.91, 6.45),
               (6.50, 7.91, 6.45, 8.19), (7.91, 8.29, 8.19, 8.66), (8.29, 9.80, 8.66, 10.74),
               (9.80, 10.05, 10.74, 11.29)],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("veo"); ap.add_argument("voice"); ap.add_argument("out")
    ap.add_argument("--map", required=True, choices=sorted(MAPS))
    ap.add_argument("--cut-bottom", type=float, default=0.0)
    a = ap.parse_args()
    M = MAPS[a.map]
    cap = cv2.VideoCapture(a.veo); vfps = cap.get(cv2.CAP_PROP_FPS); fr = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        h, w = f.shape[:2]
        if a.cut_bottom:
            nh = int(h * (1 - a.cut_bottom)); nw = int(nh * 16 / 9)
            f = f[:nh, w - nw:]                      # bo day + bo ben trai cho ve 16:9
        fr.append(cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4))
    total = M[-1][3]
    n = int(round(total * FPS))
    for (va, vb, xa, xb) in M:
        if vb > va:
            k = (xb - xa) / (vb - va)
            print(f"  veo {va:5.2f}-{vb:5.2f} -> vv {xa:5.2f}-{xb:5.2f}  x{k:.2f}")
        else:
            print(f"  GIU khung veo {va:5.2f} trong vv {xa:5.2f}-{xb:5.2f}")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", a.voice, "-map", "0:v", "-map", "1:a",
                            "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", a.out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        seg = next((s for s in M if s[2] <= t < s[3]), M[-1])
        va, vb, xa, xb = seg
        tv = va if vb <= va else va + (t - xa) * (vb - va) / (xb - xa)
        p = min(max(tv * vfps, 0), len(fr) - 1)
        i0 = int(p); i1 = min(i0 + 1, len(fr) - 1); w1 = p - i0
        img = fr[i0] if w1 < 1e-3 else cv2.addWeighted(fr[i0], 1 - w1, fr[i1], w1, 0)
        enc.stdin.write(img.tobytes())
    enc.stdin.close(); enc.wait()
    print(f"OK {n} frame ({total:.2f}s) -> {a.out}")
    sys.exit(enc.returncode)


if __name__ == "__main__":
    main()
