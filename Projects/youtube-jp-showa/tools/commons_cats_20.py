# -*- coding: utf-8 -*-
"""commons_cats_20.py — ung vien Commons theo CATEGORY (search chu cua Commons tach tieng Nhat qua te:
'がま口' ra anh nguoi A Rap, '判子' ra thi tran Hanko o Phan Lan). Moi key = 1..n category (+ category con 1 tang).
Loc license (PD/CC0/CC BY/BY-SA) + >=800px + so den. Sheet 40 o/key.
"""
import io, sys, json, time, re
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / "20_sumai-okane"
OUT = VD / "_cat"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
OK_LIC = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d?(\.\d)?( .*)?|attribution)", re.I)
BAD_LIC = re.compile(r"(nc|nd|non-?commercial|no derivatives)", re.I)
USED = set(x.strip().replace("_", " ") for x in (VD / "_blacklist" / "commons_used.txt").read_text(encoding="utf-8").splitlines() if x.strip())

CATS = {
 "c_danchi":     ["Danchi", "Hibarigaoka Danchi", "Housing estates in Japan", "Matsubara Danchi"],
 "c_matsudo":    ["Matsudo Museum"],
 "c_showamuse":  ["The Showa Era Lifestyle Museum", "Interior of the Showa Era Lifestyle Museum", "Collections of The Showa Era Lifestyle Museum"],
 "c_sento":      ["Sento", "Kitanoyu Bathhouse", "Aichi Sento Museum"],
 "c_edotokyo":   ["Edo-Tokyo Open Air Architectural Museum", "Kodakara-yu"],
 "c_nagaya":     ["Nagaya (apartment)", "Nagaya"],
 "c_tansu":      ["Tansu"],
 "c_pc1950":     ["1950s postcards of Japan"],
 "c_getabako":   ["Getabako", "Geta"],
 "c_shitamachi": ["Shitamachi Museum", "Interior of the Shitamachi Museum"],
 "c_bungo":      ["Bungotakada Showa no Machi"],
 "c_urmuseum":   ["UR Museum of Urban and Lifestyle Design"],
 "c_tokiwa":     ["Tokiwadaira Danchi", "Tokiwadaira Danchi (Matsudo Museum)"],
 "c_akabane":    ["Akabanedai Danchi"],
 "c_kodakara":   ["Kodakarayu (1929)", "Inari-yu (1930)"],
 "c_pubhousing": ["Public housing in Japan"],
 "c_tokyo60":    ["Tokyo in the 1960s"],
 "c_tokyo70":    ["Tokyo in the 1970s"],
 "c_garasudo":   ["Garasudo (Japanese glass doors)"],
 "c_kitchen":    ["Kitchens in Japan"],
}
MAXF = 40

def api(p):
    for k in range(5):
        try:
            r = requests.get(API, params=dict(p, format="json"), headers=H, timeout=60)
            if r.status_code == 200 and r.text.startswith("{"): return r.json()
            print("   http", r.status_code); time.sleep(6 + 6 * k)
        except Exception as e:
            print("   err", e); time.sleep(6)
    return {}

def members(cat, typ):
    out, cont = [], {}
    while True:
        j = api(dict({"action": "query", "list": "categorymembers", "cmtitle": "Category:" + cat, "cmtype": typ, "cmlimit": 200}, **cont))
        out += [m["title"] for m in j.get("query", {}).get("categorymembers", [])]
        if "continue" not in j or len(out) >= 400: break
        cont = j["continue"]; time.sleep(0.5)
    return out

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
            out[p["title"]] = dict(url=ii["url"], thumb=ii.get("thumburl"), w=ii["width"], h=ii["height"], license=lic,
                                   artist=re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value", ""))[:80],
                                   date=em.get("DateTimeOriginal", {}).get("value", "")[:20])
        time.sleep(0.5)
    return out

info_p = OUT / "cat_info.json"
allinfo = json.loads(info_p.read_text(encoding="utf-8")) if info_p.exists() else {}
for key in (sys.argv[1:] or list(CATS)):
    files = []
    for c in CATS[key]:
        files += members(c, "file")
        for sub in members(c, "subcat")[:12]:
            files += members(sub.replace("Category:", ""), "file"); time.sleep(0.3)
    files = [f for f in dict.fromkeys(files) if f.replace("_", " ") not in USED]
    meta = info(files[:160])
    cands = [(t, m) for t, m in meta.items() if OK_LIC.search(m["license"]) and not BAD_LIC.search(m["license"]) and m["w"] >= 800][:MAXF]
    ims = []
    for i, (t, m) in enumerate(cands):
        dst = OUT / f"{key}__{i:02d}.jpg"
        if not dst.exists() and m["thumb"]:
            try:
                r = requests.get(m["thumb"], headers=H, timeout=60)
                if r.status_code == 200 and len(r.content) > 2000: dst.write_bytes(r.content)
                else: print("   dl", r.status_code); time.sleep(8)
            except Exception as e: print("   dl err", e)
            time.sleep(0.5)
        if dst.exists():
            ims.append((i, t, m, dst)); allinfo[f"{key}__{i:02d}"] = dict(title=t, **m)
    print(f"{key:14} {len(ims)} / {len(files)} file")
    if not ims: continue
    W, Hh, cols = 320, 200, 5; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, (Hh + 30) * rows), "black"); d = ImageDraw.Draw(sh)
    for i, t, m, dst in ims:
        try: im = Image.open(dst).convert("RGB")
        except Exception: continue
        im.thumbnail((W, Hh)); x, y = (i % cols) * W, (i // cols) * (Hh + 30); sh.paste(im, (x, y))
        d.text((x + 3, y + Hh + 2), f"{i:02d} {m['license'][:14]} {m['w']}x{m['h']} {m['date'][:10]}", fill="yellow")
        d.text((x + 3, y + Hh + 15), t.replace("File:", "")[:50].encode("ascii", "replace").decode(), fill="white")
    sh.save(OUT / f"sheet_{key}.jpg", quality=85)
    info_p.write_text(json.dumps(allinfo, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK", OUT)
