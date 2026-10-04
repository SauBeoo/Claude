# -*- coding: utf-8 -*-
"""Diagram tự vẽ — kênh 年金と老後のお金研究室 (COMBO 4 skin, chốt 2026-07-19).

Skin theo loại nội dung:
  navy  — biểu đồ số (mặc định)          warm — card cast いらすとや
  news  — tin 改正/給付金 (wall2/impact)   paper — 研究ノート
Contract: python tools/make_diagrams.py <SLIDES.json> <outdir> [tên_test]
"""
import inspect
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT_PATH = "C:/Windows/Fonts/YuGothB.ttc"
# navy palette
GOLD = (255, 213, 79); WHITE = (245, 245, 245); DIM = (168, 180, 202)
SAFE = (86, 204, 136); OVER = (235, 87, 87); EDGE = (255, 196, 60)
BG_TOP = (15, 23, 42); BG_BOT = (28, 40, 70); PANEL = (34, 46, 72); PANEL_LT = (44, 58, 90)
# warm (いらすとや) palette
WARM_TOP = (255, 249, 236); WARM_BOT = (250, 236, 214)
INK = (72, 60, 50); INK_SUB = (152, 138, 120)
INK_GREEN = (52, 148, 96); INK_RED = (198, 60, 52); INK_EDGE = (206, 138, 32)
# news palette
NEWS_BG = (238, 242, 246); NEWS_BLUE = (26, 84, 158); NEWS_RED = (208, 44, 44); NEWS_TEXT = (34, 40, 52)
# paper palette
PAPER = (247, 242, 228); P_LINE = (214, 206, 186); P_MARGIN = (226, 150, 140)

IRA_DIR = Path(__file__).parent.parent / "assets" / "irasutoya"
_fc, _ira = {}, {}


def F(size):
    if size not in _fc:
        _fc[size] = ImageFont.truetype(FONT_PATH, size)
    return _fc[size]


def IRA(name):
    if name not in _ira:
        _ira[name] = Image.open(IRA_DIR / name).convert("RGBA")
    return _ira[name]


def _grad(top, bot):
    img = Image.new("RGB", (W, H))
    for y in range(H):
        t = y / H
        img.paste(tuple(int(a + (b - a) * t) for a, b in zip(top, bot)), (0, y, W, y + 1))
    return img


def bg():
    return _grad(BG_TOP, BG_BOT)


def bg_warm():
    return _grad(WARM_TOP, WARM_BOT)


def bg_paper():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    for y in range(180, H, 96):
        d.line((90, y, W - 90, y), fill=P_LINE, width=3)
    d.line((230, 90, 230, H - 60), fill=P_MARGIN, width=4)
    return img


def bg_news():
    img = Image.new("RGB", (W, H), NEWS_BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 86), fill=NEWS_BLUE)
    tw = d.textlength("年金と老後のお金研究室", font=F(46))
    d.text((60, 16), "年金と老後のお金研究室", font=F(46), fill=(255, 255, 255))
    d.rectangle((0, H - 110, W, H), fill=(252, 252, 252))
    d.rectangle((0, H - 110, W, H - 104), fill=NEWS_BLUE)
    txt = "在職老齢年金：2026年4月から基準額65万円に引き上げ"
    tw = d.textlength(txt, font=F(44))
    d.text(((W - tw) / 2, H - 84), txt, font=F(44), fill=NEWS_TEXT)
    return img


def center(d, txt, size, y, fill=WHITE):
    w = d.textlength(txt, font=F(size))
    d.text(((W - w) / 2, y), txt, font=F(size), fill=fill)


def at(d, txt, size, cx, y, fill=WHITE):
    for i, ln in enumerate(txt.split("\n")):
        w = d.textlength(ln, font=F(size))
        d.text((cx - w / 2, y + i * (size + 14)), ln, font=F(size), fill=fill)


def title(d, txt, sub=None, color=GOLD, subcolor=DIM):
    size = 84
    while d.textlength(txt, font=F(size)) > W - 220 and size > 48:
        size -= 4
    center(d, txt, size, 62, color)
    if sub:
        center(d, sub, 44, 175, subcolor)


def panel(d, x0, y0, x1, y1, fill=PANEL, outline=None):
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=fill, outline=outline, width=5)


def mark_x(d, cx, cy, r=52, w=16, color=OVER):
    d.line((cx - r, cy - r, cx + r, cy + r), fill=color, width=w)
    d.line((cx - r, cy + r, cx + r, cy - r), fill=color, width=w)


def mark_o(d, cx, cy, r=52, w=16, color=SAFE):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=w)


def hanko(d, cx, cy, r, txt, color=INK_RED):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=max(int(r * 0.09), 6))
    at(d, txt, int(r * 0.6), cx, cy - r * 0.34, color)


def paste_ira(img, name, x, y, height):
    ch = IRA(name)
    scale = height / ch.height
    ch2 = ch.resize((int(ch.width * scale), height))
    img.paste(ch2, (x, y), ch2)


# ───────────────── warm cast cards (いらすとや) ─────────────────

def cast_card(d, img, ira_file, ttl, sub, sal, pen, verdict, vcol):
    title(d, ttl, sub, INK, INK_SUB)
    paste_ira(img, ira_file, 130, 300, 600)
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle((820, 300, 1800, 700), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
    at(d2, f"給料 {sal}万円 ＋ 年金 {pen}万円", 60, 1310, 360, INK)
    at(d2, f"合計 {sal + pen}万円", 128, 1310, 470, vcol)
    at(d2, verdict, 62, 1310, 800, vcol)


def d_cast_tanaka(d, img):
    title(d, "田中さん（67歳・横浜）", "長年勤めた会社に再雇用・週5日勤務", INK, INK_SUB)
    paste_ira(img, "tanaka_ojiisan.png", 150, 300, 580)
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle((820, 320, 1800, 680), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
    at(d2, "お給料 も 年金 も", 66, 1310, 400, INK)
    at(d2, "両方 受け取っている", 76, 1310, 510, INK_EDGE)
    at(d2, "→ 在職老齢年金の「調整」の対象", 54, 960, 800, INK)


def d_cast_yamada(d, img):
    title(d, "山田さんご夫妻（大阪）", "夫67歳・再雇用 ／ 妻65歳・パート", INK, INK_SUB)
    paste_ira(img, "yamada_couple.png", 120, 320, 560)
    d2 = ImageDraw.Draw(img)
    for y0, who, sal, pen in ((300, "夫", 26, 16), (540, "妻", 10, 9)):
        d2.rounded_rectangle((820, y0, 1800, y0 + 210), radius=30, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
        at(d2, f"{who}　給料 {sal}万円 ＋ 年金 {pen}万円", 52, 1310, y0 + 30, INK)
        at(d2, f"合計 {sal + pen}万円", 78, 1310, y0 + 100, INK_GREEN)
    at(d2, "？ 二人合わせたら 61万円…ぎりぎり？", 56, 960, 850, INK_EDGE)


# ───────────────── navy chart diagrams (giữ nguyên layout đã duyệt) ─────────────────

def money_panel(d, cx, y, label, value, color=WHITE, pw=430, ph=250):
    panel(d, cx - pw / 2, y, cx + pw / 2, y + ph)
    at(d, label, 46, cx, y + 28, DIM)
    at(d, value, 88, cx, y + 110, color)


def ladder(d, cases, note=None):
    title(d, "「65万円の壁」で判定", note)
    x0, x1, y_base, y_top, vmax = 260, 1660, 900, 260, 78

    def ytov(v):
        return y_base - (y_base - y_top) * v / vmax

    y65 = ytov(65)
    for xx in range(int(x0), int(x1), 46):
        d.line((xx, y65, xx + 24, y65), fill=OVER, width=6)
    at(d, "基準額 65万円", 50, x0 + 190, y65 - 72, OVER)
    n = len(cases)
    span = (x1 - x0) / n
    for i, (name, total) in enumerate(cases):
        cx = x0 + span * (i + 0.5)
        bw = 120
        color = SAFE if total < 65 else (EDGE if total == 65 else OVER)
        top = ytov(total)
        if total > 65:
            d.rectangle((cx - bw, y65, cx + bw, y_base), fill=SAFE)
            d.rectangle((cx - bw, top, cx + bw, y65), fill=OVER)
            at(d, f"超過 {total - 65}万円", 44, cx, top - 120, OVER)
            at(d, f"→ 停止 {(total - 65) / 2:g}万円", 44, cx, top - 66, OVER)
        else:
            d.rectangle((cx - bw, top, cx + bw, y_base), fill=color)
        at(d, f"{total}万円", 60, cx, top - (200 if total > 65 else 78), color)
        at(d, name, 52, cx, y_base + 22, WHITE)


def myth_lr(d, t, sub, lt, ls, rt, rs, lok=False, rok=True):
    title(d, t, sub)
    for cx, head, body, ok in ((520, lt, ls, lok), (1400, rt, rs, rok)):
        panel(d, cx - 420, 280, cx + 420, 860)
        (mark_o if ok else mark_x)(d, cx, 390)
        at(d, head, 60, cx, 490, WHITE)
        at(d, body, 48, cx, 740, SAFE if ok else OVER)


def quiz(d, n, q, answer_note=None):
    title(d, f"○×クイズ　第{n}問")
    panel(d, 200, 300, 1720, 620, PANEL_LT)
    size = 72
    while d.textlength(q, font=F(size)) > 1400 and size > 44:
        size -= 4
    at(d, q, size, 960, 420, WHITE)
    if answer_note is None:
        at(d, "○ か ✕ か ？", 90, 960, 760, EDGE)
    else:
        mark_x(d, 960, 780, r=90, w=26)
        at(d, answer_note, 54, 960, 930, SAFE)


def d_hook(d):
    center(d, "あなたの年金、", 84, 170)
    center(d, "＋月7万円!?", 210, 330, GOLD)
    center(d, "2026年4月の改正で", 60, 680, DIM)
    center(d, "働くシニアのルールが大きく変わりました", 60, 770, WHITE)


def d_wall(d):
    title(d, "年金カットが始まるライン")
    at(d, "51万円", 96, 500, 430, DIM)
    at(d, "2025年度まで", 46, 500, 560, DIM)
    d.line((820, 480, 1080, 480), fill=GOLD, width=14)
    d.polygon([(1080, 440), (1080, 520), (1160, 480)], fill=GOLD)
    at(d, "65万円", 130, 1420, 400, GOLD)
    at(d, "2026年4月から", 46, 1420, 560, WHITE)
    center(d, "一気に ＋14万円", 76, 760, EDGE)


def d_people(d):
    title(d, "年金をカットされる人", "厚生労働省の試算")
    at(d, "約50万人", 100, 520, 400, OVER)
    d.line((830, 450, 1030, 450), fill=WHITE, width=10)
    d.polygon([(1030, 420), (1030, 480), (1090, 450)], fill=WHITE)
    at(d, "約30万人", 100, 1400, 400, DIM)
    center(d, "およそ20万人が カットの対象外に", 74, 700, SAFE)


def d_mechanism(d):
    title(d, "在職老齢年金の仕組み")
    money_panel(d, 460, 280, "お給料（月）", "＿＿万円")
    at(d, "＋", 96, 800, 340, DIM)
    money_panel(d, 1140, 280, "厚生年金（月）", "＿＿万円")
    at(d, "＞ 基準額", 74, 1660, 340, EDGE)
    center(d, "超えた分 × １/２ だけ 支給停止", 84, 700, OVER)
    center(d, "（全部止まるわけではない）", 50, 830, DIM)


def d_rule(d):
    title(d, "今日の計算ルール（これだけ）")
    center(d, "給料 ＋ 年金月額 ＞ 65万円", 108, 350, WHITE)
    center(d, "→ 超えた分の半分が 止まる", 96, 560, OVER)
    center(d, "65万円以内なら 1円も減らない", 66, 800, SAFE)


def d_half(d):
    myth_lr(d, "よくある誤解", None,
            "働くと年金が\n全部なくなる", "誤解", "止まるのは\n超えた分の半分", "こちらが正解",
            lok=False, rok=True)


def d_suzuki_before(d):
    title(d, "鈴木さんの場合（給料45万＋年金20万）")
    for cx, label, body, color in (
            (520, "2025年度まで", "−月7万円\n（年間84万円）", OVER),
            (1400, "2026年4月から", "カット ゼロ\nまるごと戻った", SAFE)):
        panel(d, cx - 420, 280, cx + 420, 800)
        at(d, label, 56, cx, 320, DIM)
        yy = 460
        for ln in body.split("\n"):
            at(d, ln, 76, cx, yy, color)
            yy += 120
    center(d, "年間84万円の復活", 66, 880, GOLD)


def d_per_person(d):
    title(d, "夫婦は「合算」しません", "一人ひとり、別々に判定")
    panel(d, 100, 270, 920, 720)
    at(d, "夫", 60, 510, 300, GOLD)
    at(d, "42万円", 110, 510, 420, SAFE)
    at(d, "65万円以内 → 満額", 48, 510, 610, SAFE)
    panel(d, 1000, 270, 1820, 720)
    at(d, "妻", 60, 1410, 300, GOLD)
    at(d, "19万円", 110, 1410, 420, SAFE)
    at(d, "65万円以内 → 満額", 48, 1410, 610, SAFE)
    at(d, "「合算61万円」で心配 → 不要", 60, 960, 840, EDGE)
    mark_x(d, 430, 870, r=40, w=12)


def d_myth1(d):
    myth_lr(d, "勘違いその1「国民年金も減らされる」", None,
            "厚生年金\n（報酬比例）", "調整の対象", "老齢基礎年金\n（国民年金）", "いくら稼いでも満額",
            lok=False, rok=True)


def d_myth2(d):
    myth_lr(d, "勘違いその2「自営業でも減らされる」", None,
            "会社員\n（厚生年金加入）", "対象になる", "自営業\nフリーランス", "カット対象外",
            lok=False, rok=True)


def d_myth4(d):
    title(d, "勘違いその4「繰り下げれば戻ってくる」")
    panel(d, 260, 300, 1660, 640, PANEL_LT)
    at(d, "在職老齢年金で止められた部分", 62, 960, 360, WHITE)
    at(d, "→ 繰り下げ増額の対象外", 72, 960, 480, OVER)
    center(d, "カットされた分は、あとから取り戻せない", 60, 760, OVER)


def d_onepoint(d):
    title(d, "研究室からのワンポイント", "基礎年金は在職老齢年金の対象外")
    center(d, "基礎年金だけを繰り下げる", 90, 300, GOLD)
    center(d, "＋0.7％ × 遅らせた月数", 74, 480, WHITE)
    center(d, "70歳まで繰り下げ → ＋42％", 90, 620, SAFE)
    center(d, "※健康状態・家計で損得は変わります（参考情報）", 44, 880, DIM)


def d_steps(d):
    title(d, "ご自身の数字を確かめる 3ステップ")
    items = [("①", "年金月額を確認", "ねんきん定期便・ねんきんネット"),
             ("②", "給料側を確認", "月給＋ボーナス÷12"),
             ("③", "足して65万円と比べる", "超えた分の半分が調整")]
    for i, (no, head, sub) in enumerate(items):
        y = 270 + i * 220
        panel(d, 220, y, 1700, y + 180)
        at(d, no, 80, 330, y + 46, GOLD)
        d.text((460, y + 28), head, font=F(66), fill=WHITE)
        d.text((460, y + 112), sub, font=F(44), fill=DIM)


# ───────────────── news skin (改正/給付金) ─────────────────

def d_wall2_news(d):
    d.rectangle((70, 130, 340, 220), fill=NEWS_RED)
    at(d, "改正", 52, 205, 145, (255, 255, 255))
    at(d, "基準額（支給停止調整額）の見直し", 72, 1080, 150, NEWS_BLUE)
    for cx, label, v, color in ((620, "2025年度", 51, (150, 158, 170)), (1300, "2026年4月〜", 65, NEWS_BLUE)):
        hgt = int(400 * v / 70)
        d.rectangle((cx - 140, 800 - hgt, cx + 140, 800), fill=color)
        at(d, f"{v}万円", 84, cx, 800 - hgt - 100, color)
        at(d, label, 50, cx, 820, NEWS_TEXT)
    at(d, "法律上62万円 → 賃金・物価反映で実際は65万円", 46, 960, 940 - 40, NEWS_TEXT)


def d_impact_news(d):
    d.rectangle((70, 130, 340, 220), fill=NEWS_RED)
    at(d, "試算", 52, 205, 145, (255, 255, 255))
    at(d, "カットされる年金の総額（年間）", 72, 1080, 150, NEWS_BLUE)
    at(d, "約4500億円", 104, 520, 420, NEWS_RED)
    d.line((900, 470, 1040, 470), fill=NEWS_TEXT, width=10)
    d.polygon([(1040, 440), (1040, 500), (1100, 470)], fill=NEWS_TEXT)
    at(d, "約2900億円", 104, 1420, 420, (150, 158, 170))
    at(d, "その差は、働くシニアの手取りに戻る", 58, 960, 720, (30, 140, 84))


# ───────────────── paper skin (研究ノート) ─────────────────

def d_note_paper(d, img):
    at(d, "今日の研究ノート", 84, 900, 110, INK_RED)
    bullets = [
        "・基準額 51万円 → 65万円（2026年4月〜）",
        "・合計65万円以内なら 年金は満額",
        "・超えても 止まるのは「超えた分の半分」",
        "・判定は夫婦合算ではなく 一人ずつ",
        "・カット分は繰下げで戻らない",
        "　→ 基礎年金の繰下げは有効",
    ]
    y = 280
    for b in bullets:
        d.text((300, y), b, font=F(58), fill=INK)
        y += 100
    d.text((300, 930), "出典：厚生労働省・日本年金機構（2026年7月時点）", font=F(40), fill=INK_SUB)
    paste_ira(img, "mascot_hakui.png", 1500, 380, 480)
    d2 = ImageDraw.Draw(img)
    hanko(d2, 1700, 240, 110, "済")


# ═════════════════ SCRIPT 02 — 繰り下げ受給・損益分岐点 (navy/warm/paper) ═════════════════

def d_k_hook(d):
    center(d, "70歳まで待って、", 84, 150)
    center(d, "大損!?", 200, 300, OVER)
    center(d, "年金の「繰り下げ受給」", 60, 660, DIM)
    center(d, "損か得かの分かれ目 ―― 損益分岐点は約82歳", 58, 770, GOLD)


def d_k_lost40(d):
    title(d, "待っている間に、消えるお金")
    center(d, "受け取れたはずの", 60, 340, WHITE)
    center(d, "年 約42万円", 150, 440, OVER)
    center(d, "まるまる 取り逃すことも", 66, 720, EDGE)


def d_k_grow(d):
    title(d, "繰り下げの増え方", "1か月遅らせるごとに")
    center(d, "＋0.7％ / 月", 150, 350, GOLD)
    center(d, "増えた金額は、その後ずっと 一生続く", 66, 640, SAFE)


def d_k_rate(d):
    title(d, "どれだけ増える？")
    rows = [("1年待つ", "＋8.4％", DIM), ("5年・70歳まで", "＋42％", GOLD), ("10年・75歳まで", "＋84％", SAFE)]
    for i, (a, b, col) in enumerate(rows):
        y = 300 + i * 210
        panel(d, 260, y, 1660, y + 160)
        at(d, a, 62, 700, y + 42, WHITE)
        at(d, b, 100, 1340, y + 22, col)


def d_k_kuriage(d):
    title(d, "早める「繰り上げ」もある", "65歳より早く受け取る")
    center(d, "1か月ごとに −0.4％", 90, 350, OVER)
    center(d, "60歳まで早める → −24％", 96, 540, OVER)
    center(d, "この減額も、やはり 一生続く", 64, 780, DIM)


def d_k_twotier(d):
    title(d, "年金は「二階建て」", "基礎と厚生、別々に繰り下げできる")
    panel(d, 560, 300, 1360, 470, PANEL_LT)
    at(d, "2階　厚生年金", 64, 960, 350, WHITE)
    panel(d, 560, 500, 1360, 670, PANEL)
    at(d, "1階　基礎年金（国民年金）", 56, 960, 555, WHITE)
    center(d, "→ それぞれ 別々に繰り下げできる", 72, 760, GOLD)
    center(d, "これが「かしこい待ち方」のカギ", 50, 880, DIM)


def d_cast_takahashi02(d, img):
    title(d, "高橋さん（65歳・東京）", "この春、部長を退職。5歳年下の妻", INK, INK_SUB)
    paste_ira(img, "takahashi_businessman.png", 150, 300, 560)
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle((820, 320, 1800, 700), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
    at(d2, "65歳からの年金　月20万円", 58, 1310, 400, INK)
    at(d2, "70歳まで待つと　月28.4万円", 58, 1310, 510, INK_EDGE)
    at(d2, "→ 待つべき？ 分岐点は？", 56, 1310, 800, INK_RED)


def d_cast_sato02(d, img):
    title(d, "佐藤さん（66歳・仙台）", "単身。ご主人を早くに亡くされた", INK, INK_SUB)
    paste_ira(img, "sato_obaasan.png", 150, 300, 560)
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle((820, 320, 1800, 700), radius=34, fill=(255, 255, 255), outline=(228, 210, 184), width=5)
    at(d2, "年金 月14万円で暮らす", 60, 1310, 400, INK)
    at(d2, "「待つ間の生活費は どこから？」", 50, 1310, 510, INK_RED)
    at(d2, "→ 迷わず 65歳で受給", 58, 1310, 800, INK_GREEN)


def d_k_65vs70(d):
    title(d, "高橋さん：65歳 と 70歳", "年金 月額の比較")
    money_panel(d, 560, 320, "65歳から受け取る", "月20万円", WHITE)
    money_panel(d, 1360, 320, "70歳まで待つ", "月28.4万円", GOLD)
    center(d, "月に ＋8万円以上（年 約100万円）", 76, 720, SAFE)


def d_k_forgone(d):
    title(d, "でも、待つ5年間は…", "年金を1円も受け取れない")
    center(d, "240万円 × 5年", 96, 360, WHITE)
    center(d, "＝ 1200万円", 160, 500, OVER)
    center(d, "受け取らずに 見送る総額", 60, 800, EDGE)


def d_k_calc(d):
    title(d, "元をとるのに、何年かかる？")
    center(d, "1200万円 ÷ 年100万円 ≒ 12年", 90, 360, WHITE)
    center(d, "70歳 ＋ 12年", 84, 560, DIM)
    center(d, "＝ およそ 82歳で追いつく", 96, 700, GOLD)


def d_k_breakeven(d):
    title(d, "損益分岐点は およそ82歳", "累計で受け取る額の逆転")
    x0, y0, x1, y1 = 320, 860, 1620, 300
    vmax = 7200
    d.line((x0, y0, x1, y0), fill=DIM, width=4)
    d.line((x0, y0, x0, y1), fill=DIM, width=4)

    def X(age):
        return x0 + (x1 - x0) * (age - 65) / 25

    def Y(v):
        return y0 - (y0 - y1) * v / vmax

    pts65 = [(X(a), Y(240 * (a - 65))) for a in range(65, 91)]
    pts70 = [(X(a), Y(0 if a < 70 else 340 * (a - 70))) for a in range(65, 91)]
    d.line(pts65, fill=SAFE, width=8)
    d.line(pts70, fill=GOLD, width=8)
    cx = X(82)
    for yy in range(int(y1), int(y0), 34):
        d.line((cx, yy, cx, yy + 18), fill=OVER, width=4)
    at(d, "82歳", 50, cx, y0 + 20, OVER)
    at(d, "65歳", 40, x0, y0 + 20, DIM)
    at(d, "90歳", 40, x1, y0 + 20, DIM)
    at(d, "65歳受給", 46, X(87), Y(240 * 24) - 20, SAFE)
    at(d, "70歳受給", 46, X(86), Y(340 * 20) - 20, GOLD)


def d_k_longevity(d):
    title(d, "寿命しだいで、こう変わる", "70歳まで待った場合")
    for cx, label, amt, col, sub in ((560, "90歳まで生きたら", "＋約800万円", SAFE, "待って得"),
                                     (1360, "78歳で終えたら", "−約400万円", OVER, "待って損")):
        panel(d, cx - 400, 300, cx + 400, 760)
        at(d, label, 56, cx, 350, WHITE)
        at(d, amt, 92, cx, 480, col)
        at(d, sub, 64, cx, 640, col)


def d_k_netbreak(d):
    title(d, "税・保険料まで考えると", "分岐点は後ろへずれる")
    center(d, "額面 … およそ 82歳", 90, 360, GOLD)
    center(d, "手取り … およそ 84歳", 90, 540, EDGE)
    center(d, "増えた年金には 税・保険料もかかる", 56, 780, DIM)


def d_k_75wait(d):
    title(d, "75歳まで目いっぱい待つと", "増額 ＋84％・月36.8万円")
    center(d, "受け取らない期間 10年 ＝ 2400万円", 72, 380, OVER)
    center(d, "分岐点は さらに後ろ、約87歳", 90, 580, EDGE)
    center(d, "長く待つほど増えるが、ゴールも遠のく", 54, 820, DIM)


def d_k_split(d):
    title(d, "待てる人・待てない人", "最初の分かれ道")
    panel(d, 120, 300, 940, 780)
    at(d, "高橋さん", 62, 530, 350, GOLD)
    at(d, "蓄え・収入がある", 54, 530, 480, WHITE)
    at(d, "→ 待って増やせる", 54, 530, 630, SAFE)
    panel(d, 1000, 300, 1820, 780)
    at(d, "佐藤さん", 62, 1410, 350, GOLD)
    at(d, "年金で 今の暮らし", 54, 1410, 480, WHITE)
    at(d, "→ 65歳で受け取る", 54, 1410, 630, EDGE)


def d_k_pitfall1(d):
    title(d, "落とし穴①　加給年金", "65歳未満の配偶者がいる人")
    center(d, "家族手当のような上乗せ 年 約42万円", 64, 350, WHITE)
    center(d, "厚生年金の繰り下げ中は 受け取れない", 72, 520, OVER)
    center(d, "しかも 繰り下げても 1円も増えない", 64, 720, OVER)


def d_k_pitfall2(d):
    title(d, "落とし穴②　働きながら受け取る人", "在職老齢年金（前回の復習）")
    center(d, "給料と年金が高い → 厚生年金の一部が止まる", 58, 360, WHITE)
    center(d, "止められた部分は 繰り下げても増えない", 72, 560, OVER)
    center(d, "高収入で働き続ける人ほど 増えにくい", 56, 780, DIM)


def d_k_pitfall3(d):
    title(d, "落とし穴③　遺族年金")
    center(d, "繰り下げで増やした分は", 64, 360, WHITE)
    center(d, "遺族年金には 反映されない", 84, 520, OVER)
    center(d, "「自分が長生きして受け取る」前提の制度", 54, 760, DIM)


def d_k_burden(d):
    title(d, "増えた年金が 連れてくる負担")
    items = [("医療費の窓口負担　2割 → 3割", OVER), ("介護保険料", WHITE),
             ("住民税", WHITE), ("健康保険料", WHITE)]
    for i, (it, col) in enumerate(items):
        y = 300 + i * 135
        panel(d, 360, y, 1560, y + 108)
        at(d, it, 56, 960, y + 22, col)
    center(d, "額面42％増でも 手取りは思ったほど増えない", 48, 905, EDGE)


def d_k_smart1(d):
    title(d, "かしこい待ち方①", "基礎年金「だけ」を繰り下げる")
    panel(d, 120, 320, 940, 720)
    at(d, "厚生年金", 58, 530, 370, WHITE)
    at(d, "65歳から受け取る", 50, 530, 490, SAFE)
    at(d, "加給年金42万も確保", 48, 530, 600, SAFE)
    panel(d, 1000, 320, 1820, 720)
    at(d, "基礎年金", 58, 1410, 370, WHITE)
    at(d, "70歳まで繰り下げ", 50, 1410, 490, GOLD)
    at(d, "＋42％に育てる", 48, 1410, 600, GOLD)
    center(d, "これが「両取り」", 74, 800, GOLD)


def d_k_smart_calc(d):
    title(d, "高橋さんの基礎年金で試すと")
    center(d, "月6.5万円 → 月9.2万円", 96, 380, WHITE)
    center(d, "＋月2.7万円", 130, 540, GOLD)
    center(d, "これが 一生 上乗せされる", 64, 780, SAFE)


def d_k_smart2(d):
    title(d, "かしこい待ち方②", "気が変わっても やり直せる")
    center(d, "待機中にお金が必要 → 65歳にさかのぼり一括受給", 54, 360, WHITE)
    center(d, "増額はないが まとまった資金が手に入る", 60, 560, SAFE)
    center(d, "※ さかのぼれるのは 5年前まで（時効）", 52, 780, EDGE)


def _selfcheck(d, no, q, verdict, vcol):
    title(d, f"セルフチェック 質問{no}")
    panel(d, 220, 300, 1700, 560, PANEL_LT)
    size = 70
    while d.textlength(q, font=F(size)) > 1360 and size > 42:
        size -= 4
    at(d, q, size, 960, 400, WHITE)
    for i, ln in enumerate(verdict):
        at(d, ln, 58, 960, 640 + i * 92, vcol)


def d_note02_paper(d, img):
    at(d, "今日の研究ノート", 84, 860, 110, INK_RED)
    bullets = [
        "・1か月0.7％／70歳で＋42％、一生増える",
        "・損益分岐点＝額面 約82歳／手取り 約84歳",
        "・損しやすい人：年下配偶者・高収入就労・健康不安",
        "・かしこい道：加給年金は受取り、基礎だけ繰り下げ",
        "・「増やす」より「いつ・いくら要るか」で逆算",
    ]
    y = 285
    for b in bullets:
        d.text((300, y), b, font=F(50), fill=INK)
        y += 112
    d.text((300, 935), "出典：日本年金機構（2026年7月時点）", font=F(38), fill=INK_SUB)
    paste_ira(img, "mascot_hakui.png", 1530, 410, 440)
    d2 = ImageDraw.Draw(img)
    hanko(d2, 1720, 250, 105, "済")


# ───────────────── script 04: 年金生活者支援給付金 ─────────────────

def _bt(d, txt, sub=None, color=GOLD, y=64):
    """Tieu de TO, gan dinh, tran ngang (cu gia doc tu xa)."""
    s = 108
    while d.textlength(txt, font=F(s)) > W - 140 and s > 68:
        s -= 4
    center(d, txt, s, y, color)
    if sub:
        center(d, sub, 56, y + s + 16, DIM)


def g_hook(d):
    center(d, "申請しないと消えるお金", 112, 96, GOLD)
    center(d, "年金生活者支援給付金", 60, 250, DIM)
    center(d, "受け取る「権利」があるのに、申請しないと", 66, 430, WHITE)
    center(d, "年 約6万7千円", 216, 560, OVER)
    center(d, "が、静かに消える", 78, 872, WHITE)


def g_amount(d):
    _bt(d, "満額 月 約5,620円", "老齢の給付金（令和8年度）")
    y = 348
    for lab, val, col in [("1年", "約6万7千円", SAFE), ("10年", "約67万円", EDGE), ("20年", "約134万円", GOLD)]:
        panel(d, 120, y, 1800, y + 152, PANEL)
        at(d, lab, 90, 470, y + 26, DIM)
        at(d, val, 124, 1270, y + 8, col)
        y += 176
    center(d, "はがき1枚が、20年で約134万円の価値", 62, 912, WHITE)


def g_types(d):
    _bt(d, "給付金は 3種類")
    x = 150
    for name, sub, col in [("老齢", "老齢基礎年金", SAFE), ("障害", "障害年金", EDGE), ("遺族", "遺族年金", DIM)]:
        panel(d, x, 320, x + 500, 828, PANEL, outline=col)
        at(d, name, 156, x + 250, 420, col)
        at(d, sub, 54, x + 250, 660, WHITE)
        x += 555
    center(d, "今日は「老齢」を中心に", 60, 910, DIM)


def _gates(d, active):
    _bt(d, "もらえる 3つの関門")
    labels = ["① 65歳以上で\n老齢基礎年金", "② 世帯全員が\n住民税 非課税", "③ 前年の収入が\n基準以下"]
    x = 130
    for i, txt in enumerate(labels, 1):
        on = (i == active)
        panel(d, x, 300, x + 520, 864, PANEL_LT if on else PANEL, outline=(GOLD if on else None))
        at(d, txt, 68, x + 260, 400, WHITE if on else DIM)
        if on:
            mark_o(d, x + 260, 740, 62, 18, SAFE)
        x += 555


def g_gates(d): _gates(d, 0)
def g_gate1(d): _gates(d, 1)
def g_gate2(d): _gates(d, 2)
def g_gate3(d): _gates(d, 3)


def g_income(d):
    _bt(d, "関門③ 収入の基準", "前年の年金収入＋その他所得（令和8年度）")
    y = 328
    for rng, txt, col in [("〜約81万円", "満額に近い給付金", SAFE),
                          ("約81〜91万円", "補足的（少し減額）", EDGE),
                          ("約91万円 超", "対象外", OVER)]:
        panel(d, 120, y, 1800, y + 152, PANEL, outline=col)
        at(d, rng, 88, 490, y + 26, col)
        at(d, txt, 66, 1320, y + 40, WHITE)
        y += 176
    center(d, "伊藤さん 約78万円 → 満額の対象", 64, 910, SAFE)


def g_hosoku(d):
    _bt(d, "「少し超え」でもあきらめない", "補足的な給付金")
    center(d, "常連さん 年 約90万円", 100, 366, WHITE)
    center(d, "満額の81万は超え → でも 91万まで内", 62, 520, EDGE)
    center(d, "→ 補足的給付金 の対象 ○", 104, 640, SAFE)
    center(d, "「少しだけ超え」で申請しないのが一番もったいない", 54, 872, DIM)


def g_noapply(d):
    _bt(d, "申請しないと 1円も出ない", color=OVER)
    panel(d, 120, 328, 940, 872, PANEL, outline=SAFE)
    at(d, "ふつうの年金", 76, 530, 392, SAFE)
    at(d, "一度手続きすれば\n自動でずっと", 62, 530, 560, WHITE)
    panel(d, 980, 328, 1800, 872, PANEL, outline=OVER)
    at(d, "支援給付金", 76, 1390, 392, OVER)
    at(d, "認定請求しないと\n0円のまま", 62, 1390, 560, WHITE)


def g_delay(d):
    _bt(d, "遅れるほど もらえない", "手続きした月の 翌月分から")
    y = 328
    for lab, val, col in [("半年 放置", "約3万4千円", EDGE), ("1年 放置", "約6万7千円", OVER), ("5年 気づかず", "約34万円", OVER)]:
        panel(d, 120, y, 1800, y + 152, PANEL)
        at(d, lab, 76, 470, y + 32, DIM)
        at(d, "▲ " + val, 124, 1300, y + 8, col)
        y += 176
    center(d, "あとから全部は戻らないことも", 60, 910, WHITE)


def g_sagi(d):
    _bt(d, "「給付金」をかたる詐欺に注意", color=OVER)
    center(d, "「ATMへ行って」「手数料を振り込んで」", 70, 372, WHITE)
    center(d, "→ 100％　詐欺", 176, 512, OVER)
    center(d, "お金を受け取る制度なのに", 62, 790, DIM)
    center(d, "振り込ませる時点で、おかしい", 62, 876, DIM)


def g_aikotoba(d):
    _bt(d, "合言葉", "切って・調べて・かけ直す")
    x = 130
    for name, sub in [("切る", "その場で\n対応しない"), ("調べる", "正規の番号を\n自分で確認"), ("かけ直す", "自分から\nかけ直す")]:
        panel(d, x, 316, x + 520, 836, PANEL, outline=GOLD)
        at(d, name, 108, x + 260, 400, GOLD)
        at(d, sub, 54, x + 260, 606, WHITE)
        x += 555
    center(d, "本物なら、かけ直しても問題なし", 56, 916, DIM)


def note04(d):
    center(d, "研究ノート", 96, 56, (48, 66, 104))
    y = 262
    for ln in ["① 低所得の年金受給者への上乗せ（月 約5,620円）",
               "② 関門は3つ：65歳以上・世帯 非課税・収入 81〜91万",
               "③ 最大の罠：申請しないと1円も出ない",
               "④ 「振り込んで」は詐欺。本物だけ受け取る"]:
        d.text((205, y), ln, font=F(58), fill=(52, 44, 38))
        y += 178


# ───────── script 05: 60歳で即退職 (BIG / full-screen) ─────────

def t_blank5(d):
    _bt(d, "60歳で辞めると「空白の5年間」", "年金は原則 65歳から")
    center(d, "60歳 ―― 65歳", 120, 330, GOLD)
    center(d, "給料 ゼロ ＋ 年金 ゼロ", 84, 500, WHITE)
    center(d, "貯蓄から ▲ 約1680万円", 128, 640, OVER)
    center(d, "年金が始まる前に、大きく削られる", 56, 880, DIM)


def t_kuriage(d):
    _bt(d, "60歳から早くもらうと", "繰り上げ受給の落とし穴")
    center(d, "1か月 −0.4％ ／ 60歳で −24％（一生）", 68, 330, EDGE)
    center(d, "月18万円 → 月13万7千円", 100, 470, WHITE)
    center(d, "生涯で ▲ 約1000万円", 132, 620, OVER)
    center(d, "焦って早くもらうと、一生分が目減り", 56, 870, DIM)


def t_avb(d):
    _bt(d, "即退職 vs あと2年 継続雇用", "2年後の貯蓄で比べる")
    panel(d, 120, 320, 940, 780, PANEL, outline=OVER)
    at(d, "今すぐ辞める", 66, 530, 380, OVER)
    at(d, "貯蓄", 52, 530, 520, DIM)
    at(d, "▲ 672万円", 104, 530, 610, OVER)
    panel(d, 980, 320, 1800, 780, PANEL, outline=SAFE)
    at(d, "あと2年 働く", 66, 1390, 380, SAFE)
    at(d, "貯蓄", 52, 1390, 520, DIM)
    at(d, "ほぼ ±0", 104, 1390, 610, SAFE)
    center(d, "たった2年で 差は 約700万円", 78, 840, GOLD)


def t_5year(d):
    _bt(d, "長く働くほど、差が開く", "即退職との貯蓄差")
    y = 350
    for lab, val, col in [("2年 継続", "約700万円", EDGE), ("5年 継続（65歳まで）", "約1700万円", GOLD)]:
        panel(d, 120, y, 1800, y + 170, PANEL)
        at(d, lab, 72, 540, y + 44, DIM)
        at(d, val, 128, 1330, y + 20, col)
        y += 200
    center(d, "＋ 65歳から満額の年金・将来の年金も増える", 58, 862, SAFE)


def t_kyufu(d):
    _bt(d, "高年齢雇用継続給付", "働き続けた人だけがもらえる")
    center(d, "給料が60歳時の 75％未満 に下がると", 62, 330, WHITE)
    center(d, "国が 最大10％ を補助", 116, 450, SAFE)
    center(d, "松本さん 月＋2.8万円 → 2年で 約67万円", 68, 640, GOLD)
    center(d, "※2025年4月から 15％→10％ に縮小", 50, 870, DIM)


def t_kenpo(d):
    _bt(d, "落とし穴② 退職後の健康保険", "会社の半額負担がなくなる")
    panel(d, 120, 320, 940, 720, PANEL, outline=EDGE)
    at(d, "任意継続", 66, 530, 380, EDGE)
    at(d, "月 約3.5万円", 92, 530, 500, WHITE)
    at(d, "会社員の約2倍", 46, 530, 630, DIM)
    panel(d, 980, 320, 1800, 720, PANEL, outline=OVER)
    at(d, "国民健康保険", 60, 1390, 380, OVER)
    at(d, "1年目 月 約5万円超", 78, 1390, 500, WHITE)
    at(d, "前年の所得で計算", 46, 1390, 630, DIM)
    center(d, "所得が高かった人は 1年目は任意継続が有利（申込 20日以内）", 50, 790, GOLD)


def t_bills(d):
    _bt(d, "落とし穴③ 翌年に来る 二つの請求書", color=OVER)
    panel(d, 120, 330, 940, 700, PANEL, outline=OVER)
    at(d, "住民税", 88, 530, 420, OVER)
    at(d, "前年の所得で計算", 50, 530, 560, WHITE)
    panel(d, 980, 330, 1800, 700, PANEL, outline=OVER)
    at(d, "国民健康保険料", 62, 1390, 430, OVER)
    at(d, "前年の所得で計算", 50, 1390, 560, WHITE)
    center(d, "収入はゼロなのに、請求だけ現役並み", 72, 800, GOLD)


def t_whoshould(d):
    _bt(d, "続けたほうがいい人・辞めていい人")
    panel(d, 120, 320, 940, 800, PANEL, outline=SAFE)
    at(d, "続けたほうが得", 60, 530, 370, SAFE)
    at(d, "健康で働ける", 50, 530, 500, WHITE)
    at(d, "65歳まで蓄えに不安", 50, 530, 600, WHITE)
    panel(d, 980, 320, 1800, 800, PANEL, outline=EDGE)
    at(d, "辞めていい", 60, 1390, 370, EDGE)
    at(d, "体調に不安", 50, 1390, 480, WHITE)
    at(d, "家族の介護", 50, 1390, 570, WHITE)
    at(d, "蓄えにゆとり", 50, 1390, 660, WHITE)
    center(d, "「みんなが働くから」ではなく、自分の数字で決める", 52, 890, DIM)


def t_shitsugyo(d):
    _bt(d, "辞めるなら「失業給付」を確認", "基本手当（60〜64歳も対象）")
    center(d, "自己都合・勤続が長い → 150日分", 68, 340, WHITE)
    center(d, "総額 約100万円前後 も", 120, 480, GOLD)
    center(d, "「定年だから関係ない」と申請せず損する人が多い", 56, 700, EDGE)
    center(d, "※自己都合は数か月の待機あり", 48, 850, DIM)


def _tquiz(d, n, q, ox, ans):
    _bt(d, f"○×クイズ 第{n}問")
    center(d, q, 64, 320, WHITE)
    (mark_o if ox else mark_x)(d, 960, 560, 110, 26)
    center(d, ans, 60, 720, SAFE if ox else OVER)


def t_quiz1(d): _tquiz(d, 1, "年金は60歳になれば自動でもらえる", False, "バツ ― 今の世代は原則65歳から")
def t_quiz2(d): _tquiz(d, 2, "給料が下がったら国が一部を補ってくれる", True, "マル ― 高年齢雇用継続給付（最大10％）")
def t_quiz3(d): _tquiz(d, 3, "60歳で辞めたら失業給付は一切もらえない", False, "バツ ― 60代前半も対象になりうる")


def note05(d):
    center(d, "研究ノート", 96, 56, (48, 66, 104))
    y = 262
    for ln in ["① 年金は原則65歳から ― 60歳即退職は「空白の5年」",
               "② 給料半分でも あと2年で 老後資金 約700万円の差",
               "③ 辞めると 継続給付＋厚生年金の上乗せ を手放す",
               "④ 翌年に 住民税＋国保 の請求。辞めるなら失業給付を確認"]:
        d.text((205, y), ln, font=F(56), fill=(52, 44, 38))
        y += 178


DIAGRAMS = {
    "hook": d_hook,
    "wall": d_wall,
    "people": d_people,
    "wall2": d_wall2_news,
    "impact": d_impact_news,
    "mechanism": d_mechanism,
    "rule": d_rule,
    "half": d_half,
    "cast_tanaka": d_cast_tanaka,
    "cast_sato": lambda d, img: cast_card(d, img, "sato_obaasan.png", "佐藤さん（66歳・仙台）", "スーパーでパート勤務", 23, 14, "65万円まで余裕 → 満額", INK_GREEN),
    "cast_suzuki": lambda d, img: cast_card(d, img, "suzuki_syachou.png", "鈴木さん（65歳・名古屋）", "会社役員", 45, 20, "ちょうど65万円 → 満額", INK_EDGE),
    "cast_takahashi": lambda d, img: cast_card(d, img, "takahashi_businessman.png", "高橋さん（64歳・東京）", "現役の部長職", 50, 20, "65万円を 5万円オーバー", INK_RED),
    "cast_yamada": d_cast_yamada,
    "ladder1": lambda d: ladder(d, [("佐藤さん", 37)]),
    "ladder2": lambda d: ladder(d, [("佐藤さん", 37), ("鈴木さん", 65)]),
    "ladder3": lambda d: ladder(d, [("佐藤さん", 37), ("鈴木さん", 65), ("高橋さん", 70)]),
    "suzuki_before": d_suzuki_before,
    "per_person": d_per_person,
    "myth1": d_myth1,
    "myth2": d_myth2,
    "myth4": d_myth4,
    "onepoint": d_onepoint,
    "steps": d_steps,
    "quiz1q": lambda d: quiz(d, 1, "働くと、国民年金も減らされる"),
    "quiz1a": lambda d: quiz(d, 1, "働くと、国民年金も減らされる", "減る可能性があるのは 厚生年金の部分だけ"),
    "quiz2q": lambda d: quiz(d, 2, "夫婦の収入は、合算して判定される"),
    "quiz2a": lambda d: quiz(d, 2, "夫婦の収入は、合算して判定される", "一人ずつ、別々に判定"),
    "quiz3q": lambda d: quiz(d, 3, "65万円を超えたら、超えた分が全部止められる"),
    "quiz3a": lambda d: quiz(d, 3, "65万円を超えたら、超えた分が全部止められる", "止まるのは 超えた分の半分だけ"),
    "note": d_note_paper,
    # ── script 02 ──
    "k_hook": d_k_hook,
    "k_lost40": d_k_lost40,
    "k_grow": d_k_grow,
    "k_rate": d_k_rate,
    "k_kuriage": d_k_kuriage,
    "k_twotier": d_k_twotier,
    "cast_takahashi02": d_cast_takahashi02,
    "cast_sato02": d_cast_sato02,
    "k_65vs70": d_k_65vs70,
    "k_forgone": d_k_forgone,
    "k_calc": d_k_calc,
    "k_breakeven": d_k_breakeven,
    "k_longevity": d_k_longevity,
    "k_netbreak": d_k_netbreak,
    "k_75wait": d_k_75wait,
    "k_split": d_k_split,
    "k_pitfall1": d_k_pitfall1,
    "k_pitfall2": d_k_pitfall2,
    "k_pitfall3": d_k_pitfall3,
    "k_burden": d_k_burden,
    "k_smart1": d_k_smart1,
    "k_smart_calc": d_k_smart_calc,
    "k_smart2": d_k_smart2,
    "k_self1": lambda d: _selfcheck(d, 1, "65歳未満の配偶者が いますか？",
                                    ["はい → 厚生年金の繰り下げは 加給年金を失う", "基礎年金だけの繰り下げを検討"], EDGE),
    "k_self2": lambda d: _selfcheck(d, 2, "待つ間の生活費に 余裕がありますか？",
                                    ["いいえ → 無理に待たなくていい", "65歳受給も 立派な選択"], SAFE),
    "k_self3": lambda d: _selfcheck(d, 3, "長寿家系で、健康に自信は？",
                                    ["はい → 繰り下げで増やす価値大", "分岐点82歳を こえやすい"], GOLD),
    "note02": d_note02_paper,
    # ── script 04: 支援給付金 ──
    "g_hook": g_hook, "g_amount": g_amount, "g_types": g_types,
    "g_gates": g_gates, "g_gate1": g_gate1, "g_gate2": g_gate2, "g_gate3": g_gate3,
    "g_income": g_income, "g_hosoku": g_hosoku, "g_noapply": g_noapply,
    "g_delay": g_delay, "g_sagi": g_sagi, "g_aikotoba": g_aikotoba, "note04": note04,
    # ── script 05: 即退職 ──
    "t_blank5": t_blank5, "t_kuriage": t_kuriage, "t_avb": t_avb, "t_5year": t_5year,
    "t_kyufu": t_kyufu, "t_kenpo": t_kenpo, "t_bills": t_bills, "t_whoshould": t_whoshould,
    "t_shitsugyo": t_shitsugyo, "t_quiz1": t_quiz1, "t_quiz2": t_quiz2, "t_quiz3": t_quiz3, "note05": note05,
}

BG_MAP = {
    "cast_tanaka": bg_warm, "cast_sato": bg_warm, "cast_suzuki": bg_warm,
    "cast_takahashi": bg_warm, "cast_yamada": bg_warm,
    "wall2": bg_news, "impact": bg_news,
    "note": bg_paper,
    "cast_takahashi02": bg_warm, "cast_sato02": bg_warm, "note02": bg_paper,
    "note04": bg_paper,
    "note05": bg_paper,
}


def render_one(name, path, rank=None):
    img = BG_MAP.get(name, bg)()
    d = ImageDraw.Draw(img)
    fn = DIAGRAMS[name]
    if len(inspect.signature(fn).parameters) >= 2:
        fn(d, img)
    else:
        fn(d)
    if rank:
        d = ImageDraw.Draw(img)
        tw = d.textlength(rank, font=F(56))
        d.rounded_rectangle((50, 44, 50 + tw + 70, 148), radius=20, fill=OVER)
        d.text((85, 62), rank, font=F(56), fill=WHITE)
    img.save(path)
    print(f"  ✓ {Path(path).name}  ({name})")


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: make_diagrams.py <SLIDES.json> <outdir> [tên_test]")
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 3:
        render_one(sys.argv[3], outdir / f"_test_{sys.argv[3]}.png")
        return
    n = 0
    for i, spec in enumerate(cfg):
        dg = spec.get("diagram")
        if not dg:
            continue
        if dg not in DIAGRAMS:
            print(f"  ⚠ slide {i}: diagram '{dg}' không tồn tại — bỏ qua")
            continue
        render_one(dg, outdir / f"slide_{i:02d}.png", spec.get("rank"))
        n += 1
    print(f"Xong: {n} diagram → {outdir}")


if __name__ == "__main__":
    main()
