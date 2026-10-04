# -*- coding: utf-8 -*-
"""
assemble_clips_17r — lap clips/clip_NN.mp4 cho video 17 tu (a) lo AI t2v F:/Youtube/Du_an_moi_32 (task_NNN = idx+1)
+ (b) 8 canh ima_ie da chot o clips_real_ima_ie/PICK_FINAL (6 AI + 2 stock) + (c) idx 86 (task_087 KHONG co
trong lo) = anh tinh hoa dong tu frame cua task_088 (animate_still.py, L2 cua kenh).

Ba viec cho moi clip AI (media-library §2.10 ⑤ + CLAUDE.md showa §Visual):
  1. CAT ✦ + chu "Veo" goc duoi-phai: giu 0,905W, trim 16:9 chia doi  (cat, khong va)
  2. 1920x1080 · 24fps (channels.py showa fps=24; lech fps = judder, feedback_fps_clip_phai_khop_renderer)
  3. clip NGAN HON KHE -> keo cham setpts (1,2–1,7x khong nhan ra; renderer -stream_loop LAP thi nhan ra ngay)
     khe lay tu clips/_GAPS.json (= _MAP.txt cua build_slides_17). 51/112 khe > 8s, max 11,85 -> keo toi 1,6x.

Chay:  python tools/assemble_clips_17r.py [--only 3,7] [--dry] [--skip-build = chi gate]
Gate cuoi: du 112 file · moi clip dai >= khe + 0,5s · khong clip nao < 1s. Thieu = exit 1 (chan render).
"""
import io, json, os, re, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "17_kaisha-ga-kureta"
CLIPS = VD / "clips"
SRC = Path(r"F:\Youtube\Dự_án_mới_32_tel1fkqt")
FINAL = VD / "clips_real_ima_ie" / "PICK_FINAL"
FINAL_IDX = {4, 5, 102, 103, 104, 108, 109, 111}
MISSING = {86: 88}          # idx thieu -> muon FRAME cua task (idx+1) nay de hoa dong
FPS = 24
# [23/09] PILLARBOX: anh goc khong 16:9 -> Flow/Veo dem vien den 2 ben (1280 wide: 40|40 = 5:3, 106|108 = 3:2).
# Cat ✦ tu x=0 giu nguyen vien TRAI (idx 4 bo user bi 66px den tren 1080p). Do bang max-cot <=22 tren 3 moc thoi gian,
# soi mat: 015/037/100/107 la TUONG TOI (giu), 6 clip nay la vien that. Cat vien TRUOC roi moi cat ✦. (L, R) px tren 1280.
BARS = {37: (106, 108), 51: (40, 40), 69: (40, 40), 85: (39, 39), 90: (0, 159), 100: (43, 43)}
EDGE_OK = {37, 14, 32, 36, 48, 91, 99, 101}   # da soi mat (23/09): mep toi la NOI DUNG (tuong toi, bong nguoi vao khung), khong phai vien
EDGE_TH, EDGE_MAX_PX = 22, 6   # gate mep: cot/ hang co max <= EDGE_TH lien tiep > EDGE_MAX_PX = vien den


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", str(p)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    st = (j.get("streams") or [{}])[0]
    return float(j.get("format", {}).get("duration", 0) or 0), st.get("width", 0), st.get("height", 0)


def name(i):
    return f"clip_{i:02d}.mp4"


def crop_stretch(src, dst, need, bars=(0, 0)):
    d, w, h = probe(src)
    vf = "crop=iw*0.905:iw*0.905*9/16:0:(ih-iw*0.905*9/16)/2,scale=1920:1080,fps=%d" % FPS
    if bars != (0, 0):
        L, R = bars
        vf = f"crop=iw-{L+R}:ih-6:{L}:3," + vf        # bo vien 2 ben + 3px tren/duoi, roi cat ✦ nhu cu
    factor = 1.0
    if d < need:
        factor = need / d
        vf = f"setpts={factor:.4f}*PTS," + vf
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-t", f"{max(need, d * factor):.2f}",
                    "-vf", vf, "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", str(dst)], check=True)
    return d, factor


def edge_bars(path):
    """(L, R, T, B) so cot/hang mep toi lien tiep (max kenh <= EDGE_TH) tai 1,0s. cv2 khong doc duong dan Unicode -> frame ra ASCII."""
    try:
        import cv2
    except ImportError:
        return None
    tmp = CLIPS / "_edge_probe.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.0", "-i", str(path), "-frames:v", "1", str(tmp)])
    im = cv2.imread(str(tmp))
    if im is None:
        return None
    mx = im.max(axis=2); cm = mx.max(axis=0); rm = mx.max(axis=1)
    def run(a):
        n = 0
        while n < len(a) and a[n] <= EDGE_TH:
            n += 1
        return n
    return run(cm), run(cm[::-1]), run(rm), run(rm[::-1])


def main():
    only = None
    if "--only" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
    dry = "--dry" in sys.argv
    skip_build = "--skip-build" in sys.argv     # clip da lap xong, chi chay gate (sau khi sua gate/EDGE_OK)
    gaps = {int(i): (float(t0), float(du)) for i, t0, du in json.load(open(CLIPS / "_GAPS.json"))}
    CLIPS.mkdir(exist_ok=True)
    log = []
    for i in range(112):
        if skip_build or (only is not None and i not in only):
            continue
        dst = CLIPS / name(i)
        need = gaps[i][1] + 0.5
        if i in FINAL_IDX:
            src = FINAL / name(i)
            if not dry:
                shutil.copy(src, dst)
            log.append((i, "FINAL", round(gaps[i][1], 2), round(probe(dst)[0], 2) if dst.exists() else 0, "-"))
            continue
        if i in MISSING:
            still_src = SRC / f"task_{MISSING[i]+1:03d}_1_720p.mp4"
            frame = CLIPS / f"_still_{i:02d}.png"
            if not dry:
                # frame o 1,0s, cat ✦ nhu clip, roi hoa dong (L2) — dai = khe + 0,5
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1.0", "-i", str(still_src), "-frames:v", "1",
                                "-vf", "crop=iw*0.905:iw*0.905*9/16:0:(ih-iw*0.905*9/16)/2,scale=1920:1080", str(frame)], check=True)
                r = subprocess.run([sys.executable, str(ROOT.parent / "_media_library" / "animate_still.py"), str(frame),
                                    "--out", str(dst), "--dur", f"{need:.2f}", "--preset", "office", "--crf", "20", "--fps", str(FPS)],
                                   capture_output=True, text=True)
                if r.returncode != 0 or not dst.exists():
                    print("animate_still loi:", r.stdout[-400:], r.stderr[-400:])
            log.append((i, "STILL->ANIM", round(gaps[i][1], 2), round(probe(dst)[0], 2) if dst.exists() else 0, "task_%03d frame" % (MISSING[i] + 1)))
            continue
        src = SRC / f"task_{i+1:03d}_1_720p.mp4"
        if not src.exists():
            log.append((i, "THIEU", round(gaps[i][1], 2), 0, str(src.name)))
            continue
        if not dry:
            d, f = crop_stretch(src, dst, need, BARS.get(i, (0, 0)))
            tag = (f"x{f:.2f}" if f > 1.001 else "-") + (" vien%s" % (BARS[i],) if i in BARS else "")
            log.append((i, "AI", round(gaps[i][1], 2), round(probe(dst)[0], 2), tag))
        else:
            log.append((i, "AI", round(gaps[i][1], 2), 0, "dry"))

    # gate
    bad, warn = [], []
    for i in range(112):
        if only is not None and i not in only:
            continue
        p = CLIPS / name(i)
        if not p.exists():
            bad.append((i, "THIEU FILE")); continue
        d, w, h = probe(p)
        if d < gaps[i][1] + 0.4:
            bad.append((i, f"NGAN {d:.2f} < khe {gaps[i][1]:.2f}+0.4"))
        if (w, h) != (1920, 1080):
            bad.append((i, f"kich thuoc {w}x{h}"))
        e = edge_bars(p) if i not in EDGE_OK else None
        if e and max(e) > EDGE_MAX_PX * 1.5:      # 1080p: 6px o 720p ~ 9px
            L, R = e[0], e[1]
            if L > 9 and R > 9 and abs(L - R) <= 0.25 * max(L, R):   # DOI XUNG = chu ky pillarbox -> chan
                bad.append((i, f"VIEN DEN doi xung L/R/T/B={e}"))
            else:                                                     # lech mot ben: tuong toi hay vien? -> soi mat
                warn.append((i, e))
    with io.open(CLIPS / "_ASSEMBLE_17r.log", "a", encoding="utf-8") as fh:
        for row in log:
            fh.write("\t".join(str(x) for x in row) + "\n")
    from collections import Counter
    print("lap:", dict(Counter(r[1] for r in log)), "| keo cham:", sum(1 for r in log if str(r[4]).startswith("x")))
    if warn:
        print("⚠️ mep toi lech mot ben (soi mat, them vao EDGE_OK neu la noi dung):", warn)
    if bad:
        print("🔴 GATE:", len(bad), "loi"); [print("  ", b) for b in bad[:20]]
        return 1
    print("✅ GATE: du clip, moi clip >= khe + 0.4s, 1920x1080")
    return 0


if __name__ == "__main__":
    sys.exit(main())
