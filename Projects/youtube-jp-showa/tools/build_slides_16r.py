# -*- coding: utf-8 -*-
"""build_slides_16r.py — SLIDES cho video 16, ban REAL-FIRST v2 (2026-09-21).

Khac ban `build_slides_16.py` o DUNG MOT DIEU, nhung la dieu quan trong nhat:

  🔴 TRAN DO DAI O KHONG CON LA MOT SO CHUNG — no THEO LOP NUOI O DO.
     Tran 7,0s cua ban cu sinh ra tu GIOI HAN CUA FLOW (clip t2v giao ra ~7s), khong
     phai tu nhip mong muon. O nao duoc nuoi bang ANH THAT thi gioi han do khong ton
     tai => Style A (giu 12-16s/hinh, khuon cua ban 232K) tro nen lam duoc.

       film  (phim tu lieu PD)  -> 12,0s   phim co chuyen dong that, giu lau khong chet khung
       still (anh that hoa dong)-> 16,0s   khung dung yen nhung dong cuc bo, gate MAD>3 lo phan do
       ai    (t2v tai dung)     ->  7,0s   vuot la renderer `-stream_loop` LAP clip

BA THU GIU NGUYEN tu ban cu (moi thu la mot loi da tra gia, dung dong):
  1. CUE CUNG — clip neo dung t0 cua MOT DONG loi that, khong "xin slot gan nhat".
  2. GATE CHAY SAU KHI GHI FILE — gate exit(1) truoc khi ghi tung lam SLIDES dung im
     qua 4 luot sua ma khong ai hieu vi sao cue cung khong an.
  3. clips/clip_<index>.mp4 theo SO THU TU SLOT — dat ten mo ta thi renderer am tham
     fallback anh tinh trong khi preflight van in dau tick.

Usage:
  python tools/build_slides_16r.py [--dry]
Xuat them `clips/_PLAN.json` = lop cua tung o, de buoc cat clip / chon clip AI doc lai.
"""
import sys, json, math
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

STEM = "16_omiai-kekkon"
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD   = ROOT / "06_VIDEO" / STEM
OUT  = ROOT / "03_SCRIPTS" / (STEM + "_SLIDES.json")

CAP      = {"film": 16.0, "still": 16.0, "ai": 7.0}
# 🔴 film 12,0 -> 16,0 (do, khong doan): dong loi cua bai nay co trung vi 6,85s va
# HAI dong lien nhau co trung vi 14,15s. Tran 12 nam DUOI 14,15 nen moi o film chi
# chua noi MOT dong => 64 o film, 9,3 doi hinh/phut, vuot dai ngach 3,2-8,9.
# 12 von la con so tu dat, khong phai gioi han ky thuat (clip phim cat dai bao nhieu
# cung duoc). Nang len 16 = bang still, va dung ly le: phim co chuyen dong that thi
# giu chan it nhat cung bang mot anh tinh da hoa dong.
CAP_HOOK = 5.5    # cold open la PHIM THAT -> 5,5s thay vi 3,4s cua ban t2v:
# 🔴 SUA 2026-09-21 sau khi soi 51 clip: o 4,0s thi cold open co 15 o, nhung phim goc
# giu MOT goc may suot 43 giay => 7-8 o lien tiep la CUNG MOT KHUNG. Cat vun mot
# canh tinh khong tao ra nhip, chi tao ra nhieu o giong nhau. 5,5s -> ~10 o, va
# bo cap phat xoay vong (gen_archival_16.py) dam bao o canh nhau la shot KHAC.
# phim co chuyen dong noi tai nen khong can cat vun moi thay "song". Peer ngach: 60 giay
# dau 7-8 cat; o day 47,7s / 4,0s ~ 12 cat, dung dai do.
MIN_CLIP = 2.2
FLOOR_REAL = 0.60   # san ti le hinh THAT (film+still) tren tong thoi luong — gate CHAN

# ---------------------------------------------------------------- KE HOACH LOP
# (moc bat dau, lop). Lay tu VISUAL_REDESIGN_2026-09-21.md §3, rai trong tung khoi
# sao cho lop THAT bam vao beat ma kho phim PD thuc su co hinh.
PLAN = [
    (0.0,    "film"),   # COLD OPEN — dam cuoi that 平安神宮 (USAF-11070)
    (62.3,   "film"),   # M1 vao bai: 呉服屋 / ngo nha
    (95.0,   "still"),
    (135.0,  "ai"),     # 見合い写真・釣書 — can tay, vat cu the: khong co phim that
    (200.0,  "film"),
    (237.0,  "still"),
    (250.2,  "film"),   # M2 仲人・結納 — 祭壇/神前 that
    (290.0,  "ai"),
    (325.0,  "still"),
    (360.0,  "ai"),
    (390.0,  "film"),
    (411.0,  "film"),   # M3 寿退社 — 🔴 VAN PHONG khong co phim PD, AI ganh gan tron
    (435.0,  "ai"),
    (500.0,  "still"),
    (530.0,  "ai"),
    (578.0,  "film"),
    (593.8,  "still"),  # CTA giua
    (631.0,  "film"),   # M4 適齢期 — 商店街/dam dong
    (680.0,  "ai"),
    (715.0,  "still"),
    (750.0,  "film"),
    (786.0,  "ai"),
    (795.9,  "ai"),     # M5 年金 — 役所 khong co phim that
    (835.0,  "still"),
    (880.0,  "ai"),
    (928.0,  "film"),   # ちゃぶ台 that (USAF-11059 585-711)
    (997.8,  "film"),   # KET
    (1032.8, "still"),
]

DRY = "--dry" in sys.argv
EPS = 1e-6

d = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
lines, total = d["lines"], d["total"]
starts = [ln["start"] for ln in lines]

_h = next((ln["start"] for ln in lines if "こんばんは" in ln["text"]), None)
if _h is None:
    raise SystemExit("[LOI] khong tim thay dong loi chao -> khong biet cold open het o dau")
HOOK_END = round(_h, 2)
print("cold open het o %.2fs (do tu timeline)" % HOOK_END)

# 🔴 SNAP ranh gioi lop ve MOC DONG LOI gan nhat.
# Khong snap thi moi ranh gioi roi vao GIUA mot dong => sinh mot o thua dai 0,0-1,1s
# (do that: 4 o, co o 0,00s) va day so o len 174 = 9,8 doi hinh/phut, vuot dai ngach.
# Snap xong: ranh gioi lop == ranh gioi cau, khong con o rac va it o hon.
def _snap(t):
    return t if t <= 0.01 else min(starts + [total], key=lambda s: abs(s - t))
_pl, _seen = [], set()
for _t, _l in sorted(PLAN):
    _s = _snap(_t)
    if _s in _seen:          # hai moc snap ve cung mot dong -> giu moc DAU
        continue
    _seen.add(_s); _pl.append((_s, _l))
_pl.sort()

def layer_at(t):
    k = _pl[0][1]
    for s, l in _pl:
        if s <= t + EPS: k = l
        else: break
    return k

def cap(t0):
    """Tran TAI THOI DIEM t0: cold open co nhip rieng, con lai theo LOP nuoi o do."""
    if t0 < HOOK_END - 0.01:
        return CAP_HOOK
    return CAP[layer_at(t0)]

# ---------- 1. chon moc cat (tham lam theo TRAN, khong theo trung binh) ----------
cuts, cur = [0.0], 0.0
while cur < total - 0.05:
    c = cap(cur)
    far = None
    for s in starts:
        if s <= cur + EPS: continue
        if s - cur > c + EPS: break
        far = s
    # 🔴 khong cho mot o vat qua RANH GIOI LOP: o "film" ma an sang vung "ai" thi
    # nua sau cua no se duoc nuoi bang clip sai lop.
    nb = next((s for s, _ in _pl if s > cur + EPS), total)
    if far is not None and far <= nb + EPS:
        cuts.append(far); cur = far; continue
    nxt = min(next((s for s in starts if s > cur + EPS), total), nb if nb > cur + MIN_CLIP else total)
    gap = nxt - cur
    n = math.ceil(gap / c)
    while n > 1 and gap / n < MIN_CLIP: n -= 1
    for k in range(1, n):
        cuts.append(round(cur + k * gap / n, 2))
    if nxt >= total - 0.05: cur = total
    else: cuts.append(nxt); cur = nxt
cuts = sorted(set(cuts))

# ---------- 2. cut -> entry ----------
def owner(t):
    k = 0
    for i, s in enumerate(starts):
        if s <= t + EPS: k = i
        else: break
    return k

def uniq_match(li):
    txt = lines[li]["text"]
    for n in range(6, len(txt) + 1):
        m = txt[:n]
        if next(i for i, ln in enumerate(lines) if m in ln["text"]) == li:
            return m
    return None

entries, rows, plan_rows, bad = [], [], [], []
for idx, t in enumerate(cuts):
    li = owner(t); m = uniq_match(li)
    if m is None:
        bad.append((idx, li, lines[li]["text"][:20])); m = lines[li]["text"][:10]
    end = cuts[idx + 1] if idx + 1 < len(cuts) else total
    lay = layer_at(t)
    entries.append({"match": m, "video": True, "source": "clips/clip_%02d.mp4" % idx,
                    "offset": round(t - lines[li]["start"], 2), "dur": round(end - t, 2)})
    plan_rows.append({"idx": idx, "t": round(t, 2), "dur": round(end - t, 2), "layer": lay,
                      "line": li, "text": lines[li]["text"][:40]})
    rows.append("%3d  %7.2fs  %5.2fs  %-5s  L%-3d  %s"
                % (idx, t, end - t, lay, li, lines[li]["text"][:32]))

if not DRY:
    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
(VD / "clips").mkdir(parents=True, exist_ok=True)
(VD / "clips" / "_MAP.txt").write_text(
    "idx     bat dau    dai  lop    dong  loi\n" + "\n".join(rows) + "\n", encoding="utf-8")
(VD / "clips" / "_PLAN.json").write_text(json.dumps(plan_rows, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- 3. GATE (SAU khi ghi) ----------
durs = [cuts[i + 1] - cuts[i] for i in range(len(cuts) - 1)] + [total - cuts[-1]]
lays = [layer_at(t) for t in cuts]
sec = {"film": 0.0, "still": 0.0, "ai": 0.0}
for l, x in zip(lays, durs): sec[l] += x
over = [(i, lays[i], round(x, 2)) for i, x in enumerate(durs) if x > CAP[lays[i]] + 0.01]
tiny = [(i, round(x, 2)) for i, x in enumerate(durs) if x < 2.0]
real = sec["film"] + sec["still"]

print("=== SLIDES %s REAL-FIRST v2 ===%s" % (STEM, " (CHAY THU)" if DRY else ""))
print("tong          : %.1fs = %.2f phut | %d dong loi" % (total, total / 60, len(lines)))
print("so o          : %d  ->  %.1f doi hinh/phut" % (len(entries), len(entries) / (total / 60)))
for l in ("film", "still", "ai"):
    n = sum(1 for x in lays if x == l)
    print("  %-5s       : %3d o | %6.1fs | %4.1f%%" % (l, n, sec[l], 100 * sec[l] / total))
print("HINH THAT     : %.1fs = %.1f%%" % (real, 100 * real / total))
print("dai o         : min %.2fs | tb %.2fs | max %.2fs" % (min(durs), sum(durs) / len(durs), max(durs)))
print("-" * 62)
ok = True
if over:
    print("[CHAN] %d o VUOT tran cua lop: %s" % (len(over), over[:8])); ok = False
else:
    print("[OK  ] khong o nao vuot tran lop (%s)" % " / ".join("%s %g" % kv for kv in CAP.items()))
if bad:
    print("[CHAN] %d match KHONG duy nhat: %s" % (len(bad), bad[:5])); ok = False
else:
    print("[OK  ] match duy nhat (%d dong)" % len(lines))
if lays[0] != "film":
    print("[CHAN] entry 0 phai la lop 'film' (clip phim tu lieu that)"); ok = False
else:
    print("[OK  ] entry 0 = phim that")
if real / total < FLOOR_REAL:
    print("[CHAN] hinh that %.1f%% < san %.0f%%" % (100 * real / total, 100 * FLOOR_REAL)); ok = False
else:
    print("[OK  ] hinh that %.1f%% >= san %.0f%%" % (100 * real / total, 100 * FLOOR_REAL))
if tiny: print("[warn] %d o < 2,0s: %s" % (len(tiny), tiny[:8]))
nhook = sum(1 for c in cuts if c < HOOK_END)
print("[ ok ] cold open: %d o / %.1fs = %.1fs moi canh" % (nhook, HOOK_END, HOOK_END / max(1, nhook)))
print("-" * 62)
print("SLIDES -> %s" % (OUT if not DRY else "(chay thu, KHONG ghi)"))
print("MAP    -> %s" % (VD / "clips" / "_MAP.txt"))
print("PLAN   -> %s" % (VD / "clips" / "_PLAN.json"))
print("KET QUA: %s" % ("SACH" if ok else "CO LOI CHAN"))
sys.exit(0 if ok else 1)
