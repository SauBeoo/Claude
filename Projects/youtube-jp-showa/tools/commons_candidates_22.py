# -*- coding: utf-8 -*-
"""commons_candidates_22.py — tim UNG VIEN anh that tren Wikimedia Commons cho video 22 (kieta-shigoto).

Khuon chep tu commons_candidates_08.py (video thang v08). Moi key = mot VAT duoc doc len trong
22_kieta-shigoto_TTS.md -> search File -> loc license (PD/CC0/CC BY/BY-SA, cam NC/ND) -> thumb 640
-> 1 contact sheet / key de duyet MAT. So den: _cc/commons_used.txt (anh da len song o video truoc).

    python tools/commons_candidates_22.py            # chay het
    python tools/commons_candidates_22.py tv_color pawnshop   # chi vai key
"""
import io, sys, json, time, re
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "22_kieta-shigoto" / "_cc"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
OK_LIC = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d?(\.\d)?( .*)?|attribution)", re.I)
BAD_LIC = re.compile(r"(nc|nd|non-?commercial|no derivatives)", re.I)

Q = {
 # HOOK + 1 バスの車掌
 "bus_bonnet":  ["ボンネットバス", "bonnet bus Japan", "昭和 路線バス", "Japanese bus 1950s", "Japanese bus 1960s"],
 "bus_girl":    ["バスガール", "女性車掌 バス", "bus conductress Japan", "車掌 バス 昭和"],
 "bus_ticket":  ["バス 乗車券 昭和", "改札鋏", "ticket punch Japan", "硬券 切符"],
 "gamaguchi":   ["がま口", "gamaguchi purse", "車掌かばん"],
 "coin10":      ["十円硬貨 ギザ", "10 yen coin 1951", "五円硬貨", "5 yen coin Japan"],
 "bus_stop":    ["バス停 昭和", "old bus stop Japan", "バス停留所 標識"],
 "busdepot":    ["バス 営業所", "bus depot Japan", "バス車庫 昭和"],
 "oneman":      ["ワンマンバス", "one-man bus Japan", "降車ボタン", "整理券 バス"],
 "graduation":  ["中学校 卒業式 昭和", "Japanese junior high school 1960s", "集団就職"],
 # 2 踏切警手
 "fumikiri":    ["踏切 昭和", "踏切警手", "railroad crossing Japan 1960s", "level crossing Japan old", "手動 遮断機"],
 "fumikiri_hut":["踏切 小屋", "踏切保安係", "crossing keeper hut", "信号所 小屋"],
 "steam_train": ["蒸気機関車 D51", "C57 蒸気機関車", "steam locomotive Japan 1960s", "SL 煙 鉄道"],
 "stove_coal":  ["だるまストーブ", "石炭ストーブ", "pot-belly stove Japan"],
 "flag_signal": ["手旗 鉄道", "signal flag railway Japan", "合図 旗 駅員"],
 "bento_alu":   ["アルミ 弁当箱", "aluminium lunch box Japan", "弁当箱 昭和"],
 # 3 炭鉱
 "tanko":       ["炭鉱 昭和", "coal mine Japan", "三池炭鉱", "夕張炭鉱", "筑豊 炭鉱", "Miike coal mine"],
 "tanju":       ["炭住", "炭鉱住宅", "coal miners housing Japan", "炭鉱 長屋"],
 "cap_lamp":    ["キャップランプ", "miner cap lamp", "炭鉱 ヘルメット ランプ", "安全灯 炭鉱"],
 "tategou":     ["立坑 櫓", "炭鉱 立坑", "headframe Japan coal", "宮原坑", "万田坑"],
 "botayama":    ["ボタ山", "slag heap Japan coal", "筑豊 ボタ山"],
 "sentan":      ["選炭", "coal sorting Japan", "石炭 選炭場"],
 "yakou":       ["夜行列車 昭和", "上野駅 昭和", "night train Japan 1960s", "急行 寝台 昭和"],
 "boston_bag":  ["ボストンバッグ", "Boston bag vintage", "旅行かばん 昭和"],
 "kouji":       ["工事現場 昭和", "construction workers Japan 1960s", "東京 工事 昭和40年"],
 # 4 電話交換手
 "koukandai":   ["電話交換台", "電話交換手", "telephone switchboard operators Japan", "manual telephone exchange", "交換機 手動"],
 "headset":     ["電話交換手 ヘッドセット", "operator headset vintage", "telephone operator headset"],
 "koushuu":     ["公衆電話 昭和", "public telephone Japan 1960s", "電話ボックス 昭和", "青電話"],
 "denwakyoku":  ["電報電話局", "電話局 昭和", "telephone office Japan old"],
 "dial":        ["ダイヤル 電話機", "rotary dial", "600形電話機"],
 # 5 タイピスト
 "wabuntype":   ["和文タイプライター", "Japanese typewriter", "邦文タイプライター", "kanji typewriter"],
 "katsuji":     ["活字 鉛", "movable type Japan", "活字 棚", "metal type Japanese characters"],
 "office_old":  ["事務所 昭和", "Japanese office 1970s", "オフィス 昭和40年代", "事務員 昭和"],
 "wordpro":     ["ワードプロセッサ 東芝", "JW-10", "Japanese word processor 1980s", "ワープロ 昭和"],
 "keypunch":    ["キーパンチ", "keypunch operator", "パンチカード"],
 # KET
 "kyuryo":      ["給料袋", "給与袋", "pay envelope Japan", "月給袋"],
 "hanayome":    ["花嫁 昭和", "Japanese bride 1970s", "白無垢 昭和", "結婚式 昭和"],
 "hyosho":      ["表彰状", "certificate of commendation Japan", "感謝状"],
 "crossing_now":["踏切 警報機", "railroad crossing signal Japan", "踏切 遮断機"],
 "bus_now":     ["路線バス 車内", "bus interior Japan", "降車ボタン"],
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
