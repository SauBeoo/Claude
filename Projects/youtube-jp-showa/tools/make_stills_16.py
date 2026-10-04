# -*- coding: utf-8 -*-
"""make_stills_16.py — LOP L2 cua video 16: ANH THAT -> clip hoa dong.

Duong di: frame that cat tu phim PD (grab_stills.py, cung crop/PRE/grade voi clip
film nen hai lop CUNG MOT TONG) -> animate_still.py hoa dong CUC BO (khung dung yen)
-> clip dai bang o + margin.

Vi sao khong dung thang anh tinh: renderer giu mot o toi 16 giay; anh chet cung 16
giay la "khung chet". Ba video 191-232K cua nganh deu la anh tinh, nhung ho cat canh
day hon; minh giu lau hon nen phai bu bang chuyen dong cuc bo (CLAUDE.md §Visual).

Chay:  python tools/make_stills_16.py [--only 20,21] [--no-animate]
"""
import json, subprocess, sys, shutil, tempfile
from pathlib import Path
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
from animate_still import PRESETS  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
FP   = ROOT / "06_VIDEO" / "_footage_pd"
VD   = ROOT / "06_VIDEO" / "16_omiai-kekkon"
ANIM = Path(r"E:\Claude\Projects\_media_library\animate_still.py")
MARGIN = 1.0

S = {"70": FP / "usaf11070_religious_1946.mp4",
     "59": FP / "usaf11059_kyoto_home_1946.mp4",
     "79": FP / "usaf11079_hiroshima_life_1946.mp4",
     "50": FP / "usaf11050_agri_1946.mp4"}

# o  -> (nguon, giay, preset hoa dong, ghi chu)
# ⛔ moi moc da doi chieu: KHONG vung nao trung voi POOLS cua gen_archival_16.py
#    (11070: 255-292/313-409/488-545/600-660 · 11059: 2-60/146-210/216-280/585-711/
#     713-840/903-959/967-1035/1038-1087/1223-1287)
# 🔴 DANH SACH THEO THU TU o 'still', KHONG phai dict theo chi so o tuyet doi.
# Ly do: doi CAP_HOOK trong build_slides lam cold open bot 2 o => MOI chi so o phia
# sau dich -2 va bang nay sai im lang. Thu tu thi khong dich.
STILLS_ORD = [
    ("59", 878, "tatami", "phong tatami, phu nu kimono"),  # v2: 846 ra canh AN COM, trung lop film o139-147
    ("59", 868, "tatami", "phu nu kimono, cui trai futon"),
    ("70", 575, "flat",   "CHAN DUNG nguoi mac kimono le — dung cho 「写真館の白い幕」"),  # v3
    ("70", 432, "street", "五重塔 — chuyen doan"),
    ("70", 60,  "street", "doan nghi le truoc chinh dien"),  # v3: 150 bi nhoe
    ("70", 230, "street", "cau da trong khuon vien den"),
    ("70", 200, "street", "doan nghi le di qua cau da — trang trong"),
    ("79", 478, "kitchen", "phu nu lam banh trong tiem"),
    ("59", 300, "kitchen", "xuong thu cong, nguoi lam"),  # v2: 79@466 ra TOAN CANH THANH PHO
    ("59", 286, "kitchen", "quay hang, nguoi ban"),  # v3: 340 toi va xa
    ("79", 428, "street", "phu nu can hang"),
    ("79", 446, "street", "nguoi ganh hang"),
    ("79", 464, "street", "me be con o quay hang"),
    ("59", 1118, "street", "phu nu tre mac kimono trong vuon"),  # v4: 1100 ra cau be lay nuoc
    ("59", 1140, "street", "phu nu tre, can"),  # v3
    ("50", 350, "flat", "canh dong"),  # v2: 330 mo, khong ro chu the
    ("50", 72,  "flat",  "phu nu cuoc dat tren ruong bac thang"),
    ("50", 96,  "flat",  "phu nu ganh thung"),
    ("50", 404, "flat",  "田植え — nguoi cui cay"),
    ("50", 472, "flat",  "田植え can"),
    ("59", 64,  "flat",   "ngo nha go — tinh"),  # v2: 50@300 mo
    ("70", 100, "flat",   "san den, doan nghi le xa"),
    ("70", 470, "street", "den, mai ngoi"),
    ("50", 492, "flat",   "duong que, nguoi di xa dan"),
]

only = None
for i, a in enumerate(sys.argv):
    if a == "--only" and i + 1 < len(sys.argv):
        only = {int(x) for x in sys.argv[i + 1].split(",")}
NO_ANIM = "--no-animate" in sys.argv

_all = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
plan = {r["idx"]: r for r in _all}
_st = [r["idx"] for r in _all if r["layer"] == "still"]
if len(_st) != len(STILLS_ORD):
    print("🔴 PLAN co %d o 'still' nhung STILLS_ORD khai %d" % (len(_st), len(STILLS_ORD))); sys.exit(1)
STILLS = {idx: STILLS_ORD[k] for k, idx in enumerate(_st)}
want = [i for i in sorted(STILLS) if only is None or i in only]
print("o still: %s" % _st)

# ---------- 1. grab stills (mot spec cho moi nguon, vi grab_stills nhan 1 src) ----------
outdir = VD / "real_photos"; outdir.mkdir(parents=True, exist_ok=True)
for tag, src in S.items():
    ids = [i for i in want if STILLS[i][0] == tag]
    if not ids: continue
    spec = {"src": str(src), "stills": [
        {"id": "st16_%03d" % i, "t": STILLS[i][1], "ybias": 0.5, "grade": 0, "note": STILLS[i][3]}
        for i in ids]}
    sp = ROOT / "tools" / f"stills_spec_16_{tag}.json"
    sp.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "grab_stills.py"), "--spec", str(sp),
                        "--outdir", str(outdir), "--record", "16_omiai-kekkon"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout.strip() or r.stderr.strip()[-400:])
    if r.returncode: print("🔴 grab_stills loi", tag); sys.exit(r.returncode)

if NO_ANIM:
    print("\n--no-animate: dung o buoc grab. Soi %s roi chay lai." % outdir); sys.exit(0)

# ---------- 2. hoa dong tung anh thanh clip dung do dai o ----------
clipdir = VD / "real_still"; clipdir.mkdir(parents=True, exist_ok=True)
bad = []
for i in want:
    tag, t, preset, note = STILLS[i]
    img = outdir / ("st16_%03d.jpg" % i)
    if not img.exists(): print("🔴 thieu", img); sys.exit(2)
    dur = round(plan[i]["dur"] + MARGIN, 2)
    out = clipdir / ("s16_%03d.mp4" % i)
    if out.exists() and out.stat().st_mtime > img.stat().st_mtime:
        print("  = %s da co, bo qua" % out.name); continue
    # 🔴 LOP PHIM PHAI MANH HON PRESET MAC DINH.
    # Do that tren 24 clip dau: MAD trung vi **0,87** — TINH HON ca anh tinh tro cua
    # doi thu (1,2-2,8), trong khi nguong "co dong that" la >3. Preset `flat` con
    # KHONG CO fx nao, chi con lop phim grain 0,7.
    # ⚠️ animate_still IN ra MAD nhung KHONG chan theo no (chi chan dich khung), nen
    # 24/24 "thanh cong" ma van qua tinh — phai tu do lai.
    spec = json.loads(json.dumps(PRESETS[preset]))
    f = spec["film"]
    f["grain"]   = max(f.get("grain", 0.7), 2.2)
    f["flicker"] = max(f.get("flicker", 0.01), 0.026)
    f["dust"]    = round(f.get("dust", 0.3) * 1.6, 2)
    f["scratch"] = round(f.get("scratch", 0.12) * 1.6, 2)
    sp = Path(tempfile.gettempdir()) / ("spec16_%03d.json" % i)
    sp.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ANIM), str(img), "--out", str(out),
                        "--dur", str(dur), "--preset", preset, "--spec", str(sp), "--crf", "23"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    _ls = (r.stdout or "").strip().splitlines()
    _mad = next((l.split(":")[1].split()[0] for l in _ls if "MAD frame" in l), "?")
    print("  %s o%-4d %5.1fs %-8s MAD %s %s" % ("✓" if r.returncode == 0 else "🔴", i, dur,
          preset, _mad, "" if _mad == "?" or float(_mad) > 3 else "⚠️ DUOI 3"))
    if r.returncode: bad.append(i)
print("\n%d/%d clip anh that -> %s" % (len(want) - len(bad), len(want), clipdir))
if bad: print("🔴 loi o:", bad); sys.exit(3)
