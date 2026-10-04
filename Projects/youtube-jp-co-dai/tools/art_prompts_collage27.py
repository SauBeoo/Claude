# -*- coding: utf-8 -*-
r"""art_prompts_collage27.py — prompt ảnh HERO (scene) phong cách ANIME cho video 27 (換気扇の油・灰汁).

Chép khuôn `art_prompts_collage26.py` (STYLE/PEOPLE/FRAME/NOTEXT giữ nguyên), chỉ đổi nội dung
SCENE theo 63 hero của `build_remotion_27.py::SCENES` (đọc từ builder, không chép tay).

CHẠY:  python tools/art_prompts_collage27.py      # → 06_VIDEO/27_*/art_prompts_photocard_{FLOW,BLOCKS,TENFILE}
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_remotion_27 as B  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]

STYLE = (
    "Japanese anime-style illustration, hand-drawn look with clean thin ink linework and soft "
    "watercolor-like cel shading, warm nostalgic palette (cream, terracotta, indigo, warm amber "
    "light), gentle painterly textures, cinematic 16:9 composition, high detail, calm storytelling "
    "mood like a quiet slice-of-life animation film."
)
PEOPLE = (
    "Any person is JAPANESE, drawn in the same anime style with natural proportions (not chibi, "
    "not exaggerated), modest everyday Japanese clothing, present-day unless noted otherwise. The "
    "woman Setsuko is in her mid-60s, gentle round face, short greying hair, a soft home apron."
)
FRAME = (
    "Composition: the main subject large and clearly readable near the centre of the frame, "
    "background simplified so the subject stands out at a glance; leave a small quiet margin "
    "around the edges."
)
NOTEXT = ("No text, no letters, no numbers, no signs with writing, no logo, no watermark anywhere.")
MOOD = {"clay": "warm earthy terracotta tones", "indigo": "cool indigo dusk/night tones",
        "cream": "soft cream daylight", "mustard": "golden afternoon light",
        "red": "hot red-orange heat haze", "moss": "fresh green shade",
        "flame": "warm dangerous orange firelight glow", "soot": "dim smoky charcoal-grey tones"}

# ── scene → (mood, mô tả). Key = tên hero trong SCENES. ───────────────────────
SCENE = {
    "card_fumidai_yure": ("indigo", "an elderly Japanese woman standing on a small step-stool in a "
        "kitchen at dusk, reaching up toward a ceiling range-hood fan, her stool tilting slightly, "
        "tense unsteady moment, dim warm kitchen light"),
    "card_hane_abura_hi": ("flame", "extreme close-up of a range-hood fan blade thickly caked in dark "
        "sticky grease, a faint dangerous orange flame glow reflected on the grime, ominous mood"),
    "card_fumidai_yakusoku": ("cream", "a small step-stool folded and standing quietly in a tidy "
        "Japanese kitchen corner, morning light, a sense of a promise waiting to be kept"),
    "card_intro_kanban": ("cream", "an old wooden signboard hanging above a traditional Japanese shop "
        "doorway, soft morning light, quiet inviting mood, a small trimmed garden tree beside it"),
    "card_setsuko_radio": ("cream", "an elderly Japanese woman cooking at a stove, a small radio "
        "sitting on top of the refrigerator behind her, warm kitchen daylight, homely mood"),
    "card_setsuko_utagau": ("indigo", "an elderly Japanese woman touching her own ear with a puzzled "
        "expression, standing in a dim kitchen at dusk, a small radio faintly glowing behind her"),
    "card_tissue_shindan": ("cream", "an elderly hand holding a single white tissue paper sheet near a "
        "kitchen range-hood intake grille, the tissue fluttering loosely instead of sticking, daylight"),
    "card_tissue_hattari": ("indigo", "close-up of a range-hood intake grille with a faint dusty grey "
        "film over the mesh, dim evening kitchen light, subtle change over time mood"),
    "card_juusou_kosuru": ("clay", "an elderly Japanese woman sitting on her kitchen floor exhausted, a "
        "scrubbing cloth and an open box of baking soda beside her, a dull grease-caked fan blade "
        "propped nearby, warm afternoon light, tired resigned mood"),
    "card_yaku_hakari": ("cream", "an old-fashioned brass balance scale with a small box of baking soda "
        "on one side sitting low, weighing less than an invisible stronger match, plain daylight"),
    "card_gimon_senzai": ("cream", "an elderly Japanese woman standing puzzled in front of a kitchen "
        "shelf lined with dish detergent bottles, scratching her head lightly, soft daylight"),
    "card_yubisaki_kachikachi": ("indigo", "extreme close-up of a fingertip touching a dark, hard, "
        "glossy caked layer on a metal fan blade, the finger sliding rather than sinking in, dim "
        "kitchen light"),
    "card_sanka_juugou": ("flame", "a stylised illustration of tiny golden oil droplets rising into the "
        "air above a stove flame, some droplets glowing and linking together like beads on a chain, "
        "warm dangerous orange light"),
    "card_purasuchikku_hen": ("clay", "a thin dark caked layer on a fan blade transforming visually into "
        "a smooth glossy plastic-like sheen, half oil half hardened resin, warm kitchen light"),
    "card_abura_concrete": ("earth", "extreme macro of a thick dark crusted layer on a range-hood fan "
        "blade, fine dust and lint fibres embedded in it like a rough concrete surface, dim light"),
    "card_taiketsu_ita": ("indigo", "a bottle of neutral dish detergent facing off against a thick dark "
        "hardened plastic-like crust on a fan blade, like two opponents, dramatic dim lighting"),
    "card_chuusei_senzai": ("cream", "a hand squeezing a dish detergent bottle, clear soapy bubbles "
        "forming, but sliding uselessly off a hard dark crusted surface nearby, daylight"),
    "card_jourei_kanban": ("clay", "a formal municipal fire-prevention ordinance notice pinned to a "
        "kitchen wall beside a range hood, official calm lighting, a small stamp seal shape on it"),
    "card_setsuko_hansei": ("indigo", "an elderly Japanese woman sitting quietly at her kitchen table "
        "looking at a wall calendar with several days circled and crossed out, dim evening light, "
        "regretful mood"),
    "card_kakushin_taitoru": ("indigo", "a glowing beaker of clear alkaline liquid standing beside a "
        "small dish of golden oil, the two about to meet, dramatic focused spotlight, quiet suspense"),
    "card_kenka_zu": ("cream", "a simple illustrative diagram: a drop of golden oil meeting a drop of "
        "clear alkaline liquid and transforming into soft white soap bubbles, warm glowing light"),
    "card_kagayaki_kenka": ("mustard", "a dark greasy stain on a cloth glowing and dissolving into soft "
        "white soap foam by itself, small sparkles of light radiating outward, magical warm mood"),
    "card_kamado_soko": ("soot", "the dark firebox at the bottom of an old traditional Japanese kamado "
        "clay stove, embers glowing faintly, a small mound of pale wood ash visible at the base"),
    "card_akujiru_hikaku": ("clay", "two glass jars of clear liquid side by side, one labelled by a "
        "faint glow as ordinary washing soda, the other glowing brighter and stronger, comparison mood"),
    "card_akujiru_tsukurikata": ("clay", "a stainless steel mixing bowl filled with pale grey wood ash, "
        "steaming hot water being poured over it from a kettle, warm kitchen daylight"),
    "card_akujiru_sumi": ("cream", "a glass jar with a clear golden liquid settled on top and a darker "
        "thick sediment layer at the bottom, soft daylight, clean separation visible"),
    "card_tsukeoki_fuku": ("indigo", "a detached range-hood fan blade soaking in a basin of warm water, "
        "steam rising gently, a cloth soaked in clear liquid resting beside it, calm patient mood"),
    "card_shippai_atsui_hai": ("soot", "a person's hand pouring water over a mound of still-smoking hot "
        "grey ash in a bowl, the liquid coming out cloudy and murky, dim disappointed mood"),
    "card_hai_nioi_kioku": ("clay", "an elderly hand reaching into a pile of soft cool wood ash early in "
        "the morning, a faint white layer visible on top, warm nostalgic wood-stove kitchen light"),
    "card_gomu_tebukuro": ("flame", "a pair of thick yellow rubber gloves and safety goggles laid out "
        "beside a glass jar of strong clear alkaline liquid, cautionary warm-orange warning light"),
    "card_arumi_seiryuuban": ("indigo", "a shiny aluminium range-hood fan component held in one hand, "
        "light glinting off its metal surface, a small warning symbol shape glowing faintly nearby"),
    "card_motor_keikoku": ("cream", "the dark inner motor housing of a range hood being wiped carefully "
        "with a well-wrung damp cloth from the outside only, careful cautious hand movement, daylight"),
    "card_seski_bin": ("mustard", "a small spray bottle of clear liquid labelled only by a simple leaf-"
        "like sesquicarbonate icon glow, standing on a kitchen counter, warm daylight"),
    "card_seski_pakku": ("cream", "a paper towel soaked in clear liquid draped over a stained fan blade "
        "like a compress pack, a small timer nearby, calm patient daylight"),
    "card_nazo_hai_kieta": ("indigo", "a large soft glowing question mark hovering over a cold, empty, "
        "long-unused traditional kamado stove, dusty and quiet, dim mysterious light"),
    "card_share_onegai": ("cream", "an elderly Japanese woman sitting at a low table, one hand near a "
        "smartphone on the table, a small teapot and two cups beside it, warm cosy living room light"),
    "card_haigai_shounin": ("clay", "a wandering Edo-period ash merchant with a wooden box on his back "
        "walking down a narrow lane at dawn, his hair dusted grey with ash, warm sepia morning light"),
    "card_haikai_koe": ("clay", "an Edo-period wooden nagaya row-house lane at dawn, a merchant's figure "
        "calling out in the distance, small wooden ash storage boxes outside doorways, warm sepia tone"),
    "card_souzou_ita": ("flame", "a glowing pile of coins transforming visually into a dark thick "
        "crusted stain on a fan blade, an imaginative comparison, warm-orange dreamlike light"),
    "card_akujiruoke": ("indigo", "a traditional Edo-period wooden ash-lye tub (akujiru-oke) with a "
        "small tap at the base dripping clear liquid into a basin below, a washtub nearby, sepia light"),
    "card_okane_nagare": ("mustard", "a stylised illustration of coins flowing in one direction from a "
        "wallet toward a service worker's hand, simple warm golden light, economic-flow mood"),
    "card_edo_shounin_kai": ("clay", "an Edo-period merchant holding out a small pouch of coins toward "
        "an unseen customer, ash boxes stacked beside him, warm sepia daylight"),
    "card_mukisagyaku": ("cream", "a simple mirrored illustration: on one side a hand giving away ash "
        "and receiving coins, on the other a hand giving away coins and receiving a bag of grease "
        "waste, symmetrical warm daylight"),
    "card_radio_modoru": ("indigo", "a small radio on top of a refrigerator glowing warmly, sound waves "
        "drawn softly radiating from it, a range-hood fan blade visible faintly narrowing behind it"),
    "card_kabegami_kiba": ("clay", "a kitchen ceiling wallpaper patch directly above a stove shown "
        "slightly yellowed compared to the surrounding clean wallpaper, warm daylight, subtle detail"),
    "card_3nen_shinkou": ("indigo", "a calendar showing three overlapping years fading softly into one "
        "another, a faint yellow stain slowly spreading in the background, dim time-passing mood"),
    "card_kizuki_setsuko": ("cream", "an elderly Japanese woman standing in her kitchen with a sudden "
        "realizing expression, one hand raised slightly, a soft question mark glow above her head"),
    "card_juugou_gyakute": ("flame", "a stylised illustration of two small glowing shapes, one for "
        "'time' (a clock) and one for 'heat' (a flame), pulling apart from each other instead of "
        "joining, warm dramatic light"),
    "card_ryouri_sara_sara": ("mustard", "fine golden oil droplets rising freely and lightly from a "
        "stovetop just after cooking, still loose and unconnected, warm cheerful kitchen light"),
    "card_juubyou_nuno_nade": ("mustard", "an elderly hand gently wiping a dry cloth once across a clean "
        "range-hood fan blade right after cooking, warm satisfying golden light, a calm decisive moment"),
    "card_zenbu_10byou": ("clay", "a small pile of cleaning items — ash-lye jar, sesquicarbonate bottle, "
        "a basin of warm water, and a pouch of coins — fading into the background behind one dry cloth "
        "standing out in front, warm daylight"),
    "card_okane_dewanai": ("indigo", "a simple soft heart shape glowing gently beside a small dry cloth, "
        "no coins or money symbols nearby, warm quiet sincere mood"),
    "card_ita_naikara": ("indigo", "an elderly woman's kitchen shown with a clean fan overhead and the "
        "step-stool folded and put away in a corner, calm relieved daylight"),
    "card_kaisuu_mamoru": ("cream", "a simple tally-mark counter shape glowing softly beside a folded "
        "step-stool, each mark representing one avoided climb, warm daylight"),
    "card_taorukake_furui": ("cream", "a worn soft old towel hanging from the end of a kitchen towel "
        "rail, within easy arm's reach of a stove, warm homely daylight"),
    "card_oto_modotta": ("indigo", "an elderly Japanese woman smiling gently while listening to a radio "
        "on top of a refrigerator, sound waves now drawn clean and even, warm kitchen light"),
    "card_fumidai_monooki": ("clay", "a small step-stool standing folded and dusty in a quiet home "
        "storage closet, no longer needed, warm soft afternoon light through a small window"),
    "card_shoujiki_genkai": ("flame", "a glass jar of strong clear alkaline liquid beside a shiny "
        "aluminium part with a small warning symbol, and an empty ash-less modern kitchen stove nearby, "
        "honest cautionary lighting"),
    "card_korekara_saki": ("indigo", "a dry cloth glowing softly beside a dark hardened crusted fan "
        "blade that remains unaffected by it, showing the cloth only prevents future build-up, dim mood"),
    "card_matteshimau": ("clay", "a tall old step-ladder leaning beside a jar of strong cleaning liquid, "
        "both representing things sought only after waiting too long, muted contemplative daylight"),
    "card_comment_onegai2": ("cream", "an old traditional kamado wood-stove beside a modern speech-"
        "bubble shape glowing softly, inviting a memory to be shared, warm daylight"),
    "card_tsugi_no_hanashi": ("indigo", "a softly glowing doorway opening into darkness, hinting at "
        "another hidden household secret waiting beyond, quiet mysterious dusk light"),
    "card_shimei_tojiru2": ("indigo", "a warm glowing paper lantern (andon) light shining softly beside "
        "a quiet kitchen window at night, calm and peaceful closing image, a thin crescent moon outside"),
}
MOOD["earth"] = "warm dim earthy brown tones"


def compose(desc, mood):
    d = desc.strip().rstrip(".;") + "."
    parts = [STYLE, f"SCENE: {d}", f"Lighting and colour: {MOOD[mood]}."]
    if any(w in d.lower() for w in ("man", "woman", "men", "women", "person", "people", "hand",
                                    "couple", "figure", "child", "elderly", "craftsman", "mother",
                                    "merchant", "setsuko")):
        parts.append(PEOPLE)
    parts += [FRAME, NOTEXT]
    return " ".join(p.strip() for p in parts)


def main():
    vdir = PROJ / "06_VIDEO" / B.STEM
    heros = []
    for s in B.SCENES:
        h = s.get("hero")
        if h and h not in heros:
            heros.append(h)
    missing = [h for h in heros if h not in SCENE]
    if missing:
        print(f"🔴 hero trong SCENES chưa có prompt: {missing}")
        return 1
    flow, ten, blocks = [], [], ["# Prompt HERO anime · video 27\n\n",
                                 "Gen xong → `python tools/make_photocard27.py --src <folder> --apply` "
                                 "(đổi tên + cắt ✦ + bo viền trắng tròn + bóng).\n"
                                 "Ảnh 1376×768, chủ thể giữa khung. KHÔNG chữ.\n"]
    for i, h in enumerate(heros, 1):
        mood, desc = SCENE[h]
        p = compose(desc, mood)
        flow.append(p)
        ten.append(f"{h + '.png':<32}<- dòng {i} FLOW  [{mood}]")
        blocks.append(f"\n## {i}. `{h}.png` · {mood}\n\n```\n{p}\n```\n")
    (vdir / "art_prompts_photocard_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (vdir / "art_prompts_photocard_BLOCKS.md").write_text("".join(blocks), encoding="utf-8")
    (vdir / "art_prompts_photocard_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")
    ln = [len(x) for x in flow]
    print(f"✓ {len(flow)} prompt hero anime → {vdir}")
    print(f"   độ dài: min {min(ln)} · TB {sum(ln)//len(ln)} · max {max(ln)} ký")
    return 0


if __name__ == "__main__":
    sys.exit(main())
