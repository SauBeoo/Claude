# -*- coding: utf-8 -*-
"""post_02.py — hau ky BAN FULL video 02 (kieta-mise): lop TRO CHOI + dong ho + SFX that.

Chay SAU video_render:  py -3 tools/post_02.py
Lop dap them (thiet ke da duyet qua demo 02demo-asa6, user chot 2026-08-19):
1. CHIP DONG HO goc trai — 10 moc 朝4時→夜9時, cham mau doi theo gio trong ngay
2. CHIP DIEM 「n/30」 duoi chip gio — bang diem thuong truc (user che dau to o goc phai)
3. DAU HANKO 「n点目」 goc phai — pop 2.2s dung luc ghi diem roi bien, kem tieng pon
4. GRADING TROI THEO GIO: som lanh toi → sang tuoi → trua am → chieu vang → toi cam → dem navy
5. SFX THAT (pocket-se.info, YouTube OK, can credit): カタン dat chai (putpod) + ken dau phu (tofu)
   → CREDIT bat buoc khi dong goi: 「効果音：ポケットサウンド – https://pocket-se.info/」
"""
import io, re, sys, wave, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "02_kieta-mise"
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Black.otf"
SR = 44100

KANJI = {}
_d = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
for n in range(1, 31):
    t, o = divmod(n, 10)
    s = ("" if t == 0 else ("十" if t == 1 else _d[t] + "十")) + _d[o]
    KANJI[s] = n

# (khoa tim trong srt | None = t0, nhan chip, mau cham, ten grade)
CLOCK = [
    (None,          "朝4時",  (110, 130, 210), "dawn"),
    ("朝の六時",     "朝6時",  (255, 176, 66),  "morning"),
    ("朝の八時",     "朝8時",  (255, 205, 80),  "morning"),
    ("お昼を過ぎました", "昼",  (255, 230, 120), "noon"),
    ("昼下がり",     "昼下がり", (255, 215, 100), "noon"),
    ("午後の三時",   "午後3時", (255, 180, 90),  "afternoon"),
    ("夕方です",     "夕方",   (255, 140, 70),  "evening"),
    ("夜の、七時",   "夜7時",  (150, 160, 230), "night"),
    ("夜の八時",     "夜8時",  (120, 135, 225), "night"),
    ("夜の九時",     "夜9時",  (100, 115, 215), "night"),
]
GRADE = {
    "dawn":      "colorbalance=bs=0.11:bm=0.05:enable='{w}',eq=brightness=-0.07:saturation=0.80:enable='{w}'",
    "morning":   "colorbalance=bs=0.05:bm=0.02:rh=0.03:enable='{w}',eq=brightness=0.015:saturation=0.95:enable='{w}'",
    "noon":      "colorbalance=rh=0.02:rm=0.01:enable='{w}',eq=brightness=0.02:saturation=1.0:enable='{w}'",
    "afternoon": "colorbalance=rm=0.04:rh=0.05:bs=-0.02:enable='{w}',eq=brightness=0.01:saturation=1.02:enable='{w}'",
    "evening":   "colorbalance=rm=0.06:rh=0.06:bm=-0.02:enable='{w}',eq=brightness=-0.005:saturation=1.02:enable='{w}'",
    "night":     "colorbalance=bs=0.09:bm=0.05:rh=-0.02:enable='{w}',eq=brightness=-0.04:saturation=0.88:enable='{w}'",
}


def parse_srt(p):
    t = p.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(
            r"(\d+)\n(\d\d):(\d\d):(\d\d)[,.](\d{3}) --> (\d\d):(\d\d):(\d\d)[,.](\d{3})\n(.*?)(?:\n\n|\Z)",
            t, re.S):
        g = list(map(int, m.groups()[1:9]))
        out.append((g[0]*3600+g[1]*60+g[2]+g[3]/1000,
                    g[4]*3600+g[5]*60+g[6]+g[7]/1000,
                    m.group(10).replace("\n", "")))
    return out


def first_at(subs, key):
    for st, en, tx in subs:
        if key in tx:
            return st, en
    raise SystemExit(f"[LOI] khong thay '{key}' trong srt")


def chip(path, label, dot):
    f = ImageFont.truetype(FONT, 52)
    tw = ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(label, font=f)
    W, H = int(66 + tw + 26), 96
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W-1, H-1), radius=20, fill=(31, 42, 68, 232),
                        outline=(255, 255, 255, 255), width=3)
    d.ellipse((22, H//2-13, 48, H//2+13), fill=dot+(255,))
    d.text((66, H//2), label, font=f, fill=(255, 255, 255, 255), anchor="lm")
    im.save(path)


def counter_chip(path, n):
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


def stamp(path, num):
    S = 190
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    RED = (196, 58, 47, 255)
    d.ellipse((5, 5, S-5, S-5), fill=(255, 252, 245, 210))
    d.ellipse((8, 8, S-8, S-8), outline=RED, width=7)
    d.ellipse((18, 18, S-18, S-18), outline=RED, width=2)
    fn = ImageFont.truetype(FONT, 86 if num < 10 else 76)
    fs = ImageFont.truetype(FONT, 36)
    d.text((S//2, S//2 - 20), str(num), font=fn, fill=RED, anchor="mm")
    d.text((S//2, S//2 + 46), "点目", font=fs, fill=RED, anchor="mm")
    im = im.rotate(-7, expand=True, resample=Image.BICUBIC)
    im.save(path)


def load_mp3(p):
    w = VD / (p.stem + "_tmp.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p),
                    "-ar", str(SR), "-ac", "1", str(w)], check=True)
    with wave.open(str(w), "rb") as f:
        y = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(float)/32767.0
    w.unlink()
    return y


def pon():
    dur = 0.14
    t = np.linspace(0, dur, int(SR*dur), False)
    f = 760*np.exp(-t*14)+180
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*0.8


def write_wav(path, y):
    y16 = (np.clip(y, -1, 1)*32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(y16.tobytes())


def main():
    src = VD / "02_kieta-mise.mp4"
    if not src.exists():
        raise SystemExit("[LOI] chua co video render: " + str(src))
    subs = parse_srt(VD / "subs.srt")
    total = subs[-1][1] + 2.0

    # --- moc dong ho ---
    marks = []
    for key, label, dot, gname in CLOCK:
        t = 0.0 if key is None else first_at(subs, key)[0]
        marks.append((t, label, dot, gname))
    marks.sort(key=lambda x: x[0])
    # overlay (chip gio + chip diem) RUT LUI khi vao doan dap an/ket — khung sach
    t_end_overlay = first_at(subs, "最初のお約束")[0]
    # DAY-FOR-NIGHT cho mo bai (clip phim that quay ban ngay -> ep dem 4h sang):
    # cua so [0, cau tra loi 牛乳の瓶), de len tren grade dawn
    t_night_open = first_at(subs, "牛乳の瓶が")[0]

    # --- 30 diem ---
    pts = []
    seen = set()
    for st, en, tx in subs:
        for m in re.finditer(r"([一二三四五六七八九十]+)点目", tx):
            n = KANJI.get(m.group(1))
            if n and n not in seen:
                seen.add(n); pts.append((n, st))
    pts.sort()
    if len(pts) != 30:
        raise SystemExit(f"[LOI] tim thay {len(pts)}/30 diem trong srt: {sorted(seen)}")

    # --- ve overlay ---
    ov = VD / "_overlay"; ov.mkdir(exist_ok=True)
    for i, (t, label, dot, g) in enumerate(marks):
        chip(ov / f"clock{i:02d}.png", label, dot)
    for n, t in pts:
        stamp(ov / f"stamp{n:02d}.png", n)
        counter_chip(ov / f"cnt{n:02d}.png", n)

    # --- SFX ---
    y = np.zeros(int(SR * total))
    def put(sig, at, gain):
        i = int(SR * at)
        if i < 0 or i >= len(y): return
        y[i:i+len(sig)] += sig[:len(y)-i]*gain
    horn = load_mp3(VD / "_sfx_horn_raw.mp3")
    katan = load_mp3(VD / "_sfx_katan_raw.mp3")
    put(katan, first_at(subs, "カタン、と音がします")[1] + 0.15, 0.75)
    put(horn, first_at(subs, "ラッパが鳴ります")[1] - 0.25, 0.55)
    pp = pon()
    for n, t in pts:
        put(pp, t + 0.05, 0.28)
    write_wav(VD / "_sfx.wav", y)

    # --- filter graph (ghi ra FILE — 70 input PNG) ---
    DS = 2.2
    seg = []
    for i, (t, label, dot, g) in enumerate(marks):
        t2 = marks[i+1][0] if i+1 < len(marks) else total + 5
        seg.append((t, t2, g))
    grade_chain = [("eq=brightness=-0.17:saturation=0.52:contrast=1.06:enable='between(t,0,{tn:.2f})',"
                    "colorbalance=bs=0.18:bm=0.12:rm=-0.04:enable='between(t,0,{tn:.2f})',"
                    "vignette=PI/4.4:enable='between(t,0,{tn:.2f})'").format(tn=t_night_open)]
    for a, b, g in seg:
        grade_chain.append(GRADE[g].format(w=f"between(t,{a:.2f},{b:.2f})"))
    lines = [f"[0:v]{','.join(grade_chain)}[g0]"]
    inputs = []
    cur = "g0"; k = 1
    for i, (t, label, dot, g) in enumerate(marks):
        t2 = marks[i+1][0] if i+1 < len(marks) else t_end_overlay
        inputs.append(ov / f"clock{i:02d}.png")
        lines.append(f"[{cur}][{k}:v]overlay=36:32:enable='between(t,{t:.2f},{t2:.2f})'[g{k}]")
        cur = f"g{k}"; k += 1
    for j, (n, t) in enumerate(pts):
        t2 = pts[j+1][1] if j+1 < len(pts) else t_end_overlay
        inputs.append(ov / f"cnt{n:02d}.png")
        lines.append(f"[{cur}][{k}:v]overlay=36:142:enable='between(t,{t:.2f},{t2:.2f})'[g{k}]")
        cur = f"g{k}"; k += 1
    for n, t in pts:
        inputs.append(ov / f"stamp{n:02d}.png")
        lines.append(f"[{cur}][{k}:v]overlay=W-w-36:118:enable='between(t,{t:.2f},{t+DS:.2f})'[g{k}]")
        cur = f"g{k}"; k += 1
    lines[-1] = lines[-1].rsplit("[", 1)[0] + "[vo]"
    sfx_idx = k
    lines.append(f"[0:a][{sfx_idx}:a]amix=inputs=2:duration=first:normalize=0[ao]")
    fc = ";\n".join(lines)
    (VD / "_post_filter.txt").write_text(fc, encoding="utf-8")

    out = VD / "02_kieta-mise_POST.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src)]
    for p in inputs:
        cmd += ["-i", str(p)]
    cmd += ["-i", str(VD / "_sfx.wav"),
            "-filter_complex_script", str(VD / "_post_filter.txt"),
            "-map", "[vo]", "-map", "[ao]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
            str(out)]
    print(f"inputs: {len(inputs)+2} | moc gio: {len(marks)} | diem: {len(pts)} | tong {total:.0f}s")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:]); raise SystemExit(3)
    print(f"OK -> {out}")


if __name__ == "__main__":
    main()
