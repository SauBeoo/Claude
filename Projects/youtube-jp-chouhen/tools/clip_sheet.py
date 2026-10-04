# -*- coding: utf-8 -*-
"""clip_sheet.py — contact sheet để DUYỆT CLIP BẰNG MẮT trước khi render.

Bắt buộc theo `Projects/youtube-jp-chouhen/CLAUDE.md` §Visual (bài học video 09: clip có
2 người áo blouse trắng mặt nhận diện rõ lọt vào bản render → phải render lại từ đầu).

2 chế độ:
  new    — soi clip MỚI TẢI (lọc theo mtime): duyệt vòng 1 ngay sau fetch_bg
  picks  — soi ĐÚNG bộ clip renderer ĐÃ CHỌN, đọc từ 06_VIDEO/<slug>/_render_plan.json
           (duyệt vòng 2 sau --stage segs; đây mới là vòng CHẶN THẬT, vì renderer chọn
           từ CẢ pool nên clip cũ chưa ai soi vẫn lọt vào)

  python tools/clip_sheet.py new  --minutes 60 -o 06_VIDEO/<slug>/_sheet_new.jpg
  python tools/clip_sheet.py picks <slug>      -o 06_VIDEO/<slug>/_sheet_picks.jpg

Mỗi ô = 1 frame giữa clip + tên file (để loại thì biết xoá cái nào).
Loại 1 clip = 2 việc: `ln` vào `_bg/rejected/` VÀ `rm` bản trong `_bg/` (hardlink!).
"""
import argparse, json, math, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
BG = PROJ / "06_VIDEO" / "_bg"
COLS, TW = 6, 320          # 6 cột, mỗi ô rộng 320px


def dur(f):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return 0.0


def grab(f, out):
    d = dur(f)
    subprocess.run(["ffmpeg", "-y", "-ss", f"{d/2:.2f}", "-i", str(f), "-frames:v", "1",
                    "-vf", f"scale={TW}:-2", str(out), "-loglevel", "error"], check=False)
    return out.exists(), d


def sheet(files, out):
    from PIL import Image, ImageDraw, ImageFont
    tmp = out.parent / "_sheet_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
    tiles = []
    for i, f in enumerate(files):
        p = tmp / f"{i:03d}.jpg"
        ok, d = grab(f, p)
        if ok:
            tiles.append((p, f.name, d))
        print(f"  [{i+1}/{len(files)}] {'OK  ' if ok else 'FAIL'} {f.name} ({d:.0f}s)")
    if not tiles:
        sys.exit("[LỖI] không trích được frame nào")
    th = Image.open(tiles[0][0]).height
    rows = math.ceil(len(tiles) / COLS)
    LAB = 20
    canvas = Image.new("RGB", (COLS * TW, rows * (th + LAB)), (18, 18, 22))
    dr = ImageDraw.Draw(canvas)
    for i, (p, name, d) in enumerate(tiles):
        x, y = (i % COLS) * TW, (i // COLS) * (th + LAB)
        canvas.paste(Image.open(p), (x, y))
        dr.rectangle([x, y + th, x + TW, y + th + LAB], fill=(28, 28, 34))
        dr.text((x + 4, y + th + 3), f"{i+1:02d} {name[:30]} {d:.0f}s", font=font,
                fill=(210, 210, 215))
        dr.rectangle([x, y, x + TW - 1, y + th + LAB - 1], outline=(60, 60, 70))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=88)
    for p, _, _ in tiles:
        p.unlink(missing_ok=True)
    tmp.rmdir()
    print(f"\n→ {out}  ({len(tiles)} ô, {COLS}×{rows})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["new", "picks"])
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--minutes", type=float, default=60, help="mode new: clip tải trong N phút qua")
    ap.add_argument("--from-log", help="mode new: lấy ĐÚNG danh sách từ fetch log (dòng '  OK <file>'). "
                                       "DÙNG CÁI NÀY khi có nhiều vòng fetch gần nhau — "
                                       "lọc theo --minutes sẽ trộn 2 batch và làm LỆCH số ô "
                                       "(sự cố thật 2026-07-30: loại oan 3 clip vì đếm sai ô).")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    if a.mode == "new":
        if a.from_log:
            import re as _re
            txt = Path(a.from_log).read_text(encoding="utf-8", errors="replace")
            names = [m.group(1) for m in _re.finditer(r"^  OK (\S+\.mp4)", txt, _re.M)]
            files = [BG / n for n in names if (BG / n).exists()]
            print(f"clip theo {a.from_log}: {len(names)} tải, {len(files)} còn trong _bg")
        else:
            cut = time.time() - a.minutes * 60
            files = sorted((f for f in BG.glob("*.mp4") if f.stat().st_mtime >= cut),
                           key=lambda f: f.name)
            print(f"clip tải trong {a.minutes:.0f} phút qua: {len(files)}")
            print("⚠️ lọc theo thời gian: nếu vừa chạy >1 vòng fetch thì số ô sẽ TRỘN 2 batch. "
                  "Có nhiều vòng → dùng --from-log <fetch.log>.")
    else:
        if not a.slug:
            sys.exit("mode picks cần <slug>")
        # `--plan-only` chỉ ghi _picks.json (chưa cắt segment) → duyệt được TRƯỚC khi cắt.
        # ⚠️ Phải lấy file MỚI HƠN, không ưu tiên cứng _render_plan.json: sau một vòng loại
        # clip + chạy lại --plan-only thì _render_plan.json là bản LẠC HẬU, đọc nó = duyệt
        # sai bộ (bắt được ngay lúc dùng lần đầu, video 16).
        vd = PROJ / "06_VIDEO" / a.slug
        cands = [p for p in (vd / "_render_plan.json", vd / "_picks.json") if p.exists()]
        if not cands:
            sys.exit(f"[LỖI] chưa có {vd}/_picks.json — chạy scene_render --stage segs --plan-only")
        plan = max(cands, key=lambda p: p.stat().st_mtime)
        print(f"(đọc {plan.name})")
        if not plan.exists():
            sys.exit(f"[LỖI] chưa có {plan} — chạy scene_render.py {a.slug} --stage segs trước")
        d = json.loads(plan.read_text(encoding="utf-8"))
        picks = d.get("picks") or sorted({s.get("clip") for s in d.get("scenes", []) if s.get("clip")})
        files = [BG / p if not Path(p).is_absolute() else Path(p) for p in picks]
        files = [f if f.exists() else BG / Path(f).name for f in files]
        print(f"clip renderer ĐÃ CHỌN cho {a.slug}: {len(files)}")
    if not files:
        sys.exit("không có clip nào để soi")
    sheet(files, Path(a.out))
    print("Soi từng ô: có MẶT người nhận diện được? logo/chữ thương hiệu? màu rực phá mood đêm?")
    print("Loại thì báo số ô — tao ln vào _bg/rejected/ + rm bản trong _bg/ (hardlink nên phải xoá cả 2).")


if __name__ == "__main__":
    main()
