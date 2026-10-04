# -*- coding: utf-8 -*-
"""kb_cells_01.py — chuyen dong KIEU SHOWA cho kinishinai bai 1: moi o ANH thanh clip still_kb.py
(anh sach + zoom/truot CHAM xoay vong, ease dau-cuoi; KHONG meo cuc bo) — khuon youtube-jp-showa/tools/v08look_18.py.

- O anh = entry SLIDES khong co card/reveal; nguon = slides_img/slide_NN.png (da cat ✦ luc ingest -> --wm 0)
- bien do = min(0,06, max(0,03, 0,011 x giay)) — muc showa sau khi user che "hoi nhanh" (2026-09-24)
- fps 30 = ho so kenh kinishinai (showa 24) — lech fps la judder (feedback_fps_clip_phai_khop_renderer)
- HOLD (2 o cung mot anh, vd 59->60): dung MOT clip lien cho ca hai roi cat doi -> khong nhay giua chung
- entry duoc gan "video": true + "_kb": mode; o card/reveal giu nguyen
- clip podcast cu trong clips/ duoc chuyen sang clips/_podcast_old/ (khong xoa)
Chay: python tools/kb_cells_01.py 01_kuchiguse-hitonome [--only 10,13] [--dry]
"""
import sys, io, json, argparse, subprocess, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
KB = Path(r"E:\Claude\Projects\_media_library\still_kb.py")
# 2026-10-03: user chot PARALLAX 2.5D (canh gan troi nhieu hon canh xa) thay truot phang still_kb
PX = Path(r"E:\Claude\Projects\_media_library\parallax_still.py")
PX_MODE = {"zin": "zin", "zout": "zout", "pl": "pl", "pr": "pr", "tu": "zin", "td": "zout"}
MODES = ["zin", "pl", "zout", "pr", "tu", "zin", "td", "pl", "zout", "pr"]   # = v08look_18
FPS = 30
HOLD = {59: 60, 61: 62}   # 2 o cung MOT anh -> mot clip lien roi cat doi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem"); ap.add_argument("--only"); ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    vd = PROJ / "06_VIDEO" / a.stem
    sp = PROJ / "03_SCRIPTS" / f"{a.stem}_SLIDES.json"
    sl = json.loads(sp.read_text(encoding="utf-8"))
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    lines, total = tl["lines"], tl["total"]
    st = []
    for i, e in enumerate(sl):
        hit = next(ln for ln in lines if e["match"] in ln["text"])
        st.append((hit["start"] + float(e.get("offset", 0.0)), i))
    st.sort(); st[0] = (0.0, st[0][1])
    dur = {i: (st[k + 1][0] if k + 1 < len(st) else total) - t for k, (t, i) in enumerate(st)}
    only = {int(x) for x in a.only.split(",")} if a.only else None

    cd = vd / "clips"; old = cd / "_podcast_old"; old.mkdir(exist_ok=True)
    jobs, k = [], 0
    for i, e in enumerate(sl):
        if e.get("card") or e.get("reveal") or i in HOLD.values():
            continue
        if e.get("_pod"):
            sys.exit(f"slot {i} con dau podcast — SLIDES chua tra ve ban khong podcast")
        img = vd / "slides_img" / f"slide_{i:02d}.png"
        assert img.exists(), f"thieu {img.name}"
        d = dur[i] + (dur[HOLD[i]] if i in HOLD else 0.0) + 0.5
        amt = min(0.06, max(0.03, 0.011 * d))
        jobs.append((i, img, d, MODES[k % len(MODES)], amt)); k += 1
        e["video"] = True; e["_kb"] = MODES[(k - 1) % len(MODES)]
        if i in HOLD:
            sl[HOLD[i]]["video"] = True; sl[HOLD[i]]["_kb"] = e["_kb"] + f" (noi tiep o {i})"
    print(f"{len(jobs)} o anh -> still_kb ({FPS}fps) · bien do {min(j[4] for j in jobs):.3f}-{max(j[4] for j in jobs):.3f}")
    if a.dry:
        for j in jobs[:12]:
            print(f"  clip_{j[0]:02d} {j[3]:4s} {j[2]:5.1f}s amt {j[4]:.3f}")
        return

    def run(j):
        i, img, d, mode, amt = j
        dst = cd / f"clip_{i:02d}.mp4"
        if dst.exists() and not (old / dst.name).exists() and not (cd / f"_kb_{i:02d}.ok").exists():
            shutil.move(str(dst), str(old / dst.name))     # clip podcast cu
        p = subprocess.run([sys.executable, str(PX), str(img), str(dst), "--dur", f"{d:.2f}", "--mode", PX_MODE[mode],
                            "--fps", str(FPS)], capture_output=True, text=True)
        if p.returncode:
            return i, mode, "LOI " + p.stderr[-200:]
        (cd / f"_kb_{i:02d}.ok").write_text(mode)
        if i in HOLD:   # cat doi: phan dau cho o i, phan sau cho o HOLD[i]
            j2 = HOLD[i]; a_ = dur[i]
            full = cd / f"_kb_full_{i:02d}.mp4"; shutil.move(str(dst), str(full))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(full), "-t", f"{a_ + 0.5:.2f}", "-c:v", "libx264",
                            "-crf", "18", "-preset", "veryfast", str(dst)])
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a_:.2f}", "-i", str(full), "-c:v", "libx264",
                            "-crf", "18", "-preset", "veryfast", str(cd / f"clip_{j2:02d}.mp4")])
        return i, mode, "ok"

    todo = [j for j in jobs if not only or j[0] in only]
    with ThreadPoolExecutor(2) as ex:
        res = list(ex.map(run, todo))
    bad = [r for r in res if r[2] != "ok"]
    sp.write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8")
    print("KET QUA:", f"SACH {len(res)} o anh" if not bad else f"LOI {len(bad)}: {bad[:3]}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
