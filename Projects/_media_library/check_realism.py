# -*- coding: utf-8 -*-
"""
ĐO "ĐỘ THẬT" của một lô clip AI so với mốc đo từ video 異世界さんぽ (pJPST9DG92I, 2026-09-22).

Chạy:
  python tools/check_realism.py <thư mục clip>              # đo lô + dựng sheet 4 frame cỡ thật
  python tools/check_realism.py <video.mp4> --ref           # đo lại video mẫu (tự dò cắt cảnh) → in mốc

Bốn số, mỗi số gắn với một khác biệt ĐÃ ĐO giữa mẫu và lô mình:
  ① MAD trong shot (p50)      mẫu 1,5   · mình 9,4      → trần 3,0
  ② % khung gần đứng yên      mẫu 35,6% · mình 0,6%     → sàn 20%
  ③ MÁY DI (|scale−1|≥5% hoặc dịch ≥8px)  mẫu 32% shot · mình 95%  → cảnh KHOÁ MÁY phải là 0
  ④ % pixel cháy trắng        mẫu 0,5% · mình 3,6%  → ≤1%. Sáng TB CHỈ IN, không chấm: mốc 55–95 cũ là
     trung bình CẢ video mẫu (trộn ngày+đêm) — đo riêng: ngày 108 ấm +27 · đêm 31 ấm +7 (bẫy cửa sổ đo, lần 8)
⚠️ Số không chứng minh "thật": mặt sượng, tay sai, chữ bịa chỉ MẮT thấy → sheet 4 frame cỡ thật
   là bắt buộc (camera-language.md §7 quy trình 1). Tool KHÔNG chấm đạt/rớt cho lớp đó.
🔴 Bẫy đơn vị đã dính 7 lần trong workspace: so MAD của CLIP (một shot) với MAD TRONG SHOT của mẫu,
   không phải MAD cả bài (cả bài cộng cả cắt cảnh). Mốc trên đã tách cắt cảnh (ngưỡng 20 @6fps).
"""
import os, sys, glob, argparse, subprocess, statistics as st
import numpy as np, cv2

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REF = dict(mad_p50=1.5, still_pct=35.6, move_pct=32, area=10.5, speed=14, bright=65, clip_pct=0.52, day=(108, 27), night=(31, 7), src="異世界さんぽ pJPST9DG92I 2026-09-22")
# 🔴 sang TB KHONG chấm dat/rot nua: moc 55-95 la trung binh ca video mau (tron ngay+dem) — do rieng:
#    ngay 108 / am +27 · dem 31 / am +7. In ra cho MAT so theo gio trong ngay cua tung canh.
TH = dict(mad_p50=3.0, still_min=20.0, clip_max=1.0, area_max=25.0, speed_max=22.0)
MARKS = (0.3, 2.6, 5.2, 7.6)


def sample(path, hz=6):
    cap = cv2.VideoCapture(path); fps = cap.get(5) or 24; step = max(1, int(round(fps / hz)))
    out = []; i = 0
    while True:
        if not cap.grab(): break
        if i % step == 0:
            ok, fr = cap.retrieve()
            if ok: out.append((i / fps, cv2.resize(fr, (160, 90))))
        i += 1
    cap.release()
    return out, fps


def flow(frames):
    """⑤⑥ 'êm' = ít thứ động + thứ động thì chậm: % diện tích đang động (>8px/s) và tốc độ trung vị của phần đó.
    Đo mẫu 2026-09-22: 10,5% · 14 px/s. Lô 31 'ảo': 87% · 37 px/s (cả khung bơi vì máy bay)."""
    g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for _, f in frames]
    A = []; V = []
    for a, b in zip(g, g[1:]):
        fl = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        m = np.hypot(fl[..., 0], fl[..., 1]) * 8 * 6      # px/giay o khung 1280, mau 6fps
        mv = m[m > 8]; A.append(100 * float((m > 8).mean())); V.append(float(np.median(mv)) if mv.size else 0.0)
    return float(np.median(A)), float(np.median(V))


def stats(frames):
    g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for _, f in frames]
    mads = np.array([float(np.abs(a - b).mean()) for a, b in zip(g, g[1:])])
    hsv = [cv2.cvtColor(f, cv2.COLOR_BGR2HSV) for _, f in frames]
    bright = float(np.mean([h[..., 2].mean() for h in hsv]))
    clip = float(np.mean([100 * (h[..., 2] >= 250).mean() for h in hsv]))
    return g, mads, bright, clip


def cam_move(g0, g1):
    W = np.eye(2, 3, dtype=np.float32)
    try:
        _, W = cv2.findTransformECC(g0, g1, W, cv2.MOTION_AFFINE,
                                    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5), None, 5)
        sc = float(np.sqrt(abs(np.linalg.det(W[:, :2])))); sh = float(np.hypot(W[0, 2], W[1, 2])) * 8
        return sc, sh, (abs(sc - 1) >= 0.05 or sh >= 8)
    except cv2.error:
        return None, None, None   # ECC không hội tụ ≠ máy không di (camera-language §8.2): soi mắt


def sheet(path, out):
    tiles = []
    for i, t in enumerate(MARKS):
        f = f"{out}_m{i}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", f])
        if os.path.exists(f) and os.path.getsize(f) > 1000: tiles.append(f)
    if not tiles: return None
    dst = out + ".jpg"
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + sum([["-i", t] for t in tiles], []) +
                   ["-filter_complex", f"hstack=inputs={len(tiles)}", "-q:v", "3", dst])
    for t in tiles:
        try: os.remove(t)
        except OSError: pass
    return dst if os.path.exists(dst) else None


def check_lot(folder):
    files = sorted(glob.glob(os.path.join(folder, "*.mp4")))
    if not files: sys.exit("khong co mp4")
    outd = os.path.join(folder, "_realism_check"); os.makedirs(outd, exist_ok=True)
    allm = []; rows = []; n_move = n_meas = 0; B = []; C = []; AR = []; SP = []
    for f in files:
        fr, fps = sample(f)
        if len(fr) < 4: continue
        g, mads, bright, clip = stats(fr)
        allm += mads.tolist(); B.append(bright); C.append(clip)
        ar, sp = flow(fr); AR.append(ar); SP.append(sp)
        sc, sh, mv = cam_move(g[0], g[-1])
        if mv is not None:
            n_meas += 1; n_move += int(mv)
        rows.append((os.path.basename(f), float(np.median(mads)), 100 * float((mads < 1.0).mean()), bright, clip, sc, sh, mv, ar, sp))
        sheet(f, os.path.join(outd, "sheet_" + os.path.splitext(os.path.basename(f))[0]))
    allm = np.array(allm)
    p50 = float(np.median(allm)); still = 100 * float((allm < 1.0).mean())
    move_pct = 100 * n_move / max(1, n_meas)
    br = float(np.mean(B)); cl = float(np.mean(C)); ar = float(np.median(AR)); sp = float(np.median(SP))
    print(f"LO {os.path.basename(folder)} — {len(rows)} clip   (moc mau: {REF['src']})")
    print(f"{'':28s}{'LO NAY':>10s}{'MAU':>10s}{'MOC':>14s}")
    ok1 = p50 <= TH['mad_p50'];  ok2 = still >= TH['still_min']
    # ③ sua toi 22/09: mau co 32% shot TROI NHE (zoom +3..8%, dich 40-110px/shot). Khoa 100% la qua tay.
    #    Dat: <=40% shot di, va shot di nao cung phai la troi nhe (scale <1.12, dich <150px) — khong phai bay.
    gentle = all((r[5] is None) or (not r[7]) or (r[5] < 1.12 and r[6] < 150) for r in rows)
    ok3 = move_pct <= 40 and gentle;  ok4 = cl <= TH['clip_max']
    print(f"① MAD trong shot p50        {p50:10.2f}{REF['mad_p50']:10.2f}{'<= ' + str(TH['mad_p50']):>14s}  {'✅' if ok1 else '🔴'}")
    print(f"② % khung gan dung yen      {still:9.1f}%{REF['still_pct']:9.1f}%{'>= ' + str(TH['still_min']):>14s}  {'✅' if ok2 else '🔴'}")
    print(f"③ % shot MAY DI             {move_pct:9.0f}%{REF['move_pct']:9d}%{'<=40%, troi nhe':>14s}  {'✅' if ok3 else '🔴'}")
    print(f"④ % chay trang              {cl:9.2f}%{REF['clip_pct']:9.2f}%{'<= 1%':>14s}  {'✅' if ok4 else '🔴'}")
    ok5 = ar <= TH['area_max']; ok6 = sp <= TH['speed_max']
    print(f"⑤ % dien tich khung DANG DONG{ar:9.1f}%{REF['area']:9.1f}%{'<= 25%':>14s}  {'✅' if ok5 else '🔴'}   (lo 31: 87%)")
    print(f"⑥ toc do phan dang dong     {sp:7.0f} px/s{REF['speed']:7d} px/s{'<= 22':>14s}  {'✅' if ok6 else '🔴'}   (lo 31: 37)")
    print(f"   sang TB (chi de MAT so)   {br:10.0f}   mau ngay {REF['day'][0]} am{REF['day'][1]:+d} · dem {REF['night'][0]} am{REF['night'][1]:+d}")
    print(f"\n{'clip':30s}{'MADp50':>7s}{'%yen':>6s}{'sang':>6s}{'chay%':>6s}{'scale':>7s}{'dich':>6s}{'%dong':>6s}{'px/s':>6s}  may")
    for r in rows:
        sc = f"{r[5]:.3f}" if r[5] is not None else "  ?  "; sh = f"{r[6]:.0f}" if r[6] is not None else "?"
        mv = "DI" if r[7] else ("dung" if r[7] is not None else "SOI MAT")
        print(f"{r[0][:30]:30s}{r[1]:7.2f}{r[2]:6.0f}{r[3]:6.0f}{r[4]:6.2f}{sc:>7s}{sh:>6s}{r[8]:6.0f}{r[9]:6.0f}  {mv}")
    print(f"\nsheet 4 frame co that: {outd}  ← soi MẮT: mặt · tay · chữ bịa · vật lý")
    return 0 if (ok1 and ok2 and ok3 and ok4 and ok5 and ok6) else 1


def measure_ref(path):
    fr, fps = sample(path)
    g, mads, bright, clip = stats(fr)
    cut = mads > 20
    inshot = mads[~cut]
    ts = [t for (t, _) in fr[1:]]
    cuts = [t for t, c in zip(ts, cut) if c]
    m = []
    for c in cuts:
        if not m or c - m[-1] > 0.5: m.append(c)
    b = [0] + m + [ts[-1]]
    n_move = n_meas = 0
    for a, z in zip(b, b[1:]):
        fs = [gg for (t, _), gg in zip(fr, g) if a + 0.3 <= t <= z - 0.3]
        if len(fs) < 3: continue
        sc, sh, mv = cam_move(fs[0], fs[-1])
        if mv is not None: n_meas += 1; n_move += int(mv)
    print(f"MAU {os.path.basename(path)}: shot~{len(m)+1} · MAD trong shot p50={np.median(inshot):.2f} mean={inshot.mean():.2f} · "
          f"%khung <1.0={100*(inshot<1.0).mean():.1f}% · may DI={100*n_move/max(1,n_meas):.0f}% · sang={bright:.0f} · chay={clip:.2f}%")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("target"); ap.add_argument("--ref", action="store_true")
    a = ap.parse_args()
    sys.exit(measure_ref(a.target) if a.ref else check_lot(a.target))
