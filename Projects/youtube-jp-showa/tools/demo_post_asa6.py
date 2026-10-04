# -*- coding: utf-8 -*-
"""demo_post_asa6.py — hau ky DEMO 朝6時 (video 02): lop TRO CHOI + grading + SFX. (v2)

v2 sua theo user 2026-08-19:
- Con dau do goc phai VUONG -> thu nho 190px, chi hien 2.2s luc ghi diem roi bien.
  Bang diem thuong truc chuyen thanh CHIP NHO 「◯/30」 duoi chip dong ho (goc trai).
- Ken dau phu v2: not 2 TUOT DOC xuong (bend), timbre re/mui hon (odd harmonics),
  va day RA XA (echo 2 lop + lowpass) — dung ky uc "nghe tu dau ngo", giau chat synth.
  Xuat them _horn_v2.wav de nghe rieng khong can tua video.

Chay SAU khi video_render xong:  py -3 tools/demo_post_asa6.py
"""
import io, re, sys, wave, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "02demo-asa6"
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Black.otf"
SR = 44100


# ---------- 1. doc srt -> timeline ----------
def parse_srt(p):
    t = p.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(
            r"(\d+)\n(\d\d):(\d\d):(\d\d)[,.](\d{3}) --> (\d\d):(\d\d):(\d\d)[,.](\d{3})\n(.*?)(?:\n\n|\Z)",
            t, re.S):
        g = list(map(int, m.groups()[1:9]))
        st = g[0]*3600 + g[1]*60 + g[2] + g[3]/1000
        en = g[4]*3600 + g[5]*60 + g[6] + g[7]/1000
        out.append((st, en, m.group(10).replace("\n", "")))
    return out


def first_at(subs, key):
    for st, en, tx in subs:
        if key in tx:
            return st, en
    raise SystemExit(f"[LOI] khong thay '{key}' trong srt")


# ---------- 2. ve overlay PNG ----------
def make_clock_chip(path):
    W, H = 300, 96
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W-1, H-1), radius=20, fill=(31, 42, 68, 232),
                        outline=(255, 255, 255, 255), width=3)
    d.ellipse((22, H//2-13, 48, H//2+13), fill=(255, 176, 66, 255))
    f = ImageFont.truetype(FONT, 52)
    d.text((66, H//2), "朝6時", font=f, fill=(255, 255, 255, 255), anchor="lm")
    im.save(path)


def make_counter_chip(path, n):
    """Chip nho 「n/30」 — bang diem thuong truc, nam duoi chip dong ho."""
    W, H = 170, 64
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W-1, H-1), radius=14, fill=(31, 42, 68, 210),
                        outline=(255, 255, 255, 230), width=2)
    fb = ImageFont.truetype(FONT, 40)
    fs = ImageFont.truetype(FONT, 28)
    d.text((18, H//2), str(n), font=fb, fill=(255, 214, 92, 255), anchor="lm")
    w = d.textlength(str(n), font=fb)
    d.text((18+w+6, H//2+3), "/30", font=fs, fill=(255, 255, 255, 255), anchor="lm")
    im.save(path)


def make_stamp(path, num):
    """Dau hanko — v2 nho lai (190px), chi hien 2.2s luc ghi diem."""
    S = 190
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    RED = (196, 58, 47, 255)
    d.ellipse((5, 5, S-5, S-5), fill=(255, 252, 245, 210))
    d.ellipse((8, 8, S-8, S-8), outline=RED, width=7)
    d.ellipse((18, 18, S-18, S-18), outline=RED, width=2)
    fn = ImageFont.truetype(FONT, 86)
    fs = ImageFont.truetype(FONT, 36)
    d.text((S//2, S//2 - 20), str(num), font=fn, fill=RED, anchor="mm")
    d.text((S//2, S//2 + 46), "点目", font=fs, fill=RED, anchor="mm")
    im = im.rotate(-7, expand=True, resample=Image.BICUBIC)
    im.save(path)


# ---------- 3. synth SFX (license sach - tu tao) ----------
def _lowpass(y, alpha=0.14):
    out = np.empty_like(y)
    acc = 0.0
    for i in range(len(y)):
        acc += alpha * (y[i] - acc)
        out[i] = acc
    return out


def horn():
    """Ken dau phu v2 「トーフー」:
    not 1 ngan, not 2 TUOT DOC ~4 semitone; timbre re/mui (odd harmonics manh);
    day ra xa: lowpass + 2 lop echo — nhu nghe tu dau ngo."""
    def tone(f0, dur, bend_to=None, vol=1.0):
        t = np.linspace(0, dur, int(SR*dur), False)
        f = np.full_like(t, float(f0))
        if bend_to:
            # giu 35% dau, roi truot xuong bend_to theo duong cong lom
            k = int(len(t)*0.35)
            curve = (np.linspace(0, 1, len(t)-k))**1.4
            f[k:] = f0 + (bend_to - f0)*curve
        f = f*(1 + 0.014*np.sin(2*np.pi*5.3*t)*np.minimum(1, t*4))
        ph = 2*np.pi*np.cumsum(f)/SR
        y = (1.00*np.sin(ph) + 0.30*np.sin(2*ph) + 0.55*np.sin(3*ph)
             + 0.15*np.sin(4*ph) + 0.28*np.sin(5*ph) + 0.10*np.sin(7*ph))
        # hoi re: nhieu bien do nho theo chu ky
        y *= 1 + 0.06*np.sign(np.sin(ph*0.5))
        atk = int(SR*0.09); rel = int(SR*0.30)
        env = np.ones_like(t)
        env[:atk] = np.linspace(0, 1, atk)**0.7
        env[-rel:] *= np.linspace(1, 0, rel)
        return y*env*vol
    a = tone(466.16, 0.55)                       # 「トー」 A#4
    gap = np.zeros(int(SR*0.10))
    b = tone(466.16, 1.55, bend_to=370.0)        # 「フー」 tuot xuong ~F#4
    y = np.concatenate([a, gap, b])
    y = np.tanh(y*0.55)
    # --- day ra xa ---
    y = _lowpass(y, 0.16)
    d1, d2 = int(SR*0.21), int(SR*0.43)
    out = np.zeros(len(y)+d2)
    out[:len(y)] += y
    out[d1:d1+len(y)] += 0.34*y
    out[d2:d2+len(y)] += 0.16*y
    return out/np.max(np.abs(out))


def pon():
    dur = 0.14
    t = np.linspace(0, dur, int(SR*dur), False)
    f = 760*np.exp(-t*14)+180
    y = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)
    return y*0.8


def write_wav(path, y):
    y16 = (np.clip(y, -1, 1)*32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(y16.tobytes())


def main():
    src = VD/"02demo-asa6.mp4"
    if not src.exists():
        raise SystemExit("[LOI] chua co video render: " + str(src))
    subs = parse_srt(VD/"subs.srt")
    total = subs[-1][1] + 2.0

    t_horn = first_at(subs, "ラッパが鳴ります")[1] - 0.25
    t4 = first_at(subs, "四点目")[0]
    t5 = first_at(subs, "五点目")[0]
    t6 = first_at(subs, "六点目")[0]

    ov = VD/"_overlay"; ov.mkdir(exist_ok=True)
    make_clock_chip(ov/"clock.png")
    for n in (4, 5, 6):
        make_stamp(ov/f"stamp{n}.png", n)
        make_counter_chip(ov/f"cnt{n}.png", n)

    # KEN THAT — ban thu goc, khong synth (user chot 2026-08-19).
    # Nguon: pocket-se.info/archives/539 (tofu.mp3) — YouTube kiem tien OK,
    # cat/sua OK, CAN CREDIT: 「効果音：ポケットサウンド – https://pocket-se.info/」
    import subprocess as _sp
    raw = VD/"_horn_real_raw.mp3"
    if not raw.exists():
        raise SystemExit("[LOI] thieu ban thu ken that: " + str(raw))
    _sp.run(["ffmpeg","-v","error","-y","-i",str(raw),
             "-ar",str(SR),"-ac","1",str(VD/"_horn_real.wav")],check=True)
    with wave.open(str(VD/"_horn_real.wav"),"rb") as w:
        h = np.frombuffer(w.readframes(w.getnframes()),dtype="<i2").astype(float)/32767.0
    y = np.zeros(int(SR*total))
    def put(sig, at, gain):
        i = int(SR*at)
        y[i:i+len(sig)] += sig[:len(y)-i]*gain
    put(h, t_horn, 0.55)
    for tt in (t4, t5, t6):
        put(pon(), tt+0.05, 0.30)
    write_wav(VD/"_sfx.wav", y)

    out = VD/"02demo-asa6_POST.mp4"
    grade = ("colorbalance=bs=0.05:bm=0.02:rh=0.03:bh=-0.02,"
             "eq=brightness=0.015:saturation=0.95")
    DS = 2.2   # dau chi hien 2.2s
    fc = (
        f"[0:v]{grade}[g];"
        f"[g][1:v]overlay=36:32[v1];"
        # bang diem thuong truc: chip nho duoi chip gio
        f"[v1][5:v]overlay=36:142:enable='between(t,{t4:.2f},{t5:.2f})'[c1];"
        f"[c1][6:v]overlay=36:142:enable='between(t,{t5:.2f},{t6:.2f})'[c2];"
        f"[c2][7:v]overlay=36:142:enable='gte(t,{t6:.2f})'[c3];"
        # dau hanko: pop 2.2s roi bien
        f"[c3][2:v]overlay=W-w-36:118:enable='between(t,{t4:.2f},{t4+DS:.2f})'[s1];"
        f"[s1][3:v]overlay=W-w-36:118:enable='between(t,{t5:.2f},{t5+DS:.2f})'[s2];"
        f"[s2][4:v]overlay=W-w-36:118:enable='between(t,{t6:.2f},{t6+DS:.2f})'[vo];"
        f"[0:a][8:a]amix=inputs=2:duration=first:normalize=0[ao]"
    )
    cmd = ["ffmpeg", "-v", "error", "-y",
           "-i", str(src),
           "-i", str(ov/"clock.png"),
           "-i", str(ov/"stamp4.png"), "-i", str(ov/"stamp5.png"), "-i", str(ov/"stamp6.png"),
           "-i", str(ov/"cnt4.png"), "-i", str(ov/"cnt5.png"), "-i", str(ov/"cnt6.png"),
           "-i", str(VD/"_sfx.wav"),
           "-filter_complex", fc,
           "-map", "[vo]", "-map", "[ao]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
           str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:]); raise SystemExit(3)
    print(f"OK -> {out}")
    print(f"   horn @{t_horn:.2f}s | dau pop 2.2s @ {t4:.2f}/{t5:.2f}/{t6:.2f} | chip diem duoi chip gio")


if __name__ == "__main__":
    main()
