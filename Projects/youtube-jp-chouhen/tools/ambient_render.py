# -*- coding: utf-8 -*-
"""ambient_render.py — render kênh youtube-jp-chouhen.
Nền = 1 clip ambient (sông/suối) LẶP suốt bài + phủ tối nhẹ + vignette,
phụ đề glass sync từng câu, giọng AivisSpeech, BGM nhỏ.

SCENES (2026-07-10): ảnh minh họa theo nhịp truyện đè lên nền ambient.
Config `03_SCRIPTS/<stem>_SCENES.json` = [{"match": "...", "img": "scene_01.jpg"}]
— match là substring của MỘT dòng TTS (mốc thời gian lấy từ timeline),
ảnh nằm ở `06_VIDEO/<stem>/scenes/`. Ảnh hiện từ mốc đó tới cảnh kế
(fade in/out), nền ambient vẫn lộ quanh viền. Thiếu file ảnh → cảnh đó
bỏ qua (chỉ ambient) — render vẫn chạy, khỏi chờ đủ ảnh.
Tái dùng render_audio_timeline / write_srt / SUB_STYLES / mix_bgm của video_render.
"""
import sys, io, argparse, json, subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEALTH_TOOLS = Path(__file__).resolve().parents[2] / "youtube-jp-health/tools"
sys.path.insert(0, str(HEALTH_TOOLS))
import video_render as VR   # noqa: E402

W, H, FPS = 1920, 1080, 30


def pick_bg(proj, stem, explicit=None):
    """LUẬT NỀN (user chốt 2026-07-09): mỗi video MỘT CLIP KHÁC NHAU — clip đã
    dùng cho video trước thì KHÔNG BAO GIỜ dùng lại.
    - Video đã có trong USAGE.log → giữ nguyên clip của nó (re-render/--reuse).
    - Video mới → chọn clip CHƯA TỪNG dùng trong _bg (file mới tải trước).
    - Hết clip chưa dùng → DỪNG, yêu cầu tải clip mới bằng tools/fetch_bg.py.
    - --bg truyền tay vẫn thắng (cảnh báo nếu clip đó đã dùng) + vẫn ghi log."""
    bg_dir = proj / "06_VIDEO" / "_bg"
    log = bg_dir / "USAGE.log"
    entries = []
    if log.exists():
        for ln in log.read_text(encoding="utf-8").splitlines():
            if "\t" in ln:
                entries.append(tuple(ln.split("\t", 1)))
    logged = dict(entries)
    used = {c for _, c in entries}

    if explicit:
        clip = Path(explicit).resolve()
        if not clip.exists():
            raise SystemExit(f"[LỖI] Không thấy clip nền: {clip}")
        if clip.name in used and logged.get(stem) != clip.name:
            print(f"⚠️ CẢNH BÁO: {clip.name} ĐÃ dùng cho video khác — luật kênh là mỗi video 1 clip khác nhau.")
        print(f"Nền: {clip.name} (chỉ định bằng --bg)")
    elif stem in logged and (bg_dir / logged[stem]).exists():
        clip = bg_dir / logged[stem]
        print(f"Nền: {clip.name} (giữ theo USAGE.log — clip riêng của video này)")
    else:
        fresh = sorted((p for p in bg_dir.glob("*.mp4") if p.name not in used),
                       key=lambda p: p.stat().st_mtime, reverse=True)
        if not fresh:
            raise SystemExit(
                "[LỖI] Hết clip nền CHƯA DÙNG trong 06_VIDEO/_bg — luật kênh: mỗi video 1 clip khác nhau.\n"
                "  → Tải clip mới: python tools/fetch_bg.py \"<query khác: waterfall forest / mountain stream / rain window...>\"\n"
                "  rồi chạy render lại (nhớ ghi nguồn vào _bg/SOURCES.md).")
        clip = fresh[0]
        print(f"Nền: {clip.name} (clip mới chưa dùng — còn lại {len(fresh) - 1} clip chưa dùng trong _bg)")

    if clip.parent.resolve() == bg_dir.resolve() and logged.get(stem) != clip.name:
        with log.open("a", encoding="utf-8") as f:
            f.write(f"{stem}\t{clip.name}\n")
    return clip


def prep_scene_image(src, dest):
    """Ảnh gen thô → canvas RGBA 1920x1080 trong suốt: fit ~76% chiều cao,
    hơi dồn lên trên (chừa đáy cho phụ đề), bo góc + viền ấm mảnh + bóng đổ."""
    from PIL import Image, ImageDraw, ImageFilter
    MAX_H = int(H * 0.76)
    MAX_W = int(W * 0.86)
    img = Image.open(src).convert("RGB")
    img.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
    iw, ih = img.size
    R = 26
    mask = Image.new("L", (iw, ih), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, iw, ih], R, fill=255)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = (W - iw) // 2
    y = max((H - ih) // 2 - 46, 24)  # dồn lên: đáy để phụ đề glass
    # bóng đổ mềm
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x + 10, y + 14, x + iw + 10, y + ih + 14],
                                         R, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, sh)
    canvas.paste(img, (x, y), mask)
    # viền vàng ấm mảnh
    ImageDraw.Draw(canvas).rounded_rectangle([x, y, x + iw, y + ih], R,
                                             outline=(212, 175, 55, 165), width=3)
    canvas.save(dest)


def load_scenes(scenes_json, scenes_dir, prep_dir, timeline, total):
    """Đọc SCENES json → [(png_prepped, start, end)]. Thiếu ảnh → bỏ cảnh đó."""
    cfg = json.loads(Path(scenes_json).read_text(encoding="utf-8"))
    prep_dir.mkdir(parents=True, exist_ok=True)
    marks = []
    missing = []
    for i, spec in enumerate(cfg):
        hit = next((ln for ln in timeline if spec["match"] in ln["text"]), None)
        if hit is None:
            raise SystemExit(f"[LỖI] Scene {i}: không thấy dòng chứa「{spec['match']}」")
        src = Path(scenes_dir) / spec["img"]
        if not src.exists():
            missing.append(spec["img"])
            continue
        dest = prep_dir / f"scene_{i:02d}.png"
        if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
            prep_scene_image(src, dest)
        marks.append((dest, hit["start"]))
    if missing:
        print(f"⚠️ Thiếu {len(missing)} ảnh cảnh (bỏ qua, chỉ ambient): {', '.join(missing)}")
    marks.sort(key=lambda m: m[1])
    out = []
    for k, (png, st) in enumerate(marks):
        end = marks[k + 1][1] if k + 1 < len(marks) else total
        out.append((png, st, end))
    return out


def build_video(video_dir, bg_clip, wav_name, srt_name, out_name, sub_style,
                brightness=-0.08, saturation=0.85, vignette="PI/5",
                scenes=None, limit=None):
    bg = Path(bg_clip).resolve()
    vgn = f"vignette={vignette}," if vignette else ""
    scenes = scenes or []
    FADE = 0.8
    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(bg), "-i", wav_name]
    parts = [(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},fps={FPS},"
              f"eq=brightness={brightness}:saturation={saturation},"
              f"{vgn}setsar=1[base]")]
    cur = "base"
    for k, (png, st, end) in enumerate(scenes):
        idx = 2 + k
        dur = max(end - st, FADE * 2 + 0.2)
        cmd += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(png)]
        parts.append(
            f"[{idx}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
            f"fade=t=out:st={dur - FADE:.3f}:d={FADE}:alpha=1,"
            f"setpts=PTS-STARTPTS+{st:.3f}/TB[sc{k}]")
        parts.append(f"[{cur}][sc{k}]overlay=0:0:eof_action=pass[ov{k}]")
        cur = f"ov{k}"
    parts.append(f"[{cur}]subtitles={srt_name}:force_style='{sub_style}'[vout]")
    parts.append("[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[aout]")  # chuẩn hóa loudness giọng (user chốt 2026-07-22)
    fc = ";".join(parts)
    cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k"]
    if limit:
        cmd += ["-t", f"{limit}"]
    cmd += ["-shortest", out_name]
    print(f"ffmpeg đang ghép nền lặp + {len(scenes)} ảnh cảnh + phụ đề…")
    r = subprocess.run(cmd, cwd=video_dir, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit("[LỖI] ffmpeg thất bại.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--bg", help="clip nền ambient (bỏ trống = tự chọn clip CHƯA DÙNG từ 06_VIDEO/_bg, log ở _bg/USAGE.log)")
    ap.add_argument("--engine", default="aivis", choices=list(VR.T.ENGINE_PRESETS))
    ap.add_argument("--speaker", default="morioki")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--intonation", type=float, default=1.0)
    ap.add_argument("--gap", type=float, default=0.5)
    ap.add_argument("--section-gap", type=float, default=1.1)
    ap.add_argument("--sub-style", default="glass", choices=list(VR.SUB_STYLES))
    ap.add_argument("--brightness", type=float, default=-0.08, help="eq brightness nền")
    ap.add_argument("--saturation", type=float, default=0.85, help="eq saturation nền")
    ap.add_argument("--vignette", default="PI/5", help="cường độ vignette; '' = tắt")
    ap.add_argument("--bgm")
    ap.add_argument("--bgm-gain", type=float, default=-26.0)
    ap.add_argument("--out-dir", help="thư mục output (mặc định 06_VIDEO/<stem>)")
    ap.add_argument("--out-name")
    ap.add_argument("--reuse", action="store_true", help="dùng lại voice.wav + subs.srt")
    ap.add_argument("--scenes", help="SCENES json (mặc định: 03_SCRIPTS/<stem>_SCENES.json nếu có; 'none' = tắt)")
    ap.add_argument("--scenes-dir", help="folder ảnh cảnh (mặc định: 06_VIDEO/<stem>/scenes)")
    ap.add_argument("--limit", type=float, help="chỉ render N giây đầu (test nhanh)")
    ap.add_argument("--voice-only", action="store_true",
                    help="chỉ synth voice.wav + subs.srt + timeline.json rồi dừng "
                         "(khâu 1 của pipeline mới: tiếp theo chạy scene_render.py)")
    args = ap.parse_args()

    inp = Path(args.input).resolve()
    stem = inp.stem.replace("_TTS", "")
    proj = inp.parents[1]
    video_dir = Path(args.out_dir).resolve() if args.out_dir else (proj / "06_VIDEO" / stem)
    video_dir.mkdir(parents=True, exist_ok=True)
    out_name = args.out_name or f"{stem}.mp4"
    wav_name, srt_name = "voice.wav", "subs.srt"
    bg_clip = None if args.voice_only else pick_bg(proj, stem, args.bg)

    if not args.reuse:
        timeline, total = VR.render_audio_timeline(str(inp), str(video_dir / wav_name), args)
        VR.write_srt(timeline, video_dir / srt_name)
        (video_dir / "timeline.json").write_text(
            json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Giọng: {total/60:.1f} phút | {len(timeline)} câu")

    if args.voice_only:
        print(f"--voice-only: XONG khâu synth → {video_dir / wav_name} + {video_dir / srt_name}. "
              f"Tiếp: python tools/scene_render.py {stem}")
        return
    else:
        print("reuse: bỏ qua synth, dùng voice.wav + subs.srt sẵn có")
        data = json.loads((video_dir / "timeline.json").read_text(encoding="utf-8"))
        timeline = data["lines"] if isinstance(data, dict) else data
        import wave
        with wave.open(str(video_dir / wav_name)) as w:
            total = w.getnframes() / w.getframerate()

    # SCENES: ảnh minh họa theo nhịp truyện (tùy chọn)
    scenes = []
    scenes_json = None
    if args.scenes != "none":
        scenes_json = (Path(args.scenes).resolve() if args.scenes
                       else proj / "03_SCRIPTS" / f"{stem}_SCENES.json")
        if not scenes_json.exists():
            scenes_json = None
    if scenes_json:
        scenes_dir = (Path(args.scenes_dir).resolve() if args.scenes_dir
                      else video_dir / "scenes")
        scenes = load_scenes(scenes_json, scenes_dir, video_dir / "scenes_prep",
                             timeline, total)
        print(f"Scenes: {len(scenes)} ảnh cảnh (config {scenes_json.name})")

    build_video(video_dir, bg_clip, wav_name, srt_name, out_name, VR.SUB_STYLES[args.sub_style],
                brightness=args.brightness, saturation=args.saturation, vignette=args.vignette,
                scenes=scenes, limit=args.limit)
    if args.bgm:
        import wave
        with wave.open(str(video_dir / wav_name)) as w:
            total = w.getnframes() / w.getframerate()
        VR.mix_bgm(video_dir, out_name, Path(args.bgm).resolve(), total, args.bgm_gain)
    print(f"\nXONG -> {video_dir / out_name}")


if __name__ == "__main__":
    main()
