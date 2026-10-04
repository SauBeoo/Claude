# -*- coding: utf-8 -*-
"""Sinh SLIDES.json + prompt gen anh cho video 04 (showa45-asa) — BAN 3.

BAN 3 (2026-08-25): user chot nhip cat ~6 GIAY/KHUNG cho CA VIDEO (khong lap), giong dung
"NHIP 4 GIAY/ANH" ma kenh da lam o video 01 (289 khung). Tu ~30 anh (ban 2) len ~131 khung
(1 clip that + 130 anh AI): moi ITEM giu lai anh cu lam "anchor" + them shot MOI (coverage
kieu dien anh: wide/medium/close/insert) de lap kin nhip 6s theo dung do dai tung item.

Co che phan bo: moi ITEM co 1 danh sach shot co dinh (list SHOTS); script tu tinh khung thoi
gian that su cua item do (tu do dai ky tu cua dung doan dong thoai, he so 3.983 ky/giay - GIA
DINH, chua phai timeline that vi chua rebuild toan bo giong) roi CHIA DEU N shot vao khung do,
tu suy ra (line_idx, offset) cho tung shot — khong can go tay 131 offset.

⚠️ Sau khi co giong that (render full) → doc lai timeline.json that va doi chieu, offset co the
lech vai giay so voi uoc luong nay (da thay o demo: sai lech ~5s/100s, chap nhan duoc).
"""
import io, sys, re, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "04_showa45-asa_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "04_showa45-asa_SLIDES.json"
OUT_DIR = ROOT / "06_VIDEO" / "04_showa45-asa"
RATE = 3.983

LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, "
        "faded warm Fujicolor palette, soft natural light, gentle film grain, "
        "slight vignette, nostalgic documentary photography, muted greens and ochres, "
        "natural imperfect framing, 16:9")

PRESET = {
    "home": ("small Showa house interior, tatami room, wooden sliding doors, "
             "low table, single bare bulb"),
    "street": ("quiet Showa-era residential back lane at dawn, low wooden houses with "
               "dark tiled roofs on both sides, unpainted wooden fences and gates, "
               "narrow unpaved or worn concrete road, utility poles, no cars parked or "
               "moving anywhere in frame"),
    "station": ("a small 1970s Japanese train station platform, wooden platform edge, "
                "simple metal roof pillars, a route board visible but blurred and "
                "illegible, morning light"),
    "park": ("a small neighborhood park at sunrise, open gravel ground, a few trees, "
             "a simple wooden fence at the edge, open sky, long morning shadows"),
    "today": ("a small paper milk carton left beside a modern apartment door, soft "
              "natural daylight, gentle documentary photography, clean simple "
              "composition"),
}

AVOID = ("no watermark, no logo, no signature, no sparkle mark. "
         "Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, "
         "modern clothing, sneakers with logos, readable text or signage, brand logos, "
         "western faces, anime style, oversaturated HDR look, close-up faces.")
AVOID_TODAY = ("no watermark, no logo, no signature, no sparkle mark. "
               "Avoid: readable text or brand logos on the carton, western faces, "
               "anime style, oversaturated HDR look, close-up faces.")

# ============================================================================
# ITEM_RANGES: (line_idx_start, line_idx_end_exclusive, window_start_override)
# window_start_override=None -> dung dung line_starts[start]; item1 dung 5.2 (sau clip that)
# ============================================================================
ITEM_RANGES = {
    1: (0, 8, 5.2),
    2: (8, 15, None),
    3: (15, 18, None),
    4: (18, 21, None),
    5: (21, 23, None),
    6: (23, 27, None),
    7: (27, 32, None),   # gom ca CTA (dong 31)
    8: (32, 35, None),
    9: (35, 39, None),
    10: (39, 43, None),
    11: (43, 47, None),
    12: (47, 59, None),  # gom ca doan ket
}

# ============================================================================
# SHOTS theo ITEM — moi phan tu: (name, preset, desc). Anh co ten trung voi 30 anh
# BAN 2 (00_yoake_roji, 01_toufuya_jitensha, ...) la ANH DA GEN, giu nguyen khong doi.
# ============================================================================
SHOTS = {
1: [
    ("00_yoake_roji", "street", "a narrow residential back lane in the pale blue light just before sunrise, low wooden houses with dark tiled roofs on both sides, a single paper lantern-style porch light still glowing near a doorway, empty and completely still, no people visible anywhere in the frame"),
    ("i1_02_gaitou", "street", "close-up of a single old street lamp still glowing against a pale pre-dawn sky, dew on the glass, no people visible"),
    ("i1_03_shutters", "street", "a row of wooden shop shutters still closed along a quiet lane, morning light grazing across the wood grain, no people, no readable signage"),
    ("i1_04_amimizu_taru", "street", "close-up of a wooden rain barrel beside a house, still water inside reflecting the pale morning sky, no people"),
    ("i1_05_neko", "street", "a cat curled asleep on a wooden doorstep in the pale morning light, quiet residential lane, no people visible"),
    ("i1_06_tsuyu_kaki", "street", "close-up of dew beading on a weathered wooden fence rail, soft pre-dawn light, no people"),
    ("i1_07_roji_kasumi", "street", "a wide view of the residential lane curving away between houses, thin mist hanging near the ground, empty and still"),
    ("i1_08_futon_hosu", "street", "close-up of a folded futon airing over a windowsill, morning light, quiet house exterior, no people"),
    ("i1_09_bell_close", "street", "extreme close-up of an old bicycle bell mounted on a handlebar, a bead of dew on the metal, soft morning light"),
    ("i1_10_bike_kuru", "street", "a delivery bicycle approaching down the lane, seen from behind at a distance, morning light, rider silhouette only, no face visible"),
    ("i1_11_kaban_shinbun", "street", "close-up of a canvas delivery bag hanging from a bicycle handlebar, folded newspapers visible inside, morning light"),
    ("08_shinbun_toukanguchi", "street", "a folded newspaper wedged into a metal mail slot on a plain wooden gate, seen close, morning light, paper texture only, no readable text or headlines legible"),
    ("i1_13_shinbun_hazure", "street", "close-up of a single rolled newspaper resting against a wooden gate post, morning light, paper texture only"),
    ("i1_14_engawa_kara", "home", "an empty wooden engawa veranda with a folded floor cushion, morning light spilling across it, no people visible"),
    ("09_sofu_engawa", "home", "an elderly man's hands holding open a folded newspaper while seated on a wooden engawa veranda, warm morning sunlight, seen strictly from behind so no face is visible, the newsprint blurred with no legible text"),
    ("i1_16_yuge_chawan", "home", "close-up of a simple teacup with steam rising, resting on a low wooden table beside a folded newspaper, warm morning light"),
],
2: [
    ("01_toufuya_jitensha", "street", "an old bicycle with a battered metal delivery box mounted on the rear rack and a small brass trumpet horn hanging from the handlebar, parked at the edge of a quiet residential lane, soft early morning light, no rider or person visible in frame"),
    ("01b_rappa_close", "street", "extreme close-up of an old brass trumpet horn catching the very first warm light of morning, dew still visible on its surface, blurred bicycle handlebar behind it"),
    ("i2_03_hako_tsuyu", "street", "close-up of the battered wooden delivery box mounted on a bicycle's rear rack, condensation beading on its lid, soft morning light"),
    ("i2_04_wadachi", "street", "a narrow lane wet with morning dew, faint bicycle wheel tracks in the dust, no people visible"),
    ("02_nabe_te", "street", "a small hand holding an old aluminum pot by its handle, walking along a narrow residential lane, morning light, seen strictly from behind the shoulder so no face is visible"),
    ("i2_06_hadashi", "street", "close-up of small bare feet running along a stone path, morning light, no face or upper body visible"),
    ("i2_07_mizu_yure", "street", "extreme close-up of water rippling inside an aluminum pot carried at a hurried pace, morning light"),
    ("03_toufu_kobore", "street", "a few broken pieces of white tofu scattered beside a small puddle of water at the corner of a narrow lane, morning light, no people anywhere in the frame"),
    ("i2_09_haha_sukuu", "street", "close-up of a mother's hand gently scooping a broken piece of tofu into a small bowl, warm morning light, no face visible"),
    ("i2_10_mise_to", "street", "a wooden shop door half open, faint steam drifting out from inside, morning light, no people visible, no readable signage"),
    ("03b_okara_fukuro", "street", "a small paper bag of soft white soybean pulp being handed through a half-open wooden shop door, only hands visible on both sides, morning light, no faces"),
    ("i2_12_okara_shitsu", "street", "extreme close-up of soft white soybean pulp texture inside a paper bag, morning light"),
    ("i2_13_nedan_ita", "street", "a small blank wooden price board leaning against a shop's window sill, weathered, no readable text or numbers, morning light"),
    ("i2_14_roji_akarui", "street", "a wide view of the same residential lane now a little brighter, the delivery bicycle gone, only faint wheel tracks remaining, no people"),
    ("i2_15_wheel_stop", "street", "extreme close-up of a bicycle wheel slowly coming to a stop, spokes catching the morning light"),
],
3: [
    ("04_mezamashi_dokei", "home", "a small wind-up alarm clock with twin brass bells on top, sitting on a low wooden bedside stand beside a neatly folded futon, dim pre-dawn light coming through a paper shoji screen"),
    ("i3_02_bell_kinzoku", "home", "extreme close-up of the alarm clock's twin brass bells, fine dust motes visible in the thin pre-dawn light"),
    ("i3_03_futon_yami", "home", "a neatly folded futon and pillow in a dim quiet bedroom, soft pre-dawn light through a paper screen, no people visible"),
    ("i3_04_kabe_dokei", "home", "close-up of a simple wall clock's second hand, soft morning light, small Showa-era room, no people"),
    ("05_haha_daidokoro_mizu", "home", "hands running water at an old ceramic kitchen sink in a small Showa-era kitchen, faint steam rising, seen strictly from behind the shoulder, no face visible, dim early morning light"),
    ("i3_06_yakan_yuge", "home", "close-up of faint steam rising from a metal kettle warming on a small stove, dim kitchen light"),
    ("i3_07_tana_wan", "home", "a simple wooden kitchen shelf with plain ceramic bowls stacked neatly, soft morning light, no people visible"),
],
4: [
    ("06_gyunyu_bako", "street", "a small wooden milk delivery box mounted beside a house's front gate, its lid open, two glass milk bottles with round paper caps standing inside, a thick pale cream-colored layer visible just under the cap of one bottle, condensation beading on the glass, soft morning light, no people in frame"),
    ("i4_02_kanban_gyunyu", "street", "close-up of a small weathered tin sign for milk delivery mounted on a wooden gate post, no legible text, morning light"),
    ("i4_03_roji_hako", "street", "a wide view of a quiet residential lane with a few more milk delivery boxes visible on distant gates, soft morning light, no people"),
    ("i4_04_bin_tsuyu", "street", "extreme close-up of dew beading on a glass milk bottle's round paper cap, soft morning light"),
    ("06b_kuriimu_sukuu", "street", "close-up of a small child's finger reaching into an open glass milk bottle to scoop the thick cream layer just under the cap, morning light, only the hand and finger visible, no face"),
    ("i4_06_futa_modosu", "street", "close-up of a small hand replacing a paper cap back onto a glass milk bottle, morning light, no face visible"),
    ("i4_07_bin_kara", "street", "close-up of an empty glass milk bottle from the day before, waiting to be collected beside a gate, morning light"),
    ("i4_08_kago_kara", "street", "a small woven delivery basket hanging empty on a wooden fence, morning light, no people visible"),
    ("i4_09_shimo_toke", "street", "close-up of frost melting on a metal delivery box hinge as the first sunlight touches it"),
],
5: [
    ("10_denkigama_yuge", "home", "gentle steam rising from the lid vent of a round white electric rice cooker on a kitchen counter, warm morning light, a small Showa-era kitchen softly blurred behind it"),
    ("i5_02_dial", "home", "close-up of a round white electric rice cooker's simple control dial, warm morning light"),
    ("i5_03_daidokoro_wide", "home", "a wide view of a small Showa-era kitchen counter with a rice cooker and a few simple utensils, warm morning light, no people visible"),
    ("i5_04_yuge_mado", "home", "close-up of steam curling near a small kitchen window, soft backlight, quiet morning"),
    ("i5_05_shamoji", "home", "close-up of a wooden rice paddle resting in a small stand beside the rice cooker, warm morning light"),
],
6: [
    ("11_chabudai_asagohan", "home", "a low round wooden chabudai table set with small bowls of miso soup, a single grilled dried fish, and a bowl of rice topped with a raw egg, individual rice bowls and chopsticks at each place, soft morning light from a nearby window, no people visible, just the table setting"),
    ("i6_02_sakana_yaku", "home", "close-up of a small dried fish grilling, faint smoke rising, warm morning light"),
    ("i6_03_hashioki", "home", "close-up of a pair of chopsticks resting on a simple ceramic chopstick rest beside a bowl, morning light"),
    ("12_shoyu_tamagogohan", "home", "close-up of dark soy sauce being poured over a bowl of rice topped with a raw egg, the liquid pooling at the edge of the bowl, a pair of chopsticks resting beside it"),
    ("i6_05_chabudai_ato", "home", "a wide view of the low chabudai table with bowls half emptied, morning light, no people visible, quiet aftermath of breakfast"),
],
7: [
    ("13_terebi_ima", "home", "a boxy 1970s television set glowing softly in the corner of a small tatami living room, a family seated on the floor in front of it seen only from behind in soft silhouette, warm screen light reflecting across the tatami mats"),
    ("i7_02_dial_terebi", "home", "close-up of a boxy television's round control knobs and channel dial, warm screen glow reflected on them"),
    ("i7_03_shinbun_yoko", "home", "close-up of a folded newspaper resting beside a glowing television set, warm morning light"),
    ("i7_04_ima_wide", "home", "a wide view of a small tatami living room, warm television screen light spilling across the mats, no people visible"),
    ("i7_05_hachiue", "home", "close-up of a small potted plant on a windowsill beside the glowing television, soft morning light"),
    ("14_terebi_kazoku_chikayoru", "home", "a closer view of a family seated together on tatami mats in front of a glowing television screen, seen strictly from behind so no faces are visible, warm soft light from the screen, a quiet stillness in the room"),
    ("i7_07_chawan_kigo", "home", "close-up of a teacup steaming gently on a low table beside seated family members, seen only from behind, warm light"),
    ("i7_08_zabuton", "home", "close-up of a woven floor cushion on tatami mats, warm morning light, quiet room"),
    ("i7_09_fusuma", "home", "a wide view of sliding paper doors in a small living room, softly lit from within, no people visible"),
    ("i7_10_kazoku_shashin", "home", "close-up of a simple framed family photograph on a low shelf, soft light, details unreadable"),
    ("i7_11_speaker", "home", "close-up of a boxy television's fabric-covered speaker grille, warm screen light reflected on the weave"),
    ("i7_12_kabe_dokei2", "home", "close-up of a simple wall clock ticking in the corner of a small living room, soft morning light"),
    ("i7_13_moufu", "home", "close-up of a folded blanket resting on tatami mats, soft morning light, quiet room"),
    ("i7_14_ima_kara", "home", "a wide view of the same living room now empty, the television still glowing softly, no people visible"),
    ("i7_15_hokori_hikari", "home", "close-up of fine dust motes drifting through a beam of morning light crossing a tatami floor, quiet room, no people"),
],
8: [
    ("15_sentakumono_hosu", "street", "a bamboo laundry pole bowed slightly under the weight of hanging white bedsheets, catching the morning breeze, a small wooden house wall behind, no people visible"),
    ("i8_02_pin", "street", "close-up of a wooden clothespin holding the corner of a white sheet, morning breeze, soft light"),
    ("i8_03_haha_hosu", "street", "a mother's hands hanging laundry on a bamboo pole, seen strictly from behind, morning light, no face visible"),
    ("i8_04_niwa_wide", "street", "a wide view of a small Showa-era garden with laundry poles and a few potted plants, morning light, no people visible"),
    ("i8_05_shizuku", "street", "close-up of water droplets falling from a freshly hung white sheet, morning light"),
    ("i8_06_kago", "street", "close-up of a wicker laundry basket resting on the ground beside the pole, morning light, no people visible"),
    ("i8_07_kabe_sentaku", "street", "a wide view of the house's back wall with laundry now fully hung, morning light, no people visible"),
],
9: [
    ("16_randoseru_genkan", "home", "a black leather school satchel resting upright beside a pair of small shoes at a wooden genkan entrance step, morning light spilling in through the open front door, no people in frame"),
    ("i9_02_buckle", "home", "close-up of a black leather satchel's metal buckle catching morning light"),
    ("i9_03_kutsu_haku", "home", "close-up of small shoes being slipped on at a wooden genkan step, morning light, no face visible"),
    ("i9_04_mon_hiraku", "street", "a wide view of a front gate standing open, morning light spilling onto the residential lane, no people visible"),
    ("17_shudan_tokou", "street", "a line of small figures walking together along a narrow residential lane in soft morning light, seen from behind at a distance, wearing simple plain uniforms, no faces visible, one slightly taller figure leading at the front"),
    ("i9_06_ashimoto", "street", "close-up of small feet walking along a dusty lane, morning light, no faces or upper bodies visible"),
    ("i9_07_tooku", "street", "a wide view of the group of small figures now farther away down the lane, morning light, no faces visible"),
    ("i9_08_ishi_keru", "street", "close-up of a single loose stone being kicked along a dusty road, morning light, no faces visible"),
],
10: [
    ("18_manin_densha_platform", "station", "commuters in dark coats standing shoulder to shoulder on a small train station platform, seen strictly from behind, a train just arriving in soft morning light, simple metal roof pillars overhead, no legible signage"),
    ("i10_02_senaka", "station", "close-up of commuters' dark coats and shoulders pressed together, seen strictly from behind, no faces visible"),
    ("i10_03_yane_hashira", "station", "a wide view of a small station platform's simple metal roof pillars against a hazy morning sky, no people visible"),
    ("i10_04_sharin", "station", "close-up of a train's wheel and undercarriage arriving at the platform, motion blur, morning light"),
    ("19_densha_doa_shimaru", "station", "a closer view of the same crowded platform as a train's doors begin to close, packed commuters seen only from behind and in silhouette, soft morning light, no legible signage anywhere"),
    ("i10_06_tsurikawa", "station", "close-up of a hand gripping an overhead strap inside a crowded train car, seen from behind, no face visible"),
    ("i10_07_platform_kara", "station", "a wide view of the station platform now emptied, a single distant figure walking away, morning light"),
    ("i10_08_mado_kumori", "station", "close-up of a train window fogged with condensation, blurred figures faintly visible inside, no faces legible"),
    ("i10_09_senro", "station", "a wide view of train tracks receding into the hazy morning distance, no train visible, quiet"),
],
11: [
    ("20_rajio_taisou_kouen", "park", "a small group of people doing synchronized morning calisthenics in an open neighborhood park at sunrise, seen from behind in gentle silhouette, a simple wooden fence and a few trees at the edge of the frame, warm early light"),
    ("i11_02_ashimoto_taisou", "park", "close-up of small feet in simple shoes standing on gravel, morning light, no faces visible"),
    ("i11_03_kouen_wide", "park", "a wide view of a small park's simple wooden fence and a few trees, empty gravel ground, morning light"),
    ("i11_04_te_nobasu", "park", "close-up of hands raised together in a stretching motion, seen from behind, no faces visible"),
    ("21_taisou_stampcard", "park", "close-up of a small hand holding a plain cardboard stamp card strung on a cord around the neck, a rubber stamp being pressed onto one of the empty squares on the card, soft morning park light, no readable text on the card"),
    ("i11_06_card_yure", "park", "close-up of a cardboard stamp card swinging gently on its cord, soft morning light"),
    ("i11_07_kaisan", "park", "a wide view of the small group dispersing across the park, soft morning light, no faces visible"),
    ("i11_08_kusa_tsuyu", "park", "close-up of dew on blades of grass at the edge of the gravel ground, soft morning light"),
],
12: [
    ("22_shinbun_midashi_bokeh", "home", "close-up of an open newspaper page held in two hands, a large blurred photograph of a crowd beneath a hazy futuristic tower structure faintly visible on the page, the whole page softly out of focus so no text or headline is legible, warm morning light"),
    ("i12_02_te_shiwa", "home", "close-up of aged hands holding the edge of a newspaper page, morning light, no legible text"),
    ("i12_03_shashin_bokeh", "home", "extreme close-up of a blurred newspaper photograph, indistinct shapes only, warm morning light"),
    ("i12_04_engawa_yomu", "home", "a wide view of an empty engawa veranda where a newspaper was just being read, morning light, no people visible"),
    ("23_banpaku_gunshuu_toi", "street", "a vast crowd of small silhouetted figures walking together toward a hazy, abstract futuristic tower structure in the far distance, warm hazy morning light, every figure indistinct and anonymous, no legible signage anywhere"),
    ("i12_06_gunshuu_close", "street", "close-up of countless small silhouettes within a vast crowd, hazy warm morning light, every figure anonymous"),
    ("i12_07_tou_hitori", "street", "a wide view of a single hazy tower structure alone against a pale sky, no crowd visible, distant and abstract"),
    ("i12_08_hitori_senaka", "street", "close-up of a single figure among many, seen only from behind, morning haze"),
    ("i12_09_roji_shizuka", "street", "a wide view of a quiet residential lane, completely still, soft morning light, a deliberate contrast to a distant crowd"),
    ("24_ie_zentai_asa", "home", "a wide view of a small Showa-era wooden house from its front garden in the early morning, soft sunlight on the tiled roof and wooden walls, laundry visible on a line, completely quiet, no people visible"),
    ("i12_11_mongi", "home", "close-up of a wooden gate post with morning light catching the grain, quiet, no people visible"),
    ("i12_12_yane_sora", "home", "a wide view of a tiled roof against a clearing morning sky, soft light"),
    ("i12_13_tobi_ishi", "home", "close-up of a garden stone path leading to a front door, morning light, no people visible"),
    ("25_gyunyu_kamipakku_ima", "today", "a small modern paper milk carton left beside the door of a present-day apartment, soft natural daylight, a clean simple quiet composition, no people visible"),
    ("i12_15_doorbell", "today", "close-up of a modern doorbell button beside an apartment door, soft daylight, quiet"),
    ("25b_anpi_kakunin", "today", "a small folded note left leaning against the modern milk carton at the same apartment door, soft natural daylight, quiet and still, no legible text on the note, no people visible"),
    ("i12_17_memo_yure", "today", "close-up of a folded note's corner lifting slightly in a breeze, soft daylight"),
    ("i12_18_roka", "today", "a wide view of a quiet modern apartment corridor, soft daylight, no people visible"),
    ("26_ie_asahi_shizuka", "home", "warm morning sunlight streaming through a paper shoji screen onto a quiet empty tatami room, fine dust motes drifting visibly in the light beam, completely still, no people in frame"),
    ("i12_20_hokori2", "home", "close-up of dust motes drifting in a warm light beam across an empty tatami room, quiet"),
    ("i12_21_shinbun_oki", "home", "close-up of a folded newspaper resting undisturbed on a low table, morning light"),
    ("i12_22_engawa_shizumu", "home", "a wide view of an empty engawa veranda, morning light softening, quiet, no people visible"),
    ("i12_23_chawan_sameta", "home", "close-up of a single teacup left on a low table, steam long gone, soft morning light"),
    ("i12_24_roji_hiru", "street", "a wide view of the quiet residential lane once more, fuller daylight now, no people visible"),
    ("i12_25_shoji_hikaru", "home", "close-up of a paper shoji screen glowing softly with morning light, quiet room, no people"),
    ("i12_26_ie_sora", "home", "a wide view of the house from its garden, morning fully arrived, soft light, no people visible"),
    ("i12_27_tatami_hikari", "home", "close-up of warm morning light spreading gently across a tatami floor, quiet, no people visible"),
],
}


def content_lines(raw):
    out = []
    for l in raw.split("\n"):
        s = re.sub(r"\[[^\]]*\]", "", l).strip()
        if s:
            out.append(s)
    return out


def line_starts(lines):
    """tra ve (starts, ends, total) - moc thoi gian UOC LUONG tung dong theo he so RATE."""
    starts, cum = [], 0.0
    for l in lines:
        starts.append(cum / RATE)
        cum += len(l)
    total = cum / RATE
    ends = starts[1:] + [total]
    return starts, ends, total


def find_line_and_offset(t, starts, ends):
    for i, (s, e) in enumerate(zip(starts, ends)):
        if s <= t < e or (i == len(starts) - 1 and t >= s):
            return i, round(t - s, 2)
    return len(starts) - 1, 0.0


def main():
    raw = TTS.read_text(encoding="utf-8")
    lines = content_lines(raw)
    starts, ends, total = line_starts(lines)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    slides, flow, names, rows = [], [], [], []
    err = 0

    # --- clip that (vi tri 0) ---
    entries = [("vid", 0.0, None)]  # (kind, target_time, shot_tuple)

    for item, (li0, li1, win_override) in ITEM_RANGES.items():
        shots = SHOTS[item]
        n = len(shots)
        window_start = win_override if win_override is not None else starts[li0]
        window_end = starts[li1] if li1 < len(starts) else total
        dur = window_end - window_start
        for k, shot in enumerate(shots):
            t = window_start + k * dur / n
            entries.append(("img", t, shot))

    entries.sort(key=lambda x: x[1])

    for kind, t, shot in entries:
        if kind == "vid":
            idx, off = 0, 0.0
            line = lines[idx]
            m = line[:14]
            slides.append({"match": m, "video": True})
            names.append(f"CLIP_slide_{len(slides)-1:02d}_toufuya_gaikei_press.mp4 (da cat san, xem clips/)")
            continue
        idx, off = find_line_and_offset(t, starts, ends)
        line = lines[idx]
        m = line[:14]
        if not any(m in L for L in lines):
            print(f"[LOI] match khong khop: {m}"); err += 1; continue
        name, preset, desc = shot
        ent = {"match": m, "photo": True}
        if off:
            ent["offset"] = off
        slides.append(ent)
        is_new = name.startswith("i")
        avoid = AVOID_TODAY if preset == "today" else AVOID
        tag = "MOI" if is_new else "DA CO (ban 2, khong doi)"
        names.append(f"slide_{len(slides)-1:02d}_{name}.jpg  [{tag}]" + (f"  (t~{t:.1f}s, offset {off}s)" if off else f"  (t~{t:.1f}s)"))
        rows.append((len(rows), name, preset, m, desc, is_new))
        if is_new:
            flow.append(f"{desc}, {PRESET[preset]}, {LOCK}. {avoid}")

    # GATE mau thuan
    PAIRS = [("no street", "shopping street"), ("no people", "figures"),
             ("no face", "face"), ("no cars", "car"), ("indoor", "outdoor")]

    def _positive(text, pos):
        t2 = re.sub(r"\bno\b(?:\s+\w+){0,3}\s+" + re.escape(pos), " ", text)
        return re.search(r"\b" + re.escape(pos) + r"\b", t2) is not None

    for i, (name, preset, m, desc, is_new) in enumerate([(r[1], r[2], r[3], r[4], r[5]) for r in rows]):
        low = f"{desc}, {PRESET[preset]}, {LOCK}".lower()
        for neg, pos in PAIRS:
            if neg in low and _positive(low, pos):
                print(f"[LOI] prompt {i:02d} ({name}) TU MAU THUAN: co '{neg}' nhung van ta '{pos}'")
                err += 1

    # GATE trung ten (2 shot cung ten o vi tri khac nhau la BINH THUONG - anh cu tai su dung -
    # chi bao neu TRUNG Y HET match+offset, tuc loi logic that)
    seen = set()
    for s in slides:
        key = (s["match"], s.get("offset", 0.0))
        if key in seen:
            print(f"[LOI] trung hoan toan match+offset: {key}"); err += 1
        seen.add(key)

    if err:
        print(f"\n[X] {err} loi - KHONG ghi file"); sys.exit(1)

    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT_DIR / "scene_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (OUT_DIR / "scene_prompts_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    with open(OUT_DIR / "scene_prompts_BLOCKS.md", "w", encoding="utf-8") as f:
        f.write("# Prompt gen anh AI MOI — 04_showa45-asa (BAN 3, nhip ~6s/khung)\n\n")
        f.write("> Chi liet ke anh MOI (30 anh ban 2 da co, KHONG gen lai). "
                "Gen bang Nano Banana/Gemini, 16:9, 3 ban/canh -> duyet mat chon 1.\n")
        f.write(f"> Tong {len(rows)} khung ({sum(1 for r in rows if r[5])} moi + "
                f"{sum(1 for r in rows if not r[5])} tai su dung).\n\n")
        for i, name, preset, m, desc, is_new in rows:
            if not is_new:
                continue
            f.write(f"## {i:02d} — {name}  (preset: {preset})\n")
            f.write(f"Khớp dòng: _{m}…_\n\n")
            avoid = AVOID_TODAY if preset == "today" else AVOID
            f.write(f"```\n{desc}, {PRESET[preset]}, {LOCK}. {avoid}\n```\n\n")

    n = len(slides)
    dur_gap = [entries[i+1][1] - entries[i][1] for i in range(len(entries)-1)] + [total - entries[-1][1]]
    print(f"OK {n} entry -> {OUT_JSON.name}")
    print(f"   do dai uoc tinh: {total:6.1f} giay = {int(total)//60}:{int(total)%60:02d}")
    print(f"   {total/n:5.2f} giay/hinh trung binh (muc tieu ~6)")
    print(f"   khung ngan nhat: {min(dur_gap):.1f}s | dai nhat: {max(dur_gap):.1f}s")
    n_new = sum(1 for r in rows if r[1].startswith("i"))
    print(f"   anh MOI can gen: {n_new} / {len(rows)} (con lai la 30 anh ban 2 tai su dung)")


if __name__ == "__main__":
    main()
