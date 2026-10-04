# -*- coding: utf-8 -*-
"""
_scenes26.py — BẢNG SCENE của video 26 (介護保険料の段階は「世帯」で決まる).

Copy khuôn từ `_scenes25.py`. **Nguồn sự thật duy nhất** cho cả ba thứ: số clip phải gen ·
lớp hình của builder · prompt. Sửa nội dung video thì sửa ở đây.

CÁCH ĐỌC MỘT DÒNG:
    (dòng_timeline_bắt_đầu, kind, telop, nội_dung)
  · `dòng_timeline_bắt_đầu` — chỉ số dòng trong `timeline.json`. Scene kết ở dòng bắt đầu
    của scene KẾ TIẾP.
    🔴 Neo theo CHỈ SỐ DÒNG thì vỡ IM LẶNG nếu `_TTS.md` bị sửa. `plan26` có gate
       `len(timeline) == 101` chặn trước — đừng bỏ.
       (`feedback_builder_neo_dong_kiem_timeline_truoc`)
  · `kind`:
      art     — hình collage toàn khung. Cần ceil(giây/8,7) clip.
      stat    — thẻ số liệu `papercut-stat`, KHÔNG footage. `nội_dung` = list "nhãn|số".
      formula — thẻ `papercut-formula`, KHÔNG footage. `nội_dung` = list dòng công thức.
      genten  — ảnh chụp THẬT trang 新宿区/厚労省, KHÔNG footage, `motion: none`.
      gfx     — khối THUẦN ĐỒ HOẠ, Remotion vẽ 100% bằng font. KHÔNG gen bằng AI.
  · `telop` — chữ to đè lên. `{...}` = cụm nhấn màu. ⚠️ Trần 11 ký/dòng.

⭐ `gfx` hay `art`? — NGHĨA NẰM Ở ĐÂU:
  · Nghĩa do **CHỮ** tải (lộ trình, danh sách, checklist) ⇒ **gfx** (font luôn đúng).
  · Nghĩa do **HÌNH + CHUYỂN ĐỘNG** tải (cánh cửa đóng, thước đo tráo, bậc thang) ⇒
    **art khuôn META/GAUGE** — không chữ nào trong khung ⇒ không chạm vùng AI hỏng.

🔴🔴 SỬA TRỤC BÀI 2026-09-16 — ĐỌC TRƯỚC KHI ĐỤNG VÀO BẢNG NÀY
─────────────────────────────────────────────────────────────────────────────────
Bản v1 của `_TTS.md` gán chênh lệch **49,600円 (第3→第6)** cho nguyên nhân 「世帯」 — SAI.
Đối chiếu 3 nguồn độc lập (新宿区 file07_02_00006 · 延岡市 第9期段階表 · **上越市 段階表**):

    第1〜第3段階  = 世帯全員が住民税非課税
    第4・第5段階  = 本人は非課税 だが 世帯員に課税者あり
    第6段階〜     = 本人が住民税課税              ← 第6 đòi BẢN THÂN bị đánh thuế
    (ĐÚNG, giữ nguyên) 第1〜5 nhìn 課税年金収入額＋その他の合計所得金額 ·
                       第6〜 nhìn 本人の合計所得金額 ⇒ khối 「物差し」 không phải sửa.

⇒ `_TTS.md` đã viết lại (v2, cùng ngày): 中村 giữ **年金147万 · 非課税 · 第3段階 39,500円**;
  con gái đi làm dọn về ⇒ 課税年金収入額 147万 > **826,500円** ⇒ **第5段階 77,400円**
  ⇒ **差 37,900円/năm ≒ 3,158円/月**. Beat 「線を2万円またいだ / 5千円の税金が5万円…」
  **đã cắt** — nó là cơ chế 本人課税, và là trục của video 14.
  Cả 4 con số 39,500 · 69,700 · 77,400 · 89,100 nằm trên MỘT bảng 上越市 (fact #7).

🎨 STYLE: vox paper-collage `newsprint-editorial` (CLAUDE.md §② — luật từ video 23).
   BA GUARD dán vào mọi scene `art` (do `beats26.py` nối vào cuối): ① người Nhật cao tuổi
   ② mọi mặt giấy TRỐNG, không một chữ/kanji nào (SỐ thì ĐƯỢC, cắt từ bìa màu)
   ③ chừa dải phải ~1/10 khung cho mascot + logo.
"""

A, S, G, X, F = "art", "stat", "genten", "gfx", "formula"

# ⛔ RỖNG có chủ ý — guard ② cấm chữ trong ảnh, số chốt do font của Remotion vẽ.
#    Giữ tên vì plan26 import.
NUM = {}

# (url, mô tả vùng cần khoanh, tên file raw, (y0, y1) thô)
# 🔴 LUẬT: chụp TRƯỚC → đọc bằng MẮT → RỒI mới chốt y (video 22 từng bịa 3 URL, cả ba 404).
#    ✅ Cả 4 URL dưới đây ĐÃ CURL VÀ ĐỌC HTML THẬT trong phiên 2026-09-16 (HTTP 200, đã
#       grep thấy đúng cụm chữ ghi ở cột mô tả).
#    ✅ ĐÃ CHỤP 2026-09-16 (`tools/shoot_genten_26.py`) → `06_VIDEO/26_.../genten_raw/`,
#       ĐÃ SOI BẰNG MẮT, và ĐÃ DỰNG **9 thẻ** bằng `tools/make_genten_26.py`.
#       Toạ độ cắt + hộp khoanh đỏ nằm trong `make_genten_26.CARDS` (snap vào đường kẻ
#       thật của bảng, đo bằng máy). Ô thứ 4 dưới đây giữ `None` — không ai đọc nó nữa.
#    🔴 HAI BẪY LÚC CHỤP: 新宿区 trả 403 cho UA mặc định của chrome-headless-shell, và khi
#       có UA thật thì nó đẩy sang trang DỊCH MÁY J-SERVER (vì Accept-Language tiếng Anh).
#       Cả hai lần đều ra ảnh "thành công" rc=0 — chỉ lộ khi soi mắt. Phải truyền
#       `--user-agent=<Chrome thật> --lang=ja-JP --accept-lang=ja-JP,ja;q=0.9`.
GENTEN = {
    # Bảng 18 段階 của 新宿区: cột trái ghi rõ 「世帯全員 住民税非課税」 cho 第1〜3,
    # 「本人が住民税非課税で世帯員が住民税課税」 cho 第4・5, 「本人が住民税課税」 từ 第6.
    # ⭐ MỘT trang chở cả ba thứ bài cần ⇒ chẻ thành nhiều thẻ bằng cách ĐỔI CHỖ KHOANH ĐỎ
    #    (đúng bài học video 22 §5: chẻ bằng khoanh, không bằng zoom).
    "shinjuku_dankai": (
        "https://www.city.shinjuku.lg.jp/fukushi/file07_02_00006.html",
        "第1〜3段階=世帯全員非課税 / 第4・5=世帯員が課税 / 第6〜=本人課税 ＋ 物差しの列",
        "raw_shinjuku_dankai.png", None),

    # 「標準段階を9段階から13段階へと改訂」＋「新宿区は16→18段階」＋ 基準額 月6,600円
    "shinjuku_9ki": (
        "https://www.city.shinjuku.lg.jp/fukushi/file07_02_00002.html",
        "国の標準段階 9段階→13段階 ／ 新宿区 18段階 ／ 基準額 月6,600円(年79,200円)",
        "raw_shinjuku_9ki.png", None),

    # ⭐ Bảng 17段階 của 上越市 — chở ĐÚNG hai con số của bài: 第3段階 39,500円 ·
    #    第5段階 77,400円 (và 第4 69,700 · 第6 89,100). Cùng khớp cast đã chốt ở script 14.
    "joetsu_dankai": (
        "https://www.city.joetsu.niigata.jp/site/kaigo/hokenryou.html",
        "上越市 第9期 段階表: 第3段階 39,500円 / 第5段階 77,400円 (＋条件欄 826,500円)",
        "raw_joetsu_dankai.png", None),

    # 第9期(令和6〜8年度) 第1号保険料 全国加重平均 月6,225円 (第8期 6,014円)
    # ⚠️ Con số nằm trong PDF, KHÔNG ở trang HTML ⇒ chụp thẳng PDF. Dùng lại từ video 25.
    "mhlw_kaigo": (
        "https://www.mhlw.go.jp/content/12303500/001253798.pdf",
        "第9期の第1号保険料 全国加重平均 月6,225円 (PDF 48 trang — số ở TRANG 1)",
        "raw_kaigo_p1.png", None),
}

SCENES = [
    # ══ COLD OPEN 0:00–1:11 · 対決型 · あなた@0:00 · lộ trình@1:02 ══════════════
    # ⚠️ scene 0–7 viết TRUNG TÍNH — xem cảnh báo YMYL ở docstring.
    (0,  A, "どちらも{147万}",   "SPLIT: two paper coin stacks of exactly the same height pasted flat side by side on the newsprint, an elderly Japanese man cut from a bold vintage printed illustration at the left edge and an elderly Japanese woman cut-out at the right, a wide strip of torn charcoal paper taped flat across between the two stacks at exactly the same height as both of their tops"),
    (1,  A, "同じ町 同じ年",     "CROWD: two identical flat paper houses standing side by side on one paper street seen head-on, one elderly cut-out figure at each front door, a row of small paper trees pasted along the kerb"),
    (2,  S, "保険料だけ{倍}",     ["ひとり暮らし|年3万9,500円",
                                   "*同居|年7万7,400円"]),
    (3,  F, "差は{3万7,900}",    ["七万七千四百円 − 三万九千五百円 ＝ 三万七千九百円"]),
    (4,  A, "収入は{同じ}",       "SPLIT: two identical paper envelopes pinned side by side on flat colour blocks with a taped equals accent between them, an elderly woman cut from a bold vintage printed illustration standing small below"),
    (5,  A, "{玄関}の内側",       "META: a flat paper house seen head-on with its front door cut open, two cut-out silhouettes standing inside the doorway of the right house and one standing alone inside the left"),
    (6,  A, "高いのは{どちら}",   "an elderly Japanese woman cut from a bold vintage printed illustration, thick white die-cut border, her head tilted and one paper palm turned upward, a large empty torn-paper speech bubble taped beside her"),
    (7,  A, "{一緒}のほう",       "SPLIT: two paper coin stacks side by side, the right one clearly taller, a taped arrow curving from a pair of cut-out figures toward the taller stack"),
    (8,  X, "{世帯}で決まる",     "INFOG: two rounded blocks joined by a thin arrow, the left block carrying a small single-figure icon and the right a group icon, the right block filling in last"),
    (9,  X, "今日は{二つ}",       "INFOG: two rounded blocks stacked vertically, each carrying one simple line icon, fading in one after another from top to bottom"),
    (10, A, "{研究室}です",       "DESK: an elderly Japanese researcher cut from a bold vintage printed illustration sits behind a paper desk seen flat-on, a magnifier and a paper paperweight and a stack of plain documents cut from card in front of him, a small paper bar chart of three rising bars pinned on the flat wall behind"),
    (11, X, "まず{事実}から",     "INFOG: a horizontal divider rule with one large rounded block below it and two smaller faded blocks above"),

    # ══ 決定通知書 1:11–1:45 ═══════════════════════════════════════════════════
    (12, A, "七月に{届く紙}",     "HOLD: an elderly Japanese woman cut from a bold vintage printed illustration holds a cream envelope square-on to the camera, a paper letterbox standing open behind her with a second identical envelope lying flat inside it"),
    (13, A, "{段階}の欄",         "HOLD: an elderly man cut from a bold vintage printed illustration holds a plain notice slip square-on, its ruled boxes left completely bare, one narrow strip of torn red paper taped across a single box in the middle of the sheet"),
    (14, A, "見ずに{しまう}",     "an elderly Japanese man cut from a bold vintage printed illustration slides a folded paper slip into a paper drawer, his eyes turned away from it, the drawer already holding two identical folded slips"),
    (15, A, "ここから{全部}",     "DESK: a paper drawer pulled wide open seen flat-on with one folded notice slip lying alone at the bottom of it, a torn paper shadow under the drawer front, no people in frame"),

    # ══ ① 段階は何で決まるか 1:45–2:40 (PAYOFF:数字 ~19%) ═══════════════════════
    (16, X, "何を{見て}決まる",   "INFOG: a single rounded block with a question-mark icon at its centre, a thin dashed outline pulsing around it"),
    (17, X, "{三つ}あります",     "INFOG: three rounded blocks stacked vertically, each carrying one simple line icon, appearing one after another from top to bottom"),
    (18, S, "段階を決める三つ",   ["①|4月1日の世帯",
                                   "②|その年度の課税状況",
                                   "*③|前の年の所得"]),
    (19, A, "{二つ}だけ思う",     "SPLIT: three paper cards pinned in a row with the leftmost one pushed back into shadow while the other two stand proud, an elderly woman cut from a bold vintage printed illustration looking at the two"),
    (20, A, "効くのは{世帯}",     "META: three paper levers standing in a row, the leftmost one pulled fully down while the other two stay upright, a cut-out paper hand resting on the lowered lever"),

    # ══ 世帯全員が非課税 2:40–3:40 ══════════════════════════════════════════════
    (21, X, "条件は{一行}",       "INFOG: one wide rounded block containing a single long horizontal rule, the rule drawing itself from left to right"),
    (22, S, "入れる条件",         ["第1〜第3段階|世帯全員が住民税非課税",
                                   "*ひとりでも課税なら|入れません"]),
    (23, A, "{全員}です",         "CROWD: four elderly and middle-aged Japanese cut-out figures standing shoulder to shoulder inside one drawn paper outline of a house, a single unbroken torn-paper band running behind all four"),
    (24, A, "ご自宅は{どう}",     "an elderly Japanese woman cut from a bold vintage printed illustration seated at a low paper table, her chin resting on one paper hand, a cut-out house shape pinned on the flat wall behind her"),
    (25, A, "子が{働く}と",       "SPLIT: a paper house outline with two cut-out figures inside it, a taped arrow running from the younger figure to a small paper office building on the right, a torn paper band closing across the lower half of the house"),
    (26, A, "年金は{そのまま}",   "VIZ: one solid paper bar standing unchanged beside a second bar that has grown taller, a dashed masking-tape line drawn level across the top of the unchanged bar"),
    (27, X, "あなたが{決めない}", "INFOG: two rounded blocks, the smaller left one outlined in dashes and the larger right one solid, a thin arrow running from the right block back to the left"),

    # ══ 物差しが取り替わる 3:40–4:30 ════════════════════════════════════════════
    (28, A, "{物差し}が変わる",   "META: two long paper measuring sticks laid one above the other on the newsprint, the upper one sliding away to the left while the lower one slides in from the right to take its place, no people in frame"),
    (29, S, "第1〜第5の物差し",   ["見るもの|課税年金収入額",
                                   "＋|その他の合計所得金額",
                                   "*これを|足した額で見る"]),
    (30, S, "第6からの物差し",    ["足さない|年金収入はそのままではない",
                                   "*見るのは|本人の合計所得金額"]),
    (31, A, "同じ言葉 中身違う",  "SPLIT: two identical paper boxes pinned side by side, the left one packed full of small paper squares and the right one holding only a few, an elderly man cut from a bold vintage printed illustration between them"),
    (32, A, "坂でなく{段}",       "GAUGE: a smooth paper ramp on the left and a flight of sharply cut paper steps on the right pasted flat on the newsprint, an elderly cut-out figure standing at the foot of the steps"),
    (33, G, "{原典}新宿区",       "shinjuku_dankai"),

    # ══ ② 計算タイム 中村さん 4:30–6:40 ════════════════════════════════════════
    (34, X, "{計算}してみます",   "INFOG: one rounded block with a small calculator icon at its centre, two short horizontal rules appearing beneath it"),
    (35, A, "上越の{中村さん}",   "an elderly Japanese woman cut from a bold vintage printed illustration, thick white die-cut border, seated square-on with a teacup cut-out beside her, a framed paper silhouette portrait pinned on the flat wall behind"),
    (36, A, "給食室で{40年}",     "CROWD: the inside of a paper school kitchen seen head-on, three large paper pots in a row and two cut-out figures in aprons working at a long counter, a long row of paper serving trays stacked along the flat wall"),
    (37, S, "中村さんの年金",     ["年金|年147万円",
                                   "*上越市の非課税の線|148万円"]),
    (38, A, "一万円{下}",         "GAUGE: a tall paper column standing just below a dashed masking-tape line, the gap between the column top and the tape marked with a torn paper wedge and left clearly open"),
    (39, S, "いまの中村さん",     ["世帯|ひとり暮らし・全員非課税",
                                   "*第3段階|年3万9,500円"]),

    # ══ 娘さんが同居したら 6:00–7:40 ═══════════════════════════════════════════
    (40, X, "ここからが{本題}",   "INFOG: a horizontal divider rule with one large rounded block below it and two smaller faded blocks above"),
    (41, A, "新潟の姉 都内の娘",  "CROWD: three flat paper houses set far apart across the page with two long taped lines linking them, one elderly cut-out figure standing at each of the outer houses"),
    (42, A, "{一緒に住もうか}",   "a middle-aged Japanese woman cut from a bold vintage printed illustration leaning toward an elderly Japanese woman cut-out, one paper hand extended, a large empty torn-paper speech bubble taped above them"),
    (43, A, "{親孝行}です",       "an elderly Japanese woman and a middle-aged Japanese woman cut from a bold vintage printed illustration standing close together, a torn paper heart-shaped accent pasted behind their shoulders"),
    (44, A, "娘さんは{課税}",     "SPLIT: two paper cards pinned side by side, the left one plain and the right one carrying a bold cut-out stamp shape, a taped arrow running from a small paper office building to the right card"),
    (45, A, "世帯に{入る}と",     "META: a paper house outline with one cut-out figure already inside and a second figure sliding in through the doorway, a torn paper band closing across the threshold behind them"),
    (46, A, "{三つ}の扉が閉まる", "META: a row of five paper doors pasted flat on the newsprint, the three leftmost ones swinging shut while the two on the right stay open, a numeral 3 cut from deep red card above the closing doors"),
    (47, X, "課税の方は{何人}",   "INFOG: one rounded block containing four small figure icons, a thin dashed ring drawing itself around two of them, a question-mark icon at the edge"),
    (48, F, "年金は{82万}超え",   ["百四十七万円 ＞ 八十二万六千五百円",
                                   "→ 第五段階"]),
    (49, S, "段階が上がると",     ["ひとりのとき|第3段階 年3万9,500円",
                                   "*娘さんと同じ世帯|第5段階 年7万7,400円"]),
    (50, F, "一年の差",           ["七万七千四百円 − 三万九千五百円 ＝ 三万七千九百円",
                                   "三万七千九百円 ÷ 十二 ≒ 三千百五十八円"]),
    (51, A, "何も{変わらない}",   "VIZ: three solid paper bars of identical height standing in a row with a dashed masking-tape line drawn level across all three tops, an elderly cut-out figure standing beside them"),
    (52, G, "{原典}上越市",       "joetsu_dankai"),
    (53, A, "{ありがたい}けど",   "an elderly Japanese woman cut from a bold vintage printed illustration with her brow strip lifted, a large empty torn-paper speech bubble taped beside her head"),
    (54, A, "少し{黙って}",       "an elderly Japanese woman cut from a bold vintage printed illustration seated very still with her hands folded low, the torn-paper speech bubble beside her now smaller and turned away"),
    (55, A, "{どう言えば}",       "an elderly Japanese woman cut from a bold vintage printed illustration with her head lowered, two empty torn-paper speech bubbles taped one behind the other beside her"),
    (56, A, "優しいほど{上がる}", "SPLIT: a paper staircase climbing to the right with a cut-out paper heart resting on the lowest step and a stack of paper coins growing taller on each higher step"),
    (57, X, "制度を{責めない}",   "INFOG: one rounded block with a small open-palm icon at its centre and a thin ring drawn around it"),

    # ══ CTA ~53% ═══════════════════════════════════════════════════════════════
    (58, A, "{応援}おねがいします", "an elderly Japanese couple cut from a bold vintage printed illustration seated side by side, both dipping their head strips forward, paper accent shapes fanning out behind them"),

    # ══ ③ 動かせるのか — 誤解 8:00–9:20 ════════════════════════════════════════
    (59, X, "二つ目{動かせる}",   "INFOG: one rounded block with a thin arrow curving out of it and back again, a small dashed outline beneath"),
    (60, X, "よくある{誤解}",     "INFOG: two rounded blocks side by side, the left one carrying a small cross icon and the right one left blank"),
    (61, A, "{医療費控除}で？",   "HOLD: an elderly Japanese man cut from a bold vintage printed illustration holds a thick bundle of small blank paper slips fanned out toward the camera, a large empty torn-paper speech bubble taped beside him"),
    (62, X, "{下がりません}",     "INFOG: one rounded block with a downward arrow that stops dead against a heavy horizontal bar below it"),
    (63, S, "医療費控除がするのは", ["所得控除|課税される所得を減らす",
                                   "*減らさないもの|合計所得金額"]),
    (64, S, "段階が見るのは",     ["見ている数字|合計所得金額",
                                   "*それは|控除を引く前の数字"]),
    (65, A, "住民税は{安く}",     "SPLIT: two solid paper bars side by side, the left one visibly shortened by a clean scissor cut while the right one stands at its original height untouched"),
    (66, A, "分けて{覚える}",     "META: one plain paper card torn cleanly down the middle and the two halves laid apart on the newsprint with a clear gap between them, a torn paper shadow under each half, no people in frame"),

    # ══ 本当に動く三つ 9:20–10:40 ══════════════════════════════════════════════
    (67, X, "動くものは{三つ}",   "INFOG: three rounded blocks in a horizontal row, each carrying a different simple line icon, appearing one after another from left to right"),
    (68, A, "毎年{決め直す}",     "META: twelve plain paper squares pinned in a row with a solid paper bar of a different height standing on each, an elderly Japanese woman cut from a bold vintage printed illustration looking along the row"),
    (69, X, "二つ{世帯の課税}",   "INFOG: one rounded block containing three small figure icons, one of the three icons changing tone while the other two stay the same"),
    (70, A, "娘さんの話へ",       "a middle-aged Japanese woman and an elderly Japanese woman cut from a bold vintage printed illustration standing apart with a taped arrow curving back from the younger one to the older one"),
    (71, A, "同居と{同一世帯}",   "SPLIT: one paper house outline holding two cut-out figures, and beside it the same house drawn with a torn paper line running down its middle separating the two figures"),
    (72, A, "分けると{損}も",     "GAUGE: a paper balance beam pasted flat with a small stack of coins on the left pan and a taller stack on the right pan, the beam tipping to the right"),
    (73, A, "判断は{窓口}で",     "CROWD: a municipal counter built from flat paper panels with a queue of elderly cut-out figures waiting, rows of paper chairs behind them and a clerk cut-out at the window"),
    (74, A, "三つ{減免制度}",     "META: a wide paper umbrella opened over a small flat paper house, torn paper rain-strips falling on either side of the umbrella and none underneath it, no people in frame"),

    # ══ ④ 数字を三つ 10:40–11:40 (PAYOFF:答え ~73%) ════════════════════════════
    (75, X, "数字を{三つ}",       "INFOG: three rounded blocks stacked vertically, each carrying one simple line icon, appearing one after another from top to bottom"),
    (76, G, "{原典}厚生労働省",   "mhlw_kaigo"),
    (77, G, "9段階→{13段階}",     "shinjuku_9ki"),
    (78, S, "新宿区の場合",       ["段階の数|18段階",
                                   "*基準額|年7万9,200円"]),
    (79, A, "あくまで{目安}",     "GAUGE: a horizontal axis pasted flat with one tall marker standing at its centre and a wide band of shorter markers spreading on either side, an elderly cut-out figure standing under the tall marker"),

    # ══ 研究ノート 11:40–12:40 ═════════════════════════════════════════════════
    (80, X, "今日の{研究ノート}", "INFOG: five rounded blocks stacked vertically, each carrying a different simple line icon, appearing one after another from top to bottom"),
    (81, S, "研究ノート ①",       ["段階を決めるのは|4月1日の世帯",
                                   "その年度の|住民税の課税状況",
                                   "*前の年の|所得"]),
    (82, S, "研究ノート ②",       ["第1〜第3段階|世帯全員が非課税",
                                   "*同居の方が課税なら|入れません"]),
    (83, S, "研究ノート ③",       ["第1〜第5|年金収入を足した額",
                                   "*第6段階から|本人の合計所得金額"]),
    (84, S, "研究ノート ④",       ["医療費控除で|段階は下がらない",
                                   "*所得控除と|合計所得金額は別"]),
    (85, S, "研究ノート ⑤",       ["段階は|毎年決め直される",
                                   "*所得が戻れば|翌年7月に戻る"]),
    (86, S, "お手元で三つ",       ["①|7月の決定通知書を出す",
                                   "②|段階の欄に丸をひとつ",
                                   "*③|同じ世帯の課税者を数える"]),
    (87, X, "三つ目まで{数える}", "INFOG: three small rounded blocks filling in one after another from left to right, a thin bracket drawing itself under the third"),

    # ══ 中村さんの後日談 12:40–13:30 ═══════════════════════════════════════════
    (88, A, "中村さんは{今}",     "an elderly Japanese woman cut from a bold vintage printed illustration standing in a paper kitchen doorway, one paper hand resting on the frame"),
    (89, A, "まだ{相談中}",       "an elderly Japanese woman and a middle-aged Japanese woman cut from a bold vintage printed illustration seated across a low paper table, two empty torn-paper speech bubbles taped above them"),
    (90, A, "{冷蔵庫}に貼った",   "HOLD: a flat paper refrigerator door seen head-on with one plain notice slip taped to it, a torn red paper ring pasted over a single box on the slip, an elderly cut-out figure standing small beside the door"),
    (91, A, "{驚くのは嫌}",       "an elderly Japanese woman cut from a bold vintage printed illustration with her chin lifted and both paper hands resting flat on a table, a plain torn paper sheet pinned on the wall behind her"),
    (92, S, "知っているかどうか",  ["段階|第3段階 → 第5段階",
                                   "*一年の差|3万7,900円"]),

    # ══ CTA登録 + 次回予告 13:30–end ═══════════════════════════════════════════
    (93, A, "{チャンネル登録}を", "an elderly Japanese couple cut from a bold vintage printed illustration seated side by side looking toward the camera, a paper bell shape and a torn paper starburst taped behind their shoulders"),
    (94, X, "{数字}を計算する",   "INFOG: one wide rounded block with a small calculator icon on the left and three short horizontal rules on the right"),
    (95, X, "さて{次回}です",     "INFOG: one rounded block sliding out to the left while a second block slides in from the right"),
    (96, A, "今日は{世帯}の話",   "SPLIT: one paper house outline holding three cut-out figures on the left and a single figure standing alone on the right, a taped arrow between them"),
    (97, A, "{扶養}に入れたら",   "META: a large paper umbrella shape pasted flat with a small elderly cut-out figure standing beneath it and a middle-aged cut-out figure holding the handle"),
    (98, A, "{両方}は取れない",   "GAUGE: a paper balance beam with a stack of coins on each pan, a cut-out paper hand reaching for both pans at once, the beam tipping sharply to one side"),
    (99, X, "{令和8年9月}時点",   "INFOG: one wide rounded block with three short horizontal rules inside it, a small calendar icon at the left edge"),
    (100, A, "また{次回}の研究で", "DESK: an elderly Japanese researcher cut from a bold vintage printed illustration at a paper desk with both paper hands resting flat, a teacup and a closed folder beside him, a small paper bar chart pinned on the wall behind"),
]
