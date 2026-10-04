# -*- coding: utf-8 -*-
"""ingest_photos_01.py — anh nguoi that lo zip_0228 -> slides_img/slide_NN.png theo _plan/storyboard_src.py.

- shot -> chi so SLIDES qua khoa "_shot"; file anh = tien to ten trong storyboard_src (khop dung 1 file)
- cat ✦: phai 0,905W + trim 16:9 chia doi tren/duoi + resize 1920x1080 (media-library §2.10 ⑤b, lo 1376x768)
- bo qua slot da la clip podcast ("video": true) va slot card/reveal
- xuat sheet duyet mat: _plan/_ingest_sheet_*.jpg (so slot tren moi o) + _plan/_ingest_corners.jpg (goc duoi-phai 1:1)
Chay: python tools/ingest_photos_01.py 01_kuchiguse-hitonome
"""
import sys, io, json, importlib.util
from pathlib import Path
from PIL import Image, ImageDraw

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
BATCH = "_user_raw/zip_0228"
HOLD = {59: 60}   # slot -> slot co anh: giu CUNG anh cho thanh mot canh dai (khong co anh dung cho slot)


def crop_wm(im):
    W, H = im.size
    nw = int(W * 0.905); nh = round(nw * 9 / 16); top = (H - nh) // 2
    return im.crop((0, top, nw, top + nh)).resize((1920, 1080), Image.LANCZOS)


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    sp = importlib.util.spec_from_file_location("sb", vd / "_plan" / "storyboard_src.py")
    sb = importlib.util.module_from_spec(sp); sp.loader.exec_module(sb)
    sl = json.loads((PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json").read_text(encoding="utf-8"))
    files = sorted((vd / BATCH).rglob("*.jpg"))
    out = vd / "slides_img"; out.mkdir(exist_ok=True)
    done, skip, miss = [], [], []
    for i, e in enumerate(sl):
        shot = e.get("_shot")
        if not isinstance(shot, int) or shot not in sb.S:
            continue
        pref = sb.S[shot][2]
        if e.get("video"):
            skip.append(i); continue
        if not pref:
            miss.append(i); continue
        hit = [f for f in files if f.name.startswith(pref)]
        assert len(hit) == 1, f"slot {i}: tien to「{pref}」khop {len(hit)} file"
        crop_wm(Image.open(hit[0]).convert("RGB")).save(out / f"slide_{i:02d}.png")
        done.append((i, hit[0].name))
    for a, b in HOLD.items():
        if (out / f"slide_{b:02d}.png").exists():
            Image.open(out / f"slide_{b:02d}.png").save(out / f"slide_{a:02d}.png"); miss = [m for m in miss if m != a]
    print(f"nap {len(done)} anh · bo qua (clip podcast) {skip} · THIEU anh {miss}")
    # sheet duyet
    tw, th, c = 384, 216, 5
    for k in range(0, len(done), 40):
        part = done[k:k + 40]
        s = Image.new("RGB", (tw * c, th * ((len(part) + c - 1) // c)), "white"); d = ImageDraw.Draw(s)
        for j, (i, _) in enumerate(part):
            x, y = (j % c) * tw, (j // c) * th
            s.paste(Image.open(out / f"slide_{i:02d}.png").resize((tw, th)), (x, y))
            d.rectangle([x, y, x + 40, y + 20], fill="black"); d.text((x + 4, y + 4), str(i), fill="yellow")
        s.save(vd / "_plan" / f"_ingest_sheet_{k // 40}.jpg", quality=85)
    cw, ch, c = 240, 135, 8
    s = Image.new("RGB", (cw * c, ch * ((len(done) + c - 1) // c)), "white")
    for j, (i, _) in enumerate(done):
        im = Image.open(out / f"slide_{i:02d}.png")
        s.paste(im.crop((1920 - cw, 1080 - ch, 1920, 1080)), ((j % c) * cw, (j // c) * ch))
    s.save(vd / "_plan" / "_ingest_corners.jpg", quality=90)


if __name__ == "__main__":
    main()
