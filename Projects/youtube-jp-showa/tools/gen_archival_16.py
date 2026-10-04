# -*- coding: utf-8 -*-
"""gen_archival_16.py — sinh `archival_spec_16.json` tu `clips/_PLAN.json`.

Vi sao sinh bang may chu khong go tay 51 doan: moi o film co do dai RIENG (2,2-15,8s)
va clip cat ra PHAI DAI HON O cua no — ngan hon la renderer `-stream_loop` LAP clip va
cu nhay ve dau trong nhu video loi (CLAUDE.md §Visual). Go tay 51 cap (ss, dur) khop
voi 51 do dai o la kieu viec chac chan sai it nhat mot cho.

KHO (POOLS): tung vung thoi gian da SOI MAT tren contact sheet, ghi ro noi dung.
Moi o film duoc cap phat TUAN TU trong kho cua cum no — khong doan lai bao gio.
"""
import json, sys, itertools
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
FP   = ROOT / "06_VIDEO" / "_footage_pd"
VD   = ROOT / "06_VIDEO" / "16_omiai-kekkon"
OUT  = ROOT / "tools" / "archival_spec_16.json"

S70 = str(FP / "usaf11070_religious_1946.mp4")
S59 = str(FP / "usaf11059_kyoto_home_1946.mp4")
S79 = str(FP / "usaf11079_hiroshima_life_1946.mp4")
S50 = str(FP / "usaf11050_agri_1946.mp4")

MARGIN = 1.0   # clip dai hon o 1,0s — du bu sai so lam tron cua renderer, chua lap

# 🔴 KEY = KHOANG THOI GIAN (giay), KHONG phai chi so o, cung khong phai cum lien tiep.
# Ly do: doi mot hang so trong build_slides (CAP_HOOK 4,0 -> 5,5) lam cold open tu 15 o
# xuong 13 o => MOI chi so o phia sau dich -2 va ca bang POOLS tro nen sai im lang.
# Cum lien tiep cung khong dung: cold open + loi chao + M1-vao-bai la MOT cum lien tiep
# nhung phai lay 3 kho khac nhau. Chi co MOC GIAY la khong doi khi so o thay doi —
# no chinh la thu PLAN cua build_slides_16r duoc viet bang.
# ⛔ moi vung deu da soi mat tren sheet; khong lay vung co bang slate / linh / do nat.
POOLS = [
    ((0.0, 47.71), [(S70, 370, 398, "CAN co dau 打掛 + chu re — canh dat nhat cua phim"),
     (S70, 313, 356, "co dau 色打掛 + phu dau, thung ruou o san den"),
     (S70, 356, 370, "doan ruoc di tren soi, canh rong"),
     (S70, 398, 409, "doan ruoc qua cong den")]),   # COLD OPEN
    ((47.71, 62.3), [(S70, 488, 545, "kien truc 平安神宮 do — canh tinh, dat loi chao")]),  # loi chao
    ((62.3, 95.0), [(S59, 2, 60,   "ngo nha go, tre con, thung nuoc, san truoc")]),  # M1 vao bai
    ((200.0, 237.0), [(S59, 903, 959, "鏡台 + 縫い物 — co gai ngoi truoc guong, tay dang khau")]),  # M1 「畳に並べた夜」
    ((250.2, 290.0), [(S70, 255, 292, "祭壇/神棚 co do cung — dat 結納"),
     (S70, 600, 660, "nguoi di le o hang rao den")]),  # M2 仲人・結納
    ((390.0, 435.0), [(S59, 967, 1035, "台所 — phu nu 割烹着 nau an, noi lon tren bep")]),  # M2 cuoi + M3 dau
    ((578.0, 593.8), [(S59, 1038, 1087, "rua bat o bon, bep")]),  # M3 「今は、仕事は続く」
    # 🔴 DOI NGUON 2026-09-21 sau khi soi 1:1 ban render dau:
    # vung 146-280 cua 11059 la pho Kyoto 1946 va DINH HAI DAU HIEU CHIEM DONG —
    #   · bien hieu tieng Anh 「GRAND KYOTO INTERNATIONAL…」 (bien phuc vu quan doi My)
    #   · nguoi mac QUAN PHUC kaki dung giua cho
    # Ca hai deu lo boi canh 1946 trong mot bai ke 昭和30〜50年 => loai ca vung.
    # Thay bang vung 1223-1287 (song Kamo, phu nu kimono, bien hieu chu Nhat) — da soi
    # 15 frame o 640px, sach.
    # ⛔⛔ VONG SUA 2: vung 1223-1287 CHI SACH TOI ~1268. Doan 1269+ co MOT DOAN NGUOI
    # MAC QUAN PHUC VAC GAY di qua tiem 東榮堂 — lot ca vong soi truoc vi cac clip cu chi
    # phu toi 1269. => cat tran o 1268 va them 2 vung da soi 640px (t=1088-1180).
    ((631.0, 680.0), [(S59, 1223, 1268, "ben song Kamo, hang lieu, phu nu kimono, bien 鴨川"),
     (S59, 1133, 1180, "舞妓 mac kimono trong vuon chua · ao ca koi"),
     (S59, 1093, 1128, "cau be rua chao lon o voi nuoc — doi song")]),  # M4 商店街
    # nhan lai vung cua cum tren (da soi sheet 29 frame): ngo nha go, xe keo, nguoi quet,
    # rua o be nuoc. ⛔ BO khoang 78-88 = DONG RAC/DO NAT va 133+ = quay hang co nguoi
    # doi mu kieu quan doi.
    ((750.0, 786.0), [(S59, 60, 77,  "ngo nha go, hien nha, cua so shoji"),
     (S59, 90, 132, "pho co xe keo cho thung, nguoi rua o be nuoc, nguoi quet san")]),  # M4 cuoi
    ((928.0, 1032.8), [(S59, 585, 711, "⭐ gia dinh ngoi an quanh ちゃぶ台, rot tra, nang chen"),
     (S59, 713, 840, "⭐ vo gap thuc an cho chong, ca nha an com")]),  # M5 cuoi + KET
]

plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
film = [r for r in plan if r["layer"] == "film"]

# 🔴 Moc trong POOLS la moc DANH NGHIA (lay tu PLAN cua build_slides_16r). PLAN do
# SNAP moi ranh gioi lop ve dau cau gan nhat, nen moc THAT lech vai phan muoi den vai
# giay (250,2 -> 250,17 · 750,0 -> 749,56 · 928,0 -> 927,09). Khop bang khoang cung thi
# truot. Cach dung: gan moi moc danh nghia vao o film GAN NO NHAT, roi chia theo do.
_marks = sorted((a, gi) for gi, ((a, b), _) in enumerate(POOLS))
_assign = {}
for _a, _gi in _marks:
    _near = min(film, key=lambda r: abs(r["t"] - _a))
    _assign[_near["idx"]] = _gi
_cur = None
_grp = {}
for r in film:
    if r["idx"] in _assign: _cur = _assign[r["idx"]]
    _grp[r["idx"]] = _cur
if any(v is None for v in _grp.values()):
    print("🔴 co o film truoc moc dau tien cua POOLS"); raise SystemExit(1)
_n = len(set(_grp.values()))
if _n != len(POOLS):
    print("🔴 chi %d/%d kho duoc dung — hai moc cung gan ve mot o?" % (_n, len(POOLS)))
    raise SystemExit(1)

def pool_of_t_idx(idx):
    gi = _grp[idx]; return gi, POOLS[gi][1]

cuts, cursor, short = [], {}, []
for r in film:
    key, pool = pool_of_t_idx(r["idx"])
    need = r["dur"] + MARGIN
    # 🔴 XOAY VONG giua cac vung, khong lay tuan tu het vung 1 roi moi sang vung 2:
    # phim tu lieu giu mot goc may rat lau (43s lien), lay tuan tu => cac o canh nhau
    # ra CUNG MOT KHUNG. Xoay vong thi o n va o n+1 chac chan khac shot.
    turn = cursor.get(("turn", key), 0)
    cursor[("turn", key)] = turn + 1
    order = [(turn + k) % len(pool) for k in range(len(pool))]
    placed = False
    for pi in order:
        src, t0, t1, note = pool[pi]
        used = cursor.get((key, pi), t0)
        if t1 - used >= need:
            cuts.append({"id": "a16_%03d" % r["idx"], "src": src, "ss": round(used, 2),
                         "dur": round(need, 2), "ybias": 0.5, "grade": 0,
                         "note": f"o{r['idx']} ({r['dur']}s) · {note}"})
            cursor[(key, pi)] = used + need
            placed = True; break
    if not placed:
        short.append((r["idx"], round(need, 1), key))
if short:
    print("🔴 KHO KHONG DU cho %d o: %s" % (len(short), short))
    print("   -> noi them vung vao POOLS (phai soi mat truoc), hoac doi PLAN cua build_slides_16r.")
    raise SystemExit(1)

spec = {"_note": "Video 16 REAL-FIRST v2 (2026-09-21). 4 phim USAF 1946, Public Domain Mark 1.0, "
                 "chua tung dung o video nao (so den _footage_test/FOOTAGE_USED.json). "
                 "grade=0 vi toan bo hieu chinh nam trong PRE+HOUSE cua cut_archival.py.",
        "_caveat": "Phim 1946 cho bai ke 昭和30〜50年 — lech nien dai, chap nhan CO CHU DICH nhu "
                   "video 01-08 (archival_spec_08._caveat). Le phuc 紋付・打掛 gan nhu khong doi "
                   "giua 1946 va 1970. Giong doc KHONG BAO GIO noi 'day la canh nam 19xx'. "
                   "Da loai moi vung co bang slate / linh chiem dong / do nat.",
        "cuts": cuts}
OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")

tot = sum(c["dur"] for c in cuts)
print("✓ %d doan phim that -> %s" % (len(cuts), OUT))
print("  tong cat: %.1fs  (o film can %.1fs)" % (tot, sum(r["dur"] for r in film)))
for src, g in itertools.groupby(sorted(cuts, key=lambda c: c["src"]), key=lambda c: c["src"]):
    g = list(g); print("   %-34s %2d doan  %6.1fs" % (Path(src).name, len(g), sum(x["dur"] for x in g)))
