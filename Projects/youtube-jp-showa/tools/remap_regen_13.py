# -*- coding: utf-8 -*-
"""Video 13: doi so thu tu cua LO GEN LAI ve DUNG so o.

🔴 BAY PHAI VA, khong phai tien nghi. Extension dat ten `task_NNN_*.mp4` theo **so dong cua
   file duoc bom**. Bom `videogen_REGEN_FLOW.txt` (98 dong) thi no danh so task_001..task_098
   — trong khi 98 clip do thuoc cac o 0,1,2,3,4,6,11,... rai suot 162 o. Do thang vao
   `F:\\Youtube\\showa_13_uyfd62mb` thi clip cua o 0 de len clip cua o 0 (dung), clip cua o 1
   de len o 1 (dung), nhung clip thu 7 (o 11) lai de len o 6 — **lech tu do den het bai, va
   khong mot dong loi nao**. Cung ho voi bay §2.5 `render-background.md`: tool tim thay MOT
   file khop ten khong co nghia la no tim thay DUNG file.

Cach dung:
    python tools\\remap_regen_13.py "F:\\Youtube\\<folder_lo_gen_lai>"
    python tools\\remap_regen_13.py "F:\\Youtube\\<folder>" --dry     # xem truoc, khong ghi

Sau khi chay: `crop_place_13.py` khong can sua gi — no da co san luat "vai so co 2 ban
(gen lai): lay ban MOI NHAT", va file dat ra day co mtime moi hon.
"""
import os, re, sys, glob, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "13_kosodate-joushiki"
# --map <NHOM> de doi chieu theo mot NHOM (A_30GIAY / B_DONGNGUOI / C_TRONGNHA).
# 🔴 Bat buoc khop: bom FLOW cua nhom nao thi --map DUNG nhom do. Bom nhom A ma doi
#    chieu bang ban do ca 98 dong thi 6 clip se roi vao 6 o dau cua ban do lon =>
#    dung o 0..4 va LECH o thu 6. Sai kieu nay khong co dong loi nao.
_g = [a.split("=", 1)[1] if "=" in a else None for a in sys.argv if a.startswith("--map")]
_grp = _g[0] if _g and _g[0] else (
    sys.argv[sys.argv.index("--map") + 1] if "--map" in sys.argv[:-1] else None)
MAP = VD / ("videogen_REGEN_%s_TENFILE.txt" % _grp if _grp else "videogen_REGEN_TENFILE.txt")
DST = Path(r"F:\Youtube\showa_13_uyfd62mb")     # kho task_NNN goc ma crop_place doc

args = [a for a in sys.argv[1:] if not a.startswith("--")
        and not (("--map" in sys.argv[:-1]) and a == sys.argv[sys.argv.index("--map") + 1])]
DRY = "--dry" in sys.argv
if not args:
    print(__doc__)
    sys.exit(2)
SRC = Path(args[0])

if not MAP.exists():
    print("[CHAN] chua co", MAP.name, "— chay lai buoc doi chieu FLOW truoc")
    sys.exit(1)
if not SRC.is_dir():
    print("[CHAN] khong thay folder lo gen lai:", SRC)
    sys.exit(1)

# dong REGEN (1-based)  ->  o so (0-based)
pairs = []
for ln in MAP.read_text(encoding="utf-8").split("\n"):
    m = re.match(r"\s*(\d+)\s+o\s+(\d+)\s+(\S+)", ln)
    if m:
        pairs.append((int(m.group(1)), int(m.group(2)), m.group(3)))
print("ban do: %d dong REGEN -> %d o" % (len(pairs), len({p[1] for p in pairs})))

# task_NNN trong lo gen lai (co 2 ban thi lay moi nhat)
raw = {}
for f in glob.glob(str(SRC / "task_*.mp4")):
    n = int(re.search(r"task_(\d+)_", os.path.basename(f)).group(1))
    if n not in raw or os.path.getmtime(f) > os.path.getmtime(raw[n]):
        raw[n] = f
print("lo gen lai: %d clip" % len(raw))

thieu = [j for j, _, _ in pairs if j not in raw]
if thieu:
    print("[CHAN] lo gen lai thieu dong REGEN:", thieu)
    print("       (gen du 98 clip roi hay chay lai — dat thieu la lech o)")
    sys.exit(1)

if not DRY:
    DST.mkdir(parents=True, exist_ok=True)
ok = 0
for j, slot, name in pairs:
    src = Path(raw[j])
    dst = DST / ("task_%03d_regen.mp4" % (slot + 1))     # crop_place: slot i <- task_(i+1)
    print("  REGEN %3d -> o %3d  %-34s %s" % (j, slot, name, dst.name))
    if DRY:
        continue
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)          # cung o F: thi hardlink, 0 byte ton them
    except OSError:
        shutil.copy2(src, dst)
    os.utime(dst, None)            # mtime moi => crop_place se cat lai o nay
    ok += 1

print("\n%s %d/%d clip" % ("(chay thu) se dat" if DRY else "DA DAT", len(pairs) if DRY else ok, len(pairs)))
if not DRY:
    print("Tiep: 06_VIDEO\\run_build13.cmd  (crop -> anh that -> ghep -> va duoi)")
sys.exit(0)
