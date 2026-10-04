# -*- coding: utf-8 -*-
r"""redo_img21.py — prompt ANH TINH (text-to-image) cho 11 shot `still=True`.

User chot 2026-09-04: *"cai nay may dung hinh anh di. Chu video tao gen ra no
khong ro noi dung"*. 11 shot bang trang doi tu clip 8s sang **anh tinh**.

🔴 HAI LY DO, ghi ro de sau khong ai doi lai:
  ① Veo **khong viet duoc chu Nhat/so co nghia** — frame 10800 ban render thu ra
     「50 ≒ 50 0 ハ」 loang ngoang chiem ~1/4 khung (`media-library.md` §2.9).
  ② Bo chu, chi ve KY HIEU, thi clip 8s **van khong ro noi dung**: ve trong 8
     giay thi net ve chay loang ngoang theo tay, khong doc ra hinh gi.
  ⇒ Anh tinh: net ve la net TINH (da ve XONG), va user gen nhieu ban roi CHON.

📐 KHAC PROMPT VIDEO O BA CHO:
  · khong co `mo` (khong co hanh dong) — the bang la **da ve xong**, nguoi dan
    dang chi/nhin vao no;
  · **ta ky hieu that RO va DON GIAN** (mot vong tron / mot mui tui / dau ＋ ＝),
    vi anh tinh doc duoc nen ky hieu phai dung nghia;
  · them cau giu **1/5 duoi khung** thoang cho phu de chay qua.

⚠️ Anh AI CUNG nat chu => prompt **khong duoc yeu cau chu/so**. Mo ta TICH CUC
   (`the rest of the board is clean and empty`), ⛔ dung viet `no text` —
   bo loc Google doc TU KHOA, khong doc phu dinh (`_policy20.py` §①).

CHAY:  python tools/redo_img21.py
       → 06_VIDEO/<STEM>/flow21_REDO_IMG.txt      (11 prompt, moi prompt 1 dong)
       → 06_VIDEO/<STEM>/flow21_REDO_IMG_TENFILE.txt
       → 06_VIDEO/<STEM>/flow21_REDO_IMG_BLOCKS.md
"""
import collections
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scenes21 import CAST, PROP, SCENES              # noqa: E402
from _policy20 import GOOGLE_BLOCK, GOOGLE_SWAP       # noqa: E402
from _scenes20_real import POLICY_SWAP                # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)

IMG_STYLE = (
    "Photorealistic documentary photograph, 50mm lens at f/2.8, natural window "
    "light, muted warm colour grade, gentle film grain, shallow depth of field "
    "with a softly blurred background. Contemporary Japan, an ordinary "
    "middle-class study that looks genuinely lived in — worn edges, honest "
    "textures, a little everyday clutter. Calm, respectful and unposed, like a "
    "frame from a quiet documentary."
)
IMG_JP = (
    "The man shown is Japanese, of the age described, in modest everyday "
    "Japanese clothing. His face carries his real age — lines, real skin "
    "texture, white hair."
)
IMG_FRAME = (
    "Composition: the board and the man share the frame, both large and clearly "
    "readable. The drawn marks on the board are crisp, simple and fully in "
    "focus. Keep the top fifth of the frame simple and open, and keep the bottom "
    "fifth of the frame quiet and free of anything important. Horizontal 16:9."
)
IMG_TAIL = "Quiet, natural, unstaged. A still photograph."

# ── KY HIEU tren bang, ta RO va DON GIAN cho tung shot ────────────────────
# 🔴 Day la phan THAY the cho `mo` cua ban video: the bang **da ve xong**, nen
#    ta KET QUA chu khong ta hanh dong. Ky hieu phai dung nghia cua loi doc.
MARKS = {
 # 🔴 SUA 2026-09-04 SAU KHI USER GEN: ban dau tao viet "with one firm diagonal
 #    stroke through it" — nhung bang DUYET tao lai ghi "vong tron TRON, chua
 #    gach" (co y: L14 chi noi "nhieu nguoi van nho so nay", con phu dinh moi den
 #    o L15). Tao sua BANG ma QUEN sua PROMPT => anh 001 ra y het anh 002.
 #    ⇒ Bai hoc: bang duyet va prompt phai sua CUNG MOT LUOT; bang duyet la thu
 #    user doc, prompt la thu may doc — lech nhau thi user duyet mot thu va nhan
 #    mot thu khac.
 "ooi_gokai": ("On the whiteboard a single large open ring is drawn in black "
               "marker, unbroken and complete, and the rest of the board is "
               "clean and empty. He stands beside the board with the marker "
               "still in his hand, looking at the ring."),
 "mou_tsukawanai": ("On the whiteboard a single large open ring with a diagonal "
                    "stroke through it is drawn in black marker, the rest of the "
                    "board clean and empty. He holds one thin open leaflet up "
                    "beside the board at chest height, level with the crossed "
                    "ring, looking between the two."),
 "yonjunana_agaru": ("On the whiteboard two short horizontal strokes are drawn "
                     "in black marker, one low and one high, with a long clear "
                     "arrow rising from the lower stroke to the higher one; the "
                     "rest of the board is clean and empty. He stands to one "
                     "side with the marker lowered, looking at the arrow."),
 "tashizan_te": ("On the whiteboard two short horizontal strokes are drawn one "
                 "under the other with a clear plus sign between them, a long "
                 "line ruled underneath, and one thicker stroke below that "
                 "line; the rest of the board is clean and empty. He stands "
                 "beside it with the marker held down at his side."),
 "rainen_mata": ("On the whiteboard three short horizontal strokes are drawn in "
                 "a column, a line ruled under the lower two, and a short arrow "
                 "rising to the topmost stroke; the rest of the board is clean "
                 "and empty. He stands well to one side so the whole column is "
                 "visible, marker lowered."),
 "sore_wa_chigau": ("On the whiteboard two large open rings are drawn side by "
                    "side with a clear equals sign between them and one line "
                    "ruled beneath both; the rest of the board is clean and "
                    "empty. He stands squarely beside the board, marker lowered, "
                    "one hand open toward the equals sign."),
 "hiku_mae_no_gaku": ("On the whiteboard two open rings sit side by side with an "
                      "equals sign between them, and around the left ring two "
                      "boxes are drawn, one inside the other, the outer box "
                      "noticeably larger; the rest of the board is clean and "
                      "empty. He stands at the board with the marker lowered."),
 "mitsume": ("The whiteboard is freshly wiped and clean, with three short "
             "hand-drawn tick marks in a column down its left edge and nothing "
             "else on it. A folded cloth rests in the easel tray beside the "
             "marker. He stands beside the board with one hand on the easel "
             "frame."),
 "juuminzei_tame": ("On the whiteboard two open rings are drawn one above the "
                    "other, with a long arrow running down from them to a firm "
                    "solid dot near the foot of the board; the rest of the board "
                    "is clean and empty. He has stepped back a full pace and is "
                    "looking at the arrow, marker down at his side."),
 "otoshiana": ("On the whiteboard a wide shallow curve is drawn across the "
               "middle like a dip, with one small filled circle sitting in the "
               "lowest part of the dip; the rest of the board is clean and "
               "empty. He stands to the left of the board, marker uncapped in "
               "his lowered hand, looking at the circle."),
 "uwanose": ("On the whiteboard one short thick stroke is drawn, with a much "
             "smaller stroke above and to its right, a plus sign between them "
             "and a line ruled beneath both; the rest of the board is clean and "
             "empty. He stands clear of the board with the marker lowered."),
}


def policy_clean(text, tally):
    for pat, sub in list(POLICY_SWAP) + list(GOOGLE_SWAP):
        new, k = re.subn(pat, sub, text)
        if k:
            tally[pat] += k
            text = new
    return re.sub(r"\s{2,}", " ", text)


def main():
    order = [sh["key"] for s in SCENES for sh in s.get("shots", [])]
    shots = {sh["key"]: sh for s in SCENES for sh in s.get("shots", [])}
    keys = [k for k in order if shots[k].get("still")]
    if set(keys) != set(MARKS):
        print(f"🔴 lech: still={sorted(keys)}\n   MARKS={sorted(MARKS)}")
        return 1

    tally = collections.Counter()
    out, rows, blocks = [], [], []
    blocks.append(
        "# flow21 REDO — 11 ANH TINH thay cho clip bang trang\n\n"
        "- Ly do: Veo khong viet duoc chu, va ngay khi bo chu thi clip 8s van "
        "khong ro noi dung (net ve chay loang ngoang theo tay).\n"
        "- **Gen ANH (text-to-image)**, khong phai video. Gen nhieu ban roi CHON "
        "ban co ky hieu dung nghia va net.\n"
        "- Ten file dich: `a21_<key>.png` — cho vao thu muc anh roi chay "
        "`python tools/ingest_art21.py <thu_muc>`.\n"
        "- ⚠️ Ban nao ma ky hieu ve sai nghia (vd mui tui chi xuong thay vi len) "
        "thi LOAI, dung 'de tam roi sua sau'.\n")

    for j, k in enumerate(keys, 1):
        sh = shots[k]
        cid = sh.get("cast")
        lk = ""
        if cid:
            lk = (f"CHARACTER {cid} — the same recurring character as in the rest "
                  f"of the series; keep the same age, hair, build and clothing: "
                  f"{CAST[cid]['lock']}.")
        pr = sh.get("props", [])
        if pr:
            parts = [PROP[pr[0]]] + [re.sub(r"^the SAME [^:]+: ", "", PROP[q])
                                     for q in pr[1:]]
            lk += " PROP LOCK — " + ", and ".join(parts) + "."
        p = f"{MARKS[k]} {lk} {IMG_JP} {IMG_STYLE} {IMG_FRAME} {IMG_TAIL}"
        p = policy_clean(re.sub(r"\s+", " ", p).strip(), tally)
        out.append(p)
        rows.append((j, order.index(k) + 1, f"a21_{k}.png", k))
        blocks.append(f"\n### {j:02d} · `a21_{k}.png` · (dong goc {order.index(k)+1:03d})"
                      f"\n\n**PROMPT (text → image):**\n```\n{p}\n```\n")

    def w(n, t):
        io.open(os.path.join(VD, n), "w", encoding="utf-8", newline="\n").write(t)

    w("flow21_REDO_IMG.txt", "\n".join(out) + "\n")
    w("flow21_REDO_IMG_TENFILE.txt",
      "thu_tu_bom\tdong_goc\tanh (GIU NGUYEN TEN)\tkey\n"
      + "\n".join(f"{j}\t{n:03d}\t{fn}\t{k}" for j, n, fn, k in rows) + "\n")
    w("flow21_REDO_IMG_BLOCKS.md", "\n".join(blocks) + "\n")

    # GATE
    gb = collections.Counter()
    for i, x in enumerate(out, 1):
        for pat in GOOGLE_BLOCK:
            c = len(re.findall(pat, x, re.I))
            if c:
                gb[pat] += c
    dup = {(i, m.group(0)) for i, x in enumerate(out, 1)
           for m in re.finditer(r"\b([a-z][\w-]{2,})\s+\1\b", x, re.I)}
    lens = [len(x) for x in out]

    print(f"→ {VD}")
    print(f"   flow21_REDO_IMG.txt      {len(out)} prompt text→image "
          f"({min(lens)}–{max(lens)} ky)")
    print(f"   flow21_REDO_IMG_TENFILE.txt · _BLOCKS.md")
    if tally:
        print(f"   policy_clean: doi {sum(tally.values())} cum")
    print()
    for j, n, fn, k in rows:
        print(f"   bom thu {j:2d}  ->  {fn:32s} (dong goc {n:03d})")
    bad = False
    if gb:
        bad = True
        print(f"\n🔴 GATE TU KHOA GOOGLE: {dict(gb)}")
    if dup:
        bad = True
        print(f"\n🔴 GATE TU LAP: {sorted(dup)[:6]}")
    print("\n✅ GATE SACH" if not bad else "")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
