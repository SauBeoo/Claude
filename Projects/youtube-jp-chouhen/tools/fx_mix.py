# -*- coding: utf-8 -*-
"""fx_mix.py — lớp FX radio-drama cho kênh 朗読 (user duyệt demo 2026-07-22).

Đọc `03_SCRIPTS/<slug>_FX.json` + `06_VIDEO/<slug>/timeline.json` → kế hoạch FX:
SFX đúng khoảnh khắc + BGM động (dâng căng→cắt phựt→im lặng / swell) + quote card
+ phụ đề màu theo nhân vật. Dùng 2 kiểu:
  1. PIPELINE MỚI: scene_render.py tự import (subs màu + card burn lúc render, audio ở stage final).
  2. RETRO video ĐÃ render (chưa đăng): `python tools/fx_mix.py <slug> --apply`
     → build lại audio từ voice.wav (SFX + BGM động) + remux -c:v copy (vài phút, KHÔNG re-render;
     card/phụ đề màu KHÔNG áp được retro — cần re-render mới có).

FORMAT <slug>_FX.json (skill script-chouhen xuất kèm khi viết kịch bản):
{
  "speakers": {"玲奈": "villain", "沙織": "hero"},        // class màu: hero=vàng ấm, villain=cyan lạnh, other=trắng
  "lines":   [{"match": "あ、やっと出た", "speaker": "玲奈"}],   // các câu thoại ĐẮT muốn tô màu + gắn tên (opt-in, không cần全部)
  "events": [
    {"type":"sfx",  "match":"スマートフォンが震えた", "name":"phone_buzz", "offset":-0.2, "gain":-8},
    {"type":"ambience", "from":"一月の大雪の朝だった", "to":"三人が、同時に笑った", "name":"blizzard", "gain":-30},
    {"type":"bgm_tense_cut", "from":"祖母の着物", "cut":"凍りつく", "resume":"調べはついています"},
    {"type":"bgm_swell", "from":"蜂の巣を", "to":"静かに告げた"},
    {"type":"card", "match":"婚約者の方にも", "text":"ご両親と婚約者にも、お送りしました", "style":"hero", "hold":1.2}
  ]
}
- match = substring của MỘT dòng trong timeline.json (dòng TTS); thêm "after": <giây> nếu chuỗi xuất hiện nhiều lần.
- sfx name = file trong 06_VIDEO/_sfx (sinh bởi sfx_bank.py). gain mặc định -8dB.
- **ambience** (thêm 2026-07-30) = TIẾNG KHUNG CẢNH chảy dưới cả một khối cảnh, loop từ câu
  `from` đến câu `to` (bed trong 06_VIDEO/_amb, sinh bởi ambience_bank.py). Đây là lớp khán giả
  kênh này — người NGHE — cảm được rõ nhất, và là thứ làm mỗi video có "chỗ" riêng thay vì
  cùng một phòng thu. gain mặc định -30dB; `fade` (mặc định 2.0s) vào/ra; `lead`/`tail` (1.0s)
  = vào trước / giữ sau khối thoại. Mỗi video nên có 2-4 bed cho các khung cảnh ĐỐI LẬP nhau.
- bgm_tense_cut: dâng -40→-25dB từ `from`→`cut`, CẮT PHỰT im lặng từ `cut`→`resume`, rồi về nền.
- card style: hero (vàng viền đỏ) / villain (cyan viền navy). hold = giây giữ thêm sau khi dòng kết thúc.
"""
import json, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SFX_DIR = PROJ / "06_VIDEO" / "_sfx"
AMB_DIR = PROJ / "06_VIDEO" / "_amb"
LN = "loudnorm=I=-16:TP=-1.5:LRA=11"

# hệ số tuyến tính BGM (base lấy từ --bgm-gain; mặc định kênh -40dB)
TENSE_LIN = 0.055   # ≈ -25dB
SWELL_LIN = 0.05    # ≈ -26dB
SFX_GAIN_DEFAULT = -8
AMB_GAIN_DEFAULT = -24   # tiếng khung cảnh: nghe ra "đang ở đâu" mà không đè giọng đọc.
                         # -24 = mức user DUYỆT BẰNG TAI 2026-07-30 (chọn bản LOUD của demo
                         # video 13; bản -30 bị đánh giá còn khẽ). Bed "phải im" như room_still
                         # thì hạ thêm 3dB trong FX.json.
CARD_STYLES = {  # fill, stroke ngoài
    "hero":    ((255, 235, 59, 255), (160, 0, 0, 255)),
    "villain": ((140, 235, 255, 255), (10, 30, 60, 255)),
}
SUB_COLORS = {"hero": "#FFD75E", "villain": "#8CEBFF"}


def load_timeline(vdir):
    d = json.loads((vdir / "timeline.json").read_text(encoding="utf-8"))
    return d["lines"] if isinstance(d, dict) else d


def find_line(tl, spec_match, after=0.0, what=""):
    for l in tl:
        if spec_match in l["text"] and l["start"] >= after:
            return l
    raise SystemExit(f"[LỖI FX] không thấy dòng chứa「{spec_match}」{what}")


def load_fx(slug):
    """Trả (fx_cfg, path) hoặc (None, None) nếu video không có FX.json."""
    p = PROJ / "03_SCRIPTS" / f"{slug}_FX.json"
    if not p.exists():
        return None, None
    return json.loads(p.read_text(encoding="utf-8")), p


def resolve_plan(slug, vdir, bgm_gain_db=-40.0):
    """FX.json + timeline → plan: sfx[(file,t,gain)], vol_expr BGM, cards[(text,style,t0,t1)]."""
    cfg, _ = load_fx(slug)
    if not cfg:
        return None
    tl = load_timeline(vdir)
    base = 10 ** (bgm_gain_db / 20)
    sfx, cards, segs, amb = [], [], [], []
    for ev in cfg.get("events", []):
        t = ev.get("type")
        if t == "sfx":
            l = find_line(tl, ev["match"], ev.get("after", 0), "(sfx)")
            f = SFX_DIR / f"{ev['name']}.wav"
            if not f.exists():
                raise SystemExit(f"[LỖI FX] thiếu {f} — chạy python tools/sfx_bank.py")
            sfx.append((f, l["start"] + ev.get("offset", 0.0), ev.get("gain", SFX_GAIN_DEFAULT)))
        elif t == "ambience":
            f = AMB_DIR / f"{ev['name']}.wav"
            if not f.exists():
                raise SystemExit(f"[LỖI FX] thiếu bed {f} — chạy python tools/ambience_bank.py")
            a = find_line(tl, ev["from"], ev.get("after", 0), "(amb from)")["start"]
            b = find_line(tl, ev["to"], a, "(amb to)")["end"]
            t0 = max(0.0, a - ev.get("lead", 1.0))
            t1 = b + ev.get("tail", 1.0)
            amb.append((f, t0, t1, ev.get("gain", AMB_GAIN_DEFAULT), ev.get("fade", 2.0)))
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
    # ghép vol expr (lồng if từ ngoài vào)
    expr = f"{base:.4f}"
    for kind, a, b, v0, v1 in reversed(sorted(segs, key=lambda s: s[1])):
        if kind == "ramp":
            expr = (f"if(between(t\\,{a:.2f}\\,{b:.2f})\\,"
                    f"{v0:.4f}+({v1:.4f}-{v0:.4f})*(t-{a:.2f})/({b - a:.2f})\\,{expr})")
        else:
            expr = f"if(between(t\\,{a:.2f}\\,{b:.2f})\\,{v0:.4f}\\,{expr})"
    return {"sfx": sfx, "vol_expr": expr, "cards": cards, "amb": amb,
            "speakers": cfg.get("speakers", {}), "lines": cfg.get("lines", [])}


# ---------- quote card PNG ----------

def make_card_png(path, text, style):
    from PIL import Image, ImageDraw, ImageFont
    Wc, Hc = 1920, 1080
    fill, stroke2 = CARD_STYLES.get(style, CARD_STYLES["hero"])
    img = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    size = 96
    f = ImageFont.truetype("C:/Windows/Fonts/yugothb.ttc", size)
    bb = dr.textbbox((0, 0), text, font=f, stroke_width=8)
    while bb[2] - bb[0] > Wc - 160:
        size -= 6
        f = ImageFont.truetype("C:/Windows/Fonts/yugothb.ttc", size)
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


def render_cards(plan, vdir):
    """Xuất PNG card → [(png, t0, t1)] (thời gian TUYỆT ĐỐI)."""
    out = []
    fx_dir = vdir / "_fx"
    fx_dir.mkdir(exist_ok=True)
    for k, (text, style, t0, t1) in enumerate(plan["cards"]):
        png = fx_dir / f"card_{k:02d}.png"
        if not png.exists():
            make_card_png(png, text, style)
        out.append((png, t0, t1))
    return out


# ---------- phụ đề màu ----------

def colorize_srt(plan, src_srt, out_srt, tl):
    """Tô màu + gắn tên các câu thoại khai báo trong lines. Cue srt khớp theo text chứa match."""
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
            # cue là MẢNH của dòng TTS (đã split) → tô khi cue nằm trong dòng gốc chứa match
            hit = any(match in l["text"] and (text.replace("\n", "") in l["text"]
                      or l["text"] in text) for l in tl)
            if hit or match in text:
                prefix = f"{name}" if text.startswith("「") else ""
                text = f'<font color={color}>{prefix}{text}</font>'
                break
        out.append("\n".join(lines[:2]) + "\n" + text)
    Path(out_srt).write_text("\n\n".join(out) + "\n", encoding="utf-8")


# ---------- audio build (dùng cả pipeline lẫn retro) ----------

def build_audio(vdir, out_audio, bgm_path, bgm_gain_db, plan, no_bgm=False):
    voice = vdir / "voice.wav"
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
        # kẹp về 0: offset âm ở câu ĐẦU video cho t<0 → adelay báo "Delay must be
        # non negative" và giết cả khâu final SAU khi đã ghép xong part (video 21,
        # 2026-08-09). Kẹp ở đây để lỗi chỉ làm lệch tiếng vài phần trăm giây,
        # không đốt cả lượt render.
        ms = max(0, int(t * 1000))
        parts.append(f"[{n + k}:a]adelay={ms}|{ms},volume={g}dB[s{k}]")
        mix += f"[s{k}]"
    n += len(plan["sfx"])
    # tiếng khung cảnh: bed 32s loop suốt khối cảnh, fade vào/ra để không "bật/tắt" lộ
    for k, (f, t0, t1, g, fade) in enumerate(plan.get("amb", [])):
        cmd += ["-stream_loop", "-1", "-i", str(f)]
        dur = max(2.0, t1 - t0)
        fd = min(fade, dur / 2)
        ms = max(0, int(t0 * 1000))   # cùng lý do với SFX ở trên (lead đẩy bed về trước 0s)
        parts.append(f"[{n + k}:a]atrim=0:{dur:.2f},asetpts=N/SR/TB,"
                     f"afade=t=in:st=0:d={fd:.2f},"
                     f"afade=t=out:st={dur - fd:.2f}:d={fd:.2f},"
                     f"volume={g}dB,adelay={ms}|{ms}[m{k}]")
        mix += f"[m{k}]"
    total = n + len(plan.get("amb", []))
    parts.append(f"{mix}amix=inputs={total}:duration=first:normalize=0,"
                 f"alimiter=limit=0.95[a]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[a]",
            "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_audio), "-loglevel", "error"]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit("[LỖI FX] build audio fail")


def apply_retro(slug, vdir, bgm, bgm_gain, no_bgm):
    """Video đã render: thay track audio = voice + BGM động + SFX (KHÔNG card/màu phụ đề).
    Video có CTA overlay sẵn → tiếng CTA nằm trong track cũ sẽ mất khi thay track,
    nên tự TÁI TẠO tiếng CTA (whoosh/pop/bell) đúng timestamp từ subs.srt."""
    plan = resolve_plan(slug, vdir, bgm_gain)
    if not plan:
        raise SystemExit(f"[LỖI] không có 03_SCRIPTS/{slug}_FX.json")
    video = vdir / f"{slug}.mp4"
    if not video.exists():
        raise SystemExit(f"[LỖI] không thấy {video}")
    # tái tạo tiếng CTA (nếu video có câu CTA trong srt)
    from cta_inject import parse_srt_start, PATTERNS
    from gen_cta_overlay import SFX_EVENTS
    cta_t = parse_srt_start(vdir / "subs.srt", PATTERNS["jp"])
    if cta_t is not None:
        cta_sfx = vdir / "_fx" / "cta_sfx"
        if not (cta_sfx / "bell.wav").exists():
            subprocess.run([sys.executable, str(PROJ / "tools" / "gen_cta_sfx.py"),
                            "--out", str(cta_sfx)], check=True)
        for name, ev_t in SFX_EVENTS:
            plan["sfx"].append((cta_sfx / f"{name}.wav", cta_t + ev_t, -10))
        print(f"CTA @ {cta_t/60:.2f}m — tái tạo {len(SFX_EVENTS)} tiếng CTA vào track mới")
    audio = vdir / "_fx_audio.m4a"
    build_audio(vdir, audio, bgm, bgm_gain, plan, no_bgm)
    tmp = vdir / f"{slug}_fx_tmp.mp4"
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
        print(f"ℹ️ {len(plan['cards'])} quote card KHÔNG áp retro được (cần re-render); "
              f"video mới render qua scene_render sẽ tự có.")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--apply", action="store_true", help="áp retro audio lên <slug>.mp4 (in-place)")
    ap.add_argument("--bgm", default="auto",
                    help="auto = theo vòng xoay bgm/ROTATION.log (dùng chung scene_render)")
    ap.add_argument("--bgm-gain", type=float, default=-40.0)
    ap.add_argument("--no-bgm", action="store_true")
    args = ap.parse_args()
    vdir = PROJ / "06_VIDEO" / args.slug
    from scene_render import pick_bgm          # dùng CHUNG vòng xoay, không tự chọn riêng
    bgm_sel = pick_bgm(args.slug, args.bgm)
    if args.apply:
        apply_retro(args.slug, vdir, bgm_sel, args.bgm_gain, args.no_bgm)
    else:
        plan = resolve_plan(args.slug, vdir, args.bgm_gain)
        if not plan:
            print("Không có FX.json — pipeline sẽ chạy như cũ.")
        else:
            print(f"Plan: {len(plan['sfx'])} SFX | {len(plan.get('amb', []))} ambience | "
                  f"{len(plan['cards'])} card | {len(plan['lines'])} câu tô màu")
            for f, t, g in plan["sfx"]:
                print(f"  sfx {f.stem:20s} @ {t/60:6.2f}m  {g}dB")
            for f, t0, t1, g, fd in plan.get("amb", []):
                print(f"  amb {f.stem:20s} {t0/60:6.2f}m → {t1/60:6.2f}m "
                      f"({(t1-t0)/60:5.2f}m)  {g}dB")
