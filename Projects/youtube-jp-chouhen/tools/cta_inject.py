# -*- coding: utf-8 -*-
"""
cta_inject.py — ghép hiệu ứng CTA (like/share/comment/subscribe + SFX) vào video ĐÃ render,
KHÔNG re-encode cả bài: tự tìm timestamp câu CTA trong subs.srt → chỉ encode lại đoạn
[keyframe trước CTA .. keyframe sau CTA] với overlay + tiếng, 2 phần còn lại concat -c copy.

Usage:
  python cta_inject.py <video.mp4> [--srt subs.srt] [--lang jp|kr|vn] [--match "..."]
                       [--dur 8] [--sfx-gain -10] [--pos 70:H-h-170] [--in-place] [--crf 21]

- --srt mặc định: file subs.srt cùng thư mục với video.
- Tự phát hiện câu CTA theo PATTERNS[lang] (câu canonical .claude/rules/cta-midvideo.md);
  --match để chỉ định chuỗi khác. Không thấy CTA → exit code 2 (pipeline coi là skip).
- --in-place: thay thẳng file gốc; mặc định xuất <tên>_cta.mp4.
- Frames + SFX tự sinh vào <thư mục video>/_cta/ (gen_cta_overlay.py + gen_cta_sfx.py).
Rule gốc: .claude/rules/cta-midvideo.md
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gen_cta_overlay import SFX_EVENTS  # noqa: E402

# chuỗi nhận diện câu CTA trong srt (khớp câu canonical từng kênh)
PATTERNS = {
    "jp": ["ご感想やご要望", "高評価とシェア", "高評価と、同じ世代", "高評価と、この動画",
           "高評価と、同じように知りたい",
           # nenkin (年金と老後のお金研究室): canonical 2.4b cta-midvideo.md — pattern = câu MỞ
           # CTA nằm trọn 1 cue (câu 高評価と、同じように年金が… bị SUB_MAXLEN cắt cue tại 、)
           "ここで、ひとつだけお願いです",
           # co-dai (古代の秘訣): cùng bệnh với nenkin, lộ ra 2026-08-03 khi hạ
           # SUB_MAXLEN theo sub_size 26 (cue còn 27 ký) → "高評価と、同じように知りたい"
           # bị cắt làm đôi giữa 2 cue nên pattern dài không khớp nữa. Dùng câu MỞ.
           # ⚠️ Luật chung: pattern phải NGẮN hơn cue ngắn nhất mà kênh có thể sinh ra
           # (SUB_MAXLEN nhỏ nhất hiện tại = 24 ký ở sub_size ≥30).
           "この知恵に価値を感じて",
           # shokutaku (60代からの食卓): câu canonical dùng 良いね, KHÔNG có 高評価
           "良いねと、", "そっと分けてあげて"],
    "kr": ["좋아요와", "공유까지 부탁", "댓글로 꼭"],
    "vn": ["một lượt thích", "lượt chia sẻ"],
}
LEAD_IN = 0.2   # overlay vào sớm hơn câu CTA (giây)
PAD = 1.5       # đệm quanh đoạn re-encode trước khi bắt keyframe


def _probe_fps(video, default=30):
    """fps thuc cua file (r_frame_rate). Loi/khong doc duoc -> default."""
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0",
                            str(video)], capture_output=True, text=True).stdout.strip()
        num, _, den = r.partition("/")
        f = float(num) / float(den or 1)
        return int(round(f)) if 1 <= f <= 240 else default
    except Exception:
        return default


def ffprobe_json(args_):
    r = subprocess.run(["ffprobe", "-v", "error", "-of", "json"] + args_,
                       capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


def parse_srt_start(srt, patterns):
    blocks = [b for b in srt.read_text(encoding="utf-8").strip().split("\n\n") if b.strip()]
    for blk in blocks:
        lines = blk.splitlines()
        if len(lines) < 3:
            continue
        text = " ".join(lines[2:])
        if any(p in text for p in patterns):
            ts = lines[1].split("-->")[0].strip()
            h, m, rest = ts.split(":")
            s, ms = rest.split(",")
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    return None


def keyframes_near(video, t0, t1):
    """Trả (K0, K1): keyframe cuối ≤ t0 và keyframe đầu ≥ t1 (scan cục bộ, nhanh)."""
    def kfs(around, span):
        data = ffprobe_json(["-select_streams", "v:0", "-skip_frame", "nokey",
                             "-show_entries", "frame=pts_time",
                             "-read_intervals", f"{max(0, around):.3f}%+{span:.3f}",
                             str(video)])
        return [float(f["pts_time"]) for f in data.get("frames", []) if "pts_time" in f]
    k_before = [k for k in kfs(t0 - 30, 31) if k <= t0]
    K0 = max(k_before) if k_before else 0.0
    k_after = [k for k in kfs(t1, 35) if k >= t1]
    K1 = min(k_after) if k_after else None  # None = tới hết video
    return K0, K1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--srt")
    ap.add_argument("--lang", default="jp", choices=list(PATTERNS))
    ap.add_argument("--match")
    ap.add_argument("--dur", type=float, default=8.0)
    ap.add_argument("--sfx-gain", type=float, default=-10.0)
    ap.add_argument("--pos", default="70:H-h-170")
    ap.add_argument("--crf", type=int, default=21)
    ap.add_argument("--in-place", action="store_true")
    ap.add_argument("--keep-tmp", action="store_true",
                    help="giữ thư mục làm việc _cta/; mặc định tự xoá sau khi ghép xong")
    a = ap.parse_args()

    video = Path(a.video).resolve()
    if not video.exists():
        sys.exit(f"[LỖI] không thấy {video}")
    srt = Path(a.srt).resolve() if a.srt else video.parent / "subs.srt"
    if not srt.exists():
        sys.exit(f"[LỖI] không thấy srt {srt}")

    patterns = [a.match] if a.match else PATTERNS[a.lang]
    cta_t = parse_srt_start(srt, patterns)
    if cta_t is None:
        print(f"[SKIP] không thấy câu CTA trong {srt.name} (patterns {a.lang})")
        sys.exit(2)
    start = max(0.0, cta_t - LEAD_IN)
    print(f"CTA @ {cta_t:.2f}s → overlay {start:.2f}s..{start + a.dur:.2f}s")

    # ---- keyframes bao quanh đoạn cần encode ----
    K0, K1 = keyframes_near(video, start - PAD, start + a.dur + PAD)
    print(f"re-encode đoạn [{K0:.2f}s .. {'%.2f s' % K1 if K1 else 'EOF'}], còn lại copy")

    # ---- sinh frames + sfx ----
    work = video.parent / "_cta"
    py = sys.executable
    subprocess.run([py, str(HERE / "gen_cta_overlay.py"), "--out", str(work / "frames"),
                    "--lang", a.lang, "--dur", str(a.dur)], check=True)
    subprocess.run([py, str(HERE / "gen_cta_sfx.py"), "--out", str(work / "sfx")],
                   check=True)

    # ---- audio gốc: lấy sample_rate/channels để encode khớp ----
    ast = ffprobe_json(["-select_streams", "a:0", "-show_entries",
                        "stream=sample_rate,channels", str(video)])["streams"][0]
    ar, ac = ast.get("sample_rate", "44100"), str(ast.get("channels", 2))

    # ---- part MID (re-encode overlay + sfx) ----
    rel = start - K0
    mid = work / "mid.mp4"
    fc_v = f"[0:v][1:v]overlay={a.pos}:eof_action=pass[v]"
    sfx_in, fc_a, mixes = [], [], []
    for idx, (name, ev_t) in enumerate(SFX_EVENTS):
        sfx_in += ["-i", str(work / "sfx" / f"{name}.wav")]
        d_ms = int((rel + ev_t) * 1000)
        fc_a.append(f"[{2 + idx}:a]volume={a.sfx_gain}dB,adelay={d_ms}:all=1[s{idx}]")
        mixes.append(f"[s{idx}]")
    fc = (fc_v + ";" + ";".join(fc_a) +
          f";[0:a]{''.join(mixes)}amix=inputs={1 + len(mixes)}:duration=first:"
          f"normalize=0[a]")
    # 🔴 fps cua overlay PHAI theo fps GOC cua video (2026-09-06). Truoc day hard-code 30:
    # video 24fps (kenh showa dung clip AI Flow/Veo) thi 240 frame overlay bi tieu thu o
    # 24fps => hoat canh CTA chay CHAM 25% va nhip frame trong cua so re-encode lech voi
    # phan con lai cua video. Cung benh voi FPS=30 cua video_render.py._seg_chain.
    src_fps = _probe_fps(video)
    cmd = ["ffmpeg", "-y", "-ss", f"{K0:.3f}", "-i", str(video),
           "-framerate", str(src_fps), "-itsoffset", f"{rel:.3f}",
           "-i", str(work / "frames" / "f_%04d.png")] + sfx_in
    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]"]
    if K1 is not None:
        cmd += ["-t", f"{K1 - K0:.3f}"]  # output option: cắt mid đúng tới keyframe K1
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", str(a.crf),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", ar, "-ac", ac,
            str(mid), "-loglevel", "error"]
    subprocess.run(cmd, check=True)

    # ---- part A/C (copy) + concat ----
    parts = []
    if K0 > 0.05:
        pa = work / "partA.mp4"
        subprocess.run(["ffmpeg", "-y", "-i", str(video), "-to", f"{K0:.3f}",
                        "-c", "copy", str(pa), "-loglevel", "error"], check=True)
        parts.append(pa)
    parts.append(mid)
    if K1 is not None:
        pc = work / "partC.mp4"
        subprocess.run(["ffmpeg", "-y", "-ss", f"{K1:.3f}", "-i", str(video),
                        "-c", "copy", str(pc), "-loglevel", "error"], check=True)
        parts.append(pc)
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    out = video if a.in_place else video.with_name(video.stem + "_cta.mp4")
    tmp = work / "out.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(tmp), "-loglevel", "error"], check=True)
    os.replace(tmp, out)
    print(f"DONE CTA inject → {out} ({out.stat().st_size / 1e6:.0f} MB)")
    if not a.keep_tmp:
        import shutil
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
