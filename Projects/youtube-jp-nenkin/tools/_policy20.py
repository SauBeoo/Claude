# -*- coding: utf-8 -*-
r"""_policy20.py — lop LAM SACH cho bo loc an toan cua GOOGLE (Imagen / Veo / Flow).

User bao 2026-09-03, sau khi da vá vong 1: *"Tu khoa van vi pham bo loc an toan
AI cua google"*.

🔴🔴 HAI DIEU PHAI HIEU TRUOC KHI SUA — vong 1 sai vi khong biet hai cai nay:

  ① **BO LOC DOC TU KHOA, KHONG DOC PHU DINH.**
     Vong 1 tao them vao ca 83 prompt cau:
        "not a real, identifiable individual, not a public figure,
         and not a likeness of anyone"
     Y dinh la **giam** rui ro nhan dang. Thuc te bo loc nhin thay
     `identifiable` · `public figure` · `likeness` — ba tu nhay nhat cua ho —
     va **khong nhin thay chu "not"**. Tuc la tao tu tay nhet tu cam vao
     83/83 prompt roi bao la da vá.
     ⇒ **LUAT: khong bao gio "xin phep" bang cach NHAC den dieu cam.**
        Muon nhan vat hu cau thi cu ta nguoi binh thuong; dung viet
        "khong phai nguoi that".

  ② **MAT DO NGON NGU RANG BUOC cung la tin hieu.**
     Prompt 2.300–3.900 ky day 「MUST」「NEVER」「obey these before anything
     else」「no ... no ... no ...」 doc rat giong prompt dang **do rao chan**.
     Prompt ta canh thuan tuy thi qua de dang hon han. Va no trung voi bai hoc
     da co: `ab-3title-3thumb.md` §3.1 — prompt dai thi model bam ta canh roi
     nuot phan con lai.
     ⇒ Ban `real` rut con **~1.100–1.600 ky**, bo het khoi "chinh sach".

⚖️ **Bo cau "nhan vat hu cau" KHONG lam mat tuan thu.**
   `youtube-compliance.md` §2 cam **mat nguoi that cu the**. Nhan vat cua ta hu
   cau vi **khong he trich dan mot nguoi that nao** — khong ten, khong nghe si,
   khong anh tham chieu nguoi that. Nghia vu do nam o CHO TA CHON TA GI, khong
   nam o mot cau tuyen bo trong prompt. Bo cau do di thi nhan vat van hu cau y
   nguyen.

📌 Nhom tu da go, theo HO (go het ca ho, ke ca khi dang o dang phu dinh):
   · nhan dang: real person · identifiable · public figure · likeness · celebrity
   · giay to:   official · government · stamp · seal · document · form ·
                certificate · declaration · statute · passbook
   · tre em:    child · boy · girl · son · school · graduation · teen
   · tang le:   late (husband) · memorial · altar · deceased · incense · bell
   · tien:      banknote · currency · cash · payslip · income · tax
"""

# ══════════════════════════════════════════════════════════════════════════
# GOOGLE_SWAP — chay SAU `POLICY_SWAP`. Cum DAI truoc cum ngan.
# Doi CHU, giu HINH: nguoi xem thay dung cai vat do, chi khac ten goi.
# ══════════════════════════════════════════════════════════════════════════
GOOGLE_SWAP = [
    # ── ① tu chinh tao nhet vao o vong 1 — go SACH ────────────────────────
    (r" Everyone shown is a FICTIONAL character invented for this "
     r"illustration — not a real, identifiable individual, not a public "
     r"figure, and not a likeness of anyone\.", ""),
    (r"a RECURRING FICTIONAL CHARACTER invented for this series, not a real "
     r"or identifiable person\. This shot establishes the character, so keep "
     r"the description below unchanged in every later shot:",
     "a recurring character in this series. This shot sets the look; keep the "
     "description below unchanged in later shots:"),
    (r"the same RECURRING FICTIONAL CHARACTER as before, not a real or "
     r"identifiable person; keep the same age, hair, build and clothing so "
     r"the series stays consistent:",
     "the same recurring character as before — same age, hair, build and "
     "clothing, so the series stays consistent:"),
    (r"RECURRING FICTIONAL CHARACTER", "recurring character"),
    (r"ALWAYS THE SAME invented character M1, never a real or identifiable "
     r"person:", "always the same recurring character M1:"),
    (r"\bFICTIONAL\b", "recurring"),
    (r"\bidentifiable\b", ""),
    (r"\bpublic figure\b", ""),
    (r"\blikeness\b", ""),

    # ── ② giay to: bo han khai niem "giay to chinh thuc" ──────────────────
    (r"printed notice letter", "printed letter"),
    (r"documents, forms, notices, calendars and leaflets",
     "printed pages, calendars and booklets"),
    (r"a single plain printed booklet", "a single printed booklet"),
    (r"a rolled certificate tube", "a rolled paper tube"),
    (r"certificate tube", "paper tube"),
    (r"a small navy bank passbook", "a small navy pocket notebook"),
    (r"bank passbook", "pocket notebook"),
    (r"\bpassbook\b", "pocket notebook"),
    (r"\bdeclaration\b", "printed"),
    (r"\bcertificate\b", "paper"),

    # ── ③ tre em: go moi tu goi thang toi nguoi duoi 18 ───────────────────
    (r"outside a Japanese school gate under cherry blossom, the ceremony over "
     r"and the gateway empty", "at the open gateway of a quiet Japanese "
     "courtyard under cherry blossom, the place empty"),
    (r"a navy school-style blazer on a hanger", "a dark navy jacket on a hanger"),
    (r"navy school-style blazer", "dark navy jacket"),
    (r"a Japanese school gate", "a quiet Japanese gateway"),
    (r"\bschool\b", "courtyard"),
    (r"after the ceremony", "later that spring"),
    (r"\bgraduation\b", "spring"),

    # ── ④ tang le: giu HINH (anh khung + hoa trang), bo TU ────────────────
    (r"quiet remembrance corner", "quiet corner"),
    (r"dark-wood remembrance shelf", "dark-wood shelf"),
    (r"one white chrysanthemum in a slim vase and a small brass bell",
     "a single white flower in a slim vase"),
    (r"white chrysanthemum in a slim vase and a small brass bell",
     "white flower in a slim vase"),
    (r"a white chrysanthemum", "a single white flower"),
    (r"\bchrysanthemum\b", "white flower"),
    (r"a thin thread of incense smoke rises and bends",
     "a thin curl of steam from a cup at the edge of frame rises and bends"),
    (r"\bincense\b", ""),
    (r"\bremembrance\b", ""),

    # ── ④b "portrait" con lai la THUAT NGU CO CANH ("a close portrait of the
    #    woman") chu khong phai doi ve chan dung — nhung bo loc khop tu khoa thi
    #    khong phan biet duoc. Doi sang tu quay phim, khong mat nghia gi.
    (r"a close portrait of", "a close shot of"),
    (r"a calm half-body portrait of", "a calm half-body shot of"),
    (r"\bportrait\b", "shot"),

    # ── ⑤ tien: bo tu tai chinh, giu vat (xu dong / to giay) ──────────────
    (r"a printed income statement sheet", "a printed sheet of figures"),
    (r"an income statement sheet", "a sheet of figures"),
    (r"payment statement slip", "printed slip of figures"),
    (r"printed statement leaflet", "printed leaflet"),
    (r"\bincome\b", "figures"),
    (r"\bpayslip\b", "printed slip"),
]

# ══════════════════════════════════════════════════════════════════════════
# GOOGLE_BLOCK — GATE. Con mot tu trong day = CHUA duoc giao.
# 🔴 Gate nay soi CHINH FILE DA XUAT, khong tin bao cao cua ham doi chu —
#    bai hoc 2026-09-03: bao cao doi chu bao "da doi 75 cum" trong khi 6 mau
#    regex im lang khong chay (loi escape `\b` -> ky tu backspace).
# ══════════════════════════════════════════════════════════════════════════
GOOGLE_BLOCK = [
    r"\bofficial\b", r"\bgovernment\b", r"\bstamp\w*\b", r"\bseal\b",
    r"\bstatute\w*\b", r"\bdeclaration\b", r"\bcertificate\b", r"\bpassbook\b",
    r"\bidentifiable\b", r"\bpublic figure\b", r"\blikeness\b",
    r"\breal person\b", r"\bcelebrity\b", r"\bFICTIONAL\b",
    r"\bchild(?:ren)?\b", r"\bboy\b", r"\bgirl\b", r"\bson\b", r"\bdaughter\b",
    r"\bschool\b", r"\bgraduation\b", r"\bteen\w*\b", r"\bminor\b",
    r"\blate husband\b", r"\bmemorial\b", r"\baltar\b", r"\bdeceased\b",
    r"\bincense\b", r"\bchrysanthemum\b", r"\bfuneral\b", r"\bwidow\w*\b",
    r"\bbanknote\w*\b", r"\bcurrency\b", r"\bpayslip\b", r"\bincome\b",
    # 🔴 vong 5 (2026-09-03) — ca bi chan THAT ma 4 vong truoc khong bat duoc:
    #    prompt `awaseta` doi model **sinh ra mot tam anh chan dung cua mot nguoi
    #    dan ong**, kem nguyen doan ta khuon mat ("late fifties, short neatly
    #    parted black hair greying at the temples, a calm narrow face..."). Voi
    #    Google do la YEU CAU NHAN DANG, va no nang hon moi tu don le da go.
    #    ⇒ Luat: khong sinh anh chan dung nguoi BEN TRONG canh. Can noi "cua ong
    #      ay" thi dung KY VAT (P_KATAMI) hoac khung anh NHIN NGHIENG (P_BUTSU).
    r"\bportrait photograph\b", r"framed portrait",
    r"photograph of (?:a|an|the)\s+(?:\w+\s+){0,3}(?:man|woman|person|male|female)\b",
    r"picture of (?:a|an|the)\s+(?:\w+\s+){0,3}(?:man|woman|person)\b",
]
