# -*- coding: utf-8 -*-
"""flow25_3d.py — BIẾN THỂ 3D của lô test video 25 (user: *"hay gen theo 3d đi xem nào"*).

⚠️ ĐỌC TRƯỚC KHI DÙNG — đây là NHÁNH THỬ, không phải bản thay thế:
  · `vox-director` **không có theme 3D**: cả 10 THEME_PRESET đều là ngôn ngữ IN PHẲNG
    (collage / poster / zine / ink), và guard của chính nó hard-code
    「Stay flat 2D — no 3D rotation, no perspective change」 + 「NOT CGI, NOT a 3D render」.
    ⇒ Đi 3D là **đi ngược engine**, nên khối style + guard ở đây viết tay hoàn toàn.
  · Bản collage vẫn giữ nguyên ở `vox25_TEST10.txt`. File này xuất ra `vox25_TEST10_3D.txt`
    để **so cạnh nhau** — đó mới là cách quyết, không phải thay mù.

⭐ CHỌN "PAPERCRAFT DIORAMA" chứ không phải 3D bóng bẩy, vì ba lý do đo được:
  1. Giữ được BẢN SẮC GIẤY của kênh ⇒ thẻ 原典, telop, mascot, dải punch đang dùng vẫn khớp;
     đổi sang 3D render bóng loáng là phải làm lại cả lớp Remotion.
  2. Chữa đúng cái user chê ở bản collage: *"phẳng lì, không khối, nhân vật chìm vào nền"*.
     Diorama có ÁNH SÁNG THẬT ⇒ có bóng đổ, có khối, nhân vật tách khỏi nền.
  3. Giữ được guard **KHÔNG CHỮ** — vật thể thật thì không sinh chữ Nhật giả như nền báo.

Chạy:  python tools/flow25_3d.py      → 06_VIDEO/25_.../vox25_TEST10_3D.txt (+ _TENFILE)
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scenes25 import SCENES                                  # noqa: E402

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\25_nenkin-tenbiki-tetori-6man2sen")

# 10 beat của lô test — CÙNG bộ với bản collage để so được cạnh nhau
TEST = [0, 1, 2, 5, 9, 11, 26, 32, 47, 73]

# ── Dịch ngôn ngữ GIẤY PHẲNG sang VẬT THỂ trong không gian ─────────────────────
# 🔴 Thứ tự quan trọng: cụm DÀI phải đứng trước cụm ngắn, nếu không cụm ngắn ăn mất.
SWAP = [
    # 🔴 Cụm này nằm GIỮA danh từ và động từ ("an elderly woman [X] holds …") nên bản thay
    #    phải là MỆNH ĐỀ PHÂN TỪ, không phải danh ngữ — bản đầu cho ra
    #    "woman a hand-sculpted miniature figure holds" (mất liên từ).
    ("cut from a bold vintage printed illustration, thick white die-cut border",
     "sculpted as a poseable miniature figure"),
    ("cut from a bold vintage printed illustration", "sculpted as a poseable miniature figure"),
    ("cut from grainy photographic paper", "sculpted as a poseable miniature figure"),
    ("cut from deep red card is pasted flat on the newsprint",
     "stands on the set as a solid object in deep red, casting its own shadow"),
    ("cut from mustard card is pasted flat", "stands on the set as a solid mustard-yellow object"),
    ("is pasted flat on the newsprint", "stands upright on the set, casting its own shadow"),
    ("pasted flat on the newsprint", "standing upright on the set"),
    ("pasted flat", "standing upright"),
    ("cut from deep red card", "moulded in deep red"),
    ("cut from mustard card", "moulded in mustard yellow"),
    ("cut from charcoal card", "moulded in charcoal"),
    ("cut from cream card", "moulded in cream"),
    ("cut-out paper coins", "little metal coins"),
    ("cut-out coins", "little metal coins"),
    ("paper cut-outs", "miniature objects"),
    ("cut-outs", "miniature objects"),
    ("cut-out", "miniature"),
    ("torn paper", "folded card"),
    ("paper ", "miniature "),
    ("the newsprint", "the tabletop"),
]

STYLE = (
    "A STOP-MOTION MINIATURE DIORAMA, shot on a real tabletop set — everything in frame is a "
    "physical hand-made object with real volume, real weight and real cast shadows, in the "
    "style of a handcrafted papercraft/felt animation. Built from layered card, felt, wood and "
    "clay, with visible material texture: paper fibre, felt fuzz, thumb marks in the clay, "
    "slightly imperfect hand-cut edges. Warm soft key light from one side with a gentle fill, "
    "so every object throws a soft directional shadow onto the surface behind it. Shallow depth "
    "of field: the main subject is crisply in focus and the deep background falls softly out of "
    "focus. Palette: one dominant deeply saturated ground colour plus deep red, mustard yellow "
    "and charcoal; rich saturated materials, mid-dark overall, never pale or washed out. "
    "Miniature-set realism, tactile and handmade, NOT a slick CGI product render and NOT a "
    "cartoon."
)

CHAR = (
    " CHARACTER CRAFT — the people are hand-made poseable miniature figures with real sculpted "
    "volume: clearly modelled faces with warm skin tone and specific, readable expressions, "
    "hair in soft dark fibre, hands properly sculpted with separate fingers. Their clothes are "
    "real cloth — deep indigo, crimson, forest green, warm ochre — with visible woven texture "
    "and real folds that catch the light. The figures are the richest, most detailed, "
    "best-lit thing in the frame and stand clear of the background."
)

COMP = (
    " THE SET IS COMPLETE IN THE VERY FIRST FRAME and stays that way: every figure, prop and "
    "background piece is already built and placed when the shot opens, and the arrangement "
    "never changes. Nothing enters the frame and nothing leaves it. Dress the set richly — "
    "around a dozen distinct built objects, layered front to back, so no large area of bare "
    "background is left empty. The main figures are LARGE in frame, cropped by the frame edges "
    "like a close set photograph."
)

GUARD = (
    " Any person shown is JAPANESE and elderly (60s-70s), in modest everyday Japanese clothing "
    "— not Western, not American, not 1950s retro fashion. NUMERALS ARE WANTED: where the scene "
    "names a figure, build it as BIG bold three-dimensional Arabic numerals standing on the set. "
    "Every other surface stays blank: no words in any language, no Japanese lettering, no "
    "headline, no caption, no signage, no logo, no watermark — every document, sign and label "
    "is left empty apart from those built numerals. Leave a narrow empty strip along the right "
    "edge, about one tenth of the width."
)

MOTION_TAIL = (
    " MOTION: the camera is locked off on a tripod. All of the movement belongs to the figures "
    "and the objects they handle, animated in smooth stop-motion: limbs and props travel a long "
    "way across the set in generous, flowing arcs at one even speed, continuing from the first "
    "frame to the last. The set dressing and background hold their places. Aspect ratio 16:9."
)


# 🔴 Kho MOTION viết cho bản GIẤY nên đầy "head strip / eye strips / paper palms / on its
#    tape" — dán nguyên vào bản 3D là tả một con rối giấy trong một cảnh vật thể thật.
MOTION_SWAP = [
    ("head strip", "head"), ("shoulder strips", "shoulders"), ("eye strips", "eyes"),
    ("brow strip", "brow"), ("chest strip", "chest"), ("chin cut-out", "chin"),
    ("paper palms", "hands"), ("paper hand", "hand"), ("paper thumb", "thumb"),
    ("paper figures", "miniature figures"), ("paper finger", "finger"),
    ("on its tape", "on its base"), ("on their tape", "on their base"),
    ("torn half-square", "folded card tile"), ("half-squares", "card tiles"),
    ("paper stools", "miniature stools"), ("paper board", "little board"),
]


def to3d(body: str) -> str:
    b = re.sub(r"^[A-Z_]+:\s*", "", body)          # bỏ tiền tố khuôn (HOLD:/VIZ:/CROWD:…)
    for a, c in SWAP + MOTION_SWAP:
        b = b.replace(a, c)
    return b


def main() -> int:
    from beats25 import MOTION                     # dùng lại 10 chuyển động đã viết tay
    rows, names = [], []
    for i in TEST:
        ln, kind, telop, body = SCENES[i]
        scene = to3d(body)
        mo = MOTION.get(i, "")
        mo = to3d(mo) if mo else ""
        p = (STYLE + " SCENE (built on the tabletop set): " + scene.rstrip(".") + "."
             + CHAR + COMP + GUARD
             + (" ELEMENT MOTION: " + mo.rstrip(".") + "." if mo else "")
             + MOTION_TAIL)
        p = " ".join(p.split())
        rows.append(p)
        names.append(f"clip_{i}a.mp4   {telop}")
    io.open(os.path.join(VD, "vox25_TEST10_3D.txt"), "w",
            encoding="utf-8", newline="\n").write("\n".join(rows) + "\n")
    with io.open(os.path.join(VD, "vox25_TEST10_3D_TENFILE.txt"), "w",
                 encoding="utf-8", newline="\n") as f:
        for n, nm in enumerate(names, 1):
            f.write(f"dong {n:2d} -> {nm}\n")
    print(f"OK  {len(rows)} prompt 3D -> {VD}\\vox25_TEST10_3D.txt")
    print(f"    do dai {min(map(len, rows))}-{max(map(len, rows))} ky")
    # gate: khong con tu giay-phang sot lai
    bad = {}
    for w in ("paper cut-out", "pasted flat", "newsprint", "flat 2D", "die-cut",
              "printed illustration", "halftone"):
        c = sum(1 for r in rows if w in r)
        if c:
            bad[w] = c
    print("    GATE tu giay-phang sot:", bad if bad else "SACH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
