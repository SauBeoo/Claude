# -*- coding: utf-8 -*-
"""assemble_clips_16.py — lap 3 LOP vao `clips/clip_NN.mp4` theo `_PLAN.json`.

  film  -> real_film/a16_NNN.mp4     (cut_archival tu phim PD)
  still -> real_still/s16_NNN.mp4    (grab_stills + animate_still)
  ai    -> clips_named/clip_*.mp4    (220 clip t2v DA GEN, chon lai ~77)

🔴 Ten dich BAT BUOC la `clip_{i:02d}.mp4` theo SO THU TU SLOT — `video_render.py`
dong 516 doc dung ten do. Dat ten mo ta thi renderer coi nhu KHONG CO CLIP va am
tham fallback anh tinh, ma preflight van in dau tick (CLAUDE.md §Visual).

Chon clip AI:
 · theo KHOI (hook/m1..m5/bridge/ket) suy tu moc thoi gian cua o;
 · LAY MAU DEU trong danh sach cua khoi (stride = co/can) — clip duoc gen theo thu tu
   kich ban, nen lay mau deu giu duoc mach ke; lay N clip dau se chi phu 1/3 dau khoi;
 · boi canh `ima_ie` (canh thoi NAY, prep_clips_16.py CO Y khong grade) chi duoc dung
   cho o co chu 「今」/「いま」/「現在」 trong loi. Lop film 1946 nay chiem 40% thoi
   luong, nen mot canh digital sach xen vao giua se lo ngay neu khong dung cho.

Gate: clip NGAN HON o => renderer `-stream_loop` LAP clip (CLAUDE.md §Visual) => CHAN.
"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD   = ROOT / "06_VIDEO" / "16_omiai-kekkon"
DRY  = "--dry" in sys.argv

BOUND = [(0, 62.3, "hook"), (62.3, 250.2, "m1"), (250.2, 411.0, "m2"), (411.0, 593.8, "m3"),
         (593.8, 631.0, "bridge"), (631.0, 795.9, "m4"), (795.9, 997.8, "m5"), (997.8, 1e9, "ket")]
def blk(t):
    for a, b, k in BOUND:
        if a <= t < b: return k
    return "ket"

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(p)], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return 0.0

plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))

# ---------- kho clip AI ----------
pat = re.compile(r"clip_([A-Z]\d+[a-z]*)_([a-z0-9]+)_(.+)\.mp4")
pool = {}
for p in sorted((VD / "clips_named").glob("clip_*.mp4")):
    m = pat.match(p.name)
    if m: pool.setdefault(m.group(2), []).append((p, m.group(3)))

ai_slots = [r for r in plan if r["layer"] == "ai"]
# 🔴 CHI kanji 今 va 現在. ⛔ TUYET DOI khong dua 「いま」 vao day: no la CHUOI CON cua
# duoi dong tu 〜てい・ます / 〜てい・ました, nen khop vao gan nhu moi cau ke qua khu.
# Do that: 5/6 lan dung ima_ie la duong tinh gia — 「終わっていました」「辞めています」
# 「使われていました」「拍手をしていました」「呼んでいます」 => canh NOI THAT HIEN DAI
# (sofa, laptop) roi vao dung nhung cau dang ke chuyen 1948-1986.
IMA = ("今", "現在")
chosen, used = {}, set()
for k in sorted({blk(r["t"]) for r in ai_slots}):
    slots = [r for r in ai_slots if blk(r["t"]) == k]
    cands = pool.get(k, [])
    ima  = [c for c in cands if c[1] == "ima_ie"]
    norm = [c for c in cands if c[1] != "ima_ie"]
    if len(norm) < len(slots):                       # thieu thi moi dung toi ima_ie
        norm = norm + ima; ima = []
    if not norm:
        print(f"🔴 khoi {k}: khong co clip AI nao"); sys.exit(1)
    step = len(norm) / len(slots)
    for j, r in enumerate(slots):
        want_ima = any(w in r["text"] for w in IMA) and ima
        if want_ima:
            src = ima.pop(0)[0]
        else:
            i = int(j * step)
            while i < len(norm) and norm[i][0] in used: i += 1
            if i >= len(norm):
                i = next((x for x, c in enumerate(norm) if c[0] not in used), None)
                if i is None: print(f"🔴 khoi {k} het clip"); sys.exit(1)
            src = norm[i][0]
        used.add(src); chosen[r["idx"]] = src

# ---------- lap ----------
dst_dir = VD / "clips"; dst_dir.mkdir(exist_ok=True)
rows, short, miss = [], [], []
for r in plan:
    i, lay = r["idx"], r["layer"]
    if lay == "film":  src = VD / "real_film"  / ("a16_%03d.mp4" % i)
    elif lay == "still": src = VD / "real_still" / ("s16_%03d.mp4" % i)
    else: src = chosen[i]
    if not src.exists(): miss.append((i, lay, src.name)); continue
    d = dur(src)
    if d + 0.05 < r["dur"]: short.append((i, lay, round(d, 2), r["dur"], src.name))
    dst = dst_dir / ("clip_%02d.mp4" % i)
    if not DRY:
        if dst.exists() or dst.is_symlink(): dst.unlink()
        try: os.link(src, dst)
        except OSError: shutil.copy2(src, dst)
    rows.append("%3d  %7.2fs %5.2fs  %-5s  %-34s  %s" % (i, r["t"], r["dur"], lay, src.name, r["text"][:26]))

# don clip thua cua ban 220 o cu
stale = [p for p in dst_dir.glob("clip_*.mp4")
         if not p.name[5:-4].isdigit() or int(p.name[5:-4]) >= len(plan)]
if not DRY:
    for p in stale: p.unlink()
    (dst_dir / "_MAP.txt").write_text(
        "idx     bat dau   dai  lop    nguon                               loi\n" + "\n".join(rows) + "\n",
        encoding="utf-8")

import collections
c = collections.Counter(r["layer"] for r in plan)
print("=== LAP CLIP video 16 ===%s" % (" (CHAY THU)" if DRY else ""))
print("o: %d  (film %d · still %d · ai %d)" % (len(plan), c["film"], c["still"], c["ai"]))
print("da xoa %d clip thua cua ban 220 o cu" % len(stale))
ok = True
if miss:
    print("🔴 THIEU %d clip nguon:" % len(miss))
    for m in miss[:12]: print("   o%-4d %-5s  %s" % m)
    ok = False
else: print("[OK  ] du %d clip nguon" % len(plan))
if short:
    print("🔴 %d clip NGAN HON o (renderer se LAP clip):" % len(short))
    for s in short[:12]: print("   o%-4d %-5s clip %.2fs < o %.2fs  %s" % s)
    ok = False
else: print("[OK  ] moi clip deu >= do dai o cua no")
print("MAP -> %s" % (dst_dir / "_MAP.txt"))
print("KET QUA: %s" % ("SACH" if ok else "CO LOI CHAN"))
sys.exit(0 if ok else 1)
