# -*- coding: utf-8 -*-
"""
defringe_logo.py — gỡ VỆT MAGENTA còn sót ở rìa một PNG đã cutout nền `#FF00FF`.

Ca gốc (2026-09-10, `brand_logo.png` của nenkin 22): logo đã có alpha và render ra đúng
hình tròn, **nhưng rìa trái còn 67–77 pixel ngả hồng** — thấy rõ ở 1:1 trên MỌI frame vì
logo là lớp dán cứng. Đây đúng bệnh đã ghi ở `nenkin/CLAUDE.md` §② (khối cắt nền magenta):
*erode hình học MỘT MÌNH KHÔNG ĐỦ* — viền bị nhiễm magenta không còn thuần `#FF00FF` nên
phép tách theo khoảng cách màu để nó lại, còn erode thì cắt theo hình học nên không biết
pixel nào bị nhiễm.

Ba bước, và thứ tự có lý do:
  ① **Loại theo MÀU**: pixel ngả magenta (`R−G>34` và `B−G>34`) ⇒ alpha 0.
     ⛔ Đừng "sửa màu" pixel viền bằng cách hạ R,B theo G: magenta có `G≈0` nên hạ xong ra
        `(145,0,90)` = vẫn đỏ tím. **Suy màu từ chính pixel đã nhiễm thì không bao giờ sạch.**
  ② **Co alpha 1px** cho mượt mép sau khi khoét.
  ③ **Lấy blob lớn nhất** — bước ① có thể chẻ mask thành mảnh, và nó cũng loại luôn dấu ✦
     watermark nếu generator đóng ở góc.

🔴 Nghiệm thu bằng SỐ, không bằng mắt trên sheet: đếm pixel `alpha > 250` mà ngả magenta.
   Phép đo cũ từng đếm pixel **bán trong suốt** (`8 < alpha < 250`) và trả **0** trên 15/15
   ảnh còn vệt tím rõ — vì `erode` cho alpha nhị phân. Gate nào chưa từng báo đỏ thì phải
   nghi nó, không phải tin nó.
"""
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOL_RG = 34          # ngưỡng "ngả magenta" — đo được ở lô cast video 17
TOL_BG = 34


def imread_u(p):
    # cv2.imread KHÔNG đọc được path non-ASCII trên Windows (trả None, im lặng)
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_UNCHANGED)


def imwrite_u(p, im):
    ok, buf = cv2.imencode(os.path.splitext(p)[1], im)
    if not ok:
        raise RuntimeError("imencode fail")
    buf.tofile(p)


def count_fringe(im) -> int:
    """Pixel ĐỤC mà ngả magenta — phép đo đúng chiều."""
    if im.shape[2] < 4:
        return -1
    b, g, r, a = (im[:, :, i].astype(int) for i in range(4))
    return int((((r - g) > TOL_RG) & ((b - g) > TOL_BG) & (a > 250)).sum())


def main() -> int:
    # 🔴 Lọc CỜ ra khỏi tham số vị trí — bản đầu lấy `sys.argv[2]` làm output nên
    #    `--circle` bị hiểu là đường dẫn, `splitext` ra chuỗi rỗng và `imencode` chết
    #    bằng "could not find encoder". Lỗi ồn nên thấy ngay, nhưng cùng loại với bẫy
    #    im lặng: đừng đọc argv theo VỊ TRÍ khi có cờ trộn vào.
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not pos:
        print("dùng: python tools/defringe_logo.py <file.png> [out.png] [--circle]")
        return 2
    src = pos[0]
    dst = pos[1] if len(pos) > 1 else src
    im = imread_u(src)
    if im is None:
        print(f"🔴 đọc không được {src}")
        return 1
    if im.shape[2] == 3:                                  # chưa có alpha
        im = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
        im[:, :, 3] = 255

    before = count_fringe(im)
    b, g, r, a = (im[:, :, i].astype(int) for i in range(4))

    # ① loại theo MÀU
    tint = ((r - g) > TOL_RG) & ((b - g) > TOL_BG)
    a2 = np.where(tint, 0, a).astype(np.uint8)

    # ② co 1px
    a2 = cv2.erode(a2, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)

    # ③ giữ blob lớn nhất (bước ① có thể chẻ mask; cũng loại ✦ ở góc)
    nb, lab, st, _ = cv2.connectedComponentsWithStats((a2 > 8).astype(np.uint8), 8)
    if nb > 2:
        keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        a2 = np.where(lab == keep, a2, 0).astype(np.uint8)
        print(f"   bỏ {nb - 2} đốm rời (✦/mảnh vụn)")

    # ④ ⭐ KHOÉT THEO ĐĨA (chỉ khi `--circle`) — huy hiệu tròn thì đây là phép chắc nhất.
    # 🔴 Vì sao cần thêm bước này dù ①–③ đã báo "0 pixel magenta": vệt còn lại ở
    #    `brand_logo.png` là **quầng sáng HỒNG NHẠT** của ảnh gen (kiểu 255,200,220 ⇒
    #    `b−g` chỉ ~20 nên lọt cả hai ngưỡng). Phép đo theo màu magenta **không thấy nó**,
    #    và tao đã suýt kết luận "sạch" trên một ảnh còn smudge rõ ở 1:1.
    #    ⇒ Cùng bài học `feedback_do_pixel_cua_so_quet`: số đo sạch chỉ có nghĩa TRONG
    #      phạm vi thứ nó đo được. Với hình dạng đã biết thì khoét theo HÌNH DẠNG.
    # Đĩa suy từ VÀNH VÀNG, không từ toàn mask — quầng sáng nằm trong mask nên
    # `minEnclosingCircle` của cả mask sẽ phình ra bao luôn nó.
    # 🔴 Đo bán kính bằng PHÂN VỊ khoảng cách tới tâm, KHÔNG bằng `minEnclosingCircle`.
    #    Hai cách cũ đều hỏng, mỗi cách một kiểu:
    #      · fit vào VÀNH VÀNG  → sai khi huy hiệu có **vành navy NẰM NGOÀI vành vàng**
    #        (đúng logo beaker mới) ⇒ cắt mất viền tối, huy hiệu trông sứt.
    #      · `minEnclosingCircle` cả blob → một cái gai/quầng sáng dính vào rìa là bán kính
    #        phình theo (đúng logo cũ).
    #    Đĩa đầy thì tỉ lệ pixel trong bán kính r là (r/R)² ⇒ **p99,5 = R·√0,995**, tức chỉ
    #    lệch 0,25%. Một cái gai chiếm vài phần nghìn pixel gần như không dịch được phân vị.
    if "--circle" in sys.argv:
        blob = (a2 > 8)
        ys, xs = np.nonzero(blob)
        if len(xs) > 100:
            cx, cy = xs.mean(), ys.mean()
            d = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
            rad = float(np.percentile(d, 99.5)) / np.sqrt(0.995)
            disc = np.zeros_like(a2)
            cv2.circle(disc, (int(round(cx)), int(round(cy))),
                       int(round(rad * 1.002)), 255, -1)   # nới 0,2% cho khỏi cắn viền
            a2 = cv2.bitwise_and(a2, disc)
            print(f"   khoét theo đĩa: tâm ({cx:.0f},{cy:.0f}) r={rad:.0f} "
                  f"(phân vị 99,5 của {len(xs)} px; max {d.max():.0f})")
        else:
            print("   ⚠ blob quá nhỏ — bỏ qua bước khoét đĩa")

    out = im.copy()
    out[:, :, 3] = a2

    # ⑤ 🔴 CẮT SÁT bbox của alpha (mặc định; tắt bằng `--no-crop`).
    #    Bắt buộc vì `BrandOverlay` đặt `height: logoH` cho **CẢ TẤM ẢNH**: để lại viền
    #    trong suốt thì huy hiệu render ra nhỏ hơn `logoH` theo đúng tỉ lệ viền. Lô beaker
    #    ra 1835×1024 mà đĩa chỉ 792px ⇒ logo sẽ chỉ cao 85px thay vì 110px, và lệch sang
    #    một bên. Ảnh đã cắt sát thì `logoH` nghĩa đúng là chiều cao huy hiệu.
    if "--no-crop" not in sys.argv:
        ys, xs = np.nonzero(a2 > 8)
        if len(xs):
            m = 2
            y0, y1 = max(0, ys.min() - m), min(out.shape[0], ys.max() + 1 + m)
            x0, x1 = max(0, xs.min() - m), min(out.shape[1], xs.max() + 1 + m)
            out = out[y0:y1, x0:x1]
            print(f"   cắt sát: ({x0},{y0})–({x1},{y1}) ⇒ {x1-x0}×{y1-y0}")
    # RGB dưới alpha=0 vẫn để nguyên: không renderer nào đọc nó, và ghi đè là thêm một
    # bước có thể sai. Cái quyết định là ALPHA.
    imwrite_u(dst, out)

    after = count_fringe(out)
    print(f"✅ {dst}")
    print(f"   pixel ngả magenta (alpha>250): {before} → {after}")
    ys, xs = np.nonzero(a2 > 8)
    print(f"   hình còn lại: x {xs.min()}-{xs.max()} · y {ys.min()}-{ys.max()} "
          f"({xs.max()-xs.min()+1}×{ys.max()-ys.min()+1})")
    return 0 if after == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
