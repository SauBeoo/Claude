# -*- coding: utf-8 -*-
"""
make_diagrams_codai.py — Diagram「なぜ効くのか」cho kênh 古代の秘訣 (co-dai).

Lý do tồn tại: kênh này bán CHIỀU SÂU (`02_CONTENT_STRATEGY.md` — gate「なぜ」).
Cơ chế hoá học/vật lý thì không chụp ảnh được → vẽ card diagram cùng tông
navy/vàng với slide của video_render, ghép liền mạch với ảnh thật + clip thật.

Dùng chung bộ vẽ (nền gradient, font, arrow, panel, ×/○) của
`youtube-jp-health/tools/make_diagrams.py` — chỉ THÊM diagram riêng của co-dai
vào cùng registry, nên CLI y hệt:

    python tools/make_diagrams_codai.py <SLIDES.json> <folder ảnh ra>
    python tools/make_diagrams_codai.py <SLIDES.json> <folder ảnh ra> <tên_diagram>   # test 1 cái

Entry SLIDES dùng diagram:  {"match": "...", "photo": true, "diagram": "neutralize_foam"}
(diagram ghi ra slide_<index>.png trong folder ảnh → video_render coi như ảnh full-frame.)

Thêm diagram mới = viết 1 hàm d_xxx(d) rồi khai báo trong DIAGRAMS ở cuối file.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"E:\Claude\Projects\youtube-jp-health\tools")))
import make_diagrams as D  # noqa: E402  (nền, font, helper, CLI dùng chung)

W, H = D.W, D.H
GOLD, WHITE, DIM, RED, GREEN = D.GOLD, D.WHITE, D.DIM, D.RED, D.GREEN
PANEL = D.PANEL

# ⚠️ VÙNG CẤM ĐÁY — phụ đề burn-in (video_render, style outline/pill) ăn từ ~y=780
# trở xuống khi phụ đề DÀI 2 DÒNG (1 dòng thì từ ~y=845). Câu thoại của kênh này
# thường xuyên 2 dòng → lấy mốc 2 dòng làm chuẩn. Mọi chi tiết CÓ NGHĨA (chữ, ×/○,
# mũi tên chốt hạ) phải nằm TRÊN mốc này; panel/nền trang trí thì tràn xuống được.
# Đo thật ở proof 06_proofA (2026-07-25): mốc 845 vẫn bị phụ đề 2 dòng đè.
SAFE_BOTTOM = 780
PANEL_BOTTOM = 828        # đáy tối đa cho khối nền (chữ vẫn phải ≤ SAFE_BOTTOM)
BLUE = (108, 158, 214)          # tông "acid" — lạnh
AMBER = (226, 168, 88)          # tông "alkali" — ấm
GRIME = (96, 78, 60)            # màu vệt bẩn


# ---------- icon riêng của ngách dọn dẹp ----------

def bubbles(d, cx, cy, w, h, n=26, color=(190, 226, 250)):
    """Cụm bọt khí bay lên (dùng cho phản ứng trung hoà / 過炭酸)."""
    import random
    rnd = random.Random(7)          # cố định seed → render lại y hệt
    for _ in range(n):
        r = rnd.randint(9, 26)
        x = cx + rnd.randint(-w // 2, w // 2)
        y = cy + rnd.randint(-h // 2, h // 2)
        d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=4)


def powder_jar(d, cx, cy, s, color=AMBER):
    """Hộp bột (重曹/過炭酸) — thân hộp + nắp + bột trắng phía trên."""
    d.rounded_rectangle([cx - s, cy - s * 0.55, cx + s, cy + s], s * 0.18, fill=color)
    d.rounded_rectangle([cx - s * 0.75, cy - s * 0.95, cx + s * 0.75, cy - s * 0.5],
                        s * 0.14, fill=tuple(max(0, c - 40) for c in color))
    d.rectangle([cx - s * 0.6, cy - s * 0.2, cx + s * 0.6, cy + s * 0.55],
                fill=(245, 245, 240))


def bottle(d, cx, cy, s, color=BLUE):
    """Chai lỏng (酢/クエン酸水) — cổ chai + thân + mực nước."""
    d.rectangle([cx - s * 0.22, cy - s * 1.05, cx + s * 0.22, cy - s * 0.6], fill=color)
    d.rounded_rectangle([cx - s * 0.6, cy - s * 0.62, cx + s * 0.6, cy + s], s * 0.2,
                        fill=color)
    d.rounded_rectangle([cx - s * 0.45, cy - s * 0.1, cx + s * 0.45, cy + s * 0.85],
                        s * 0.14, fill=tuple(min(255, c + 60) for c in color))


def scale_chunk(d, cx, cy, s, color=(238, 238, 232)):
    """Cục 水垢/尿石 — khối trắng lởm chởm (vảy khoáng)."""
    pts = [(cx - s, cy + s * 0.5), (cx - s * 0.8, cy - s * 0.2),
           (cx - s * 0.35, cy - s * 0.6), (cx + s * 0.1, cy - s * 0.85),
           (cx + s * 0.6, cy - s * 0.45), (cx + s, cy + s * 0.15),
           (cx + s * 0.7, cy + s * 0.6)]
    d.polygon(pts, fill=color)
    for k in range(4):                      # vân vảy
        y = cy - s * 0.4 + k * s * 0.3
        d.line([(cx - s * 0.7, y), (cx + s * 0.7, y)], fill=(206, 206, 198), width=4)


def grime_layer(d, x1, x2, y, th=34, color=GRIME):
    """Lớp bẩn bám (油/ぬめり) — dải dày bám mặt vật liệu."""
    d.rounded_rectangle([x1, y, x2, y + th], th // 2, fill=color)


# ---------- diagram ----------

def d_neutralize_foam(d):
    """Vì sao bọt trung hoà bóc được cặn bám (第二の知恵 — 重曹＋酢)."""
    D.title(d, "なぜ、泡が汚れをはがすのか", "アルカリ ＋ 酸 ＝ 二酸化炭素の泡")

    D.panel(d, [150, 240, 780, 505], (58, 48, 34))
    powder_jar(d, 300, 375, 72, AMBER)
    D.at(d, "重曹", 60, 560, 305, GOLD)
    D.at(d, "アルカリ性", 38, 560, 392, DIM)

    D.panel(d, [1140, 240, 1770, 505], (32, 46, 68))
    bottle(d, 1290, 375, 76, BLUE)
    D.at(d, "酢・クエン酸", 54, 1540, 305, (150, 200, 245))
    D.at(d, "酸性", 38, 1540, 392, DIM)

    D.arrow(d, (790, 425), (930, 512), GOLD, 12, 30)
    D.arrow(d, (1130, 425), (990, 512), (150, 200, 245), 12, 30)
    D.at(d, "二酸化炭素の泡", 50, W / 2, 534, WHITE)
    D.at(d, "すき間にもぐり込み、下から持ち上げてはがす", 44, W / 2, 600, GOLD)

    # bọt trồi lên từ dưới lớp bẩn, nâng lớp bẩn bong ra (mọi thứ trên SAFE_BOTTOM)
    bubbles(d, W / 2, 690, 760, 92)
    grime_layer(d, 470, 1450, SAFE_BOTTOM - 44, th=44)
    D.at(d, "汚れ", 44, 388, SAFE_BOTTOM - 48, DIM)
    for x in (620, 960, 1300):
        D.arrow(d, (x, SAFE_BOTTOM - 52), (x, 686), (190, 226, 250), 10, 26)


def d_acid_vs_alkali(d):
    """Vì sao cặn trắng phải dùng acid — cùng tính thì không tan (水垢/尿石)."""
    D.title(d, "白い水垢は「アルカリ性」", "同じ性質では落ちない。反対の性質で溶かす")

    scale_chunk(d, W / 2, 300, 112)
    D.at(d, "カルシウムが乾いて固まった汚れ", 40, W / 2, 412, DIM)

    # panel được tràn xuống PANEL_BOTTOM, nhưng CHỮ kết luận phải ≤ SAFE_BOTTOM
    D.panel(d, [150, 470, 900, PANEL_BOTTOM], (58, 40, 44))
    D.at(d, "アルカリの洗剤", 52, 525, 496, WHITE)
    powder_jar(d, 525, 610, 58, AMBER)
    D.xmark(d, 525, 692, 38)
    D.at(d, "ほとんど効かない", 44, 525, SAFE_BOTTOM - 44, RED)

    D.panel(d, [1020, 470, 1770, PANEL_BOTTOM], (30, 52, 44))
    D.at(d, "酢・クエン酸（酸）", 52, 1395, 496, WHITE)
    bottle(d, 1395, 610, 62, BLUE)
    D.omark(d, 1395, 692, 38)
    D.at(d, "すっと溶ける", 44, 1395, SAFE_BOTTOM - 44, GREEN)


def _trap(d, cx, top, water=True):
    """Mặt cắt ống chữ U dưới bồn — vẽ bằng nét dày hình chữ U để đọc ra ngay là ống.
    có/không đọng nước 封水 (mặt nước bịt mùi)."""
    grey, dark, wcol = (168, 176, 194), (26, 34, 50), (86, 150, 214)
    dx, bot = 160, top + 330
    path = [(cx - dx, top), (cx - dx, bot), (cx + dx, bot), (cx + dx, top)]
    d.line(path, fill=grey, width=132, joint="curve")      # vỏ ống
    d.line(path, fill=dark, width=104, joint="curve")      # lòng ống
    if water:
        wl = 150                                            # mực nước tính từ đáy
        d.line([(cx - dx, bot - wl), (cx - dx, bot), (cx + dx, bot), (cx + dx, bot - wl)],
               fill=wcol, width=104, joint="curve")
        D.at(d, "封水", 46, cx, bot - 46, (12, 20, 36))


def d_fusui(d):
    """封水 = mặt nước đọng bịt mùi cống. Cross-section — không ảnh nào chụp được."""
    D.title(d, "封水（ふうすい）＝ 臭いのふた", "排水口の底にたまった水が、下水の臭いをせき止める")

    for k, (cx, water, head, verdict) in enumerate((
            (560, True, "水がある", "臭いは上がれない"),
            (1400, False, "水が乾いた", "臭いが部屋へ"))):
        D.at(d, head, 54, cx, 258, WHITE if water else (250, 210, 120))
        _trap(d, cx, 330, water)
        col = GREEN if water else RED
        # mũi tên mùi từ dưới lên
        y_from, y_to = 748, (600 if water else 296)
        D.arrow(d, (cx + 160, y_from), (cx + 160, y_to), col, 13, 30)
        if water:
            D.at(d, "×", 80, cx + 160, 520, RED)
        D.at(d, verdict, 46, cx, SAFE_BOTTOM - 44, col)


DIAGRAMS = {
    "neutralize_foam": d_neutralize_foam,
    "acid_vs_alkali": d_acid_vs_alkali,
    "fusui": d_fusui,
}

D.DIAGRAMS.update(DIAGRAMS)

if __name__ == "__main__":
    D.main()
