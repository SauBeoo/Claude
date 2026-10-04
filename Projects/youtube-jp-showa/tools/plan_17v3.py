# -*- coding: utf-8 -*-
"""plan_17v3.py — video 17 dung lai theo REAL-FIRST (user 2026-09-23: "Video nay khong giu chan duoc nguoi xem.
Gio chuyen ve che do cu. Tim anh va video that tao video, thieu thi moi dung video AI hoac anh AI").

Bang duoi = MOT DONG / CAU LOI (chi so dong trong timeline.json). Nguon:
  film  : ("F", file_trong__footage_pd, ss)          phim PD/CC0 da soi (CATALOG_*.md, RANGES_VERIFIED.md)
  stock : ("S", "stock/<file>.mp4", ss)              Pexels thoi nay (MANIFEST_stock.json)
  photo : ("P", "real_photos/<file>")                anh THAT Commons PD/CC (MANIFEST_photos.json)
  ai    : ("A",)                                     LAP bang clip AI cu cua chinh dong do (clips_v17ai)
  ima   : ("I", old_idx)                             canh "thoi nay" cua nguoi ke (PICK_FINAL/clip_<old_idx>)
Xuat 06_VIDEO/17_kaisha-ga-kureta/visual_plan.json (build_slides_v3) + _ASSIGN_17v3.json (make_17v3 doc).
"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\17_kaisha-ga-kureta")
JT, K59, U68, U69 = "japan_today_1959.mp4", "usaf11059_kyoto_home_1946.mp4", "usaf11068_industry_1946.mp4", "usaf11069_transport_1946.mp4"
YIJ, WTJ = "you_in_japan_512kb.mp4", "we_the_japanese_512kb.mp4"
# ⛔ KHONG dung steel_1960 (phim Iwanami cho Yawata) va japan_1960_nsc (ABC News): ban NARA ghi CC0 nhung
#    ban quyen goc cua hang phim tu nhan chua chac het -> rui ro Content ID. Chi dung phim DO CHINH PHU MY lam.
CS1, CS2 = "color_story_japan_1957_r1_sq.mp4", "color_story_japan_1957_r2_sq.mp4"
A = ("A",)
S = lambda f, ss=0.5: ("S", "stock/" + f, ss)
F = lambda f, ss: ("F", f, ss)
P = lambda f: ("P", "real_photos/" + f)

L = {
 # ---- HOOK (entry 0 = phim that) ----
 0: F(YIJ, 1231.5),      # van phong 1957, nhan vien ban giay
 1: F(WTJ, 692.0),       # 3 cong nhan doi dien 2 quan ly — dam phan luong
 2: F(CS2, 289.0),       # quang truong Hoang cung, khoi van phong Marunouchi
 3: F(K59, 648.0),       # bua com gia dinh — nha, tro cap, con
 4: F(JT, 1235.0),       # Ginza, dam dong cong chuc — 「これが、昭和の会社です」
 5: F(CS1, 425.0),       # dai lo, dam dong di ve phia may — loi chao
 6: F(JT, 109.0),       # dai lo tuyet tung, dong nguoi (duyet mat 23/09: WTJ 422 dinh shot co o dau)
 # ---- M1 luong ----
 7: F(U69, 341.0),       # can mat cac cau be tho duong sat mat lem muoi — nhan vien tre
 8: F(CS2, 8.0),         # pho Nakamise dong nguoi
 9: F(CS2, 66.0),        # can mat dan ong, nguoi lon tuoi deo kinh
 10: A, 11: A,           # thang hai / to giay yeu cau tren bang cong doan
 12: F(WTJ, 550.5),      # hop hop tac xa, ngoi chat san, tranh luan
 13: F(WTJ, 1023.5),     # mit tinh, bang ron
 14: F(WTJ, 1061.5),     # nguoi tren thang dan ten len bang lon tren dam dong
 15: A, 16: A, 17: A,    # to roneo, nam thap thi im lang, to giay mot nam
 18: F(WTJ, 650.5),     # nha may thep (USIA 1952)
 19: F(CS1, 205.5),      # pho hang, nguoi di mua
 20: F(WTJ, 578.5),      # cong nhan tran qua cong nha may
 21: F(WTJ, 1034.5),     # dien gia truoc micro roi dam dong
 22: A,
 23: A,
 24: F(WTJ, 662.5),     # day chuyen lap rap xe tai
 25: F(U69, 270.0),     # nha dau may toan canh
 26: F(U69, 491.0),     # doan tau hang nhin tu tren
 27: F(U69, 366.5),     # tau dien tren tuyen chinh
 28: A,                  # khung hoang dau
 29: F(JT, 767.5),       # vuon yen, nguoi di xa
 30: S("tokyo_eki_hiroba_34883472.mp4"),
 31: S("rush_station_36035831.mp4"),
 32: S("crossing_timelapse_35488300.mp4"),
 33: S("tokyo_skyline_tl_10024586.mp4"),
 34: S("shibuya_crowd_25947488.mp4"),
 35: F(YIJ, 1213.5),     # san ga ngam nguoi di lam
 36: F(YIJ, 1219.5),     # hanh lang ga, dam dong
 37: F(JT, 736.0),       # ong lao com-le trong vuon
 # ---- M2 gia dinh ----
 38: F(JT, 286.5),       # vo kimono, chong com-le dat con nho
 39: A, 40: A,           # nop giay dang ky ket hon / bang luong them dong
 41: F(JT, 266.5),       # nhom tre con cuoi
 42: A,                  # phong bi day hon, hop canh thung gao
 43: F(U69, 451.0),     # nhan vien dieu do phat co — nguoi dang lam viec
 44: F(K59, 769.0),      # bua com gia dinh toan canh
 45: F(U69, 2.5),        # san ga chat nguoi 1946
 46: F(U68, 161.5),      # tram bien ap — 電産 1946
 47: F(U68, 231.0),      # can gao, thu ky ghi so
 48: F(K59, 804.5),      # vo chong an com
 49: F(U69, 188.5),      # tho duong sat tra dau dau may
 50: F(K59, 820.5),      # can mat gia dinh an
 51: F(K59, 658.0),      # ca nha quanh ban
 52: S("tokyo_eki_night_18910159.mp4"),
 53: S("jp_meeting_7844861.mp4"),
 54: S("jp_typing_7844927.mp4"),
 55: S("calculator_notes_7593891.mp4"),
 56: S("calculator_man_8478944.mp4"),
 57: S("subway_commuters_39403955.mp4"),
 58: F(CS2, 90.2),       # bo com-le dat con trai nho
 59: P("meshi_1951_shokutaku.jpg"),
 # ---- M3 nha o ----
 60: P("danchi_nishinomiya_1960.jpg"),
 61: A, 62: A,           # chia khoa ky tuc xa / phong 3 chieu, bon tam chung, gio gioi nghiem
 63: P("danchi_tokiwadaira_1960.jpg"),
 64: A, 65: A,           # phoi do / bon tam theo gio, tuong mong
 66: F(K59, 1017.0),     # bep, nguoi vo nau an
 67: A,
 68: F(YIJ, 1244.0),     # dan ong di ve doc hang rao, tre con nhin ra cua
 69: A,
 70: P("kodan_chosa_1960_a.jpg"),   # bang dieu tra nguoi thue nha Kodan 1960
 71: A,
 72: A,
 73: S("plaza_aerial_37439460.mp4"),
 74: A,
 75: S("rush_station2_36035783.mp4"),
 76: A, 77: A,
 78: F(YIJ, 887.0),     # mai nha may va ong khoi, toan canh
 79: F(K59, 856.5),      # trai futon
 # ---- CTA ----
 80: F(CS2, 518.5),      # Phu Si tren vinh
 # ---- M4 tiet kiem ----
 81: S("coin_jar_7118320.mp4"),
 82: A,
 83: F(WTJ, 423.2),      # hai thu ky gia ben chong so
 84: A, 85: A,
 86: A,
 87: F(YIJ, 920.5),     # xuong cap dien, cau truc, may cuon — may moc
 88: A, 89: A,
 90: P("takasaki_shichosha_1954.jpg"),
 91: F(YIJ, 1015.5),     # khoi van phong moi, cong nhan xay dung
 92: A, 93: A, 94: A,
 95: S("jp_meeting2_7844856.mp4"),
 96: A,
 97: F(JT, 472.0),       # ho suong
 # ---- M5 huu tri ----
 98: F(JT, 413.0),       # nguoi com-le di ra tu cong chua
 99: A, 100: A, 101: A, 102: A, 103: A, 104: A,
 105: F(YIJ, 1260.5),    # bo, con trai, me ben ban thap
 106: F(U69, 404.5),   # hai tho duong sat chat thuoc — nghi giai lao
 107: F(WTJ, 727.5),     # tho tan dinh xuong tau
 108: F(WTJ, 592.5),     # phu nu ve dia o xuong gom (cong ty nho)
 109: F(WTJ, 742.5),     # ha thuy tau, cong nhan reo
 110: A,
 111: S("subway_arrival_30364860.mp4"),
 112: S("jp_salaryman_portrait_7845250.mp4"),
 113: S("subway_green_17371342.mp4"),
 114: A, 115: A, 116: A,
 117: F(CS1, 318.0),      # gia dinh tre con ben ho
 118: F(CS2, 150.5),      # dam dong co tre nho
 # ---- KET ----
 119: ("I", 102), 120: ("I", 103), 121: ("I", 104),
 122: F(U69, 547.0),     # nguoi di lam chen len tau dien 1946
 123: F(CS2, 498.5),     # ben xe buyt ga Kamakura
 124: F(K59, 704.5),     # vo xoi com cho chong
 125: A,
 126: F(K59, 879.5),     # trai futon
 127: ("I", 108), 128: ("I", 108), 129: ("I", 109),
 130: F(JT, 180.5),      # dam dong com-le o den — 社員旅行
 131: A,
 132: F(JT, 213.0),      # nhom dan ong com-le truoc dien
 133: F(JT, 76.0),       # thung lung, thi tran
 134: ("I", 111),
}

tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
lines = tl["lines"]
assert set(L) == set(range(len(lines))), "thieu dong: %s" % sorted(set(range(len(lines))) - set(L))
film_lines, ranges, ai = [], [], []
for i in range(len(lines)):
    k = L[i]; t = lines[i]["start"]
    if k[0] in ("F", "S"):
        film_lines.append([t, k[1], k[2], ""]); continue
    ranges.append([t, "photo" if k[0] == "P" else "aistill"])
    if k[0] in ("A", "I"):
        dur = (lines[i + 1]["start"] if i + 1 < len(lines) else tl["total"]) - t
        if dur <= 9.5:
            ai.append(t)      # dong ngan: clip AI chay that; dong dai: anh tinh AI giu toi 18s
plan = {"_note": "REAL-FIRST lai cho video 17 (sinh boi tools/plan_17v3.py). film_lines = phim PD + stock Pexels.",
        "default": "aistill", "ranges": ranges, "ai": ai, "film_lines": film_lines,
        "preset": [[0.0, "office"], [lines[38]["start"], "tatami"], [lines[60]["start"], "flat"],
                   [lines[81]["start"], "office"], [lines[119]["start"], "flat"]]}
(VD / "visual_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
(VD / "_ASSIGN_17v3.json").write_text(json.dumps({str(i): list(v) for i, v in L.items()}, ensure_ascii=False, indent=0), encoding="utf-8")
from collections import Counter
c = Counter(v[0] for v in L.values())
print("dong theo nguon:", dict(c), "| ai marks:", len(ai))
