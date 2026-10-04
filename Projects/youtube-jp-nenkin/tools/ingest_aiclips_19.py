# -*- coding: utf-8 -*-
r"""ingest_aiclips_19.py — nhap 74 clip AI (Veo) cho ban vox cua video 19.

User gen 74 clip tu `flow19_VIDEO.txt` va de o
    F:\Youtube\Du_an_moi_7_qnpzs39n\task_001_1_1080p.mp4 .. task_074_...
Thu tu file = thu tu dong trong `flow19_VIDEO.txt` = thu tu THOI GIAN
(da xac minh bang mat: 001=kho+tien bay · 027=tien bi xe nen do · 043=CTA vo
chong · 058=cua quay -> khop 4/4).

HAI VIEC:
  (1) XOA WATERMARK "Veo" — luat `media-library.md` §2.10 ⑤b, user chot
      2026-08-14: *"lúc nào cũng phải xóa watermark cho tôi"*.
      Do bang may 16 lan tren 4 clip x 4 moc thoi gian: Veo CO DINH o
      **x 1865..1895 · y 1042..1055**. => crop 1856x1044 tu goc (0,0) la
      Veo ra HAN ngoai khung theo truc x (du 9px), khong con vet.
      ⛔ Khong dung `delogo`: no lam mo tai cho va de lai vet tren nen co van
      — dung cai §2.10 ⑤ ket an ("patch texture de lai vet hinh chu nhat").
      1856x1044 = 1.7778 = dung 16:9 => scale ve 1920x1080 khong meo.
      Cai gia: noi dung to hon 3,4%, mat ~3% mep phai/day — vung do prompt da
      bat de trong (banner tren + day 1/5) nen khong mat gi.

  (2) DOI TEN theo shot, khong giu `task_NNN` — de builder doc duoc bang mat:
      task_001 -> clip19_hataraku.mp4 (lay ten tu flow19_TENFILE.txt).

  ⓘ Bo LUON audio (`-an`): giong da co rieng (VOICEVOX), audio cua Veo la
    tieng nen sinh kem, gap vao la doi tieng.

CHAY:  python tools/ingest_aiclips_19.py [--dry]
"""
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")
SRC = os.path.join("F:" + os.sep, "Youtube", "Dự_án_mới_7_qnpzs39n")
# 🔴 Remotion doc asset tu **public/**projects/<name>/assets — KHONG phai
# projects/<name>/assets (cho do chi chua project.json). Xem
# build_remotion_19.py: `ad = RV / "public" / "projects" / NAME / "assets"`.
DST = os.path.join("E:" + os.sep, "Claude", "Projects", "remotion-vox",
                   "public", "projects", "nenkin-19vox", "assets")

# crop: bo 64px mep phai + 36px day -> 1856x1044 (dung 16:9) -> scale 1920x1080
CROP = "crop=1856:1044:0:0,scale=1920:1080:flags=lanczos"
WM_BOX = (1865, 1895, 1042, 1055)   # do duoc, de gate kiem lai


def names():
    """dong N -> ten shot, doc tu flow19_TENFILE.txt (nguon su that duy nhat)."""
    out = []
    for ln in io.open(os.path.join(VD, "flow19_TENFILE.txt"), encoding="utf-8"):
        m = re.match(r"\s*(\d+)\s+card19_(\S+)\.png", ln)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    out.sort()
    assert len(out) == 74, f"TENFILE phai co 74 dong, dang co {len(out)}"
    assert [i for i, _ in out] == list(range(1, 75)), "TENFILE thieu/lech so dong"
    return [n for _, n in out]


# ── LO BU 720p (user gen lai 4 clip, 2026-09-03) ─────────────────────────
# Veo o lo nay: x 1242..1266 · y 695..710 (CHOT BANG MAT — nen sang nen nguong
# do sang bat ca nen, may khong tach duoc; dung `media-library.md` §2.10 ⑤).
# Cung ti le tuong doi voi lo 1080p (0,971W x 0,965H) => cat phai 44px.
# 1236x695 = 1.778 = 16:9, roi UPSCALE len 1920x1080 cho dong co voi 70 clip kia.
SRC2 = os.path.join("F:" + os.sep, "Youtube", "Dự_án_mới_1_057pn2oo")
CROP2 = "crop=1236:695:0:0,scale=1920:1080:flags=lanczos"
LOT2 = {1: "hataraku", 2: "hataraku_b", 3: "futari", 4: "futari_b"}


def lot2():
    """4 clip bu — ghi DE len ban cu cung ten trong assets."""
    done = 0
    for i, name in LOT2.items():
        src = os.path.join(SRC2, f"task_{i:03d}_1_720p.mp4")
        dst = os.path.join(DST, f"clip19_{name}.mp4")
        if not os.path.exists(src):
            print(f"  THIEU {os.path.basename(src)}")
            continue
        print(f"  [lo2 {i}/4] {os.path.basename(src)} -> clip19_{name}.mp4", flush=True)
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", CROP2, "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             "-pix_fmt", "yuv420p", dst],
            capture_output=True, text=True, errors="replace")
        if r.returncode:
            print("    LOI ffmpeg:", (r.stderr or "")[:300])
            sys.exit(1)
        done += 1
    print(f"OK lo bu: {done}/4 clip (720p -> 1080p)")


# ── LO NGUOI THAT (photoreal, 2026-09-03) ────────────────────────────────
# Tron bo 74 clip 1080p tu `flow19real_VIDEO.txt`. Veo cung vi tri lo 1080p dau
# (x 1865..1895 · y 1042..1055) => cung mot phep crop, da nghiem thu 0/15 frame.
SRC3 = os.path.join("F:" + os.sep, "Youtube", "nenkin19_crx6ufq9")
DST3 = os.path.join("E:" + os.sep, "Claude", "Projects", "remotion-vox",
                    "public", "projects", "nenkin-19real", "assets")


def lot3():
    os.makedirs(DST3, exist_ok=True)
    nm = names()          # cung thu tu shot (flow19_TENFILE = flow19real_TENFILE)
    done = skip = 0
    miss = []
    for i, name in enumerate(nm, 1):
        src = os.path.join(SRC3, f"task_{i:03d}_1_1080p.mp4")
        dst = os.path.join(DST3, f"rclip19_{name}.mp4")
        if not os.path.exists(src):
            miss.append(os.path.basename(src)); continue
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            skip += 1; continue
        print(f"  [{i:2d}/74] task_{i:03d} -> rclip19_{name}.mp4", flush=True)
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", CROP, "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             "-pix_fmt", "yuv420p", dst],
            capture_output=True, text=True, errors="replace")
        if r.returncode:
            print("    LOI ffmpeg:", (r.stderr or "")[:300]); sys.exit(1)
        done += 1
    print(f"OK lo REAL: crop {done} · skip {skip}")
    if miss:
        print(f"THIEU {len(miss)}: {', '.join(miss[:5])}"); sys.exit(1)
    print(f"   -> {DST3}")


def main():
    if "--lot3" in sys.argv:
        lot3()
        return
    if "--lot2" in sys.argv:
        lot2()
        return
    dry = "--dry" in sys.argv
    os.makedirs(DST, exist_ok=True)
    nm = names()
    miss, done, skip = [], 0, 0
    for i, name in enumerate(nm, 1):
        src = os.path.join(SRC, f"task_{i:03d}_1_1080p.mp4")
        dst = os.path.join(DST, f"clip19_{name}.mp4")
        if not os.path.exists(src):
            miss.append(os.path.basename(src))
            continue
        # resume ĐÚNG cách (render-background.md §2.5): so mtime, khong chi exists
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            skip += 1
            continue
        print(f"  [{i:2d}/74] {os.path.basename(src)} -> clip19_{name}.mp4", flush=True)
        if dry:
            continue
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", CROP, "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             "-pix_fmt", "yuv420p", dst],
            capture_output=True, text=True, errors="replace")
        if r.returncode:
            print("    LOI ffmpeg:", (r.stderr or "")[:300])
            sys.exit(1)
        done += 1
    print(f"\nOK  crop {done} clip · skip {skip} (da moi hon nguon)")
    if miss:
        print(f"🔴 THIEU {len(miss)} file nguon: {', '.join(miss[:6])}")
        sys.exit(1)
    print(f"   -> {DST}")


if __name__ == "__main__":
    main()
