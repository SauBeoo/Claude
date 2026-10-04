# -*- coding: utf-8 -*-
"""build_scenes_07.py -- video 07 (kieta-oto), REAL-FIRST, ~10s/khung (chua dat 7s user muon)

Ket qua cuoi (2026-08-31, sau khi soi 1:1 va loai 8/15 anh nhiem yeu to hien dai/sai
quoc gia -- xem 03_SCRIPTS/07_kieta-oto.md muc "LOP HINH"):
  vid  1 doan phim that (sumo, japan_today_1959 @2136s, da cat + ghi so den 07_kieta-oto)
  cc   8 anh Commons PD/CC con lai: kamishibai box, hyoshigi (x2), washboard, furin,
       shoe_locker -- hyoshigi chi co ban 400x400 do rate-limit 429, can fetch lai full-res
  px   5 anh Pexels con lai: cicada, dusk sky (x2), ice block, ice shards
  ai   81 = 85% tong khung -- VUOT xa tran 20% cua CLAUDE.md Visual. Nguyen nhan: (1) chu
       de qua hep, kho phim CC0 khong co canh nghe rong (2) 8 anh ban dau (kamishibai
       performer, chindonya, bicycle bell, newspaper bundle, locomotive, bathhouse tile,
       alley night) deu lo yeu to hien dai/sai quoc gia khi soi full-res, phai thay bang AI

User can quyet 1 trong 3 phuong an truoc khi gen anh -- xem file .md.
"""
import io, sys, re, json, shutil
from pathlib import Path
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "07_kieta-oto_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "07_kieta-oto_SLIDES.json"
VD = ROOT / "06_VIDEO" / "07_kieta-oto"
REAL = VD / "real_photos"; IMG = VD / "slides_img"; CLIPS = VD / "clips"; FOOTAGE = VD / "footage_raw"
RATE = 3.983

LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, "
        "soft natural light, gentle film grain, slight vignette, nostalgic documentary photography, "
        "muted greens and ochres, natural imperfect framing, 16:9")
AVOID = ("no watermark, no logo, no signature, no sparkle mark. Avoid: modern objects, smartphones, LED lights, "
         "plastic bottles, air conditioner, modern clothing, sneakers with logos, readable text or signage, "
         "brand logos, western faces, anime style, oversaturated HDR look, close-up faces.")

SECTION_RANGES = {
    "cold": (0, 3), "hook": (3, 6), "item2": (6, 10), "item3": (10, 14), "item4": (14, 19),
    "item5": (19, 23), "item6": (23, 28), "item7cta": (28, 34), "item8": (34, 38),
    "item9": (38, 43), "item10": (43, 47), "item11": (47, 51), "item12": (51, 55),
    "item13": (55, 59), "item14": (59, 63), "item15": (63, 72), "ending": (72, 76),
}

# name, kind(vid|cc|px|ai), ref[, dur nếu vid]
SHOTS = {
"cold": [
    ("kamishibai_box", "cc", "cc_kamishibai_box"),
    ("hyoshigi_prop", "cc", "cc_hyoshigi"),
    ("kamishibai_performer_ai", "ai", "an elderly Japanese man in a simple happi coat and straw hat standing beside a wooden kamishibai story-telling box mounted on the back of a bicycle, on a quiet residential street, no readable text, no modern signage, no faces visible, soft daylight"),
],
"hook": [
    ("kitchen_hands_chop", "ai", "close-up of a woman's hands chopping vegetables on a low wooden kitchen counter near a window, her face out of frame, a pot with rising steam nearby, warm midday light"),
    ("kitchen_window_light", "ai", "wide shot of a small 1970 Japanese home kitchen, morning light through a frosted glass window, a kettle on a gas stove, no people in frame"),
    ("street_residential_day", "ai", "wide shot of a quiet Japanese residential back-street at midday, narrow paved lane between low wooden houses, laundry hanging on a pole outside one window, no people in frame"),
    ("engawa_empty", "ai", "a small wooden engawa porch of a Japanese house, sliding paper doors half open, a pair of straw sandals by the step, soft afternoon light, no people in frame"),
    ("kitchen_pot_steam", "ai", "close-up of a pot gently steaming on a gas stove in a small 1970 Japanese kitchen, a wooden ladle resting beside it, no people in frame"),
    ("kitchen_window_glance", "ai", "medium shot from inside a small 1970 Japanese kitchen looking toward a frosted window, a woman's silhouette pausing to glance outside, face out of frame, soft midday light"),
    ("laundry_pole_closeup", "ai", "close-up of laundry hanging to dry on a bamboo pole outside a Japanese house window, gentle breeze, soft daylight, no people in frame"),
    ("street_residential_day_alt", "ai", "wide shot of a narrow Japanese residential alley at midday from a slightly different angle, low wooden fences, a bicycle leaning against a wall, no people in frame"),
],
"item2": [
    ("newspaper_stack", "px", "px_newspaper_stack"),
    ("recycling_truck_wide", "ai", "a small flatbed truck with a hand-painted loudspeaker horn on its roof, parked on a narrow residential street, bundles of old newspapers stacked on the truck bed, no people in frame"),
    ("recycling_truck_close", "ai", "close-up of an old megaphone loudspeaker mounted on a small truck roof, weathered metal, residential street blurred behind it"),
    ("bicycle_bell_ai_a", "ai", "close-up of a simple chrome bicycle handlebar bell with a plain unmarked dome, no text or engraving, weathered metal, soft daylight"),
    ("street_residential_day_b", "ai", "wide shot of a quiet Japanese residential street corner at midday, wooden utility pole, a bicycle leaning against a wall, no people in frame"),
    ("newspaper_bundle_close", "ai", "close-up of stacks of old bundled newspapers and magazines tied with straw string, sitting on a wooden doorstep, soft daylight, no people in frame"),
    ("tissue_packets_hand", "ai", "close-up of a small stack of plain tissue paper packets held in two hands, soft daylight, no face visible"),
    ("street_corner_wide", "ai", "wide shot of a quiet Japanese neighborhood street corner at midday, a small wooden signpost, utility wires overhead, no people in frame"),
],
"item3": [
    ("bamboo_pole_bicycle_wide", "ai", "an old bicycle loaded with many long bamboo poles tied along the frame and rear rack, parked on a quiet residential street, no rider in frame, weathered wood and metal, soft afternoon light"),
    ("bamboo_pole_bicycle_close", "ai", "close-up of bamboo poles bundled and tied with rope on the back rack of an old bicycle, texture of weathered bamboo, soft daylight"),
    ("bicycle_bell_ai_b", "ai", "close-up of a small chrome bell mounted on rusted bicycle handlebars, plain unmarked surface, soft afternoon light"),
    ("window_face_glance", "ai", "a Japanese house window with wooden shutters half open, a curtain moving slightly as if someone glanced out, no face visible, soft daylight"),
    ("laundry_pole_leaning_wall", "ai", "a few unused bamboo poles leaning against a wooden garden wall, soft afternoon light, no people in frame"),
],
"item4": [
    ("pongashi_vacant_lot", "ai", "wide shot of a small vacant lot in a Japanese neighborhood, a simple wooden stall and a cart, midday sun, no people in frame"),
    ("pongashi_cannon_wide", "ai", "a blackened iron cylinder puffed-rice cannon resting over glowing charcoal embers on a simple cart, wisps of steam rising, outdoor vacant lot setting, no people in frame"),
    ("pongashi_cannon_close", "ai", "close-up of a blackened iron puffed-rice cannon with a hand crank, glowing embers underneath, steam curling upward, no people in frame"),
    ("pongashi_children_watching", "ai", "a small group of Japanese children standing a few steps back with their hands over their ears, waiting, seen from behind, no faces visible, a street vendor cart blurred in front of them"),
    ("pongashi_steam_burst", "ai", "a sudden burst of white steam and puffed rice scattering in the air above an iron cannon cart, motion blur, soft daylight, no people in frame"),
    ("pongashi_smell_closeup", "ai", "close-up of freshly puffed rice grains scattered on a wooden tray, faint steam rising, soft daylight"),
],
"item5": [
    ("ice_block", "px", "px_ice_block"),
    ("ice_shards", "px", "px_ice_shards"),
    ("ice_saw_action", "ai", "close-up of a large block of clear ice being cut with a hand saw on a wooden ice-shop counter, saw teeth biting into the ice, small ice shavings scattered on the wet wooden surface, hands and forearms only, no face visible"),
    ("ice_shop_storefront", "ai", "a small old-fashioned ice shop storefront with a wooden sliding door half open, a block of ice visible just inside, soft daylight, no people in frame"),
],
"item6": [
    ("washboard_tub", "cc", "cc_washboard"),
    ("idobata_laundry_women", "ai", "a small group of Japanese women in simple house dresses gathered around wash tubs at a communal well, seen from behind or at a distance, no faces visible, laundry hanging on lines nearby, midday light"),
    ("tarai_closeup_b", "ai", "close-up of a wooden washtub and ridged washboard with wet cloth being scrubbed, water droplets, soft daylight, no people in frame"),
    ("well_pump", "cc", "cc_well_pump"),
    ("laundry_line_courtyard", "ai", "wide shot of a small residential courtyard with several lines of laundry drying, wash tubs stacked to one side, soft midday light, no people in frame"),
],
"item7cta": [
    ("chindonya_group", "ai", "a Japanese street performer in colourful traditional costume with white kabuki-style stage makeup, playing a hand drum mounted on a decorated wooden frame, close side profile, no modern clothing or bystanders visible, no readable text, soft daylight"),
    ("chindonya_parade_wide", "ai", "a trio of Japanese street performers in colourful traditional costume playing a drum, gong and clarinet, walking down a narrow shopping street, a small crowd of onlookers, no readable signage, soft daylight"),
    ("chindonya_drum_close", "ai", "close-up of a hand striking a traditional drum worn by a street performer in colourful costume, motion blur on the drumstick, soft daylight"),
    ("shopping_street_bunting", "ai", "a small Japanese shopfront decorated with colourful paper bunting and a hand-painted opening banner, no readable text, narrow street, soft daylight"),
    ("children_following_parade", "ai", "a small group of Japanese children in simple clothes walking together down a narrow street, seen from behind, following unseen music, no faces visible, soft daylight"),
    ("shopping_street_wide", "ai", "wide shot of a narrow Japanese shopping street lined with small wooden shopfronts, awnings, no readable signage, soft daylight, no people in frame"),
    ("chindonya_clarinet_close", "ai", "close-up of a hand playing a clarinet, colourful traditional costume sleeve visible, narrow shopping street blurred behind, soft daylight"),
    ("chindonya_umbrella_prop", "ai", "close-up of a colourful paper parasol and a small gong carried by a street performer, narrow shopping street blurred behind, soft daylight"),
    ("onlookers_watching", "ai", "a small group of Japanese shopkeepers and passersby standing in doorways watching something down the street, seen from behind or at a distance, no faces visible, soft daylight"),
],
"item8": [
    ("cicada_tree", "px", "px_cicada"),
    ("furin_hanging", "cc", "cc_furin"),
    ("afternoon_nap_room", "ai", "a quiet tatami room with a folded futon pillow and a paper sliding door casting dappled afternoon light, no people in frame, soft warm tones"),
    ("tree_canopy_light", "ai", "sunlight filtering through green tree leaves onto a quiet residential lane, dappled shadows, no people in frame"),
    ("cicada_shell_bark", "ai", "close-up of an empty cicada shell clinging to tree bark, soft dappled sunlight, no people in frame"),
    ("eaves_shade_summer", "ai", "close-up of the wooden eaves of a Japanese house casting deep shade on a hot summer afternoon, a bamboo blind rolled halfway down, no people in frame"),
],
"item9": [
    ("yakiimo_cart_wide", "ai", "a wooden two-wheeled cart loaded with roasting sweet potatoes over a small charcoal firebox, steam rising, parked on a sloped residential street at dusk, warm orange light from the fire, no vendor visible"),
    ("yakiimo_cart_close", "ai", "close-up of roasted sweet potatoes nestled in hot stones inside a wooden cart firebox, glowing embers, steam rising, warm orange light"),
    ("yakiimo_potato_split_steam", "ai", "close-up of a roasted sweet potato split in half, steam rising from the bright orange flesh, held in two hands wrapped in newspaper, no face visible"),
    ("dusk_slope_street", "ai", "a quiet Japanese residential street on a gentle slope at dusk, warm orange sky, utility poles, no people in frame"),
    ("dusk_sky_a", "px", "px_dusk_sky"),
    ("child_running_cart", "ai", "a small child running down a sloped residential street at dusk chasing a distant cart, seen from behind, no face visible, warm orange light"),
    ("coins_in_hand", "ai", "close-up of a few small coins held in a child's open palm, soft warm dusk light, no face visible"),
],
"item10": [
    ("dusk_sky_b", "px", "px_dusk_sky"),
    ("utility_pole_speaker", "ai", "close-up of an old public-announcement loudspeaker mounted on a wooden utility pole against a dusk sky, silhouette, no people in frame"),
    ("children_walking_home_silhouette", "ai", "silhouettes of small children walking home together down a quiet street at dusk, warm orange sky behind them, no faces visible"),
    ("window_lamp_glow_dusk", "ai", "a small Japanese house window beginning to glow with warm lamplight against a darkening dusk sky, no people in frame"),
],
"item11": [
    ("bicycle_bell_ai_c", "ai", "close-up of a plain chrome bicycle bell on worn handlebars, no text or logo, residential street blurred behind, soft daylight"),
    ("mail_bicycle", "cc", "cc_mail_bicycle"),
    ("kairanban_board", "ai", "a plain thin wooden clipboard-style community notice board lying closed on a wooden genkan entry step, the cover completely blank with no visible text, soft indoor light"),
    ("genkan_talking_women", "ai", "two Japanese women in simple house dresses standing and talking at a home's front entrance, seen from behind or at a distance, no faces visible, soft daylight"),
    ("wooden_geta_sound_path", "ai", "close-up of a pair of wooden geta sandals walking along a stone garden path toward a house entrance, soft daylight, no face visible"),
],
"item12": [
    ("shoe_locker", "cc", "cc_shoe_locker"),
    ("bathhouse_tile_ai", "ai", "close-up of pale tiled walls inside a Japanese public bathhouse, low wooden stools and a brass faucet row, steam in the air, no people in frame, soft warm light"),
    ("sento_entrance_noren", "ai", "the entrance of a Japanese public bathhouse with a plain fabric noren curtain hanging over the doorway, no readable text on the curtain, soft evening light, no people in frame"),
    ("towel_basket_bathhouse", "ai", "close-up of a small folded towel and a yellow wash basin resting on a wooden bathhouse bench, soft warm light, no people in frame"),
],
"item13": [
    ("steam_locomotive_running", "cc", "cc_locomotive_running"),
    ("alley_kyoto_a", "px", "px_alley_kyoto_a"),
    ("train_platform_dusk", "ai", "a small quiet train station platform at dusk, wooden signal post, no readable signage, no people in frame, warm fading light"),
    ("wet_hair_towel_closeup", "ai", "close-up of a damp towel draped over someone's shoulder, seen from behind, walking down a quiet dusk street, no face visible"),
],
"item14": [
    ("sumo_broadcast", "vid", "jt07_01_sumo_bout", 10),
    ("vintage_radio_ai", "ai", "close-up of a 1970s Japanese tube radio with a simple round tuning dial, no readable text on the dial, warm wood cabinet, soft dim light, no people in frame"),
    ("neighbor_wall_listening", "ai", "a plain thin plaster interior wall of a 1970 Japanese home at dusk, warm lamp light glowing from the other side, no people in frame"),
    ("family_dinner_prep", "ai", "close-up of hands setting simple bowls and chopsticks on a low round dining table in a 1970 Japanese home, warm evening light, no faces visible"),
    ("radio_dial_glow_closeup", "ai", "close-up of a vintage radio dial glowing warmly in a dim room at dusk, soft bokeh, no people in frame"),
],
"item15": [
    ("hyoshigi_night", "cc", "cc_hyoshigi"),
    ("watchman_lantern_wide", "ai", "an elderly man in a dark happi coat walking alone down a narrow unlit residential alley at night, carrying a small paper lantern in one hand and two wooden clappers in the other, seen from behind, no face visible, quiet dark houses on both sides"),
    ("watchman_lantern_close", "ai", "close-up of a hand holding a small glowing paper lantern and a pair of wooden clappers at night, dark alley blurred behind, no face visible"),
    ("alley_kyoto_b", "px", "px_alley_kyoto_b"),
    ("geta_footsteps_closeup", "ai", "close-up of wooden geta sandals on bare feet walking on a dark stone path at night, motion, no face visible, warm lantern light spilling from one side"),
    ("mother_relief_doorway", "ai", "close-up of a woman's hand resting on a wooden sliding door frame at a home entrance at night, warm lamp light from inside, her face out of frame, a quiet sense of relief in her posture"),
    ("watchman_receding_silhouette", "ai", "the small silhouette of an elderly night watchman receding into the distance down a dark narrow alley, a single paper lantern glowing, no face visible"),
    ("front_door_key_closeup", "ai", "close-up of a hand turning an old door latch at a home entrance at night, warm lamp light spilling from inside, no face visible"),
],
"ending": [
    ("kamishibai_box_b", "cc", "cc_kamishibai_box"),
    ("geta_footsteps_closeup_b", "ai", "close-up of wooden geta sandals resting side by side on a wooden genkan step at night, warm lamp light from inside, no people visible"),
    ("dusk_neighborhood_wide", "ai", "a wide quiet view over a small Japanese neighborhood at dusk, tiled rooftops, warm fading sky, no people in frame"),
    ("hyoshigi_prop_ending", "cc", "cc_hyoshigi"),
],
}

IMG_SLOT_MIN = 7.0


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
    vid_total = sum(sh[3] for sh in shots if sh[1] == "vid")
    n_img = sum(1 for sh in shots if sh[1] != "vid")
    slot = (we - ws - vid_total) / n_img if n_img else 0
    out, t = [], ws
    for sh in shots:
        out.append((t, sh)); t += sh[3] if sh[1] == "vid" else slot
    return out, slot, len(shots)


def cover_1080(src, dst):
    im = Image.open(src).convert("RGB"); W, H = im.size
    tw, th = W, int(round(W * 9 / 16))
    if th > H: th, tw = H, int(round(H * 16 / 9))
    x0, y0 = (W - tw) // 2, (H - th) // 2
    im = im.crop((x0, y0, x0 + tw, y0 + th)).resize((1920, 1080), Image.LANCZOS)
    im.save(dst, quality=93)


def main():
    lines = content_lines(TTS.read_text(encoding="utf-8")); starts, ends, total = line_starts(lines)
    IMG.mkdir(exist_ok=True, parents=True); CLIPS.mkdir(exist_ok=True, parents=True)
    for f in list(IMG.glob("slide_*.jpg")) + list(CLIPS.glob("clip_*.mp4")): f.unlink()

    entries, report = [], []
    for sec, (a, b) in SECTION_RANGES.items():
        ws, we = starts[a], (starts[b] if b < len(starts) else total)
        placed, slot, kept = place_section(SHOTS[sec], ws, we)
        report.append(f"   {sec:9} {we-ws:6.1f}s  slot={slot:5.1f}s  n={kept}")
        entries += [(t, sh, sec) for t, sh in placed]
    entries.sort(key=lambda x: x[0])

    slides, flow, names, err = [], [], [], 0
    cnt = {"vid": 0, "cc": 0, "px": 0, "ai": 0}
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
        elif kind in ("cc", "px"):
            ent["photo"] = True
            cands = list(REAL.glob(f"{ref}.*"))
            if not cands: print(f"[LOI] thieu anh that {ref}"); err += 1; continue
            src = cands[0]
            ent["source"] = f"real_photos/{src.name}"; ent["kind"] = {"cc": "commons", "px": "pexels"}[kind]
            cover_1080(src, IMG / f"slide_{pos:02d}.jpg")
        else:
            ent.update(photo=True, source=f"slides_img/slide_{pos:02d}.jpg (AI CAN GEN)", kind="ai")
            flow.append(f"{ref}, {LOCK}. {AVOID}")
        cnt[kind] += 1; slides.append(ent)
        names.append(f"slide_{pos:03d}_{name}  [{kind}]  (t~{t:.1f}s, {sec}, offset={off}s)")

    if not slides or not slides[0].get("photo") and not slides[0].get("video"):
        pass
    seen = set()
    for s_ in slides:
        k = (s_["match"], s_.get("offset", 0.0))
        if k in seen: print("[LOI] trung match+offset", k); err += 1
        seen.add(k)
    if err: print(f"\n[X] {err} loi - KHONG ghi"); sys.exit(1)

    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (VD / "scene_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "scene_prompts_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    ai_slots = [n for n in names if "[ai]" in n]
    (VD / "scene_prompts_AI_SLOTS.txt").write_text("\n".join(ai_slots) + "\n", encoding="utf-8")

    n = len(slides); vid_sec = sum(sh[3] for _, sh, _ in entries if sh[1] == "vid")
    real = cnt["vid"] + cnt["cc"] + cnt["px"]
    print(f"OK {n} entry -> {OUT_JSON.name}   ({total:.0f}s = {int(total)//60}:{int(total)%60:02d}, {total/n:.2f}s/khung)")
    print("\n".join(report))
    print(f"\n   clip THAT {cnt['vid']} ({vid_sec:.0f}s) | Commons {cnt['cc']} | Pexels {cnt['px']} | AI {cnt['ai']} = {cnt['ai']/n*100:.0f}%")
    print(f"   THAT {real}/{n} = {real/n*100:.0f}%")


if __name__ == "__main__":
    main()
