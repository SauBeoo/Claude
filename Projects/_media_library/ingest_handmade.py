# -*- coding: utf-8 -*-
"""ingest_handmade.py — Nhập footage TỰ LÀM (tay thật / iPad) vào pipeline video.

Đây là cầu nối cho "lớp không copy được" của mọi kênh:
`.claude/rules/handmade-layer.md` là nguồn sự thật về CHÍNH SÁCH; file này lo phần CƠ KHÍ.

4 loại footage (field `hm_kind`):
    tegami    — 手元動画: bàn tay thật làm thật (co-dai: pha, cắt, dán, đo)
    notebook  — iPad + Apple Pencil viết ノート thật, screen-record (nenkin/kaigo/akiya)
    genten    — 原典: mở trang luật/PDF cơ quan, khoanh đỏ bằng Pencil, screen-record
    character — nhân vật vẽ tay (Procreate / Procreate Dreams) cho kênh truyện

Vì sao phải qua tool: file thô từ iPad/iPhone là .MOV HEVC dọc 60fps có audio —
ffmpeg trong renderer ghép thẳng sẽ lệch khung/màu/fps hoặc chèn tiếng phòng vào
video. Tool chuẩn hóa về đúng khuôn renderer (1920x1080, 30fps, h264, không audio)
rồi nhập kho chung để tái dùng + tra được đã dùng ở video nào.

Cách chạy — B1 nhập kho (chuẩn hóa 1 lần):
    python ingest_handmade.py ingest "C:\\...\\IMG_0421.MOV" --channel youtube-jp-co-dai \\
        --hm-kind tegami --tags "重曹 掃除 手元" --speed 1.8 --trim 0:04,0:38

B2 xem kho:
    python ingest_handmade.py list --channel youtube-jp-co-dai [--unused-for youtube-jp-co-dai]

B3 gắn vào 1 video (hardlink + tự bật cờ trong SLIDES.json):
    python ingest_handmade.py place E:\\...\\06_VIDEO\\<slug> --map 03=<tên> 11=<tên> \\
        --slides E:\\...\\03_SCRIPTS\\<x>_SLIDES.json --used-by youtube-jp-co-dai/<slug>

B4 duyệt mắt trước render (BẮT BUỘC — luật media-library §3):
    python ingest_handmade.py sheet E:\\...\\06_VIDEO\\<slug> -o sheet.jpg

Slot trong --map = **chỉ số 0-based của entry trong SLIDES.json** (khớp clip_XX.mp4
mà video_render.py đọc), KHÔNG phải số 第N位.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_lib as ML

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H, FPS = 1920, 1080, 30
HM_KINDS = ("tegami", "notebook", "genten", "character")


# ---------------------------------------------------------------- ffprobe/ffmpeg

def probe(path):
    """Trả (width, height, duration, has_audio) — thiếu stream thì 0/False."""
    cmd = ["ffprobe", "-v", "error", "-print_format", "json",
           "-show_streams", "-show_format", str(path)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"[LỖI] ffprobe không đọc được {path}\n{r.stderr[:400]}")
    d = json.loads(r.stdout)
    vs = next((s for s in d["streams"] if s.get("codec_type") == "video"), None)
    if vs is None:
        raise SystemExit(f"[LỖI] {path} không có stream video")
    has_audio = any(s.get("codec_type") == "audio" for s in d["streams"])
    w, h = int(vs.get("width", 0)), int(vs.get("height", 0))
    # iPhone/iPad quay dọc: khung lưu ngang + rotate metadata → đảo lại cho đúng thực tế
    rot = 0
    for tag in (vs.get("side_data_list") or []):
        if "rotation" in tag:
            rot = abs(int(float(tag["rotation"]))) % 180
    if rot == 90:
        w, h = h, w
    dur = float(d.get("format", {}).get("duration") or vs.get("duration") or 0)
    return w, h, dur, has_audio


def _hms(t):
    """'0:04' / '4' / '1:02:03' / '4.5' → giây (float)."""
    parts = str(t).strip().split(":")
    try:
        parts = [float(p) for p in parts]
    except ValueError:
        raise SystemExit(f"[LỖI] --trim không hiểu mốc thời gian: {t}")
    sec = 0.0
    for p in parts:
        sec = sec * 60 + p
    return sec


def parse_crop_box(s, w, h):
    """'x0,y0,x1,y1' (pixel hoặc tỉ lệ 0–1) → chuỗi filter crop của ffmpeg.
    Dùng để cắt status bar + toolbar app khỏi screen-record iPad."""
    try:
        v = [float(x) for x in str(s).split(",")]
    except ValueError:
        raise SystemExit(f"[LỖI] --crop-box cần 4 số x0,y0,x1,y1: {s}")
    if len(v) != 4:
        raise SystemExit(f"[LỖI] --crop-box cần đúng 4 số: {s}")
    if max(v) <= 1.0:  # dạng tỉ lệ
        v = [v[0] * w, v[1] * h, v[2] * w, v[3] * h]
    x0, y0, x1, y1 = (int(round(n)) for n in v)
    if x1 <= x0 or y1 <= y0:
        raise SystemExit("[LỖI] --crop-box: x1>x0 và y1>y0")
    x0, y0 = max(x0, 0), max(y0, 0)
    x1, y1 = min(x1, w), min(y1, h)
    cw, ch = (x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2  # chẵn cho yuv420p
    if cw < 16 or ch < 16:
        raise SystemExit("[LỖI] --crop-box quá nhỏ sau khi kẹp vào khung gốc")
    return f"crop={cw}:{ch}:{x0}:{y0}", (cw, ch)


def normalize(src, dest, speed=1.0, trim=None, fit="cover", fps=FPS,
              keep_audio=False, denoise=False, crop_box=None, src_size=None):
    """Chuẩn hóa 1 file thô về khuôn renderer. Trả duration thật sau xử lý."""
    src, dest = Path(src), Path(dest)
    vf = []
    if crop_box:
        w0, h0 = src_size
        f, (cw, ch) = parse_crop_box(crop_box, w0, h0)
        vf.append(f)  # cắt UI TRƯỚC khi scale, nếu không sẽ scale cả thanh công cụ
        print(f"  → cắt UI: {cw}x{ch} (từ {w0}x{h0})")
        ar = cw / ch
        if fit == "cover" and abs(ar - W / H) > 0.02:
            ideal = int(round(cw / (W / H))) // 2 * 2
            print(f"  ⚠ khung cắt {ar:.2f}:1 không phải 16:9 → bước scale sẽ cắt "
                  f"thêm {'trên/dưới' if ar < W / H else 'hai bên'}. Muốn không mất "
                  f"gì: chọn crop-box cao đúng {ideal}px (vd 0,<y>,{cw},<y+{ideal}>)")
    if fit == "cover":
        # phủ kín khung rồi cắt giữa — footage dọc bị cắt hai đầu (chấp nhận, tay
        # thường ở giữa khung); muốn thấy trọn khung dọc thì dùng --fit contain
        vf.append(f"scale={W}:{H}:force_original_aspect_ratio=increase")
        vf.append(f"crop={W}:{H}")
    else:
        vf.append(f"scale={W}:{H}:force_original_aspect_ratio=decrease")
        vf.append(f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black")
    if denoise:
        vf.append("hqdn3d=2:1:3:3")
    if speed and abs(speed - 1.0) > 1e-6:
        vf.append(f"setpts=PTS/{speed}")
    vf.append(f"fps={fps}")

    cmd = ["ffmpeg", "-y"]
    if trim:
        cmd += ["-ss", f"{trim[0]:.3f}"]
        if trim[1] is not None:
            cmd += ["-to", f"{trim[1]:.3f}"]
    cmd += ["-i", str(src), "-vf", ",".join(vf),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if keep_audio:
        # tăng tốc thì audio phải khớp, nhưng atempo chỉ nhận 0.5–2.0
        if speed and abs(speed - 1.0) > 1e-6:
            if not (0.5 <= speed <= 2.0):
                raise SystemExit("[LỖI] --keep-audio + --speed ngoài 0.5–2.0: "
                                 "bỏ --keep-audio (giọng lấy từ TTS) hoặc hạ speed")
            cmd += ["-filter:a", f"atempo={speed}", "-c:a", "aac", "-b:a", "128k"]
        else:
            cmd += ["-c:a", "aac", "-b:a", "128k"]
    else:
        cmd += ["-an"]
    cmd += [str(dest)]

    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0 or not dest.exists():
        raise SystemExit(f"[LỖI] ffmpeg chuẩn hóa thất bại:\n{r.stderr[-1500:]}")
    return probe(dest)[2]


# ---------------------------------------------------------------- ingest

def cmd_ingest(a):
    idx = ML.load_index()
    trim = None
    if a.trim:
        p = [s for s in a.trim.split(",")]
        trim = (_hms(p[0]), _hms(p[1]) if len(p) > 1 and p[1].strip() else None)
        if trim[1] is not None and trim[1] <= trim[0]:
            raise SystemExit("[LỖI] --trim: mốc kết thúc phải sau mốc bắt đầu")

    tags = [t for t in re.split(r"[,\s]+", a.tags or "") if t]
    tmp_dir = ML.HANDMADE_DIR / "_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    added = []

    for raw in a.src:
        src = Path(raw)
        if not src.exists():
            print(f"  ⚠ bỏ qua (không tồn tại): {src}")
            continue
        w0, h0, dur0, has_a = probe(src)
        print(f"\n▶ {src.name}  {w0}x{h0}  {dur0:.1f}s"
              f"{'  (có audio → sẽ bỏ)' if has_a and not a.keep_audio else ''}")

        stem = f"{a.hm_kind}_{ML._slug(a.channel, 24)}_{ML._slug(src.stem, 16)}"
        tmp = tmp_dir / f"{stem}.mp4"
        dur = normalize(src, tmp, speed=a.speed, trim=trim, fit=a.fit,
                        fps=a.fps, keep_audio=a.keep_audio, denoise=a.denoise,
                        crop_box=a.crop_box or None, src_size=(w0, h0))
        print(f"  → chuẩn hóa: {W}x{H} @{a.fps}fps, {dur:.1f}s"
              f"{f' (speed x{a.speed})' if a.speed != 1.0 else ''}")
        if dur < 3.0:
            print(f"  ⚠ chỉ {dur:.1f}s — cue trong video thường 8–20s, renderer sẽ "
                  f"LOOP clip này (thấy rõ nhịp lặp). Nên quay dài hơn.")

        name = ML.add_file(
            tmp, "handmade", source="handmade", source_id=stem,
            url="", query=" ".join(tags), title=a.title or src.stem,
            tags=sorted(set(tags + [a.hm_kind, a.channel])),
            license="Own footage (tự quay/tự vẽ) — toàn quyền",
            width=W, height=H, duration=round(dur, 2), idx=idx, autosave=False,
        )
        e = idx[name]
        e["hm_kind"] = a.hm_kind
        e["channel"] = a.channel
        e["src_file"] = str(src)
        e["shot_on"] = a.shot_on or ""
        e["note"] = a.note or ""
        e["ingested"] = date.today().isoformat()
        added.append((name, dur))
        print(f"  ✓ vào kho: {name}")

    ML.save_index(idx)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    if not added:
        raise SystemExit("[LỖI] không nhập được file nào")
    print(f"\n✅ Nhập {len(added)} file vào {ML.HANDMADE_DIR}")
    for n, d in added:
        print(f"   {n}  ({d:.1f}s)")
    print("\nBước sau:  ingest_handmade.py place <video_dir> --map <slot>=<tên> "
          "--slides <SLIDES.json> --used-by <kênh>/<slug>")


# ---------------------------------------------------------------- list

def cmd_list(a):
    idx = ML.load_index()
    rows = []
    for name, e in idx.items():
        if e.get("kind") != "handmade":
            continue
        if a.channel and e.get("channel") != a.channel:
            continue
        if a.hm_kind and e.get("hm_kind") != a.hm_kind:
            continue
        if a.tag and a.tag not in (e.get("tags") or []):
            continue
        if a.unused_for and ML._is_used(e, a.unused_for):
            continue
        rows.append((name, e))
    if not rows:
        print("(kho footage tự làm chưa có gì khớp bộ lọc)")
        return
    rows.sort(key=lambda r: (r[1].get("hm_kind", ""), r[0]))
    print(f"{len(rows)} footage tự làm:\n")
    for name, e in rows:
        used = e.get("used_in") or []
        print(f"  [{e.get('hm_kind','?'):9}] {name}")
        print(f"      {e.get('duration',0):.1f}s · {e.get('channel','—')} · "
              f"tags: {', '.join(e.get('tags') or []) or '—'}")
        print(f"      đã dùng: {', '.join(used) if used else 'CHƯA DÙNG'}")


# ---------------------------------------------------------------- place

def _patch_slides(slides_path, slots):
    """Bật cờ "handmade": true cho các entry được gắn clip. Trả list cảnh báo."""
    p = Path(slides_path)
    if not p.exists():
        raise SystemExit(f"[LỖI] không có file SLIDES: {p}")
    # utf-8-sig: file do PowerShell/Notepad ghi hay có BOM, json.loads chết vì nó
    cfg = json.loads(p.read_text(encoding="utf-8-sig"))
    if not isinstance(cfg, list):
        raise SystemExit(f"[LỖI] {p} không phải mảng slide")
    warn = []
    for slot in slots:
        if slot >= len(cfg):
            warn.append(f"slot {slot:02d} vượt số entry SLIDES ({len(cfg)}) "
                        f"→ renderer sẽ KHÔNG bao giờ đọc clip_{slot:02d}.mp4")
            continue
        spec = cfg[slot]
        spec["handmade"] = True
        if spec.get("video"):
            warn.append(f"slot {slot:02d} đang có \"video\": true (stock-clip) "
                        f"— footage tự làm đã đè lên, nên xóa cờ cũ cho sạch")
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")
    return warn, len(cfg)


def cmd_place(a):
    video_dir = Path(a.video_dir).resolve()
    if not video_dir.is_dir():
        raise SystemExit(f"[LỖI] không có folder video: {video_dir}")
    clips_dir = video_dir / "clips"
    clips_dir.mkdir(exist_ok=True)
    idx = ML.load_index()

    pairs = []
    for item in a.map:
        if "=" not in item:
            raise SystemExit(f"[LỖI] --map cần dạng <slot>=<tên trong kho>: {item}")
        slot_s, name = item.split("=", 1)
        if not slot_s.strip().isdigit():
            raise SystemExit(f"[LỖI] slot phải là số 0-based: {item}")
        slot, name = int(slot_s), name.strip()
        e = idx.get(name)
        if e is None:
            raise SystemExit(f"[LỖI] không có trong kho: {name}\n"
                             f"       (chạy `ingest_handmade.py list` xem tên đúng)")
        if e.get("kind") != "handmade":
            raise SystemExit(f"[LỖI] {name} không phải footage tự làm "
                             f"(kind={e.get('kind')}) — dùng fetch_clips cho stock")
        pairs.append((slot, name, e))

    # đọc thử SLIDES trước khi hardlink — sai đường dẫn/JSON hỏng thì fail sớm,
    # đừng để clip đã gắn mà cờ chưa bật (renderer im lặng bỏ qua)
    if a.slides:
        _patch_slides(a.slides, [])

    for slot, name, e in pairs:
        dest = clips_dir / f"clip_{slot:02d}.mp4"
        ML.link_out(name, dest, used_by=a.used_by, idx=idx)
        print(f"  ✓ clip_{slot:02d}.mp4 ← {name}  ({e.get('duration',0):.1f}s)")

    n_entries = None
    if a.slides:
        warn, n_entries = _patch_slides(a.slides, [s for s, _, _ in pairs])
        print(f"  ✓ bật \"handmade\": true cho {len(pairs)} entry trong "
              f"{Path(a.slides).name} ({n_entries} entry tổng)")
        for w in warn:
            print(f"  ⚠ {w}")
    else:
        print("  ⚠ KHÔNG có --slides → renderer sẽ BỎ QUA clip vừa gắn. "
              "Phải tự thêm \"handmade\": true vào đúng entry trong SLIDES.json.")

    print(f"\n✅ Gắn {len(pairs)} footage tự làm vào {video_dir.name}")
    print("Bước sau (BẮT BUỘC): ingest_handmade.py sheet "
          f"\"{video_dir}\" -o sheet.jpg  → Read ảnh, duyệt mắt trước khi render")


# ---------------------------------------------------------------- sheet

def cmd_sheet(a):
    video_dir = Path(a.video_dir).resolve()
    clips = sorted((video_dir / "clips").glob("clip_*.mp4"))
    if not clips:
        raise SystemExit(f"[LỖI] không thấy clip_*.mp4 trong {video_dir / 'clips'}")
    out = Path(a.out) if Path(a.out).is_absolute() else video_dir / a.out
    tmp = video_dir / "_sheet_tmp"
    tmp.mkdir(exist_ok=True)
    tiles = []
    for c in clips:
        dur = probe(c)[2]
        png = tmp / f"{c.stem}.png"
        r = subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{max(dur / 2, 0):.2f}", "-i", str(c),
             "-frames:v", "1", "-vf", "scale=480:-2", str(png)],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 and png.exists():
            tiles.append(png)
        else:
            print(f"  ⚠ không trích được frame: {c.name}")
    if not tiles:
        raise SystemExit("[LỖI] không trích được frame nào")
    cols = min(3, len(tiles))
    cmd = ["ffmpeg", "-y"]
    for t in tiles:
        cmd += ["-i", str(t)]
    cmd += ["-filter_complex", f"tile={cols}x{-(-len(tiles) // cols)}:margin=8:padding=8",
            "-frames:v", "1", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    shutil.rmtree(tmp, ignore_errors=True)
    if r.returncode != 0 or not out.exists():
        raise SystemExit(f"[LỖI] ghép contact sheet thất bại:\n{r.stderr[-800:]}")
    print(f"✅ Contact sheet ({len(tiles)} clip): {out}")
    print("   → Read ảnh này, soi từng ô: khung có đúng thứ đang nói? tay có rõ? "
          "có lộ mặt/nhãn hiệu/đồ bừa bộn không?")


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(
        description="Nhập footage tự làm (tay thật/iPad) vào pipeline video")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ingest", help="chuẩn hóa file thô + nhập kho")
    p.add_argument("src", nargs="+", help="file thô từ iPad/iPhone/máy quay")
    p.add_argument("--channel", required=True, help="vd youtube-jp-co-dai")
    p.add_argument("--hm-kind", required=True, choices=HM_KINDS)
    p.add_argument("--tags", default="", help="từ khóa tra cứu, cách nhau bởi dấu cách")
    p.add_argument("--title", default="")
    p.add_argument("--speed", type=float, default=1.0,
                   help="tăng tốc (tay thật thường 1.5–2.0)")
    p.add_argument("--trim", default="", help="cắt: 'bắt_đầu,kết_thúc' vd 0:04,0:38")
    p.add_argument("--fit", choices=("cover", "contain"), default="cover")
    p.add_argument("--crop-box", dest="crop_box", default="",
                   help="cắt UI trước khi scale: 'x0,y0,x1,y1' pixel hoặc tỉ lệ 0–1 "
                        "(screen-record iPad: bỏ status bar + thanh công cụ app)")
    p.add_argument("--fps", type=int, default=FPS)
    p.add_argument("--keep-audio", action="store_true",
                   help="giữ tiếng gốc (mặc định BỎ — giọng lấy từ TTS)")
    p.add_argument("--denoise", action="store_true", help="giảm nhiễu (quay thiếu sáng)")
    p.add_argument("--shot-on", default="", help="iPad Pro / iPhone 13 / …")
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("list", help="xem kho footage tự làm")
    p.add_argument("--channel")
    p.add_argument("--hm-kind", choices=HM_KINDS)
    p.add_argument("--tag")
    p.add_argument("--unused-for", dest="unused_for", help="lọc cái chưa dùng ở kênh này")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("place", help="gắn footage vào 1 video + bật cờ SLIDES")
    p.add_argument("video_dir", help="06_VIDEO/<slug>")
    p.add_argument("--map", nargs="+", required=True,
                   help="<slot 0-based>=<tên trong kho>, vd 03=tegami_co-dai_img0421.mp4")
    p.add_argument("--slides", help="đường dẫn *_SLIDES*.json để tự bật cờ handmade")
    p.add_argument("--used-by", dest="used_by", help="<kênh>/<slug> để ghi sổ đã dùng")
    p.set_defaults(func=cmd_place)

    p = sub.add_parser("sheet", help="contact sheet duyệt mắt trước render")
    p.add_argument("video_dir")
    p.add_argument("-o", "--out", default="handmade_sheet.jpg")
    p.set_defaults(func=cmd_sheet)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
