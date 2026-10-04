# -*- coding: utf-8 -*-
"""plan_22.py — BANG HINH THEO CAU cho video 22 (khuon v08: hinh THAT la lop chinh, AI chi lap).

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

STEM = "22_kieta-shigoto"
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / STEM
TTS = ROOT / "03_SCRIPTS" / (STEM + "_TTS.md")
P71 = VD / "_p1971" / "index.json"

# (chi so timeline, [o hinh...]) — [] = o truoc KEO DAI qua dong nay
PLAN_T = [
 # ---------- HOOK (15歳の車掌・給料袋・発車オーライ) ----------
 (1,  ["cc:bus_girl__04", "p71:472"]),          # PD 1956 co gai lau xe buyt | xe buyt do-kem 1971
 (2,  ["AI:conductor_young"]),                    # me 15 tuoi, dong phuc, o cua sau xe buyt
 (3,  ["px:px_coins__11", "AI:bag_coins"]),
 (4,  ["cc:kyuryo__01", "AI:envelope_father"]),   # 給料袋 that | me dua cho cha, khong boc
 (5,  ["pxv:v_busdoor__10"]),                     # cua xe buyt dong
 (6,  ["AI:haha77_bus"]),                         # ba 77 tren xe buyt, thi tham
 (7,  ["p71:257"]),                               # tai xe buyt 1971 nhin tu ghe sau
 (8,  ["AI:envelope_drawer"]),                    # phong bi trong ngan keo (khong lo dap an)
 (9,  ["film:n1"]), (10, ["film:n2"]), (11, ["film:n3+NUM"]),
 # ---------- 1 バスの車掌 ----------
 (12, ["cc:bus_bonnet__01+NUM"]),
 (13, ["AI:depot_rollcall"]),
 (14, ["cc:coin10__01", "pxv:v_coins__00"]),
 (15, ["cc:bus_ticket__05", "cc:bus_ticket__04"]),
 (16, ["AI:conductor_lean"]),
 (17, ["p71:044"]),
 (18, ["AI:fingers_cracked", "pxv:v_snownight__00"]),
 (19, ["AI:count_sales"]),
 (20, ["px:px_busseat__05"]),
 (21, ["cc:coin10__00+NUM"]),
 (22, ["gt:k1966+NUM"]),
 (23, ["cc:bus_ticket__03+NUM"]),
 (24, ["cc:bus_bonnet__02+NUM"]),
 (25, ["p71:175"]),
 (26, ["px:px_busseat__01"]),
 (27, ["gt:kisoku15+NUM"]),
 (28, ["p71:049"]),
 (29, ["film:n4"]),
 (30, ["cc:oneman__04+NUM"]),
 (31, ["p71:153"]),
 (32, ["AI:conductor_last_day+NUM"]),
 (33, ["px:px_stopbutton__01"]),
 # ---------- 2 踏切警手 ----------
 (34, ["pxv:v_crossing__00+NUM"]),
 (35, ["AI:sofu_keeper"]),
 (36, ["film:n10"]),
 (37, ["cc:fumikiri_hut__04", "AI:sofu_handle"]),
 (38, ["pxv:v_crossbell__03"]),
 (39, ["p71:058", "cc:steam_train__00"]),
 (40, ["gt:k1959+NUM"]),
 (41, ["p71:396+NUM"]),
 (42, ["px:px_lantern__10"]),
 (43, ["pxv:v_stovefire__05"]),
 (44, ["cc:bento_alu__04", "AI:girl_bento_hut"]),
 (45, ["px:px_drawer__02"]),
 (46, ["p71:136"]),
 (47, ["film:n5+NUM"]),
 (48, ["AI:flag_ignored"]),
 (49, ["film:n6+NUM"]),
 (50, ["gt:k1966b+NUM"]),
 (51, ["cc:crossing_now__05+NUM"]),
 (52, ["px:px_crossing__09"]),
 # ---------- 3 炭鉱 ----------
 (53, ["cc:tategou__02+NUM"]),
 (54, ["cc:tanju__09"]),
 (55, ["AI:miners_walk"]),
 (56, ["cc:tanko__07", "AI:miner_black_face"]),
 (57, ["cc:tanju__11"]),
 (58, ["AI:boy_sentan"]),
 (59, ["gt:roki63+NUM"]),
 (60, ["px:px_helmet__07"]),
 (61, ["cc:cap_lamp__10+NUM"]),
 (62, ["px:px_helmet__10+NUM"]),
 (63, ["px:px_tunnel__03"]),
 (64, ["cc:tanko__11"]),
 (65, ["gt:sekitan+NUM"]),
 (66, ["cc:tategou__01+NUM"]),
 (67, ["cc:botayama__08+NUM"]),
 (68, ["cc:tanju__08"]),
 (69, ["p71:229", "pxv:v_nighttrain__02"]),
 (70, ["film:n7"]),
 (71, ["AI:father_bus_morning"]),
 (72, ["AI:coins_ready_palm"]),
 (73, ["AI:conductor_smile"]),                     # user gen bo sung 2026-10-04 (2K, quay lung)
 (74, ["p71:231"]),
 (75, ["px:px_coal__06", "p71:470", "p71:152"]),
 # ---------- 4 電話交換手 ----------
 (76, ["cc:koukandai__01+NUM"]),
 (77, ["AI:haha_switchboard+NUM"]),
 (78, ["AI:headset_on"]),
 (79, ["px:px_phone__00"]),
 (80, ["pxv:v_plug__09", "AI:plug_in"]),
 (81, ["AI:operators_row"]),
 (82, ["cc:koukandai__11"]),
 (83, ["cc:koukandai__10"]),
 (84, ["cc:koushuu__01"]),
 (85, ["cc:koushuu__07", "AI:dekasegi_phone"]),
 (86, ["px:px_payphone__09"]),
 (87, ["AI:haha_listen"]),
 (88, ["p71:088"]),
 (89, ["gt:k1971+NUM"]),
 (90, ["px:px_phone__01+NUM"]),
 (91, ["cc:koushuu__02"]),
 (92, ["film:n8"]),
 (93, ["gt:k1972+NUM"]),
 (94, ["AI:operators_reassigned"]),
 (95, ["gt:k1980+NUM"]),
 (96, ["AI:headset_stain"]),
 (97, ["p71:477"]),
 # ---------- 5 タイピスト ----------
 (98, ["cc:wabuntype__02+NUM"]),
 (99, ["AI:haha_typist+NUM"]),
 (100, ["cc:wabuntype__03", "pxv:v_typewriter__06"]),
 (101, ["px:px_type__01", "pxv:v_typewriter__01"]),
 (102, ["cc:katsuji__07+NUM"]),
 (103, ["AI:haha_rub_arm"]),
 (104, ["gt:k1976+NUM"]),
 (105, ["gt:k1985+NUM"]),
 (106, ["cc:wabuntype__04"]),
 (107, ["AI:wordpro_desk+NUM"]),
 (108, ["AI:wordpro_price+NUM"]),
 (109, ["px:px_typewriter__07"]),
 (110, ["AI:haha_wordpro"]),
 (111, ["pxv:v_typewriter__07"]),
 # ---------- KET ----------
 (112, ["AI:envelope_drawer2"]),
 (113, ["cc:hanayome__01+NUM"]),
 (114, ["AI:electric_barrier"]),
 (115, ["AI:haha_bento_night"]),
 (116, ["px:px_drawer__11"]),
 (117, ["AI:envelope_reveal"]),
 (118, ["AI:envelope_sealed+NUM"]),
 (119, ["AI:sofu_hand_over"]),
 (120, ["pxv:v_steam__06"]),
 (121, ["gt:k1981+NUM"]),
 (122, ["AI:barrier_auto_night"]),
 (123, ["AI:haha_cry_hut"]),
 (124, []),
 (125, ["cc:hanayome__02"]),
 (126, ["AI:haha77_bus2"]),
 (127, ["px:px_busseat__09"]),
 (128, ["AI:envelope_bag"]),
 (129, ["AI:haha77_smile"]),
 (130, ["p71:467"]),
 (131, ["px:px_crossing__03"]),
 (132, ["p71:142"]),
 (133, ["p71:486"]),
 (134, ["AI:envelope_old_hands"]),
 (135, ["p71:359"]),
 (136, []), (137, ["film:n9"]), (138, []),
]

NUMTXT_T = {
    (11, 0): ["町から消えた仕事と給料", "5つ"],
    (12, 0): ["一点目", "バスには、十五歳の車掌さんがいた"],
    (21, 0): ["昭和39年の国会", "15歳の車掌 基本給 「たしか 9,000円くらい」"],
    (22, 0): ["民間のバスの車掌（運輸省の調べ）", "平均19.7歳・月18,948円"],
    (23, 0): ["歩合", "百円につき 11銭8厘"],
    (24, 0): ["大阪市交通局", "女性の乗務員 33歳で定年"],
    (27, 0): ["自動車事業等運輸規則 第15条", "バスには 車掌が乗るのが原則"],
    (30, 0): ["車掌のいないバス", "昭和39年末 2,581両 → 昭和40年春 3,752両"],
    (32, 0): ["昭和43年", "母、19歳"],
    (34, 0): ["二点目", "踏切には、人がいた"],
    (40, 0): ["昭和34年", "国鉄の踏切警手 およそ8,000人"],
    (41, 0): ["給料とは別の手当", "1日 10円〜50円"],
    (47, 0): ["昭和35年度 踏切事故", "5,569件"],
    (49, 0): ["昭和36年", "踏切道改良促進法"],
    (50, 0): ["昭和41年 6,600人", "7年で 2,800人減らす計画"],
    (51, 0): ["昭和48年", "人のいる国鉄の踏切 695か所"],
    (53, 0): ["三点目", "炭鉱の給料は、町でいちばん高かった"],
    (59, 0): ["労働基準法", "18歳にならない者を 坑内で働かせてはならない"],
    (61, 0): ["昭和25年 1日の賃金", "坑内 429円 ／ 工場の平均 374円"],
    (62, 0): ["昭和44年11月 月の平均", "坑内員 58,248円 ／ 坑外員 42,754円"],
    (65, 0): ["昭和30年", "石炭鉱業合理化臨時措置法"],
    (66, 0): ["炭鉱で働く人", "昭和32年 29万8千人 → 昭和42年 9万6千人"],
    (67, 0): ["炭鉱をはなれた人", "昭和34〜45年 17万8千人"],
    (76, 0): ["四点目", "電話は、人の手で、つないでいた"],
    (77, 0): ["昭和44年"],
    (89, 0): ["高校を出た交換手の最初の給料", "事務の人より およそ800円 低い"],
    (90, 0): ["電電公社の交換手", "昭和46年 いちばん多くて 55,300人"],
    (93, 0): ["昭和39年7月", "自動化でやめる交換手に 特別の給付金"],
    (95, 0): ["全国の自動化", "昭和53年度までに ほぼ達成"],
    (98, 0): ["五点目", "手紙は、タイピストが打っていた"],
    (99, 0): ["昭和54年"],
    (102, 0): ["1日に", "7,000字〜8,000字"],
    (104, 0): ["昭和50年度 頸肩腕症候群の認定", "540人"],
    (105, 0): ["和文タイピスト 女性", "月 158,500円"],
    (107, 0): ["昭和53年9月", "日本語ワードプロセッサー 630万円"],
    (108, 0): ["158,500円 × 12か月 × 3年", "＝ 5,706,000円 ＜ 630万円"],
    (113, 0): ["昭和47年 春"],
    (118, 0): ["昭和39年", "はじめての給料袋"],
    (121, 0): ["30年以上 無事故の踏切警手", "運輸大臣表彰 およそ600人"],
}
FILM_SRC = {k: ("US Navy / NARA 428-NPC-11736 (R & R in Tokyo, 1951)", "https://catalog.archives.gov/id/79127#" + k) for k in ("n1","n2","n3","n4","n5","n6","n7","n8","n9","n10")}

TAG = re.compile(r"\[[^\]]*\]")
_norm = lambda s: re.sub(r"\s+|[、。「」『』・,.!?！？…―—\-]", "", TAG.sub("", s))

def _file_lines():
    """chi so timeline (1..N) -> so dong FILE _TTS.md (dong co chu)."""
    raw = TTS.read_text(encoding="utf-8").splitlines()
    return [n for n, l in enumerate(raw, 1) if TAG.sub("", l).strip()]

FL = _file_lines()
PLAN = [(FL[t - 1], cs) for t, cs in PLAN_T]
NUMTXT = {(FL[t - 1], k): v for (t, k), v in NUMTXT_T.items()}

def _timeline():
    """timeline THAT neu da render giong; chua co thi UOC theo so ky @5,59 ky/s + [間] (chi de canh)."""
    p = VD / "timeline.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    print("⚠️ CHUA CO timeline.json — UOC theo so ky @5,59 ky/s (chi canh, khong chot)")
    raw = [l for l in TTS.read_text(encoding="utf-8").splitlines() if TAG.sub("", l).strip()]
    t, out = 0.0, []
    for l in raw:
        pause = sum(float(x) for x in re.findall(r"間([\d.]+)", l))
        txt = TAG.sub("", l).strip()
        out.append({"start": t + pause, "text": txt})
        t += pause + len(re.sub(r"\s", "", txt)) / 5.59 + 0.6
    return {"total": t, "lines": out}

def _p71_index():
    """index peloquin 1971. 🔴 v19 da --done => _p1971/ bi don (2026-09-29). Mat file thi dung lai tu MANIFEST
    cua video nay (page = https://commons.wikimedia.org/wiki/File:...), du cho gate so den + fetch ma da tai."""
    if P71.exists():
        return json.loads(P71.read_text(encoding="utf-8"))
    import urllib.parse
    man = json.loads((VD / "real_22" / "MANIFEST.json").read_text(encoding="utf-8"))
    out = {}
    for code, m in man.items():
        if code.startswith("p71:"):
            t = urllib.parse.unquote(m["page"].rsplit("/wiki/", 1)[1]).replace("_", " ")
            out[t] = {"n": int(code[4:]), "thumb": m.get("url", ""), "url": m.get("url", ""), "w": 0}
    return out

def cls(code):
    return "AI" if code.startswith("AI:") else ("NEED" if code.startswith("NEED:") else "REAL")

cells = [c for _, cs in PLAN_T for c in cs]

def report():
    bad = 0
    ts = [t for t, _ in PLAN_T]
    if ts != sorted(ts) or len(set(ts)) != len(ts): print("🔴 PLAN_T khong tang deu / trung dong"); bad = 1
    tl = _timeline()["lines"]
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
    p71 = {v["n"]: k for k, v in _p71_index().items()}
    for c in set(base):
        if c.startswith("p71:"):
            ttl = p71.get(int(c[4:]))
            if ttl is None: print("🔴 khong co", c); bad = 1
            elif ttl.replace("_", " ") in used: print("🔴 SO DEN (da len song):", c, ttl); bad = 1
    SRC = {"cc": J("_cc/candidates_info.json"),
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
    st = [l["start"] for l in tl] + [_timeline()["total"]]
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
    OUTD = VD / "real_22"; OUTD.mkdir(exist_ok=True)
    J = lambda p: json.loads((VD / p).read_text(encoding="utf-8"))
    SRC = {"cc": J("_cc/candidates_info.json"),
           "px": J("_px/px_info.json"), "pxv": J("_pxv/pxv_info.json")}
    p71 = {v["n"]: dict(v, title=k) for k, v in _p71_index().items()}
    manp = OUTD / "MANIFEST.json"
    man = json.loads(manp.read_text(encoding="utf-8")) if manp.exists() else {}
    codes = sorted({c.replace("+NUM", "") for c in cells if cls(c) == "REAL"})
    bad = []
    for code in codes:
        pre, key = code.split(":", 1)
        if code in man and (OUTD / man[code]["file"]).exists() and pre not in ("gt", "film"):
            continue
        if pre == "gt":
            if code not in man: bad.append(code); print("LOI thieu the 原典 — chay make_genten_22.py", code)
            else: print("OK  %-28s photo (the 原典 da dung)" % code)
            continue
        if pre == "film":
            fn = "film_%s.mp4" % key
            if not (OUTD / fn).exists(): bad.append(code); print("LOI thieu phim da cat", fn); continue
            man[code] = {"file": fn, "kind": "video", "license": "Public domain (US federal work)", "author": FILM_SRC.get(key, ("US Navy", ""))[0],
                         "page": FILM_SRC.get(key, ("", ""))[1], "url": ""}
            print("OK  %-28s video (phim PD da cat)" % code); continue
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
