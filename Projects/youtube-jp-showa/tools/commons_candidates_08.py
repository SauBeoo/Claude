# -*- coding: utf-8 -*-
"""commons_candidates_08.py — tim UNG VIEN anh that tren Wikimedia Commons cho video 08 (okane-joushiki).

Moi key: vai query (JP + EN) -> search namespace File -> imageinfo+extmetadata -> LOC license
(PD / CC0 / CC BY / CC BY-SA, cam NC/ND) -> tai thumb 640px -> 1 contact sheet / key de duyet MAT.
Sau khi duyet, chon ten file -> commons_fetch_08.py tai ban goc + ghi ATTRIBUTIONS.

Loc SO DEN tai dung: ten file da dung o video 06/07 (real_photos/cc_*) — doc tu commons_used_08.txt.
"""
import io, sys, json, time, re
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "08_okane-joushiki" / "_cc_candidates"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "showa-kurashi-zukan/1.0 (research; contact via youtube channel)"}
OK_LIC = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d?(\.\d)?( .*)?|attribution)", re.I)
BAD_LIC = re.compile(r"(nc|nd|non-?commercial|no derivatives)", re.I)

Q = {
 "red_phone":        ["赤電話 公衆電話", "red public telephone Japan", "公衆電話 昭和"],
 "phone_booth":      ["電話ボックス 日本 旧型", "telephone booth Japan vintage", "公衆電話ボックス"],
 "coin_10yen":       ["十円硬貨", "10 yen coin"],
 "coin_100yen_old":  ["百円硬貨 鳳凰", "100 yen coin 1960"],
 "note_10000_back":  ["Series C 10000 yen back", "一万円札 聖徳太子 裏"],
 "note_5000_back":   ["Series C 5000 yen back", "五千円札 聖徳太子"],
 "note_1000_ito":    ["千円札 伊藤博文", "Series C 1000 yen"],
 "note_500_iwakura": ["五百円札 岩倉具視", "500 yen note Iwakura"],
 "banknotes_bundle": ["札束", "bundle of banknotes Japan"],
 "passbook":         ["郵便貯金通帳", "貯金通帳", "bank passbook Japan"],
 "post_office_old":  ["旧郵便局 建物", "old post office building Japan", "郵便局 昭和"],
 "yubin_mark":       ["郵便局 看板 〒", "post office sign Japan"],
 "pawnshop":         ["質屋", "pawnshop Japan sign", "質 看板"],
 "ticket_hard":      ["硬券 切符", "国鉄 切符 硬券", "old train ticket Japan"],
 "ticket_punch":     ["改札鋏", "ticket punch railway Japan", "改札 鋏"],
 "jnr_train_101":    ["101系電車 山手線", "国鉄101系", "103系 山手線 1970"],
 "jnr_station_1970": ["国鉄 駅 1970年代", "JNR station 1970s", "東京駅 1970"],
 "toden_tram":       ["都電 1960年代", "Tokyo tram 1960s", "都電 荒川線 旧型"],
 "taxi_crown":       ["タクシー トヨペットクラウン", "Toyota Crown taxi 1960s Japan", "昭和 タクシー"],
 "tv_color_vintage": ["カラーテレビ 1960年代", "vintage color television Japan 1970", "家具調テレビ"],
 "tv_bw_vintage":    ["白黒テレビ 昭和", "vintage television Japan 1960"],
 "electric_fan":     ["扇風機 昭和", "vintage electric fan Japan"],
 "chadansu":         ["茶箪笥", "chadansu tea cabinet"],
 "chabudai_alt":     ["ちゃぶ台", "chabudai low table"],
 "hanko_inkpad":     ["印鑑 朱肉", "hanko inkpad", "認印"],
 "abacus":           ["そろばん", "soroban abacus Japan"],
 "kakeibo":          ["家計簿", "household account book Japan"],
 "genkan_showa":     ["玄関 昭和 民家", "genkan Japanese house entrance old"],
 "geta":             ["下駄", "geta sandals"],
 "getabako":         ["下駄箱", "shoe cabinet Japan genkan"],
 "shotengai_1970":   ["商店街 1970年代", "shopping street Japan 1970s", "昭和 商店街"],
 "bank_branch_old":  ["住友銀行 支店 昭和", "bank branch building Japan 1960s", "銀行 建物 昭和"],
 "cd_atm_old":       ["現金自動支払機", "cash dispenser Japan 1970", "ATM 日本 初期"],
 "postal_savings_poster": ["郵便貯金 ポスター", "定額貯金", "postal savings Japan poster"],
 "dial_phone_black": ["黒電話 600型", "black rotary telephone Japan"],
 "showa_kitchen_alt":["昭和 台所 民家", "Showa kitchen Japan house museum"],
 "tofu_shop":        ["豆腐屋 店先", "tofu shop Japan old"],
 "rice_shop":        ["米屋 昭和", "rice shop Japan old"],
 "salaryman_1960s":  ["サラリーマン 1960年代 東京", "Tokyo commuters 1960s"],
 "expo70_crowd":     ["大阪万博 1970 群衆", "Expo 70 Osaka crowd"],
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

used_p = OUT / "commons_used_08.txt"
USED = set(x.strip() for x in used_p.read_text(encoding="utf-8").splitlines() if x.strip()) if used_p.exists() else set()

all_info = {}
for key, qs in Q.items():
    titles = []
    for q in qs:
        for t in search(q):
            if t not in titles: titles.append(t)
        time.sleep(0.4)
    meta = info(titles)
    cands = [(t, m) for t, m in meta.items() if lic_ok(m["license"]) and m["w"] >= 800 and t not in USED][:12]
    if not cands:
        print(f"{key:22} 0 (tim {len(titles)}, license loai {sum(1 for m in meta.values() if not lic_ok(m['license']))})"); continue
    ims = []
    for i, (t, m) in enumerate(cands):
        dst = OUT / f"{key}__{i:02d}.jpg"
        if not dst.exists() and m["thumb"]:
            try:
                dst.write_bytes(requests.get(m["thumb"], headers=H, timeout=60).content)
            except Exception as e:
                print("   dl err", t, e); continue
        if dst.exists():
            ims.append((i, t, m, dst)); all_info[f"{key}__{i:02d}"] = dict(title=t, **m)
    if not ims: continue
    W, Hh = 320, 200; cols = 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, (Hh + 30) * rows), "black"); d = ImageDraw.Draw(sh)
    for i, t, m, dst in ims:
        try: im = Image.open(dst).convert("RGB")
        except Exception: continue
        im.thumbnail((W, Hh)); x, y = (i % cols) * W, (i // cols) * (Hh + 30)
        sh.paste(im, (x, y))
        d.rectangle((x, y + Hh, x + W, y + Hh + 30), fill="black")
        d.text((x + 3, y + Hh + 2), f"{i:02d} {m['license'][:14]} {m['w']}x{m['h']}", fill="yellow")
        d.text((x + 3, y + Hh + 15), t.replace("File:", "")[:52], fill="white")
    sh.save(OUT / f"sheet_{key}.jpg", quality=85)
    print(f"{key:22} {len(ims)} ung vien (tim {len(titles)})")
    time.sleep(0.5)

(OUT / "candidates_info.json").write_text(json.dumps(all_info, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK ->", OUT)
