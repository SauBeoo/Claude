# -*- coding: utf-8 -*-
"""
BÀI THỬ "REALISM" — 6 cảnh, góc THỨ BA, máy KHOÁ CỨNG, ảnh-trước-rồi-hoá-động (2026-09-22).

VÌ SAO CÓ FILE NÀY: user xem 異世界さんぽ (pJPST9DG92I) nói "video này rất thật, của tôi ảo quá".
Đo bằng máy (tools/check_realism.py --ref) thì khoảng cách KHÔNG nằm ở model (họ cũng Google Veo):
    MAD trong shot p50   họ 1,5   · lô mình cùng ngày 9,4
    % khung gần đứng yên họ 35,6% · mình 0,6%
    shot có MÁY DI       họ 32%   · mình 95%
    sáng TB / cháy trắng họ 65 / 0,5% · mình 111 / 3,6%
⇒ Bài thử này đổi đúng 4 biến, cùng lúc, trên 6 cảnh của bản Ⓑ:
    ① máy KHOÁ CỨNG góc thứ ba (không POV, không handheld)   ② ảnh tĩnh trước → Frames-to-Video
    ③ ánh sáng MỘT NGUỒN, mờ bụi, không cháy, nửa số cảnh tối  ④ prompt NGẮN ~1.000–1.400 ký
⚠️ Đây là A/B, KHÔNG phải luật mới: POV/HANDHELD của bản Ⓑ vẫn nguyên. So sánh bằng số + mắt rồi
   user quyết. Nếu thắng → mới bàn đổi công thức v3.

Chạy:  python tools/gen_test_realism.py
Xuất:  06_VIDEO/01_tou-no-fumoto/_realism/
         still_FLOW.txt    6 prompt ẢNH (bơm ở chế độ Image, 1 dòng/prompt)
         motion_FLOW.txt   6 prompt ĐỘNG cho Frames-to-Video (dán tay, kèm ảnh khung đầu)
         t2v_FLOW.txt      6 prompt t2v THUẦN cùng nội dung (đối chứng, bơm extension được)
         TENFILE.txt       thứ tự ↔ tên clip ↔ cách gen
         HUONG_DAN.md      bước bấm gì trong Flow + cách đo
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from blocks_s100 import (REALISM_HEAD, LOCKED_CAM, DRIFT_CAM, SUBJECT_GENTLE, LIGHT_MUTED,
                         SILENT_REALTIME, WORLD_SHORT, FILM_TAIL, STILL_HEAD)

S = lambda **k: k

# ─────────────────────────────────────────────────────────────────────────────
# 6 CẢNH — id khớp bản Ⓑ (gen_ep01_ichinichi.py) để so cùng cảnh.
#   where/height: chỗ NGƯỜI đứng được + chiều cao = tư thế người trong cảnh (camera-language §1)
#   still: khung hình đóng băng ở NHỊP 1 của hành động (chưa bung)
#   act:   3 nhịp tả bằng CƠ THỂ, đỉnh ở nhịp 2, vật lý của VẬT TO tự kể
#   alive: ≥2 thứ động liên tục ngoài hành động chính
# ─────────────────────────────────────────────────────────────────────────────
SCENES = [
 S(id="04_shutter", light="dawn", world=True,
   where="a neighbour standing in the lane across from the shop", height="standing eye height",
   still=("A narrow Japanese back lane before sunrise: a small family shop with its wooden slatted "
          "shutter still down, a blank painted board over the door, bicycles against the wall beside a "
          "red cylindrical post box, potted plants crowding the step, a street lamp with a fluted glass "
          "shade still burning. A man in his sixties in shirtsleeves, seen from behind, has just put "
          "both hands up to the bottom edge of the shutter."),
   act=("The shopkeeper, seen from behind, pushes the heavy wooden shutter up its runners — it rattles "
        "and rises in one long shove, the slats folding away overhead — he props it, then stands in "
        "his own doorway a moment with one hand on the small of his back, looking down the lane, before "
        "he turns and goes in."),
   alive="The lamp filament flickers; a cloth noren in the next doorway lifts and settles in the air."),

 S(id="09_mizumaki", light="day", world=True, cam="drift",
   where="someone on the opposite pavement", height="standing eye height",
   still=("A wide view of a small shopfront on a sunlit Japanese lane, potted plants crowding the step, a polished "
          "copper pipe running down the tiled wall, a canvas awning, bicycles against the tile, a "
          "shallow tin bucket held in both hands by a woman in an apron who has just drawn it back to "
          "throw; the lane opens out behind her towards the towers."),
   act=("The woman swings the bucket and the water leaves it in one flat sheet "
        "and slaps across the pavement — the dust goes dark where it lands and the air above "
        "it turns hazy. She watches the wet stone spread, tips the last of the water out at the foot of "
        "the plants, and goes back in."),
   alive="Water runs along the kerb; the awning edge stirs; leaves on the potted plants move in the air."),

 S(id="11_yaoya", light="day", world=True,
   where="the next customer waiting behind her", height="standing eye height, just over her shoulder",
   still=("A greengrocer's sloping stand of vegetables in wooden crates under a canvas awning at the open "
          "end of a market street, paper lanterns overhead, a mechanical brass cash register at the end "
          "of the counter, and beyond the end of the street the towers standing up in the sun. The grocer, a broad man in his fifties with a towel round his neck, holds a "
          "paper-wrapped parcel out over the crates with both hands towards a woman customer seen from "
          "behind."),
   act=("He holds the parcel out with both hands; she takes it and bows her head over it; his hands are "
        "already reaching back behind him for the next one before she has finished bowing, and he "
        "nods once to himself as he turns."),
   alive="Lanterns turn slowly on their cords; other shoppers pass out of focus behind them."),

 S(id="14_shokudou", light="interior", world=False,
   where="a customer sitting two stools along the counter", height="seated eye height at the counter",
   still=("Along the worn timber counter of a small Japanese eating house: jars and bottles crowding the "
          "shelves, a glass globe lamp in a brass cage, an electric fan with a brass cage at the end of "
          "the counter, the bright doorway onto the street beyond. A woman in her forties in a green "
          "apron leans over the counter setting a steaming bowl of noodles down in front of a man in "
          "shirtsleeves who sits with his back three-quarters to the camera."),
   act=("She sets the bowl down and the steam comes straight up off it into his face; he leans back from "
        "it, blinks, then leans in again and picks up his chopsticks, and she is already turning away to "
        "the pot behind her."),
   alive="Steam rises and leans in the fan's air the whole time; the fan turns; light shifts in the doorway."),

 S(id="21_sentou", light="dusk", world=True, cam="drift",
   where="someone waiting on the pavement opposite", height="standing eye height",
   still=("A Japanese bathhouse entrance at dusk, a cloth noren in the doorway with the single word ゆ on "
          "it in large brush strokes, steam drifting out along the pavement beneath it, a rack of wooden "
          "clogs to one side, bicycles against the tiled wall, potted plants along the step, the first "
          "lamps of the street just switched on. An old man is halfway through the noren, a small towel "
          "on his head, his face still red from the heat."),
   act=("He comes out through the noren, stops on the step, lets his breath all the way out so his "
        "shoulders drop, rubs the towel once over the back of his neck, and stands there in the cool air "
        "a moment before he steps down and starts along the street."),
   alive="Steam pours out under the noren and lifts in the lamp light; the noren swings back and settles."),

 S(id="27_yuushoku", light="night", world=False,
   where="a third person sitting at the free side of the low table", height="seated eye height at the table",
   still=("A small Japanese front room at night around a low wooden table, one glass globe lamp in a "
          "brass cage lit warm above it, bowls and a shared dish on the wood, worn tatami, the window a "
          "black rectangle, a television in a timber cabinet dark in the corner. A woman of about forty "
          "and an old man sit at the table eating, both seen in three-quarter view, her hand just "
          "reaching towards the shared dish."),
   act=("Without looking up from her own bowl she slides the shared dish across the wood until it is in "
        "front of him; he takes from it, chews, and only then glances at her — and she has already "
        "looked back down. Steam rises off both bowls between them."),
   alive="Steam rises off the bowls; the lamp filament breathes; a moth circles the lamp."),
]


def cam_block(sc):
    return (DRIFT_CAM if sc.get("cam") == "drift" else LOCKED_CAM)(sc["where"], sc["height"])


def motion_prompt(sc):
    """Prompt cho FRAMES-TO-VIDEO (ảnh khung đầu đã tải thế giới + ánh sáng) — chỉ nói máy + hành động."""
    P = [REALISM_HEAD,
         cam_block(sc),
         "Starting from exactly the framing of the first frame: " + sc["act"],
         SUBJECT_GENTLE,
         sc["alive"],
         LIGHT_MUTED[sc["light"]],
         SILENT_REALTIME]
    return " ".join(P)


def t2v_prompt(sc):
    """Cùng cảnh, KHÔNG ảnh khung đầu — đối chứng cho câu 'ảnh-trước có hơn không'."""
    P = [REALISM_HEAD,
         cam_block(sc),
         sc["still"],
         sc["act"],
         SUBJECT_GENTLE,
         sc["alive"],
         LIGHT_MUTED[sc["light"]],
         SILENT_REALTIME]
    if sc["world"]:
        P.append(WORLD_SHORT)
    P.append(FILM_TAIL)
    return " ".join(P)


def still_prompt(sc):
    P = [STILL_HEAD, sc["still"], LIGHT_MUTED[sc["light"]],
         "Faces in three-quarter view or looking down, nobody looking at the camera, no face filling the frame."]
    if sc["world"]:
        P.append(WORLD_SHORT)
    P.append("Shallow depth of field, one out-of-focus object at the near edge of the frame, evenly exposed "
             "into all four corners, fine film grain.")
    return " ".join(P)


BAD = ("dolly", "handheld", "35mm", "16mm", "vivid", "hdr", "sunny", "bright blue sky", "cinematic",
       "masterpiece", "8k", "push in", "pull back", "pan ", "tracking shot", "slow motion")


LIMIT = {"motion": (1300, 2100), "t2v": (1800, 3300)}   # motion khong tai the gioi/anh sang → ngan hon


def _strip_neg(lo):
    """Bo cac menh de phu dinh ('no handheld shake', 'never ...', 'not ...') truoc khi quet token cam —
    khong thi gate doc trung chinh cau cam cua minh (ai-video-regen.md §6, da dinh lan 3)."""
    return re.sub(r"\b(?:no|never|not|nothing)\b[^,.;—]*", " ", lo)


def gate(rows):
    fails = 0
    for sc, kind, p in rows:
        lo = p.casefold()
        probs = []
        if kind in LIMIT and not (LIMIT[kind][0] <= len(p) <= LIMIT[kind][1]):
            probs.append(f"do dai {len(p)} ngoai {LIMIT[kind][0]}–{LIMIT[kind][1]}")
        i = lo.find("no writing")
        if i < 0 or i * 100 // len(p) > 15:
            probs.append("guard chu/so khong o 15% dau")
        if kind != "still":
            j = max(lo.find("locked off"), lo.find("eases forward by no more than"))
            if j < 0 or j * 100 // len(p) > 30:
                probs.append("khoi may khoa khong o 30% dau")
        pos = _strip_neg(lo)
        for b in BAD:
            if b in pos:
                probs.append(f"token cam: {b!r}")
        if re.search(r"\d", p.replace("16:9", "")):
            probs.append("co chu so trong prompt (model hay in so len hinh)")
        if probs:
            fails += 1
            print(f"  🔴 {sc['id']} [{kind}]: " + " · ".join(probs))
    return fails


def main():
    vd = os.path.join(ROOT, "06_VIDEO", "01_tou-no-fumoto", "_realism")
    os.makedirs(vd, exist_ok=True)
    rows = []
    for sc in SCENES:
        rows += [(sc, "still", still_prompt(sc)), (sc, "motion", motion_prompt(sc)),
                 (sc, "t2v", t2v_prompt(sc))]
    for kind, fn in (("still", "still_FLOW.txt"), ("motion", "motion_FLOW.txt"), ("t2v", "t2v_FLOW.txt")):
        with io.open(os.path.join(vd, fn), "w", encoding="utf-8") as fh:
            fh.write("\n".join(p for sc, k, p in rows if k == kind) + "\n")
    with io.open(os.path.join(vd, "TENFILE.txt"), "w", encoding="utf-8") as fh:
        fh.write("# BAI THU REALISM — 6 canh x 3 file. Dong i cua moi FLOW = canh i.\n")
        fh.write("# still_FLOW -> anh khung dau (che do Image)  |  motion_FLOW -> Frames-to-Video voi anh do\n")
        fh.write("# t2v_FLOW -> cung canh, khong anh (doi chung). Tai clip ve dat ten theo cot 2/3.\n#\n")
        for i, sc in enumerate(SCENES, 1):
            fh.write(f"{i}\tR_{sc['id']}_i2v.mp4\tR_{sc['id']}_t2v.mp4\t{sc['light']}\t"
                     f"{'THAP xa' if sc['world'] else 'khong thap'}\n")
    print("BAI THU REALISM — 6 canh")
    for kind in ("still", "motion", "t2v"):
        L = [len(p) for sc, k, p in rows if k == kind]
        print(f"  {kind:6s}: {min(L)}–{max(L)} ky, TB {sum(L)//len(L)}")
    print("GATE:")
    bad = gate(rows)
    print("  ✅ SACH 18/18" if not bad else f"  🔴 {bad}/18 loi")
    print(f"-> {vd}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
