# -*- coding: utf-8 -*-
r"""Xuất PNG cho TỪNG entry SLIDES + contact sheet phân trang — để duyệt mắt TRƯỚC render.

    python tools\preview_frames.py 03_SCRIPTS\19_..._SLIDES.json 06_VIDEO\19_... --channel co-dai

Vì sao cần tool này (user chốt 2026-08-12: *"tao cần duyệt từng frame 1"*):
`make_vox.py` chỉ dựng PNG cho **thẻ vox** (26/89 entry của video 19). 63 entry ảnh thường
được `video_render.build_slides()` ghép **trong lúc render** — nên trước đó không có gì để
soi. nenkin có đủ PNG vì nó dùng `make_stage.py` (dựng mọi slide); co-dai dùng lớp `vox`,
không dựng slide ảnh thường.

⚠️ Tool này KHÔNG vẽ lại theo cách riêng — nó **gọi thẳng `video_render.make_slide()`**,
đúng hàm renderer dùng. Thấy gì ở đây là thấy đúng cái sẽ render. Chỉ khác 2 điểm, ghi rõ:
  · KHÔNG có phụ đề cháy (renderer burn sau, từ subs.srt) → sheet vẽ MOCK 2 dòng để kiểm đè chữ
  · KHÔNG có crop-pan (renderer pan 1.12× khi motion bật) → mép ảnh thật sẽ bị ăn ~65px
"""
import argparse, importlib.util, io, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HEALTH_TOOLS = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
FONTS = [r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc",
         r"C:\Windows\Fonts\arialbd.ttf"]


def font(sz):
    for f in FONTS:
        try:
            return ImageFont.truetype(f, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def load_vr():
    sys.path.insert(0, str(HEALTH_TOOLS))
    keep = sys.argv
    sys.argv = ["video_render.py"]
    spec = importlib.util.spec_from_file_location("vr", HEALTH_TOOLS / "video_render.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    sys.argv = keep
    return m


def sub_mock(im):
    """MOCK phụ đề outline 2 dòng (co-dai: sub_style outline / size 26) — kiểm 'chữ có nghĩa
    của slide có bị phụ đề đè không'. Cùng ý đồ với --sub-mock của make_vox."""
    d = ImageDraw.Draw(im)
    f = font(46)
    for k, t in enumerate(("ここに焼き込み字幕の一行目が入ります", "二行目はここまで伸びます")):
        w = d.textlength(t, font=f)
        x, y = (im.width - w) / 2, im.height - 250 + k * 62
        for dx in (-3, 3):
            for dy in (-3, 3):
                d.text((x + dx, y + dy), t, font=f, fill=(0, 0, 0))
        d.text((x, y), t, font=f, fill=(255, 255, 255))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides")
    ap.add_argument("videodir")
    ap.add_argument("--channel", default="co-dai")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=6)
    ap.add_argument("--no-sub", action="store_true", help="không vẽ mock phụ đề")
    a = ap.parse_args()

    VD = Path(a.videodir)
    cfg = json.loads(Path(a.slides).read_text(encoding="utf-8"))
    out = VD / "preview"
    out.mkdir(parents=True, exist_ok=True)
    vr = load_vr()
    bg = vr.make_bg()
    img_dir, clips = VD / "slides_img", VD / "clips"

    frames, vox_done = [], set()
    for i, spec in enumerate(cfg):
        dst = out / f"frame_{i:02d}.png"
        src_vox = clips / f"clip_{i:02d}.png"
        if spec.get("video") and src_vox.exists():            # thẻ vox: đã có PNG
            Image.open(src_vox).convert("RGB").save(dst)
            kind = "vox:" + (spec.get("vox", {}).get("kind", "?"))
            vox_done.add(i)   # make_vox --sub-mock ĐÃ burn mock → không vẽ lần 2
        else:
            src = next((p for ext in (".jpg", ".jpeg", ".png")
                        if (p := img_dir / f"slide_{i:02d}{ext}").exists()), None)
            vr.make_slide(spec, dst, bg, src, bake_rank=False)
            kind = "photo" if src else "🔴 THIẾU ẢNH"
        frames.append((i, dst, kind, spec.get("match", "")))

    # ── contact sheet phân trang, burn số slot + kind + match
    CW, CH, PAD, LBL = 620, 349, 10, 54
    per = a.cols * a.rows
    pages = (len(frames) + per - 1) // per
    for p in range(pages):
        chunk = frames[p * per:(p + 1) * per]
        rows = (len(chunk) + a.cols - 1) // a.cols
        W = a.cols * (CW + PAD) + PAD
        H = rows * (CH + LBL + PAD) + PAD
        sh = Image.new("RGB", (W, H), (24, 24, 26))
        d = ImageDraw.Draw(sh)
        f1, f2 = font(26), font(21)
        for k, (i, path, kind, match) in enumerate(chunk):
            cx = PAD + (k % a.cols) * (CW + PAD)
            cy = PAD + (k // a.cols) * (CH + LBL + PAD)
            im = Image.open(path).convert("RGB").resize((CW, CH))
            if not a.no_sub and i not in vox_done:
                im = sub_mock(im.resize((1920, 1080))).resize((CW, CH))
            sh.paste(im, (cx, cy))
            col = (255, 90, 90) if "THIẾU" in kind else (255, 210, 0)
            d.text((cx + 4, cy + CH + 4), f"[{i:02d}] {kind}", font=f1, fill=col)
            d.text((cx + 4, cy + CH + 30), match[:26], font=f2, fill=(190, 190, 190))
        sh.save(out / f"_sheet_p{p+1}.jpg", quality=90)

    miss = [i for i, _, k, _ in frames if "THIẾU" in k]
    print(f"{len(frames)} frame → {out}")
    print(f"sheet: {pages} trang (_sheet_p1..p{pages}.jpg) · {a.cols}×{a.rows}/trang")
    print(f"thẻ vox {sum(1 for _,_,k,_ in frames if k.startswith('vox'))} · "
          f"ảnh {sum(1 for _,_,k,_ in frames if k=='photo')} · THIẾU ẢNH {len(miss)}")
    if miss:
        print("  slot thiếu ảnh:", miss)


if __name__ == "__main__":
    main()
