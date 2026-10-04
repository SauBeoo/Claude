# 22 — ラーメン：汁を半分で、血管を守る（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI
- **Chủ đề:** ラーメンが血管・血圧・コレステロールに与える影響 × 「注文のひと言」で防ぐ工夫
- **Bản đọc chuẩn:** `22_ramen-kekkan_TTS.md` — **4.128 ký (thuần) · 147 dòng · ước 16′15** (mô hình CPS 4.40 + GAP 0.25/dòng). Nằm trong dải chuẩn kênh **dưới 20 phút** (`CLAUDE.md` §①).
- **⛔ GATE MÁY:** `python tools\check_coldopen.py 22` → ✅ **PASS, cold open 86 giây** (L1–L5 · S6 · S7 sạch, dư 4s so trần 90s) · 0 tag giữa câu · 0 tag đứng dòng riêng ngoài base · blacklist Mục 7 = 0 · whitelist ≥12 loại · S8 9 điểm cảnh báo (không chặn, gate tự nhận chưa hiệu chuẩn), đã soi mắt: khối persona/CTA bắt buộc và khối cơ chế thiếu "con số có đơn vị" theo định nghĩa hẹp — không phải đoạn trang trí, giữ nguyên.

### v2 (sau đánh giá + sửa theo yêu cầu user 2026-08-30) — 3 sửa thật, không phải chỉnh câu chữ

1. **Hook 30 giây:** câu stake gốc chồng 2 lớp hedge (「思いがけない負担が…かもしれません」), đẩy sự thật mạnh nhất (một tô có thể vượt cả định mức muối một ngày) xuống sâu trong ITEM1. → Đưa thẳng câu "一杯の塩分だけで、一日分の目安を、超えてしまうことがあります" lên làm cú đánh thứ ba của cold open (~giây 20), bớt hedge chồng.
2. **⭐ Gộp 3 ẩn dụ rời rạc (ゴムホース／排水溝／砂糖を焦がす) thành MỘT ẩn dụ trung tâm nuôi suốt bài:** 血管 = **家中を巡る一本の水道管**. Ba cạm bẫy giờ là ba cách ống hỏng — 塩 → **硬くなる**、脂 → **詰まる**（台所の排水管の喩え giữ lại nhưng gắn vào "cùng một ống"）、血糖値スパイク → **サビる**（「血管のサビ」là cách nói quen thuộc trong truyền thông sức khỏe Nhật, không phải ẩn dụ tự chế). Recap cuối callback đủ cả ba: 「塩で、硬くなる。脂で、詰まる。糖で、サビる。」— đúng khuôn "một ẩn dụ duy nhất" đã chứng minh hiệu quả ở video 19.
3. **Sửa điểm ngắt trước khối chào hỏi:** bản cũ gài hook cho mục 2 (「血管を痛めつけるのは、塩分だけではありません」) rồi cắt ngay sang chào — cảm giác bị ngắt quảng cáo giữa cao trào. → Đóng trọn mục 1 bằng một câu chốt riêng (「塩分は、水道管を、硬くする。」) rồi mới chuyển sang nghỉ có chủ ý (「さて、ここで少し、休憩をかねて」), và khi quay lại thì mở bằng đúng câu "さて、水道管のお話に、戻りましょう" — nối liền mạch thay vì bắt đầu lại.

⚠️ **Trung thực về giới hạn:** đây là sửa theo đúng nguyên tắc đã đo được của kênh (một ẩn dụ · payoff sớm · không tự tháo ngòi) và qua hết gate máy — nhưng "9–10 điểm" thật sự chỉ đo được bằng đường cong retention sau khi video lên sóng, không phải thứ khẳng định trước được. Coi đây là bản đã sửa đúng chỗ hỏng đã chỉ ra, không phải cam kết điểm số.

---

## 1. Người xem đến vì cái gì, ở lại vì cái gì

- **Đến vì:** thumbnail/title hứa "ラーメンの汁が体を傷つける" — nỗi sợ quen thuộc của người thích ăn ramen nhưng canh cánh với huyết áp/mỡ máu. Stake không phải chỉ số xét nghiệm mà là **むくみ・靴下の跡・薄味が物足りない → 血管が硬くなる → 高血圧・動脈硬化**.
- **Ở lại vì:** open loop lớn xuyên suốt — **「いつもの注文にたったひと言」** (hứa ở cold open ~80s, trả ở ~72% thời lượng = 「汁は、半分で大丈夫です」), cộng 3 cơ chế cụ thể (塩分 → ゴムホースの喩え, 脂 → 排水溝の喩え, 血糖値スパイク → 砂糖を焦がす喩え) mỗi cái đều có 1 nguồn thật + 1 hành động làm được ngay tối nay.

## 2. STAKE & KHUÔN

1. **3 ẩn dụ độc lập, mỗi cái gắn 1 cơ quan/cơ chế:** 血管 = 若い頃はしなやかな**ゴムホース**、塩分で硬くもろくなる · 脂の蓄積 = **台所の排水溝**にこびりつく油汚れ · 血糖値スパイク = 鍋の底で**お砂糖を焦がす**。Ba ẩn dụ đều là hình ảnh gian bếp quen thuộc với tệp 60–80.
2. **Open loop = HÀNH ĐỘNG, không phải kiến thức:** twist đặt câu trả lời ở ngay quán quen của khán giả — 「汁は、半分で大丈夫です」, một câu nói khi gọi món, không phải công thức hay số liệu phải nhớ.
3. **Nguồn thật giữ nguyên tên** (không bịa số): 厚生労働省「日本人の食事摂取基準」目標量 (男性ななてんごグラム未満／女性ろくてんごグラム未満) · 日本高血圧学会 (高血圧の方の目安ろくグラム未満) · 世界保健機関WHO (ごグラム未満)。Số liệu về lượng muối trong nước súp ramen (ろく〜はちグラム/杯) và cơ chế đường huyết/AGE dùng hedge 「という報告があります」「と考えられています」, KHÔNG gắn tên tổ chức vì không chắc nguồn chính xác — đúng luật Mục 11.
4. **Chất người ≥4/6 mũi tiêm:** ① みのり tự thú 「寒い日に、あの汁を、つい飲み干したくなる気持ち、私もよく分かります」+ tự thử nghiệm câu nói ở quán quen ② 正治さん có thoại 「あんなに好きなもの、やめられるわけないだろう」+ chi tiết đời sống vô dụng-về-thông-tin (盆栽の手入れが日課) ③ ký ức giác quan mở bài (湯気・豚骨と醤油の匂い) ④ みのり tự dùng câu 「汁は半分で大丈夫です」ở quán thật ⑤ 幸子さん đóng bằng cảm xúc 「同じラーメンなのに、体が、ちょっと軽くなった気がするの」+ chi tiết đời sống (教え子から届く着物の相談) ⑥ phá nhịp 「それだけです。」「たったひと言だけ。」lặp lại như điệp khúc.
5. **YMYL đúng luật:** cảnh báo thuốc huyết áp/cholesterol đặt ngay sau payoff #1 (khối persona) — KHÔNG trong cold open (giữ L2 sạch) — và nhắc lại trong disclaimer cuối.

**Mốc thời gian (ước từ mô hình CPS, cập nhật lại từ `subs.srt` sau render):**

| mốc ước | khối |
|---|---|
| 00:00–01:25 | Cold open: stake + 3 câu triệu chứng + friction release + open loop tease |
| 01:25 | **# ITEM1 = 落とし穴①塩分** (đúng luật payoff sớm) |
| ~03:40 | khối persona + xin đăng ký + câu hỏi tỉnh thành (SAU mục đầu ✅) |
| ~04:10 | cảnh báo thuốc huyết áp/cholesterol (YMYL, đặt sau payoff #1) |
| ~05:10 | 落とし穴②脂 (排水溝の喩え) |
| ~07:00 | anecdote 1 — 三重県・正治さん(69) |
| ~07:40 | **CTA giữa + checkpoint「に」** |
| ~08:10 | 落とし穴③血糖値スパイク (お砂糖を焦がす喩え) |
| ~10:00 | checkpoint「さん」ngay trước khi trả loop |
| ~10:20 | **TRẢ OPEN LOOP:「汁は、半分で大丈夫です」** (~65–70%) |
| ~11:30 | anecdote 2 — 山形県・幸子さん(73) |
| ~12:40 | recap + kết 4 lớp + disclaimer + câu kết cố định |
| ~15:48 | hết |

## 3. Bộ title A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代の落とし穴】ラーメンの汁が体を老けさせる理由｜注文の「ひと言」` | 34 | ラーメン@10 | khung cảnh báo P0 + payoff hành động cụ thể |
| **A2** | `60歳を過ぎたら要注意｜ラーメンの塩分が「あの数値」に与える影響` | 32 | ラーメン@12 | đổi keyword dẫn sang 塩分/số liệu (P3 ngưỡng số) |
| **A3** | `ラーメンは、本当に体に悪いのか｜内側が喜ぶ意外な食べ方` | 27 | ラーメン@1 | đổi kiểu hook: P5 câu hỏi trực diện + đảo nhận thức |

⚠️ Cả 3 bản **tránh chữ 血 (血管・血圧・血糖) và 透析** theo Phần E của skill (từ nhạy title/thumbnail) — thay bằng 体／内側／あの数値／老けさせる. Từ 血管・血圧・コレステロール vẫn dùng đầy đủ ở 概要欄/tag (Mục 9 dưới).

### Title CHỐT

```
【60代の落とし穴】ラーメンの汁が体を老けさせる理由｜注文の「ひと言」
```

**Tên file upload:** `ramen-shio-kekkan-60dai.mp4`

## 4. TEXT THUMBNAIL (3 dòng — HÀNH VI → HẬU QUẢ → ĐÁP ÁN GIẤU)

| dòng | chữ | ký | vai (gate 7 `audience-45plus.md` §1) | màu |
|---|---|---|---|---|
| 1 | `ラーメン` | 4 | **① VỀ CÁI GÌ** | 白/クリーム |
| 2 | `体が悲鳴` | 4 | **② CHUYỆN GÌ XẢY RA** — hero, loss-aversion | **VÀNG KIM, to nhất** |
| 3 | `汁は半分で` | 5 | **③ PHẢI LÀM GÌ** — đáp án hành động, khớp open loop | **ĐỎ** |

- Che ảnh vẫn đọc ra: "ラーメン — 体が悲鳴 — 汁は半分で" ✅ gate 7.
- Không chữ 血/透析, không 医師/専門家, không claim khỏi bệnh. Gate 1 (≤6 ký/dòng) ✅ · gate 3 (đúng 3 dòng) ✅.

## 5. PROMPT ẢNH THUMBNAIL (theo khuôn đã lên sóng — bà cụ "gương mặt kênh")

Khuôn lấy từ ảnh đã dùng ở video 16–19 (`02_THUMBNAIL_TITLE_RULES.md` Phần D/E): photorealistic, ánh sáng ban ngày sáng rõ, bà cụ ~68 tuổi tóc bạc ngắn + tạp dề be trên áo cardigan xanh, con dấu tròn ĐỎ 「食卓」, dải vàng kim mép, chữ 3 dòng 袋文字 viền nâu đậm + halo trắng, hero to nhất chiếm ≥1/3 chiều cao/rộng khung.

**Prompt nháp (tiếng Anh, cần soi + vá watermark sau khi gen):**
```
Photorealistic kitchen-table scene, bright daylight, high contrast, no shadows.
TEXT, exactly these 3 blocks and nothing else:
line 1, white/cream: "ラーメン"
line 2, LARGEST, golden yellow with thick brown outline and white halo: "体が悲鳴"
line 3, red with thick brown outline: "汁は半分で"
LAYOUT: text column occupies left half, large steaming bowl of ramen lower-right filling
about half the frame, Japanese woman late 60s with short gray hair, beige apron over
teal cardigan, mildly surprised/concerned expression (not painful), holding chopsticks,
looking at the bowl. Red circular stamp reading "食卓" top-right corner. Thin gold ribbon
along the right edge. Keep the very bottom-right corner free of text.
Text must be perfectly formed Japanese characters, crisp and legible. No watermark, no
logo, no signature, no additional text, no doctors, no white coats. --ar 16:9
```

Xuất theo `ab-3title-3thumb.md` §3.1 Bước 4: `thumb_prompts_FLOW.txt` (1 dòng/prompt) + `thumb_prompts_BLOCKS.md` (bản đọc) + `thumb_prompts_TENFILE.txt` + `thumb_prompts_PLATE.txt` (3 plate không chữ dự phòng). T1 baseline khuôn kênh · T2 đổi 1 biến hình (crop cận mặt/tô) · T3 đổi layout (đảo trục chữ/người).

## 6. QUÉT COMPLIANCE (`.claude/rules/youtube-compliance.md` + skill Mục 15E)

1. **Title/thumbnail:** không 殺/死/自殺/レイプ/虐待 · **không 血/透析** (đã thay bằng 体/内側/あの数値) · không 医師が解説/医師警告. ✅
2. **Persona:** みのり không xưng 医師/管理栄養士/専門家; script không có khối credential (S7 gate = 0 vi phạm). ✅
3. **Không tên thật** hãng/cửa hàng ramen cụ thể/người thật. Nguồn nêu đích danh là cơ quan có thật: 厚生労働省「日本人の食事摂取基準」・日本高血圧学会・世界保健機関(WHO). ✅
4. **YMYL:** 0 lần 治る/完治/薬の代わり/絶対 · cảnh báo thuốc huyết áp/cholesterol đặt ngay sau payoff #1 + nhắc lại trong disclaimer cuối · disclaimer cố định ✅. Không khuyên ngừng/giảm thuốc.
5. **Thumbnail** nhân vật AI hư cấu + món ăn → không cần tick synthetic. Nếu dùng ảnh AI làm slide TRONG video (minh hoạ pastel theo format chốt cứng của kênh) → tick theo `youtube-compliance.md` §2.1.
6. **Tình tiết** đều có thật trong video (3 cơ chế + 1 twist hành động) — không hứa cảnh không tồn tại.

## 7. TAG + HASHTAG + 概要欄

### タグ
```
60代からの食卓,シニアの健康,60代の食事,ラーメン,ラーメン 塩分,ラーメン 血管,ラーメン 血圧,塩分の摂りすぎ,動脈硬化,悪玉コレステロール,血糖値スパイク,高血圧学会,厚生労働省 食事摂取基準,60歳からの健康,70代 健康,シニア 食事,つけ麺,インスタントラーメン,健康長寿,老後の健康,高齢者 食事,むくみ 塩分,血管年齢,食べ方の工夫,健康雑学,シニアライフ,みのり
```

### 概要欄 — 3 DÒNG ĐẦU
```
「あの汁を、つい飲み干してしまう」——六十代からのラーメンは、汁の量ひとつで、血管への負担が大きく変わります。
この動画では、塩分・脂・血糖値スパイクという三つの落とし穴と、注文のときにたったひと言添えるだけの、続けやすい工夫をお話しします。
ラーメンが大好きな六十代・七十代のご本人と、離れて暮らすご家族に向けた、台所の言葉だけでお伝えする回です。
```

### 概要欄 — MÔ TẢ ĐẦY ĐỦ
```
「あの汁を、つい飲み干してしまう」——六十代からのラーメンは、汁の量ひとつで、血管への負担が大きく変わります。
この動画では、塩分・脂・血糖値スパイクという三つの落とし穴と、注文のときにたったひと言添えるだけの、続けやすい工夫をお話しします。
ラーメンが大好きな六十代・七十代のご本人と、離れて暮らすご家族に向けた、台所の言葉だけでお伝えする回です。

厚生労働省の「日本人の食事摂取基準」では、一日の塩分の目標量を男性でななてんごグラム未満、女性でろくてんごグラム未満としています。
すでに血圧が高めの方については、日本高血圧学会が、さらに厳しく一日ろくグラム未満を目安とし、世界保健機関(WHO)の目標はごグラム未満です。
ラーメンの汁を一杯飲み干すだけで、ろくグラムからはちグラムほどの塩分になるという報告もあります。
けれども、我慢してラーメンをやめる必要はありません。汁を半分残す、脂をレンゲでよける、野菜を先に一口——それだけで、続けやすい工夫になります。

【この動画でお話しすること】
00:00 湯気の向こうから——ラーメンと血管の話
01:26 落とし穴①：塩分が水道管を硬くする
04:31 ごあいさつと、大切なお願い
05:42 落とし穴②：脂が水道管を詰まらせる
07:46 三重県・正治さんの話
08:52 応援のお願い
09:29 落とし穴③：血糖値スパイクが水道管をサビさせる
11:32 お約束していた「注文のひと言」の正体
12:37 山形県・幸子さんの話
13:48 今日のまとめ

【出典】
・厚生労働省「日本人の食事摂取基準」
・日本高血圧学会 減塩の目安
・世界保健機関(WHO)塩分摂取目標

※この動画は、公表されている研究や公的資料をもとにした、健康に関する一般的な情報です。お一人おひとりに合わせた医療のアドバイスではありません。とくに血圧やコレステロールのお薬を服用されている方は、食事の目安が人によって異なる場合があります。持病のある方やお薬を飲んでいる方は、食事を変える前に、必ずかかりつけの先生にご相談ください。

音声：VOICEVOX:青山龍星

#60代からの食卓 #シニアの健康 #60代の食事 #ラーメン #高血圧予防
```

## 8. HANDOFF（format chốt cứng — remotion-vox）

```
py tools\build_slides_22.py                # PLAN + prompt FLOW -> user gen ảnh pastel
py tools\cutout_cast.py                     # chỉ khi cần cast mới (nền magenta)
py tools\ingest_slides_22.py                # trim viền + vá watermark + khung sân khấu
py ..\remotion-vox\tools\import_pipeline.py
py ..\remotion-vox\tools\build_overlays_22.py
run_full22.cmd                              # chạy NỀN (render-background.md), deliver --mp4 bắt buộc
```

⚠️ Chưa có `build_slides_22.py`/`ingest_slides_22.py` — cần tạo theo mẫu video 18/19 trước khi render. Sau render: cập nhật 目次 ở §7 bằng mốc thật từ `subs.srt`.
