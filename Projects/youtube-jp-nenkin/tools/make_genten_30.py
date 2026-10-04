# -*- coding: utf-8 -*-
r"""make_genten_30.py — 7 the 原典 cho video 30 (chup + khoanh do trong MOT buoc).

KHAC make_genten_26: khong do toa do bang tay tren anh chup san. Playwright mo trang THAT, tim
cau bang **Range cua DOM** (toa do chinh xac, khong doan), roi chup dung vung do.

VI SAO PHAI THU HEP COT + TANG CO CHU (media-library.md §2.10 ②):
build28 dat anh vao o phai 864x778. Trang chup nguyen khung rong ~1.900px => chu 32px con **14px**
tren video — khan gia 45+ khong doc duoc. => JS dat `max-width` + `font-size` cho DUNG khoi chua cau
(chu, so, thu tu giu nguyen; chi doi cach xuong dong). Bang thi thu hep bang, cot giu nguyen.

YMYL: ban cat mat logo co quan => baked dong 出典 vao tung the.
CHAY: python tools/make_genten_30.py   -> 06_VIDEO/<stem>/genten/genten_*.png + art_final/shot_KKK.png
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
VD = PROJ / "06_VIDEO" / "30_nenkin-furikomi-10gatsu-fueru-hito"
OUT = VD / "genten"
ART = VD / "art_final"
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Medium.otf"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0 Safari/537.36")
DSF = 2
CARD_W, CARD_H = 1100, 990          # ~ ti le o anh 864x778 cua build28
RED = (214, 45, 32)

# needle: (chuoi, lan xuat hien thu may) — lan 0 = dau tien trong body
PAGES = {
 "nenkin": dict(
    url="https://www.nenkin.go.jp/service/jukyu/tuutisyo/gakukaitei/0601-02.html",
    credit="出典：日本年金機構「年金振込通知書」",
    blocks=[("予定額として6月の額", 0, "block")],
    css=dict(maxWidth="560px", fontSize="30px", lineHeight="1.7"),
    cards=[("genten_yotei_nenkin.png", [("8月以降の額は、予定額として6月の額を記載しています。", 0, "range")]),
           ("genten_kettei_nenkin.png", [("決定額は、市区町村から送付される通知書でご確認ください。", 0, "range")])]),
 "setagaya": dict(
    url="https://www.city.setagaya.lg.jp/02061/2286.html",
    credit="出典：世田谷区「介護保険料の納め方」",
    blocks=[("仮徴収期間（4月・6月・8月）", 1, "block"), ("前年度の2月と同じ金額", 0, "block")],
    css=dict(maxWidth="600px", fontSize="28px", lineHeight="1.7"),
    cards=[("genten_kari_setagaya.png", [("原則として前年度の2月と同じ金額が差し引かれます。", 0, "range")]),
           ("genten_kari_setagaya_b.png", [("仮徴収期間（4月・6月・8月）", 1, "range"),
                                           ("原則として前年度の2月と同じ金額が差し引かれます。", 0, "range")])]),
 "dankai": dict(
    url="https://www.city.niigata.lg.jp/iryo/kaigo/kaigoindex/hokenryou.html",
    credit="出典：新潟市「介護保険料について」（令和6〜8年度）",
    blocks=[("第3段階", 0, "tr"), ("第4段階", 0, "tr"), ("第5段階", 0, "tr")],
    table=dict(width="760px", fontSize="24px"),
    cards=[("genten_dankai_niigata.png", [("第3段階", 0, "tr"), ("第5段階", 0, "tr")])]),
 "minashi": dict(
    url="https://www.city.niigata.lg.jp/iryo/kaigo/kaigoindex/R8kaigohokenryo.html",
    credit="出典：新潟市「令和8年度介護保険料の算定方法」",
    blocks=[("みなし課税と記載される方", 1, "block"), ("介護保険料の算定では課税とみなされ", 0, "list")],
    css=dict(maxWidth="620px", fontSize="28px", lineHeight="1.7"),
    cards=[("genten_minashi_niigata.png", [("みなし課税と記載される方", 1, "range")]),
           ("genten_minashi_niigata_b.png", [("介護保険料の算定では課税とみなされ", 0, "range")])]),
}
# o trong plan30 -> the (thu tu cau dan 原典 trong _TTS.md; img30_TENFILE.txt ghi 7 o 原典)
SHOT = {11: "genten_yotei_nenkin.png", 12: "genten_kettei_nenkin.png",
        18: "genten_kari_setagaya_b.png", 19: "genten_kari_setagaya.png",
        34: "genten_dankai_niigata.png",
        65: "genten_minashi_niigata.png", 66: "genten_minashi_niigata_b.png"}

JS_FIND = """([nd, occ, mode]) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, seen = 0;
  while (n = w.nextNode()) { let i = n.textContent.indexOf(nd);
    while (i >= 0) { if (seen++ === occ) {
        const p = n.parentElement;
        if (mode === 'range') { const r = document.createRange(); r.setStart(n, i);
          r.setEnd(n, i + nd.length);
          // MOT hop cho MOI DONG chu: bounding rect cua cau xuong dong trum ca cau ben canh
          const L = [];
          for (const b of r.getClientRects()) { if (b.width < 2) continue;
            const q = L.find(o => Math.abs(o[1] - (b.top + scrollY)) < 4);
            if (q) { q[0] = Math.min(q[0], b.left + scrollX); q[2] = Math.max(q[2], b.right + scrollX);
                     q[3] = Math.max(q[3], b.bottom + scrollY); }
            else L.push([b.left + scrollX, b.top + scrollY, b.right + scrollX, b.bottom + scrollY]); }
          return L; }
        let el = p;
        if (mode === 'tr') el = p.closest('tr');
        else if (mode === 'list') el = p.closest('ul,ol') || p.closest('p,li,div');
        else el = p.closest('p,li,h1,h2,h3,h4,h5,dt,dd,div');
        const b = el.getBoundingClientRect();
        return [[b.left + scrollX, b.top + scrollY, b.right + scrollX, b.bottom + scrollY]]; }
      i = n.textContent.indexOf(nd, i + 1); } }
  return null; }"""
JS_STYLE = """([nd, occ, mode, css]) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, seen = 0;
  while (n = w.nextNode()) { let i = n.textContent.indexOf(nd);
    while (i >= 0) { if (seen++ === occ) { const p = n.parentElement;
        let el = mode === 'list' ? (p.closest('ul,ol') || p) : p.closest('p,li,h1,h2,h3,h4,h5,dt,dd,div');
        if (mode === 'tr') { const t = p.closest('table'); t.style.width = css.width;
          t.style.maxWidth = css.width; t.style.tableLayout = 'auto';
          t.querySelectorAll('th,td,th *,td *').forEach(c => { c.style.fontSize = css.fontSize; c.style.lineHeight = '1.5'; });
          return true; }
        Object.assign(el.style, css);
        el.querySelectorAll('*').forEach(c => { c.style.fontSize = css.fontSize; c.style.lineHeight = css.lineHeight; });
        return true; }
      i = n.textContent.indexOf(nd, i + 1); } }
  return false; }"""


def union(bs):
    return [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    fcred = ImageFont.truetype(FONT, 26)
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHS, args=["--lang=ja-JP"])
        ctx = br.new_context(viewport={"width": 1500, "height": 1200}, device_scale_factor=DSF,
                             locale="ja-JP", user_agent=UA)
        for key, pg_ in PAGES.items():
            pg = ctx.new_page()
            pg.goto(pg_["url"], wait_until="networkidle", timeout=90000)
            pg.wait_for_timeout(1200)
            for nd, occ, mode in pg_["blocks"]:
                css = pg_.get("table") if mode == "tr" else pg_["css"]
                if not pg.evaluate(JS_STYLE, [nd, occ, mode, css]):
                    print(f"🔴 {key}: không thấy khối «{nd}»#{occ}")
                    bad += 1
            pg.wait_for_timeout(400)
            blk = [pg.evaluate(JS_FIND, [nd, occ, "tr" if m == "tr" else "block"])
                   for nd, occ, m in pg_["blocks"]]
            if None in blk:
                print(f"🔴 {key}: khối mất sau khi đổi style")
                bad += 1
                continue
            area = union([r for b in blk for r in b])
            shot = VD / "genten_raw" / f"pw30_{key}.png"
            pg.screenshot(path=str(shot), full_page=True)
            src = Image.open(shot).convert("RGB")
            for fn, needles in pg_["cards"]:
                boxes = [pg.evaluate(JS_FIND, list(n)) for n in needles]
                if None in boxes:
                    print(f"🔴 {fn}: không thấy câu khoanh {needles}")
                    bad += 1
                    continue
                # vung cat = khoi noi dung + le 36px CSS, dan ra dung ti le the
                x0, y0, x1, y1 = area[0] - 36, area[1] - 36, area[2] + 36, area[3] + 36
                need_h = (y1 - y0)
                need_w = max(x1 - x0, need_h * CARD_W / (CARD_H - 60))
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                hh = need_w * (CARD_H - 60) / CARD_W
                cx0, cy0 = cx - need_w / 2, cy - hh / 2
                crop = src.crop(tuple(int(v * DSF) for v in (cx0, cy0, cx0 + need_w, cy0 + hh)))
                sc = CARD_W / crop.width
                crop = crop.resize((CARD_W, int(crop.height * sc)), Image.LANCZOS)
                card = Image.new("RGB", (CARD_W, CARD_H), (255, 255, 255))
                card.paste(crop, (0, 0))
                d = ImageDraw.Draw(card)
                for b in [r for bb in boxes for r in bb]:
                    bx = [(b[0] - cx0) * DSF * sc - 14, (b[1] - cy0) * DSF * sc - 10,
                          (b[2] - cx0) * DSF * sc + 14, (b[3] - cy0) * DSF * sc + 10]
                    d.rounded_rectangle(bx, radius=18, outline=RED, width=7)
                d.rectangle([0, CARD_H - 60, CARD_W, CARD_H], fill=(243, 240, 232))
                d.line([0, CARD_H - 60, CARD_W, CARD_H - 60], fill=(200, 196, 186), width=2)
                d.text((24, CARD_H - 50), pg_["credit"], font=fcred, fill=(60, 64, 72))
                card.save(OUT / fn)
                print(f"✅ {fn}  vùng CSS {need_w:.0f}×{hh:.0f}  chữ ×{sc * DSF:.2f}")
            pg.close()
        br.close()
    for k, fn in SHOT.items():
        if (OUT / fn).exists():
            Image.open(OUT / fn).save(ART / f"shot_{k:03d}.png")
    print(f"→ {OUT}  ·  {len(SHOT)} ô 原典 ghi vào art_final/")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
