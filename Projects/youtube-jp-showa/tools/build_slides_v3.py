# -*- coding: utf-8 -*-
"""build_slides_v3.py — SLIDES khuon REAL-FIRST v3 / STYLE A (user chot 2026-09-23).

Vi sao co ban v3 (khac v2 = build_slides_16r.py):
  User: "tam thoi tao khong gen duoc nhieu video AI nua… tuan duoc tam 30 video 8s thoi".
  30 clip/tuan / 3 video/tuan = NGAN SACH 10 CLIP AI / VIDEO. Ban v2 de AI ganh ~35%
  (video 16: 150 o, 53 o AI) va video 17 thi 105/112 o la AI => khong con nuoi noi.
  ⇒ Them LOP 'aistill' = ANH AI TINH (Nano Banana, gen thoai mai) -> animate_still.py
     hoa dong CUC BO, giu toi 18s (Style A cua ban 232K: trung vi 15,8–18,0s/anh).
  ⇒ Clip AI thanh HANG HIEM: chi dat o cho KHAI BAO trong visual_plan.json, co TRAN.

BON LOP, uu tien tu tren xuong:
  film    phim tu lieu PD that (cut_archival.py)      tran 16,0s
  photo   anh THAT (frame phim PD / Commons / NDL)    tran 18,0s  -> animate_still
  aistill anh AI tinh (Nano Banana)                   tran 18,0s  -> animate_still   <- MAC DINH
  ai      clip AI 8s (Flow: STILL -> Animate)         MOT o / moc, <= 9,5s (keo cham <=1,2x)

GIU NGUYEN tu v2 (moi thu la mot loi da tra gia):
  1. cue cung theo dong loi that · 2. gate chay SAU khi ghi · 3. clips/clip_<index>.mp4
  4. snap ranh gioi lop ve moc dong loi · 5. entry 0 = phim that (luat kenh)

visual_plan.json (06_VIDEO/<stem>/visual_plan.json):
  {"default": "aistill",
   "ranges": [[0.0, "film"], [48.3, "aistill"], [300, "photo"], [340, "aistill"]],
   "ai":     [12.0, 30.5, 95.0, ...],            # moi moc = MOT clip AI (neo vao dong gan nhat)
   "preset": [[0, "office"], [500, "kitchen"]]}  # preset hoa dong theo moc
  Khong co file -> default aistill, o dau = film, 0 clip AI (tool in goi y).

Chay:  python tools/build_slides_v3.py <stem> [--dry] [--budget 10] [--out-dir DIR]
Xuat:  03_SCRIPTS/<stem>_SLIDES.json · clips/_PLAN.json · clips/_MAP.txt · clips/_SOURCING.md
"""
import sys, json, math, argparse
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
CAP = {"film": 16.0, "photo": 18.0, "aistill": 18.0}
CAP_HOOK = 5.5      # cold open: o ngan hon (v2: 5,5s la muc khong cat vun mot goc may)
AI_MAX = 9.5        # clip 8s, keo cham toi 1,2x la mat khong nhan ra (video 09/17: toi 1,36x)
AI_NATIVE = 8.0
MIN_CLIP = 2.2
BAND = (3.2, 8.9)   # dai doi hinh/phut do duoc cua nganh (CHANNEL_BENCHMARK_stills_2026-09-08)
EPS = 1e-6
LAYERS = ("film", "photo", "aistill", "ai")

ap = argparse.ArgumentParser()
ap.add_argument("stem")
ap.add_argument("--dry", action="store_true", help="khong ghi SLIDES")
ap.add_argument("--budget", type=int, default=10, help="tran clip AI / video (30/tuan : 3 video)")
ap.add_argument("--out-dir", default=None, help="noi ghi _PLAN/_MAP/_SOURCING (mac dinh <vd>/clips)")
ap.add_argument("--plan", default=None, help="visual_plan.json (mac dinh <vd>/visual_plan.json)")
ap.add_argument("--timeline", default=None, help="mac dinh <vd>/timeline.json; truoc khi co giong: timeline_EST.json")
a = ap.parse_args()

VD = ROOT / "06_VIDEO" / a.stem
OUT = ROOT / "03_SCRIPTS" / (a.stem + "_SLIDES.json")
ODIR = Path(a.out_dir) if a.out_dir else VD / "clips"
PLANF = Path(a.plan) if a.plan else VD / "visual_plan.json"

TLF = Path(a.timeline) if a.timeline else VD / "timeline.json"
d = json.loads(TLF.read_text(encoding="utf-8"))
if "_ESTIMATE" in d or "EST" in TLF.name:
    print("⚠️  TIMELINE UOC LUONG (%s) — SLIDES nay CHUA dung de render; chay lai sau khi co timeline.json that" % TLF.name)
lines, total = d["lines"], d["total"]
starts = [ln["start"] for ln in lines]

plan = json.loads(PLANF.read_text(encoding="utf-8")) if PLANF.exists() else {}
if not plan:
    print("[info] khong co %s -> default aistill, o dau film, 0 clip AI" % PLANF.name)
DEFAULT = plan.get("default", "aistill")
ranges = plan["ranges"] if "ranges" in plan else [[0.0, "film"]]   # khoa co mat (ke ca rong) thi dung dung gia tri do
def _t(x):
    """moc = so giay HOAC mot chuoi loi -> dau dong chua chuoi do (ben voi viec render lai giong)."""
    if isinstance(x, (int, float)):
        return float(x)
    hit = [ln["start"] for ln in lines if x in ln["text"]]
    if len(hit) != 1:
        raise SystemExit("[LOI] moc '%s' khop %d dong (can dung 1)" % (x, len(hit)))
    return hit[0]
ai_marks = sorted(_t(x) for x in plan.get("ai", []))
ranges = [[_t(t), l] for t, l in ranges]
presets = sorted([_t(t), p_] for t, p_ in (plan.get("preset") or [[0.0, "flat"]]))
for _, l in ranges:
    if l not in CAP:
        raise SystemExit("[LOI] lop '%s' trong ranges khong hop le (film/photo/aistill)" % l)

_h = next((ln["start"] for ln in lines if "こんばんは" in ln["text"]), None)
HOOK_END = round(_h, 2) if _h is not None else 45.0
print("cold open het o %.2fs%s" % (HOOK_END, "" if _h is not None else " (KHONG thay loi chao -> mac dinh 45s)"))


def snap(t):
    return 0.0 if t <= 0.01 else min(starts + [total], key=lambda s: abs(s - t))


# ---------- 1. lop NEN theo ranges (snap) ----------
base, seen = [], set()
for t, l in sorted((float(t), l) for t, l in ranges):
    s = snap(t)
    if s in seen:
        continue
    seen.add(s); base.append((s, l))
if not base or base[0][0] > 0.01:
    base.insert(0, (0.0, DEFAULT))


def base_at(t):
    k = DEFAULT
    for s, l in base:
        if s <= t + EPS: k = l
        else: break
    return k


# ---------- 2. o AI: moi moc = mot o ----------
ai_iv = []
for t in ai_marks:
    s = snap(t)
    if s >= total - 1.0 or any(x0 - EPS <= s < x1 - EPS for x0, x1 in ai_iv):
        continue
    nxt = next((x for x in starts if x > s + EPS), total)
    e = nxt if nxt - s <= AI_MAX + EPS else s + AI_NATIVE
    if e - s < MIN_CLIP:          # dong qua ngan -> an them dong sau cho du mot clip
        nx2 = next((x for x in starts if x > nxt + EPS), total)
        e = nx2 if nx2 - s <= AI_MAX + EPS else s + AI_NATIVE
    ai_iv.append((s, min(e, total)))   # 🔴 KHONG round: moc lech 0,001s voi starts -> sinh o 0,00s
ai_iv.sort()

# ---------- 2b. "film_lines": [[chuoi loi, nguon, ss], ...] -> DONG do nuoi bang PHIM THAT ----------
# (thu tu uu tien lop: ai > film_lines > ranges). Nguon + ss di vao _PLAN.json de gen spec cat.
film_iv = []   # (t0, t1, src, ss_dau_dong)
for fl in plan.get("film_lines", []):
    anc, fsrc, fss = fl[0], fl[1], float(fl[2])
    s0 = _t(anc)
    s1 = next((x for x in starts if x > s0 + EPS), total)
    if s0 == starts[0]:
        s0 = 0.0     # dong dau: phim phu ca khoang lang truoc cau 1 (entry 0 = phim that)
    film_iv.append((s0, s1, fsrc, fss))
film_iv.sort()


def film_at(t):
    return next((iv for iv in film_iv if iv[0] - EPS <= t < iv[1] - EPS), None)


# ---------- 3. doan (t0, t1, lop) ----------
# "cuts": ep cat o tai dau cac dong chi dinh (khoanh khac lat dap an can HINH RIENG)
cut_ts = {snap(_t(x)) for x in plan.get("cuts", [])}
bps = sorted({0.0, total} | {s for s, _ in base} | {x for iv in ai_iv for x in iv} | cut_ts
             | {x for iv in film_iv for x in iv[:2]})
segs = []
for t0, t1 in zip(bps, bps[1:]):
    if t1 - t0 < 0.05:
        continue
    lay = ("ai" if any(x0 - EPS <= t0 < x1 - EPS for x0, x1 in ai_iv)
           else "film" if film_at(t0) else base_at(t0))
    if segs and segs[-1][2] == lay and lay != "ai" and t0 not in cut_ts and not (lay == "film" and film_at(t0)):
        segs[-1] = (segs[-1][0], t1, lay)
    else:
        segs.append((t0, t1, lay))


def cap(t0, lay):
    return CAP_HOOK if t0 < HOOK_END - 0.01 else CAP[lay]


# ---------- 4. cat trong tung doan (tham lam theo TRAN) ----------
cells = []   # (t0, t1, lay)
for s0, s1, lay in segs:
    if lay == "ai":
        cells.append((s0, s1, lay)); continue
    cur = s0
    while cur < s1 - 0.05:
        c = cap(cur, lay)
        far = None
        for s in starts:
            if s <= cur + 0.05: continue
            if s - cur > c + EPS or s > s1 + EPS: break
            far = s
        if far is not None and far < s1 - 0.05:
            cells.append((cur, far, lay)); cur = far; continue
        if s1 - cur <= c + EPS:
            cells.append((cur, s1, lay)); cur = s1; continue
        nxt = min(next((s for s in starts if s > cur + 0.05), s1), s1)
        gap = nxt - cur
        n = max(1, math.ceil(gap / c))
        while n > 1 and gap / n < MIN_CLIP: n -= 1
        for k in range(n):
            cells.append((cur + k * gap / n, cur + (k + 1) * gap / n, lay))
        cur = nxt
# gop o rac < MIN_CLIP vao o truoc cung lop
merged = []
for c in cells:
    if merged and c[1] - c[0] < MIN_CLIP and merged[-1][2] == c[2] and c[2] != "ai":
        merged[-1] = (merged[-1][0], c[1], c[2])
    else:
        merged.append(c)
# o dau bai qua ngan (khoang lang truoc cau 1) -> gop VE SAU, khong co o truoc de gop
if len(merged) > 1 and merged[0][1] - merged[0][0] < MIN_CLIP and merged[0][2] == merged[1][2]:
    merged[1] = (merged[0][0], merged[1][1], merged[1][2]); merged.pop(0)
cells = [(round(x0, 2), round(x1, 2), l) for x0, x1, l in merged if x1 - x0 >= 0.05]


# ---------- 5. entry ----------
def owner(t):
    # 🔴 t da ROUND 2 chu so, starts cua timeline THAT thi khong (7,2712 vs 7,27) -> dung EPS 1e-6 la
    #    o bi gan nham sang CAU TRUOC (lech ca match lan offset). Dung sai 0,02s.
    k = 0
    for i, s in enumerate(starts):
        if s <= t + 0.02: k = i
        else: break
    return k


def uniq_match(li):
    txt = lines[li]["text"]
    for n in range(min(6, len(txt)), len(txt) + 1):   # dong ngan hon 6 ky (「姉です。」) van phai match duoc
        m = txt[:n]
        if next(i for i, ln in enumerate(lines) if m in ln["text"]) == li:
            return m
    return None


def preset_at(t):
    k = "flat"
    for s, p in presets:
        if float(s) <= t + EPS: k = p
        else: break
    return k


entries, rows, prow, bad = [], [], [], []
for idx, (t0, t1, lay) in enumerate(cells):
    li = owner(t0); m = uniq_match(li)
    if m is None:
        bad.append((idx, li)); m = lines[li]["text"][:10]
    entries.append({"match": m, "video": True, "source": "clips/clip_%02d.mp4" % idx,
                    "offset": round(max(0.0, t0 - lines[li]["start"]), 2), "dur": round(t1 - t0, 2)})
    row = {"idx": idx, "t": t0, "dur": round(t1 - t0, 2), "layer": lay, "line": li,
           "preset": preset_at(t0), "text": lines[li]["text"][:60]}
    if any(_t(a_) - EPS <= t0 < _t(b_) - EPS for a_, b_ in plan.get("bw", [])):
        row["bw"] = True    # make_cells_v3 bo mau (khop tong phim den trang cua doan do)
    fi = film_at(t0 + 0.01) if lay == "film" else None
    if fi:   # vi tri trong phim = ss dau dong + do lech cua o so voi dau dong
        row["src"] = fi[2]; row["ss"] = round(fi[3] + (t0 - fi[0]), 2)
    prow.append(row)
    rows.append("%3d  %7.2fs  %5.2fs  %-7s  L%-3d  %s" % (idx, t0, t1 - t0, lay, li, lines[li]["text"][:32]))

ODIR.mkdir(parents=True, exist_ok=True)
if not a.dry:
    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
(ODIR / "_MAP.txt").write_text("idx     bat dau    dai  lop      dong  loi\n" + "\n".join(rows) + "\n", encoding="utf-8")
(ODIR / "_PLAN.json").write_text(json.dumps(prow, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- 6. SOURCING — bang "can gi, tu dau" ----------
sec = Counter(); cnt = Counter()
for r in prow:
    sec[r["layer"]] += r["dur"]; cnt[r["layer"]] += 1
src_md = ["# SOURCING %s — REAL-FIRST v3 (Style A)" % a.stem, "",
          "| lop | so o | giay | % | lay o dau | file vao |", "|---|---|---|---|---|---|"]
WHERE = {"film": ("phim PD: gen_archival -> `cut_archival.py --record`", "`clips/clip_NN.mp4` (cut_archival ghi thang)"),
         "photo": ("frame phim PD / Commons PD / NDL — verify license", "`cells_in/NN.jpg|png`"),
         "aistill": ("Nano Banana (Flow Image) — prompt STILL", "`cells_in/NN.png`"),
         "ai": ("Flow: STILL -> ⋮ Animate -> MOTION (Veo)", "`cells_in/NN.mp4`")}
for l in LAYERS:
    src_md.append("| %s | %d | %.0f | %.1f | %s | %s |" % (l, cnt[l], sec[l], 100 * sec[l] / total, *WHERE[l]))
for l in LAYERS:
    src_md += ["", "## %s (%d)" % (l, cnt[l]), ""]
    src_md += ["- `%02d` %6.1fs  %4.1fs  [%s]  %s" % (r["idx"], r["t"], r["dur"], r["preset"], r["text"])
               for r in prow if r["layer"] == l]
(ODIR / "_SOURCING.md").write_text("\n".join(src_md) + "\n", encoding="utf-8")

# ---------- 7. GATE (SAU khi ghi) ----------
durs = [r["dur"] for r in prow]
per_min = len(prow) / (total / 60)
real = sec["film"] + sec["photo"]
ok = True
print("=== SLIDES %s REAL-FIRST v3 ===%s" % (a.stem, " (CHAY THU)" if a.dry else ""))
print("tong      : %.1fs = %.2f phut | %d dong loi" % (total, total / 60, len(lines)))
print("so o      : %d  ->  %.1f doi hinh/phut (dai nganh %.1f–%.1f)" % (len(prow), per_min, *BAND))
for l in LAYERS:
    print("  %-7s : %3d o | %6.1fs | %4.1f%%" % (l, cnt[l], sec[l], 100 * sec[l] / total))
print("hinh THAT : %.1f%% (film+photo) — bao cao, khong chan (v3 cho phep aistill ganh)" % (100 * real / total))
nonai = [r["dur"] for r in prow if r["layer"] != "ai" and r["t"] >= HOOK_END]
if nonai:
    s_ = sorted(nonai)
    print("giu anh   : trung vi %.1fs | max %.1fs (than bai, khong tinh o AI)" % (s_[len(s_) // 2], s_[-1]))
print("-" * 64)
over = [(r["idx"], r["layer"], r["dur"]) for r in prow if r["layer"] != "ai" and r["dur"] > cap(r["t"], r["layer"]) + 0.01]
over += [(r["idx"], "ai", r["dur"]) for r in prow if r["layer"] == "ai" and r["dur"] > AI_MAX + 0.01]
if over: print("[CHAN] %d o vuot tran: %s" % (len(over), over[:8])); ok = False
else:    print("[OK  ] khong o nao vuot tran (film 16 · photo/aistill 18 · ai %.1f · hook %.1f)" % (AI_MAX, CAP_HOOK))
if cnt["ai"] > a.budget: print("[CHAN] %d clip AI > ngan sach %d/video" % (cnt["ai"], a.budget)); ok = False
else:                    print("[OK  ] clip AI %d / ngan sach %d" % (cnt["ai"], a.budget))
if bad: print("[CHAN] %d match KHONG duy nhat: %s" % (len(bad), bad[:5])); ok = False
else:   print("[OK  ] match duy nhat")
if prow[0]["layer"] != "film": print("[CHAN] entry 0 phai la 'film' (luat kenh)"); ok = False
else:                          print("[OK  ] entry 0 = phim that")
if not (BAND[0] <= per_min <= BAND[1]):
    print("[warn] %.1f doi hinh/phut nam NGOAI dai nganh %.1f–%.1f" % (per_min, *BAND))
str_ai = [(r["idx"], round(r["dur"] / AI_NATIVE, 2)) for r in prow if r["layer"] == "ai" and r["dur"] > AI_NATIVE]
if str_ai: print("[info] o AI phai keo cham (>8s): %s" % str_ai)
if cnt["ai"] == 0: print("[goi y] chua khai bao clip AI: dat ~3 moc trong 60s dau + 1/chuong o dinh + 1 o ket (visual_plan.json 'ai')")
print("-" * 64)
print("SLIDES   -> %s" % (OUT if not a.dry else "(chay thu, KHONG ghi)"))
print("PLAN/MAP/SOURCING -> %s" % ODIR)
print("KET QUA: %s" % ("SACH" if ok else "CO LOI CHAN"))
sys.exit(0 if ok else 1)
