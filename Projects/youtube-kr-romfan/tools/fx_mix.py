# -*- coding: utf-8 -*-
"""fx_mix.py — lớp FX radio-drama cho kênh 사우 오디오 (port từ chouhen, user duyệt 2026-07-22).

Đọc `02_SCRIPTS/<slug>_FX.json` + `03_VOICE/<slug>/timeline.json` → SFX đúng khoảnh khắc
+ BGM động (dâng căng→cắt phựt→im lặng / swell) + quote card + phụ đề màu theo nhân vật.
- PIPELINE MỚI: scene_render.py tự import (subs màu + card burn lúc render + audio FX).
- RETRO video ĐÃ render (chưa đăng): `python tools/fx_mix.py <slug> --apply`
  → build lại audio từ voice.wav + remux -c:v copy (tự tái tạo tiếng CTA lang kr;
  card/phụ đề màu KHÔNG áp retro được).

FORMAT 02_SCRIPTS/<slug>_FX.json (skill script-kr-romfan xuất kèm khi viết kịch bản):
{
  "speakers": {"한소미": "hero", "백여우": "villain"},
  "lines":   [{"match": "câu thoại đắt", "speaker": "백여우"}],
  "events": [
    {"type":"sfx",  "match":"휴대폰이 진동했다", "name":"phone_buzz", "offset":-0.2, "gain":-8},
    {"type":"bgm_tense_cut", "from":"...", "cut":"...", "resume":"..."},
    {"type":"bgm_swell", "from":"...", "to":"..."},
    {"type":"card", "match":"...", "text":"≤20 ký hangul", "style":"hero|villain", "hold":1.2}
  ]
}
SFX bank: 04_VIDEO/_sfx (sinh bởi tools/sfx_bank.py): phone_buzz, phone_buzz_urgent,
heartbeat, sub_drop, door_knock, slap.
"""
import json, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SFX_DIR = PROJ / "04_VIDEO" / "_sfx"
CHOUHEN_TOOLS = Path(r"E:\Claude\Projects\youtube-jp-chouhen\tools")
LN = "loudnorm=I=-16:TP=-1.5:LRA=11"
FONT = "C:/Windows/Fonts/malgunbd.ttf"   # hangul bold

TENSE_LIN = 0.055   # ≈ -25dB
SWELL_LIN = 0.05    # ≈ -26dB
SFX_GAIN_DEFAULT = -8
CARD_STYLES = {
    "hero":    ((255, 235, 59, 255), (160, 0, 0, 255)),
    "villain": ((140, 235, 255, 255), (10, 30, 60, 255)),
}
SUB_COLORS = {"hero": "#FFD75E", "villain": "#8CEBFF"}


def voice_dir(slug):
    return PROJ / "03_VOICE" / slug


def out_dir(slug):
    return PROJ / "04_VIDEO" / slug


def load_timeline(slug):
    d = json.loads((voice_dir(slug) / "timeline.json").read_text(encoding="utf-8"))
    return d["lines"] if isinstance(d, dict) else d


def find_line(tl, spec_match, after=0.0, what=""):
    for l in tl:
        if spec_match in l["text"] and l["start"] >= after:
            return l
    raise SystemExit(f"[LỖI FX] không thấy dòng chứa「{spec_match}」{what}")


def load_fx(slug):
    p = PROJ / "02_SCRIPTS" / f"{slug}_FX.json"
    if not p.exists():
        return None, None
    return json.loads(p.read_text(encoding="utf-8")), p


def resolve_plan(slug, bgm_gain_db=-40.0):
    cfg, _ = load_fx(slug)
    if not cfg:
        return None
    tl = load_timeline(slug)
    base = 10 ** (bgm_gain_db / 20)
    sfx, cards, segs = [], [], []
    for ev in cfg.get("events", []):
        t = ev.get("type")
        if t == "sfx":
            l = find_line(tl, ev["match"], ev.get("after", 0), "(sfx)")
            f = SFX_DIR / f"{ev['name']}.wav"
            if not f.exists():
                raise SystemExit(f"[LỖI FX] thiếu {f} — chạy python tools/sfx_bank.py")
            sfx.append((f, l["start"] + ev.get("offset", 0.0), ev.get("gain", SFX_GAIN_DEFAULT)))
        elif t == "bgm_tense_cut":
            a = find_line(tl, ev["from"], ev.get("after", 0), "(bgm from)")["start"] - 0.2
            c = find_line(tl, ev["cut"], a, "(bgm cut)")["start"] - 1.0
            r = find_line(tl, ev["resume"], c, "(bgm resume)")["end"] + 0.6
            segs.append(("ramp", a, c, base, TENSE_LIN))
            segs.append(("flat", c, r, 0.0, 0.0))
        elif t == "bgm_swell":
            a = find_line(tl, ev["from"], ev.get("after", 0), "(swell from)")["start"]
            b = find_line(tl, ev["to"], a, "(swell to)")["start"]
            segs.append(("flat", a, b, SWELL_LIN, SWELL_LIN))
        elif t == "card":
            l = find_line(tl, ev["match"], ev.get("after", 0), "(card)")
            cards.append((ev["text"], ev.get("style", "hero"),
                          l["start"], l["end"] + ev.get("hold", 1.2)))
    expr = f"{base:.4f}"
    for kind, a, b, v0, v1 in reversed(sorted(segs, key=lambda s: s[1])):
        if kind == "ramp":
            expr = (f"if(between(t\\,{a:.2f}\\,{b:.2f})\\,"
                    f"{v0:.4f}+({v1:.4f}-{v0:.4f})*(t-{a:.2f})/({b - a:.2f})\\,{expr})")
        else:
            expr = f"if(between(t\\,{a:.2f}\\,{b:.2f})\\,{v0:.4f}\\,{expr})"
    return {"sfx": sfx, "vol_expr": expr, "cards": cards,
            "speakers": cfg.get("speakers", {}), "lines": cfg.get("lines", [])}


def make_card_png(path, text, style):
    from PIL import Image, ImageDraw, ImageFont
    Wc, Hc = 1920, 1080
    fill, stroke2 = CARD_STYLES.get(style, CARD_STYLES["hero"])
    img = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    size = 96
    f = ImageFont.truetype(FONT, size)
    bb = dr.textbbox((0, 0), text, font=f, stroke_width=8)
    while bb[2] - bb[0] > Wc - 160:
        size -= 6
        f = ImageFont.truetype(FONT, size)
        bb = dr.textbbox((0, 0), text, font=f, stroke_width=8)
    x = (Wc - (bb[2] - bb[0])) // 2 - bb[0]
    y = int(Hc * 0.40) - (bb[3] - bb[1]) // 2 - bb[1]
    pad = 46
    band = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    ImageDraw.Draw(band).rounded_rectangle(
        [90, y - pad + bb[1], Wc - 90, y + bb[3] + pad], 26, fill=(0, 0, 0, 150))
    img = Image.alpha_composite(img, band)
    dr = ImageDraw.Draw(img)
    dr.text((x, y), text, font=f, fill=fill, stroke_width=10, stroke_fill=stroke2)
    dr.text((x, y), text, font=f, fill=fill, stroke_width=4, stroke_fill=(0, 0, 0, 255))
    img.save(path)


def render_cards(plan, odir):
    out = []
    fx_dir = odir / "_fx"
    fx_dir.mkdir(parents=True, exist_ok=True)
    for k, (text, style, t0, t1) in enumerate(plan["cards"]):
        png = fx_dir / f"card_{k:02d}.png"
        if not png.exists():
            make_card_png(png, text, style)
        out.append((png, t0, t1))
    return out


def colorize_srt(plan, src_srt, out_srt, tl):
    marks = []
    for ln in plan["lines"]:
        cls = plan["speakers"].get(ln["speaker"], "other")
        color = SUB_COLORS.get(cls)
        if color:
            marks.append((ln["match"], ln["speaker"], color))
    blocks = [b for b in Path(src_srt).read_text(encoding="utf-8").strip().split("\n\n") if b.strip()]
    out = []
    for blk in blocks:
        lines = blk.splitlines()
        text = "\n".join(lines[2:])
        for match, name, color in marks:
            hit = any(match in l["text"] and (text.replace("\n", "") in l["text"]
                      or l["text"] in text) for l in tl)
            if hit or match in text:
                prefix = f"{name}" if text.startswith(("“", "\"", "「")) else ""
                text = f'<font color={color}>{prefix}{text}</font>'
                break
        out.append("\n".join(lines[:2]) + "\n" + text)
    Path(out_srt).write_text("\n\n".join(out) + "\n", encoding="utf-8")


def build_audio(slug, out_audio, bgm_path, bgm_gain_db, plan, no_bgm=False):
    voice = voice_dir(slug) / "voice.wav"
    cmd = ["ffmpeg", "-y", "-i", str(voice)]
    parts = [f"[0:a]{LN}[voc]"]
    mix = "[voc]"
    n = 1
    if not no_bgm:
        cmd += ["-stream_loop", "-1", "-i", str(bgm_path)]
        parts.append(f"[1:a]volume=volume='{plan['vol_expr']}':eval=frame[bg]")
        mix += "[bg]"
        n += 1
    for k, (f, t, g) in enumerate(plan["sfx"]):
        cmd += ["-i", str(f)]
        ms = int(t * 1000)
        parts.append(f"[{n + k}:a]adelay={ms}|{ms},volume={g}dB[s{k}]")
        mix += f"[s{k}]"
    total = n + len(plan["sfx"])
    parts.append(f"{mix}amix=inputs={total}:duration=first:normalize=0,"
                 f"alimiter=limit=0.95[a]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[a]",
            "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_audio), "-loglevel", "error"]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit("[LỖI FX] build audio fail")


def apply_retro(slug, bgm, bgm_gain, no_bgm):
    """Video đã render: thay track audio (voice + BGM động + SFX + tái tạo tiếng CTA kr)."""
    plan = resolve_plan(slug, bgm_gain)
    if not plan:
        raise SystemExit(f"[LỖI] không có 02_SCRIPTS/{slug}_FX.json")
    odir = out_dir(slug)
    video = odir / f"{slug}.mp4"
    if not video.exists():
        raise SystemExit(f"[LỖI] không thấy {video}")
    sys.path.insert(0, str(CHOUHEN_TOOLS))
    from cta_inject import parse_srt_start, PATTERNS
    from gen_cta_overlay import SFX_EVENTS
    cta_t = parse_srt_start(voice_dir(slug) / "subs.srt", PATTERNS["kr"])
    if cta_t is not None:
        cta_sfx = odir / "_fx" / "cta_sfx"
        if not (cta_sfx / "bell.wav").exists():
            subprocess.run([sys.executable, str(CHOUHEN_TOOLS / "gen_cta_sfx.py"),
                            "--out", str(cta_sfx)], check=True)
        for name, ev_t in SFX_EVENTS:
            plan["sfx"].append((cta_sfx / f"{name}.wav", cta_t + ev_t, -10))
        print(f"CTA @ {cta_t/60:.2f}m — tái tạo {len(SFX_EVENTS)} tiếng CTA vào track mới")
    audio = odir / "_fx_audio.m4a"
    build_audio(slug, audio, bgm, bgm_gain, plan, no_bgm)
    tmp = odir / f"{slug}_fx_tmp.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-i", str(video), "-i", str(audio),
                        "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest",
                        str(tmp), "-loglevel", "error"])
    if r.returncode != 0:
        raise SystemExit("[LỖI FX] remux fail")
    video.unlink()
    tmp.rename(video)
    audio.unlink()
    print(f"OK retro FX (audio-only): {len(plan['sfx'])} SFX + BGM động → {video}")
    if plan["cards"]:
        print(f"ℹ️ {len(plan['cards'])} quote card KHÔNG áp retro được (cần re-render).")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--bgm", default="04_VIDEO/bgm/Heartwarming.mp3")
    ap.add_argument("--bgm-gain", type=float, default=-40.0)
    ap.add_argument("--no-bgm", action="store_true")
    args = ap.parse_args()
    if args.apply:
        apply_retro(args.slug, PROJ / args.bgm, args.bgm_gain, args.no_bgm)
    else:
        plan = resolve_plan(args.slug, args.bgm_gain)
        if not plan:
            print("Không có FX.json — pipeline sẽ chạy như cũ.")
        else:
            print(f"Plan: {len(plan['sfx'])} SFX | {len(plan['cards'])} card | "
                  f"{len(plan['lines'])} câu tô màu")
            for f, t, g in plan["sfx"]:
                print(f"  sfx {f.stem:20s} @ {t/60:6.2f}m  {g}dB")
