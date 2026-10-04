# -*- coding: utf-8 -*-
r"""prep_bubble.py — biến ảnh bong bóng thoại vẽ sáp (nền giấy trắng) thành prop PNG.

🔴 KHÔNG dùng rembg ở đây: rembg tách "chủ thể", mà chủ thể của ảnh này là NÉT VẼ —
   nó sẽ ăn mất phần ruột. Bong bóng cần **ruột ĐỤC** (chữ đen đọc trên ảnh nền tối)
   nhưng **nền ngoài TRONG SUỐT**.

Cách làm: vùng sáng nào LIÊN THÔNG với mép ảnh = nền giấy → alpha 0.
Vùng sáng bị nét vẽ bao kín (ruột bong bóng) không chạm mép → giữ đục.

    python prep_bubble.py <raw.jpg> <ten_prop>      # -> props/<ten_prop>.png + INDEX
"""
import io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROPS = Path(__file__).resolve().parent / "props"


def main():
    raw, name = Path(sys.argv[1]), sys.argv[2]
    im = Image.open(raw).convert("RGB")
    a = np.asarray(im.convert("L"), dtype=np.int16)

    bright = a > 205                       # giấy trắng + ruột bong bóng
    lab, n = ndimage.label(bright)
    edge = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    edge.discard(0)
    outside = np.isin(lab, list(edge))     # nền giấy (liên thông với mép)

    alpha = np.where(outside, 0, 255).astype("uint8")
    # mềm mép 1px cho đỡ răng cưa
    alpha = ndimage.uniform_filter(alpha.astype("float32"), 3).astype("uint8")

    out = np.dstack([np.asarray(im), alpha])
    img = Image.fromarray(out, "RGBA")
    ys, xs = np.nonzero(alpha > 8)
    if len(xs):
        img = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    PROPS.mkdir(exist_ok=True)
    img.save(PROPS / f"{name}.png")

    idxp = PROPS / "INDEX.json"
    idx = json.loads(idxp.read_text(encoding="utf-8")) if idxp.exists() else {}
    idx[name] = {"kind": "bubble", "method": "flood", "w": img.width, "h": img.height,
                 "src": raw.name}
    idxp.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    keep = int((alpha > 8).sum() * 100 / alpha.size)
    print(f"  {name}.png  {img.size}  giữ {keep}% pixel (ruột đục, nền ngoài trong suốt)")


if __name__ == "__main__":
    main()
