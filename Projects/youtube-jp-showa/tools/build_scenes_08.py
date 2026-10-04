# -*- coding: utf-8 -*-
"""build_scenes_08.py — video 08 (okane-joushiki, 12 diem) — REAL-FIRST, AI chi lap <=20% (khuon build_scenes_06_v2).

Nguon (moi shot mot kind):
  vid  clip phim CC0 (footage_raw/, cat bang cut_archival.py --record 08_okane-joushiki)           12
  st   ANH TINH cat tu phim CC0 (real_photos/st08_*.jpg, bp08_st_*.jpg, grab_stills.py, da ghi so den) 18
  cc   Wikimedia Commons PD/CC (real_photos/cc_*.jpg, commons_fetch_08.py -> ATTRIBUTIONS_commons.md)
  px   Pexels — VAT TRUNG TINH khong lo nam, duyet mat 2026-09-03 tren _px_candidates/sheet_*.jpg
  ai   9 CLIP AI (Veo/Flow, i2v 8s) — user gen 2026-09-03, da crop bo watermark "Veo" (+ datestamp
       "OCT 14 1969" o clip 03) roi scale 1920x1080/30fps -> footage_raw/ai08_*.mp4. Van TICK synthetic.

🔴 RATE = 5.45 ky/giay — do that cua AivisSpeech 阿井田茂 0.90 (video 06: 3.273 ky -> 600s). KHONG dung 3.983.
🔴 Moi asset (clip/still/cc/px id) chi xuat hien DUNG 1 LAN trong video (gate trong tool).
🔴 Entry 0 phai la CLIP PHIM THAT (luat kenh showa).
"""
import io, sys, re, json, shutil, time, os
from pathlib import Path
import requests
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grade_vintage import grade  # noqa: E402

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "08_okane-joushiki_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "08_okane-joushiki_SLIDES.json"
VD = ROOT / "06_VIDEO" / "08_okane-joushiki"
REAL = VD / "real_photos"; IMG = VD / "slides_img"; CLIPS = VD / "clips"; FOOTAGE = VD / "footage_raw"; PXC = VD / "_px_candidates"
RATE = 5.45
PEXELS_KEY = (ROOT.parent / "youtube-jp-health" / "tools" / ".pexels_key").read_text(encoding="utf-8").strip()

LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, "
        "soft natural light, gentle film grain, slight vignette, nostalgic documentary photography, "
        "muted greens and ochres, natural imperfect framing, 16:9")
PRESET = {
    "home": ("inside a modest 1970 Japanese wooden house, tatami floor, a low table, a dark wooden tea cabinet, "
             "paper sliding doors, one warm bulb, no street and no sky in frame"),
    "bank": ("inside a 1969 Japanese bank branch, long wooden counter with a wire-mesh teller window, "
             "worn linoleum floor, a round wall clock, no street and no sky in frame"),
    "postoffice": ("inside a small Showa-era post office, a long wooden counter, a wire mesh screen at the window, "
                   "worn linoleum floor, no street and no sky in frame"),
    "street": ("a narrow Japanese shopping street around 1970, low wooden shopfronts, cloth awnings, "
               "a few bicycles, soft evening light, no cars in frame"),
}
AVOID = ("no watermark, no logo, no signature, no sparkle mark. Avoid: modern objects, smartphones, LED lights, "
         "plastic bottles, air conditioner, modern clothing, sneakers with logos, readable text or signage, "
         "brand logos, western faces, anime style, oversaturated HDR look, close-up faces.")

# chi so dong noi dung (content_lines) — xem bang moc trong 08_okane-joushiki.md §LOP HINH
SECTION_RANGES = {
    "cold": (0, 6), "item1": (6, 12), "rules": (12, 15), "item2": (15, 21), "item3": (21, 29),
    "item4": (29, 36), "item5": (36, 44), "item6": (44, 51), "item7": (51, 58), "cta": (58, 59),
    "item8": (59, 67), "item9": (67, 76), "item10": (76, 84), "item11": (84, 90), "item12": (90, 98),
    "ending": (98, 106),
}

# Pexels picks (duyet mat 2026-09-03). key -> id. ⛔ khong dung id da len song o 06/07 (px_candidates_08 da loc)
PX = {
    "geta_stone_step": 37252613, "geta_temple_door": 13684423, "old_house_facade": 8495950,
    "cabinet_drawers_wood": 4140920, "hand_open_old_drawer": 38371820, "hand_reach_shelf": 7303858,
    "kraft_envelopes": 8250874, "hagaki_postcards": 4410164, "doorbell_brass": 1978,
    "inkpad_seals": 6213061, "wood_stamp_radio": 38978902,
    "rotary_black_handset": 13758303, "rotary_black_pen": 47319, "rotary_black_green": 38104133,
    "hand_dial_red": 10397356, "hand_dial_red_b": 36238556,
    "shop_wood_person": 31376737, "shop_retro_signs": 31338881, "shop_dark_kanji": 8050439,
    "shop_facade_old": 17776658, "old_town_street": 7146295, "shop_night_old": 8050435,
    "tram_bw_pair": 15164392, "tram_preserved": 35639573, "taxi_crown_bw": 32093048, "taxi_crown_night": 39111637,
    "taxis_station_front": 5010456, "train_old_platform": 17099379, "train_orange_115": 30688320,
    "bus_night_old": 31376740, "bus_retro": 23024120,
    "queue_bw_wall": 25211989, "ledger_columns": 164686, "desk_clock_notebook": 159618, "hand_pencil_bw": 26855735,
    "tv_attic_old": 34729461, "tv_shelf_old": 33805706, "room_vintage_tv": 27307265, "radio_dials": 16183458,
    "fan_yellow_old": 1374448, "fridge_yellow_dim": 5668902,
    "pawn_window_clocks": 2029594, "jewelry_shop_small": 39272820, "silk_cream_folds": 8465943, "fabrics_stacked": 365066,
    "briefcase_latch": 35859938, "briefcases_legs": 6535352, "wall_clock_wood": 191703, "wall_clock_bracket": 23916841,
    "mirror_clock_phone": 285857, "dressing_table_antique": 21612521,
    "books_two_old": 5984609, "books_stack_old": 1333742, "pencils_wood_notebook": 419635,
    "smartphone_hands": 6969811, "arcade_lanterns": 793432, "arcade_people": 10698284,
    "wood_door_bicycle": 30953502, "shoten_lantern_alley": 7631461, "shop_wood_signboard": 4070930,
    "coins_on_low_table": 144233, "old_lane_morning": 7146301, "drawer_papers_upright": 5089125, "coins_stack_rising": 8369695, "butsudan_home": 27500610,
    "camera_watch_wood": 6113, "gold_rings_wood": 37488824, "postbox_red_street": 10698491, "piggy_terracotta": 31191992,
}

# SHOTS: (name, kind, ref[, dur])  kind: vid | st | cc | px | ai
SHOTS = {
"cold": [
    ("jt08_01_rain_umbrellas", "vid", "jt08_01_rain_umbrellas", 6),          # GIAY 0 = CLIP THAT (luat kenh)
    ("geta_stone_step", "px", "geta_stone_step"),                            # 下駄
    ("cc_geta_feet_awa", "cc", "cc_geta_feet_awa"),                          # 下駄の音
    ("cc_coins_yen_closeup", "cc", "cc_coins_yen_closeup"),                  # 小銭
    ("cc_notes_old_recto", "cc", "cc_notes_old_recto"),                      # 千円札
    ("cabinet_drawers_wood", "px", "cabinet_drawers_wood"),                  # 茶箪笥
    ("hand_open_old_drawer", "px", "hand_open_old_drawer"),                  # 奥に手を入れる
],
"item1": [
    ("wood_door_bicycle", "px", "wood_door_bicycle"),                        # 玄関に立っていたのは — cua go nha Nhat
    ("doorbell_brass", "px", "doorbell_brass"),
    ("inkpad_seals", "px", "inkpad_seals"),                                  # 判子
    ("tv_attic_old", "px", "tv_attic_old"),                                  # 受信料
    ("ai08_01_genkan_getabako", "vid", "ai08_01_genkan_getabako", 8),
    ("briefcase_latch", "px", "briefcase_latch"),
    ("geta_temple_door", "px", "geta_temple_door"),                          # 下駄箱の上
    ("wood_stamp_radio", "px", "wood_stamp_radio"),
],
"rules": [
    ("cc_notes_old_verso", "cc", "cc_notes_old_verso"),
    ("ledger_columns", "px", "ledger_columns"),
    ("st08_22_temple_path_crowd", "st", "st08_22_temple_path_crowd"),
    ("cc_note_1000_back", "cc", "cc_note_1000_back"),
    ("hand_reach_shelf", "px", "hand_reach_shelf"),
],
"item2": [
    ("kraft_envelopes", "px", "kraft_envelopes"),                            # 茶色い封筒
    ("cc_tatami_room_lowtable", "cc", "cc_tatami_room_lowtable"),            # 卓袱台
    ("cc_note_500_seriesB", "cc", "cc_note_500_seriesB"),
    ("cc_soroban_23rods", "cc", "cc_soroban_23rods"),                            # 経理のそろばん
    ("st08_05_kinkakuji_crowd", "st", "st08_05_kinkakuji_crowd"),
    ("cc_station_1968_small", "cc", "cc_station_1968_small"),                # 三億円事件 1968 — ga nho 1968 BW
    ("cc_shotengai_showa20s", "cc", "cc_shotengai_showa20s"),                # 商店街 昭和20年代 (PD)
    ("arcade_lanterns", "px", "arcade_lanterns"),
    ("shop_dark_kanji", "px", "shop_dark_kanji"),                            # 魚屋
    ("shoten_lantern_alley", "px", "shoten_lantern_alley"),                  # 給料日の夕方、商店街が明るく
],
"item3": [
    ("jt08_03_park_bicycles", "vid", "jt08_03_park_bicycles", 8),           # 日曜
    ("cc_note_5000_back", "cc", "cc_note_5000_back"),
    ("st08_06_park_family_pond", "st", "st08_06_park_family_pond"),
    ("fan_yellow_old", "px", "fan_yellow_old"),                              # 扇風機
    ("cc_fans_80s", "cc", "cc_fans_80s"),
    ("fridge_yellow_dim", "px", "fridge_yellow_dim"),                        # 冷蔵庫
    ("cc_first_electric_goods", "cc", "cc_first_electric_goods"),            # 冷蔵庫が来た家も
],
"item4": [
    ("cc_note_10000_back", "cc", "cc_note_10000_back"),                      # 一万円札
    ("cc_notes_old_verso_b", "cc", "cc_notes_old_recto_dup_guard"),         # placeholder — thay ben duoi
    ("shop_night_old", "px", "shop_night_old"),                              # 豆腐屋
    ("desk_clock_notebook", "px", "desk_clock_notebook"),
    ("coins_on_low_table", "px", "coins_on_low_table"),                      # 給料の四分の一
    ("ai08_02_hands_count_notes", "vid", "ai08_02_hands_count_notes", 8),
    ("cc_coin_10yen_pair", "cc", "cc_coin_10yen_pair"),
],
"item5": [
    ("old_lane_morning", "px", "old_lane_morning"),                          # 翌朝、銀行へ — ngo pho cu buoi sang
    ("wall_clock_wood", "px", "wall_clock_wood"),                            # 午後三時
    ("ai08_03_bank_counter", "vid", "ai08_03_bank_counter", 8),
    ("cc_jnr_steam_station", "cc", "cc_jnr_steam_station"),                 # 新宿と梅田 — nha ga (mood)
    ("ai08_04_cash_dispenser", "vid", "ai08_04_cash_dispenser", 8),
    ("wall_clock_bracket", "px", "wall_clock_bracket"),
    ("ledger_columns_b", "px", "desk_clock_notebook_dup_guard"),             # placeholder — thay ben duoi
],
"item6": [
    ("jt08_02_kimono_women_walk", "vid", "jt08_02_kimono_women_walk", 8),   # 母が商店街へ
    ("st08_01_kimono_women_close", "st", "st08_01_kimono_women_close"),
    ("shop_wood_person", "px", "shop_wood_person"),                          # 米屋・酒屋
    ("cc_rice_shop_naha_1935", "cc", "cc_rice_shop_naha_1935"),              # 米屋 — cho gao 1935 (PD)
    ("shop_facade_old", "px", "shop_facade_old"),
    ("cc_shotengai_hiroshima_1955", "cc", "cc_shotengai_hiroshima_1955"),    # 商店街 1955 (PD)
    ("cc_chabudai_round", "cc", "cc_chabudai_round"),                        # 茶箪笥の引き出し (nha)
    ("st08_02_kimono_women_smile", "st", "st08_02_kimono_women_smile"),
],
"item7": [
    ("bp08_01_tram_street", "vid", "bp08_01_tram_street", 8),               # 都電 + xe
    ("cc_ticket_hard_odawara", "cc", "cc_ticket_hard_odawara"),             # 硬い切符
    ("cc_kaisatsu_basami", "cc", "cc_kaisatsu_basami"),                     # 鋏
    ("cc_jnr101_orange_mountain", "cc", "cc_jnr101_orange_mountain"),       # 国鉄
    ("cc_toden_1968_stop", "cc", "cc_toden_1968_stop"),                     # 都電
    ("cc_toden_1968_street", "cc", "cc_toden_1968_street"),                  # 都電やバスは二十円 — pho co tram 1968
    ("cc_rail_1968_crossing", "cc", "cc_rail_1968_crossing"),                # 十年前は十円 → 七十円に
],
"cta": [
    ("st08_10_seashore_crowd", "st", "st08_10_seashore_crowd"),
    ("cc_toden_1968_platform", "cc", "cc_toden_1968_platform"),
    ("bp08_st_01_street_buses", "st", "bp08_st_01_street_buses"),
    ("tram_bw_pair", "px", "tram_bw_pair"),
],
"item8": [
    ("cc_red_phone_stand", "cc", "cc_red_phone_stand"),                     # 赤い電話
    ("cc_coin_10yen_pair_b", "cc", "cc_coin_10yen_pair_dup_guard"),         # placeholder — thay ben duoi
    ("cc_red_phone_dial", "cc", "cc_red_phone_dial"),
    ("rotary_black_handset", "px", "rotary_black_handset"),
    ("jt08_04_tea_pickers_wide", "vid", "jt08_04_tea_pickers_wide", 8),     # 田舎の祖母
    ("hand_dial_red", "px", "hand_dial_red"),
    ("cc_black_phone_showa", "cc", "cc_black_phone_showa"),                  # 黒電話 — 母が祖母にかける
    ("cc_red_phone_wall", "cc", "cc_red_phone_wall"),
    ("jt08_05_tea_picker_hat", "vid", "jt08_05_tea_picker_hat", 8),
    ("st08_08_tea_picker_hat_turn", "st", "st08_08_tea_picker_hat_turn"),
],
"item9": [
    ("tv_shelf_old", "px", "tv_shelf_old"),                                  # テレビ
    ("cc_tv_console_museum", "cc", "cc_tv_console_museum"),
    ("jt08_07_sumo_bout", "vid", "jt08_07_sumo_bout", 10),                  # テレビで見た相撲
    ("radio_dials", "px", "radio_dials"),
    ("st08_16_stage_dancers", "st", "st08_16_stage_dancers"),
    ("st08_12_sumo_audience", "st", "st08_12_sumo_audience"),
    ("jt08_08_sumo_b", "vid", "jt08_08_sumo_b", 10),
    ("hagaki_postcards", "px", "hagaki_postcards"),                          # 月賦の集金
    ("ai08_05_livingroom_tv", "vid", "ai08_05_livingroom_tv", 8),
],
"item10": [
    ("pawn_window_clocks", "px", "pawn_window_clocks"),                      # 質屋
    ("silk_cream_folds", "px", "silk_cream_folds"),                          # 着物
    ("camera_watch_wood", "px", "camera_watch_wood"),                        # 時計
    ("gold_rings_wood", "px", "gold_rings_wood"),                            # 指輪
    ("jewelry_shop_small", "px", "jewelry_shop_small"),
    ("fabrics_stacked", "px", "fabrics_stacked"),
    ("shop_dark_kanji_b", "px", "old_town_street"),                          # のれん (pho cu)
    ("st08_18_rice_planter_b", "st", "st08_18_rice_planter_b"),             # あの日の母 — mood
],
"item11": [
    ("drawer_papers_upright", "px", "drawer_papers_upright"),                # 十一点目 へそくり — ngan keo giau giay to
    ("butsudan_home", "px", "butsudan_home"),                                # 仏壇の下
    ("ai08_06_hesokuri_drawer", "vid", "ai08_06_hesokuri_drawer", 8),
    ("piggy_terracotta", "px", "piggy_terracotta"),                          # 貯金箱
    ("old_house_facade", "px", "old_house_facade"),                          # どの家にも
    ("cc_geta_makers_old", "cc", "cc_geta_makers_old"),                      # 母たちの時代 (anh cu)
    ("st08_09_tea_field_two", "st", "st08_09_tea_field_two"),
],
"item12": [
    ("cc_post_office_shimoyama", "cc", "cc_post_office_shimoyama"),         # 郵便局
    ("cc_yubin_old_sign", "cc", "cc_yubin_old_sign"),
    ("cc_postal_savings_sign", "cc", "cc_postal_savings_sign"),              # 郵便貯金
    ("postbox_red_street", "px", "postbox_red_street"),
    ("ai08_07_passbook_stamp", "vid", "ai08_07_passbook_stamp", 8),
    ("cc_post_office_ushikubo", "cc", "cc_post_office_ushikubo"),
    ("cc_jnr101_yellow_nanbu", "cc", "cc_jnr101_yellow_nanbu"),             # 昭和四十九年 — mood thoi dai
    ("ai08_08_post_counter", "vid", "ai08_08_post_counter", 8),
    ("coins_stack_rising", "px", "coins_stack_rising"),                      # 百万円が二百十九万円
],
"ending": [
    ("smartphone_hands", "px", "smartphone_hands"),                          # 手のひらの画面
    ("cc_children_tea_party_old", "cc", "cc_children_tea_party_old"),
    ("st08_15_daibutsu_students", "st", "st08_15_daibutsu_students"),
    ("jt08_09_schoolgirls_crowd", "vid", "jt08_09_schoolgirls_crowd", 5),
    ("books_two_old", "px", "books_two_old"),                                # 教科書
    ("pencils_wood_notebook", "px", "pencils_wood_notebook"),                # 鉛筆
    ("jt08_10_schoolboys_crowd", "vid", "jt08_10_schoolboys_crowd", 6),
    ("books_stack_old", "px", "books_stack_old"),
    ("ai08_09_passbook_pencil", "vid", "ai08_09_passbook_pencil", 8),
    ("st08_19_rice_field_wide", "st", "st08_19_rice_field_wide"),
    ("jt08_11_seashore_crowd", "vid", "jt08_11_seashore_crowd", 6),
],
}
# thay placeholder bang asset that (giu SHOTS de doc)
SHOTS["item4"][1] = ("cc_soroban_counter", "cc", "cc_soroban_counter")             # 「くずれますか」 quay tinh tien
SHOTS["item5"][6] = ("cc_wooden_seals", "cc", "cc_wooden_seals")                   # 印鑑
SHOTS["item8"][1] = ("cc_red_phone_museum", "cc", "cc_red_phone_museum")

IMG_SLOT_MIN = 5.5


def content_lines(raw):
    return [s for s in (re.sub(r"\[[^\]]*\]", "", l).strip() for l in raw.split("\n")) if s]


def line_starts(lines):
    starts, cum = [], 0.0
    for l in lines:
        starts.append(cum / RATE); cum += len(l)
    total = cum / RATE
    return starts, starts[1:] + [total], total


def uniq_match(lines, idx):
    L = lines[idx]
    for n in range(14, len(L) + 1, 2):
        if sum(1 for x in lines if L[:n] in x) == 1: return L[:n]
    return L


def find_line_and_offset(t, starts, ends):
    for i, (s, e) in enumerate(zip(starts, ends)):
        if s <= t < e or (i == len(starts) - 1 and t >= s): return i, round(t - s, 2)
    return len(starts) - 1, 0.0


def place_section(shots, ws, we):
    shots = list(shots)
    while True:
        vid_total = sum(sh[3] for sh in shots if sh[1] == "vid")
        n_img = sum(1 for sh in shots if sh[1] != "vid")
        slot = (we - ws - vid_total) / n_img if n_img else 0
        if slot >= IMG_SLOT_MIN or n_img == 0: break
        for k in ("ai", "px"):   # bo dan: AI truoc, roi px — khong bao gio bo clip/still/cc
            idx = [i for i, sh in enumerate(shots) if sh[1] == k]
            if idx: shots.pop(idx[-1]); break
        else: break
    out, t = [], ws
    for sh in shots:
        out.append((t, sh)); t += sh[3] if sh[1] == "vid" else slot
    return out, slot, len(shots)


def cover_1080(src, dst, do_grade):
    im = Image.open(src).convert("RGB"); W, H = im.size
    tw, th = W, int(round(W * 9 / 16))
    if th > H: th, tw = H, int(round(H * 16 / 9))
    x0, y0 = (W - tw) // 2, (H - th) // 2
    im = im.crop((x0, y0, x0 + tw, y0 + th)).resize((1920, 1080), Image.LANCZOS)
    im.save(dst, quality=93)
    if do_grade: grade(str(dst))


PX_CACHE = {}
def px_original(key):
    pid = PX[key]; dst = REAL / f"px_{key}_{pid}.jpg"
    if dst.exists(): return dst, PX_CACHE.get(pid)
    rr = requests.get(f"https://api.pexels.com/v1/photos/{pid}", headers={"Authorization": PEXELS_KEY}, timeout=60)
    r = rr.json() if rr.status_code == 200 else {}
    if "src" in r:
        url = r["src"].get("original") or r["src"]["large2x"]
        dst.write_bytes(requests.get(url, timeout=180).content); time.sleep(0.4)
        PX_CACHE[pid] = (r.get("photographer", ""), r.get("url", ""))
    else:
        cands = list(PXC.glob(f"*__{pid}.jpg"))
        if not cands: raise SystemExit(f"[LOI] Pexels {key}={pid}: {rr.status_code} {rr.text[:80]} va khong co ban candidate")
        shutil.copy2(cands[0], dst); print(f"  [CANH BAO] Pexels {key}={pid} API {rr.status_code} -> dung ban large 940px")
        PX_CACHE[pid] = ("", f"https://www.pexels.com/photo/{pid}/")
    return dst, PX_CACHE[pid]


def main():
    lines = content_lines(TTS.read_text(encoding="utf-8")); starts, ends, total = line_starts(lines)
    assert len(lines) == 106, f"TTS co {len(lines)} dong noi dung, SECTION_RANGES viet cho 106 — kiem lai truoc khi build"
    IMG.mkdir(exist_ok=True); CLIPS.mkdir(exist_ok=True)
    for f in list(IMG.glob("slide_*.jpg")) + list(CLIPS.glob("clip_*.mp4")): f.unlink()

    # 🔴 GATE: moi asset dung DUNG 1 lan trong video
    refs = [(sh[1], sh[2] if sh[1] != "ai" else sh[0]) for sec in SHOTS.values() for sh in sec]
    dup = {r for r in refs if refs.count(r) > 1}
    if dup: print("[LOI] asset dung 2 lan trong video:", dup); sys.exit(1)

    entries, report = [], []
    for sec, (a, b) in SECTION_RANGES.items():
        ws, we = starts[a], (starts[b] if b < len(starts) else total)
        placed, slot, kept = place_section(SHOTS[sec], ws, we)
        report.append(f"   {sec:7} {we-ws:6.1f}s  slot={slot:4.1f}s  giu {kept}/{len(SHOTS[sec])}")
        entries += [(t, sh, sec) for t, sh in placed]
    entries.sort(key=lambda x: x[0])

    slides, flow, names, att_px, err = [], [], [], {}, 0
    cnt = {"vid": 0, "st": 0, "cc": 0, "px": 0, "ai": 0}
    for t, sh, sec in entries:
        name, kind, ref = sh[0], sh[1], sh[2]
        idx, off = find_line_and_offset(t, starts, ends); m = uniq_match(lines, idx)
        pos = len(slides); ent = {"match": m}
        if off: ent["offset"] = off
        if kind == "vid":
            ent.update(video=True, source=f"footage_raw/{ref}.mp4", dur=sh[3])
            src = FOOTAGE / f"{ref}.mp4"
            if src.exists():
                dst = CLIPS / f"clip_{pos:02d}.mp4"
                try: os.link(src, dst)
                except Exception: shutil.copy2(src, dst)
            else: print(f"[CANH BAO] thieu clip {ref}"); err += 1
        elif kind in ("st", "cc", "px"):
            ent["photo"] = True
            if kind == "px":
                src, meta = px_original(ref); att_px[ref] = (PX[ref], meta)
            else:
                cands = list(REAL.glob(f"{ref}.*"))
                if not cands: print(f"[LOI] thieu anh that {ref}"); err += 1; continue
                src = cands[0]
            ent["source"] = f"real_photos/{src.name}"; ent["kind"] = {"st": "still-film", "cc": "commons", "px": "pexels"}[kind]
            cover_1080(src, IMG / f"slide_{pos:02d}.jpg", do_grade=(kind != "st"))
        else:
            preset, desc = ref
            ent.update(photo=True, source=f"slides_img/slide_{pos:02d}.jpg (AI CAN GEN — xem scene_prompts_FLOW.txt)", kind="ai")
            flow.append(f"{desc}, {PRESET[preset]}, {LOCK}. {AVOID}")
        cnt[kind] += 1; slides.append(ent)
        names.append(f"slide_{pos:03d}_{name}  [{kind}]  (t~{t:.1f}s, {sec}, offset={off}s)")

    if not slides or not slides[0].get("video"):
        print("[LOI] ENTRY 0 KHONG PHAI CLIP PHIM THAT — cold open showa bat buoc clip that o giay 0"); err += 1
    seen = set()
    for s_ in slides:
        k = (s_["match"], s_.get("offset", 0.0))
        if k in seen: print("[LOI] trung match+offset", k); err += 1
        seen.add(k)
    if err: print(f"\n[X] {err} loi — KHONG ghi"); sys.exit(1)

    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (VD / "scene_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "scene_prompts_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    (VD / "scene_prompts_AI_SLOTS.txt").write_text("\n".join(n for n in names if "[ai]" in n) + "\n", encoding="utf-8")
    with open(VD / "ATTRIBUTIONS_pexels.md", "w", encoding="utf-8") as f:
        f.write("# Pexels — video 08 (license Pexels: thuong mai OK, khong bat buoc credit; ghi de tra nguon)\n\n| key | id | photographer | url |\n|---|---|---|---|\n")
        for k, (pid, meta) in sorted(att_px.items()):
            ph, url = meta or ("", f"https://www.pexels.com/photo/{pid}/")
            f.write(f"| {k} | {pid} | {ph} | {url} |\n")
    n = len(slides); vid_sec = sum(sh[3] for _, sh, _ in entries if sh[1] == "vid")
    print(f"OK {n} entry -> {OUT_JSON.name}   ({total:.0f}s = {int(total)//60}:{int(total)%60:02d}, {total/n:.1f}s/khung)")
    print("\n".join(report))
    real = cnt["vid"] + cnt["st"] + cnt["cc"] + cnt["px"]
    print(f"   clip THAT {cnt['vid']} ({vid_sec:.0f}s={vid_sec/total*100:.0f}%) | still phim {cnt['st']} | Commons {cnt['cc']} | Pexels {cnt['px']} | AI {cnt['ai']} = {cnt['ai']/n*100:.0f}%")
    print(f"   THAT {real}/{n} = {real/n*100:.0f}%")


if __name__ == "__main__":
    main()
