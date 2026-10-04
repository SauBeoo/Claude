# -*- coding: utf-8 -*-
"""SCENES / STAT / FORMULA / PUNCH cho video 24 (年金生活者支援給付金・9月の緑の封筒).
Import bởi build_remotion_24.py. pad_sup/cap_reuse dùng chung từ _scenes19.py.

45 scene, mọi gap ≥6.4s (kiểm tay trước khi ghi — chỗ hẹp nhất L37→L38 = 6.4s,
L41→L42 = 6.5s). 2 peak: L=0 (mở phong bì) · L=39 (来ませんでした, callback open-loop).
6 punch. Cast dùng ĐÚNG 10 pose đã có sẵn ratio trong build_remotion_19.py — không cần đo mới.
"""

NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#E0A32A"
GET, LOSE = "#2E6B4F", "#A82026"

SCENES = [
    # ── COLD OPEN (0–72s) ───────────────────────────────────────────────
    dict(L=0,  tag="緑の封筒", heroes=["card_24_futou", "card_24_futou_b"], sup=[], peak=0,
         l="sensei_present", r="kikite_listen",    sp=["#B44A4A", "#C8B88A"]),
    dict(L=1,  tag="切手一枚のあいだ", hero=None, stat="nazo", sup=["el_stamp"],
         l="sensei_point",   r="kikite_surprised", sp=["#C87A72", "#8A93A8"]),
    dict(L=2,  tag="対象は",   heroes=["card_24_taisho"], sup=["el_signpost"],
         l="sensei_present", r="kikite_listen",    sp=["#9FB6C8", "#C8B88A"]),
    dict(L=3,  tag="三つのこと", hero=None, stat="junban", sup=["el_hand_stop"],
         l="sensei_point",   r="kikite_think",     sp=["#8FA9C0", "#C8B88A"]),
    dict(L=4,  tag="もうひとつ", heroes=["card_24_tomaru"], sup=["el_magnifying_glass"],
         l="sensei_caution", r="kikite_worried",   sp=["#8A93A8", "#C87A72"]),
    dict(L=5,  tag="研究室です", heroes=["card_24_kenkyu"], sup=["el_newspaper"],
         l="sensei_present", r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    # ── 第1章 誰に届くのか (88–188s) ────────────────────────────────────
    dict(L=6,  tag="誰に届くのか", heroes=["card_24_yubinbako", "card_24_yubinbako_b"], sup=["el_green_envelope"],
         l="sensei_serious", r="kikite_think",     sp=["#C8B88A", "#9FB6C8"]),
    dict(L=7,  tag="原典・年金機構①", heroes=["card_genten24_01", "card_genten24_01_b"], sup=["el_magnifying_glass"],
         l="sensei_point",   r="kikite_listen",    sp=["#8A93A8", "#8FA9C0"]),
    dict(L=8,  tag="はがき型請求書", heroes=["card_24_naka"], sup=["el_hagaki"],
         l="sensei_present", r="kikite_listen",    sp=["#C8B88A", "#9FB6C8"]),
    dict(L=9,  tag="新たに対象", heroes=["card_24_aratani"], sup=["el_newspaper"],
         l="sensei_present", r="kikite_think",     sp=["#9FB6C8", "#C8B88A"]),
    dict(L=10, tag="条件は三つ", hero=None, stat="jouken", sup=["el_hand_stop"],
         l="sensei_point",   r="kikite_listen",    sp=["#9FB6C8", "#8A93A8"]),
    dict(L=12, tag="世帯の全員", heroes=["card_24_setai", "card_24_setai_b"], sup=["el_hand_stop"],
         l="sensei_caution", r="kikite_worried",   sp=["#C87A72", "#8A93A8"]),
    dict(L=13, tag="去年の数字", heroes=["card_24_kyonen"], sup=["el_calendar"],
         l="sensei_present", r="kikite_think",     sp=["#C8B88A", "#9FB6C8"]),
    # ── 第2章 あなたの金額 (208–442s) — モニター 渡辺さん ────────────────
    dict(L=14, tag="あなたの金額", heroes=["card_24_keisan"], sup=["el_coin_stack"],
         l="sensei_present", r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    dict(L=15, tag="原典・年金機構②", heroes=["card_genten24_02", "card_genten24_02_b"], sup=["el_magnifying_glass"],
         l="sensei_point",   r="kikite_listen",    sp=["#8FA9C0", "#8A93A8"]),
    dict(L=16, tag="六万七千円が基準", hero=None, stat="kijun", sup=["el_coin_stack"],
         l="sensei_present", r="kikite_surprised", sp=["#C87A72", "#C8B88A"]),
    dict(L=17, tag="渡辺さん", heroes=["card_24_watanabe", "card_24_watanabe_b"], sup=["el_nenkin_techo"],
         l="sensei_present", r="kikite_listen",    sp=["#C8B88A", "#9FB6C8"]),
    dict(L=18, tag="はがきを読む", heroes=["card_24_watanabe_hagaki", "card_24_watanabe_hagaki_b"], sup=["el_hagaki"],
         l="sensei_point",   r="kikite_think",     sp=["#9FB6C8", "#C8B88A"]),
    dict(L=19, tag="審査結果の通知", heroes=["card_24_tsuchi"], sup=["el_newspaper"],
         l="sensei_present", r="kikite_listen",    sp=["#8A93A8", "#9FB6C8"]),
    dict(L=20, tag="三つの段",  hero=None, stat="dankai", sup=["el_percent_badge"],
         l="sensei_point",   r="kikite_listen",    sp=["#9FB6C8", "#8A93A8"]),
    dict(L=22, tag="渡辺さんの年金", heroes=["card_24_watanabe_kingaku"], sup=["el_coin_stack"],
         l="sensei_present", r="kikite_think",     sp=["#C8B88A", "#9FB6C8"]),
    dict(L=23, tag="割ってみます", hero=None, formula="wari24", sup=["el_percent_badge"],
         l="sensei_point",   r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    dict(L=25, tag="この線の細さ", heroes=["card_24_zero"], sup=["el_zero_stamp"],
         l="sensei_caution", r="kikite_worried",   sp=["#B44A4A", "#8A93A8"]),
    dict(L=27, tag="免除の期間", heroes=["card_24_menjo"], sup=["el_percent_badge"],
         l="sensei_point",   r="kikite_think",     sp=["#9FB6C8", "#C8B88A"]),
    dict(L=28, tag="別枠の給付金", heroes=["card_24_shougai"], sup=["el_signpost"],
         l="sensei_present", r="kikite_listen",    sp=["#8FA9C0", "#8A93A8"]),
    dict(L=29, tag="いちばん割のいい葉書", heroes=["card_24_kitte", "card_24_kitte_b"], sup=["el_stamp"],
         l="sensei_reassure",r="kikite_relieved",  sp=["#C8B88A", "#9FB6C8"]),
    dict(L=31, tag="灯油代のぶん", heroes=["card_24_touyu"], sup=["el_house_bills"],
         l="sensei_present", r="kikite_relieved",  sp=["#9FB6C8", "#C8B88A"]),
    dict(L=32, tag="お願いです", heroes=["card_24_cta"], sup=["el_smartphone"],
         l="sensei_reassure",r="kikite_relieved",  sp=["#C8B88A", "#9FB6C8"]),
    # ── 第3章 対象なのに来ない (470–586s) — モニター 中村さん ────────────
    dict(L=33, tag="対象なのに来ない", heroes=["card_24_konai"], sup=["el_signpost"],
         l="sensei_serious", r="kikite_think",     sp=["#8A93A8", "#8FA9C0"]),
    dict(L=34, tag="三か月以内", heroes=["card_24_3kagetsu"], sup=["el_calendar"],
         l="sensei_caution", r="kikite_worried",   sp=["#C87A72", "#9FB6C8"]),
    dict(L=35, tag="世帯構成の変更", heroes=["card_24_henkou"], sup=["el_signpost"],
         l="sensei_present", r="kikite_think",     sp=["#8A93A8", "#9FB6C8"]),
    dict(L=36, tag="機構ではなく、あなた", hero=None, stat="jibunde", sup=["el_hand_stop"],
         l="sensei_point",   r="kikite_listen",    sp=["#9FB6C8", "#8A93A8"]),
    dict(L=37, tag="冒頭の答え", heroes=["card_24_tomaru_2"], sup=["el_magnifying_glass"],
         l="sensei_serious", r="kikite_think",     sp=["#8A93A8", "#8FA9C0"]),
    dict(L=38, tag="中村さん", heroes=["card_24_nakamura", "card_24_nakamura_b"], sup=["el_nenkin_techo"],
         l="sensei_present", r="kikite_listen",    sp=["#C8B88A", "#9FB6C8"]),
    dict(L=39, tag="来ませんでした", heroes=["card_24_tomatta", "card_genten24_03"], sup=[], peak=39,
         l="sensei_caution", r="kikite_surprised", sp=["#B44A4A", "#C87A72"]),
    dict(L=41, tag="再開のボタンは、あなたの側に", heroes=["card_24_saikai"], sup=["el_hand_stop"],
         l="sensei_serious", r="kikite_think",     sp=["#8A93A8", "#C87A72"]),
    dict(L=42, tag="相談先",   heroes=["card_24_soudan"], sup=["el_smartphone"],
         l="sensei_present", r="kikite_listen",    sp=["#8FA9C0", "#8A93A8"]),
    dict(L=43, tag="消えないペンで丸", heroes=["card_24_calendar_maru", "card_24_kigen"], sup=["el_calendar"],
         l="sensei_present", r="kikite_relieved",  sp=["#C8B88A", "#9FB6C8"]),
    # ── 第4章 期限 (624–675s) ───────────────────────────────────────────
    dict(L=45, tag="提出期限", heroes=["card_24_ichigatsu"], sup=["el_calendar"],
         l="sensei_present", r="kikite_think",     sp=["#9FB6C8", "#C8B88A"]),
    dict(L=46, tag="翌月分から", hero=None, stat="okure", sup=["el_chart_down"],
         l="sensei_caution", r="kikite_worried",   sp=["#C87A72", "#8A93A8"]),
    dict(L=47, tag="ATMの操作", heroes=["card_24_sagi"], sup=["el_smartphone"],
         l="sensei_serious", r="kikite_worried",   sp=["#8A93A8", "#C87A72"]),
    # ── 研究ノート + セルフチェック + 次回 (675–779s) ─────────────────────
    dict(L=49, tag="研究ノート", hero=None, stat="note", sup=["el_nenkin_techo"],
         l="sensei_present", r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    dict(L=53, tag="セルフチェック", hero=None, stat="self", sup=["el_magnifying_glass"],
         l="sensei_point",   r="kikite_think",     sp=["#9FB6C8", "#8A93A8"]),
    dict(L=54, tag="次の支給日の前にも", heroes=["card_24_cta2"], sup=["el_teacup"],
         l="sensei_reassure",r="kikite_relieved",  sp=["#C8B88A", "#9FB6C8"]),
    dict(L=56, tag="次回予告", heroes=["card_24_yokoku", "card_24_yokoku_b"], sup=["el_nenkin_techo"],
         l="sensei_reassure",r="kikite_relieved",  sp=["#8FA9C0", "#C8B88A"]),
]

# ── bảng số (papercut-stat) · mọi con số kế thừa FACT SHEET verify 2026-08-10 ──
STAT = {
    "nazo": (f"{GET}|出せば|もらえる" + NL + f"{LOSE}|出さなければ|0円"
             + NL + "*あいだにあるのは|切手一枚", 58),
    "junban": ("①誰に|届くのか" + NL + "②いくら|なのか"
               + NL + "*③来ない時|どう動くか", 58),
    "jouken": ("①年齢|65歳以上・老齢基礎年金を受給" + NL + "②世帯|全員が住民税非課税"
               + NL + "*③前年の所得|基準額以下", 54),
    "kijun": ("基準額|月5,620円" + NL + "40年納付なら|そのまま"
              + NL + "*年にすると|およそ6万7千円", 56),
    "dankai": (f"{GET}|80万9千円以下|満額・年およそ6万7千円" + NL
               + "80万9千円〜90万9千円|補足的・率で減る" + NL
               + f"{LOSE}|*90万9千円超|0円", 52),
    "jibunde": (f"{LOSE}|機構は|待つだけ" + NL + f"{GET}|*動くのは|あなたの側", 60),
    "okure": ("期限内に届けば|10月分から遡り" + NL + "*期限を過ぎたら|請求した月の翌月分から", 54),
    "note": ("一｜緑の封筒は9月の第1営業日から順次届く" + NL
             + "二｜基準は月額5,620円、渡辺さんは月2,529円だった" + NL
             + "三｜世帯の変化で対象になった方は、自分から手続きする" + NL
             + "*四｜一度止まったら、再開も自分から", 46),
    "self": ("①世帯は全員|住民税非課税ですか" + NL + "②前年の所得は|90万9千円以下ですか"
             + NL + "*③9月の郵便受けを|もう確かめましたか", 54),
}

# ── công thức (papercut-formula) — chia lại từ số đã verify ────────────────
FORMULA = {
    "wari24": ("4万5千円 ÷ 10万円 ≒ 0.45", 80),
}

# ── punch banner (chữ, không cần asset) ────────────────────────────────────
PUNCH = [
    (9,  "対象は、去年ではなく、今年のあなたかもしれません", INK),
    (13, "お子さんの独立が、条件を変えます",                INK),
    (24, "月2,529円、年およそ3万円",                        AMBER),
    (26, "この線の細さが、この制度の顔です",                INK),
    (37, "止まったまま、戻らなかった給付金",                LOSE),
    (48, "切ってください",                                  RED),
]

# ── SFX đỉnh bài (2 peak) ───────────────────────────────────────────────────
SFX = {0: ("sfx/paper.wav", 0.30), 39: ("sfx/drop.wav", 0.30)}

# pad_sup / cap_reuse dùng chung từ _scenes19.py — import ở builder, không chép lại.
POOL = [
    "el_coin_stack", "el_calendar", "el_percent_badge", "el_hand_stop", "el_signpost",
    "el_newspaper", "el_nenkin_techo", "el_magnifying_glass", "el_chart_up", "el_chart_down",
    "el_kyuryo_meisai", "el_passbook", "el_smartphone", "el_house_bills", "el_mynumber_card",
    "el_speaker_robot", "el_teacup", "el_two_men_desk", "el_zero_stamp",
    "el_senior_phone", "el_burst_red", "el_green_envelope", "el_hagaki", "el_stamp",
]
