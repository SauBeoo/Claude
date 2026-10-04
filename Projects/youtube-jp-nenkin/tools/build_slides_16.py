# -*- coding: utf-8 -*-
"""build_slides_16.py — sinh `16_..._SLIDES.json` cho video 16 (12月の年金だけ違う・所得税の精算).

VÌ SAO CÓ TOOL NÀY: xem `build_slides_11.py` / `build_slides_13.py`. Bản 16 chép nguyên
helpers đã qua gate của `build_slides_14.py` (`spine` `line` `chain` `polish` + auto-beats)
— luật `CLAUDE.md` §VISUAL: *"video sau COPY các hàm này, đừng dựng lại từ node thô"*.

⭐ TRỤC HÌNH CỦA VIDEO NÀY: **一行 (một dòng trên tờ giấy) + tháng 12 lệch nhịp**.
Video 14 lấy trục "một đường kẻ". Bài này có hai motif lặp:
 1. `spine` số-cũ→số-mới (6,000→4,600 · 控除額 cũ→mới · 12月の欄 ít hơn) — cùng một cú
    "số tự động đổi" nhìn thấy 5 lần, khớp cold open "数字だけが、勝手に動く".
 2. Đáp án nằm ở **「所得税」の欄** trên 年金振込通知書 — tờ giấy đã quen từ video 08,
    xuất hiện mờ ở cold open (紙 ngủ trong ngăn kéo) và được mở đúng ở ~80% bài.

🔴 GIẤY TỜ TRONG ẢNH AI: mọi mock 通知書/申告書 phải CHUNG CHUNG, ô kẻ trống, KHÔNG chữ
thật (media-library §2.10 ⑦) — giấy thật chỉ ở 2 genten screenshot (Claude tự chụp trang
nenkin.go.jp + khoanh đỏ, không phải việc của user).

CHẠY:  python tools/build_slides_16.py
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
STEM = "16_shotokuzei-12gatsu-seisan-kangen"
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


# ── thẻ SPINE: số CŨ → số MỚI, bong bóng nói VÌ SAO (chép nguyên từ video 13/14) ──
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


# ── thẻ LINE: [内側] ─ ‖số của vạch‖ ─ [外側] + dải chốt (chép nguyên từ video 14) ──
def line(match, title, sen, uchi, soto, close, why, uchi_dim=False, soto_dim=False,
         left="sensei_explain", right="kikite_think", sub=None):
    return C(match, "zu", title=title, nodes=[
        N("in", "label", [0.08, 0.42], label=uchi, lw=300, dim=uchi_dim),
        N("sen", "label", [0.50, 0.42], label=sen, lw=400, hero=True, under=True),
        N("out", "label", [0.92, 0.42], label=soto, lw=300, dim=soto_dim),
        N("bb", "bubble", [0.58, 0.66], label=why, tail="up", lw=470),
        N("cl", "label", [0.50, 0.99], label=close, lw=560)],
        left=left, right=right, sub=sub)


# ── thẻ TWO GROUP: 2 hộp lớn cạnh nhau + banner chốt (khuôn two_ways của 13/14, ────
#    edge tùy chọn — so sánh thì đừng vẽ mũi tên, nhân quả/dòng thời gian thì vẽ) ──
def twogrp(match, title, l_kw, r_kw, close, edge=None, close_icon=None,
           left="sensei_explain", right="kikite_think"):
    ns = [N("L", "group", [0.16, 0.34], w=386, h=330, fix=True, **l_kw),
          N("R", "group", [0.84, 0.34], w=386, h=330, fix=True, **r_kw),
          N("B", "banner", [0.50, 0.97], w=950,
            **({"icon": close_icon} if close_icon else {}), label=close, fix=True)]
    eg = [E("L", "R", **edge)] if edge else []
    return C(match, "zu", title=title, nodes=ns, edges=eg, left=left, right=right)


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
    # ═════════════════════════ COLD OPEN (0:00–1:09) — 間違いか、詐欺か
    # Entry 0 = ẢNH CHỦ THỂ (§2.10 ⑦): sổ 通帳 tháng 12, con số đang "động".
    C("あなたの年金から引かれている税金", "art",
      title="12月だけ、《数字が動く》",
      img="art_tsucho_12gatsu.png", fly="up",
      cap="手続きをした覚えは、ない。それなのに",
      # ⭐ LỚP STICKER NỔI (props_top) — user 2026-08-24 dán frame đối thủ cạnh thẻ này:
      # "hiện ra mỗi cái hình ảnh vs text không nhìn nó không đặc sắc". Thẻ `art` vốn chỉ có
      # 1 ảnh giữa card ⇒ trơ. Đối thủ xếp ~14 vật quanh một hình lớn. 6 vật hai bên, vào
      # lệch nhau nên frame "mọc" dần suốt cold open thay vì hiện một lúc.
      # Dùng props_top (không props) vì ảnh chính sẽ đè mất lớp dưới.
      # ⭐ SYNC (phương án C, user chốt 2026-08-24): mỗi vật gắn vào ĐÚNG CỤM TỪ nó
      # minh hoạ, hàm `sync_layer` tự tính giây. Bản trước rải 12 vật theo chủ đề ⇒
      # 10/12 không nằm trong câu nào, và chart_down SAI CHIỀU với 「多くなる方向に」.
      sync=[{"ph": "12月だけ", "icon": "calendar", "at": [0.085, 0.22], "s": 140,
             "rot": -10},
            {"ph": "12月だけ", "pin": {"kind": "badge", "t": "12月" + NL + "だけ",
                                       "at": [0.16, 0.14], "tone": "red", "r": 0.115,
                                       "size": 52}},
            {"ph": "金額が動く", "icon": "yen_coins", "at": [0.075, 0.50], "s": 132},
            {"ph": "多くなる方向に", "icon": "chart_up", "at": [0.925, 0.30], "s": 136},
            {"ph": "多くなる方向に", "pin": {"kind": "stamp", "t": "多くなる方向に",
                                            "at": [0.70, 0.13], "rot": -9, "size": 54}}],
      left="sensei_serious", right="kikite_listen"),

    # 原典 shot #1 rơi ở 0:14 — trong 3 phút đầu (GĐ0d): bảng ví dụ 6,000→4,600 của 機構.
    C("国の資料に、実例が載っています", "art",
      title="原典：日本年金機構『令和8年度税制改正による主な改正事項』",
      sync=[{"ph": "6,000円", "pin": {"kind": "stamp", "t": "実例です",
                                        "at": [0.72, 0.10], "rot": -7, "size": 46}},
            {"ph": "勝手に動く", "icon": "warning", "at": [0.925, 0.24], "s": 118}],
      img="genten_02_kikou_rei.png", fly="up",
      cap="赤で囲んだところ ＝ 6,000円 → 4,600円の実例",
      left="sensei_point", right="kikite_think"),

    C("これを見て、たいていのかたは", "pict",
      title="たいていのかたが、こう思います",
      sync=[{"ph": "間違えられたんじゃないか", "icon": "magnifier",
             "at": [0.075, 0.24], "s": 124},
            {"ph": "詐欺なんじゃないか", "icon": "phone", "at": [0.925, 0.24],
             "s": 120, "rot": 8}],
      panels=[{"label": "振込先の\n《間違い》？", "img": "art_machigai_gimon.png"},
              {"label": "還付金\n《詐欺》？", "img": "art_sagi_denwa.png",
               "tone": "red"}],
      cap="通帳を、二度見してしまいます",
      left="sensei_serious", right="kikite_worried"),

    C("どちらでもありません", "check",
      title="間違いでも、詐欺でもありません", bgimg="bg_denwa_shinpai.png",
      sync=[{"ph": "ほぼ全員に起きること", "pin": {"kind": "badge", "t": "ほぼ" + NL + "全員",
                                                  "at": [0.84, 0.16], "tone": "blue",
                                                  "r": 0.115, "size": 50}}],
      no=[("bank", "振込先の間違いでは、ない"), ("phone", "還付金詐欺でも、ない")],
      ok=[("receipt", "所得税が引かれている方の"), ("couple_senior", "ほぼ全員に起きること")],
      left="sensei_explain", right="kikite_surprised"),

    C("原因は、今年の税制改正", "big",
      title="本当の理由は", value="もう少し、意地悪", unit="", pop=True,
      sync=[{"ph": "意地悪", "pin": {"kind": "stamp", "t": "もう少し、意地悪",
                                     "at": [0.74, 0.12], "rot": -8, "size": 48}}],
      bgimg="bg_shorui_tsumi.png",
      props=[{"icon": "docs", "at": [0.09, 0.62], "s": 150, "rot": -8},
             {"icon": "hanko", "at": [0.10, 0.86], "s": 120, "rot": 12, "t0": 0.5},
             {"icon": "cityhall", "at": [0.91, 0.64], "s": 160, "t0": 0.7},
             {"icon": "warning", "at": [0.90, 0.88], "s": 110, "t0": 0.9}],
      cap="税制改正——《それだけ》では、ありません",
      left="sensei_serious", right="kikite_think"),

    # mở OPEN-LOOP: tờ giấy biết nửa câu trả lời — trả ở thẻ [~80%] 振込通知書
    C("おそらく、あなたの家のどこかに", "art",
      title="答えの《半分》を知っている紙",
      sync=[{"ph": "すでに眠っています", "icon": "envelope_open",
             "at": [0.075, 0.26], "s": 128, "rot": -8},
            {"ph": "半分だけを知っている", "pin": {"kind": "badge", "t": "答えの" + NL + "半分",
                                                "at": [0.84, 0.17], "tone": "amber",
                                                "r": 0.115, "size": 46}}],
      img="art_nemuru_kami.png", fly="up",
      cap="あなたの家の、どこかに眠っています",
      left="sensei_point", right="kikite_think"),

    C("前回の研究で、こんな約束をしました", "big",
      title="前回の約束", value="増えるかたが、います", unit="",
      sync=[{"ph": "増えるかたがいます", "icon": "chart_up", "at": [0.925, 0.28],
             "s": 134}],
      bgimg="bg_tsucho_calendar.png",
      props=[{"icon": "calendar", "at": [0.09, 0.62], "s": 150, "rot": -7, "t0": 0.35},
             {"icon": "passbook", "at": [0.1, 0.87], "s": 130, "t0": 0.51},
             {"icon": "clock", "at": [0.91, 0.66], "s": 140, "t0": 0.67}],
      cap="今日は、その《答え合わせ》です",
      left="sensei_present", right="kikite_nod"),

    # chẻ entry 32,0s (gate builder ≤29s). Neo vào chính dòng đồng cảm vừa chèn —
    # thẻ này trả lời câu 「え、全員ですか」 bằng hình, đúng lúc câu hỏi nảy ra.
    # ⭐ ĐỔI check → pict (2026-08-25, user: *"thay vì text hãy cho nó thành các ảnh minh hoạ,
    # 1 ảnh chuyển thành nhiều frame, hiển thị lần lượt theo sub"*). `pict` = panel ẢNH TO +
    # label ngắn, mỗi panel pop theo `beats` khớp lời — khuôn đo từ kênh mẫu りょう.
    C("年金から所得税が引かれているかたなら", "pict",
      title="「ほぼ全員」とは、どなたか",
      sync=[{"ph": "ご自身も", "pin": {"kind": "badge", "t": "あなたも" + NL + "対象",
                                       "at": [0.88, 0.20], "tone": "blue", "r": 0.105,
                                       "size": 44}}],
      fit=True,   # anh minh hoa: thay TRON, khong cover-crop (hop panel la DOC)
      panels=[{"label": "引かれて《いる》方", "img": "art_p7_hikareteru.png"},
              {"label": "引かれて《いない》方", "img": "art_p7_taisyougai.png",
               "tone": "paper"}],
      cap="ご自身も、その中に入ります",
      left="sensei_explain", right="kikite_think"),

    # ═════════════════════════ 第2章 高橋さんの居間 (1:27–2:45)
    C("灯油ストーブの匂いがする居間で", "art",
      title="12月・高橋さんの居間",
      img="art_ima_stove.png", fly="up",
      cap="年賀状の宛名を、書き終えたところ",
      left="sensei_explain", right="kikite_listen"),

    C("「ねえ、これ——振込先", "pict",
      title="奥さまの、ひとこと",
      panels=[{"label": "「振込先、間違え\nられたんじゃない？」",
               "img": "art_okusama_tsucho.png", "tone": "paper"}],
      cap="たしかに、先月より《多い》",
      left="sensei_serious", right="kikite_surprised"),

    C("振り込め詐欺の還付金、という言葉が", "zu", title="心当たりは、ひとつだけ",
      nodes=[N("sagi", "circle", [0.14, 0.38], icon="warning", label="詐欺かも"),
             N("fuu", "panel", [0.62, 0.38], icon="env", label="茶色い封筒"),
             N("bb", "bubble", [0.60, 0.68], label="「あの紙に、何か\n書いてあった気がする」",
               tail="up", lw=470),
             N("cl", "label", [0.50, 0.99], label="7月に届いた、扶養親族等申告書です",
               lw=560)],
      edges=[E("sagi", "fuu", "arrow", tone="ink")],
      left="sensei_explain", right="kikite_worried"),

    spine("高橋さんの勘は、半分だけ", "勘は、半分だけ当たっていました",
          "あの紙？", "国の制度", "答えは、もっと\n大きな場所に",
          "紙の話は、あとでもう一度戻ってきます",
          left="sensei_point", right="kikite_think"),

    line("高橋さんの年金は、月およそ20万円", "高橋さんは、線の外側",
         "214万円", "内側\n引かれない", "高橋さん\n240万円",
         "今日の話の、当事者です",
         "以前の研究で\n確かめた線です",
         left="sensei_explain", right="kikite_nod"),

    # ⭐ THẺ MENU — đúc từ 2 video đối thủ đang được đề xuất (2026-08-24):
    # demo1 サンデーマネー có 本日のメニュー @02:00 · demo2 シニアのお金相談所 có
    # 「今回の動画では①…④…を順番にお話しします」 @~02:30. Cả hai mở loop TẬP THỂ để
    # người xem biết còn mấy món chưa mở → có lý do ở lại tới hết. Script 16 vốn KHÔNG có.
    # 🔴 Thẻ này còn bịt một lỗ ĐO ĐƯỢC: sau khi chèn khối MENU vào lời, thẻ `line` ngay
    # trên giữ hình **45,3 giây** — dài nhất bài, và là kiểu "hình đứng im" mà cả hai đối
    # thủ không bao giờ để xảy ra (họ thêm phần tử mới mỗi ~5 giây).
    C("今日は、4つのことを、順番に確かめます", "steps",
      title="今日、確かめる4つのこと",
      bgimg="bg_note_yubi.png",
      props=[{"icon": "checklist", "at": [0.09, 0.64], "s": 155, "rot": -6, "t0": 0.35},
             {"icon": "magnifier", "at": [0.91, 0.66], "s": 140, "t0": 0.51}],
      steps=[("calendar", "12月だけ動く、その仕組み"), ("yen_coins", "では、いくら戻るのか"),
             ("shield_dash", "何も起きないのは、どんなかた"), ("passbook_open", "答えが印刷されている場所")],
      left="sensei_present", right="kikite_listen"),

    # ═════════════════════════ 第3章 改正の中身 (2:45–3:52)
    spine("発端は、今年の税制改正です", "発端は、今年の税制改正",
          "これまでの\n基礎控除", "引き上げ", "年金の税金の線が\n動きました",
          "どこが動いたのか、順番に見ていきます",
          left="sensei_explain", right="kikite_listen"),

    twogrp("65歳以上のかたなら", "所得税が引かれない線",
           dict(tone="ink", head="65歳以上", hero="214万円", foot="未満なら0円",
                under=True),
           dict(tone="ink", head="65歳未満", hero="164万円", foot="未満なら0円",
                under=True),
           "去年までは、205万円と155万円でした",
           left="sensei_explain", right="kikite_think"),

    C("高橋さんは、240万円ですから", "big",
      title="高橋さんの席は", value="外側のまま", unit="",
      props=[{"icon": "scale", "at": [0.09, 0.63], "s": 160, "t0": 0.35},
             {"icon": "form", "at": [0.1, 0.88], "s": 125, "rot": 10, "t0": 0.51},
             {"icon": "person", "at": [0.91, 0.66], "s": 135, "t0": 0.67}],
      cap="240万円は、新しい線の《外側》",
      left="sensei_explain", right="kikite_nod"),

    spine("ですが、ここに、もうひとつ", "もうひとつ、動いた数字",
          "去年までの\n控除額", "少し大きく", "控除が大きいほど\n税金は少ない",
          "線の外側のかたにも、恩恵があります",
          left="sensei_point", right="kikite_surprised"),

    # ═════════════════════════ 第4章 なぜ12月だけ (3:52–4:47)
    C("問題は、ここからです", "big",
      title="新しい控除額、いつから？", value="途中から", unit="",
      props=[{"icon": "calendar", "at": [0.09, 0.63], "s": 150, "rot": -8, "t0": 0.35},
             {"icon": "hourglass", "at": [0.1, 0.88], "s": 120, "t0": 0.51},
             {"icon": "clock", "at": [0.91, 0.65], "s": 145, "t0": 0.67}],
      cap="1年の《途中》からしか、反映されません",
      left="sensei_serious", right="kikite_think"),

    # 原典 shot #2 — đoạn 11月/12月 (FACT #2)
    C("国の資料は、こう説明しています", "art",
      title="原典：日本年金機構『令和8年度税制改正による主な改正事項』",
      img="genten_01_kikou_seisan.png", fly="up",
      cap="赤で囲んだところ ＝ 11月まで改正前・12月に精算",
      left="sensei_point", right="kikite_think"),

    twogrp("「令和8年12月の年金支払い時に", "1年の、ふたつの区間",
           dict(tone="ink", head="4月〜11月", icon="calendar", iconsize=110,
                foot="改正前の控除額"),
           dict(tone="amber", head="12月", hero="精算", foot="1年分を計算し直す",
                under=True),
           "多めに引かれていた分は、12月に戻ります",
           edge=dict(style="arrow", tone="amber", w=18),
           left="sensei_explain", right="kikite_nod"),

    # chẻ entry 29,5s. Neo vào câu hỏi vừa chèn — mở loop cho khối 計算タイム ngay sau.
    # ⚠️ neo phải dài hơn cụm 「では、いくら戻るのか」 — cụm ngắn đó cũng nằm trong thẻ MENU
    # ở trên ⇒ match không duy nhất, builder chặn không ghi file.
    C("では、いくら戻るのか。いちばん気になる", "big",
      title="では、ご自身は", value="いくら戻る？", unit="",
      props=[{"icon": "magnifier", "at": [0.09, 0.63], "s": 150, "t0": 0.35},
             {"icon": "calc", "at": [0.1, 0.88], "s": 125, "rot": 7, "t0": 0.51},
             {"icon": "passbook", "at": [0.91, 0.66], "s": 140, "t0": 0.67}],
      cap="次に、機構の《一例》で確かめます",
      left="sensei_point", right="kikite_think"),

    # ═════════════════════════ 計算タイム (4:47–5:57)
    spine("冒頭の例に、戻りましょう", "機構の示す、一例",
          "改正前\n月6,000円", "月4,600円", "その差、\n1,400円",
          "2月から10月まで、5回分ありました",
          left="sensei_explain", right="kikite_think"),

    C("これが、2月から10月まで", "big",
      title="多めに引かれていた合計", value="7,000", unit="円", pop=True,
      bgimg="bg_kozeni_tsumi.png",
      props=[{"icon": "yen_coins", "at": [0.09, 0.63], "s": 165, "rot": -6},
             {"icon": "calc", "at": [0.10, 0.87], "s": 130, "t0": 0.5},
             {"icon": "money_pouch", "at": [0.91, 0.65], "s": 170, "t0": 0.7},
             {"icon": "nenkin_techo", "at": [0.90, 0.88], "s": 120, "rot": 10, "t0": 0.9}],
      cap="1,400円 × 5回分",
      left="sensei_explain", right="kikite_surprised"),

    spine("12月には、まず、いつもどおり", "12月の振込みで、起きること",
          "12月分の税金\n4,600円", "＋2,400円", "払いすぎた7,000円\nとの差額です",
          "まとめて、振込みに上乗せで戻ります",
          left="sensei_point", right="kikite_nod"),

    # chẻ entry 33,0s. Thẻ này gánh đúng chỗ script tự nhận STAKE nhạt (2,400円 nhỏ hơn
    # mọi hero-number của kênh): nói hộ 「たった、それだけか」 rồi lật ngay sang "đó chỉ là
    # VÍ DỤ của cơ quan, số của bạn khác". Không có thẻ này thì phản ứng đó không được trả lời.
    C("ただ、これは機構が示した", "check",
      title="この2,400円は、あくまで《一例》",
      bgimg="bg_dentaku_hitori.png",
      props=[{"icon": "calc", "at": [0.09, 0.64], "s": 145, "rot": -6, "t0": 0.35},
             {"icon": "receipt", "at": [0.91, 0.63], "s": 130, "t0": 0.51},
             {"icon": "scale", "at": [0.9, 0.88], "s": 125, "t0": 0.67}],
      no=[("magnifier", "ご自身の金額とは、限りません")],
      ok=[("scale", "年金額と扶養の状況で、変わります"), ("yen_coins", "大きいことも、小さいことも あります")],
      left="sensei_explain", right="kikite_worried"),

    C("高橋さんも、電卓を取り出して", "art",
      title="ところが、指が止まります",
      img="art_takahashi_dentaku.png", fly="up",
      cap="この式だけでは、決まらない",
      left="sensei_serious", right="kikite_think"),

    C("実際に何円戻るのかは", "check",
      title="この式だけでは、決まりません", bgimg="bg_dentaku_techou.png",
      no=[("scale", "年金の額で、控除額が違う"), ("couple", "扶養家族の有無でも、違う")],
      left="sensei_explain", right="kikite_worried"),

    C("さっきの、茶色い封筒", "art",
      title="茶色い封筒、ふたたび",
      img="art_chairo_fuutou.png", fly="up",
      cap="扶養親族等申告書が、もう一度関わります",
      left="sensei_point", right="kikite_surprised"),

    # ═════════════════════════ 扶養親族等申告書 (5:57–6:57)
    spine("配偶者がいて、その所得が少ないと", "申告書が、効いてくるところ",
          "基礎的\n控除額", "＋配偶者の分", "所得の少ない配偶者が\nいる場合の上乗せ",
          "高橋さんは、提出済みでした",
          left="sensei_explain", right="kikite_nod"),

    twogrp("つまり、同じ240万円の年金でも", "同じ240万円でも",
           dict(tone="amber", head="申告書を\n出したかた", hero="上乗せあり",
                under=True),
           dict(tone="ink", head="出していない\nかた", hero="上乗せなし"),
           "戻る額は、人によって変わります",
           left="sensei_explain", right="kikite_think"),

    C("この場で、正確な金額を計算することは", "check",
      title="この動画で、できること", bgimg="bg_kenkyu_desk.png",
      no=[("calc", "全パターンの計算は、できません")],
      ok=[("magnifier", "方法は、ひとつだけあります")],
      left="sensei_explain", right="kikite_listen"),

    C("答えは、すでに、高橋さんの手元にある紙に", "big",
      title="答えのありか", value="印刷済み", unit="",
      props=[{"icon": "envelope_open", "at": [0.09, 0.63], "s": 160, "rot": -7, "t0": 0.35},
             {"icon": "docs", "at": [0.1, 0.88], "s": 125, "t0": 0.51},
             {"icon": "magnifier", "at": [0.91, 0.66], "s": 140, "t0": 0.67}],
      cap="手元の《紙》に、もう書かれています",
      left="sensei_point", right="kikite_surprised"),

    # ═════════════════════════ 田中さんとの対比 (6:57–7:59)
    C("隣の田中さんは、少し、事情が違います", "pict",
      title="隣の、田中さん",
      panels=[{"label": "田中さん\n年金 月16万円", "img": "art_tanaka_shigoto.png"}],
      cap="まだ週5日、勤めに出ています",
      left="sensei_explain", right="kikite_listen"),

    line("192万円は、新しい線の214万円はもちろん", "田中さんは、線の内側",
         "214万円", "田中さん\n192万円", "外側",
         "今年も去年も、引かれていません",
         "0円は0円のまま\n12月も変化なし",
         soto_dim=True,
         left="sensei_explain", right="kikite_nod"),

    twogrp("ただし、田中さんには、パートのお給料が", "ふたつの、別々の仕組み",
           dict(tone="ink", head="年金", icon="passbook", iconsize=110,
                foot="12月に精算"),
           dict(tone="ink", head="お給料", icon="wallet", iconsize=110,
                foot="年末調整"),
           "別々に動いています。混ぜないように",
           edge=dict(style="dot", tone="ink"),
           left="sensei_caution", right="kikite_think"),

    # ═════════════════════════ CTA (~57%)
    C("ここで、ひとつだけお願いです", "source",
      title="この研究室について",
      org="年金と老後のお金研究室",
      doc="高評価・シェア・コメントが" + NL + "次の研究テーマになります",
      note="※ご感想や、調べてほしいテーマをお寄せください",
      left="sensei_present", right="kikite_nod"),

    C("ご感想や、調べてほしいテーマがあれば", "big",
      title="ご感想・リクエスト", value="コメント欄へ", unit="",
      props=[{"icon": "phone", "at": [0.09, 0.64], "s": 140, "t0": 0.35},
             {"icon": "mailbox", "at": [0.91, 0.64], "s": 140, "t0": 0.51},
             {"icon": "checklist", "at": [0.9, 0.88], "s": 120, "rot": 8, "t0": 0.67}],
      cap="皆さまの声が、次の研究テーマになります",
      left="sensei_present", right="kikite_nod"),

    # ═════════════════════════ 第8章 答え合わせ：振込通知書 (8:31–9:46)
    # trả OPEN-LOOP của cold open: tờ giấy trong ngăn kéo = 年金振込通知書 (đã quen từ video 08)
    C("先ほどの、答えが書かれている紙", "art",
      title="答えの紙 ＝ 年金振込通知書",
      img="art_furikomi_tsuchisho.png", fly="up",
      cap="以前の研究でも登場した、あの紙です",
      left="sensei_point", right="kikite_surprised"),

    C("その中の、「所得税」と書かれた", "big",
      title="答えは、たった一行", value="所得税", unit="の欄", pop=True,
      bgimg="bg_tsuchisho_gyou.png",
      props=[{"icon": "passbook_open", "at": [0.09, 0.63], "s": 170, "rot": -5, "t0": 0.35},
             {"icon": "form", "at": [0.1, 0.88], "s": 125, "rot": 9, "t0": 0.51},
             {"icon": "magnifier", "at": [0.91, 0.66], "s": 140, "t0": 0.67}],
      cap="12月分の数字が、答え《そのもの》です",
      left="sensei_explain", right="kikite_nod"),

    C("高橋さんは、その足で、6月に届いていた", "art",
      title="引き出しの、いつもの場所",
      img="art_hikidashi_sagasu.png", fly="up",
      cap="封筒の隅が、少しめくれています",
      left="sensei_explain", right="kikite_listen"),

    twogrp("10月分の「所得税」の欄と", "ふたつの欄を、並べて見比べる",
           dict(tone="ink", head="10月分", icon="docs", iconsize=110,
                foot="所得税の欄"),
           dict(tone="amber", head="12月分", hero="少ない", foot="所得税の欄",
                under=True),
           "差は、数千円のオーダーでした",
           edge=dict(style="arrow", tone="amber", w=18),
           left="sensei_point", right="kikite_surprised"),

    C("「本当に、戻ってくるんだな」", "pict",
      title="高橋さんの、つぶやき",
      panels=[{"label": "「本当に、\n戻ってくるんだな」",
               "img": "art_takahashi_tsubuyaki.png", "tone": "paper"}],
      cap="通帳より先に、紙が教えてくれました",
      left="sensei_reassure", right="kikite_relieved"),

    # ═════════════════════════ よくある誤解 (9:46–10:41)
    C("ここで、よくある誤解を", "pict",
      title="誤解①：別便で届く？",
      sync=[{"ph": "上乗せされて", "pin": {"kind": "stamp", "t": "上乗せ、だけ",
                                          # ⚠️ y=0.12 ĐÈ LÊN TIÊU ĐỀ (đã dựng thấy). Dải trống thật là DƯỚI panel (y≈0.93,
      # trên mép card 902 và dưới đáy panel ~790).
      "at": [0.52, 0.93], "rot": -6, "size": 50}}],
      fit=True,   # anh minh hoa: thay TRON, khong cover-crop (hop panel la DOC)
      # gộp 2 mục ✗ thành MỘT panel: 「別便で来ない」 và 「現金も来ない」 nói cùng một chuyện,
      # mà 3 panel thì ảnh chỉ còn ~230px (user: "ảnh nhỏ so với khung"). 2 panel ⇒ ~384px.
      panels=[{"label": "12月分に《上乗せ》", "img": "art_p43_uwanose.png"},
              {"label": "別便・現金は《無い》", "img": "art_p43_genkin.png", "tone": "red"}],
      left="sensei_caution", right="kikite_think"),

    C("ふたつ。「来年も、12月だけ多くなる」", "check",
      title="誤解②：来年も12月だけ多い？",
      props=[{"icon": "calendar", "at": [0.09, 0.64], "s": 150, "rot": -7, "t0": 0.35},
             {"icon": "warning", "at": [0.91, 0.63], "s": 130, "t0": 0.51},
             {"icon": "chart_down", "at": [0.9, 0.88], "s": 125, "t0": 0.67}],
      no=[("clock", "来年は、月ごとの差はありません")],
      ok=[("calendar", "最初から新しい控除額で計算")],
      left="sensei_caution", right="kikite_nod"),

    C("もうひとつ、覚えておいてください", "big",
      title="年金そのものは", value="±0", unit="円",
      props=[{"icon": "passbook", "at": [0.09, 0.63], "s": 150, "rot": -6, "t0": 0.35},
             {"icon": "yen_coins", "at": [0.1, 0.88], "s": 130, "t0": 0.51},
             {"icon": "shield_check", "at": [0.91, 0.66], "s": 135, "t0": 0.67}],
      cap="動くのは、天引きされる《税金》の側だけ",
      left="sensei_reassure", right="kikite_relieved"),

    # ═════════════════════════ ○×クイズ (10:41–11:56)
    C("さて、ここまでの話を", "big",
      title="ここまでの話を、あなたに", value="3問", unit="",
      props=[{"icon": "checklist", "at": [0.09, 0.63], "s": 155, "rot": -6, "t0": 0.35},
             {"icon": "person", "at": [0.91, 0.65], "s": 140, "t0": 0.51},
             {"icon": "magnifier", "at": [0.9, 0.88], "s": 115, "t0": 0.67}],
      cap="○か×か、答えてみてください",
      left="sensei_present", right="kikite_nod"),

    twogrp("ひとつめ。65歳以上で", "①あなたの年金は、線の上か下か",
           dict(tone="amber", head="○ 線の上", foot="今日の話の対象"),
           dict(tone="ink", head="× 線の下", foot="12月も変化なし"),
           "65歳以上214万円・65歳未満164万円",
           left="sensei_explain", right="kikite_think"),

    C("ふたつめ。今年の年金額は", "check",
      title="②年金額は、去年と同じくらい？", bgimg="bg_tsuchisho_te.png",
      ok=[("yen_coins", "同じなら、数千円のオーダーが目安")],
      no=[("chart_up", "途中で変わった方は、別の見え方")],
      left="sensei_explain", right="kikite_nod"),

    # chẻ entry 29,0s — và nói thẳng cái người xem đang nghĩ: số này nhỏ.
    C("大きな金額を待っていたかたには", "big",
      title="金額は、大きくありません", value="数千円", unit="の目安", pop=True,
      bgimg="bg_saifu_kozeni.png",
      props=[{"icon": "wallet_open", "at": [0.09, 0.63], "s": 165, "rot": -5, "t0": 0.35},
             {"icon": "yen_coins", "at": [0.1, 0.88], "s": 130, "t0": 0.51},
             {"icon": "receipt", "at": [0.91, 0.66], "s": 130, "t0": 0.67}],
      cap="ただ、放っておいても《損はしない》お金です",
      left="sensei_explain", right="kikite_think"),

    C("みっつめ。手元の年金振込通知書", "zu", title="③通知書で、答え合わせ",
      nodes=[N("doc", "panel", [0.16, 0.38], icon="docs", label="通知書"),
             N("tsu", "circle", [0.64, 0.38], icon="passbook", label="通帳"),
             N("bb", "bubble", [0.62, 0.68], label="10月分と12月分を\n並べて見比べる",
               tail="up", lw=470),
             N("cl", "label", [0.50, 0.99], label="それが、あなたの答え合わせです",
               lw=560)],
      left="sensei_point", right="kikite_nod"),

    # ═════════════════════════ 高橋さんの締め + 研究ノート (11:56–13:08)
    C("高橋さんは、通知書をしまいながら", "art",
      title="「税金って、増える話しか来ないと思ってたよ」",
      img="art_takahashi_warau.png", fly="up",
      cap="通知書をしまいながら、少し笑って",
      left="sensei_reassure", right="kikite_relieved"),

    C("奥さまが、「増えなくても", "pict",
      title="奥さまの、返し",
      panels=[{"label": "「減るなら、それで\nいいじゃない」",
               "img": "art_fusai_ima.png", "tone": "paper"}],
      cap="二人で笑っていたそうです",
      left="sensei_reassure", right="kikite_relieved"),

    C("それでは、今日の研究ノートです", "check",
      title="研究ノート（前半）", bgimg="bg_note_pen.png",
      ok=[("scale", "65歳以上は214万円が線"), ("hourglass", "65歳未満は164万円が線"),
          ("receipt", "外側の方も、税金は少し軽く")],
      left="sensei_conclude", right="kikite_nod"),

    C("みっつ。新しい控除額が反映されるのは", "check",
      title="研究ノート（後半）", bgimg="bg_note_pen.png",
      ok=[("calendar", "反映は、12月分から"), ("passbook_open", "答えは通知書の所得税の欄に"),
          ("shield_check", "手続きは不要。全員、自動")],
      left="sensei_conclude", right="kikite_nod"),

    C("今日のお願いは、ひとつだけです", "pict",
      title="今日のお願いは、ひとつだけ",
      sync=[{"ph": "5分も", "pin": {"kind": "num", "t": "5分", "at": [0.87, 0.24],
                                    "size": 104, "w": 0.20, "burst": True}}],
      fit=True,   # anh minh hoa: thay TRON, khong cover-crop (hop panel la DOC)
      panels=[{"label": "①《記帳》する", "img": "art_p55_kicho.png"},
              {"label": "②《所得税》の欄", "img": "art_p55_ran.png"},
              {"label": "③《見比べる》", "img": "art_p55_kurabe.png", "tone": "amber"}],
      left="sensei_present", right="kikite_nod"),

    chain("さて、次回です", "次回：年金機構をかたる詐欺",
          [("warning", "詐欺が急増", False), ("phone", "偽物の電話", False),
           ("magnifier", "見分け方", True)],
          chip="次回予告",
          close="本物の通知との違いを、確かめます",
          left="sensei_point", right="kikite_think"),

    C("なお、この動画は2026年8月時点の情報です", "source",
      title="ご確認のお願い",
      org="年金と老後のお金研究室",
      doc="正確な金額は、" + NL + "人によって変わります",
      note="※実際の通知書と、税務署・年金事務所でご確認ください",
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


def sync_layer(cards, lines, idx, holds):
    """⭐ KHỚP STICKER VỚI LỜI ĐỌC — user chốt 2026-08-24 (phương án C).

    Khai báo trong thẻ:  sync=[{"ph": "<cụm từ trong lời>", ...spec}]
      · có khoá "icon"  → thành 1 phần tử của `props_top` (sticker nổi trên ảnh), t0 = giây
        mà CHÍNH CỤM TỪ đó được đọc.
      · có khoá "pin"   → thành 1 phần tử của `pins`, beat = giây đó (kind stamp/badge/num…).

    VÌ SAO: bản đầu tao rải sticker "theo chủ đề thẻ" ⇒ 10/12 vật không nằm trong câu nào,
    và có vật SAI CHIỀU NGHĨA (câu nói 「多くなる方向に」 = tăng, mà đặt chart_down = giảm).
    User: *"vật phải hiển thị đúng với sub mày nói chứ"*. Hàm này làm việc đó bằng máy.

    🔴 GATE: cụm từ không tìm thấy trong phần lời của CHÍNH thẻ đó ⇒ in 🔴 và exit 1.
    Không cho phép gắn vật "trang trí" không khớp lời — đó là cả điểm của phương án C.

    Giây = secs(tới đầu dòng) + (vị trí ký tự của cụm trong dòng) / CH_PER_SEC.
    """
    bad = []
    for k, c in enumerate(cards):
        v = c["stage"]
        spec = v.pop("sync", None)
        if not spec:
            continue
        a = idx[k]
        b = idx[k + 1] if k + 1 < len(cards) else len(lines)
        hold = holds[k]
        # layout `art`/`photo` co L_art tu ve `pins` (toa do theo O ANH). Layout khac phai
        # dung `pins_card` (toa do theo KHUNG CARD) — them o make_stage 2.3.
        _pk = "pins" if v.get("layout") in ("art", "photo") else "pins_card"
        props, pins = list(v.get("props_top") or []), list(v.get(_pk) or [])
        for it in spec:
            ph = it["ph"]
            hit = None
            for m in range(a, b):
                if lines[m] and ph in lines[m]:
                    hit = (m, lines[m].index(ph))
                    break
            if hit is None:
                bad.append(f"  [{k:02d}] cụm {ph!r} KHÔNG có trong lời của thẻ "
                           f"{c['match']!r} — vật này không khớp sub, sửa hoặc bỏ")
                continue
            m, pos = hit
            t = secs(lines, a, m) + pos / CH_PER_SEC
            t = max(0.35, min(t, hold - 0.45))          # kẹp trong thời lượng thẻ
            if "icon" in it:
                props.append({kk: vv for kk, vv in it.items() if kk not in ("ph", "pin")}
                             | {"t0": round(t, 2)})
            elif "pin" in it:
                pins.append(dict(it["pin"], beat=round(t, 2)))
        if props:
            v["props_top"] = props
        if pins:
            v[_pk] = pins
    if bad:
        print("🔴 SYNC: vật không khớp lời — chưa ghi file:")
        print(chr(10).join(bad))
        sys.exit(1)
    n = sum(1 for c in cards if c["stage"].get("props_top") or c["stage"].get("pins"))
    print(f"[sync] {n} thẻ có sticker/pin khớp lời đọc")


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

    sync_layer(CARDS, lines, idx, holds)

    # ══ ⭐ AUTO-BEATS — nhịp xuất hiện theo LỜI ĐỌC (style りょう, chép từ video 14) ══
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
    sp = [i for i, c in enumerate(CARDS)
          if c["stage"]["layout"] == "zu" and any(x["id"] == "old" for x in c["stage"]["nodes"])]
    ln = [i for i, c in enumerate(CARDS)
          if c["stage"]["layout"] == "zu" and any(x["id"] == "sen" for x in c["stage"]["nodes"])]
    art = sorted({c["stage"][x] for c in CARDS for x in ("img", "fill", "bgimg")
                  if c["stage"].get(x)}
                 | {p["img"] for c in CARDS for p in c["stage"].get("panels", [])
                    if isinstance(p, dict) and p.get("img")})
    print(f"✅ ghi {OUT.name}  —  {n} thẻ  ·  video {int(dur)//60}:{int(dur)%60:02d}")
    print(f"   nhịp: {n/(dur/60):.2f} đổi hình/phút (trần 6)  ·  "
          f"entry: min {min(holds):.1f}s · TB {dur/n:.1f}s · max {max(holds):.1f}s")
    print(f"   layout: {dict(dist)}")
    print(f"   TRỤC HÌNH — spine (số cũ→mới): {sp}  ·  line (vạch 214万): {ln}")
    print(f"   ảnh cần có ({len(art)}): {art}")


if __name__ == "__main__":
    main()
