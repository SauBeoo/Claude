# -*- coding: utf-8 -*-
r"""sticker_prompts_collage26.py — prompt STICKER (từng vật) phong cách ANIME, nền MAGENTA, video 26.

Chép khuôn `sticker_prompts_collage25.py` nguyên vẹn (STYLE/CUTOUT/BG/NOTEXT), chỉ đổi nội dung
SPEC theo 92 sticker của `build_remotion_26.py::SCENES` (đọc từ builder, không chép tay).

🔴 Nền MAGENTA #FF00FF thuần · ĐÚNG 1 vật / ảnh · cắt nền: `tools/cutout_sticker26.py --src <folder> --apply`.

CHẠY:  python tools/sticker_prompts_collage26.py
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_remotion_26 as B  # noqa: E402

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
    "el_yubisaki":        "an elderly fingertip touching a damp wooden surface, seen close up",
    "el_shimi_ten":       "a cluster of small dark grey mould spots on a pale wooden surface",
    "el_mushimegane":     "a round magnifying glass with a dark wooden handle, lens clear",
    "el_yubi_sasu":       "an elderly hand with one finger pointing downward, seen from the side",
    "el_neko_sakeru":     "a small Japanese cat turning away and walking off, tail raised",
    "el_juushi_curtain":  "a rolled sheet of smooth glossy plastic curtain material, blank",
    "el_senzai_bin":      "a plain plastic detergent bottle with a pump top, blank label",
    "el_kanki_mado":      "a small window cracked open with a thin arrow showing air flowing out",
    "el_kami_ichimai":    "a single flat sheet of white washi paper, glowing faintly at the edges",
    "el_hatena_ai":       "a rounded question mark shape, indigo blue with a soft glow",
    "el_noren":           "a traditional Japanese noren doorway curtain with a plain indigo pattern",
    "el_niwaki":          "a small round-trimmed garden tree in a low pot, green",
    "el_shouji_koma":     "a small single wooden-framed shoji screen panel, standing alone",
    "el_hatena_dai":      "a large bold question mark, cream coloured with a brown outline",
    "el_ondokei":         "an old glass mercury thermometer with a red column, no numbers on its scale",
    "el_mado_danmen":     "a cross-section diagram-style illustration of a window pane with a thin "
                          "paper layer beside it and a glowing air gap between them",
    "el_taiyou_ya":       "a warm bright cartoon sun with soft rays, amber and cream, slightly dimmed "
                          "as if partially blocked",
    "el_yajirushi_ao":    "a bold curved blue arrow pointing downward, simple and clean",
    "el_kutsushita":      "a pair of thick warm knitted socks, cream colour, folded together",
    "el_kaze_samu":       "three thin wavy blue cold-draft lines, like a chilly breeze",
    "el_purasuchikku_maki": "a rolled sheet of shiny smooth plastic material standing upright, blank",
    "el_kagayaki":        "a cluster of small bright sparkle shapes, pale gold, shiny",
    "el_nefuda_shiro":    "a blank white price tag on a string, rectangular",
    "el_hoshi_kagayaki":  "a cluster of four sparkle stars of different sizes, golden yellow",
    "el_senni_kirakira":  "a soft cluster of thin glowing fibre-like threads with tiny sparkles woven "
                          "through them",
    "el_iki_moya":        "three soft curling wisps of pale mist, gentle and breath-like",
    "el_kensabikyou":     "a small round magnifying glass with a thin metal handle, lens clear",
    "el_shitsuke_moya":   "a soft thin haze of pale blue vapour drifting sideways",
    "el_suiteki_retsu":   "a row of small clear water droplets trickling down a vertical surface",
    "el_atatakai_kuuki":  "three soft wavy orange heat-shimmer lines rising upward",
    "el_kaaten_nunoji":   "a swatch of smooth plain fabric curtain material, folded, blank",
    "el_toho_kao":        "a small round speech-bubble-like shape with a soft downcast crescent "
                          "expression drawn simply inside it",
    "el_shitsudokei":     "a small round analogue hygrometer dial with a plain needle, no numbers",
    "el_mado_kanki":      "a wooden-framed window opened slightly with a small gap showing",
    "el_te_yasashiku":    "two hands gently cupped together as if holding something delicate",
    "el_kami_kagayaki":   "a single sheet of washi paper glowing warmly at its centre",
    "el_kirifuki":        "a small clear spray bottle with a pump nozzle, half filled with water",
    "el_nori_bake":       "a wide flat paste brush with soft bristles, wooden handle",
    "el_taiko_kawa":      "a round taut drum skin (taiko) surface, seen close up, smooth and tight",
    "el_kansou_kage":     "a paper screen standing upright in dappled shade, seen from the side",
    "el_kirifuki_bin":    "a small glass spray bottle filled with clear water, blank label",
    "el_pin_to":          "a small taut rectangle of paper shown perfectly flat and wrinkle-free, "
                          "glowing softly",
    "el_yuki_mado":       "a snow-covered window ledge seen from outside, thick white snow, cold blue "
                          "light",
    "el_kumiko_ryoumen":  "a wooden lattice frame (kumiko) shown with paper visible on both the front "
                          "and back faces, cut-away style",
    "el_daiso_kago":      "a small shopping basket with a single roll of paper inside, blank label",
    "el_kattaa2":         "a plain cutter knife with a fresh silver blade, retracted handle",
    "el_taiyou_nishi":    "a warm low afternoon sun with long golden rays, setting toward one side",
    "el_kouyoku_kami":    "a rectangle of paper slightly yellowed at one edge compared to the rest, "
                          "which stays crisp white",
    "el_kattaa_ha":       "a cutter knife with a fresh new blade extended, shown carefully held",
    "el_hikari_kazashi":  "a rectangle of pale paper held up toward soft light, a faint uneven patch "
                          "visible through it",
    "el_taoru_nure":      "a folded damp white hand towel with a few water drops on it",
    "el_airon":           "a small clothes iron standing upright, plain and simple, no cord tangle",
    "el_rousoku":         "a single short white candle, unlit, standing upright",
    "el_souji_ki":        "a small handheld vacuum cleaner nozzle attachment, simple grey plastic",
    "el_yuuhi_kage":      "a warm golden dusk light glowing through a thin sheet of paper, soft "
                          "silhouette shapes",
    "el_yubi_ana":        "a small child's finger poking gently through a torn hole in thin paper",
    "el_omoide_frame":    "a small soft-edged oval photo-frame shape with a warm faded sepia tint "
                          "inside, no picture detail, just a warm glow",
    "el_hohoemi":         "a small simple crescent-shaped warm smile drawn softly, gentle line only",
    "el_hatena_shiro":    "a large rounded question mark, plain white with a thin grey outline",
    "el_toji_mon":        "an old wooden sliding door frame, closed, seen straight on",
    "el_bushi_katana":    "a sheathed traditional Japanese sword resting horizontally on a low wooden "
                          "stand, plain and dignified",
    "el_washi_maki":      "a rolled bundle of pale handmade washi paper tied with a thin cord",
    "el_shokunin_te":     "a craftsman's weathered hand holding a small paste brush, seen close up",
    "el_gurafu_ochiru":   "a simple downward-sloping line-graph shape on a blank card, no numbers or "
                          "text, just the falling line",
    "el_shouji_ura":      "a shoji screen panel shown from the back, its wooden lattice frame visible, "
                          "turned the wrong way round",
    "el_warau_haha":      "a small simple warm laughing mouth-and-eyes shape, gentle line only, cream "
                          "colour",
    "el_smartphone_ai":   "a modern smartphone lying at a slight angle, screen blank and pale",
    "el_kyuusu_cha":      "a small Japanese ceramic teapot (kyusu) with a side handle, brown glaze",
    "el_kumo_no_su":      "a dusty cobweb spanning a corner, thin grey threads",
    "el_hokori":          "a soft grey dust cloud puff, small and light",
    "el_fuutou_kuni":     "a plain sealed white official envelope with a small formal government-style "
                          "emblem shape, no readable text",
    "el_hyou_shou":       "a small blank official certificate or form card with a soft formal border, "
                          "no readable text",
    "el_kouji_gyousha":   "a small tool belt with a measuring tape and screwdriver, construction "
                          "worker's gear, simple and neat",
    "el_uchimado_zu":     "a simple diagram-style side view of a double-pane window with a visible air "
                          "gap between two panes of glass, softly glowing",
    "el_sofubo_kage":     "two soft warm silhouette shapes of an elderly seated couple, gentle and calm",
    "el_dougu_bako":      "a small wooden tool box with a simple metal handle, closed",
    "el_garasu_nimai":    "two panes of glass shown standing slightly apart with a glowing gap between "
                          "them, side view",
    "el_kuuki_sou":       "a soft glowing vertical band of pale blue light representing a thin layer of "
                          "still air",
    "el_kaisou_moya":     "a soft hazy swirl of pale translucent mist, dreamlike and faint",
    "el_kami_hikari2":    "a single sheet of washi paper glowing warmly, seen at a slight angle, second "
                          "variant",
    "el_te_kakeru":       "a hand gently lifting a small screen panel by its wooden frame edge",
    "el_muryou_fuda":     "a small round tag or badge shape, blank, with a soft warm golden glow",
    "el_amado":           "a solid wooden rain shutter panel (amado) with metal fittings, closed and "
                          "sturdy",
    "el_kagi":            "a small old-fashioned brass door lock with a plain key, simple",
    "el_tenbin_kami_garasu": "an old brass balance scale with a small paper sheet on one pan and a "
                          "small glass pane on the other, perfectly level",
    "el_wa":              "a simple soft circular ring shape (wa), warm cream colour, symbolising "
                          "harmony",
    "el_neko_marumaru":   "a small Japanese cat curled up asleep in a round ball shape, content",
    "el_kansou_mado":     "a windowsill shown dry and clean, no droplets, warm daylight on the wood",
    "el_toikake_kumo":    "a small soft speech-bubble cloud shape with a simple question mark inside, "
                          "gentle and inviting",
    "el_comment_fukidashi": "a small rounded speech-bubble shape, blank inside, cream colour with a "
                          "thin outline",
    "el_andon_akari":     "a warm glowing paper lantern lamp (andon) on a small wooden stand, soft "
                          "amber light",
    "el_tsuki_shime":     "a thin crescent moon with two small stars, pale yellow on deep indigo "
                          "shading",
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
    flow, ten, blocks = [], [], ["# Prompt STICKER anime · video 26\n\n"
                                 "🔴 nền MAGENTA thuần · 1 vật / ảnh · cắt nền: "
                                 "`tools/cutout_sticker26.py --src <folder> --apply` (điền MAP hoặc --order).\n"
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
