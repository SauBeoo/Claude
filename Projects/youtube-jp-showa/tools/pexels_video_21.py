# -*- coding: utf-8 -*-
"""pexels_video_19.py — clip QUAY THAT (Pexels) cho chuyen dong khong lo thoi dai cua video 21.
Loc: >=1920 ngang (net), 5-40s, bo id da used_in o INDEX.json. Sheet = frame dau (anh preview cua Pexels).
"""
import io, sys, json, time
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "21_umaredoshi-okane" / "_pxv"; OUT.mkdir(parents=True, exist_ok=True)
KEY = (ROOT.parent / "youtube-jp-health" / "tools" / ".pexels_key").read_text(encoding="utf-8").strip()
IDX = json.loads((ROOT.parent / "_media_library" / "INDEX.json").read_text(encoding="utf-8"))
USED = {str(v.get("source_id")) for v in IDX.values() if v.get("source") == "pexels" and v.get("used_in")}
USED |= set((ROOT / "06_VIDEO" / "21_umaredoshi-okane" / "_blacklist" / "pexels_used.txt").read_text(encoding="utf-8").split())

Q = {
 "v_passbook": "flipping pages old notebook hands",
 "v_pencil":   "pencil writing numbers paper close up",
 "v_incense":  "incense smoke altar",
 "v_coin":     "coin in palm hand close up",
 "v_bulb":     "light bulb glowing dark",
 "v_ink":      "grinding ink stone calligraphy",
 "v_stamp":    "stamping paper ink",
 "v_postcard": "flipping old postcards",
 "v_radio":    "vintage radio dial turning",
 "v_rotary":   "dialing rotary phone",
 "v_pickup":   "picking up old telephone receiver",
 "v_sakura":   "cherry blossom petals falling",
 "v_heater":   "kerosene heater flame",
 "v_cash":     "counting banknotes hands",
 "v_oldhands": "elderly woman hands holding",
 "v_rain_win": "rain on window night",
}
H = {"Authorization": KEY}
info = {}
for key, q in Q.items():
    try:
        vs = requests.get("https://api.pexels.com/videos/search", headers=H, params={"query": q, "per_page": 30, "orientation": "landscape"}, timeout=60).json().get("videos", [])
    except Exception as e:
        print(key, "err", e); continue
    vs = [v for v in vs if str(v["id"]) not in USED and v["width"] >= 1920 and 5 <= v["duration"] <= 40][:12]
    ims = []
    for i, v in enumerate(vs):
        dst = OUT / f"{key}__{i:02d}.jpg"
        if not dst.exists():
            try: dst.write_bytes(requests.get(v["image"], timeout=60).content)
            except Exception: continue
        best = max((f for f in v["video_files"] if (f.get("width") or 0) <= 1920), key=lambda f: f.get("width") or 0, default=None)
        info[f"{key}__{i:02d}"] = dict(id=v["id"], url=v["url"], user=v["user"]["name"], w=v["width"], h=v["height"], dur=v["duration"], file=best and best["link"])
        ims.append((i, v, dst))
    if not ims: print(key, 0); continue
    W, Hh, cols = 320, 180, 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, (Hh + 16) * rows), "black"); d = ImageDraw.Draw(sh)
    for i, v, dst in ims:
        try: im = Image.open(dst).convert("RGB")
        except Exception: continue
        im.thumbnail((W, Hh)); x, y = (i % cols) * W, (i // cols) * (Hh + 16); sh.paste(im, (x, y))
        d.text((x + 3, y + Hh + 2), f"{i:02d} id{v['id']} {v['width']}x{v['height']} {v['duration']}s", fill="yellow")
    sh.save(OUT / f"sheet_{key}.jpg", quality=85)
    print(f"{key:12} {len(ims)}"); time.sleep(0.5)
(OUT / "pxv_info.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK", OUT)
