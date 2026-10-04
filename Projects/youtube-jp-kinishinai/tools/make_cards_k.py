# -*- coding: utf-8 -*-
"""make_cards_k.py — ve the chu cho video kinishinai (他人の目を気にしない心理学) ra PNG 1920x1080.

Chep khung tu youtube-jp-yawa/tools/make_cards.py (co chu TU CO theo be rong — audience-45plus §2.0e),
doi sang bo mau kenh (navy + xanh thep + am be, NEN SANG — audience-45plus §1 gate 6) va them loai the:
  chapter  ["その一", "「すみません」"]
  stat     [cau tren, SO TO (font ve — khong giao AI), cau duoi/nguon]
  swap     [cau cu (gach), cau moi]            — the "noi lai", moi muc mot the
  seven    open=N, lines=[tieu de 2 dong]      — 7 o khau khuoc; o > N hien 「？」 (dem so, giu chan)
  asch     [tieu de, nguon]                    — so do thi nghiem do dai doan thang
  people   n, hit, lines=[cau, SO TO]          — N hinh nguoi, hit to mau
  concept  [thuat ngu, nguon]
  two      [trai1, trai2, trai-ket, phai1, phai2, phai-ket]
  quote    [dong...]                           — loi thoai quan trong tren giay
Entry "reveal": {"lines","times"} + "_dur" -> clips/clip_NN.mp4 (chi dung khi da co timeline.json);
  --preview ve ban TINH cua the reveal ra _plan/cards_preview/ de duyet truoc.
Vung an toan: x 160..1760, y 110..790 (duoi = dai phu de).
Chay: python tools/make_cards_k.py 01_kuchiguse-hitonome [--only 12,27] [--preview]
"""
import sys, io, json, argparse, re, importlib.util
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 160, 1760, 110, 790
MINCHO = "C:/Windows/Fonts/yumindb.ttf"
GOTHIC = "C:/Windows/Fonts/YuGothB.ttc"
# 2026-10-02: doi sang tong KEM AM cua lop minh hoa 絵本 (ban xanh-xam cu: tools/_make_cards_k_bluegrey.py.bak)
# nen giay kem · quang vang o giua · chu nau dam · nhan nau-cam (bien BLUE giu ten cho khoi doi code ve)
TOP, BOT = (250, 244, 232), (238, 226, 205)
GLOW = (252, 236, 205)
INK, BLUE, CORAL, GREY = (74, 52, 38), (176, 104, 52), (196, 78, 60), (172, 158, 140)
CX = (SAFE_X0 + SAFE_X1) / 2


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", size)


def wrap(text, fnt, maxw, draw):
    out, cur = [], ""
    tokens = [t for t in re.findall(r"[^、。」]*[、。」]?", text) if t]
    for t in tokens:
        if draw.textlength(cur + t, font=fnt) <= maxw:
            cur += t; continue
        if cur:
            out.append(cur); cur = ""
        while draw.textlength(t, font=fnt) > maxw:
            k = len(t)
            while k > 1 and draw.textlength(t[:k], font=fnt) > maxw:
                k -= 1
            out.append(t[:k]); t = t[k:]
        cur = t
    if cur:
        out.append(cur)
    return out


def fit(texts, path, start, minsize, maxw, maxh, gap=1.5):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for size in range(start, minsize - 1, -2):
        f = font(path, size)
        lines = [ln for t in texts for part in t.split("／") for ln in wrap(part, f, maxw, d)]
        if len(lines) * size * gap <= maxh and all(d.textlength(l, font=f) <= maxw for l in lines):
            return f, size, lines
    raise SystemExit(f"[LOI] khong vua khung ngay ca co {minsize}: {texts}")


_BG = None
def bg():
    global _BG
    if _BG is None:
        im = Image.new("RGB", (W, H), TOP); d = ImageDraw.Draw(im)
        for y in range(H):
            k = y / (H - 1)
            d.line((0, y, W, y), fill=tuple(int(TOP[i] * (1 - k) + BOT[i] * k) for i in range(3)))
        glow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(glow).ellipse((W * 0.22, H * 0.08, W * 0.78, H * 0.78), fill=150)
        glow = glow.filter(ImageFilter.GaussianBlur(180))
        _BG = Image.composite(Image.new("RGB", (W, H), GLOW), im, glow)
    return _BG.copy()


def text_c(d, s, f, color, cx, y):
    d.text((cx - d.textlength(s, font=f) / 2, y), s, font=f, fill=color)


def block(d, lines, f, size, color, cx, y0, y1, gap=1.5):
    lh = size * gap
    y = (y0 + y1) / 2 - lh * len(lines) / 2 + (lh - size) / 2
    for ln in lines:
        text_c(d, ln, f, color, cx, y); y += lh
    return y


def rbox(d, xy, fill, outline=None, width=3, r=28):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def person(d, cx, cy, s, color):
    d.ellipse((cx - s * 0.32, cy - s, cx + s * 0.32, cy - s * 0.36), fill=color)
    d.pieslice((cx - s * 0.62, cy - s * 0.28, cx + s * 0.62, cy + s * 0.95), 180, 360, fill=color)


def card(spec):
    typ, L = spec["type"], spec.get("lines", [])
    im = bg(); d = ImageDraw.Draw(im)
    maxw = SAFE_X1 - SAFE_X0 - 120
    if typ == "chapter":
        f0 = font(GOTHIC, 70)
        text_c(d, L[0], f0, BLUE, CX, 230)
        d.line((CX - 70, 335, CX + 70, 335), fill=BLUE, width=4)
        f, size, ls = fit([L[1]], GOTHIC, 128, 64, maxw, 360)
        block(d, ls, f, size, INK, CX, 380, 740)
    elif typ == "stat":
        f1, s1, l1 = fit([L[0]], GOTHIC, 58, 40, maxw, 90)
        block(d, l1, f1, s1, INK, CX, 180, 290)
        f2, s2, l2 = fit([L[1]], GOTHIC, 150, 72, maxw, 260)
        block(d, l2, f2, s2, BLUE, CX, 320, 600)
        d.line((CX - 260, 640, CX + 260, 640), fill=GREY, width=2)
        f3, s3, l3 = fit([L[2]], GOTHIC, 46, 32, maxw, 80)
        block(d, l3, f3, s3, GREY if L[2][:1].isascii() or "より" in L[2] else INK, CX, 660, 740)
    elif typ == "swap":
        rbox(d, (SAFE_X0 + 60, 150, SAFE_X1 - 60, 360), fill=(250, 250, 252), outline=GREY, width=2)
        f1, s1, l1 = fit([f"「{L[0]}」"], GOTHIC, 78, 44, maxw - 120, 170)
        yb = block(d, l1, f1, s1, GREY, CX, 160, 350)
        for k, ln in enumerate(l1):            # gach ngang cau cu
            wln = d.textlength(ln, font=f1); lh = s1 * 1.5
            ymid = (160 + 350) / 2 - lh * len(l1) / 2 + (lh - s1) / 2 + k * lh + s1 * 0.55
            d.line((CX - wln / 2 - 10, ymid, CX + wln / 2 + 10, ymid), fill=CORAL, width=6)
        # mui ten
        d.polygon([(CX - 46, 395), (CX + 46, 395), (CX, 465)], fill=BLUE)
        d.rectangle((CX - 14, 372, CX + 14, 400), fill=BLUE)
        rbox(d, (SAFE_X0 + 20, 495, SAFE_X1 - 20, 770), fill=(255, 255, 255), outline=BLUE, width=5)
        f2, s2, l2 = fit([f"「{L[1]}」"], GOTHIC, 110, 56, maxw - 60, 240)
        block(d, l2, f2, s2, INK, CX, 505, 760)
    elif typ == "seven":
        from_plan = SEVEN
        n_open = spec.get("open", 0)
        f0, s0, l0 = fit(L, GOTHIC, 64, 40, maxw, 170)
        block(d, l0, f0, s0, INK, CX, 110, 280)
        pos = [(0, 0), (1, 0), (2, 0), (3, 0), (0.5, 1), (1.5, 1), (2.5, 1)]
        bw, bh, gx, gy = 350, 170, 30, 34
        x0 = CX - (4 * bw + 3 * gx) / 2
        for i, (cxk, ry) in enumerate(pos):
            x = x0 + cxk * (bw + gx); y = 340 + ry * (bh + gy)
            opened = i < n_open
            last = (i == 6)
            fill = (255, 255, 255) if opened else (242, 232, 216)
            outline = CORAL if (last and n_open == 7) else (BLUE if opened else GREY)
            rbox(d, (x, y, x + bw, y + bh), fill=fill, outline=outline, width=4, r=22)
            fn = font(GOTHIC, 34)
            text_c(d, ["その一", "その二", "その三", "その四", "その五", "その六", "その七"][i], fn,
                   BLUE if opened else GREY, x + bw / 2, y + 16)
            if opened:
                fi, si, li = fit([f"「{DISP[i]}」"], GOTHIC, 40, 28, bw - 30, bh - 70, gap=1.3)
                block(d, li, fi, si, INK, x + bw / 2, y + 58, y + bh - 8, gap=1.3)
            else:
                text_c(d, "？", font(GOTHIC, 70), GREY, x + bw / 2, y + 62)
    elif typ == "asch":
        f0, s0, l0 = fit([L[0]], GOTHIC, 60, 40, maxw, 80)
        block(d, l0, f0, s0, INK, CX, 105, 185)
        # nhan TREN khung, doan thang nam gon TRONG khung (day chung y=660)
        fs = font(GOTHIC, 40)
        text_c(d, "この線と", fs, GREY, 560, 215)
        text_c(d, "同じ長さは？", fs, GREY, 1275, 215)
        rbox(d, (330, 280, 790, 700), fill=(255, 255, 255), outline=GREY, width=2)
        rbox(d, (960, 280, 1590, 700), fill=(255, 255, 255), outline=GREY, width=2)
        ybot, ref = 660, 280
        d.line((560, ybot - ref, 560, ybot), fill=INK, width=14)
        for x, ln, col in [(1080, 200, INK), (1275, ref, BLUE), (1470, 340, INK)]:
            d.line((x, ybot - ln, x, ybot), fill=col, width=14)
        text_c(d, L[1], font(GOTHIC, 36), GREY, CX, 725)
    elif typ == "people":
        n, hit = spec.get("n", 4), spec.get("hit", 3)
        f0, s0, l0 = fit([L[0]], GOTHIC, 58, 40, maxw, 90)
        block(d, l0, f0, s0, INK, CX, 130, 230)
        s = 150; gap = 250
        xs = [CX - gap * (n - 1) / 2 + gap * k for k in range(n)]
        for k, x in enumerate(xs):
            person(d, x, 470, s, CORAL if k < hit else GREY)
        f2, s2, l2 = fit([L[1]], GOTHIC, 140, 70, maxw, 170)
        block(d, l2, f2, s2, BLUE, CX, 600, 780)
    elif typ == "concept":
        f1, s1, l1 = fit([L[0]], MINCHO, 170, 80, maxw, 260)
        block(d, l1, f1, s1, INK, CX, 250, 560)
        d.line((CX - 180, 600, CX + 180, 600), fill=BLUE, width=3)
        text_c(d, L[1], font(GOTHIC, 48), BLUE, CX, 630)
    elif typ == "two":
        for side, (a, b, c) in enumerate([L[0:3], L[3:6]]):
            x0 = 230 + side * 770; x1 = x0 + 690
            col = GREY if side == 0 else BLUE
            rbox(d, (x0, 170, x1, 740), fill=(255, 255, 255), outline=col, width=5)
            cxs = (x0 + x1) / 2
            f1, s1, l1 = fit([a, b], GOTHIC, 66, 40, 600, 220)
            block(d, l1, f1, s1, INK, cxs, 210, 440)
            d.polygon([(cxs - 30, 470), (cxs + 30, 470), (cxs, 515)], fill=col)
            f2, s2, l2 = fit([c], GOTHIC, 92, 50, 620, 150)
            block(d, l2, f2, s2, col if side else (110, 118, 132), cxs, 545, 710)
    elif typ == "quote":
        rbox(d, (SAFE_X0 + 40, 130, SAFE_X1 - 40, 770), fill=(252, 250, 245), outline=(214, 204, 188), width=3, r=18)
        for y in range(230, 740, 96):
            d.line((SAFE_X0 + 110, y + 70, SAFE_X1 - 110, y + 70), fill=(232, 224, 210), width=2)
        f, size, ls = fit(L, MINCHO, 84, 48, maxw - 160, 560, gap=1.55)
        block(d, ls, f, size, INK, CX, 150, 750, gap=1.55)
    elif typ == "reveal_static":
        f, size, ls = fit(L, GOTHIC, 96, 50, maxw, 560, gap=1.6)
        block(d, ls, f, size, INK, CX, SAFE_Y0, SAFE_Y1, gap=1.6)
    else:
        raise SystemExit(f"[LOI] type la: {typ}")
    return im


def reveal_clip(spec, dur, path, fps=30, fade=0.35):
    """Chu hien dan tung dong (khung = the reveal_static): dong DANG doc dam navy, dong da doc diu xam."""
    import subprocess
    import numpy as np
    lines, times = spec["lines"], spec["times"]
    maxw = SAFE_X1 - SAFE_X0 - 120
    f, size, _ = fit(lines, GOTHIC, 96, 50, maxw, 560, gap=1.6)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    rows = [(i, ln) for i, t in enumerate(lines) for ln in wrap(t, f, maxw, d0)]
    lh = size * 1.6
    y0 = (SAFE_Y0 + SAFE_Y1) / 2 - lh * len(rows) / 2 + (lh - size) / 2
    base = np.asarray(bg()).astype(np.float32)
    layers = []
    for i in range(len(lines)):
        m = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(m)
        for k, (j, ln) in enumerate(rows):
            if j == i:
                dm.text((CX - d0.textlength(ln, font=f) / 2, y0 + k * lh), ln, font=f, fill=255)
        layers.append(np.asarray(m).astype(np.float32)[..., None] / 255.0)
    bright, dim = np.array(INK, np.float32), np.array((140, 150, 166), np.float32)
    n = int(round((dur + 0.3) * fps))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
                          "-pix_fmt", "yuv420p", "-crf", "18", str(path)], stdin=subprocess.PIPE)
    last = buf = None
    for fr in range(n):
        t = fr / fps
        key = tuple(round(min(max((t - times[i]) / fade, 0), 1), 2) for i in range(len(lines))) + (sum(t >= x for x in times),)
        if key != last:
            img = base.copy()
            cur = max([i for i in range(len(lines)) if t >= times[i]], default=-1)
            for i, lay in enumerate(layers):
                a = min(max((t - times[i]) / fade, 0), 1)
                if a > 0:
                    col = bright if i == cur else dim
                    img = img * (1 - lay * a) + col * lay * a
            buf = img.clip(0, 255).astype(np.uint8).tobytes(); last = key
        p.stdin.write(buf)
    p.stdin.close(); p.wait()
    return p.returncode


SEVEN = []
# cach hien trong o nho: "／" = cho ngat dong chi dinh (tranh ngat giua tu: 「どう思われるか／しら」)
DISP = ["すみません", "どう思われる／かしら", "みんな、／そうしてるから", "つまらない話で、／ごめんなさいね",
        "こんなこと言ったら、／恥ずかしい", "いい年して", "私さえ、／我慢すれば"]


def main():
    global SEVEN
    ap = argparse.ArgumentParser()
    ap.add_argument("stem")
    ap.add_argument("--only", default="")
    ap.add_argument("--preview", action="store_true", help="ve ca the reveal ban tinh ra _plan/cards_preview/")
    a = ap.parse_args()
    vd = PROJ / "06_VIDEO" / a.stem
    spec = importlib.util.spec_from_file_location("plan", vd / "_plan" / "plan.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    SEVEN = m.SEVEN
    sl = json.load(open(PROJ / "03_SCRIPTS" / f"{a.stem}_SLIDES.json", encoding="utf-8"))
    out = vd / "slides_img"; out.mkdir(parents=True, exist_ok=True)
    clips = vd / "clips"; clips.mkdir(parents=True, exist_ok=True)
    prev = vd / "_plan" / "cards_preview"; prev.mkdir(parents=True, exist_ok=True)
    only = {int(x) for x in a.only.split(",") if x}
    n = nr = npv = 0
    for i, e in enumerate(sl):
        if only and i not in only:
            continue
        if "card" in e:
            im = card(e["card"]); im.save(out / f"slide_{i:02d}.png"); n += 1
            if a.preview:
                im.save(prev / f"slide_{i:02d}.png")
        elif "reveal" in e:
            if a.preview:
                card({"type": "reveal_static", "lines": e["reveal"]["lines"]}).save(prev / f"slide_{i:02d}_reveal.png"); npv += 1
            if e["reveal"].get("times") and "_dur" in e:
                rc = reveal_clip(e["reveal"], e["_dur"], clips / f"clip_{i:02d}.mp4")
                if rc:
                    raise SystemExit(f"[LOI] ffmpeg reveal slide {i} exit {rc}")
                nr += 1
    print(f"ve {n} the -> {out} | {nr} clip chu hien dan | {npv} ban tinh reveal -> {prev}")
    if not nr:
        print("(clip chu hien dan chua dung: can times + _dur tu timeline.json sau khi render voice)")


if __name__ == "__main__":
    main()
