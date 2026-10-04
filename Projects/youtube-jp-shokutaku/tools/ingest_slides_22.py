# -*- coding: utf-8 -*-
r"""Nhap MINH HOA AI user gen -> slides_img_photo/slide_XX.jpg (video 22, khung san khau).

    python tools\ingest_slides_22.py "C:\Users\tuana\Downloads\download (1)"          # xem thu
    python tools\ingest_slides_22.py "C:\Users\tuana\Downloads\download (1)" --cut-x 1250 --apply
    python tools\ingest_slides_22.py "C:\Users\tuana\Downloads\download (1)" --no-cut --apply
    python tools\ingest_slides_22.py --restore

Sao chep tu ingest_slides_21.py (cung khung san khau, cung ham make_stage) — CHI doi
VD, POSE_MAP, CHIP_MAP cho dung noi dung video 22 (ラーメン x 水道管を守る). Doc lai
chu thich day du o ingest_slides_20.py neu can hieu co che.

⭐ AN DU RIENG cua video nay: duong ong nuoc (血管) la an du TRUNG TAM chay xuyen
suot 9 slide (05-06-07-08-20-23-35-37-49) — khung san khau + cast KHONG dung cham
gi vao no, chi dan minori/kikite 2 ben the nhu moi video khac.

CAN TRUOC KHI CHAY: `_map.json` DA duyet bang MAT va ghi san (ten file <-> slot).
"""
import argparse
import io
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, r"E:\Claude\Projects\_media_library")
import make_stage as MS                                                    # noqa: E402

sys.stdout = io.TextIOWrapper(io.FileIO(1, "w"), encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "22_ramen-kekkan"
IMG = VD / "slides_img_photo"
ORIG = VD / "_wm_orig"

CARD = (MS.CARD_X0, MS.CARD_Y0, MS.CARD_X1, MS.CARD_Y1)
CW, CH = MS.CARD_X1 - MS.CARD_X0, MS.CARD_Y1 - MS.CARD_Y0

MS.CAST = ROOT / "assets" / "cast"

HEAD_PX = 200
CAST_H = 416
CAST_GAP = 8
HEAD_W_OVER_H = 0.72
CAST_W_MAX = 360

# ⭐ POSE_MAP — doi tu the theo tung doan bai. Index = so trong ten file slide_NN.jpg
# (doi chieu cot dau tien cua slide_prompts_TENFILE.txt).
POSE_MAP = [
    (0,  "minori_talk",  "kikite_worried"),    # cold open: mui, tay/mat kho chiu
    (5,  "minori_point", "kikite_listen"),     # gioi thieu duong ong (con mo)
    (9,  "minori_point", "kikite_note"),       # bang so lieu thuc te 7.5g/6.5g
    (12, "minori_talk",  "kikite_surprised"),  # 6-8g mot bat vuot ca ngay
    (14, "minori_hold",  "kikite_nod"),        # tuc: tuoi giam
    (15, "minori_stop",  "kikite_worried"),    # NG: cho com vao nuoc con lai
    (17, "minori_smile", "kikite_nod"),        # つけ麺
    (18, "minori_smile", "kikite_listen"),     # persona みのり
    (19, "minori_stop",  "kikite_worried"),    # canh bao thuoc huyet ap/mo mau
    (20, "minori_point", "kikite_listen"),     # quay lai duong ong — muc 2
    (23, "minori_talk",  "kikite_nod"),        # ong tac vi mo
    (24, "minori_point", "kikite_note"),       # so sanh 3 loai ramen
    (28, "minori_talk",  "kikite_listen"),     # case 正治さん Mie
    (32, "minori_talk",  "kikite_surprised"),  # 正治さん bat ngo
    (33, "minori_smile", "kikite_relieved"),   # 正治さん hai long
    (34, "minori_smile", "kikite_nod"),        # CTA giua
    (35, "minori_point", "kikite_listen"),     # quay lai duong ong — muc 3
    (37, "minori_talk",  "kikite_worried"),    # ong ri set vi duong huyet
    (41, "minori_point", "kikite_note"),       # recap 3 cai bay
    (42, "minori_talk",  "kikite_listen"),     # cho tra loop
    (43, "minori_smile", "kikite_surprised"),  # tra loop: 半分
    (44, "minori_smile", "kikite_nod"),        # みのり tu thu nghiem
    (45, "minori_talk",  "kikite_listen"),     # case 幸子さん Yamagata
    (48, "minori_smile", "kikite_relieved"),   # 幸子さん hanh phuc
    (49, "minori_smile", "kikite_relieved"),   # duong ong sach — ket qua
    (53, "minori_talk",  "kikite_listen"),     # disclaimer
    (54, "minori_smile", "kikite_relieved"),   # ket bai
]

BROKEN: dict[str, str] = {}


def pose_for(idx):
    left, right = POSE_MAP[0][1], POSE_MAP[0][2]
    for start, l, r in POSE_MAP:
        if idx >= start:
            left, right = l, r
    return BROKEN.get(left, left), BROKEN.get(right, right)


_CAST = {}


def cast_img(name):
    if name in _CAST:
        return _CAST[name]
    p = MS.CAST / f"{name}.png"
    if not p.exists():
        _CAST[name] = None
        return None
    im = Image.open(p).convert("RGBA")
    al = np.asarray(im)[:, :, 3] > 60
    w = al.sum(axis=1)
    ys = np.flatnonzero(w > 0)
    y0, y1 = int(ys[0]), int(ys[-1])
    h = y1 - y0 + 1
    band = w[y0 + int(h * 0.06): y0 + int(h * 0.14)]
    head = float(np.median(band[band > 0])) / HEAD_W_OVER_H
    sc = HEAD_PX / max(head, 1)
    if im.width * sc > CAST_W_MAX:
        sc = CAST_W_MAX / im.width
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))),
                   Image.LANCZOS)
    top = int(y0 * sc)
    im = im.crop((0, top, im.width, min(im.height, top + CAST_H)))
    _CAST[name] = im
    return im


def put_cast_flush(base, name, side):
    ch = cast_img(name)
    if ch is None:
        return
    if side == "left":
        x = max(0, MS.CARD_X0 - CAST_GAP - ch.width)
    else:
        x = min(MS.W - ch.width, MS.CARD_X1 + CAST_GAP)
    base.alpha_composite(ch, dest=(int(x), MS.SUB_Y0 - ch.height))


BORDER = 5


def trim_border(im, px=BORDER):
    if im.width <= 2 * px or im.height <= 2 * px:
        return im
    im = im.crop((px, px, im.width - px, im.height - px))

    g = np.asarray(im.convert("L")).astype(int)
    ink = (g < 245).mean(axis=1)
    rows = np.flatnonzero(ink >= 0.01)
    if rows.size == 0:
        return im
    b = int(rows[-1])
    if im.height - 1 - b < 20:
        return im
    top = b
    while top > 0 and ink[top - 1] >= 0.01:
        top -= 1
    if b - top <= 6 and (top == 0 or ink[top - 1] < 0.01):
        b = top - 1
    return im.crop((0, 0, im.width, max(b + 1, 1)))


def edge_step(im):
    a = np.asarray(im.convert("L")).astype(float)
    profs = ([a[:, i].mean() for i in range(6)], [a[:, -1 - i].mean() for i in range(6)],
             [a[i, :].mean() for i in range(6)])
    return max(p[i + 1] - p[i] for p in profs for i in range(4))


# ⭐ Chip nhan doan + dau nhan — ve bang font Noto (make_stage.F), KHONG bake bang AI.
CHIP_MAP = [
    (0,  "ラーメンと水道管",     "warn"),
    (5,  "① 塩：管が硬くなる",  "num"),
    (9,  "厚労省の目安",         None),
    (12, "汁だけで一日分",       "warn"),
    (14, "汁は半分でOK",         "ok"),
    (18, "案内人・みのり",       None),
    (19, "腎臓・お薬の方へ",     "warn"),
    (20, "② 脂：管が詰まる",    "num"),
    (28, "三重県・正治さんの話", None),
    (34, "応援のお願い",         None),
    (35, "③ 糖：管がサビる",    "num"),
    (41, "3つの落とし穴",        "num"),
    (43, "答え：ひと言だけ",     "ok"),
    (45, "山形県・幸子さんの話", None),
    (49, "3つの守り方",          "ok"),
    (54, "今夜の食卓から",       None),
]
CHIP_BG = (58, 74, 104)
CHIP_FG = (255, 255, 255)
MARK = {"warn": ("！", (226, 92, 60)), "ok": ("✓", (76, 152, 106)),
        "num": ("＋", (206, 148, 46))}

_MASK = None


def card_mask():
    global _MASK
    if _MASK is None:
        _MASK = Image.new("L", (CW, CH), 0)
        ImageDraw.Draw(_MASK).rounded_rectangle([0, 0, CW - 1, CH - 1], 28, fill=255)
    return _MASK


def cover_loss(im):
    sc = max(CW / im.width, CH / im.height)
    cut = int(max(0, (int(im.width * sc) - CW) / 2 / sc))
    if cut < 1:
        return 0.0
    ink = np.asarray(im.convert("L")).astype(int) < 245
    tot = ink.sum()
    if not tot:
        return 0.0
    return float((ink[:, :cut].sum() + ink[:, im.width - cut:].sum()) / tot)


LOSS_MAX = 0.12


def chip_for(idx):
    cur = CHIP_MAP[0]
    for row in CHIP_MAP:
        if idx >= row[0]:
            cur = row
    return cur[1], cur[2]


def draw_chip(base, idx):
    label, mark = chip_for(idx)
    d = ImageDraw.Draw(base)
    f = MS.fit(label, "bold", 470, 40, 26)
    tb = d.textbbox((0, 0), label, font=f)
    tw_, th_ = tb[2] - tb[0], tb[3] - tb[1]
    px, py = 22, 13
    x0, y0 = MS.CARD_X0 + 26, MS.CARD_Y0 + 24
    x1, y1 = x0 + tw_ + px * 2, y0 + th_ + py * 2
    d.rounded_rectangle([x0, y0, x1, y1], (th_ + py * 2) // 2, fill=CHIP_BG)
    d.text((x0 + px - tb[0], y0 + py - tb[1]), label, font=f, fill=CHIP_FG)
    if mark:
        ch, col = MARK[mark]
        r = (y1 - y0) // 2
        cx, cy = x1 + 18 + r, (y0 + y1) // 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        d.text((cx, cy + 1), ch, font=MS.F("black", int(r * 1.15)),
               fill=(255, 255, 255), anchor="mm")


def stage_canvas(im, idx=0):
    art = trim_border(im.convert("RGB"))
    if cover_loss(art) <= LOSS_MAX:
        sc = max(CW / art.width, CH / art.height)
        art = art.resize((max(1, int(art.width * sc)), max(1, int(art.height * sc))),
                         Image.LANCZOS)
        art = art.crop(((art.width - CW) // 2, (art.height - CH) // 2,
                        (art.width - CW) // 2 + CW, (art.height - CH) // 2 + CH))
        lay = art
    else:
        art.thumbnail((CW, CH), Image.LANCZOS)
        lay = Image.new("RGB", (CW, CH), MS.CARDC)
        lay.paste(art, ((CW - art.width) // 2, (CH - art.height) // 2))

    base = MS.stage_base()
    base.paste(lay, (MS.CARD_X0, MS.CARD_Y0), card_mask())
    draw_chip(base, idx)
    left, right = pose_for(idx)
    put_cast_flush(base, left, "left")
    put_cast_flush(base, right, "right")
    MS.sub_bar(base)
    return base.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", action="store_true")
    ap.add_argument("--cut-x", type=int, default=None,
                    help="cat mep phai tai x nay de bo ✦ (soi MAT theo LO roi truyen)")
    ap.add_argument("--no-cut", action="store_true",
                    help="lo da soi mat KHONG co ✦ — bo qua buoc cat")
    ap.add_argument("--slots", help="chi nhap slot chi dinh, vd slide_10.jpg,slide_64.jpg")
    ap.add_argument("--from-orig", action="store_true",
                    help="dung lai tu backup _wm_orig/")
    a = ap.parse_args()

    if a.restore:
        n = 0
        for f in sorted(ORIG.glob("*")):
            shutil.copy2(f, IMG / f.name)
            n += 1
        print(f"restore {n} anh tu _wm_orig/")
        return 0
    if not a.src and not a.from_orig:
        print("thieu folder nguon (hoac dung --from-orig de dung lai tu _wm_orig)")
        return 1
    if a.cut_x is None and not a.no_cut:
        print("🔴 THIEU --cut-x: soi MAT goc duoi-phai 5-8 anh cua LO nay roi truyen "
              "--cut-x <mep trai ✦ - 15>, hoac --no-cut neu lo sach.\n"
              "   (toa do ✦ doi theo LO — media-library.md §2.10 ⑤, cam be so lo cu)")
        return 1

    flow = (VD / "slide_prompts_FLOW.txt").read_text(encoding="utf-8").splitlines()
    tenfile = (VD / "slide_prompts_TENFILE.txt").read_text(encoding="utf-8").splitlines()[1:]
    slots = []
    for line, tf in zip(flow, tenfile):
        m = re.search(r"SUBJECT: (.*?)\. (?:TEXT|STYLE)", line)
        parts = tf.split("\t")
        slots.append({"name": parts[0], "subj": m.group(1) if m else "",
                      "moc": parts[1], "text": parts[2].strip()})
    if a.slots:
        keep = {s.strip() for s in a.slots.split(",")}
        slots = [s for s in slots if s["name"] in keep]
        if len(slots) != len(keep):
            print(f"⚠️ chi tim thay {len(slots)}/{len(keep)} slot chi dinh")

    if a.from_orig:
        plan = []
        for s in slots:
            stem = Path(s["name"]).stem
            hit = next((p for p in sorted(ORIG.glob(stem + ".*"))), None)
            plan.append((s, hit, 1.0))
        print(f"nguon: _wm_orig ({sum(1 for _s, p, _x in plan if p)} anh) | "
              f"slot can: {len(slots)}\n")
    else:
        srcs = sorted(Path(a.src).glob("*.jpe*g")) + sorted(Path(a.src).glob("*.png"))
        print(f"nguon: {len(srcs)} anh | slot can: {len(slots)}\n")

        import json as _json
        mapf = VD / "_map.json"
        if not mapf.exists():
            print("🔴 THIEU _map.json — ghep ten file <-> slot phai duyet bang MAT truoc.")
            return 1
        mp = _json.loads(mapf.read_text(encoding="utf-8"))
        by_name = {p.name: p for p in srcs}
        plan = []
        for s in slots:
            n = int(re.search(r"slide_(\d+)", s["name"]).group(1))
            fn = mp.get(str(n))
            plan.append((s, by_name.get(fn), 1.0 if fn in by_name else 0.0))

    miss = [s["name"] for s, p, _ in plan if p is None]
    for s, p, sc in plan:
        print(f"{s['name']}  {s['moc']}  {'← ' + p.name[:58] + f' ({sc:.2f})' if p else '🔴 CHUA CO ANH'}")
    if miss:
        print(f"\n🔴 {len(miss)} slot chua co anh: {', '.join(miss[:10])}"
              + (" …" if len(miss) > 10 else ""))
    if not a.apply:
        print("\n(xem thu — them --apply de ghi that; SOI BANG MAT bang ghep tren truoc)")
        return 0

    IMG.mkdir(parents=True, exist_ok=True)
    ORIG.mkdir(parents=True, exist_ok=True)
    n, framed, bands, losses = 0, [], [], []
    for s, p, _ in plan:
        if p is None:
            continue
        im = Image.open(p)
        if not a.from_orig:
            shutil.copy2(p, ORIG / (Path(s["name"]).stem + p.suffix))
        if not a.no_cut:
            if im.width <= a.cut_x:
                print(f"⚠️ {s['name']}: anh rong {im.width} <= cut_x {a.cut_x}, bo qua cat")
            else:
                im = im.crop((0, 0, a.cut_x, im.height))
        cut = trim_border(im.convert("RGB"))
        d = edge_step(cut)
        if d > 12:
            framed.append((s["name"], d))
        bands.append(im.height - 2 * BORDER - cut.height)
        loss = cover_loss(cut)
        if s["text"] != "-" or loss > LOSS_MAX:
            losses.append((s["name"], loss, s["text"]))
        idx = int(re.search(r"(\d+)", s["name"]).group(1))
        stage_canvas(im, idx).save(IMG / s["name"], quality=95)
        n += 1
    print(f"\nghi {n} anh -> {IMG.relative_to(ROOT)} "
          f"(KHUNG SAN KHAU: the {CW}x{CH}@({MS.CARD_X0},{MS.CARD_Y0}) cover-crop, "
          f"dai den tu y={MS.SUB_Y0})")
    need = sorted({c for _s, l, r in POSE_MAP for c in (l, r)})
    miss = [c for c in need if not (MS.CAST / f"{c}.png").exists()]
    if miss:
        print(f"⚠️ CHUA CO CAST {len(miss)}/{len(need)} — khung ra KHONG nhan vat: "
              f"{', '.join(miss)}")
    else:
        hs = [cast_img(c) for c in need]
        ws = [i.width for i in hs if i]
        print(f"✅ CAST {len(need)}/{len(need)} (dung lai bo co san cua kenh, khong gen "
              f"moi) · dau ep {HEAD_PX}px, cao {CAST_H}px · rong {min(ws)}-{max(ws)}px")
        print(f"   doi tu the {len(POSE_MAP)} lan · chip nhan {len(CHIP_MAP)} doan")
    if losses:
        fits = [r for r in losses if r[1] > LOSS_MAX]
        print(f"ⓘ cover-crop: {n - len(fits)}/{n} anh phu TRON the · {len(fits)} anh tu lui "
              f"ve FIT (mat >{LOSS_MAX*100:.0f}% noi dung):")
        for name, lo, txt in sorted(losses, key=lambda r: -r[1])[:12]:
            mode = "FIT " if lo > LOSS_MAX else "cover"
            print(f"      {mode} {name}  mat {lo*100:4.1f}%"
                  + (f"   ← CHU BAKE {txt}" if txt != "-" else ""))
    print(f"    trim vien {BORDER}px moi mep")
    cut_n = sum(1 for b in bands if b > 0)
    if cut_n:
        nz = sorted(b for b in bands if b > 0)
        print(f"    cat dai trang day + duong ke o {cut_n}/{n} anh "
              f"(min {nz[0]}px / trung vi {nz[len(nz)//2]}px / max {nz[-1]}px)")
    if framed:
        print(f"🔴 {len(framed)} anh CON BAC NHAY o mep (vien chua cat het) — nang BORDER:")
        for name, d in framed[:10]:
            print(f"      {name}  bac {d:+.1f}")
    else:
        print(f"✅ GATE VIEN: 0/{n} anh con bac nhay o mep — khong con khung bao")
    print("⚠️ NGHIEM THU: soi 1:1 CA 4 GOC vai anh (✦ sot?) + soi TUNG KY TU cac anh co "
          "chu (7.5g/6.5g 6g 5g 6-8g 1日分 半分 週1 三重県 山形県 3つ) — sai net la gen "
          "lai, khong sua tay.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
