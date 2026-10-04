# -*- coding: utf-8 -*-
"""pexels_candidates_19.py — ung vien Pexels cho cac VAT KHONG LO THOI DAI cua video 21
(can canh do an, vai, dong xu...). Loc so den: INDEX.json cua _media_library (id da used_in bat ky video nao).
Xuat _px/<key>__NN.jpg + sheet_<key>.jpg + px_info.json. Duyet MAT sheet, roi moi tai ban goc.
"""
import io, sys, json, time
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "21_umaredoshi-okane" / "_px"; OUT.mkdir(parents=True, exist_ok=True)
KEY = (ROOT.parent / "youtube-jp-health" / "tools" / ".pexels_key").read_text(encoding="utf-8").strip()
IDX = json.loads((ROOT.parent / "_media_library" / "INDEX.json").read_text(encoding="utf-8"))
USED = {str(v.get("source_id")) for v in IDX.values() if v.get("source") == "pexels" and v.get("used_in")}
USED |= set((ROOT / "06_VIDEO" / "21_umaredoshi-okane" / "_blacklist" / "pexels_used.txt").read_text(encoding="utf-8").split())

Q = {
 "px_passbook":  "old bank passbook handwriting",
 "px_pencil":    "pencil writing notebook close up",
 "px_oldhands":  "elderly woman hands old photo",
 "px_ledger":    "handwritten ledger numbers pencil",
 "px_coin":      "old silver coin in palm",
 "px_bulb":      "bare light bulb dark room",
 "px_postcard":  "vintage postcards desk",
 "px_imo":       "sweet potato cut half knife",
 "px_ink":       "inkstone calligraphy brush",
 "px_mailbox":   "old wooden mailbox",
 "px_radio":     "vintage tube radio glow",
 "px_rotary":    "black rotary phone",
 "px_receiver":  "old telephone receiver hand",
 "px_sakura":    "cherry blossom campus spring",
 "px_board":     "notice board papers numbers",
 "px_heater":    "kerosene heater flame",
 "px_hanko":     "red ink stamp seal paper",
 "px_tatami":    "tatami room night lamp",
 "px_wrapped":   "coin wrapped in paper",
}

H = {"Authorization": KEY}
info = {}
for key, q in Q.items():
    try:
        r = requests.get("https://api.pexels.com/v1/search", headers=H, params={"query": q, "per_page": 20, "orientation": "landscape"}, timeout=60)
        ph = r.json().get("photos", [])
    except Exception as e:
        print(key, "err", e); continue
    ph = [p for p in ph if str(p["id"]) not in USED][:12]
    ims = []
    for i, p in enumerate(ph):
        dst = OUT / f"{key}__{i:02d}.jpg"
        if not dst.exists():
            try: dst.write_bytes(requests.get(p["src"]["medium"], timeout=60).content)
            except Exception: continue
        info[f"{key}__{i:02d}"] = dict(id=p["id"], url=p["url"], photographer=p["photographer"], w=p["width"], h=p["height"], alt=p.get("alt", ""), original=p["src"]["original"])
        ims.append((i, p, dst))
    if not ims: print(key, 0); continue
    W, Hh, cols = 320, 200, 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, (Hh + 18) * rows), "black"); d = ImageDraw.Draw(sh)
    for i, p, dst in ims:
        im = Image.open(dst).convert("RGB"); im.thumbnail((W, Hh))
        x, y = (i % cols) * W, (i // cols) * (Hh + 18); sh.paste(im, (x, y))
        d.text((x + 3, y + Hh + 3), f"{i:02d} id{p['id']} {p['width']}x{p['height']}", fill="yellow")
    sh.save(OUT / f"sheet_{key}.jpg", quality=85)
    print(f"{key:15} {len(ims)}")
    time.sleep(0.5)
(OUT / "px_info.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK", OUT)
