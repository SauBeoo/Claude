# -*- coding: utf-8 -*-
r"""stamp_brand_shokutaku.py — đóng DẤU NHẬN DIỆN kênh 60代からの食卓 lên thumbnail.

VÌ SAO PHẢI LÀ TOOL, KHÔNG ĐỂ AI BAKE:
  Dấu nhận diện chỉ có giá trị khi nó **giống hệt từng pixel qua MỌI video**. AI gen mỗi
  lần vẽ một kiểu → không bao giờ thành nhận diện. Cùng lý do dấu 「秘」 của co-dai
  (`youtube-jp-co-dai/tools/stamp_brand.py`).

SPEC ĐO TỪ 2 BẢN LIVE ĐÃ ĐẠT GATE (2026-08-05) — video 11 麦茶 `faVfnoKXEos` và
video 12 ヨーグルト `aFbENSzinnQ`. Hai bản này khớp nhau từng thông số, nên đây là spec
của kênh, không phải tao tự bịa:
  · dải vàng mép TRÁI: rộng 18px trên khung 1280 = **1,41% bề ngang**, màu **#FFDE00**,
    chạy hết chiều cao. Có ở CẢ HAI bản → đây là neo nhận diện chính.
  · badge tròn ĐỎ **#FF3D31** chữ 「食卓」 trắng, **đường kính 25,7% chiều cao**
    (185px/720), lề ~1,5–3% từ hai cạnh của góc nó đứng.
  · Vị trí badge = **góc ĐỐI DIỆN cột chữ** (v11 chữ phải → badge dưới-trái;
    v12 chữ trái → badge trên-phải). Nên `--corner` là cờ bắt buộc nghĩ, không mặc định bừa.

⛔ Đừng đổi spec giữa các video — đổi là mất sạch giá trị nhận diện đã tích được.

CHẠY
    python tools\stamp_brand_shokutaku.py <ảnh vào> --corner tr|tl|br|bl [-o ra.png] [--preview]
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── SPEC ĐÃ KHOÁ ─────────────────────────────────────────────────────────────
YELLOW = (255, 222, 0)      # #FFDE00 — đo ở cả 2 bản
RED = (255, 61, 49)         # #FF3D31
WHITE = (255, 255, 255)
STRIPE_W = 0.0141           # bề ngang dải vàng / bề ngang khung
BADGE_D = 0.257             # đường kính badge / chiều cao khung
MARGIN = 0.028              # lề badge tới cạnh khung (theo bề ngang)
RING = 0.006                # vòng trắng quanh badge / chiều cao khung
LABEL = "食卓"

FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\YuGothB.ttc"),                                  # chuẩn của make_thumb kênh này
    Path(r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Black.otf"),  # dự phòng
]


def _font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise SystemExit("❌ Không thấy font nào trong FONT_CANDIDATES")


def stamp(src: Path, out: Path, corner: str) -> Path:
    im = Image.open(src).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)

    # ① dải vàng mép trái — neo nhận diện, LUÔN bên trái ở cả 2 bản chuẩn
    d.rectangle([0, 0, max(1, int(W * STRIPE_W)) - 1, H], fill=YELLOW)

    # ② badge tròn đỏ 「食卓」
    dia = int(H * BADGE_D)
    m = int(W * MARGIN)
    x0 = m if corner in ("tl", "bl") else W - dia - m
    y0 = m if corner in ("tl", "tr") else H - dia - m
    r = int(H * RING)
    d.ellipse([x0 - r, y0 - r, x0 + dia + r, y0 + dia + r], fill=WHITE)
    d.ellipse([x0, y0, x0 + dia, y0 + dia], fill=RED)
    f = _font(int(dia * 0.42))
    d.text((x0 + dia / 2, y0 + dia / 2), LABEL, font=f, fill=WHITE, anchor="mm")

    im.save(out, quality=95, subsampling=0) if out.suffix.lower() in (".jpg", ".jpeg") else im.save(out)
    print(f"[BRAND 食卓] {out}  (badge {corner}, {dia}px = {dia/H*100:.1f}% cao)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("-o", "--out")
    ap.add_argument("--corner", required=True, choices=("tr", "tl", "br", "bl"),
                    help="góc đặt badge — chọn góc ĐỐI DIỆN cột chữ")
    ap.add_argument("--preview", action="store_true", help="xuất thêm bản 168px + 120px")
    a = ap.parse_args()

    src = Path(a.src)
    out = Path(a.out) if a.out else src.with_name(f"{src.stem}_brand{src.suffix}")
    stamp(src, out, a.corner)

    if a.preview:
        im = Image.open(out)
        for w in (168, 120):
            p = out.with_name(f"{out.stem}_prev{w}.png")
            im.resize((w, round(w * im.size[1] / im.size[0])), Image.LANCZOS).save(p)
            print(f"  {w}px → {p.name}")


if __name__ == "__main__":
    main()
