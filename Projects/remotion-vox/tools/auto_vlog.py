# -*- coding: utf-8 -*-
"""auto_vlog.py — TỰ dựng video VLOG beat-sync kiểu CapCut (reel Edit Không Khó)
từ clip + nhạc của user. Không viết timeline tay: máy dò beat, cắt theo nhịp,
xoay vòng hiệu ứng.

  py -3 tools/auto_vlog.py --clips <folder chứa mp4/mov> --out <tên project>
      [--music nhac.mp3|.wav]   (không có -> tự synth beat 120bpm)
      [--bpm 120]               (bỏ qua bộ dò, ép BPM)
      [--seconds 15] [--size 1080x1920 | 1920x1080]
      [--title "今日はコレ"] [--endtext "EDIT xong 🎬"]
      [--stickers <folder png cutout>]   (vd vịt/doodle; không có -> bỏ qua)

Cấu trúc sinh ra (tỉ lệ theo tổng số beat, đúng công thức reel):
  A intro   ~25%: cắt mỗi beat, speed 2.0 ↔ 0.5 xen kẽ + title + sticker
  B feature ~20%: giữ 1 clip + đếm ngược 3-2-1 theo beat
  C mirror  ~20%: mặt nạ gương (lật) rồi lật lại
  D split   ~25%: 3 dải ngang wipe vào lệch 1 beat
  E outro   ~10%: tua nhanh + end text
Beat được dò bằng onset-flux + autocorrelation (numpy, không lib ngoài);
nhạc mp3/m4a decode qua ffmpeg.
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from auto_collage import ensure_sfx  # noqa: E402

FPS = 30
SR = 22050
HOP = 512


# ---------------------------------------------------------------------------
# beat detection
# ---------------------------------------------------------------------------

def decode_mono(path: Path) -> np.ndarray:
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR),
         "-f", "f32le", "-"],
        capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"[LOI] ffmpeg decode {path.name}: {r.stderr[-200:]}")
    return np.frombuffer(r.stdout, np.float32)


def onset_envelope(x: np.ndarray) -> np.ndarray:
    n = (len(x) // HOP) * HOP
    frames = x[:n].reshape(-1, HOP)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    flux = np.maximum(0.0, np.diff(rms, prepend=rms[0]))
    if flux.max() > 0:
        flux = flux / flux.max()
    return flux


def detect_beats(path: Path, forced_bpm=None):
    """-> (bpm, first_beat_sec). Autocorr 60–180bpm + quét pha."""
    x = decode_mono(path)
    env = onset_envelope(x)
    fr = SR / HOP  # env frames / sec

    if forced_bpm:
        bpm = float(forced_bpm)
    else:
        lo, hi = int(fr * 60 / 180), int(fr * 60 / 60)  # lag 180bpm..60bpm
        ac = np.correlate(env, env, mode="full")[len(env) - 1:]
        lag = lo + int(np.argmax(ac[lo:hi]))
        bpm = 60.0 * fr / lag
        # gấp đôi nếu quá chậm (autocorr hay bắt nửa nhịp)
        if bpm < 90:
            bpm *= 2

    def grid_score(bpm_try):
        period = fr * 60.0 / bpm_try
        best_off, best_score = 0.0, -1.0
        for off in np.linspace(0, period, 24, endpoint=False):
            idx = np.arange(off, len(env), period).astype(int)
            score = env[idx].mean()
            if score > best_score:
                best_score, best_off = score, off
        return best_score, best_off

    if not forced_bpm:
        # tinh chỉnh quanh ước lượng thô: BPM nào cho beat-grid khớp env nhất
        best = (grid_score(bpm)[0], bpm)
        for cand in np.arange(bpm - 4, bpm + 4.01, 0.25):
            s, _ = grid_score(cand)
            if s > best[0]:
                best = (s, cand)
        bpm = float(best[1])

    _, best_off = grid_score(bpm)
    return round(bpm, 2), best_off / fr


# ---------------------------------------------------------------------------
# clip helpers
# ---------------------------------------------------------------------------

def probe_seconds(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def video_clip(cid, asset, from_f, dur, **extra):
    base = {
        "id": cid, "kind": "video", "from": from_f, "durationInFrames": dur,
        "asset": asset, "trimStartFrames": 0, "fit": "cover", "layout": {},
        "motion": "none", "speed": 1, "mirror": False, "volume": 0,
        "fadeInFrames": 0, "wipeInFrames": 0, "wipeDir": "left", "filter": {},
    }
    base.update(extra)
    return base


def text_clip(cid, content, from_f, dur, **extra):
    base = {
        "id": cid, "kind": "text", "from": from_f, "durationInFrames": dur,
        "content": content, "preset": "tag", "color": "#FFE01B",
        "animation": "pop",
        "animationParams": {"damping": 11, "stiffness": 180, "restDeg": -2},
        "layout": {}, "fontSize": None,
    }
    base.update(extra)
    return base


def sfx_clip(cid, name, from_f, total, vol=0.45):
    return {"id": cid, "kind": "audio", "from": from_f,
            "durationInFrames": max(1, min(60, total - from_f)),
            "asset": f"sfx/{name}.wav", "volume": vol, "trimStartFrames": 0}


COUNT_COLORS = ["#FF3B30", "#FF9500", "#2EC46F"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--music", default=None)
    ap.add_argument("--bpm", type=float, default=None)
    ap.add_argument("--seconds", type=float, default=15.0)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--title", default="VLOG")
    ap.add_argument("--endtext", default="EDIT xong 🎬")
    ap.add_argument("--stickers", default=None)
    args = ap.parse_args()

    W, H = (int(v) for v in args.size.lower().split("x"))
    vertical = H >= W

    src_dir = Path(args.clips)
    clips_src = sorted(p for p in src_dir.iterdir()
                       if p.suffix.lower() in (".mp4", ".mov", ".webm", ".m4v"))
    if not clips_src:
        raise SystemExit(f"[LOI] khong co clip video trong {src_dir}")

    assets = ROOT / "public" / "projects" / args.out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    ensure_sfx()

    # ---- nhạc + beat grid ---------------------------------------------------
    if args.music:
        music_src = Path(args.music)
        music_ref = f"assets/music{music_src.suffix.lower()}"
        dst = assets / Path(music_ref).name
        if not dst.exists() or dst.stat().st_size != music_src.stat().st_size:
            shutil.copy2(music_src, dst)
        bpm, first_beat = detect_beats(music_src, args.bpm)
        music_len = probe_seconds(music_src)
    else:
        dst = assets / "music.wav"
        subprocess.run([sys.executable, str(ROOT / "tools" / "make_beat.py"),
                        str(dst), "--seconds", str(args.seconds), "--bpm", "120"],
                       check=True, capture_output=True)
        music_ref = "assets/music.wav"
        bpm, first_beat, music_len = 120.0, 0.0, args.seconds

    total_sec = min(args.seconds, music_len if music_len > 1 else args.seconds)
    B = 60.0 / bpm  # giây / beat
    # mốc beat (giây) từ first_beat tới hết
    beats = []
    t = first_beat
    while t < total_sec - 0.2:
        beats.append(t)
        t += B
    if len(beats) < 8:
        raise SystemExit(f"[LOI] nhac ngan qua ({len(beats)} beat) — can >=8")
    bf = [round(b * FPS) for b in beats]  # beat -> frame
    TOTAL = round(total_sec * FPS)
    print(f"BPM {bpm} · beat dau {first_beat:.2f}s · {len(beats)} beat · {total_sec:.1f}s")

    # ---- copy clip nguồn ----------------------------------------------------
    refs, durs = [], []
    for i, p in enumerate(clips_src):
        ref = f"assets/v{i}{p.suffix.lower()}"
        dst = assets / Path(ref).name
        if not dst.exists() or dst.stat().st_size != p.stat().st_size:
            shutil.copy2(p, dst)
        refs.append(ref)
        durs.append(probe_seconds(p))
    n = len(refs)
    print(f"{n} clip: " + ", ".join(f"{Path(r).name}({d:.0f}s)" for r, d in zip(refs, durs)))

    stickers = []
    if args.stickers:
        for i, p in enumerate(sorted(Path(args.stickers).glob("*.png"))):
            ref = f"assets/st{i}.png"
            shutil.copy2(p, assets / f"st{i}.png")
            stickers.append(ref)

    # ---- chia section theo beat --------------------------------------------
    nb = len(beats)
    a_end = max(3, round(nb * 0.25))
    b_end = a_end + max(3, round(nb * 0.20))
    c_end = b_end + max(3, round(nb * 0.20))
    d_end = c_end + max(3, round(nb * 0.25))
    d_end = min(d_end, nb - 1)

    footage, bands, texts, sticks, sfxs = [], [], [], [], []
    total = TOTAL
    ci = 0  # con trỏ xoay vòng clip

    def next_clip():
        nonlocal ci
        r = refs[ci % n]
        d = durs[ci % n]
        ci += 1
        return r, d

    def trim_for(d_sec, need_frames, speed):
        """trimStart an toàn trong clip nguồn."""
        usable = max(0.0, d_sec - need_frames / FPS * speed - 0.5)
        return round(usable * 0.4 * FPS)

    # A — intro beat-cut, speed xen kẽ
    speeds = [2.0, 0.5, 1.0, 2.0]
    for k in range(a_end):
        f0 = bf[k]
        f1 = bf[k + 1] if k + 1 < nb else TOTAL
        sp = speeds[k % len(speeds)]
        ref, d = next_clip()
        footage.append(video_clip(
            f"a{k}", ref, f0, max(1, f1 - f0), speed=sp,
            trimStartFrames=trim_for(d, f1 - f0, sp),
            filter={"saturate": 1.3} if k % 2 else {},
        ))
        if k > 0:
            sfxs.append(sfx_clip(f"sa{k}", "pop", f0, total, 0.35))
    texts.append(text_clip("t-title", args.title, bf[0] + 4,
                           max(1, bf[a_end] - bf[0] - 4),
                           layout={"x": round(W * 0.06), "y": round(H * 0.08)},
                           fontSize=max(56, round(W * 0.08))))
    if stickers:
        sticks.append({
            "id": "st-intro", "kind": "sticker", "from": bf[0] + 6,
            "durationInFrames": max(1, bf[a_end] - bf[0] - 6),
            "asset": stickers[0],
            "layout": {"x": round(W * 0.04), "y": round(H * 0.72),
                       "w": round(W * 0.3), "rotation": 0, "opacity": 1},
            "entrance": {"variant": "pop", "delayFrames": 0, "params": {}},
            "exit": None, "idle": {"amp": 6, "phase": 1}, "shadow": "lg",
        })
    sfxs.append(sfx_clip("s-start", "whoosh", bf[0], total, 0.5))

    # B — feature + đếm ngược
    fB0, fB1 = bf[a_end], bf[b_end]
    ref, d = next_clip()
    footage.append(video_clip("b0", ref, fB0, fB1 - fB0, fadeInFrames=6,
                              trimStartFrames=trim_for(d, fB1 - fB0, 1)))
    cnt_beats = list(range(a_end + 1, min(a_end + 4, b_end)))
    for j, kb in enumerate(cnt_beats):
        label = str(len(cnt_beats) - j)
        texts.append(text_clip(
            f"cnt{j}", label, bf[kb], max(1, (bf[kb + 1] if kb + 1 < nb else TOTAL) - bf[kb]),
            preset="plain", color=COUNT_COLORS[j % 3],
            layout={"x": round(W * 0.44), "y": round(H * 0.24)},
            fontSize=round(W * 0.14)))
        sfxs.append(sfx_clip(f"sc{j}", "click" if j < len(cnt_beats) - 1 else "coin",
                             bf[kb], total, 0.5))
    if len(stickers) > 1:
        sticks.append({
            "id": "st-feat", "kind": "sticker", "from": fB0 + 4,
            "durationInFrames": max(1, fB1 - fB0 - 4), "asset": stickers[1],
            "layout": {"x": round(W * 0.58), "y": round(H * 0.2),
                       "w": round(W * 0.22), "rotation": 0, "opacity": 1},
            "entrance": {"variant": "grow", "delayFrames": 0, "params": {}},
            "exit": None, "idle": {"amp": 2, "phase": 0}, "shadow": "none",
        })

    # C — mirror
    fC0, fC1 = bf[b_end], bf[c_end]
    mid = fC0 + round((fC1 - fC0) * 0.6)
    ref, d = next_clip()
    footage.append(video_clip("c0", ref, fC0, mid - fC0, mirror=True,
                              wipeInFrames=10, wipeDir="right",
                              trimStartFrames=trim_for(d, mid - fC0, 1)))
    footage.append(video_clip("c1", ref, mid, fC1 - mid, mirror=False,
                              trimStartFrames=trim_for(d, fC1 - mid, 1) + 60))
    texts.append(text_clip("t-mirror", "MIRROR", fC0 + 4, max(1, fC1 - fC0 - 4),
                           color="#4EC3E0",
                           layout={"x": round(W * 0.06), "y": round(H * 0.08)},
                           fontSize=max(48, round(W * 0.07))))
    sfxs.append(sfx_clip("s-mirror", "swipe", fC0, total, 0.5))
    sfxs.append(sfx_clip("s-flip", "thud", mid, total, 0.5))

    # D — split 3 dải (dọc: 3 dải ngang · ngang: 3 cột dọc)
    fD0, fD1 = bf[c_end], bf[d_end]
    gap = round(H * 0.02) if vertical else round(W * 0.02)
    for j in range(3):
        ref, d = next_clip()
        start = min(fD0 + j * round(FPS * B), fD1 - 1)
        if vertical:
            band_h = (H - 4 * gap) // 3
            layout = {"x": 0, "y": gap + j * (band_h + gap), "w": W, "h": band_h}
        else:
            band_w = (W - 4 * gap) // 3
            layout = {"x": gap + j * (band_w + gap), "y": 0, "w": band_w, "h": H}
        footage_or_bands = bands
        footage_or_bands.append(video_clip(
            f"d{j}", ref, start, max(1, fD1 - start),
            layout=layout, wipeInFrames=10,
            wipeDir="left" if j % 2 == 0 else "right",
            trimStartFrames=trim_for(d, fD1 - start, 1)))
        sfxs.append(sfx_clip(f"sd{j}", "paper", start, total, 0.45))

    # E — outro
    fE0 = bf[d_end]
    ref, d = next_clip()
    footage.append(video_clip("e0", ref, fE0, TOTAL - fE0, speed=2,
                              fadeInFrames=8,
                              trimStartFrames=trim_for(d, TOTAL - fE0, 2)))
    texts.append({
        "id": "t-end", "kind": "text", "from": fE0 + 6,
        "durationInFrames": max(1, TOTAL - fE0 - 6),
        "content": args.endtext, "preset": "punch", "color": "#FFE01B",
        "animation": "pop", "animationParams": {"restDeg": -1.5},
        "layout": {"x": round(W * 0.08), "y": round(H * 0.85)},
        "fontSize": max(48, round(W * 0.065)),
    })
    sfxs.append(sfx_clip("s-endriser", "riser", max(0, fE0 - round(FPS * B)), total, 0.45))

    # ---- project ------------------------------------------------------------
    now = datetime.now(timezone.utc).isoformat()
    project = {
        "version": 1,
        "meta": {"name": args.out, "channel": None, "templateRef": None,
                 "fps": FPS, "width": W, "height": H,
                 "createdAt": now, "modifiedAt": now},
        "timeline": {"durationInFrames": TOTAL},
        "sceneMarkers": [
            {"id": "mA", "atFrame": bf[0], "label": "A beat-cut"},
            {"id": "mB", "atFrame": bf[a_end], "label": "B feature"},
            {"id": "mC", "atFrame": bf[b_end], "label": "C mirror"},
            {"id": "mD", "atFrame": bf[c_end], "label": "D split"},
            {"id": "mE", "atFrame": bf[d_end], "label": "E outro"},
        ],
        "tracks": [
            {"id": "trk-video", "name": "Footage", "type": "video",
             "muted": False, "hidden": False, "locked": False, "clips": footage},
            {"id": "trk-bands", "name": "Split", "type": "video",
             "muted": False, "hidden": False, "locked": False, "clips": bands},
            {"id": "trk-sticker", "name": "Stickers", "type": "sticker",
             "muted": False, "hidden": False, "locked": False, "clips": sticks},
            {"id": "trk-text", "name": "Text", "type": "text",
             "muted": False, "hidden": False, "locked": False, "clips": texts},
            {"id": "trk-music", "name": "Music", "type": "audio",
             "muted": False, "hidden": False, "locked": False,
             "clips": [{"id": "music-1", "kind": "audio", "from": 0,
                        "durationInFrames": TOTAL, "asset": music_ref,
                        "volume": 0.6, "trimStartFrames": 0}]},
            {"id": "trk-sfx", "name": "SFX", "type": "audio",
             "muted": False, "hidden": False, "locked": False, "clips": sfxs},
        ],
        "captions": {"source": "none", "style": "outline", "enabled": False,
                     "fontSize": 44, "lines": [], "words": []},
        "theme": {"palette": {"bgTop": "#0B0C10", "bgBottom": "#0B0C10",
                              "accent": "#FFE01B"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#000000"},
    }

    out_dir = ROOT / "projects" / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "project.json").write_text(
        json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK projects/{args.out}/project.json — {len(footage)+len(bands)} clip / "
          f"{len(texts)} text / {len(sfxs)} sfx · section A@{bf[0]} B@{bf[a_end]} "
          f"C@{bf[b_end]} D@{bf[c_end]} E@{bf[d_end]}")
    print(f"Render: npx remotion render VoxProject --props=projects/{args.out}/project.json out/{args.out}.mp4")


if __name__ == "__main__":
    main()
