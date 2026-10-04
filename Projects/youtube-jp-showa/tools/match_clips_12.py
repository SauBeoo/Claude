# -*- coding: utf-8 -*-
"""Khop 170 clip Flow (ten theo NOI DUNG) -> 165 slot cua video 12.

🔴 VI SAO KHONG KHOP THEO THU TU: thu tu file trong zip KHONG phai thu tu prompt
   (zip dau tien mo bang "Woman_taking_down_mosquito_net" = shot B1 = slot 39, khong phai H0),
   va mtime trong zip chi co 3-4 moc = gio TAI VE, khong phai gio gen. Khop sai thu tu =
   dung cai loi "hook lech mot nhip" da ghi trong CLAUDE.md §Visual.
   => Khop bang NOI DUNG: ten Flow sinh ra tu chinh prompt nen trung tu vung voi ACT.

Chay:
    python tools/match_clips_12.py            -> chi bao cao, khong dung file nao
    python tools/match_clips_12.py --apply    -> chep sang clips_named/ dung ten TENFILE
"""
import sys, os, re, ast, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "12_natsu-atarimae"
RAW = VD / "_flow_raw"
NAMED = VD / "clips_named"
TEN = VD / "videogen_TENFILE.txt"
GEN = ROOT / "tools" / "gen_prompts_12.py"

STOP = set("a an the of on in at to and then while with his her its into out from for by "
           "over under up down back again one two both it them he she they there that this "
           "as is are be being not no".split())

# tu khoa dac trung cua tung boi canh -> thuong diem khi ten file co no
PRESET_KEY = {
    "zashiki":    "net mosquito bedding tatami room night coil indoors",
    "engawa":     "veranda boards chime glass door garden porch tatami",
    "ido":        "well bucket rope kerb yard water melon",
    "daidokoro":  "kitchen chest ice jug sink shelf tray",
    "michi_natsu": "lane street residential window fence walking dust",
    "koriya":     "cart handcart ice saw straw lane block",
    "undoujou":   "ground sports field line lime cap whistle school",
    "mizunomi":   "tap taps trough water drinking fountain concrete",
    "genkansaki": "pail dirt entrance step splashing sprinkling water lane",
    "nokishita":  "reed screen blind eaves shade bamboo striped",
    "niwa_yoru":  "garden tub wash hedge lantern night sparkler coil",
    "machi_yoru": "bench lane night lantern board game sparkler fan",
}


# Preset moi them sau nay (vd `zashiki_asa`) khong co trong bang tren => tu suy tu chinh
# mo ta boi canh trong P cua gen_prompts_12.py. Bang tay chi de THUONG them, khong bat buoc.
_PK_CACHE = {}


def _pk_auto(pre):
    if pre in _PK_CACHE:
        return _PK_CACHE[pre]
    import ast as _ast
    src = GEN.read_text(encoding="utf-8")
    got = set()
    m = re.search(r'^P = \{(.*?)^\}', src, re.S | re.M)
    if m:
        try:
            d = _ast.literal_eval("{" + m.group(1) + "}")
            got = set(toks(d.get(pre, "")))
        except Exception:
            pass
    _PK_CACHE[pre] = got
    return got


def toks(s):
    return [w for w in re.split(r"[^a-z]+", s.lower()) if w and w not in STOP and len(w) > 2]


# ---- doc 165 shot tu gen_prompts_12.py ----
shots = []
for ln in GEN.read_text(encoding="utf-8").split("\n"):
    s = ln.strip()
    if not (s.startswith('("') or s.startswith("('")) or not s.endswith("),"):
        continue
    try:
        t = ast.literal_eval(s[:-1])
    except Exception:
        continue
    if len(t) >= 8:
        shots.append(list(t))

# ---- doc ten dich tu TENFILE ----
dest = []
for ln in TEN.read_text(encoding="utf-8").splitlines():
    m = re.match(r"\s*(\d+)\s+(\S+\.mp4)", ln)
    if m:
        dest.append((int(m.group(1)) - 1, m.group(2)))
dest.sort()

if len(shots) != len(dest):
    print("[CHAN] gen_prompts co %d shot nhung TENFILE co %d dong" % (len(shots), len(dest)))
    sys.exit(1)

files = sorted(p.name for p in RAW.glob("*.mp4"))
print("shot can khop : %d" % len(shots))
print("clip co san   : %d" % len(files))
print("")

ftok = {}
for f in files:
    base = re.sub(r"_\d{14}(_\d+)?(__\d+)?\.mp4$", "", f)
    ftok[f] = (base, set(toks(base)))


def score(i, f):
    """Diem khop giua shot i va file f."""
    sid, blk, act, pre, cam = shots[i][0], shots[i][1], shots[i][2], shots[i][3], shots[i][4]
    base, ft = ftok[f]
    # ACT: 22 tu dau la phan Flow dung de dat ten
    at = set(toks(" ".join(act.split()[:22])))
    pk = set(PRESET_KEY.get(pre, "").split()) or _pk_auto(pre)
    sc = 3.0 * len(ft & at) + 2.0 * len(ft & pk)
    # gioi tinh / vai dien: tranh gan clip "Woman_" vao shot cua A_CHICHI
    low = act.lower()
    if "woman" in ft and ("a_haha" in low or "a_tonari" in low):
        sc += 2
    if "man" in ft and ("a_chichi" in low or "a_sensei" in low or "a_kori" in low or "a_rojin" in low):
        sc += 2
    if ("child" in ft or "boy" in ft or "figure" in ft) and ("a_ko" in low or "a_seito" in low):
        sc += 2
    # phat khi lech gioi tinh ro rang
    if "woman" in ft and ("a_chichi" in low or "a_sensei" in low or "a_rojin" in low) \
            and "a_haha" not in low and "a_tonari" not in low:
        sc -= 4
    if "man" in ft and ("a_haha" in low or "a_tonari" in low) \
            and "a_chichi" not in low and "a_sensei" not in low \
            and "a_kori" not in low and "a_rojin" not in low:
        sc -= 4
    return sc


# ---- gan tham lam: lay cap diem cao nhat truoc ----
pairs = []
for i in range(len(shots)):
    for f in files:
        s = score(i, f)
        if s > 0:
            pairs.append((s, i, f))
pairs.sort(key=lambda x: -x[0])

asg, usedf, usedi = {}, set(), set()
for s, i, f in pairs:
    if i in usedi or f in usedf:
        continue
    asg[i] = (f, s)
    usedi.add(i)
    usedf.add(f)

missing = [i for i in range(len(shots)) if i not in asg]
unused = [f for f in files if f not in usedf]
weak = sorted([(v[1], i) for i, v in asg.items()])[:18]

print("khop duoc     : %d/%d" % (len(asg), len(shots)))
print("clip thua     : %d" % len(unused))
print("")
if missing:
    print("SHOT CHUA CO CLIP (%d):" % len(missing))
    for i in missing:
        print("  slot %3d  %-5s %-11s %s" % (i, shots[i][0], shots[i][3], shots[i][2][:58]))
    print("")
if unused:
    print("CLIP THUA, khong gan vao dau (%d):" % len(unused))
    for f in unused:
        print("  ", ftok[f][0])
    print("")
print("18 CAP YEU NHAT — soi mat truoc khi tin:")
for s, i in weak:
    print("  diem %5.1f | slot %3d %-5s %-11s | %s" % (s, i, shots[i][0], shots[i][3], ftok[asg[i][0]][0]))

if "--apply" in sys.argv:
    NAMED.mkdir(parents=True, exist_ok=True)
    n = 0
    for i, (f, s) in asg.items():
        shutil.copyfile(RAW / f, NAMED / dest[i][1])
        n += 1
    print("")
    print("DA CHEP %d clip -> %s (dat ten theo TENFILE)" % (n, NAMED))
    print("Buoc tiep: python tools/place_clips_12.py --apply")
else:
    print("")
    print("(chay lai voi --apply de chep sang clips_named/)")
