# -*- coding: utf-8 -*-
"""add_sfx.py — thêm lớp ÂM HOÀI NIỆM vào project.json (chạy SAU patch_archival).

🔴 THỨ TỰ BẮT BUỘC: `patch_archival.py` dựng lại track hình từ `project.orig.json`,
nên nó XOÁ mọi track khác mình thêm tay. Luôn chạy:
    1) patch_archival.py   (hình)
    2) add_sfx.py          (tiếng)   ← file này
Chạy ngược lại là mất sạch lớp tiếng mà không báo lỗi gì.

Lớp tiếng gồm 2 loại, khác hẳn nhau về nguồn gốc và rủi ro:
  · TƯ LIỆU THẬT — trẻ em Nhật hát, phim "Japan" (1960, NARA, CC0). Chỉ có ~42 giây
    trong đúng một cảnh; dùng cho MỞ BÀI.
  · TỰ SYNTH — chuông trường Westminster + chuông phát thanh (make_nostalgia_sfx.py),
    license sạch tuyệt đối; dùng cho các mốc GIỮA bài.

Mốc đặt neo theo NỘI DUNG CÂU trong captions, không phải theo giây cứng — sửa lời hay
đổi giọng thì mốc tự trôi theo, không lệch.

Usage:
  py -3 tools/add_sfx.py --project showa-01-v2 [--dry]
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SFX_SRC = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\01_kyushoku\_sfx")
J1960 = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_footage_test\japan_1960\japan_1960.mp4")

# đoạn trẻ em hát trong phim 1960: thuyết minh tiếng Anh dứt ở ~1470s, hát tới ~1512s
SONG_SS, SONG_DUR = 1472.0, 14.0

# (id, file, neo = chuỗi trong câu phụ đề, lệch giây, âm lượng, ghi chú)
PLAN = [
    ("sfx_kids_song", "sfx_kids_song.wav", None, 0.0, 0.22,
     "trẻ em Nhật hát (1960, CC0) — chạy dưới mở bài, tắt dần"),
    ("sfx_chime_lunch", "sfx_chime_lunch.wav", "廊下の向こうから", -0.3, 0.30,
     "chuông hết tiết 4 — đúng lúc nói về mùi bay từ hành lang"),
    ("sfx_pa", "sfx_pa.wav", "放送委員", -0.5, 0.34,
     "chuông phát thanh trưa — đúng câu 放送委員の、少し緊張した声"),
    ("sfx_chime_far", "sfx_chime_far.wav", "昼休みの校庭へ", 1.2, 0.13,
     "chuông trường xa và nhỏ — lúc lũ trẻ chạy ra sân"),
]


def build_assets(assets: Path) -> None:
    assets.mkdir(parents=True, exist_ok=True)
    # ① trẻ em hát — lọc băng + cân âm + fade sẵn (schema không có field fade)
    out = assets / "sfx_kids_song.wav"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", str(SONG_SS), "-t", str(SONG_DUR), "-i", str(J1960),
         "-map", "0:a:0", "-af",
         f"highpass=f=200,lowpass=f=5200,dynaudnorm=g=9,"
         f"afade=t=in:st=0:d=1.0,afade=t=out:st={SONG_DUR-4.5}:d=4.5",
         "-ac", "2", "-ar", "48000", str(out)], check=True)
    # ② chuông: lấy nguyên bản đã synth sẵn
    shutil.copy2(SFX_SRC / "school_chime.wav", assets / "sfx_chime_lunch.wav")
    shutil.copy2(SFX_SRC / "pa_chime.wav", assets / "sfx_pa.wav")
    # ③ bản chuông XA: cắt treble + vọng → nghe như vang từ cuối sân
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(SFX_SRC / "school_chime.wav"),
         "-af", "lowpass=f=1800,aecho=0.8:0.85:60|110:0.32|0.22,volume=0.9",
         "-ac", "2", "-ar", "48000", str(assets / "sfx_chime_far.wav")], check=True)


def dur_sec(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    pdir = ROOT / "projects" / a.project
    pjson = pdir / "project.json"
    proj = json.loads(pjson.read_text(encoding="utf-8"))
    fps = proj["meta"]["fps"]
    lines = proj["captions"]["lines"]
    assets = ROOT / "public" / "projects" / a.project / "assets"

    if not a.dry:
        build_assets(assets)

    clips, report = [], []
    for cid, fname, anchor, offset, vol, note in PLAN:
        path = assets / fname
        if not path.exists():
            print(f"❌ thiếu {fname}")
            return 2
        if anchor is None:
            start = 0.0
        else:
            hit = [l for l in lines if anchor in l["text"]]
            if not hit:
                print(f"❌ không thấy câu neo '{anchor}' — lời đã đổi? Sửa PLAN.")
                return 2
            if len(hit) > 1:
                print(f"⚠️ '{anchor}' khớp {len(hit)} câu — lấy câu đầu")
            start = hit[0]["startMs"] / 1000 + offset
        d = dur_sec(path)
        clips.append({
            "id": cid, "kind": "audio",
            "from": max(0, int(round(start * fps))),
            "durationInFrames": int(round(d * fps)),
            "asset": f"assets/{fname}", "volume": vol, "trimStartFrames": 0,
        })
        report.append((start, cid, d, vol, note))

    proj["tracks"] = [t for t in proj["tracks"] if t["id"] != "trk-sfx"]
    # `name` là field BẮT BUỘC của TrackSchema — thiếu thì Remotion chặn render với
    # `tracks.N.name: Invalid input` (đã dính 2026-08-17). Schema mới là nơi kiểm, không
    # phải tool này, nên copy đủ shape của track có sẵn thay vì tự chế.
    proj["tracks"].append({
        "id": "trk-sfx", "name": "SFX", "type": "audio", "muted": False,
        "hidden": False, "locked": False, "clips": clips,
    })

    if not a.dry:
        pjson.write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{'(DRY) ' if a.dry else ''}✅ trk-sfx: {len(clips)} tiếng")
    for start, cid, d, vol, note in sorted(report):
        print(f"   · {int(start//60):02d}:{start%60:04.1f}  {cid:16} {d:5.1f}s  vol {vol:.2f}  {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
