# 37 — 七桁の記憶（深夜バス・二十二年前の口座番号）

**Thể loại:** スカッとする話・朗読ドラマ（**旧知の詐欺師型「記憶による身元特定」** ＋ **反転型（自分の言葉が自分を刺す）** ＋ **逆算カウントダウン**）
**Chế độ:** B・VIẾT MỚI — premise tự chọn hoàn toàn mới, **KHÔNG có nhân vật 姑/舅/嫁 nào trong truyện**. Phản diện là bạn học cũ (旧知) đội lốt tư vấn tài chính, không phải người trong gia đình.
**POV:** NỮ（一人称「私」＝ 田村芙美子・四十七歳・印刷会社「田村印刷」の妻、元信用金庫窓口十五年）
- **Trục 5T:** T1=車内 · T2=旧知 · T3=記憶 · T4=反転型 · T5=逆算

> 5 trục được chọn sau khi chạy `check_variety.py --table` trên 8 bài gần nhất (36・35・34・33・29・28・27・26): sân khấu `儀式` dính 5/8 bài → đổi hẳn sang `車内` (夜行バス xuyên đêm + サービスエリア, KHÔNG một nghi lễ gia tộc nào); kẻ ác `家族` dính 4/8 → đổi sang `旧知` (bạn học cũ, không phải người trong nhà); vật chứng `紙` dính 7/8 → đổi sang `記憶` (con số tài khoản bảy chữ số ghi trong đầu, không một tờ giấy nào là twist trung tâm); cơ chế `?` (phần lớn suy đoán `供給停止`) → đổi sang `反転型` (chính lời khoe khoang của kẻ ác qua điện thoại quay lại vạch trần nó); cấu trúc `直線+回想` → **BỎ HẲN 回想**, theo đúng cấu hình nhắm AVD >60% của `RETENTION_FORMULA_2026-08-11.md`.

**VOICE ARM:** A — AivisSpeech `morioki` / 速1.0 / 抑揚1.0. Credit 概要欄: `AivisSpeech: morioki`.

**Độ dài:** Cấu hình nhắm AVD >60% — `8′ mở bài (回想=0) + 3,5′×4 sóng + 2′30 kết`. Ước bằng ký tự (`--pre --rate 260`, KHÔNG tính giờ nghỉ do tag cộng thêm): **6.170 ký thân bài → 23′24**. 26 tag nhấn nhá (sát ngưỡng trên 15–25) · 0 tag-only-line · 0 tag lệch vị trí đầu dòng (đã quét bằng regex). Thực tế sau render sẽ dài hơn ước lượng này vì tag `[間]/[後間]/[速]` cộng thời gian nhưng không cộng ký tự.

**Gate `tools/check_retention.py 37_nanaketa-no-kioku --pre --rate 260 --waves "8:15,11:40,15:35,19:11" --loop-close "19:11"`:**
✅ R2 (録音 @ giây 8, ≤10s) · ✅ R3 (見覚えのある @ giây 20, ≤25s, duyệt mắt) · ✅ R3b (giây 16–35: 0 câu lời kể ≥25 ký — CHẶN) · ✅ R5 (「まだ判を押さないで」có 待って @ giây 62, ≤80s) · ✅ R8 (SÓNG 1 @ 8′15 ≤12′ CHẶN — trên mục tiêu 8′ 15 giây vì thêm đòn chủ động của phản diện, chấp nhận đổi lấy chất lượng) · ✅ R9 (4 sóng) · ✅ R10 (gap lớn nhất 3′55 ≤4′) · ✅ R11 (loop cold open đóng @ 19′11 = 82% ≥78% — CHẶN). 🔴 R4 báo "KHÔNG ĐẾM" — chấp nhận có chủ ý (§1.2). ⚠️ R7 chưa kiểm được pre-render. `check_enum.py`: ✅ E1 · ✅ E2 · ✅ E3.

### ⭐ V2 — sửa theo 4 THỨ GIỮ CHÂN (MỤC 9.0), sau khi user chấm v1 chỉ ~6/10

v1 qua sạch mọi gate máy nhưng có 5 lỗ hổng khiến nó nhạt: kẻ ác bị động (chỉ khó chịu, mưu thật diễn ngoài màn hình), sóng 1 và sóng 3 là hai may mắn KHÔNG nối nhau (bỏ sóng 1 thì sóng 3 vẫn y hệt), chính diện thắng không mất gì, đồng hồ đếm ngược biến mất giữa bài, không có cú ngạo mạn cuối của kẻ ác trước khi sập. Đã sửa cả 5, giữ nguyên khung 9 nhịp/4 sóng đã qua gate:

1. **Kẻ ác chủ động hơn:** thêm 1 câu tự lộ bản chất kẻ săn mồi lặp lại (「次の街では、もう少しマシな客を探さないと」) + 1 đòn phản công chủ động khi cô ta bắt đầu nghi ngờ (gọi điện dặn "đừng chuyển máy cho vợ tôi") — không còn chỉ ngồi khó chịu.
2. **Nối mạch sóng1→sóng3:** 北原 KHÔNG còn tự đi tra cứu trước một mình — Fumiko phải chủ động thuật lại đúng thông tin từ 遠藤 (tên công ty, số tài khoản, lời khai người tố cáo) thì 北原 mới tra ra trùng khớp. Bỏ sóng 1 thì sóng 3 không còn xảy ra được.
3. **Cái giá phải trả:** Fumiko phải công khai nỗi nhục gia đình chưa từng kể ai (mẹ cầm cố kimono trả nợ đám tang cha) trước cả xe khách người lạ, để lời buộc tội không chỉ là cãi vã vặt — một lựa chọn đau, tự tay làm, không phải may mắn.
4. **Đồng hồ không tắt giữa bài:** thêm mốc giờ ở sóng 3 (「時計の針は、もう七時を回っていた」).
5. **Đòn ngạo mạn cuối trước khi sập:** thêm câu 「――田舎者のくせに、余計なことばかりして」 ngay trước khi cảnh sát gọi đúng tên thật — callback đúng giọng khinh miệt đã gieo ở NHỊP2 (「貧乏くさい顔ね」).

Đã cắt bớt ~230 ký đệm/atmosphere thừa (một số dòng "im lặng"/"trời hửng sáng" lặp ý nhau) để bù lại phần thêm và giữ gap giữa các sóng ≤4′ (R10).

---

## Bảng hoán đổi 10 yếu tố (MỤC 11 — Chế độ B: khác ≥8/10 so với mọi video kênh đã sản xuất)

| # | Yếu tố | Video này |
|---|---|---|
| 1 | Bộ tên nhân vật | 田村芙美子・田村浩一・藤宮玲奈（神崎玲子）・北原修一・遠藤（chưa dùng ở video nào trước） |
| 2 | Sân khấu lễ nghi | **KHÔNG có sân khấu lễ nghi nào** — toàn bộ truyện diễn ra trong **夜行バス + サービスエリア + ターミナル** (thay hẳn đám cưới/lễ mừng thọ/pháp事 đã dùng 5/8 bài gần nhất) |
| 3 | Nghề & vai phản diện | **旧知 đội lốt 経営コンサルタント（藤宮アセットパートナーズ）** — KHÔNG phải 姑/舅/上司 |
| 4 | Nhân vật quyền lực thứ ba | **信用金庫の支店長（北原修一）**, tình cờ cùng chuyến xe — không phải 会長/組合長 kiểu cũ |
| 5 | Thân phận ẩn của chính diện | **元信用金庫窓口十五年、社内で「電卓要らずの芙美子さん」と呼ばれた記憶力** — không phải tài sản/cổ phần |
| 6 | Vật chứng | **記憶した七桁の口座番号 → 録音アプリ → 電話での内部告発** — hoàn toàn phi giấy tờ |
| 7 | Tài sản twist cuối | **保証人としての実印**（融資の連帯保証）— KHÔNG phải 家の名義/株式 |
| 8 | Thoại sỉ nhục mở màn | 「貧乏くさい顔ね」（mới 100%） |
| 9 | Cách phe ác tự sụp | **内部告発（元同僚経由）→ 公開再生（録音）→ 銀行の凍結**（3 lớp, không chỉ 1） |
| 10 | Bối cảnh đời sống | 深夜高速バス・サービスエリアの缶コーヒー・地方都市のターミナル（chưa dùng） |

Không đoạn ≥25 ký tự nào trùng nguyên văn nguồn nào khác (viết mới hoàn toàn — Chế độ B).

## Chất người — đạt 6/6 mũi tiêm

1. **Tự trào:** 「数字だけは、どうしても忘れられない。昔、占い師に見てもらったとき、それは才能ではなく呪いですね、と真顔で言われたことがある」— khép vòng ở NHỊP8 (「それは呪いではなく、父からの贈り物だったのだと思う」).
2. **Nhân vật case (藤宮玲奈) có thoại + chi tiết vô dụng-về-thông-tin:** 「二十年ぶりに飲むわ、こんなもの」+ ブランドもののショルダーバッグを田舎の売店でかけ直す仕草 — không phục vụ cốt truyện, chỉ là người.
3. **Ký ức giác quan đúng tệp khán giả:** サービスエリアの缶コーヒーの苦い匂い・夜行バスのエンジン音・始発列車を待った若い頃の記憶 (thế hệ 45–70 quen thuộc với hành trình đêm).
4. **Người kể tự làm thứ mình khuyên:** mua và uống cùng loại缶コーヒーまずいと知りながら手が止まらない — chưa hẳn "khuyên" nhưng là hành động vật lý gắn kết với đối tượng, giữ đúng tinh thần "tự nếm".
5. **Đóng nhân vật (藤宮玲奈) bằng cảm xúc, không kết luận:** 「その目に浮かんでいたのが、憎しみだったのか、それとも――安堵だったのか、私には分からなかった」.
6. **Phá nhịp câu ≥3 lần:** câu cụt (「相談？」「二年前……？」「別の書類？」), câu tự cắt lời (「え？ でも、藤宮さんの書類、もうほとんど揃ってて――」), câu treo dấu gạch (「――もういい、計画通りに進めて」).

## Gate máy — đã tự soát trước khi giao

- `check_enum.py`: khối open-loop cold open viết đúng khuôn 4 dòng — câu mở `この夜、私はまだ何も知らなかった。` + 3 mệnh đề `〜のかも、` treo dưới cùng vị ngữ, KHÔNG đếm 一つ二つ三つ, KHÔNG tuyên bố số lượng. Chuỗi số đếm duy nhất trong bài (「七、二、一、四、六、六、二」) là CHỮ SỐ tài khoản trong thoại/hồi tưởng, không phải liệt kê open-loop — không thuộc diện cấm.
- Tag chỉ ở ĐẦU DÒNG, dính liền câu — 0 dòng chỉ có tag, 0 tag lệch vị trí (đã quét bằng regex, xem block Gate ở trên).
- Số trong thân bài toàn bộ 漢数字（七桁・二十二年・四十七歳・七時間半・九時・十五年…）; tiêu đề/thumbnail dùng số Ả Rập theo đúng ngoại lệ.
- Compliance: không tên công ty/người thật (田村印刷・藤宮アセットパートナーズ đều hư cấu; tên ngân hàng chỉ gọi chung 「信用金庫」, không gán tên cụ thể); phản diện thumbnail không mặt người thật; trả thù qua cảnh sát/信用金庫本部/内部告発— chính diện không tự tay phạm pháp (chỉ ghi âm cuộc nói chuyện chính mình có mặt, phát lại công khai để tự vệ); disclaimer フィクション ở 概要欄.

---

## HÀNG XÓM MỤC TIÊU (theo `.claude/rules/youtube-suggested-growth.md` §1)

Video này thiết kế làm "next watch" của 3 video trong `01_SOURCES/SWIPE_TITLES.md` đang thắng đúng cơ chế **bằng chứng ẩn giấu → quyền lực hành động → tổ chức của kẻ ác sụp đổ**, khác hẳn nhánh 嫁姑-gia đình đang bão hoà (11/13 bài gần nhất của kênh dùng sân khấu nghi lễ gia tộc):

1. **「会長、机の下に盗聴器があります！」清掃員がそっと渡した一枚のメモ――それを見た財閥会長は、翌日すぐに動き出した。**（語り茶屋, 153.844 view, 23,4×growth）— cùng cơ chế: bằng chứng ẩn giấu (thiết bị nghe lén/ghi âm) trao cho người có quyền, người đó lập tức hành động.
2. **婚約者の女性にコーヒーを浴びせた姑――翌日、会社は跡形もなく消え去った。**（語り茶屋, 104.282 view, 15,9×growth）— cùng kết cục: tổ chức/công ty của kẻ ác biến mất hoàn toàn ngay sau khi bị lộ, không cần cảnh phán xét dài dòng.
3. **新任副社長が突然私を解雇！夫を見て「あなたの愛人、ずいぶん大胆ね…」その一言で会議室が凍りついた**（孤独な桜の木, 49.751 view, 12,2×growth）— cùng cơ chế: thân phận thật của chính diện lộ ra đột ngột giữa đám đông, khiến kẻ ác đông cứng ngay lập tức.

Lý do video này là next-watch: cả ba video trên dừng ở khoảnh khắc "bằng chứng lộ ra / quyền lực phản ứng", còn video này kéo dài thành một **cuộc rượt đuổi thời gian thực trên xe khách đêm** (điện thoại, SA, ga cuối) — đúng thứ khán giả vừa xem 3 video kia còn muốn biết: "rồi sau đó, kẻ ác bị bắt như thế nào?"

---

## Đóng gói CTR

### KHỐI 1 · 5 TIÊU ĐỀ VIRAL

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | giả thuyết thử |
|---|---|---|---|
| **A1** ⭐ dùng khi đăng | `深夜バスの隣で、二十二年前に消えた口座番号を、あの女は平然と口にした。だが再生ボタンを押した瞬間、彼女の名前は「神崎玲子」に変わった――｜スカッとする話｜修羅場` | 88 | bản mạnh nhất: mở bằng đúng cơ chế cold open (con số + đổi tên) |
| **A2** | `二十二年前、父の葬式代ごと消えた香典。隣で笑うその女が、同じ口座番号を平然と口にしたとき、私は静かに録音を始めた――｜スカッとする話｜修羅場` | 82 | đổi keyword dẫn: bi kịch quá khứ (香典・葬式代) lên đầu thay vì bối cảnh xe khách |
| **A3** | `夜行バスの隣で笑うその女が、まだ知らなかったこと。その口座番号を二十二年間、一度も忘れていない女が、隣に座っていたとは――｜スカッとする話｜修羅場` | 84 | đổi kiểu hook: mystery-tease（「まだ知らなかったこと」）thay vì kể thẳng sự kiện |

### 2 tiêu đề dự phòng (không thuộc bộ A/B chính thức, để tham khảo thêm góc)

- `藤宮玲奈と名乗るその女の正体を、私はもう知っていた。地元に戻る夜行バスの中で――｜スカッとする話｜修羅場`
- `夫が判を捺す九時まで、あと七時間半。隣の女の声を録音した瞬間から、逆転は静かに動き出した――｜スカッとする話｜修羅場`

**Quét compliance:** không có 殺/血/死/レイプ/虐待 hay từ nhóm cấm nào ở cả 5 tiêu đề; không tên công ty/người thật (田村・藤宮・神崎・北原・遠藤 đều hư cấu); mọi tình tiết nêu ra (口座番号・二十二年前・香典・録音・神崎玲子・九時・七時間半) đều có thật trong thân truyện.

### KHỐI 2 · THUMBNAIL — bộ 3 T1/T2/T3

**(a) SPEC CHỮ — T1 (K1 text-wall + dàn người, baseline)**

| dòng | màu | nội dung | ký |
|---|---|---|---|
| 1 | TRẮNG | `深夜バスの隣席` | 7 |
| 2 | TRẮNG | `消えない口座番号` | 8 |
| 3 | CYAN（quote phản diện） | `「もう忘れたわ」` | 8 |
| 4 | VÀNG（twist bất ngờ） | `二十二年前と同じ` | 8 |
| 5 | ĐỎ double-stroke（đòn cuối, TO NHẤT） | `正体は神崎玲子` | 7 |

Lệnh render (đường lui nếu ảnh AI nát chữ):
```
python tools/make_thumb_textwall.py 06_VIDEO/37_nanaketa-no-kioku/thumb_T1_k1.png --lines "深夜バスの隣席" "消えない口座番号" "「もう忘れたわ」" "二十二年前と同じ" "正体は神崎玲子" --colors auto --bg 06_VIDEO/37_nanaketa-no-kioku/scene_k1.jpg --preset k1
```

**T2 (K1 biến thể — đổi 1 biến HÌNH, GIỮ NGUYÊN 5 dòng chữ của T1):** đổi tông nền từ lạnh-xanh (đèn xe khách ban đêm) sang ấm-cam (đèn service area), giữ nguyên bố cục dàn người + vật chứng (điện thoại đang ghi âm).

**T3 (K2 — cảnh sáng kể chuyện, layout 3 dòng kẹp trên-dưới, biến LAYOUT):**

| vị trí | màu | nội dung | ký |
|---|---|---|---|
| trên-1 | TRẮNG | `消えない口座番号` | 8 |
| trên-2 | CYAN | `「もう忘れたわ」` | 8 |
| dưới（to nhất, ĐỎ） | ĐỎ double-stroke | `正体は――神崎玲子` | 9 |

```
python tools/make_thumb_textwall.py 06_VIDEO/37_nanaketa-no-kioku/thumb_T3_k2.png --lines "消えない口座番号" "「もう忘れたわ」" "正体は――神崎玲子" --colors auto --bg 06_VIDEO/37_nanaketa-no-kioku/scene_k2.jpg --preset k2 --mark --mark-style circle
```

**(b) PROMPT GEN ẢNH NỀN — bake cả text, ≥2 nhân vật biểu cảm đang diễn + ≥1 vật chứng**

Xuất 4 file trong `06_VIDEO/37_nanaketa-no-kioku/`:
- `thumb_prompts_FLOW.txt` — mỗi prompt 1 dòng, TEXT block ở đầu (≤15% prompt)
- `thumb_prompts_BLOCKS.md` — bản khối cho người đọc (nội dung y hệt bên dưới)
- `thumb_prompts_TENFILE.txt` — khớp thứ tự dòng FLOW ↔ tên file `thumb_T1/T2/T3_*.png`
- `thumb_prompts_PLATE.txt` — 3 plate KHÔNG chữ (đường lui khi ảnh nát kanji)

Nội dung prompt K1 (T1/T2):

```
Photorealistic dramatic scene, dim interior of a Japanese overnight highway bus at midnight, cinematic low lighting, bold Japanese text burned into the image.

TEXT, exactly these 5 blocks and nothing else:
line 1, white: 深夜バスの隣席
line 2, white: 消えない口座番号
line 3, cyan: 「もう忘れたわ」
line 4, yellow: 二十二年前と同じ
line 5, red with black outline and white halo, LARGEST, roughly twice the height: 正体は神崎玲子

LAYOUT: text block fills the LEFT 65-70% of frame, five lines stacked, line 5 clearly the tallest and boldest.
Two people at CENTER-RIGHT, occupying roughly 33% of frame width, seated side by side on bus seats: a composed Japanese woman in her late forties in plain travel clothes, calm and alert expression, holding a smartphone with a visible audio-recording waveform icon on its screen; beside her, a stylish Japanese woman in her late forties in an expensive blazer, mouth open mid-sentence, startled and pale expression (顔面蒼白) as if just caught.
BACKGROUND: dim bus interior, rows of dark seats fading into shadow, a faint reading light overhead, cold blue-tinted night light through the window, shallow depth of field, no legible text on any background sign.
BOTTOM-LEFT: small red circular badge space reserved, no characters written anywhere near it.
Keep the very bottom-right corner free of text.
Text must be perfectly formed Japanese characters, crisp and legible. No watermark, no logo, no signature, no additional text. --ar 16:9
```

Nội dung prompt K2 (T3):

```
Photorealistic bright storytelling scene, an early-morning Japanese bus terminal, soft daylight, bold Japanese text burned into the image.

TEXT, exactly these 3 blocks and nothing else:
line 1 (top), white: 消えない口座番号
line 2 (top), cyan: 「もう忘れたわ」
line 3 (bottom), red with black outline and white halo, LARGEST: 正体は――神崎玲子

LAYOUT: line 1-2 stacked at the very TOP of frame; line 3 stacked at the very BOTTOM of frame; the CENTER of the frame is fully open for the scene.
CENTER: two people mid-scene, occupying the open middle band: a composed Japanese woman in her late forties holding a smartphone with a visible audio-waveform icon on screen, calm expression; a stylish Japanese woman in her late forties in an expensive blazer standing slightly apart, pale and shocked expression, one hand raised as if caught off guard.
BACKGROUND: bright bus terminal hall, 70-75% overall brightness, warm morning light, blurred rows of seats and a departure board, no legible text anywhere in the background.
Keep the very bottom-right corner free of text.
Text must be perfectly formed Japanese characters, crisp and legible. No watermark, no logo, no signature, no additional text. --ar 16:9
```

Duyệt 3 cấp bắt buộc trước giao: full-size (chữ không đè mặt) → 168px (đọc được dòng chính + biểu cảm) → 120px (đọc được dòng ĐỎ cuối). Huy hiệu kênh `--mark --mark-style circle` góc trên-phải.

---

## SEO — 概要欄 (SEO NHẸ, chỉ chouhen — `.claude/rules/youtube-upload-seo.md` §5)

**Tên file upload**

```
nanaketa-no-kioku-shinya-bus.mp4
```

### 概要欄 — SEO NHẸ (~300 ký, KHÔNG 目次)

```
深夜バスの隣で、あの女が平然と口にした七桁の口座番号。
それは、二十二年前に消えた香典と、まったく同じ数字だった――そこから始まる、静かな逆転劇。
録音・内部告発・銀行の凍結、地元に戻るまでの一夜の物語です。

※この物語はフィクションです。実在の人物・団体とは一切関係ありません。
AivisSpeech: morioki

#スカッとする話 #修羅場 #朗読
```

(Tag: 0 — SEO nhẹ chouhen, peer 44K–205K view đều 0 tag, `youtube-upload-seo.md` §5)

---

=== KỊCH BẢN HOÀN CHỈNH ===

「――口座番号はそのままでいい。二十二年前と、一桁も変えていないんだから」

聞いた瞬間、指が録音ボタンへ伸びた。

深夜零時を過ぎた、夜行バスの中だった。

七、二、一、四、六、六、二。

見覚えのある数字だった。

私は、まだ何も言わなかった。

膝の上で、拳だけを、静かに握った。

窓の外は、まだ真っ暗だった。

この夜、私はまだ何も知らなかった。
あと九時間足らずで、夫が何に判を捺そうとしているのかも、
二十二年前、父の葬式代ごと消えた香典が、どこへ流れ着いていたのかも、
そして、この一本の録音が、何人の運命を変えることになるのかも。

そっと、指先だけを動かした。

「浩一さん――待って。まだ判を押さないで」

数字だけは、どうしても忘れられない。

昔、占い師に見てもらったとき、それは才能ではなく呪いですね、と真顔で言われたことがある。

当たっているのかもしれない、と今なら思う。

バスが最初のサービスエリアに滑り込んだのは、午前一時を過ぎた頃だった。

乗客たちが次々と外へ降りていく中、私も彼女――藤宮玲奈と名乗るその女の後ろに続いた。

自動販売機の前で、彼女は缶コーヒーのボタンを押した。

「二十年ぶりに飲むわ、こんなもの」

ひと口飲んで、顔をしかめた。

「まずい。田舎の機械は変わらないのね」

彼女は誰にともなく、小さく呟いた。

「次の街では、もう少しマシな客を探さないと」

私はつい、隣の販売機で同じ缶コーヒーを買っていた。

一口飲むと、確かにひどい味がした。

けれど、なぜか、手が止まらなかった。

田舎の夜行バスの休憩所には、決まってこの苦い匂いが漂っている。

若い頃、始発列車を待ちながら飲んだ味と、少しも変わっていなかった。

彼女がふと、こちらを見た。

「さっきから、何を見ているの」

「いえ、別に」

「貧乏くさい顔ね」

彼女はそう言うと、缶を片手にブランドもののショルダーバッグをかけ直した。

田舎の売店には不釣り合いなほど、艶やかな革だった。

答えられずにいると、背後で誰かが小さく息を呑んだ。

振り返ると、初老の男性が、深々と――九十度近くまで腰を折っていた。

「田村さん……! これは、大変ご無礼をいたしました」

藤宮玲奈の表情が、初めて揺れた。

「田村……さん？」

私は曖昧に笑い、頭を下げ返すことしかできなかった。

「昔、少しお世話になっただけです」

男性――北原修一は、私がかつて十五年勤めた信用金庫の、今の支店長だった。

出張で偶然、同じバスに乗り合わせていたのだという。

「窓口の田村さんに教わった通りに、今もやっているんです」

北原さんは懐かしそうに、そう続けた。

藤宮玲奈が、探るような目でこちらを見ていた。

「何かのお仕事をされていたんですか」

「もうずいぶん昔のことです」

私は言葉を濁した。

北原さんは名刺を差し出しながら、小さな声で付け加えた。

「何かあれば、いつでもお電話を」

藤宮玲奈は、まだ何か言いたそうに私を見ていたが、やがて興味を失ったように缶を放り、バスへ戻っていった。

私は名刺をポケットに滑り込ませ、一番後ろの席に座り直すと、電話をかけた。

「遠藤さん。夜分にごめんなさい」

「田村さん？ どうしたの、こんな時間に」

「二十二年前の、あの件――覚えてる？」

電話の向こうで、遠藤さんの声が固くなった。

「まさか、また……」

「多分、そう。さっき、隣の席で同じ口座番号を聞いたの」

「同じ声で？」

「ええ。今は藤宮玲奈と名乗ってる」

遠藤さんは、しばらく黙っていた。

私も、あの日のことを思い出していた。

父の葬儀の朝、香典帳を任されていたのは、当時仲の良かった同級生――神崎玲子だった。

葬式代の足しにと、町内会が集めてくれたお金ごと、彼女は姿を消した。

告別式の翌日、香典帳だけが玄関先に放り出されていた。

数字の欄は、几帳面な字で最後まで埋まっていたのに、肝心のお金は一円も残っていなかった。

母は何も言わずに、古い着物を質に入れて、その穴を埋めた。

高校を出たばかりの私に、それ以上できることは何もなかった。

ただ、あの日から、数字だけは一度も忘れないようになった。

「田村さん。今すぐは言えない。三十分だけ、時間をちょうだい」

通話が切れた。

バスは静かに、また高速道路へ戻っていった。

夫が判を捺すまで、あと七時間半しかなかった。

ご感想やご要望はぜひコメントで、そして楽しんでいただけていましたら高評価とシェアで、真夜中の朗読便を応援していただけると嬉しいです。――続きです。

三十分は、体感で三時間ほどに長く感じられた。

隣の藤宮玲奈は、何度もスマートフォンを操作しては、舌打ちを繰り返していた。

既読がつかないのだろう。

やがて彼女は舌打ちをやめ、声を潜めて電話をかけ始めた。

「――念のため、社長の奥さんから電話が入っても、絶対に取り次がないで」

見ず知らずの他人のはずなのに、その用意周到さに、背筋が冷えた。

バスが長いトンネルに入り、電波が切れた。

暗闇の中で、エンジン音だけが唸っていた。

トンネルを抜けた瞬間、私のスマートフォンが震えた。

遠藤さんからだった。

「田村さん、聞いて」

その声は、さっきより硬かった。

「藤宮アセットパートナーズの担当をしていた子――今日の午前中に、警察に相談に行ってた」

「相談？」

「横領されそうになった、って。自分の給料も、三か月分未払いのままだって」

喉の奥が、きゅっと締まった。

「その子、何て？」

「田村印刷という会社に、今日中に融資を実行させたい。上から強く言われてたって」

「おかしいと思って、給与明細も、指示のメモも、全部残していたそうよ」

「二十代の子が、よくそこまで」

「怖かったんだと思う。でも、それ以上に、悔しかったんだって」

その一言が、二十二年前の母の顔と重なった。

「その子の証言と、田村さんが今言った口座番号――一致したら、これは立件できる」

数字をもう一度、ゆっくりと口にした。

「七、二、一、四、六、六、二」

遠藤さんが、小さく息を呑んだ。

「――一致した」

電話の向こうで、キーボードを叩く音がした。

「二十二年前の記録と、今の口座、送金先の名義まで同じ」

「よく残ってたね、そんな昔の記録」

「田村さんが忘れなかったから、こっちも捨てられなかったのよ」

安堵より先に、指先が震えた。

「でも、田村さん。もう一つ、厄介なことがある」

「何？」

「その会社、融資の実行が今朝の九時。もう止められないところまで来てる」

「あと五時間もない」

「うん。だから、田村さんが今できることをやって。私はこっちで動く」

バスの窓の外が、わずかに白みはじめていた。

夫が起きる時刻まで、もういくらも残っていなかった。

藤宮玲奈が、こちらをじっと見ていることに気づいた。

「さっきから、電話ばかりね」

「ただの世間話です」

「へえ」

彼女は疑わしげに目を細めた。

「まさか、録音でもしてるんじゃないでしょうね」

とっさに、頬が強張った。

藤宮玲奈は、声を張り上げた。

「運転手さん！ この人、さっきからずっと私を撮ってるんです！」

バスの中が、ざわついた。

前方の座席から、何人かが振り返った。

運転手が、ゆっくりとバスを路肩に寄せた。

「お客様、何かございましたか」

藤宮玲奈は勝ち誇ったように、私を指さした。

「この人が、勝手に私を撮影してるんです。降ろしてください」

私は静かに、スマートフォンを取り出した。

「撮ってはいません。ただ――」

再生ボタンを押した。

「――口座番号はそのままでいい。二十二年前と、一桁も変えていないんだから」

自分の声を借りて、彼女自身の声が、暗いバスの中に響いた。

藤宮玲奈の顔から、血の気が引いていくのが見えた。

前の座席の女性が、小さく声を上げた。

「藤宮……？ もしかして、去年うちの町内会に来てた、あの投資セミナーの人？」

隣に座っていた男性も、思い出したように顔を上げた。

「うちの母も、その人の説明会に呼ばれてたな。危うく判を押すところだったって、あとで笑ってたけど」

「その節は、母がご迷惑をおかけして」

「いや、迷惑をかけてたのは、あんたの方だろう」

このままでは、ただの痴話喧嘩として忘れられてしまう。

私は、これまで誰にも話したことのないことを、静かに口にした。

「二十二年前、父の葬式の朝、この人は香典を持って消えました。母は、着物を質に入れて、その穴を埋めました」

車内が、しんと静まり返った。

これを声に出すのは、二十二年ぶりだった。

母の丸まった背中を思い出すたびに感じていた、あの惨めさが、喉の奥に蘇った。

車内のあちこちで、小さくスマートフォンが構えられるのが見えた。

藤宮玲奈は答えなかった。

ただ、唇だけが小さく震えていた。

運転手は困ったように、「発車します」とだけ告げて、再びバスを出した。

車内は、しばらくの間、誰も口をきかなかった。

彼女は震える指でスマートフォンを操作し、最後方へ逃げるように移動した。

小さな声が漏れ聞こえた。

「――もういい、計画通りに進めて。私はここで降りるから」

その一言に、新しい違和感を覚えた。

藤宮玲奈は、一人で動いているのではなかった。

震える手で、夫に電話をかけた。

浩一はすぐに出た。

「もしもし？ 芙美子、今、支店のロビーにいるんだけど」

「浩一さん、判、絶対に押さないで」

「え？ でも、藤宮さんの書類、もうほとんど揃ってて――」

「お願い。少しだけ待って」

浩一の声は、困惑していた。

「藤宮さんは、うちの会社を助けてくれるって……あの人、いい人だと思ってたんだけどな」

「悪い人ほど、最初はそう見えるものよ」

「わかった。九時までは、何も押さない」

「浩一さんは悪くない。ただ、少しだけ時間が欲しいの」

電話を切り、北原さんからもらった名刺を取り出した。

震える指で、番号を押した。

「北原です」

「田村です。突然すみません」

「田村さん、どうされましたか」

私は、遠藤さんから聞いたことを、できるだけ簡潔に伝えた。

会社名。二十二年前と同じ口座番号。そして、名乗り出た元担当者の証言。

北原さんは、しばらく黙って聞いていた。

「――少し、お待ちください」

キーボードを叩く音が、電話越しに響いた。

「田村さん、実は――藤宮アセットパートナーズという名前、うちのシステムに、二年前の別件で記録が残っていました。今のお話と、符合します」

心のどこかで、力が抜けた。

「二年前……？」

「融資の連帯保証をめぐる、別の問題です。今朝の実行は、念のため保留にさせてもらいました」

安堵より先に、めまいのようなものが来た。

だが、北原さんは付け加えた。

「ただ、藤宮さんという方が今朝、別の書類を持ってご主人のところへ向かっている、という情報もあります」

「別の書類？」

「個人名義の、小口の契約書のようです。融資ではなく、業務委託という形の」

背筋が、すっと冷たくなった。

時計の針は、もう七時を回っていた。

形を変えて、まだ罠は仕掛けられたままだった。

北原さんが、静かに言った。

「田村さん。あとは、私たちの仕事です。ご主人には、私から連絡を入れておきます」

その一言だけで、十分だった。

十五年間、窓口に立ち続けた日々は、無駄ではなかったのだと、初めて思えた。

窓の外に、夜明け前の薄青い空が広がっていた。

バスが減速し、終点のターミナルへと滑り込んでいった。

窓の外には、夜が白く溶けはじめた空が広がっていた。

私が降りるより先に、藤宮玲奈がバッグを抱えて、足早に出口へ向かった。

早朝のターミナルは、通勤客でざわめきはじめていた。

改札へ向かう人波の中に、彼女の後ろ姿が紛れていく。

追いつけないかもしれない、と思った瞬間、人波の先で、彼女の足が止まった。

ターミナルの明かりの下に、制服姿の男性が二人、立っていた。

藤宮玲奈が、足を止めた。

まわりの通勤客たちが、何ごとかと歩みを緩めた。

しばらく、誰も動かなかった。

私は少し離れた場所で、足を止めた。

心臓の音だけが、やけにはっきりと聞こえた。

彼女が逃げようとして半歩下がるのが見えたが、もう一人の警官が、ちょうどその背後に回り込んでいた。

「藤宮玲奈さん、で間違いありませんか」

彼女は、笑おうとして失敗したような顔をした。

「人違いです。急いでいるので」

その声は、いつもの余裕とはほど遠く、かすれていた。

彼女は、こちらを睨みつけた。

「――田舎者のくせに、余計なことばかりして」

その声にはまだ、二十二年前と同じ、人を見下す響きが残っていた。

一人の警官が、静かに手帳を開いた。

「神崎玲子さん、ですね」

その名前を呼ばれた瞬間、彼女の全身から力が抜けていくのが、遠目にもわかった。

ゆっくりと歩み寄り、警官の一人に、もう一度だけ数字を口にした。

「七、二、一、四、六、六、二。二十二年前、町内会の香典が消えた口座番号と、同じです」

神崎玲子――藤宮玲奈は、その場に崩れるように膝をついた。

朝の人波の中で、額を地面にこすりつけた。

「お願い……許して。もう、後がないの」

その声には、二十二年前と同じ、震えがあった。

私は静かに、彼女を見下ろした。

「二十二年前の香典も、今朝の保証金も、他人の名前を盗んだことも――私は、一つも忘れていません」

「許して、お願い……」

「許しません」

「けれど、あなたを地獄に突き落とすことにも、興味はない。警察には、すべて正直に話してください。それだけです」

彼女は、それ以上何も言えなかった。

連れて行かれる直前、彼女は一度だけ振り返った。

その目に浮かんでいたのが、憎しみだったのか、それとも――安堵だったのか、私には分からなかった。

制服姿の男性たちに支えられるようにして、その場を離れていった。

数週間後、遠藤さんから連絡があった。

神崎玲子は、詐欺未遂と業務上横領の容疑で送検された。

藤宮アセットパートナーズという会社は、登記簿の上からも消えた。

彼女が声をかけていた高齢者は、私たちの町だけで、少なくとも七人いたという。

被害の大半は、実行される前に止まった。

町内会のLINEグループには、彼女の本当の名前が、静かに、けれど確かに広まっていった。

あの、勇気を出して声を上げてくれた若い担当者にも、遠藤さんを通じて、お礼の手紙を送った。

返事の最後に、小さくこう書かれていた。

「怖かったけど、言ってよかったです」

それから一年が過ぎた。

田村印刷は今、地元の学校の卒業アルバムを中心に、堅実に仕事を続けている。

浩一は、あの朝以来、契約書には必ず私の目を通すようになった。

「芙美子がいなかったら、うちの会社はなかった」

そう言って、少し照れくさそうに笑うようになった。

私は月に一度、公民館で、近所の人たち相手に小さな講座を開いている。

「怪しい数字の見分け方」という、地味な講座だ。

生徒は毎回、十人にも満たない。

それでも、誰かの家計簿を、静かに救えている気がしている。

机の上には、父が商店会の帳簿をつけるときに使っていた、古い電卓を置いている。

もう電池は入っていないけれど、指がその上を滑るたびに、なぜか安心する。

数字だけは、どうしても忘れられない。

それは呪いではなく、今ではきっと、父からの贈り物だったのだと思う。

私の人生は、四十七歳を過ぎてから、本当の意味で始まったのだった。

最後までお聴きいただき、ありがとうございました。耐えた人が、最後に必ず報われる。真夜中の朗読便は、そんな物語を今夜もお届けします。どうか、安らかな夜をお過ごしください。
