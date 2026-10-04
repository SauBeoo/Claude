# -*- coding: utf-8 -*-
r"""telop28.py — chữ hiện trên khung cho 92 ô của video 28.

LUẬT VIẾT TELOP (giữ nguyên từ v27, đừng sửa nếu chưa đọc):
  · Chữ rút TỪ CHÍNH lời đọc của ô đó. ⛔ Không thêm số mới, không thêm chế độ mới —
    YMYL: mọi số phải đã có trong `_TTS.md` và FACT SHEET (`nenkin/CLAUDE.md` §③).
  · Dòng chính ≤ 9 ký full-width/dòng, tối đa 2 dòng → đọc được ở điện thoại.
  · `circle=True` chỉ cho dòng CÓ SỐ và chỉ ở khoảnh khắc lật.
  · màu: NAVY mặc định · RED cho mất mát/cảnh báo · TEAL cho phần được/giải pháp.
  · `sub` = thẻ trắng viền navy, ≤4 thẻ, mỗi thẻ ≤ 11 ký.

📌 Mọi con số dưới đây đã đối chiếu với `_TTS.md`: 7,989 · 95,875 · 56,083 · 1,351 · 49,200 ·
   1,148 · 52,370 · 2,182 · 8,189 · 10,352 · 4,990 · 6万4千 · 26,185 · 194 · 578 · 18万.
"""
NAVY, RED, TEAL = (31, 56, 100), (192, 57, 43), (62, 124, 120)

TELOP = {
  # ── cold open ──────────────────────────────────────────────────────────────
  0:  dict(big=["七十五歳の", "誕生日"], color=NAVY),
  1:  dict(big=["計算式が", "変わります"], color=RED),
  2:  dict(big=["月7,989円"], color=RED, size=120, circle=True,
           sub=["全国平均", "年95,875円"]),
  3:  dict(big=["七月に届く", "茶色い封筒"], color=NAVY, sub=["保険料額決定通知書"]),
  4:  dict(big=["書いていない", "ものが一つ"], color=RED),
  5:  dict(big=["誰も", "教えてくれません"], color=RED),
  6:  dict(big=["三つのうち一つ", "負担が三倍に"], color=RED),
  7:  dict(big=["まず、事実から"], color=NAVY),
  # ── 第1章 誕生日当日 ───────────────────────────────────────────────────────
  8:  dict(big=["七十四歳までは", "どちらかの保険"], color=NAVY),
  9:  dict(big=["誕生日当日に", "全員が移ります"], color=NAVY),
  10: dict(big=["申請は", "要りません"], color=RED),
  11: dict(big=["誕生月から", "月割で計算"], color=NAVY),
  12: dict(big=["二つの請求が", "重なって見える"], color=NAVY),
  13: dict(big=["二重払いでは", "ありません"], color=TEAL),
  14: dict(big=["均等割と", "所得割"], color=NAVY),
  15: dict(big=["均等割 年", "5万6,083円"], color=NAVY, sub=["所得割 10.17%"]),
  16: dict(big=["月7,989円"], color=RED, size=120, circle=True, sub=["厚生労働省", "令和8年4月10日"]),
  17: dict(big=["毎月引かれる", "額の目安"], color=NAVY),
  18: dict(big=["年金額から", "引いてみる"], color=NAVY),
  # ── 第2章 子ども・子育て支援金 ─────────────────────────────────────────────
  19: dict(big=["子ども・子育て", "支援金"], color=NAVY),
  20: dict(big=["均等割 年", "1,351円"], color=NAVY, sub=["所得割 0.25%", "平均 月194円"]),
  21: dict(big=["令和十年度まで", "段階的に"], color=NAVY),
  22: dict(big=["来年の額は", "まだ決まらず"], color=RED),
  23: dict(big=["来年の紙は", "ご自分で確認"], color=NAVY),
  # ── 第3章 10月に額が変わる ────────────────────────────────────────────────
  24: dict(big=["年18万円以上", "年金から天引き"], color=NAVY, sub=["特別徴収"]),
  25: dict(big=["年金額の", "二分の一まで"], color=NAVY),
  26: dict(big=["仮徴収", "四・六・八月"], color=NAVY),
  27: dict(big=["本徴収", "十・十二・二月"], color=NAVY),
  28: dict(big=["残りを", "三回に分ける"], color=NAVY),
  29: dict(big=["十月が最初の月"], color=RED, size=110, circle=True),
  30: dict(big=["引かれない方も", "います"], color=NAVY),
  31: dict(big=["納付書か", "口座振替"], color=NAVY, sub=["普通徴収"]),
  32: dict(big=["逆です"], color=RED, size=130),
  33: dict(big=["あとで", "まとめて請求"], color=RED),
  # ── 計算タイム① 中村さん ──────────────────────────────────────────────────
  34: dict(big=["まず、所得が", "低い方から"], color=NAVY),
  35: dict(big=["中村さん 71歳", "新潟県上越市"], color=NAVY),
  36: dict(big=["「灯油を", "我慢することに」"], color=NAVY),
  37: dict(big=["新潟県 均等割", "年4万9,200円"], color=NAVY),
  38: dict(big=["七割・五割", "二割の軽減"], color=NAVY),
  39: dict(big=["中村さんは", "七割の段"], color=TEAL),
  40: dict(big=["七割二分まで", "減らせます"], color=TEAL, sub=["令和8・9年度"]),
  41: dict(big=["月1,148円"], color=TEAL, size=120, circle=True),
  42: dict(big=["都道府県ごとの", "表で確かめる"], color=NAVY),
  43: dict(big=["広域連合ごとの", "判断です"], color=RED),
  44: dict(big=["お住まいの", "広域連合へ"], color=NAVY),
  45: dict(big=["この先四年は", "大丈夫そうです"], color=TEAL),
  # ── CTA giữa video ────────────────────────────────────────────────────────
  46: dict(big=["高評価と", "シェアを"], color=NAVY),
  47: dict(big=["コメントで", "教えてください"], color=NAVY),
  48: dict(big=["それでは、続きへ"], color=NAVY),
  # ── 計算タイム② 小林さん（本題）──────────────────────────────────────────
  49: dict(big=["小林さん 75歳", "埼玉県川口市"], color=NAVY),
  50: dict(big=["保険料は", "ゼロ円でした"], color=TEAL, sub=["息子さんの扶養"]),
  51: dict(big=["「考えたことも", "ありませんでした」"], color=NAVY),
  52: dict(big=["一段目", "年ゼロ円"], color=TEAL),
  53: dict(big=["二段目 均等割が", "五割に"], color=TEAL, sub=["所得割は賦課されず"]),
  54: dict(big=["埼玉県 均等割", "年5万2,370円"], color=NAVY),
  55: dict(big=["月2,182円"], color=TEAL, size=120, circle=True),
  56: dict(big=["思ったより", "安かった"], color=TEAL),
  57: dict(big=["三段目", "二年で切れる"], color=RED),
  58: dict(big=["自動的に", "切れます"], color=RED),
  59: dict(big=["その日付は", "どこにもない"], color=RED),
  60: dict(big=["所得割も", "加わります"], color=RED),
  61: dict(big=["埼玉県の平均", "月8,189円"], color=NAVY),
  62: dict(big=["平均のほうへ", "動きます"], color=RED),
  63: dict(big=["三倍以上に"], color=RED, size=130, circle=True,
           sub=["ゼロ円", "月2,182円", "そして三倍"]),
  64: dict(big=["答えは", "三つ目でした"], color=NAVY),
  65: dict(big=["封を切る前に", "カレンダーを"], color=TEAL),
  # ── 第4章 誤解三つ ────────────────────────────────────────────────────────
  66: dict(big=["誤解①", "全国同じ？"], color=NAVY),
  67: dict(big=["県ごとに", "違います"], color=RED),
  68: dict(big=["いちばん高い県と", "低い県"], color=NAVY),
  69: dict(big=["東京都 月1万352円", "青森県 月4,990円"], color=NAVY),
  70: dict(big=["年6万4千円の差"], color=RED, size=110, circle=True),
  71: dict(big=["同じ制度でも", "県で変わる"], color=RED),
  72: dict(big=["誤解②", "安い県へ移せる？"], color=NAVY),
  73: dict(big=["誤解③", "軽減は続く？"], color=NAVY),
  74: dict(big=["続きません"], color=RED, size=120),
  75: dict(big=["毎年", "判定し直されます"], color=RED),
  # ── 第5章 やること ────────────────────────────────────────────────────────
  76: dict(big=["①七月の", "封筒を探す"], color=TEAL),
  77: dict(big=["一年分の額が", "書いてあります"], color=NAVY),
  78: dict(big=["②加入月に", "二年を足す"], color=TEAL),
  79: dict(big=["紙にない日付を", "自分で書く"], color=TEAL),
  80: dict(big=["八月と十月を", "並べて見る"], color=NAVY),
  81: dict(big=["窓口は", "広域連合"], color=NAVY, sub=["年金事務所ではありません"]),
  # ── 研究ノート + シェア用ノート ───────────────────────────────────────────
  82: dict(big=["研究ノート"], color=NAVY, size=120),
  83: dict(big=["月7,989円", "二年前より578円増"], color=NAVY),
  84: dict(big=["子育て支援金", "月194円"], color=NAVY),
  85: dict(big=["十月から", "額が変わります"], color=NAVY),
  86: dict(big=["年2万6,185円", "ふえます"], color=RED, circle=True),
  87: dict(big=["あなたの県では？"], color=NAVY),
  88: dict(big=["七月の封筒を", "探しておいて"], color=TEAL),
  89: dict(big=["ご家族に", "送っておく"], color=TEAL),
  90: dict(big=["チャンネル登録で", "お待ちください"], color=NAVY),
  91: dict(big=["令和八年九月", "時点の情報です"], color=NAVY),
}
