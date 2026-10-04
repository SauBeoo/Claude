# -*- coding: utf-8 -*-
"""commons_candidates_20.py — tim UNG VIEN anh that tren Wikimedia Commons cho video 20 (kaimono-joushiki).

Khuon chep tu commons_candidates_08.py (video thang v08). Moi key = mot VAT duoc doc len trong
20_sumai-okane_TTS.md -> search File -> loc license (PD/CC0/CC BY/BY-SA, cam NC/ND) -> thumb 640
-> 1 contact sheet / key de duyet MAT. So den: _cc/commons_used.txt (anh da len song o video truoc).

    python tools/commons_candidates_20.py            # chay het
    python tools/commons_candidates_20.py tv_color pawnshop   # chi vai key
"""
import io, sys, json, time, re
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "20_sumai-okane" / "_cc"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
OK_LIC = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d?(\.\d)?( .*)?|attribution)", re.I)
BAD_LIC = re.compile(r"(nc|nd|non-?commercial|no derivatives)", re.I)

Q = {
 # HOOK
 "chadansu":   ["茶箪笥", "chadansu cabinet Japan", "茶だんす 昭和"],
 "hagaki_old": ["官製はがき 昭和", "Japanese postcard 1960s stamp", "郵便はがき 昭和40年代"],
 # muc 1 — 六畳一間
 "apart_wood": ["木造アパート 昭和", "wooden apartment Japan old", "木賃アパート", "文化住宅 アパート"],
 "fudousan":   ["不動産屋 貼り紙", "real estate agent window Japan old", "不動産 物件 貼り紙"],
 "tatami6":    ["六畳 和室 畳", "tatami room six mats", "四畳半 アパート"],
 "monohoshi":  ["物干し台 昭和", "laundry balcony Japan old", "物干し 路地"],
 "clock_old":  ["目覚まし時計 レトロ", "vintage alarm clock Japan", "目覚まし時計 昭和"],
 "insatsu":    ["活版印刷 印刷所", "letterpress printing shop Japan", "活字 組版"],
 # muc 2 — 銭湯
 "sento":      ["銭湯 番台", "sento bathhouse Japan", "銭湯 富士山 ペンキ絵", "銭湯 脱衣所"],
 "sento_out":  ["銭湯 煙突", "sento chimney Tokyo", "銭湯 のれん 外観"],
 "okeya":      ["ケロリン 桶", "Kerorin bucket", "洗面器 銭湯"],
 "geta":       ["下駄", "geta sandals", "下駄箱 銭湯"],
 # muc 3 — 団地
 "danchi_old": ["団地 1960年代", "danchi 1960s Japan", "公団住宅 昭和", "日本住宅公団 団地"],
 "dk":         ["ダイニングキッチン 団地", "danchi kitchen 1960s", "2DK 団地 再現"],
 "balance":    ["バランス釜", "balance-gama bath heater", "風呂釜 ガス"],
 "key_old":    ["鍵 レトロ", "old key Japan", "シリンダー錠 鍵"],
 # muc 4 — 公庫 / tabako
 "tsuchou":    ["預金通帳 昭和", "Japanese bank passbook old", "通帳"],
 "hilite":     ["ハイライト たばこ", "Hi-lite cigarettes Japan", "昭和 たばこ パッケージ"],
 "futon":      ["布団 和室", "futon tatami room", "布団 敷く"],
 # muc 5 — 郊外 / 通勤
 "bunjouchi":  ["分譲地 昭和", "new housing development Japan 1970s", "宅地造成 1970年代"],
 "tateuri":    ["建売住宅 昭和", "Japanese suburban house 1970s", "昭和 住宅 二階建て"],
 "bus_old":    ["路線バス 昭和", "Japanese bus 1970s", "いすゞ バス 1970"],
 "mancha":     ["満員電車 昭和", "rush hour train Tokyo 1970s", "通勤ラッシュ 昭和"],
 "hyousatsu":  ["表札", "nameplate house Japan", "表札 木"],
 "kanbeer":    ["缶ビール 昭和", "vintage beer can Japan", "ビール缶 1970年代"],
 "saifu":      ["財布 革 古い", "old leather wallet", "財布"],
}

def api(params):
    for k in range(4):
        try:
            r = requests.get(API, params=dict(params, format="json"), headers=H, timeout=60)
            if r.status_code == 200: return r.json()
            print("   http", r.status_code); time.sleep(3 + 3 * k)
        except Exception as e:
            print("   err", e); time.sleep(3)
    return {}

def search(q, n=14):
    j = api({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": n})
    return [x["title"] for x in j.get("query", {}).get("search", [])]

def info(titles):
    out = {}
    for i in range(0, len(titles), 20):
        j = api({"action": "query", "titles": "|".join(titles[i:i+20]), "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 640})
        for p in j.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [None])[0]
            if not ii or not ii.get("mime", "").startswith("image/"): continue
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "") or em.get("License", {}).get("value", "")
            out[p["title"]] = dict(url=ii["url"], thumb=ii.get("thumburl"), w=ii["width"], h=ii["height"],
                                   license=lic, artist=re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value", ""))[:80],
                                   date=em.get("DateTimeOriginal", {}).get("value", "")[:40],
                                   desc=re.sub(r"<[^>]+>", "", em.get("ImageDescription", {}).get("value", ""))[:160])
    return out

def lic_ok(l):
    return bool(OK_LIC.search(l)) and not BAD_LIC.search(l)

used_p = OUT.parent / "_blacklist" / "commons_used.txt"
USED = set(x.strip().replace("_", " ") for x in used_p.read_text(encoding="utf-8").splitlines() if x.strip()) if used_p.exists() else set()

info_p = OUT / "candidates_info.json"
all_info = json.loads(info_p.read_text(encoding="utf-8")) if info_p.exists() else {}
keys = sys.argv[1:] or list(Q)
for key in keys:
    qs = Q[key]
    titles = []
    for q in qs:
        for t in search(q):
            if t not in titles: titles.append(t)
        time.sleep(0.4)
    meta = info(titles)
    cands = [(t, m) for t, m in meta.items() if lic_ok(m["license"]) and m["w"] >= 800 and t not in USED][:12]
    if not cands:
        print(f"{key:18} 0 (tim {len(titles)}, license loai {sum(1 for m in meta.values() if not lic_ok(m['license']))})"); continue
    ims = []
    for i, (t, m) in enumerate(cands):
        dst = OUT / f"{key}__{i:02d}.jpg"
        if not dst.exists() and m["thumb"]:
            try:
                r = requests.get(m["thumb"], headers=H, timeout=60)
                if r.status_code == 200 and len(r.content) > 2000: dst.write_bytes(r.content)
                else: print("   dl", r.status_code, t); time.sleep(2)
            except Exception as e:
                print("   dl err", t, e); continue
        if dst.exists():
            ims.append((i, t, m, dst)); all_info[f"{key}__{i:02d}"] = dict(title=t, **m)
        time.sleep(0.3)
    if not ims: continue
    W, Hh = 320, 200; cols = 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, (Hh + 30) * rows), "black"); d = ImageDraw.Draw(sh)
    for i, t, m, dst in ims:
        try: im = Image.open(dst).convert("RGB")
        except Exception: continue
        im.thumbnail((W, Hh)); x, y = (i % cols) * W, (i // cols) * (Hh + 30)
        sh.paste(im, (x, y))
        d.rectangle((x, y + Hh, x + W, y + Hh + 30), fill="black")
        d.text((x + 3, y + Hh + 2), f"{i:02d} {m['license'][:14]} {m['w']}x{m['h']} {m['date'][:10]}", fill="yellow")
        d.text((x + 3, y + Hh + 15), t.replace("File:", "")[:52].encode("ascii", "replace").decode(), fill="white")
    sh.save(OUT / f"sheet_{key}.jpg", quality=85)
    print(f"{key:18} {len(ims)} ung vien (tim {len(titles)})")
    info_p.write_text(json.dumps(all_info, ensure_ascii=False, indent=1), encoding="utf-8")
    time.sleep(0.5)

print("OK ->", OUT)
