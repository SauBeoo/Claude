# -*- coding: utf-8 -*-
r"""add_overlays_16.py — them lop overlay cho project shokutaku-16-banana.

    py -3 tools/add_overlays_16.py [--dry]

Lam 3 viec:
  1. XOA sticker rac do editor/wizard de lai (asset la .jpg ca khung, khong phai
     cutout PNG) — no dang de mot anh chu nhat lo lung tren canh ong thoat nuoc.
  2. TRA LAI BADGE 一つめ/二つめ/三つめ. import_pipeline.py chi bien `rank` thanh
     sceneMarkers (dieu huong, KHONG hien hinh) -> ban remotion dang MAT badge ma
     renderer cua kenh co burn len khung. Day la hoi quy, khong phai trang tri.
  3. Them sticker CUTOUT (chi cai dat): qua chuoi, o 2 moc chot.

Luat da ap:
  - idle.amp = 0 o MOI sticker. Schema mac dinh amp=5 (bob lien tuc, luat
    paper-collage) nhung kenh nay user GHET rung (feedback_video_no_motion_mot_giong:
    "slide tinh mac dinh, ghet Ken Burns").
  - entrance 'rise' cham, KHONG 'wobble'/'punch' — nhip 45+ (audience-45plus.md 2).
  - Thua it: 3 badge + 2 sticker = 5 phan tu cho 23 phut.
  - Badge goc TREN-TRAI (nghiem thu video 15 da chot goc nay).
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJ = ROOT / "projects" / "shokutaku-16-banana" / "project.json"
FPS = 30

# moc lay tu sceneMarkers cua chinh project + dong ket thuc khoi 3 loi
# Track PHAI du khoa: name/muted/hidden/locked — thieu `name` thi Zod bao
# "tracks.N.name: Invalid input" va remotion tu choi ca project.
TRACK_BASE = {"muted": False, "hidden": False, "locked": False}

BADGES = [("一つめ", 22511, 25569), ("二つめ", 25569, 27124), ("三つめ", 27124, 28950)]
# (asset, from_frame, so giay, x, y, w)  — 1080p, goc toa do tam? -> dung x,y goc tren-trai
# STICKER — chi MOT khoanh khac: khoi RECAP 「夕方の十分。上げた足と、バナナ一本と、
# 温かい麦茶。」 (frame 38672-38868, slide nen la HANH LANG -> khong co vat nao de de).
# Ba vat hien LAN LUOT dung luc giong doc ten tung cai = tro nho, khong phai trang tri.
#
# ⛔ DA LOAI 2 cho khac vi DE LEN CHINH VAT DO (kiem bang cach tra slide nao phu frame):
#   frame  7289 「枕元の時計」 -> nen la slide_17 = DA LA anh dong ho
#   frame 26850 「一日一本」   -> nen la slide_60 = DA LA anh 3 qua chuoi
# Day dung loi da mac o vong truoc (sticker chuoi de len canh 3 qua chuoi).
#
# ⛔ DA LOAI stk_tokei khoi ca video: mat so chi ~12:00, ma moi moc gio trong bai
#   deu khac (一時二時ごろ · 四時から六時) -> de vao la anh CHOI voi loi doc.
#
# (asset, from_frame, DUR_FRAMES, x, y, w) — x,y la GOC TREN-TRAI (Sticker.tsx: left/top)
# ⚠️ Cot thu 3 la SO FRAME, KHONG phai giay. Ban dau ham nhan (sec*FPS) nen 228
#    thanh 228 GIAY = sticker bam 4 phut, che ca doan ket. Doi han sang frame.
# user chot 2026-08-16: "cat ra thanh HINH GIAY, chi hien thi TRONG slider do thoi"
#  -> (a) cutout co VIEN TRANG (process_cutout --edge 12) = kieu cat bang keo
#     (b) KHONG con sticker tha noi tren video; tat ca nam TRONG panel o khoi recap
# Da bo 3 cho don le (16:21 · 18:05 · 19:11) du chung da qua duoc 2 lop kiem.
# user chot 2026-08-16: "cat ra thanh HINH GIAY, chi hien thi TRONG slider do thoi"
#  -> (a) cutout co VIEN TRANG (make_stickers_16.py --edge 12) = kieu cat bang keo
#     (b) KHONG con sticker tha noi tren video; TAT CA nam trong panel o khoi recap
#
# Panel mo som hon 3 dong tho, o cau 「夕方の十分。」 (38601) — DONG HO vao truoc lam
# DAU KHOI (nghia: gio nao), roi 3 vat hien lan luot dung luc giong goi ten:
#   38601 時計(5:00) -> 38672 座布団 -> 38715 バナナ -> 38770 麦茶
# Kim dong ho da duoc VE LAI ve 5:00 cho khop 「四時から六時ごろ」 (anh goc ~12:10).
#
# Day thang hang o y=640; nghieng nhe cho ra chat giay dan tay (tinh, khong rung).
STICKERS = [
    ("assets/stk_panel.png",   38601, 300,  200, 340, 1520, "none",  0),
    ("assets/stk_tokei.png",   38601, 300,  250, 370, 200,  "sm",    3),
    ("assets/stk_zabuton.png", 38672, 229,  530, 472, 330,  "sm",   -3),
    ("assets/stk_banana.png",  38715, 186,  920, 515, 350,  "sm",    2),
    ("assets/stk_mugicha.png", 38770, 131, 1340, 434, 225,  "sm",   -2),
]


# ── BIEU CAM CAT GIAY (user chot 2026-08-16) ─────────────────────────────────
# Quet toan bo 284 dong theo 7 nhom tu khoa -> ra 48 cho khop. Rai het la hong,
# nen chi giu DINH cam xuc: 7 cai / 23 phut = ~1 cai moi 3,3 phut.
# Dat goc TREN-PHAI (phu de o duoi, badge o tren-trai), hien 1,6-2,2s roi tat.
# ⛔ Da bo: 0:13 靴下の跡 (slide_01 da la anh co chan, them nhan la lam ron BANG
#    CHUNG chinh cua bai) · 0:31 ひやりとした床 (cach cai 0:26 chi 5 giay)
# ex_zzz ve roi nhung KHONG dung: moi cho hop deu da co nhan khac gan do.
EXPR = [
    ("assets/ex_itami.png",      780,  55, 1520, 150, 220,  6),  # 0:26 「暗い廊下で、転びます」
    ("assets/ex_hatena.png",    1751,  60, 1560, 140, 170, -5),  # 0:58 「あの水はどこから来たのか」
    ("assets/ex_furatsuki.png", 3967,  60, 1540, 155, 210,  4),  # 2:12 「くらっとする」
    ("assets/ex_mukumi.png",   13991,  66, 1500, 165, 250, -4),  # 7:46 「へこんだまま…水がたまって」
    ("assets/ex_hirameki.png", 15329,  60, 1600, 140, 120,  5),  # 8:30 xuong song: khong phai chuyen dem
    ("assets/ex_hirameki.png", 24788,  55, 1600, 140, 120, -6),  # 13:46 「偶然ではありませんでした」
    ("assets/ex_hiyari.png",   25358,  60, 1560, 150, 190,  3),  # 14:05 「廊下の床がやけに冷たかった」
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    d = json.loads(PROJ.read_text(encoding="utf-8"))
    tracks = {t["type"]: t for t in d["tracks"]}
    stk = tracks.get("sticker")
    if stk is None:
        stk = dict(TRACK_BASE, id="trk-sticker", name="Stickers",
                   type="sticker", clips=[])
        d["tracks"].append(stk)

    # 1. don sticker rac: asset khong phai .png = khong phai cutout
    junk = [c for c in stk["clips"] if not str(c.get("asset", "")).lower().endswith(".png")]
    for c in junk:
        print(f"  XOA sticker rac: {c['id']} asset={c.get('asset')} @frame {c.get('from')}")
    stk["clips"] = [c for c in stk["clips"] if c not in junk]

    # 2. badge rank (text track)
    txt = tracks.get("text")
    if txt is None:
        txt = dict(TRACK_BASE, id="trk-text", name="Badges", type="text", clips=[])
        d["tracks"].append(txt)
    txt["clips"] = [c for c in txt["clips"] if not c["id"].startswith("badge-")]
    for i, (label, f0, f1) in enumerate(BADGES):
        txt["clips"].append({
            "id": f"badge-{i}", "from": f0, "durationInFrames": max(1, f1 - f0),
            "kind": "text", "content": label, "preset": "tag",
            "color": d["theme"]["palette"]["accent"], "animation": "fade",
            "animationParams": {}, "fontSize": 52,
            "layout": {"x": 96, "y": 84, "w": 300, "opacity": 0.95},
        })
        print(f"  BADGE {label}: frame {f0}-{f1}  ({(f1-f0)/FPS:.0f}s)")

    # 3. sticker cutout + bieu cam
    stk["clips"] = [c for c in stk["clips"]
                    if not (c["id"].startswith("stk16-") or c["id"].startswith("expr-"))]
    for i, (asset, f0, dur_f, x, y, w, sh, rot) in enumerate(STICKERS):
        if not (ROOT / "public" / "projects" / "shokutaku-16-banana" / asset).exists():
            print(f"  [LOI] thieu {asset}"); return 1
        stk["clips"].append({
            "id": f"stk16-{i}", "from": f0, "durationInFrames": int(dur_f),
            "kind": "sticker", "asset": asset,
            "layout": {"x": x, "y": y, "w": w, "rotation": rot, "opacity": 1},
            "entrance": {"variant": "rise", "delayFrames": 0, "params": {"distance": 40}},
            "exit": None,
            "idle": {"amp": 0, "phase": 0},   # 0 = KHONG bob (user ghet rung)
            "shadow": sh,
        })
        print(f"  STICKER {asset} @ {f0//FPS//60:.0f}:{f0//FPS%60:02.0f}  {dur_f/FPS:.1f}s  w={w}")

    for i, (asset, f0, dur_f, x, y, w, rot) in enumerate(EXPR):
        if not (ROOT / "public" / "projects" / "shokutaku-16-banana" / asset).exists():
            print(f"  [LOI] thieu {asset}"); return 1
        stk["clips"].append({
            "id": f"expr-{i}", "from": f0, "durationInFrames": int(dur_f),
            "kind": "sticker", "asset": asset,
            "layout": {"x": x, "y": y, "w": w, "rotation": rot, "opacity": 1},
            "entrance": {"variant": "grow", "delayFrames": 0, "params": {"from": 0.72}},
            "exit": None, "idle": {"amp": 0, "phase": 0}, "shadow": "sm",
        })
        print(f"  BIEU CAM {asset.split('/')[-1]:22} @ {f0//FPS//60}:{f0//FPS%60:02d}  {dur_f/FPS:.1f}s")

    if a.dry:
        print("\n(--dry: khong ghi)"); return 0
    shutil.copy2(PROJ, PROJ.with_suffix(".json.bak"))
    PROJ.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nOK -> {PROJ.relative_to(ROOT)}  (backup .json.bak)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
