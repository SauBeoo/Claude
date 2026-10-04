# -*- coding: utf-8 -*-
"""
strip_wm_star.py — gỡ watermark ✦ của model gen ảnh bằng TEMPLATE MATCH + UN-BLEND.

Vì sao cần tool thứ hai bên cạnh `strip_wm.py`:
  `strip_wm.py` định vị watermark bằng "điểm SÁNG NHẤT trong một ô đoán trước". Cách đó gãy
  ngay khi nền quanh ✦ sáng hơn nó (gỗ nhạt, washi kem, bồn inox lấp lánh) — BFS sẽ bám vào
  một điểm sáng KHÁC rồi vá nhầm chỗ. Đo thật trên 20 ảnh AI của co-dai video 17
  (2026-08-09): 15/20 ca **báo "vá thành công" nhưng ✦ còn nguyên**, lại đắp thêm một mảng
  donor ngay cạnh — tức là làm ảnh XẤU ĐI mà vẫn exit 0. Bài học: **định vị bằng HÌNH DẠNG
  (template match), và bắt buộc SOI MẮT bằng contact sheet — exit code không chứng minh gì.**

⚠️ ĐỌC TRƯỚC KHI DÙNG — đo rồi mới biết cách rẻ nhất:
  Với model đang dùng (2026-08-09), ✦ nằm ở **VỊ TRÍ CỐ ĐỊNH x 0.907–0.953 · y 0.833–0.914**
  của khung (8/8 ca khớp điểm cao trùng khít). Khi nó cố định như vậy thì **CẮT ẢNH là cách
  đúng**, không phải vá pixel: cắt phải tại 0.90W rồi trim đáy về đúng 16:9 là ✦ ra ngoài
  khung, **không artifact, không đoán alpha, không phải soi từng ảnh** (đổi lại: mất ~10%
  bề ngang + ~9% chiều cao). Tool này chỉ cần đến khi ✦ rơi vào GIỮA ảnh, hoặc khi bố cục
  chật tới mức không cắt nổi.
  → Luôn CHẠY BƯỚC ĐO TRƯỚC (`--check` trên cả bộ) rồi mới chọn cắt hay vá.

Cách làm ở đây:
  ① residual = gray − medianBlur(gray, 31)  → tách lớp phủ mỏng khỏi nền
  ② cv2.matchTemplate(residual, SHAPE, TM_CCOEFF_NORMED) → tìm ĐÚNG hình ngôi sao 4 cánh
  ③ UN-BLEND thay vì vá đè: ✦ là lớp trắng alpha-composite
         out = img·(1−a) + 255·a   ⇒   img = (out − 255·a) / (1−a)
     khôi phục lại CHÍNH vân nền bên dưới — không donor, không inpaint, không mảng phẳng.
     ⚠️ Giới hạn ĐO ĐƯỢC: cách này xoá được thân sao nhưng **còn để lại VIỀN mờ hình sao**
     (bản đồ alpha học từ 1 ảnh không tả đúng rìa mềm + nhiễu JPEG). Chấp nhận được khi thẻ
     có darken/duotone đè lên; KHÔNG đủ sạch cho ảnh nền sáng phẳng — ca đó thì cắt.
  ④ ASSERT điểm khớp ≥ --min-score, nếu không thì BÁO TRƯỢT chứ không vá bừa.

Template (hình + bản đồ alpha) học một lần từ một ca ✦ nằm trên nền phẳng, lưu ở
`wm_star_tmpl.npz` cạnh file này. Model đổi watermark → học lại bằng `--learn`.

Dùng:
    python strip_wm_star.py <in> <out> [--zoom z.png]
    python strip_wm_star.py <in> --check
    python strip_wm_star.py <in> --learn x0,y0,x1,y1     # dạy lại template
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

TMPL = Path(__file__).with_name("wm_star_tmpl.npz")


def imread_u(path):
    """cv2.imread CHẾT trên đường dẫn có ký tự ngoài ASCII (tên ảnh gen hay dính '…').
    Nó trả None chứ không ném lỗi ⇒ dễ đi tiếp rồi vỡ ở chỗ khác. Đọc qua numpy cho chắc."""
    return cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)


def imwrite_u(path, img, q=95):
    ok, buf = cv2.imencode(Path(path).suffix or ".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, q])
    if ok:
        buf.tofile(str(path))
    return ok


def residual(bgr):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return g.astype(np.float32) - cv2.medianBlur(g, 31).astype(np.float32)


def learn(src, box):
    """Ước lượng bản đồ alpha của ✦.

    ⚠️ Nền phải ước lượng bằng MORPH_OPEN, không phải medianBlur: ✦ là vệt SÁNG, mà cửa sổ
    median 31px vẫn nuốt một phần chính ngôi sao vào "nền" ⇒ alpha bị hụt ⇒ un-blend xong
    còn bóng ma hình sao. Opening với kernel lớn hơn ngôi sao thì xoá sạch nó khỏi nền.
    Và KHÔNG cắt cứng `res < 5` — cắt cứng để lại viền tròn ở rìa mềm của sao."""
    bgr = imread_u(src)
    x0, y0, x1, y1 = box
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (75, 75))
    bg_full = cv2.morphologyEx(g, cv2.MORPH_OPEN, k).astype(np.float32)
    res = g.astype(np.float32) - bg_full
    res = res[y0:y1, x0:x1]
    bg = bg_full[y0:y1, x0:x1]
    a = np.clip(res / np.maximum(255.0 - bg, 1.0), 0, 0.95)
    a -= np.median(a[:3, :])               # trừ nền phẳng thay vì cắt cứng
    a = np.clip(a, 0, 0.95)
    a = cv2.GaussianBlur(a, (3, 3), 0)
    shape = (res - res.mean()).astype(np.float32)
    np.savez(TMPL, alpha=a.astype(np.float32), shape=shape)
    print(f"đã học template {a.shape} — alpha đỉnh {a.max():.2f}, {int((a > 0.02).sum())} px thân")


def locate(bgr, shape, region=(0.55, 0.55, 1.0, 1.0)):
    H, W = bgr.shape[:2]
    th, tw = shape.shape
    x0, y0 = int(region[0] * W), int(region[1] * H)
    x1, y1 = min(W, int(region[2] * W)), min(H, int(region[3] * H))
    sub = residual(bgr)[y0:y1, x0:x1]
    if sub.shape[0] < th or sub.shape[1] < tw:
        return None, 0.0
    r = cv2.matchTemplate(sub, shape, cv2.TM_CCOEFF_NORMED)
    _, score, _, loc = cv2.minMaxLoc(r)
    return (x0 + loc[0], y0 + loc[1]), float(score)


def unblend(bgr, at, alpha, k=1.0):
    """img = (out − 255·a)/(1−a), làm trên float, kẹp biên. `k` = hệ số chỉnh alpha."""
    x, y = at
    th, tw = alpha.shape
    patch = bgr[y:y + th, x:x + tw].astype(np.float32)
    a = np.clip(alpha * k, 0, 0.95)[..., None]
    out = (patch - 255.0 * a) / np.maximum(1.0 - a, 1e-3)
    res = bgr.copy()
    res[y:y + th, x:x + tw] = np.clip(out, 0, 255).astype(np.uint8)
    return res


def best_k(bgr, at, alpha, shape):
    """Dò hệ số alpha cho TỪNG ảnh: chọn k làm TẮT NHẤT dấu vết hình sao còn lại.

    Một hệ số alpha học từ 1 ảnh không khớp mọi ảnh (nền sáng/tối làm lớp phủ trông
    đậm nhạt khác nhau). Đo trực tiếp thứ mình muốn: sau khi gỡ, tương quan giữa phần dư
    và hình ngôi sao phải ~0. Đây chính là gate tự động thay cho việc nhìn bằng mắt."""
    x, y = at
    th, tw = alpha.shape
    sh = shape - shape.mean()
    sh /= (np.linalg.norm(sh) + 1e-6)
    out = []
    for k in np.arange(0.5, 3.55, 0.05):
        r = residual(unblend(bgr, at, alpha, k))[y:y + th, x:x + tw]
        r = r - r.mean()
        out.append((abs(float((r * sh).sum()) / (np.linalg.norm(r) + 1e-6)), float(k)))
    return min(out)[1], min(out)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--learn", help="x0,y0,x1,y1 — vùng chứa ✦ để học template")
    ap.add_argument("--min-score", type=float, default=0.45,
                    help="điểm khớp tối thiểu (TM_CCOEFF_NORMED); dưới ngưỡng = BÁO TRƯỢT")
    ap.add_argument("--region", default="0.55,0.55,1.0,1.0",
                    help="vùng dò, tỉ lệ x0,y0,x1,y1 (mặc định góc phần tư dưới-phải)")
    ap.add_argument("--zoom", help="xuất ảnh soi ×4 quanh chỗ vá")
    a = ap.parse_args()

    if a.learn:
        learn(a.src, [int(v) for v in a.learn.split(",")])
        return
    if not TMPL.exists():
        sys.exit(f"❌ chưa có template {TMPL} — chạy --learn trước")

    d = np.load(TMPL)
    alpha, shape = d["alpha"], d["shape"]
    bgr = imread_u(a.src)
    if bgr is None:
        sys.exit(f"❌ không đọc được {a.src}")
    at, score = locate(bgr, shape, tuple(float(v) for v in a.region.split(",")))
    name = Path(a.src).name
    if at is None or score < a.min_score:
        sys.exit(f"❌ {name}: điểm khớp {score:.3f} < {a.min_score} — KHÔNG vá (tránh vá nhầm chỗ)")
    print(f"{name}: khớp {score:.3f} tại (x={at[0]}, y={at[1]})")
    if a.check:
        return
    if not a.out:
        sys.exit("cần <out>")

    k, corr = best_k(bgr, at, alpha, shape)
    print(f"   hệ số alpha {k:.2f} — dấu vết sao còn lại {corr:.3f} (0 = sạch)")
    res = unblend(bgr, at, alpha, k)
    imwrite_u(a.out, res)
    print(f"OK {a.out}")

    if a.zoom:
        th, tw = alpha.shape
        pad = 30
        x0, y0 = max(0, at[0] - pad), max(0, at[1] - pad)
        x1, y1 = min(res.shape[1], at[0] + tw + pad), min(res.shape[0], at[1] + th + pad)
        cr = res[y0:y1, x0:x1]
        imwrite_u(a.zoom, cv2.resize(cr, (cr.shape[1] * 4, cr.shape[0] * 4),
                                       interpolation=cv2.INTER_NEAREST))
        print(f"   soi ×4 → {a.zoom}")


if __name__ == "__main__":
    main()
