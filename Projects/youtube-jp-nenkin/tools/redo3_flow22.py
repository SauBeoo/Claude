# -*- coding: utf-8 -*-
r"""redo3_flow22.py — VONG 3 gen lai video 22: **3 khe** con lai.

Lo vong 2 (2026-09-10 21:33, 10 clip) da chua 7/10 khe:
  c22_00 (khung anh tho TRON) · c22_07 (bac tam cap sach) · c22_22 (bang tuong sach) ·
  c22_31_2 (360,000 4/15 360,000 — DUNG ca hai) · c22_38 (to khai chu nho) ·
  c22_39 (man hinh bang chu nho) · c22_53 · c22_69 (giay chu nho).
Con lai:
  · `c22_46` — Flow **KHONG tra clip 2/2 lan** (vong 1 va vong 2 deu thieu dung khe nay)
  · `c22_31_1` — 360000 dung gia tri nhung **thieu dau phay**, va **cast khong phai nguoi Nhat**
  · `c22_02` — 360,000 dung, nhung con **mot dong rac** `36 0, 04/5` ben duoi

🔴🔴 LOI CUA CHINH VONG 2, tim ra khi doc lai prompt DA XUAT RA (khong phai khi viet):
   `redo2` chi thay **cai duoi cua cau**, de nguyen **cai dau**. Ket qua o khe `NONE`:
     "...exactly two rows are printed MUCH LARGER and highlighted in a pale colour band,
      in CRISP ARABIC NUMERALS the camera reads easily: no large number ... appears anywhere"
   Tuc mot cau **tu chọi**: doi hai dong so TO roi ngay sau do cam so to.
   Vong 2 van ra dung o 3/3 khe NONE co man hinh — nhung do la **may**, khong phai thiet ke.
   ⇒ Vong 3 thay **CA CLAUSE** (dau + duoi), theo tung KHUON:
        SCREEN  -> clause "Out of all that, exactly two rows ... dense texture."
        BOOK    -> clause "Two of those lines are printed noticeably LARGER ..."
        FORM    -> clause "BUT two amount cells are filled in with LARGE CRISP ..."
   Va gate moi: khe `NONE` khong duoc con **bat ky** tu `LARGER` / `CRISP` / `reads easily`.
   📌 Lan thu BA cung mot benh trong mot video (`feedback_prompt_khoi_chung_huy_mo_ta`).
      Bai hoc dung: **vá xong phai doc lai dong thanh pham** — va gate phai kiem CA CLAUSE,
      khong chi kiem cai chuoi minh vua thay.

⚠️ `c22_46` bi Flow bo qua HAI lan lien tiep => khong retry y nguyen. Doi cach ta chu the
   (bo cum "a young female clerk", dung "a female office worker in her thirties") va bo cum
   "points at" — giu NGHIA (co nguoi dung canh man hinh, tay huong vao nua phai) nhung doi
   token. Neu lan nay van thieu thi ket luan la **prompt bi loc**, va phai doi han khuon
   scene 46 trong `_scenes22.py` (vd bo nguoi, chi con man hinh).

CHAY:  python tools/redo3_flow22.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flow22_full as F                                             # noqa: E402

VD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "06_VIDEO", "22_mishikyu-nenkin-36man")

SLOTS = {
    "c22_02":   ("ONE",  "360,000 dung nhung con dong rac 36 0, 04/5 ben duoi"),
    "c22_31_1": ("PAIR", "360000 thieu dau phay + cast khong phai nguoi Nhat"),
    "c22_46":   ("NONE", "Flow khong tra clip 2/2 lan — doi cach ta chu the"),
}

# ── CLAUSE DAY DU cua tung khuon, dung lai tu chinh hang cua flow22_full ────
#    (dung F.FIG de neu hang doi thi cho nay tu vo, khong lech im lang)
CL_SCREEN = ("Out of all that, exactly two rows are printed MUCH LARGER and highlighted in a "
             "pale colour band, in CRISP ARABIC NUMERALS the camera reads easily: "
             + F.FIG + "; every other figure is tiny dense texture.")
CL_BOOK = ("Two of those lines are printed noticeably LARGER and read clearly in CRISP ARABIC "
           "NUMERALS: " + F.FIG + "; the rest are tiny dense print")
CL_FORM = ("BUT two amount cells are filled in with LARGE CRISP ARABIC NUMERALS the camera "
           "reads clearly: " + F.FIG)

# ── ba ban thay ────────────────────────────────────────────────────────────
# PAIR (chi cho SCREEN): hai dong BANG NHAU, danh van tung chu so, ep dau phay
PAIR_SCREEN = (
    "Out of all that, exactly two rows are printed MUCH LARGER and highlighted in a pale "
    "colour band, and nothing else on the screen is highlighted. Both highlighted rows show "
    "the SAME amount, written with a thousands comma as the seven characters 3 6 0 , 0 0 0 — "
    "a three, a six, a zero, then a comma, then three zeros — and the comma is clearly there "
    "in both. The upper row has the date 4/15 beside it, the lower row the date 6/15. Those "
    "two are the only large figures in the whole frame: no third large figure, no second copy "
    "of the table, no other highlighted row anywhere in the shot; every other figure is tiny "
    "dense texture.")

# ONE (cho BOOK): dung MOT dong to, va cam manh dong-rac-thu-hai
ONE_BOOK = (
    "Exactly ONE line on the open page is printed noticeably LARGER than the rest and lightly "
    "highlighted, and it reads the amount written with a thousands comma as the seven "
    "characters 3 6 0 , 0 0 0 — a three, a six, a zero, then a comma, then three zeros — with "
    "the date 4/15 beside it. No other line on the page is enlarged, highlighted, or partly "
    "enlarged: there is no second copy of that amount, no half-sized repeat of it, and no "
    "cropped or broken fragment of it anywhere on the page. Every other line is tiny dense "
    "print")

# NONE: bo han yeu cau so; giay/man hinh van KIN chu nho
NONE_ANY = (
    "No row and no cell on the screen is enlarged or highlighted, and no large number and no "
    "large word appears anywhere in the frame. The whole display stays a dense grey texture of "
    "very small figures filling it right to its edges, with almost no empty white space, and "
    "none of it is large enough to read.")

BG = (" Wall signs, notice boards, price boards, desk calendars, posters, leaflets and small "
      "table cards or tags are plain blank coloured panels with no writing and no figures on "
      "them. This applies ONLY to that background signage; papers, forms and computer screens "
      "keep their normal dense tiny print and must not be blank white.")

# khoa CAST — chi them cho khe co nguoi lo mat (bat duoc o c22_31_1: model tra nguoi da mau)
CAST_JP = (" The person in frame is JAPANESE, East Asian features, and is in their late "
           "sixties or seventies with grey hair; no other ethnicity appears in the shot.")

# ⚠️ c22_46 bi Flow bo qua 2/2 lan => doi TOKEN cua chu the, giu nghia
SUBJ_FROM = ("a monitor stands on a low cabinet, a young female clerk stands beside it and "
             "points at the right-hand side of the screen")
SUBJ_TO = ("a monitor stands on a low cabinet and a female office worker in her thirties, in a "
           "plain navy vest, stands beside it with one open hand held toward the right-hand "
           "half of the screen")


def main() -> int:
    items = []
    for r in F.build():
        if r["kind"] != "art" or r["nshot"] == 0:
            continue
        for k in range(r["nshot"]):
            suf = f"_{k+1}" if r["nshot"] > 1 else ""
            items.append(dict(stem=f"c22_{r['i']:02d}{suf}", scene=r["i"], telop=r["telop"],
                              kind=F.classify(r["body"]),
                              prompt=" ".join(F.prompt_for(r["body"], len(items)).split())))
    by = {x["stem"]: x for x in items}
    miss = [s for s in SLOTS if s not in by]
    if miss:
        print(f"GATE DO: khe khong khop flow22_FULL: {miss}")
        return 1

    rows, nocl = [], []
    for stem, (pol, why) in SLOTS.items():
        x = by[stem]
        p = x["prompt"]
        # 🔴 thay CA CLAUSE, khong chi thay cai duoi (loi cua vong 2)
        hit = False
        for cl, rep in ((CL_SCREEN, PAIR_SCREEN if pol == "PAIR" else NONE_ANY),
                        (CL_BOOK, ONE_BOOK if pol == "ONE" else NONE_ANY),
                        (CL_FORM, NONE_ANY)):
            if cl in p:
                p = p.replace(cl, rep)
                hit = True
                break
        if not hit:
            nocl.append(stem)
        if stem == "c22_46":
            if SUBJ_FROM not in p:
                print(f"GATE DO: khong tim thay chu the cu de doi o {stem}")
                return 1
            p = p.replace(SUBJ_FROM, SUBJ_TO)
        if pol == "NONE":
            p += BG
        if stem == "c22_31_1":
            p += CAST_JP
        # bo cau xin so-to o cuoi prompt cho khe NONE (mieng va cua vong 2, van can)
        if pol == "NONE":
            crisp = ("the only characters meant to be read in the frame are Arabic numerals — "
                     "yen figures and dates — printed large and crisp in a clean sans-serif; "
                     "any Japanese writing on signs, labels, book spines or form headings "
                     "stays small and softly out of focus")
            p = p.replace(crisp, "every document, form, ledger and screen in this shot stays "
                                 "densely covered in tiny print and none of it is large enough "
                                 "to read; no numeral and no word anywhere in the frame is "
                                 "printed large or crisp")
        rows.append((stem, x["scene"], x["kind"], x["telop"], pol, why, " ".join(p.split())))

    if nocl:
        print(f"GATE DO: khong tim thay CLAUSE so de thay o {nocl} — hang cua flow22_full "
              f"da doi, sua CL_SCREEN/CL_BOOK/CL_FORM cho khop")
        return 1

    rows.sort(key=lambda r: r[1])
    io.open(os.path.join(VD, "flow22_REDO3_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(r[6] for r in rows) + "\n")
    with io.open(os.path.join(VD, "flow22_REDO3_TENFILE.txt"), "w", encoding="utf-8") as fh:
        fh.write("# GEN LAI VONG 3 — ten file dich GIU NGUYEN, tha vao Downloads roi ingest\n")
        for i, (stem, sc, kind, tel, pol, why, _) in enumerate(rows, 1):
            fh.write(f"dong {i} -> {stem}.mp4   [scene {sc} - {kind} - so={pol}]  "
                     f"telop {tel} — {why}\n")

    print(f"OK flow22_REDO3_FLOW.txt     ({len(rows)} prompt)")
    print("OK flow22_REDO3_TENFILE.txt")
    ln = [len(r[6]) for r in rows]
    print(f"   dai prompt: {min(ln)}-{max(ln)} ky")

    # ── GATE ───────────────────────────────────────────────────────────────
    bad = [r[0] for r in rows if F.FIG in r[6] or "180,000" in r[6]]
    print(f"   {'ok' if not bad else 'GATE DO'} con cap 180,000/360,000 cu: {bad or 'khong'}")
    # 🔴 GATE MOI cua vong 3: khe NONE khong con MOT tu nao xin so to
    words = ("LARGER", "CRISP", "reads easily", "reads clearly", "large and crisp")
    left = [(r[0], w) for r in rows if r[4] == "NONE" for w in words if w in r[6]]
    print(f"   {'ok' if not left else 'GATE DO'} khe NONE con tu xin-so-to: {left or 'khong'}")
    n1 = [r[0] for r in rows if r[4] == "ONE" and ONE_BOOK not in r[6]]
    n2 = [r[0] for r in rows if r[4] == "PAIR" and PAIR_SCREEN not in r[6]]
    n0 = [r[0] for r in rows if r[4] == "NONE" and NONE_ANY not in r[6]]
    print(f"   {'ok' if not (n1 or n2 or n0) else 'GATE DO'} ban thay ap du "
          f"(ONE {not n1} · PAIR {not n2} · NONE {not n0})")
    c = [r[0] for r in rows if r[0] == "c22_31_1" and CAST_JP not in r[6]]
    print(f"   {'ok' if not c else 'GATE DO'} khoa cast JP cho c22_31_1: {c or 'co'}")
    s46 = [r[0] for r in rows if r[0] == "c22_46" and SUBJ_TO not in r[6]]
    print(f"   {'ok' if not s46 else 'GATE DO'} doi chu the c22_46: {s46 or 'co'}")
    for stem, sc, kind, tel, pol, why, _ in rows:
        print(f"     {stem:<9} scene {sc:>2} {kind:<7} so={pol}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
