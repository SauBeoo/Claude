# -*- coding: utf-8 -*-
"""plan_19.py — BANG HINH THEO CAU cho video 19 (khuon v08, muc tieu >=80% hinh THAT).

Moi dong TTS -> danh sach o hinh. Ma nguon:
  cc:<key>__NN   Commons tim chu      (_cc/candidates_info.json)
  cat:<key>__NN  Commons theo category (_cat/cat_info.json)
  p71:NNN        wilford peloquin 1971, CC BY 2.0 (_p1971/index.json)
  px:<key>__NN   Pexels anh           (_px/px_info.json)
  pxv:<key>__NN  Pexels clip QUAY THAT (_pxv/pxv_info.json)
  AI:<ten>       canh bat buoc co NGUOI dang dien — gen Flow (tick altered/synthetic)
  NEED:<mo ta>   chua co nguon that — phai tim tiep (khong duoc tu dong thanh AI)
  +NUM           o so lieu: chu so ve bang FONT de len anh that (van tinh la anh that)

    python tools/plan_19.py            # in bao cao ti le + ghi SOURCING_19.md
    python tools/plan_19.py --fetch    # tai ban goc (anh 2560px / clip 1920) vao real_19/
"""
import io, sys, json, re, time
from pathlib import Path
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / "19_kaimono-joushiki"

# (so dong TTS, [o hinh...])  — so dong = dong trong 19_kaimono-joushiki_TTS.md
PLAN = [
 # ---------- HOOK 0-60s ----------
 (1,  ["cat:c_genkan__20", "AI:denkiya_bow"]),            # entry 0 = 玄関 THAT (khop 「玄関で」), roi nguoi cui dau
 (2,  []),                                               # clip AI:denkiya_bow chay tiep qua loi thoai
 (3,  ["AI:kids_tv"]),
 (4,  ["cat:c_furoshiki__27"]),                      # (thu AI:mother_night 2026-09-26 -> BO: la anh goc cua clip mother_two_piles = lap hinh)                          # hai ban tay that dang that furoshiki
 (5,  ["px:px_purse__06"]),                           # 2026-09-26 hook A9: gamaguchi__01 co to quang cao + URL hien dai (AI:pawn_counter = anh goc clip hands_shichifuda -> bo)
 (6,  ["cc:kimono_houmongi__06"]),                        # 訪問着 THAT (MET, CC0)
 (7,  ["cc:factory_1970__02"]),                           # TV go co chan
 (9,  ["p71:571"]),
 (10, ["p71:460"]),
 (11, ["cat:c_gamaguchi__00"]),                       # doi 2026-09-26: cc:gamaguchi__10 = CUNG FILE voi cat:c_gamaguchi__03
 # ---------- MUC 1 thang gop ----------
 (13, ["cat:c_showamuse__26"]),
 (15, ["pxv2:w_woodhouse__00"]),
 (16, ["cc:kei_truck__01", "cc:tv_color__00"]),
 (17, ["p71:181", "p71:180"]),
 (18, []), (19, ["pxv:v_crt__01"]),
 (20, ["cat:c_chanoma__24", "cat:c_showamuse__25"]),
 (21, ["px:px_stamp__04"]),
 (22, ["era:e00", "cc:coin_100yen__00"]),               # 2026-09-26 era-fix: v_stamp = dau cao su Tay
 (23, ["cat:c_showamuse__33"]),
 (24, ["cc:fridge_old__00", "p71:188"]),
 (25, ["p71:291", "p71:292"]),
 (26, ["cat:c_showamuse__09+NUM", "cat:c_chanoma__19+NUM", "cat:c_showamuse__11+NUM"]),
 (27, ["cat:c_shitamachi__21"]),
 (28, ["p71:554+NUM", "cat:c_shitamachi__26+NUM"]),
 (29, ["AI:book_half"]),                               # era-fix: v_stamp__09 = the qua THANK YOU
 (30, ["cat:c_genkan__09", "cat:c_edotokyo__04"]),
 (31, ["cat:c_genkan__35"]),
 (32, ["cat:c_chanoma__22", "pxv:v_crt__11"]),
 # ---------- MUC 2 cam do ----------
 (34, ["cat:c_iseya__00"]),
 (36, ["AI:father_factory", "p71:448"]),
 (37, ["cc:furoshiki__09"]),
 (38, ["pxv2:w_lantern__00", "cat:c_shitamachi__20"]),
 (39, ["pxv:v_fabric__01"]),
 (40, ["cat:c_iseya__02"]),
 (41, ["AI:hands_shichifuda", "cat:c_furoshiki__36"]),  # 2026-09-26: dong 41 dai them (風呂敷 gap lai)
 (42, ["cat:c_iseya__04", "cc:kura__00"]),
 (43, ["cat:c_iseya__05"]),
 (44, ["p71:170"]),
 (45, ["pxv2:w_tatami__09", "cc:furoshiki__07"]),
 (46, ["cat:c_iseya__01+NUM"]),
 (47, ["cc:noren__08+NUM"]),
 (48, ["p71:199", "p71:242"]),
 (49, ["cat:c_iseya__03+NUM"]),
 (50, ["pxv2:w_tatami__05", "pxv:v_coinhand__02"]),
 (51, ["AI:book_open", "cat:c_shitamachi__34"]),         # era-fix: v_stamp__00 = dau sap chau Au (anh me dong dau khong co trong lo -> so mo tren ban)
 # ---------- MUC 3 my pham ----------
 (53, ["cc:register_old__07"]),
 (55, ["AI:mother_cosme_window", "cat:c_showamuse__12"]),
 (56, ["cat:c_showamuse__13", "cc:lipstick_old__03"]),
 (57, ["AI:lipstick_hand"]),
 (58, ["cc:lipstick_old__05"]),
 (59, ["p71:461", "p71:190"]),
 (60, ["px:px_lipstick__09"]),
 (61, ["cc:pharmacy_old__03"]),
 (62, ["cat:c_showamuse__16", "cat:c_showamuse__17"]),
 (63, ["cat:c_showamuse__21+NUM", "cat:c_showamuse__18+NUM"]),
 (64, ["cat:c_showamuse__03", "cat:c_showamuse__22"]),
 (65, ["p71:193+NUM", "p71:185+NUM"]),
 (66, ["pxv3:n_drugstore__11"]),
 (67, ["cat:c_gamaguchi__04"]),
 (68, ["p71:258", "p71:257"]),
 # ---------- CTA ~48% ----------
 (70, ["p71:306", "p71:363", "p71:197", "p71:553", "p71:454"]),
 # ---------- MUC 4 dong cua ----------
 (72, ["cat:c_shotengai__00"]),
 (74, ["cat:c_shotengai__03", "p71:516"]),
 (75, ["p71:452"]),
 (76, ["cat:c_fish__22"]),                                # nguoi ban ca THAT, 1962
 (77, ["pxv:v_fish__10"]),
 (78, ["pxv2:w_greengro__05", "p71:349"]),
 (79, ["pxv:v_fry__07", "pxv:v_tofu__00"]),
 (80, ["era:e06", "cc:shutter__08"]),                   # era-fix: v_shutter__04 = nguoi mac mang to hien dai
 (81, ["cat:c_edotokyo__15"]),
 (82, ["cat:c_edotokyo__30"]),
 (83, ["p71:557"]),
 (84, ["cv:v_tofu__07", "cat:c_tofu__04"]),
 (85, ["p71:572+NUM", "cat:c_shotengai__10+NUM", "cat:c_shotengai__06+NUM"]),
 (86, ["p71:556+NUM", "p71:453+NUM"]),
 (87, ["p71:560"]),
 (88, ["p71:558+NUM", "pxv3:n_konbini__10"]),
 (89, ["pxv3:n_drugstore__01"]),
 (90, ["pxv2:w_fishmkt__06", "p71:350"]),
 # ---------- MUC 5 thue an trong gia ----------
 (92, ["cat:c_fish__04"]),                                # the gia viet tay 百円・三百円
 (94, ["cat:c_edotokyo__27", "cat:c_edotokyo__35"]),
 (95, ["pxv:v_coinhand__09", "cat:c_1yen__02"]),
 (96, ["cc:coin_1yen__05"]),
 (97, ["pxv:v_coins__06"]),
 (98, ["cc:car_1970__00", "cc:fridge_old__01"]),
 (99, ["cat:c_showamuse__10", "cat:c_showamuse__37"]),
 (100, ["AI:tv_night"]),                               # era-fix: CRT thap nien 90
 (101, ["era:e07"]),                                   # era-fix: SONY Trinitron doi Showa
 (102, ["AI:tv_front+NUM", "AI:tv_console+NUM"]),     # era-fix: CRT 90s -> TV hop go 1970 / console cuoi 70
 (103, ["AI:stamp_close"]),                            # era-fix: dau sap chau Au
 (104, ["cat:c_edotokyo__05"]),
 (105, ["cc:daikon__00", "pxv2:w_tofumake__08", "cat:c_yaoya__17"]),
 (106, ["px:px_register__05+NUM", "cat:c_1yen__00+NUM"]),  # 2026-09-26: c_1yen__01 nhin y het c_1yen__00; register_old__04 = cung file c_edotokyo__35
 (107, ["cat:c_yaoya__38", "cat:c_yaoya__10"]),
 (108, ["AI:yaoya_103yen"]),
 (109, ["cat:c_gamaguchi__02"]),
 (110, ["cc:coin_1yen__10+NUM", "cat:c_1yen__03+NUM"]),
 (111, ["pxv:v_coins__11", "p71:007"]),
 # ---------- KET ----------
 (113, ["cv:v_house__00"]),
 (114, ["pxv:v_fabric__00"]),
 (115, ["cat:c_kimono__24"]),
 (116, ["AI:mother_two_piles", "pxv:v_coinhand__00"]),
 (117, ["pxv:v_crt__10"]),
 (118, ["AI:book_full", "cat:c_kura__00"]),            # era-fix: dau sap chau Au
 (119, ["AI:daughter_bride"]), (120, []),
 (121, ["AI:mother_smile"]),
 (122, ["cat:c_chanoma__02"]),
 (123, ["cat:c_gamaguchi__03"]),
 (124, ["pxv:v_fabric__06", "cc:kimono_houmongi__04"]),
 (126, ["p71:226"]), (127, ["cv:c_tsukiji__00", "p71:267"]),
 (128, ["p71:003"]), (129, ["cat:c_fish__06", "p71:138", "cat:c_yaoya__26"]), (130, ["p71:253"]),
 (132, ["p71:051"]), (133, ["p71:050", "p71:113"]), (134, ["p71:114"]), (135, ["p71:154"]),
 (137, ["p71:155"]), (138, ["p71:562"]),
]

def cls(code):
    if code.startswith("AI:"): return "AI"
    if code.startswith("NEED:"): return "NEED"
    return "REAL"

cells = [c for _, cs in PLAN for c in cs]
cnt = Counter(cls(c) for c in cells)
n = len(cells)
base = [re.sub(r"(\+NUM|b)$", "", c.replace("+NUM", "")) for c in cells if cls(c) == "REAL"]
dup = [k for k, v in Counter(base).items() if v > 1]
print(f"o hinh: {n} | THAT {cnt['REAL']} ({cnt['REAL']*100//n}%) | AI {cnt['AI']} ({cnt['AI']*100//n}%) | CHUA CO {cnt['NEED']}")
print("  trong THAT: clip quay that", sum(1 for c in cells if c.startswith(("pxv:", "pxv2:", "pxv3:", "cv:"))), "| o so lieu font-tren-anh", sum(1 for c in cells if "+NUM" in c))
print("  AI:", sorted({c for c in cells if c.startswith('AI:')}))
print("  NEED:", sorted({c for c in cells if c.startswith('NEED:')}))
if dup: print("  ⚠ ma lap (hau to b = can anh KHAC cung nguon, chon luc tai):", dup)

# ---------------------------------------------------------------- --fetch
def _thumb(url_thumb, w, want=3840):
    # Commons chi nhan co thumb CHUAN (w.wiki/GHai: ...1280/1920/3840) -> goc to hon 3840 thi lay 3840, con lai lay goc
    return re.sub(r"/(\d+)px-", "/%dpx-" % want, url_thumb.split("?")[0], count=1) if w > want else None

def fetch():
    import requests
    H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
    OUTD = VD / "real_19"; OUTD.mkdir(exist_ok=True)
    J = lambda p: json.loads((VD / p).read_text(encoding="utf-8"))
    SRC = {"cc": J("_cc/candidates_info.json"), "cat": J("_cat/cat_info.json"),
           "px": J("_px/px_info.json"), "pxv": J("_pxv/pxv_info.json"),
           "pxv2": J("_pxv2/pxv2_info.json"), "pxv3": J("_pxv3/pxv3_info.json"), "cv": J("_cv/cv_info.json")}
    p71 = {v["n"]: dict(v, title=k) for k, v in J("_p1971/index.json").items()}
    SRC["era"] = J("_fix_era/era_info.json")
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
            if pre in ("cc", "cat", "era"):
                kind = "photo"; url = _thumb(v["thumb"], v["w"]) or v["url"].split("?")[0]
                lic, who, page = v.get("license"), v.get("artist"), "https://commons.wikimedia.org/wiki/" + v["title"].replace(" ", "_")
            elif pre == "px":
                kind = "photo"; url = v["original"] + "?auto=compress&cs=tinysrgb&w=2560"
                lic, who, page = "Pexels License", v.get("photographer"), v["url"]
            elif pre == "cv":
                kind = "video"; url = v["url"].split("?")[0]
                lic, who, page = v.get("license"), v.get("artist"), "https://commons.wikimedia.org/wiki/" + v["title"].replace(" ", "_")
            else:
                kind = "video"; url = v["file"]
                lic, who, page = "Pexels License", v.get("user"), v["url"]
        ext = ".jpg" if kind == "photo" else ("." + url.rsplit(".", 1)[-1].lower())
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

if "--fetch" in sys.argv:
    sys.exit(fetch())
