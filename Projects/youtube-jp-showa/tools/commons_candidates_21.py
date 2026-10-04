# -*- coding: utf-8 -*-
"""commons_candidates_20.py — tim UNG VIEN anh that tren Wikimedia Commons cho video 21 (umaredoshi-okane).

Khuon chep tu commons_candidates_08.py (video thang v08). Moi key = mot VAT duoc doc len trong
21_umaredoshi-okane_TTS.md -> search File -> loc license (PD/CC0/CC BY/BY-SA, cam NC/ND) -> thumb 640
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
OUT = ROOT / "06_VIDEO" / "21_umaredoshi-okane" / "_cc"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
OK_LIC = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d?(\.\d)?( .*)?|attribution)", re.I)
BAD_LIC = re.compile(r"(nc|nd|non-?commercial|no derivatives)", re.I)

Q = {
 # HOOK — 四十九日の夜・通帳・鉛筆
 "tsucho":     ["郵便貯金 通帳", "passbook Japan post office savings", "預金通帳 昭和", "貯金通帳"],
 "pencil":     ["鉛筆 手書き", "pencil handwriting paper Japan", "ちびた鉛筆"],
 "butsudan":   ["仏壇 和室", "butsudan Japanese altar home", "仏間"],
 # 1 — 銀の百円玉
 "coin100_old":["百円硬貨 鳳凰", "100 yen coin 1957 phoenix", "百円銀貨", "稲穂 百円 銀貨", "100円硬貨"],
 "note100":    ["板垣退助 百円札", "100 yen note Itagaki", "B百円券"],
 "coin50":     ["五十円硬貨 穴", "50 yen coin 1959", "旧五十円 ニッケル"],
 "note10000":  ["聖徳太子 一万円札", "10000 yen note Shotoku Taishi", "C一万円券"],
 "school1959": ["入学式 昭和30年代", "Japanese elementary school 1950s", "小学校 昭和34年", "ランドセル 昭和"],
 "futon_lamp": ["裸電球 和室", "old light bulb Japanese room", "電灯 昭和 室内"],
 # 2 — 年賀はがき
 "nengajo":    ["年賀はがき 昭和", "nengajo New Year card Japan old", "お年玉付年賀はがき", "年賀状 昭和"],
 "imoban":     ["芋版", "potato stamp print Japan", "いもばん 年賀状"],
 "suzuri":     ["硯 墨", "inkstone sumi ink", "書道 硯"],
 "chabudai":   ["ちゃぶ台", "chabudai table", "卓袱台 昭和"],
 "postbox":    ["郵便受け 木製", "old mailbox Japanese house", "郵便ポスト 丸型", "郵便配達 自転車"],
 "kitte_sheet":["切手シート 年賀", "stamp sheet Japan New Year", "お年玉切手シート"],
 # 3 — ラジオ
 "radio_tube": ["真空管ラジオ", "vacuum tube radio Japan", "5球スーパー ラジオ", "古いラジオ 木製"],
 "tv_color":   ["カラーテレビ 昭和", "color television 1968 Japan", "白黒テレビ 昭和"],
 # 4 — 電話
 "akadenwa":   ["赤電話 たばこ屋", "red public telephone Japan", "委託公衆電話", "たばこ屋 店先"],
 "kurodenwa":  ["黒電話 600形", "black rotary telephone Japan", "黒電話", "ダイヤル電話 昭和"],
 "koukanshu":  ["電話交換手", "telephone operators Japan", "電話交換台"],
 "denchu":     ["電柱 電話線 昭和", "telephone poles wires Japan 1960s", "電電公社"],
 "tabakoya":   ["たばこ屋 昭和", "tobacco shop Japan old", "煙草屋"],
 # 5 — 国立大学
 "univ1970":   ["国立大学 1970年代", "Japanese university campus 1970s", "大学 キャンパス 昭和", "東北大学 昭和"],
 "goukaku":    ["合格発表 掲示板", "university entrance exam results board Japan", "合格発表"],
 "ryo":        ["学生寮 昭和", "student dormitory Japan old", "寮 四畳半"],
 "pinkdenwa":  ["ピンク電話", "pink telephone Japan", "特殊簡易公衆電話"],
 "yubinkyoku": ["郵便局 窓口 昭和", "post office counter Japan 1970s", "郵便局 昭和"],
 "hanko":      ["印鑑 朱肉", "hanko seal red ink", "判子"],
 "stove":      ["石油ストーブ 昭和", "kerosene heater Japan old", "石油ストーブ"],
 "note100b":   ["Series B 100 Yen Bank of Japan note", "100 yen banknote Itagaki Taisuke", "B100yen"],
 "note10000b": ["Series C 10000 Yen banknote", "10000 yen note Shotoku", "C10000yen"],
 "radio_jp":   ["National radio 1950s Japan", "Japanese tube radio Showa", "ナショナル ラジオ 真空管", "Sharp radio 1950s"],
 "exam1970":   ["university entrance examination Japan 1970", "入学試験 1960年代", "大学入試 昭和"],
 "yubin_old":  ["post office Japan 1960s interior", "郵便局 1960年代", "Japan post office 1950s"],
 "tsucho2":    ["Japanese bankbook", "通帳 郵便局", "預金通帳"],
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
