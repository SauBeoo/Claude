# -*- coding: utf-8 -*-
"""
gen_cta_overlay.py — ve PNG sequence (nen trong suot) cho hieu ung CTA giua video:
3 nut like / share / comment kieu glass, sang dan theo thu tu + ring pulse + particle
+ "+1" bay len. Dung chung cho moi kenh (label theo --lang).

Usage:
  python gen_cta_overlay.py --out <dir> [--lang jp|kr|vn] [--dur 8] [--fps 30] [--scale 1.0]

Ghep vao video (overlay dung khoang CTA, lay timing tu subs.srt):
  ffmpeg -i video.mp4 -framerate 30 -itsoffset <start_s> -i <dir>/f_%04d.png \
    -filter_complex "[0][1]overlay=70:H-h-170:eof_action=pass" ...
Rule goc: .claude/rules/cta-midvideo.md
"""
import argparse
import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---- layout (truoc scale) ----
CANVAS_W, CANVAS_H = 440, 330
CARD_X, CARD_Y, CARD_W, CARD_H = 30, 96, 380, 210
BTN_R = 32
BTN_XS = [CARD_X + 65, CARD_X + 190, CARD_X + 315]   # tam 3 nut
BTN_Y = CARD_Y + 52
LABEL_Y = BTN_Y + BTN_R + 10
PILL = (CARD_X + 30, CARD_Y + 132, CARD_X + CARD_W - 30, CARD_Y + 180)  # nut subscribe

ACCENT = (62, 166, 255)          # xanh youtube-ish
RED = (230, 33, 23)              # do subscribe
WHITE = (255, 255, 255)

LABELS = {
    "jp": ["高評価", "シェア", "コメント"],
    "kr": ["좋아요", "공유", "댓글"],
    "vn": ["Thích", "Chia sẻ", "Bình luận"],
}
SUB_LABEL = {"jp": "チャンネル登録", "kr": "구독", "vn": "Đăng ký"}
FONTS = {
    "jp": r"C:\Windows\Fonts\YuGothB.ttc",
    "kr": r"C:\Windows\Fonts\malgunbd.ttf",
    "vn": r"C:\Windows\Fonts\segoeuib.ttf",
}

# ---- timeline (giay) ----
SLIDE_IN = 0.45
PRESS = [0.9, 2.1, 3.3]          # thoi diem "bam" nut 0/1/2
PRESS_SUB = 4.6                  # thoi diem bam subscribe (chuong keu)
BELL_DUR = 1.0                   # chuong rung sau khi bam
PULSE_DUR = 0.55
PART_DUR = 0.8
FADE_OUT = 0.6
# SFX (gen_cta_sfx tao whoosh/pop/bell.wav): whoosh luc truot len, pop tai cac PRESS
# + PRESS_SUB, bell (chime 2 not) tai PRESS_SUB
SFX_EVENTS = [("whoosh", 0.0),
              ("pop", PRESS[0]), ("pop", PRESS[1]), ("pop", PRESS[2]),
              ("pop", PRESS_SUB), ("bell", PRESS_SUB + 0.05)]


def ease_out(t):
    return 1 - (1 - t) ** 3


def draw_thumb(d, cx, cy, s, color):
    """Icon like (thumb-up) flat, ve bang polygon trong hop 40x40 quanh (cx,cy)."""
    def p(x, y):
        return (cx + (x - 20) * s, cy + (y - 20) * s)
    # co tay (cuff)
    d.rounded_rectangle([p(3, 18), p(11, 37)], radius=2 * s, fill=color)
    # ban tay + ngon cai
    d.polygon([p(13, 37), p(13, 19), p(21, 7), p(24, 9), p(24, 11),
               p(21.5, 18), p(34, 18), p(36.5, 21), p(35, 34),
               p(31, 37)], fill=color)


def draw_share(d, cx, cy, s, color):
    """Icon share (3 nut noi nhau kieu Android)."""
    pts = [(cx - 11 * s, cy), (cx + 11 * s, cy - 11 * s), (cx + 11 * s, cy + 11 * s)]
    lw = max(2, int(3.4 * s))
    d.line([pts[0], pts[1]], fill=color, width=lw)
    d.line([pts[0], pts[2]], fill=color, width=lw)
    for (x, y) in pts:
        r = 5.2 * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def draw_comment(d, cx, cy, s, color):
    """Icon comment (bong thoai + 3 cham)."""
    x0, y0 = cx - 16 * s, cy - 12 * s
    x1, y1 = cx + 16 * s, cy + 9 * s
    d.rounded_rectangle([x0, y0, x1, y1], radius=7 * s, fill=color)
    d.polygon([(cx - 8 * s, y1 - 1), (cx - 1 * s, y1 + 8 * s), (cx + 4 * s, y1 - 1)], fill=color)
    hole = (15, 15, 22, 255)
    for i in (-1, 0, 1):
        r = 2.4 * s
        d.ellipse([cx + i * 8 * s - r, cy - 1.5 * s - r, cx + i * 8 * s + r, cy - 1.5 * s + r],
                  fill=hole)


def draw_bell(d, cx, cy, s, color, tilt=0.0):
    """Icon chuong (dome + vanh + qua lac); tilt = nghieng khi rung (px)."""
    cx += tilt
    d.pieslice([cx - 10 * s, cy - 11 * s, cx + 10 * s, cy + 9 * s], 180, 360, fill=color)
    d.polygon([(cx - 10 * s, cy - 1 * s), (cx - 12 * s, cy + 6 * s),
               (cx + 12 * s, cy + 6 * s), (cx + 10 * s, cy - 1 * s)], fill=color)
    r = 3 * s
    d.ellipse([cx - r, cy + 7 * s - r, cx + r, cy + 7 * s + r], fill=color)


ICON_FNS = [draw_thumb, draw_share, draw_comment]


def render_frame(t, dur, lang, scale):
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    try:
        f_label = ImageFont.truetype(FONTS[lang], 21)
        f_plus = ImageFont.truetype(FONTS["vn"], 30)
    except OSError:
        f_label = f_plus = ImageFont.load_default()

    # card glass
    d.rounded_rectangle([CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H],
                        radius=24, fill=(15, 15, 22, 190), outline=(255, 255, 255, 60), width=2)

    for i, cx in enumerate(BTN_XS):
        pressed = t >= PRESS[i]
        # nut tron
        if pressed:
            d.ellipse([cx - BTN_R, BTN_Y - BTN_R, cx + BTN_R, BTN_Y + BTN_R],
                      fill=ACCENT + (235,))
        else:
            d.ellipse([cx - BTN_R, BTN_Y - BTN_R, cx + BTN_R, BTN_Y + BTN_R],
                      fill=(255, 255, 255, 38), outline=(255, 255, 255, 90), width=2)
        # ring pulse khi vua bam
        dt = t - PRESS[i]
        if 0 <= dt <= PULSE_DUR:
            k = ease_out(dt / PULSE_DUR)
            r = BTN_R + 4 + 22 * k
            a = int(200 * (1 - k))
            d.ellipse([cx - r, BTN_Y - r, cx + r, BTN_Y + r],
                      outline=ACCENT + (a,), width=3)
        # icon
        ICON_FNS[i](d, cx, BTN_Y, 1.0, WHITE + (255,))
        # label
        lb = LABELS[lang][i]
        w = d.textlength(lb, font=f_label)
        d.text((cx - w / 2, LABEL_Y), lb, font=f_label, fill=(255, 255, 255, 230))

    # ---- nut subscribe (pill do) ----
    sub_pressed = t >= PRESS_SUB
    try:
        f_sub = ImageFont.truetype(FONTS[lang], 24)
    except OSError:
        f_sub = f_label
    if sub_pressed:
        d.rounded_rectangle(PILL, radius=24, fill=RED + (240,))
    else:
        d.rounded_rectangle(PILL, radius=24, fill=(255, 255, 255, 38),
                            outline=(255, 255, 255, 90), width=2)
    # ring pulse quanh pill khi vua bam
    dts = t - PRESS_SUB
    if 0 <= dts <= PULSE_DUR:
        k = ease_out(dts / PULSE_DUR)
        g = 4 + 14 * k
        a = int(200 * (1 - k))
        d.rounded_rectangle([PILL[0] - g, PILL[1] - g, PILL[2] + g, PILL[3] + g],
                            radius=24 + g, outline=RED + (a,), width=3)
    pill_cx, pill_cy = (PILL[0] + PILL[2]) // 2, (PILL[1] + PILL[3]) // 2
    txt = SUB_LABEL[lang]
    tw = d.textlength(txt, font=f_sub)
    if sub_pressed:
        # chuong rung ben trai chu
        tilt = 0.0
        if 0 <= dts <= BELL_DUR:
            tilt = 3.5 * math.sin(dts * 26) * (1 - dts / BELL_DUR)
        bx = pill_cx - tw / 2 - 22
        draw_bell(d, bx, pill_cy, 1.0, WHITE + (255,), tilt)
        d.text((pill_cx - tw / 2 + 8, pill_cy - 16), txt, font=f_sub,
               fill=(255, 255, 255, 255))
        # particle do ban ra khi bam
        if 0 <= dts <= PART_DUR:
            k = ease_out(dts / PART_DUR)
            a = int(220 * (1 - k))
            for j in range(10):
                ang = math.radians(j * 36 - 90)
                dist = 34 + 34 * k
                px = pill_cx + dist * 1.9 * math.cos(ang)
                py = pill_cy + dist * 0.8 * math.sin(ang)
                r = 3.2 * (1 - 0.5 * k)
                d.ellipse([px - r, py - r, px + r, py + r], fill=RED + (a,))
    else:
        d.text((pill_cx - tw / 2, pill_cy - 16), txt, font=f_sub,
               fill=(255, 255, 255, 235))

    # particles + "+1" cho nut like
    dt = t - PRESS[0]
    if 0 <= dt <= PART_DUR:
        k = ease_out(dt / PART_DUR)
        a = int(220 * (1 - k))
        for j in range(8):
            ang = math.radians(j * 45 - 90)
            dist = (BTN_R + 8) + 30 * k
            px = BTN_XS[0] + dist * math.cos(ang)
            py = BTN_Y + dist * math.sin(ang)
            r = 3.5 * (1 - 0.5 * k)
            d.ellipse([px - r, py - r, px + r, py + r], fill=ACCENT + (a,))
    if 0 <= dt <= 1.2:
        k = ease_out(min(1.0, dt / 1.2))
        a = int(255 * (1 - k)) if dt > 0.25 else int(255 * dt / 0.25)
        d.text((BTN_XS[0] + 26, BTN_Y - BTN_R - 14 - 44 * k), "+1",
               font=f_plus, fill=ACCENT + (max(0, a),))

    # slide-in / fade-out toan khoi
    off_y, fade = 0, 1.0
    if t < SLIDE_IN:
        k = ease_out(t / SLIDE_IN)
        off_y, fade = int(40 * (1 - k)), k
    elif t > dur - FADE_OUT:
        k = (t - (dur - FADE_OUT)) / FADE_OUT
        off_y, fade = int(24 * k), 1 - k

    frame = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    frame.paste(img, (0, off_y), img)
    if fade < 1.0:
        alpha = frame.split()[3].point(lambda p: int(p * fade))
        frame.putalpha(alpha)
    if scale != 1.0:
        frame = frame.resize((int(CANVAS_W * scale), int(CANVAS_H * scale)),
                             Image.LANCZOS)
    return frame


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="jp", choices=list(LABELS))
    ap.add_argument("--dur", type=float, default=8.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    n = int(a.dur * a.fps)
    for i in range(n):
        render_frame(i / a.fps, a.dur, a.lang, a.scale).save(
            os.path.join(a.out, f"f_{i + 1:04d}.png"))
    print(f"OK: {n} frames -> {a.out}")


if __name__ == "__main__":
    main()
