# -*- coding: utf-8 -*-
"""build_slides_15.py — sinh `15_..._SLIDES.json` cho video 15 (10月15日の年金振込・仮徴収と本徴収).

VÌ SAO CÓ TOOL NÀY: xem `build_slides_11/13/14/16.py`. Bản 15 chép nguyên helpers đã qua
gate (`spine` `line` `twogrp` `chain` `polish` + auto-beats style りょう) từ `build_slides_16.py`.

⭐ TRỤC HÌNH CỦA BÀI: **1年・6回の振込, chia 2 nửa (仮徴収 vs 本徴収)** — header script đã ghi
"timeline 6 kỳ trong năm (4·6·8 vs 10·12·2 — chưa dùng từ video 07)". Dùng lại layout `bars`
(đã chứng minh ở video 14 cho biểu đồ 6 bậc) nhưng trục là THÁNG thay vì BẬC, tô 2 tông màu
khác nhau cho nửa trước/nửa sau — nhìn PHÁT là thấy "3 rẻ + 3 đắt", đúng nội dung 「安いほうが
3回、高いほうが3回」.

🔴 GIẤY TỜ TRONG ẢNH AI: mọi mock 通知書/振込通知書/期別表 phải CHUNG CHUNG, ô kẻ trống, KHÔNG
chữ thật (media-library §2.10 ⑦) — giấy thật chỉ ở 2 genten screenshot (Claude tự chụp, không
phải việc của user): 世田谷区『介護保険料の納め方』(FACT #1-2) + 上越市『介護保険料』段階表 (FACT #3,
khoanh hàng 第6段階 — khác vùng khoanh với video 14 đã khoanh 第3段階, không lặp hình).

CHẠY:  python tools/build_slides_15.py
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
STEM = "15_nenkin-furikomi-10gatsu-honchoshu"
TTS = PROJ / "03_SCRIPTS" / f"{STEM}_TTS.md"
OUT = PROJ / "03_SCRIPTS" / f"{STEM}_SLIDES.json"

NL = "\n"
CH_PER_SEC, GAP_LINE, GAP_PARA = 5.72, 0.45, 1.0
MIN_SEC = 6.0


def C(match, layout, **kw):
    return {"match": match, "video": True, "stage": dict(layout=layout, **kw)}


def V(match, **kw):
    """Entry VOX (make_vox.py) — dùng RIÊNG cho ảnh thật + annotate, khác hẳn thẻ
    sân khấu `C()`. Chỉ dùng cho beat cảm xúc cần ảnh thật (§VISUAL CLAUDE.md: kênh
    này 100% stage, ngoại lệ 1-2 entry theo đúng đường đã ghi sẵn trong tài liệu).
    `make_vox.py slides ... --only <idx>` chỉ build đúng entry có khoá "vox"."""
    return {"match": match, "video": True, "vox": dict(kind="flow", bg="photo", **kw)}


def N(id_, kind, at, **kw):
    return dict(id=id_, kind=kind, at=at, **kw)


def E(a, b, style="arrow", **kw):
    return dict({"from": a, "to": b, "style": style}, **kw)


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


def line(match, title, sen, uchi, soto, close, why, uchi_dim=False, soto_dim=False,
         left="sensei_explain", right="kikite_think", sub=None):
    return C(match, "zu", title=title, nodes=[
        N("in", "label", [0.08, 0.42], label=uchi, lw=300, dim=uchi_dim),
        N("sen", "label", [0.50, 0.42], label=sen, lw=400, hero=True, under=True),
        N("out", "label", [0.92, 0.42], label=soto, lw=300, dim=soto_dim),
        N("bb", "bubble", [0.58, 0.66], label=why, tail="up", lw=470),
        N("cl", "label", [0.50, 0.99], label=close, lw=560)],
        left=left, right=right, sub=sub)


def twogrp(match, title, l_kw, r_kw, close, edge=None, close_icon=None,
           left="sensei_explain", right="kikite_think"):
    ns = [N("L", "group", [0.16, 0.34], w=386, h=330, fix=True, **l_kw),
          N("R", "group", [0.84, 0.34], w=386, h=330, fix=True, **r_kw),
          N("B", "banner", [0.50, 0.97], w=950,
            **({"icon": close_icon} if close_icon else {}), label=close, fix=True)]
    eg = [E("L", "R", **edge)] if edge else []
    return C(match, "zu", title=title, nodes=ns, edges=eg, left=left, right=right)


def chain(match, title, steps, chip=None, wrong=None, close=None, left="sensei_caution",
          right="kikite_nod", y=0.44):
    ns = ROW([N(f"n{k}", "circle", None, icon=ic, label=lb, fix=True,
                **({"tone": "amber"} if am else {}))
              for k, (ic, lb, am) in enumerate(steps)], y, mingap=104)
    if chip:
        ns = [N("chip", "chip", [0.02, 0.02], label=chip, spark=True, fix=True)] + ns
    eg = [E(f"n{k}", f"n{k+1}", "arrow", tone="ink", w=16) for k in range(len(steps) - 1)]
    if wrong:
        eg.append(E(wrong[0], wrong[1], "arc", tone="ink", x=True, drop=200))
    if close:
        ns = ns + [N("cl", "label", [0.50, 0.99], label=close, lw=560)]
    return C(match, "zu", title=title, nodes=ns, edges=eg, left=left, right=right)


def polish(cards):
    nb = nr = 0
    for c in cards:
        v = c.get("stage")
        if not v or v.get("layout") != "zu":
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
    # ═════════════════════════ COLD OPEN (0:00–0:56)
    # Entry 0 = ẢNH CHỦ THỂ (§2.10 ⑦): thông tuong tháng 10, con số ít hơn thường lệ.
    # ⭐ 2026-08-22 — user chê đoạn mở đứng 1 ảnh quá lâu (19.3s/13.6s), đòi nhịp ~6s/lần đổi.
    # Chèn 2 thẻ CHỮ nhanh (big) vào 2 mốc câu tự nhiên → 4 thẻ cũ (19.3/11.0/13.6/17.7s)
    # thành 6 thẻ (11.2/8.1/11.0/8.0/12.2/11.1s). Sàn 6s của audience-45plus §2 vẫn giữ
    # nguyên (mọi entry ≥6s) — chỉ ÁP RIÊNG đoạn cold open bị chê, không đụng phần sau.
    # ⭐⭐ 2026-08-22 v2 — user: "đánh mạnh vào tâm lý, dùng dạng vox cho sinh động".
    # ẢNH THẬT + annotate thay art vector (ngoại lệ đã ghi sẵn ở §VISUAL CLAUDE.md —
    # "mở lại 1-2 entry ảnh thật cho beat cảm xúc"). Lời đọc GIỮ NGUYÊN (voice.wav
    # không phải render lại) — chỉ đổi lớp chữ hiện TRÊN ảnh + chính tấm ảnh.
    # TODO sau khi có ảnh: đo vị trí số trên thông thật trong ảnh rồi điền pins/arrows
    # (skill video-vox GĐ3b — đặt toạ độ theo chi tiết THẬT, không đoán trước).
    # pins/arrows đo TRÊN ảnh thật đã nhận (skill video-vox GĐ3b) — mũi tên đi từ hàng
    # số phía trên xuống đúng chỗ ngón tay cái đang tì lên cột số dưới.
    V("10月15日、木曜日",
      kicker="10月15日、振込日の朝",
      head="いつもより、1万円以上少ない",
      photo="06_VIDEO/15_nenkin-furikomi-10gatsu-honchoshu/art/vox_tsucho_shock.png",
      # user 2026-08-22: nhãn lên trên, mũi tên chỉ LÊN, tách xa dải chữ vàng đáy.
      arrows=[[1030, 470, 950, 260, 0.22]],
      pins=[[950, 220, "ここが、いつもと違う", 46]]),

    C("年金が減ったわけでは", "big",
      title="年金が減ったわけでは", value="1円も", unit="減っていない",
      cap="なのに、手取りだけが減る",
      left="sensei_serious", right="kikite_worried"),

    C("何も知らずに通帳を見たら", "pict",
      title="役所の間違いでも、詐欺でもありません",
      panels=[{"label": "役所の\n《間違い》？", "img": "art_yakusho_gimon.png"},
              {"label": "還付金の\n《詐欺》？", "img": "art_sagi_denwa15.png",
               "tone": "red"}],
      cap="答えは、もう家の中にあります",
      left="sensei_serious", right="kikite_worried"),

    # mở OPEN-LOOP — trả ở thẻ 「その、10月の欄を」(~8:00)
    C("そして実は、あなたがいくら引かれるのか", "art",
      title="答えを知っている、1枚の紙",
      img="art_1mai_nemuru.png", fly="up",
      cap="7月に届いた、あの紙です",
      left="sensei_point", right="kikite_think"),

    C("7月に届いた、1枚の紙", "big",
      title="7月に届いた、1枚の紙の", value="たった一マス", unit="",
      cap="今日は、あなたの回です",
      left="sensei_point", right="kikite_think"),

    C("10月の朝に慌てないように", "big",
      title="10月の朝に慌てないように", value="その一マスまで", unit="",
      cap="まっすぐご案内します",
      left="sensei_present", right="kikite_nod"),

    # ═════════════════════════ 第1章 中村さんの10月の朝 (0:56–3:03)
    C("新潟県上越市の、中村さん", "art",
      title="新潟県上越市・中村さん（71）",
      img="art_nakamura_daidokoro.png", fly="up",
      cap="おひとり暮らし。40年、学校給食の調理場で",
      left="sensei_explain", right="kikite_listen"),

    C("2通目は、介護保険料が4万9600円上がる", "pict",
      title="前回の、2通の封筒",
      panels=[{"label": "年金額改定通知書\n《＋3万円》", "img": "art_fuutou_nenkin15.png",
               "tone": "green"},
              {"label": "介護保険料決定通知書\n《＋4万9600円》", "img": "art_fuutou_kaigo15.png",
               "tone": "red"}],
      cap="今日はその続き、答え合わせの日です",
      left="sensei_serious", right="kikite_nod"),

    C("中村さんは、振込の日の朝", "art",
      title="振込の日の朝の、習慣",
      img="art_nokyo_kicho.png", fly="up",
      cap="ジジ、ジジ、と印字される音を聞く",
      left="sensei_explain", right="kikite_listen"),

    C("中村さんの年金は、年に150万円", "big",
      title="中村さんの年金は", value="年150万円", unit="",
      cap="振込は2か月分ずつ。1回、25万円です",
      left="sensei_explain", right="kikite_listen"),

    twogrp("引かれる額が、いきなり3倍以上に", "引かれる額が、いきなり3倍以上に",
           dict(tone="ink", head="8月", hero="24万3千円", foot="いつもどおり",
                under=True),
           dict(tone="amber", head="10月", hero="22万7千円", foot="どういうわけか",
                under=True),
           "――1万6千500円、少ない",
           edge=dict(style="arrow", tone="amber", w=18),
           left="sensei_serious", right="kikite_surprised"),

    C("印字の音は、いつもと同じです", "pict",
      title="印字の音は、いつもと同じ",
      panels=[{"label": "「役所が、間違えた\nんじゃないの」",
               "img": "art_nakamura_gimon.png", "tone": "paper"}],
      cap="数字だけが、違う",
      left="sensei_caution", right="kikite_worried"),

    C("しかも、このずれには", "big",
      title="増えるのは、なぜかいつも", value="10月", unit="",
      cap="4月でも、6月でもなく",
      left="sensei_point", right="kikite_surprised"),

    # ═════════════════════════ 第2章 仮徴収と本徴収 (3:03–5:27)
    twogrp("年金から引かれる介護保険料には", "値段の決め方は、《ふたつ》",
           dict(tone="ink", head="前半", icon="calendar", iconsize=110,
                foot="仮徴収"),
           dict(tone="amber", head="後半", icon="calendar", iconsize=110,
                foot="本徴収"),
           "4月・6月・8月 と 10月・12月・2月",
           left="sensei_point", right="kikite_listen"),

    C("役所のページに、そのまま書いてあります", "art",
      title="原典：世田谷区『介護保険料の納め方』",
      img="genten_15_setagaya_karichoshu.png", fly="up",
      cap="赤で囲んだところ ＝ 仮徴収・本徴収のしくみ",
      left="sensei_point", right="kikite_think"),

    spine("「原則として、前年度の2月と", "仮徴収は、《去年の値段》",
          "去年の2月", "同じ金額", "前半3回は、去年の\n値段のままです",
          "新しい値段が決まるまで、いままでの値段で",
          left="sensei_explain", right="kikite_nod"),

    C("昔の、お米屋さんのツケに似ています", "pict",
      title="お米屋さんの、ツケに似ています",
      panels=[{"label": "値上げが決まるまでは\n《いままでの値段》で",
               "img": "art_komeya_tsuke.png", "tone": "paper"}],
      cap="差額は、あとでまとめて払う",
      left="sensei_explain", right="kikite_nod"),

    C("では、今年の値段は、いつ決まるのか", "big",
      title="今年の値段が決まるのは", value="7月", unit="",
      cap="決定通知書＝「今年の値段表」",
      left="sensei_point", right="kikite_surprised"),

    spine("今年の年額から、前半に仮払いした分を", "本徴収は、《残りを3で割った額》",
          "今年の年額", "－仮払い分\n÷3", "10月・12月・2月の\n1回分になります",
          "決まるのは7月、通帳に出るのは10月",
          left="sensei_explain", right="kikite_think"),

    # ═════════════════════════ 中村さんの数字にあてはめる (4:31–5:27)
    C("この、前半と後半の仕組みそのものは", "art",
      title="原典：上越市『介護保険料』（段階表）",
      img="genten_16_joetsu_dankai.png", fly="up",
      cap="赤で囲んだところ ＝ 第6段階（中村さんの今年）",
      left="sensei_point", right="kikite_think"),

    spine("中村さんの保険料は、去年の3万9500円から", "中村さんの、段階の変化",
          "去年\n3万9500円", "今年\n8万9100円", "差額は、\n4万9600円",
          "でも、前半3回は去年の値段のままでした",
          left="sensei_serious", right="kikite_worried"),

    C("払ったのは、合わせて、およそ2万円だけです", "big",
      title="前半3回で払った、仮の分", value="およそ2万円", unit="",
      cap="上がった分は、まだ払っていません",
      left="sensei_explain", right="kikite_think"),

    spine("それがそっくり、後ろ半分の3回に", "後半3回に、のしかかる額",
          "残額\n69,300円", "÷3\n＝23,100円", "上がった分の全部と\n足りなかった分",
          "8月との差が、あの1万6千500円です",
          left="sensei_serious", right="kikite_surprised"),

    C("値上げそのものは、4月から始まっていました", "check",
      title="ずれの正体は、《半年》", bgimg="bg_calendar_toki.png",
      no=["値上げが始まったのは、4月から"],
      ok=["通帳が知らされるのは、10月"],
      left="sensei_serious", right="kikite_nod"),

    # ═════════════════════════ 計算タイム：1年6回の振込 (5:27–6:52)
    C("では、1年を、通帳の目線で並べてみます", "bars",
      title="中村さんの、6回の振込（介護保険料）",
      label_w=210, max=25000,
      rows=[["4月", 6600, "grey", "6千600円"],
            ["6月", 6600, "grey", "6千600円"],
            ["8月", 6600, "grey", "6千600円"],
            ["10月", 23100, "bad", "2万3100円"],
            ["12月", 23100, "bad", "2万3100円"],
            ["2月", 23100, "bad", "2万3100円"]],
      left="sensei_explain", right="kikite_surprised"),

    C("そして、10月。2万3千100円", "big",
      title="段差は、一度だけ", value="8月と10月の間", unit="",
      cap="12月・来年2月も、同じ額が続きます",
      left="sensei_explain", right="kikite_nod"),

    C("ここで、ひとつ、大事な確認をさせてください", "big",
      title="1年分を全部足すと", value="8万9100円", unit="",
      cap="今年の決定額と、ぴったり同じ",
      left="sensei_explain", right="kikite_nod"),

    C("取られる時期が、後ろに寄っただけなんです", "check",
      title="正体は、脅しでも罰でもなく", bgimg="bg_denpyo_seisan.png",
      no=["1円も、多く取られてはいない"],
      ok=["前半が安すぎたぶんの、精算"],
      left="sensei_reassure", right="kikite_relieved"),

    C("私たちも、この6回の表を実際に手で書いてみました", "art",
      title="実際に、手で書いてみました",
      img="art_hyou_tegaki.png", fly="up",
      cap="書いてみると、怖さがすっと消えます",
      left="sensei_present", right="kikite_nod"),

    # ═════════════════════════ CTA (~49%)
    C("ここで、ひとつだけお願いです", "source",
      title="この研究室について",
      org="年金と老後のお金研究室",
      doc="高評価・シェア・コメントが" + NL + "次の研究テーマになります",
      note="※ご感想や、調べてほしいテーマをお寄せください",
      left="sensei_present", right="kikite_nod"),

    C("ご感想や、調べてほしいテーマがあれば", "big",
      title="ご感想・リクエスト", value="コメント欄へ", unit="",
      cap="皆さまの声が、次の研究テーマになります",
      left="sensei_present", right="kikite_nod"),

    # ═════════════════════════ 第4章 冒頭の約束——あの一マス (7:24–8:14)
    C("さて、冒頭の約束を、果たします", "art",
      title="答えの紙 ＝ 7月の決定通知書",
      img="art_kettei_tsuchisho.png", fly="up",
      cap="紙のなかの、「期別」の表です",
      left="sensei_point", right="kikite_surprised"),

    C("表の名前は、市区町村によって少し違います", "check",
      title="表の名前は、いろいろでも", bgimg="bg_tsuchisho_hyou.png",
      ok=["10月から欄が並んでいれば、それです"],
      no=["期別徴収額・徴収予定額など、呼び方は様々"],
      left="sensei_explain", right="kikite_think"),

    C("10月15日にあなたの通帳で起きることは", "big",
      title="10月の欄に、すでに", value="印刷済み", unit="",
      cap="計算も、予想も、要りません",
      left="sensei_point", right="kikite_surprised"),

    # ═════════════════════════ 3つの場合（+ 2つの誤解を統合）(8:14–10:37)
    C("そのうえで、ご自分がどの場合にあたるか", "zu", title="あなたは、どの場合ですか",
      nodes=[N("a", "circle", [0.10, 0.38], num=1, icon="checklist",
               label="変わらず"),
             N("b", "circle", [0.42, 0.38], num=2, icon="chart_up", tone="amber",
               label="上がった"),
             N("c", "circle", [0.74, 0.38], num=3, icon="person", label="新しく対象"),
             N("cl", "label", [0.50, 0.99], label="ひとつずつ、確かめます", lw=560)],
      left="sensei_explain", right="kikite_think"),

    C("7月の通知の額が、去年とほとんど変わらなかったかた", "check",
      title="①変わらなかったかた", bgimg="bg_tsuchisho_calm.png",
      ok=["10月も、8月とほぼ同じ", "答え合わせだけで、大丈夫"],
      left="sensei_reassure", right="kikite_relieved"),

    spine("ふたつめ。中村さんのように、額が上がっていたかた", "②上がったかたの、目安",
          "上がった年額\n÷3", "＋いまの1回分", "中村さんの数字で試すと\n2万3100円に戻ります",
          "上がった分が、10月からの3回にまとめて乗ります",
          left="sensei_explain", right="kikite_nod"),

    C("ここで、ひとつだけ、はっきりさせておきます", "check",
      title="「年金が減らされた」わけでは、ない", bgimg="bg_tsuchisho_nenkin.png",
      no=["年金支払額の欄は、8月と同じ", "変わったのは、引かれる側だけ"],
      left="sensei_reassure", right="kikite_relieved"),

    C("みっつめ。今年から新しく対象になったかた", "pict",
      title="③新しく対象になったかた",
      panels=[{"label": "65歳になった／\n引っ越してきた", "img": "art_65sai_hikkoshi.png"}],
      cap="天引きは、まだ始まっていないことが多い",
      left="sensei_explain", right="kikite_listen"),

    C("この春65歳になって、納付書が届いて", "check",
      title="「二重払いでは」の、答え", bgimg="bg_noufusho_shinpai.png",
      no=["通帳から引かれていなければ、二重ではない"],
      ok=["切り替えは、半年〜1年後に自動"],
      left="sensei_reassure", right="kikite_relieved"),

    C("手続きは、要りません。何かを間違えたわけでも", "check",
      title="この切り替わりは、全員、自動です", bgimg="bg_denwa_yakusho.png",
      no=["間違えようが、ない"],
      ok=["「そういう仕組みです」が答え"],
      left="sensei_explain", right="kikite_nod"),

    C("中村さんに届いた住民税5千円の案内も", "pict",
      title="中村さんの、住民税5千円も",
      panels=[{"label": "今年は\n《納付書》でした", "img": "art_juminzei_noufusho.png",
               "tone": "paper"}],
      cap="年金天引きは、来年度からの見込みです",
      left="sensei_explain", right="kikite_nod"),

    C("なお、75歳からの後期高齢者医療保険料も", "big",
      title="75歳からの、後期高齢者医療保険料も", value="同じ二段構え", unit="",
      cap="仮の姿は、切り替えを待つあいだだけ",
      left="sensei_conclude", right="kikite_nod"),

    # ═════════════════════════ 来年の見通し + どの紙を信じるか (11:00–11:57)
    C("最後に、ひとつだけ、来年の話をしておきます", "check",
      title="来年も、12月だけ多くなる？", bgimg="bg_calendar_2027.png",
      no=["そうとは限りません"],
      ok=["段階が同じなら、来年は段差なし"],
      left="sensei_explain", right="kikite_nod"),

    C("来年の4月は、また「今年の2月と同じ額」から", "big",
      title="来年4月は、また", value="今年2月と同額", unit="から",
      cap="市区町村により、途中で調整が入ることも",
      left="sensei_explain", right="kikite_nod"),

    spine("もうひとつだけ。6月に年金機構から届いた", "どちらの紙を、信じるか",
          "6月の紙\n予定額", "7月の紙\n決定額", "新しい紙が、\n正しい紙です",
          "信じる順番は、7月の紙が先",
          left="sensei_point", right="kikite_nod"),

    # ═════════════════════════ 中村さんの締め + 研究ノート (11:57–13:14)
    C("先日、中村さんは、新潟市のお姉さんに電話で", "pict",
      title="お姉さんへの、電話",
      panels=[{"label": "「あんた、\n詳しくなったねえ」",
               "img": "art_nakamura_denwa.png", "tone": "paper"}],
      cap="少し得意そうでした",
      left="sensei_reassure", right="kikite_relieved"),

    C("それでは、今日の研究ノートです", "check",
      title="研究ノート（前半）", bgimg="bg_note_pen15.png",
      ok=["前半4・6・8月は「去年の値段」", "後半10・12・2月が、精算",
          "上がった分は、後半3回にまとめて乗る"],
      left="sensei_conclude", right="kikite_nod"),

    C("10月にいくら引かれるかは、7月の決定通知書の", "check",
      title="研究ノート（後半）", bgimg="bg_note_pen15.png",
      ok=["答えは、期別の表に印刷済み", "年金そのものは、1円も減っていない",
          "新しく対象の方は、しばらく納付書"],
      left="sensei_conclude", right="kikite_nod"),

    C("7月の決定通知書を出してきて、期別の表の", "steps",
      title="今日のお願いは、ひとつだけ", bgimg="bg_tsuchisho_maru.png",
      steps=["7月の決定通知書を出す", "期別の表の10月欄を見る",
             "丸を、ひとつつける"],
      left="sensei_present", right="kikite_nod"),

    chain("さて、次回です", "次回：12月の年金だけ、振込額が違う",
          [("calendar", "12月15日", False), ("docs", "所得税", False),
           ("money_pouch", "精算で還付", True)],
          chip="次回予告",
          close="取られすぎていた分が、戻ってくる方がいます",
          left="sensei_point", right="kikite_think"),

    C("なお、この動画は2026年8月時点の情報です", "source",
      title="ご確認のお願い",
      org="年金と老後のお金研究室",
      doc="保険料の額や納め方は、" + NL + "お住まいの市区町村で変わります",
      note="※ご自分の数字は、7月の決定通知書と市区町村の窓口でご確認ください",
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
        v = c.get("stage")
        if not v:
            continue
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
        v = c.get("stage")
        if not v:
            continue
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
        v = c.get("stage")
        if not v:
            continue
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

    for k, c in enumerate(CARDS):
        v = c.get("stage")
        if not v:
            continue
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
    stg = [c["stage"] for c in CARDS if c.get("stage")]
    dist = collections.Counter(v["layout"] for v in stg)
    n_vox = sum(1 for c in CARDS if c.get("vox"))
    if n_vox:
        dist["vox"] = n_vox
    sp = [i for i, c in enumerate(CARDS)
          if c.get("stage", {}).get("layout") == "zu"
          and any(x["id"] == "old" for x in c["stage"]["nodes"])]
    art = sorted({v[x] for v in stg for x in ("img", "fill", "bgimg") if v.get(x)}
                 | {p["img"] for v in stg for p in v.get("panels", [])
                    if isinstance(p, dict) and p.get("img")}
                 | {c["vox"]["photo"] for c in CARDS
                    if c.get("vox", {}).get("photo")})
    print(f"✅ ghi {OUT.name}  —  {n} thẻ  ·  video {int(dur)//60}:{int(dur)%60:02d}")
    print(f"   nhịp: {n/(dur/60):.2f} đổi hình/phút (trần 6)  ·  "
          f"entry: min {min(holds):.1f}s · TB {dur/n:.1f}s · max {max(holds):.1f}s")
    print(f"   layout: {dict(dist)}")
    print(f"   TRỤC HÌNH — spine (số cũ→mới): {sp}  ·  bars (6 kỳ): "
          f"{[i for i, c in enumerate(CARDS) if c.get('stage', {}).get('layout') == 'bars']}")
    print(f"   ảnh cần có ({len(art)}): {art}")


if __name__ == "__main__":
    main()
