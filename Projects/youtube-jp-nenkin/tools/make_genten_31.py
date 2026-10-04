# -*- coding: utf-8 -*-
r"""make_genten_31.py - the 原典 cho video 31 (chup trang THAT + khoanh do trong MOT buoc).

Khuon y nguyen make_genten_30.py (Playwright + Range cua DOM, thu hep cot + tang co chu, bake dong 出典).
Them 2 kieu the ma v30 khong co:
  - mode "td"   : khoanh O BANG (bang 非課税限度額 cua 大阪市)
  - kind "img"  : the tu MOT ANH tren trang (so do 148万〜214万 cua 年金機構), khoanh vung mau cam
  - kind "pdf"  : the tu trang PDF da render (bang 介護保険料 cua 大阪市) - toa do hang DO BANG MAT
                  tren raw_osaka_kaigo_table_p0.png (1654x2339, 200dpi)
O nao dung the nao: KHOA THEO CUE VAN BAN trong plan31.json (khong theo chi so o).
CHAY: python tools/make_genten_31.py   -> 06_VIDEO/<stem>/genten/genten_*.png + art_final/shot_KKK.png
"""
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
VD = PROJ / "06_VIDEO" / "31_fuyo-shinkokusho-hikazei-domino"
OUT = VD / "genten"
ART = VD / "art_final"
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Medium.otf"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0 Safari/537.36")
DSF = 2
CARD_W, CARD_H = 1100, 990
RED = (214, 45, 32)

PAGES = {
 "r9": dict(
    url="https://www.nenkin.go.jp/oshirase/taisetu/kojin/2026/202606/0617.html",
    credit="出典：日本年金機構「令和8年度税制改正による公的年金等に係る主な改正事項」",
    blocks=[("年金受給者が個人住民税の各種控除を受けようとする場合も", 0, "block")],
    css=dict(maxWidth="600px", fontSize="30px", lineHeight="1.7"),
    cards=[("genten_r9_juminzei_nenkin.png",
            [("年金受給者が個人住民税の各種控除を受けようとする場合も日本年金機構へ扶養親族等申告書を提出することとされました。", 0, "range")])],
    img=("0617.images/2.png", "genten_r9_zu_nenkin.png")),
 "r9t": dict(
    url="https://www.nenkin.go.jp/oshirase/taisetu/kojin/2026/202606/0617.html",
    credit="出典：日本年金機構（更新日 2026年6月17日）",
    blocks=[("令和8年度税制改正による公的年金等に係る主な改正事項", 0, "block"),
            ("令和8年度税制改正により、所得税の基礎控除の引上げ", 0, "block")],
    css=dict(maxWidth="620px", fontSize="30px", lineHeight="1.6"),
    cards=[("genten_r9_title_nenkin.png", [("令和8年度税制改正による公的年金等に係る主な改正事項", 0, "block")])]),
 "hikazei_title": dict(
    url="https://www.city.osaka.lg.jp/zaisei/page/0000384084.html",
    credit="出典：大阪市（2025年12月26日）",
    blocks=[("市民税・府民税・森林環境税が課税されない方", 0, "block"),
            ("生活保護法の規定による生活扶助を受けている方", 0, "block")],
    css=dict(maxWidth="620px", fontSize="30px", lineHeight="1.6"),
    cards=[("genten_hikazei_title_osaka.png", [("市民税・府民税・森林環境税が課税されない方", 0, "block")])]),
 "faq": dict(
    url="https://www.nenkin.go.jp/section/faq/jukyu/jukyushatodoke/rourei/fuyoushinkoku/teishutsu/20141022-08.html",
    credit="出典：日本年金機構「扶養親族等申告書を提出しなかった場合はどうなるのですか。」",
    blocks=[("申告書を提出しない場合は", 0, "block")],
    css=dict(maxWidth="600px", fontSize="30px", lineHeight="1.7"),
    cards=[("genten_mitei_nenkin.png",
            [("翌年の個人住民税において、障害者控除や配偶者控除等を受けることができません。", 0, "range")])]),
 "hikazei": dict(
    url="https://www.city.osaka.lg.jp/zaisei/page/0000384084.html",
    credit="出典：大阪市「市民税・府民税・森林環境税が課税されない方」",
    blocks=[("が135万円以下（給与所得者の場合、年収2,043,999円以下）である方", 0, "block")],
    css=dict(maxWidth="620px", fontSize="30px", lineHeight="1.7"),
    cards=[("genten_kafu_osaka.png", [("が135万円以下（給与所得者の場合、年収2,043,999円以下）である方", 0, "block")])]),
 "rourei": dict(
    url="https://www.nenkin.go.jp/service/jukyu/seido/sonota-kyufu/shienkyufukin/rourei.html",
    credit="出典：日本年金機構「老齢（補足的老齢）年金生活者支援給付金の概要」",
    blocks=[("請求する方の世帯全員の市町村民税が非課税となっている", 0, "list")],
    css=dict(maxWidth="620px", fontSize="28px", lineHeight="1.7"),
    cards=[("genten_shien_setai_nenkin.png", [("請求する方の世帯全員の市町村民税が非課税となっている", 0, "range")])]),
 "tetsu3": dict(
    url="https://www.nenkin.go.jp/section/faq/jukyu/seido/sonota-kyufu/shienkyufukin/tetsuduki/tetsuduki03.html",
    credit="出典：日本年金機構「年金生活者支援給付金を受け取るためには、毎年、手続きが必要ですか。」",
    blocks=[("継続支給の判定結果は", 0, "block")],
    css=dict(maxWidth="600px", fontSize="30px", lineHeight="1.7"),
    cards=[("genten_shien_10gatsu_nenkin.png", [("毎年10月分（12月支払）から1年間反映", 0, "range")])]),
}

# PDF 大阪市 介護保険料 — toa do (pixel cua anh 200dpi) DO BANG MAT tren sheet crop 1:1
PDF = dict(src="raw_osaka_kaigo_table_p0.png", out="genten_kaigo_osaka.png",
           credit="出典：大阪市「介護保険料について」第9期（令和6〜8年度）",
           crop=(140, 620, 1480, 1220), rows=[(756, 820), (902, 962), (964, 1024), (1096, 1156)], row_names=["第2段階", "第4段階", "第5段階", "第7段階"])

# the cat thang tu anh chup goc (bang cua 大阪市 bi co meo khi doi CSS -> dung ban chup nguyen trang)
RAW = [dict(src="raw_osaka_hikazei.png", out="genten_hikazei_osaka.png",
            credit="出典：大阪市「市民税・府民税・森林環境税が課税されない方」（令和8年度課税分以降）",
            crop=(500, 3880, 1880, 4830), boxes=[(866, 4206, 1066, 4508), (1066, 4206, 1266, 4508)])]

# o (theo cue loi doc trong plan31.json) -> the. Thu tu = thu tu trong bai.
CUE2CARD = [
    ("こちらが、日本年金機構のページです", "genten_r9_title_nenkin.png"),
    ("年金受給者が個人住民税の各種控除", "genten_r9_juminzei_nenkin.png"),
    ("年金が214万円から上は", "genten_r9_zu_nenkin.png"),
    ("こちらが、大阪市の、住民税が課税されない", "genten_hikazei_title_osaka.png"),
    ("前の年の所得が、同一生計配偶者", "genten_hikazei_osaka.png"),
    ("同じページには、寡婦", "genten_kafu_osaka.png"),
    ("年金機構のよくある質問には", "genten_mitei_nenkin.png"),
    ("こちらが、大阪市の、介護保険料の表", "genten_kaigo_osaka.png"),
    ("年金生活者支援給付金の条件の一つは", "genten_shien_setai_nenkin.png"),
    ("判定の結果は、毎年10月分から", "genten_shien_10gatsu_nenkin.png"),
]

JS_FIND = """([nd, occ, mode]) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, seen = 0;
  while (n = w.nextNode()) { let i = n.textContent.indexOf(nd);
    while (i >= 0) { if (seen++ === occ) {
        const p = n.parentElement;
        if (mode === 'range') { const r = document.createRange(); r.setStart(n, i);
          r.setEnd(n, i + nd.length);
          const L = [];
          for (const b of r.getClientRects()) { if (b.width < 2) continue;
            const q = L.find(o => Math.abs(o[1] - (b.top + scrollY)) < 4);
            if (q) { q[0] = Math.min(q[0], b.left + scrollX); q[2] = Math.max(q[2], b.right + scrollX);
                     q[3] = Math.max(q[3], b.bottom + scrollY); }
            else L.push([b.left + scrollX, b.top + scrollY, b.right + scrollX, b.bottom + scrollY]); }
          return L; }
        let el = p;
        if (mode === 'tr') el = p.closest('table');
        else if (mode === 'td') el = p.closest('td,th');
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


def footer(card, credit, f):
    d = ImageDraw.Draw(card)
    d.rectangle([0, CARD_H - 60, CARD_W, CARD_H], fill=(243, 240, 232))
    d.line([0, CARD_H - 60, CARD_W, CARD_H - 60], fill=(200, 196, 186), width=2)
    d.text((24, CARD_H - 50), credit, font=f, fill=(60, 64, 72))


def fit_card(img):
    """dat anh vao the CARD_W x (CARD_H-60), giu ti le, can giua, nen trang."""
    card = Image.new("RGB", (CARD_W, CARD_H), (255, 255, 255))
    box_w, box_h = CARD_W - 40, CARD_H - 60 - 40
    sc = min(box_w / img.width, box_h / img.height)
    im = img.resize((int(img.width * sc), int(img.height * sc)), Image.LANCZOS)
    ox, oy = (CARD_W - im.width) // 2, 20 + (box_h - im.height) // 2
    card.paste(im, (ox, oy))
    return card, sc, ox, oy


def orange_box(img):
    """vung mau cam (住民税のみ課税) o NUA PHAI so do — so do ben phai la 令和9年分."""
    px = img.convert("RGB").load()
    W, H = img.size
    xs, ys = [], []
    for y in range(H):
        for x in range(W // 2, W):
            r, g, b = px[x, y]
            if r > 220 and 110 < g < 180 and b < 90:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    # hai khoi cam chong nhau (所得税の課税対象 tren · 住民税のみ課税 duoi) -> lay khoi DUOI:
    # tim khe ngang (hang khong co pixel cam) lon nhat, lay phan duoi khe
    rows = sorted(set(ys))
    gaps = [(rows[i + 1] - rows[i], rows[i + 1]) for i in range(len(rows) - 1)]
    cut = max(gaps)[1] if gaps and max(gaps)[0] > 2 else min(ys)
    pts = [(x, y) for x, y in zip(xs, ys) if y >= cut]
    return [min(p[0] for p in pts), cut, max(p[0] for p in pts), max(p[1] for p in pts)]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    fcred = ImageFont.truetype(FONT, 24)
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHS, args=["--lang=ja-JP"])
        ctx = br.new_context(viewport={"width": 1500, "height": 1200}, device_scale_factor=DSF,
                             locale="ja-JP", user_agent=UA)
        for key, pg_ in PAGES.items():
            pg = ctx.new_page()
            pg.goto(pg_["url"], wait_until="networkidle", timeout=90000)
            pg.wait_for_timeout(1200)
            # the tu ANH (chup truoc khi doi style)
            if "img" in pg_:
                sel, fn = pg_["img"]
                png = pg.locator(f'img[src*="{sel}"]').first.screenshot()
                src = Image.open(io.BytesIO(png)).convert("RGB")
                ob = orange_box(src)
                card, sc, ox, oy = fit_card(src)
                if ob is None:
                    print(f"🔴 {fn}: không thấy vùng cam 住民税のみ課税")
                    bad += 1
                else:
                    d = ImageDraw.Draw(card)
                    d.rounded_rectangle([ox + ob[0] * sc - 16, oy + ob[1] * sc - 14,
                                         ox + ob[2] * sc + 16, oy + ob[3] * sc + 14],
                                        radius=18, outline=RED, width=7)
                footer(card, pg_["credit"], fcred)
                card.save(OUT / fn)
                print(f"✅ {fn}  (ảnh sơ đồ {src.width}×{src.height}, vùng cam {ob})")
            for nd, occ, mode in pg_["blocks"]:
                css = pg_.get("table") if mode == "tr" else pg_["css"]
                if not pg.evaluate(JS_STYLE, [nd, occ, mode, css]):
                    print(f"🔴 {key}: không thấy khối «{nd}»#{occ}")
                    bad += 1
            pg.wait_for_timeout(400)
            blk = [pg.evaluate(JS_FIND, [nd, occ, m if m in ("tr", "list") else "block"])
                   for nd, occ, m in pg_["blocks"]]
            if None in blk:
                print(f"🔴 {key}: khối mất sau khi đổi style")
                bad += 1
                pg.close()
                continue
            area = union([r for b in blk for r in b])
            shot = VD / "genten_raw" / f"pw31_{key}.png"
            pg.screenshot(path=str(shot), full_page=True)
            src = Image.open(shot).convert("RGB")
            for fn, needles in pg_["cards"]:
                boxes = [pg.evaluate(JS_FIND, list(n)) for n in needles]
                if None in boxes:
                    print(f"🔴 {fn}: không thấy câu khoanh {needles}")
                    bad += 1
                    continue
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
                footer(card, pg_["credit"], fcred)
                card.save(OUT / fn)
                print(f"✅ {fn}  vùng CSS {need_w:.0f}×{hh:.0f}  chữ ×{sc * DSF:.2f}")
            pg.close()
        br.close()

    # the cat tu anh chup goc
    for r in RAW:
        src = Image.open(VD / "genten_raw" / r["src"]).convert("RGB").crop(r["crop"])
        card, sc, ox, oy = fit_card(src)
        d = ImageDraw.Draw(card)
        for (x0, y0, x1, y1) in r["boxes"]:
            d.rounded_rectangle([ox + (x0 - r["crop"][0]) * sc, oy + (y0 - r["crop"][1]) * sc,
                                 ox + (x1 - r["crop"][0]) * sc, oy + (y1 - r["crop"][1]) * sc],
                                radius=12, outline=RED, width=7)
        footer(card, r["credit"], fcred)
        card.save(OUT / r["out"])
        print(f"✅ {r['out']}  (cắt từ ảnh chụp gốc, {len(r['boxes'])} ô khoanh)")

    # the PDF
    src = Image.open(VD / "genten_raw" / PDF["src"]).convert("RGB").crop(PDF["crop"])
    card, sc, ox, oy = fit_card(src)
    d = ImageDraw.Draw(card)
    for (ry0, ry1) in PDF["rows"]:
        y0 = oy + (ry0 - PDF["crop"][1]) * sc
        y1 = oy + (ry1 - PDF["crop"][1]) * sc
        d.rounded_rectangle([ox - 8, y0 - 4, ox + src.width * sc + 8, y1 + 4], radius=14, outline=RED, width=6)
    footer(card, PDF["credit"], fcred)
    card.save(OUT / PDF["out"])
    if not PDF["rows"]:
        print(f"⚠️ {PDF['out']}: CHƯA có toạ độ hàng — chạy xong soi ảnh rồi điền PDF['rows']")
        bad += 1
    else:
        print(f"✅ {PDF['out']}  ({len(PDF['rows'])} hàng khoanh)")

    # gan the vao o theo CUE
    plan = VD / "plan31.json"
    if plan.exists():
        shots = json.loads(plan.read_text(encoding="utf-8"))["shots"]
        taken = {}
        for cue, fn in CUE2CARD:
            ks = [k for k, s in enumerate(shots) if cue in s["text"]]
            if not ks:
                print(f"🔴 cue 原典 không khớp ô nào: «{cue}»")
                bad += 1
                continue
            k = ks[0]
            if k in taken:
                print(f"⚠️ ô {k} đã có {taken[k]} — {fn} bị gộp (cue «{cue}»), cân nhắc chẻ ô")
                continue
            taken[k] = fn
            if (OUT / fn).exists():
                Image.open(OUT / fn).save(ART / f"shot_{k:03d}.png")
        print(f"→ {len(taken)} ô 原典: " + " · ".join(f"{k}={v}" for k, v in sorted(taken.items())))
    else:
        print("⚠️ chưa có plan31.json — chưa gán thẻ vào ô")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
