# -*- coding: utf-8 -*-
"""Sinh SLIDES.json cho script 14 (co-dai) + validate match theo TTS thật."""
import io, json, re, sys, pathlib

TTS = pathlib.Path(r"E:\Claude\Projects\youtube-jp-co-dai\03_SCRIPTS\14_ka-hakko-trap_TTS.md")
OUT = pathlib.Path(r"E:\Claude\Projects\youtube-jp-co-dai\03_SCRIPTS\14_ka-hakko-trap_SLIDES.json")

lines = [re.sub(r"^(\[[^\]]+\])+\s*", "", l).strip()
         for l in io.open(TTS, encoding="utf-8").read().splitlines()
         if l.strip() and not l.startswith("#")]

def P(i, q, src=None):          # ảnh stock
    e = {"_i": i, "photo": True, "q": q, "min_score": 0.9}
    if src: e["src"] = src
    return e
def V(i, qv):                   # clip động
    return {"_i": i, "video": True, "qv": qv}
def C(i, *txt, accent=True):    # card chữ
    return {"_i": i, "photo": False, "lines": list(txt), "accent": accent}

S = [
 # ── HOOK ────────────────────────────────────────────────────────────────
 V(0,  "japanese veranda summer evening garden dusk"),
 P(1,  "asian couple relaxing outdoors summer evening"),
 C(2,  "血がおいしいから？"),
 C(4,  "いいえ、", "それは違います"),
 P(5,  "mosquito macro close up"),
 C(6,  "50メートル先から", "あなたを見つける"),
 C(8,  "答えは", "あなたの息"),
 P(9,  "old japanese wooden house at dusk"),
 P(11, "white bucket in a garden at dusk"),
 C(12, "材料費 300円", "5分で完成"),
 P(13, "dry yeast sugar and dish soap on a table"),
 P(15, "浮世絵", src="commons"),
 V(17, "dark bedroom at night window moonlight"),
 C(19, "なぜ耳元なのか"),
 P(22, "supermarket shelf of household products"),
 C(24, "古代の秘訣"),
 # ── 第1章 なぜ「あなた」なのか ──────────────────────────────────────────
 C(26, "なぜ「あなた」なのか"),
 P(30, "mosquito on human skin macro"),
 P(31, "mosquito close up on leaf"),
 P(32, "mosquito on a flower"),
 P(33, "insect antenna extreme macro"),
 C(34, "最大 50メートル", "二酸化炭素を感知"),
 V(35, "smoke rising slowly against dark sky"),
 P(37, "humid summer evening garden still air"),
 P(38, "asian family sitting on veranda evening"),
 C(39, "刺されやすい人"),
 C(40, "体が大きい", "運動のあと", "体温が高い・汗", "ビールのあと"),
 P(43, "glass of cold beer on a table outdoors"),
 C(44, "血の味では", "ありません"),
 C(45, "のろしが", "少し大きいだけ"),
 P(46, "asian man scratching his arm outdoors"),
 P(48, "蚊取り線香", src="commons"),
 V(50, "electric fan spinning in a dim room"),
 P(51, "spraying insect repellent on arm"),
 C(53, "これまでの虫よけ", "= 隠れる道具"),
 V(54, "incense smoke curling in dark room"),
 C(56, "発想を変えます"),
 C(57, "偽物ののろしを", "庭に立てる"),
 P(59, "bucket of water in a dark garden"),
 P(61, "dry yeast granules macro"),
 # ── 第2章 作り方 ────────────────────────────────────────────────────────
 C(62, "必要なもの 4つ"),
 P(63, "empty white plastic bucket"),
 P(64, "dry yeast in a spoon"),
 C(65, "ドライイースト", "大さじ1 / 約200円"),
 P(66, "brown sugar in a spoon"),
 C(67, "砂糖 大さじ2", "＝酵母のごはん"),
 P(68, "dark brown sugar cubes"),
 P(69, "dish soap bottle on kitchen counter"),
 C(70, "材料費", "合計 300円ほど"),
 C(71, "作り方は5分"),
 P(72, "pouring water into a bucket"),
 P(73, "steam rising from hot water"),
 P(75, "testing water temperature with wrist"),
 P(76, "hands kneading bread dough"),
 P(77, "stirring liquid with a wooden spoon"),
 P(78, "tiny bubbles on liquid surface macro"),
 P(79, "yeast foam bubbles close up"),
 P(80, "freshly baked bread on a kitchen table"),
 C(81, "泡＝発酵の合図"),
 P(82, "fermentation bubbles in a glass jar"),
 P(83, "beer foam bubbles macro"),
 C(84, "酵母が出す二酸化炭素", "＝ 蚊への目印"),
 P(85, "bucket standing in a garden at dusk"),
 C(86, "最後の仕上げ"),
 P(87, "drop of soap falling onto water"),
 C(88, "ここでは絶対に", "かき混ぜない"),
 P(89, "thin film spreading on water surface"),
 C(90, "なぜ洗剤なのか"),
 P(91, "water strider standing on pond surface"),
 P(92, "water droplet surface tension macro"),
 P(93, "soap breaking the water surface"),
 P(94, "insect on the surface of dark water"),
 C(95, "薬の力ではなく", "物理の性質"),
 C(96, "泡が立たない時", "① お湯が熱すぎた", "② イーストが古い"),
 P(98, "two liter clear plastic bottle"),
 P(99, "plastic bottle cut into a funnel diy"),
 P(100, "bottle wrapped in black paper"),
 C(101, "安全上のお願い"),
 C(102, "子ども・ペットの", "手が届かない所へ"),
 P(103, "bee on a flower close up"),
 P(104, "hands wearing rubber gloves"),
 C(105, "偽物ののろし", "完成"),
 P(107, "bucket in a shaded corner of a garden"),
 # ── CTA giữa ────────────────────────────────────────────────────────────
 C(108, "高評価・シェア", "コメント"),
 # ── 第3章 どこに置くか ──────────────────────────────────────────────────
 C(110, "置き場所で", "働きが変わる"),
 P(111, "wooden deck of a japanese house"),
 V(112, "insects swarming in evening light"),
 C(113, "考え方は", "通せんぼ"),
 P(114, "stepping stone path in a garden"),
 P(116, "shady damp corner with bushes"),
 P(117, "puddle in a garden after rain"),
 P(118, "entrance door of a japanese house"),
 P(120, "eaves of a japanese roof in the rain"),
 P(121, "two buckets standing in a garden"),
 C(122, "一つ 300円"),
 P(123, "aerosol spray can on a shelf"),
 C(125, "3〜4日ごとに", "中身を入れ替え"),
 C(126, "週に一度", "置き場所をずらす"),
 C(128, "効き目は", "環境によって差があります"),
 P(130, "quiet garden at night under the moon"),
 # ── 夜の蚊（loop 2 đóng）────────────────────────────────────────────────
 V(131, "dark bedroom at 3am clock"),
 P(132, "asian tiger mosquito striped legs macro"),
 P(133, "mosquito biting an ankle"),
 P(134, "person sleeping in a dark bedroom"),
 C(135, "ヤブカ＝昼の庭", "イエカ＝夜の寝室"),
 C(136, "なぜ、耳のそばなのか"),
 C(137, "狙いは", "耳ではありません"),
 P(138, "sleeping face in dim light"),
 C(139, "口と鼻から流れ出る", "二酸化炭素の流れ"),
 P(140, "mosquito flying in the dark"),
 P(141, "human ear close up"),
 C(142, "蚊は耳を", "狙っていない"),
 C(144, "昼の庭も 夜の枕元も", "同じ一つの合図"),
 # ── 第4章 江戸の知恵 ────────────────────────────────────────────────────
 P(147, "江戸", src="commons"),
 P(148, "蚊帳", src="commons"),
 P(149, "green mesh fabric texture"),
 P(150, "child hiding under a canopy"),
 C(151, "「早くお入り。", "蚊が入るよ」"),
 P(152, "sheer curtain being lifted"),
 P(154, "looking up at a green mesh canopy"),
 P(155, "dim light bulb glowing at night"),
 C(156, "風は通す", "蚊は通さない"),
 C(157, "電気も薬も", "使わない道具"),
 P(158, "old japanese closet with folded futon"),
 P(159, "aluminum window screen mesh"),
 P(160, "mosquito net bed malaria prevention africa"),
 C(161, "捨てられた道具ではなく", "海を渡った知恵"),
 C(163, "追い払うより", "湧かせないほうが早い"),
 P(164, "stagnant water puddle close up"),
 P(165, "water collected in a bottle cap"),
 P(166, "mosquito larvae in water macro"),
 P(167, "plant pot saucer filled with water"),
 P(168, "old watering can in a garden"),
 C(168 + 0, "蚊のゆりかご", "受け皿・じょうろ・雨どい", accent=False) if False else P(170, "rain barrel in an old town"),
 P(169, "天水桶", src="commons"),
 P(171, "green algae water in a barrel"),
 P(172, "goldfish swimming in a water bowl"),
 C(173, "生き物に", "働いてもらう"),
 P(174, "十円硬貨", src="commons"),
 C(175, "言い伝えとして", "頭の隅に置く程度に", accent=False),
 P(177, "hands tipping water out of a saucer"),
 C(178, "なぜ、週に一度？"),
 C(179, "卵から成虫まで", "およそ10日"),
 C(180, "7日ごとに水を捨てる", "→ 羽化が間に合わない"),
 C(181, "蚊の暦の", "裏をかく"),
 # ── 第5章 お金の流れ ────────────────────────────────────────────────────
 C(183, "なぜ売り場では", "教えてくれないのか"),
 P(186, "蚊遣豚", src="commons"),
 P(187, "thin smoke rising against dark background"),
 P(188, "burning incense coil ash"),
 C(190, "1890年", "上山英一郎"),
 C(191, "1895年ごろ", "渦巻き型が誕生"),
 P(192, "coiled snake on the ground"),
 P(193, "除虫菊", src="commons"),
 P(194, "field of white daisies on a hillside"),
 C(195, "あの夏の匂いは", "植物の知恵だった"),
 P(196, "abandoned overgrown field"),
 P(197, "supermarket aisle with products"),
 P(198, "empty aerosol cans"),
 P(199, "store shelf with summer goods"),
 C(200, "数百円 × ひと夏", "× 毎年 × 日本中"),
 C(201, "大きな、大きな市場"),
 C(202, "既製品が", "悪いのではありません", accent=False),
 C(204, "バケツと砂糖は", "誰の売上にもならない"),
 C(207, "知っているか", "知らないか"),
 # ── Kết 3 lớp ───────────────────────────────────────────────────────────
 C(209, "正直なところ"),
 C(210, "万能では", "ありません"),
 C(212, "① 発生源の水を断つ", "② 置き場所を工夫する"),
 P(214, "marigold flowers in a garden"),
 P(215, "lavender flowers in a summer garden"),
 C(216, "今日の芯"),
 P(217, "mosquito flying at dusk"),
 C(219, "追い払うのではなく", "道の途中で先回り"),
 C(220, "一つに", "頼り切らない"),
 C(222, "どれから試しますか？"),
 P(225, "dusty window sliding door track"),
 P(226, "cleaning a window sash groove"),
 C(228, "古代の秘訣"),
]

# ── VÒNG 2 QUERY: sửa 28 ô lệch phát hiện khi duyệt contact sheet 2026-07-30 ──
# Lý do lệch: ① Pexels trả người TÂY cho query có "japanese/asian" ② query khái niệm
# (thin film / antenna) trả vật khác hẳn ③ Commons hụt token. Vật Nhật đặc thù → Commons.
FIX = {
  0:   ("commons", "縁側"),                       # gia đình Tây trên hiên → hiên nhà Nhật thật
  1:   ("card",    ["隣の人は", "平気な顔"]),        # không có ảnh nào tả được ý này
  13:  ("commons", "ドライイースト"),                # cục bột mặt cười giữa lá thu
  15:  ("commons", "日本橋"),                       # ukiyo-e võ sĩ → phố Edo
  17:  ("photo",   "glowing alarm clock in a dark bedroom"),   # clip đen thui
  33:  ("photo",   "mosquito head close up macro"),            # ra mặt bọ cánh cứng xanh
  38:  ("photo",   "japanese paper lantern glowing at night"), # lại gia đình Tây
  48:  ("photo",   "green mosquito coil spiral"),              # Commons trả bánh sandwich
  61:  ("photo",   "active dry yeast granules in a bowl"),     # ra hạt nâu như cám
  63:  ("photo",   "white bucket on the grass"),               # ra góc phòng tối
  68:  ("photo",   "brown sugar in a wooden bowl"),            # nền vàng chóe phá style
  72:  ("photo",   "pouring water from a kettle into a bowl"), # ảnh đen trắng dội đầu
  75:  ("photo",   "hand touching warm water"),                # găng tay siêu thực nền cyan
  77:  ("photo",   "wooden spoon stirring a bowl of liquid"),  # nồi trên bếp gas
  85:  ("photo",   "metal bucket on the ground in a garden"),  # cô gái tóc vàng
  89:  ("photo",   "oil film on water surface rainbow"),       # vân đá xám
  91:  ("commons", "アメンボ"),                     # ra muỗi trên nền trắng
  99:  ("photo",   "empty plastic bottle cut in half"),        # phễu thủy tinh phòng lab
  107: ("photo",   "watering can in a shady garden corner"),   # sân sau đen trắng lộn xộn
  112: ("photo",   "wooden terrace table and chairs in a garden"),  # clip ra con bọ ngựa
  118: ("commons", "玄関"),                        # ảnh đen trắng
  138: ("photo",   "asian man sleeping in bed"),               # mặt Tây có râu
  148: ("photo",   "green mosquito net canopy over a futon"),  # Commons ra mùng kiểu Tây
  154: ("photo",   "view from inside a mosquito net"),         # ra tán cây nhìn lên
  167: ("photo",   "water in a plant pot saucer close up"),    # nhà kính, không thấy đĩa lót
  177: ("photo",   "hands pouring water out of a small dish"), # tay cầm ly rượu bên suối
  197: ("photo",   "shelves of household cleaning products"),  # biển chữ Bắc Âu dễ nhận ra
  225: ("photo",   "dirty window sill and rail close up"),     # ảnh bokeh chữ "Slide Door"
}
# ── VÒNG 3: duyệt sheet lần 2 → 9 ô vẫn lệch. 3 ô đổi query, 6 ô HẠ THÀNH CARD.
# Nguyên tắc: thà card chữ đúng còn hơn ảnh stock sai (user chốt "text phải khớp hình").
FIX.update({
  63:  ("card", ["① バケツ", "（大きめの容器）"]),          # 2 lần fetch: ra CON CHÓ trong xô, rồi chợ bán xô nhựa loạn màu
  75:  ("photo", "hand in a basin of water"),       # "hand touching warm water" → ra tay chạm sóng BIỂN
  225: ("card", ["次回：", "窓とサッシ"]),                   # 2 lần fetch: ống kim loại gỉ, rồi phủi bụi khung ảnh
  13:  ("card", ["イースト・砂糖", "食器用洗剤"]),        # Commons ドライイースト → ra cốc + bánh mì
  48:  ("card", ["それでも、", "刺される"]),             # "green mosquito coil" → ra vòi nước cuộn
  118: ("card", ["玄関・勝手口の", "わきも良い"]),         # Commons 玄関 → ra cửa đá kiểu La Mã
  154: ("card", ["中から見上げる", "薄い緑の天井"]),       # trùng Y HỆT ảnh slide 85 (蚊帳) → phải tách
  177: ("card", ["週に一度", "水を捨てる"]),             # ra cảnh rưới sốt lên ĐĨA THỨC ĂN
  197: ("card", ["毎年買い直す", "使い切りの商品"]),       # kệ hàng lộ NHÃN HIỆU thật (Pepsi/Ajax) — compliance
})

_byi = {e["_i"]: e for e in S if e}
for ln, (kind, val) in FIX.items():
    e = _byi.get(ln)
    if e is None:
        raise SystemExit("FIX tro vao dong %d khong co trong SLIDES" % ln)
    for k in ("q", "qv", "src", "lines", "accent", "min_score", "video", "photo"):
        e.pop(k, None)
    if kind == "card":
        e.update({"photo": False, "lines": val, "accent": True})
    else:
        e.update({"photo": True, "q": val, "min_score": 0.9})
        if kind == "commons":
            e["src"] = "commons"

# ── THƯA BỚT: nhịp chuẩn kênh ~11-13s/slide (video 07: 109 slide/24'). ─────
# Bỏ entry trùng ý với entry liền kề, giữ nguyên vùng hook (0-26) vốn cần cắt nhanh.
DROP = {9, 11, 31, 32, 37, 51, 59, 64, 66, 67, 73, 76, 79, 82, 83, 93, 94, 100,
        104, 105, 114, 117, 121, 122, 123, 130, 133, 140, 141, 149, 150, 152,
        155, 159, 164, 165, 168, 170, 171, 175, 187, 192, 194, 196, 198, 199,
        202, 215, 216, 217, 226}

# ── validate + xuất ────────────────────────────────────────────────────────
S = [e for e in S if e and e["_i"] not in DROP]
S.sort(key=lambda e: e["_i"])
errs = []
seen = set()
out = []
for e in S:
    i = e.pop("_i")
    if i in seen:
        errs.append("trung dong %d" % i); continue
    seen.add(i)
    if i >= len(lines):
        errs.append("dong %d vuot file" % i); continue
    src = lines[i]
    m = src[:24] if len(src) > 24 else src
    if m not in src:
        errs.append("match hong o dong %d" % i); continue
    hits = sum(1 for l in lines if m in l)
    if hits != 1:
        errs.append("match KHONG DUY NHAT (%d hit) dong %d: %s" % (hits, i, m)); continue
    out.append({"match": m, **e})

if errs:
    print("LOI:"); [print("  -", x) for x in errs]; sys.exit(1)

io.open(OUT, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
np = sum(1 for e in out if e.get("photo") is True)
nv = sum(1 for e in out if e.get("video"))
nc = sum(1 for e in out if e.get("photo") is False)
print("OK -> %s" % OUT)
print("tong %d entry | anh %d | clip %d | card %d" % (len(out), np, nv, nc))
print("mat do: 1 slide / %.1f dong doc" % (len(lines) / len(out)))
