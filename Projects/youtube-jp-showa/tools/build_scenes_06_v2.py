# -*- coding: utf-8 -*-
"""build_scenes_06_v2.py — video 06 (shokyu-kakeibo) — BAN 2: REAL-FIRST, AI chi lap <=20%.

User chot 2026-08-29 (A+B): "khong muon dung anh AI nua" -> uu tien THAT, AI chi cho canh khong co
nguon that (ky tuc xa ben trong, 集団就職 sinh hoat), van tick synthetic.

4 nguon THAT + 1 nguon AI, moi shot mot kind:
  vid  clip phim CC0 (footage_raw/, cat bang cut_archival.py, da ghi so den)         17
  st   ANH TINH cat tu chinh phim CC0 (real_photos/st06_*.jpg, grab_stills.py)          ~40
  cc   Wikimedia Commons PD/CC (real_photos/cc_*.jpg — tien giay 1963-69 PD, 銭湯 一の湯,
       rap 小倉昭和館, ケロリン, ちゃぶ台 ...) — credit o ATTRIBUTIONS_commons.md            ~18
  px   Pexels — VAT TRUNG TINH khong lo nam (xu, phong bi, bat, voi dong, dong ho...)   ~45
       da duyet mat tren _px_candidates/sheet_*.jpg; tai lai ban ORIGINAL khi build
  ai   <=20% tong khung, chi cho canh khong the co nguon that                            <=25

Script tu: tinh timeline theo ky tu (RATE) -> chia deu slot ~6s -> COPY/CROP anh that vao
slides_img/slide_NNN.jpg (1920x1080 cover-crop; px/cc qua grade_vintage cho cung tong) -> SLIDES.json
-> FLOW.txt chi con prompt AI -> ATTRIBUTIONS.md (Commons + Pexels).
"""
import io, sys, re, json, shutil, time
from pathlib import Path
import requests
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grade_vintage import grade  # noqa: E402

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "06_shokyu-kakeibo_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "06_shokyu-kakeibo_SLIDES.json"
VD = ROOT / "06_VIDEO" / "06_shokyu-kakeibo"
REAL = VD / "real_photos"; IMG = VD / "slides_img"; CLIPS = VD / "clips"; FOOTAGE = VD / "footage_raw"
PXC = VD / "_px_candidates"
RATE = 3.983
PEXELS_KEY = (ROOT.parent / "youtube-jp-health" / "tools" / ".pexels_key").read_text(encoding="utf-8").strip()

LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, "
        "soft natural light, gentle film grain, slight vignette, nostalgic documentary photography, "
        "muted greens and ochres, natural imperfect framing, 16:9")
PRESET = {
    "dorm": ("inside a 1970 Japanese company dormitory, narrow wooden corridor, thin plaster walls, "
             "three-mat tatami rooms, one bare bulb, still dusty air, no street and no sky in frame"),
    "office": ("a small 1970 Japanese company office, grey steel desks, stacked paper ledgers, a frosted "
               "glass partition, worn linoleum floor, no street and no sky in frame"),
    "postoffice": ("inside a small Showa post office, a long wooden counter, a wire mesh screen at the "
                   "window, worn linoleum floor, no street and no sky in frame"),
    "furusato": ("a rural Japanese farmhouse around 1970, tatami room, a low table by a paper screen "
                 "window, muted country daylight, no city and no asphalt in frame"),
}
AVOID = ("no watermark, no logo, no signature, no sparkle mark. Avoid: modern objects, smartphones, LED lights, "
         "plastic bottles, air conditioner, modern clothing, sneakers with logos, readable text or signage, "
         "brand logos, western faces, anime style, oversaturated HDR look, close-up faces.")

SECTION_RANGES = {
    "cold": (0, 4), "intro": (4, 8), "item1": (8, 13), "item2": (13, 19), "item3": (19, 25),
    "item4": (25, 30), "item5": (30, 34), "cta": (34, 35), "item6": (35, 41), "item7": (41, 46),
    "item8": (46, 50), "item9": (50, 55), "item10": (55, 63), "watch": (63, 67), "ending": (67, 72),
}

# Pexels picks (duyet mat 2026-08-29 tren _px_candidates/sheet_*.jpg). key -> id
PX = {
    "envelope_kraft_hold": 5899171, "envelope_open_hand": 7390817, "envelope_desk": 5712451, "envelope_string": 8250811,
    "ashtray_a": 9565888, "ashtray_b": 28747786,
    "noodles_lift_a": 1395319, "noodles_lift_b": 36964057,
    "match_a": 34934581, "match_b": 6496361, "match_c": 6496368,
    "curtain_a": 6899765, "curtain_b": 35836715,
    "seats_a": 7991381, "seats_b": 7991489, "seats_c": 7991231, "seats_old": 6198785,
    "coffee_red": 6207309, "coffee_dark": 15697027, "coffee_top": 8249580,
    "station_night_a": 33390911, "station_night_b": 30258210,
    "corridor_dark": 5745572, "wood_interior": 31218428, "old_street_a": 7526814, "old_street_b": 5392369,
    "drawer_papers": 16514852, "drawers_wall": 5273174, "drawer_c": 11105148,
    "tatami_dark": 35680939, "tatami_sun": 31355891, "tatami_c": 33097432, "irori_light": 2187966, "tatami_open": 5220089,
    "kissaten_dark": 16781258, "kissaten_b": 34654509, "kissaten_window_a": 31692598, "kissaten_window_b": 31692607,
    "letter_write": 5425602, "letter_write_b": 7333509, "ramen_c": 6646067, "night_street_lantern_b": 31640564, "letter_hold": 3826667,
    "photos_bw_stack": 37947884, "cards_pile": 3235029,
    "night_street_a": 33469141, "night_street_lantern": 30209211, "night_street_c": 30037331, "night_street_d": 36580122,
    "projector_lens": 5515483, "projector_b": 13019528, "projector_reel": 34084909,
    "radio_dial": 3098, "radio_b": 5161816, "radio_c": 37620872,
    "ramen_shoyu": 5649309, "ramen_b": 6645920,
    "yatai_lanterns": 7107238, "yatai_dark": 20250944, "yatai_c": 33061228,
    "record_wood": 35279502, "record_bw": 714530,
    "sacks_stacked": 12293641, "sacks_store": 30688218,
    "faucet_brass_tile": 6653903, "faucet_b": 7746104, "tiled_row": 29017467,
    "sewing_a": 5030573, "sewing_b": 29222239, "sewing_c": 27893061,
    "smoke_silhouette": 8780929, "smoke_b": 36210489, "streetlight_fog": 9266927,
    "stamps_desk": 18687845, "stamp_box": 3838319,
    "tea_a": 38643042, "tea_b": 6713234, "tea_pickers": 13760478,
    "watchshop_a": 37235235, "watch_repair_bw": 34619339, "watchshop_c": 2029594,
    "watch_leather": 8327544, "watch_hands": 6328850, "watch_c": 13028361, "watches_row": 30094119,
}

# ---------------------------------------------------------------------------
# SHOTS: (name, kind, ref[, dur])  kind: vid | st | cc | px | ai
#   vid ref = ten clip trong footage_raw (dur giay that)
#   st  ref = ten file trong real_photos (st06_*)
#   cc  ref = ten file trong real_photos (cc_*), khong duoi
#   px  ref = key trong PX
#   ai  ref = (preset, prompt)
# ⭐ entry 0 = chu the (phong bi luong) — media-library §2.0
# ---------------------------------------------------------------------------
SHOTS = {
"cold": [
    ("jt06_01_crowd_toward", "vid", "jt06_01_crowd_toward", 8),   # GIAY 0 = CLIP THAT (luat kenh)
    ("envelope_kraft_hold", "px", "envelope_kraft_hold"),
    ("envelope_open_hand", "px", "envelope_open_hand"),
],
"intro": [
    ("jt06_02_tokyo_skyline", "vid", "jt06_02_tokyo_skyline", 10),
    ("st06_13_crowd_walking", "st", "st06_13_crowd_walking"),
    ("envelope_desk", "px", "envelope_desk"),
    ("jt06_03_ginza_district", "vid", "jt06_03_ginza_district", 9),
    ("cc_coin_10yen", "cc", "cc_coin_10yen"),
    ("st06_16_globe_building", "st", "st06_16_globe_building"),
    ("st06_14_crowd_business", "st", "st06_14_crowd_business"),
    ("envelope_string", "px", "envelope_string"),
],
"item1": [
    ("cc_note_1000yen", "cc", "cc_note_1000yen_seriesC_front"),
    ("st06_22_young_men_crowd", "st", "st06_22_young_men_crowd"),
    ("jt06_04_office_street", "vid", "jt06_04_office_street", 8),
    ("ai_office_desks", "ai", ("office", "wide shot of a row of grey steel desks in a small company office, stacked ledgers and a wooden abacus on one desk, no people in frame")),
    ("st06_23_young_men_b", "st", "st06_23_young_men_b"),
    ("cc_note_10000yen", "cc", "cc_note_10000yen_seriesC_front"),
    ("cc_note_500yen", "cc", "cc_note_500yen_seriesC_front"),
    ("st06_24_man_hat_crowd", "st", "st06_24_man_hat_crowd"),
    ("radio_dial", "px", "radio_dial"),
    ("cc_note_5000yen", "cc", "cc_note_5000yen_seriesC_front"),
],
"item2": [
    ("st06_01_boy_train_window", "st", "st06_01_boy_train_window"),
    ("jt06_05_young_workers", "vid", "jt06_05_young_workers", 6),
    ("st06_02_boy_train_window_b", "st", "st06_02_boy_train_window_b"),
    ("ai_dorm_room_futon", "ai", ("dorm", "wide shot of a three-mat tatami room with a folded futon, a small round mirror on the wall and a wicker trunk in the corner, one bare bulb, no people in frame")),
    ("tatami_dark", "px", "tatami_dark"),
    ("jt06_06_plaza_crossing", "vid", "jt06_06_plaza_crossing", 12),
    ("ai_dorm_corridor", "ai", ("dorm", "wide shot of a narrow dormitory corridor with two plain wooden doors facing each other, one bare bulb overhead, no people in frame")),
    ("radio_b", "px", "radio_b"),
    ("jt06_09_shoten_street_day", "vid", "jt06_09_shoten_street_day", 7),
    ("corridor_dark", "px", "corridor_dark"),
    ("night_street_a", "px", "night_street_a"),
],
"item3": [
    ("night_street_lantern", "px", "night_street_lantern"),
    ("cc_sento_ichinoyu_01", "cc", "cc_sento_ichinoyu_01"),
    ("cc_kerorin_bathpail", "cc", "cc_kerorin_bathpail"),
    ("faucet_brass_tile", "px", "faucet_brass_tile"),
    ("cc_sento_ichinoyu_03", "cc", "cc_sento_ichinoyu_03"),
    ("tiled_row", "px", "tiled_row"),
    ("cc_sento_ichinoyu_04", "cc", "cc_sento_ichinoyu_04"),
    ("faucet_b", "px", "faucet_b"),
    ("ai_sento_steam_ceiling", "ai", ("dorm", "wide shot of steam drifting under the high wooden ceiling of a Showa public bathhouse, soft light through a high window, pale tiles below, no people in frame")),
    ("night_street_c", "px", "night_street_c"),
    ("st06_44_street_bus", "st", "st06_44_street_bus"),
],
"item4": [
    ("st06_34_market_stalls_a", "st", "st06_34_market_stalls_a"),
    ("cc_chabudai", "cc", "cc_chabudai"),
    ("jt06_07_taue", "vid", "jt06_07_taue", 12),
    ("cc_kitchen_showa", "cc", "cc_kitchen_showa"),
    ("st06_36_ox_plough", "st", "st06_36_ox_plough"),
    ("jt06_08_ine_drying", "vid", "jt06_08_ine_drying", 10),
    ("sacks_stacked", "px", "sacks_stacked"),
    ("st06_37_rice_planting_still", "st", "st06_37_rice_planting_still"),
    ("sacks_store", "px", "sacks_store"),
],
"item5": [
    ("night_street_d", "px", "night_street_d"),
    ("ramen_shoyu", "px", "ramen_shoyu"),
    ("st06_08_street_signs_a", "st", "st06_08_street_signs_a"),
    ("night_street_lantern_b", "px", "night_street_lantern_b"),
    ("noodles_lift_a", "px", "noodles_lift_a"),
    ("ramen_c", "px", "ramen_c"),
    ("noodles_lift_b", "px", "noodles_lift_b"),
    ("yatai_c", "px", "yatai_c"),
],
"cta": [
    ("jt06_10_ongakukai_crowd", "vid", "jt06_10_ongakukai_crowd", 9),
    ("st06_17_audience_a", "st", "st06_17_audience_a"),
    ("st06_18_audience_b", "st", "st06_18_audience_b"),
    ("st06_19_women_crowd", "st", "st06_19_women_crowd"),
    ("st06_42_families_crowd_a", "st", "st06_42_families_crowd_a"),
    ("st06_43_families_crowd_b", "st", "st06_43_families_crowd_b"),
],
"item6": [
    ("cc_kariya_cinema_showa20s", "cc", "cc_kariya_cinema_showa20s"),
    ("jt06_11_depaato_welcome", "vid", "jt06_11_depaato_welcome", 9),
    ("seats_b", "px", "seats_b"),
    ("seats_old", "px", "seats_old"),
    ("jt06_12_crowd_dense", "vid", "jt06_12_crowd_dense", 8),
    ("curtain_a", "px", "curtain_a"),
    ("projector_lens", "px", "projector_lens"),
    ("seats_a", "px", "seats_a"),
    ("curtain_b", "px", "curtain_b"),
    ("st06_15_department_store", "st", "st06_15_department_store"),
],
"item7": [
    ("match_a", "px", "match_a"),
    ("smoke_silhouette", "px", "smoke_silhouette"),
    ("match_b", "px", "match_b"),
    ("ashtray_a", "px", "ashtray_a"),
    ("streetlight_fog", "px", "streetlight_fog"),
    ("station_night_b", "px", "station_night_b"),
    ("ashtray_b", "px", "ashtray_b"),
],
"item8": [
    ("st06_25_shirobasha_sign_a", "st", "st06_25_shirobasha_sign_a"),
    ("jt06_13_tearoom_men", "vid", "jt06_13_tearoom_men", 8),
    ("coffee_red", "px", "coffee_red"),
    ("coffee_top", "px", "coffee_top"),
    ("st06_26_shirobasha_sign_b", "st", "st06_26_shirobasha_sign_b"),
    ("record_wood", "px", "record_wood"),
    ("coffee_dark", "px", "coffee_dark"),
],
"item9": [
    ("envelope_kraft_hold", "px", "envelope_kraft_hold"),
    ("ai_registered_envelope", "ai", ("postoffice", "close-up of a small stiff paper envelope with a thin red border lying on a wooden counter, warm light, the envelope completely blank")),
    ("letter_write", "px", "letter_write"),
    ("jt06_14_chatsumi", "vid", "jt06_14_chatsumi", 12),
    ("envelope_string", "px", "envelope_string"),
    ("tea_pickers", "px", "tea_pickers"),
    ("jt06_15_wara_stacks", "vid", "jt06_15_wara_stacks", 9),
    ("irori_light", "px", "irori_light"),
    ("stamps_desk", "px", "stamps_desk"),
    ("ai_post_counter", "ai", ("postoffice", "wide shot of a small post office counter with a wire mesh screen and a worn linoleum floor, no people in frame")),
    ("sewing_a", "px", "sewing_a"),
    ("tatami_sun", "px", "tatami_sun"),
],
"item10": [
    ("cc_coin_10yen", "cc", "cc_coin_10yen"),
    ("envelope_desk", "px", "envelope_desk"),
    ("ai_notebook_columns", "ai", ("dorm", "close-up of an old ruled household account notebook open on a low table showing faint pencil column lines, the writing softly blurred and illegible, warm light")),
    ("jt06_16_ekimae_plaza", "vid", "jt06_16_ekimae_plaza", 9),
    ("cc_note_1000yen", "cc", "cc_note_1000yen_seriesC_front"),
    ("ai_passbook_open", "ai", ("postoffice", "close-up of a small savings passbook lying open on a wooden counter, the printed lines softly blurred and illegible, warm light")),
    ("stamp_box", "px", "stamp_box"),
    ("jt06_17_street_walk", "vid", "jt06_17_street_walk", 12),
    ("st06_39_station_plaza_a", "st", "st06_39_station_plaza_a"),
    ("st06_40_station_plaza_b", "st", "st06_40_station_plaza_b"),
    ("ai_two_passbooks", "ai", ("dorm", "close-up of two small savings passbooks lying side by side on a low table, warm bulb light, both covers completely plain")),
    ("st06_41_street_dept", "st", "st06_41_street_dept"),
],
"watch": [
    ("watchshop_a", "px", "watchshop_a"),
    ("watch_leather", "px", "watch_leather"),
    ("watch_repair_bw", "px", "watch_repair_bw"),
    ("watch_hands", "px", "watch_hands"),
],
"ending": [
    ("envelope_open_hand", "px", "envelope_open_hand"),
    ("tatami_c", "px", "tatami_c"),
    ("drawers_wall", "px", "drawers_wall"),
    ("drawer_papers", "px", "drawer_papers"),
    ("watch_c", "px", "watch_c"),
    ("st06_45_boy_camera", "st", "st06_45_boy_camera"),
    ("photos_bw_stack", "px", "photos_bw_stack"),
    ("st06_46_schoolkids", "st", "st06_46_schoolkids"),
    ("tatami_open", "px", "tatami_open"),
],
}

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
        # bo dan: AI truoc, roi px (that nhung trung tinh) — khong bao gio bo clip/still/cc
        for k in ("ai", "px"):
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
        # id loi/404 -> dung ban 'large' da tai luc duyet (940px, se upscale ~2x — ghi canh bao)
        cands = list(PXC.glob(f"*__{pid}.jpg"))
        if not cands: raise SystemExit(f"[LOI] Pexels {key}={pid}: {rr.status_code} {rr.text[:80]} va khong co ban candidate")
        shutil.copy2(cands[0], dst); print(f"  [CANH BAO] Pexels {key}={pid} API {rr.status_code} -> dung ban large 940px")
        PX_CACHE[pid] = ("", f"https://www.pexels.com/photo/{pid}/")
    return dst, PX_CACHE[pid]


def main():
    lines = content_lines(TTS.read_text(encoding="utf-8")); starts, ends, total = line_starts(lines)
    IMG.mkdir(exist_ok=True); CLIPS.mkdir(exist_ok=True)
    for f in list(IMG.glob("slide_*.jpg")) + list(CLIPS.glob("clip_*.mp4")): f.unlink()

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
                try: __import__("os").link(src, dst)
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
            ent["source"] = f"real_photos/{src.name}"; ent["kind"] = {"st": "still-1959", "cc": "commons", "px": "pexels"}[kind]
            cover_1080(src, IMG / f"slide_{pos:02d}.jpg", do_grade=(kind != "st"))
        else:
            preset, desc = ref
            ent.update(photo=True, source=f"slides_img/slide_{pos:02d}.jpg (AI CAN GEN — xem scene_prompts_FLOW.txt)", kind="ai")
            flow.append(f"{desc}, {PRESET[preset]}, {LOCK}. {AVOID}")
        cnt[kind] += 1; slides.append(ent)
        names.append(f"slide_{pos:03d}_{name}  [{kind}]  (t~{t:.1f}s, {sec}, offset={off}s)")

    # 🔴 LUAT KENH showa (user nhac nhieu lan, vi pham 2 lan o video 06): ENTRY 0 PHAI LA CLIP PHIM THAT.
    # De len media-library §2.0 (anh chu the) — luat kenh cu the hon thi thang.
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
    ai_slots = [n for n in names if "[ai]" in n]
    (VD / "scene_prompts_AI_SLOTS.txt").write_text("\n".join(ai_slots) + "\n", encoding="utf-8")
    with open(VD / "ATTRIBUTIONS_pexels.md", "w", encoding="utf-8") as f:
        f.write("# Pexels — video 06 (license Pexels: thuong mai OK, khong bat buoc credit; ghi de tra nguon)\n\n| key | id | photographer | url |\n|---|---|---|---|\n")
        for k, (pid, meta) in sorted(att_px.items()):
            ph, url = meta or ("", f"https://www.pexels.com/photo/{pid}/")
            f.write(f"| {k} | {pid} | {ph} | {url} |\n")
    n = len(slides); vid_sec = sum(sh[3] for _, sh, _ in entries if sh[1] == "vid")
    print(f"OK {n} entry -> {OUT_JSON.name}   ({total:.0f}s = {int(total)//60}:{int(total)%60:02d}, {total/n:.1f}s/khung)")
    print("\n".join(report))
    real = cnt["vid"] + cnt["st"] + cnt["cc"] + cnt["px"]
    print(f"   clip THAT {cnt['vid']} ({vid_sec:.0f}s={vid_sec/total*100:.0f}%) | still 1959 {cnt['st']} | Commons {cnt['cc']} | Pexels {cnt['px']} | AI {cnt['ai']} = {cnt['ai']/n*100:.0f}%")
    print(f"   THAT {real}/{n} = {real/n*100:.0f}%")


if __name__ == "__main__":
    main()
