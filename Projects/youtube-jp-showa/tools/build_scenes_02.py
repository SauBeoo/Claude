# -*- coding: utf-8 -*-
"""Sinh SLIDES.json + prompt gen anh cho video 02 (kieta-mise).

- 30 anh cho 30 diem + 12 anh khung = 42 entry.
- match lay THANG tu dong trong _TTS.md -> khong bao gio chet cue.
- prompt = [canh] + [preset boi canh 1B] + [style lock 1A] + [Avoid] (04_VIDEOGEN_PROMPTS.md).
"""
import io, sys, re, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "02_kieta-mise_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "02_kieta-mise_SLIDES.json"
OUT_DIR = ROOT / "06_VIDEO" / "02_kieta-mise"
# DUR tu do tu chinh file _TTS.md — KHONG hardcode (sua loi thi so nay phai tu doi theo)
def _dur():
    import re as _re
    t = _re.sub(r"\[[^\]]*\]", "", TTS.read_text(encoding="utf-8"))
    return len(_re.sub(r"\s", "", t)) / 3.98  # 3.98 ky/giay = he so do that cua kenh (video 01)

# --- 04_VIDEOGEN_PROMPTS.md §1 ---
LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, "
        "faded warm Fujicolor palette, soft natural light, gentle film grain, "
        "slight vignette, nostalgic documentary photography, muted greens and ochres, "
        "natural imperfect framing, 16:9")
PRESET = {
    "shotengai": ("narrow Showa shopping street, wooden shopfronts, fabric awnings and noren curtains, "
                  "hand-painted signage kept out of focus, worn asphalt and concrete"),
    "home": ("small Showa house interior, tatami room, wooden sliding doors, low table, single bare bulb"),
    # pho nhung KHONG nhac noren/bien hieu — cho canh can mat tien TRON (slide_39)
    "shotengai_nosign": ("narrow Showa shopping street, wooden shopfronts, worn asphalt and concrete, "
                         "plain weathered timber and blank boards, no lettering and no shop signs anywhere"),
    # canh BEN TRONG cua hang: KHONG dung 'shotengai' (chuoi do ta PHO -> mau thuan
    # voi 'no street visible' va model se chon ve dai hon; da dinh that o slide_20)
    "shop_interior": ("inside a small Showa-era shop, dark stained wood shelving, worn plank floor, "
                      "low ceiling, one bare bulb, dusty still air, no street and no sky in frame"),
    "super": ("early 1970s Japanese supermarket interior, metal shelving, fluorescent strip lights, "
              "stacked cardboard, wide aisle"),
}
# 🔴 'no watermark' PHAI CO — thieu no o lot gen 2026-08-10 lam ca 42 anh dinh dau ✦
#    goc duoi phai, phai crop 9,7% de cuu. Dung bo dong nay.
AVOID = ("no watermark, no logo, no signature, no sparkle mark. "
         "Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, "
         "modern clothing, sneakers with logos, readable text or signage, brand logos, "
         "western faces, anime style, oversaturated HDR look, close-up faces.")

# (chi so dong noi dung trong TTS, ten file, preset, mo ta canh)
SCENES = [
    (2, "27_milk_box", "home", "a small wooden milk box mounted beside a house entrance before dawn, two glass bottles inside, blue morning light"),
    (5, "28_paper_cap", "home", "extreme close-up of a glass milk bottle with a round paper cap, a thumbnail pressing at its edge"),
    (6, "29_caps_collect", "home", "small hands arranging a row of collected round paper milk caps on a tatami mat"),
    (8, "40_futari", "shotengai", "two figures at a shop counter seen in silhouette against the evening street, one leaning in, faces not visible"),
    (9, "00_itsumono", "shotengai", "seen from behind, an aproned shopkeeper and a customer talking across a low wooden counter at dusk, both figures backlit, faces not visible"),
    (11, "02_one_shutter", "shotengai", "a single closed corrugated shutter between two open shops, faded paint, an empty crate in front"),
    (14, "03_rappa", "shotengai", "close-up of a small brass horn hanging from the handle of a wooden vendor handcart, worn leather strap"),
    (15, "04_nabe", "shotengai", "close-up of two hands holding an aluminium pot filled with water, a white block of tofu floating inside, shot from above"),
    (17, "05_okara", "shotengai", "close-up of soft white okara crumbs in an open brown paper bag on a wet wooden counter"),
    (18, "06_tofu_kama", "shotengai", "interior of a tiny tofu workshop before dawn, a large steaming metal vat, steam catching a shaft of light, no people"),
    (20, "11_goyoukiki", "home", "seen from inside a doorway, an aproned delivery man standing at the entrance holding a small notebook, face turned away"),
    (21, "12_komebitsu", "home", "rice pouring from a paper sack into a wooden rice bin, grains caught mid-air, dim kitchen light"),
    (22, "13_kayoicho", "shotengai", "close-up of a small worn ledger notebook lying open on a shop counter with a stub pencil across it, writing illegible and out of focus"),
    (25, "14_kome_ya", "shotengai", "interior of a rice shop, stacked straw and paper sacks, an old balance scale, dusty light"),
    (27, "15_hakariuri", "shotengai", "close-up of a glass bottle and a metal funnel on a counter beside a large wooden soy sauce barrel with a tap"),
    (28, "16_buriki_bucket", "shotengai", "three galvanised tin buckets stacked outside a general goods shop, dented and scratched"),
    (29, "17_katori", "home", "close-up of a round metal mosquito coil tin, open, a spiral coil burning on a small stand, thin smoke"),
    (32, "07_nokogiri", "shotengai", "close-up of a hand saw biting into a large clear block of ice, fine ice sawdust scattered on wet wooden boards"),
    (36, "08_ice_box", "home", "an old wooden icebox with its upper door open, a square block of ice inside, condensation running down the wood"),
    (37, "09_kakigori", "shotengai", "close-up of a hand-cranked ice shaver on a shop counter, beside it a glass bowl of freshly shaved white ice topped with bright clear strawberry syrup, vivid cheerful red, clean and appetising, definitely not dark red and not brown"),
    (39, "10_reizouko", "home", "a rounded-corner electric refrigerator standing in a small kitchen, chrome handle, checked curtain behind"),
    (43, "21_peak_street", "shotengai", "a crowded shopping street at its busiest, many distant shoppers, awnings and hanging lanterns receding into the distance"),
    (45, "23_shutters_row", "shotengai", "a row of five closed shutters in a row along an empty shopping street, weeds at the base, overcast light"),
    (46, "22_super", "super", "a wide aisle of an early 1970s supermarket, long metal shelves fully stocked, a shopping basket left on the floor, no people"),
    (51, "24_kuji", "shotengai", "close-up of a child-sized hand holding a single ten-yen coin above a paper lottery board full of small numbered tabs"),
    (52, "25_okashi_oku", "shotengai", "looking into the dark interior of a tiny sweet shop from the bright doorway, a seated figure silhouetted at the back, face not visible"),
    (53, "26_dagashi_tray", "shotengai", "close-up of shallow wooden trays and glass jars filled with assorted small penny sweets, no price cards"),
    (55, "37_kasa_hone", "shotengai", "close-up of an umbrella frame with pliers repairing a single broken rib, rain visible outside the shop entrance"),
    (58, "36_hanao", "shotengai", "close-up of weathered hands threading a new fabric thong into a wooden geta sandal on a workbench"),
    (60, "38_kutsu_soko", "shotengai", "close-up of a worn leather shoe upside down on a cobbler's last, a hand pressing a new sole into place"),
    (62, "18_kashihonya", "shotengai", "interior of a small book lending shop, tall wooden shelves packed with worn magazines reaching the ceiling, dim bulb"),
    (64, "19_manga_corner", "shotengai", "close-up of a stack of well-thumbed magazines, corners rounded and soft, one page folded down"),
    (66, "20_dust_light", "shop_interior", "interior of a cramped book lending shop, a very narrow gap between two tall wooden bookshelves packed with worn magazines, one shaft of light from a high window crossing the gap, dust motes floating thickly in the beam, no street and no sky visible, no people"),
    (67, "30_tabakoya", "shotengai", "a small square service window cut into the corner of a wooden house, a shadowed figure seated inside, faces not visible"),
    (69, "31_akai_denwa", "shotengai", "close-up of a red public telephone on a small shelf beside a shop window, coin slot and dial"),
    (70, "32_michi_annai", "shotengai", "seen from across the street, a seated figure at a corner shop window pointing down the road for a passer-by, both distant"),
    (71, "33_shinkukan", "home", "a hand reaching into the open back panel of a wooden-cased television, pulling out a glowing vacuum tube, dim room"),
    (74, "34_geppu", "home", "close-up of an old collection ledger and a few worn banknotes on a low wooden table, writing illegible"),
    (75, "35_tv_kita_hi", "home", "a wooden-cased television on legs glowing in a dark tatami room, several people seen from behind sitting close together"),
    (82, "39_tofuya_asa", "shotengai_nosign", "a tofu shop front at first light, shutter half raised, steam drifting out into the cold street, the signboard above the entrance is completely blank and weathered with no characters written on it, no noren curtain, no lettering anywhere on the building, no shop name"),
    (89, "41_yugure", "shotengai", "the shopping street at dusk, paper lanterns just lit, the road empty and glistening"),
]

# Phim tu lieu THAT (Japan Today 1959, CC0) — (chi so dong, id, ss, dur).
# Cat bang cut_archival.py voi spec tools/archival_spec_02.json; file = clips/clip_<entry>.mp4
ARCH = [
    (0, "yoake_alley", 924.5, 8.0),
    (12, "machi_aruki", 900.0, 7.0),
    (13, "tofu_asa_stall", 913.0, 9.5),
    (19, "yasai_haitatsu", 1352.0, 9.0),
    (24, "taue_ushi", 1664.5, 8.0),
    (42, "peak_banner_st", 937.0, 9.0),
    (50, "dagashi_stall", 1611.0, 6.5),
    (57, "machiai_kutsumigaki", 961.0, 8.5),
    (59, "kutsu_soko_syuuri", 1317.0, 8.0),
]


def content_lines(raw):
    out = []
    for l in raw.split("\n"):
        s = re.sub(r"\[[^\]]*\]", "", l).strip()
        if s:
            out.append(s)
    return out


def main():
    raw = TTS.read_text(encoding="utf-8")
    lines = content_lines(raw)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    slides, flow, names, rows = [], [], [], []
    err = 0
    # TRON anh AI (SCENES) + phim that (ARCH) theo thu tu dong — entry index chay chung.
    merged = sorted([("img", s[0], s) for s in SCENES] + [("vid", a[0], a) for a in ARCH],
                    key=lambda x: x[1])
    for kind, idx, item in merged:
        if idx >= len(lines):
            print(f"[LOI] chi so dong {idx} vuot ngoai file"); err += 1; continue
        line = lines[idx]
        m = line[:14]
        # GATE: match phai la substring cua MOT dong (sau khi strip tag)
        if not any(m in L for L in lines):
            print(f"[LOI] match khong khop: {m}"); err += 1; continue
        if kind == "vid":
            slides.append({"match": m, "video": True})
            continue
        _, name, preset, desc = item
        slides.append({"match": m, "photo": True})
        flow.append(f"{desc}, {PRESET[preset]}, {LOCK}. {AVOID}")
        names.append(f"slide_{len(slides)-1:02d}_{name}.jpg")
        rows.append((len(rows), name, preset, m, desc))

    # GATE 2: prompt TU MAU THUAN — mo ta ghi 'no X' ma preset phia sau lai ta X.
    # Da dinh 2 lan: slide_20 ('no street' + preset ta pho), slide_39 ('no noren/
    # no lettering' + preset ta noren/signage). Model chon ve dai hon -> ve ra X.
    PAIRS = [("no street", "shopping street"), ("no noren", "noren"),
             ("no lettering", "signage"), ("no shop sign", "signage"),
             ("no sky", "sky"), ("no people", "shoppers")]
    # ⚠️ Phai BO moi cum phu dinh 'no ... <pos>' truoc khi tim <pos>, neu khong
    #    chinh cum 'no noren' chua chu 'noren' se tu to cao minh (false positive).
    def _positive(text, pos):
        t = re.sub(r"\bno\b(?:\s+\w+){0,3}\s+" + re.escape(pos), " ", text)
        return pos in t

    # ⚠️ CHI quet [mo ta + preset + lock] — KHONG quet AVOID, vi ca danh sach Avoid
    #    von la phu dinh ('readable text or signage' = TRANH signage).
    for i, (idx, name, preset, desc) in enumerate(SCENES):
        low = f"{desc}, {PRESET[preset]}, {LOCK}".lower()
        for neg, pos in PAIRS:
            if neg in low and _positive(low, pos):
                print(f"[LOI] prompt {i:02d} TU MAU THUAN: co '{neg}' nhung van ta '{pos}'")
                err += 1

    if err:
        print(f"\n🔴 {err} loi — KHONG ghi file"); sys.exit(1)

    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT_DIR / "scene_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (OUT_DIR / "scene_prompts_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8")

    n = len(slides)
    print(f"OK {n} entry -> {OUT_JSON.name}")
    print(f"   {_dur()/n:5.1f} giay/hinh   (khong duoi 6s)      {'OK' if _dur()/n >= 6 else 'RỚT'}")
    print(f"   {n/(_dur()/60):5.2f} doi hinh/phut (tran 6)      {'OK' if n/(_dur()/60) <= 6 else 'RỚT'}")
    print(f"   {_dur()/n:5.1f}s max treo    (canh bao >60s)     {'OK' if _dur()/n <= 60 else 'CANH BAO'}")
    print(f"   phim that: {sum(1 for e in slides if e.get('video'))} entry (clips/clip_XX.mp4 theo index)")
    print(f"   30 diem co anh: {sum(1 for r in rows if '点目' in lines[dict((s[1],s[0]) for s in SCENES)[r[1]]])}")


if __name__ == "__main__":
    main()
