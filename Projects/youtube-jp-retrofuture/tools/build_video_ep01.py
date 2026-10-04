# -*- coding: utf-8 -*-
"""
Dựng video tập 01 từ `06_VIDEO/01_kumo-no-ue/SLIDES.json` + 40 clip t2v.

Chạy:
  python tools/build_video_ep01.py --check      # preflight: đủ clip chưa, đo gì được
  python tools/build_video_ep01.py --telop      # chỉ dựng PNG telop (rẻ, duyệt trước)
  python tools/build_video_ep01.py --build      # dựng video (CHẠY NỀN qua .cmd — xem §render-background)

🔴 LUẬT ĐÃ CÀI SẴN:
  · `render-background.md` §1.5 — THIẾU CLIP LÀ KHÔNG RENDER. `--build` tự chặn.
  · §2.7 ① — ⛔ KHÔNG dùng ffmpeg `drawtext` (chết vì fontconfig, và vẫn in "xong").
              Telop vẽ bằng PIL ra PNG rồi overlay.
  · §2.7 ③ — `amix` phải có `normalize=0`, nếu không lời nền bị chia âm lượng.
  · §2.7 ④ — `alimiter` phải `level=disabled`, nếu không tự đẩy đỉnh sát trần.
  · audience-45plus §2 — dissolve ≥0,4s (ở đây 0,5s).
"""
import io, os, sys, json, math, subprocess, argparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD   = os.path.join(ROOT, "06_VIDEO", "01_kumo-no-ue")
SPEC = os.path.join(VD, "SLIDES.json")


def load():
    with io.open(SPEC, encoding="utf-8") as fh:
        return json.load(fh)


def clip_path(spec, sc):
    return os.path.join(ROOT, spec["clip_dir"], f"ep01_{sc['id']}.mp4")


# ── PREFLIGHT ────────────────────────────────────────────────────────────────
def cmd_check(spec):
    miss, have = [], []
    for sc in spec["scenes"]:
        p = clip_path(spec, sc)
        (have if os.path.exists(p) else miss).append(sc)
    n = len(spec["scenes"])
    print(f"CLIP : {len(have)}/{n}")
    if miss:
        print(f"\n🔴 THIEU {len(miss)} CLIP — render-background.md §1.5: CHUA DUOC RENDER VIDEO")
        for sc in miss[:12]:
            print(f"   {sc['n']:02d}  ep01_{sc['id']}.mp4   ({sc['beat']})")
        if len(miss) > 12:
            print(f"   … va {len(miss)-12} clip nua")

    d, diss = spec["clip_sec"], spec["dissolve_sec"]
    total = n * d - (n - 1) * diss
    print(f"\nDO DAI: {n} x {d}s - {n-1} x {diss}s = {total:.1f}s = {int(total//60)}:{int(total%60):02d}")
    print(f"TELOP : {len(spec['telop']['items'])} dong (tran 6 — 00_WORLD_BIBLE §6)")
    print(f"SFX   : {len(spec['sfx'])} tieng, mot chum duy nhat (motif kim dan)")
    st = [sc for sc in spec["scenes"] if sc["story"]]
    print(f"MACH  : {len(st)}/{n} canh cho chuyen")
    for sc in st:
        print(f"   {sc['n']:02d}  {sc['story']}")

    bgm = os.path.join(ROOT, spec["audio"]["music"]["file"])
    print(f"\nBGM   : {'✅' if os.path.exists(bgm) else '🔴 CHUA CO'}  {spec['audio']['music']['file']}")
    sfxdir = os.path.join(ROOT, os.path.dirname(spec["audio"]["music"]["file"]), "sfx")
    nsfx = sum(1 for s in spec["sfx"] if os.path.exists(os.path.join(sfxdir, s["file"])))
    print(f"SFX   : {nsfx}/{len(spec['sfx'])} file co san trong {sfxdir}")
    return 0 if not miss else 1


# ── TELOP → PNG (⛔ không dùng drawtext) ─────────────────────────────────────
def cmd_telop(spec):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("🔴 can Pillow:  pip install pillow"); return 1
    t = spec["telop"]
    W, H = spec["size"]
    out = os.path.join(VD, "telop")
    os.makedirs(out, exist_ok=True)

    fp = None
    for c in [r"C:\Windows\Fonts\NotoSerifJP-Bold.otf", r"C:\Windows\Fonts\NotoSerifCJKjp-Bold.otf",
              r"C:\Windows\Fonts\msmincho.ttc", r"C:\Windows\Fonts\YuMin_36.ttc",
              r"C:\Windows\Fonts\meiryob.ttc"]:
        if os.path.exists(c):
            fp = c; break
    if not fp:
        print("🔴 khong tim thay font serif JP — cai Noto Serif JP hoac sua danh sach trong tool")
        return 1
    print(f"font  : {fp}")

    font = ImageFont.truetype(fp, t["size_px"])
    mx, my = t["margin_px"]
    for it in t["items"]:
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        bb = d.textbbox((0, 0), it["text"], font=font, stroke_width=t["stroke_px"])
        x, y = mx, H - my - (bb[3] - bb[1])
        d.text((x, y), it["text"], font=font, fill=t["colour"],
               stroke_width=t["stroke_px"], stroke_fill=t["stroke_colour"])
        f = os.path.join(out, f"telop_{it['scene']:02d}.png")
        img.save(f)
        print(f"  {it['scene']:02d}  {it['text']}   -> {os.path.basename(f)}")
    print(f"\n-> {out}")
    print("⚠️  Duyet bang MAT o co that truoc khi dung: chu co doc duoc tren nen SANG NHAT cua canh do khong")
    return 0


# ── BUILD → sinh .cmd chạy nền ───────────────────────────────────────────────
def cmd_build(spec):
    if cmd_check(spec) != 0:
        print("\n⛔ DUNG LAI — thieu clip (render-background.md §1.5). Gen du roi hay build.")
        return 1
    vd = VD
    os.makedirs(vd, exist_ok=True)
    n, d, diss = len(spec["scenes"]), spec["clip_sec"], spec["dissolve_sec"]

    # chuoi xfade — noi tiep, offset cong don
    inputs, filt, prev, off = [], [], "[0:v]", 0.0
    for i, sc in enumerate(spec["scenes"]):
        inputs.append(f'-i "{clip_path(spec, sc)}"')
    for i in range(1, n):
        off += d - diss
        lab = f"[vx{i}]"
        filt.append(f"{prev}[{i}:v]xfade=transition=fade:duration={diss}:offset={off:.3f}{lab}")
        prev = lab
    fc = ";".join(filt) if filt else "[0:v]null[vx0]"
    last = prev

    cmd = os.path.join(vd, "run_build.cmd")
    log = os.path.join(vd, "build.log")
    body = [
        "@echo off", "chcp 65001 >nul",
        f'cd /d "{ROOT}"',
        "set PYTHONUNBUFFERED=1", "set PYTHONIOENCODING=utf-8",
        "",
        "rem step 1 - concat clips with dissolve",
        f'ffmpeg -y {" ".join(inputs)} -filter_complex "{fc}" -map "{last}" '
        f'-c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r {spec["fps"]} '
        f'"{os.path.join(vd, "_v_noaudio.mp4")}" > "{log}" 2>&1',
        "set E1=%ERRORLEVEL%",
        f'>> "{log}" echo STEP1_EXIT=%E1%',
        'if not "%E1%"=="0" ( >> "%s" echo STOP - concat failed & exit /b 1 )' % log,
        "",
        "rem step 2 - telop overlay + audio mix: xem ghi chu trong tool",
        f'>> "{log}" echo STEP2_TODO=telop_overlay_and_audio',
        "",
        f'>> "{log}" echo EXITCODE=%ERRORLEVEL%',
    ]
    with io.open(cmd, "w", encoding="ascii", newline="\r\n") as fh:
        fh.write("\n".join(body) + "\n")

    print(f"\n-> {cmd}")
    print("\n🔴 CHAY NEN, KHONG chay foreground (render-background.md §1):")
    print(f'   cmd //c "{cmd}"      voi run_in_background: true')
    print(f"   log: {log}   — xong = co dong EXITCODE=0 VA duyet >=4 frame bang MAT")
    print("\n⚠️  Buoc 2 (telop overlay + tron nhac/SFX/loudnorm) chua noi day —")
    print("    can BGM + SFX that truoc, va do la thu phai NGHE roi moi chot (00_WORLD_BIBLE §7).")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--telop", action="store_true")
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    spec = load()
    print(f"《{spec['title_jp']}》 — {len(spec['scenes'])} canh\n" + "─" * 60)
    if a.telop: return cmd_telop(spec)
    if a.build: return cmd_build(spec)
    return cmd_check(spec)


if __name__ == "__main__":
    sys.exit(main())
