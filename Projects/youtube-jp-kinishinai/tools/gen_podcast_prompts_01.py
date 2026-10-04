# -*- coding: utf-8 -*-
"""kinishinai bai 1 — nguoi ke chuyen trong phong thu podcast: ANH NGUOI THAT (t2i) -> clip (Flow Animate).

Buoc 1 (ANH):  _plan/podcast_IMG_FLOW.txt — 5 prompt anh photoreal. Dong 1 = anh MOC khuon mat;
               dong 2-5 gen KEM anh moc lam reference (t2i khong co character-lock, day la cach giu mat).
Buoc 2 (CLIP): --base <thu muc 5 anh da gen, thu tu A-E> -> cat ✦ vao _plan/podcast_base/pod_XX.png
               -> upload Animate voi _plan/podcast_FLOW.txt (cung thu tu pod_XX).
_plan/podcast_TENFILE.txt: dong FLOW <-> anh <-> vai <-> ten clip tra ve + bang tai dung 5 clip -> 11 cho.
Gate: guard (NO TEXT) trong 15% dau prompt · khong token cam.
"""
import argparse
import sys
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
from realism_blocks import LOCKED_CAM, DRIFT_CAM  # noqa: E402

VD = Path(r"E:\Claude\Projects\youtube-jp-kinishinai\06_VIDEO\01_kuchiguse-hitonome")
OUT = VD / "_plan"
BASE = OUT / "podcast_base"

# Nguoi ke = {K} cua _plan/plan.py (cung mot nguoi voi cac shot ke chuyen trong bai) + chi tiet mat de giu nhan dang
K = ("a Japanese woman of about 68 with short soft silver hair in a neat bob, small pearl earrings and a navy "
     "cardigan over a plain cream blouse, a gentle oval face with fine smile lines at the eyes, light natural "
     "makeup, no glasses")
STUDIO = ("a small, warm podcast recording room: walls of dark wood with soft grey fabric acoustic panels, a "
          "round light-wood table, one black studio microphone on a boom arm in front of her, a pair of "
          "headphones resting on the table, a glass of water, one small table lamp with a warm shade behind her")

# ---------------- BUOC 1: ANH ----------------
IMG_GUARD = ("NO TEXT: no letters, no words, no numbers, no logos and no signs anywhere in the picture; any "
             "paper on the table is blank. Exactly one person in the picture.")
IMG_HEAD = ("A 16:9 photorealistic photograph, natural documentary look, a real Japanese person in a real room "
            "of today, shallow depth of field, the background melting softly out of focus.")
IMG_LIGHT = ("Light: the warm table lamp and soft light from one side, gentle and even, skin natural and "
             "unretouched, warm gentle colours, fine photographic grain, evenly exposed into all four corners.")
IMG_END = ("She looks at the microphone or just past the camera, never straight into the lens. Keep her and "
           "the microphone inside the left 85% of the frame, the bottom-right corner plain dark wall. "
           "No watermark, no signature, no text.")
REF = "the same woman as in the reference image — same face, same hair, same clothes — "

# (vai, khung hinh, tu the = NHIP 1 cua clip cung so)
IMGS = [
    ("A · MOC khuon mat + ke chuyen am (rong)",
     "a medium shot from the waist up, the table edge along the bottom of the frame",
     "sitting at the table talking warmly into the microphone, both hands resting flat on the table, her eyes "
     "creasing into a soft smile"),
    ("B · hoi tuong (tay dat len nguc)",
     "a medium close shot from the chest up, the microphone beside her",
     "speaking slowly with one hand resting on her chest, her eyes lowered a little as if remembering "
     "something long ago"),
    ("C · bat cuoi tu trao",
     "a close shot in three-quarter profile, her face and shoulders, the microphone soft in the near foreground",
     "pressing her lips together to hold in a laugh, eyes crinkled, about to laugh at herself"),
    ("D · nghiem tuc, khuyen nhu",
     "a close shot from the shoulders up, almost straight on, the microphone just below her chin to one side",
     "leaning a little towards the microphone, her eyes soft and steady, about to say something sincere"),
    ("E · khoang lang",
     "a medium shot from slightly to one side, the empty half of the round table and the lamp behind her",
     "sitting still with her hands folded on the table, her gaze dropped away from the microphone, quiet "
     "and thoughtful"),
]

# ---------------- BUOC 2: CLIP ----------------
GUARD = ("NO TEXT AND NO NEW PEOPLE: no letters, no words, no numbers, no captions, no logos and no signs "
         "appear anywhere at any moment, any paper on the table stays blank; she is the only person in the "
         "room for the whole shot and nobody else ever enters.")
STYLE = ("Animate this exact photograph and keep it exactly as it is: photorealistic, a real woman, the same "
         "Japanese woman of about 68 with short silver hair in a neat bob, pearl earrings and a navy cardigan, "
         "the same small recording room with dark wood walls, grey acoustic panels, the round table and the "
         "black microphone on its boom arm. Her face, hair, clothes and the room never change.")
WHERE = "a radio producer sitting quietly across the table from her"
HEIGHT = "her own seated eye height"
GENTLE = ("She moves gently and without hurry, the one action spread across the whole eight seconds, nothing "
          "quick or sudden; only she moves, the microphone, the boom arm and the room stay perfectly still.")
TALK = ("When she talks, she talks softly and slowly into the microphone, her lips moving only a little, with "
        "small natural pauses between phrases, the way someone talks on a calm late-night radio programme.")
QUIET = "Her mouth stays closed for this whole moment; she is between sentences, not speaking."
END = ("Warm soft studio lamp light, gentle and even, nothing burnt out. Silent clip, no speech audio, only a "
       "faint quiet room tone. Keep the very bottom-right corner plain. No watermark, no logo, no text.")

# 5 clip, MOI CLIP 2 NHIP khac han nhau (0-4s / 4-8s) -> cat duoc 2 doan + 1 ban crop can
# => tai dung 11 cho ma khong cho nao chieu lai cung khung (media-library §2 muc 4).
# (vai, may, nhip 1 noi?, hanh dong: NHIP 1 roi NHIP 2)
CLIPS = [
    ("A · ke chuyen am (rong)", "lock", True,
     "For the first half of the shot she talks warmly into the microphone, both hands resting flat on the "
     "table, eyes creasing into a smile. Then, for the second half, she stops talking, gives one small easy "
     "nod and settles back a little in her chair, still smiling, mouth closed."),
    ("B · hoi tuong (tay dat len nguc)", "lock", True,
     "For the first half of the shot she speaks slowly with her hand resting on her chest, her eyes lowered as "
     "if remembering something long ago. Then, for the second half, she lifts her eyes with a small proud "
     "smile and dips her head once, the hand staying where it is, mouth closed."),
    ("C · bat cuoi tu trao", "lock", False,
     "For the first half of the shot she presses her lips together to hold in a laugh, it escapes through "
     "her nose anyway and her shoulders shake once. Then, for the second half, she looks down and to the "
     "side with an embarrassed little smile and gently shakes her head at herself."),
    ("D · nghiem tuc, khuyen nhu", "drift", True,
     "For the first half of the shot she leans a little closer to the microphone and speaks gently and "
     "sincerely, her eyes soft and steady. Then, for the second half, she stops talking and gives one slow "
     "encouraging nod, mouth closed, a kind small smile."),
    ("E · khoang lang", "drift", False,
     "For the first half of the shot she sits still with her hands folded on the table, her gaze resting low "
     "and away from the microphone, and she takes one slow breath that lifts her shoulders slightly. Then, for the second half, she lets the "
     "breath out and a small quiet smile comes back to her face as she looks up again."),
]

REUSE = """
# BANG TAI DUNG — 5 clip -> 11 cho, khong cho nao chieu lai cung khung
# doan: a = 0-4s (nhip 1) · b = 4-8s (nhip 2) · c = crop can 1.25x quanh mat, lay 2-6s
slot   | moc   | cau dang doc                                   | clip.doan
#10    | 01:46 | ラジオのように、気楽に聞いてくださいね          | pod_01.a
#13    | 02:14 | 今年、六十八になります                          | pod_02.a
#23    | 04:03 | でも、見張り番が本当に気にしているのは          | pod_04.a
#33    | 05:56 | ちょっと、がっかりしたくらいです                | pod_03.a
#46    | 08:17 | ご近所の次は、もっと近い人です                  | pod_01.b
#57    | 10:04 | 本当に聞いてほしい話は、まだ、胸の奥に          | pod_05.a
#80    | 13:47 | 七つ目だけは、どうしても、やめられなかった      | pod_02.b
#90    | 15:30 | 今日、ひとつだけ…正直に言ってみてください      | pod_04.b
#92    | 15:49 | 私の、今年のお正月の話をさせてください          | pod_01.c
#106   | 18:11 | 見張り番は、あなたの敵ではありません            | pod_03.b
#111   | 19:05 | 楽に過ごせますように                            | pod_05.b
"""

BANNED = ("35mm", "16mm", "hands only", "respectful distance", "never comes to rest")


def crop_wm(src: Path, dst: Path):
    """Cat ✦ — cat phai 0,905W, trim 16:9 chia doi tren/duoi, resize lai."""
    im = Image.open(src).convert("RGB")
    W, H = im.size
    nw = int(W * 0.905)
    nh = round(nw * 9 / 16)
    top = (H - nh) // 2
    im.crop((0, top, nw, top + nh)).resize((W, H), Image.LANCZOS).save(dst)


def gate(p, tag):
    pos = p.find("NO TEXT")
    assert pos * 100 // len(p) <= 15, f"{tag}: guard nam qua sau"
    for b in BANNED:
        assert b not in p, f"{tag}: token cam {b}"
    return pos * 100 // len(p)


def build(base_dir=None):
    img = []
    for i, (role, frame, pose) in enumerate(IMGS, 1):
        who = K if i == 1 else REF + K
        p = " ".join([IMG_GUARD, IMG_HEAD, f"SUBJECT: {who}, {pose}.",
                      f"FRAMING: {frame}, the camera at her own seated eye height, from the chair of a producer "
                      f"across the table.", f"ROOM: {STUDIO}.", IMG_LIGHT, IMG_END])
        g = gate(p, f"img {i}")
        img.append(p)
        print(f"IMG  pod_{i:02d} {len(p):5d} ky  guard@{g}%  {role}")
    (OUT / "podcast_IMG_FLOW.txt").write_text("\n".join(img) + "\n", encoding="utf-8")

    srcs = sorted(p for p in Path(base_dir).iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg")) if base_dir else []
    if base_dir:
        assert len(srcs) == len(CLIPS), f"can {len(CLIPS)} anh theo thu tu A-E, co {len(srcs)}"
        BASE.mkdir(parents=True, exist_ok=True)
    flow, ten = [], ["dong FLOW | anh upload | vai | may | nhip 1 noi | ten clip tra ve"]
    for i, (role, cam, talk, act) in enumerate(CLIPS, 1):
        base = BASE / f"pod_{i:02d}.png"
        if srcs:
            crop_wm(srcs[i - 1], base)
        camb = (DRIFT_CAM if cam == "drift" else LOCKED_CAM)(WHERE, HEIGHT)
        p = " ".join([GUARD, STYLE, camb, "ACTION: " + act, TALK if talk else QUIET, GENTLE, END])
        g = gate(p, f"pod_{i:02d}")
        flow.append(p)
        ten.append(f"{i:2d} | {base.name} | {role} | {cam} | {'co' if talk else 'khong'} | pod_{i:02d}.mp4")
        print(f"CLIP pod_{i:02d} {len(p):5d} ky  guard@{g}%  {cam:5s} {role}")
    (OUT / "podcast_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (OUT / "podcast_TENFILE.txt").write_text("\n".join(ten) + "\n" + REUSE, encoding="utf-8")
    print(f"OK -> {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="thu muc 5 anh nguoi ke da gen (thu tu A-E) -> cat ✦ vao podcast_base/")
    build(ap.parse_args().base)
