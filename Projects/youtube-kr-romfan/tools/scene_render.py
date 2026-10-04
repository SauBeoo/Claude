# -*- coding: utf-8 -*-
"""scene_render.py — dựng video kênh youtube-kr-romfan (사우 오디오).

Visual = N cảnh nền ĐỘNG luân phiên (mặc định ~22 cảnh/1h, chia đều theo thời
lượng voice), mỗi cảnh 1 clip cozy từ 04_VIDEO/_bg lặp đủ đoạn của nó, fade
in/out mềm ở ranh giới — chống flag "nền loop tĩnh + giọng AI" (inauthentic
content 07/2025). Phụ đề Hàn sync từng câu + BGM nhỏ (-40dB chuẩn hệ thống).

Input: output của tools/azure_tts.py (03_VOICE/<slug>/{voice.wav, subs.srt}).

Usage:
    python tools/scene_render.py 01_slug                        # video full, ~22 cảnh/h
    python tools/scene_render.py 01_slug --scenes 3 --suffix _test   # test ngắn
    python tools/scene_render.py 01_slug --bgm 04_VIDEO/bgm/Heartwarming.mp3 --bgm-gain -40

Clip được xáo trộn deterministic theo slug (mỗi video một thứ tự cảnh khác
nhau); nếu số clip trong _bg < số cảnh thì clip được dùng lại vòng tròn —
tải thêm bằng tools/fetch_bg.py để đủ 20-25 clip khác nhau cho video full.
Output: 04_VIDEO/<slug>/<slug><suffix>.mp4
"""
import argparse
import hashlib
import random
import subprocess
import sys
import wave
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
W, H, FPS = 1920, 1080, 30
FADE = 0.8
SUB_STYLE = ("FontName=Malgun Gothic,FontSize=15,PrimaryColour=&H00FFFFFF,"
             "BorderStyle=1,Outline=2,OutlineColour=&HC8000000,Shadow=1,"
             "ShadowColour=&H96000000,MarginV=46,Alignment=2")


def run(cmd):
    r = subprocess.run(cmd, cwd=PROJ)
    if r.returncode != 0:
        sys.exit(f"[LỖI] lệnh fail: {' '.join(map(str, cmd))}")


def voice_duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="slug video (thư mục trong 03_VOICE)")
    ap.add_argument("--scenes", type=int, help="số cảnh (mặc định ~22 cảnh/giờ, min 2)")
    ap.add_argument("--bgm", default="04_VIDEO/bgm/Heartwarming.mp3")
    ap.add_argument("--bgm-gain", type=float, default=-40.0, help="dB (chuẩn hệ thống -40)")
    ap.add_argument("--no-bgm", action="store_true")
    ap.add_argument("--suffix", default="", help="hậu tố tên file output (vd _test)")
    ap.add_argument("--crf", type=int, default=21)
    ap.add_argument("--no-cta", action="store_true",
                    help="bỏ qua bước ghép hiệu ứng CTA giữa video")
    args = ap.parse_args()

    # Hạ priority BELOW_NORMAL (ffmpeg con thừa hưởng) — render nền không giành CPU
    # với UI trên máy 6 nhân; máy rảnh vẫn ăn full tốc độ. Chốt 2026-08-20.
    if sys.platform == "win32":
        try:
            import ctypes
            _k32 = ctypes.windll.kernel32
            _k32.GetCurrentProcess.restype = ctypes.c_void_p  # HANDLE 64-bit — thiếu là fail im lặng
            _h = ctypes.c_void_p(_k32.GetCurrentProcess())
            if _k32.SetPriorityClass(_h, 0x00004000):
                print("priority: BELOW_NORMAL (render nhường CPU cho UI)")
        except Exception:
            pass

    voice_dir = PROJ / "03_VOICE" / args.slug
    voice = voice_dir / "voice.wav"
    subs = voice_dir / "subs.srt"
    if not voice.exists():
        sys.exit(f"[LỖI] chưa có {voice} — chạy tools/azure_tts.py trước")
    total = voice_duration(voice)

    n = args.scenes or max(2, round(total / 3600 * 22))
    seg_dur = total / n

    bg_dir = PROJ / "04_VIDEO" / "_bg"
    clips = sorted(bg_dir.glob("*.mp4"))
    if not clips:
        sys.exit("[LỖI] 04_VIDEO/_bg trống — tải clip: python tools/fetch_bg.py")
    # chống trùng visual GIỮA các video (inauthentic content 07/2025):
    # ưu tiên clip CHƯA dùng ở video trước (theo _bg/USAGE.log), thiếu mới tái dùng
    usage_log = bg_dir / "USAGE.log"
    used_names = set()
    if usage_log.exists():
        for line in usage_log.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split("\t")
            if len(parts) >= 3 and parts[1] != args.slug:
                used_names.update(parts[2].split(","))
    seed = int(hashlib.md5(args.slug.encode()).hexdigest(), 16)
    rng = random.Random(seed)
    fresh = [c for c in clips if c.name not in used_names]
    reused = [c for c in clips if c.name in used_names]
    rng.shuffle(fresh)
    rng.shuffle(reused)
    order = fresh + reused
    picked = [order[i % len(order)] for i in range(n)]
    if n > len(fresh):
        print(f"⚠️ chỉ {len(fresh)}/{n} clip chưa dùng ở video trước — "
              f"{n - len(fresh)} cảnh phải tái dùng clip cũ; "
              f"chạy tools/fetch_bg.py với query MỚI trước video sau")

    out_dir = PROJ / "04_VIDEO" / args.slug
    tmp = out_dir / "_segs"
    tmp.mkdir(parents=True, exist_ok=True)
    print(f"voice {total:.1f}s → {n} cảnh × {seg_dur:.1f}s")

    # 1) render từng cảnh (loop clip đủ độ dài đoạn, tối nhẹ + vignette + fade)
    concat_lines = []
    for i, clip in enumerate(picked):
        # ⚠️ Tên segment mang DANH TÍNH CLIP, không chỉ index cảnh (vá 2026-07-29).
        # Trước: seg_000.mp4 theo index → pool _bg đổi (tải thêm/loại clip) làm `picked`
        # đổi hẳn, nhưng seg cũ vẫn tồn tại → skip → video ghép clip CŨ trong khi
        # USAGE.log ghi tên clip MỚI (sổ sách lệch hẳn với thứ trên màn hình).
        _st = clip.stat()
        _key = hashlib.md5(
            f"{clip.name}|{int(_st.st_mtime)}|{_st.st_size}|{seg_dur:.3f}|{args.crf}".encode()
        ).hexdigest()[:10]
        seg = tmp / f"seg_{i:03d}_{_key}.mp4"
        concat_lines.append(f"file '_segs/{seg.name}'")
        if seg.exists():
            continue
        d = seg_dur
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},fps={FPS},eq=brightness=-0.10:saturation=0.85,"
              f"vignette=PI/4.5,"
              f"fade=t=in:st=0:d={FADE},fade=t=out:st={max(d - FADE, 0):.3f}:d={FADE}")
        run(["ffmpeg", "-y", "-stream_loop", "-1",
             "-i", str(clip), "-t", f"{d:.3f}", "-an",
             "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
             "-crf", str(args.crf), "-pix_fmt", "yuv420p",
             str(seg), "-loglevel", "error"])
        print(f"  cảnh {i + 1}/{n}: {clip.name}")

    (out_dir / "concat.txt").write_text("\n".join(concat_lines), encoding="utf-8")

    # 1.5) Lớp FX (fx_mix.py — port từ chouhen, user duyệt 2026-07-22): có
    # 02_SCRIPTS/<slug>_FX.json → phụ đề màu nhân vật + quote card + SFX + BGM động.
    # Không có file → chạy y như cũ.
    sys.path.insert(0, str(PROJ / "tools"))
    import fx_mix
    plan = fx_mix.resolve_plan(args.slug, args.bgm_gain)
    cards = []
    if plan:
        fx_mix.colorize_srt(plan, subs, voice_dir / "subs_fx.srt",
                            fx_mix.load_timeline(args.slug))
        subs = voice_dir / "subs_fx.srt"
        cards = fx_mix.render_cards(plan, out_dir)
        print(f"FX: {len(plan['sfx'])} SFX | {len(cards)} card | "
              f"{len(plan['lines'])} câu thoại tô màu")

    # 2) nối cảnh + phụ đề (+card) + voice + BGM (+SFX) (1 pass cuối)
    out = out_dir / f"{args.slug}{args.suffix}.mp4"
    subs_rel = subs.relative_to(PROJ).as_posix()
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
           "-i", str(out_dir / "concat.txt"), "-i", str(voice)]
    LN = "loudnorm=I=-16:TP=-1.5:LRA=11"  # chuẩn hóa loudness giọng -16 LUFS (fix voice bé, user chốt 2026-07-22)
    idx = 2
    bgm_idx = None
    if not args.no_bgm:
        bgm = PROJ / args.bgm
        if not bgm.exists():
            sys.exit(f"[LỖI] không thấy BGM {bgm}")
        cmd += ["-stream_loop", "-1", "-i", str(bgm)]
        bgm_idx = idx
        idx += 1
    sfx_list = plan["sfx"] if plan else []
    sfx_base = idx
    for f, _, _ in sfx_list:
        cmd += ["-i", str(f)]
        idx += 1
    card_base = idx
    FD = 0.35
    for png, a, b in cards:
        cmd += ["-loop", "1", "-t", f"{b - a:.3f}", "-i", str(png)]
        idx += 1
    # video: phụ đề rồi đè card
    parts = [f"[0:v]subtitles={subs_rel}:force_style='{SUB_STYLE}'[vs]"]
    last = "vs"
    for j, (png, a, b) in enumerate(cards):
        parts.append(f"[{card_base + j}:v]format=rgba,fade=t=in:st=0:d={FD}:alpha=1,"
                     f"fade=t=out:st={b - a - FD:.3f}:d={FD}:alpha=1,"
                     f"setpts=PTS-STARTPTS+{a:.3f}/TB[kc{j}]")
        parts.append(f"[{last}][kc{j}]overlay=0:0:eof_action=pass[vk{j}]")
        last = f"vk{j}"
    parts.append(f"[{last}]null[v]")
    # audio: voice + BGM (curve khi có FX) + SFX
    parts.append(f"[1:a]{LN}[voc]")
    mix = "[voc]"
    n_mix = 1
    if bgm_idx is not None:
        if plan:
            parts.append(f"[{bgm_idx}:a]volume=volume='{plan['vol_expr']}':eval=frame[bg]")
        else:
            parts.append(f"[{bgm_idx}:a]volume={args.bgm_gain}dB[bg]")
        mix += "[bg]"
        n_mix += 1
    for k, (f, t, g) in enumerate(sfx_list):
        ms = int(t * 1000)
        parts.append(f"[{sfx_base + k}:a]adelay={ms}|{ms},volume={g}dB[s{k}]")
        mix += f"[s{k}]"
        n_mix += 1
    tail = ",alimiter=limit=0.95" if plan else ""
    parts.append(f"{mix}amix=inputs={n_mix}:duration=first:normalize=0{tail}[a]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[v]", "-map", "[a]"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", str(args.crf),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(out), "-loglevel", "error"]
    run(cmd)
    # CTA overlay giữa video (rule E:\Claude\.claude\rules\cta-midvideo.md §5) — tự tìm
    # câu CTA trong subs.srt, chỉ re-encode đoạn đó; chưa có câu CTA → skip êm (rc=2)
    if not args.no_cta:
        cta = Path(r"E:\Claude\Projects\youtube-jp-chouhen\tools\cta_inject.py")
        rc = subprocess.run([sys.executable, str(cta), str(out), "--srt", str(subs),
                             "--lang", "kr", "--in-place", "--crf", str(args.crf)]).returncode
        if rc == 2:
            print("⚠️ script chưa có câu CTA giữa (rule cta-midvideo.md) — video giữ nguyên")
        elif rc != 0:
            print(f"⚠️ cta_inject lỗi — video gốc giữ nguyên, chạy tay: "
                  f"python {cta} {out} --lang kr --in-place")
    mb = out.stat().st_size / 1e6
    if not args.suffix:  # chỉ bản chính thức mới tính là "đã dùng" clip
        import datetime
        names = ",".join(c.name for c in picked)
        with open(usage_log, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M}\t{args.slug}\t{names}\n")
    print(f"DONE {out} ({mb:.0f} MB, {total/60:.1f} phút, {n} cảnh)")


if __name__ == "__main__":
    main()
