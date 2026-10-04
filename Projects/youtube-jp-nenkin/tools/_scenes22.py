# -*- coding: utf-8 -*-
"""
_scenes22.py — BẢNG SCENE của video 22 (未支給年金 36万円).

Đây là **nguồn sự thật duy nhất** cho cả ba thứ: số clip phải gen · lớp hình của builder ·
prompt. Sửa nội dung video thì sửa ở đây, đừng sửa ba chỗ.

CÁCH ĐỌC MỘT DÒNG:
    (dòng_timeline_bắt_đầu, kind, telop, nội_dung)
  · `dòng_timeline_bắt_đầu` — chỉ số dòng trong `timeline.json`. Scene kết thúc ở dòng
    bắt đầu của scene KẾ TIẾP.
    🔴 Neo theo CHỈ SỐ DÒNG thì vỡ IM LẶNG nếu `_TTS.md` bị sửa (thêm/bớt câu) mà không
       dựng lại timeline. Builder có gate `len(timeline) == 113` chặn trước — đừng bỏ.
       (`feedback_builder_neo_dong_kiem_timeline_truoc`)
  · `kind`:
      art     — footage Veo toàn khung. Cần ceil(giây/8) clip.
      stat    — thẻ số liệu `papercut-stat`, KHÔNG footage. `nội_dung` = list dòng "nhãn|số".
      genten  — ảnh chụp thật trang 年金機構/国税庁, có pan. KHÔNG footage.
  · `telop` — chữ to đè lên. `{...}` = cụm nhấn màu. ⚠️ Trần ~10 ký/dòng, xuống dòng bằng \n.
  · `nội_dung` — với `art` là mô tả cảnh (đi thẳng vào prompt); với `stat` là các dòng bảng.

⚖️ YMYL: mọi con số ở `stat` đều lấy TỪ CHÍNH LỜI ĐỌC, không thêm số mới. Phép cộng
   18万×2=36万 là tính lại từ hai số đã có trong script, không phải số bịa.
"""

# kind viết tắt cho gọn bảng
# `X` = khối THUẦN ĐỒ HOẠ, Remotion vẽ 100% bằng font — KHÔNG gen bằng Veo.
# 🔴 Vì sao tách ra (user 2026-09-09): 11 scene này không có gì ngoài SƠ ĐỒ và CHỮ.
#    Veo không viết được tiếng Nhật ⇒ nó trả về hộp màu + chữ giả "Lorem ipsum",
#    và người xem nhìn vào không rút ra được gì. Gen bằng Veo là đốt clip để lấy
#    một tấm ảnh vô nghĩa. Font vẽ thì chữ luôn sắc và luôn ĐÚNG nội dung.
A, S, G, X = "art", "stat", "genten", "gfx"

SCENES = [
    # ── COLD OPEN 0-60s: không モニター kể chuyện (CLAUDE.md §③) ──────────────
    (0,   A, "{葬儀}のあと",       "an elderly woman sits quietly at a low table and bows her head, palms together in front of her chest, a small framed photograph and a white chrysanthemum on the table"),
    (1,   A, "通帳で{手が止まる}",  "an elderly woman sits with an open bank passbook already lying flat in front of her, her hand comes to a stop and she looks down at the page"),
    (2,   A, "{36万円}が入った",    "HOLD: an elderly woman holds an open bank passbook up beside her face, her eyes wide and her mouth slightly open"),
    (3,   A, "二か月後{もう一度}",  "SCREEN: a large desktop monitor stands on a table, an elderly woman sits beside it with her body turned toward the screen, looking at it"),
    (4,   A, "見た目は{同じ}",      "SCREEN: a large monitor stands on a table, an elderly man sits beside it and reaches out to point at the screen"),
    (5,   A, "片方は{返金}",        "an elderly man stands behind a table with one plain envelope already in each hand, pushing his left hand forward toward the camera while drawing his right hand back toward his chest"),
    (6,   A, "線は{どこ}に",        "SCREEN: a monitor stands on a desk, an elderly man sits in front of it with his chin lifted, studying the screen"),
    (7,   A, "いつか必ず{並ぶ}",    "an elderly couple sit side by side and both turn to face the camera"),
    (8,   A, "黙っていて{入る}？",  "an elderly man holds a phone up at chest height, its screen showing a completed form with green check marks"),
    (9,   X, "ここが{取り逃し}",    "INFOG: a two-branch diagram, the left branch carrying a check-mark icon and the right branch a cross icon, both joining one shared block in the middle"),
    (10,  X, "まず{事実}から",      "INFOG: a horizontal timeline with six evenly spaced round milestones that light up one after another from left to right"),

    # ── ĐỊNH VỊ + CƠ CHẾ TRẢ SAU ─────────────────────────────────────────────
    (12,  A, "なぜお金が{残る}",    "CROWD: the consultation counter of a Japanese social insurance office, a female clerk talking with an elderly visitor, rows of waiting chairs behind them"),
    (13,  A, "年金は{後払い}",      "CROWD: the large hall of an administrative centre, many elderly people queuing at the counters, an electronic number board on the wall"),
    (14,  G, "{原典}で確かめる",    "nenkin_shiharai"),
    (16,  S, "四月の振込は",        ["四月に入るお金|二月分と三月分",
                                     "つまり|二か月前の分",
                                     "*年金は|後払い"]),
    (17,  A, "いまの口座は{二か月前}", "CROWD: the reception counter of a social insurance office, three uniformed clerks standing behind it, several elderly people queuing in front"),
    (18,  A, "必ず{残る}分がある",  "SCREEN: a monitor stands on a low cabinet, a young female clerk stands beside it and points at the upper part of the screen"),
    (19,  A, "これが{未支給年金}",  "CROWD: a corner of a consultation room with three desks, at each desk a clerk talking with an elderly visitor"),
    (20,  X, "相続財産では{ない}",  "GAUGE: a large gauge dial standing on the floor, the needle resting in the green zone near the middle mark, an elderly man standing at the right looking up at it"),

    # ── CASE 中村 / お姉さま ─────────────────────────────────────────────────
    (21,  A, "{数字}で見る",        "CROWD: the waiting hall of a Japanese social insurance office, many elderly people seated in rows of chairs, the reception counter behind them"),
    (22,  A, "上越市の{中村さん}",  "DESK: an elderly man sits at the table, a teacup beside him, looking calmly at the camera"),
    (23,  A, "新潟市の{お姉さま}",  "SCREEN: a tablet sits upright on a stand, an elderly woman leans in toward it, reading"),
    (25,  A, "「まだ{入ってくる}」", "an elderly woman holds a desk telephone handset to her ear, a worried look on her face"),
    (26,  A, "月{18万円}ほど",      "SCREEN: a tablet sits upright on a stand, an elderly man sits beside it looking at the screen"),
    (27,  A, "二つの振込を{並べる}", "SPLIT: an elderly man sits at a bright bank counter looking down at the paper in front of him, calm and composed"),
    (28,  S, "四月十五日の振込",    ["四月十五日|二月分＋三月分",
                                     "亡くなったのは|三月五日",
                                     "*その月の分まで|受け取れる"]),
    (29,  X, "亡くなった月{まで}",  "META: a large round golden shield hovers in the air, an envelope flies toward it and stops just in front of it, then the shield turns slightly and holds"),
    (30,  S, "受け取れる金額",      ["ひと月|十八万円",
                                     "二か月分|三十六万円",
                                     "*これが|未支給年金"]),
    (31,  A, "請求すれば{受け取れる}", "CROWD: a procedure briefing in a community hall, many elderly people seated in rows, a staff member standing at the front explaining"),
    (32,  A, "六月分は{どうか}",    "SCREEN: an elderly man holds a phone up at chest height with the screen facing the camera, his eyes on it"),
    (33,  S, "六月十五日の振込",    ["六月十五日|四月分＋五月分",
                                     "四月には|もういない",
                                     "*こちらは|受け取れない"]),
    (35,  A, "同じ{36万円}だが",    "SCREEN: a monitor stands on a table, an elderly man sits square in front of it, looking at the screen"),
    (36,  G, "機構は{こう書く}",    "nenkin_gessuu"),
    (37,  A, "片方は{返す}",        "SPLIT: the same elderly man leans back at the same counter, one hand rising to chest height, frozen in surprise"),
    (38,  A, "だから{混ざる}",      "SCREEN: a wide monitor stands on a desk, an elderly woman sits in front of it with both hands on the desk, looking at the screen"),
    (39,  A, "通帳は「{年金}」だけ", "HOLD: an elderly woman holds an open bank passbook up close to the camera and taps twice on the page with her index finger"),
    (40,  A, "線は{亡くなった日}",  "an elderly man draws a single straight horizontal line across the middle of a plain sheet of paper with his index finger"),

    # ── CTA ~50% ─────────────────────────────────────────────────────────────
    (41,  A, "{応援}おねがいします", "an elderly couple sit side by side and both nod once toward the camera"),

    # ── 死亡届 + マイナンバー ────────────────────────────────────────────────
    (42,  A, "答えは{届出}",        "HOLD: an elderly man holds up a plain printed form with one hand and points at it with the other"),
    (43,  A, "{死亡届}を出す",      "SCREEN: an open laptop sits on a table, an elderly man sits in front of it, hands resting either side of it"),
    (44,  S, "届出の期限",          ["厚生年金のかた|十日以内",
                                     "国民年金だけ|十四日以内",
                                     "*葬儀の|最中です"]),
    (45,  A, "{葬儀}の最中に",      "DESK: an elderly woman sits at the table, a tall stack of paperwork in front of her, both hands resting on the table, looking tired"),
    (46,  X, "救いが{ひとつ}",      "GAUGE: a large gauge dial on a table in a bright room, its needle almost touching the boundary between the green and amber zones, no people in frame"),
    (47,  G, "{マイナンバー}で省略", "nenkin_mynumber"),
    (49,  A, "ここで{安心しない}",  "an elderly man holds one palm out flat toward the camera as if to stop something, his expression serious"),
    (50,  A, "届出は{必要}",        "SCREEN: a monitor stands on a table, an elderly woman sits beside it with her head turned to the screen"),
    (51,  A, "止めるは自動\n{受取は手動}", "SCREEN: a monitor stands on a low cabinet, a young female clerk stands beside it and points at the right-hand side of the screen"),
    (52,  A, "請求しないと{渡らない}", "an elderly woman looks straight at the camera, both forearms resting on the table"),

    # ── AI ĐƯỢC YÊU CẦU + 生計同一 ───────────────────────────────────────────
    (53,  A, "誰が{請求}できる",    "VIZ: seven small wooden blocks of descending height standing in a row on a table, the tallest on the left, each block wide and flat-bottomed so it stands stably"),
    (54,  S, "請求できる順番",      ["一番目|配偶者",
                                     "つぎに|子・父母・孫",
                                     "そのあと|祖父母・兄弟姉妹",
                                     "*先の順位がいると|あとには回らない"]),
    (56,  X, "もうひとつ{条件}",    "INFOG: a diagram of two conditions placed side by side in two rounded frames, each frame carrying one simple icon, a small illustrated figure standing at the edge"),
    (57,  A, "{生計同一}",          "CROWD: a ward office reception counter, two female clerks standing behind it, an elderly couple standing in front"),
    (58,  A, "住所が同じなら{OK}",  "SCREEN: an open laptop sits on a wooden table, an elderly woman sits behind it looking down at the screen"),
    (59,  A, "離れていても{道はある}", "an elderly man looks out through the window, then turns back toward the camera"),
    (60,  S, "離れて暮らす場合",    ["日常生活を|共にしていた",
                                     "または|経済的な援助＋音信",
                                     "*出す書類|生計同一関係の申立書"]),
    (61,  A, "施設の{ご両親}",      "CROWD: the common room of a care facility, many elderly people seated around round tables, sunlight coming through the large windows"),
    (62,  A, "{諦めないで}",        "CROWD: a consultation session in a community hall, many elderly people seated in rows, a staff member handing out leaflets along the aisle"),
    (63,  A, "職員が{証明}",        "SCREEN: a monitor stands on a desk, an elderly man sits in front of it leaning slightly forward"),
    (64,  A, "{門前払い}ではない",  "SCREEN: a large desktop monitor stands on a table, an elderly man sits beside it with one arm on the table, looking at the screen"),

    # ── GIẤY TỜ ──────────────────────────────────────────────────────────────
    (65,  A, "何を{持っていく}",    "DESK: an elderly woman sits at the table, lifting a teacup with one hand"),
    (66,  S, "請求に持っていくもの", ["①|年金証書",
                                     "②|マイナンバーが分かるもの",
                                     "③|戸籍の謄本か抄本",
                                     "④|住民票の除票と世帯全員のもの",
                                     "*⑤|振込先の通帳の写し"]),
    (70,  A, "ずいぶん{多い}",      "DESK: an elderly woman looks down at the loaded table and lets out a breath"),
    (71,  A, "マイナンバーで{省ける}", "an elderly man holds a small plain card up at face height"),
    (72,  A, "公金受取口座なら{不要}", "SCREEN: an open laptop sits on a table, an elderly woman is seated behind it, looking at the screen"),
    (73,  A, "死亡診断書は{要らない}", "an elderly man shakes his head once, one palm turned upward"),
    (74,  A, "この{四つか五つ}だけ", "CROWD: a procedure guidance room, a male staff member standing and pointing at a wall chart, six elderly people seated listening"),
    (75,  A, "請求書は{一枚}",      "SCREEN: a large monitor stands on a table, an elderly man sits beside it and points at the lower part of the screen"),
    (76,  S, "この書類の正式名",    ["名前|年金受給権者死亡届",
                                     "そのうしろに|未支給年金請求書",
                                     "*報告と請求が|一枚になっている"]),
    (78,  A, "省略される人は{機会なし}", "PANEL: an elderly woman sits with her head bowed over a stack of papers, one hand propping up her forehead"),
    (79,  A, "そこが{危ない}",      "PANEL: an elderly man turns his head to look off to one side, his mouth slightly open and his shoulders dropping"),

    # ── THỜI HIỆU ────────────────────────────────────────────────────────────
    (80,  A, "みっつ目{期限}",      "SCREEN: a monitor stands on a desk, an elderly man sits in front of it with his head tilted"),
    (81,  S, "時効",                ["未支給年金|五年",
                                     "死亡一時金|二年",
                                     "*混同|しやすい"]),
    (82,  X, "数えはじめが{ちがう}", "INFOG: a five-year timeline with five evenly spaced round milestones, the first one marked with an accent ring, the milestones lighting up from left to right"),
    (83,  S, "五年の数えかた",      ["起点は|亡くなった日ではない",
                                     "起点は|支払日の翌月初日",
                                     "*そこから|五年"]),
    (85,  A, "まだ{間に合う}かも",  "PANEL: an elderly woman straightens up, her eyes brightening, one hand resting on the table top"),
    (87,  X, "混同{注意}",          "META: two hourglasses standing side by side, the left one twice as tall as the right, sand running slowly in both"),

    # ── THUẾ ─────────────────────────────────────────────────────────────────
    (88,  A, "最後に{税金}",        "DESK: an elderly man sits at the table, a pocket calculator in front of him, his hand resting beside it"),
    (89,  A, "相続税は{かからない}", "CROWD: a tax consultation call centre, four headset-wearing operators seated in a row in front of their monitors"),
    (90,  A, "でも{無税ではない}",  "an elderly woman tilts her head, a faintly worried look on her face"),
    (91,  G, "国税庁は{こう書く}",  "kokuzei_ichiji"),
    (92,  S, "一時所得の計算",      ["受け取った額|三十六万円",
                                     "特別控除|五十万円",
                                     "*三十六万円は五十万円より少ない|税金はかからない"]),
    (94,  X, "他の収入と{合算}",    "INFOG: a flat diagram of a two-pan balance scale, the left and right pans almost level, an icon label on each pan"),

    # ── 研究ノート + 3 việc kiểm ─────────────────────────────────────────────
    (95,  S, "今日の研究ノート",    ["一|年金は二か月分の後払い",
                                     "二|亡くなった月の分までが受け取れる分",
                                     "三|死亡届は十日か十四日以内",
                                     "四|未支給年金の請求は省略できない",
                                     "*五|時効は五年・支払日の翌月初日から"]),
    (101, X, "三つだけ{確かめる}",  "INFOG: three check blocks stacked vertically, each with one simple icon and an empty square at the start of the line, the blocks appearing one after another"),
    (102, S, "確かめる三つ",        ["ひとつ|二か月分はいくらか",
                                     "ふたつ|マイナンバーは結びついているか",
                                     "*みっつ|仕送りや連絡の記録はあるか"]),
    (105, X, "{令和八年八月}時点",  "INFOG: three groups of round icons arranged in a horizontal row, each group in a different pastel colour, joined by thin lines"),

    # ── NEXT + KẾT ───────────────────────────────────────────────────────────
    (106, A, "{次回}です",          "an elderly man sits at a table and leans toward the camera as he speaks"),
    (108, A, "受け取りはじめも{同じ}", "an elderly woman nods slowly, both forearms resting on the table"),
    (109, A, "65歳でも{届かない}",  "SCREEN: a monitor stands on a desk, an elderly man sits in front of the computer with his shoulders dropped"),
    (110, A, "理由は{四つ}",        "CROWD: a post office counter, a female clerk receiving an envelope from an elderly woman, a few customers waiting behind"),
    (112, A, "また{次回}",          "an elderly couple sit side by side and both bow their heads slightly"),
]

# ── ẢNH 原典 — ĐÃ CHỤP + VERIFY BẰNG MẮT 2026-09-07 ─────────────────────────
# 🔴 BA URL ĐẦU TAO TỰ BỊA Ở BẢN TRƯỚC VÀ CẢ BA ĐỀU 404. Chỉ lộ ra khi chụp màn hình
#    thật (trang trả về 「お探しのページが見つかりません」). Đúng thứ luật YMYL của kênh
#    cấm: "verify link TRƯỚC khi viết". Tệ hơn: URL 支払日 ĐÃ CÓ SẴN trong
#    `.claude/rules/upload-schedule.md` §3 — bịa một URL mới trong khi nguồn nằm sẵn trong
#    rule của chính workspace.
# ⇒ Từ nay: chụp trước, đọc bằng mắt, RỒI mới ghi URL vào bảng. Ảnh chụp chính là bằng
#    chứng URL sống — không có ảnh thì coi như chưa có nguồn.
#
# (khoá): (URL, mô tả câu cần khoanh, file ảnh đã chụp, vùng y trong ảnh gốc 1400px rộng)
GENTEN = {
    # bảng 「年金の支払月と支払対象月」 — 4月→2月・3月分, 6月→4月・5月分.
    # Đây là bằng chứng đắt nhất của bài: nó chứng minh CHÍNH cặp tháng mà script dùng.
    "nenkin_shiharai": (
        "https://www.nenkin.go.jp/section/faq/jukyu/uketori/uketori/shiharaiduki/20140421-01.html",
        "年金の支払月と支払対象月（4月→2月・3月分）", "raw_shiharai.png", (820, 1170)),

    # 「亡くなった月分までの年金については、未支給年金として…遺族が受け取ることができます」
    "nenkin_gessuu": (
        "https://www.nenkin.go.jp/service/jukyu/tetsuduki/kyotsu/jukyu/20140731-01.html",
        "亡くなった月分までの年金は未支給年金として遺族が受け取れる", "raw_shibou.png", (432, 505)),

    # 「マイナンバーが収録されている方は、原則として、年金受給権者死亡届（報告書）を省略できます」
    # ⚠️ CÙNG một trang với thẻ trên, chỉ khác VÙNG KHOANH — nên hai thẻ phải cắt khác y,
    #    nếu không người xem thấy đúng một tấm ảnh hai lần.
    "nenkin_mynumber": (
        "https://www.nenkin.go.jp/service/jukyu/tetsuduki/kyotsu/jukyu/20140731-01.html",
        "マイナンバー収録なら死亡届は原則省略できる", "raw_shibou.png", (515, 590)),

    # 総収入金額 − 支出 − 特別控除額(最高50万円) ＝ 一時所得の金額
    "kokuzei_ichiji": (
        "https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1490.htm",
        "一時所得の計算式・特別控除額（最高50万円）", "raw_ichiji.png", (1255, 1310)),
}


# ── NỘI DUNG MÀN HÌNH — REMOTION VẼ, VEO KHÔNG GEN ─────────────────────────
# 🔴 user chốt 2026-09-09: *"màn hình với giấy không hiển thị chữ hay số gì cả…
#    người xem xem cái ảnh đó để làm gì"*. Đúng, và nguyên nhân là mô tả scene
#    BẢO màn hình hiện nội dung trong khi khối guard lại CẤM đọc được chữ — hai vế
#    chọi nhau nên Veo trả về mấy mảng màu vô nghĩa.
# ⇒ Theo phương án lai: **Veo quay cái màn hình RỖNG (chính diện, đứng yên),
#   Remotion dán nội dung thật vào hình chữ nhật đó bằng font** ⇒ chữ Nhật luôn sắc
#   và luôn ĐÚNG nội dung. Bảng dưới là hợp đồng giữa hai tầng: sửa nội dung màn hình
#   thì sửa ở đây, KHÔNG sửa vào mô tả scene (mô tả chỉ nói thứ Veo quay được).
SCREEN_FILL = {
    3  : "hai lịch tháng liền nhau, mỗi tháng sáng một ô ngày",
    4  : "hai dòng giao dịch giống hệt nhau xếp trên dưới",
    6  : "một đường kẻ ngang chia bảng làm hai nửa, hai màu khác nhau",
    16 : "biểu đồ thanh ngang: thanh trên dài, thanh dưới ngắn",
    21 : "một tờ khai đã điền xong",
    23 : "một thẻ số lớn",
    29 : "danh mục các mục, dấu tích xanh sáng dần lên",
    31 : "hai thẻ số giống hệt nhau, thẻ phải có một chấm màu ở góc",
    34 : "hai cửa sổ bảng mở song song, nội dung hai bên trông giống nhau",
    39 : "một biểu mẫu trực tuyến còn trống",
    45 : "danh mục giấy tờ phải nộp, các ô tích xanh sáng dần",
    46 : "hai cột: cột trái có dấu tích, cột phải còn trống",
    52 : "một biểu mẫu trực tuyến",
    57 : "một biểu mẫu nhiều ô, ba ô liên tiếp sáng lên",
    58 : "bảng so sánh hai cột: trái dấu chéo, phải dấu tích",
    63 : "một trang web chính thức, một dòng trong bảng sáng lên",
    66 : "một biểu mẫu chia hai phần trên và dưới",
    70 : "trục thời gian ngang ba mốc, mốc cuối nhấp nháy",
    88 : "hộp thư đến trống rỗng kèm một dòng thông báo",
}
