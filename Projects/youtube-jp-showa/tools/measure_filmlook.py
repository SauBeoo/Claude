# -*- coding: utf-8 -*-
"""measure_filmlook.py — do KHOANG CACH giua clip AI (t2v) va phim tu lieu THAT.

Muc dich: bien cau "lam cho giong phim that" thanh mot bo SO, de con biet chinh cai gi
va chinh bao nhieu. Do tren frame da resize ve cung chieu cao (720) de so sanh cong bang
— khong lam vay thi do net/hat chi do do phan giai.

  luma        trung binh / do lech chuan cua kenh Y
  sat         trung binh S trong HSV (do bao hoa)
  sharp       phuong sai Laplacian (cang cao cang net/gat)
  grain       MAD giua frame lien tiep TRONG VUNG PHANG (loai chuyen dong that:
              chi lay 20% pixel co gradient thap nhat)
  clip_lo/hi  % pixel duoi 16 / tren 240 (bong ket - highlight chay)
"""
import sys, io, subprocess, tempfile, os
import numpy as np, cv2
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def frames(path, ts, h=720):
    """Lay 2 frame LIEN TIEP tai moi moc (can 2 frame de do hat theo thoi gian).
    🔴 Ban dau dung p.replace("f","g") de doi ten -> no thay chu "f" DAU TIEN trong CA
       duong dan (trung ten thu muc temp) => ghi de nhau, tra ve NaN. Doi ten file phai
       lam tren BASENAME, khong lam tren ca path."""
    out = []
    d = tempfile.mkdtemp()
    for i, t in enumerate(ts):
        pat = os.path.join(d, "s%02d_%%02d.png" % i)
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path,
                        "-frames:v", "2", "-vf", "scale=-2:%d" % h, pat],
                       capture_output=True)
    for f in sorted(os.listdir(d)):
        im = cv2.imread(os.path.join(d, f))
        if im is not None: out.append(im)
    return out

def stats(ims):
    Y = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY).astype(np.float32) for i in ims]
    S = [cv2.cvtColor(i, cv2.COLOR_BGR2HSV)[..., 1].astype(np.float32) for i in ims]
    lum = float(np.mean([y.mean() for y in Y]))
    con = float(np.mean([y.std() for y in Y]))
    sat = float(np.mean([s.mean() for s in S]))
    sharp = float(np.mean([cv2.Laplacian(y, cv2.CV_32F).var() for y in Y]))
    lo = float(np.mean([(y < 16).mean() for y in Y]) * 100)
    hi = float(np.mean([(y > 240).mean() for y in Y]) * 100)
    g = []
    for a, b in zip(Y, Y[1:]):
        gx = cv2.Sobel(a, cv2.CV_32F, 1, 0, 3); gy = cv2.Sobel(a, cv2.CV_32F, 0, 1, 3)
        mag = cv2.magnitude(gx, gy)
        flat = mag < np.percentile(mag, 20)          # chi vung PHANG
        if flat.sum() > 1000: g.append(float(np.abs(a - b)[flat].mean()))
    return dict(luma=lum, contrast=con, sat=sat, sharp=sharp, grain=float(np.mean(g)) if g else 0.0,
                clip_lo=lo, clip_hi=hi)

for label, path, ts in [
    ("PHIM THAT mau  (Japan Today 1959)", r"06_VIDEO\_footage_test\japan_today_1959.mp4", [930, 1000, 1300]),
    ("PHIM THAT B&W  (steel 1960)",       r"06_VIDEO\_footage_test\steel_1960\steel_1960.mp4", [1096, 1114, 1330]),
    ("AI t2v         (clip_v3 pho)",      r"06_VIDEO\11_kyuryobukuro\clips_v3\Man_walking_down_street.mp4", [2, 4, 6]),
    ("AI t2v         (clip_v3 trong nha)", r"06_VIDEO\11_kyuryobukuro\clips_v3\Woman_laying_out_banknotes.mp4", [2, 4, 6]),
]:
    if not os.path.exists(path): print(f"-- thieu: {path}"); continue
    st = stats(frames(path, ts))
    print(f"{label:<34} luma {st['luma']:6.1f} | contrast {st['contrast']:5.1f} | sat {st['sat']:5.1f} | "
          f"sharp {st['sharp']:8.1f} | grain {st['grain']:5.2f} | den {st['clip_lo']:4.1f}% | trang {st['clip_hi']:4.1f}%")
