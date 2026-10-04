# -*- coding: utf-8 -*-
"""build_slides_22.py — SLIDES video 22 theo KHUON v08, doc thang bang PLAN theo dong cua plan_22.py.

Khac build_slides_v3 (chia lop theo visual_plan.json): o day moi dong TTS da co san danh sach o hinh
(plan_22.PLAN). Tool nay chi lam 3 viec:
  1. neo so dong file TTS -> dong trong timeline.json (doi chieu CHU, khong tin thu tu mu)
  2. chia khoang thoi gian cua dong (tu dau dong toi dau dong ke tiep — dung cach renderer do khe)
     deu cho cac o cua dong; dong co [] thi o truoc KEO DAI qua dong do
  3. ghi 03_SCRIPTS/<stem>_SLIDES.json + clips/_PLAN.json + clips/_MAP.txt, roi GATE sau khi ghi
O +NUM: chu so (chu so A-rap) ve bang FONT len anh that — chu lay NGUYEN tu cau dang doc (NUMTXT).
    python tools/build_slides_22.py [--dry]
"""
import sys, json, re, math
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.argv, _argv = [sys.argv[0]], sys.argv            # plan_22 doc argv khi import -> cat tam
sys.path.insert(0, str(Path(__file__).parent))
import plan_22 as P
sys.argv = _argv

STEM = "22_kieta-shigoto"
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / STEM
CL = VD / "clips"
TTS = ROOT / "03_SCRIPTS" / (STEM + "_TTS.md")
AI_DIR = VD / "cells_in_ai"
REAL = VD / "real_22"
MARGIN = 0.5
AI_MAX = 8.0 * 1.2          # clip AI 8s, keo cham toi da 1,2x

# chu tren o +NUM: khai o plan_22.NUMTXT_T (theo chi so timeline), plan_22 tu doi sang so dong file
NUMTXT = P.NUMTXT

TAG = re.compile(r"\[[^\]]*\]")


def norm(s):
    return re.sub(r"\s+", "", TAG.sub("", s))


def ai_file(name):
    c = sorted(AI_DIR.glob("ai_[0-9][0-9]_%s.*" % name))
    return c[0] if c else None


def real_src(code, man):
    m = man.get(code)
    return (REAL / m["file"], m["kind"]) if m else (None, None)


def dhash(path):
    """dHash 64 bit — anh: chinh no; clip: frame o giua (ffmpeg)."""
    import subprocess, io as _io
    from PIL import Image
    p = VD / path
    if p.suffix.lower() in (".mp4", ".webm", ".ogv", ".mov"):
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                           capture_output=True, text=True).stdout.strip()
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.2f" % (float(d or 2) / 2), "-i", str(p),
                              "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        im = Image.open(_io.BytesIO(raw))
    else:
        im = Image.open(p)
    g = im.convert("L").resize((9, 8), Image.LANCZOS)
    px = list(g.getdata())
    return sum(1 << k for k in range(64) if px[(k // 8) * 9 + k % 8] > px[(k // 8) * 9 + k % 8 + 1])


def near_dups(rows, thr=6):
    hs, out = [], []
    for r in rows:
        try:
            h = dhash(r["src"])
        except Exception as e:
            print("⚠️ khong bam duoc", r["src"], e); continue
        for c, h2 in hs:
            if bin(h ^ h2).count("1") <= thr:
                out.append((c, r["code"]))
        hs.append((r["code"], h))
    return out


def main(dry=False):
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
    lines, total = tl["lines"], tl["total"]
    # 1) so dong file -> chi so timeline (doi chieu chu)
    raw = TTS.read_text(encoding="utf-8").splitlines()
    fmap, j = {}, 0
    for n, l in enumerate(raw, 1):
        if not norm(l):
            continue
        while j < len(lines) and norm(lines[j]["text"])[:8] != norm(l)[:8]:
            j += 1
        if j >= len(lines):
            sys.exit("🔴 khong neo duoc dong %d vao timeline: %s" % (n, l[:30]))
        fmap[n] = j; j += 1
    starts = [x["start"] for x in lines] + [total]
    planned = {n for n, _ in P.PLAN}
    loose = sorted(set(fmap) - planned)
    if loose:
        print("⚠️ dong TTS khong co trong PLAN (o truoc keo dai qua):", loose)

    # 2) gom nhom: dong co o -> mo nhom moi; dong [] / khong co trong PLAN -> keo dai nhom truoc
    plan = dict(P.PLAN)
    groups = []
    for n in sorted(fmap):
        i = fmap[n]
        cs = plan.get(n, [])
        if cs:
            groups.append({"line": n, "i": i, "t0": starts[i], "t1": starts[i + 1], "cells": cs})
        else:
            if not groups:
                sys.exit("🔴 dong dau tien khong co o hinh")
            groups[-1]["t1"] = starts[i + 1]

    man = json.loads((REAL / "MANIFEST.json").read_text(encoding="utf-8")) if (REAL / "MANIFEST.json").exists() else {}
    out, slides, missing, warn = [], [], [], []
    for g in groups:
        n_c = len(g["cells"]); span = g["t1"] - g["t0"]
        # o AI (clip 8s) co tran -> phan con lai chia cho o that
        ai_idx = [k for k, c in enumerate(g["cells"]) if c.startswith("AI:") and (ai_file(c[3:]) or Path("x")).suffix == ".mp4"]
        durs = [span / n_c] * n_c
        if ai_idx and n_c > len(ai_idx) and span / n_c > AI_MAX:
            pass
        elif ai_idx and n_c > len(ai_idx):
            # cho clip AI du do dai tu nhien (~8s) neu dong du dai, o that nhan phan con lai
            want = min(8.0, span / n_c * 1.6)
            rest = span - want * len(ai_idx)
            if rest / (n_c - len(ai_idx)) >= 3.0:
                durs = [want if k in ai_idx else rest / (n_c - len(ai_idx)) for k in range(n_c)]
        t = g["t0"]; numk = 0
        for k, code in enumerate(g["cells"]):
            d = durs[k]
            base = code.replace("+NUM", "")
            r = {"idx": len(out), "t": round(t, 3), "dur": round(d, 3), "line": g["line"],
                 "text": lines[g["i"]]["text"], "code": base}
            if base.startswith("AI:"):
                f = ai_file(base[3:])
                r["layer"] = "ai" if (f and f.suffix == ".mp4") else "aistill"
                r["src"] = str(f.relative_to(VD)) if f else None
                if not f: missing.append((r["idx"], base))
                if r["layer"] == "ai" and d + MARGIN > AI_MAX:
                    warn.append("o %d %s dai %.1fs > tran clip AI %.1fs (se keo cham qua 1,2x)" % (r["idx"], base, d, AI_MAX))
            else:
                f, kind = real_src(base, man)
                r["layer"] = "video" if kind == "video" else "photo"
                r["src"] = str(f.relative_to(VD)) if f else None
                if not f or not f.exists(): missing.append((r["idx"], base))
            if "+NUM" in code:
                key = (g["line"], numk); numk += 1
                if key not in NUMTXT:
                    sys.exit("🔴 thieu chu cho o +NUM %s" % (key,))
                r["num"] = NUMTXT[key]
            out.append(r)
            # match: renderer lay dong DAU TIEN chua chuoi (video_render.py:513) -> can tien to ma dong khop
            # dau tien CHINH LA dong neo. Dong lap nguyen van mot dong truoc (hook dong 6 == dong 114)
            # thi khong neo duoc -> lui ve dong truoc gan nhat neo duoc, offset cong them.
            li = max(x for x in range(len(lines)) if lines[x]["start"] <= t + 1e-6) if t > 0 else 0
            a, m = li, None
            while m is None and a >= 0:
                txt = lines[a]["text"]
                for L in range(6, len(txt) + 1):
                    if next(x for x in range(len(lines)) if txt[:L] in lines[x]["text"]) == a:
                        m = txt[:L]; break
                else:
                    a -= 1
            if m is None:
                sys.exit("🔴 khong neo duoc o %d" % r["idx"])
            if a != li:
                print("  o %d: dong %d lap chu dong truoc -> neo dong %d + %.2fs" % (r["idx"], li, a, t - lines[a]["start"]))
            slides.append({"match": m, "video": True, "source": "clips/clip_%02d.mp4" % r["idx"],
                           "offset": round(t - lines[a]["start"], 3), "dur": round(d, 3)})
            t += d

    # 3) GATE (chay tren du lieu SE GHI)
    used = Counter(r["code"] for r in out)
    dup = [c for c, v in used.items() if v > 1]
    ds = sorted(r["dur"] for r in out)
    med = ds[len(ds) // 2]
    per_min = len(out) / (total / 60)
    print("o: %d | tong %.1fs (%.2f phut) | giu trung vi %.1fs | dai nhat %.1fs | %.1f doi/phut"
          % (len(out), total, total / 60, med, ds[-1], per_min))
    print("lop:", dict(Counter(r["layer"] for r in out)), "| o so lieu:", sum(1 for r in out if "num" in r))
    long_ = [(r["idx"], r["code"], r["dur"]) for r in out if r["dur"] > 12]
    if long_: print("⚠️ o > 12s:", long_)
    for w in warn: print("⚠️", w)
    bad = []
    if dup: bad.append("ma lap trong video: %s" % dup)
    # 🔴 user 2026-09-26: "khong de lap hinh anh va video trong cung 1 video" — ma khac nhau van co the
    # cung MOT nguon (Pexels tra cung clip cho 2 tu khoa; Commons co ban sao). Gate theo danh tinh that.
    page = Counter(man[r["code"]]["page"] for r in out if r["code"] in man)
    dpage = [p for p, v in page.items() if v > 1]
    if dpage: bad.append("CUNG NGUON o nhieu ma: %s" % dpage)
    near = near_dups([r for r in out if r.get("src")], thr=10)   # 10: bat duoc 2 anh 1円 khac file ma nhin y het
    if near: bad.append("HINH GAN TRUNG (dHash<=10): %s" % near)
    if abs(sum(r["dur"] for r in out) - total) > 0.05: bad.append("tong dur lech timeline")
    if missing: print("🔴 THIEU nguon %d o:" % len(missing), missing[:20])
    if bad:
        for b in bad: print("🔴", b)
        return 1
    if dry:
        print("(dry) khong ghi"); return 0
    CL.mkdir(parents=True, exist_ok=True)
    (ROOT / "03_SCRIPTS" / (STEM + "_SLIDES.json")).write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (CL / "_PLAN.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (CL / "_MAP.txt").write_text("\n".join("clip_%02d  %6.2f  %5.2fs  %-7s %-28s %s" % (
        r["idx"], r["t"], r["dur"], r["layer"], r["code"], " / ".join(r.get("num", []))) for r in out), encoding="utf-8")
    # gate sau khi ghi: moi match tim dung dong, offset khong am
    chk = json.loads((ROOT / "03_SCRIPTS" / (STEM + "_SLIDES.json")).read_text(encoding="utf-8"))
    for s, r in zip(chk, out):
        k0 = next(x for x in range(len(lines)) if s["match"] in lines[x]["text"])   # dung cach renderer tim
        if s["offset"] < -1e-6 or abs(lines[k0]["start"] + s["offset"] - r["t"]) > 0.01:
            print("🔴 match hong:", s); return 1
    print("GHI: SLIDES %d o · clips/_PLAN.json · _MAP.txt" % len(chk))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main("--dry" in sys.argv))
