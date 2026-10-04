# -*- coding: utf-8 -*-
"""GO/NO-GO test: tim anh PD/CC tren Wikimedia Commons cho 14 mon kyushoku.
Moi mon: search Commons (token JP don - bai hoc memory), tai 2 ung vien tot nhat,
xuat contact sheet de duyet mat. Khong nhap kho _media_library o buoc test.

Chay:  python tools/test_fetch_kyushoku.py
Out :  06_VIDEO/_asset_test/<slug>_N.jpg + _contact_sheet.jpg + report.txt
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "06_VIDEO", "_asset_test")
os.makedirs(OUT, exist_ok=True)

UA = "ShowaKurashiZukan-AssetTest/0.1 (personal research; contact via github)"

# (slug, [queries thu theo thu tu], mo ta mon)
ITEMS = [
    ("agepan",        ["揚げパン", "揚げパン 給食"], "banh mi chien duong"),
    ("kujira",        ["鯨肉 竜田揚げ", "鯨 竜田揚げ", "鯨肉"], "ca voi tatsuta-age"),
    ("dasshifunnyu",  ["脱脂粉乳", "スキムミルク"], "sua bot gay"),
    ("milmake",       ["ミルメーク"], "bot pha sua Milmake"),
    ("reitomikan",    ["冷凍みかん", "冷凍ミカン"], "quyt dong lanh"),
    ("softmen",       ["ソフト麺", "ソフトスパゲッティ式めん"], "mi mem"),
    ("almite",        ["アルマイト 食器", "アルマイト", "給食 食器"], "khay/bat nhom almite"),
    ("koppepan",      ["コッペパン"], "banh mi koppe"),
    ("tetrapack",     ["テトラパック 牛乳", "三角 牛乳", "テトラ・クラシック"], "sua tui tam giac"),
    ("fruitponchi",   ["フルーツポンチ", "フルーツみつ豆"], "fruit punch"),
    ("sakiware",      ["先割れスプーン"], "thia xe dau"),
    ("kyushoku_ban",  ["給食当番", "給食 配膳"], "truc nhat chia com"),
    ("curry_shichu",  ["カレーシチュー", "給食 カレー"], "curry stew kieu kyushoku"),
    ("bin_gyunyu",    ["瓶牛乳", "牛乳瓶"], "sua chai thuy tinh"),
]

API = "https://commons.wikimedia.org/w/api.php"
OK_LICENSE = re.compile(
    r"(cc0|cc[ -]?by(?![ -]?nc)|public domain|pd-|attribution)", re.I)
BAD_TITLE = re.compile(r"(map|logo|diagram|\.svg|\.pdf|\.ogg|\.webm)", re.I)


def api_get(params):
    params = dict(params, format="json")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def search_item(queries):
    """Tra ve list ung vien (title, thumb_url, full_url, license, w, h)."""
    for q in queries:
        try:
            data = api_get({
                "action": "query", "generator": "search",
                "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 8,
                "prop": "imageinfo",
                "iiprop": "url|extmetadata|size|mime",
                "iiurlwidth": 1600,
            })
        except Exception as e:
            print(f"    [WARN] API loi voi query '{q}': {e}")
            continue
        pages = (data.get("query") or {}).get("pages") or {}
        cands = []
        for p in pages.values():
            title = p.get("title", "")
            if BAD_TITLE.search(title):
                continue
            ii = (p.get("imageinfo") or [{}])[0]
            if not ii or "jpeg" not in ii.get("mime", "") and "png" not in ii.get("mime", ""):
                continue
            if ii.get("width", 0) < 640:
                continue
            meta = ii.get("extmetadata") or {}
            lic = (meta.get("LicenseShortName") or {}).get("value", "")
            if not OK_LICENSE.search(lic or ""):
                continue
            cands.append({
                "title": title,
                "url": ii.get("thumburl") or ii.get("url"),
                "page": ii.get("descriptionurl", ""),
                "license": lic,
                "w": ii.get("width"), "h": ii.get("height"),
                "query": q,
            })
        if cands:
            return cands
    return []


def download(url, dest, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
                f.write(r.read())
            return
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 15 * (attempt + 1)
                print(f"    [429] doi {wait}s roi thu lai...")
                time.sleep(wait)
                continue
            raise


def main():
    report = []
    hits = 0
    for slug, queries, note in ITEMS:
        print(f"[{slug}] {note} ...")
        existing = os.path.join(OUT, f"{slug}_0.jpg")
        if os.path.exists(existing) and os.path.getsize(existing) > 10000:
            print("    da co tu lan truoc, skip")
            report.append((slug, note, [(existing, {"title": "(cached)", "license": "(xem report cu)",
                                                    "w": "?", "h": "?", "query": queries[0], "page": ""})]))
            hits += 1
            continue
        time.sleep(3)
        cands = search_item(queries)
        if not cands:
            print("    KHONG co ung vien license sach")
            report.append((slug, note, None))
            continue
        saved = []
        for i, c in enumerate(cands[:2]):
            if saved:
                break  # 1 anh dat la du cho go/no-go
            dest = os.path.join(OUT, f"{slug}_{i}.jpg")
            try:
                download(c["url"], dest)
                saved.append((dest, c))
                print(f"    OK  {c['title']}  [{c['license']}]")
            except Exception as e:
                print(f"    [WARN] tai loi: {e}")
            time.sleep(3)
        report.append((slug, note, saved or None))
        if saved:
            hits += 1

    # report.txt — APPEND, khong ghi de (bug 2026-08-07: mode "w" xoa nguon/license
    # cac batch truoc, mat dau ATTRIBUTIONS, phai rebuild bang perceptual hash)
    import datetime
    with open(os.path.join(OUT, "report.txt"), "a", encoding="utf-8") as f:
        f.write(f"\n===== batch {datetime.date.today()} =====\n")
        f.write(f"GO/NO-GO kyushoku asset test — {hits}/{len(ITEMS)} mon co anh\n\n")
        for slug, note, saved in report:
            f.write(f"## {slug} ({note})\n")
            if not saved:
                f.write("   MISS\n\n")
                continue
            for dest, c in saved:
                f.write(f"   {os.path.basename(dest)} | {c['title']} | "
                        f"{c['license']} | {c['w']}x{c['h']} | q={c['query']}\n"
                        f"   {c['page']}\n")
            f.write("\n")

    # contact sheet
    try:
        from PIL import Image, ImageDraw, ImageFont
        cell_w, cell_h, label_h = 420, 320, 46
        cols = 4
        rows = (len(ITEMS) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "white")
        d = ImageDraw.Draw(sheet)
        font = None
        for fp in [r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\msgothic.ttc",
                   r"C:\Windows\Fonts\YuGothM.ttc"]:
            if os.path.exists(fp):
                font = ImageFont.truetype(fp, 20)
                break
        for idx, (slug, queries, note) in enumerate(ITEMS):
            x = (idx % cols) * cell_w
            y = (idx // cols) * (cell_h + label_h)
            img_path = os.path.join(OUT, f"{slug}_0.jpg")
            status = "MISS"
            if os.path.exists(img_path):
                try:
                    im = Image.open(img_path).convert("RGB")
                    im.thumbnail((cell_w - 8, cell_h - 8))
                    sheet.paste(im, (x + (cell_w - im.width) // 2,
                                     y + (cell_h - im.height) // 2))
                    status = "OK"
                except Exception:
                    status = "ERR"
            else:
                d.rectangle([x + 4, y + 4, x + cell_w - 4, y + cell_h - 4],
                            outline="red", width=3)
            d.text((x + 10, y + cell_h + 8),
                   f"{queries[0]} ({status})", fill="black" if status == "OK" else "red",
                   font=font)
        sheet_path = os.path.join(OUT, "_contact_sheet.jpg")
        sheet.save(sheet_path, quality=88)
        print(f"\nContact sheet: {sheet_path}")
    except Exception as e:
        print(f"[WARN] khong dung duoc contact sheet: {e}")

    print(f"\n=== KET QUA: {hits}/{len(ITEMS)} mon co anh license sach "
          f"({hits * 100 // len(ITEMS)}%) — chuan GO >= 70% ===")


if __name__ == "__main__":
    main()
