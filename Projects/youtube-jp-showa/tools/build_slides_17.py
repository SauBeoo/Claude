# -*- coding: utf-8 -*-
"""build_slides_17.py — SLIDES cho video 17, ban FULL AI (user chot 2026-09-21: "tao muon tao video full AI").

KHAC ban 16r (REAL-FIRST v2) o cho: KHONG CO LOP PHIM THAT.
  16r: film 16,0s / still 16,0s / ai 7,0s + san hinh that >=60% + entry 0 bat buoc la phim that
  17 : ai 8,0s cho TOAN BAI, khong san hinh that, entry 0 cung la AI

🔴 VI SAO BO LOP PHIM O BAI NAY — do duoc, khong phai tuy hung:
   Bai 17 la bai VAN PHONG (bang thong bao, quay ke toan, ket sat tong vu, le ve huu).
   Kho phim PD cua kenh: USAF-11050/11059/11070/11079 = nha + nong thon + den chua 1946,
   `japan_today_1959.mp4` = phim DU LICH (vuon, ho Chuzenji, den Nikko, ca koi) — soi 96 frame,
   KHONG mot canh van phong. Ep canh nha 1946 vao muc noi ve van phong la sai NOI DUNG,
   te hon lech nien dai. => user chot full AI.
   ⚖️ Gia phai tra, biet truoc: TICK "altered/synthetic" la BAT BUOC tuyet doi, va moat
   "phim tu lieu that" cua video 16 mat o bai nay.

BA THU GIU NGUYEN tu 16r (moi thu la mot loi da tra gia):
  1. CUE CUNG — clip neo dung t0 cua MOT DONG loi that, khong "xin slot gan nhat".
  2. GATE CHAY SAU KHI GHI FILE — gate exit(1) truoc khi ghi tung lam SLIDES dung im 4 luot.
  3. clips/clip_<index>.mp4 theo SO THU TU SLOT — dat ten mo ta thi renderer am tham fallback
     anh tinh trong khi preflight van in dau tick.

🔴 TRAN 8,0s KHONG PHAI NHIP MONG MUON — no la gioi han cua Flow (clip t2v giao ra toi da 8s).
   Clip NGAN HON KHE thi renderer `-stream_loop` LAP clip (render-background.md §Visual 🔴🔴),
   nen moi khe PHAI <= 8,0s. Spreader chia theo TRAN, khong chia theo trung binh:
   chia theo trung binh khong bao gio dam bao duoc tran (da do o video 11: 15 cho vuot ->
   them 15 clip -> lai vuot o 4 cho KHAC).

Usage:  python tools/build_slides_17.py [--dry]
"""
import sys, json, math
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

STEM = "17_kaisha-ga-kureta"
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD   = ROOT / "06_VIDEO" / STEM
OUT  = ROOT / "03_SCRIPTS" / (STEM + "_SLIDES.json")

# 🔴 TRAN O KHONG CON LA 8,0s — user chot 2026-09-22 "kich ban cham rai thoi".
#   8,0s la GIOI HAN CUA FLOW (clip t2v giao ra toi da 8s), khong phai nhip mong muon.
#   Giu 8,0 thi moi o chi chua noi MOT dong loi (dong trung vi 5,33s, hai dong 10,7s)
#   => 163 o = 11,3 doi hinh/phut, VUOT dai ngach do duoc 3,2-8,9 (CLAUDE.md §Visual).
#   Nang tran len 12,0 => o dai hon clip => renderer `-stream_loop` LAP clip
#   (render-background.md §Visual 🔴🔴). Cach chua DUY NHAT: GIAN clip bang setpts
#   (tien le video 09: `stretch2.py`). Tran 12,0 => he so gian toi da 12,0/8,0 = 1,50x,
#   nam trong vung "1,2-1,7x khong nhan ra" da ghi o CLAUDE.md §Visual.
MAX_CLIP = 12.0
CAP_HOOK = 7.0     # cold open van nhanh hon than bai, nhung cung cham lai theo
MIN_CLIP = 2.2     # duoi nguong nay thi o chi kip nhay mot cai, khong doc duoc gi

DRY = "--dry" in sys.argv
EPS = 1e-6

d = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
lines, total = d["lines"], d["total"]
starts = [ln["start"] for ln in lines]

_h = next((ln["start"] for ln in lines if "こんばんは" in ln["text"]), None)
if _h is None:
    raise SystemExit("[LOI] khong tim thay dong loi chao -> khong biet cold open het o dau")
HOOK_END = round(_h, 2)

# ---------------------------------------------------------------- KHOI NOI DUNG
# Neo theo TEXT, khong theo giay cung: doi mot cau trong _TTS.md thi moc tu dich theo.
# (CLAUDE.md §Visual: "moi bang cau hinh neo theo CHI SO O se sai im lang")
BLOCKS = [
    ("HOOK",   None,            "cold open — bang thong bao, dam dong hanh lang"),
    ("M1",     "一つ目",         "M1 春闘 — bang thong bao, dam dong, van phong"),
    ("M2",     "二つ目",         "M2 家族手当 — tong vu, bang luong, gia dinh o nha"),
    ("M3",     "三つ目",         "M3 社宅・寮 — khu tap the, hanh lang ky tuc"),
    ("CTA",    "ここで、ひとつだけ", "CTA giua video"),
    ("M4",     "四つ目",         "M4 社内預金 — ket sat tong vu, giay"),
    ("M5",     "五つ目",         "M5 退職金 — le ve huu, bo hoa, ve nha"),
    ("END",    "五つ、並べてみました", "tong luan"),
]

def find_start(key):
    if key is None:
        return 0.0
    for ln in lines:
        if key in ln["text"]:
            return ln["start"]
    raise SystemExit("[LOI] khong tim thay khoi '%s' trong timeline" % key)

blocks = []
for name, key, note in BLOCKS:
    blocks.append({"name": name, "t": round(find_start(key), 2), "note": note})
for i, b in enumerate(blocks):
    b["end"] = blocks[i + 1]["t"] if i + 1 < len(blocks) else total

def block_at(t):
    cur = blocks[0]
    for b in blocks:
        if b["t"] <= t + EPS: cur = b
        else: break
    return cur

def cap(t0):
    return CAP_HOOK if t0 < HOOK_END - 0.01 else MAX_CLIP

# ---------- 1. chon moc cat (tham lam theo TRAN) ----------
cuts, cur = [0.0], 0.0
while cur < total - 0.05:
    c = cap(cur)
    far = None
    for s in starts:
        if s <= cur + EPS: continue
        if s - cur > c + EPS: break
        far = s
    # khong cho mot o vat qua RANH GIOI KHOI (o nua M1 nua M2 thi khong biet gen canh gi)
    nb = next((b["t"] for b in blocks if b["t"] > cur + EPS), total)
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
    blk = block_at(t)
    entries.append({"match": m, "video": True, "source": "clips/clip_%02d.mp4" % idx,
                    "offset": round(t - lines[li]["start"], 2), "dur": round(end - t, 2)})
    plan_rows.append({"idx": idx, "t": round(t, 2), "dur": round(end - t, 2),
                      "block": blk["name"], "line": li, "text": lines[li]["text"][:44]})
    rows.append("%3d  %7.2fs  %5.2fs  %-5s  L%-3d  %s"
                % (idx, t, end - t, blk["name"], li, lines[li]["text"][:32]))

if not DRY:
    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
(VD / "clips").mkdir(parents=True, exist_ok=True)
(VD / "clips" / "_MAP.txt").write_text(
    "idx     bat dau    dai  khoi   dong  loi\n" + "\n".join(rows) + "\n", encoding="utf-8")
(VD / "clips" / "_PLAN.json").write_text(
    json.dumps({"blocks": blocks, "slots": plan_rows}, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- 3. GATE (SAU khi ghi) ----------
durs = [cuts[i + 1] - cuts[i] for i in range(len(cuts) - 1)] + [total - cuts[-1]]
over = [(i, round(x, 2)) for i, x in enumerate(durs) if x > MAX_CLIP + 0.01]
tiny = [(i, round(x, 2)) for i, x in enumerate(durs) if x < 2.0]

print("=== SLIDES %s — FULL AI ===%s" % (STEM, " (CHAY THU)" if DRY else ""))
print("tong          : %.1fs = %.2f phut | %d dong loi" % (total, total / 60, len(lines)))
print("so o          : %d  ->  %.1f doi hinh/phut" % (len(entries), len(entries) / (total / 60)))
print("dai o         : min %.2fs | tb %.2fs | max %.2fs" % (min(durs), sum(durs) / len(durs), max(durs)))
print("cold open     : het o %.2fs" % HOOK_END)
for b in blocks:
    n = sum(1 for p in plan_rows if p["block"] == b["name"])
    print("  %-5s %7.2fs  %3d o   %s" % (b["name"], b["t"], n, b["note"]))
print("-" * 64)
ok = True
if over:
    print("[CHAN] %d o VUOT tran %.1fs cua may gen: %s" % (len(over), MAX_CLIP, over[:8])); ok = False
else:
    print("[OK  ] khong o nao vuot tran %.1fs (o >8,0s phai GIAN clip bang setpts)" % MAX_CLIP)
if bad:
    print("[CHAN] %d match KHONG duy nhat: %s" % (len(bad), bad[:5])); ok = False
else:
    print("[OK  ] match duy nhat (%d dong)" % len(lines))
if tiny: print("[warn] %d o < 2,0s: %s" % (len(tiny), tiny[:8]))
nhook = sum(1 for c in cuts if c < HOOK_END)
print("[ ok ] cold open: %d o / %.1fs = %.1fs moi canh" % (nhook, HOOK_END, HOOK_END / max(1, nhook)))
print("-" * 64)
print("SLIDES -> %s" % (OUT if not DRY else "(chay thu, KHONG ghi)"))
print("MAP    -> %s" % (VD / "clips" / "_MAP.txt"))
print("PLAN   -> %s" % (VD / "clips" / "_PLAN.json"))
print("KET QUA: %s" % ("SACH" if ok else "CO LOI CHAN"))
print("\nTiep: python tools/check_cast_unique.py 17   ->  tools/gen_prompts_17.py")
sys.exit(0 if ok else 1)
