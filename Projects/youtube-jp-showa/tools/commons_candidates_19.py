# -*- coding: utf-8 -*-
"""commons_candidates_19.py — tim UNG VIEN anh that tren Wikimedia Commons cho video 19 (kaimono-joushiki).

Khuon chep tu commons_candidates_08.py (video thang v08). Moi key = mot VAT duoc doc len trong
19_kaimono-joushiki_TTS.md -> search File -> loc license (PD/CC0/CC BY/BY-SA, cam NC/ND) -> thumb 640
-> 1 contact sheet / key de duyet MAT. So den: _cc/commons_used.txt (anh da len song o video truoc).

    python tools/commons_candidates_19.py            # chay het
    python tools/commons_candidates_19.py tv_color pawnshop   # chi vai key
"""
import io, sys, json, time, re
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "19_kaimono-joushiki" / "_cc"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
OK_LIC = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d?(\.\d)?( .*)?|attribution)", re.I)
BAD_LIC = re.compile(r"(nc|nd|non-?commercial|no derivatives)", re.I)

Q = {
 # HOOK + muc 1 — TV / thang gop
 "tv_color":        ["カラーテレビ 1960年代", "家具調テレビ", "vintage color television Japan 1970", "National television 1960s Japan"],
 "tv_family":       ["テレビ 家族 昭和", "family watching television Japan 1960s", "茶の間 テレビ"],
 "tv_antenna":      ["テレビアンテナ 屋根 昭和", "TV antennas rooftops Japan 1960s", "八木アンテナ 屋根"],
 "denkiya":         ["電器店 昭和", "electrical appliance store Japan 1960s", "電器屋 店頭"],
 "kei_truck":       ["ダイハツ ミゼット", "Daihatsu Midget", "スバル サンバー 初代", "マツダ K360"],
 "hanko":           ["印鑑 朱肉", "hanko seal stamp Japan", "認印 判子"],
 "gamaguchi":       ["がま口", "gamaguchi purse", "clasp purse Japan"],
 "bicycle_old":     ["実用自転車 昭和", "old delivery bicycle Japan", "Japanese utility bicycle vintage"],
 # muc 2 — thieu tien / cam do
 "factory_1970":    ["町工場 昭和", "small factory Japan 1960s", "machine shop Japan 1970"],
 "pawnshop":        ["質屋", "pawnshop Japan", "質 看板", "質屋 蔵"],
 "kura":            ["土蔵 白壁", "kura storehouse Japan", "蔵 なまこ壁"],
 "kimono_houmongi": ["訪問着", "houmongi kimono", "kimono silk pattern closeup"],
 "furoshiki":       ["風呂敷", "furoshiki cloth wrapping", "風呂敷包み"],
 "roji":            ["路地 昭和 長屋", "narrow alley Tokyo 1960s", "路地裏 下町"],
 "noren":           ["暖簾 紺", "noren curtain shop entrance Japan", "のれん 店"],
 # muc 3 — my pham dinh gia
 "cosme_shop":      ["化粧品店 昭和", "cosmetics shop Japan vintage", "化粧品 ショーケース"],
 "lipstick_old":    ["口紅 昭和 レトロ", "vintage lipstick", "資生堂 口紅 1960"],
 "cosme_bottles":   ["化粧品 瓶 レトロ", "vintage cosmetics bottles Japan", "おしろい 昭和"],
 "pharmacy_old":    ["薬局 昭和 看板", "old pharmacy Japan", "薬店 レトロ"],
 # muc 4 — thuong xa dong cua
 "shotengai":       ["商店街 1970年代", "shopping street Japan 1970s", "昭和 商店街 アーケード"],
 "fish_shop":       ["魚屋 店先", "fishmonger Japan shop", "鮮魚店 昭和"],
 "aji":             ["マアジ", "Japanese horse mackerel", "鯵 魚屋"],
 "yaoya":           ["八百屋 店先", "greengrocer Japan", "vegetable shop Japan old"],
 "tofu_shop":       ["豆腐屋 水槽", "tofu shop Japan", "豆腐 店先"],
 "croquette":       ["コロッケ 肉屋", "korokke croquette Japan butcher", "揚げたてコロッケ"],
 "shutter":         ["シャッター 商店街 閉店", "shuttered shops Japan", "シャッター通り"],
 "shoyu_bottle":    ["醤油瓶 一升瓶", "soy sauce bottle Japan old", "醤油 瓶 レトロ"],
 "fukubiki":        ["福引 抽選器", "garapon lottery drum", "ガラガラ 抽選"],
 "supermarket_70s": ["スーパーマーケット 1970年代 日本", "supermarket Japan 1970s", "ダイエー 昭和"],
 "seven_eleven_old":["セブン-イレブン 1970年代", "7-Eleven Japan 1970s store", "コンビニ 昭和"],
 # muc 5 — gia tron, thue, 1 yen
 "price_tag":       ["値札 昭和", "handwritten price tags Japan market", "値札 八百屋"],
 "register_old":    ["レジスター 昭和", "vintage cash register", "金銭登録機"],
 "coin_1yen":       ["一円硬貨", "1 yen coin", "1円玉"],
 "coin_100yen":     ["百円硬貨 稲穂", "100 yen coin", "百円硬貨 鳳凰"],
 "daikon":          ["大根", "daikon radish", "大根 八百屋"],
 "fridge_old":      ["電気冷蔵庫 昭和", "vintage refrigerator Japan", "冷蔵庫 1960年代"],
 "car_1970":        ["トヨタ カローラ 初代", "Nissan Sunny 1970", "昭和 自家用車 1970"],
 "tax_1989":        ["消費税 導入 1989", "consumption tax Japan 1989", "消費税 3%"],
 # KET
 "bride_1970":      ["花嫁 昭和 白無垢", "Japanese bride 1970s", "結婚式 昭和 着物"],
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

used_p = OUT / "commons_used.txt"
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
