# -*- coding: utf-8 -*-
"""Style lab — thử nghiệm các trường phái visual KHÁC diagram navy.

Cùng 1 nội dung (case 佐藤さん) render 3 style để so sánh:
  A. 家計簿 giấy sổ tay (kem + mực + dấu hanko đỏ)
  B. Tài liệu ảnh thật (photo mờ tối + panel kính + count-up)
  C. Bản tin ニュース (nền sáng flat + card trượt + băng tiêu đề)

CLI: python tools/style_lab.py   → 06_VIDEO/_demo_motion/demo_styles.mp4
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FPS = 30
FONT_PATH = "C:/Windows/Fonts/YuGothB.ttc"
_fc = {}


def F(s):
    if s not in _fc:
        _fc[s] = ImageFont.truetype(FONT_PATH, s)
    return _fc[s]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def seg(t, start, dur):
    return ease((t - start) / dur)


def at(d, txt, size, cx, y, fill):
    w = d.textlength(txt, font=F(size))
    d.text((cx - w / 2, y), txt, font=F(size), fill=fill)


# ───────── STYLE A — 家計簿 giấy sổ tay ─────────
PAPER = (247, 242, 228)
INK = (46, 58, 82)
INK_SOFT = (120, 128, 146)
HANKO = (196, 52, 48)
MARKER_G = (58, 158, 106)


def bg_paper():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    for y in range(180, H, 96):
        d.line((90, y, W - 90, y), fill=(214, 206, 186), width=3)
    d.line((230, 90, 230, H - 60), fill=(226, 150, 140), width=4)
    return img, d


def style_a(d, t, img):
    at(d, "佐藤さん（66歳・仙台） スーパーでパート", 66, 1060, 120, INK)
    p1 = seg(t, 0.08, 0.25)
    if p1 > 0:
        at(d, "給料 23万円 ＋ 年金 14万円", int(76 * min(1, 0.5 + p1 / 2)), 1060, 320, INK)
    p2 = seg(t, 0.35, 0.4)
    if p2 > 0:
        at(d, f"合計 {int(37 * p2)}万円", 150, 1060, 480, MARKER_G)
    # thanh bút dạ mọc tới 37/65
    bar_y = 760
    d.line((330, bar_y, 1740, bar_y), fill=INK_SOFT, width=5)
    at(d, "0", 40, 330, bar_y + 18, INK_SOFT)
    at(d, "65万円", 40, 1740 - 40, bar_y + 18, HANKO)
    d.line((1700, bar_y - 46, 1700, bar_y + 10), fill=HANKO, width=6)
    p3 = seg(t, 0.5, 0.3)
    if p3 > 0:
        x_end = 330 + (1700 - 330) * (37 / 65) * p3
        d.line((330, bar_y - 22, x_end, bar_y - 22), fill=MARKER_G, width=26)
    # dấu hanko 満額 đóng xuống
    p4 = seg(t, 0.82, 0.14)
    if p4 > 0:
        r = int(150 * (1.9 - 0.9 * p4))
        cx, cy = 1560, 460
        wd = max(int(r * 0.09), 6)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=HANKO, width=wd)
        at(d, "満額", int(r * 0.62), cx, cy - r * 0.36, HANKO)


# ───────── STYLE B — tài liệu ảnh thật + panel kính ─────────

_photo_cache = {}


def bg_photo():
    key = "p"
    if key not in _photo_cache:
        src = Path(__file__).parent.parent / "06_VIDEO" / "01_zaishoku-rorei-nenkin-kaisei-2026" / "slides_img" / "slide_01.jpg"
        im = Image.open(src).convert("RGB")
        ratio = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * ratio) + 1, int(im.height * ratio) + 1))
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                      (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        im = im.filter(ImageFilter.GaussianBlur(3))
        im = Image.blend(im, Image.new("RGB", (W, H), (8, 10, 18)), 0.62)
        _photo_cache[key] = im
    return _photo_cache[key].copy()


def glass(img, x0, y0, x1, y1):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=(16, 22, 40, 170), outline=(255, 255, 255, 60), width=3)
    img.alpha_composite(ov)


GOLD = (255, 213, 79)
SAFE = (86, 204, 136)


def style_b(d, t, img):
    p0 = seg(t, 0.05, 0.25)
    if p0 > 0:
        glass(img, 240, 150, 1680, 320)
        d = ImageDraw.Draw(img)
        at(d, "佐藤さん（66歳・仙台）働きながら年金受給", 62, 960, 200, (245, 245, 245))
    p1 = seg(t, 0.3, 0.3)
    if p1 > 0:
        glass(img, 340, 400, 1580, 760)
        d = ImageDraw.Draw(img)
        at(d, "給料 23万円 ＋ 年金 14万円", 58, 960, 450, (225, 228, 238))
        p2 = seg(t, 0.42, 0.4)
        at(d, f"合計 {int(37 * p2)}万円", 140, 960, 550, GOLD)
    if t > 0.85:
        at(d, "基準額65万円以内 → 年金は満額", 60, 960, 850, SAFE)


# ───────── STYLE C — bản tin ニュース sáng ─────────
NEWS_BG = (238, 242, 246)
NEWS_BLUE = (26, 84, 158)
NEWS_RED = (208, 44, 44)
NEWS_TEXT = (34, 40, 52)


def bg_news():
    img = Image.new("RGB", (W, H), NEWS_BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 86), fill=NEWS_BLUE)
    at(d, "年金と老後のお金研究室", 46, 350, 16, (255, 255, 255))
    d.rectangle((0, H - 110, W, H), fill=(252, 252, 252))
    d.rectangle((0, H - 110, W, H - 104), fill=NEWS_BLUE)
    at(d, "在職老齢年金：2026年4月から基準額65万円に引き上げ", 44, 960, H - 84, NEWS_TEXT)
    return img, d


def style_c(d, t, img):
    d.rectangle((70, 140, 340, 230), fill=NEWS_RED)
    at(d, "ケース1", 52, 205, 155, (255, 255, 255))
    # card trắng trượt vào từ phải
    p0 = seg(t, 0.08, 0.3)
    off = int((1 - p0) * 900)
    x0, y0, x1, y1 = 260 + off, 290, 1660 + off, 860
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0 + 14, y0 + 18, x1 + 14, y1 + 18), radius=26, fill=(0, 0, 0, 60))
    img.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=(255, 255, 255))
    d.rectangle((x0, y0 + 26, x0 + 18, y1 - 26), fill=NEWS_BLUE)
    at(d, "佐藤さん（66歳・仙台）パート勤務", 60, (x0 + x1) // 2, y0 + 60, NEWS_BLUE)
    if p0 >= 1:
        at(d, "給料 23万円 ＋ 年金 14万円", 56, (x0 + x1) // 2, y0 + 190, NEWS_TEXT)
        p2 = seg(t, 0.45, 0.4)
        at(d, f"合計 {int(37 * p2)}万円", 130, (x0 + x1) // 2, y0 + 290, NEWS_BLUE)
        if t > 0.85:
            at(d, "→ 年金カットなし（満額）", 58, (x0 + x1) // 2, y0 + 470, (30, 140, 84))


# ───────── STYLE D — いらすとや minh họa (free, ≤20 hình/video) ─────────
WARM_TOP = (255, 249, 236)
WARM_BOT = (250, 236, 214)
D_INK = (72, 60, 50)
D_GREEN = (52, 148, 96)
D_RED = (198, 60, 52)

_ira_cache = {}


def ira(name):
    if name not in _ira_cache:
        p = Path(__file__).parent.parent / "06_VIDEO" / "_demo_motion" / "anime" / name
        _ira_cache[name] = Image.open(p).convert("RGBA")
    return _ira_cache[name]


def bg_warm():
    img = Image.new("RGB", (W, H))
    for y in range(H):
        t = y / H
        img.paste(tuple(int(a + (b - a) * t) for a, b in zip(WARM_TOP, WARM_BOT)), (0, y, W, y + 1))
    d = ImageDraw.Draw(img)
    return img, d


def style_d(d, t, img):
    at(d, "佐藤さん（66歳・仙台） スーパーでパート", 66, 960, 90, D_INK)
    # nhân vật いらすとや trượt vào từ trái + "nảy" nhẹ
    p0 = seg(t, 0.05, 0.3)
    ch = ira("irasutoya_obaasan.png")
    scale = 620 / ch.height
    chr_img = ch.resize((int(ch.width * scale), 620))
    x = int(-500 + (170 + 500) * p0)
    img.paste(chr_img, (x, 300), chr_img)
    d = ImageDraw.Draw(img)
    # panel số bên phải
    if t > 0.3:
        d.rounded_rectangle((820, 300, 1800, 700), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
        at(d, "給料 23万円 ＋ 年金 14万円", 60, 1310, 360, D_INK)
        p2 = seg(t, 0.42, 0.4)
        at(d, f"合計 {int(37 * p2)}万円", 130, 1310, 470, D_GREEN)
    # hanko 満額
    p4 = seg(t, 0.84, 0.14)
    if p4 > 0:
        r = int(130 * (1.9 - 0.9 * p4))
        cx, cy = 1620, 850
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=D_RED, width=max(int(r * 0.09), 6))
        at(d, "満額", int(r * 0.6), cx, cy - r * 0.34, D_RED)


STYLES = {
    "A_kakeibo": (bg_paper, style_a, False),
    "B_photo": (None, style_b, True),
    "C_news": (bg_news, style_c, False),
    "D_irasutoya": (bg_warm, style_d, False),
}


def render_style(name, out_path, dur=4.2, hold=1.6):
    bg_fn, draw_fn, is_photo = STYLES[name]
    out_path = Path(out_path)
    tmp = out_path.parent / f"_frames_{out_path.stem}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    n = int(dur * FPS)
    for f in range(n):
        t = f / (n - 1)
        if is_photo:
            img = bg_photo().convert("RGBA")
            d = ImageDraw.Draw(img)
            draw_fn(d, t, img)
            img = img.convert("RGB")
        else:
            img, d = bg_fn()
            # nhãn style nhỏ góc phải để user gọi tên khi duyệt
            draw_fn(d, t, img)
        dd = ImageDraw.Draw(img)
        dd.text((W - 340, 20), f"STYLE {name[0]}", font=F(40),
                fill=(150, 150, 150) if name != "B_photo" else (220, 220, 220))
        img.save(tmp / f"{f:05d}.png")
    cmd = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp / "%05d.png"),
           "-vf", f"tpad=stop_mode=clone:stop_duration={hold}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"ffmpeg lỗi ({name}):\n{r.stderr[-1500:]}")
    shutil.rmtree(tmp)
    print(f"  ✓ {out_path.name}")


def main():
    outdir = Path(__file__).parent.parent / "06_VIDEO" / "_demo_motion"
    outdir.mkdir(parents=True, exist_ok=True)
    clips = []
    for name in ("A_kakeibo", "B_photo", "C_news", "D_irasutoya"):
        p = outdir / f"style_{name}.mp4"
        render_style(name, p)
        clips.append(p)
    lst = outdir / "list_styles.txt"
    lst.write_text("".join(f"file '{c.name}'\n" for c in clips), encoding="utf-8")
    demo = outdir / "demo_styles.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(demo)],
                       cwd=outdir, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"concat lỗi:\n{r.stderr[-1500:]}")
    print(f"DEMO STYLES → {demo}")


if __name__ == "__main__":
    main()
