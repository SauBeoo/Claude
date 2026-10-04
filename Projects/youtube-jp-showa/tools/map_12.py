# -*- coding: utf-8 -*-
"""BANG GHEP slot -> clip cho video 12, dung bang MAT tren _sheet/sheet_1..9.jpg.

Khoa = so slot trong SLIDES (0..164). Gia tri = so #NNN tren contact sheet.
⛔ #010 (clip rac) va #158 (co DIEU HOA gan tuong) da bi loai, khong duoc dung.

Cach doc do tin cay:
  - Boi canh DAC TRUNG (gieng, xe da, vat nuoc, may lanh khong co, man, vo nuoc truong,
    yoshizu, phao bong) -> ghep CHAC, vi frame khac nhau ro.
  - Boi canh LAP (di bo trong ngo, ngoi hien) -> cac clip gan NHU Y HET nhau, ghep nham
    giua chung khong mat gi.
"""

# ---- ido (gieng) — 9/9 chac -------------------------------------------------
IDO = {3: 122, 40: 162, 41: 96, 44: 121, 45: 109, 46: 107, 49: 95, 63: 123, 152: 100}

# ---- daidokoro (bep / tu da) — 9/9 -----------------------------------------
DAIDOKORO = {42: 124, 43: 166, 50: 125, 51: 126, 52: 115, 53: 164, 60: 128, 61: 119, 62: 165}

# ---- koriya (xe da) — 6/6 chac tuyet doi ------------------------------------
KORIYA = {54: 48, 55: 81, 56: 65, 57: 33, 58: 3, 59: 15}

# ---- mizunomi (vo nuoc truong) — 8/9, THIEU slot 78 ------------------------
MIZUNOMI = {72: 42, 77: 41, 86: 75, 87: 71, 88: 80, 89: 61, 90: 34, 149: 60}

# ---- undoujou (san truong) — 16/18, THIEU slot 81 va 84 --------------------
UNDOUJOU = {67: 59, 68: 47, 69: 23, 70: 9, 71: 78, 73: 64, 74: 2, 75: 0, 76: 46,
            79: 50, 80: 24, 82: 77, 83: 1, 85: 37, 91: 8, 92: 32}

# ---- nokishita (yoshizu / mai hien) — 9/9, muon 6 clip tu nhom hien --------
NOKISHITA = {107: 62, 108: 72, 109: 44, 110: 6, 111: 5, 121: 69, 122: 52, 123: 54, 151: 45}

# ---- zashiki (man ngu) — 18/18 ---------------------------------------------
ZASHIKI = {1: 19, 2: 153, 12: 106, 13: 133, 14: 22, 15: 36, 16: 13, 17: 14, 18: 18,
           19: 145, 20: 20, 21: 118, 22: 35, 27: 129, 28: 163, 29: 91, 39: 149, 137: 56}
ZASHIKI_ASA = {158: 104}

# ---- genkansaki (uot nuoc truoc cua) — 11/11 -------------------------------
GENKANSAKI = {100: 88, 101: 112, 102: 140, 103: 93, 104: 146, 105: 147, 106: 86,
              112: 152, 113: 131, 114: 151, 150: 141}

# ---- niwa_yoru (vuon dem) — 7/7 --------------------------------------------
NIWA_YORU = {124: 161, 127: 101, 128: 132, 129: 116, 130: 87, 131: 167, 136: 169}

# ---- machi_yoru (ngo dem) — 12/12 ------------------------------------------
MACHI_YORU = {125: 89, 126: 111, 132: 67, 133: 68, 134: 16, 135: 17, 138: 135,
              145: 90, 146: 102, 147: 82, 153: 136, 154: 110}

# ---- michi_natsu (ngo ban ngay) — 15/16, THIEU slot 118 --------------------
MICHI_NATSU = {4: 154, 9: 155, 10: 103, 30: 156, 31: 113, 32: 157, 33: 85, 34: 26,
               66: 28, 99: 31, 115: 159, 116: 120, 117: 160, 119: 11, 120: 30}

MAP = {}
for d in (IDO, DAIDOKORO, KORIYA, MIZUNOMI, UNDOUJOU, NOKISHITA,
          ZASHIKI, ZASHIKI_ASA, GENKANSAKI, NIWA_YORU, MACHI_YORU, MICHI_NATSU):
    MAP.update(d)

# Slot chua co clip nao khop — CAN GEN THEM, khong duoc lay clip khac dung 2 lan
# (memory feedback_slide_khong_trung_anh_trong_video).
THIEU = {
    78:  "C13 mizunomi — seito cham lai ngang voi voi cuoi cung roi di tiep, khong dung",
    81:  "C16 undoujou — seito gio hai tay ngang truoc mat roi ha xuong",
    84:  "C19 undoujou — sensei gio mot tay len cao qua dau va giu",
    118: "E20 michi_natsu — tonari gio quat che mat, di xa khoi camera xuong cuoi ngo "
         "(clip #158 dinh DIEU HOA nen bi loai)",
}

BAD = {10, 158}

# ---- engawa (hien / phong tatami) — 36/40, THIEU 4 slot cuoi khoi END -------
# Nhom nay cac clip gan nhu thay the duoc cho nhau (dan ong / dan ba ngoi hien),
# nen ghep nham trong noi bo nhom KHONG mat gi. Cac nhip DAC TRUNG (cat dua hau,
# nho hat, rot tra, bat/tat TV, chuong gio) thi ghep chac vi frame khac han.
ENGAWA = {
  0: 148,   5: 53,    6: 51,    7: 21,    8: 57,
 11: 138,  23: 79,   24: 70,   25: 58,   26: 49,
 35: 94,   36: 114,  37: 40,   38: 4,
 47: 98,   48: 134,  64: 12,   65: 7,
 93: 92,   94: 130,  95: 127,  96: 84,   97: 55,   98: 66,
139: 63,  140: 73,  141: 38,  142: 137, 143: 74,  144: 76,
148: 105, 155: 39,  156: 43,  159: 143, 160: 144, 161: 99,
}
MAP.update(ENGAWA)

THIEU.update({
 157: "G11 engawa — ko dung day khoi mep hien roi di xa camera vao phong tatami trong",
 162: "G16 engawa — haha dung day, di cham ra xa camera doc hien, dung o cot goc",
 163: "G17 engawa — haha dung o cot goc, mot tay tren cot, quay dau nhin lai hien trong",
 164: "G18 engawa — haha roi tay khoi cot, buoc xuong vuon, di xa dan  <-- CANH CUOI VIDEO",
})
