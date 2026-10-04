# -*- coding: utf-8 -*-
r"""ingest_clips_21.py — nhan 84 clip Veo cua video 21, lam sach, doi ten theo shot.

User giao 2026-09-04: `F:\Youtube\nenkin_21_k95bsyz2` — 84 file
`task_NNN_1_1080p.mp4`, do duoc: **1920x1080 / 24fps / 8,000s / co audio AAC**
(giong y lo video 20).

LAM 3 VIEC:
 ① 🔴 XOA WATERMARK "Veo" — bat buoc theo `media-library.md` §2.10 ⑤b
    (user: *"luc nao cung phai xoa watermark cho toi"*), ap cho MOI anh/clip AI.
    **Do lai cho lo nay** (rule doi do lai tung lo, khong bua toa do cu):
    trich frame @4s cua 5 clip -> quet "sang hon trung vi HANG > 28".
    · clip 042 (nen toi): **x 1865-1895, y 1042-1054** — sach, va TRUNG DUNG lo 20.
    · 4 clip nen SANG: phep do tra bbox **cham mep cua so quet** (1660/1919/
      960/1079) = so RAC, dung hai bay da ghi o `media-library.md` §2.10 ⑤ (may
      do truot o nen sang) va `audience-45plus.md` §2.0g (cham mep cua so thi
      do lai, dung tin).
    ⇒ Cach xu ly: **CAT KHUNG**, khong patch (patch tren video de lai vet dong
      yen giua canh dong, lo hon anh tinh nhieu).
      crop=1840:1035:0:0  -> bo phai 80px, bo day 45px, **dung ti le 16:9**
                             (1840/1035 = 1,7778) nen scale lai KHONG meo
      scale=1920:1080     -> phong 4,3%
    Bien an toan: 25px theo x, 7px theo y so voi mep watermark.
 ② 🔇 BO AUDIO — prompt da ghi "Silent" nhung Veo van gan audio AAC. Video nay
    dung giong VOICEVOX rieng; de lai la chong tieng.
 ③ 📛 DOI TEN theo shot (`a21_<key>.mp4`) lay tu `flow21_TENFILE.txt`, de builder
    tra ten thay vi tra so thu tu.

⚠️ Thu tu: task_001 <-> dong 1 cua `flow21_T2V.txt` <-> shot 001 cua TENFILE.
   **PHAI kiem bang mat vai clip sau khi ingest** (`--sheet`) — dung tin thu tu file.

CHAY:  python tools/ingest_clips_21.py            (chay nen theo render-background.md)
       python tools/ingest_clips_21.py --check    (chi in bang doi chieu, khong dung)
       python tools/ingest_clips_21.py --sheet    (trich frame giua 12 clip de soi mat)
"""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
SRC = r"F:\Youtube\nenkin_21_k95bsyz2"
OUT = os.path.join(VD, "clips")

# 🔴 do tren lo nay 2026-09-04, watermark x1865-1895 y1042-1054 — dung sua bua
VF = "crop=1840:1035:0:0,scale=1920:1080:flags=lanczos"


def rows():
    p = os.path.join(VD, "flow21_TENFILE.txt")
    out = []
    for ln in io.open(p, encoding="utf-8").read().split("\n")[1:]:
        c = ln.split("\t")
        if len(c) >= 3 and c[0].strip().isdigit():
            a, b = c[2].split("-")
            out.append(dict(n=int(c[0]), name=c[1].strip(),
                            t0=float(a), t1=float(b.rstrip("s ")),
                            scene=c[3] if len(c) > 3 else "",
                            said=c[4] if len(c) > 4 else ""))
    return out


def sheet(R):
    """Trich frame giua 12 clip rai deu de soi mat: thu tu co dung khong."""
    d = os.path.join(VD, "_probe")
    os.makedirs(d, exist_ok=True)
    pick = [R[i] for i in range(0, len(R), max(1, len(R) // 12))][:12]
    for r in pick:
        src = os.path.join(OUT, r["name"])
        if not os.path.exists(src):
            src = os.path.join(SRC, f"task_{r['n']:03d}_1_1080p.mp4")
        dst = os.path.join(d, f"sheet_{r['n']:03d}_{r['name'][4:-4]}.png")
        subprocess.call(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", src,
                         "-vframes", "1", "-vf", "scale=640:-1", dst])
        print(f"   {r['n']:03d} {r['name'][4:-4]:24s} {r['scene']:28s} {r['said'][:30]}")
    print(f"→ {d}")


def main():
    R = rows()
    os.makedirs(OUT, exist_ok=True)
    if "--sheet" in sys.argv:
        sheet(R)
        return 0

    miss, todo = [], []
    for r in R:
        src = os.path.join(SRC, f"task_{r['n']:03d}_1_1080p.mp4")
        dst = os.path.join(OUT, r["name"])
        if not os.path.exists(src):
            miss.append(src)
            continue
        # resume dung cach: so mtime, khong chi hoi "da ton tai chua"
        # (`render-background.md` §2.5 — hoi sai cau thi ra HINH CU, exit 0)
        if (os.path.exists(dst)
                and os.path.getmtime(dst) >= os.path.getmtime(src)):
            continue
        todo.append((src, dst, r))

    print(f"{len(R)} shot | thieu file nguon: {len(miss)} | can xu ly: {len(todo)}")
    for m in miss[:5]:
        print("   THIEU:", m)
    if "--check" in sys.argv or not todo:
        for r in R[:3]:
            print(f"   {r['n']:03d} -> {r['name']}  ({r['t1']-r['t0']:.1f}s khe)")
        return 1 if miss else 0

    for i, (src, dst, r) in enumerate(todo, 1):
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src,
               "-vf", VF, "-an",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
               "-pix_fmt", "yuv420p", "-r", "24", dst]
        rc = subprocess.call(cmd)
        print(f"[{i:3d}/{len(todo)}] {r['name']}  "
              f"{'OK' if rc == 0 else 'LOI rc=' + str(rc)}", flush=True)
        if rc != 0:
            return 2
    print("XONG:", OUT)
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
