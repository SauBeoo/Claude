# -*- coding: utf-8 -*-
"""make_cards.py — ve the chu cho video yawa (the chuong / the 古典 / the thu) ra PNG 1920x1080.

Vi sao khong dung card cua video_render.py: card do KHONG xuong dong va dat chu o nua tren
(ca 7/7 the chuong + 3/3 the 古典 bai 1 tran khung, soi 2026-09-29). Luat audience-45plus §2.0e:
the chu phai TU CO CO theo be rong.

Doc 03_SCRIPTS/<stem>_SLIDES.json. Entry co khoa "reveal": {"lines","times"} + "_dur" -> clips/clip_NN.mp4
(chu hien dan tung dong, renderer lay qua "video": true). Entry co khoa "card": {"type": "chapter"|"quote"|"letter",
"lines": [...]}. Ghi PNG vao 06_VIDEO/<stem>/slides_img/slide_NN.png (NN = index slide, :02d nhu video_render).

Vung an toan: x 160..1480 (chua goc duoi-phai cho nguoi ke), y 120..800 (chua dai phu de).
Chay: python tools/make_cards.py 01_danshari-kokoro [--only 15,64]
"""
import sys, io, json, argparse, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 160, 1480, 120, 800
MINCHO = "C:/Windows/Fonts/yumindb.ttf"      # 游明朝 Demibold — 古典 + thu
GOTHIC = "C:/Windows/Fonts/YuGothB.ttc"      # 游ゴシック Bold — the chuong
TOP, BOT = (40, 44, 78), (22, 24, 46)        # = channels.PALETTES["yawa"]
GOLD, CREAM, INK = (240, 196, 110), (246, 238, 222), (58, 46, 36)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", size)


def wrap(text, fnt, maxw, draw):
    """Ngat dong o sau dau cau (、。」) truoc; khong duoc thi cat theo ky tu."""
    out, cur = [], ""
    tokens = re.findall(r"[^、。」]*[、。」]?", text)
    tokens = [t for t in tokens if t]
    for t in tokens:
        if draw.textlength(cur + t, font=fnt) <= maxw:
            cur += t
            continue
        if cur:
            out.append(cur); cur = ""
        while draw.textlength(t, font=fnt) > maxw:      # token don le qua dai -> cat ky tu
            k = len(t)
            while k > 1 and draw.textlength(t[:k], font=fnt) > maxw:
                k -= 1
            out.append(t[:k]); t = t[k:]
        cur = t
    if cur:
        out.append(cur)
    return out


def fit(texts, path, start, minsize, maxw, maxh, gap=1.55):
    """Co co tu `start` xuong toi khi TAT CA dong vua be rong va tong chieu cao vua maxh."""
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for size in range(start, minsize - 1, -2):
        f = font(path, size)
        # "／" = cho ngat dong do nguoi viet chi dinh (cau 古典: ngat dung nhip doc, khong che doi tu)
        lines = [ln for t in texts for part in t.split("／") for ln in wrap(part, f, maxw, d)]
        if len(lines) * size * gap <= maxh and all(d.textlength(l, font=f) <= maxw for l in lines):
            return f, size, lines
    raise SystemExit(f"[LOI] khong vua khung ngay ca co {minsize}: {texts}")


def bg_night():
    im = Image.new("RGB", (W, H), TOP)
    px = im.load()
    for y in range(H):
        k = y / (H - 1)
        c = tuple(int(TOP[i] * (1 - k) + BOT[i] * k) for i in range(3))
        for x in range(W):
            px[x, y] = c
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((W * 0.18, H * 0.05, W * 0.78, H * 0.85), fill=60)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new("RGB", (W, H), (70, 70, 110)), im, glow)
    return im


def bg_paper():
    im = Image.new("RGB", (W, H), (214, 200, 176))
    d = ImageDraw.Draw(im)
    d.rectangle((150, 70, 1490, 830), fill=CREAM)
    for y in range(150, 820, 86):                       # dong ke giay viet thu
        d.line((210, y, 1430, y), fill=(222, 206, 184), width=2)
    return im


def centered(d, lines, f, size, color, cx, y0, y1, gap=1.55):
    lh = size * gap
    y = (y0 + y1) / 2 - lh * len(lines) / 2 + (lh - size) / 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text((cx - w / 2, y), ln, font=f, fill=color)
        y += lh
    return y


def card(spec):
    typ, lines = spec["type"], spec["lines"]
    cx = (SAFE_X0 + SAFE_X1) / 2
    maxw = SAFE_X1 - SAFE_X0 - 80
    if typ == "chapter":
        im = bg_night(); d = ImageDraw.Draw(im)
        fs = font(GOTHIC, 64)
        d.text((cx - d.textlength(lines[0], font=fs) / 2, 250), lines[0], font=fs, fill=GOLD)
        d.line((cx - 60, 345, cx + 60, 345), fill=GOLD, width=3)
        f, size, ls = fit([lines[1]], GOTHIC, 92, 56, maxw, 380)
        centered(d, ls, f, size, (250, 248, 240), cx, 380, 760)
    elif typ == "quote":
        im = bg_night(); d = ImageDraw.Draw(im)
        f, size, ls = fit([lines[0]], MINCHO, 84, 52, maxw, 470)
        yend = centered(d, ls, f, size, (250, 246, 232), cx, 150, 640)
        fs = font(MINCHO, 44)
        src = lines[1]
        d.text((cx - d.textlength(src, font=fs) / 2, max(yend + 30, 680)), src, font=fs, fill=GOLD)
    elif typ == "letter":
        im = bg_paper(); d = ImageDraw.Draw(im)
        f, size, ls = fit(lines, MINCHO, 76, 50, maxw - 100, 600)
        centered(d, ls, f, size, INK, cx, 120, 780)
    else:
        raise SystemExit(f"[LOI] type la: {typ}")
    return im


def reveal_clip(spec, dur, path, fps=30, fade=0.35):
    """The CHU HIEN DAN TUNG DONG (user 2026-09-29: "thinh thoang hien thi chu chay tung dong").
    lines[i] hien ra o giay times[i] (= luc giong doc toi dong do, lay tu timeline.json),
    mo dan `fade` giay; dong DANG doc sang trang, dong da doc diu xuong kem. Bo cuc co dinh tu
    khung dau (co chu tinh cho TAT CA dong) nen chu khong nhay cho khi dong moi vao."""
    import subprocess
    import numpy as np
    lines, times = spec["lines"], spec["times"]
    cx = (SAFE_X0 + SAFE_X1) / 2
    f, size, _ = fit(lines, GOTHIC, 84, 50, SAFE_X1 - SAFE_X0 - 80, 560)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    rows = []                                   # (dong goc index, text dong da ngat)
    for i, t in enumerate(lines):
        for ln in wrap(t, f, SAFE_X1 - SAFE_X0 - 80, d0):
            rows.append((i, ln))
    lh = size * 1.6
    y0 = (SAFE_Y0 + SAFE_Y1) / 2 - lh * len(rows) / 2
    base = np.asarray(bg_night()).astype(np.float32)
    layers = []                                 # moi dong goc = 1 lop mat na chu
    for i in range(len(lines)):
        m = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(m)
        for k, (j, ln) in enumerate(rows):
            if j == i:
                dm.text((cx - d0.textlength(ln, font=f) / 2, y0 + k * lh), ln, font=f, fill=255)
        layers.append(np.asarray(m).astype(np.float32)[..., None] / 255.0)
    bright, dim = np.array([250, 248, 240], np.float32), np.array([200, 190, 170], np.float32)
    n = int(round((dur + 0.3) * fps))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
                          "-pix_fmt", "yuv420p", "-crf", "18", str(path)], stdin=subprocess.PIPE)
    last = None
    for fr in range(n):
        t = fr / fps
        key = tuple(round(min(max((t - times[i]) / fade, 0), 1), 2) for i in range(len(lines))) + (sum(t >= x for x in times),)
        if key != last:
            img = base.copy()
            cur = max([i for i in range(len(lines)) if t >= times[i]], default=-1)
            for i, lay in enumerate(layers):
                a = min(max((t - times[i]) / fade, 0), 1)
                if a <= 0:
                    continue
                col = bright if i == cur else dim
                img = img * (1 - lay * a) + col * lay * a
            buf = img.clip(0, 255).astype(np.uint8).tobytes(); last = key
        p.stdin.write(buf)
    p.stdin.close(); p.wait()
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    sl = json.load(open(PROJ / "03_SCRIPTS" / f"{a.stem}_SLIDES.json", encoding="utf-8"))
    out = PROJ / "06_VIDEO" / a.stem / "slides_img"
    out.mkdir(parents=True, exist_ok=True)
    only = {int(x) for x in a.only.split(",") if x}
    n = 0
    clips = PROJ / "06_VIDEO" / a.stem / "clips"
    clips.mkdir(parents=True, exist_ok=True)
    nr = 0
    for i, e in enumerate(sl):
        if only and i not in only:
            continue
        if "card" in e:
            card(e["card"]).save(out / f"slide_{i:02d}.png")
            n += 1
        elif "reveal" in e:
            rc = reveal_clip(e["reveal"], e["_dur"], clips / f"clip_{i:02d}.mp4")
            if rc:
                raise SystemExit(f"[LOI] ffmpeg reveal slide {i} exit {rc}")
            nr += 1
    print(f"ve {n} the -> {out} | {nr} clip chu hien dan -> {clips}")


if __name__ == "__main__":
    main()
