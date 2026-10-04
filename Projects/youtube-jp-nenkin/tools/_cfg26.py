# -*- coding: utf-8 -*-
r"""_cfg26.py — KHOI CAU HINH rieng cua video 26, tach khoi `build_remotion_26.py`.

Tach ra de builder giu nguyen phan CO KHI cua ban 25 (hop khoi chu, phep tu co co,
chia shot, chia phu de, 6 gate) — chi doi DU LIEU. Sua noi dung video thi sua o day.
"""

# ── 原典: khoa GENTEN cua `_scenes26` -> CAC CHANG the (make_genten_26.py) ──
# Mot khoa = 2-3 the CUNG mot vung cat, khac CHO KHOANH DO. Su kien hinh cua scene 原典
# den tu **doi cho khoanh**, khong tu pan (bai hoc lo i2v video 22 muc 5 + muc 15).
GT_STAGES = {
    "shinjuku_dankai": ["genten_sj_setai1.png", "genten_sj_setai2.png"],
    "joetsu_dankai":   ["genten_jt_dan3.png", "genten_jt_dan5.png"],
    "mhlw_kaigo":      ["genten_mhlw.png", "genten_mhlw_8ki.png", "genten_mhlw_9ki.png"],
    "shinjuku_9ki":    ["genten_9ki_13.png", "genten_9ki_18.png"],
}

# ── 22 KHOI gfx — loi VERBATIM tu narration cua CHINH scene do ──────────────
# ⚖️ YMYL: khong mot con so / che do nao khong co trong loi doc cua scene ay.
# 📐 Nham >=2-3 dong (LUAT BA KHOI) khi scene du dai; scene <4s thi 1 dong cho khoi
#    khong bi nen. `*` dau dong = dong CHOT (duoc nhan).
GFX = {
    8:  ["あなたの所得|では決まりません",
         "*同じ屋根の下のかたの所得|でも決まります"],
    9:  ["一つ目|なぜ、あなたの段階はそこなのか",
         "*二つ目|そして、動かせるのか"],
    11: ["*まず|事実から"],
    16: ["*市区町村は|何を見て決めているのか"],
    17: ["*三つです|いくつ言えますでしょうか"],
    21: ["第一段階から第三段階|この三つに入る条件は",
         "*たった一行|です"],
    27: ["*あなたの段階は|あなたが決めていません"],
    34: ["同じ世帯に|課税のかたが一人増えると",
         "*いくら変わるのか|一緒に計算します"],
    40: ["*ここからが|今日いちばんお伝えしたいところ"],
    47: ["ご自宅を|思い浮かべてください",
         "あなたと同じ世帯に|住民税が課税されているかた",
         "*何人|いらっしゃいますか"],
    57: ["制度を|責めたいのではありません",
         "*知らずにぶつかると|ただ痛いだけだから"],
    59: ["*二つ目の問い|動かせるのか"],
    60: ["*まず|よくある誤解を片づけます"],
    62: ["*答え|下がりません"],
    67: ["*本当に動くものは|三つあります"],
    69: ["*二つ|世帯の課税状況が変わること"],
    75: ["*最後に|数字を三つだけ"],
    80: ["*それでは|今日の研究ノートです"],
    87: ["*三つ目まで数えて|はじめて理由が分かります"],
    94: ["制度を読む|チャンネルではありません",
         "*あなたの数字を計算する|研究室です"],
    95: ["*さて|次回です"],
    99: ["時点|令和8年9月",
         "段階の数・金額・軽減制度|市区町村によって変わります",
         "*ご判断の前に|市区町村の介護保険担当窓口へ"],
}

# ── fx "hoa la canh": THUA + moi variant <=2 lan ────────────────────────────
# 12 fx tren 101 scene = 0,91/phut — DIEM NHAN, khong phai nhip.
# ⛔ KHONG dung `confetti`: bai nay khong co beat TIN VUI nao (tien TANG len, khong
#    phai tien nhan ve) — nhet vao la trang tri vo nghia, dung bai hoc video 22 muc 10.
FX = {
    5:  ("glow",     20, None),       # 「玄関の内側に何人住んでいるか」 — cau chot cold open
    9:  ("sparkle",  16, None),       # gfx lo trinh 2 muc
    20: ("arrow",    14, None),       # 「いちばん効くのは一つ目です。世帯。」 — PAYOFF so
    40: ("rays",     14, None),       # 「ここからが、今日いちばんお伝えしたいところ」
    46: ("vignette", 12, "full"),     # 「三つの扉が閉まります」 — beat nang nhat
    50: ("coins",    18, None),       # formula 「差は三万七千九百円」 — dinh so cua bai
    56: ("arrow",    12, None),       # 「娘さんが優しいほど、保険料は上がる」
    62: ("stampx",    1, "gfxleft"),  # 「下がりません」 — PHU DINH, dau ✗ navy
    75: ("sparkle",  14, None),       # 「最後に、数字を三つだけ」
    80: ("rays",     12, None),       # gfx 研究ノート — chot bai
    92: ("coins",    16, None),       # stat 「一年の差 3万7,900円」 — callback so
    98: ("vignette", 10, "full"),     # 「一度に両方は取れない」 — tien cao next
}
