# -*- coding: utf-8 -*-
"""scene_render.py v2 — dựng video kênh youtube-jp-chouhen (真夜中の朗読便).

MƯỢT HƠN (user chốt 2026-07-14, thay v1 cắt cứng + loop giật):
- NHIỀU cảnh hơn: mặc định ~38 cảnh/giờ (v1 chỉ 22) → mỗi clip hiện ngắn, đỡ lặp.
- BOOMERANG: mỗi clip chạy xuôi→ngược nối liền → điểm loop biến mất, không còn "khựng"
  khi clip nhảy về đầu (bm dựng từ 8s đầu clip để chặn RAM khi reverse).
- CROSSFADE (xfade): chuyển cảnh HÒA TAN ~0.9s thay vì fade ra đen → mượt như phim.
- Vẫn 1 clip/cảnh KHÔNG trùng video khác (USAGE.log), phụ đề glass, BGM -40dB.

CHỐNG KILL RENDER DÀI (máy tự kill ffmpeg chạy >~24' — sự cố 2026-07-14):
- Chia assembly làm 2 NỬA (mỗi nửa ~12' encode) + RESUMABLE (skip file đã xong).
- Chạy theo STAGE để mỗi ffmpeg ngắn:
    python tools/scene_render.py <slug> --stage segs   # dựng boomerang tất cả clip + _render_plan.json
    python tools/scene_render.py <slug> --stage A       # ghép nửa A (xfade + phụ đề) -> vA.mp4
    python tools/scene_render.py <slug> --stage B       # ghép nửa B -> vB.mp4
    python tools/scene_render.py <slug> --stage final    # audio(voice+BGM) + concat vA+vB + mux
  (bỏ --stage = chạy tuần tự cả 4 stage; máy có kill thì chạy từng stage qua wrapper .cmd detached)

Input: 06_VIDEO/<slug>/{voice.wav, subs.srt} (output khâu synth ambient_render --voice-only).
"""
import argparse
import datetime
import hashlib
import json
import random
import subprocess
import sys
import wave
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
W, H, FPS = 1920, 1080, 30
XF = 0.9            # crossfade (giây) giữa 2 cảnh
BM_SRC = 8.0       # số giây đầu clip dùng dựng boomerang (chặn RAM khi reverse)
SCENES_PER_HR = 38
SUB_STYLE = ("FontName=Yu Gothic,FontSize=17,Bold=1,PrimaryColour=&H00FFFFFF,"
             "BackColour=&H90000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=16")


def run(cmd):
    r = subprocess.run(cmd, cwd=PROJ)
    if r.returncode != 0:
        sys.exit(f"[LỖI] lệnh fail: {' '.join(map(str, cmd))}")


def voice_duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def read_usage(usage_log, slug):
    used = set()
    if not usage_log.exists():
        return used
    for line in usage_log.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split("\t")
        if len(parts) == 2 and parts[0] != slug:
            used.add(parts[1])
        elif len(parts) >= 3 and parts[1] != slug:
            used.update(parts[2].split(","))
    return used


# ---------- phụ đề: tách theo mốc split ----------

def _parse_ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def _fmt_ts(t):
    if t < 0:
        t = 0
    h = int(t // 3600); t -= h * 3600
    m = int(t // 60); t -= m * 60
    s = int(t); ms = round((t - s) * 1000)
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_srt(src, split_t, out_a, out_b):
    blocks = [b for b in src.read_text(encoding="utf-8").strip().split("\n\n") if b.strip()]
    a, b, ia, ib = [], [], 0, 0
    for blk in blocks:
        lines = blk.splitlines()
        st, en = [_parse_ts(x.strip()) for x in lines[1].split("-->")]
        text = "\n".join(lines[2:])
        if st < split_t:
            ia += 1
            a.append(f"{ia}\n{_fmt_ts(st)} --> {_fmt_ts(min(en, split_t))}\n{text}")
        else:
            ib += 1
            b.append(f"{ib}\n{_fmt_ts(st - split_t)} --> {_fmt_ts(en - split_t)}\n{text}")
    out_a.write_text("\n\n".join(a) + "\n", encoding="utf-8")
    out_b.write_text("\n\n".join(b) + "\n", encoding="utf-8")
    return ia, ib


# ---------- stages ----------

def stage_segs(vdir, slug, crf, n_override):
    voice = vdir / "voice.wav"
    subs = vdir / "subs.srt"
    if not voice.exists() or not subs.exists():
        sys.exit(f"[LỖI] thiếu {voice} / {subs} — chạy khâu synth (ambient_render --voice-only) trước")
    # Lớp FX (fx_mix.py, user duyệt 2026-07-22): có <slug>_FX.json → phụ đề màu theo
    # nhân vật (subs_fx.srt) + xuất card PNG + _fx_plan.json cho stage A/B/final.
    import fx_mix
    plan = fx_mix.resolve_plan(slug, vdir)
    if plan:
        fx_mix.colorize_srt(plan, subs, vdir / "subs_fx.srt",
                            fx_mix.load_timeline(vdir))
        subs = vdir / "subs_fx.srt"
        cards = fx_mix.render_cards(plan, vdir)
        (vdir / "_fx_plan.json").write_text(json.dumps(
            {"cards": [[str(p), a, b] for p, a, b in cards],
             "vol_expr": plan["vol_expr"],
             "sfx": [[str(f), t, g] for f, t, g in plan["sfx"]]},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"FX: {len(plan['sfx'])} SFX | {len(cards)} card | "
              f"{len(plan['lines'])} câu thoại tô màu")
    total = voice_duration(voice)
    n = n_override or max(2, round(total / 3600 * SCENES_PER_HR))
    # L: dài mỗi cảnh; tổng timeline = N*L - (N-2)*XF = total (mất 1 xfade ở mối nối 2 nửa)
    L = (total + (n - 2) * XF) / n

    bg_dir = PROJ / "06_VIDEO" / "_bg"
    # Clip đã bị loại khi duyệt mắt (người nhận diện được / brand / màu phá mood) nằm ở
    # _bg/rejected/. BẮT BUỘC lọc ra: fetch_bg hardlink lại từ kho chung nên tên đã loại
    # VẪN xuất hiện trong _bg (bug phát hiện 2026-07-26 ở video 09 — old-wooden-s_8657331
    # là clip 2 người áo blouse trắng, từng bị loại, quay lại và lọt vào bản render).
    rejected = {p.name for p in (bg_dir / "rejected").glob("*.mp4")}
    clips = sorted(p for p in bg_dir.glob("*.mp4") if p.name not in rejected)
    if rejected:
        print(f"bỏ qua {len(rejected)} clip trong _bg/rejected/")
    if not clips:
        sys.exit("[LỖI] 06_VIDEO/_bg trống — tải clip: python tools/fetch_bg.py")
    used = read_usage(bg_dir / "USAGE.log", slug)
    rng = random.Random(int(hashlib.md5(slug.encode()).hexdigest(), 16))
    fresh = [c for c in clips if c.name not in used]
    reused = [c for c in clips if c.name in used]
    rng.shuffle(fresh); rng.shuffle(reused)
    order = fresh + reused
    picks = [order[i % len(order)].name for i in range(n)]
    if n > len(fresh):
        print(f"⚠️ chỉ {len(fresh)}/{n} clip chưa dùng — {n - len(fresh)} cảnh tái dùng; "
              f"chạy fetch_bg với query MỚI trước video sau")

    bm_dir = vdir / "_bm"
    bm_dir.mkdir(parents=True, exist_ok=True)
    print(f"voice {total:.1f}s → {n} cảnh × {L:.1f}s (xfade {XF}s, boomerang)")
    for i, name in enumerate(picks):
        bm = bm_dir / f"bm_{name}"
        if bm.exists():
            continue
        clip = bg_dir / name
        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"fps={FPS},eq=brightness=-0.10:saturation=0.85,vignette=PI/4.5,"
              f"split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1,setpts=PTS-STARTPTS[v]")
        run(["ffmpeg", "-y", "-t", f"{BM_SRC}", "-i", str(clip),
             "-filter_complex", vf, "-map", "[v]", "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
             "-pix_fmt", "yuv420p", str(bm), "-loglevel", "error"])
        print(f"  boomerang {i + 1}/{n}: {name}")

    split_index = n // 2
    durA = split_index * L - (split_index - 1) * XF
    plan = {"n": n, "L": L, "XF": XF, "picks": picks,
            "split_index": split_index, "durA": durA, "total": total, "crf": crf}
    (vdir / "_render_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
    # tách phụ đề theo durA
    ia, ib = split_srt(subs, durA, vdir / "subsA.srt", vdir / "subsB.srt")
    print(f"segs XONG: {n} boomerang | split @ {durA:.1f}s | subsA={ia} subsB={ib}")


def _xfade_filter(m, L, xf, sub_rel, cards=None, card_base_idx=0):
    """Chuỗi xfade cho m input đã chuẩn hoá + burn phụ đề (+ quote card FX). Trả filter_complex string."""
    parts = [f"[{k}:v]fps={FPS},format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[v{k}]"
             for k in range(m)]
    if m == 1:
        last = "v0"
    else:
        prev = "v0"
        for k in range(1, m):
            out = f"x{k}" if k < m - 1 else "vc"
            parts.append(f"[{prev}][v{k}]xfade=transition=fade:duration={xf}:"
                         f"offset={k * (L - xf):.3f}[{out}]")
            prev = out
        last = "vc"
    parts.append(f"[{last}]subtitles={sub_rel}:force_style='{SUB_STYLE}'[vs]")
    last = "vs"
    FD = 0.35
    for j, (png, t0, t1) in enumerate(cards or []):
        idx = card_base_idx + j
        parts.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d={FD}:alpha=1,"
                     f"fade=t=out:st={t1 - t0 - FD:.3f}:d={FD}:alpha=1,"
                     f"setpts=PTS-STARTPTS+{t0:.3f}/TB[kc{j}]")
        parts.append(f"[{last}][kc{j}]overlay=0:0:eof_action=pass[vk{j}]")
        last = f"vk{j}"
    parts.append(f"[{last}]null[v]")
    return ";".join(parts)


def stage_half(vdir, which, crf):
    plan = json.loads((vdir / "_render_plan.json").read_text(encoding="utf-8"))
    n, L, split_index = plan["n"], plan["L"], plan["split_index"]
    picks = plan["picks"]
    durA = plan["durA"]
    bm_dir = vdir / "_bm"
    if which == "A":
        seg_names = picks[:split_index]
        sub_rel = (vdir / "subsA.srt").relative_to(PROJ).as_posix()
        out = vdir / "vA.mp4"
        t_off, t_end = 0.0, durA
    else:
        seg_names = picks[split_index:]
        sub_rel = (vdir / "subsB.srt").relative_to(PROJ).as_posix()
        out = vdir / "vB.mp4"
        t_off, t_end = durA, plan["total"] + 60
    # quote card FX rơi vào nửa này (thời gian đổi về gốc của nửa)
    cards = []
    fx_plan = vdir / "_fx_plan.json"
    if fx_plan.exists():
        fxp = json.loads(fx_plan.read_text(encoding="utf-8"))
        cards = [(Path(p), a - t_off, b - t_off) for p, a, b in fxp.get("cards", [])
                 if t_off <= a < t_end]
    m = len(seg_names)
    cmd = ["ffmpeg", "-y"]
    for name in seg_names:
        cmd += ["-stream_loop", "-1", "-t", f"{L:.3f}", "-i", str(bm_dir / f"bm_{name}")]
    for png, a, b in cards:
        cmd += ["-loop", "1", "-t", f"{b - a:.3f}", "-i", str(png)]
    cmd += ["-filter_complex", _xfade_filter(m, L, XF, sub_rel, cards, card_base_idx=m),
            "-map", "[v]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
            "-pix_fmt", "yuv420p", str(out), "-loglevel", "error"]
    dur = m * L - (m - 1) * XF
    print(f"nửa {which}: {m} cảnh xfade + {len(cards)} card → {out.name} (~{dur/60:.1f} phút)")
    run(cmd)
    print(f"nửa {which} XONG → {out}")


def cleanup_tmp(vdir):
    """Xoá file/thư mục trung gian sau khi ra final thành công (giữ resume tới lúc này).
    Giữ lại: <slug>.mp4, subs.srt, voice.wav, thumbnail*, script/json. Xoá phần render dở."""
    import shutil
    tmp_files = ["video_final.mp4", "vA.mp4", "vB.mp4", "audio.m4a", "vlist.txt",
                 "subsA.srt", "subsB.srt", "_render_plan.json"]
    tmp_dirs = ["_bm", "_cta"]
    freed = 0
    for name in tmp_files:
        p = vdir / name
        if p.exists():
            freed += p.stat().st_size
            p.unlink()
    for name in tmp_dirs:
        p = vdir / name
        if p.is_dir():
            freed += sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
            shutil.rmtree(p, ignore_errors=True)
    if freed:
        print(f"🧹 dọn file trung gian: giải phóng {freed / 1e9:.2f} GB")


def stage_final(vdir, slug, args):
    plan = json.loads((vdir / "_render_plan.json").read_text(encoding="utf-8"))
    voice = vdir / "voice.wav"
    vA, vB = vdir / "vA.mp4", vdir / "vB.mp4"
    for f in (vA, vB):
        if not f.exists():
            sys.exit(f"[LỖI] thiếu {f} — chạy stage A/B trước")
    # 1) audio: voice + BGM -40dB (hoặc no-bgm); có _fx_plan.json → BGM động + SFX (fx_mix)
    audio = vdir / "audio.m4a"
    LN = "loudnorm=I=-16:TP=-1.5:LRA=11"  # chuẩn hóa loudness giọng -16 LUFS (fix voice bé, user chốt 2026-07-22)
    fx_plan_p = vdir / "_fx_plan.json"
    if fx_plan_p.exists():
        import fx_mix
        fx_plan = fx_mix.resolve_plan(slug, vdir, args.bgm_gain)
        fx_mix.build_audio(vdir, audio, PROJ / args.bgm, args.bgm_gain, fx_plan,
                           no_bgm=args.no_bgm)
        print(f"audio FX: {len(fx_plan['sfx'])} SFX + BGM động")
    elif args.no_bgm:
        run(["ffmpeg", "-y", "-i", str(voice), "-af", LN, "-c:a", "aac", "-b:a", "192k",
             str(audio), "-loglevel", "error"])
    else:
        bgm = PROJ / args.bgm
        if not bgm.exists():
            sys.exit(f"[LỖI] không thấy BGM {bgm}")
        fc = (f"[1:a]volume={args.bgm_gain}dB[bg];"
              f"[0:a]{LN}[voc];"
              f"[voc][bg]amix=inputs=2:duration=first:normalize=0[a]")
        run(["ffmpeg", "-y", "-i", str(voice), "-stream_loop", "-1", "-i", str(bgm),
             "-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "192k",
             "-shortest", str(audio), "-loglevel", "error"])
    # 2) concat vA+vB (-c copy)
    vlist = vdir / "vlist.txt"
    vlist.write_text("file 'vA.mp4'\nfile 'vB.mp4'\n", encoding="utf-8")
    video_final = vdir / "video_final.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(vlist),
         "-c", "copy", str(video_final), "-loglevel", "error"])
    # 3) mux video + audio
    out = vdir / f"{slug}{args.suffix}.mp4"
    run(["ffmpeg", "-y", "-i", str(video_final), "-i", str(audio),
         "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest",
         str(out), "-loglevel", "error"])
    # 4) hiệu ứng CTA giữa video (rule .claude/rules/cta-midvideo.md) — tự tìm câu CTA
    #    trong subs.srt, chỉ re-encode đoạn đó; không thấy CTA → skip êm (rc=2)
    if not args.no_cta:
        r = subprocess.run([sys.executable, str(PROJ / "tools" / "cta_inject.py"),
                            str(out), "--srt", str(vdir / "subs.srt"),
                            "--lang", "jp", "--in-place", "--crf", str(args.crf)])
        if r.returncode == 2:
            print("⚠️ script chưa có câu CTA giữa (xem rule cta-midvideo.md) — video giữ nguyên")
        elif r.returncode != 0:
            print("⚠️ cta_inject lỗi — video gốc giữ nguyên, chạy tay: "
                  f"python tools/cta_inject.py {out} --in-place")
    mb = out.stat().st_size / 1e6
    if not args.suffix:
        names = ",".join(sorted(set(plan["picks"])))
        with open(PROJ / "06_VIDEO" / "_bg" / "USAGE.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M}\t{slug}\t{names}\n")
    print(f"DONE {out} ({mb:.0f} MB, {plan['total']/60:.1f} phút, {plan['n']} cảnh, "
          f"boomerang+xfade)")
    # dọn rác trung gian (chỉ khi render chính thức thành công, không phải bản _test/--suffix)
    if not args.suffix and not args.keep_tmp:
        cleanup_tmp(vdir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--stage", choices=["segs", "A", "B", "final"],
                    help="chạy 1 stage (bỏ = chạy cả 4 tuần tự)")
    ap.add_argument("--scenes", type=int, help="số cảnh (mặc định ~38/giờ)")
    ap.add_argument("--bgm", default="06_VIDEO/bgm/Anguish.mp3")
    ap.add_argument("--bgm-gain", type=float, default=-40.0)
    ap.add_argument("--no-bgm", action="store_true")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--crf", type=int, default=21)
    ap.add_argument("--no-cta", action="store_true",
                    help="bỏ qua bước ghép hiệu ứng CTA giữa video")
    ap.add_argument("--keep-tmp", action="store_true",
                    help="giữ file trung gian (_bm/_cta/vA/vB/video_final…); mặc định tự dọn")
    args = ap.parse_args()

    vdir = PROJ / "06_VIDEO" / args.slug
    if not vdir.exists():
        sys.exit(f"[LỖI] không thấy {vdir}")

    if args.stage in (None, "segs"):
        stage_segs(vdir, args.slug, args.crf, args.scenes)
    if args.stage in (None, "A"):
        stage_half(vdir, "A", args.crf)
    if args.stage in (None, "B"):
        stage_half(vdir, "B", args.crf)
    if args.stage in (None, "final"):
        stage_final(vdir, args.slug, args)


if __name__ == "__main__":
    main()
