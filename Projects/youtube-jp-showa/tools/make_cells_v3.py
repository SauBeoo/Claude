# -*- coding: utf-8 -*-
"""make_cells_v3.py — bien dau vao cua tung o thanh clips/clip_NN.mp4 (khuon REAL-FIRST v3).

Doc clips/_PLAN.json (build_slides_v3.py xuat). Theo LOP cua o:
  film    -> KHONG lam gi: cut_archival.py --record da ghi thang clips/clip_NN.mp4. Chi kiem.
  photo   -> cells_in/NN.jpg|png (anh THAT)      -> chuan 1920x1080 -> animate_still (preset cua o)
  aistill -> cells_in/NN.png     (Nano Banana)   -> CAT ✦ -> 1920x1080 -> animate_still
  ai      -> cells_in/NN.mp4     (Flow Animate)  -> CAT ✦ -> 1920x1080 -> keo cham neu ngan hon o

🔴 Ba luat da tra gia, cai san:
  · Thieu dau vao -> ghi clips/_MISSING_ART.json -> video_render.py preflight ④b CHAN CUNG
    (render-background.md §1.5: du asset moi duoc render). Du het thi XOA so do.
  · Resume so MTIME dau ra vs dau vao, khong hoi "co file chua" (render-background.md §2.5).
  · Cat ✦ bang CAT KHUNG (0,905W + trim 16:9 chia doi), khong va — media-library.md §2.10 ⑤/6e.
    Moc 0,905 la moc cua lo Flow showa 17 (assemble_clips_17r.py). LO MOI thi soi 1:1 ca 4 goc
    truoc khi tin moc nay (--wm 0.88 neu ✦ to hon).

Chay NEN (render-background.md): ~2 phut / o anh 16s.
  python tools/make_cells_v3.py <stem> [--only 3,7] [--jobs 2] [--wm 0.905] [--fps 24] [--dry]
"""
import sys, json, subprocess, argparse, io, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
ANIM = Path(r"E:\Claude\Projects\_media_library\animate_still.py")
sys.path.insert(0, str(ANIM.parent))
from animate_still import PRESETS  # noqa: E402
MARGIN = 0.5      # clip dai hon o 0,5s — renderer thieu do dai thi LAP clip (CLAUDE.md §Visual)
MAX_STRETCH = 1.25

ap = argparse.ArgumentParser()
ap.add_argument("stem")
ap.add_argument("--only", default=None)
ap.add_argument("--jobs", type=int, default=2, help="2 la tran an toan tren may 6 nhan")
ap.add_argument("--wm", type=float, default=0.905, help="cat phai tai ti le nay de bo ✦ (0 = khong cat)")
ap.add_argument("--fps", type=int, default=24)
ap.add_argument("--boost", type=float, default=1.0, help="nhan bien do lop phim + fx (MAD<3 thi tang 1,3–1,6)")
ap.add_argument("--dry", action="store_true")
ap.add_argument("--vd", default=None, help="thu muc video (mac dinh 06_VIDEO/<stem>) — dung de chay thu ngoai du an")
a = ap.parse_args()

VD = Path(a.vd) if a.vd else ROOT / "06_VIDEO" / a.stem
CL = VD / "clips"
IN = VD / "cells_in"
TMP = VD / "_cells_tmp"
plan = json.loads((CL / "_PLAN.json").read_text(encoding="utf-8"))
only = {int(x) for x in a.only.split(",")} if a.only else None


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", str(p)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    st = (j.get("streams") or [{}])[0]
    return float(j.get("format", {}).get("duration", 0) or 0), st.get("width", 0), st.get("height", 0)


def find_in(i, exts):
    for e in exts:
        p = IN / ("%02d%s" % (i, e))
        if p.exists():
            return p
    return None


def vf_norm(cut_wm, bw=False):
    """cat ✦ (neu co) + trim 16:9 CHIA DOI tren/duoi + cover 1920x1080 (+ bo mau neu o co co bw)."""
    f = ["hue=s=0"] if bw else []
    if cut_wm and a.wm > 0:
        f.append("crop=iw*%.3f:ih:0:0" % a.wm)
    f.append("crop='min(iw,ih*16/9)':'min(ih,iw*9/16)':'(iw-min(iw,ih*16/9))/2':'(ih-min(ih,iw*9/16))/2'")
    f.append("scale=1920:1080:flags=lanczos,setsar=1")
    return ",".join(f)


def fresh(dst, src):
    return dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime and \
        dst.stat().st_mtime >= (CL / "_PLAN.json").stat().st_mtime


def do_still(r, src, cut_wm):
    i, need = r["idx"], r["dur"] + MARGIN
    dst = CL / ("clip_%02d.mp4" % i)
    if fresh(dst, src):
        return i, "skip (con moi)", None
    if a.dry:
        return i, "dry", None
    TMP.mkdir(exist_ok=True)
    frame = TMP / ("%02d.png" % i)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-frames:v", "1",
                    "-vf", vf_norm(cut_wm, r.get("bw", False)), str(frame)], check=True)
    # 🔴 LOP PHIM PHAI MANH HON PRESET MAC DINH (bai hoc make_stills_16: preset goc ra MAD 0,87–0,97,
    # tinh hon ca anh tro cua doi thu; nguong "co dong that" la >3). Cung bo so cua video 16.
    pre = r.get("preset", "flat")
    spec = json.loads(json.dumps(PRESETS[pre])); f = spec["film"]
    f["grain"] = max(f.get("grain", .7), 2.2 * a.boost); f["flicker"] = max(f.get("flicker", .01), .026 * a.boost)
    f["dust"] = round(f.get("dust", .3) * 1.6 * a.boost, 2); f["scratch"] = round(f.get("scratch", .12) * 1.6 * a.boost, 2)
    for fx in spec.get("fx", []):
        fx["amp"] = round(fx.get("amp", .3) * a.boost, 3)
    sp = TMP / ("spec_%02d.json" % i); sp.write_text(json.dumps(spec), encoding="utf-8")
    p = subprocess.run([sys.executable, str(ANIM), str(frame), "--out", str(dst), "--dur", "%.2f" % need,
                        "--preset", pre, "--spec", str(sp), "--fps", str(a.fps), "--crf", "20"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    mad = re.findall(r"MAD[^0-9]*([0-9]+[.,][0-9]+)", p.stdout + p.stderr)
    mad = float(mad[-1].replace(",", ".")) if mad else None
    if p.returncode != 0 or not dst.exists():
        return i, "LOI animate_still: " + (p.stderr or p.stdout)[-300:], None
    return i, "ok", mad


def do_ai(r, src):
    i, need = r["idx"], r["dur"] + MARGIN
    dst = CL / ("clip_%02d.mp4" % i)
    if fresh(dst, src):
        return i, "skip (con moi)", None
    d, _, _ = probe(src)
    fac = max(1.0, need / d) if d else 1.0
    if a.dry:
        return i, "dry x%.2f" % fac, None
    vf = ("setpts=%.4f*PTS," % fac if fac > 1.001 else "") + vf_norm(True, r.get("bw", False)) + ",fps=%d" % a.fps
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-t", "%.2f" % max(need, d * fac), "-vf", vf,
                    "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(dst)],
                   check=True)
    return i, "ok x%.2f%s" % (fac, "  ⚠️ keo cham qua %.2f" % MAX_STRETCH if fac > MAX_STRETCH else ""), None


jobs, missing, log = [], [], []
for r in plan:
    i, lay = r["idx"], r["layer"]
    if only is not None and i not in only:
        continue
    if lay == "film":
        continue
    if lay == "ai":
        src = find_in(i, (".mp4",))
        if src is None: missing.append(("%02d.mp4" % i, lay, r["text"][:30])); continue
        jobs.append(("ai", r, src))
    else:
        src = find_in(i, (".png", ".jpg", ".jpeg", ".webp"))
        if src is None: missing.append(("%02d.png" % i, lay, r["text"][:30])); continue
        jobs.append((lay, r, src))

print("o can dung: %d | thieu dau vao: %d" % (len(jobs), len(missing)))
with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
    futs = [ex.submit(do_ai, r, s) if k == "ai" else ex.submit(do_still, r, s, k == "aistill") for k, r, s in jobs]
    for f in futs:
        i, st, mad = f.result()
        log.append((i, st, mad))
        print("  clip_%02d  %-24s %s" % (i, st[:60], "" if mad is None else "MAD %.2f%s" % (mad, "  ⚠️ <3 khung gan chet" if mad < 3 else "")))

# ---------- GATE ----------
bad = []
for r in plan:
    i = r["idx"]
    if only is not None and i not in only:
        continue
    p = CL / ("clip_%02d.mp4" % i)
    if not p.exists():
        if r["layer"] == "film":
            missing.append(("clip_%02d.mp4" % i, "film", "chay cut_archival.py --record"))
        continue
    d, w, h = probe(p)
    if d < r["dur"] + 0.4: bad.append((i, "NGAN %.2f < o %.2f+0.4" % (d, r["dur"])))
    if (w, h) != (1920, 1080): bad.append((i, "kich thuoc %sx%s" % (w, h)))
    if not a.dry and any(x[1].startswith("LOI") for x in log if x[0] == i): bad.append((i, "animate_still loi"))

MF = CL / "_MISSING_ART.json"
if missing:
    MF.write_text(json.dumps([{"file": f, "layer": l, "note": n} for f, l, n in missing], ensure_ascii=False, indent=1),
                  encoding="utf-8")
    print("🔴 THIEU %d dau vao — CHUA DUOC RENDER VIDEO (so: %s)" % (len(missing), MF))
    for f, l, n in missing[:40]:
        print("   %-14s %-8s %s" % (f, l, n))
elif only is None and MF.exists():
    MF.unlink()
low = [x for x in log if x[2] is not None and x[2] < 3]
if low: print("⚠️ %d o MAD < 3 (gate §2.0-ter): %s -> doi preset manh hon" % (len(low), [x[0] for x in low]))
if bad:
    print("🔴 GATE: %d loi" % len(bad)); [print("  ", b) for b in bad[:30]]
print("KET QUA: %s" % ("SACH" if not bad and not missing else "CHUA XONG"))
sys.exit(0 if not bad and not missing else 1)
