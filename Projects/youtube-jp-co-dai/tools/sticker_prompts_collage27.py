# -*- coding: utf-8 -*-
r"""sticker_prompts_collage27.py — prompt STICKER (từng vật) phong cách ANIME, nền MAGENTA, video 27.

Chép khuôn `sticker_prompts_collage26.py` nguyên vẹn (STYLE/CUTOUT/BG/NOTEXT), chỉ đổi nội dung
SPEC theo 114 sticker của `build_remotion_27.py::SCENES` (đọc từ builder, không chép tay).

🔴 Nền MAGENTA #FF00FF thuần · ĐÚNG 1 vật / ảnh · cắt nền: `tools/cutout_sticker27.py --src <folder> --apply`.

CHẠY:  python tools/sticker_prompts_collage27.py
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_remotion_27 as B  # noqa: E402

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
    "el_ashimoto_gura":   "an elderly foot in a house sock standing on the tilted edge of a small "
                          "step-stool, seen close up, slight loss of balance",
    "el_kanki_mado_yogore": "a small kitchen range-hood vent grille with dark grease staining around "
                          "its edges",
    "el_honoo_kage":      "a small dangerous orange flame silhouette flickering, simple and stylised",
    "el_kegura_tumu":     "a soft grey dust-and-soot puff drifting, small and light",
    "el_tokei_matsu":     "a simple round clock face with no numbers, its hands paused, waiting mood",
    "el_yubikiri":        "two small fingers linked together in a pinky-promise gesture",
    "el_kaki_pen":        "an old-fashioned fountain pen resting on a blank open notebook page",
    "el_hon_hirogaru":    "an old book lying open with its pages fanned out, soft warm glow rising "
                          "from the pages",
    "el_radio_reizouko":  "a small vintage radio sitting on top of a white refrigerator, warm glow",
    "el_onryou_dial":     "a round volume knob dial on an old radio, turned up high",
    "el_hatena_mimi":     "a large soft question mark shaped like a human ear, pale and curious",
    "el_tissue_hirahira":"a single white tissue paper sheet fluttering loosely in mid-air, not sticking "
                          "to anything",
    "el_suikomiguchi":    "a round metal fan intake grille with faint air-flow arrow lines around it",
    "el_calendar_hantoshi": "a wall calendar page showing six months flipped back, a faint change "
                          "highlighted",
    "el_juusou_bin":      "a plain cardboard box of baking soda powder, blank label, lid half open",
    "el_zoukin":          "a folded grey cleaning cloth, slightly damp and worn",
    "el_yukazuwari":      "a person sitting cross-legged directly on a kitchen floor, tired posture, "
                          "seen from behind",
    "el_tenbin_yaku":     "an old brass balance scale with a small medicine bottle on the lighter side",
    "el_senzai_yajirushi": "a dish detergent bottle with a small red arrow pointing at it and a soft "
                          "question mark beside it",
    "el_hatena_daikizu":  "a large bold cream-coloured question mark with a thin brown outline",
    "el_yubisaki_up":     "an extreme close-up of a single fingertip pressed against a dark hard "
                          "glossy surface",
    "el_kagami_han":      "a small round hand mirror reflecting a faint puzzled expression",
    "el_bunshi_te":       "two small golden droplet shapes with tiny cartoon hands linking together",
    "el_kemuri_abura":    "a thin curl of pale oily smoke rising from a stovetop pan",
    "el_ita_hikari":      "a thin dark glossy plastic-like sheet catching a cold light reflection",
    "el_hokori_maru":     "a small round grey dust-and-lint ball, fuzzy texture",
    "el_sen_ori":         "a few thin fabric fibres tangled together in a small clump",
    "el_ken_kakera":      "a small broken shard of dark hardened plastic-like material",
    "el_te_kobushi":      "a clenched fist raised in a determined, ready-for-battle pose",
    "el_te_tsurutsuru":   "a hand sliding smoothly across a slick glassy surface, unable to grip it",
    "el_mizu_shizuku2":   "a single clear water droplet suspended mid-fall, second variant",
    "el_hanko_shorui":    "an official document page with a small red hanko stamp mark on it, no "
                          "readable text",
    "el_houki":           "a traditional Japanese broom (houki) leaning against a wall",
    "el_karendaa_batsu":  "a wall calendar with three days circled in red and crossed out with an X",
    "el_hikari_hourensou": "a glowing beaker of clear liquid emitting a soft radiant halo of light",
    "el_flask_alkali":    "a laboratory-style glass flask filled with a clear glowing liquid, simple "
                          "and clean",
    "el_yajirushi_henka": "a curved bold arrow transforming from an orange droplet shape into a white "
                          "soap-bubble shape",
    "el_awa_sekken":      "a small cluster of soft round white soap bubbles, glossy and clean",
    "el_te_douguzu":      "a hand holding a small scrubbing brush, but set down and unused, resting",
    "el_hikari_bakuhatsu": "a small burst of soft golden sparkle light radiating outward, magical",
    "el_hi_kamado":       "small glowing embers deep inside an old clay kamado stove firebox",
    "el_hai_yama":        "a small mound of soft pale grey wood ash",
    "el_hakari_dejitaru":"a simple round pH-scale gauge dial with a needle pointing near its upper end, "
                          "no numbers printed",
    "el_bowl_stainless":  "a plain stainless steel mixing bowl, empty and shiny",
    "el_oyu_yugeki":      "a kettle pouring a stream of steaming hot water, visible steam curls",
    "el_migakiko_soko":   "a thick dark sediment layer settled at the bottom of a clear glass jar",
    "el_koppu_sumu":      "a clear glass cup with clean settled liquid on top, sediment below",
    "el_hane_oyu":        "a detached metal fan blade partly submerged in a basin of warm water",
    "el_nuno_fuku":       "a cloth soaked in clear liquid, wiping across a dark stained surface",
    "el_tokei_15fun":     "a small kitchen timer clock showing a short quarter-hour segment shaded in",
    "el_suji_nokoru":     "a faint streaky smear mark left behind on a wiped metal surface",
    "el_hai_atsui":       "a small mound of ash with faint heat-shimmer lines still rising from it",
    "el_yubisaki_hai":    "a fingertip pressed gently into a mound of cool soft ash, fine powder "
                          "clinging to the skin",
    "el_kamado_asa":      "an old kamado stove lid opened at early morning, a thin white layer visible "
                          "on the ash inside",
    "el_gomu_tebukuro2":  "a pair of thick yellow rubber gloves laid out neatly, ready to be worn",
    "el_kanki_mado2":     "a small kitchen window propped open with a soft breeze line drawn beside it",
    "el_megusuri":        "a small first-aid eye-wash bottle standing upright, plain and simple",
    "el_arumi_hikari":    "a shiny curved aluminium panel piece catching a bright cold light reflection",
    "el_senzai_chuusei2": "a small bottle of neutral pH dish detergent, second variant, plain label",
    "el_batsu_maaku":     "a bold red X cross mark, simple and clear",
    "el_katakushi_nuno":  "a well-wrung damp cloth folded neatly, ready for careful wiping",
    "el_supuun_koya":     "a small measuring spoon resting beside a compact travel-size bottle",
    "el_mizu500ml":       "a plain clear plastic bottle filled with water, blank label, mid-size",
    "el_kitchen_paper":   "a folded sheet of kitchen paper towel, slightly damp, ready to be applied",
    "el_yubi_kanshoku":   "a fingertip pressing gently into a softened surface, sinking in slightly",
    "el_hatena_hai":      "a soft grey question mark shape rising like a wisp of ash smoke",
    "el_smartphone_share": "a modern smartphone lying at a slight angle showing a simple glowing heart "
                          "icon on its blank screen",
    "el_ohanashi_kotoba": "a small rounded speech-bubble shape, warm cream colour, blank inside",
    "el_haato_iine":      "a small glowing red heart shape with a soft thumbs-up shape beside it",
    "el_hai_bako":        "a small wooden box filled with grey ash, carried on a merchant's shoulder "
                          "strap",
    "el_kaminuno_hai":    "a merchant's headscarf and hair dusted grey with fine ash powder",
    "el_nagaya_michi":    "a narrow Edo-period wooden row-house lane path, seen from low angle, sepia "
                          "morning light",
    "el_kane_de":         "a small pile of old Edo-period coins glinting softly",
    "el_kokoro_tobu":     "a soft glowing thought-bubble shape with a small sparkle inside, imaginative "
                          "mood",
    "el_tarai_sentaku":   "a round wooden Edo-period washtub (tarai) with clothes being hand-washed "
                          "inside it",
    "el_sen_kuchi":       "a small wooden tap spout at the base of a barrel, a thin stream of clear "
                          "liquid dripping from it",
    "el_okane_saifu":     "a plain leather wallet open, showing a few paper bills and coins inside",
    "el_gyousha_denwa":   "a service worker's hand holding a phone receiver, small tool bag beside them",
    "el_zeni_bukuro":     "a small drawstring pouch of coins, held out in an offering gesture",
    "el_te_to_okane":     "a hand releasing a pouch of coins with the other hand receiving a bag of "
                          "grease waste, simple mirrored gesture",
    "el_saifu_kawaru":    "an open wallet transforming between coins going out and coins staying in, "
                          "soft glowing arrow between the two states",
    "el_hane_maku":       "a thin dark film slowly narrowing the round opening of a fan blade housing",
    "el_kaze_hosoi":      "three thin wavy air-flow lines, noticeably narrower and weaker than before",
    "el_agemono_nioi":    "a soft trail of pale golden cooking-oil scent lines drifting upward from a "
                          "frying pan",
    "el_kabegami_shimi":  "a small patch of ceiling wallpaper shown slightly yellowed compared to the "
                          "surrounding clean area",
    "el_calendar_3nen":   "a wall calendar with three overlapping year numbers fading gently into one "
                          "another, no other text",
    "el_hatena_shousetsu": "a small soft question mark resting on top of a stack of simple building-"
                          "block shapes, foundational mood",
    "el_te_ita":          "a hand pressing gently on a thin dark hardened crust, testing its firmness",
    "el_kuuki_toki":      "a small clock face paired with a soft floating air-current swirl beside it",
    "el_netsu_kioku":     "a small stovetop flame icon paired with a faint heat-shimmer memory trail",
    "el_abura_tsubu":     "a cluster of tiny loose golden oil droplets, still separate and unconnected",
    "el_nuno_kawaita":    "a single dry soft cloth, clean and ready, held out in a hand",
    "el_akujiru_mini":    "a tiny miniature glass jar of clear ash-lye liquid, small icon scale",
    "el_oyu_mini":        "a tiny miniature kettle with a small curl of steam, small icon scale",
    "el_kokoro_te":       "a soft glowing heart shape cradled gently between two open hands",
    "el_fumidai_muyou":   "a small step-stool with a soft red slash line drawn across it, no longer "
                          "needed",
    "el_kaidan_anzen":    "a sturdy step-ladder standing safely and evenly on flat ground, stable "
                          "reassuring pose",
    "el_kazu_kaunto":     "a small row of tally marks glowing softly, counting upward",
    "el_taoru_hankaketa":  "a single worn towel draped halfway over a towel rail, within easy reach",
    "el_te_todoku":       "a relaxed hand reaching out and easily touching a nearby towel without "
                          "walking anywhere",
    "el_radio_onryou_futuu": "a small radio glowing warmly with clean even sound-wave lines, volume "
                          "dial back to a normal middle position",
    "el_akujiru_nuno":    "a cloth freshly wrung out from a jar of clear ash-lye liquid, slightly damp",
    "el_neko_kao_niru":   "a small Japanese cat's face with a calm content closed-eye expression, "
                          "gentle and warm",
    "el_arumi_batsu":     "a shiny aluminium panel piece with a small red X warning mark beside it",
    "el_hai_nashi_ie":    "a modern kitchen stove with a small soft grey X where an old ash pile would "
                          "have been, ash no longer present",
    "el_ita_sudeni":      "a thin dark hardened crust already fully formed on a fan blade, unaffected "
                          "by a nearby dry cloth",
    "el_tokei_osoi":      "a round clock face with hands moving very slowly, a soft drowsy waiting mood",
    "el_kutsu_takai":     "a tall step-ladder shoe rung shown from a high dizzying angle looking down",
    "el_comment_fukidashi2": "a small rounded speech-bubble shape, blank inside, warm cream colour, "
                          "second variant",
    "el_chiiki_hai":      "a small stylised map pin shape with a soft ash-grey glow inside it",
    "el_tobira_hikari":   "a softly glowing doorway crack letting warm light spill through into "
                          "darkness",
    "el_andon_akari2":    "a warm glowing paper lantern lamp (andon) on a small wooden stand, second "
                          "variant, soft amber light",
    "el_tsuki_shime2":    "a thin crescent moon with two small stars, pale yellow on deep indigo "
                          "shading, second variant",
    "el_hai_saigo":       "a final small handful of soft grey ash resting quietly in an open palm, calm "
                          "closing mood",
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
    flow, ten, blocks = [], [], ["# Prompt STICKER anime · video 27\n\n"
                                 "🔴 nền MAGENTA thuần · 1 vật / ảnh · cắt nền: "
                                 "`tools/cutout_sticker27.py --src <folder> --apply` (điền MAP hoặc --order).\n"
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
