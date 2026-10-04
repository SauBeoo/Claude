# -*- coding: utf-8 -*-
r"""Dung SLIDES + 3 file prompt anh cho video 15 (生姜).

    python tools\build_slides_15.py

Xuat:
  04_SCRIPTS/15_shoga-tabekata_SLIDES_photo.json   (renderer doc)
  06_VIDEO/15_shoga-tabekata/slide_prompts_FLOW.txt     (1 prompt / 1 DONG -> bom vao extension)
  06_VIDEO/15_shoga-tabekata/slide_prompts_TENFILE.txt  (ten file <-> moc giay <-> cue)
  06_VIDEO/15_shoga-tabekata/slide_prompts_BLOCKS.md    (ban nguoi doc)

Luat da ap:
  - match = nguyen van 1 DONG trong _TTS.md (bo dau cau cuoi) -> chac chan la substring
  - moi entry cach nhau >= 6 giay, mat do <= 6 doi hinh/phut  (audience-45plus.md §2)
  - entry 0 = CHU THE cua bai (gung mai tren dau phu lanh)     (media-library.md §2.0)
  - moi prompt ket bang CUNG MOT khoi STYLE nguyen van -> 83 anh dong nhat
  - nhan vat ヨシ子 dung CUNG MOT cau ta o moi slot -> nhan ra la mot nguoi
  - moi prompt co "no text, no letters, no numbers" (chu Nhat gen ra nat net)
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "15_shoga-tabekata_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "15_shoga-tabekata_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "15_shoga-tabekata"

CPS, PER_LINE = 4.49, 0.25

STYLE = ("photorealistic documentary photography, Japanese home kitchen, warm natural "
         "window light from the left, soft shadows, shallow depth of field, muted deep "
         "navy and warm amber accents, calm and clean composition, no people unless "
         "stated, no text, no letters, no numbers, no watermark, no logo")

CHAR = ("a Japanese woman in her late seventies, silver hair in a small neat bun, pale "
        "grey cardigan over a beige blouse, gentle tired eyes, no glasses")
DAUGHTER = "her daughter in her early fifties, short dark hair, navy blouse"

# (line_index, rank, prompt_core)
PLAN = [
    # ── COLD OPEN ───────────────────────────────────────────────────────────
    (0, "", "extreme close-up of a block of chilled silken tofu on a small white plate, a generous mound of freshly grated ginger sitting on top, cold water droplets on the plate, chopsticks resting beside"),
    (4, "", "a rice bowl on a dining table with exactly half the rice still left in it, chopsticks laid across the rim, one person's place setting only"),
    (6, "", "an elderly woman's hand gripping the edge of a kitchen counter as she pushes herself up to stand, shot from behind at hip height, face not visible"),
    (9, "", "a pair of outdoor sandals left unused on the entryway step of a Japanese house, closed front door behind them, a thin elderly hand resting on the door frame, thin daylight"),
    (12, "", "a pot of gently simmering dashi broth with thin ginger slices swirling in it, steam rising, seen slightly from above"),
    (14, "", "an elderly hand lifting chopsticks holding a piece of grilled fish, a steaming bowl of miso soup beside it on the tray"),
    # ── ITEM 1 ──────────────────────────────────────────────────────────────
    (19, "一つめ", "a finished bowl of miso soup on a lacquer tray with a small heap of raw grated ginger sitting on the surface, untouched, no steam from the ginger"),
    (23, "一つめ", "thin ginger slices being dropped from fingertips into a pot at the very start of simmering root vegetables"),
    (25, "一つめ", "macro of a simmering broth surface with two ginger slices among tiny bubbles, warm amber tone"),
    (28, "一つめ", "an elderly person holding a bowl of hot soup close to the chest with both hands, steam drifting up past the collar, face not shown"),
    (30, "一つめ", "a mound of grated ginger drying out on a cold white plate on a counter, no steam anywhere, cool blue-grey light"),
    (34, "一つめ", "steam rising thickly off a freshly filled bowl of miso soup on a wooden table, warm backlight through the steam"),
    (37, "一つめ", "a squeeze tube of ginger paste standing in the door pocket of an open refrigerator, other condiment bottles around it, cold interior light"),
    (40, "一つめ", "close-up of a hand squeezing ginger paste from a plastic squeeze tube into a steaming bowl of miso soup, the tube clearly visible and central, steam rising from the bowl"),
    # ── PERSONA ─────────────────────────────────────────────────────────────
    (47, "", "a tidy Japanese home kitchen in warm morning light, apron hanging on a hook, a pot on the stove, nobody in the frame"),
    (54, "", "a small notepad and a pencil resting on a kitchen table beside a teacup of tea, blank paper, no writing visible"),
    # ── ITEM 2 ──────────────────────────────────────────────────────────────
    (56, "二つめ", "a wooden cutting board with two separate piles of ginger: one of thick chunky slices, one of paper-thin translucent slices"),
    (61, "二つめ", "extreme close-up of chopsticks holding a thick slice of ginger just above a bowl of soup, the slice snapped in half to reveal a pale raw uncooked centre against the darker cooked outer rim, the broken cross-section fills the frame"),
    (64, "二つめ", "a single paper-thin ginger slice held up between two fingertips against window light, so thin it is translucent"),
    (66, "二つめ", "two hands drawing a kitchen knife backwards across a ginger rhizome on a wooden board, thin slice separating"),
    (68, "二つめ", "macro cross-section of a cut ginger rhizome showing the fibrous layer just beneath the skin, water beading on the cut face"),
    (70, "二つめ", "hands scrubbing a knobbly ginger rhizome with an old worn bristle brush under running water in a stainless sink"),
    (75, "二つめ", "looking straight down into a bowl of miso soup with two skin-on ginger slices resting at the bottom, tofu and wakame around them"),
    (78, "二つめ", "an elderly person's cupped hands holding a warm bowl against the chest, shoulders relaxed, eyes closed, face partly out of frame"),
    # ── ANECDOTE 1 ──────────────────────────────────────────────────────────
    (82, "", f"portrait of {CHAR}, seated at a small dining table beside a window, hands folded on the table"),
    (84, "", "extreme close-up, a small round damp sponge sitting in a shallow round metal tin fills the centre of the frame, placed on a worn wooden shelf beside an old lidded sewing box, the wet sponge clearly the subject"),
    (87, "", "a single-person summer supper on a small table: chilled tofu topped with grated ginger, a small bowl of rice, nothing else"),
    (89, "", f"{CHAR}, seated at the table, a rice bowl still half full pushed slightly away from her, chopsticks set down"),
    (92, "", f"{CHAR} gripping the kitchen counter edge as she stands up, {DAUGHTER} watching quietly from the doorway behind her"),
    (95, "", "a hand pulling open a kitchen drawer, the contents still in shadow and unclear, low evening light"),
    # ── ITEM 3 ──────────────────────────────────────────────────────────────
    (98, "三つめ", "raw grated ginger heaped on chilled tofu, heavy condensation on the plate, cool bluish light, no steam"),
    (100, "三つめ", "a summer table with three cold dishes: chilled tofu, cold somen noodles in a glass bowl, a glass of iced barley tea"),
    (102, "三つめ", "close-up of an elderly temple and cheek with a film of sweat drying, an electric fan blurred in the background, faint chill in the light"),
    (103, "三つめ", "an elderly person sitting in an air-conditioned room with a thin blanket over the knees, arms crossed for warmth"),
    (107, "三つめ", "a seated person's hand touching their own bare ankle on a tatami floor, testing the temperature"),
    (112, "三つめ", "the same summer table of cold dishes, now with one steaming bowl of miso soup added beside them, steam contrasting with the condensation"),
    (116, "三つめ", "cold somen noodles in a glass bowl with a very generous mound of raw grated ginger on top, ice cubes visible"),
    # ── GENTEN ──────────────────────────────────────────────────────────────
    (119, "", "a plain official government booklet lying open on a kitchen table, pages out of focus and completely unreadable, reading glasses beside it"),
    (120, "", "a hand turning a page of that plain booklet, the print blurred beyond reading, warm lamp light"),
    (122, "", "an elderly hand and a younger hand resting together on a table, quiet and supportive, no faces"),
    (124, "", "a small kitchen scale on the counter with one piece of raw fish on the tray, the dial face blurred and unreadable"),
    (126, "", "one grilled fish fillet plated as a single serving on a simple ceramic dish"),
    (131, "", "a ginger rhizome sitting in a vegetable basket among a carrot, a daikon radish and an onion"),
    # ── CTA ─────────────────────────────────────────────────────────────────
    (135, "", "a warm kitchen table set with two teacups facing each other, afternoon light, a feeling of sharing"),
    # ── ITEM 4 ──────────────────────────────────────────────────────────────
    (140, "四つめ", "an unreasonably large mound of grated ginger filling a small plate, far more than one serving"),
    (144, "四つめ", "three ginger rhizomes lined up on a counter, two of them grated part-way down and left half-used"),
    (146, "四つめ", "a low blue gas flame burning under a pot on a stove, seen from the side in a dim kitchen"),
    (149, "四つめ", "an elderly person pressing one palm flat against the upper abdomen while seated, mild discomfort, face not shown"),
    (151, "四つめ", "an untouched breakfast tray with rice and soup gone cold, a hand pushing the tray slightly away"),
    (152, "四つめ", "an elderly hand lifting a soup bowl to sip the broth first, a small dish of grated ginger waiting beside it"),
    (154, "四つめ", "an elderly hand resting still on the table beside an almost full plate of food, soft low evening light"),
    (158, "四つめ", "exactly three thin ginger slices arranged on a small white dish, nothing else on the dish"),
    # ── 生姜湯 ──────────────────────────────────────────────────────────────
    (168, "", "a plain paper sachet of instant powdered ginger drink beside a teacup of hot water, sachet completely blank with no printing"),
    (170, "", "a hand turning that blank sachet over to look at its back, surface plain with no printing at all"),
    (172, "", "extreme close-up of a teaspoon heaped high with white granulated sugar, held in a hand directly above a teacup of pale ginger drink, individual sugar grains visible, the spoon of sugar fills the centre of the frame"),
    (177, "", "reading glasses resting on top of the blank sachet on a kitchen table, close-up"),
    # ── ANECDOTE 2 ──────────────────────────────────────────────────────────
    (181, "", "an old ceramic ginger grater and three part-grated, shrivelled dried ginger rhizomes lying together in an open kitchen drawer"),
    (184, "", f"{CHAR} sitting with her hands in her lap looking down, {DAUGHTER} beside her with a hand on her shoulder"),
    (186, "", "close-up of three ginger rhizomes on a counter: two neatly peeled and pale, one still with its skin on, all shrunken and dry"),
    (188, "", "raw grated ginger drying and browning at the edges on a cold plate left on a kitchen counter"),
    (192, "", "an old analogue bathroom scale on a tiled floor with bare elderly feet stepping onto it, the dial face blurred and unreadable"),
    # ── CHECKPOINT ──────────────────────────────────────────────────────────
    (196, "", "a teacup and a pencil side by side on a kitchen table, quiet pause, late afternoon light"),
    # ── LOOP PAYOFF ─────────────────────────────────────────────────────────
    (197, "", "hero shot from directly above of one steaming bowl of miso soup on a lacquer tray, tofu and wakame inside, rich warm light"),
    (200, "", "three thin ginger slices laid in a neat row on a small wooden board"),
    (203, "", "hot broth being poured from a small pot into a bowl that already has one thin ginger slice resting at the bottom, a burst of steam rising as it hits, seen from the side"),
    (210, "", "hero shot of a pot on the flame with two ginger slices simmering in the broth, warm flame light on the pot rim"),
    # ── ANECDOTE 3 ──────────────────────────────────────────────────────────
    (213, "", f"{CHAR}'s hands lowering a single ginger slice into an empty bowl before pouring the soup"),
    (215, "", f"{CHAR} smiling faintly at an empty rice bowl in front of her, chopsticks set down neatly"),
    # ── RECAP ───────────────────────────────────────────────────────────────
    (219, "", "a hand dropping thin ginger slices into a pot of dashi before the miso is added, steam beginning to rise"),
    (222, "", "a small dish holding only three thin ginger slices, placed beside a much larger empty plate for contrast"),
    (224, "", "close-up of a gas flame under the base of a pot, warm orange edge"),
    (227, "", "a complete simple supper for one on a wooden table: bowl of miso soup, rice, grilled fish, small pickled side dish"),
    # ── BONUS ───────────────────────────────────────────────────────────────
    (232, "", "thin ginger slices spread out in a bamboo steamer basket with steam rising through them"),
    (234, "", "a flat round bamboo drying basket of ginger slices sitting in bright sunlight by a window, sun-warmed wooden floor"),
    # ── ENDING ──────────────────────────────────────────────────────────────
    (237, "", "a single knobbly ginger rhizome sitting alone on a clean kitchen counter, morning light"),
    (243, "", "an elderly woman standing at a kitchen counter seen from behind, morning light through the window, quiet and steady"),
    (244, "", "elderly hands washing vegetables in a sink, water running, morning light"),
    (247, "", "a supper table laid for one person in the evening, lamp light, waiting"),
    (252, "", "a calm empty kitchen table with a single teacup of tea, soft late light"),
    (260, "", "a warm complete supper for one seen slightly from above: miso soup, rice, grilled fish, a small side dish, evening lamp light"),
]


def body_lines():
    out = []
    for ln in TTS.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"\[[^\]]*\]", "", s).strip()
        if s:
            out.append(s)
    return out


def main():
    body = body_lines()
    starts, t = [], 0.0
    for b in body:
        starts.append(t)
        t += len(b) / CPS + PER_LINE
    total = t

    slides, flow, tenfile, blocks = [], [], [], []
    prev = -99.0
    errs = []
    for n, (idx, rank, core) in enumerate(PLAN):
        if idx >= len(body):
            errs.append(f"entry {n}: line index {idx} vuot so dong ({len(body)})")
            continue
        line = body[idx]
        match = line.rstrip("。")
        if match not in TTS.read_text(encoding="utf-8"):
            errs.append(f"entry {n}: match KHONG phai substring -> {match}")
        gap = starts[idx] - prev
        if gap < 6:
            errs.append(f"entry {n} (dong {idx}, {starts[idx]:.0f}s): cach entry truoc {gap:.1f}s < 6s")
        prev = starts[idx]

        e = {"match": match, "photo": True, "q": "AI-GEN"}
        if rank:
            e["rank"] = rank
        slides.append(e)

        prompt = f"{core}. {STYLE}."
        flow.append(prompt)
        mm, ss = int(starts[idx]) // 60, int(starts[idx]) % 60
        tenfile.append(f"slide_{n:02d}.jpg\t{mm:02d}:{ss:02d}\t{rank or '-':6}\t{line}")
        blocks.append(f"### slide_{n:02d}.jpg — {mm:02d}:{ss:02d} — {rank or '(ngoai muc)'}\n"
                      f"- cue: `{line}`\n- shot: {core}\n")

    if errs:
        print("[LOI] khong xuat file:")
        for e in errs:
            print("   ", e)
        return 1

    VD.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (VD / "slide_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "slide_prompts_TENFILE.txt").write_text(
        "ten file\tmoc\trank\tcau cue trong _TTS.md\n" + "\n".join(tenfile) + "\n", encoding="utf-8")
    (VD / "slide_prompts_BLOCKS.md").write_text(
        f"# Video 15 — {len(slides)} prompt anh slide\n\n"
        f"> Khoi STYLE dung chung cuoi MOI prompt (giu 83 anh dong nhat):\n>\n> `{STYLE}`\n\n"
        f"> Nhan vat ヨシ子 (cung mot cau ta o moi slot): `{CHAR}`\n\n" + "\n".join(blocks),
        encoding="utf-8")

    n = len(slides)
    print(f"OK  {n} entry | video ~{int(total)//60}'{int(total)%60:02d}")
    print(f"    {total/n:.1f} giay/anh | {n/(total/60):.2f} doi hinh/phut  (tran 6/phut)")
    print(f"    rank: " + " ".join(f"{r}={sum(1 for s in slides if s.get('rank')==r)}"
                                   for r in ["一つめ", "二つめ", "三つめ", "四つめ"])
          + f" | ngoai muc={sum(1 for s in slides if 'rank' not in s)}")
    print(f"    -> {OUT_JSON.relative_to(ROOT)}")
    print(f"    -> {(VD/'slide_prompts_FLOW.txt').relative_to(ROOT)}")
    print(f"    -> {(VD/'slide_prompts_TENFILE.txt').relative_to(ROOT)}")
    print(f"    -> {(VD/'slide_prompts_BLOCKS.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
