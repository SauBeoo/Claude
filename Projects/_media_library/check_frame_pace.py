#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check_frame_pace.py — GATE NHỊP HÌNH cho project Remotion (dùng chung mọi kênh).

Đo HAI đại lượng KHÁC NHAU mà trước đây bị gộp làm một:

  ① TRẦN đổi HERO  (chống MỆT)  — <= 6 lần đổi ảnh chính / phút
     Nguồn: .claude/rules/audience-45plus.md §2 muc 1. Jump-cut don dap
     lam tep 45+ met va thoat.

  ② SÀN sự kiện HÌNH (chống CHÁN) — moi khe <= 7s phai co 1 su kien
     User chot 2026-08-30: "tam 7s phai chuyen frame anh 1 lan... frame
     dung yen lau qua". Su kien = doi hero / sticker vao / sticker ra /
     punch / bang so / cong thuc / pop / zoom-punch.

  ③ CẤM "nền trống" — scene nao cung phai co MOT thu o vung giua:
     hero photocard, hoac bang so, hoac cong thuc.

  ④ TRAN LAP STICKER — moi file sticker <= 3 lan / video
     User chot 2026-08-31: "khong muon 1 anh trung sticker nhieu lan hoac
     sticker lap lai qua nhieu lan trong 1 video".

Hai gate ①② KHONG mau thuan: doi HERO la cat canh cung (bi chan tren),
sticker truot vao la chuyen dong nho (bi chan duoi). Gop hai cai lam mot
con so "doi hinh/phut" la do sai thu minh muon do.

Dung:
    python check_frame_pace.py <project.json> [--max-gap 7] [--max-hero-per-min 6]
Exit 1 neu co gate do.
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from pathlib import Path

# 🔴 Console Windows mặc định cp1252 KHÔNG in nổi ①②③ ⇒ gate CRASH giữa chừng,
#    exit code ≠ 0, và builder gọi nó sẽ báo "🔴 GATE NHỊP HÌNH ĐỎ" — tức **báo đỏ
#    GIẢ trên một project sạch**. Nguy hiểm hơn cả gate im lặng: nó dụ người ta đi
#    sửa NỘI DUNG cho một lỗi nằm ở CÔNG CỤ. (Bắt 2026-08-31, nenkin video 19.)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Track nao tinh la "su kien hinh" khi mot clip BAT DAU
EVENT_TRACK_PREFIX = (
    "trk-hero",     # anh chinh (photocard)
    "trk-peak",     # zoom-punch footage
    "trk-video",    # ⭐ clip VIDEO lam hinh chinh (duong vox: clip AI full-bleed)
    "trk-sup",      # sticker phu (sup1/sup2/sup3...)
    "trk-stat",     # bang so lieu
    "trk-formula",  # cong thuc
    "trk-punch",    # dai punch
    "trk-tag",      # tag chu goc tren
    "trk-genten",   # ⭐ anh 原典 (screenshot trang chinh thuc) — them 2026-09-04
)
# Track "chiem vung giua" — scene thieu ca ba la NEN TRONG
CENTER_TRACK = ("trk-hero", "trk-peak", "trk-video", "trk-stat", "trk-formula",
                "trk-genten")
# Track doi ANH CHINH — dung cho tran ①
HERO_TRACK = ("trk-hero", "trk-peak", "trk-video")
# 🔴 `trk-genten` CO trong `CENTER_TRACK` NHUNG KHONG trong `HERO_TRACK`
#    (them 2026-09-04, nenkin 21). Ly le, khong phai "cho qua cho de":
#    · gate ① do cai gay MET = **cat canh cung**. Anh 原典 la screenshot TINH co
#      `motion: pan` cham — khong cat canh, nen tinh no vao tran 6/phut la do sai
#      thu no muon do (cung ho `audience-45plus.md` §6.10 va §2.0b).
#    · nhung no CO noi dung o vung giua, nen van phai tinh cho gate ③, neu khong
#      moi scene 原典 bi ket an oan la "nen trong".
#    📊 So do nenkin 21: 84 clip footage = **5,89/phut** (dat tran 6); cong 9 anh
#      原典 thanh 93 = **6,52/phut** (do). Chenh do HOAN TOAN la 9 anh tinh.
# 🔴 THEM `trk-video` 2026-09-03 — bai hoc `audience-45plus.md` §2.0f-bis:
#    doi DON VI HINH thi phai ra moi lop neo vao don vi cu. Duong dung "vox"
#    (`build_remotion_19vox.py`) dat hinh chinh o track **video** (clip AI
#    full-bleed) chu khong phai sticker photocard. Gate ban cu hard-code
#    "trk-hero"/"trk-peak" nen bao **33 scene NEN TRONG** tren mot project ma
#    33 scene do dang chieu clip video chay lien tuc => bao do GIA, va no du
#    nguoi ta di sua NOI DUNG cho mot loi nam o CONG CU (§2.0h).
#    ⚠️ Clip video la chuyen dong LIEN TUC nen ban chat khac anh tinh: moi clip
#    bat dau van tinh la 1 su kien (dung cho gate ②), nhung "khe giua 2 su kien"
#    trong long mot clip KHONG phai frame dung yen. Doc ket qua gate ② tren
#    project dung track nay voi hieu biet do.


def hhmmss(sec: float) -> str:
    return f"{int(sec // 60)}:{sec % 60:04.1f}"


def load(path: Path):
    p = json.loads(path.read_text(encoding="utf-8"))
    fps = p.get("fps") or p.get("meta", {}).get("fps") or 30
    dur = p["timeline"]["durationInFrames"]
    return p, int(fps), int(dur)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    # user chot 2026-08-31 (lan 2): 8-9s/anh de bot so anh phai gen.
    # 9,0s van du dieu kien "khong dung yen lau" va tra lai duoc tran 6/phut cu.
    ap.add_argument("--max-gap", type=float, default=9.0,
                    help="tran khe dung yen, giay (9,0 cho Remotion doi-anh; 7,0 ban dau)")
    # TRA VE 6,0: user chot lai 8-9s/anh (thay vi 7s) => 5,3-5,8 doi/phut, dat tran cu.
    #    Khong con xung dot voi audience-45plus §2 muc 1.
    ap.add_argument("--max-hero-per-min", type=float, default=6.0,
                    help="tran doi anh chinh moi phut (7,2 cho Remotion; 6,0 cho make_stage)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    path = Path(a.project)
    if not path.exists():
        print(f"KHONG THAY {path}")
        return 2
    p, fps, dur = load(path)
    total_s = dur / fps

    markers = sorted(m["atFrame"] for m in p.get("sceneMarkers", []))
    bounds = markers + [dur]

    tracks = {t["id"]: t.get("clips", []) for t in p.get("tracks", [])}

    def frames_of(prefixes) -> list[int]:
        out: list[int] = []
        for tid, clips in tracks.items():
            if tid.startswith(prefixes):
                out += [c["from"] for c in clips]
        return out

    # ---- su kien hinh: clip BAT DAU + clip KET THUC co exit ----
    ev: set[int] = set(markers)
    for tid, clips in tracks.items():
        if not tid.startswith(EVENT_TRACK_PREFIX):
            continue
        for c in clips:
            ev.add(c["from"])
            if c.get("exit"):          # sticker rut di cung la mot su kien
                ev.add(c["from"] + c["durationInFrames"])
    frames = sorted(f for f in ev if 0 <= f <= dur)

    fails: list[str] = []

    # ---------- ② SAN: khe dung yen ----------
    gaps: list[tuple[float, float]] = []       # (giay bat dau, do dai khe)
    seq = frames + [dur]
    for x, y in zip(seq, seq[1:]):
        gaps.append((x / fps, (y - x) / fps))
    # ⭐ MIỄN scene SỐ LIỆU (user chốt 2026-08-31: "7s đổi ảnh 1 lần nếu nó KHÔNG
    #    PHẢI là số liệu"). Bảng/công thức tự build-on từng dòng — chuyển động đó nằm
    #    TRONG một clip nên phép đếm "clip bắt đầu" không nhìn thấy được. Đếm nó là
    #    đứng yên thì gate đang đo sai thứ nó muốn đo.
    # miễn theo SCENE (không theo khoảng của clip bảng): bảng bắt đầu sau đầu scene
    # ~10% nên so với clip thì khe đầu scene lọt ra ngoài và bị chấm oan.
    data_iv = []
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        for tid in ("trk-stat", "trk-formula"):
            if any(lo <= c["from"] < hi for c in tracks.get(tid, [])):
                data_iv.append((lo, hi))
                break

    # ⭐ MIỄN khe nằm TRỌN trong một clip FOOTAGE ĐỘNG (thêm 2026-09-10, nenkin 22 i2v).
    #    Lý lẽ đã nằm ngay trong chú thích của chính tool này (khối `trk-video`, 2026-09-03):
    #    *"khe giữa 2 sự kiện trong lòng một clip KHÔNG phải frame đứng yên"* — nhưng bản đó
    #    chỉ GHI cảnh báo cho người đọc rồi vẫn `exit 1`. Một gate phải-bỏ-qua-bằng-phán-đoán
    #    thì hoặc bị bỏ qua mãi (thành vô dụng) hoặc dụ người ta đi sửa NỘI DUNG cho một lỗi
    #    của CÔNG CỤ (đúng bệnh `audience-45plus.md` §2.0h).
    # 🔴 Miễn theo ĐUÔI FILE, KHÔNG miễn cả track: schema remotion-vox cho `kind:"video"`
    #    nhận **mp4 HOẶC ảnh tĩnh**, nên miễn trọn `trk-video` sẽ tha luôn ảnh tĩnh đặt ở
    #    đó — đúng cái gate này sinh ra để bắt. Ảnh 原典 (`trk-genten`) vẫn bị tính vì nó
    #    là screenshot TĨNH: 21s một tấm đứng là đứng yên thật.
    MOVING = (".mp4", ".mov", ".webm", ".mkv")
    move_iv = []
    for tid, clips in tracks.items():
        if not tid.startswith(HERO_TRACK):
            continue
        for c in clips:
            if str(c.get("asset", "")).lower().endswith(MOVING):
                move_iv.append((c["from"], c["from"] + c["durationInFrames"]))

    def in_data(f0, f1):
        if any(lo <= f0 and f1 <= hi + 2 for lo, hi in data_iv):
            return True
        return any(lo <= f0 and f1 <= hi + 2 for lo, hi in move_iv)

    # 🔴 PHAI `round()` — bug float bat duoc 2026-09-04 (nenkin 21): khe duoc
    #    doi sang GIAY (`t = x/fps`) roi doi NGUOC lai frame de kiem mien, va
    #    `8054/30*30 = 8053.9999...` < 8054 => dieu kien `lo <= f0` FALSE =>
    #    scene 計算の式 bi cham "dung yen 14,7s" du no la scene CONG THUC va da
    #    nam trong `data_iv`. Gate bao do tren mot project dung luat.
    bad = [(t, g) for t, g in gaps
           if g > a.max_gap + 1e-6
           and not in_data(round(t * fps), round((t + g) * fps))]
    frozen_s = sum(g for _, g in bad)

    # ---------- ① TRAN: doi hero ----------
    hero_f = sorted(frames_of(HERO_TRACK))
    hero_per_min = len(hero_f) / (total_s / 60) if total_s else 0.0

    # ---------- ③ NEN TRONG ----------
    center_f = sorted(frames_of(CENTER_TRACK))
    # ⭐ Scene được coi là CÓ nội dung nếu ① một clip BẮT ĐẦU trong nó (bản gốc) HOẶC
    #    ② một clip đang CHẠY QUA điểm giữa scene (thêm 2026-09-10).
    # 🔴 Vì sao thêm ②: khi một clip cố ý trải qua nhiều scene (`plan22` cho scene 1 và 12
    #    của nenkin 22 dùng CHUNG clip với scene trước để giữ trần 6/phút), phép đếm
    #    "clip bắt đầu trong scene" báo hai scene đó là NỀN TRỐNG — trong khi màn hình
    #    đang chiếu footage liên tục. Cùng đúng một bệnh mà khối chú thích `trk-video`
    #    ở đầu file đã chữa một nửa: gate neo vào "clip bắt đầu" thì vỡ mỗi lần đơn vị
    #    hình trải rộng hơn một scene (`audience-45plus.md` §2.0f-bis).
    # ⚖️ Chỉ NỚI, không siết: điều kiện ② thêm vào bằng OR nên không thể sinh báo đỏ mới
    #    trên project nào đang sạch.
    center_iv = []
    for tid, clips in tracks.items():
        if tid.startswith(CENTER_TRACK):
            center_iv += [(c["from"], c["from"] + c["durationInFrames"]) for c in clips]
    empty: list[tuple[int, float, float]] = []
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        j = bisect.bisect_left(center_f, lo)
        starts_in = j < len(center_f) and center_f[j] < hi
        mid = (lo + hi) // 2
        runs_through = any(c0 <= mid < c1 for c0, c1 in center_iv)
        if not (starts_in or runs_through):
            empty.append((i, lo / fps, (hi - lo) / fps))

    # ---------- BAO CAO ----------
    if not a.quiet:
        print(f"=== NHIP HINH — {path.name} ===")
        print(f"video {total_s:.1f}s · {len(bounds)-1} scene · {len(frames)} su kien hinh")
        print()
        print(f"① TRAN doi anh chinh : {hero_per_min:5.2f} /phut  (tran {a.max_hero_per_min:.0f})")
        print(f"② SAN nhip su kien   : khe dai nhat {max(g for _, g in gaps):5.1f}s  (tran {a.max_gap:.0f}s)")
        print(f"   khe vuot tran     : {len(bad)}/{len(gaps)} khe · "
              f"{frozen_s:.0f}s = {frozen_s / total_s * 100:.1f}% thoi luong")
        print(f"③ Scene nen trong    : {len(empty)}/{len(bounds)-1}")
        print()

    if hero_per_min > a.max_hero_per_min + 1e-6:
        fails.append(
            f"① doi anh chinh {hero_per_min:.2f}/phut > tran {a.max_hero_per_min:.0f} "
            f"— cat canh don dap, tep 45+ met (audience-45plus §2 muc 1)")

    if bad:
        fails.append(
            f"② {len(bad)} khe frame dung yen > {a.max_gap:.0f}s "
            f"({frozen_s / total_s * 100:.1f}% thoi luong video)")
        if not a.quiet:
            for t, g in bad[:25]:
                print(f"   dung yen {g:5.1f}s  tai {hhmmss(t)}")
            if len(bad) > 25:
                print(f"   ... con {len(bad)-25} khe nua")
            print()

    if empty:
        fails.append(f"③ {len(empty)} scene KHONG co gi o vung giua (nen trong)")
        if not a.quiet:
            for i, t, d in empty:
                print(f"   scene {i:2d}  {hhmmss(t)}  dai {d:.1f}s  — thieu hero/bang/cong thuc")
            print()

    if fails:
        print("GATE NHIP HINH: DO")
        for f in fails:
            print("  X " + f)
        print()
        print("Cach chua (theo thu tu re -> dat):")
        print("  1. Them SUP STICKER vao scene trong — nhung phai them FILE moi,")
        print("     KHONG lap lai file cu (user chot: sticker dung trung nhau nhieu).")
        print("  2. Bat `exit` cho sticker — no rut di cung la 1 su kien, mien phi.")
        print("  3. Them PUNCH banner / pop so o giua scene dai.")
        print("  4. CHE scene >30s thanh 2 scene — nhung phai co hero KHAC,")
        print("     dung lai hero cu la lap anh.")
        print("  ⛔ KHONG chua bang cach tang doi HERO — se dam vao tran ①.")
        print("  ⛔ KHONG xoay vong LAP cung file sticker qua cac vi tri (user ket an")
        print("     2026-08-31 o co-dai 26: 'lap di lap lai 1 sticker roi doi vi tri...")
        print("     rat nham'). 1 sticker = 1 lan/scene, vao SAU hero ~2s roi exit;")
        print("     scene >20s thi them file sticker RIENG (~1 file moi 5-6s).")
        return 1

    print("GATE NHIP HINH: SACH 3/3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
