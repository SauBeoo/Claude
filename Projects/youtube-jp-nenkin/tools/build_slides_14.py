# -*- coding: utf-8 -*-
"""build_slides_14.py — sinh `14_..._SLIDES.json` cho video 14 (住民税非課税の「線」).

VÌ SAO CÓ TOOL NÀY: xem `build_slides_11.py` / `build_slides_13.py`. Bản 14 chép nguyên
5 khuôn helper của 13 (`spine` `cols3` `slots` `two_ways` `chain` `one_to_n` `polish`) —
luật `CLAUDE.md` §VISUAL: *"video sau COPY 4 hàm này, đừng dựng lại từ node thô"*.

⭐ TRỤC HÌNH CỦA VIDEO NÀY: **一本の線** (một đường kẻ).
Video 13 lấy trục là "một con số bị viết lại 4 lần" (`spine` ×8). Bài này lấy trục là
**một đường kẻ có hai phía**: mọi thứ trong bài đều là "ở phía nào của vạch".
⇒ Khuôn mới `line()` = [内側] ─ ‖số của vạch‖ ─ [外側] + dải chốt đáy, dùng **8 lần**:
線とは → 3本ある → 中村の147/150 → 姉との2本 → 5千円の線 → 段階の線 → 資格の線 → 夫婦の線.
Đổi layout mấy thẻ đó là phá xương sống thị giác của bài.

🔴 `line()` KHÔNG vẽ đường kẻ bằng edge. Lý do đo được: `_zu_trim` cắt mũi tên theo hộp bao
hai đầu, nên một edge nằm GIỮA hai hộp chữ sẽ teo còn ~40px (gate mũi-tên-lép bắt). Vạch được
mã hoá bằng **node hero ở giữa** — nó chính là con số, và con số chính là vạch.

CHẠY:  python tools/build_slides_14.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, r"E:\Claude\Projects\_media_library")
from make_stage import zu_check as _zu_check      # noqa: E402
from make_stage import zu_row as ROW              # noqa: E402
from make_stage import icon_path as _icon_path    # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STEM = "14_juminzei-hikazei-sakaime-148man"
TTS = PROJ / "03_SCRIPTS" / f"{STEM}_TTS.md"
OUT = PROJ / "03_SCRIPTS" / f"{STEM}_SLIDES.json"

NL = "\n"
CH_PER_SEC, GAP_LINE, GAP_PARA = 5.72, 0.45, 1.0
MIN_SEC = 6.0


def C(match, layout, **kw):
    return {"match": match, "video": True, "stage": dict(layout=layout, **kw)}


def N(id_, kind, at, **kw):
    return dict(id=id_, kind=kind, at=at, **kw)


def E(a, b, style="arrow", **kw):
    return dict({"from": a, "to": b, "style": style}, **kw)


# ══════════════════════════════════════════════════════════════════════════════
# ⭐ KHUÔN TRỤC CỦA BÀI: 一本の線
# ══════════════════════════════════════════════════════════════════════════════
def line(match, title, sen, uchi, soto, close, why, uchi_dim=False, soto_dim=False,
         left="sensei_explain", right="kikite_think", sub=None):
    """[内側] ─ ‖線‖ ─ [外側] + dải chốt đáy.

    LUẬT BA KHỐI (`stage-zu-layout.md` §2): hàng nội dung · (không bong bóng) · dải chốt.
    Ba node cùng một hàng nên gate ⑬ (node lơ lửng) không bắt — chúng không "một mình
    một hàng", và cả ba đều có nhãn.
    `sen` là node HERO ở giữa: nó vừa là con số, vừa là cái vạch.
    """
    return C(match, "zu", title=title, nodes=[
        N("in", "label", [0.08, 0.42], label=uchi, lw=300, dim=uchi_dim),
        N("sen", "label", [0.50, 0.42], label=sen, lw=400, hero=True, under=True),
        N("out", "label", [0.92, 0.42], label=soto, lw=300, dim=soto_dim),
        N("bb", "bubble", [0.58, 0.66], label=why, tail="up", lw=470),
        N("cl", "label", [0.50, 0.99], label=close, lw=560)],
        left=left, right=right, sub=sub)


# ── thẻ SPINE: số CŨ → số MỚI, bong bóng nói VÌ SAO (chép nguyên từ video 13) ──
def spine(match, title, old, new, why, close, sub=None, left="sensei_explain",
          right="kikite_think", tone_new="amber", bb_y=0.62, sp=(0.17, 0.75)):
    return C(match, "zu", title=title,
             nodes=[N("old", "label", [sp[0], 0.40], label=old, lw=300),
                    N("new", "label", [sp[1], 0.40], label=new, lw=360, hero=True,
                      under=True),
                    N("bb", "bubble", [0.62, bb_y], label=why, tail="up", lw=480),
                    N("cl", "label", [0.50, 0.99], label=close, lw=560)],
             edges=[E("old", "new", "arrow", tone=tone_new)],
             left=left, right=right, sub=sub)


# ── thẻ 3 CỘT DỌC (chép nguyên) ────────────────────────────────────────────────
def cols3(match, title, items, close, left="sensei_caution", right="kikite_worried"):
    ns = [N(f"c{i}", "group", [0.0, 0.42], w=248, h=430, icon=ic, foot=lab, iconsize=190,
            fix=True)
          for i, (ic, lab) in enumerate(items)]
    ROW(ns, 0.42, mingap=104)
    ns.append(N("x", "label", [0.50, 0.92], label=close, lw=560))
    return C(match, "zu", title=title, nodes=ns, left=left, right=right)


def two_ways(match, title, l_head, l_icon, r_head, r_hero, r_foot, close,
             close_icon="money_pouch", left="sensei_serious", right="kikite_worried"):
    return C(match, "zu", title=title, nodes=[
        N("L", "group", [0.16, 0.34], w=386, h=330, tone="ink", head=l_head,
          icon=l_icon, iconsize=165, fix=True),
        N("R", "group", [0.84, 0.34], w=386, h=330, tone="ink", head=r_head,
          hero=r_hero, foot=r_foot, under=True, fix=True),
        N("B", "banner", [0.50, 0.97], w=950, icon=close_icon, label=close, fix=True)],
        edges=[E("L", "R", "arrow", tone="ink", w=18)], left=left, right=right)


def one_to_n(match, title, big, big_icon, items, close, left="sensei_point",
             right="kikite_think"):
    L = ROW([N("L", "group", None, w=230, h=300, tone="ink", head=big, icon=big_icon,
               iconsize=140, fix=True)], 0.40, 0.0, 0.17)
    R = ROW([N(f"i{k}", "group", None, w=196, h=300, tone="amber", head=h, icon=ic,
               iconsize=100, fix=True) for k, (h, ic) in enumerate(items)],
            0.40, 0.38, 1.0, mingap=26)
    return C(match, "zu", title=title,
             nodes=[*L, *R,
                    N("B", "banner", [0.50, 0.99], w=950, tone="ink", label=close, fix=True)],
             edges=[E("L", "i0", "arrow", tone="ink", w=16)], left=left, right=right)


def chain(match, title, steps, chip=None, wrong=None, close=None, left="sensei_caution",
          right="kikite_nod"):
    ns = ROW([N(f"n{k}", "circle", None, icon=ic, label=lb, fix=True,
                **({"tone": "amber"} if am else {}))
              for k, (ic, lb, am) in enumerate(steps)], 0.44, mingap=104)
    if chip:
        ns = [N("chip", "chip", [0.02, 0.02], label=chip, spark=True, fix=True)] + ns
    eg = [E(f"n{k}", f"n{k+1}", "arrow", tone="ink", w=16) for k in range(len(steps) - 1)]
    if wrong:
        eg.append(E(wrong[0], wrong[1], "arc", tone="ink", x=True, drop=200))
    if close:
        ns = ns + [N("cl", "label", [0.50, 0.99], label=close, lw=560)]
    return C(match, "zu", title=title, nodes=ns, edges=eg, left=left, right=right)


def polish(cards):
    """① label ở ĐÁY → banner  ② hàng ≥3 vật → zu_row. Cân dọc do `zu_fit` của tool."""
    nb = nr = 0
    for c in cards:
        v = c["stage"]
        if v.get("layout") != "zu":
            continue
        ns = v["nodes"]
        for n in ns:
            if n["kind"] == "label" and n["at"][1] >= 0.85 and not n.get("hero"):
                n.update(kind="banner", at=[0.50, 0.99], w=950)
                n.pop("lw", None)
                nb += 1
        cs = [n for n in ns if n["kind"] in ("circle", "mark", "icon", "oval", "group")]
        rows = {}
        for n in cs:
            rows.setdefault(round(n["at"][1], 2), []).append(n)
        for y, grp in rows.items():
            if len(grp) < 3 or any(n.get("fix") for n in grp):
                continue
            ids = {n["id"] for n in grp}
            linked = any(e["from"] in ids and e["to"] in ids for e in v.get("edges", []))
            ROW(grp, y, mingap=104 if linked else 40)
            nr += 1
    print(f"[polish] {nb} label đáy → banner  ·  {nr} hàng ≥3 vật → zu_row")
    return cards


# ══════════════════════════════════════════════════════════════════════════════
CARDS = [
    # ═════════════════════════ COLD OPEN — hai phong bì trên bàn bếp
    C("中村さんの台所のテーブルに", "art",
      title="台所のテーブルに、封筒が《2通》",
      img="art_futatsu_no_fuutou.png", fly="up",
      cap="新潟県上越市・中村さん（71）。おひとり暮らし",
      left="sensei_serious", right="kikite_listen"),

    # 🔴 KHÔNG dùng two_ways ở đây: hai phong bì là ĐỐI CHIẾU, không phải nhân quả.
    # Bản đầu dùng two_ways ⇒ mũi tên giữa hai hộp đọc thành "1 dẫn tới 2", hộp trái chỉ có
    # icon nên trống nghĩa (không nói là giấy gì, không có ＋3万円), và đĩa vàng của
    # cắt mất chữ số. Gate hình học cho qua sạch — đây là lỗi NGHĨA, phải soi 1:1 mới thấy.
    # ⭐ 2026-08-19 đổi compare → pict (style りょう): 2 panel MÀU đối nhau — xanh = tin tốt,
    # đỏ = tin xấu (bộ màu signature kênh) — mỗi panel một ẢNH phong bì, số nằm trong label.
    C("「年金額改定通知書」。今年から", "pict",
      title="同じころに届いた、2通の通知書",
      panels=[{"label": "年金額改定通知書\n《＋3万円》",
               "img": "art_tsuchi_nenkin.png", "tone": "green"},
              {"label": "介護保険料決定通知書\n《＋4万9600円》",
               "img": "art_tsuchi_kaigo.png", "tone": "red"}],
      cap="増えたより、増やされたほうが《大きい》",
      left="sensei_serious", right="kikite_surprised"),

    spine("中村さんは71歳、新潟県上越市で", "去年と今年で、何が変わったか",
          "147万円", "150万円", "去年から今年で\n3万円ふえました",
          "それなのに、手元のお金は減りました",
          left="sensei_explain", right="kikite_think"),

    line("なぜ、そんなことが起きるのか", "答えは、《一本の線》です",
         "線", "非課税", "課税", "この線を、今日いっしょに確かめます",
         "線の内側か\n外側か",
         left="sensei_point", right="kikite_think"),
    C("その線を超えるのに必要だったのは", "big",
      title="線を超えるのに必要な額", value="1", unit="円",
      cap="《1円》多いか、少ないか。それだけで差がつきます",
      left="sensei_serious", right="kikite_surprised"),

    # ⭐ 2026-08-19 cols3 → pict 3-panel (style りょう): 3 NGƯỜI thật thay 3 icon —
    # beat "chuyện này của CHÍNH BÁC" phải thấy người, không phải thấy túi tiền.
    C("この線の話は、中村さんだけの話ではありません", "pict",
      title="この線に触れるかた",
      panels=[{"label": "年金《200万円》", "img": "art_hito_200man.png"},
              {"label": "年金《150万円》", "img": "art_hito_150man.png"},
              {"label": "年金《80万円》", "img": "art_hito_80man.png"}],
      cap="金額にかかわらず、《全員》が関わります",
      left="sensei_explain", right="kikite_listen"),

    C("いちばん多い落とし穴は", "zu", title="いちばん多い《落とし穴》",
      nodes=[N("me", "circle", [0.14, 0.40], icon="person", label="ご自分"),
             N("ie", "circle", [0.60, 0.40], icon="house", label="ご家族"),
             N("bb", "bubble", [0.62, 0.66], label="ご家族に、線を\n越えさせてしまう",
               tail="up", lw=460),
             N("cl", "label", [0.50, 0.99], label="このお話は、動画の後半で", lw=560)],
      edges=[E("me", "ie", "arrow", tone="ink")],
      left="sensei_caution", right="kikite_worried"),

    # ═════════════════════════ 第1章 市役所の答え
    C("中村さんは、市役所に電話をしました", "zu", title="中村さんは、市役所に電話をしました",
      nodes=[N("me", "circle", [0.14, 0.40], icon="phone", label="中村さん"),
             N("shi", "panel", [0.66, 0.40], icon="madoguchi", label="市役所"),
             N("cl", "label", [0.50, 0.99], label="返ってきた答えは、ひとことでした", lw=560)],
      edges=[E("me", "shi", "arrow", tone="ink")],
      left="sensei_explain", right="kikite_listen"),

    spine("「去年までは、非課税でした", "市役所の、ひとこと",
          "非課税", "課税", "「今年から、課税に\nなりました」",
          "そのふたつの言葉のあいだに、線があります",
          left="sensei_serious", right="kikite_surprised"),

    C("こちらが、日本年金機構のページです", "art",
      title="原典：日本年金機構『令和8年度税制改正による主な改正事項』",
      img="genten_01_kikou_kyuchi.png", fly="up",
      cap="赤で囲んだところ ＝「級地区分ごとの非課税限度額（単身者の場合）」",
      left="sensei_point", right="kikite_think"),

    cols3("65歳以上の欄を、横に見ていきます", "65歳以上・おひとりの線（年金額）",
          [("house", "1級地\n155万円"), ("house", "2級地\n151万5千円"),
           ("house", "3級地\n148万円")],
          "どの線かは、住んでいる町で決まります",
          left="sensei_explain", right="kikite_think"),

    C("線は、1本ではありません", "big",
      title="線は、いくつあるか", value="3", unit="本",
      cap="1級地・2級地・3級地。《町ごと》に違います",
      left="sensei_point", right="kikite_surprised"),

    line("中村さんの線は、148万円でした", "上越市は3級地。線は《148万円》",
         "148万円", "去年\n147万円", "今年\n150万円",
         "去年は内側、今年は外側になりました",
         "線そのものは\n動いていません",
         left="sensei_explain", right="kikite_nod"),
    C("超えた額は、2万円", "big",
      title="線を超えた額", value="2", unit="万円",
      cap="たった《2万円》で、席が変わりました",
      left="sensei_serious", right="kikite_worried"),

    # ═════════════════════════ 第2章 線は市の名前で決まる
    C("では、ご自分の町の線が、どれなのか", "zu", title="うちの町は、何級地か",
      nodes=[N("q", "circle", [0.16, 0.38], icon="magnifier", label="うちは\n何級地?"),
             N("m", "panel", [0.66, 0.38], icon="docs", label="厚生労働省"),
             N("cl", "label", [0.50, 0.99], label="機構のページから、直接つながっています",
               lw=560)],
      edges=[E("q", "m", "arrow", tone="ink")],
      left="sensei_point", right="kikite_think"),

    C("厚生労働省の、こちらのページです", "art",
      title="原典：厚生労働省『お住まいの地域の級地』",
      img="genten_02_mhlw_kyuchi.png", fly="up",
      cap="赤で囲んだところ ＝ 新潟市は2級地、上越市は3級地",
      left="sensei_point", right="kikite_think"),

    cols3("この表が、そのまま住民税の線になります", "同じ新潟県のなかで",
          [("house", "新潟市\n2級地"), ("house", "長岡市\n2級地"),
           ("house", "上越市\n3級地")],
          "同じ県でも、線が2本に分かれています",
          left="sensei_explain", right="kikite_surprised"),

    C("収入とも、持ち家かどうかとも、関係ありません", "check",
      title="線は、《市の名前》で決まります", bgimg="bg_machinami.png",
      ok=["市の名前で決まります"],
      no=["収入では決まりません", "持ち家かどうかでも決まりません"],
      left="sensei_explain", right="kikite_nod"),

    C("「電車で1時間のところにいる姉には", "zu", title="電車で1時間の、お姉さん",
      nodes=[N("a", "circle", [0.14, 0.36], icon="house", label="上越市\n中村さん"),
             N("b", "circle", [0.62, 0.36], icon="house", label="新潟市\nお姉さん"),
             N("bb", "bubble", [0.60, 0.66], label="「あちらには、\n何も来ないんですよ」",
               tail="up", lw=470),
             N("cl", "label", [0.50, 0.99], label="年金の額は、ほとんど同じだそうです",
               lw=560)],
      edges=[E("a", "b", "line", tone="ink", label="電車で1時間")],
      left="sensei_serious", right="kikite_worried"),

    line("そのあいだの3万5千円のなかに", "ふたりの線のあいだ",
         "3万5千円", "148万円\n上越市", "151万5千円\n新潟市",
         "中村さんの150万円は、ちょうどこのなか",
         "同じ県のなかに\n線が2本あります",
         left="sensei_point", right="kikite_surprised"),
    C("暮らしにかかる費用が、地域で違うからです", "check",
      title="なぜ、町によって違うのか", bgimg="bg_shotengai.png",
      ok=["暮らしの費用が地域で違う", "物価の高い町は、線も高い",
          "法律の施行令に書かれています"],
      left="sensei_explain", right="kikite_nod"),

    C("ただ、電車で1時間の距離に、線が2本ある", "big",
      title="電車で1時間の距離に", value="線が2本", unit="",
      cap="それが、いま起きていることです",
      left="sensei_serious", right="kikite_think"),

    # ═════════════════════════ 第3章 いくら変わったのか
    one_to_n("線を越えると、動くものはふたつです", "線を越えると、動くものは《ふたつ》",
             "線を\n越える", "warning",
             [("① 住民税", "cityhall"), ("② 介護\n保険料", "hospital")],
             "ひとつずつ、見ていきます",
             left="sensei_point", right="kikite_listen"),

    cols3("内訳は、市民税が3千円、県民税が1千円", "5千円の内訳",
          [("cityhall", "市民税\n3千円"), ("cityhall", "県民税\n1千円"),
           ("env", "森林環境税\n1千円")],
          "令和6年度から、3つ目が加わりました",
          left="sensei_explain", right="kikite_nod"),

    C("上越市のページは、この3つを、ひとつの見出しで並べています", "source",
      title="原典：上越市『課税の基準』",
      org="新潟県上越市（掲載日 2025年1月27日）",
      doc="「市民税・県民税・" + NL + "　森林環境税が" + NL + "　課税されない人」",
      note="※3つが、同じ非課税の基準で並んでいます",
      left="sensei_point", right="kikite_think"),

    line("線の内側にいるあいだは、この5千円が", "5千円は、《どちら側》で決まるか",
         "5千円", "内側\n0円", "外側\n5千円",
         "内側にいるあいだは、まるごと来ません",
         "均等割と\n森林環境税です",
         left="sensei_explain", right="kikite_relieved"),
    # ⭐ 2026-08-19 zu → pict 1-panel (style りょう): beat cảm xúc "yên tâm nhầm" cần
    # MẶT NGƯỜI nhẹ nhõm, không phải icon sổ. Panel `paper` để quote nổi trên nền trắng.
    C("「なんだ、5千円か」", "pict",
      title="通知書を見たときの、ひとこと",
      panels=[{"label": "「なんだ、5千円か」",
               "img": "art_gosen_anshin.png", "tone": "paper"}],
      cap="ここで安心してしまうかたが、いちばん《損》をします",
      left="sensei_caution", right="kikite_nod"),

    C("介護保険料です", "big",
      title="ふたつめが、《本命》です", value="介護保険料", unit="",
      cap="本当に動くのは、税金のほうではありません",
      left="sensei_serious", right="kikite_surprised"),

    C("上越市の表を、ご覧ください", "art",
      title="原典：上越市『介護保険料』（令和6年度から令和8年度）",
      img="genten_03_joetsu_kaigo.png", fly="up",
      cap="赤で囲んだところ ＝ 第3段階と第6段階",
      left="sensei_point", right="kikite_think"),

    # ⭐ vòng 2 (user 2026-08-19: "trình bày nhiều bằng hình ảnh và biểu đồ"): spine →
    # BIỂU ĐỒ CỘT 6 bậc thật của 上越市 — cú nhảy 第3→第6 thấy bằng CHIỀU DÀI CỘT.
    # Không note: 6 hàng × 104px đã chạm đáy vùng nội dung, câu chốt do thẻ sau chở.
    C("世帯全員が住民税非課税で、年金収入が120万円を超える方は", "bars",
      title="介護保険料の段階（上越市・年額）",
      label_w=270, max=95000,
      rows=[["第1段階", 15500, "grey", "1万5500円"],
            ["第2段階", 20200, "grey", "2万200円"],
            ["第3段階", 39500, "ok", "3万9500円"],
            ["第4段階", 69700, "grey", "6万9700円"],
            ["第5段階", 77400, "grey", "7万7400円"],
            ["第6段階", 89100, "bad", "8万9100円"]],
      left="sensei_explain", right="kikite_surprised"),

    C("第4段階と第5段階は、", "check",
      title="なぜ、ふたつ飛び越えるのか", bgimg="bg_hitori_ie.png",
      ok=["第4・第5 ＝ 世帯に課税の方がいて", "　　　　　ご本人は非課税のかたの席"],
      no=["中村さんは、おひとり暮らし", "世帯にいるのは、ご本人だけ"],
      left="sensei_explain", right="kikite_nod"),

    C("差額は、4万9600円", "big",
      title="段階が動いた差額", value="49600", unit="円",
      cap="月にならすと、4100円ほど。ひと月ぶんの《電気代》です",
      left="sensei_serious", right="kikite_worried"),

    # ═════════════════════════ 計算タイム
    C("同じ上越市の、おふたりです", "compare",
      title="同じ上越市の、おふたり",
      panels=[{"cap": "年金 147万円", "icon": "avatar_seniors"},
              {"cap": "年金 150万円", "icon": "avatar_watanabe"}],
      rows=["住民税　　　0円　→　5千円",
            "介護保険料　3万9500円　→　8万9100円",
            "手元に残る　143万500円　→　140万5900円"],
      left="sensei_explain", right="kikite_think"),

    spine("手元に残るのは、143万500円", "手元に残るお金",
          "143万500円", "140万5900円", "年金を3万円\n多くもらったほうが",
          "手元に残るお金は、少なくなります", bb_y=0.70, sp=(0.06, 0.92),
          left="sensei_serious", right="kikite_surprised"),

    C("手元に残るお金は、2万4600円、少ない", "big",
      title="3万円多くもらったかたの手取り", value="－24600", unit="円",
      cap="多くもらっているほうが、《少なく残ります》",
      left="sensei_serious", right="kikite_worried"),

    C("147万円のかたに、手取りで追いつくには", "zu", title="では、いくらあれば追いつくのか",
      nodes=[N("a", "label", [0.06, 0.40], label="147万円の手取り", lw=280),
             N("b", "label", [0.86, 0.40], label="152万5千円", lw=330, hero=True,
               under=True),
             N("bb", "bubble", [0.60, 0.64], label="5万4600円ぶん\n取り返して、やっと同じ",
               tail="up", lw=470),
             N("cl", "label", [0.50, 0.99], label="追いつくのに、5万5千円ちかく必要です",
               lw=580)],
      edges=[E("a", "b", "arrow", tone="amber")],
      left="sensei_point", right="kikite_think"),

    line("148万円から、152万5千円まで", "《逆転》の帯",
         "4万5千円", "148万円", "152万5千円",
         "このあいだは、多くもらうほど手元が減ります",
         "この帯のなかでは\n多いほど減ります",
         left="sensei_serious", right="kikite_worried"),
    C("いまの数字は、上越市の令和8年度の表で計算しています", "check",
      title="ひとつ、お断りです",
      no=["介護保険料は、段階の数も金額も", "市区町村ごとに違います", "帯の幅も、町によって変わります"],
      left="sensei_caution", right="kikite_nod"),

    C("ここで、ひとつだけお願いです", "source", title="この研究室について",
      org="年金と老後のお金研究室",
      doc="高評価・シェア・コメントが" + NL + "次の研究テーマになります",
      note="※ご感想や、調べてほしいテーマをお寄せください",
      left="sensei_present", right="kikite_nod"),

    C("皆さまの声が、次の研究テーマになります", "zu", title="皆さまの声が、次の研究テーマに",
      nodes=[N("c", "circle", [0.16, 0.38], icon="phone", label="コメント"),
             N("k", "panel", [0.66, 0.38], icon="docs", label="次の研究テーマ"),
             N("cl", "label", [0.50, 0.99], label="調べてほしいテーマを、お寄せください", lw=580)],
      edges=[E("c", "k", "arrow", tone="amber")],
      left="sensei_present", right="kikite_nod"),

    # ═════════════════════════ 第4章 線の内側にあるもの
    C("では、内側にいると、何があるのか", "compare",
      title="新潟市の渡辺さん（66）",
      panels=[{"cap": "渡辺さんの年金", "icon": "avatar_watanabe"},
              {"cap": "新潟市の線", "icon": "house"}],
      rows=["年金　　1年で86万4千円",
            "線　　　151万5千円",
            "どちら側　ずっと内側です"],
      left="sensei_explain", right="kikite_listen"),

    cols3("内側にいるから、受け取れているものがあります", "線の内側にあるもの",
          [("money_pouch", "支援給付金\n月2529円"), ("hospital", "介護保険料\n低い段階"),
           ("shield_check", "医療費の\n上限も低い")],
          "内側にいるから、受け取れています",
          left="sensei_explain", right="kikite_relieved"),

    two_ways("中村さんが失ったのは、5千円ではありませんでした", "中村さんが失ったもの",
             "払うことになった額", "cityhall", "本当に失ったもの", "資格", "住民税非課税世帯",
             "5千円ではなく、資格のほうでした",
             close_icon="lock", left="sensei_serious", right="kikite_worried"),

    # ═════════════════════════ 第5章 いちばん多い落とし穴
    C("そして、ここからが、冒頭で申し上げたお話です", "big",
      title="冒頭のお約束", value="ご家族の線", unit="",
      cap="ご自分の年金が、どちら側にあっても関係します",
      left="sensei_caution", right="kikite_think"),

    C("給付金の条件を、もう一度ご覧ください", "check",
      title="年金生活者支援給付金の3つの条件", bgimg="bg_kyufu_fuutou.png",
      ok=["① 65歳以上で老齢基礎年金", "② 前年の収入が基準額以下",
          "③ 世帯全員が住民税非課税"],
      left="sensei_explain", right="kikite_nod"),

    C("もし来年、息子さんが仕事の都合で戻ってきて", "zu", title="もし、息子さんが戻ってきたら",
      nodes=[N("s", "circle", [0.12, 0.36], icon="person", label="息子さん\n住民税あり"),
             N("h", "circle", [0.58, 0.36], icon="house", label="渡辺さんの\n世帯"),
             N("bb", "bubble", [0.58, 0.66], label="住民票を移した\nその日から",
               tail="up", lw=440),
             N("cl", "label", [0.50, 0.99], label="世帯は、非課税ではなくなります", lw=560)],
      edges=[E("s", "h", "arrow", tone="ink")],
      left="sensei_caution", right="kikite_worried"),

    C("渡辺さんの年金は、1円も変わっていません", "check",
      title="渡辺さんに起きること",
      no=["給付金が止まります", "介護保険料が第4・第5段階へ"],
      ok=["年金の額は、1円も変わりません"],
      left="sensei_serious", right="kikite_worried"),

    C("年金が200万円あるかたにも関わります、と申し上げたのは", "zu",
      title="線を越えさせるのは、《ご自分ではありません》",
      nodes=[N("me", "circle", [0.12, 0.36], icon="person", label="あなた\n年金200万円"),
             N("mo", "circle", [0.58, 0.36], icon="couple_senior", label="お母さま\n線の内側"),
             N("bb", "bubble", [0.58, 0.66], label="実家に住民票を\n移したその日に",
               tail="up", lw=450),
             N("cl", "label", [0.50, 0.99], label="お母さまを、線の外へ連れ出してしまう",
               lw=580)],
      edges=[E("me", "mo", "arrow", tone="ink")],
      left="sensei_caution", right="kikite_surprised"),

    # ⭐ 2026-08-19 zu → art (style りょう): đỉnh cảm xúc của bài — kênh mẫu dùng nguyên
    # một khung tranh cho khoảnh khắc kiểu này. Quote lên TITLE, ảnh chở nỗi chờ.
    C("「息子が帰ってくるのを、待っていたんですけどねえ」", "art",
      title="「息子が帰ってくるのを、待っていたんですけどねえ」",
      img="art_madobe_watanabe.png", fly="up",
      cap="待たなくていい、というお話ではありません",
      left="sensei_serious", right="kikite_down"),

    C("住民票をどうするかは、移す前に", "check",
      title="決める前に、できること", bgimg="bg_madoguchi.png",
      ok=["移す前に、市区町村の窓口で聞けます", "知ったうえで決めれば、それでいい"],
      no=["知らずに決めると、あとで戻せません"],
      left="sensei_reassure", right="kikite_nod"),

    C("引っ越しは、税金の話でもある", "big",
      title="今日、覚えて帰っていただきたい一行", value="引っ越しは、税金の話", unit="",
      cap="同居を決める前に、この一行だけ",
      left="sensei_conclude", right="kikite_nod"),

    # ═════════════════════════ 第6章 ご夫婦の線
    C("横浜の田中さんから、こんな質問をいただいています", "zu",
      title="横浜の田中さん（67）からのご質問",
      nodes=[N("me", "circle", [0.16, 0.36], icon="avatar_tanaka", label="田中さん"),
             N("bb", "bubble", [0.60, 0.42],
               label="「ふたりになったら、\n線も変わるんですか」", tail="left", lw=490),
             N("cl", "label", [0.50, 0.99], label="変わります。しかも、上がります", lw=560)],
      left="sensei_explain", right="kikite_think"),

    C("ご夫婦の表は、どこにも出ていません", "check",
      title="ここから先は、お断りをさせてください",
      ok=["おひとりの表 ＝ 機構が出しています"],
      no=["ご夫婦の表 ＝ どこにも出ていません",
          "市区町村の式から、当研究室で計算しました"],
      left="sensei_caution", right="kikite_nod"),

    C("「35万円かける、ご本人と配偶者の人数", "source",
      title="計算のもと：横浜市『均等割・所得割の納税義務者』",
      org="横浜市（1級地）",
      doc="35万円 ×（ご本人＋配偶者）" + NL + "＋ 10万円 ＋ 21万円",
      note="※級地ごとに、35万円と21万円の数字が変わります",
      left="sensei_point", right="kikite_think"),

    cols3("ご夫婦2人で計算すると、年金額でおよそ211万円", "ご夫婦2人の線（当研究室の計算）",
          [("couple", "1級地\n211万円"), ("couple", "2級地\n201万9千円"),
           ("couple", "3級地\n192万8千円")],
          "おひとりのときより、45万〜56万円ほど上がります",
          left="sensei_explain", right="kikite_surprised"),

    C("奥さまご自身にも年金があるときは", "check",
      title="ご夫婦の落とし穴",
      no=["奥さまが線を越えていれば", "世帯は、非課税ではありません"],
      ok=["まず奥さまが、おひとりの表で判定されます"],
      left="sensei_caution", right="kikite_worried"),

    # ⭐ vòng 2: line → BIỂU ĐỒ CỘT — 211万 vs 155万 chênh 27%, cột nói rõ hơn hộp chữ.
    C("そして、この線は、どちらかが亡くなった年に", "bars",
      title="線は、もう一度《動きます》",
      label_w=330, max=230,
      rows=[["ご夫婦2人の線", 211, "ok", "211万円"],
            ["おひとりの線", 155, "bad", "155万円"]],
      note="世帯の人数が変わった年に。前回の遺族年金の回と地続きです",
      left="sensei_serious", right="kikite_down"),
    C("日本年金機構は、非課税所得とは", "source",
      title="原典：日本年金機構 年金Q&A『非課税所得とは』",
      org="日本年金機構（更新日 2019年9月2日）",
      doc="「死亡を支給事由とする年金」" + NL + "「障害を支給事由とする年金」",
      note="※前回の13万9千円は、今日の線の計算に乗りません",
      left="sensei_point", right="kikite_nod"),

    C("この判定に、手続きは要りません", "check",
      title="間違えやすいところ ②",
      ok=["市区町村が、自動で判定します", "申請しそこねることは、ありません"],
      no=["こちらから止めることも、できません"],
      left="sensei_explain", right="kikite_nod"),

    C("それでは、今日の研究ノートです", "check",
      title="今日の研究ノート",
      ok=["おひとりの線 148万・151万5千・155万",
          "町の級地は、厚労省の一覧表で決まる",
          "越えて払う税金は5千円。動くのは介護保険料"],
      no=["上越市では 第3段階→第6段階で年4万9600円",
          "線を越えるのは、世帯の顔ぶれでも起きる"],
      left="sensei_conclude", right="kikite_nod"),

    C("線を越えるのは、自分の年金だけではありません", "big",
      title="今日いちばん、覚えて帰っていただきたいこと", value="世帯の顔ぶれ", unit="",
      cap="線を越えるのは、自分の年金だけではありません",
      left="sensei_conclude", right="kikite_nod"),

    C("中村さんに、最後にお会いしたときのことです", "art",
      title="40年、学校給食の大鍋をかき回してきたかた",
      img="art_kyushoku_oonabe.png", fly="up",
      cap="新潟の冬、朝いちばんに火を入れるのは、いつも自分だったと",
      left="sensei_serious", right="kikite_listen"),

    C("「知らないままだったら、あの通知書を見て", "zu", title="中村さんの、ひとこと",
      nodes=[N("me", "circle", [0.16, 0.36], icon="avatar_seniors", label="中村さん"),
             N("bb", "bubble", [0.60, 0.42],
               label="「役所が間違えたと、\n思ってたわ」", tail="left", lw=470),
             N("cl", "label", [0.50, 0.99], label="線は動かせません。けれど、確かめられます",
               lw=580)],
      left="sensei_reassure", right="kikite_relieved"),

    C("3つだけ、お願いします", "steps",
      title="今日、できること3つ", bgimg="bg_denwa_techou.png",
      steps=["厚労省のページで級地を見る", "去年の年金額を通知書で確かめる",
             "線から5万円以内なら電話を1本"],
      left="sensei_present", right="kikite_nod"),

    chain("さて、次回です", "次回：10月15日の振込",
          [("calendar", "10月15日", False), ("passbook", "振込額", False),
           ("warning", "8月と違う", True)],
          chip="次回予告",
          close="住民税と介護保険料が、10月から本徴収に変わります",
          left="sensei_point", right="kikite_think"),

    C("なお、この動画は2026年8月時点の情報です", "source", title="ご確認のお願い",
      org="年金と老後のお金研究室",
      doc="金額は、お住まいの" + NL + "市区町村で変わります",
      note="※ご自分の数字は、市区町村の税務担当と年金事務所でご確認ください",
      left="sensei_conclude", right="kikite_nod"),
]

# ══════════════════════════════════════════════════════════════════════════════
CAPS = {"check": (24, ("ok", "no")), "compare": (32, ("rows",)),
        "steps": (22, ("steps",)), "source": (23, ("doc",))}
ZU_CAP = {"label": (30, 2), "circle": (26, 2), "mark": (26, 2), "icon": (26, 2),
          "panel": (26, 1), "bubble": (26, 3),
          "banner": (30, 1), "ribbon": (38, 1), "chip": (28, 1),
          "oval": (24, 2), "bigicon": (26, 2), "group": (28, 2)}
ZU_LW = {"label": 470, "bubble": 340, "banner": 950, "ribbon": 900, "chip": 300,
         "oval": 182, "group": 400}
ZU_MAX_NODES = 7


def secs(lines, i, j):
    tot = 0.0
    for k in range(i, j):
        t = lines[k]
        tot += GAP_PARA if not t else len(t) / CH_PER_SEC + GAP_LINE
    return tot


def main():
    polish(CARDS)
    lines = [re.sub(r"^(\[[^\]]*\])+", "", raw).strip()
             for raw in TTS.read_text(encoding="utf-8").splitlines()]
    dur = secs(lines, 0, len(lines))

    idx, errs = [], []
    for c in CARDS:
        hits = [i for i, t in enumerate(lines) if t and c["match"] in t]
        if len(hits) != 1:
            errs.append(f"  match {'0 dòng' if not hits else f'{len(hits)} dòng {hits}'}"
                        f": {c['match']!r}")
            idx.append(None)
        else:
            idx.append(hits[0])
    if errs:
        print("🔴 MATCH KHÔNG DUY NHẤT — chưa ghi file:")
        print("\n".join(errs))
        sys.exit(1)

    for a, b in zip(idx, idx[1:]):
        if b <= a:
            errs.append(f"  thứ tự sai: dòng {a} → {b}")

    holds = [secs(lines, a, b) for a, b in zip(idx, idx[1:])]
    holds.append(secs(lines, idx[-1], len(lines)))
    for k, s in enumerate(holds):
        if s < MIN_SEC:
            errs.append(f"  [{k:02d}] entry chỉ {s:.1f}s < {MIN_SEC}s (dòng {idx[k]}) "
                        f"— gộp với thẻ liền kề: {CARDS[k]['match']!r}")
        if s > 29.0:
            errs.append(f"  [{k:02d}] entry {s:.1f}s > 29s — clip 30s sẽ LẶP build-on. "
                        f"Chẻ thêm một thẻ: {CARDS[k]['match']!r}")

    # ══ ⭐ AUTO-BEATS — nhịp xuất hiện theo LỜI ĐỌC (style りょう, 2026-08-19) ══════════
    # Đo từ kênh mẫu 節約看護師りょう (video 6DN88wQyBFg, beat sheet 1fps): phần tử pop
    # cách nhau 3–6s, đúng lúc giọng chạm ý — KHÔNG lắp hết trong 2s đầu rồi đứng im.
    # Không có srt (voice chưa synth) nên mốc ước từ hệ số 5,72 ký/giây + gap, và BÁM
    # ĐẦU DÒNG gần nhất — dòng ≈ một ý, nên bám dòng là bám lời đọc. Thẻ nào cần chỉnh
    # tay thì ghi "beats": [...] thẳng trong CARDS, auto sẽ nhường.
    def n_elems(v):
        L = v["layout"]
        if L == "zu":
            return len(v["nodes"])
        if L == "check":
            return len(v.get("ok", [])) + len(v.get("no", []))
        if L == "pict":
            return len(v["panels"]) + (1 if v.get("cap") else 0)
        if L == "compare":
            return 2 + len(v.get("rows", []))
        if L == "big":
            return 1 + (1 if v.get("cap") else 0) + (1 if v.get("note") else 0)
        if L in ("art", "photo"):
            return 1 + (1 if v.get("cap") else 0)
        if L == "bars":
            return len(v.get("rows", [])) + (1 if v.get("note") else 0)
        return 0

    n_auto = 0
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if "beats" in v:
            continue
        n = n_elems(v)
        if n < 2:
            continue
        a = idx[k]
        b = idx[k + 1] if k + 1 < len(CARDS) else len(lines)
        hold = holds[k]
        offs = [secs(lines, a, m) for m in range(a, b) if lines[m]]
        span0, span1 = 1.6, max(hold - 1.4, 2.4)
        bts, prev = [], 0.0
        for j in range(n):
            tgt = span0 + (span1 - span0) * (j / (n - 1) if n > 1 else 0)
            t = min(offs, key=lambda o: abs(o - tgt)) if offs else tgt
            t = max(t, span0 if j == 0 else prev + 0.8)
            t = min(t, hold - 0.5)
            bts.append(round(t, 2))
            prev = t
        v["beats"] = bts
        n_auto += 1
    print(f"[beats] gắn nhịp lời đọc cho {n_auto} thẻ (thẻ có beats tay thì giữ nguyên)")

    for k, c in enumerate(CARDS):
        v = c["stage"]
        spec = CAPS.get(v.get("layout"))
        if not spec:
            continue
        cap, keys = spec
        for key in keys:
            val = v.get(key)
            if not val:
                continue
            for j, row in enumerate([val] if isinstance(val, str) else val):
                txt = row[1] if isinstance(row, (list, tuple)) else row
                for ln in str(txt).split(NL):
                    if len(ln) > cap:
                        errs.append(f"  [{k:02d}] {v['layout']}.{key}[{j}] TRÀN: "
                                    f"{len(ln)} ký > trần {cap}: {ln!r}")

    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "zu":
            continue
        ns = v["nodes"]
        ids = [n["id"] for n in ns]
        if len(ns) > ZU_MAX_NODES:
            errs.append(f"  [{k:02d}] zu có {len(ns)} node > trần {ZU_MAX_NODES}")
        if len(set(ids)) != len(ids):
            errs.append(f"  [{k:02d}] zu trùng id node: {ids}")
        for n in ns:
            fx, fy = n["at"]
            if not (0.0 <= fx <= 1.0 and 0.0 <= fy <= 1.0):
                errs.append(f"  [{k:02d}] zu node {n['id']} at={n['at']} ra ngoài 0..1")
            if n.get("icon") and _icon_path(n["icon"]) is None:
                errs.append(f"  [{k:02d}] zu node {n['id']} icon {n['icon']!r} KHÔNG CÓ FILE")
            for key, mx in ((("head", 2), ("hero", 1), ("foot", 2))
                            if n.get("kind") == "group" else ()):
                txt = n.get(key)
                if not txt:
                    continue
                if len(txt.split(NL)) > mx:
                    errs.append(f"  [{k:02d}] zu {n['id']}.{key} {len(txt.split(NL))} dòng "
                                f"> {mx}: {txt!r}")
                cap = int(n.get("w", 400) * n.get("s", 1.0) // (28 if key != "hero" else 40))
                for ln in txt.split(NL):
                    if len(ln) > cap:
                        errs.append(f"  [{k:02d}] zu {n['id']}.{key} TRÀN: {len(ln)} ký "
                                    f"> trần {cap} (w={n.get('w', 400)}): {ln!r}")
            lab = n.get("label", "")
            if lab:
                floor, maxln = ZU_CAP[n.get("kind", "circle")]
                lw = n.get("lw", ZU_LW.get(n.get("kind", "circle"), 300))
                cap = int(lw * n.get("s", 1.0) // floor)
                if len(lab.split(NL)) > maxln:
                    errs.append(f"  [{k:02d}] zu {n['id']} {len(lab.split(NL))} dòng > "
                                f"{maxln}: {lab!r}")
                for ln in lab.split(NL):
                    if len(ln) > cap:
                        errs.append(f"  [{k:02d}] zu {n['id']} ({n.get('kind','circle')}) "
                                    f"TRÀN: {len(ln)} ký > trần {cap} (lw={lw}): {ln!r}")
        for e in v.get("edges", []):
            for side in ("from", "to"):
                if e[side] not in ids:
                    errs.append(f"  [{k:02d}] zu edge {side}={e[side]!r} không có node đó")
        for msg in _zu_check(v):
            errs.append(f"  [{k:02d}] zu {msg}")

    # ── gate layout `pict` (style りょう): trần ký label theo bề rộng panel THẬT ──────
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "pict":
            continue
        ps = v.get("panels", [])
        n = len(ps)
        if not 1 <= n <= 3:
            errs.append(f"  [{k:02d}] pict có {n} panel — trần 1–3")
            continue
        span = 1400 - 520
        pw = span * 0.66 if n == 1 else (span - 40 * (n - 1)) / n
        capn = int((pw - 48) // 30)
        for j, pn in enumerate(ps):
            lab = pn.get("label", "").replace("《", "").replace("》", "")
            if len(lab.split(NL)) > 2:
                errs.append(f"  [{k:02d}] pict panel[{j}] label >2 dòng: {lab!r}")
            for ln in lab.split(NL):
                if len(ln) > capn:
                    errs.append(f"  [{k:02d}] pict panel[{j}] label TRÀN: {len(ln)} ký > "
                                f"trần {capn} (pw={pw:.0f}): {ln!r}")
            if not pn.get("img"):
                errs.append(f"  [{k:02d}] pict panel[{j}] thiếu \"img\" — panel không ảnh "
                            f"là thẻ trống (bài học demo 2026-08-19)")
        capln = v.get("cap", "").replace("《", "").replace("》", "")
        if capln and len(capln) > 29:
            errs.append(f"  [{k:02d}] pict cap TRÀN: {len(capln)} ký > 29: {capln!r}")

    if errs:
        print("🔴 GATE:")
        print("\n".join(errs))
        sys.exit(1)

    OUT.write_text(json.dumps(CARDS, ensure_ascii=False, indent=1), encoding="utf-8")

    import collections
    n = len(CARDS)
    dist = collections.Counter(c["stage"]["layout"] for c in CARDS)
    ln = [i for i, c in enumerate(CARDS)
          if c["stage"]["layout"] == "zu" and any(x["id"] == "sen" for x in c["stage"]["nodes"])]
    sp = [i for i, c in enumerate(CARDS)
          if c["stage"]["layout"] == "zu" and any(x["id"] == "old" for x in c["stage"]["nodes"])]
    art = sorted({c["stage"][x] for c in CARDS for x in ("img", "fill", "bgimg")
                  if c["stage"].get(x)}
                 | {p["img"] for c in CARDS for p in c["stage"].get("panels", [])
                    if isinstance(p, dict) and p.get("img")})
    print(f"✅ ghi {OUT.name}  —  {n} thẻ  ·  video {int(dur)//60}:{int(dur)%60:02d}")
    print(f"   nhịp: {n/(dur/60):.2f} đổi hình/phút (trần 6)  ·  "
          f"entry: min {min(holds):.1f}s · TB {dur/n:.1f}s · max {max(holds):.1f}s")
    print(f"   layout: {dict(dist)}")
    print(f"   TRỤC HÌNH — line (một đường kẻ): {ln}  ·  spine (số cũ→mới): {sp}")
    print(f"   ảnh cần có ({len(art)}): {art}")


if __name__ == "__main__":
    main()
