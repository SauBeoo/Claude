# -*- coding: utf-8 -*-
r"""Gỡ watermark ✦ bằng CẮT KHUNG (không vá pixel) + backup gốc.

    python tools\strip_wm_crop.py 06_VIDEO\<slug>            # cắt
    python tools\strip_wm_crop.py 06_VIDEO\<slug> --restore  # trả lại bản gốc

Vì sao CẮT chứ không vá (theo đúng hướng dẫn trong `_media_library/strip_wm_star.py`):
đo 89 ảnh của video 19 → ✦ nằm ở **VỊ TRÍ CỐ ĐỊNH** (trung vị x=1278/1376 = 0.929 ·
y=670/768 = 0.872), xác nhận bằng 7 mẫu soi mắt. Khi nó cố định thì cắt là cách đúng:
**không artifact, không đoán alpha, không phải soi từng ảnh**.

🔴 Hai bài học đã đo được, đừng đi lại:
  · `strip_wm_star.py --check` **KHÔNG bắt được ✦ của lô này** — 89/89 dưới ngưỡng, và mọi
    vị trí nó trả về đều ≤0.900W tức là bắt nhầm vân nền. Template `wm_star_tmpl.npz` học từ
    lô khác nên hình/cỡ sao không khớp. **Đừng tin exit code của nó.**
  · Residual-max cũng lệch: 20/89 ảnh trả x≈1183 vì cực đại rơi vào **cánh trái** của sao
    hoặc highlight cạnh đó. Soi mắt mới thấy cả 20 ca ✦ vẫn ở đúng chỗ cũ.
  ⇒ Kết luận: định vị bằng máy ở đây không đáng tin; cái đáng tin là **vị trí cố định đã đo
    bằng mắt trên nhiều mẫu**, và cắt thì miễn nhiễm với sai số định vị.

Cắt: bỏ mọi thứ từ x ≥ 0.908W (=1250 với khung 1376) → ✦ ra ngoài khung với ~6px lề, rồi
trim đáy về đúng 16:9. Mất ~9,2% bề ngang + ~8,5% chiều cao — đánh đổi đã biết.
"""
import argparse, io, shutil, sys
from pathlib import Path
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
CUT_X = 0.908          # cắt phải tại tỉ lệ này của bề ngang
SUBDIRS = ("slides_img", "ai_clean", "slides_img_photo")  # + shokutaku 2026-08-13
BAK = "_wm_orig"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videodir")
    ap.add_argument("--restore", action="store_true")
    # ⭐ 2026-08-16: cho phep chinh moc cat theo TUNG LO.
    #   Mac dinh 0.908 giu nguyen (lo video 19, da chay 89 anh).
    #   Lo video 20 do bang MAT: ✦ trai nhat o x≈1255 (=0.912W) => 0.908 chi con 6px le.
    #   `media-library.md` §2.10⑤ ghi ro "co ✦ KHONG co dinh trong mot lo" (ca nenkin 12
    #   co anh nen xam voi tia dai toi 0.882W), nen ha ve 0.900 = 17px le. Gia: +0,8% be ngang.
    ap.add_argument("--cut", type=float, default=CUT_X,
                    help="ti le be ngang de cat phai (mac dinh %(default)s)")
    a = ap.parse_args()
    globals()["CUT_X"] = a.cut
    VD = Path(a.videodir)
    bak = VD / BAK

    if a.restore:
        n = 0
        for sub in SUBDIRS:
            src = bak / sub
            if not src.is_dir():
                continue
            for p in src.iterdir():
                shutil.copy2(p, VD / sub / p.name)
                n += 1
        print(f"trả lại {n} ảnh gốc từ {bak}")
        return

    done, skip = 0, 0
    for sub in SUBDIRS:
        d = VD / sub
        if not d.is_dir():
            continue
        (bak / sub).mkdir(parents=True, exist_ok=True)
        for p in sorted(d.iterdir()):
            if p.suffix.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            b = bak / sub / p.name
            if b.exists():          # đã cắt ở lượt trước → bỏ qua, KHÔNG cắt hai lần
                skip += 1
                continue
            shutil.copy2(p, b)
            im = Image.open(p).convert("RGB")
            W, H = im.size
            nw = int(W * CUT_X)
            nh = min(H, int(round(nw * 9 / 16)))
            im.crop((0, 0, nw, nh)).save(p, quality=95)
            done += 1
    print(f"cắt {done} ảnh · bỏ qua {skip} (đã có backup) · gốc lưu ở {bak}")
    if done:
        print("⚠️ SOI MẮT lại contact sheet — exit code không chứng minh ✦ đã sạch.")


if __name__ == "__main__":
    main()
