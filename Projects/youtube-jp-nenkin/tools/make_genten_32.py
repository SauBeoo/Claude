# -*- coding: utf-8 -*-
r"""make_genten_32.py - the 原典 cho video 32 (本人確認 2027 · 免許証の暗証番号2つ).

Hai loai nguon:
  - WEB (警視庁 IC免許証 · 金融庁 報道発表): Playwright + Range cua DOM, thu hep cot + tang co chu
    (co khi mượn nguyen tu make_genten_31: JS_FIND / JS_STYLE / footer / union).
  - PDF (警察庁 チラシ · 犯収法の概要 · Q&A): render 200dpi bang pymupdf. Cau co lop chu ⇒ toa do lay bang
    `page.search_for` (chinh xac). Tieu de chirashi la chu DANG HINH (khong tim duoc) ⇒ toa do pixel
    DO BANG MAT tren raw_npa_chirashi_p1.png (1654x2339), ghi o ZONE.
MOI O MOT THE RIENG (khong dung lai cung mot anh trong video — media-library §2 muc 4).
O nao dung the nao: KHOA THEO CUE VAN BAN trong plan32.json.
CHAY: python tools/make_genten_32.py  -> 06_VIDEO/<stem>/genten/genten_*.png + art_final/shot_KKK.png
"""
import json
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
import make_genten_31 as g  # noqa: E402  (JS_FIND, JS_STYLE, footer, union, fit_card, CARD_*)

VD = PROJ / "06_VIDEO" / "32_ginko-honnin-kakunin-2027"
RAW = VD / "genten_raw"
OUT = VD / "genten"
ART = VD / "art_final"
FONT = g.FONT
RED = g.RED
DPI = 200
PT = DPI / 72

WEB = {
 "keishicho": dict(
    url="https://www.keishicho.metro.tokyo.lg.jp/menkyo/menkyo/menkyo_annai/ic.html",
    credit="出典：警視庁「ICカード免許証」（更新日 2024年10月1日）",
    css=dict(maxWidth="620px", fontSize="30px", lineHeight="1.7"),
    cards=[
     ("genten_keishicho_koushin.png", "暗証番号の控えは確実に保管してください",
      "暗証番号は次回の運転免許証交付時まで変更できません。"),
     ("genten_keishicho_hitsuyou.png", "ICカード免許証は、表面に記載されている内容がICチップに記録されます",
      "ICチップの記録内容は、ICカード読み取り装置に暗証番号を入力しないと見ることができません。"),
     ("genten_keishicho_chuki.png", "暗証番号はキャッシュカード、クレジットカード等の暗証番号とは異なるものにしてください",
      "暗証番号はキャッシュカード、クレジットカード等の暗証番号とは異なるものにしてください。"),
     ("genten_keishicho_3kai.png", "暗証番号を3回続けて間違えると、それ以降は",
      "暗証番号を3回続けて間違えると、それ以降は、ICチップに記録された内容の読み取りができなくなります"),
     ("genten_keishicho_denwa.png", "個人情報の保護の観点から電話での照会には応じられません",
      "個人情報の保護の観点から電話での照会には応じられませんのでご了承ください。"),
     ("genten_keishicho_gizou.png", "最近、一見しただけでは判別できない精巧な偽変造免許証が出回り",
      "他人名義の運転免許証を用いて銀行口座を開設したり、携帯電話の利用契約を結び、振り込め詐欺等に不正に使用されています。"),
    ]),
 "fsa": dict(
    url="https://www.fsa.go.jp/news/r7/sonota/20260626/20260626.html",
    credit="出典：金融庁「犯罪収益移転防止法施行規則の一部を改正する命令の公布等について」（2026年6月26日）",
    css=dict(maxWidth="640px", fontSize="28px", lineHeight="1.7"),
    cards=[
     ("genten_fsa_kouza.png", "犯罪・犯罪収益の移転に利用又はそのおそれがあると認めた口座について",
      "犯罪・犯罪収益の移転に利用又はそのおそれがあると認めた口座について"),
     ("genten_fsa_sekou.png", "本改正に係る命令等は、本日付で公布・公表し",
      "令和９年４月１日（木曜）から施行・適用されます。"),
    ]),
}

# PDF: (file, page, credit, crop_px, [circle rects])  — circle = ("px", x0,y0,x1,y1) | ("find", needle, occ)
CHIRASHI = ("src_npa_chirashi20260623.pdf", 0,
            "出典：警察庁「口座開設等で本人確認を受ける際 ICチップ情報の読み取り等が必須となります」")
PDFCARDS = {
 "genten_chirashi_gimuka.png": (CHIRASHI, (0, 0, 720, 600), [("px", 10, 28, 272, 238)]),
 "genten_chirashi_hissu.png": (CHIRASHI, (0, 0, 1654, 540), [("px", 150, 222, 1600, 505)]),
 "genten_chirashi_taimen.png": (CHIRASHI, (40, 540, 1654, 930), [("px", 76, 590, 1020, 890)]),
 "genten_chirashi_senko.png": (CHIRASHI, (700, 360, 1620, 560), [("find", "各金融機関等の判断により", 0),
                                                            ("find", "先行実施する場合があります", 0)]),
 "genten_gaiyou_zumi.png": (("src_npa_hougaiyou20260807.pdf", 36,
                             "出典：警察庁「犯罪収益移転防止法の概要」（2026年8月7日更新）p.34"),
                            (60, 90, 1600, 620), [("find", "改めて取引時確認を行う必要", 0),
                                                  ("find", "はありません", 1)]),
 "genten_qa_keireki.png": (("src_npa_260306qa.pdf", 1,
                            "出典：警察庁「犯罪収益移転防止法施行規則の改正に係るQ&A」No.6"),
                           (882, 1570, 1545, 2010), [("find", "身体障害者手帳、運転経歴証明書", 0)]),
 "genten_digital_shougou.png": (("src_digital_taimen_app.pdf", 4,
                                 "出典：デジタル庁「マイナンバーカード対面確認アプリについて」（2024年7月）p.4"),
                                (250, 500, 2560, 1400), [("px", 1590, 780, 2400, 1080)]),
}

# o (theo cue loi doc trong plan32.json) -> the. Thu tu = thu tu trong bai.
CUE2CARD = [
    ("赤で囲んだところ、ご覧ください。2027年4月1日から義務化", "genten_chirashi_gimuka.png"),
    ("口座開設等で本人確認を受ける際", "genten_chirashi_hissu.png"),
    ("窓口では、運転免許証やマイナンバーカード等", "genten_chirashi_taimen.png"),
    ("各金融機関等の判断により", "genten_chirashi_senko.png"),
    ("こちらは、警察庁の、法律の概要", "genten_gaiyou_zumi.png"),
    ("こちらは、東京の警視庁の、免許証のページ", "genten_keishicho_koushin.png"),
    ("つまり、番号を決めたのは", "genten_keishicho_hitsuyou.png"),
    ("暗証番号は、キャッシュカード、クレジットカード等", "genten_keishicho_chuki.png"),
    ("同じページには、暗証番号を3回続けて", "genten_keishicho_3kai.png"),
    ("ただし、ここに、もう一行あります", "genten_keishicho_denwa.png"),
    ("窓口でカードの中を読む仕組みの一つに", "genten_digital_shougou.png"),
    ("警察庁の質問と回答の資料では", "genten_qa_keireki.png"),
    ("一見しただけでは判別できない", "genten_keishicho_gizou.png"),
    ("こちらは、金融庁の発表です", "genten_fsa_kouza.png"),
    ("そうした努力をする決まりも始まります", "genten_fsa_sekou.png"),
]


def pdf_cards(fcred, bad):
    cache = {}
    for fn, ((src, pg, credit), crop, circles) in PDFCARDS.items():
        key = (src, pg)
        if key not in cache:
            doc = pymupdf.open(RAW / src)
            pix = doc[pg].get_pixmap(dpi=DPI)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            cache[key] = (doc[pg], im)
        page, im = cache[key]
        rects = []
        for c in circles:
            if c[0] == "px":
                rects.append(c[1:])
            else:
                hits = page.search_for(c[1])
                if len(hits) <= c[2]:
                    print(f"🔴 {fn}: không thấy «{c[1]}»#{c[2]} trong PDF")
                    bad.append(fn)
                    continue
                r = hits[c[2]]
                rects.append((r.x0 * PT, r.y0 * PT, r.x1 * PT, r.y1 * PT))
        part = im.crop(crop)
        card, sc, ox, oy = g.fit_card(part)
        d = ImageDraw.Draw(card)
        for (x0, y0, x1, y1) in rects:
            d.rounded_rectangle([ox + (x0 - crop[0]) * sc - 12, oy + (y0 - crop[1]) * sc - 10,
                                 ox + (x1 - crop[0]) * sc + 12, oy + (y1 - crop[1]) * sc + 10],
                                radius=16, outline=RED, width=7)
        g.footer(card, credit, fcred)
        card.save(OUT / fn)
        print(f"✅ {fn}  (PDF {src} p{pg + 1} · {len(rects)} ô khoanh · chữ ×{sc:.2f})")


def trim_cut_lines(im, h_vis):
    """Dòng chữ bị mép khung CẮT NGANG (nửa trên/dưới lộ ra) ⇒ tô trắng tới hàng trống đầu tiên.
    Chỉ xét trong 140px sát mép trên và sát mép dưới của vùng HIỂN THỊ (trên dải 出典)."""
    import numpy as np
    a = np.asarray(im.convert("L")).copy()
    h = min(h_vis, a.shape[0])
    ink = (a[:h] < 200).sum(1) > 2
    out = np.asarray(im).copy()
    if ink[:24].any():
        y0 = int(np.argmax(ink[:24]))
        y = next((i for i in range(y0, min(140, h)) if not ink[i]), 0)
        out[:y] = 255
    if ink[h - 24:h].any():
        y1 = h - 1 - int(np.argmax(ink[h - 24:h][::-1]))
        y = next((i for i in range(y1, max(0, h - 140), -1) if not ink[i]), h)
        out[y:h] = 255
    return Image.fromarray(out)


def web_cards(fcred, bad):
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=g.CHS, args=["--lang=ja-JP"])
        ctx = br.new_context(viewport={"width": 1500, "height": 1200}, device_scale_factor=g.DSF,
                             locale="ja-JP", user_agent=g.UA)
        for key, pg_ in WEB.items():
            for fn, block, needle in pg_["cards"]:
                pg = ctx.new_page()
                pg.goto(pg_["url"], wait_until="networkidle", timeout=90000)
                pg.wait_for_timeout(1200)
                if not pg.evaluate(g.JS_STYLE, [block, 0, "block", pg_["css"]]):
                    print(f"🔴 {fn}: không thấy khối «{block}»")
                    bad.append(fn)
                    pg.close()
                    continue
                pg.wait_for_timeout(400)
                blk = pg.evaluate(g.JS_FIND, [block, 0, "block"])
                box = pg.evaluate(g.JS_FIND, [needle, 0, "range"])
                if not blk or not box:
                    print(f"🔴 {fn}: không thấy câu khoanh «{needle[:30]}»")
                    bad.append(fn)
                    pg.close()
                    continue
                area = g.union(blk + box)
                shot = RAW / f"pw32_{fn[:-4]}.png"
                pg.screenshot(path=str(shot), full_page=True)
                src = Image.open(shot).convert("RGB")
                x0, y0, x1, y1 = area[0] - 36, area[1] - 36, area[2] + 36, area[3] + 36
                need_h = y1 - y0
                need_w = max(x1 - x0, need_h * g.CARD_W / (g.CARD_H - 60))
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                hh = need_w * (g.CARD_H - 60) / g.CARD_W
                cx0, cy0 = cx - need_w / 2, cy - hh / 2
                crop = src.crop(tuple(int(v * g.DSF) for v in (cx0, cy0, cx0 + need_w, cy0 + hh)))
                sc = g.CARD_W / crop.width
                crop = crop.resize((g.CARD_W, int(crop.height * sc)), Image.LANCZOS)
                crop = trim_cut_lines(crop, g.CARD_H - 60)
                card = Image.new("RGB", (g.CARD_W, g.CARD_H), (255, 255, 255))
                card.paste(crop, (0, 0))
                d = ImageDraw.Draw(card)
                for b in box:
                    d.rounded_rectangle([(b[0] - cx0) * g.DSF * sc - 14, (b[1] - cy0) * g.DSF * sc - 10,
                                         (b[2] - cx0) * g.DSF * sc + 14, (b[3] - cy0) * g.DSF * sc + 10],
                                        radius=18, outline=RED, width=7)
                g.footer(card, pg_["credit"], fcred)
                card.save(OUT / fn)
                print(f"✅ {fn}  vùng CSS {need_w:.0f}×{hh:.0f}  chữ ×{sc * g.DSF:.2f}")
                pg.close()
        br.close()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    fcred = ImageFont.truetype(FONT, 22)
    bad = []
    pdf_cards(fcred, bad)
    web_cards(fcred, bad)
    shots = json.loads((VD / "plan32.json").read_text(encoding="utf-8"))["shots"]
    taken = {}
    for cue, fn in CUE2CARD:
        ks = [k for k, s in enumerate(shots) if s["text"].startswith(cue) or
              (s["lines"] and cue in s["text"][:len(cue) + 40])]
        if not ks:
            print(f"🔴 cue 原典 không khớp ô nào: «{cue}»")
            bad.append(fn)
            continue
        k = ks[0]
        if k in taken:
            print(f"🔴 ô {k} đã có {taken[k]} — {fn} bị trùng (cue «{cue}»)")
            bad.append(fn)
            continue
        taken[k] = fn
        if (OUT / fn).exists():
            Image.open(OUT / fn).save(ART / f"shot_{k:03d}.png")
    print(f"→ {len(taken)} ô 原典: " + " · ".join(f"{k}={v[7:-4]}" for k, v in sorted(taken.items())))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
