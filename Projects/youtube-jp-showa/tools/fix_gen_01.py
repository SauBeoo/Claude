# -*- coding: utf-8 -*-
"""Nghiem thu + sua bo anh gen video 01 BAN 4:
1. Rename ten mo ta -> ma gen_G◯◯ (map theo VISUALS_v2)
2. Xoa watermark ✦ Gemini (BFS tu diem sang nhat trong o goc duoi-phai,
   nguong ~60, component <4000px, gian 3px, fill median nen local — cach DUNG
   theo memory feedback_thumbnail_health_chi_dua_prompt)
3. G44 crop bo hop sua giay hien dai (barcode) · G27 crop bo chu rac tren goi
4. G21 + G29 blur defocus vung chu Nhat doc duoc (bang den / khung thu phap)
Ra: gen/ (JPEG q95) + _gen_fixed_sheet.jpg
"""
import os, sys
from collections import deque
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\01_kyushoku_v2"
RAW, OUT = os.path.join(ROOT, "gen_raw"), os.path.join(ROOT, "gen")
os.makedirs(OUT, exist_ok=True)

MAP = {  # prefix ten file -> (ma G, crop frac hoac None, list vung blur frac)
    "Bread_roll_on_school_desk": ("G12", None, []),
    "Bread_roll_on_serving_tray": ("G50", None, []),
    "Bread_roll_on_wooden_tray": ("G52", None, []),
    "Cloth_pouch_on_wooden_desk": ("G30", None, []),
    "Cloth_pouch_resting_on_windowsill": ("G57", None, []),
    "Cook_frying_bread_rolls": ("G07", None, []),
    "Cook_stirring_milk_in_pot": ("G53", None, []),
    "Empty_Japanese_school_classroom": ("G43", None, []),
    "Fingers_folding_foil_wrapper": ("G14", None, []),
    "Fried_bread_roll_on_plate": ("G06", None, []),
    "Fried_meat_chunks_in_bowl": ("G32", None, []),
    "Frozen_mandarin_oranges_on_tray": ("G44", (0.03, 0.30, 0.63, 0.90), []),
    "Hands_playing_rock_paper_scissors": ("G51", None, []),
    "Hands_rolling_bread_in_kinako": ("G09", None, []),
    "Japanese_school_lunch_on_tray": ("G49", None, []),
    "Milk_cartons_in_wooden_crate": ("G23", None, []),
    "Milk_cup_on_school_desk": ("G18", None, []),
    "Paper_straw_wrapper_flying": ("G24", None, []),
    "Powder_streaming_into_milk_bottle": ("G27", (0.14, 0.28, 0.86, 1.00), []),
    "School_lunch_tray_on_desk": ("G01", None, []),
    "Stainless_steel_spork_on_tray": ("G47", None, []),
    "Stove_heating_milk_in_classroom": ("G21", None, [(0.60, 0.00, 1.00, 0.46)]),
    "Student_opening_glass_milk_bottle": ("G22", None, []),
    "Students_carrying_food_canister": ("G16", None, []),
    "Students_cleaning_spilled_stew": ("G17", None, []),
    "Students_eating_lunch_in_classroom": ("G03", None, []),
    "Students_rearranging_desks": ("G28", None, []),
    "Students_running_in_schoolyard": ("G55", None, []),
    "Wooden_loudspeaker": ("G29", None, [(0.44, 0.40, 1.00, 0.64), (0.86, 0.58, 1.00, 0.80)]),
}


def remove_watermark(im):
    """Sao ✦ Gemini vi tri THAY DOI theo anh -> template-match astroid tren
    gradient map vung goc duoi-phai, peak >= nguong moi inpaint."""
    import cv2
    import numpy as np
    w, h = im.size
    g = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
    x0, y0 = int(w * 0.60), int(h * 0.50)
    roi = g[y0:, x0:]
    edges = cv2.magnitude(*np.gradient(roi.astype(np.float32))[::-1]) if False else None
    gx = cv2.Sobel(roi, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(roi, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy)
    mag = cv2.normalize(mag, None, 0, 1, cv2.NORM_MINMAX)
    best = None
    for R in (22, 26, 30):
        # template: vien astroid |x|^(2/3)+|y|^(2/3) = R^(2/3)
        S = 2 * R + 9
        tpl = np.zeros((S, S), np.float32)
        cs = S // 2
        t = np.linspace(0, 2 * np.pi, 240)
        xs = (R * np.cos(t) ** 3 + cs).astype(int)
        ys = (R * np.sin(t) ** 3 + cs).astype(int)
        for a, b in zip(xs, ys):
            cv2.circle(tpl, (a, b), 1, 1.0, -1)
        res = cv2.matchTemplate(mag, tpl, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(res)
        if best is None or mx > best[0]:
            best = (mx, loc, R, S)
    score, (lx, ly), R, S = best
    if score < 0.22:
        return im, 0.0
    cx, cy = x0 + lx + S // 2, y0 + ly + S // 2
    mask = np.zeros((h, w), np.uint8)
    t = np.linspace(0, 2 * np.pi, 240)
    pts = np.stack([((R + 4) * np.cos(t) ** 3 + cx), ((R + 4) * np.sin(t) ** 3 + cy)], axis=1).astype(np.int32)
    cv2.fillPoly(mask, [pts], 255)
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    arr = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    out = cv2.inpaint(arr, mask, 6, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)), score


def soft_blur(im, rect, radius=16):
    w, h = im.size
    x1, y1, x2, y2 = [int(v * s) for v, s in zip(rect, (w, h, w, h))]
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rectangle([x1, y1, x2, y2], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(24))
    return Image.composite(im.filter(ImageFilter.GaussianBlur(radius)), im, mask)


def main():
    files = sorted(os.listdir(RAW))
    done = []
    for f in files:
        hit = next(((p, v) for p, v in MAP.items() if f.startswith(p)), None)
        if not hit:
            print("?? khong map:", f)
            continue
        prefix, (code, crop, blurs) = hit
        im = Image.open(os.path.join(RAW, f)).convert("RGB")
        im, n = remove_watermark(im)
        note = f"wm score={n:.2f}" + ("" if n else " KHONG-THAY")
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
            note += " crop"
        for r in blurs:
            im = soft_blur(im, r)
            note += " blur"
        if im.width < 1920:
            im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT, f"gen_{code}.jpg"), quality=95)
        done.append((code, note))
        print(f"{code}: {note}")
    # contact sheet
    fnt = ImageFont.truetype(r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Bold.otf", 26)
    codes = sorted(c for c, _ in done)
    cols, cw, ch = 5, 384, 216
    rows = (len(codes) + cols - 1) // cols
    sheet = Image.new("RGB", (cw * cols, (ch + 32) * rows), (18, 18, 18))
    d = ImageDraw.Draw(sheet)
    for i, c in enumerate(codes):
        im = Image.open(os.path.join(OUT, f"gen_{c}.jpg"))
        im.thumbnail((cw, ch))
        x, y = (i % cols) * cw, (i // cols) * (ch + 32)
        sheet.paste(im, (x + (cw - im.width) // 2, y))
        d.text((x + 8, y + ch + 2), c, font=fnt, fill=(255, 220, 90))
    sheet.save(os.path.join(ROOT, "_gen_fixed_sheet.jpg"), quality=88)
    print(f"\nXONG {len(done)}/30 (thieu G10) -> gen/ + _gen_fixed_sheet.jpg")


if __name__ == "__main__":
    main()
