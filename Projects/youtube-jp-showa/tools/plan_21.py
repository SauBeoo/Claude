# -*- coding: utf-8 -*-
"""plan_20.py — BANG HINH THEO CAU cho video 21 (khuon v08: hinh THAT la lop chinh, AI chi lap).

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

STEM = "21_umaredoshi-okane"
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / STEM
TTS = ROOT / "03_SCRIPTS" / (STEM + "_TTS.md")
P71 = ROOT / "06_VIDEO" / "19_kaimono-joushiki" / "_p1971" / "index.json"

# (chi so timeline, [o hinh...]) — [] = o truoc KEO DAI qua dong nay
PLAN_T = [
 # ---------- HOOK v3 cam xuc (四十九日の夜 -> 通帳 -> 姉の告白) ----------
 (1,  ["cc:butsudan__04", "cc:butsudan__06"]),   # THAT: phong 仏間 + tay trai anh cu (user 09-29: 30s dau it AI)   # entry 0 = phong 仏間 THAT; o 2 = hai chi em + so (chu the <10s)
 (2,  ["AI:tsucho_pencil+NUM"]),              # so trang, chu 「でんわ」 ve bang FONT viet tay
 (3,  ["pxv:v_oldhands__00"]),                 # THAT: hai ban tay gia siet chat (im lang)                     # CLIP: chi dung tay tren trang so
 (4,  ["AI:ane_confess"]),                    # CLIP: cau thu nhan — 1 khuon mat duy nhat cho chi 74
 (5,  ["p71:95"]),                           # dam dong Tokyo 1971
 (6,  ["p71:287"]),                            # THAT 1971: hai be gai o cua nha (chi em)
 (7,  ["film:f2"]),                            # PHIM THAT 1957: me dat be gai ngay Tet                       # anh chan dung me tren ban tho (AI, khong chu)
 (8,  ["cc:kurodenwa__09+NUM"]),              # THAT: 黒電話 + chu でんわ
 (9,  ["pxv:v_pencil__05"]), (10, ["pxv:v_rain_win__00"]), (11, ["cc:chabudai__09"]),
 # ---------- 1 百円玉は、銀 ----------
 (12, ["cc:coin100_old__00+NUM"]),
 (13, ["film:f1"]), (14, ["film:f7"]),
 (15, ["AI:coin_palm"]),                      # CLIP: me dat dong xu len tay be gai
 (16, ["AI:coin_phoenix_macro"]),
 (17, ["AI:haha_young_speak"]),
 (18, ["px:px_bulb__02", "AI:ane_futon_coin"]),
 (19, ["px:px_coin__00"]),
 (20, ["cc:coin100_old__03+NUM"]),
 (21, ["cc:note100b__02+NUM"]),
 (22, ["cc:coin50__02+NUM"]),
 (23, ["cc:coin50__04+NUM", "cc:coin100_old__06"]),
 (24, []),
 (25, ["AI:far_banknote+NUM"]),              # 聖徳太子 一万円札 — chua co anh PD dung duoc
 (26, ["AI:haha_young_smile"]),
 (27, ["pxv:v_sakura__10"]),
 # ---------- 2 年賀はがき ----------
 (28, ["film:f3+NUM"]),
 (29, ["cc:chabudai__02"]),
 (30, ["cc:imoban__01", "cc:imoban__03"]),
 (31, ["AI:haha_brush"]),
 (32, ["cc:kitte_sheet__00+NUM"]),
 (33, ["cc:suzuri__06"]),
 (34, ["AI:tailor_kyoto"]),                   # tho may 1949 an danh — KHONG mat nguoi that
 (35, []),
 (36, ["film:f4"]),
 (37, ["gt:postal+NUM"]),            # 原典: 郵政博物館 研究紀要 (screenshot)
 (38, ["cc:kitte_sheet__01+NUM"]),
 (39, ["film:f5+NUM"]),
 (40, ["cc:postbox__00"]),
 (41, ["cc:postbox__08+NUM"]),
 (42, ["AI:kids_lottery"]),
 (43, ["p71:509"]),                           # nha mai tranh 1971 = nha ba ngoai o que
 (44, ["AI:haha_genkan_wait"]),
 (45, ["p71:500"]),
 # ---------- 3 ラジオ ----------
 (46, ["AI:radio_wood+NUM"]),
 (47, ["AI:radio_night"]),                    # CLIP: bat radio, ca nha quay lai
 (48, ["pxv:v_bulb__00"]),
 (49, ["AI:radio_back_glow"]),
 (50, ["AI:family_listen"]),
 (51, ["px:px_ledger__04"]),
 (52, ["cc:koukanshu__09"]),
 (53, ["gt:housou+NUM"]),
 (54, ["AI:radio_dial_close+NUM"]),
 (55, ["p71:186+NUM"]),
 (56, ["AI:tv_color_1968+NUM"]),
 (57, ["AI:haha_radio_quiet"]),
 (58, []),
 (59, ["AI:kakeibo_pencil+NUM"]),             # so chi: o 「でんわ」 ve bang FONT
 (60, ["px:px_pencil__02"]),
 (61, ["p71:93", "p71:189", "p71:192"]),                           # CTA — tre con 1971
 # ---------- 4 電話 ----------
 (62, ["cc:akadenwa__06+NUM"]),               # 1955 PD: nguoi goi dien o cua tiem
 (63, ["film:f6"]),
 (64, ["AI:tabakoya_call"]),
 (65, ["AI:haha_run_sandal"]),                # CLIP
 (66, ["cc:akadenwa__01"]),
 (67, ["cc:akadenwa__08"]),
 (68, ["p71:294+NUM"]),
 (69, ["AI:haha_decide"]),
 (70, []),
 (71, ["cc:kurodenwa__00"]),
 (72, ["cc:denchu__01+NUM"]),
 (73, ["cc:koukanshu__04+NUM"]),
 (74, ["gt:ntt+NUM"]),               # 原典: NTT東 databook (東京・単独)
 (75, ["gt:kokkai1966+NUM"]),
 (76, ["cc:koukanshu__01+NUM"]),
 (77, ["p71:510+NUM"]),
 (78, ["cc:akadenwa__02+NUM"]),
 (79, ["AI:haha_count_savings"]),
 (80, ["AI:kurodenwa_lace"]),
 (81, ["p71:499"]),
 (82, ["cc:koukanshu__10"]),
 (83, ["AI:haha_first_call"]),                # CLIP: hai tay cam ong nghe
 (84, []),
 (85, ["AI:tsucho_interest+NUM"]),
 (86, []),
 (87, ["cc:kurodenwa__07"]),
 (88, ["AI:haha_tsucho_drawer"]),
 (89, ["pxv:v_sakura__06"]),
 # ---------- 5 授業料 ----------
 (90, ["p71:96+NUM"]),
 (91, ["p71:314"]),
 (92, ["AI:ane_goukaku"]),                    # CLIP
 (93, ["AI:table_bg_c+NUM"]),
 (94, ["AI:ryo_room"]),
 (95, ["cc:pinkdenwa__06"]),                  # 1965 PD mau
 (96, ["AI:ryo_phone"]),
 (97, ["cc:pinkdenwa__04"]),
 (98, ["p71:517+NUM"]),
 (99, ["cc:pinkdenwa__07"]),
 (100,["gt:kokkai1963+NUM"]),
 (101,["AI:univ_notice+NUM"]),
 (102,[]),
 (103,["gt:kokkai1972"]),
 (104,[]),
 (105,["p71:97"]),
 (106,["AI:lecture_hall"]),
 (107,["AI:table_bg+NUM"]),                   # bang nam nhap hoc -> hoc phi (font)
 (108,[]), (109,[]), (110,["AI:table_bg_b+NUM"]), (111,[]),
 (112,["p71:191"]),
 (113,["AI:yubin_window", "px:px_hanko__05"]),                   # CLIP: me dem tien, dong dau
 (114,["gt:mext+NUM"]),
 (115,["AI:ane_young_photo"]),
 (116,["AI:private_univ+NUM"]),
 (117,["pxv:v_sakura__09+NUM"]),
 (118,["pxv:v_sakura__04"]),
 # ---------- KET ----------
 (119,["AI:siblings_night2"]),
 (120,["AI:tsucho_pages"]),
 (121,["AI:tsucho_rows+NUM"]),
 (122,["AI:tsucho_out1+NUM"]),
 (123,["AI:tsucho_out2+NUM"]),
 (124,["px:px_pencil__09+NUM"]),
 (125,["AI:haha_bond_kept"]),
 (126,["AI:haha_phone_old"]),
 (127,[]),
 (128,["AI:tsucho_first"]),
 (129,["cc:pinkdenwa__09"]),
 (130,["AI:ane_handbag"]),
 (131,["AI:coin_unwrap"]),                    # CLIP: mo goi giay, dong 鳳凰
 (132,["AI:ane_tears"]),
 (133,["AI:coin_on_tsucho"]),                 # CLIP: dat dong xu len so, ngon tay run
 (134,["pxv:v_sakura__03"]),
 (135,["pxv:v_ink__00"]),
 (136,["px:px_oldhands__01"]),
 (137,["AI:ane_smile"]),
 (138,["p71:45"]),
 (139,["cc:chabudai__01"]),
 (140,[]),
 (141,["pxv:v_pencil__09"]), (142,["AI:siblings_back"]), (143,[]),
]

# chu tren o +NUM — (chi so timeline, thu tu o +NUM trong dong) -> cac dong chu. Moi chu PHAI co trong cau doc.
NUMTXT_T = {
    (2, 0):  ["でんわ"],
    (8, 0):  ["でんわ"],
    (12, 0): ["一点目", "百円玉は、銀でできていた"],
    (20, 0): ["昭和32年の百円玉", "銀 6割・4.8グラム"],
    (21, 0): ["それまでの百円は", "板垣退助の、お札"],
    (22, 0): ["昭和34年", "五十円玉に 穴"],
    (23, 0): ["昭和42年", "銅とニッケルの百円玉へ"],
    (25, 0): ["昭和33年の暮れ", "聖徳太子の一万円札"],
    (28, 0): ["二点目", "年賀はがきは、くじつきで、五円"],
    (32, 0): ["はがき 一枚 5円"],
    (37, 0): ["国の審議会", "「食べるものも食べられない時代」"],
    (38, 0): ["お年玉付き郵便はがき等の", "発売に関する法律"],
    (39, 0): ["一枚2円 ＋ 寄付金1円", "特等は 高級ミシン"],
    (41, 0): ["はがき", "昭和26年 5円 → 昭和41年7月 7円"],
    (46, 0): ["三点目", "ラジオを聞くにも、お金を払った"],
    (53, 0): ["昭和25年 放送法", "受信の契約"],
    (54, 0): ["昭和37年4月", "ラジオだけの契約 月50円"],
    (55, 0): ["昭和43年4月", "ラジオだけの契約 廃止"],
    (56, 0): ["カラー契約 月465円"],
    (59, 0): ["でんわ"],
    (62, 0): ["四点目", "電話は、債券を買って、引くもの"],
    (68, 0): ["昭和41年"],
    (72, 0): ["昭和27年", "日本電信電話公社"],
    (73, 0): ["昭和35年", "電信電話設備の拡充のための", "暫定措置に関する法律"],
    (74, 0): ["東京で一本", "設備料 1万円 ＋ 債券 15万円"],
    (75, 0): ["昭和41年の国会", "額面の およそ95%で売れる"],
    (76, 0): ["申し込んでもつかない電話", "昭和45年度末 291万"],
    (77, 0): ["住まいの電話 100世帯あたり", "昭和45年度 28.5"],
    (78, 0): ["昭和58年", "電話の債券 廃止"],
    (85, 0): ["でんわ"],
    (90, 0): ["五点目", "大学の授業料は、入学した年で決まった"],
    (93, 0): ["昭和45年 大学の学部に進んだ人", "女子 6.5%・男子 27.2%"],
    (98, 0): ["姉の授業料", "1年 12,000円"],
    (100, 0): ["国立大学の授業料", "昭和38年 12,000円"],
    (101, 0): ["昭和47年", "月1,000円 → 月3,000円"],
    (107, 0): ["入学した年の授業料", "〜昭和46年 12,000円", "昭和47〜50年 36,000円"],
    (110, 0): ["昭和51・52年 96,000円", "昭和53年 144,000円"],
    (114, 0): ["96,000円", "姉の 8倍"],
    (116, 0): ["昭和51年 私立大学の平均", "221,844円"],
    (117, 0): ["今の国立大学 標準の額", "535,800円"],
    (121, 0): ["でんわ"],
    (122, 0): ["昭和46年 春"],
    (123, 0): ["昭和52年 春"],
    (124, 0): ["利子 年7分2厘", "はじめの年 10,800円"],
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
    man = json.loads((VD / "real_21" / "MANIFEST.json").read_text(encoding="utf-8"))
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
    OUTD = VD / "real_21"; OUTD.mkdir(exist_ok=True)
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
            if code not in man: bad.append(code); print("LOI thieu the 原典 — chay make_genten_21.py", code)
            else: print("OK  %-28s photo (the 原典 da dung)" % code)
            continue
        if pre == "film":
            fn = "film_%s.mp4" % key
            if not (OUTD / fn).exists(): bad.append(code); print("LOI thieu phim da cat", fn); continue
            man[code] = {"file": fn, "kind": "video", "license": "Public domain (US federal work)", "author": "US Navy / NARA 428-npc-521",
                         "page": "https://archive.org/details/428-npc-521#%s" % key, "url": ""}
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
