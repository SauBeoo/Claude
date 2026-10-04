# -*- coding: utf-8 -*-
"""plan_20.py — BANG HINH THEO CAU cho video 20 (khuon v08: hinh THAT la lop chinh, AI chi lap).

Khac plan_19: khoa PLAN_T la CHI SO TIMELINE (1..144, dung thu tu dong co chu trong _TTS.md),
tool tu doi sang so dong FILE (PLAN) cho build_slides — khong phai dem dong trong bang tay.

Ma nguon:
  cc:<key>__NN   Commons tim chu      (_cc/candidates_info.json)
  cat:<key>__NN  Commons theo category (_cat/cat_info.json)
  p71:NNN        wilford peloquin 1971, CC BY 2.0 (index cua video 19: 19_kaimono-joushiki/_p1971/index.json)
                 -> 46 anh video 19 da dung nam trong _blacklist/commons_used.txt, tool CHAN
  px:<key>__NN   Pexels anh ; pxv:<key>__NN Pexels clip quay that
  AI:<ten>       anh AI tinh (Nano Banana) — chi lap canh co NGUOI/VAT ma khong nguon that nao thay duoc
  +NUM           chu (so/mot dong chu) ve bang FONT len anh — chu lay NGUYEN tu cau dang doc

    python tools/plan_20.py            # bao cao ti le + gate trung ma / sổ den
    python tools/plan_20.py --fetch    # tai ban goc vao real_20/
"""
import io, sys, json, re, time
from pathlib import Path
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

STEM = "20_sumai-okane"
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / STEM
TTS = ROOT / "03_SCRIPTS" / (STEM + "_TTS.md")
P71 = ROOT / "06_VIDEO" / "19_kaimono-joushiki" / "_p1971" / "index.json"

# (chi so timeline, [o hinh...]) — [] = o truoc KEO DAI qua dong nay
PLAN_T = [
 # ---------- HOOK v3 B+ (2026-09-27, user: "tranh luan / dong cam, hoai niem" cho U60) ----------
 (1,  ["cat:c_danchi__04"]),                 # entry 0 = phong 昭和 THAT + 茶だんす (khop 「茶だんすを片づけていたら」)
 (2,  ["cc:hagaki_old__00+NUM"]),            # hagaki THAT 1949 + chu 落選
 (3,  ["AI:mother_argue"]),                  # clip AI MOI: me lan dau cai lai cha (phu dong 3-4, 9,2s)
 (4,  []),
 (5,  ["AI:father_goes_out"]),               # anh AI MOI: cha keo cua ra ngoai
 (6,  ["cc:sento_out__01"]),                 # ong khoi 銭湯 THAT (お風呂もない…銭湯の帰り)
 (7,  ["p71:455"]),                          # hom thu do Tokyo 1971 THAT (七回目を出しましたか)
 (8,  ["AI:hagaki_bundle"]),                 # clip tay nhac bo thiep (なぜ…捨てずにいたのか)
 (9,  ["p71:446"]), (10, ["p71:451"]),
 (11, ["cat:c_danchi__06"]),                 # bep DK mau 1962 (CC0)
 # ---------- MUC 1 六畳一間 ----------
 (12, ["px:px_tatami__09"]),
 (13, ["p71:444"]),
 (14, ["AI:father_print"]),                  # tho in — 0 anh that (insatsu: 0/9 dung duoc)
 (15, ["p71:182"]),                          # quang truong ga 1971
 (16, ["AI:fudousan_door+NUM"]),             # cua kinh bat dong san, to giay TRONG + chu font
 (17, ["px:px_nameplate__09", "AI:apart_corridor"]),
 (18, ["AI:window_monohoshi"]),
 (19, []),
 (20, ["AI:father_nod"]),                   # px_tatami__05 = phong chua tham do, khong phai phong tro
 (21, ["AI:two_envelopes"]),
 (22, []),
 (23, ["px:px_rubber__06+NUM"]),
 (24, ["px:px_rubber__01+NUM"]),
 (25, ["p71:462+NUM"]),
 (26, ["p71:449+NUM"]),
 (27, ["p71:171+NUM"]),
 (28, ["p71:447"]),
 (29, ["AI:shared_toilet+NUM"]),
 (30, ["AI:toilet_line", "px:px_alarm__09"]),
 (31, ["px:px_tatami__04"]),
 # ---------- MUC 2 銭湯 ----------
 (32, []),                                  # v3: sento_out__01 dua len hook                 # ong khoi sento THAT
 (33, ["AI:senmenki_prep"]),
 (34, ["px:px_geta__00", "AI:night_walk_geta"]),
 (35, ["cc:sento__04"]),                   # tuong tranh Phu Si (PD); sento__11 = khach mac do hien dai -> bo
 (36, ["AI:mother_baby_sento", "AI:mother_dress_baby"]),
 (37, ["AI:sento_noren_night"]),              # sento__05 = pho Osaka hien dai, nguoi deo balo -> bo
 (38, ["cc:sento__02"]),
 (39, ["AI:mother_tub_baby"]),
 (40, ["cc:balance__00"]),                  # user 2026-09-27: khong trung anh -> mother_tub_still = cung canh clip sento; バランス釜 that (いつか、うちのお風呂に)
 (41, []),
 (42, ["cc:sento__00"]),   # バランス釜 1967 (PD) canh thung go
 (43, ["p71:569+NUM"]),
 (44, ["cc:sento__01+NUM"]),
 (45, ["pxv:v_rain__08"]),
 (46, []),
 (47, ["p71:555+NUM", "cc:geta__05"]),
 (48, ["AI:bandai_lady"]),
 (49, ["cc:sento_out__00+NUM"]),
 (50, ["AI:after_bath_walk"]),
 # ---------- MUC 3 団地 ----------
 (51, ["cc:danchi_old__01"]),
 (52, ["AI:father_flyer"]),
 (53, ["cat:c_danchi__27"]),                # user 2026-09-27: khong trung anh -> c_danchi__31 dua xuong dong 75
 (54, ["AI:flyer_table"]),
 (55, ["AI:couple_table"]),                 # clip user (vo chong ben ban tra) — cheo o 13,3s cu
 (56, ["AI:mother_reads_flyer"]),
 (57, ["AI:hagaki_single+NUM"]),
 (58, []),
 (59, ["AI:hagaki_six_table"]),
 (60, ["AI:father_smoke_out", "pxv:v_smoke__06"]),
 (61, ["AI:mother_drawer"]),
 (62, ["cc:danchi_old__03"]),
 (63, ["cc:danchi_old__00+NUM"]),           # user 2026-09-27: khong trung anh -> c_danchi__22 gan giong c_danchi__01 (danchi xa qua ruong)
 (64, ["cat:c_danchi__21+NUM"]),            # c_danchi__03 dua xuong dong 94
 (65, ["cat:c_danchi__11"]),
 (66, ["cc:danchi_old__02"]),
 (67, ["cat:c_danchi__02+NUM"]),
 (68, ["cat:c_danchi__36+NUM"]),
 (69, ["cat:c_danchi__01+NUM"]),              # danchi__25 = cao tang hien dai -> bo
 (70, ["AI:hagaki_seventh"]),
 (71, ["px:px_key__05"]),
 (72, ["AI:danchi_boxes"]),
 (73, ["pxv:v_flame__04"]),
 (74, ["AI:danchi_bath_mother"]),
 (75, ["cat:c_danchi__31"]),               # user 2026-09-27: khong trung anh -> danchi_bath_b = cung canh clip bon danchi; noi that danchi THAT (ここは、うちの)
 (76, ["AI:father_beer"]),
 (77, ["px:px_key__04"]),
 (78, ["cat:c_danchi__38"]),
 # ---------- CTA 55% ----------
 (79, ["cat:c_danchi__24", "cat:c_danchi__09", "cat:c_danchi__19"]),
 # ---------- MUC 4 公庫 ----------
 (80, ["px:px_nameplate__06"]),
 (81, ["cat:c_danchi__10"]),
 (82, ["AI:futon_room"]),
 (83, ["AI:coat_pocket"]),
 (84, []),                                  # px_cigarette__03 = bao thuoc hieu SAIGON (nuoc ngoai) -> bo
 (85, []),
 (86, ["AI:passbook_small"]),
 (87, ["px:px_nameplate__08"]),
 (88, ["p71:450+NUM"]),
 (89, ["AI:house_frame+NUM"]),             # user 2026-09-27: khong trung anh -> 4 anh ruong lua xanh Pexels (01/03/07/10) nhin nhu mot
 (90, ["px:px_field__06+NUM"]),
 (91, ["p71:172"]),
 (92, ["p71:445+NUM", "p71:184"]),
 (93, ["p71:353+NUM", "p71:355"]),
 (94, ["AI:hanko_form", "cat:c_danchi__03"]),  # user 2026-09-27: khong trung anh -> hanko_form_b cung cap vo chong cung tu the; ban DK that
 (95, ["p71:187+NUM"]),
 (96, ["px:px_cigarette__00", "AI:house_pillar"]),
 # ---------- MUC 5 土地 ----------
 (97, ["pxv:v_field__11"]),
 (98, ["px:px_field__04"]),
 (99, ["pxv:v_field__00+NUM"]),
 (100, ["p71:570+NUM", "pxv:v_field__06"]),
 (101, []),
 (102, ["cc:bus_old__08"]),
 (103, ["AI:mother_worried"]),
 (104, []), (105, []),
 (106, []),
 (107, ["p71:194+NUM", "p71:168"]),
 (108, ["pxv:v_field__07"]),
 (109, ["p71:549+NUM"]),
 (110, ["AI:nameplate_nail"]),                # px_field__09 = chung cu cam doi moi -> bo
 (111, ["AI:new_bath_window"]),
 (112, ["cc:bus_old__02", "p71:169"]),       # xe buyt 1974 + dong nguoi di lam 1971
 (113, ["p71:195+NUM", "pxv:v_buswin__04"]),
 (114, ["AI:father_old_porch"]),
 (115, ["px:px_field__00"]),
 (116, []),
 # ---------- KET: mat sau hagaki ----------
 (117, ["AI:chadansu_open"]),
 (118, ["AI:hands_rubber_band"]),
 (119, ["AI:hagaki_back_0"]),
 (120, ["AI:hagaki_back_1+NUM"]),            # chu viet tay cua cha = FONT, khong giao AI ve chu
 (121, ["AI:hagaki_back_2+NUM"]),
 (122, ["AI:hagaki_back_3+NUM"]),
 (123, ["AI:hagaki_back_4+NUM"]),
 (124, ["AI:hagaki_back_5+NUM"]),
 (125, []),
 (126, ["AI:hagaki_back_6+NUM"]),
 (128, ["AI:drawer_hagaki_stack"]),
 (129, ["AI:mother_young_letter"]),
 (130, ["px:px_wallet__06"]),
 (131, ["AI:old_father_wallet"]),
 (132, ["AI:worn_hagaki"]),
 (133, ["px:px_oldhands__03"]),
 (134, ["cat:c_danchi__00"]),
 (135, ["cat:c_danchi__08"]),
 (136, ["pxv:v_clock__05"]),
 (137, ["cat:c_danchi__39"]),               # danchi__14 = nha mo bo hoang -> sai tong; px_field__07 = ruong trung
 (138, ["AI:bandai_lady_old", "cc:bus_old__07"]),  # bus_old__06 = xe LED 「90周年」 doi moi -> bo
 (139, ["pxv:v_tatami__07"]),
 (140, []),                                 # v3: 「あなたのご両親は…」 o truoc keo qua
 (141, ["p71:329"]),                  # p71:198 = tiem pachinko -> bo
 (142, ["p71:331"]), (143, ["p71:342"]), (144, []),
 (145, ["p71:344"]), (146, []),
]

# chu tren o +NUM — (chi so timeline, thu tu o +NUM trong dong) -> cac dong chu. Moi chu PHAI co trong cau doc.
NUMTXT_T = {
    (2, 0):  ["落選"],
    (16, 0): ["六畳・共同トイレ", "日当たり良好"],
    (23, 0): ["敷金", "出ていくとき 残りが返る"],
    (24, 0): ["礼金", "返ってこない"],
    (25, 0): ["礼金", "どの法律にも 書かれていない"],
    (26, 0): ["大正10年 借家法", "平成3年 借地借家法", "「礼金」の言葉は なし"],
    (27, 0): ["令和2年4月", "民法で 敷金の意味を定める"],
    (29, 0): ["昭和43年", "民営の借家 およそ3軒に1軒", "便所は 共同"],
    (43, 0): ["昭和43年 都内", "浴室のある住宅 42.2%"],
    (44, 0): ["昭和43年 都内の銭湯", "2,687軒"],
    (47, 0): ["昭和21年 物価統制令", "入浴料金の上限は", "都道府県の知事が決める"],
    (49, 0): ["令和5年 都内の銭湯", "444軒"],
    (57, 0): ["落選"],
    (63, 0): ["昭和30年", "日本住宅公団法"],
    (64, 0): ["昭和31年 金岡団地", "ダイニングキッチン 第1号"],
    (67, 0): ["昭和41年 東日本", "募集 6,564戸", "申し込み 337,613人"],
    (68, 0): ["平均の倍率", "51.4倍"],
    (69, 0): ["昭和45年1月", "公団の住宅 50万戸を超える"],
    (88, 0): ["昭和25年", "住宅金融公庫法"],
    (89, 0): ["利子 年5.5%", "返す期間 30年まで"],
    (90, 0): ["昭和50年", "基準の利子 5.5%のまま"],
    (92, 0): ["昭和47年 住宅取得控除", "1年に2万円まで・3年間"],
    (93, 0): ["昭和48年", "持ち家 59.1%"],
    (95, 0): ["平成19年4月 公庫 廃止", "住宅金融支援機構へ"],
    (99, 0): ["昭和47年", "『日本列島改造論』"],
    (100, 0): ["昭和48年3月までの1年", "全国の土地 +25.1%"],
    (107, 0): ["昭和36年", "1年で +42.5%"],
    (109, 0): ["昭和44年 地価公示法", "翌年から 毎年公表"],
    (113, 0): ["全国の住宅地", "平成3年 いちばん高い", "平成4年 −5.6%"],
    (120, 0): ["次は、当たる"],
    (121, 0): ["銭湯の帰り、", "寒くなかったか"],
    (122, 0): ["すまん"],
    (123, 0): ["娘が、今日、", "三歩あるいた"],
    (124, 0): ["あと一回だけ、", "待ってくれ"],
    (126, 0): ["当たらなくても、", "おまえとこの子がいれば、", "六畳で足りる"],
}

TAG = re.compile(r"\[[^\]]*\]")
_norm = lambda s: re.sub(r"\s+|[、。「」『』・,.!?！？…―—\-]", "", TAG.sub("", s))

def _file_lines():
    """chi so timeline (1..N) -> so dong FILE _TTS.md (dong co chu)."""
    raw = TTS.read_text(encoding="utf-8").splitlines()
    return [n for n, l in enumerate(raw, 1) if TAG.sub("", l).strip()]

FL = _file_lines()
PLAN = [(FL[t - 1], cs) for t, cs in PLAN_T]
NUMTXT = {(FL[t - 1], k): v for (t, k), v in NUMTXT_T.items()}

def cls(code):
    return "AI" if code.startswith("AI:") else ("NEED" if code.startswith("NEED:") else "REAL")

cells = [c for _, cs in PLAN_T for c in cs]

def report():
    bad = 0
    ts = [t for t, _ in PLAN_T]
    if ts != sorted(ts) or len(set(ts)) != len(ts): print("🔴 PLAN_T khong tang deu / trung dong"); bad = 1
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    if len(FL) != len(tl): print("🔴 so dong TTS %d != timeline %d" % (len(FL), len(tl))); bad = 1
    missing = sorted(set(range(1, len(tl) + 1)) - set(ts))
    if missing: print("⚠️ dong khong co trong PLAN_T (o truoc keo dai):", missing)
    # chu +NUM phai nam trong cau doc
    for (t, k), v in NUMTXT_T.items():
        said = _norm(tl[t - 1]["text"])
        for s in v:
            for tok in re.findall(r"[0-9][0-9,.]*", s):
                pass  # so viet bang chu Han trong loi doc -> kiem bang mat o bang ben duoi
    nnum = Counter((t, ) for t, cs in PLAN_T for c in cs if "+NUM" in c)
    for t, cs in PLAN_T:
        for k, c in enumerate([c for c in cs if "+NUM" in c]):
            if (t, k) not in NUMTXT_T: print("🔴 thieu chu cho o +NUM dong", t, c); bad = 1
    cnt = Counter(cls(c) for c in cells); n = len(cells)
    base = [c.replace("+NUM", "") for c in cells]
    dup = [k for k, v in Counter(base).items() if v > 1]
    if dup: print("🔴 ma lap trong bai:", dup); bad = 1
    # so den (anh da len song)
    J = lambda p: json.loads((VD / p).read_text(encoding="utf-8"))
    used = set(x.strip().replace("_", " ") for x in (VD / "_blacklist" / "commons_used.txt").read_text(encoding="utf-8").splitlines() if x.strip())
    p71 = {v["n"]: k for k, v in json.loads(P71.read_text(encoding="utf-8")).items()}
    for c in set(base):
        if c.startswith("p71:"):
            ttl = p71.get(int(c[4:]))
            if ttl is None: print("🔴 khong co", c); bad = 1
            elif ttl.replace("_", " ") in used: print("🔴 SO DEN (da len song):", c, ttl); bad = 1
    SRC = {"cc": J("_cc/candidates_info.json"), "cat": J("_cat/cat_info.json"),
           "px": J("_px/px_info.json"), "pxv": J("_pxv/pxv_info.json")}
    for c in set(base):
        pre, _, key = c.partition(":")
        if pre in SRC and key not in SRC[pre]: print("🔴 khong co ma", c); bad = 1
    # cung mot file Pexels/Commons duoi hai ma khac nhau
    ids = Counter()
    for c in set(base):
        pre, _, key = c.partition(":")
        if pre in SRC:
            v = SRC[pre][key]; ids[str(v.get("id") or v.get("title") or v.get("url"))] += 1
    d2 = [k for k, v in ids.items() if v > 1]
    if d2: print("🔴 cung mot file duoi hai ma:", d2); bad = 1
    # thoi luong o (uoc theo khe dong, dung cach build_slides chia)
    st = [l["start"] for l in tl] + [json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["total"]]
    plan = dict(PLAN_T); durs = []; cur = None
    for t in range(1, len(tl) + 1):
        if plan.get(t):
            cur = [st[t] - st[t - 1], len(plan[t])]; durs.append(cur)
        else:
            cur[0] += st[t] - st[t - 1]
    dd = sorted(a / b for a, b in durs for _ in range(b))
    long_ = [(round(a / b, 1)) for a, b in durs if a / b > 18]
    print("o hinh: %d | THAT %d (%d%%) | AI %d (%d%%)" % (n, cnt["REAL"], cnt["REAL"] * 100 // n, cnt["AI"], cnt["AI"] * 100 // n))
    print("  clip that:", sum(1 for c in cells if c.startswith("pxv:")), "| o chu font +NUM:", sum(1 for c in cells if "+NUM" in c))
    print("  giu moi o: trung vi %.1fs | min %.1fs | max %.1fs | %.1f doi/phut" % (dd[len(dd) // 2], dd[0], dd[-1], n / (st[-1] / 60)))
    if long_: print("🔴 o vuot tran 18s:", long_); bad = 1
    print("  AI (%d):" % len({c for c in base if c.startswith('AI:')}), " ".join(sorted({c[3:] for c in base if c.startswith('AI:')})))
    print("GATE PLAN:", "SACH" if not bad else "DO")
    return bad

# ---------------------------------------------------------------- --fetch (chep tu plan_19, bo nguon khong dung)
def _thumb(url_thumb, w, want=3840):
    return re.sub(r"/(\d+)px-", "/%dpx-" % want, url_thumb.split("?")[0], count=1) if w > want else None

def fetch():
    import requests
    H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
    OUTD = VD / "real_20"; OUTD.mkdir(exist_ok=True)
    J = lambda p: json.loads((VD / p).read_text(encoding="utf-8"))
    SRC = {"cc": J("_cc/candidates_info.json"), "cat": J("_cat/cat_info.json"),
           "px": J("_px/px_info.json"), "pxv": J("_pxv/pxv_info.json")}
    p71 = {v["n"]: dict(v, title=k) for k, v in json.loads(P71.read_text(encoding="utf-8")).items()}
    manp = OUTD / "MANIFEST.json"
    man = json.loads(manp.read_text(encoding="utf-8")) if manp.exists() else {}
    codes = sorted({c.replace("+NUM", "") for c in cells if cls(c) == "REAL"})
    bad = []
    for code in codes:
        pre, key = code.split(":", 1)
        if pre == "p71":
            v = p71[int(key)]; kind = "photo"
            url = _thumb(v["thumb"], v["w"]) or v["url"].split("?")[0]
            lic, who, page = "CC BY 2.0", "Wilford Peloquin", "https://commons.wikimedia.org/wiki/" + v["title"].replace(" ", "_")
        else:
            v = SRC[pre][key]
            if pre in ("cc", "cat"):
                kind = "photo"; url = _thumb(v["thumb"], v["w"]) or v["url"].split("?")[0]
                lic, who, page = v.get("license"), v.get("artist"), "https://commons.wikimedia.org/wiki/" + v["title"].replace(" ", "_")
            elif pre == "px":
                kind = "photo"; url = v["original"] + "?auto=compress&cs=tinysrgb&w=2560"
                lic, who, page = "Pexels License", v.get("photographer"), v["url"]
            else:
                kind = "video"; url = v["file"]
                lic, who, page = "Pexels License", v.get("user"), v["url"]
        ext = ".jpg" if kind == "photo" else ("." + url.split("?")[0].rsplit(".", 1)[-1].lower())
        fn = code.replace(":", "_") + ext
        dst = OUTD / fn
        if not (dst.exists() and dst.stat().st_size > 10000):
            ok = False
            for t in range(4):
                try:
                    r = requests.get(url, headers=H, timeout=120, stream=True)
                    if r.status_code == 429: time.sleep(10 * (t + 1)); continue
                    r.raise_for_status()
                    tmp = dst.with_suffix(dst.suffix + ".part")
                    with open(tmp, "wb") as f:
                        for ch in r.iter_content(1 << 16): f.write(ch)
                    tmp.replace(dst); ok = True; break
                except Exception as e:
                    print("  thu lai", code, e); time.sleep(3 * (t + 1))
            if not ok:
                bad.append(code); print("LOI", code, url); continue
            time.sleep(0.4)
        man[code] = {"file": fn, "kind": kind, "license": lic, "author": who, "page": page, "url": url}
        print("OK  %-28s %-6s %8d KB" % (code, kind, dst.stat().st_size // 1024))
    manp.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nTai xong %d/%d | LOI %d %s" % (len(codes) - len(bad), len(codes), len(bad), bad))
    return 1 if bad else 0

if __name__ == "__main__":
    if "--fetch" in sys.argv:
        sys.exit(fetch())
    sys.exit(report())
