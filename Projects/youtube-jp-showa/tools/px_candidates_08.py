# -*- coding: utf-8 -*-
"""px_candidates_08.py — UNG VIEN Pexels (vat trung tinh, khong lo nam) cho video 08 (okane-joushiki).
1 sheet / query de duyet MAT. Loc SO DEN: id da dung o video 06/07 (real_photos/px_*_<id>.jpg) + INDEX.json kho chung.
"""
import io, sys, json, re, time, requests
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
KEY = (ROOT.parent / "youtube-jp-health" / "tools" / ".pexels_key").read_text(encoding="utf-8").strip(); H = {"Authorization": KEY}
OUT = ROOT / "06_VIDEO" / "08_okane-joushiki" / "_px_candidates"; OUT.mkdir(parents=True, exist_ok=True)

used = set()
for f in ROOT.glob("07_UPLOADED/*/_scripts/*_SLIDES.json"):
    for e in json.loads(f.read_text(encoding="utf-8")):
        m = re.search(r"px_.*?_(\d+)\.jpg", e.get("source", ""))
        if m: used.add(m.group(1))
try:
    idx = json.load(open(r"E:\Claude\Projects\_media_library\INDEX.json", encoding="utf-8"))
    for k, v in (idx.items() if isinstance(idx, dict) else []):
        if isinstance(v, dict) and v.get("used_in") and v.get("source") == "pexels": used.add(str(v.get("source_id")))
except Exception as e: print("INDEX.json:", e)
print("so den pexels:", len(used))

Q = {
 "geta_entrance": "wooden sandals japanese entrance", "genkan_shoes": "shoes lined up entrance japan house",
 "low_table_coins": "coins on wooden table closeup", "counting_cash_hands": "hands counting banknotes table",
 "coins_stack": "stack of coins wooden table", "wallet_coins": "old leather wallet coins",
 "tea_cabinet": "old wooden cabinet drawer japan", "drawer_hidden": "hand reaching into wooden drawer",
 "envelope_brown_b": "kraft envelope on table warm light", "envelope_thick": "thick envelope cash",
 "doorbell_old": "old doorbell button house", "hanko_stamp": "japanese seal stamp red ink",
 "receipt_book": "receipt book carbon paper pen", "black_bag_leather": "old black leather briefcase",
 "rotary_phone": "black rotary telephone closeup", "phone_booth_night": "telephone booth night street",
 "coin_slot": "coin slot payphone closeup", "phone_receiver": "hand holding telephone receiver vintage",
 "bank_counter": "bank counter wooden vintage", "queue_people": "people waiting in line vintage",
 "passbook_pen": "bank passbook pen table", "bank_clock": "old wall clock office",
 "ledger_pencil": "old notebook pencil handwriting ledger", "shop_storefront_old": "old japanese shop storefront wooden",
 "tofu_shop": "tofu shop japan", "rice_bags": "rice bags shop japan",
 "train_ticket_old": "old paper train ticket", "ticket_gate": "railway ticket gate vintage",
 "tram_old": "old tram street japan", "train_platform_old": "old train platform japan",
 "taxi_vintage": "vintage taxi car japan", "bus_old_japan": "old bus japan",
 "tv_vintage": "vintage television wooden cabinet", "tv_knob": "old television dial knob closeup",
 "fan_vintage": "vintage electric fan metal", "fridge_vintage": "vintage refrigerator kitchen retro",
 "pawnshop_window": "jewelry watch display window shop", "kimono_folded": "folded kimono silk",
 "wristwatch_old": "old wristwatch leather table", "ring_gold": "gold ring on wooden table",
 "piggy_bank": "ceramic piggy bank coins", "savings_jar": "glass jar coins savings",
 "butsudan": "japanese buddhist altar home", "mirror_stand": "old dressing table mirror",
 "post_office_jp": "post office japan", "postbox_red_jp": "red post box japan",
 "school_textbook": "old textbooks stack wooden desk", "pencil_name": "pencil writing name notebook",
 "smartphone_payment": "smartphone payment screen hand", "shopping_street_lantern": "japanese shopping street lanterns",
 "fish_shop": "fish market stall japan", "bonus_envelope": "envelope with money on table",
}
for key, q in Q.items():
    try:
        r = requests.get("https://api.pexels.com/v1/search", params=dict(query=q, per_page=15, orientation="landscape"), headers=H, timeout=60).json()
    except Exception as e:
        print(key, "err", e); continue
    ph = [p for p in r.get("photos", []) if str(p["id"]) not in used][:8]
    ims = []
    for p in ph:
        dst = OUT / f"{key}__{p['id']}.jpg"
        if not dst.exists():
            try: dst.write_bytes(requests.get(p["src"]["large"], timeout=60).content)
            except Exception: continue
        ims.append((p["id"], dst))
    if not ims: print(key, "0"); continue
    W, Hh = 320, 180; sh = Image.new("RGB", (W * 4, Hh * 2), "black"); d = ImageDraw.Draw(sh)
    for i, (pid, dst) in enumerate(ims[:8]):
        im = Image.open(dst).convert("RGB"); im.thumbnail((W, Hh)); sh.paste(im, ((i % 4) * W, (i // 4) * Hh))
        d.rectangle(((i % 4) * W, (i // 4) * Hh, (i % 4) * W + 90, (i // 4) * Hh + 13), fill="black"); d.text(((i % 4) * W + 3, (i // 4) * Hh + 1), str(pid), fill="yellow")
    sh.save(OUT / f"sheet_{key}.jpg", quality=82); print(key, len(ims)); time.sleep(0.5)
print("OK ->", OUT)
