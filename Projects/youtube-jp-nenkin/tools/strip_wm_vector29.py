# -*- coding: utf-8 -*-
r"""strip_wm_vector29.py — xoá dấu ✦ trên ảnh AI **vector phẳng** (lô nenkin v29).

🔴 VÌ SAO CẦN FILE NÀY dù `ingest_art29.py` đã có bước vá: bước đó **dò vị trí ✦ bằng máy**
(local-contrast / residual) rồi `cv2.inpaint`, và nó in "✦ đã vá 90/90" — nhưng soi sheet crop
1:1 tại toạ độ chuẩn thì **còn ✦ ở hàng chục ảnh**. Đúng câu đã ghi ở `media-library.md`
§2.10 ⑤: *"số đo và exit code đều KHÔNG chứng minh ✦ đã sạch"*, và §5: *"định vị ✦ bằng máy đã
thất bại 4/4 lần"*. ⇒ Ở đây **không dò nữa**: vị trí là HẰNG SỐ đo bằng mắt, việc của máy chỉ
là xoá.

CÁCH XOÁ — hợp với chất liệu, không bê khuôn của ảnh photoreal sang:
  · Ảnh lô này là **vector phẳng**: trong một hộp 170px quanh ✦ chỉ có 1–3 màu đặc.
  · 🔴 Palette lấy từ **VÀNH NGOÀI hộp**, không lấy từ cả hộp. Bản đầu gom palette trên cả hộp
    và trượt 7 ảnh: ✦ to ~8% diện tích hộp nên nó **tự lọt vào palette** rồi được coi là màu
    nền hợp lệ. ✦ luôn ở giữa hộp ⇒ vành ngoài là mẫu nền sạch, theo định nghĩa.
  · ✦ là lớp trắng bán trong suốt phủ lên ⇒ nó tạo ra **màu LAI** không thuộc palette.
  · ⇒ gom palette của hộp → pixel nào cách palette gần nhất trong ngưỡng thì **snap về màu đó**.
    Mảng màu đặc và nét navy **không đổi** (chúng CHÍNH LÀ palette); chỉ màu lai bị kéo về.
  ⛔ Không dùng trung vị-theo-hàng (`strip_wm_thumb`): ✦ hay nằm đè lên biên hai mảng màu,
     trung vị hàng sẽ trả về màu lai ⇒ ra khối chữ nhật (đã đo ở `media-library.md` §6c).
  ⛔ Không dùng inpaint bán kính lớn: ở vector phẳng nó bo tròn mất góc của hình.

AN TOÀN — hộp nào KHÔNG phải vector phẳng thì BỎ QUA, không đoán:
  · palette >4 màu, hoặc tỉ lệ pixel không-thuộc-palette >18% ⇒ hộp có chữ/ảnh chụp ⇒ skip + báo
    tên ra để soi tay. Thà bỏ sót một ảnh còn hơn phá chữ 原典.
"""
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

VD = Path(__file__).resolve().parents[1] / "06_VIDEO" / "29_shikaku-kakuninsho-8gatsu-85sai"
ART = VD / "art_final"
BAK = VD / "_wm_orig"

# Hằng số đo BẰNG MẮT trên sheet crop 1:1 của chính lô này (1920×1080).
CX, CY, BOX = 0.930, 0.872, 170
# ✦ nửa đục trên teal đậm (62,124,120) ra (158,190,188) = cách 136 ⇒ trần 135 hụt ĐÚNG 1 đơn vị
# và để lại vệt mờ ở 4 ảnh. Đo rồi mới nới, đừng đoán.
DIST = 175
FLOOR = 3           # ✦ trên nền KEM chỉ chênh 5–16 ⇒ sàn 12 của bản đầu bỏ sót 5 ảnh
RIM = 22            # bề dày vành lấy mẫu nền
MAXPAL, MAXODD = 6, 0.18
AMIN, AMAX = 250, 9000   # diện tích ✦ đo được ~2.500–4.000 px ở khổ 1920


def palette(a):
    """Màu nền của hộp, lấy TỪ VÀNH NGOÀI (xem docstring — ✦ nằm giữa, không chạm vành)."""
    m = np.ones(a.shape[:2], bool)
    m[RIM:-RIM, RIM:-RIM] = False
    q = (a[m] // 10).reshape(-1, 3)
    key = q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]
    u, c = np.unique(key, return_counts=True)
    keep = u[c >= 0.04 * len(key)]
    return np.array([[(k // 10000) * 10 + 5, (k // 100 % 100) * 10 + 5, (k % 100) * 10 + 5]
                     for k in keep], dtype=float)


def clean(f: Path) -> str:
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(int)
    H, W, _ = a.shape
    cx, cy, r = int(W * CX), int(H * CY), BOX // 2
    x0, x1, y0, y1 = max(0, cx - r), min(W, cx + r), max(0, cy - r), min(H, cy + r)
    box = a[y0:y1, x0:x1]
    pal = palette(box)
    if len(pal) == 0 or len(pal) > MAXPAL:
        return f"skip (palette {len(pal)} màu)"
    d = np.linalg.norm(box[:, :, None, :] - pal[None, None, :, :], axis=3)
    near = d.argmin(2)
    dmin = d.min(2)
    odd = (dmin > DIST).mean()
    if odd > MAXODD:
        return f"skip (lạ {odd:.0%} — có chữ/ảnh chụp?)"
    # Vành chỉ một màu ⇒ theo định nghĩa cả hộp phải là màu đó; bỏ sàn để quét sạch ✦ mờ
    # trên nền kem (chênh 5–12, nằm ngay dưới sàn). Vật thật vẫn an toàn: nét navy cách nền
    # ~300 > DIST nên không bị đụng.
    # ⚠️ Sàn 0 KHÔNG dùng được nữa sau khi có lọc cụm: nó bắt cả nhiễu nén trên mảng phẳng
    # ⇒ cả hộp thành MỘT cụm chạm mép ⇒ bị loại sạch (đo được: "đã vá 0/95"). Sàn 3 loại nhiễu
    # (chênh 1–3) mà vẫn giữ ✦ mờ nhất trên nền kem (chênh 5–16).
    hit = (dmin > FLOOR) & (dmin <= DIST)
    # 🔴 LỌC THEO CỤM — không có bước này thì snap **ăn vào hình**: ở ảnh có biên hai mảng màu
    # chạy qua hộp, dải chống răng cưa dọc biên cũng rơi vào [floor, DIST] và bị kéo về màu kia
    # ⇒ ô 11/38/87 mọc mảng kem cắt vào vật (đã dựng sheet và thấy). Phân biệt được vì:
    #   ✦ là cụm RỜI, cỡ biết trước, nằm GIỮA hộp — biên thì dài và luôn CHẠM MÉP hộp.
    # Đúng phép lọc blob đã dùng cho cast cắt-nền (`media-library.md` §2.10 ⑨③).
    lab, n = ndimage.label(hit)
    keep = np.zeros_like(hit)
    edge = set(lab[0].tolist()) | set(lab[-1].tolist()) | set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    for i in range(1, n + 1):
        if i in edge:
            continue
        a_i = int((lab == i).sum())
        if AMIN <= a_i <= AMAX:
            keep |= lab == i
    hit = keep
    if hit.sum() < 400:
        return "sạch sẵn"
    box[hit] = pal[near[hit]]
    a[y0:y1, x0:x1] = box
    BAK.mkdir(exist_ok=True)
    if not (BAK / f.name).exists():
        shutil.copy2(f, BAK / f.name)
    Image.fromarray(a.astype(np.uint8)).save(f)
    return f"đã vá {int(hit.sum())} px"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    fs = sorted(ART.glob("shot_*.png"))
    n_fix = n_skip = 0
    for f in fs:
        r = clean(f)
        if r.startswith("đã vá"):
            n_fix += 1
        elif r.startswith("skip"):
            n_skip += 1
            print(f"  ⚠️ {f.name}: {r}")
    print(f"{len(fs)} ảnh · đã vá {n_fix} · BỎ QUA {n_skip} (soi tay) · còn lại sạch sẵn")
    print("⛔ CHƯA XONG: phải dựng lại sheet crop 1:1 và SOI MẮT — luật media-library §2.10 ⑤b.")
