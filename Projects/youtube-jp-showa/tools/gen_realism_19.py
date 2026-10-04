# -*- coding: utf-8 -*-
"""gen_realism_19.py — 10 canh AI cua video 19 (kaimono-joushiki), CONG THUC REALISM.

Video 19 chay khuon v08: 92% hinh THAT (tools/plan_19.py). AI chi con 10 o — canh bat buoc co
NGUOI dang dien ma khong anh that nao ke duoc. Moi canh: STILL (Flow Image, Nano Banana 2) ->
chon anh -> ⋮ Animate -> MOTION (Veo 3.1). Khoi chung: _media_library/realism_blocks.py.

Xuat 06_VIDEO/19_kaimono-joushiki/:
    realism19_STILL_FLOW.txt   1 prompt / dong, extension bom thang
    realism19_MOTION_FLOW.txt  1 prompt / dong, cung thu tu
    realism19_TENFILE.txt      dong i -> ten file + cau TTS + o trong plan_19
    realism19_BLOCKS.md        ban nguoi doc
"""
import io, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
from realism_blocks import build_pair, gate_prompt, gate_action, HOLD_CLAUSE, LIMIT_SHOWA

OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\19_kaimono-joushiki")

# ---- DAN DIEN video 19 — KHUON MAT (co dinh) + DO MAC (doi theo boi canh). Khong chep tu video khac.
FACE = {
 "haha":  ("a Japanese woman in her mid-thirties with a narrow oval face, high flat cheekbones, thin straight "
           "eyebrows, single-lidded eyes set slightly wide, a small low nose, a soft rounded chin and a tiny mole "
           "below the left eye, black hair pulled back into a low bun with a few loose strands at the temple"),
 "haha_old": ("the same woman in her mid-fifties — the same narrow oval face, high flat cheekbones, thin straight "
           "eyebrows, single-lidded wide-set eyes, small low nose and tiny mole below the left eye, now with fine "
           "lines at the eyes and mouth and her hair short, permed and threaded with grey"),
 "denkiya": ("a Japanese man in his early twenties with a long bony face, a prominent jaw, thick dark eyebrows "
           "that nearly meet, deep-set eyes, a slightly crooked nose and a short crew cut"),
 "chichi": ("a Japanese man about forty with a broad square face, heavy cheeks, short thick eyebrows, narrow eyes "
           "under hooded lids, a wide flat nose, a stubbled chin and hair cut very short and greying at the sides"),
 "boy":    ("a Japanese boy of about eight with a round face, big ears, a bowl haircut and a scab on one knee"),
 "girl":   ("a Japanese girl of about ten with a thin face, a pointed chin, straight-cut bangs and two short plaits"),
 "yaoya":  ("a Japanese man about sixty with a long creased face, a high forehead, sparse grey eyebrows, heavy "
           "lower eyelids, a large hooked nose and a white towel tied round his head"),
 "kesho":  ("a Japanese woman about fifty with a plump round face, arched pencilled eyebrows, a small red-painted "
           "mouth and neatly set wavy black hair"),
 "musume": ("a Japanese woman of about twenty-four with her mother's narrow oval face and high flat cheekbones but "
           "fuller lips and double-lidded eyes"),
}

W70 = ("Setting: an ordinary Japanese town in the winter of the early nineteen-seventies, the real Showa era, "
       "classic and period-correct — wooden houses, paper sliding screens, tatami, enamel and wood — nothing "
       "modern and nothing futuristic.")
W89 = ("Setting: an ordinary Japanese shopping street in the spring of the late nineteen-eighties, the real "
       "Showa-to-Heisei years, period-correct clothes and shop fittings, nothing modern, nothing futuristic.")
W85 = ("Setting: a Japanese family home in the mid-nineteen-eighties, the real Showa era, tatami room with "
       "paper screens, period-correct, nothing modern.")

S = [
 dict(key="denkiya_bow", line=1, file="ai_01_denkiya_bow",
      where="someone kneeling just behind the mother on the raised wooden step", height="kneeling eye height",
      cam="locked", light="dusk",
      still=("In the earthen entrance of an old wooden house, the sliding glass door half open onto a cold dusk "
             "street, a young man from the neighbourhood electrical shop — " + FACE["denkiya"] + ", in a grey work "
             "jacket with his cap held in both hands at his waist — stands bowing low from the waist. In the near "
             "foreground, seen from behind her shoulder and out of focus, the mother — " + FACE["haha"] + ", in a "
             "faded brown cardigan over a plain skirt — kneels on the raised wooden step, one hand resting on the "
             "edge of the step. A pair of wooden geta and a child's rubber shoes lie on the earthen floor."),
      act=("the young man stays bowed, then lifts his head only halfway and lowers it again, the cap turning once "
           "in his hands; in the foreground the mother slowly lowers her head in return and keeps it there."),
      alive="Cold air from the street makes the edge of the noren above the door stir very slightly."),
 dict(key="kids_tv", line=3, file="ai_02_kids_tv",
      where="a grandparent sitting at the back of the small tatami room", height="seated height on the tatami",
      cam="drift", light="night",
      still=("In a small tatami living room at night, a boy — " + FACE["boy"] + ", in a striped jumper — and his "
             "sister — " + FACE["girl"] + ", in a red knitted cardigan — kneel side by side very close in front of a "
             "wooden cabinet television on four short legs, their faces lit only by the soft coloured glow of the "
             "screen; the screen itself shows nothing readable, only blurred moving colour. A low round table with "
             "two teacups stands behind them."),
      act=("the girl leans a little closer to the screen with her hands on her knees; beside her the boy's mouth "
           "goes wide with no control over it and his shoulders shake as he laughs without a sound, one foot "
           "still wriggling behind him."),
      alive="The coloured glow on their faces changes slowly and softly."),
 dict(key="father_factory", line=36, file="ai_03_father_factory",
      where="a fellow worker standing by the workshop door", height="standing eye height",
      cam="locked", light="interior",
      still=("Inside a small town machine shop in winter, a lathe and a drill press stand switched off and silent. "
             "The father — " + FACE["chichi"] + ", in a navy work jacket and a cloth cap — sits alone on an "
             "upturned wooden crate beside the idle lathe, forearms resting on his knees, looking at the floor. "
             "Oil-stained floorboards, a row of hanging spanners, a cold round kerosene stove."),
      act=("the father slowly takes off his cap, rubs the back of his head with the same hand, and turns his "
           "face towards the silent lathe, holding the cap loosely on his knee."),
      alive="A little dust drifts in the light from the window."),
 dict(key="hands_shichifuda", line=41, file="ai_04_hands_shichifuda",
      where="someone waiting behind the mother at the pawnshop counter", height="standing eye height, just over her shoulder",
      cam="locked", light="interior",
      still=("Over the mother's shoulder at the counter of an old pawnshop: behind a dark wooden lattice screen "
             "sits the elderly pawnbroker in a grey kimono jacket and round glasses, and on the worn wooden counter "
             "between them lie a neatly folded silk kimono in a purple cloth wrapper and a small plain paper "
             "ticket with no marks visible. The mother — " + FACE["haha"] + ", in a dark winter coat — is seen "
             "from behind and to one side, her head bowed, her right hand resting on the counter."),
      act=("the pawnbroker slides the small plain paper ticket across the counter with two fingers; the mother's "
           "hand closes over it slowly and draws it back towards her, and she keeps her head bowed. " + HOLD_CLAUSE),
      alive=""),
 dict(key="mother_cosme_window", line=55, file="ai_05_mother_cosme_window",
      where="a passer-by pausing on the other side of the narrow street", height="standing eye height",
      cam="drift", light="dusk",
      still=("At dusk on a narrow shopping street, the mother — " + FACE["haha"] + ", in a dark winter coat and a "
             "knitted scarf, a string shopping bag with a daikon radish in her hand — stands in front of the lit "
             "glass window of a small cosmetics shop, looking in at rows of lipsticks and little glass bottles on "
             "glass shelves. Her reflection is faint in the glass. No readable writing on the window."),
      act=("the mother leans a little towards the glass, stays still for a moment, then straightens up, pulls "
           "her scarf closer and turns away along the street."),
      alive="The warm light of the window glows against the blue dusk."),
 dict(key="lipstick_hand", line=57, file="ai_06_lipstick_hand",
      where="a customer sitting at the next stool along the counter", height="seated eye height",
      cam="locked", light="interior",
      still=("Inside a small cosmetics shop, across a low glass counter, the shop owner — " + FACE["kesho"] + ", "
             "in a white smock — holds the mother's left hand gently by the wrist, and on the back of the mother's "
             "hand there is one short red line of lipstick. The mother — " + FACE["haha"] + ", in a dark winter "
             "coat — sits on a round stool, seen in three-quarter view. Glass shelves of bottles behind them."),
      act=("the shop owner lets go of the wrist; the mother slowly raises her hand towards the window light, "
           "turns it a little and looks at the red line, her mouth going up but her eyes staying level. " + HOLD_CLAUSE),
      alive=""),
 dict(key="yaoya_103yen", line=108, file="ai_07_yaoya_103yen",
      where="the next customer waiting at the open front of the shop", height="standing eye height",
      cam="locked", light="day",
      still=("Morning at the open front of a small greengrocer's shop, wooden crates of cabbages, carrots and "
             "white daikon radishes under an awning. The greengrocer — " + FACE["yaoya"] + ", in a dark apron — "
             "holds one daikon wrapped in newspaper. Facing him, the mother — " + FACE["haha_old"] + ", in a beige "
             "spring coat — holds her small clasp purse open in both hands, looking down into it."),
      act=("the greengrocer lifts his free hand and scratches the back of his head, his face creasing into an "
           "apologetic half smile; the mother keeps looking down into the open purse, then slowly looks up at him."),
      alive="Leaves of the cabbages stir faintly in the breeze."),
 dict(key="mother_two_piles", line=116, file="ai_08_mother_two_piles",
      where="a child lying awake in the next room looking through the half-open sliding door",
      height="low, at the level of the tatami", cam="drift", light="night",
      still=("Late at night in a tatami room lit by one low lamp, the mother — " + FACE["haha"] + ", in a padded "
             "winter jacket — kneels alone at a low round table. On the table lie a small booklet with a plain "
             "cover and, beside it, a small plain paper ticket with no marks visible. Behind her, dark, a wooden "
             "cabinet television on short legs."),
      act=("the mother looks from the booklet to the ticket and back, then gently rests her fingertips on the "
           "booklet and slides it a little towards herself, her chin tightening, her eyes kept wide and dry. " + HOLD_CLAUSE),
      alive="The lamp light is steady; only her hands move."),
 dict(key="daughter_bride", line=119, file="ai_09_daughter_bride",
      where="a relative sitting by the paper screen at the side of the room", height="seated height on the tatami",
      cam="locked", light="interior",
      still=("In a tatami room on the morning of a wedding, the daughter — " + FACE["musume"] + " — sits in a "
             "white wedding kimono with a white hood folded in her lap. Kneeling close behind her, the mother — "
             + FACE["haha_old"] + ", in a black formal kimono — has both hands on the collar of the white kimono, "
             "straightening it. Soft light through the paper screen."),
      act=("the daughter slowly turns her head over her shoulder towards her mother; the mother's hands stop on "
           "the collar and stay there."),
      alive=""),
 dict(key="mother_smile", line=121, file="ai_10_mother_smile",
      where="the daughter kneeling in front of her", height="seated height on the tatami",
      cam="drift", light="interior",
      still=("In the same tatami room, a medium shot of the mother — " + FACE["haha_old"] + ", in a black formal "
             "kimono — kneeling, seen in three-quarter view, her hands folded in her lap, looking down at them. "
             "Behind her, out of focus, an old wooden cabinet television on short legs stands against the wall."),
      act=("her eyes go first and crease into two slits, the cheeks pushing up and the mouth barely opening, and "
           "her head tilts slowly towards the old television behind her."),
      alive=""),
]
WORLD = {"denkiya_bow": W70, "kids_tv": W70, "father_factory": W70, "hands_shichifuda": W70,
         "mother_cosme_window": W70, "lipstick_hand": W70, "mother_two_piles": W70,
         "yaoya_103yen": W89, "daughter_bride": W85, "mother_smile": W85}

def main():
    stills, motions, rows, md, bad = [], [], [], ["# realism19 — 10 canh AI video 19 (ban nguoi doc)\n"], 0
    for i, sc in enumerate(S, 1):
        sc = dict(sc, still=sc["still"] + " " + WORLD[sc["key"]])
        st, mo, _ = build_pair(sc, "")
        for kind, p in (("still", st), ("motion", mo)):
            pr = gate_prompt(kind, p, LIMIT_SHOWA)
            if pr: bad += 1; print(f"  🔴 {i:02d} {sc['key']} {kind}: {pr}")
        for k, m in gate_action(sc["act"]):
            if k != "③": bad += 1
            print(f"  {'⚠' if k == '③' else '🔴'} {i:02d} {sc['key']} action {k}: {m}")
        stills.append(st); motions.append(mo)
        rows.append(f"{i:02d}\t{sc['file']}.png / .mp4\tTTS dong {sc['line']}\t{sc['key']}\t{len(st)}/{len(mo)} ky")
        md += [f"## {i:02d} · {sc['key']} (TTS dong {sc['line']})\n", f"**STILL** ({len(st)} ky)\n\n{st}\n",
               f"**MOTION** ({len(mo)} ky)\n\n{mo}\n"]
    io.open(OUT / "realism19_STILL_FLOW.txt", "w", encoding="utf-8", newline="\n").write("\n".join(stills) + "\n")
    io.open(OUT / "realism19_MOTION_FLOW.txt", "w", encoding="utf-8", newline="\n").write("\n".join(motions) + "\n")
    io.open(OUT / "realism19_TENFILE.txt", "w", encoding="utf-8", newline="\n").write(
        "# dong i cua STILL_FLOW / MOTION_FLOW -> ten file bo vao cells_in/\n" + "\n".join(rows) + "\n")
    io.open(OUT / "realism19_BLOCKS.md", "w", encoding="utf-8", newline="\n").write("\n".join(md))
    print(f"{len(S)} canh -> {OUT}\\realism19_*  | gate do: {bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
