# -*- coding: utf-8 -*-
"""cut_archival.py — cắt đoạn phim tư liệu PD/CC0 thành clip 1920x1080 cho remotion-vox.

Nguồn phải là phim ĐÃ VERIFY license (xem FOOTAGE_GO_NO_GO.md + §rights của item
archive.org). Tool này KHÔNG kiểm license — nó chỉ cắt; việc verify là của người gọi.

- crop vùng ảnh thật (bỏ viền đen của bản scan) → crop 16:9 (bias dọc theo từng shot,
  để không cắt mất đầu người) → scale 1920x1080 lanczos
- MUTE toàn bộ (luật: nhạc/tiếng trong phim PD vẫn có quyền riêng)
- grade nhẹ cho khớp tông 8mm/Kodachrome của kênh + hạt phim + vignette

Usage:
  py -3 tools/cut_archival.py --spec tools/archival_spec_01.json --outdir <dir>
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# vùng ảnh thật của từng bản scan (đo bằng ffmpeg cropdetect, ghi lại theo TỪNG FILE
# — đừng bê hằng số giữa các bản scan khác nhau)
ACTIVE = {
    "japan_today.mp4": (632, 480, 4, 0),
    # video 05 (2026-08-26): cung item gov.archives.arc.1692903 "Japan Today" (1959, NSC/CIA,
    # CC0), ban mp4 640x480 tai lai bang dl_parallel.py — cung vung anh that
    "japan_today_1959.mp4": (632, 480, 4, 0),
    # video 17 HD (23/09): ban .mpeg bitrate cao, 720x480 SAR 8:9 interlaced -> tien xu ly yadif+crop 712:480:4:0+scale 640:480 setsar=1
    "japan_today_1959_hd_sq.mp4": (640, 480, 0, 0),
    "you_in_japan_512kb.mp4": (312, 240, 2, 0),   # video 17 (23/09): cropdetect 316:240, dai den ~4px ben PHAI -> 312:240:2:0
    # do bang cropdetect 2026-08-22: full khung, khong vien den
    "children1941_full.mp4": (640, 480, 0, 0),
    # video 04 (2026-08-25): "We the Japanese People" (1952, USIA/gov.archives.li.111-cad-24-52,
    # CC0) - cropdetect khong bat vien den -> full 320x240 nhu you_in_japan (cung dinh dang
    # FedFlix 512kb derivative)
    "we_the_japanese_512kb.mp4": (320, 240, 0, 0),
    # video 08 (2026-09-03): "Big Picture: Japan" (US Army Signal Corps, gov.archives.arc.2569524, CC0,
    # ~1953-57, B&W) - ffprobe 320x240 full khung, FedFlix 512kb derivative nhu tren
    "big_picture_japan_512kb.mp4": (320, 240, 0, 0),
    # video 11 (2026-09-11): "Japan / Creation of New Wealth" (1960, NSC-CIA,
    # gov.archives.arc.642010, CC0, B&W, 27'35) - cropdetect 632x480+4+0, giong ban
    # japan_today_1959 (cung dong scan NARA 640x480)
    "steel_1960.mp4": (632, 480, 4, 0),
    # video 16 (2026-09-21) — REAL-FIRST v2. Hai phim USAF 1946 (PD Mark 1.0), ban mp4
    # archive.org la 640x360 FULL KHUNG 16:9, cropdetect 60/60 frame ra crop=640:360:0:0
    # => KHONG co vien den, khac han dong scan NARA 640x480 o tren. Dung bE hang so 632x480
    # sang day: no se cat mat 2 ben va keo lech khung.
    "usaf11070_religious_1946.mp4": (640, 360, 0, 0),
    "usaf11059_kyoto_home_1946.mp4": (640, 360, 0, 0),
    "usaf11079_hiroshima_life_1946.mp4": (640, 360, 0, 0),
    "usaf11050_agri_1946.mp4": (640, 360, 0, 0),
    # video 18 (2026-09-23): 「どっこい生きてる」(1951, 今井正, 新星映画社・前進座) — Commons
    # "Public domain" (phim Nhat do to chuc san xuat, cong chieu truoc 1953). webm 640x480 4:3 DEN TRANG,
    # cropdetect 6/6 mau (t=300..5000) ra 628:480:6:0 — vien den 6px hai ben.
    "dokkoi_ikiteru_1951.webm": (628, 480, 6, 0),
    "usaf11068_industry_1946.mp4": (640, 360, 0, 0),
    "usaf11069_transport_1946.mp4": (640, 360, 0, 0),
    # video 18 lan 2 (2026-09-23): thay dokkoi (ban quyen chua het) — 4 phim PD moi, soi sheet 10s/khung
    "usaf11022_industrial_life_1946.mp4": (640, 360, 0, 0),
    "usaf11018_way_of_life_tokyo_1945.mp4": (640, 360, 0, 0),
    "npc14671_ruins_tokyo_1945.mp4": (640, 360, 0, 0),
    "npc14672_street_tokyo_1945.mp4": (640, 360, 0, 0),
    "univ_japan_today_1946.mp4": (628, 472, 6, 4),
    # video 18 lan 3 (2026-09-23): ban GOC 1280x720 (.mov archive.org) — net ~4x ban mp4 640x360, cung timeline
    "usaf11022_industrial_life_1946_hd.mov": (1280, 720, 0, 0),
    "usaf11018_way_of_life_tokyo_1945_hd.mov": (1280, 720, 0, 0),
    "usaf11068_industry_1946_hd.mov": (1280, 720, 0, 0),
    "usaf11069_transport_1946_hd.mov": (1280, 720, 0, 0),
    "usaf11026_repatriates_otake_1946_hd.mov": (1280, 720, 0, 0),
    "usaf11078_hiroshima_life_1946_hd.mov": (1280, 720, 0, 0),
    "usaf11059_kyoto_home_1946_hd.mov": (1280, 720, 0, 0),
    "usaf11079_hiroshima_life_1946_hd.mov": (1280, 720, 0, 0),
    "usaf11050_agri_1946_hd.mov": (1280, 720, 0, 0),
    # video 17 (2026-09-23): "Color Story of Japan" 1957 (US Navy, 428-NPC-521/522, PD). Goc 720x480 DAR 15:11
    # (pixel KHONG vuong) -> chuyen truoc sang *_sq.mp4 = crop 712:480:4:0 + scale 648:480 setsar=1 => full khung.
    # video 22 (2026-10-03): "R & R in Tokyo" 1951, US Navy NARA 428-NPC-11736 (naId 79127), 720x480 SAR 10:11
    # -> *_sq.mp4 = crop 716:480:0:0 (cropdetect) + scale 650:480 setsar=1
    "npc11736_sq.mp4": (650, 480, 0, 0),
    "color_story_japan_1957_r1_sq.mp4": (648, 480, 0, 0),
    "color_story_japan_1957_r2_sq.mp4": (648, 480, 0, 0),
    # "Japan" 1960 NSC/CIA (gov.archives.arc.1719752, CC0) — cung dong scan NARA 640x480
    "japan_1960_nsc.mp4": (632, 480, 4, 0),
}


# ---------------------------------------------------------------- PRE (2026-09-21)
# 🔴 HIEU CHINH RIENG TUNG NGUON, tach han khoi `grade` chung.
# Ly do: 4 phim USAF 1946 do duoc LECH NHAU RAT XA — Y 64,4 / 89,1 / 90,5 / 111,1 va
# CA BON deu am do (V lech +4,5..+8,3 = Ektachrome bac mau). Mot he so `grade` duy nhat
# khong the vua keo 64 len vua keo 111 xuong; ep chung mot so thi hoac chay hoac toi.
#   PRE  = sua NGUON  (gamma ve ~100 + trung hoa am mau)  -> khac nhau tung file
#   grade= LOOK CUA KENH (hat phim, contrast)             -> giong nhau
# => spec cua video 16 dat "grade": 0 cho 4 nguon nay, toan bo nam trong PRE + HOUSE.
HOUSE = "eq=contrast=1.06:saturation=0.96,noise=alls=4:allf=t+u"
PRE = {
    # 🔬 do 2026-09-21 tren DUNG cac vung se dung (POOLS cua gen_archival_16.py),
    # n = 720..2436 frame moi nguon — khong do mot cua so roi suy ra ca phim
    # (lan dau lam vay: do o t=200, nghiem thu o t=374, ket qua lech nguoc chieu).
    #   Y tv / U lech / V lech  ->  gamma = ln(Y/255)/ln(100/255)
    # 11070: 80.0 / -11.5 / +8.6      11059: 105.9 / -3.6 / +7.1
    # 11079: 79.3 /  -1.9 / +5.4      11050: 117.5 / -5.3 / +3.6
    "usaf11070_religious_1946.mp4":     "eq=gamma=1.239,colorbalance=rm=-0.086:bm=0.115",
    "usaf11059_kyoto_home_1946.mp4":    "eq=gamma=0.939,colorbalance=rm=-0.071:bm=0.036",
    "usaf11079_hiroshima_life_1946.mp4":"eq=gamma=1.248,colorbalance=rm=-0.054:bm=0.019",
    "usaf11050_agri_1946.mp4":          "eq=gamma=0.828,colorbalance=rm=-0.036:bm=0.053",
    # 🔬 do 2026-09-23 tren 40 o se dung cua video 18: Y tb 102,0 (min 42 o canh rang dong co y) ⇒ KHONG
    # can gamma. Chi ep DEN TRANG tuyet doi (hue=s=0): ban webm co vet chroma, HOUSE lai giu saturation 0,96.
    "dokkoi_ikiteru_1951.webm":         "hue=s=0",
    # 🔬 do 2026-09-23 tren dung vung video 18 dung (12 frame/phim): Y / U lech / V lech
    # 11068: 110.3 / +0.7 / +6.3      11069: 111.6 / -10.6 / +2.3   (cong thuc cung bo 4 phim tren)
    "usaf11068_industry_1946.mp4":      "eq=gamma=0.896,colorbalance=rm=-0.063:bm=-0.007",
    "usaf11069_transport_1946.mp4":     "eq=gamma=0.882,colorbalance=rm=-0.023:bm=0.106",
    # 🔬 do 2026-09-23 signalstats tren dung cac vung video 18 dung (12 / 5 moc)
    # 11022: 120.2 / -0.9 / -3.5      11018: 94.7 / -3.0 / +4.6 (ban hong phai)
    "usaf11022_industrial_life_1946.mp4":   "eq=gamma=0.804,colorbalance=rm=0.035:bm=0.009",
    "usaf11018_way_of_life_tokyo_1945.mp4": "eq=gamma=1.058,colorbalance=rm=-0.046:bm=0.030",
    "npc14671_ruins_tokyo_1945.mp4":        "hue=s=0",
    "npc14672_street_tokyo_1945.mp4":       "hue=s=0",
    "univ_japan_today_1946.mp4":            "hue=s=0",
    # ban HD: cung phim -> cung PRE voi ban mp4; 2 cuon moi do signalstats 2026-09-23
    # 11026: 79.1 / -0.7 / +3.3     11078 (xuong in, toi): 58.0 / -4.1 / -0.5 -> gamma KEP 1.30 (1.58 thi vo hat)
    "usaf11022_industrial_life_1946_hd.mov":   "eq=gamma=0.804,colorbalance=rm=0.035:bm=0.009",
    "usaf11018_way_of_life_tokyo_1945_hd.mov": "eq=gamma=1.058,colorbalance=rm=-0.046:bm=0.030",
    "usaf11068_industry_1946_hd.mov":          "eq=gamma=0.896,colorbalance=rm=-0.063:bm=-0.007",
    "usaf11069_transport_1946_hd.mov":         "eq=gamma=0.882,colorbalance=rm=-0.023:bm=0.106",
    "usaf11059_kyoto_home_1946_hd.mov":        "eq=gamma=0.939,colorbalance=rm=-0.071:bm=0.036",
    "usaf11079_hiroshima_life_1946_hd.mov":    "eq=gamma=1.248,colorbalance=rm=-0.054:bm=0.019",
    "usaf11050_agri_1946_hd.mov":              "eq=gamma=0.828,colorbalance=rm=-0.036:bm=0.053",
    "usaf11026_repatriates_otake_1946_hd.mov": "eq=gamma=1.251,colorbalance=rm=-0.033:bm=0.007",
    "usaf11078_hiroshima_life_1946_hd.mov":    "eq=gamma=1.300,colorbalance=rm=0.005:bm=0.041",
}


def build_vf(active, ybias: float, grade: float, srcname: str = "") -> str:
    aw, ah, ax, ay = active
    # 16:9 lấy trọn bề ngang vùng ảnh thật
    ch = int(round(aw * 9 / 16))
    ch = min(ch, ah)
    # ybias 0 = sát mép trên, 0.5 = giữa, 1 = sát đáy
    cy = ay + int(round((ah - ch) * ybias))
    parts = [
        f"crop={aw}:{ch}:{ax}:{cy}",
        "scale=1920:1080:flags=lanczos",
        # nét lại nhẹ sau upscale ~3x
        "unsharp=5:5:0.45:5:5:0.0",
    ]
    if srcname in PRE:
        parts += [PRE[srcname], HOUSE]
    if grade > 0:
        g = grade
        # 🔴 NÂNG SÁNG là phần chính, không phải trang trí. Đo 2026-08-17: bản phim gốc
        # có độ sáng trung bình 26–50/255, trong khi slide ảnh AI của video là 90–113 —
        # chênh 2–4 lần. Để nguyên thì mỗi lần cắt sang phim tư liệu là màn hình tối sầm,
        # sai cả tệp 45+ (audience-45plus §1 gate 6: nền sáng). gamma 1.8 kéo về 69–102.
        # ⚠️ VIGNETTE bị BỎ HẲN: nó là thủ phạm lớn nhất (cắt thêm ~40% độ sáng) và
        # slide ảnh AI vốn đã có vignette riêng — chồng thêm chỉ tối thêm.
        parts += [
            f"eq=gamma={1+0.8*g:.3f}:contrast={1+0.05*g:.3f}:saturation={1-0.06*g:.3f}",
            f"colorbalance=rs={0.03*g:.3f}:gs={0.01*g:.3f}:bs={-0.04*g:.3f}",
            f"noise=alls={int(5*g)}:allf=t+u",
        ]
    return ",".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--only", default="", help="chỉ cắt id này (debug)")
    ap.add_argument("--allow-reuse", action="store_true", help="vượt SỔ ĐEN footage (phải có lý do, ghi vào script)")
    ap.add_argument("--record", default="", help="sau khi cắt xong, ghi các đoạn vào FOOTAGE_USED.json dưới slug này")
    a = ap.parse_args()

    # 🔴 SỔ ĐEN FOOTAGE (user chốt 2026-08-27: "video thật đã dùng rồi sẽ không dùng tiếp").
    # Cùng một item archive.org, đoạn [ss,end] đã lên sóng ở video khác → CHẶN. Bẫy gốc: ACTIVE có sẵn
    # "japan_today.mp4" từ video 01/02, video 05 tải lại cùng phim dưới tên khác và cắt lại 12/21 đoạn cũ.
    ledger_p = Path(__file__).resolve().parent.parent / "06_VIDEO" / "_footage_test" / "FOOTAGE_USED.json"
    ledger = json.loads(ledger_p.read_text(encoding="utf-8")) if ledger_p.exists() else {"aliases": {}, "used": []}
    alias = ledger.get("aliases", {})
    spec_pre = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    clashes = []
    for item in spec_pre["cuts"]:
        if a.only and item["id"] != a.only: continue
        src = Path(item["src"]).name; it = alias.get(src, src)
        s0, e0 = float(item["ss"]), float(item["ss"]) + float(item["dur"])
        for u in ledger["used"]:
            if u["item"] != it or (a.record and u["video"] == a.record): continue
            ov = min(e0, u["end"]) - max(s0, u["ss"])
            if ov > 0.5: clashes.append((item["id"], s0, e0, u["video"], u["id"], round(ov, 1)))
    if clashes:
        print(f"🔴 SỔ ĐEN FOOTAGE: {len(clashes)} đoạn ĐÃ DÙNG ở video trước:")
        for c in clashes: print(f"   {c[0]:26} {c[1]:.0f}-{c[2]:.0f}s  trùng {c[3]}/{c[4]} ({c[5]}s)")
        if not a.allow_reuse:
            print("   → đổi ss sang đoạn chưa dùng (xem FOOTAGE_GO_NO_GO.md 'CÒN CHƯA DÙNG'), hoặc --allow-reuse có lý do."); return 4

    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    made = []
    for item in spec["cuts"]:
        if a.only and item["id"] != a.only:
            continue
        src = Path(item["src"])
        if not src.exists():
            print(f"  ❌ thiếu nguồn: {src}")
            return 2
        active = ACTIVE.get(src.name)
        if active is None:
            print(f"  ❌ chưa đo vùng ảnh thật cho {src.name} — chạy cropdetect rồi thêm vào ACTIVE")
            return 2
        out = outdir / f"{item['id']}.mp4"
        vf = build_vf(active, float(item.get("ybias", 0.5)), float(item.get("grade", 1.0)), src.name)
        cmd = [
            "ffmpeg", "-v", "error", "-y",
            "-ss", str(item["ss"]), "-t", str(item["dur"]), "-i", str(src),
            "-an",                      # MUTE — quyền nhạc/tiếng trong phim là riêng
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            str(out),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ❌ {item['id']}: {r.stderr[-300:]}")
            return 3
        mb = out.stat().st_size / 1e6
        print(f"  ✓ {item['id']:22} {item['dur']:>4}s  {mb:6.1f}MB  ← {src.name}@{item['ss']}s  · {item.get('note','')}")
        made.append(item["id"])

    print(f"\nOK {len(made)} clip → {outdir}")
    if a.record and made:
        # ghi sổ đen CÙNG LƯỢT cắt (không ghi = lần sau lại trùng). Đè entry cùng (video,id).
        ledger["used"] = [u for u in ledger["used"] if not (u["video"] == a.record and u["id"] in made)]
        for item in spec["cuts"]:
            if item["id"] not in made:
                continue
            src = Path(item["src"]).name
            ledger["used"].append({"item": alias.get(src, src), "file": src, "ss": float(item["ss"]),
                                   "end": round(float(item["ss"]) + float(item["dur"]), 2),
                                   "video": a.record, "id": item["id"]})
        ledger_p.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"   📒 đã ghi {len(made)} đoạn vào sổ đen dưới '{a.record}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
