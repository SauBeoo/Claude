# -*- coding: utf-8 -*-
"""Gan clip vao o hinh THEO MUC, khong theo so thu tu.

🔴 BAY DA DINH (bat 2026-09-16 khi soi frame ban render dau):
   · `build_slides_14.py` neo cue theo THOI GIAN (bam moc dong loi, khe > tran thi che).
   · `crop_place_14.py` dat clip theo SO THU TU (slot i <- task_(i+1) <- shot i).
   Hai thu do chi trung nhau khi so SHOT tao viet cho tung MUC khop dung so CUE ma muc
   do chiem. Do thuc te: INTRO tao viet 7 shot ma chi co 2 cue; M3 viet 24 ma co 31.
   => lech don toi ±5 vi tri, tuc vai chuc clip chieu SAI thu dang duoc doc.
   Trieu chung o ban render dau: cau 「玄関で、封筒ごと母親に渡す」 (hien ba o hanh lang)
   lai chieu canh GOI PHONG BI O BAN LAM VIEC.

Cach gan dung: moi cue biet no neo vao DONG nao (cot L### trong _MAP.txt); moi dong thuoc
mot MUC (bien MUC duoi day do tu chinh timeline). Nen:
   voi tung MUC: rai cac shot cua MUC do deu tren cac cue cua MUC do, giu thu tu.
Nhieu cue hon shot -> co shot dung 2 lan; it hon -> bo bot shot cuoi muc. Khong bao gio
lay shot cua muc khac.

⚠️ KHONG can crop lai: `_flow_crop/c<shot>.mp4` da la ban da cat cua dung shot do.
   Buoc nay chi doi HARDLINK, ton 0 byte va vai giay.
"""
import os, re, sys, json, shutil, importlib.util
from pathlib import Path
from collections import Counter

sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
STEM = "14_showa-no-shokuba"
VD = ROOT / "06_VIDEO" / STEM
CROP = VD / "_flow_crop"
DST = VD / "clips"

# --- bien MUC theo CHI SO DONG, do tu timeline (xem tools log 2026-09-16) ---
#     cau mo muc: こんばんは=8 · 一点目=11 · 二点目=30 · 三点目=48 · CTA=68 ·
#                 四点目=69 · 五点目=92 · ket(正直に言えば)=118
BOUND = [("HOOK", 0), ("INTRO", 8), ("M1", 11), ("M2", 30), ("M3", 48),
         ("CTA", 68), ("M4", 69), ("M5", 92), ("KET", 118)]


def block_of_line(li):
    b = BOUND[0][0]
    for name, start in BOUND:
        if li >= start:
            b = name
        else:
            break
    return b


sp = importlib.util.spec_from_file_location("g", str(ROOT / "tools" / "gen_prompts_14.py"))
g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
shots_of = {}
for i, x in enumerate(g.S):
    shots_of.setdefault(x[1], []).append((i, x[0]))

cues = []
for l in (DST / "_MAP.txt").read_text(encoding="utf-8").split("\n"):
    m = re.match(r"\s*(\d+)\s+([\d.]+)s\s+([\d.]+)s\s+L(\d+)", l)
    if m:
        cues.append((int(m.group(1)), float(m.group(2)), int(m.group(4))))
print("cue: %d | shot: %d" % (len(cues), len(g.S)))

by_block = {}
for idx, t, li in cues:
    by_block.setdefault(block_of_line(li), []).append(idx)

DRY = "--dry" in sys.argv
plan, warn = {}, []
print("\n  muc     cue  shot   ket qua")
for name, _ in BOUND:
    cl = by_block.get(name, [])
    sh = shots_of.get(name, [])
    if not cl:
        warn.append("muc %s KHONG co cue nao — %d shot bi bo" % (name, len(sh)))
        continue
    if not sh:
        warn.append("muc %s co %d cue ma KHONG co shot nao" % (name, len(cl)))
        continue
    for k, cue in enumerate(cl):
        j = min(len(sh) - 1, k * len(sh) // len(cl))
        plan[cue] = sh[j]
    used = len({plan[c][0] for c in cl})
    note = ("dung %d/%d shot" % (used, len(sh)) if used < len(sh)
            else ("%d shot lap lai" % (len(cl) - len(sh)) if len(cl) > len(sh) else "khop 1-1"))
    print("  %-6s %4d %5d   %s" % (name, len(cl), len(sh), note))
for w in warn:
    print("  ⚠️ " + w)

# ── BU CHO KHOI THIEU bang shot CHUA DUNG, thay vi LAP clip ─────────────────────
# Chia deu sinh ra shot dung 2 lan o khoi co nhieu cue hon shot. Nhung luat cua he la
# KHONG trung hinh trong cung mot video ([[feedback_slide_khong_trung_anh_trong_video]]).
# Do duoc: tong shot chua dung = 7, tong cho bi lap = 7 — vua du. Uu tien shot CUNG
# BOI CANH voi cho can bu (INTRO toan canh `office` nen lap duoc vao M1/M2/M3/CTA/KET).
PRE = {i: x[3] for i, x in enumerate(g.S)}
used = {si for si, _ in plan.values()}
pool = [(i, g.S[i][0]) for i in range(len(g.S)) if i not in used]
dupe = []
seen = set()
for cue in sorted(plan):
    si = plan[cue][0]
    if si in seen:
        dupe.append(cue)
    seen.add(si)
if dupe and pool:
    print("\n  bu %d cho bi lap bang %d shot chua dung:" % (len(dupe), len(pool)))
    for cue in dupe:
        want = PRE[plan[cue][0]]
        fam = lambda q: q.replace("_rouka", "").replace("_hiru", "")
        cand = ([q for q in pool if PRE[q[0]] == want]
                or [q for q in pool if fam(PRE[q[0]]) == fam(want)] or pool)
        pick = cand[0]
        pool.remove(pick)
        print("    o %3d  %s(%s)  ->  %s(%s)"
              % (cue, plan[cue][1], want, pick[1], PRE[pick[0]]))
        plan[cue] = pick
    left = [q[1] for q in pool]
    print("  con chua dung: %s" % (left or "khong"))

moved = sum(1 for c, (si, _) in plan.items() if c != si)
print("\no phai doi clip: %d/%d (giu nguyen %d)" % (moved, len(plan), len(plan) - moved))
if DRY:
    print("\n(chay thu — them --apply de dat that)")
    sys.exit(0)

ok = 0
for cue, (si, sid) in sorted(plan.items()):
    src = CROP / ("c%03d.mp4" % si)
    if not src.exists():
        print("[CHAN] thieu ban da cat:", src.name); sys.exit(1)
    dst = DST / ("clip_%02d.mp4" % cue)
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
    # 🔴 BAT BUOC (bat 2026-09-16): HARDLINK KHONG DOI mtime — no dung chung inode voi
    #   `_flow_crop/cNNN.mp4` nen mtime van la luc CAT (19:07), trong khi cache chuyen canh
    #   `slides/trans_NN.png` cua luot render truoc la 19:22. Phep kiem stale cua
    #   video_render ("cache cu hon asset thi dung lai") hoi DUNG cau nhung bi mtime lua:
    #   noi dung o do da doi danh tinh ma mtime lai LUI VE. Ket qua: moi cu dissolve 0,4s
    #   trong ca video chieu SHOT CUA BAN MAP CU (170 cu × 0,4s = 68 giay hinh sai).
    #   `os.utime` day mtime len hien tai => cache tu invalidate.
    #   ⓘ Cham inode cung lam `_flow_crop/cNNN.mp4` moi theo — vo hai: crop_place so ban cat
    #     voi file task NGUON, ban cat moi hon thi van bo qua dung.
    os.utime(dst, None)
    ok += 1
(VD / "clips" / "_MAP_BLOCK.txt").write_text(
    "o    <- shot  sid    muc\n" + "\n".join(
        "%3d  <- %3d   %-4s  %s" % (c, si, sid, block_of_line(
            next(li for i, t, li in cues if i == c)))
        for c, (si, sid) in sorted(plan.items())) + "\n", encoding="utf-8")
print("da dat %d/%d o | so tra: clips\\_MAP_BLOCK.txt" % (ok, len(cues)))
sys.exit(0 if ok == len(cues) else 1)
