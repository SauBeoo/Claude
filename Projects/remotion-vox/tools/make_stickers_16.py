# -*- coding: utf-8 -*-
r"""make_stickers_16.py — sinh TOAN BO asset sticker cho video 16, chay lai duoc.

    py -3 tools/make_stickers_16.py [--src "C:\...\download (7)"]

Lam 3 viec, theo dung thu tu:
  1. VE LAI KIM DONG HO ve 5:00. Anh user gen ra ~12:10, nhung bai doc
     「時計で言えば、四時から六時ごろ」 -> de nguyen la anh CHOI voi loi doc.
     Mat so la dia trang phang + 2 kim den -> xoa kim cu bang chinh mau dia roi
     ve lai, khong can inpaint gi phuc tap.
  2. CAT NEN kieu HINH GIAY (user chot 2026-08-16: "cat ra thanh hinh giay"):
     process_cutout.py --edge 12 -> vien trang chay quanh silhouette nhu cat keo.
     🔴 PHAI truyen --model isnet-general-use: u2net mac dinh giu 100% dien tich
        o anh chup canh; o anh nen trang thi u2net cung duoc, nhung dung MOT model
        cho ca lo de vien deu nhau.
  3. VE PANEL nen (navy + vien vang theo palette kenh) cho khoi recap.

Xuat thang vao public/projects/shokutaku-16-banana/assets/.
Chay xong -> `py -3 tools/add_overlays_16.py` de gan vao project.json.
"""
import argparse
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "projects"  # placeholder, real path below
OUT = ROOT / "public" / "projects" / "shokutaku-16-banana" / "assets"
CUTOUT = Path(r"E:\Claude\.claude\skills\vox-collage-video\scripts\process_cutout.py")

SRC_DEFAULT = Path(r"C:\Users\tuana\Downloads\download (7)")
SRC = {
    "banana": "Yellow_banana_on_white_background_202608162206.jpeg",
    "mugicha": "Ceramic_teacup_filled_with_tea_202608162206.jpeg",
    "zabuton": "Plain_folded_floor_cushion_202608162206.jpeg",
    "tokei": "Twin-bell_alarm_clock_standing_202608162206.jpeg",
}

# do bang mat tren anh goc 1376x768 (out/_clockface.png)
DIAL_CX, DIAL_CY, DIAL_R = 685, 445, 172
SET_HOUR, SET_MIN = 5, 0          # 5:00 — giua dai 「四時から六時」


def redraw_clock(src: Path, dst: Path):
    im = Image.open(src).convert("RGB")
    px = im.load()
    # mau dia: trung binh mot vanh sach trong dia (tranh kim + vach so)
    sam = [px[DIAL_CX + int(DIAL_R * 0.55 * math.cos(a)),
              DIAL_CY + int(DIAL_R * 0.55 * math.sin(a))]
           for a in [0.6, 1.2, 2.4, 3.6, 4.2, 5.4]]
    face = tuple(sum(c[i] for c in sam) // len(sam) for i in range(3))

    # 1. xoa kim cu — TRUNG VI TUNG HANG, khong phai nguong cung.
    # 🔴 Nguong cung (<150) de sot BONG MA: mep khu rang cua + phan sang cua kim cu
    #    khong du toi nen song sot, thanh vet xam nhat chi sang 2 gio (thay o
    #    out/_dial.png vong 1). Trung vi hang vua xoa sach vua GIU sac do doc cua
    #    dia (dia co bong nhe o tren), fill phang se lo ra.
    import statistics
    for y in range(DIAL_CY - DIAL_R, DIAL_CY + DIAL_R):
        half = int((DIAL_R * 0.93) ** 2 - (y - DIAL_CY) ** 2)
        if half <= 0:
            continue
        half = int(math.sqrt(half))
        xs = range(DIAL_CX - half, DIAL_CX + half)
        vals = [sum(px[x, y]) / 3 for x in xs]
        if not vals:
            continue
        med = statistics.median(vals)
        rowcol = [px[x, y] for x, v in zip(xs, vals) if v >= med - 3]
        fill = (tuple(sum(c[i] for c in rowcol) // len(rowcol) for i in range(3))
                if rowcol else face)
        for x, v in zip(xs, vals):
            if v < med - 3:          # bat ca bong ma nhat, khong chi kim den
                px[x, y] = fill

    # 2. ve kim moi
    d = ImageDraw.Draw(im)

    def hand(angle_deg, length, width):
        a = math.radians(angle_deg - 90)          # 0deg = 12 gio
        x2 = DIAL_CX + length * math.cos(a)
        y2 = DIAL_CY + length * math.sin(a)
        d.line([(DIAL_CX, DIAL_CY), (x2, y2)], fill=(24, 24, 24), width=width)
        d.ellipse([x2 - width / 2, y2 - width / 2, x2 + width / 2, y2 + width / 2],
                  fill=(24, 24, 24))

    hand(SET_MIN * 6, DIAL_R * 0.74, 11)                       # kim phut
    hand((SET_HOUR % 12) * 30 + SET_MIN * 0.5, DIAL_R * 0.50, 14)   # kim gio
    d.ellipse([DIAL_CX - 15, DIAL_CY - 15, DIAL_CX + 15, DIAL_CY + 15], fill=(20, 20, 20))
    im.save(dst, quality=96)
    print(f"  dong ho -> {SET_HOUR}:{SET_MIN:02d}  (mau dia {face})")


def panel(dst: Path, w=1520, h=340, r=38):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=(24, 34, 54, 214))
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=(255, 215, 0, 90), width=3)
    im.save(dst)
    print(f"  panel {w}x{h}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(SRC_DEFAULT))
    ap.add_argument("--edge", type=int, default=12, help="do day vien giay (px)")
    a = ap.parse_args()
    src = Path(a.src)
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT.parent / "_tmp_clock.jpg"

    missing = [v for v in SRC.values() if not (src / v).exists()]
    if missing:
        print("[LOI] thieu file nguon:", missing); return 1

    print("1. ve lai kim dong ho")
    redraw_clock(src / SRC["tokei"], tmp)

    print(f"2. cat nen kieu hinh giay (--edge {a.edge}, model isnet-general-use)")
    pairs = []
    for key in ("banana", "mugicha", "zabuton"):
        pairs += [str(src / SRC[key]), str(OUT / f"stk_{key}.png")]
    pairs += [str(tmp), str(OUT / "stk_tokei.png")]
    r = subprocess.run([sys.executable, str(CUTOUT), *pairs,
                        "--edge", str(a.edge), "--margin", "18", "--max-dim", "700",
                        "--model", "isnet-general-use"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    for ln in (r.stdout or "").splitlines():
        if ".png:" in ln or "🔴" in ln:
            print("  " + ln.strip())
    if r.returncode != 0:
        print("[LOI] cutout that bai"); print((r.stderr or "")[-400:]); return 1

    print("3. panel nen")
    panel(OUT / "stk_panel.png")
    tmp.unlink(missing_ok=True)
    print(f"\nOK -> {OUT.relative_to(ROOT)}")
    print("Tiep: py -3 tools/add_overlays_16.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
