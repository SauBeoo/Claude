# -*- coding: utf-8 -*-
"""gen_era_fix_19.py — 7 prompt ANH AI TINH thay o LECH THOI DAI cua video 19 (user 2026-09-26:
"nhieu doan cho co con dau… khong cung thoi dai showa").

Soi ra 10 o hong CUNG MOT LOP: Pexels tra do TAY cho tu khoa 'stamp'/'crt' (dau sap niem phong chau Au,
TV CRT thap nien 90). 3 o thay bang anh THAT (e00 判子 · e06 シャッター · e07 Trinitron), 7 o gen o day.
Khuon: realism19_STILL_FLOW.txt (cung header, cung cast NGUYEN VAN -> cung mot me/mot dan tre).
Xuat: 06_VIDEO/19_kaimono-joushiki/era19_STILL_FLOW.txt (1 prompt/dong) + era19_TENFILE.txt
"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\19_kaimono-joushiki")

HEAD = ("A single photorealistic still photograph, wide 16:9, shot on a cinema camera with a fine film grain — real people, "
        "real place, not an illustration and not a render. No writing, lettering, numbers, logos or brand names anywhere in the "
        "picture — every stamp mark is a plain red circle or square of ink with nothing inside it, every page is blank paper "
        "with only faint ruled lines, and the television has no brand name and no picture on its screen. ")
WORLD = ("Setting: an ordinary Japanese home in the winter of the early nineteen-seventies, the real Showa era, classic and "
         "period-correct — wooden houses, paper sliding screens, tatami, enamel and wood — nothing modern and nothing futuristic. ")
LIGHT_NIGHT = ("Light: one low lamp is the only light, its warm glow falling off softly into the shade of the room; muted warm "
               "colour, nothing glaring, nothing burnt out. ")
LIGHT_DAY = ("Light: soft winter daylight from one paper screen, falling off gently into the room; muted warm colour, nothing "
             "glaring, nothing burnt out. ")
TAIL = ("Faces in three-quarter view or looking down, nobody looking at the camera, no face filling the frame. Shallow depth of "
        "field, one out-of-focus object at the near edge of the frame, evenly exposed into all four corners, fine film grain. "
        "Keep everything important in the left 85% of the frame.")
MOTHER = ("the mother — a Japanese woman in her mid-thirties with a narrow oval face, high flat cheekbones, thin straight "
          "eyebrows, single-lidded eyes set slightly wide, a small low nose, a soft rounded chin and a tiny mole below the left "
          "eye, black hair pulled back into a low bun with a few loose strands at the temple, in a faded brown cardigan over a "
          "plain skirt —")
KIDS = ("a boy — a Japanese boy of about eight with a round face, big ears, a bowl haircut and a scab on one knee, in a striped "
        "jumper — and his sister — a Japanese girl of about ten with a thin face, a pointed chin, straight-cut bangs and two "
        "short plaits, in a red knitted cardigan —")
TV = ("a wooden cabinet colour television on four short tapered legs, walnut-veneer sides, a curved grey screen, two round "
      "rotary knobs and a small speaker grille on the right of the screen")
BOOK = ("a small palm-sized instalment booklet with a plain faded blue card cover, lying open to a page ruled into a grid of "
        "small square boxes")

# (o, file, TTS dong, cau doc, anh sang, CANH)
P = [
 (33, "ai_13_book_half", 29, "判子が二十四個そろうまで", LIGHT_DAY,
  f"Close on a low wooden tea table: {BOOK}, the first several boxes each holding one plain red circle of ink and all the "
  f"remaining boxes still empty, a small cylindrical wooden seal and a round tin of red ink paste beside it. Behind, out of "
  f"focus across the tatami room, {TV} stands against the wall. No person in the frame. "),
 (62, "ai_14_mother_stamp", 51, "冊子に、判子が、ひとつ増える", LIGHT_NIGHT,
  f"Kneeling at a low wooden tea table, {MOTHER} holds {BOOK} flat with one hand and with the other lifts a small "
  f"cylindrical wooden seal straight up from the page, a fresh plain red circle of ink left in the next empty box. Far "
  f"behind her, soft and out of focus, the two children — a small boy in a striped jumper and a girl in a red knitted "
  f"cardigan — sit on the tatami facing the glowing screen of a wooden cabinet television. "),
 (131, "ai_15_tv_night", 100, "あのテレビの値段に隠れていた", LIGHT_NIGHT,
  f"A small tatami living room at night with nobody in it: {TV} stands against a paper sliding screen, its screen dark "
  f"grey and blank, a crocheted white doily and a small vase of red carnations on its top. A low round table with two "
  f"teacups and a folded newspaper with no visible print sits in the near foreground, slightly out of focus. "),
 (133, "ai_16_tv_front", 102, "物品税 10%", LIGHT_DAY,
  f"Straight-on at the height of the table, the front of {TV} fills the right two-thirds of the frame, the grain of the "
  f"walnut veneer and the chrome rim of the knobs sharp, the screen blank and grey. The upper-left third of the frame is a "
  f"plain, softly out-of-focus paper sliding screen with nothing on it. No person in the frame. "),
 (134, "ai_17_tv_console", 102, "大きな画面 20%", LIGHT_DAY,
  "A large floor-standing console colour television of the late nineteen-seventies — a long low walnut cabinet on a "
  "plinth, a big curved grey screen on the right, a row of plain push buttons and a fabric speaker panel on the left — "
  "stands in a tatami living room beside a lacquered sideboard, the screen blank. The upper-left third of the frame is "
  "plain wall and paper screen with nothing on it. No person in the frame. "),
 (135, "ai_18_stamp_close", 103, "押してもらった、あの判子", LIGHT_NIGHT,
  f"A very close view of one page of {BOOK}: a single plain red circle of ink, slightly uneven at one edge where the seal "
  f"was pressed a little harder, sits in a square box among other filled boxes, the paper fibres visible; a woman's "
  f"fingertip — the mother's hand, a thin gold wedding ring — rests at the edge of the page. The rest of the page softly "
  f"out of focus. "),
 (156, "ai_19_book_full", 118, "二十四個目の判子が押された日", LIGHT_DAY,
  f"On a low wooden tea table, {BOOK}, every single box on the page now filled with a plain red circle of ink, lies open "
  f"beside a small cylindrical wooden seal. Behind it, soft and out of focus, {MOTHER} kneels looking at the book with her "
  f"hands folded in her lap, and further back {TV} glows faintly with blurred colour. "),
]

lines, ten, bad = [], ["# dong i cua era19_STILL_FLOW -> ten file bo vao cells_in_ai/ (sau khi cat ✦)"], []
for k, (o, fn, dong, cau, light, scene) in enumerate(P, 1):
    p = HEAD + scene + WORLD + light + TAIL
    lines.append(p)
    ten.append("%02d\t%s.png\to %d · TTS dong %d · %s\t%d ky" % (k, fn, o, dong, cau, len(p)))
    pos = p.find("No writing") * 100 // len(p)
    if pos > 15: bad.append((fn, "guard chu o %d%%" % pos))
    for w in ("35mm", "16mm", "hands only", "vignette", "wax", "sealing"):
        if w in p: bad.append((fn, "token cam: " + w))
    if len(p) > 2200: bad.append((fn, "dai %d > 2200" % len(p)))
out = VD / "era19_STILL_FLOW.txt"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
(VD / "era19_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")
# gate tren FILE da ghi
chk = out.read_text(encoding="utf-8").splitlines()
assert len(chk) == len(P) and all(l.startswith("A single photorealistic") for l in chk)
for t in ten[1:]: print(t)
print("GATE:", "SACH" if not bad else bad)

# ---------------------------------------------------------------- REDO1 (2026-09-26)
# Flow CHAN 3 prompt (book_half · stamp_close · book_full) = 3 canh ma cuon so + dau la CHU THE can canh.
# Nghi bo loc doc thanh GIA MAO GIAY TO/CON DAU: instalment booklet + seal + stamp mark + ink + grid of boxes.
# Sua: bo moi tu tai chinh/con dau, ta bang VAT TRUNG TINH — hinh giu nguyen.
HEAD2 = ("A single photorealistic still photograph, wide 16:9, shot on a cinema camera with a fine film grain — real people, "
         "real place, not an illustration and not a render. No writing, lettering, numbers, logos or brand names anywhere in "
         "the picture — the notebook pages are plain paper with only faint pencil lines, and the television has no name on "
         "it and nothing on its screen. ")
NOTE = ("a small old notebook with a plain faded blue card cover, lying open to a page divided by faint pencil lines into "
        "rows of little squares")
DOT = "a small round red dot, like a tiny painted circle"
REDO = [
 ("ai_13_book_half", 29, "判子が二十四個そろうまで", LIGHT_DAY,
  f"Close on a low wooden tea table: {NOTE}, the first several squares each holding {DOT} and all the other squares still "
  f"empty; a short round wooden stick and a little round tin of red paste lie beside it. Behind, out of focus across the "
  f"tatami room, {TV} stands against the wall. No person in the frame. "),
 ("ai_18_stamp_close", 103, "押してもらった、あの判子", LIGHT_NIGHT,
  f"A very close view of one page of {NOTE}: {DOT}, slightly uneven at one edge, sits in one square among other squares "
  f"that hold the same red dots, the paper fibres visible; the tip of a woman's finger rests at the edge of the page. "
  f"The rest of the page softly out of focus. "),
 ("ai_19_book_full", 118, "二十四個目の判子が押された日", LIGHT_DAY,
  f"On a low wooden tea table lies {NOTE}, every single square on the page now holding {DOT}, beside a short round wooden "
  f"stick. Behind it, soft and out of focus, {MOTHER} kneels looking at the notebook with her hands folded in her lap, and "
  f"further back {TV} glows faintly with blurred colour. "),
]
BAN = ("instalment", "installment", "seal", "stamp", "ink", "booklet", "receipt", "payment", "wedding ring")
rl, rt, rbad = [], ["# era19_REDO1 — Flow chan 3 prompt: nghi bo loc GIA MAO GIAY TO/CON DAU -> ta bang vat trung tinh"], []
for k, (fn, dong, cau, light, scene) in enumerate(REDO, 1):
    p = HEAD2 + scene + WORLD + light + TAIL
    rl.append(p); rt.append("%02d\t%s.png\tTTS dong %d · %s\t%d ky" % (k, fn, dong, cau, len(p)))
    low = p.lower()
    rbad += [(fn, w) for w in BAN if w in low]
    if p.find("No writing") * 100 // len(p) > 15: rbad.append((fn, "guard"))
(VD / "era19_REDO1_STILL_FLOW.txt").write_text("\n".join(rl) + "\n", encoding="utf-8")
(VD / "era19_REDO1_TENFILE.txt").write_text("\n".join(rt) + "\n", encoding="utf-8")
for t in rt[1:]: print("REDO1", t)
print("GATE REDO1 (khong con tu tai chinh/con dau):", "SACH" if not rbad else rbad)
