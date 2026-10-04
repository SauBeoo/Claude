# -*- coding: utf-8 -*-
r"""sticker_prompts_collage25.py — prompt STICKER (từng vật) phong cách ANIME, nền MAGENTA, video 25.

⭐ 2026-08-28 user: *"sticker hầu như không trùng nhau"* ⇒ mỗi scene 2 sticker RIÊNG, không vật
nào dùng ở 2 scene (builder gate 🔴). 48 scene × 2 = 96 vật; 18 đã gen (lô `download (8)`) gắn
mỗi cái đúng 1 scene, còn lại xuất prompt. Chạy tool là nó tự trừ những file đã có trong `sticker/`.

Cast anime 5 tư thế đã gen nhưng KHÔNG dùng (phương án C bỏ cast) — không xuất prompt cast nữa.

🔴 Nền MAGENTA #FF00FF thuần · ĐÚNG 1 vật / ảnh · cắt nền: `tools/cutout_sticker25.py --src <folder> --apply`.

CHẠY:  python tools/sticker_prompts_collage25.py
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_remotion_25 as B  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]

STYLE = ("Japanese anime-style illustration, clean thin ink linework, soft cel shading, warm "
         "nostalgic palette (cream, terracotta, indigo, amber).")
CUTOUT = ("ONE SINGLE OBJECT only, centred, filling most of the frame, drawn as a die-cut sticker "
          "with a thick even WHITE OUTLINE all the way around it. No background scenery.")
BG = ("The background is a COMPLETELY FLAT, UNIFORM, SOLID MAGENTA #FF00FF chroma-key screen — pure "
      "magenta edge to edge, nothing else: no table, no floor, no shadow on the background, no "
      "gradient, no texture. Only the object with its white outline sits on the magenta.")
NOTEXT = "No text, no letters, no numbers, no logo, no watermark anywhere in the image."

SPEC = {
    # ── đã gen (lô 8) ──────────────────────────────────────────────────────────
    "el_ondokei":     "an old glass mercury thermometer with a red column, no numbers on its scale",
    "el_burst_red":   "a jagged red comic impact starburst shape, nothing inside it",
    "el_jaguchi":     "a chrome kitchen tap with a stream of water pouring down from it",
    "el_mizugame":    "a large rough unglazed terracotta water jar with a wide mouth and a wooden lid",
    "el_reizouko":    "a rounded Showa-era refrigerator with a chrome handle, door closed, cream colour",
    "el_mizu_shizuku": "three fat drops of clear water, pale blue, glistening",
    "el_uekibachi":   "a plain unglazed terracotta flowerpot, empty, seen slightly from above",
    "el_yuge":        "three curling wisps of vapour rising upward, soft white",
    "el_nasu":        "two glossy dark purple eggplants with green stems, side by side",
    "el_uchiwa":      "a round Japanese uchiwa fan with a bamboo handle, plain indigo face",
    "el_coin_stack":  "a tall stack of Japanese coins seen from the side",
    "el_calendar":    "a torn-off desk calendar page with an empty date grid",
    "el_teacup":      "a Japanese green-tea cup on a small saucer, seen from slightly above",
    "el_tarai":       "a wide shallow wooden washtub with metal hoops, full of still water",
    "el_senpuuki":    "a retro Japanese electric desk fan with a round wire cage, pale green body",
    "el_taoru":       "a folded damp white hand towel with a few water drops on it",
    "el_katorisenko": "a green spiral mosquito coil on a small ceramic holder with a thin smoke line",
    "el_smartphone":  "a modern smartphone lying at a slight angle, screen blank and pale",
    "el_newspaper":   "a folded morning newspaper with blank columns",
    # ── mới — theo scene ───────────────────────────────────────────────────────
    "el_kyukyusha":   "a small Japanese ambulance seen from the front-side with its red roof light glowing",
    "el_tsuki_yoru":  "a thin crescent moon with two small stars, pale yellow on deep indigo shading",
    "el_te_no_kou":   "the back of an elderly hand with water splashing onto it, fingers relaxed",
    "el_hishaku":     "a wooden ladle (hishaku) with a long handle, seen from the side",
    "el_mugicha":     "a plastic bottle of Japanese barley tea, amber liquid, blank label",
    "el_koppu":       "a clear glass of cold water with condensation drops, seen from the side",
    "el_tokei":       "a round wooden wall clock with plain hands, no numerals",
    "el_remocon":     "an air-conditioner remote control with blank buttons, lying at an angle",
    "el_kappogi":     "a white Japanese kappogi kitchen apron folded neatly, seen from the front",
    "el_furoshiki":   "a small indigo furoshiki cloth bundle tied at the top with a knot",
    "el_kakudai":     "a round magnifying glass with a wooden handle, lens clear",
    "el_koorimizu":   "a small bowl of ice water with a few ice cubes floating, seen from above",
    "el_flask":       "a laboratory glass flask half filled with clear water, no markings",
    "el_plug_off":    "an electric power plug with its cord curling away, unplugged, lying loose",
    "el_bottle":      "a clear plastic water bottle standing upright, blank label, half full",
    "el_suna":        "a small heap of damp sand on a wooden scoop",
    "el_nureta_nuno": "a wrung wet cotton cloth, pale grey, hanging loosely with a water drop falling",
    "el_yubi":        "an elderly hand with one index finger pointing, seen from the side",
    "el_hatena":      "a big rounded question mark shape, deep indigo with a cream highlight",
    "el_kaze":        "three flowing curved wind lines, soft pale blue, like a breeze",
    "el_nefuda":      "a blank shop price tag on a string, rectangular, cream paper",
    "el_taiyou":      "a warm bright cartoon sun with soft rays, amber and cream",
    "el_amagumo":     "a grey rain cloud with three raindrops falling from it",
    "el_tsubo_nijuu": "a large clay pot nested inside a bigger clay pot with damp sand between them, seen in cut-away",
    "el_tomato":      "three ripe red tomatoes with green stems in a small pile",
    "el_medal":       "a round gold medal with a plain face hanging on a short ribbon",
    "el_lantern":     "a camping lantern that is switched off, glass dark, metal handle up",
    "el_cooler":      "a blue plastic cooler box with the lid slightly open and melting ice inside",
    "el_tsubo_tsuya": "a glossy glazed ceramic vase with a shiny reflective surface, deep green",
    "el_kirakira":    "a cluster of four sparkle stars of different sizes, pale yellow",
    "el_kama":        "a small brick pottery kiln with a chimney and a glowing mouth",
    "el_tanuki":      "a Shigaraki-style ceramic tanuki raccoon-dog statue wearing a straw hat, holding a plain bottle",
    "el_tokkuri":     "a small unglazed clay flask (tokkuri) with a rope loop around its neck",
    "el_sugegasa":    "a wide conical woven straw travelling hat (sugegasa), seen from slightly below",
    "el_hamon":       "concentric water ripples on a dark water surface, seen from above",
    "el_ido":         "an old stone well with a wooden roof frame and a pulley bucket",
    "el_tenugui":     "a long thin Japanese tenugui cloth with a simple indigo pattern, hanging",
    "el_keihou":      "a red triangular warning sign with a plain exclamation shape, no text",
    "el_denwa":       "an old beige house telephone with a coiled cord, handset on the cradle",
    "el_furin":       "a small glass wind chime with a paper strip hanging below it",
    "el_ase":         "three large sweat drops, pale blue, falling",
    "el_take_hishaku": "a bamboo ladle with a short handle, water inside the cup",
    "el_shibuki":     "a burst of splashing water with round droplets flying outward, white and pale blue",
    "el_koori_bucket": "a metal bucket filled with ice cubes, frost on the rim",
    "el_batsu":       "a bold red cross mark (X) drawn with two thick brush strokes",
    "el_kyukyu_bako": "a white first-aid box with a plain red cross shape on the lid, closed",
    "el_sensu":       "a folding paper fan (sensu) half open, plain cream paper with indigo edge",
    "el_kubi_taoru":  "a rolled white towel curved as if resting around a neck, damp",
    "el_kuwa":        "a Japanese farming hoe (kuwa) with a wooden handle, leaning",
    "el_kaki":        "a branch with three orange persimmons and green leaves",
    "el_mugiwara":    "a round straw hat with a wide brim and a dark band",
    "el_kyuusu":      "a small Japanese ceramic teapot (kyusu) with a side handle, brown glaze",
    "el_pool":        "a small round inflatable children's paddling pool, light blue, filled with water",
    "el_ukiwa":       "a striped inflatable swim ring, red and white",
    "el_kumonosu":    "a dusty cobweb spanning a corner, thin grey threads",
    "el_dry_flower":  "a single dried brown hydrangea flower on a stem",
    "el_terebi":      "a boxy Showa-era black-and-white television with two dials and a blank grey screen",
    "el_sentakuki":   "a Showa-era top-loading washing machine with a wringer, cream and pale green",
    "el_kamidana":    "a small wooden household Shinto altar shelf (kamidana) with a tiny shrine",
    "el_suidoukan":   "a section of grey water pipe with an elbow joint, seen from the side",
    "el_baketsu":     "a tin bucket with a wire handle, seen from the side, slightly dented",
    "el_megane":      "a pair of reading glasses with thin brown frames, folded",
    "el_zabuton":     "a square Japanese floor cushion (zabuton), indigo with a plain pattern",
    "el_fuutou":      "a plain white envelope, sealed, no writing, seen at an angle",
    "el_horeizai":    "a soft blue gel ice pack with frost on it",
    "el_kame_modern": "a sleek modern unglazed clay water jar with clean straight lines and a wooden lid",
    "el_fukuro":      "a brown paper shopping bag with twine handles, standing",
    "el_tenbin":      "an old brass balance scale with two pans, level",
    "el_plug":        "an electric power plug plugged into a wall socket, cord going down",
    "el_concrete":    "a rough grey concrete wall block with a small crack, seen straight on",
    "el_netsu":       "three wavy heat shimmer lines rising upward, pale orange",
    "el_mado":        "a wooden-framed Japanese window with a lace curtain half drawn",
    "el_niwaki":      "a small round-trimmed garden tree in a low pot, green",
    "el_saifu":       "a worn brown leather wallet, closed, seen from the front",
    "el_hoshi":       "five small stars scattered, pale yellow, varying sizes",
    "el_jitensha":    "an old Japanese bicycle with a front basket, seen from the side",
    "el_akari":       "a warm glowing paper lantern lamp (andon) on a small stand",
}


def compose(obj):
    return " ".join([STYLE, f"SUBJECT: {obj.strip().rstrip('.')}.", CUTOUT, BG, NOTEXT])


def main():
    vdir = PROJ / "06_VIDEO" / B.STEM
    have = {p.stem for p in (vdir / "sticker").glob("el_*.png")}
    need = []
    for s in B.SCENES:
        for e in s.get("sup", []):
            if e not in need:
                need.append(e)
    miss = [e for e in need if e not in SPEC]
    if miss:
        print(f"🔴 sticker trong SCENES chưa có prompt: {miss}")
        return 1
    todo = [e for e in need if e not in have]
    flow, ten, blocks = [], [], ["# Prompt STICKER anime · video 25 · lô 2 (không trùng)\n\n"
                                 "🔴 nền MAGENTA thuần · 1 vật / ảnh · cắt nền: "
                                 "`tools/cutout_sticker25.py --src <folder> --apply` (điền MAP).\n"
                                 f"Đã có {len(need)-len(todo)}/{len(need)} · cần gen {len(todo)}.\n"]
    for i, e in enumerate(todo, 1):
        p = compose(SPEC[e])
        flow.append(p)
        ten.append(f"{e + '.png':<22}<- dòng {i} FLOW")
        blocks.append(f"\n## {i}. `{e}.png`\n\n```\n{p}\n```\n")
    (vdir / "sticker_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (vdir / "sticker_prompts_BLOCKS.md").write_text("".join(blocks), encoding="utf-8")
    (vdir / "sticker_prompts_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")
    print(f"✓ {len(need)} sticker dùng · {len(have & set(need))} đã có · {len(todo)} prompt mới → {vdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
