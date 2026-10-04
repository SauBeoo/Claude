# -*- coding: utf-8 -*-
r"""art_prompts_collage25.py — prompt ảnh HERO (scene) phong cách ANIME cho video 25.

⭐ user chốt 2026-08-27: *"Tao không muốn sử dụng dạng cắt giấy tao muốn dùng dạng anime"*
⇒ khung Remotion giữ nguyên (2 cast + hero giữa + sticker góc + bảng số), chỉ đổi STYLE ảnh:
   anime/watercolor-line (kiểu `remotion-vox/public/projects/hoathinh-demo/scene_01.jpeg`),
   màu ấm, nét mực mảnh, bố cục điện ảnh. KHÔNG collage, KHÔNG giấy xé, KHÔNG halftone.

Mỗi hero trong `build_remotion_25.py::SCENES` = đúng 1 prompt ở đây (đọc từ builder, không chép tay).
Luật giữ: KHÔNG chữ (banner/bảng do Remotion vẽ) · người Nhật, bối cảnh Nhật · generator trả
1376×768 ⇒ chủ thể GIỮA khung, chừa mép (hero được bo viền trắng tròn bởi `make_photocard25.py`).

CHẠY:  python tools/art_prompts_collage25.py      # → 06_VIDEO/25_*/art_prompts_photocard_{FLOW,BLOCKS,TENFILE}
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_remotion_25 as B  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]

STYLE = (
    "Japanese anime-style illustration, hand-drawn look with clean thin ink linework and soft "
    "watercolor-like cel shading, warm nostalgic Showa-era palette (cream, terracotta, indigo, "
    "warm amber light), gentle painterly textures, cinematic 16:9 composition, high detail, "
    "calm storytelling mood like a quiet slice-of-life animation film."
)
PEOPLE = (
    "Any person is JAPANESE, drawn in the same anime style with natural proportions (not chibi, "
    "not exaggerated), modest everyday Japanese clothing of the Showa era or today."
)
FRAME = (
    "Composition: the main subject large and clearly readable near the centre of the frame, "
    "background simplified so the subject stands out at a glance; leave a small quiet margin "
    "around the edges."
)
NOTEXT = ("No text, no letters, no numbers, no signs with writing, no logo, no watermark anywhere.")
MOOD = {"clay": "warm earthy terracotta tones", "indigo": "cool indigo dusk tones",
        "cream": "soft cream daylight", "mustard": "golden afternoon light",
        "red": "hot red-orange heat haze", "moss": "fresh green shade"}

# ── scene → (mood, mô tả). Key = tên hero trong SCENES. ───────────────────────
SCENE = {
    # ⭐ ẢNH MỞ ĐẦU GÂY SHOCK (user 2026-08-28) — 7 giây đầu, trước bảng 39/33. Không máu, không
    # gore (youtube-compliance §3): sức nặng đến từ bóng tối + quạt đứng im + đèn cấp cứu.
    "card_shock_yakan": ("red", "a dark Japanese apartment room at night seen from the doorway, "
        "an elderly person lying collapsed on the tatami floor beside an electric fan that stands "
        "still and unplugged, a glass of water tipped over, a telephone out of reach, and the red "
        "rotating light of an ambulance flashing in through the window onto the wall; heavy, "
        "silent, oppressive summer heat — dramatic low-key lighting"),
    "card_jaguchi": ("indigo", "an elderly Japanese hand held under a running kitchen tap, water "
        "splashing onto the back of the hand, summer heat haze wobbling in the air, a small "
        "thermometer on the windowsill"),
    "card_kame_daidokoro": ("clay", "a large rough unglazed earthenware water jar standing in the "
        "corner of an old Japanese kitchen, a wooden ladle resting on its rim, a cloth cover folded "
        "beside it, morning light through a lattice window"),
    "card_reizouko_mugicha": ("indigo", "an elderly Japanese man standing before an open modern "
        "refrigerator in a hot kitchen, one bottle of barley tea on the shelf, he wipes his "
        "forehead, heat haze around him"),
    "card_koppu_mizu": ("cream", "a single clear glass of cold water with beads of condensation on "
        "a low wooden table, a folded paper fan beside it, soft window light, inviting"),
    "card_reizouko_jikan": ("indigo", "a refrigerator and a round wall clock side by side, a warm "
        "bottle with heat wiggles being placed inside, a wall air-conditioner above with its remote "
        "lying far away on a table"),
    "card_sobo_kame": ("clay", "an old Japanese farmhouse kitchen with an earthen floor, a big "
        "unglazed clay water jar by the wall, a wooden engawa veranda and garden seen through the "
        "open doorway; nostalgic Showa calm"),
    "card_suyaki_macro": ("clay", "extreme close-up of the rough porous surface of an unglazed "
        "terracotta jar, tiny beads of water seeping out through the pores and glistening, the "
        "texture filling the frame"),
    "card_kika_netsu": ("indigo", "a clay jar with beads of water on its outer wall, soft wisps of "
        "vapour rising from the surface, gentle glowing arrows drawn outward from the wall to show "
        "heat leaving, a hand touching the cool side"),
    "card_uekibachi_futatsu": ("clay", "two plain unglazed terracotta flowerpots of different sizes, "
        "the small one nested inside the large one with damp sand between them, a bottle and two "
        "fruits inside the small pot, on a wooden garden shelf"),
    "card_yubisaki": ("clay", "close-up of an elderly Japanese fingertip touching the damp outer wall "
        "of a terracotta pot, small sparkle marks of cool surprise, the pot in a shaded garden corner"),
    "card_kaze_sukima": ("moss", "a terracotta pot loosely wrapped in a wet cloth with a visible gap, "
        "wind lines flowing through the gap, a paper fan and leafy shade above, a tightly wrapped pot "
        "small and dull in the corner"),
    "card_homecenter": ("cream", "a home-centre garden shelf stacked with rows of cheap unglazed "
        "terracotta flowerpots in several sizes, a blank price tag hanging, an elderly Japanese "
        "woman's hand picking one up"),
    "card_tenki": ("indigo", "a split scene: left a dry sunny inland landscape with a clay pot and "
        "crisp sun rays, right a humid grey rainy-season sky with heavy raindrops and the same pot "
        "looking dull; a soft divide between"),
    "card_nigeria_kyoushi": ("clay", "a West African schoolteacher in a simple shirt kneeling beside "
        "a large double clay pot in a sunlit dry village yard, eggplants and tomatoes beside it, a "
        "mud-brick house behind; same anime style"),
    "card_camp_teiden": ("indigo", "a campsite table at dusk, a cooler box open with melted ice, "
        "beside it a small unglazed clay bowl holding a drink bottle wrapped in a damp cloth, a "
        "lantern switched off, first stars"),
    "card_shigaraki": ("clay", "a Japanese pottery workshop yard with rows of unglazed clay water "
        "jars and flowerpots drying together on wooden boards, a kiln chimney behind, an elderly "
        "potter in an apron carrying one jar"),
    "card_edo_tabibito": ("cream", "an Edo-period Japanese traveller in straw hat and kimono walking "
        "a country road with a small unglazed clay flask hanging from his pack, a peddler with a "
        "shoulder pole behind, rice fields and hills"),
    "card_hishaku": ("clay", "a wooden ladle breaking the still water surface inside a large clay jar "
        "seen from above, gentle ripples, a child's small hand on the handle, cool dark water against "
        "the clay rim"),
    "card_sobo_kappogi": ("cream", "an elderly Japanese grandmother in a white kappogi apron with "
        "sleeves rolled up, laughing warmly and wiping her forehead with the back of her hand, "
        "standing by an earthen kitchen wall, soft summer light"),
    "card_gutta": ("red", "an elderly Japanese man slumped in a chair in a hot room, face flushed "
        "red, no sweat, a family member's worried hand on his shoulder, a stopped ceiling fan above; "
        "urgent, heavy heat"),
    "card_gyouzui_tarai": ("indigo", "a large wooden washtub full of water on the wooden engawa "
        "veranda of an old Japanese house, a bamboo ladle floating in it, garden greenery and a "
        "hanging wind chime, evening light"),
    "card_hada_jouhatsu": ("moss", "close-up of a bare forearm with water droplets on the skin, wind "
        "lines blowing across it and small wisps of vapour lifting off, an electric fan small in the "
        "far corner"),
    "card_hitosukui": ("indigo", "a bamboo ladle pouring a scoop of water over a bare shoulder and "
        "arm, a bright splash, a wooden washtub below, a garden fence behind"),
    "card_chuui_nurume": ("red", "a bamboo ladle with gentle warm steam beside a bucket of ice water "
        "marked with a red cross, an elderly Japanese man testing the water with his fingertips, "
        "cautious expression"),
    "card_nure_taoru": ("indigo", "a folded wet towel laid across the back of an elderly Japanese "
        "man's neck, a hand-held fan waving beside it with wind lines, a glass of water on the "
        "table; calm first-aid mood"),
    "card_showa_gyouzui": ("cream", "a Showa-era Japanese farmyard at dusk, a man with a towel at "
        "the waist rinsing his shoulders from a wooden tub, farm tools leaning on a wall, a "
        "persimmon tree, warm nostalgic light"),
    "card_yuusuzumi": ("moss", "an elderly Japanese man in a straw hat sitting on an engawa veranda "
        "in the evening fanning himself with an uchiwa, a mosquito coil smoking on the step, a wooden "
        "tub drying against the wall, first stars"),
    "card_share_kazoku": ("cream", "an elderly Japanese couple sitting at a low table looking "
        "together at one smartphone held between them, a teapot and two cups, a small clay jar in "
        "the background corner; warm and calm"),
    "card_vinyl_pool": ("indigo", "a small round inflatable children's paddling pool on a suburban "
        "Japanese balcony with a child's legs splashing, and faintly behind it the ghost of a wooden "
        "washtub of the same shape"),
    "card_kieta_dougu": ("cream", "a dusty clay water jar pushed into the corner of a modern kitchen "
        "behind a shiny refrigerator, a dried flower stuck in it as decoration, cobwebs, forgotten"),
    "card_sanshu_jingi": ("indigo", "three Showa-era appliances standing proudly in a row on a tatami "
        "room floor — a rounded refrigerator, a top-loading washing machine, a boxy black-and-white "
        "television — with sparkle marks and a small family admiring them"),
    "card_suidou": ("indigo", "a shiny new kitchen tap gushing water into a sink in a Showa-era "
        "kitchen, an old clay water jar standing idle in the corner with a cloth over it, a woman "
        "turning the tap with delight"),
    "card_mizu_soba": ("cream", "an elderly Japanese woman resting on a sofa in summer with a glass of "
        "water within arm's reach on a side table, a small clay jar beside the glass, sunlight and a "
        "hand fan"),
    "card_denkidai": ("clay", "a blank electricity bill envelope lying beside an air-conditioner "
        "remote and a stack of coins, a rising red arrow, a shop shelf of cooling gel packs faded "
        "behind"),
    "card_kamamoto_gendai": ("clay", "a modern Japanese pottery shop display of sleek unglazed clay "
        "water jars with clean lines, a blank price card in front of one, a young couple looking at "
        "it, warm shop lighting"),
    "card_ryouhou": ("cream", "a modern refrigerator and a small unglazed clay jar standing side by "
        "side on a kitchen counter as equals, a glass of water in front of each, morning light"),
    "card_suidoukan": ("indigo", "a cross-section view of a water pipe running through sunlit ground "
        "and a hot concrete wall into a house, heat wiggles from the soil warming the pipe, a tap at "
        "the end dripping lukewarm water"),
    "card_kame_tarai_ryouyou": ("cream", "a small unglazed clay jar on a modern kitchen counter and, "
        "through the window, a wooden washtub filled with water in a small garden; one calm "
        "present-day Japanese home"),
    "card_zero_en": ("moss", "an elderly Japanese couple on an engawa in the evening, one fanning "
        "with an uchiwa, a clay jar and a glass of water between them, a switched-off air conditioner "
        "on the wall behind, contented"),
    "card_jikka_kioku": ("cream", "an old Japanese family house seen from the garden at twilight, an "
        "engawa with a wooden tub and a clay jar by the kitchen door, a bicycle leaning on the fence, "
        "warm window light; nostalgic closing image"),
}


def compose(desc, mood):
    d = desc.strip().rstrip(".;") + "."
    parts = [STYLE, f"SCENE: {d}", f"Lighting and colour: {MOOD[mood]}."]
    if any(w in d.lower() for w in ("man", "woman", "men", "women", "person", "people", "hand",
                                    "couple", "figure", "child", "teacher", "potter",
                                    "traveller", "grandmother", "family")):
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
    flow, ten, blocks = [], [], ["# Prompt HERO anime · video 25\n\n",
                                 "Gen xong → `python tools/make_photocard25.py --src <folder> --apply` "
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
