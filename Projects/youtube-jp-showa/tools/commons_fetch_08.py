# -*- coding: utf-8 -*-
"""commons_fetch_08.py — tai BAN GOC cac anh Commons DA DUYET MAT (sheet_<key>.jpg) cho video 08.
PICKS: ten_file_dich -> (key, idx tren sheet). Doc candidates_info.json (do commons_candidates_08.py ghi khi xong).
Ghi real_photos/cc_<ten>.jpg + ATTRIBUTIONS_commons.md (license + tac gia + link — credit bat buoc cho CC BY/BY-SA).
"""
import io, sys, json, time, re
from pathlib import Path
import requests
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / "08_okane-joushiki"
CAND = VD / "_cc_candidates"; REAL = VD / "real_photos"; REAL.mkdir(exist_ok=True)
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
info = json.loads((CAND / "candidates_info.json").read_text(encoding="utf-8"))

PICKS = {
 # ten dich                  (key, idx)
 "red_phone_stand":          ("red_phone", 0),
 "red_phone_dial":           ("red_phone", 4),
 "red_phone_wall":           ("red_phone", 6),
 "red_phone_museum":         ("red_phone", 2),
 "coin_10yen_pair":          ("coin_10yen", 1),
 "coins_yen_closeup":        ("coin_10yen", 10),
 "note_10000_back":          ("note_10000_back", 0),
 "note_1000_back":           ("note_1000_ito", 1),
 "notes_old_recto":          ("note_1000_ito", 3),
 "notes_old_verso":          ("note_1000_ito", 4),
 "note_5000_back":           ("note_5000_back", 0),
 "note_500_seriesB":         ("note_500_iwakura", 1),
 "post_office_shimoyama":    ("post_office_old", 10),
 "post_office_ushikubo":     ("post_office_old", 11),
 "yubin_old_sign":           ("yubin_mark", 5),
 "ticket_hard_odawara":      ("ticket_punch", 3),
 "ticket_punchers_museum":   ("ticket_punch", 1),
 "kaisatsu_basami":          ("ticket_punch", 2),
 "ticket_jrwest_punched":    ("ticket_punch", 0),
 "jnr101_orange_mountain":   ("jnr_train_101", 5),
 "jnr101_yellow_nanbu":      ("jnr_train_101", 2),
 "jnr101_bw_valley":         ("jnr_train_101", 6),
 "jnr_kumoyuni_station":     ("jnr_station_1970", 3),
 "jnr_steam_station":        ("jnr_station_1970", 9),
 "toden_1968_stop":          ("toden_tram", 2),
 "toden_1968_platform":      ("toden_tram", 0),
 "toden_1968_street":        ("toden_tram", 1),
 "tv_console_museum":        ("tv_color_vintage", 0),
 "chabudai_round":           ("chabudai_alt", 1),
 "children_tea_party_old":   ("chabudai_alt", 9),
 "tatami_room_lowtable":     ("chabudai_alt", 10),
 "fans_80s":                 ("electric_fan", 0),
 "soroban_23rods":           ("abacus", 0),
 "soroban_counter":          ("abacus", 7),
 "wooden_seals":             ("hanko_inkpad", 2),
 "shotengai_hiroshima_1955": ("shotengai_1970", 3),
 "shotengai_showa20s":       ("shotengai_1970", 7),
 "black_phone_showa":        ("dial_phone_black", 0),
 "geta_makers_old":          ("geta", 6),
 "geta_feet_awa":            ("geta", 9),
 "postal_savings_sign":      ("postal_savings_poster", 0),
 "rice_shop_old":            ("rice_shop", 6),
 "rice_shop_naha_1935":       ("rice_shop", 5),
 "station_1968_small":       ("toden_tram", 3),
 "tobus_1960s":              ("toden_tram", 8),
 "rail_1968_crossing":        ("jnr_station_1970", 4),
 "first_electric_goods":      ("electric_fan", 1),
 "kakeibo_old_books":         ("kakeibo", 1),
}

def lic_ok(l): return bool(re.search(r"(public domain|^pd|cc0|cc[- ]by)", l, re.I)) and not re.search(r"(nc|nd)", l, re.I)

rows, n = [], 0
for name, (key, idx) in PICKS.items():
    k = f"{key}__{idx:02d}"; m = info.get(k)
    if not m: print(f"[THIEU INFO] {name} <- {k} (chua co trong candidates_info.json)"); continue
    if not lic_ok(m["license"]): print(f"[LICENSE LOAI] {name}: {m['license']}"); continue
    dst = REAL / f"cc_{name}.jpg"
    if not dst.exists():
        # ban goc Commons nhieu tam 5-15MB, upload.wikimedia.org bop toc do -> tai qua thumb 1920px (du cho 1920x1080)
        u = m["url"].split("?")[0]; fn = u.rsplit("/", 1)[1]
        thumb = u.replace("/commons/", "/commons/thumb/") + f"/1920px-{fn}" + ("" if fn.lower().endswith((".jpg", ".jpeg", ".png")) else ".jpg")
        for att, url in enumerate([thumb, thumb, thumb, u, u]):
            try:
                r = requests.get(url, headers=H, timeout=60)
                if r.status_code == 200 and len(r.content) > 20000:
                    dst.write_bytes(r.content); break
                if r.status_code == 429:   # Wikimedia bop toc do: nghe theo Retry-After, toi thieu 30s, tang dan
                    wait = max(int(r.headers.get("Retry-After", "0") or 0), 45 * (att + 1))
                    print(f"   429 {name} -> cho {wait}s"); time.sleep(wait); continue
                print("   http", r.status_code, name, url[-40:]); time.sleep(5)
            except Exception as e:
                print("   err", name, str(e)[:60]); time.sleep(5)
        if not dst.exists(): continue
        try:  # ep ve JPG RGB (nguon co the la PNG/tiff)
            im = Image.open(dst).convert("RGB")
            if max(im.size) > 3200: im.thumbnail((3200, 3200), Image.LANCZOS)
            im.save(dst, quality=94)
        except Exception as e:
            print("[LOI ANH]", name, e); dst.unlink(missing_ok=True); continue
        time.sleep(5)
    n += 1
    title = m["title"].replace("File:", "")
    rows.append(f"| cc_{name} | {title} | {m['license']} | {m.get('artist','')} | https://commons.wikimedia.org/wiki/{m['title'].replace(' ', '_')} |")
    print(f"  ✓ cc_{name:26} {m['license']:14} {m['w']}x{m['h']}  {title[:50]}")

(VD / "ATTRIBUTIONS_commons.md").write_text(
    "# Wikimedia Commons — video 08 (credit theo license; PD/CC0 ghi de tra nguon)\n\n| file | title | license | artist | url |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
    encoding="utf-8")
print(f"OK {n}/{len(PICKS)} -> {REAL}")
