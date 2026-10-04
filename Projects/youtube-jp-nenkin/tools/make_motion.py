# -*- coding: utf-8 -*-
"""Animation clip cho video — kênh 年金と老後のお金研究室 (COMBO, chốt 2026-07-19).

Xuất clip mp4 (anim 2.5–4s + đứng hình dài) cho renderer dùng qua "video": true.
Nền đứng yên tuyệt đối — chỉ nội dung số liệu/nhân vật chuyển động rồi dừng.

CLI:
    python tools/make_motion.py build <SLIDES.json> <clips_dir>   → dựng mọi clip theo CLIPS map
    python tools/make_motion.py demo                              → demo 4 cảnh cũ
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import make_diagrams as D

FPS = 30
HOLD = 75  # đứng hình dài — luôn phủ hết segment, renderer tự trim
W, H = D.W, D.H


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def seg(t, start, dur):
    return ease((t - start) / dur)


# ───────────── các cảnh (fn nhận d, img, t, **kw) ─────────────

_hook_photo_cache = {}


def bg_hook_photo():
    """Ảnh thật mở màn (slide_00.jpg) cover-crop + phủ tối nhẹ vùng chữ."""
    if "img" not in _hook_photo_cache:
        from PIL import Image, ImageDraw as _ID
        src = Path(__file__).parent.parent / "06_VIDEO" / "01_zaishoku-rorei-nenkin-kaisei-2026" / "slides_img" / "slide_00.jpg"
        im = Image.open(src).convert("RGB")
        ratio = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * ratio) + 1, int(im.height * ratio) + 1))
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                      (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        ov = Image.new("L", (1, H))
        for y in range(H):
            ov.putpixel((0, y), int(120 * max(0.0, 1 - y / (H * 0.55))))
        dark = Image.new("RGB", (W, H), (8, 10, 20))
        im = Image.composite(dark, im, ov.resize((W, H)))
        _hook_photo_cache["img"] = im
    return _hook_photo_cache["img"].copy()


def _center_stroke(d, txt, size, y, fill, sw=8, sf=(30, 24, 8)):
    w = d.textlength(txt, font=D.F(size))
    d.text(((W - w) / 2, y), txt, font=D.F(size), fill=fill, stroke_width=sw, stroke_fill=sf)


def a_hook_photo(d, img, t):
    """Hook trên ảnh thật: chữ vàng phóng to + dòng phụ hiện dần (nền ảnh đứng yên)."""
    _center_stroke(d, "あなたの年金、", 84, 90, (255, 255, 255), sw=6, sf=(20, 20, 26))
    p = seg(t, 0.1, 0.35)
    if p > 0:
        size = int(120 + 100 * p)
        _center_stroke(d, "＋月7万円!?", size, 240 + (220 - size) // 2, D.GOLD, sw=10)
    if t > 0.6:
        _center_stroke(d, "2026年4月、働くシニアのルールが変わった", 58, 560, (255, 255, 255), sw=6, sf=(20, 20, 26))


def a_hook(d, img, t):
    D.center(d, "あなたの年金、", 84, 170)
    p = seg(t, 0.1, 0.35)
    if p > 0:
        size = int(120 + 90 * p)
        D.center(d, "＋月7万円!?", size, 330 + (210 - size) // 2, D.GOLD)
    if t > 0.55:
        D.center(d, "2026年4月の改正で", 60, 680, D.DIM)
    if t > 0.75:
        D.center(d, "働くシニアのルールが大きく変わりました", 60, 770, D.WHITE)


def a_wall(d, img, t):
    D.title(d, "年金カットが始まるライン")
    D.at(d, "51万円", 96, 500, 430, D.DIM)
    D.at(d, "2025年度まで", 46, 500, 560, D.DIM)
    p_ar = seg(t, 0.15, 0.2)
    if p_ar > 0:
        x1 = 820 + int(260 * p_ar)
        d.line((820, 480, x1, 480), fill=D.GOLD, width=14)
        if p_ar >= 1:
            d.polygon([(1080, 440), (1080, 520), (1160, 480)], fill=D.GOLD)
    p = seg(t, 0.35, 0.4)
    if p > 0:
        D.at(d, f"{int(51 + 14 * p)}万円", 130, 1420, 400, D.GOLD)
        D.at(d, "2026年4月から", 46, 1420, 560, D.WHITE)
    if t > 0.85:
        D.center(d, "一気に ＋14万円", 76, 760, D.EDGE)


def a_people(d, img, t):
    D.title(d, "年金をカットされる人", "厚生労働省の試算")
    D.at(d, "約50万人", 100, 520, 400, D.OVER)
    d.line((830, 450, 1030, 450), fill=D.WHITE, width=10)
    d.polygon([(1030, 420), (1030, 480), (1090, 450)], fill=D.WHITE)
    p = seg(t, 0.2, 0.45)
    if p > 0:
        D.at(d, f"約{int(50 - 20 * p)}万人", 100, 1400, 400, D.DIM)
    if t > 0.75:
        D.center(d, "およそ20万人が カットの対象外に", 74, 700, D.SAFE)


def a_cast(d, img, t, ira, ttl, sub, sal, pen, verdict, vcol):
    D.title(d, ttl, sub, D.INK, D.INK_SUB)
    p0 = seg(t, 0.05, 0.28)
    x = int(-560 + (130 + 560) * p0)
    D.paste_ira(img, ira, x, 300, 600)
    d2 = ImageDraw.Draw(img)
    if t > 0.32:
        d2.rounded_rectangle((820, 300, 1800, 700), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
        D.at(d2, f"給料 {sal}万円 ＋ 年金 {pen}万円", 60, 1310, 360, D.INK)
        p2 = seg(t, 0.45, 0.38)
        D.at(d2, f"合計 {int((sal + pen) * p2)}万円", 128, 1310, 470, vcol)
    if t > 0.88:
        D.at(d2, verdict, 62, 1310, 800, vcol)


def a_yamada(d, img, t):
    D.title(d, "山田さんご夫妻（大阪）", "夫67歳・再雇用 ／ 妻65歳・パート", D.INK, D.INK_SUB)
    p0 = seg(t, 0.05, 0.28)
    x = int(-620 + (120 + 620) * p0)
    D.paste_ira(img, "yamada_couple.png", x, 320, 560)
    d2 = ImageDraw.Draw(img)
    for i, (y0, who, sal, pen, st) in enumerate(((300, "夫", 26, 16, 0.35), (540, "妻", 10, 9, 0.55))):
        if t > st:
            d2.rounded_rectangle((820, y0, 1800, y0 + 210), radius=30, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
            D.at(d2, f"{who}　給料 {sal}万円 ＋ 年金 {pen}万円", 52, 1310, y0 + 30, D.INK)
            p = seg(t, st + 0.08, 0.25)
            D.at(d2, f"合計 {int((sal + pen) * p)}万円", 78, 1310, y0 + 100, D.INK_GREEN)
    if t > 0.9:
        D.at(d2, "？ 二人合わせたら 61万円…ぎりぎり？", 56, 960, 850, D.INK_EDGE)


def a_ladder(d, img, t, n):
    D.title(d, "「65万円の壁」で判定")
    x0, x1, y_base, y_top, vmax = 260, 1660, 900, 260, 78

    def ytov(v):
        return y_base - (y_base - y_top) * v / vmax

    y65 = ytov(65)
    p_line = seg(t, 0.0, 0.18)
    xs = list(range(int(x0), int(x1), 46))
    for xx in xs[: max(1, int(len(xs) * p_line))]:
        d.line((xx, y65, xx + 24, y65), fill=D.OVER, width=6)
    if p_line >= 1:
        D.at(d, "基準額 65万円", 50, x0 + 190, y65 - 72, D.OVER)
    cases = [("佐藤さん", 37), ("鈴木さん", 65), ("高橋さん", 70)][:n]
    span = (x1 - x0) / max(n, 1)
    for i, (name, total) in enumerate(cases):
        # bar cũ hiện sẵn, chỉ bar MỚI (cuối) mọc
        st = 0.25 if i == n - 1 else -1
        p = seg(t, st, 0.35) if st >= 0 else 1.0
        if p <= 0:
            continue
        cx = x0 + span * (i + 0.5)
        bw = 120
        v = total * p
        top = ytov(v)
        color = D.SAFE if total < 65 else (D.EDGE if total == 65 else D.OVER)
        if total > 65 and v > 65:
            d.rectangle((cx - bw, y65, cx + bw, y_base), fill=D.SAFE)
            d.rectangle((cx - bw, top, cx + bw, y65), fill=D.OVER)
        else:
            d.rectangle((cx - bw, top, cx + bw, y_base), fill=color if total <= 65 else D.SAFE)
        D.at(d, name, 52, cx, y_base + 22, D.WHITE)
        if p >= 1:
            D.at(d, f"{total}万円", 60, cx, ytov(total) - (200 if total > 65 else 78), color)
            if total > 65 and t > 0.75:
                D.at(d, f"超過 {total - 65}万円", 44, cx, ytov(total) - 120, D.OVER)
                D.at(d, f"→ 停止 {(total - 65) / 2:g}万円", 44, cx, ytov(total) - 66, D.OVER)


def a_count84(d, img, t):
    D.title(d, "鈴木さんの場合（給料45万＋年金20万）")
    D.panel(d, 100, 280, 940, 800)
    D.at(d, "2025年度まで", 56, 520, 320, D.DIM)
    D.at(d, "−月7万円", 76, 520, 460, D.OVER)
    D.at(d, "（年間84万円）", 66, 520, 580, D.OVER)
    if t > 0.35:
        D.panel(d, 980, 280, 1820, 800)
        D.at(d, "2026年4月から", 56, 1400, 320, D.DIM)
        p = seg(t, 0.45, 0.4)
        D.at(d, f"＋{int(84 * p)}万円", 100, 1400, 440, D.SAFE)
        D.at(d, "まるごと戻った", 66, 1400, 620, D.SAFE)
    if t > 0.9:
        D.center(d, "年間84万円の復活", 66, 880, D.GOLD)


def a_quiz(d, img, t, n, q, note):
    D.title(d, f"○×クイズ　第{n}問")
    D.panel(d, 200, 300, 1720, 620, D.PANEL_LT)
    size = 72
    while d.textlength(q, font=D.F(size)) > 1400 and size > 44:
        size -= 4
    D.at(d, q, size, 960, 420, D.WHITE)
    if t < 0.25:
        D.at(d, "○ か ✕ か ？", 90, 960, 760, D.EDGE)
    else:
        p = seg(t, 0.25, 0.2)
        r = int(90 * (2.4 - 1.4 * p)) if p < 1 else 90
        D.mark_x(d, 960, 780, r=r, w=max(int(r * 0.29), 10))
        if t > 0.6:
            D.at(d, note, 54, 960, 930, D.SAFE)


def a_tanaka(d, img, t):
    D.title(d, "田中さん（67歳・横浜）", "長年勤めた会社に再雇用・週5日勤務", D.INK, D.INK_SUB)
    p0 = seg(t, 0.05, 0.28)
    x = int(-560 + (150 + 560) * p0)
    D.paste_ira(img, "tanaka_ojiisan.png", x, 300, 580)
    d2 = ImageDraw.Draw(img)
    if t > 0.35:
        d2.rounded_rectangle((820, 320, 1800, 680), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
        D.at(d2, "お給料 も 年金 も", 66, 1310, 400, D.INK)
        if t > 0.55:
            D.at(d2, "両方 受け取っている", 76, 1310, 510, D.INK_EDGE)
    if t > 0.85:
        D.at(d2, "→ 在職老齢年金の「調整」の対象", 54, 960, 800, D.INK)


def a_mechanism(d, img, t):
    D.title(d, "在職老齢年金の仕組み")
    if t > 0.05:
        D.money_panel(d, 460, 280, "お給料（月）", "＿＿万円")
    if t > 0.25:
        D.at(d, "＋", 96, 800, 340, D.DIM)
        D.money_panel(d, 1140, 280, "厚生年金（月）", "＿＿万円")
    if t > 0.5:
        D.at(d, "＞ 基準額", 74, 1660, 340, D.EDGE)
    if t > 0.65:
        D.center(d, "超えた分 × １/２ だけ 支給停止", 84, 700, D.OVER)
    if t > 0.88:
        D.center(d, "（全部止まるわけではない）", 50, 830, D.DIM)


def _stamp(d, cx, cy, t, st, ok):
    p = seg(t, st, 0.18)
    if p <= 0:
        return False
    r = int(52 * (2.2 - 1.2 * p)) if p < 1 else 52
    (D.mark_o if ok else D.mark_x)(d, cx, cy, r=r, w=max(int(r * 0.3), 8))
    return p >= 1


def a_myth2p(d, img, t, ttl, lt, ls, rt, rs):
    D.title(d, ttl)
    if t > 0.08:
        D.panel(d, 100, 280, 940, 860)
        D.at(d, lt, 60, 520, 490, D.WHITE)
        if _stamp(d, 520, 390, t, 0.2, False) and t > 0.42:
            D.at(d, ls, 48, 520, 740, D.OVER)
    if t > 0.5:
        D.panel(d, 980, 280, 1820, 860)
        D.at(d, rt, 60, 1400, 490, D.WHITE)
        if _stamp(d, 1400, 390, t, 0.62, True) and t > 0.84:
            D.at(d, rs, 48, 1400, 740, D.SAFE)


def a_myth4(d, img, t):
    D.title(d, "勘違いその4「繰り下げれば戻ってくる」")
    if t > 0.1:
        D.panel(d, 260, 300, 1660, 640, D.PANEL_LT)
        D.at(d, "在職老齢年金で止められた部分", 62, 960, 360, D.WHITE)
    if t > 0.45:
        p = seg(t, 0.45, 0.25)
        D.at(d, "→ 繰り下げ増額の対象外"[: max(1, int(13 * p))], 72, 960, 480, D.OVER)
    if t > 0.8:
        D.center(d, "カットされた分は、あとから取り戻せない", 60, 760, D.OVER)


def a_wall2_news(d, img, t):
    d.rectangle((70, 130, 340, 220), fill=D.NEWS_RED)
    D.at(d, "改正", 52, 205, 145, (255, 255, 255))
    D.at(d, "基準額（支給停止調整額）の見直し", 72, 1080, 150, D.NEWS_BLUE)
    hgt0 = int(400 * 51 / 70)
    d.rectangle((620 - 140, 800 - hgt0, 620 + 140, 800), fill=(150, 158, 170))
    D.at(d, "51万円", 84, 620, 800 - hgt0 - 100, (150, 158, 170))
    D.at(d, "2025年度", 50, 620, 820, D.NEWS_TEXT)
    p = seg(t, 0.2, 0.45)
    if p > 0:
        v = 51 + 14 * p
        hgt = int(400 * v / 70)
        d.rectangle((1300 - 140, 800 - hgt, 1300 + 140, 800), fill=D.NEWS_BLUE)
        D.at(d, f"{int(v)}万円", 84, 1300, 800 - hgt - 100, D.NEWS_BLUE)
        D.at(d, "2026年4月〜", 50, 1300, 820, D.NEWS_TEXT)
    if t > 0.85:
        D.at(d, "法律上62万円 → 賃金・物価反映で実際は65万円", 46, 960, 900, D.NEWS_TEXT)


def a_impact_news(d, img, t):
    d.rectangle((70, 130, 340, 220), fill=D.NEWS_RED)
    D.at(d, "試算", 52, 205, 145, (255, 255, 255))
    D.at(d, "カットされる年金の総額（年間）", 72, 1080, 150, D.NEWS_BLUE)
    D.at(d, "約4500億円", 104, 520, 420, D.NEWS_RED)
    d.line((900, 470, 1040, 470), fill=D.NEWS_TEXT, width=10)
    d.polygon([(1040, 440), (1040, 500), (1100, 470)], fill=D.NEWS_TEXT)
    p = seg(t, 0.2, 0.45)
    if p > 0:
        D.at(d, f"約{int(4500 - 1600 * p)}億円", 104, 1420, 420, (150, 158, 170))
    if t > 0.85:
        D.at(d, "その差は、働くシニアの手取りに戻る", 58, 960, 720, (30, 140, 84))


def a_per_person(d, img, t):
    D.title(d, "夫婦は「合算」しません", "一人ひとり、別々に判定")
    if t > 0.08:
        D.panel(d, 100, 270, 920, 720)
        D.at(d, "夫", 60, 510, 300, D.GOLD)
        p = seg(t, 0.15, 0.3)
        D.at(d, f"{int(42 * p)}万円", 110, 510, 420, D.SAFE)
        if p >= 1:
            D.at(d, "65万円以内 → 満額", 48, 510, 610, D.SAFE)
    if t > 0.4:
        D.panel(d, 1000, 270, 1820, 720)
        D.at(d, "妻", 60, 1410, 300, D.GOLD)
        p = seg(t, 0.45, 0.3)
        D.at(d, f"{int(19 * p)}万円", 110, 1410, 420, D.SAFE)
        if p >= 1:
            D.at(d, "65万円以内 → 満額", 48, 1410, 610, D.SAFE)
    if t > 0.8:
        D.at(d, "「合算61万円」で心配 → 不要", 60, 960, 840, D.EDGE)
        _stamp(d, 430, 870, t, 0.85, False)


def a_onepoint(d, img, t):
    D.title(d, "研究室からのワンポイント", "基礎年金は在職老齢年金の対象外")
    if t > 0.1:
        D.center(d, "基礎年金だけを繰り下げる", 90, 300, D.GOLD)
    if t > 0.35:
        D.center(d, "＋0.7％ × 遅らせた月数", 74, 480, D.WHITE)
    p = seg(t, 0.5, 0.35)
    if p > 0:
        D.center(d, f"70歳まで繰り下げ → ＋{int(42 * p)}％", 90, 620, D.SAFE)
    if t > 0.9:
        D.center(d, "※健康状態・家計で損得は変わります（参考情報）", 44, 880, D.DIM)


def a_steps(d, img, t):
    D.title(d, "ご自身の数字を確かめる 3ステップ")
    items = [("①", "年金月額を確認", "ねんきん定期便・ねんきんネット", 0.08),
             ("②", "給料側を確認", "月給＋ボーナス÷12", 0.38),
             ("③", "足して65万円と比べる", "超えた分の半分が調整", 0.68)]
    for i, (no, head, sub, st) in enumerate(items):
        p = seg(t, st, 0.22)
        if p <= 0:
            continue
        y = 270 + i * 220
        off = int((1 - p) * -700)
        D.panel(d, 220 + off, y, 1700 + off, y + 180)
        D.at(d, no, 80, 330 + off, y + 46, D.GOLD)
        d.text((460 + off, y + 28), head, font=D.F(66), fill=D.WHITE)
        d.text((460 + off, y + 112), sub, font=D.F(44), fill=D.DIM)


# ═════════════════ SCRIPT 02 — 繰り下げ受給 (animation) ═════════════════

def a_k_hook(d, img, t):
    D.center(d, "70歳まで待って、", 84, 150)
    p = seg(t, 0.1, 0.35)
    if p > 0:
        size = int(120 + 80 * p)
        D.center(d, "大損!?", size, 300 + (200 - size) // 2, D.OVER)
    if t > 0.6:
        D.center(d, "年金の「繰り下げ受給」", 60, 660, D.DIM)
    if t > 0.75:
        D.center(d, "損か得かの分かれ目 ―― 損益分岐点は約82歳", 58, 770, D.GOLD)


def a_k_grow(d, img, t):
    D.title(d, "繰り下げの増え方", "1か月遅らせるごとに")
    p = seg(t, 0.1, 0.4)
    if p > 0:
        size = int(90 + 60 * p)
        D.center(d, "＋0.7％ / 月", size, 350 + (150 - size) // 2, D.GOLD)
    if t > 0.7:
        D.center(d, "増えた金額は、その後ずっと 一生続く", 66, 640, D.SAFE)


def a_k_rate(d, img, t):
    D.title(d, "どれだけ増える？")
    rows = [("1年待つ", "＋8.4％", D.DIM, 0.1), ("5年・70歳まで", "＋42％", D.GOLD, 0.38), ("10年・75歳まで", "＋84％", D.SAFE, 0.66)]
    for i, (a, b, col, st) in enumerate(rows):
        p = seg(t, st, 0.22)
        if p <= 0:
            continue
        y = 300 + i * 210
        off = int((1 - p) * -700)
        D.panel(d, 260 + off, y, 1660 + off, y + 160)
        D.at(d, a, 62, 700 + off, y + 42, D.WHITE)
        D.at(d, b, 100, 1340 + off, y + 22, col)


def a_k_kuriage(d, img, t):
    D.title(d, "早める「繰り上げ」もある", "65歳より早く受け取る")
    if t > 0.1:
        D.center(d, "1か月ごとに −0.4％", 90, 350, D.OVER)
    if t > 0.4:
        D.center(d, "60歳まで早める → −24％", 96, 540, D.OVER)
    if t > 0.75:
        D.center(d, "この減額も、やはり 一生続く", 64, 780, D.DIM)


def a_k_cast_taka(d, img, t):
    D.title(d, "高橋さん（65歳・東京）", "この春、部長を退職。5歳年下の妻", D.INK, D.INK_SUB)
    p0 = seg(t, 0.05, 0.28)
    x = int(-560 + (150 + 560) * p0)
    D.paste_ira(img, "takahashi_businessman.png", x, 300, 560)
    d2 = ImageDraw.Draw(img)
    if t > 0.35:
        d2.rounded_rectangle((820, 320, 1800, 700), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
        D.at(d2, "65歳からの年金　月20万円", 58, 1310, 400, D.INK)
        if t > 0.55:
            D.at(d2, "70歳まで待つと　月28.4万円", 58, 1310, 510, D.INK_EDGE)
    if t > 0.85:
        D.at(d2, "→ 待つべき？ 分岐点は？", 56, 1310, 800, D.INK_RED)


def a_k_cast_sato(d, img, t):
    D.title(d, "佐藤さん（66歳・仙台）", "単身。ご主人を早くに亡くされた", D.INK, D.INK_SUB)
    p0 = seg(t, 0.05, 0.28)
    x = int(-560 + (150 + 560) * p0)
    D.paste_ira(img, "sato_obaasan.png", x, 300, 560)
    d2 = ImageDraw.Draw(img)
    if t > 0.35:
        d2.rounded_rectangle((820, 320, 1800, 700), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
        D.at(d2, "年金 月14万円で暮らす", 60, 1310, 400, D.INK)
        if t > 0.55:
            D.at(d2, "「待つ間の生活費は どこから？」", 50, 1310, 510, D.INK_RED)
    if t > 0.85:
        D.at(d2, "→ 迷わず 65歳で受給", 58, 1310, 800, D.INK_GREEN)


def a_k_65vs70(d, img, t):
    D.title(d, "高橋さん：65歳 と 70歳", "年金 月額の比較")
    if t > 0.05:
        D.money_panel(d, 560, 320, "65歳から受け取る", "月20万円", D.WHITE)
    if t > 0.35:
        D.money_panel(d, 1360, 320, "70歳まで待つ", "月28.4万円", D.GOLD)
    if t > 0.75:
        D.center(d, "月に ＋8万円以上（年 約100万円）", 76, 720, D.SAFE)


def a_k_forgone(d, img, t):
    D.title(d, "でも、待つ5年間は…", "年金を1円も受け取れない")
    if t > 0.1:
        D.center(d, "240万円 × 5年", 96, 360, D.WHITE)
    p = seg(t, 0.4, 0.35)
    if p > 0:
        D.center(d, f"＝ {int(1200 * p)}万円", 160, 500, D.OVER)
    if t > 0.85:
        D.center(d, "受け取らずに 見送る総額", 60, 800, D.EDGE)


def a_k_calc(d, img, t):
    D.title(d, "元をとるのに、何年かかる？")
    if t > 0.1:
        D.center(d, "1200万円 ÷ 年100万円 ≒ 12年", 90, 360, D.WHITE)
    if t > 0.45:
        D.center(d, "70歳 ＋ 12年", 84, 560, D.DIM)
    if t > 0.7:
        D.center(d, "＝ およそ 82歳で追いつく", 96, 700, D.GOLD)


def a_k_breakeven(d, img, t):
    D.title(d, "損益分岐点は およそ82歳", "累計で受け取る額の逆転")
    x0, y0, x1, y1 = 320, 860, 1620, 300
    vmax = 7200
    d.line((x0, y0, x1, y0), fill=D.DIM, width=4)
    d.line((x0, y0, x0, y1), fill=D.DIM, width=4)

    def X(age):
        return x0 + (x1 - x0) * (age - 65) / 25

    def Y(v):
        return y0 - (y0 - y1) * v / vmax

    p = seg(t, 0.1, 0.6)
    amax = 65 + 25 * p

    def poly(f):
        pts, a = [], 65.0
        while a <= amax:
            pts.append((X(a), Y(f(a))))
            a += 0.5
        pts.append((X(amax), Y(f(amax))))
        return pts

    if amax > 65.2:
        d.line(poly(lambda a: 240 * (a - 65)), fill=D.SAFE, width=8)
        d.line(poly(lambda a: 0 if a < 70 else 340 * (a - 70)), fill=D.GOLD, width=8)
    D.at(d, "65歳", 40, x0, y0 + 20, D.DIM)
    D.at(d, "90歳", 40, x1, y0 + 20, D.DIM)
    if t > 0.72:
        cx = X(82)
        for yy in range(int(y1), int(y0), 34):
            d.line((cx, yy, cx, yy + 18), fill=D.OVER, width=4)
        D.at(d, "82歳", 50, cx, y0 + 20, D.OVER)
    if t > 0.82:
        D.at(d, "65歳受給", 46, X(87), Y(240 * 24) - 20, D.SAFE)
        D.at(d, "70歳受給", 46, X(86), Y(340 * 20) - 20, D.GOLD)


def a_k_longevity(d, img, t):
    D.title(d, "寿命しだいで、こう変わる", "70歳まで待った場合")
    for cx, label, amt, col, sub, st in ((560, "90歳まで生きたら", "＋約800万円", D.SAFE, "待って得", 0.1),
                                         (1360, "78歳で終えたら", "−約400万円", D.OVER, "待って損", 0.45)):
        if t > st:
            D.panel(d, cx - 400, 300, cx + 400, 760)
            D.at(d, label, 56, cx, 350, D.WHITE)
            if t > st + 0.12:
                D.at(d, amt, 92, cx, 480, col)
            if t > st + 0.22:
                D.at(d, sub, 64, cx, 640, col)


def a_k_netbreak(d, img, t):
    D.title(d, "税・保険料まで考えると", "分岐点は後ろへずれる")
    if t > 0.1:
        D.center(d, "額面 … およそ 82歳", 90, 360, D.GOLD)
    if t > 0.45:
        D.center(d, "手取り … およそ 84歳", 90, 540, D.EDGE)
    if t > 0.75:
        D.center(d, "増えた年金には 税・保険料もかかる", 56, 780, D.DIM)


def a_k_75wait(d, img, t):
    D.title(d, "75歳まで目いっぱい待つと", "増額 ＋84％・月36.8万円")
    if t > 0.1:
        D.center(d, "受け取らない期間 10年 ＝ 2400万円", 72, 380, D.OVER)
    if t > 0.45:
        D.center(d, "分岐点は さらに後ろ、約87歳", 90, 580, D.EDGE)
    if t > 0.78:
        D.center(d, "長く待つほど増えるが、ゴールも遠のく", 54, 820, D.DIM)


def a_k_pitfall1(d, img, t):
    D.title(d, "落とし穴①　加給年金", "65歳未満の配偶者がいる人")
    if t > 0.1:
        D.center(d, "家族手当のような上乗せ 年 約42万円", 64, 350, D.WHITE)
    if t > 0.45:
        D.center(d, "厚生年金の繰り下げ中は 受け取れない", 72, 520, D.OVER)
    if t > 0.75:
        D.center(d, "しかも 繰り下げても 1円も増えない", 64, 720, D.OVER)


def a_k_pitfall2(d, img, t):
    D.title(d, "落とし穴②　働きながら受け取る人", "在職老齢年金（前回の復習）")
    if t > 0.1:
        D.center(d, "給料と年金が高い → 厚生年金の一部が止まる", 58, 360, D.WHITE)
    if t > 0.45:
        D.center(d, "止められた部分は 繰り下げても増えない", 72, 560, D.OVER)
    if t > 0.78:
        D.center(d, "高収入で働き続ける人ほど 増えにくい", 56, 780, D.DIM)


def a_k_pitfall3(d, img, t):
    D.title(d, "落とし穴③　遺族年金")
    if t > 0.1:
        D.center(d, "繰り下げで増やした分は", 64, 360, D.WHITE)
    if t > 0.45:
        D.center(d, "遺族年金には 反映されない", 84, 520, D.OVER)
    if t > 0.78:
        D.center(d, "「自分が長生きして受け取る」前提の制度", 54, 760, D.DIM)


def a_k_burden(d, img, t):
    D.title(d, "増えた年金が 連れてくる負担")
    items = [("医療費の窓口負担　2割 → 3割", D.OVER, 0.1), ("介護保険料", D.WHITE, 0.3),
             ("住民税", D.WHITE, 0.45), ("健康保険料", D.WHITE, 0.6)]
    for i, (it, col, st) in enumerate(items):
        p = seg(t, st, 0.22)
        if p <= 0:
            continue
        y = 300 + i * 135
        off = int((1 - p) * -700)
        D.panel(d, 360 + off, y, 1560 + off, y + 108)
        D.at(d, it, 56, 960 + off, y + 22, col)
    if t > 0.85:
        D.center(d, "額面42％増でも 手取りは思ったほど増えない", 48, 905, D.EDGE)


def a_k_smart1(d, img, t):
    D.title(d, "かしこい待ち方①", "基礎年金「だけ」を繰り下げる")
    if t > 0.08:
        D.panel(d, 120, 320, 940, 720)
        D.at(d, "厚生年金", 58, 530, 370, D.WHITE)
        D.at(d, "65歳から受け取る", 50, 530, 490, D.SAFE)
        D.at(d, "加給年金42万も確保", 48, 530, 600, D.SAFE)
    if t > 0.45:
        D.panel(d, 1000, 320, 1820, 720)
        D.at(d, "基礎年金", 58, 1410, 370, D.WHITE)
        D.at(d, "70歳まで繰り下げ", 50, 1410, 490, D.GOLD)
        D.at(d, "＋42％に育てる", 48, 1410, 600, D.GOLD)
    if t > 0.85:
        D.center(d, "これが「両取り」", 74, 800, D.GOLD)


def a_k_smart_calc(d, img, t):
    D.title(d, "高橋さんの基礎年金で試すと")
    if t > 0.1:
        D.center(d, "月6.5万円 → 月9.2万円", 96, 380, D.WHITE)
    p = seg(t, 0.4, 0.35)
    if p > 0:
        D.center(d, f"＋月{2.7 * p:.1f}万円", 130, 540, D.GOLD)
    if t > 0.85:
        D.center(d, "これが 一生 上乗せされる", 64, 780, D.SAFE)


def a_k_smart2(d, img, t):
    D.title(d, "かしこい待ち方②", "気が変わっても やり直せる")
    if t > 0.1:
        D.center(d, "待機中にお金が必要 → 65歳にさかのぼり一括受給", 54, 360, D.WHITE)
    if t > 0.45:
        D.center(d, "増額はないが まとまった資金が手に入る", 60, 560, D.SAFE)
    if t > 0.75:
        D.center(d, "※ さかのぼれるのは 5年前まで（時効）", 52, 780, D.EDGE)


def a_k_self(d, img, t, no, q, verdict, vcol):
    D.title(d, f"セルフチェック 質問{no}")
    D.panel(d, 220, 300, 1700, 560, D.PANEL_LT)
    size = 70
    while d.textlength(q, font=D.F(size)) > 1360 and size > 42:
        size -= 4
    D.at(d, q, size, 960, 400, D.WHITE)
    for i, ln in enumerate(verdict):
        if t > 0.35 + i * 0.25:
            D.at(d, ln, 58, 960, 640 + i * 92, vcol)


CLIPS_02 = {
    0: (a_k_hook, D.bg, {}, 3.2),
    6: (a_k_grow, D.bg, {}, 2.8),
    7: (a_k_rate, D.bg, {}, 3.2),
    8: (a_k_kuriage, D.bg, {}, 3.0),
    12: (a_k_cast_taka, D.bg_warm, {}, 3.2),
    13: (a_k_65vs70, D.bg, {}, 3.0),
    14: (a_k_forgone, D.bg, {}, 3.0),
    15: (a_k_calc, D.bg, {}, 3.0),
    16: (a_k_breakeven, D.bg, {}, 4.2),
    17: (a_k_longevity, D.bg, {}, 3.2),
    18: (a_k_netbreak, D.bg, {}, 2.8),
    19: (a_k_75wait, D.bg, {}, 3.0),
    20: (a_k_cast_sato, D.bg_warm, {}, 3.2),
    24: (a_k_pitfall1, D.bg, {}, 3.0),
    26: (a_k_pitfall2, D.bg, {}, 3.0),
    27: (a_k_pitfall3, D.bg, {}, 3.0),
    28: (a_k_burden, D.bg, {}, 3.2),
    30: (a_k_smart1, D.bg, {}, 3.2),
    31: (a_k_smart_calc, D.bg, {}, 3.0),
    32: (a_k_smart2, D.bg, {}, 3.0),
    34: (a_k_self, D.bg, dict(no=1, q="65歳未満の配偶者が いますか？", verdict=["はい → 厚生年金の繰り下げは 加給年金を失う", "基礎年金だけの繰り下げを検討"], vcol=D.EDGE), 3.0),
    35: (a_k_self, D.bg, dict(no=2, q="待つ間の生活費に 余裕がありますか？", verdict=["いいえ → 無理に待たなくていい", "65歳受給も 立派な選択"], vcol=D.SAFE), 3.0),
    36: (a_k_self, D.bg, dict(no=3, q="長寿家系で、健康に自信は？", verdict=["はい → 繰り下げで増やす価値大", "分岐点82歳を こえやすい"], vcol=D.GOLD), 3.0),
}


def pick_clips(cfg_path):
    return CLIPS_02 if "kurisage" in Path(cfg_path).name else CLIPS


# ───────────── map index SLIDES → cảnh ─────────────

CLIPS = {
    0: (a_hook_photo, bg_hook_photo, {}, 3.0),  # ảnh thật bình minh + chữ vàng (user chốt 2026-07-20)
    2: (a_wall, D.bg, {}, 3.0),
    3: (a_people, D.bg, {}, 2.8),
    7: (a_tanaka, D.bg_warm, {}, 3.0),
    8: (a_mechanism, D.bg, {}, 3.2),
    9: (a_myth2p, D.bg, dict(ttl="よくある誤解", lt="働くと年金が\n全部なくなる", ls="誤解", rt="止まるのは\n超えた分の半分", rs="こちらが正解"), 3.4),
    12: (a_wall2_news, D.bg_news, {}, 3.0),
    13: (a_impact_news, D.bg_news, {}, 2.8),
    25: (a_per_person, D.bg, {}, 3.4),
    28: (a_myth2p, D.bg, dict(ttl="勘違いその1「国民年金も減らされる」", lt="厚生年金\n（報酬比例）", ls="調整の対象", rt="老齢基礎年金\n（国民年金）", rs="いくら稼いでも満額"), 3.4),
    29: (a_myth2p, D.bg, dict(ttl="勘違いその2「自営業でも減らされる」", lt="会社員\n（厚生年金加入）", ls="対象になる", rt="自営業\nフリーランス", rs="カット対象外"), 3.4),
    31: (a_myth4, D.bg, {}, 3.0),
    32: (a_onepoint, D.bg, {}, 3.2),
    34: (a_steps, D.bg, {}, 3.0),
    17: (a_cast, D.bg_warm, dict(ira="sato_obaasan.png", ttl="佐藤さん（66歳・仙台）", sub="スーパーでパート勤務", sal=23, pen=14, verdict="65万円まで余裕 → 満額", vcol=D.INK_GREEN), 3.0),
    18: (a_ladder, D.bg, dict(n=1), 2.6),
    19: (a_cast, D.bg_warm, dict(ira="suzuki_syachou.png", ttl="鈴木さん（65歳・名古屋）", sub="会社役員", sal=45, pen=20, verdict="ちょうど65万円 → 満額", vcol=D.INK_EDGE), 3.0),
    20: (a_ladder, D.bg, dict(n=2), 2.6),
    21: (a_count84, D.bg, {}, 3.0),
    22: (a_cast, D.bg_warm, dict(ira="takahashi_businessman.png", ttl="高橋さん（64歳・東京）", sub="現役の部長職", sal=50, pen=20, verdict="65万円を 5万円オーバー", vcol=D.INK_RED), 3.0),
    23: (a_ladder, D.bg, dict(n=3), 3.2),
    24: (a_yamada, D.bg_warm, {}, 3.4),
    37: (a_quiz, D.bg, dict(n=1, q="働くと、国民年金も減らされる", note="減る可能性があるのは 厚生年金の部分だけ"), 2.4),
    39: (a_quiz, D.bg, dict(n=2, q="夫婦の収入は、合算して判定される", note="一人ずつ、別々に判定"), 2.4),
    41: (a_quiz, D.bg, dict(n=3, q="65万円を超えたら、超えた分が全部止められる", note="止まるのは 超えた分の半分だけ"), 2.4),
}


def render_clip(fn, bg_fn, kw, dur, out_path):
    out_path = Path(out_path)
    tmp = out_path.parent / f"_frames_{out_path.stem}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    n = int(dur * FPS)
    for f in range(n):
        t = f / (n - 1)
        img = bg_fn()
        d = ImageDraw.Draw(img)
        fn(d, img, t, **kw)
        img.save(tmp / f"{f:05d}.png")
    cmd = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp / "%05d.png"),
           "-vf", f"tpad=stop_mode=clone:stop_duration={HOLD}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"ffmpeg lỗi ({out_path.name}):\n{r.stderr[-1500:]}")
    shutil.rmtree(tmp)
    print(f"  ✓ {out_path.name} ({dur}s anim + {HOLD}s hold)")


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: make_motion.py build <SLIDES.json> <clips_dir>")
    if sys.argv[1] == "build":
        cfg_path, clips_dir = Path(sys.argv[2]), Path(sys.argv[3])
        clips_dir.mkdir(parents=True, exist_ok=True)
        import json
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        clips = pick_clips(cfg_path)
        for idx, (fn, bg_fn, kw, dur) in sorted(clips.items()):
            if idx >= len(cfg):
                print(f"  ⚠ index {idx} vượt SLIDES — bỏ qua")
                continue
            render_clip(fn, bg_fn, kw, dur, clips_dir / f"clip_{idx:02d}.mp4")
        print(f"Xong: {len(clips)} clip → {clips_dir}")
    elif sys.argv[1] == "one":
        idx, clips_dir = int(sys.argv[2]), Path(sys.argv[3])
        clips = pick_clips(sys.argv[4]) if len(sys.argv) > 4 else CLIPS
        fn, bg_fn, kw, dur = clips[idx]
        render_clip(fn, bg_fn, kw, dur, clips_dir / f"clip_{idx:02d}.mp4")
    else:
        sys.exit("chế độ không hỗ trợ: build | one <idx> <clips_dir>")


if __name__ == "__main__":
    main()
