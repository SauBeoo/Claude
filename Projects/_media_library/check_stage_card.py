#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""GATE NỘI DUNG THẺ SÂN KHẤU (T1–T10) — chạy TRƯỚC mọi lượt render.

    python check_stage_card.py <SLIDES.json> [--channel nenkin] [--soft]

🔴 VÌ SAO CÓ FILE NÀY. `check_zu_layout.py` đo **bố cục** (13 lớp hình học) và nó rất tốt ở
việc đó — nhưng nó **không đo được thẻ có CHỞ NGHĨA hay không**. Số đã đo trên chính kênh
nenkin: video 09 có **20/28 thẻ là `check`** (gạch đầu dòng + icon trang trí), video 16 có
**35/58 thẻ không có hình**. Cả hai lượt đó `check_zu_layout` sạch. Đó là bệnh "thẻ trơ chữ"
mà user kết án, và nó đã đẩy kênh đi vòng: thẻ chữ → bỏ hẳn sang footage AI người thật (73%
thời lượng "vô nghĩa") → nay quay lại thẻ, nhưng là **thẻ SƠ ĐỒ**.

Ba kênh thắng đo trực tiếp trên file (カメ先生 101K · フクロウ 1,63M · お金の保健室 190K):
giữa khung luôn là **một sơ đồ chở con số** (bar 24% · timeline 60→80 · 13 ô tô vàng 4 ·
mũi tên + ✗ đỏ), không phải danh sách gạch đầu dòng. Che chữ đi vẫn hiểu; thẻ `check` che chữ
đi thì còn 4 dấu ✓.

⚖️ Gate này đo NỘI DUNG nên nó chủ quan hơn gate hình học — vì thế mỗi ngưỡng đều ghi kèm
số đo mà nó đến từ đâu. Muốn nới thì nới có căn cứ, đừng nới cho vừa bài mình.

Exit 0 = sạch · 1 = có lỗi (dùng `--soft` để chỉ in cảnh báo, không chặn).
"""
import io
import re
import sys
import json
import argparse
import collections
from pathlib import Path

# 🔴 audience-45plus §2.0h: gate CRASH thì builder báo "GATE ĐỎ" trên project SẠCH —
# nguy hiểm hơn gate im lặng, vì nó dụ người ta đi sửa NỘI DUNG cho lỗi nằm ở CÔNG CỤ.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── ngưỡng, kèm nguồn của từng con số ────────────────────────────────────────────
CHECK_MAX = 0.25    # T2 — nenkin v09 đo 20/28 = 71% thẻ `check`; trần 25% ép về sơ đồ
DIAG_MIN = 0.50     # T3 — カメ/保健室: 100% thẻ giữa khung là sơ đồ; 50% là mức đã nới rộng
BODY_MAX = 60       # T4 — chữ thân thẻ; quá đây là đang viết đoạn văn lên thẻ
NODE_LINES = 2      # T4 — node zu tối đa 2 dòng (make_stage 1.3 mới cho 2 dòng)
HEAD_MAX = 18       # T5 — headline; カメ đo được 8–16 ký, フクロウ 6–14
KW_MAX = 1          # T5 — mỗi thẻ tối đa 1 cụm 《》 đỏ; nhấn hết = không còn gì nhấn
PROPS_MAX = 2       # T9 — props/thẻ
POSE_MIN = 6        # T10 — số tư thế khác nhau tối thiểu mỗi bên
PAIR_MAX = 3        # T10 — một cặp (trái,phải) lặp tối đa 3 thẻ
GENTEN_MIN = 2      # ≥2 thẻ 原典/video (skill script-nenkin GĐ0d)

# ── T11: TRẦN CHỮ/HÀNG THEO LAYOUT ─────────────────────────────────────────────
# 🔴 Bảng này đã nằm trong `audience-45plus.md` §2.1 từ 2026-08-12 **mà chưa có gate nào
# thi hành** — nên nó trôi. Đo lại bằng mắt 2026-09-06: thẻ `compare` 4 hàng có hàng thứ 4
# bắt đầu ở y=830 và **tràn khỏi đáy card 902**, `src` đè lên nó. Không renderer nào báo lỗi.
# Cơ chế: `fit()`/`fit_ml()` co chữ CÓ SÀN font; quá sàn thì nó TRÀN chứ không co thêm.
#   (bề rộng khả dụng ÷ cỡ sàn = trần ký tự; chữ full-width ≈ 1 ô font)
ROWS_MAX = {"compare": 3}                 # hàng 4 vượt đáy card — hình học, không phải style
CHARS_MAX = {"check": 24, "compare": 32, "steps": 22, "source": 23}
NOWRAP = {"steps"}                        # vẽ bằng tw() MỘT DÒNG ⇒ cấm ký tự xuống dòng

# layout được tính là "sơ đồ chở số"
DIAG = {"zu", "bars", "timeline", "compare"}
# layout chở số nhưng KHÔNG phải sơ đồ (vẫn hợp lệ cho T1, không tính vào T3)
NUMISH = {"big", "art", "pict"}
FLAT = {"check", "steps", "source", "flow", "tree"}

NUM_RE = re.compile(r"[0-9０-９]|[一二三四五六七八九十百千万億]{1,}(?=[万円年日歳％パ])|[円万％]")
KW_RE = re.compile(r"《[^》]*》")
# tư thế 聞き手 mang phản ứng (T10) — thẻ có số hero mà người nghe vẫn "listen" là chết trân
REACT = ("surprised", "worried", "think", "shock", "down")


def txt_fields(st):
    """Mọi chuỗi người xem ĐỌC ĐƯỢC trên thẻ (không gồm tên file ảnh/icon)."""
    out = []

    def walk(v, key=None):
        if isinstance(v, str):
            if key not in ("img", "bgimg", "fill", "icon", "left", "right", "layout",
                           "kind", "at", "from", "src", "ph", "name"):
                out.append(v)
        elif isinstance(v, dict):
            for k, vv in v.items():
                walk(vv, k)
        elif isinstance(v, (list, tuple)):
            for vv in v:
                walk(vv, key)

    for k, v in st.items():
        if k in ("title", "sub", "cap"):
            continue
        walk(v, k)
    return out


def has_num(st):
    j = json.dumps(st, ensure_ascii=False)
    return bool(NUM_RE.search(j))


def check(ss, soft=False, demo=False):
    bad = collections.defaultdict(list)
    warn = collections.defaultdict(list)
    cards = [(i, c["stage"]) for i, c in enumerate(ss) if c.get("stage")]
    n = len(cards)
    if not n:
        return bad, warn, 0, {}

    lay = collections.Counter(st.get("layout", "check") for _, st in cards)
    pairs = collections.Counter()
    poses = {"left": set(), "right": set()}
    genten = 0

    for i, st in cards:
        L = st.get("layout", "check")
        tag = f"[{i:02d}] {L:9s}"

        # ── T1: mỗi thẻ đúng MỘT thứ chở nghĩa ở giữa khung ────────────────────
        carries = (L in DIAG) or (L in NUMISH) or bool(st.get("pins")) or bool(st.get("pins_card"))
        if not carries and has_num(st):
            bad[i].append(f"{tag} T1 thẻ có SỐ mà giữa khung không có gì chở nó "
                          f"(layout {L} + không pin) — đổi sang zu/bars/timeline/compare, "
                          f"hoặc gắn pin `num`")

        # ── T4: chữ thân thẻ ───────────────────────────────────────────────────
        for s in txt_fields(st):
            if len(s) > BODY_MAX:
                bad[i].append(f"{tag} T4 chữ thân thẻ {len(s)} ký > {BODY_MAX}: 「{s[:34]}…」")
            if s.count("\n") + 1 > NODE_LINES:
                bad[i].append(f"{tag} T4 khối chữ {s.count(chr(10))+1} dòng > {NODE_LINES}")

        # ── T5: headline ───────────────────────────────────────────────────────
        ti = st.get("title", "")
        plain_ti = KW_RE.sub(lambda m: m.group(0)[1:-1], ti)
        if len(plain_ti) > HEAD_MAX:
            bad[i].append(f"{tag} T5 headline {len(plain_ti)} ký > {HEAD_MAX}: 「{ti}」")
        nkw = len(KW_RE.findall(json.dumps(st, ensure_ascii=False)))
        if nkw > KW_MAX:
            bad[i].append(f"{tag} T5 có {nkw} cụm 《》 > {KW_MAX} — nhấn hết là không nhấn gì")

        # ── T6: thẻ có số ⇒ phải ghi nguồn ─────────────────────────────────────
        if has_num(st) and not st.get("src"):
            (warn if soft else bad)[i].append(
                f"{tag} T6 thẻ có SỐ mà thiếu `src` (dòng nguồn đáy-phải) — "
                f"YMYL tiền: nguồn hiện trên màn là thứ lời nói không mua được")

        # ── T11: trần hàng/ký tự theo layout (audience-45plus §2.1) ────────────
        if L in ROWS_MAX and len(st.get("rows") or []) > ROWS_MAX[L]:
            bad[i].append(f"{tag} T11 `{L}` có {len(st['rows'])} hàng > {ROWS_MAX[L]} — "
                          f"hàng thứ {ROWS_MAX[L]+1} bắt đầu ở y=830 và TRÀN khỏi đáy card "
                          f"902 (audience-45plus §2.1). Chẻ thẻ, đừng bóp cỡ chữ")
        cmax = CHARS_MAX.get(L)
        if cmax:
            for r in (st.get("rows") or []):
                if isinstance(r, str) and len(r) > cmax:
                    bad[i].append(f"{tag} T11 hàng {len(r)} ký > {cmax} (sàn font của `{L}`) "
                                  f"— quá sàn thì fit() TRÀN chứ không co thêm: 「{r[:26]}…」")
            for key in ("ok", "no"):
                for r in (st.get(key) or []):
                    if isinstance(r, str) and len(r) > cmax:
                        bad[i].append(f"{tag} T11 `{key}` {len(r)} ký > {cmax}: 「{r[:26]}…」")
        if L in NOWRAP:
            for r in (list(st.get("rows") or []) + list(st.get("steps") or [])):
                if isinstance(r, str) and (chr(10) in r):
                    bad[i].append(f"{tag} T11 `{L}` vẽ MỘT DÒNG ⇒ cấm ký tự xuống dòng")

        # ── T9: props phải neo vào lời ─────────────────────────────────────────
        props = list(st.get("props") or []) + list(st.get("props_top") or [])
        if len(props) > PROPS_MAX:
            bad[i].append(f"{tag} T9 {len(props)} props > {PROPS_MAX} — đồ rời nhiều là "
                          f"trang trí, đúng thứ gate ① 'đồ mồ côi' đã kết án")
        for pr in props:
            if isinstance(pr, dict) and pr.get("t0") is None and not pr.get("ph"):
                bad[i].append(f"{tag} T9 props không có `t0`/`ph` — không neo vào lời "
                              f"thì không được đếm là sự kiện hình")

        # ── T10: cast ──────────────────────────────────────────────────────────
        lft = st.get("left") or ""
        rgt = st.get("right") or ""
        cb = st.get("cast_beats") or {}
        poses["left"].add(lft)
        poses["right"].add(rgt)
        for side in ("left", "right"):
            for b in (cb.get(side) or []):
                poses[side].add(b[1] if isinstance(b, (list, tuple)) else b["name"])
        pairs[(lft, rgt)] += 1
        hero = any(isinstance(p, dict) and p.get("kind") in ("num", "badge")
                   for p in (list(st.get("pins") or []) + list(st.get("pins_card") or []))) \
            or bool(st.get("pop"))
        if hero:
            reacts = [rgt] + [(b[1] if isinstance(b, (list, tuple)) else b["name"])
                              for b in (cb.get("right") or [])]
            if not any(any(k in r for k in REACT) for r in reacts):
                (warn if soft else bad)[i].append(
                    f"{tag} T10 thẻ có SỐ HERO mà 聞き手 vẫn '{rgt}' — cho nó "
                    f"surprised/worried, nếu không người nghe đứng chết trân đúng lúc đắt nhất")

        # ── 原典 ────────────────────────────────────────────────────────────────
        pins = list(st.get("pins") or [])
        kinds = {p.get("kind") for p in pins if isinstance(p, dict)}
        if L == "art" and ("frame" in kinds or "circle" in kinds):
            genten += 1
            if "quote" not in kinds:
                bad[i].append(f"{tag} 原典 có khoanh mà THIẾU pin `quote` — chữ web trong "
                              f"ảnh chụp quá nhỏ cho tệp 65+ trên điện thoại; フクロウ 1,63M "
                              f"luôn kèm trích nguyên văn do FONT vẽ")
            if not st.get("src"):
                bad[i].append(f"{tag} 原典 thiếu `src`")

    # ── ngưỡng CẢ VIDEO ────────────────────────────────────────────────────────
    tot = {}
    ncheck = lay.get("check", 0)
    ndiag = sum(lay.get(k, 0) for k in DIAG)
    tot["check"] = (ncheck, ncheck / n)
    tot["diag"] = (ndiag, ndiag / n)
    tot["genten"] = genten
    if ncheck / n > CHECK_MAX:
        bad[-1].append(f"T2 `check` {ncheck}/{n} = {ncheck/n*100:.0f}% > {CHECK_MAX*100:.0f}% "
                       f"— đây đúng là bệnh 'trơ chữ' (v09 đo 20/28)")
    if ndiag / n < DIAG_MIN:
        bad[-1].append(f"T3 sơ đồ (zu/bars/timeline/compare) {ndiag}/{n} = {ndiag/n*100:.0f}% "
                       f"< {DIAG_MIN*100:.0f}%")
    # ⛔ Từ đây là ngưỡng CẤP VIDEO — áp lên một đoạn demo 60–90s là báo oan:
    #    một clip 53s không thể chứa 2 thẻ 原典, và 5 thẻ không thể dùng hết 6 tư thế.
    #    Không hạ ngưỡng (video thật vẫn phải đạt) — chỉ THU HẸP PHẠM VI bằng `--demo`.
    if demo:
        return bad, warn, n, tot
    if genten < GENTEN_MIN:
        bad[-1].append(f"原典 chỉ {genten} thẻ < {GENTEN_MIN}")
    for side in ("left", "right"):
        if len(poses[side]) < POSE_MIN:
            (warn if soft else bad)[-1].append(
                f"T10 bên {side} chỉ {len(poses[side])} tư thế < {POSE_MIN} — "
                f"'có 12 tư thế mà dán MỘT CẶP cố định thì cũng như có 1 ảnh'")
    for (l, r), c in pairs.items():
        if c > PAIR_MAX:
            (warn if soft else bad)[-1].append(
                f"T10 cặp ({l},{r}) lặp {c} thẻ > {PAIR_MAX}")
    return bad, warn, n, tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides")
    ap.add_argument("--channel", default="nenkin")
    ap.add_argument("--soft", action="store_true", help="chỉ cảnh báo, không chặn")
    ap.add_argument("--demo", action="store_true",
                    help="đoạn demo 60–90s: bỏ ngưỡng CẤP VIDEO (原典 ≥2 · ≥6 tư thế/bên), "
                         "giữ nguyên mọi luật cấp THẺ")
    a = ap.parse_args()
    d = json.load(io.open(a.slides, encoding="utf-8"))
    ss = d["slides"] if isinstance(d, dict) else d
    bad, warn, n, tot = check(ss, a.soft, a.demo)

    print(f"── GATE THẺ SÂN KHẤU (T1–T10) — {n} thẻ"
          + ("  [DEMO: bỏ ngưỡng cấp video]" if a.demo else "") + " ──")
    if tot:
        print(f"   sơ đồ {tot['diag'][0]}/{n} ({tot['diag'][1]*100:.0f}%, cần ≥{DIAG_MIN*100:.0f})"
              f" · check {tot['check'][0]}/{n} ({tot['check'][1]*100:.0f}%, trần {CHECK_MAX*100:.0f})"
              f" · 原典 {tot['genten']} (cần ≥{GENTEN_MIN})")
    for k in sorted(warn):
        for m in warn[k]:
            print(f"  ⚠️  {m}")
    for k in sorted(bad):
        for m in bad[k]:
            print(f"  🔴 {m}")
    if bad:
        print(f"\n🔴 {sum(len(v) for v in bad.values())} lỗi — SỬA XONG MỚI RENDER")
        sys.exit(1)
    print("✅ SẠCH — thẻ chở nghĩa, được render")


if __name__ == "__main__":
    main()
