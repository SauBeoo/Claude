# -*- coding: utf-8 -*-
"""Phu mau phim cu len anh slide (JPG only, chua PNG drawn): am + bac mau + fade + vignette + grain."""
import os, sys
import numpy as np
from PIL import Image, ImageEnhance
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def grade(path):
    im = Image.open(path).convert("RGB")
    # desat nhe
    im = ImageEnhance.Color(im).enhance(0.82)
    a = np.asarray(im).astype(np.float32)
    # warm cast: tang R, giam B
    a[..., 0] = np.clip(a[..., 0] * 1.06 + 6, 0, 255)
    a[..., 2] = np.clip(a[..., 2] * 0.93, 0, 255)
    # fade: nang den len, ha trang xuong
    a = a * ((235 - 22) / 255.0) + 22
    # vignette mem
    h, w = a.shape[:2]
    Y, X = np.ogrid[:h, :w]
    d = np.sqrt(((X - w/2) / (w/2))**2 + ((Y - h/2) / (h/2))**2)
    vig = np.clip(1 - 0.18 * np.clip(d - 0.55, 0, None) / 0.9, 0.78, 1.0)
    a *= vig[..., None]
    # grain
    rng = np.random.default_rng(hash(os.path.basename(path)) % (2**32))
    a += rng.normal(0, 4.2, a.shape[:2])[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path, quality=93)

if __name__ == "__main__":
    folder = sys.argv[1]
    n = 0
    for f in sorted(os.listdir(folder)):
        if f.startswith("slide_") and f.endswith(".jpg"):
            grade(os.path.join(folder, f)); n += 1
    print(f"graded {n} jpg")
