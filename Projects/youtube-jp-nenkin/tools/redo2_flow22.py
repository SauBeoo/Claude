# -*- coding: utf-8 -*-
r"""redo2_flow22.py — VONG 2 gen lai video 22: **4 khe** con sai sau lo 2026-09-10 20:02.

Soi mat 25/25 clip lo redo (sheet 3 frame/clip, 1:1) -> **21 khe SACH**, va:
   · `c22_02` — so van ghi `36,000` + `36,0000` (dung phai 360,000)          SO SAI
   · `c22_38` — to khai van ghi `1800000` + `36,0000`                        SO SAI
   · `c22_46` — Flow KHONG tra clip cho khe nay (doi lai tra 2 ban `c22_28`) THIEU
   · `c22_69` — Flow KHONG tra clip cho khe nay (doi lai tra 2 ban `c22_37_3`) THIEU

NGUYEN NHAN GOC — tim duoc o luot nay, va no la LOI THIET KE, khong phai model dot:
   `flow22_full.py` nhet hang `FIG = "the two highlighted lines read 180,000 and 360,000 with
   the dates 4/15 and 6/15"` vao **CA BA** khoi `BOOK` · `FORM` · `SCREEN_NOTE` => **22/62 khe**
   (19 SCREEN + 3 HOLD) deu bi yeu cau hien DUNG cap so do, bat ke scene noi ve gi:
     · scene 38 "answer is the notification" — noi ve shibou-todoke, khong co dong nao
     · scene 46 "stop is automatic / receiving is manual" — noi ve thu tuc
     · scene 69 "that is where it is dangerous" — noi ve rui ro bi bo sot
   So khong co NEO NGU NGHIA trong canh => model coi no la hoa van va bop meo (`36,000`,
   `1800000`, `36,0000`). Va mot cap so nhan len 22 khe thi xac suat co khe meo ~ 1.
   => Va theo TUNG KHE bang **chinh sach so**, khong bang them cau ep:
        NONE  — scene khong noi ve tien  => **bo han** yeu cau so, giay/man hinh kin chu nho
        ONE   — scene noi MOT con so     => chi hoi DUNG con so do
        PAIR  — scene so hai lan chuyen  => moi hoi cap (vong 1 da ra dung o 6/6 khe PAIR)
   Cung benh `feedback_prompt_khoi_chung_huy_mo_ta`: khoi chung huy mo ta rieng.

TEN FILE DICH GIU NGUYEN (`c22_<scene>.mp4`) => tha clip moi vao cung thu muc roi ingest lai.

CHAY:  python tools/redo2_flow22.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flow22_full as F                                             # noqa: E402

VD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "06_VIDEO", "22_mishikyu-nenkin-36man")

# khe -> (chinh sach so, ly do gen lai)
#   6 khe dau = SO SAI GIA TRI tren chu the chinh (pham YMYL: so tren hinh choi loi doc)
#   4 khe sau = CHU NHOE tren dao cu NEN (bang gia, lich, bac tam cap, giay doc)
SLOTS = {
    # -- so sai gia tri ------------------------------------------------------
    "c22_02":   ("ONE",  "so van ghi 36,000 + 36,0000 — scene 36-man-en ga haitta: MOT so"),
    "c22_31_1": ("PAIR", "man hinh 36,0000 — scene onaji 36-man-en daga: HAI dong BANG NHAU"),
    "c22_31_2": ("PAIR", "man hinh 180,0000 — cung scene 31, shot 2"),
    "c22_38":   ("NONE", "to khai 1800000 / 36,0000 — scene kotae wa todoke: khong noi ve tien"),
    "c22_39":   ("NONE", "laptop 180000 / 36,000 — scene shibou-todoke o dasu: khong noi ve tien"),
    "c22_46":   ("NONE", "man hinh 180000 / 36,000 — scene tomeru wa jidou: khong noi ve tien"),
    # -- chu nhoe o dao cu NEN ----------------------------------------------
    #    c22_00 la ENTRY 0 — frame nguoi xem thay ngay sau thumbnail (`media-library.md`
    #    §2.0), nen mot chi tiet nhoe o day dat hon han o giua bai: khung anh tho in
    #    「¥¥60618日 …円」 thay vi mot buc anh.
    "c22_00":   ("NONE", "khung anh tho in so nhoe (YY60618 / ...en) — ENTRY 0"),
    "c22_07":   ("NONE", "so nhoe 034518 / 249 khac tren bac tam cap be tong"),
    "c22_22":   ("NONE", "bang gia tuong nhoe (Y1-tu 850 1000 / 760 3000)"),
    "c22_53":   ("NONE", "lich tuong nhoe (Y kyo-ji-kuwa / kushi-nen-en-en-en)"),
    "c22_69":   ("NONE", "chu doc tren hai to giay nhoe (YY0000)"),
}

# cau SO cua flow22_full, de cat/thay
FIG_SENT = "the two highlighted lines read 180,000 and 360,000 with the dates 4/15 and 6/15"

# ONE — mot con so duy nhat, viet ro tung chu so, va cam ban sao thu hai.
#   Hai ca meo cua vong 1 DEU co cap so bi ve HAI LAN (hai cot / hai ban) roi ban thu hai
#   degrade. Guard vong 1 noi "dung hai dong duoc to sang" nhung KHONG cam ban sao.
ONE = ("exactly ONE line on the page is printed larger than the rest and highlighted, and it "
       "reads the amount three hundred and sixty thousand yen written as the seven characters "
       "3 6 0 , 0 0 0 — a three, a six, a zero, then one comma, then three zeros — with the date "
       "4/15 beside it. That amount appears ONCE and only once in the whole frame: there is no "
       "second copy of it, no second column repeating it, no other large number and no other "
       "highlighted line anywhere in the shot. Every other line on the page is tiny dense "
       "illegible print")

# PAIR — scene 31 「同じ36万円だが」: hai lan chuyen tien BANG NHAU, nen hoi HAI dong
#   GIONG HET nhau. De hon han cap 180,000/360,000 cu (mot con so, viet hai lan) — va
#   dung noi dung hon: FIG cu hoi 180,000+360,000 la SAI ngay o chinh scene nay.
PAIR = ("exactly two rows on the screen are highlighted and nothing else is highlighted. The "
        "upper highlighted row reads the amount 3 6 0 , 0 0 0 with the date 4/15 beside it; the "
        "lower highlighted row reads the very same amount 3 6 0 , 0 0 0 with the date 6/15 "
        "beside it. The two amounts are IDENTICAL — each is a three, a six, a zero, then one "
        "comma, then three zeros — and they are the only two large figures in the whole frame: "
        "no third large figure, no second copy of the table, no other highlighted row anywhere "
        "in the shot. Every other row is tiny dense illegible print")

# NONE — khe khong noi ve tien: giay/man hinh van KIN chu nho, nhung KHONG co so to nao.
NONE = ("no large number and no large word appears anywhere in the frame. Every document, form, "
        "ledger and screen in this shot is instead densely covered in tiny print — many ruled "
        "rows and narrow columns of very small figures, a dense grey texture that fills the page "
        "or the display right to its edges and leaves almost no empty white space; none of it is "
        "large enough to read, and no cell is highlighted")

# 🔴🔴 KHOI CHUNG THU HAI, VA NO CHOI THANG VOI `NONE`. `flow22_full` dan cau nay vao
#    CUOI **moi** prompt: *"the only characters meant to be read in the frame are Arabic
#    numerals — yen figures and dates — printed large and crisp"*. O khe PAIR/ONE thi dung,
#    nhung o khe NONE thi no la mot loi XIN SO TO ngay sau khi ta vua CAM so to => model
#    lai tu bia. Bat duoc khi doc lai prompt xuat ra, KHONG phai khi viet no.
#    ⇒ Khe NONE phai thay CA cau nay, khong chi thay `FIG_SENT`.
#    📌 Lan thu HAI cung mot benh trong cung mot video (`feedback_prompt_khoi_chung_huy_mo_ta`):
#       vong 1 la `P0`, vong 2 la day. Bai hoc that: **doc lai prompt DA DUNG XONG**, dung
#       tin la sua hang nguon thi xong — hang khac co the noi nguoc lai.
CRISP_FROM = ("the only characters meant to be read in the frame are Arabic numerals — yen "
              "figures and dates — printed large and crisp in a clean sans-serif; any Japanese "
              "writing on signs, labels, book spines or form headings stays small and softly "
              "out of focus")
CRISP_TO = ("every document, form, ledger and screen in this shot stays densely covered in tiny "
            "print — many ruled rows and narrow columns of very small figures — and none of it "
            "is large enough to read; no numeral and no word anywhere in the frame is printed "
            "large or crisp")

# nen/bien hau canh phai TRON (giu nguyen mieng P3 da chung minh chay duoc o vong 1)
BG = (" Wall signs, notice boards, price boards, desk calendars, posters, leaflets and small "
      "table cards or tags are plain blank coloured panels with no writing and no figures on "
      "them. This applies ONLY to that background signage; papers, forms and computer screens "
      "keep their normal dense tiny print and must not be blank white.")


def main() -> int:
    # dung `items` GIONG HET flow22_full.main() — phai cung `idx` moi ra cung phong/sang/mau
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
        print(f"GATE: khe khong khop flow22_FULL: {miss}")
        return 1

    rows, nofig, nocrisp = [], [], []
    for stem, (pol, why) in SLOTS.items():
        x = by[stem]
        p = x["prompt"]
        rep = {"ONE": ONE, "PAIR": PAIR, "NONE": NONE}[pol]
        if FIG_SENT in p:
            p = p.replace(FIG_SENT, rep)
        elif pol in ("ONE", "PAIR"):
            # khe ONE/PAIR BUOC PHAI co cau FIG de thay — khong thi mieng va truot im lang
            nofig.append(stem)
        else:
            # khuon PANEL/PERSON khong co khoi man hinh/giay => khong co FIG. Noi THEM.
            p += " " + NONE + "."
        if pol == "NONE":
            if CRISP_FROM in p:
                p = p.replace(CRISP_FROM, CRISP_TO)
            else:
                nocrisp.append(stem)
            p += BG
        rows.append((stem, x["scene"], x["kind"], x["telop"], pol, why, " ".join(p.split())))

    rows.sort(key=lambda r: r[1])
    io.open(os.path.join(VD, "flow22_REDO2_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(r[6] for r in rows) + "\n")
    with io.open(os.path.join(VD, "flow22_REDO2_TENFILE.txt"), "w", encoding="utf-8") as fh:
        fh.write("# GEN LAI VONG 2 — ten file dich GIU NGUYEN, tha vao Downloads roi ingest lai\n")
        for i, (stem, sc, kind, tel, pol, why, _) in enumerate(rows, 1):
            t = tel.replace("\n", " / ")
            fh.write(f"dong {i} -> {stem}.mp4   [scene {sc} - {kind} - so={pol}]  "
                     f"telop {t} — {why}\n")

    print(f"OK flow22_REDO2_FLOW.txt     ({len(rows)} prompt)")
    print("OK flow22_REDO2_TENFILE.txt")
    ln = [len(r[6]) for r in rows]
    print(f"   dai prompt: {min(ln)}-{max(ln)} ky")

    # GATE: mieng va phai THAT SU an
    if nofig:
        print(f"   GATE DO: khe ONE/PAIR KHONG co cau FIG de thay: {nofig}")
        return 1
    # GATE: khe NONE khong duoc con MOT cau nao xin "so to, net"
    left = [r[0] for r in rows if r[4] == "NONE" and CRISP_FROM in r[6]]
    print(f"   {'ok' if not (left or nocrisp) else 'GATE DO'} khe NONE con cau xin so-to: "
          f"{left or 'khong'}" + (f"  — khong tim thay cau de thay o {nocrisp}" if nocrisp else ""))
    nf = sum(1 for r in rows if FIG_SENT not in r[6])
    print(f"   ok FIG: {nf}/{len(rows)} khe khong con cau cap-so goc")
    bad = [r[0] for r in rows if FIG_SENT in r[6] or "180,000 and 360,000" in r[6]]
    print(f"   {'ok' if not bad else 'GATE DO'} con cap 180,000/360,000: {bad or 'khong'}")
    n1 = [r[0] for r in rows if r[4] == "ONE" and ONE not in r[6]]
    n2 = [r[0] for r in rows if r[4] == "PAIR" and PAIR not in r[6]]
    n0 = [r[0] for r in rows if r[4] == "NONE" and NONE not in r[6]]
    print(f"   {'ok' if not n1 else 'GATE DO'} ONE ap du   "
          f"{'ok' if not n2 else 'GATE DO'} PAIR ap du   "
          f"{'ok' if not n0 else 'GATE DO'} NONE ap du")
    # cam chu gay TRANG (bai hoc luot truoc: user bao "man hinh va giay deu trang")
    WH = ("blank white paper", "nothing printed on the page", "empty white page")
    white = sorted({w for r in rows for w in WH if w in r[6]})
    print(f"   {'ok' if not white else 'GATE DO'} cum gay TRANG: {white or 'khong'}")
    for stem, sc, kind, tel, pol, why, _ in rows:
        print(f"     {stem:<9} scene {sc:>2} {kind:<7} so={pol}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
