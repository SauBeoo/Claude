# -*- coding: utf-8 -*-
r"""art_prompts_collage26.py — prompt ảnh HERO (scene) phong cách ANIME cho video 26 (障子).

Chép khuôn `art_prompts_collage25.py` (STYLE/PEOPLE/FRAME/NOTEXT giữ nguyên), chỉ đổi nội dung
SCENE theo 41 hero của `build_remotion_26.py::SCENES` (đọc từ builder, không chép tay).

CHẠY:  python tools/art_prompts_collage26.py      # → 06_VIDEO/26_*/art_prompts_photocard_{FLOW,BLOCKS,TENFILE}
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_remotion_26 as B  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]

STYLE = (
    "Japanese anime-style illustration, hand-drawn look with clean thin ink linework and soft "
    "watercolor-like cel shading, warm nostalgic palette (cream, terracotta, indigo, warm amber "
    "light), gentle painterly textures, cinematic 16:9 composition, high detail, calm storytelling "
    "mood like a quiet slice-of-life animation film."
)
PEOPLE = (
    "Any person is JAPANESE, drawn in the same anime style with natural proportions (not chibi, "
    "not exaggerated), modest everyday Japanese clothing, present-day unless noted otherwise."
)
FRAME = (
    "Composition: the main subject large and clearly readable near the centre of the frame, "
    "background simplified so the subject stands out at a glance; leave a small quiet margin "
    "around the edges."
)
NOTEXT = ("No text, no letters, no numbers, no signs with writing, no logo, no watermark anywhere.")
MOOD = {"clay": "warm earthy terracotta tones", "indigo": "cool indigo dusk/night tones",
        "cream": "soft cream daylight", "mustard": "golden afternoon light",
        "red": "hot red-orange heat haze", "moss": "fresh green shade"}

# ── scene → (mood, mô tả). Key = tên hero trong SCENES. ───────────────────────
SCENE = {
    "card_mado_shimi": ("indigo", "extreme close-up of a Japanese wooden windowsill, the wood damp "
        "and dark with moisture, a woman's fingertip touching the damp spot, dim bedroom light "
        "behind, tense quiet mood"),
    "card_kabi_macro": ("indigo", "macro close-up of small dark grey-black mould spots scattered on "
        "an old wooden window frame, subtle texture, soft dim indigo light"),
    "card_curtain_koukan": ("cream", "an elderly Japanese woman removing a paper shoji screen from a "
        "window frame and hanging a smooth washable plastic curtain in its place, a cat sitting a "
        "little distance away watching warily, tatami room"),
    "card_gimon_kaji": ("cream", "an elderly Japanese woman standing puzzled in front of a kitchen "
        "shelf lined with cleaning detergent bottles, scratching her head lightly, soft daylight"),
    "card_kami_hikari": ("indigo", "a single sheet of washi paper glowing softly from within like a "
        "lantern, silhouetted against a dark window frame at dusk, mysterious and quiet"),
    "card_furui_ie_gaikan": ("cream", "an old traditional Japanese house exterior at early dawn, a "
        "noren cloth curtain by the door, a small trimmed garden tree, soft morning light"),
    "card_mitsue_utagai": ("cream", "an elderly Japanese woman standing with arms crossed, looking "
        "skeptically at a plain wooden shoji screen panel leaning against a wall, daylight room"),
    "card_mitsue_samuke": ("indigo", "an elderly Japanese woman sitting on the edge of a bed at night "
        "rubbing her own arms for warmth, a bare glass window behind her with no covering, cool dim "
        "bedroom light"),
    "card_kasoku_hikaku": ("indigo", "a side-by-side comparison: a plain paper shoji screen on the "
        "left, a shiny rolled sheet of smooth plastic curtain material on the right on a shelf, "
        "cool light"),
    "card_urikoba": ("mustard", "a home-centre shelf display of rolled tear-resistant plastic window "
        "paper products with bright blank price tags, warm shop lighting, an elderly woman's hand "
        "reaching for one confidently"),
    "card_kami_iki": ("cream", "extreme macro of washi paper fibres glowing softly as if breathing, "
        "faint wisps of mist passing through the weave, warm backlight"),
    "card_washi_sen_macro": ("indigo", "extreme macro close-up of washi paper fibres with tiny visible "
        "gaps between them, soft light passing through the gaps, delicate texture filling the frame"),
    "card_ketsuro_mado": ("indigo", "close-up of a cold glass windowpane at night with many small "
        "condensation water droplets forming and trickling down, warm room light behind"),
    "card_mitsue_kizuku": ("indigo", "an elderly Japanese woman touching a smooth plastic curtain with "
        "a regretful, realizing expression, dim cool light, quiet moment"),
    "card_shitsudokei": ("cream", "two small round hygrometers side by side on two windowsills, one in "
        "a washitsu tatami room and one in a Western-style room, soft daylight"),
    "card_shouji_taisetsu": ("cream", "a pair of hands gently holding and supporting a paper shoji "
        "panel with care, warm soft light glowing through the paper"),
    "card_shokunin_mizu": ("clay", "a Japanese craftsman's hands spraying a fine mist of water over "
        "freshly pasted white shoji paper with a small spray bottle, focused calm work"),
    "card_taiko_hari": ("moss", "a shoji paper panel drying upright in a shaded, breezy spot, the "
        "paper surface taut and smooth like a drum skin, soft shadow patterns"),
    "card_watashi_taiken": ("mustard", "a person's own hands spraying water onto shoji paper with a "
        "small spray bottle, a pleasantly surprised smile, warm afternoon light"),
    "card_taikobari_yukiguni": ("indigo", "a snow-country Japanese window seen from inside, thick snow "
        "piled outside, the wooden lattice with paper visible on both sides for extra insulation, "
        "warm room glow contrasting cold blue snow light"),
    "card_nishimuki_taiyou": ("mustard", "strong warm afternoon sun streaming through a west-facing "
        "shoji screen, the paper slightly yellowed compared to a crisp white panel nearby, golden "
        "light rays"),
    "card_kodomo_anzen": ("cream", "an adult's hands carefully cutting shoji paper with a fresh blade "
        "cutter on a low table, a small child playing safely at a distance in the same room, calm "
        "daylight"),
    "card_nori_hagasu": ("cream", "a hand peeling old washi paper cleanly off a wooden shoji frame "
        "after wiping it with a damp cloth, paper coming away smoothly, soft light"),
    "card_rousoku_shikii": ("clay", "a hand rubbing a small candle along a wooden window-sill groove "
        "(shikii), warm candlelight glow, close and intimate framing"),
    "card_kodomo_ana": ("mustard", "a child's small finger gently poking a hole in an old shoji paper "
        "screen, warm golden dusk light glowing softly through the thin paper, nostalgic mood"),
    "card_haha_natsukashi": ("cream", "a warm nostalgic memory-style portrait of a smiling elderly "
        "Japanese woman with a gentle, reminiscing expression, soft cream light, slightly dreamlike "
        "framing"),
    "card_nazo_toi": ("indigo", "a large soft glowing question mark hovering over an old Japanese "
        "sliding door entrance, quiet mysterious dusk mood"),
    "card_bushi_akari_shouji": ("clay", "an elegant Heian/samurai-era Japanese aristocratic room "
        "interior with a fine wooden-lattice akari-shoji screen glowing with soft light, refined and "
        "wealthy atmosphere, warm interior light"),
    "card_watashi_machigai": ("mustard", "a person closing a shoji screen the wrong way round by "
        "mistake, an elderly mother figure laughing warmly beside them, playful embarrassed mood, "
        "soft home light"),
    "card_share_onegai": ("cream", "an elderly Japanese couple sitting at a low table, one hand near a "
        "smartphone on the table, a small teapot and two cups beside it, warm cosy living room light"),
    "card_kieta_dougu": ("indigo", "an old shoji screen panel pushed into a dim storeroom corner, "
        "faint dust and a thin cobweb in the corner, forgotten and quiet, cool dim light"),
    "card_kuni_uchimado": ("indigo", "a stack of official-looking government pamphlets and a sealed "
        "envelope about window renovation subsidies on a desk, formal cool lighting, a modern window "
        "in the background"),
    "card_sofubo_shouji": ("cream", "a contented elderly Japanese couple sitting calmly in a warm "
        "tatami room with shoji screens glowing softly with daylight, relaxed and at ease"),
    "card_kuuki_sou_hikaku": ("indigo", "a diagram-like illustrative scene: on one side a modern double-"
        "pane glass window with a glowing air gap between the panes, on the other side a shoji screen "
        "standing slightly away from a glass window with a similar glowing air gap between them, "
        "symmetrical, soft glowing blue light showing the air layer in both"),
    "card_kaisou_boutou": ("indigo", "a soft dreamlike echo of a damp windowsill scene, faint hazy "
        "double-exposure feeling, quiet realization mood, cool soft light"),
    "card_muryou_kaifuku": ("cream", "a pair of hands gently lifting a paper shoji screen and hanging "
        "it back onto its wooden track by a window, warm daylight, satisfying calm action"),
    "card_bouhan_amado": ("clay", "a solid wooden rain shutter (amado) standing beside a delicate paper "
        "shoji screen, a small brass lock visible on the shutter, contrast between sturdy and "
        "delicate, neutral daylight"),
    "card_kumiawase": ("cream", "a window shown with both a glass pane and a soft paper shoji screen "
        "working together in harmony, warm evening light glowing through both, peaceful balanced "
        "composition"),
    "card_mitsue_kaiketsu": ("cream", "an elderly Japanese woman happily touching a now-dry windowsill "
        "with a content smile, a cat curled up asleep beside her on the floor, warm soft daylight"),
    "card_shichou_toikake": ("cream", "a quiet, gentle question-mark shaped cloud drifting above a "
        "generic Japanese home window, inviting reflective mood, soft daylight"),
    "card_shimei_tojiru": ("indigo", "a warm glowing paper lantern (andon) light shining softly through "
        "a paper shoji door at night, calm and peaceful closing image, a thin crescent moon outside"),
}


def compose(desc, mood):
    d = desc.strip().rstrip(".;") + "."
    parts = [STYLE, f"SCENE: {d}", f"Lighting and colour: {MOOD[mood]}."]
    if any(w in d.lower() for w in ("man", "woman", "men", "women", "person", "people", "hand",
                                    "couple", "figure", "child", "elderly", "craftsman", "mother")):
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
    flow, ten, blocks = [], [], ["# Prompt HERO anime · video 26\n\n",
                                 "Gen xong → `python tools/make_photocard26.py --src <folder> --apply` "
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
