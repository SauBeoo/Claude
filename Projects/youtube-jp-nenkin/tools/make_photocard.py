# -*- coding: utf-8 -*-
r"""make_photocard.py — ảnh collage (scene) → PNG "mảnh ảnh DÁN" để cắm vào frame Remotion.

⭐ VÌ SAO (user chốt 2026-08-26, lần 5): *"tao muốn thêm các ảnh trong này vào nữa …
hay mày viết prompt gen ra các ảnh rồi cắt cho vào frame"*.
Ảnh trong `C:\Users\tuana\Downloads\download` là **ảnh SCENE đầy đủ** (bàn + điện thoại +
người), KHÔNG phải vật rời ⇒ `rembg` cắt ra cả mảng giấy (đã đo, `CLAUDE.md` §②).
⇒ Không cắt-nền được thì **đóng khung nó lại thành một MẢNH ẢNH DÁN** — đúng ngôn ngữ
collage: ảnh in ra, xé mép, dán nghiêng lên trang giấy, có bóng.

Làm 5 việc, mỗi việc bịt một lỗi đã biết:
 ① **viền giấy trắng xé** quanh ảnh (răng cưa ngẫu-nhiên-tiền-định theo seed, không phải
    bo tròn đều) — mép đều thì đọc ra ngay là "ảnh chèn", không phải "mảnh dán".
 ② **xoay nhẹ** ±2,5° — collage không bao giờ thẳng tuyệt đối.
 ③ **bóng giấy thật** (blur + lệch) chứ không phải box-shadow phẳng.
 ④ **2 miếng tape** ở 2 góc chéo nhau.
 ⑤ **cắt ✦ watermark trước khi đóng khung** — lô 1376×768 ✦ ở ~0,925W ⇒ cắt về 1229
    (cùng mốc `ingest_art_17.py`). Ảnh đã ingest ở `art/` thì đã cắt rồi, bỏ qua.

CHẠY:  python tools/make_photocard.py <slug>
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
CUT_W = 1229          # mốc cắt ✦ của lô 1376×768 (khớp ingest_art_17.py)
BORDER = 26           # bề dày viền giấy trắng
PAPER = (250, 246, 238)


def torn_mask(w, h, rng, amp=9, step=30):
    """Mặt nạ mảnh giấy: 4 mép răng cưa. Đây là thứ làm nó KHÔNG giống ảnh chèn."""
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    pts = []
    x = 0
    while x < w:                                     # mép trên
        pts.append((x, rng.randint(0, amp)))
        x += step
    pts.append((w, rng.randint(0, amp)))
    y = 0
    while y < h:                                     # mép phải
        pts.append((w - rng.randint(0, amp), y))
        y += step
    pts.append((w - rng.randint(0, amp), h))
    x = w
    while x > 0:                                     # mép dưới
        pts.append((x, h - rng.randint(0, amp)))
        x -= step
    pts.append((0, h - rng.randint(0, amp)))
    y = h
    while y > 0:                                     # mép trái
        pts.append((rng.randint(0, amp), y))
        y -= step
    d.polygon(pts, fill=255)
    return m


def tape(size, rot, rng):
    w, h = size
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rectangle((0, 0, w, h), fill=(233, 224, 199, 208))
    for i in range(0, w, 8):
        d.line((i, 0, i, h), fill=(213, 202, 173, 70))
    return t.rotate(rot, expand=True, resample=Image.BICUBIC)


def build(src, out, seed=0, rot=None, crop=True):
    """`crop=False` cho canvas TỰ DỰNG (genten screenshot đã khoanh đỏ): không có ✦ để cắt,
    và cắt về CUT_W là **mất cột số bên phải** (đã dính ở genten_03 video 18: mất cột 42.0%)."""
    rng = random.Random(seed)
    im = Image.open(src).convert("RGB")
    if crop and im.width > CUT_W:   # ⑤ ảnh AI chưa ingest → cắt ✦
        im = im.crop((0, 0, CUT_W, im.height))
    w, h = im.size

    # ① viền giấy trắng + mặt nạ xé
    cw, ch = w + BORDER * 2, h + BORDER * 2
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    paper = Image.new("RGBA", (cw, ch), (*PAPER, 255))
    card.paste(paper, (0, 0), torn_mask(cw, ch, rng))
    card.paste(im.convert("RGBA"), (BORDER, BORDER))

    # ④ tape 2 góc chéo
    tw, th = int(cw * 0.13), 40
    t1 = tape((tw, th), 22, rng)
    t2 = tape((tw, th), -18, rng)
    card.alpha_composite(t1, (-t1.width // 4, -t1.height // 3))
    card.alpha_composite(t2, (cw - t2.width + t2.width // 4, ch - t2.height + t2.height // 3))

    # ② xoay nhẹ  ③ bóng giấy
    r = rot if rot is not None else rng.choice([-2.4, -1.6, 1.5, 2.3])
    card = card.rotate(r, expand=True, resample=Image.BICUBIC)
    pad = 26
    fin = Image.new("RGBA", (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 112), (0, 0), card.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(11))
    fin.alpha_composite(sh, (pad + 8, pad + 11))
    fin.alpha_composite(card, (pad, pad))
    fin.save(out)
    return fin.size


# Lô 2 (2026-08-26): 5 ảnh SCENE mới cho 5 scene chưa có hero. Nguồn ở thư mục
# Downloads/`download (1)`, đã ingest vào `art/` dưới tên `card_src_*` (đổi tên + cắt ✦
# về 1229px như `ingest_art_17.py`).
# Lô 3 (2026-08-26): 15 hero còn thiếu cho TRỌN 12 chương. Prompt:
# `art_prompts_photocard2_FLOW.txt`. Góc xoay xen kẽ dấu để 2 scene liền nhau không
# nghiêng cùng chiều — nghiêng cùng chiều thì mắt đọc ra "cùng một mảnh, chỉ đổi ảnh".
SPEC = [
    ("card_src_c3_kiru.png",        "card_c3_kiru.png",        11, -2.1),
    ("card_src_c3_techo.png",       "card_c3_techo.png",       12,  1.7),
    ("card_src_c4_gotsu.png",       "card_c4_gotsu.png",       13, -1.5),
    ("card_src_c4_mynumber.png",    "card_c4_mynumber.png",    14,  2.2),
    ("card_src_c5_futatsu_koe.png", "card_c5_futatsu_koe.png", 15, -1.8),
    ("card_src_c5_jiki.png",        "card_c5_jiki.png",        16,  1.4),
    ("card_src_c7_honmono.png",     "card_c7_honmono.png",     17, -2.3),
    ("card_src_c7_isoganai.png",    "card_c7_isoganai.png",    18,  1.6),
    ("card_src_c9_watasanai.png",   "card_c9_watasanai.png",   19, -1.9),
    ("card_src_c9_kakenaosu.png",   "card_c9_kakenaosu.png",   20,  2.0),
    ("card_src_c9_soudan.png",      "card_c9_soudan.png",      21, -1.6),
    ("card_src_c10_quiz.png",       "card_c10_quiz.png",       22,  1.8),
    ("card_src_c11_okusama.png",    "card_c11_okusama.png",    23, -2.2),
    ("card_src_c12_note.png",       "card_c12_note.png",       24,  1.5),
    ("card_src_c12_okuru.png",      "card_c12_okuru.png",      25, -1.7),
    # LÔ CARD3 (2026-08-26) — 7 ảnh thay 7 chỗ đang dùng lại hero của scene khác.
    ("card_src_c2_te_tomaru.png",   "card_c2_te_tomaru.png",   26,  1.9),
    ("card_src_c9_hitokoto.png",    "card_c9_hitokoto.png",    27, -2.1),
    ("card_src_c4_keisatsu.png",    "card_c4_keisatsu.png",    28,  1.5),
    ("card_src_c9_mail_sms.png",    "card_c9_mail_sms.png",    29, -1.6),
    ("card_src_c2_hito_no_koe.png", "card_c2_hito_no_koe.png", 30,  2.3),
    ("card_src_c4_genten.png",      "card_c4_genten.png",      31, -1.4),
    ("card_src_c12_jikai.png",      "card_c12_jikai.png",      32,  1.7),
    ("card_src_kikai.png",       "card_kikai.png",     6,  1.9),
    ("card_src_yonhon.png",      "card_yonhon.png",    7, -2.0),
    ("card_src_madoguchi.png",   "card_madoguchi.png", 8,  1.6),
    ("card_src_toukei.png",      "card_toukei.png",    9, -1.7),
    ("card_src_kazoku.png",      "card_kazoku.png",   10,  2.2),
    ("art_denwa_furueru.png",    "card_denwa.png",   1, -1.8),
    ("art_te_tomaru.png",        "card_te.png",      2,  2.1),
    ("art_tsucho_kakenaosu.png", "card_kakenaosu.png", 3, -2.2),
    ("bg_tsukue_denwa.png",      "card_tsukue.png",  4,  1.4),
    ("art_tsuri_nakama.png",     "card_tsuri.png",   5, -1.5),
]


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    if not slug:
        print("dùng: python tools/make_photocard.py <slug>")
        return 1
    vdir = PROJ / "06_VIDEO" / slug
    art, dst = vdir / "art", vdir / "photocard"
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for src, out, seed, rot in SPEC:
        p = art / src
        if not p.exists():
            print(f"🔴 THIẾU {src}")
            continue
        sz = build(p, dst / out, seed, rot)
        print(f"   ✓ {out:<20} {sz[0]}×{sz[1]}  (xoay {rot:+.1f}°)  ← {src}")
        n += 1
    print(f"\n✓ {n}/{len(SPEC)} mảnh ảnh dán → {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
