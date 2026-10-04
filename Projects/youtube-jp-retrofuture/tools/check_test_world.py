# -*- coding: utf-8 -*-
"""
NGHIỆM THU 3 cảnh thử THẾ GIỚI v2 — một lệnh, đo xong dựng luôn sheet để soi mắt.

Chạy:
  python tools/check_test_world.py "F:/Youtube/Du_an_moi_NN_xxxx"
  python tools/check_test_world.py <thư mục> --ref "C:/Users/tuana/Downloads/Vientuong/...PUotm8YDbKM...mp4"

Đo gì, và VÌ SAO đo cái đó (mỗi số gắn với một lỗi đã dính thật):

  ① DỊCH KHUNG (px)  — `walk` 12–70px · `stand` ≤20px. Mốc đo từ mẫu: trung vị **36,5px/8s**
                        (= 2,8% bề ngang khung 1280) — mẫu gần như KHÔNG di máy.
  ② JITTER (px/fr)   — rung tay li ti, mẫu trung vị **0,032**; bản mượt tuyệt đối = 0,00x.
                        🔴 Đo ở ĐỘ PHÂN GIẢI GỐC — hạ về 320x180 thì rung dưới 1/4 pixel
                        biến mất sạch (đã dính, cùng họ `feedback_do_pixel_cua_so_quet`).
  ③ % KHUNG ĐỨNG YÊN — `camera-language.md` §8: trần 10%.
  ④ SHEET 4 frame    — ⛔ số KHÔNG chứng minh thế giới đúng. Siêu đô thị có hay không,
                        chữ Nhật bịa, số ở góc — chỉ MẮT thấy. Sheet ở cỡ thật, không thu nhỏ.

⚠️ Tool KHÔNG chấm đạt/rớt cho lớp thế giới — nó chỉ đưa số + ảnh. Quyết định là của mắt.
"""
import io, os, re, sys, glob, json, math, subprocess, argparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD   = os.path.join(ROOT, "06_VIDEO", "01_kumo-no-ue")

# thứ tự dòng trong _test_world_FLOW.txt ↔ ý nghĩa cảnh
# ⚠️ Phai khop THU TU SCENES trong gen_test_world.py — lech la doc sai nhan (da dinh o vong 1)
PLAN = [
    ("W1_tabako",     "stand", "hem: MAY DUNG + ba cu dan o o cua tabako"),
    ("W2_miharashi",  "stand", "nhin ra THAP XOAN — canh tho, khong nguoi"),
    ("W3_shoutengai", "walk",  "shoutengai: di cham nhat + khoanh khac trao tay"),
]
MARKS = [0.3, 2.6, 5.2, 7.6]        # 4 mốc soi/clip (camera-language §7 quy trinh 1)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe(p):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,r_frame_rate,nb_frames", "-show_entries", "format=duration",
            "-of", "json", p])
    try:
        j = json.loads(r.stdout)
        st = j["streams"][0]
        num, den = (st["r_frame_rate"].split("/") + ["1"])[:2]
        return dict(w=st["width"], h=st["height"], fps=float(num) / float(den or 1),
                    dur=float(j["format"]["duration"]))
    except Exception:
        return None


def measure(p, info):
    """Dịch khung + jitter + % đứng yên, đo ở ĐỘ PHÂN GIẢI GỐC."""
    try:
        import cv2, numpy as np
    except ImportError:
        return None, "can opencv:  pip install opencv-python"

    cap = cv2.VideoCapture(p)
    ok, prev = cap.read()
    if not ok:
        return None, "khong doc duoc frame"
    prev_g = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    first_g = prev_g.copy()

    han = cv2.createHanningWindow((prev_g.shape[1], prev_g.shape[0]), cv2.CV_32F)
    dx = dy = 0.0
    steps, mads = [], []
    n = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        # dich khung tich luy: phaseCorrelate tung buoc roi cong don
        (sx, sy), _ = cv2.phaseCorrelate(np.float32(prev_g), np.float32(g), han)
        dx += sx; dy += sy
        steps.append(math.hypot(sx, sy))
        # MAD tren anh nho => do "khung co dung yen khong" (khac han phep do dich khung)
        a = cv2.resize(g, (32, 18)); b = cv2.resize(prev_g, (32, 18))
        mads.append(float(np.mean(cv2.absdiff(a, b))))
        prev_g = g; n += 1
    cap.release()
    if n < 4:
        return None, "clip qua ngan"

    # dich TONG: do truc tiep frame dau vs frame cuoi (khong cong don sai so)
    (tx, ty), _ = cv2.phaseCorrelate(np.float32(first_g), np.float32(prev_g), han)
    total = math.hypot(tx, ty)
    # jitter = do lech chuan cua buoc dich sau khi bo xu the (dung bien thien, khong dung bien do)
    import statistics as st
    med = st.median(steps)
    jit = st.median([abs(s - med) for s in steps])
    still = 100.0 * sum(1 for m in mads if m < 2.0) / len(mads)
    return dict(travel=total, travel_cum=math.hypot(dx, dy), jitter=jit,
                mad=st.mean(mads), still=still, nfr=n), None


def sheet(p, out, info, label):
    """4 frame o CO THAT, xep doc, moi frame co nhan moc giay."""
    tiles = []
    for i, t in enumerate(MARKS):
        f = os.path.join(out, f"_{label}_m{i}.png")
        r = sh(["ffmpeg", "-y", "-ss", str(t), "-i", p, "-frames:v", "1", "-q:v", "2", f])
        if os.path.exists(f) and os.path.getsize(f) > 1000:
            tiles.append(f)
    if not tiles:
        return None
    dst = os.path.join(out, f"sheet_{label}.jpg")
    # ⛔ KHONG dung drawtext (render-background.md §2.7 ① — chet vi fontconfig ma van in "xong")
    r = sh(["ffmpeg", "-y"] + sum([["-i", t] for t in tiles], []) +
           ["-filter_complex", f"vstack=inputs={len(tiles)}", "-q:v", "3", dst])
    for t in tiles:
        try: os.remove(t)
        except OSError: pass
    return dst if os.path.exists(dst) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="thu muc chua clip vua gen (F:/Youtube/Du_an_moi_NN_xxx)")
    ap.add_argument("--ref", help="video mau de do doi chieu cung cong thuc")
    a = ap.parse_args()

    clips = sorted(glob.glob(os.path.join(a.folder, "*.mp4")))
    clips = [c for c in clips if "_720p" in c or True]
    print(f"thu muc : {a.folder}")
    print(f"clip    : {len(clips)}")
    if not clips:
        print("🔴 khong thay mp4 nao — kiem lai duong dan"); return 1
    if len(clips) != 3:
        print(f"⚠️  co {len(clips)} clip, ke hoach la 3 — map theo THU TU TEN FILE, kiem lai neu lech")

    out = os.path.join(VD, "_test_world_check")
    os.makedirs(out, exist_ok=True)

    print("\n" + "─" * 78)
    print(f"{'canh':<16}{'tu the':<7}{'dich':>8}{'jitter':>9}{'MAD':>7}{'dung yen':>10}  ket")
    print("─" * 78)
    rows = []
    for i, c in enumerate(clips):
        name, pose, desc = PLAN[i] if i < len(PLAN) else (os.path.basename(c), "?", "")
        info = probe(c)
        m, err = measure(c, info)
        if err:
            print(f"{name:<16}{pose:<7}  🔴 {err}"); continue
        # ⭐ NGUONG DO TU MAU 2026-09-22 (tools/measure_pace_ref.py, PUotm8YDbKM, 63 shot):
        #   dich khung/8s: trung vi 36,5px · p25 13,6 · p75 100,2 · 30% shot <20px · 54% <40px
        #   jitter trong shot: trung vi 0,032 · dai 0,001-0,396
        # 🔴 Moc CU (walk 100-300px · jitter 0,05-0,24) SAI DON VI: "117px" hom truoc do tren
        #   CUA SO 8 GIAY BAT KY cua video mau, cua so nao chua CAT CANH thi dich khung khong lo
        #   => median bi day len. Clip cua minh la MOT shot 8s khong cat.
        bad = []
        if pose == "walk" and not (12 <= m["travel"] <= 70):   bad.append("DICH")   # quanh trung vi mau
        if pose == "stand" and m["travel"] > 20:               bad.append("DICH")   # 30% shot mau <20px
        if not (0.01 <= m["jitter"] <= 0.12):                  bad.append("jitter") # mau 0,032
        if m["still"] > 10:                                    bad.append("dung-yen")
        print(f"{name:<16}{pose:<7}{m['travel']:>7.1f}p{m['jitter']:>9.3f}{m['mad']:>7.2f}"
              f"{m['still']:>9.1f}%  {'✅' if not bad else '🔴 ' + ','.join(bad)}")
        s = sheet(c, out, info, name)
        rows.append((name, desc, s))

    if a.ref and os.path.exists(a.ref):
        print("\nMAU doi chieu (cung cong thuc, ca video nen co CAT CANH — chi doc jitter):")
        m, err = measure(a.ref, probe(a.ref))
        if m: print(f"  jitter {m['jitter']:.3f} · MAD {m['mad']:.2f} · dung yen {m['still']:.1f}%")

    print("\n" + "─" * 78)
    print("SOI MAT — THU TU QUAN TRONG (so o tren KHONG tra loi duoc may cau nay):")
    print("  ① W2: co SIEU DO THI CHONG TANG o hau canh khong?  thieu = the gioi CHUA VAO")
    print("  ② tien canh co CHAT khong, hay lai thua/nhieu troi nhu v1?")
    print("  ③ con chu Nhat BIA khong · con SO o goc khung khong")
    print("  ④ W3: mat dam dong co meo khong · mai + bien hieu co chong lop khong")
    print("  ⑤ co con cot da / bien may / cau treo sot lai khong (the gioi v1)")
    for name, desc, s in rows:
        print(f"\n  {name}  ({desc})")
        print(f"     {s if s else '🔴 khong dung duoc sheet'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
