# -*- coding: utf-8 -*-
r"""Nhap MINH HOA AI user gen -> slides_img_photo/slide_XX.jpg (video 18, style trang).

    python tools\ingest_slides_18.py "C:\Users\tuana\Downloads\<folder>"            # xem thu
    python tools\ingest_slides_18.py <src> --cut-x 1250 --apply                     # ghi that
    python tools\ingest_slides_18.py <src> --no-cut --apply                         # lo sach ✦
    python tools\ingest_slides_18.py --restore                                      # tra ban goc

⭐ VONG 3 (user chot 2026-08-21, dua anh khung san khau: "the may lam cho tao cai khung
nhu nay con dep hon do"): BO canvas trang tron, dat minh hoa vao KHUNG SAN KHAU —
nen gradient + THE TRANG BO GOC + bong do + 2 nhan vat cat-nen o 2 mep + DAI DEN day.
  - 🔴 Goi lai CHINH ham cua `_media_library/make_stage.py` (`stage_base` / `put_cast` /
    `sub_bar`) => khung giong khit khung cua health/nenkin, va KHONG sinh bo hang so thu
    hai de lech (bai hoc `stage-zu-layout.md` §4 "mot viec, mot tang"). Doi khung o
    make_stage thi file nay tu an theo.
  - Anh dat COVER-CROP phu tron the (user chot: het moi duong mep, hinh to nhat cho tep
    45+; danh doi la cat ~8% moi ben — noi dung minh hoa deu can giua nen an toan).
  - Phu de: dai den da BAKE trong anh => `sub_style` doi "kuro" (chu DEN) -> "outline"
    (chu TRANG vien den) + `sub_marginv 12`, giong health khi dung san khau. Chu den tren
    dai den = chim hoan toan.
⤵ Vong 2 (da bo): pad len canvas 1920x1080 TRANG, anh 1920x890@y0, dai trang 190px duoi.

WATERMARK ✦ (media-library.md §2.10 ⑤/⑤b): toa do KHAC NHAU giua cac LO —
KHONG hardcode. Soi MAT 5-8 anh goc duoi-phai roi truyen --cut-x (mep TRAI cua ✦
tru ~15px an toan). Lo 1376x768 truoc gio: ✦ quanh x 1214-1278. Thieu co va
khong co --no-cut → tool TU CHOI chay (de khong lap lai ca "1 anh nen xam co tia
dai" cua nenkin 12).
"""
import argparse
import io
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, r"E:\Claude\Projects\_media_library")
import make_stage as MS                                                    # noqa: E402

# 🔴 Neo vao FD 1, KHONG dung sys.stdout.buffer: `make_stage` cung boc lai sys.stdout luc
# import, nen boc theo .buffer cua no thi buffer goc bi dong khi wrapper kia bi GC
# ("ValueError: I/O operation on closed file" ngay dong print dau tien).
sys.stdout = io.TextIOWrapper(io.FileIO(1, "w"), encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "18_ringo-tabekata"
IMG = VD / "slides_img_photo"
ORIG = VD / "_wm_orig"

# ── KHUNG SAN KHAU: hang so lay TU make_stage, khong chep lai ────────────────
# card 1376x846 @ (272,56) · bo goc 28 · dai den tu y=928 (cao 152) · cast cao CH_H=560
CARD = (MS.CARD_X0, MS.CARD_Y0, MS.CARD_X1, MS.CARD_Y1)
CW, CH = MS.CARD_X1 - MS.CARD_X0, MS.CARD_Y1 - MS.CARD_Y0

# Cast RIENG cua shokutaku (user chot 2026-08-21: gen bo rieng dung style pastel, KHONG
# dung chung cast health — cast health la line-art anime, dat canh minh hoa flat pastel
# thi lech style ro; va 2 kenh cung tep senior JP dung chung cast se trong nhu 1 kenh).
# Thieu file → put_cast in "[!] thieu … bo qua" ⇒ khung ra KHONG nhan vat (khong crash).
MS.CAST = ROOT / "assets" / "cast"

# ⭐ CAN AVATAR (user 2026-08-21: *"anh avatar gan khung ti chu voi anh dang khong deu nhau
# cao thap to nho khac nhau"*). Ba so duoi thay cho MS.CAST_SCALE — tool goc can theo
# CHIEU CAO KHUNG, o day can theo CO DAU.
#
# 🔴 XUNG DOT HINH HOC, phai chon: anh gen crop khac nhau (dau chiem 34%..48% chieu cao,
# lech 1,41x) nen KHONG THE vua "dau bang nhau" vua "cao bang nhau". Chon DAU bang nhau vi
# do la thu mat nhin thay (make_stage cung ghi: "can theo CO DAU, khong theo chieu cao").
# Cach lam: scale cho dau = HEAD_PX → CAT bot phia duoi cho moi anh cao dung CAST_H →
# dan day tai SUB_Y0 ⇒ dau cung co, dinh dau cung do cao, chan cung mot moc. Deu tuyet doi.
# ⚖️ Danh doi: anh nao dai (thay tới dui) bi cat con tới bung — giong khuon mau (nhan vat
# "moc" len tu dai den), khong phai loi.
# 🔴 HEAD_PX ha 230 -> 200 (2026-08-21, sau khi gen lai kikite_surprised):
# tu the TAY MO NGANG rong 412px khi dau=230 => hoac de len the 148px, hoac bi kep be ngang
# va thanh DAU NHO HON cac anh khac — dung cai user vua phan nan ("to nho khac nhau").
# Kep be ngang va "dau deu" DANH NHAU, nen giai o goc: ha co dau CHUNG cho moi anh sao cho
# anh RONG NHAT vua tran 360px => dau van deu tuyet doi, khong anh nao bi kep rieng.
# Gia: cast nho hon ~13%. Doi lai deu, va de len the toi da ~96px.
HEAD_PX = 200        # be cao cua DAU, ap cho ca 12 cast
CAST_H = 416         # = 478 x 200/230 — be cao hien thi chung, cat bot phia duoi
CAST_GAP = 8         # khe tu mep TRONG cua avatar tới the — "gan khung" theo yeu cau
HEAD_W_OVER_H = 0.72  # dau nguoi: rong/cao
# 🔴 TRAN BE NGANG: tu the TAY MO NGANG (kikite_surprised ban gen lai) rong 412px khi ep
# dau 230 => de len the 148px (10,7% be ngang the), du de che noi dung anh. Kep lai: anh
# nao vuot thi thu nho theo BE NGANG (dau anh do nho hon vai %, doi lay khong che the).
# Dai ben chi 272px nen de nhe la khong tranh duoc; 360 => de toi da ~96px.
CAST_W_MAX = 360

# ⭐ POSE_MAP — DOI TU THE theo tung doan bai (user: *"it bieu cam the thoi a"*).
# 🔴 Co 12 anh cast ma dan MOT CAP co dinh cho ca 82 the thi cung nhu co 1 anh: bieu cam
# phai DI THEO NOI DUNG. Bang duoi doc theo dai index slide cua PLAN trong
# build_slides_18.py (cot "cau cue" trong slide_prompts_TENFILE.txt de doi chieu).
# Dinh nghia: (index_dau, minori, kikite) — ap cho moi slide >= index_dau.
POSE_MAP = [
    (0,  "minori_talk",  "kikite_worried"),    # cold open: 1万回 · 坂道 · so kham suc khoe
    (8,  "minori_hold",  "kikite_listen"),     # ITEM1 vo tao: gioi thieu "ao giap" thu nhat
    (12, "minori_point", "kikite_surprised"),  # so 2 lan chat xo (chu bake ×2)
    (13, "minori_stop",  "kikite_note"),       # cach rua / muoi / got — huong dan lam theo
    (19, "minori_smile", "kikite_listen"),     # persona みのり + ky uc me got tao
    (23, "minori_point", "kikite_surprised"),  # mot qua hay hai qua · 200g
    (25, "minori_stop",  "kikite_worried"),    # canh bao kali · benh than
    (30, "minori_hold",  "kikite_relieved"),   # an dung luong thi tao la ban
    (31, "minori_talk",  "kikite_listen"),     # case 道子さん Shizuoka
    (38, "minori_smile", "kikite_relieved"),   # 道子さん yen tam + checkpoint 「に」
    (42, "minori_point", "kikite_surprised"),  # AO GIAP THU HAI — payoff chinh
    (48, "minori_stop",  "kikite_worried"),    # an tao mot minh luc bung rong / truoc khi ngu
    (51, "minori_taste", "kikite_note"),       # みのり tu nem thu · juice · yaki-ringo
    (59, "minori_stop",  "kikite_worried"),    # dieu can tranh
    (61, "minori_hold",  "kikite_nod"),        # trung/com cung duoc — linh hoat
    (65, "minori_talk",  "kikite_relieved"),   # case bac tai xe Miyagi
    (73, "minori_smile", "kikite_nod"),        # recap hai ao giap
    (79, "minori_smile", "kikite_relieved"),   # ket + disclaimer
]


# ✅ DA GEN LAI 2026-08-21 — dict nay giờ RONG, giu lai lam so ghi + duong lui.
# Lich su: `kikite_worried` + `kikite_surprised` ban dau ta "one hand touching his own
# cheek" => model ve BAN TAY KHONG NOI vao ong tay ao (khuyu phong thanh khoi tron mo coi;
# surprised thi ban tay tach han). Do duoc bang mat o frame VIDEO, khong thay o anh slide.
# KHONG phai loi pipeline: 2 tu the NU cung co tay gan mat (minori_taste dua tao len mieng,
# minori_stop dua tay ra) lai ve DUNG => la loi cua rieng 2 anh gen do.
# Cach chua: bo hẳn dong tac "tay len ma", tay o THAP + cau ep "both arms clearly connected
# from shoulder to hand" (prompt o `cast_prompts_FIX.txt`).
# ⇒ Tu the nao gen loi lan sau: them vao day de video khong dung anh loi, roi gen lai.
BROKEN: dict[str, str] = {}


def pose_for(idx):
    """Cap tu the cho slide index — lay muc cuoi cung co index_dau <= idx."""
    left, right = POSE_MAP[0][1], POSE_MAP[0][2]
    for start, l, r in POSE_MAP:
        if idx >= start:
            left, right = l, r
    return BROKEN.get(left, left), BROKEN.get(right, right)


_CAST = {}


def cast_img(name):
    """Cast da CAN: dau = HEAD_PX, cao = CAST_H (cat bot phia duoi neu dai)."""
    if name in _CAST:
        return _CAST[name]
    p = MS.CAST / f"{name}.png"
    if not p.exists():
        _CAST[name] = None
        return None
    im = Image.open(p).convert("RGBA")
    al = np.asarray(im)[:, :, 3] > 60
    w = al.sum(axis=1)
    ys = np.flatnonzero(w > 0)
    y0, y1 = int(ys[0]), int(ys[-1])
    h = y1 - y0 + 1
    band = w[y0 + int(h * 0.06): y0 + int(h * 0.14)]      # dai chi co TOC
    head = float(np.median(band[band > 0])) / HEAD_W_OVER_H
    sc = HEAD_PX / max(head, 1)
    if im.width * sc > CAST_W_MAX:                 # tran be ngang thang tran dau
        sc = CAST_W_MAX / im.width
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))),
                   Image.LANCZOS)
    top = int(y0 * sc)
    im = im.crop((0, top, im.width, min(im.height, top + CAST_H)))   # cat phia duoi
    _CAST[name] = im
    return im


def put_cast_flush(base, name, side):
    """Dan cast SAT THE, nhung KHONG BAO GIO de mep khung cat mat tay.

    🔴 Ca user bat (screenshot 2026-08-21): *"nhan vat bi mat tay nay"* — みのり mat han
    ban tay dua len. Nguyen nhan do duoc: avatar rong 204..335px trong khi dai ben chi
    272px, nen dat "mep trong cach the 8px" lam mep NGOAI ra khoi khung (x=-28) va bi cat.
    ⇒ Kep x vao trong khung (x>=0 / x+w<=W). He qua: avatar rong hon 264px se DE nhe len
    mep the — chap nhan duoc (avatar dung TRUOC san khau, va mep the la vung anh cover
    thuong trong), con mat tay thi khong.
    """
    ch = cast_img(name)
    if ch is None:
        return
    if side == "left":
        x = max(0, MS.CARD_X0 - CAST_GAP - ch.width)
    else:
        x = min(MS.W - ch.width, MS.CARD_X1 + CAST_GAP)
    base.alpha_composite(ch, dest=(int(x), MS.SUB_Y0 - ch.height))

# 🔴 VIEN KHUNG cua anh gen (do bang may 2026-08-21, 82/82 anh deu co):
# generator ve mot duong vien manh 1-3px TOI HON nen o mep trai/phai (slide_79 cot 0-2 =
# 215/212/244 vs nen 253; slide_80 = 227/225/240). Nen anh la TRANG, canvas cung TRANG,
# nen rieng cai vien do bien thanh mot CAI KHUNG bao quanh anh — va vi anh gen co dai
# trang o day (prompt xin "clean empty white band along the bottom edge") nen vien chay
# xuong bao luon vung phu de => dung cai "khung bao text" user chi ra.
# Cat cung 5px moi mep: vien day nhat do duoc la 3px, 5px du an toan va chi mat 0,36%
# be ngang. KHONG dung auto-detect vi anh co noi dung cham mep (slide_81 hang 0 = 97%
# pixel khong trang) se bi an nham vao noi dung.
BORDER = 5

STOP = {"a", "an", "the", "of", "on", "in", "at", "and", "with", "to", "from", "by",
        "one", "two", "three", "its", "their", "for", "into", "over", "under",
        "beside", "next", "up", "down", "small", "large", "red", "white", "soft"}


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


def trim_border(im, px=BORDER):
    """Cat vien khung manh cua anh gen (xem chu thich BORDER) + DAI TRANG DAY + duong ke.

    🔴 Phan dai trang day (2026-08-21 vong 2): prompt xin "a clean empty white band left
    along the bottom edge" va generator thi hanh bang cach ve mot DUONG KE NGANG manh roi
    de trang duoi no. Duong ke do — chay suot be ngang, ngay tren vung phu de — chinh la
    "khung bao text" user chi ra; no la NOI DUNG cua anh nen trim vien khong cham tới.
    Canvas da tu chua 190px trang cho phu de roi, nen dai trang trong anh la du thua:
    cat no + cat luon duong ke => anh con lai TO HON ~20% (fit theo chieu cao) va mep day
    hoa vao canvas trang.
    """
    if im.width <= 2 * px or im.height <= 2 * px:
        return im
    im = im.crop((px, px, im.width - px, im.height - px))

    g = np.asarray(im.convert("L")).astype(int)
    ink = (g < 245).mean(axis=1)          # ty le pixel co "muc" tung hang
    rows = np.flatnonzero(ink >= 0.01)
    if rows.size == 0:
        return im
    b = int(rows[-1])                      # hang co noi dung thap nhat
    if im.height - 1 - b < 20:
        return im                          # noi dung cham day thuc su -> khong cat gi
    # Duong ke doc lap = khoi noi dung MONG (<=6px) ma ngay TREN no la trang -> cat bo ca
    # khoi do. ⚠️ Nhan dien bang DO DAY, khong bang do phu ngang: ban dau ham nay doi
    # "hang khong phu kin be ngang" (ink < 0.98) va the la truot het, vi duong ke chinh la
    # hang PHU KIN (slide_55 con nguyen duong ke sau vong sua dau).
    top = b
    while top > 0 and ink[top - 1] >= 0.01:
        top -= 1
    if b - top <= 6 and (top == 0 or ink[top - 1] < 0.01):
        b = top - 1
    return im.crop((0, 0, im.width, max(b + 1, 1)))


def edge_step(im):
    """Do BAC NHAY do sang tai 4 mep — con vien hay khong.

    🔴 Do BAC, khong do DO TOI. Ban dau ham nay do "mep toi hon ben trong bao nhieu" va
    no bao oan 2 anh (slide_19 tu bep phia tren, slide_28) vi noi dung cham mep cung lam
    mep toi: profile 184→185→188→193→196 la GRADIENT muot cua noi dung.
    Vien thi khac han — no la mot duong 1-3px roi NHAY ve nen:
    slide_79 goc, mep trai: 215→212→244→253→253  (bac +32 o buoc thu hai).
    => tra ve bac nhay lon nhat trong 5px dau cua mep. > ~12 = con vien.

    ⚠️ CHI do 3 mep TRAI/PHAI/TREN. Mep DAY bi loai co y: trim_border cat dai trang day
    sat noi dung, nen o day "bac nhay" la KET QUA MONG DOI chu khong phai vien (do ca 4
    mep thi gate bao oan 7+ anh, dung loai loi cua chinh ban dau ham nay).
    """
    a = np.asarray(im.convert("L")).astype(float)
    profs = ([a[:, i].mean() for i in range(6)], [a[:, -1 - i].mean() for i in range(6)],
             [a[i, :].mean() for i in range(6)])
    return max(p[i + 1] - p[i] for p in profs for i in range(4))


# ⭐ LOP CHU + STICKER (user 2026-08-21: *"them text hoac hieu ung stiker gi di chu nhin
# cac frame no bi te nhat qua"*). Ve bang font Noto cua make_stage ⇒ chu Nhat KHONG nat
# (khac han chu bake bang AI). Moi doan mot CHIP nhan + mot dau nhan.
#   (index_dau, nhan chip, kieu dau: "warn"|"ok"|"num"|None)
CHIP_MAP = [
    (0,  "その一口の坂道",     "warn"),
    (8,  "① 皮という鎧",       "num"),
    (13, "皮ごと食べるコツ",   "ok"),
    (19, "案内人・みのり",     None),
    (23, "一日に何個まで？",   "num"),
    (25, "腎臓の治療中の方へ", "warn"),
    (31, "静岡・道子さんの話", None),
    (42, "② 仲間という鎧",     "num"),
    (48, "りんごを一人にしない", "warn"),
    (51, "私も試してみました", "ok"),
    (59, "避けたい食べ方",     "warn"),
    (61, "ヨーグルトが無い日は", "ok"),
    (65, "宮城・元運転手さんの話", None),
    (73, "まとめ・二つの鎧",   "ok"),
    (79, "今夜の食卓から",     None),
]
CHIP_BG = (58, 74, 104)          # navy dam — an voi nen xam nhat cua san khau
CHIP_FG = (255, 255, 255)
MARK = {"warn": ("！", (226, 92, 60)), "ok": ("✓", (76, 152, 106)),
        "num": ("＋", (206, 148, 46))}

_MASK = None


def card_mask():
    """Mat na bo goc cua the — dung chung ban kinh 28 voi make_stage."""
    global _MASK
    if _MASK is None:
        _MASK = Image.new("L", (CW, CH), 0)
        ImageDraw.Draw(_MASK).rounded_rectangle([0, 0, CW - 1, CH - 1], 28, fill=255)
    return _MASK


def cover_loss(im):
    """Cover-crop lam MAT bao nhieu phan noi dung? = muc trong dai bi cat / TONG muc.

    🔴 Ban dau ham nay tra ve "ty le pixel co muc TRONG DAI bi cat" — sai NGHIA: voi anh
    co nen phu ngang (doi cat) thi dai nao cung day muc nen no bao 49,5% trong khi thuc
    te chi mat mep nen, chu bake van nguyen. Do dung phai la ty le so voi TONG muc.
    """
    sc = max(CW / im.width, CH / im.height)
    cut = int(max(0, (int(im.width * sc) - CW) / 2 / sc))
    if cut < 1:
        return 0.0
    ink = np.asarray(im.convert("L")).astype(int) < 245
    tot = ink.sum()
    if not tot:
        return 0.0
    return float((ink[:, :cut].sum() + ink[:, im.width - cut:].sum()) / tot)


LOSS_MAX = 0.12
"""Tran mat noi dung cua cover-crop; qua nguong thi TU LUI ve fit (contain).

🔴 Vi sao phai co duong lui: user chot cover cho het duong mep, nhung anh co bo cuc SO
SANH HAI BEN thi cover cat mat mot ben. Dinh thuc te: `slide_23` (mot dia 1 qua vs mot
dia 2 qua — dung cau 「一日に何個までが目安なのか」) bi cat mat dia PHAI => hinh noi
nguoc noi dung. Anh fit thi phan thua la TRANG trung mau the nen van khong thay mep.
"""


def chip_for(idx):
    """(nhan chip, kieu dau) cho slide index."""
    cur = CHIP_MAP[0]
    for row in CHIP_MAP:
        if idx >= row[0]:
            cur = row
    return cur[1], cur[2]


def draw_chip(base, idx):
    """CHIP nhan doan + DAU NHAN, ca hai o goc TREN-TRAI the.

    🔴 Dau nhan phai nam CANH CHIP, khong phai goc tren-PHAI: watermark 「60代の食卓」 cua
    renderer dan o goc tren-phai KHUNG (328x133px) va de trum len day — do duoc o frame
    q_40/q_330 (mot cuc cam loi ra ben trai badge vang). Renderer dan watermark SAU khi
    ghep slide nen tang nay khong the "tranh" bang cach ve truoc.
    Chu ve bang font Noto (khong phai AI gen) nen luon sac net.
    """
    label, mark = chip_for(idx)
    d = ImageDraw.Draw(base)
    f = MS.fit(label, "bold", 470, 40, 26)
    tb = d.textbbox((0, 0), label, font=f)
    tw_, th_ = tb[2] - tb[0], tb[3] - tb[1]
    px, py = 22, 13
    x0, y0 = MS.CARD_X0 + 26, MS.CARD_Y0 + 24
    x1, y1 = x0 + tw_ + px * 2, y0 + th_ + py * 2
    d.rounded_rectangle([x0, y0, x1, y1], (th_ + py * 2) // 2, fill=CHIP_BG)
    d.text((x0 + px - tb[0], y0 + py - tb[1]), label, font=f, fill=CHIP_FG)
    if mark:
        ch, col = MARK[mark]
        r = (y1 - y0) // 2
        cx, cy = x1 + 18 + r, (y0 + y1) // 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        d.text((cx, cy + 1), ch, font=MS.F("black", int(r * 1.15)),
               fill=(255, 255, 255), anchor="mm")


def stage_canvas(im, idx=0):
    """Minh hoa -> KHUNG SAN KHAU 1920x1080 (nen + the bo goc + cast + dai den)."""
    art = trim_border(im.convert("RGB"))
    if cover_loss(art) <= LOSS_MAX:                        # cover: phu tron the
        sc = max(CW / art.width, CH / art.height)
        art = art.resize((max(1, int(art.width * sc)), max(1, int(art.height * sc))),
                         Image.LANCZOS)
        art = art.crop(((art.width - CW) // 2, (art.height - CH) // 2,
                        (art.width - CW) // 2 + CW, (art.height - CH) // 2 + CH))
        lay = art
    else:                                                  # fit: khong cat gi
        art.thumbnail((CW, CH), Image.LANCZOS)
        lay = Image.new("RGB", (CW, CH), MS.CARDC)
        lay.paste(art, ((CW - art.width) // 2, (CH - art.height) // 2))

    base = MS.stage_base()                       # nen gradient + the trang + bong do
    base.paste(lay, (MS.CARD_X0, MS.CARD_Y0), card_mask())
    draw_chip(base, idx)                         # chip nhan doan + dau nhan
    left, right = pose_for(idx)
    put_cast_flush(base, left, "left")           # cast da CAN + SAT the
    put_cast_flush(base, right, "right")
    MS.sub_bar(base)                             # dai den day cho phu de
    return base.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", action="store_true")
    ap.add_argument("--cut-x", type=int, default=None,
                    help="cat mep phai tai x nay de bo ✦ (soi MAT theo LO roi truyen)")
    ap.add_argument("--no-cut", action="store_true",
                    help="lo da soi mat KHONG co ✦ — bo qua buoc cat")
    ap.add_argument("--slots", help="chi nhap slot chi dinh, vd slide_10.jpg,slide_64.jpg")
    ap.add_argument("--from-orig", action="store_true",
                    help="dung lai tu backup _wm_orig/ (ten DA la slide_XX) — dung khi "
                         "folder Downloads da bi don, hoac khi chi doi khung/cast")
    a = ap.parse_args()

    if a.restore:
        n = 0
        for f in sorted(ORIG.glob("*")):
            shutil.copy2(f, IMG / f.name)
            n += 1
        print(f"restore {n} anh tu _wm_orig/")
        return 0
    if not a.src and not a.from_orig:
        print("thieu folder nguon (hoac dung --from-orig de dung lai tu _wm_orig)")
        return 1
    if a.cut_x is None and not a.no_cut:
        print("🔴 THIEU --cut-x: soi MAT goc duoi-phai 5-8 anh cua LO nay roi truyen "
              "--cut-x <mep trai ✦ - 15>, hoac --no-cut neu lo sach.\n"
              "   (toa do ✦ doi theo LO — media-library.md §2.10 ⑤, cam be so lo cu)")
        return 1

    flow = (VD / "slide_prompts_FLOW.txt").read_text(encoding="utf-8").splitlines()
    tenfile = (VD / "slide_prompts_TENFILE.txt").read_text(encoding="utf-8").splitlines()[1:]
    slots = []
    for line, tf in zip(flow, tenfile):
        m = re.search(r"SUBJECT: (.*?)\. (?:TEXT|STYLE)", line)
        parts = tf.split("\t")
        slots.append({"name": parts[0], "subj": m.group(1) if m else "",
                      "moc": parts[1], "text": parts[2].strip()})
    if a.slots:
        keep = {s.strip() for s in a.slots.split(",")}
        slots = [s for s in slots if s["name"] in keep]
        if len(slots) != len(keep):
            print(f"⚠️ chi tim thay {len(slots)}/{len(keep)} slot chi dinh")

    if a.from_orig:
        # Dung lai tu backup: ten trong _wm_orig DA la slide_XX ⇒ khop truc tiep, khong
        # can ghep token. Dung khi folder Downloads da bi don, hoac khi chi doi KHUNG/CAST
        # ma khong doi anh (khoi phai bat user tai lai lo 82 anh).
        plan = []
        for s in slots:
            stem = Path(s["name"]).stem
            hit = next((p for p in sorted(ORIG.glob(stem + ".*"))), None)
            plan.append((s, hit, 1.0))
        print(f"nguon: _wm_orig ({sum(1 for _s, p, _x in plan if p)} anh) | "
              f"slot can: {len(slots)}\n")
    else:
        srcs = sorted(Path(a.src).glob("*.jpe*g")) + sorted(Path(a.src).glob("*.png"))
        print(f"nguon: {len(srcs)} anh | slot can: {len(slots)}\n")

        # ghep ten file generator (dat theo tom tat SUBJECT) ↔ slot bang token overlap
        src_toks = [(p, toks(p.stem)) for p in srcs]
        used, plan = set(), []
        for s in slots:
            st = toks(s["subj"])
            best, bs = None, 0.0
            for p, pt in src_toks:
                if p in used or not pt:
                    continue
                sc = len(st & pt) / max(1, len(pt))
                if sc > bs:
                    best, bs = p, sc
            if best is not None and bs >= 0.25:
                used.add(best)
                plan.append((s, best, bs))
            else:
                plan.append((s, None, 0.0))

    miss = [s["name"] for s, p, _ in plan if p is None]
    for s, p, sc in plan:
        print(f"{s['name']}  {s['moc']}  {'← ' + p.name[:58] + f' ({sc:.2f})' if p else '🔴 CHUA CO ANH'}")
    if miss:
        print(f"\n🔴 {len(miss)} slot chua co anh: {', '.join(miss[:10])}"
              + (" …" if len(miss) > 10 else ""))
    if not a.apply:
        print("\n(xem thu — them --apply de ghi that; SOI BANG MAT bang ghep tren truoc)")
        return 0

    IMG.mkdir(parents=True, exist_ok=True)
    ORIG.mkdir(parents=True, exist_ok=True)
    n, framed, bands, losses = 0, [], [], []
    for s, p, _ in plan:
        if p is None:
            continue
        im = Image.open(p)
        if not a.from_orig:            # ⚠️ from_orig: nguon CHINH LA file trong ORIG →
            shutil.copy2(p, ORIG / (Path(s["name"]).stem + p.suffix))   # copy de len chinh
        # no = PermissionError (WinError 32, file dang mo). Khong can backup lai.
        if not a.no_cut:
            if im.width <= a.cut_x:
                print(f"⚠️ {s['name']}: anh rong {im.width} <= cut_x {a.cut_x}, bo qua cat")
            else:
                im = im.crop((0, 0, a.cut_x, im.height))
        cut = trim_border(im.convert("RGB"))
        d = edge_step(cut)
        if d > 12:
            framed.append((s["name"], d))
        bands.append(im.height - 2 * BORDER - cut.height)   # dai trang day da cat
        loss = cover_loss(cut)
        # Anh CO CHU BAKE: luon liet ke de soi 1:1 (chu la cho tuyet doi khong duoc cat).
        # Anh vuot LOSS_MAX: tool tu lui ve fit, ghi ra de biet anh nao khong duoc phu tron.
        if s["text"] != "-" or loss > LOSS_MAX:
            losses.append((s["name"], loss, s["text"]))
        idx = int(re.search(r"(\d+)", s["name"]).group(1))
        stage_canvas(im, idx).save(IMG / s["name"], quality=95)
        n += 1
    print(f"\nghi {n} anh -> {IMG.relative_to(ROOT)} "
          f"(KHUNG SAN KHAU: the {CW}x{CH}@({MS.CARD_X0},{MS.CARD_Y0}) cover-crop, "
          f"dai den tu y={MS.SUB_Y0})")
    need = sorted({c for _s, l, r in POSE_MAP for c in (l, r)})
    miss = [c for c in need if not (MS.CAST / f"{c}.png").exists()]
    if miss:
        print(f"⚠️ CHUA CO CAST {len(miss)}/{len(need)} — khung ra KHONG nhan vat: "
              f"{', '.join(miss)}")
        print(f"   Gen 12 anh theo {VD.name}/cast_prompts_FLOW.txt → "
              f"cutout_cast.py --apply → chay lai lenh nay.")
    else:
        hs = [cast_img(c) for c in need]
        ws = [i.width for i in hs if i]
        print(f"✅ CAST {len(need)}/{len(need)} · dau ep {HEAD_PX}px, cao {CAST_H}px "
              f"(deu nhau) · rong {min(ws)}-{max(ws)}px · sat the {CAST_GAP}px")
        print(f"   doi tu the {len(POSE_MAP)} lan · chip nhan {len(CHIP_MAP)} doan")
        if BROKEN:
            print(f"⚠️ {len(BROKEN)} cast dang bi THAY TAM (anh gen ve sai tay): "
                  + ", ".join(f"{k}→{v}" for k, v in BROKEN.items()))
            print(f"   Gen lai 2 dong trong {VD.name}/cast_prompts_FIX.txt → "
                  f"cutout_cast.py --apply → XOA dict BROKEN trong tool nay.")
    if losses:
        fits = [r for r in losses if r[1] > LOSS_MAX]
        print(f"ⓘ cover-crop: {n - len(fits)}/{n} anh phu TRON the · {len(fits)} anh tu lui "
              f"ve FIT (mat >{LOSS_MAX*100:.0f}% noi dung — vd bo cuc so sanh 2 ben):")
        for name, lo, txt in sorted(losses, key=lambda r: -r[1])[:12]:
            mode = "FIT " if lo > LOSS_MAX else "cover"
            print(f"      {mode} {name}  mat {lo*100:4.1f}%"
                  + (f"   ← CHU BAKE {txt}" if txt != "-" else ""))
    print(f"    trim vien {BORDER}px moi mep (anh gen co vien khung 1-3px — lo thanh KHUNG "
          f"tren canvas trang)")
    cut_n = sum(1 for b in bands if b > 0)
    if cut_n:
        nz = sorted(b for b in bands if b > 0)
        print(f"    cat dai trang day + duong ke o {cut_n}/{n} anh "
              f"(min {nz[0]}px / trung vi {nz[len(nz)//2]}px / max {nz[-1]}px)")
    # GATE VIEN: luat kiem bang mat thi se troi — ca 82 anh vong 1 da qua mat va lot.
    if framed:
        print(f"🔴 {len(framed)} anh CON BAC NHAY o mep (vien chua cat het) — nang BORDER:")
        for name, d in framed[:10]:
            print(f"      {name}  bac {d:+.1f}")
    else:
        print("✅ GATE VIEN: 0/82 anh con bac nhay o mep — khong con khung bao")
    print("⚠️ NGHIEM THU: soi 1:1 CA 4 GOC vai anh (✦ sot?) + soi TUNG KY TU 6 anh co chu"
          " (1万回 ×2 200g 2 3) — sai net la gen lai, khong sua tay.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
