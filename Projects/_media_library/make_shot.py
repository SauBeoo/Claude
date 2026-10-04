# -*- coding: utf-8 -*-
r"""
make_shot.py — BUILD-ON BẰNG HÌNH ẢNH (không phải bằng chữ).
v0.1 · 2026-08-18 (user: "chuyển động kiểu gần như nenkin, nhưng chuyển động bằng hình ảnh")

VÌ SAO CÓ TOOL NÀY
────────────────────────────────────────────────────────────────────────────────
`make_stage.py` (nenkin) chuyển động bằng **build-on**: sân khấu đứng yên, các phần tử
CHỮ/HỘP hiện dần theo lời đọc. Người 60+ nhìn thấy câu trả lời được LẮP RA.
`make_vox.py` (co-dai) cũng build-on, nhưng thứ lắp ra vẫn là chữ + số trên ảnh.

Bệnh còn lại của co-dai: **71/83 entry là ảnh TĨNH đứng yên ~15 giây**. Đó là chỗ chết.
Tool này lấy đúng cơ chế build-on của nenkin và thay nội dung: **thứ hiện dần LÀ HÌNH.**

⛔ KHÔNG PHẢI KEN BURNS. Khung không pan, không zoom (luật `feedback_video_no_motion_mot_giong`
   — user ghét màn hình trôi). Cái động là ẢNH ĐƯỢC LẮP VÀO, y như nenkin lắp chữ.

BA MODE (mỗi mode trả lời một kiểu câu trong script)
────────────────────────────────────────────────────────────────────────────────
  wipe   ẢNH B lộ dần đè lên ẢNH A, đường wipe dọc có vệt sáng
         → câu ĐỔI TRẠNG THÁI: chảo xỉn→bóng · gioăng đen→sạch · tường ướt→khô
  inset  ảnh nền A + một tấm ảnh B (macro) trượt lên 26px + hiện dần, viền trắng đổ bóng,
         rồi mũi tên đỏ vẽ dần từ tấm ảnh tới điểm cần nhìn
         → câu PHÓNG TO MỘT CHI TIẾT: "chỗ này mới là thứ đang xảy ra"
  soft   ảnh đứng, chỉ "thở" ±1,5% sáng — cho câu KỂ, để vòng đỏ không lặp 60 lần
  focus  vòng khoanh đỏ vẽ dần (như bút dạ) + ngoài vòng tối nhẹ 18%
         → câu CHỈ ĐÍCH DANH: "đây, chính chỗ này"

NHỊP (giống make_vox: INTRO 30fps → IDLE loop 4s, hết build-on thì ĐỨNG IM)
  0.00s  ảnh nền có mặt (không fade — nền là sân khấu)
  0.55s  phần tử 1 vào (ảnh B / vòng khoanh)
  1.70s  phần tử 2 vào (mũi tên / vệt wipe kết thúc)
  2.60s  nhãn ngắn (TUỲ CHỌN, ≤10 ký) — mặc định KHÔNG có chữ
  →      đứng im tới hết clip (idle chỉ "thở" ±1,5% sáng, loop sạch)

CHẠY
    python make_shot.py demo <folder_anh> <out_dir> [--channel co-dai]
    python make_shot.py slides <SLIDES.json> <clips_dir> --img-dir <folder_anh> [--still]
"""
import argparse, hashlib, io, json, math, shutil, subprocess, sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

# 🔴 write_through BAT BUOC: TextIOWrapper tu tao la block-buffered => log ra 0 byte
#    suot ca lan chay va nhin nhu treo (bai hoc voice_only.py 2026-08-16)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)

W, H = 1920, 1080
FPS_IN, FPS_IDLE, OUT_FPS = 30, 30, 30
IDLE_SEC = 4.0
CLIP_SEC = 30.0
RED = (224, 58, 58)
SUB_TOP = 678          # safe_bottom co-dai (outline/26): avatar/FX khong duoc xuong duoi
INK = (24, 26, 32)

# ⭐ 2026-08-18 (user: "cai hinh mui ten may co the dung anh tao gen duoc khong?"):
#    bo prop PNG user da gen (props/*.png + INDEX.json) DA CO SAN va make_vox dung no
#    qua prop_arrow/prop_circle/prop_mark. make_shot import lai — KHONG ve vector nua.
#    Thieu prop (kenh khac chua gen) thi tu roi ve duong vector cu.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import make_vox as MV
    HAVE_PROPS = MV.props_ready("arrow_curve", "arrow_straight", "circle_1", "cross_x")
except Exception as _e:          # noqa: BLE001
    MV, HAVE_PROPS = None, False
import shot_fx as FX        # lop FX + avatar (2026-08-18)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def fit_cover(im, w, h):
    """Phủ kín khung, cắt phần thừa — KHÔNG méo."""
    r = max(w / im.width, h / im.height)
    im2 = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    x = (im2.width - w) // 2
    y = (im2.height - h) // 2
    return im2.crop((x, y, x + w, y + h))


def load(p):
    return Image.open(p).convert("RGB")


def crop_at(im, cx, cy, r, w, h):
    """Cắt vùng quanh (cx,cy) bán kính r (đơn vị tỉ lệ 0..1 của cạnh ngắn)."""
    R = int(r * min(im.width, im.height))
    x, y = int(cx * im.width), int(cy * im.height)
    box = (max(0, x - R), max(0, y - R), min(im.width, x + R), min(im.height, y + R))
    return fit_cover(im.crop(box), w, h)


def shadow(im, box, blur=18, alpha=110):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle(box, 10, fill=(0, 0, 0, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    im.alpha_composite(lay)


def arrow_prop(im, x0, y0, x1, y1, p, bend=0.2):
    """Mũi tên SÁP ĐỎ (ảnh user gen) — reveal kiểu đang vẽ tay. Dùng lại make_vox."""
    MV.prop_arrow(im, (x0, y0), (x1, y1), p, bend=bend)


def arrow(d, x0, y0, x1, y1, p, width=11, col=RED):
    """(đường lui) mũi tên vector — chỉ dùng khi CHƯA có bộ prop PNG."""
    if p <= 0:
        return
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0)
    L = math.hypot(nx, ny) or 1
    bow = 0.14
    cx, cy = mx + nx / L * L * bow * 0.35, my + ny / L * L * bow * 0.35
    pts = []
    steps = 44
    for i in range(steps + 1):
        t = (i / steps) * p
        xx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1
        yy = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1
        pts.append((xx, yy))
    if len(pts) > 1:
        d.line(pts, fill=col, width=width, joint="curve")
    if p > 0.82 and len(pts) > 2:
        ax, ay = pts[-1]
        bx, by = pts[-6]
        ang = math.atan2(ay - by, ax - bx)
        s = 34
        d.polygon([(ax, ay),
                   (ax - s * math.cos(ang - 0.42), ay - s * math.sin(ang - 0.42)),
                   (ax - s * math.cos(ang + 0.42), ay - s * math.sin(ang + 0.42))], fill=col)


def ring_prop(im, cx, cy, rx, ry, p):
    """Vòng khoanh BÚT SÁP (ảnh user gen) thay vòng vector."""
    MV.prop_circle(im, cx, cy, rx * 2, ry * 2, p)


def ring(d, cx, cy, rx, ry, p, width=15, col=RED):
    """Vòng khoanh bút dạ vẽ dần (hơi quá một chút như tay người)."""
    if p <= 0:
        return
    total = 2 * math.pi * 1.08
    steps = 96
    pts = []
    for i in range(steps + 1):
        a = -0.6 + total * p * (i / steps)
        wob = 1 + 0.018 * math.sin(a * 3.1)
        pts.append((cx + rx * wob * math.cos(a), cy + ry * wob * math.sin(a)))
    if len(pts) > 1:
        d.line(pts, fill=col, width=width, joint="curve")


def vignette_outside(im, cx, cy, rx, ry, amount):
    """Tối phần NGOÀI vòng focus — dẫn mắt, không đụng vùng đang nói."""
    if amount <= 0:
        return im
    dark = ImageEnhance.Brightness(im).enhance(1 - amount)
    mask = Image.new("L", im.size, 255)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - rx * 1.18, cy - ry * 1.18, cx + rx * 1.18, cy + ry * 1.18], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(90))
    return Image.composite(dark, im, mask)


def label_box(im, text, y=None, font=None):
    """Nhãn ngắn (tuỳ chọn). Mặc định KHÔNG dùng — tool này là build-on bằng HÌNH."""
    if not text:
        return
    from PIL import ImageFont
    fp = Path(r"C:\Windows\Fonts\NotoSansJP-Black.otf")
    if not fp.exists():
        fp = Path(r"C:\Windows\Fonts\meiryob.ttc")
    f = ImageFont.truetype(str(fp), 64) if fp.exists() else ImageFont.load_default()
    d = ImageDraw.Draw(im)
    tw = d.textlength(text, font=f)
    x0 = int((W - tw) / 2) - 34
    y0 = (y if y is not None else 470)
    d.rounded_rectangle([x0, y0, x0 + tw + 68, y0 + 96], 14, fill=(255, 210, 0))
    d.text((x0 + 34, y0 + 12), text, font=f, fill=INK)


# ══════════════════════════════════════════════════════════════════ frame

def build_frame(spec, imgs, t, anim):
    mode = spec.get("mode", "focus")
    A = imgs["A"]
    im = A.copy().convert("RGBA")

    # idle: thở sáng ±1,5%, cycle NGUYÊN trong IDLE_SEC => loop sạch
    if t >= anim:
        u = (t - anim) % IDLE_SEC / IDLE_SEC
        br = 1 + 0.015 * math.sin(2 * math.pi * u)
        im = ImageEnhance.Brightness(im.convert("RGB")).enhance(br).convert("RGBA")

    if mode == "soft":
        FX.draw_avatar(im, spec, t, MV, W, H, SUB_TOP)
        FX.draw_fx(im, spec, t, MV, HAVE_PROPS, W, H, SUB_TOP)
        return im.convert("RGB")

    fx, fy, fr = spec.get("focus", [0.62, 0.5, 0.17])
    cx, cy = fx * W, fy * H
    rx, ry = fr * W * 0.92, fr * W * 0.66

    if mode == "wipe":
        B = imgs.get("B")
        p = ease((t - 0.75) / 1.65)
        if B is not None and p > 0:
            x = int(W * p)
            im.paste(B.convert("RGBA"), (0, 0), _wipe_mask(x))
            if 0 < x < W:                      # vệt sáng ở mép wipe
                d = ImageDraw.Draw(im, "RGBA")
                d.rectangle([x - 6, 0, x + 6, H], fill=(255, 255, 255, 190))
                d.rectangle([x - 26, 0, x + 26, H], fill=(255, 255, 255, 55))

    elif mode == "inset":
        p1 = ease((t - 0.55) / 0.75)
        if p1 > 0:
            iw, ih = 720, 470
            B = imgs.get("B")
            if B is None:
                B = crop_at(imgs["A_raw"], fx, fy, fr, iw, ih)
            pos = spec.get("inset_pos", "bl")
            ix = 110 if pos.endswith("l") else W - iw - 110
            iy = int(120 + 26 * (1 - p1)) if pos.startswith("t") else int(H - ih - 300 + 26 * (1 - p1))
            # card = ảnh + viền trắng; alpha đồng nhất theo p1 (đừng blend 2 lần)
            card = Image.new("RGBA", (iw + 22, ih + 22), (255, 255, 255, 255))
            card.paste(B.resize((iw, ih), Image.LANCZOS).convert("RGB"), (11, 11))
            if p1 < 1:
                card.putalpha(int(255 * p1))
            shadow(im, [ix - 4, iy - 4, ix + iw + 26, iy + ih + 26], 24, int(120 * p1))
            im.alpha_composite(card, (ix - 11, iy - 11))
            p2 = ease((t - 1.70) / 0.85)
            if p2 > 0:
                ax = ix + iw + 30 if pos.endswith("l") else ix - 30
                ay = iy + ih // 2
                if math.hypot(cx - ax, cy - ay) > 240:      # quá gần thì mũi tên thành rác
                    if HAVE_PROPS:
                        arrow_prop(im, ax, ay, cx, cy, p2,
                                   bend=0.2 if pos.endswith("l") else -0.2)
                    else:
                        arrow(ImageDraw.Draw(im, "RGBA"), ax, ay, cx, cy, p2)

    else:  # focus
        p1 = ease((t - 0.60) / 1.05)
        im = vignette_outside(im.convert("RGB"), cx, cy, rx, ry, 0.24 * p1).convert("RGBA")
        if HAVE_PROPS:
            ring_prop(im, cx, cy, rx, ry, p1)
        else:
            ring(ImageDraw.Draw(im, "RGBA"), cx, cy, rx, ry, p1)
        d = ImageDraw.Draw(im, "RGBA")
        p2 = ease((t - 1.75) / 0.8)
        if p2 > 0 and spec.get("from"):
            sx, sy = spec["from"]
            if HAVE_PROPS:
                arrow_prop(im, sx * W, sy * H, cx - rx * 0.8, cy - ry * 0.8, p2)
            else:
                arrow(d, sx * W, sy * H, cx - rx * 0.8, cy - ry * 0.8, p2)

    FX.draw_avatar(im, spec, t, MV, W, H, SUB_TOP)
    FX.draw_fx(im, spec, t, MV, HAVE_PROPS, W, H, SUB_TOP)
    out = im.convert("RGB")
    if spec.get("label") and t > 2.55:
        label_box(out, spec["label"], spec.get("label_y"))
    return out


_MASKS = {}


def _wipe_mask(x):
    m = _MASKS.get(x)
    if m is None:
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle([0, 0, x, H], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(3))
        _MASKS.clear()
        _MASKS[x] = m
    return m


def settle(spec):
    mode = spec.get("mode", "focus")
    base = {"wipe": 2.45, "inset": 2.60, "focus": 2.60, "soft": 0.6}[mode]
    return max(base, FX.settle_extra(spec)) + (0.75 if spec.get("label") else 0.0)


# ══════════════════════════════════════════════════════════════════ render

def render(spec, img_dir, out, still=False, sec=CLIP_SEC, quiet=False):
    pa = Path(spec["photo"])
    if not pa.is_absolute() and not pa.exists():
        pa = Path(img_dir) / pa
    if not pa.exists():
        # 🔴 thiếu ảnh KHÔNG được làm chết cả lô: các entry khác vẫn dựng được, và
        #    cmd_slides đếm lại ở cuối để không ai tưởng đã đủ (render-background.md §1.5)
        print(f"  [THIEU ANH] {pa.name} -> bo qua entry nay")
        return False
    A_raw = load(pa)
    imgs = {"A": fit_cover(A_raw, W, H), "A_raw": A_raw}
    if spec.get("photo2"):
        pb = Path(spec["photo2"])
        if not pb.is_absolute() and not pb.exists():
            pb = Path(img_dir) / pb
        if pb.exists():
            imgs["B"] = fit_cover(load(pb), W, H)
    if spec.get("mode") == "wipe" and "B" not in imgs:
        print(f"  ⚠ wipe thiếu photo2 ({spec.get('photo2')}) → hạ về soft")
        spec = dict(spec, mode="soft")
    if spec.get("mode") == "inset" and "B" not in imgs:
        fx, fy, fr = spec.get("focus", [0.62, 0.5, 0.17])
        imgs["B"] = crop_at(A_raw, fx, fy, fr, 760, 500)

    anim = max(settle(spec) + 0.3, 1.2 if spec.get("mode") == "soft" else 3.0)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if still:
        build_frame(spec, imgs, anim, anim).save(out.with_suffix(".png"))
        if not quiet:
            print(f"  ✓ {out.with_suffix('.png').name}  ({spec.get('mode','focus')}, build-on {anim:.1f}s)")
        return True

    tmp = out.parent / f"_tmp_{out.stem}"
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "in").mkdir(parents=True, exist_ok=True)
    (tmp / "id").mkdir(parents=True, exist_ok=True)
    for i in range(int(anim * FPS_IN)):
        build_frame(spec, imgs, i / FPS_IN, anim).save(tmp / "in" / f"f{i:05d}.png")
    for j in range(int(IDLE_SEC * FPS_IDLE)):
        build_frame(spec, imgs, anim + j / FPS_IDLE, anim).save(tmp / "id" / f"f{j:05d}.png")

    a = out.parent / f"_a_{out.stem}.mp4"
    b = out.parent / f"_b_{out.stem}.mp4"
    q = ["-vf", "noise=alls=3:allf=t,format=yuv420p", "-c:v", "libx264",
         "-preset", "medium", "-crf", "23", "-g", "60", "-r", str(OUT_FPS)]
    try:
        subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS_IN),
                        "-i", str(tmp / "in" / "f%05d.png"), *q, str(a)],
                       check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS_IDLE),
                        "-i", str(tmp / "id" / "f%05d.png"), *q, str(b)],
                       check=True, capture_output=True)
        reps = max(1, math.ceil((sec - anim) / IDLE_SEC))
        lst = out.parent / f"_cat_{out.stem}.txt"
        lst.write_text(f"file '{a.name}'\n" + f"file '{b.name}'\n" * reps, encoding="utf-8")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", "-movflags", "+faststart", str(out)],
                       check=True, capture_output=True)
        lst.unlink(missing_ok=True)
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"[LỖI] ffmpeg: {e.stderr.decode('utf-8', 'replace')[-900:]}")
    finally:
        for p in (a, b):
            p.unlink(missing_ok=True)
        shutil.rmtree(tmp, ignore_errors=True)
    if not quiet:
        print(f"  ✓ {out.name}  ({spec.get('mode','focus')}, build-on {anim:.1f}s → đứng im)")
    return True


def sig(spec, img_dir):
    h = hashlib.md5(json.dumps(spec, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    for k in ("photo", "photo2"):
        if spec.get(k):
            p = Path(spec[k])
            if not p.is_absolute() and not p.exists():
                p = Path(img_dir) / p
            if p.exists():
                h = hashlib.md5((h + str(int(p.stat().st_mtime))).encode()).hexdigest()
    return h


def sheet(pngs, out, cols=3):
    if not pngs:
        return
    tw = 640
    ims = [Image.open(p).convert("RGB").resize((tw, int(tw * H / W)), Image.LANCZOS) for p in pngs]
    rows = math.ceil(len(ims) / cols)
    sh = Image.new("RGB", (cols * tw, rows * ims[0].height), (245, 244, 240))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % cols) * tw, (i // cols) * im.height))
    sh.save(out, quality=88)
    print(f"[SHEET] {out}")


def cmd_demo(a):
    src = sorted(Path(a.img_dir).glob("*.jpg")) + sorted(Path(a.img_dir).glob("*.jpeg"))
    if len(src) < 4:
        raise SystemExit("[LỖI] cần ≥4 ảnh trong folder demo")
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    specs = [
        {"mode": "focus", "photo": str(src[0]), "focus": [0.60, 0.46, 0.16]},
        {"mode": "inset", "photo": str(src[1]), "focus": [0.42, 0.52, 0.12], "inset_pos": "bl"},
        {"mode": "wipe", "photo": str(src[2]), "photo2": str(src[3])},
        {"mode": "focus", "photo": str(src[4 % len(src)]), "focus": [0.35, 0.55, 0.19],
         "from": [0.8, 0.25]},
    ]
    pngs = []
    for i, s in enumerate(specs):
        render(s, a.img_dir, out / f"shot_demo_{i}.mp4", still=a.still)
        pngs.append(out / f"shot_demo_{i}.png" if a.still else out / f"shot_demo_{i}.mp4")
    if a.still:
        sheet(pngs, out / "_shot_sheet.jpg", cols=2)


def cmd_slides(a):
    cfg = json.loads(Path(a.slides).read_text(encoding="utf-8"))
    clips = Path(a.clips_dir)
    clips.mkdir(parents=True, exist_ok=True)
    n = skip = 0
    pngs, missing = [], []
    for i, e in enumerate(cfg):
        sp = e.get("shot")
        if not isinstance(sp, dict):
            continue
        if a.only and i not in a.only:
            continue
        dst = clips / f"clip_{i:02d}.mp4"
        sg = clips / f"clip_{i:02d}.sig"
        want = sig(sp, a.img_dir)
        if not a.force and dst.exists() and sg.exists() and sg.read_text().strip() == want and not a.still:
            skip += 1
            continue
        okk = render(sp, a.img_dir, dst, still=a.still, quiet=False)
        if okk is False:
            missing.append(i)
            continue
        if not a.still:
            sg.write_text(want, encoding="utf-8")
        else:
            pngs.append(clips / f"clip_{i:02d}.png")
        n += 1
    print(f"— dựng {n} shot, skip {skip} —")
    if missing:
        print(f"🔴 THIẾU ẢNH {len(missing)} entry: {missing} — CHƯA ĐƯỢC RENDER VIDEO "
              f"(render-background.md §1.5)")
    if a.still and pngs:
        sheet(pngs[:12], clips / "_shot_sheet.jpg")


def main():
    ap = argparse.ArgumentParser(description="Build-on bằng HÌNH ẢNH (wipe/inset/focus)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("demo")
    d.add_argument("img_dir")
    d.add_argument("out_dir")
    d.add_argument("--still", action="store_true")
    d.set_defaults(fn=cmd_demo)
    s = sub.add_parser("slides")
    s.add_argument("slides")
    s.add_argument("clips_dir")
    s.add_argument("--img-dir", required=True)
    s.add_argument("--still", action="store_true")
    s.add_argument("--force", action="store_true")
    s.add_argument("--only", nargs="*", type=int, help="chi dung vai slot (index entry)")
    s.set_defaults(fn=cmd_slides)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
