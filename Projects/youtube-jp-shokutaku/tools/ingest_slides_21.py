# -*- coding: utf-8 -*-
r"""Nhap MINH HOA AI user gen -> slides_img_photo/slide_XX.jpg (video 21, khung san khau).

    python tools\ingest_slides_21.py "C:\Users\tuana\Downloads\<folder>"            # xem thu
    python tools\ingest_slides_21.py <src> --cut-x 1250 --apply                     # ghi that
    python tools\ingest_slides_21.py <src> --no-cut --apply                         # lo sach ✦
    python tools\ingest_slides_21.py --restore                                      # tra ban goc

Sao chep tu ingest_slides_20.py (cung khung san khau, cung ham make_stage) — CHI doi
VD, POSE_MAP, CHIP_MAP cho dung noi dung video 21 (もち麦 × もう一つの台所). Doc lai
chu thich day du o ingest_slides_20.py neu can hieu co che (stage_base/put_cast/sub_bar,
watermark ✦ theo LO, cover-crop tu lui ve fit khi mat >12% noi dung, v.v.) — khong
chep lai o day de tranh 2 ban giai thich lech nhau (bai hoc `stage-zu-layout.md` §4).

⭐ AN DU RIENG cua video nay: khung san khau (the trang bo goc) DA chinh la "hanh lang
bep" trong minh hoa — cast minori/kikite dan 2 ben the giong moi video khac, KHONG can
sua gi them o buoc nay.

CAN TRUOC KHI CHAY: ma tran ghep ten file <-> slot (`_map.json`) phai duyet bang MAT
truoc (xem loi 🔴 THIEU _map.json neu chua co).
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
VD = ROOT / "06_VIDEO" / "21_mochimugi-choukatsu"
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

# ⭐ POSE_MAP — doi tu the theo tung doan bai. Index = so trong ten file slide_NN.jpg,
# tuc chinh la vi tri (0-based) cua entry trong PLAN cua build_slides_21.py — doi chieu
# bang cot dau tien cua slide_prompts_TENFILE.txt.
POSE_MAP = [
    (0,  "minori_talk",  "kikite_worried"),    # cold open: nghich ly can nang
    (4,  "minori_point", "kikite_listen"),     # ITEM1: dai trang la hanh lang bep
    (9,  "minori_smile", "kikite_surprised"),  # hero: もち麦 duoc goi ten
    (11, "minori_point", "kikite_note"),       # so lieu: 20g/17g/12g/3:1
    (14, "minori_hold",  "kikite_nod"),        # dai muong dong doc
    (15, "minori_smile", "kikite_listen"),     # persona みのり
    (16, "minori_talk",  "kikite_relieved"),   # みのり tu thu
    (18, "minori_point", "kikite_nod"),        # co che mien dich / duong huyet
    (22, "minori_talk",  "kikite_listen"),     # case 恵子さん Toyama
    (26, "minori_smile", "kikite_relieved"),   # 恵子さん nhe nguoi
    (27, "minori_smile", "kikite_nod"),        # CTA giua
    (28, "minori_stop",  "kikite_worried"),    # canh bao than/kali
    (30, "minori_stop",  "kikite_worried"),    # NG habit — van de
    (33, "minori_point", "kikite_surprised"),  # TRA LOOP: an qua nhieu ngay dau
    (34, "minori_hold",  "kikite_nod"),        # thang bac 1 tuan tang dan
    (37, "minori_talk",  "kikite_listen"),     # case 正雄さん Akita
    (41, "minori_smile", "kikite_relieved"),   # 正雄さん khong con cam lanh
    (42, "minori_smile", "kikite_nod"),        # recap
    (47, "minori_smile", "kikite_relieved"),   # ket + disclaimer
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

STOP = {"a", "an", "the", "of", "on", "in", "at", "and", "with", "to", "from", "by",
        "one", "two", "three", "its", "their", "for", "into", "over", "under",
        "beside", "next", "up", "down", "small", "large", "red", "white", "soft"}


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


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


# ⭐ Chip nhan doan + dau nhan — ve bang font Noto (make_stage.F), KHONG bake bang AI
# (chu Nhat AI hay nat — media-library.md §2.9). Index = so trong ten file slide_NN.jpg.
CHIP_MAP = [
    (0,  "体重のなぞ",           "warn"),
    (4,  "① 大腸という台所",     "num"),
    (9,  "② もち麦という材料",   "num"),
    (11, "食物繊維の目標量",     None),
    (14, "大さじ一杯から",       "ok"),
    (15, "案内人・みのり",       None),
    (16, "続けやすさのコツ",     "ok"),
    (18, "免疫との関係",         "ok"),
    (22, "富山県・恵子さんの話", None),
    (26, "二週間後の変化",       "ok"),
    (27, "応援のお願い",         None),
    (28, "腎臓・お薬の方へ",     "warn"),
    (30, "③ 続かない本当の理由", "num"),
    (33, "答え：一気に食べ過ぎ", "warn"),
    (34, "一週間ごとに増やす",   "ok"),
    (37, "秋田県・正雄さんの話", None),
    (42, "まとめ",               "ok"),
    (47, "今夜の食卓から",       None),
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
                    help="dung lai tu backup _wm_orig/ — dung khi Downloads da bi don, "
                         "hoac khi chi doi khung/cast")
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
        print(f"   Gen 12 anh theo cast_prompts_FLOW.txt → cutout_cast.py --apply → "
              f"chay lai lenh nay.")
    else:
        hs = [cast_img(c) for c in need]
        ws = [i.width for i in hs if i]
        print(f"✅ CAST {len(need)}/{len(need)} (dung lai bo co san cua kenh, khong gen "
              f"moi) · dau ep {HEAD_PX}px, cao {CAST_H}px · rong {min(ws)}-{max(ws)}px")
        print(f"   doi tu the {len(POSE_MAP)} lan · chip nhan {len(CHIP_MAP)} doan")
        if BROKEN:
            print(f"⚠️ {len(BROKEN)} cast dang bi THAY TAM: "
                  + ", ".join(f"{k}→{v}" for k, v in BROKEN.items()))
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
          "chu (3種類 もち麦 12g 3:1 大さじ1 2週間 一週目 秋田県 12月 …) — sai net la gen "
          "lai, khong sua tay.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
