# 01 — 人の目を気にしすぎる人の口癖7つと言いかえ方（kinishinai 他人の目を気にしない心理学）

> Viết 2026-09-30. Kênh **chưa có `05_SCRIPT_FORMULA.md`** → tạm mượn khuôn liệt kê 語りかけ型 của yawa (`youtube-jp-yawa/05_SCRIPT_FORMULA.md` §2–3, biến thể mở bằng nỗi sợ §2.2), **đổi lăng kính: nghiên cứu tâm lý có tên + nguồn, 0 câu 古典** (ranh giới yawa). Trạng thái: **v2 (2026-10-01) — viết lại theo yêu cầu "giữ chân · có hồn · không rời rạc", chờ user duyệt**. Bản v1: `_v1/`.
> Bản đọc: `01_kuchiguse-hitonome_TTS.md` · một giọng, người kể vô danh nói với あなた · **5.551 ký ≈ 19,5′** (ước 285 ký/phút — chưa có giọng chốt, đo lại trên wav) · 7 mục · mục 1 vào ≈ **1:57** · 25 dòng có tag.

## 0. ĐỀ + ĐO

### 0.1 Quét YouTube 30 ngày (`youtube-jp-health/tools/scan_niche_now.py`, 12 làn đề của kênh, 148 video, 2026-09-30)
Dữ liệu: `01_SOURCES/_scan_2026-09-30/scan_out.{txt,json}`.

| làn | median view/ngày | video mạnh nhất |
|---|---|---|
| **口癖** | 75 (14 kênh) | ⭐ 「【漫画】周りから愛される60代は必ず言っている魔法の口癖7選」 **2.023.797 view / 14 ngày** (141K/ngày) · ユウリ 「60代でこの口癖を言う人は本当に性格がいい人」 99K / 10 ngày · **đã có 4 kênh clone** cùng title trong 10 ngày |
| 一人 (一人が好き) | 112 | 193K · 179K — nhưng kênh tâm lý trẻ, không phải 60+ |
| 人の目 / 他人の目 | 64 / 54 | trần 947/ngày (中村天風) — **đề lõi của kênh đứng riêng thì yếu** |
| 嫌われる勇気 · 期待しない · HSP | 10 · 12 · 3 | ❌ gần như không có video 60+ ăn view |

⇒ Chủ đề đang được quan tâm nhất = **口癖**. Đề này **ghép 口癖 (vỏ đang nổ) với 人の目 (lõi kênh)**: không chép "口癖 tốt của người được yêu" mà lật vào trong — *口癖 tiết lộ mình đang sợ ánh mắt người khác* + cách nói lại.

### 0.2 Bảng đo keyword (Google Trends gprop=youtube, JP, 30 ngày, pytrends 2026-09-30, quy về thang `NICHE_RESEARCH` với 嫌われる勇気 = 27,2)
| từ | điểm | kết luận |
|---|---|---|
| いい人 | ~180 | ❌ quá rộng, intent lẫn (drama/bài hát) — chỉ tag |
| **人の目** | **~64** | ✅ lõi kênh, đầu title A1. ⚠️ related trả rỗng → chưa loại được nhiễu bài hát/drama; đối chiếu web 12 tháng trước khi đăng |
| 気にしない | ~38 | tag + mô tả |
| **口癖** | **~20** (khớp số sáng nay 20,1 ↑) | ✅ keyword đề, A2 dẫn bằng nó. ⚠️ top là VTuber/anime → luôn ghép 60代 / 人の目 |
| 自分らしく | ~17 | hashtag |
| 群れない · 期待しない · 比べない | 6,6 · 3,7 · 2,5 | tag |
| 人の目が気になる · 他人の目 · 気にしすぎ · 八方美人 | ≤1,6 | ❌ gõ nguyên cụm ≈0 |
Dữ liệu: `01_SOURCES/_scan_2026-09-30/trends_2026-09-30.json`. Lần gọi related của いい人 bị 429.

### 0.3 HÀNG XÓM MỤC TIÊU (`youtube-suggested-growth.md` §1)
| video | kênh | view | tuổi | vì sao mình là next-watch |
|---|---|---|---|---|
| [【漫画】周りから愛される60代は必ず言っている魔法の口癖7選](https://www.youtube.com/watch?v=J2WiiKe2VY4) | 人間のトリビア | 2.023.797 | 14 ngày | họ nói "口癖 TỐT nên nói" → mình nói "口癖 mình LỠ nói và vì sao" — mặt còn lại của cùng câu hỏi |
| [60代でこの口癖を言う人は本当に性格がいい人｜年を重ねて育つ7つの言葉【心理学】](https://www.youtube.com/watch?v=WATghdSAZ4g) | ユウリの優しい心理学 | 99.438 | 10 ngày | cùng khuôn 【心理学】 60代 口癖 7; mình thêm tên nghiên cứu + số đo thật |
| [【心理学】他人の顔色を気にしすぎる人へ｜「嫌われたくない」が消えていく心理学](https://www.youtube.com/watch?v=o7StvTSHRbo) | ココロの魔法 | 9.655 | 28 ngày | cùng lõi 人の目 |
⚠️ Chưa mở cột suggested bằng `Profile 3` — làm trước khi đăng.

## 0.4 ĐÁNH GIÁ v1 → VÌ SAO VIẾT LẠI (2026-10-01)
**Người xem đến vì gì:** thumbnail/title hứa một **phép tự soi** — 「mình có phải người để ý ánh mắt quá không, và câu nào của mình lộ ra điều đó?」 (vỏ 口癖 đang nổ + lõi 人の目). **Ở lại vì gì:** ① đếm xem mình dính mấy câu ② câu hỏi treo chưa trả lời ③ một người để theo tới cuối.

| | v1 | chấm | v2 sửa |
|---|---|---|---|
| câu 1 | 「すみません」 — ai cũng nói, không có cược | 5 | **câu của đứa con nói sau lưng** 「一緒にいると、ちょっと、疲れるんだよね」 = nỗi sợ thật của tệp (thành gánh nặng cảm xúc cho con) |
| gỡ tội | 「やさしい人だから」 — đúng khuôn, không bất ngờ | 6 | **đảo nghĩa**: không phải THIẾU 気づかい mà **mũi tên 気づかい chĩa sai hướng** → luận đề cả bài |
| vòng mở | "mục 7 bị giấu" + "chuyện ngồi こたつ" — là ĐẾM, không phải CÂU HỎI | 5 | **câu hỏi:** 「娘さんのたった一言」 là gì? + 「その一言が、今日のいちばんの答え」 → trả ở 16:xx |
| mạch | 7 nghiên cứu rời, người quen chỉ ghé qua → **nghe như bài giảng liệt kê** | 4 | ① một khái niệm xuyên bài: **「見積もりちがい」** (4/7 nghiên cứu đo đúng chuyện "mình tưởng bị đánh giá tệ hơn thật") ② 7 mục xếp **từ miệng → đáy lòng** (một đối một → nhóm → giọng trong đầu → câu không nói ra), mỗi mục kết bằng **câu cầu sang mục sau** ③ người quen đi **trọn một năm** (xuân → hè → thu → 10 → 11 → 12 → Tết), bỏ được 6 câu nhưng **câu 7 thì không** → tạo căng thẳng thật trước khối chốt |
| cơ chế giữ chân | không có | 3 | **gập ngón tay** mỗi mục (「当てはまったら、指を一本」) + kết hỏi 「指は何本？」 = comment dễ trả lời |
| chuyện chốt | bà tự ngồi xuống, con gái nói SAU → câu nói không làm gì cả | 6 | **câu của con gái là cái KHIẾN bà ngồi xuống** (kéo dây tạp dề) → cười (cháu) → đỉnh → **kết trả thẳng câu 1**: 「それは、嫌われているからではありません。あなたに、座ってほしいだけなんです」 |
| **tổng (phán đoán)** | **~5,5/10** | | **~8,5/10** — trần còn lại xem §6 |
⚠️ Điểm là phán đoán của người viết, không phải retention. Chỉ số thật = đường cong 0–60s sau khi đăng.

## 1. NGUỒN TÂM LÝ HỌC (kiểm 2026-09-30 — kênh cam kết 「出典を確かめたものを使います」)
> v2 đổi thứ tự mục: 1 すみません · 2 つまらない話で · 3 どう思われるかしら · 4 恥ずかしい · 5 みんなそうしてるから · 6 いい年して · 7 私さえ我慢すれば. Cột "mục" dưới đây giữ nhãn v1.

| mục | nghiên cứu | câu trong bài | nguồn |
|---|---|---|---|
| 1 すみません→ありがとう | Kumar & Epley (2018) *Undervaluing Gratitude*, Psychological Science 29(9) | người viết thư cảm ơn đánh giá THẤP độ vui của người nhận, đánh giá CAO sự ngượng | https://doi.org/10.1177/0956797618772506 |
| 2 どう思われるかしら | Gilovich, Medvec & Savitsky (2000) *The Spotlight Effect*, JPSP 78(2):211–222 (Cornell) | số người thật sự để ý áo = **đúng một nửa** số người mặc đoán | bản gốc PDF: "The average estimate made by the targets was exactly twice as high as the average accuracy rate of the observers" (Study 1) |
| 3 みんなそうしてるから | Asch (1951, 1956) thí nghiệm độ dài đoạn thẳng | một mình gần như không ai sai · có nhóm cố ý sai → **~3/4 theo nhóm ít nhất 1 lần** · có 1 người bất đồng → theo nhóm giảm mạnh (không nêu số) | https://www.simplypsychology.org/asch-conformity.html |
| 4 いい年して | Carstensen — Socioemotional Selectivity Theory (Stanford) | thời gian còn lại ngắn lại → chọn quan hệ/việc có ý nghĩa cảm xúc | https://en.wikipedia.org/wiki/Socioemotional_selectivity_theory |
| 5 恥ずかしい | Bruk, Scholl & Bless (2018) *Beautiful Mess Effect*, JPSP 115(2):192–205 (Mannheim) | mình thấy lộ yếu đuối là "bừa bộn", người khác thấy là can đảm/đáng mến; 7 nghiên cứu | https://www.researchgate.net/publication/326743464 |
| 6 つまらない話で | Boothby, Cooney, Sandstrom & Clark (2018) *The Liking Gap*, Psychological Science 29:1742–1756 | sau khi nói chuyện, người ta đánh giá thấp mức đối phương thích mình | https://pubmed.ncbi.nlm.nih.gov/30183512/ |
| 7 私さえ我慢すれば | アドラー心理学「課題の分離」 (theo 岸見一郎・古賀史健『嫌われる勇気』2013) | người khác nghĩ gì = việc của họ; mình sống ra sao = việc của mình | chỉ ở thân bài, ⛔ không lên title/thumbnail |
- ⚖️ Bài 1 nói Boothby "アメリカの" (Cornell/Yale) ✅ · Bruk "ドイツのマンハイム大学" ✅ · "ブースビーたち" dùng cho nhóm tác giả.
- ⚖️ Không suy rộng: không nói "khoa học chứng minh ありがとう tốt hơn すみません" — chỉ nói điều nghiên cứu đo.
- 「美しい散らかり効果」「好かれ度のギャップ」 là **cách mình dịch** tên hiệu ứng, không phải thuật ngữ JP chính thức (bản JP phổ biến: 「ビューティフル・メス効果」「ライキング・ギャップ」) — cố ý né 外来語 cho tệp 60+.

## 2. NGƯỜI QUEN + SỔ CHỐNG KHUÔN
- **Người quen (hư cấu):** nữ **68 tuổi**, **đứng quầy 呉服 ở デパート 34 năm** · chi tiết vô dụng: **vẫn gấp giấy gói quà theo nếp cũ, cất trong ngăn kéo** · 口癖 「すみません」.
- Xuất hiện (v2 — **một năm liền mạch**): mục 1 xuân (ありがとう với học sinh, mua あんパン) · 2 hè (điện thoại 「私も。早く言ってよ」) · 3 đầu thu (cardigan đỏ) · 4 tháng 10 (gọi em gái) · 5 tháng 11 (không giơ tay ở buổi họp tổ, bà hàng xóm thì thầm 「私もね、ほんとは、反対だったのよ」) · 6 tháng 12 (du lịch một mình, 2 hộp 駅弁) · 7 **không làm được** → chuyện chốt → **7/7 mục**.
- **Chuyện chốt (v2):** 40 cái Tết đứng trong bếp → năm nay định lại ra bồn rửa thì **con gái kéo dây tạp dề** + câu 「お母さんが台所に立ってるとね、私たち、座ってていいのか、ずっと、気をつかってたのよ」 → bà đứng sững → ngồi vào こたつ → **cười**: cháu 「おばあちゃんって、座れるんだ」 → **ĐỈNH**: 「四十回のお正月、ずっと、立ってたのね、私。……座っても、よかったのね」 → **kết trả câu 1**: câu 「一緒にいると、疲れる」 không có nghĩa là bị ghét — 「あなたに、座ってほしいだけなんです」.
- **So với yawa (đề/người quen không trùng):** yawa 01 nữ 信用金庫 goá chồng · yawa 02 nam tài xế buýt 「そのうち、な」. ⚠️ yawa 02 title có 「口ぐせ」 — khác góc (後悔), không có 「そのうち」 trong 7 mục của bài này.

## 3. MŨI TIÊM CHẤT NGƯỜI (≥4/6)
| # | có? | ở đâu |
|---|---|---|
| ① | ✅ | người kể tự thú một lần (mục 2: 「実は、私も、そうです。新しい眼鏡にした日は…」) + 証人 người quen xuyên bài |
| ② | ✅ | thoại người quen ở 6 mục; chi tiết vô dụng: gấp giấy gói quà · 2 hộp 駅弁 · ăn 3 quả quýt |
| ③ | ✅ | tiếng trong phòng lúc cả nhà im 「しん」 · こたつ · お雑煮 · giấy gói theo nếp |
| ④ | ✅ | người quen làm thử từng 「言いかえ」 và kể kết quả |
| ⑤ | ✅ | chuyện chốt đóng bằng 「お正月って、こんなに、あったかかったのね」 |
| ⑥ | ✅ | 「お昼は、そばがいい。今日は、散歩をやめておく。」 · 「みんな、大笑いです。」 · 「泣くのよ、向こうが」 |

## 4. GATE (v2, chạy 2026-10-01, ước 285 ký/phút)
| gate | kết quả |
|---|---|
| câu 1 = câu nói của người thân · 0 tên/tuổi trong đoạn mở | ✅ |
| 心当たり ≤0:45 | ✅ 0:27 |
| gỡ tội ≤0:55 | ✅ 0:31 (+ đảo nghĩa 0:38) |
| vòng mở là CÂU HỎI, trả ở cuối | ✅ 「娘さんのたった一言」 hứa 1:11 → trả ~16:40 |
| đoạn mở ≤90s | ✅ câu mời 1:26 |
| mục 1 ≤2:00 | ✅ 1:57 (sát trần — đo lại trên wav, trượt thì cắt 2 câu khái niệm 「見積もりちがい」) |
| mỗi mục: cảnh · sợ · gỡ tội · nghiên cứu · câu nói lại · người quen làm thử · ngón tay · cầu sang mục sau | ✅ 7/7 (mục 7 cố ý không có "làm thử" → dồn vào chuyện chốt) |
| tag 15–25 · gate ① · gate ② | ✅ 25 · 0 · 0 |
| 「〜そうです」 liên tiếp | ✅ tối đa 1 |
| 0 sức khoẻ/bệnh/thuốc/tiền | ✅ quét 死/殺/血/病/薬/健康/年金/円 = 0 |
| 外来語 60s đầu | ✅ không có |
| CTA giữa bài | ⏳ chưa chèn — kênh chưa có câu canonical |

## 5. ĐÓNG GÓI CTR

### Title CHỐT
```
【心理学】人の目を気にしすぎる人の口癖7つと言いかえ方
```

### 3 TITLE A/B — mỗi bản một giả thuyết (`ab-3title-3thumb.md` §2)

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【心理学】人の目を気にしすぎる人の口癖7つと言いかえ方` | 27 | 人の目@5 · 口癖@17 | keyword lõi kênh (人の目 ~64) dẫn |
| **A2** | `60代で「この口癖」が出る人は、人の目を気にしすぎです【心理学】` | 32 | 口癖@7 | đổi keyword dẫn sang 口癖 + khuôn title đang nổ 「60代でこの口癖…」 |
| **A3** | `【心理学】「私さえ我慢すれば」が口癖の人へ｜7つの言いかえ` | 29 | 口癖@16 | đổi kiểu hook: trích câu (mục giấu) |

### Tên file upload
```
hitonome-kuchiguse-7tsu-iikae.mp4
```

### 3 dòng đầu 概要欄 (vùng hiển thị — cấm lời chào)
```
「すみません」「どう思われるかしら」――人の目を気にしすぎる人ほど、つい口にしてしまう口癖があります。
60代・70代の方へ、心理学の研究からわかった7つの口癖と、心がふっと軽くなる言いかえ方をお話しします。
最後に、四十回のお正月、一度もこたつに座らなかった女性が、娘さんの一言ではじめて座った日の話を。
```

### 概要欄 — 本文（目次は render 後に subs.srt から確定 — ⏳）
```
「すみません」「どう思われるかしら」――人の目を気にしすぎる人ほど、つい口にしてしまう口癖があります。
60代・70代の方へ、心理学の研究からわかった7つの口癖と、心がふっと軽くなる言いかえ方をお話しします。
最後に、四十回のお正月、一度もこたつに座らなかった女性が、娘さんの一言ではじめて座った日の話を。

目次
=====
⏳ render 後に確定

この動画でご紹介する口癖
・「すみません」→「ありがとう」（感謝の伝え方の研究）
・「つまらない話で、ごめんなさいね」（会話のあとの好感度の研究）
・「どう思われるかしら」（スポットライト効果）
・「こんなこと言ったら恥ずかしい」（弱さを見せることの研究）
・「みんなそうしてるから」（同調の実験）
・「いい年して」（年齢と心の選び方の理論）
・「私さえ我慢すれば」（アドラー心理学「課題の分離」）

気にしない生き方は、性格を変えることではなく、言葉を少しだけ言いかえることから始められます。
他人の目、自己肯定感、人間関係に疲れたと感じる方にも。

■参考文献
Kumar & Epley (2018) Psychological Science
Gilovich, Medvec & Savitsky (2000) Journal of Personality and Social Psychology
Asch (1951, 1956)
Carstensen, Socioemotional Selectivity Theory
Bruk, Scholl & Bless (2018) Journal of Personality and Social Psychology
Boothby, Cooney, Sandstrom & Clark (2018) Psychological Science
岸見一郎・古賀史健『嫌われる勇気』（ダイヤモンド社, 2013）

※本動画に登場する人物・エピソードは、心理学の知見をわかりやすく伝えるための創作です。
※心理学の一般的な知見を紹介するもので、医療・カウンセリングの代わりになるものではありません。

音声：⏳（TTS 未定 — VOICEVOX なら「VOICEVOX:キャラ名」）
音楽：⏳

#心理学 #人の目 #口癖 #他人の目を気にしない心理学 #60代
```
⚠️ Credit + 目次 rà lại sau render (`youtube-upload-seo.md` §5, §5.1).

### タグ
```
他人の目を気にしない心理学,心理学,人の目,人の目が気になる,他人の目,気にしない,口癖,口癖でわかる性格,60代 口癖,言いかえ,すみません,ありがとう,自己肯定感,嫌われる勇気,アドラー心理学,課題の分離,スポットライト効果,同調圧力,我慢,いい人,自分らしく,人間関係,人間関係に疲れた,60代,70代,シニア,人生後半,心が軽くなる
```
(28 tag.)

### ハッシュタグ（volume 順）
```
#心理学 #人の目 #口癖
```

### Pinned comment
```
最後まで聞いてくださって、ありがとうございます。
つい「すみません」と言ってしまうのは、あなたの気が弱いからではなく、周りを大切にしてきた人だから。今日は、それだけでも持ち帰っていただけたら嬉しいです。

あなたの指は、何本折れましたか？
「三本でした」でも、「七本、全部」でも。
よろしければ、そっと教えてください。
```

### Thumbnail — ⏳ chưa làm (gói 3×3 chưa đủ)
Kênh chưa có khuôn thumbnail. Hướng đề xuất (chờ user chốt khuôn): chữ tải chủ đề = `人の目` + `口癖` + hero 「すみません」 gạch → 「ありがとう」; T1/T2/T3 theo `ab-3title-3thumb.md` §3.

### Quét compliance (`youtube-compliance.md`) — báo trước khi giao
- Title ×3 / 3 dòng đầu / hashtag: **0 từ nhóm §3**. ✅
- Tên sách 『嫌われる勇気』 chỉ ở 参考文献 + tag; **không** ở title/thumbnail ✅ (CLAUDE.md kênh). Tag `嫌われる勇気` là tên sách — giữ vì đúng nội dung (mục 7), user muốn bỏ thì bỏ.
- Tên người thật: chỉ tên nhà nghiên cứu (trích nguồn) ✅. デパート không nêu tên hãng ✅.
- Hư cấu có câu 創作 ✅ · câu "không thay tư vấn/điều trị" ✅ (HSP/tâm thần không đụng).
- Mọi tình tiết trên title/3 dòng đầu có trong video: 7 口癖 + 言いかえ ✅ · 「私さえ我慢すれば」 (A3) = mục 7 ✅ · 「四十回のお正月」「娘さんの一言」「こたつ」 = chuyện chốt ✅.
- Ảnh AI realistic trong video (nếu dùng) → **tick altered/synthetic** khi upload.

## 6. VIỆC CÒN LẠI / CẦN USER CHỐT
1. **User duyệt lời v2.** Trần còn lại (vì sao chưa 10): ⓐ 4 nghiên cứu cùng một nhịp "thí nghiệm → số → câu nói lại" — nghe liền dễ đều tai ở phút 8–12; nếu demo nghe đều thì đổi mục 4 sang kể qua người quen trước, nghiên cứu sau ⓑ câu 1 dùng 「子ども」 — người không có con bị đẩy ra ngoài một nhịp ⓒ mục 1 sát trần 2:00.
2. Chốt: **giọng TTS** · **lớp hình** · **khuôn thumbnail** · **có CTA giữa bài không** (kênh chưa có cả 4).
3. Sau khi chốt: render demo đoạn mở + chuyện chốt để nghe tag (`humanize-script-voice.md` §3); đo lại mốc giây trên wav.
4. Đối chiếu web 12 tháng cho `人の目` (loại nhiễu bài hát/drama) trước khi khoá A1.
5. Nếu bài này thành khuôn → viết `05_SCRIPT_FORMULA.md` cho kênh.
