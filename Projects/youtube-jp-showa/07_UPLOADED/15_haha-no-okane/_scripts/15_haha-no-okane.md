# 15 — 昭和の母のお金の常識5選（給料袋のその後・つけ払い・内職・妻の年金） (video #15)

Kịch bản đọc: `15_haha-no-okane_TTS.md` · Video: `06_VIDEO/15_haha-no-okane/` (chưa tạo)
Trục **B** (số tiền/chế độ có nguồn) → giọng **阿井田茂 / Calm / 0.90**, hồ sơ **`showa-b`**
(AivisSpeech port 10101 — **mở app trước khi render**). Hệ số đọc **4,93 ký/giây**.
**5.033 ký → ước 17,0 phút** (bản **v2**, viết lại 2026-09-17 sau vòng đánh giá retention — §7). 🔴 Mốc thật chỉ chốt từ `timeline.json` SAU render.

Gate: `python tools/check_script_formula.py 03_SCRIPTS/15_haha-no-okane_TTS.md --truc B` → **SẠCH toàn bộ tầng CHẶN** (§5).

---

## 0. VÌ SAO ĐỀ TÀI NÀY — chọn bằng SỐ ĐO, không bằng cảm giác

### 0.1 Số đo của CHÍNH kênh (YouTube Data API, 2026-09-17, view/ngày)

| video của kênh | v/ngày | view | tuổi |
|---|---:|---:|---:|
| **11 給料袋20選** | **258,6** | 1.519 | 5,9d |
| **08 お金の常識12選** | **109,4** | 1.523 | 13,9d |
| **06 初任給の封筒** | **95,4** | 1.804 | 18,9d |
| 02 商店街から消えたもの30 | 51,5 | 1.439 | 27,9d |
| 09 外食12選 | 27,5 | 328 | 11,9d |
| … 10 通学路 | 7,4 | 66 | 8,9d |
| **13 子育ての常識5選** | **3,7** | 7 | 1,9d |
| **12 夏の当たり前5つ** | **2,8** | 11 | 3,9d |

🔴 **Ba video mạnh nhất của kênh đều là cụm TIỀN**, và khoảng cách không nhỏ (258 vs 2,8 = **92×**).
⚠️ Và đây **không phải artifact recency**: hai bài yếu nhất lại là hai bài **mới nhất** (1,9d và 3,9d) —
nhiễu recency thổi view/ngày LÊN, nên nếu có thiên vị thì nó đang thiên vị *cho* hai bài đó.

### 0.2 「Đang được đề xuất」 đo thế nào khi kênh chưa có token Analytics

Kênh showa **không có `credentials/token.json`** ⇒ không đọc được `insightTrafficSourceDetail`.
Thay bằng phép đo public: chạy `measure_kw_youtube.py` trên rổ keyword ngách, xem **video của mình
xếp ở đâu trong chính rổ đó**:

| keyword | hạng của video kênh mình trong 30 ngày |
|---|---|
| `昭和の初任給` | **#1 (video 11, 259 v/ngày)** và **#2 (video 06, 95 v/ngày)** |
| `昭和の給料` | **#3** (sau 1 video ひろゆき 335K và 1 video あの頃の昭和) |

⇒ YouTube đã xếp kênh này vào ô **「tiền thời 昭和」**. Đó là khu phố đang mở — và là khu phố nên
đi tiếp, chứ không phải khu 常識 phi-tiền mà hai bài mới nhất vừa rớt.

### 0.3 Cung của ngách ở cụm "tiền trong NHÀ" gần như TRỐNG (2026-09-17, 30 ngày, long-form ≥8′)

| keyword | n video | med v/ngày |
|---|---:|---:|
| `昭和のへそくり` | **0** | — |
| `昭和の通帳` | **0** | — |
| `昭和のローン` | **0** | — |
| `昭和の内職` | **0** | — |
| `昭和の商店街 つけ払い` | **0** | — |
| `昭和の家計` | 14 | 2 |
| `昭和のお金` | 6 | 85 |

⚠️ **Đọc đúng: cung trống KHÔNG phải bằng chứng có cầu.** Cầu ở đây đến từ chỗ khác — từ chính
3 video tiền của kênh mình (0.1) và từ `昭和の常識` (med **3.386** v/ngày, n=9) là khung hook đang nóng.
Cung trống chỉ có nghĩa: **nếu cầu có thật thì không ai đang phục vụ nó.**

### 0.4 ### HÀNG XÓM MỤC TIÊU (`youtube-suggested-growth.md` §1)

| video | kênh | số | vì sao mình là "next watch" của nó |
|---|---|---|---|
| **給料袋20選** (video 11 của CHÍNH mình) | 昭和くらし図鑑 | 258 v/ngày | Bài đó kết ở lúc **phong bì được đưa cho mẹ**. Bài này bắt đầu **đúng từ giây sau đó**: cái phong bì ấy đi đâu |
| 【昭和30年〜40年】今とは大違い！昭和のお金の常識5選 | あの頃の昭和チャンネル | 13.975 view / 20,9d | Cùng cụm tiền, nhưng họ làm **giá cả**; mình làm **dòng tiền trong nhà + mốc luật** |
| 【昭和30〜50年代】昭和の常識20選 | 昭和の音がする | 249.234 view / 17,8d | Khung 「今なら全部アウト」. Mục 5 của mình (**妻に年金がなかった**) chính là một 「今ならアウト」 mà họ chưa chạm |

### 0.5 ⚠️ CHỒNG LẤN với video 11 và 06 — đã kiểm

| | video 06 | video 11 | **video 15 (bài này)** |
|---|---|---|---|
| chủ thể | **giá cả** một tháng lương mua được gì | **cái phong bì** + vì sao nó biến mất | **dòng tiền SAU KHI vào nhà**, và người quản nó |
| nhân vật | người mới đi làm | bố → mẹ → con | **MẸ** (chủ ngữ của cả 5 mục) |
| mốc dùng chung | 初任給 昭和45年 | 口座振込 1969/1974 | dùng lại **2 mốc** này, nhưng làm *bối cảnh*, không làm *chủ đề* |

⇒ Trùng đúng 2 con số, khác hẳn mạch. Đây là **series**, không phải lặp.

---

## 1. FACT SHEET — ✅ VERIFY 2026-09-17, nguồn cấp 1

| # | fact | giá trị | nguồn |
|---|---|---|---|
| **F1** | 労働基準法 第24条 通貨払いの原則 | 賃金は**通貨で・直接本人に・全額**払う (昭和22年法律第49号) | 労働基準法 |
| **F2** | 給与の口座振込 | サービス開始 **1969年(昭44)** · 国家公務員 **1974年(昭49)** | 国立国会図書館 レファレンス協同データベース (dẫn 『富士銀行の百年』『銀行協会五十年史』) — đã dùng ở FACT SHEET video 11 |
| **F3** | **大規模小売店舗法** | 大規模小売店舗における小売業の事業活動の調整に関する法律 = **昭和48年法律第109号**, 公布 **1973-10-01** | 衆議院「制定法律情報」第71回国会 法律第109号 |
| **F4** | **家内労働法** | **昭和45年法律第60号**, 公布 **1970-05-16**; 審議機関・施行体制の規定は6/1, その他は **1970-10-01** 施行 | 衆議院「制定法律情報」第63回国会 法律第60号 |
| **F5** | **割賦販売法** | **昭和36年法律第159号**, 公布 **1961-07-01**; 施行=公布から6か月を超えない範囲で政令の定める日 | 衆議院「制定法律情報」第38回国会 法律第159号 |
| **F6** | **貸金業の規制等に関する法律** | **昭和58年法律第32号**, 公布 **1983-05-13**; 登録制 + 業務規制 | 衆議院「制定法律情報」第98回国会 法律第32号 |
| **F7** | **国民年金法** | **昭和34年法律第141号** | 国民年金法 (dẫn trong F8) |
| **F8** | **昭和60年改正** | 国民年金法等の一部を改正する法律 = **昭和60年法律第34号**, 公布 1985-05-01, **施行 昭和61年4月1日**(附則第1条) | 衆議院「制定法律情報」第102回国会 法律第34号 |
| **F9** | 改正前の妻の扱い — **nguyên văn** | 「改正前は民間サラリーマン等の妻（専業主婦）は、夫の年金（配偶者加給年金額等）で保障することとされ、また、**国民年金に任意で加入することができた**」/「**任意加入していない妻が離婚したり、障害になった場合には年金が受給できない**という問題」 | 厚生労働省「年金制度の仕組みと考え方」**第5 公的年金制度の歴史** |
| **F10** | 第3号被保険者 + 呼称 | サラリーマン等の妻も国民年金に**加入を義務づけ**、**1人1人に自分名義の基礎年金**を支給。厚労省はこれを「**女性の年金権の確立**」と呼ぶ | 〃 |
| **F11** | 基礎年金額 | **月額50.000円**（40年加入・**1984年価格**） | 〃 |
| **F12** | 大卒初任給 昭和45年(1970) | **39.900円** | 厚生労働省「賃金構造基本統計調査」(đã verify ở video 11) |
| **F13** | CPI 全国 (2020=100) | 1970 = **30,9** → 直近 **111,9** | 総務省統計局「消費者物価指数」 |

### 🔢 PHÉP TÍNH ghi rõ để kiểm được

```
初任給 昭和45年 39.900円 を今の感覚に直す
  39.900 × (111,9 ÷ 30,9) = 39.900 × 3,6214 = 144.494 円
  → 台本では「およそ十四万円」と丸める（切り捨て側、盛らない）
```

### ⛔ Ý ĐỊNH DÙNG NHƯNG **ĐÃ BỎ** vì không verify được trong lượt này

| định dùng | vì sao bỏ |
|---|---|
| 郵便貯金 定額貯金「金利8%・10年で2倍」 | BOJ CSV `post_rate` **chỉ có từ 1988**; PDF 郵政資料館 không đọc được. Và video 08 đã dùng cụm 「貯金は10年で2倍」 ⇒ bỏ luôn, tránh lặp |
| 専業主婦世帯 vs 共働き世帯 (1980年 1114万/614万) | trang 男女共同参画白書 trả 404, WebSearch chập chờn. **Không đưa số chưa verify vào bài** |
| ダイエー1号店 1957年 (現金正価販売) | nguồn cấp 1 là tài liệu công ty, chưa tra kịp → thay bằng **F3 大店法 1973** làm mốc chết của mục 2 |
| へそくり thống kê | không có nguồn cấp 1. ⇒ 米びつ chỉ xuất hiện như **ký ức/hình ảnh**, không gắn con số nào |

---

## 2. CẤU TRÚC — E7 cold open + 5 mục × 5 ô

**COLD OPEN v2 (E7 + OPEN LOOP, không lời chào cho tới hết khối):** ① hành vi có SỐ
(母がちゃぶ台に封筒を**九枚**並べる) → ② nghịch lý 1 câu (**自分の分は、いちばん薄い**) → ③ 「これ、実話です」
+ **証人 CẦM HIỆN VẬT** (七十代の知人が、お母さんの**家計簿を、いまも持っています**) → ④ 3 cú sốc dồn, mỗi cái 1 vế
(財布は出さない／台所は工場になる／テレビは判を押して買う) → ⑤ 🔴 **OPEN LOOP**:
「ただ、どこにも書かれていない項目が、**ひとつだけあります**」 → ⑥ **dán nhãn**
→ 挨拶 → PROMISE (nhắc lại loop: 「最後に、書かれていなかった話を」) → **vào mục 1 ở 54,0s**.

| mục | tên | ③「では、なぜ」 | ④ MỐC CHẾT | ⑤ hạ cánh mềm |
|---|---|---|---|---|
| **1** | 給料は、封筒の現金で、母の手に渡る | 法律だった — **労基法24条** (昭22) | 口座振込 **昭44** → 公務員 **昭49** | 「重さを確かめる一瞬は、通帳には映らなかったのかもしれません」 |
| **2** | 買い物は、その場で払わない（ツケ・通い帳・御用聞き） | 現金が入る日が月に一度しかない → 支えたのは**信用** | 現金正価の店 → **大店法 昭48** | 「帳面に名前を書いてもらえること自体が、ひとつの財産だったのかもしれません」 |
| — | **CTA giữa video (~50%)** — câu canonical showa (`cta-midvideo.md` §2.10), đổi cụm 給食 → **お母さんのお金の思い出** | | | |
| **3** | 夜の台所が、工場になる（内職） | 外で働くのが普通でなかった + それでも足りない | **家内労働法 昭45** (5/16公布・10/1施行) — それまで最低工賃の基準すらなし | 「段ボールの山は、家計簿のどの欄にも書かれないまま片づけられたのかもしれません」 |
| **4** | 大きな買い物は月賦。足りない月は借りる | 制度が先にできていた | **割賦販売法 昭36** → **貸金業規制法 昭58年5月13日** | 「朱色の丸が最後まで並んだ日の母の顔は、制度のどこにも残らなかったのかもしれません」 |
| **5** ⭐ | **母には、自分の名前の年金がなかった** | 夫婦はずっと一緒にいる前提で作られていた | **国年法 昭34** → 任意加入 → **昭60年改正・施行 昭61年4月1日** → 第3号被保険者 | 「米びつの底のお金は、へそくりというより、自分の名前がないことへの、いちばん現実的な備えだったのかもしれません」 |

**TỔNG LUẬN — 認める→裏返す:** 「変わってよかったことばかりです」(nhận: ツケは返せない家には重すぎた・内職も線の引かれていない借金もなくなってよかった) →
「それでも」(lật: 通帳も年金も自分の名前では持たないまま、家のお金を一円単位で回していた) → 「あれは経営でした。そして、その経営者は、給料をもらっていませんでした」
→ **rồi mới** xin comment (体験談: 「お母さんは、お金をどこにしまっていましたか」) → chữ ký kênh 「次のページ」.

**Sóng độ dài (5 mục, đo thật bản v2):** 785 · 946 · 734 · 806 · **1.363 ký** — tỉ số **1,9×**, mục dài nhất = **#5 ở 73% bài** — mục dài nhất = **#5 ở 73% bài** (đỉnh cảm xúc đặt cuối, cùng chiều K1).
⚠️ Gate miễn phép đo sóng khi <8 mục (K2 1,43× · K3 1,23×); tỉ số của bài này là **1,9×**.

---

## 3. ĐÓNG GÓI CTR

### Title CHỐT

```
【昭和40〜60年】今では信じられない 母のお金の常識5選｜つけ払い・夜の内職・妻に年金はなかった【昭和100年】
```

### 📊 BẢNG ĐO KEYWORD — YouTube Data API, 30 ngày, JP/ja, long-form ≥8′ (2026-09-17)

> ⚠️ Google Trends trả 429 từ 2026-09-13 → dùng đường đo API (view THẬT), đúng ngoại lệ đã ghi ở `03_THUMBNAIL_FORMULA.md` §1.2.

| keyword | n | **med v/ngày** | max v/ngày | dùng ở đâu |
|---|---:|---:|---:|---|
| **昭和の常識** | 9 | **3.386** | 195.496 | ⭐ **từ dẫn** — vào title + hero thumbnail |
| 昭和の暮らし | 9 | 1.487 | 13.998 | 概要欄 + tag |
| 昭和の当たり前 | 3 | 454 | 13.998 | tag |
| 昭和のお金 | 6 | 85 | 668 | title (chủ đề) + tag |
| 昭和の給料 | 7 | 109 | 16.847 | tag (nối video 11) |
| 昭和の母 | 9 | 69 | 1.487 | tag |
| 昭和の初任給 | 6 | 10 | 259 | tag — **kênh mình đang #1 và #2 rổ này** |
| 昭和のへそくり / 通帳 / ローン / 内職 | **0** | — | — | cung trống, không có tín hiệu cầu → **không đưa lên title** |

### 3 TITLE A/B — mỗi bản một giả thuyết (`ab-3title-3thumb.md` §2)

| | title | keyword dẫn | giả thuyết thử |
|---|---|---|---|
| **A1** ⭐ dùng khi đăng | `【昭和40〜60年】今では信じられない 母のお金の常識5選｜つけ払い・夜の内職・妻に年金はなかった【昭和100年】` | `昭和の常識` | keyword đo cao nhất rổ (3.386 v/ngày) + khung 「今では信じられない」 đang là khung thắng của ngách |
| **A2** | `【昭和40〜60年】給料袋の、その後｜母が回していた昭和のお金5選 つけ払い・内職・月賦【昭和100年】` | `昭和の給料` | đổi keyword dẫn sang cụm mà **kênh mình đang xếp #1–#3**; nối thẳng video 11 để ăn rail suggested của chính nó |
| **A3** | `家計を握っていた母に、なぜ年金がなかったのか｜昭和のお金の常識5選【昭和40〜60年】【昭和100年】` | `昭和の常識` @0 | đổi **kiểu hook**: liệt kê → **nghịch lý + truy nguyên** (đúng định vị 図鑑), và đẩy mục 5 lên làm mặt tiền |

### Tên file upload

```
showa-haha-no-okane-joushiki-5sen.mp4
```

### 3 dòng đầu 概要欄 (vùng hiển thị — cấm lời chào)

```
昭和40〜60年、家のお金を回していたのはお母さんでした。給料袋の分け方、商店街のツケと通い帳、夜の内職、月賦、そして「妻に自分名義の年金がなかった」話まで、昭和のお金の常識を5つ。
当時それが当たり前だった理由を、労働基準法24条・家内労働法・割賦販売法・貸金業規制法・昭和60年の年金改正といった実際の制度から確かめていきます。
50代・60代・70代の方はもちろん、お母さんの昔の暮らしを知りたい方にも。出典は概要欄の最後にまとめました。
```

### 概要欄 — 本文（目次は render 後に timeline.json から確定）

```
【この動画について】
昭和40年から60年ごろ、日本の家庭でお金を管理していたのは、多くの場合お母さんでした。
給料は封筒の現金で手渡され、買い物は商店街のツケ、足りない分は夜の内職と月賦で埋める。
その一方で、会社員の妻には長いあいだ「自分の名前の年金」がありませんでした。
この動画では、昭和のお母さんのお金の常識を5つ取り上げ、なぜそれが当たり前だったのかを、
当時の法律・制度から確かめていきます。

【目次】
00:00 昭和の、お母さんのお金
00:52 一点目 給料は、封筒の現金で、母の手に渡る
03:36 二点目 買い物は、その場で払わない（ツケと通い帳）
06:08 三点目 夜の台所が、工場になる（内職）
08:55 四点目 大きな買い物は月賦、足りない月は借りる
11:09 五点目 母には、自分の名前の年金がなかった
14:10 昭和のお母さんは、給料をもらわない経営者だった

【出典】
・労働基準法 第24条（賃金の支払）
・家内労働法（昭和45年法律第60号／1970年5月16日公布）
・割賦販売法（昭和36年法律第159号／1961年7月1日公布）
・大規模小売店舗法（昭和48年法律第109号／1973年10月1日公布）
・貸金業の規制等に関する法律（昭和58年法律第32号／1983年5月13日公布）
・国民年金法等の一部を改正する法律（昭和60年法律第34号／施行 昭和61年4月1日）
・厚生労働省「年金制度の仕組みと考え方」第5 公的年金制度の歴史
・厚生労働省「賃金構造基本統計調査」／総務省統計局「消費者物価指数」
・国立国会図書館 レファレンス協同データベース（給与振込の開始時期）

※この動画は、公開されている統計・法令をもとに構成しています。
※映像は当時の雰囲気を再現したイメージで、実在の人物・団体とは関係ありません。

昭和くらし図鑑では、昭和の「当たり前」を、年号と資料でたどっていきます。
```

### Pinned comment

```
最後までご覧いただき、ありがとうございます。

あなたのお母さんは、お金をどこにしまっていましたか。
米びつの底でしたか、それとも、たんすの一番下でしたか。

封筒を分ける音、通い帳に名前を書いてもらったこと、夜中の内職。
覚えていることを、ひとつでいいので聞かせてください。

※この動画の年号と制度は、衆議院「制定法律情報」および厚生労働省
「年金制度の仕組みと考え方」など、公開資料をもとに構成しています。
出典は概要欄の最後にまとめました。
```

### タグ

```
昭和の常識,昭和の暮らし,昭和のお金,昭和の当たり前,昭和の母,昭和の主婦,昭和の家計,昭和の給料,
昭和の初任給,給料袋,つけ払い,通い帳,内職,家内労働法,月賦,割賦販売法,サラ金,貸金業規制法,
第3号被保険者,昭和60年改正,年金,昭和40年代,昭和50年代,昭和レトロ,懐かしい,昭和100年,
昭和くらし図鑑,50代,60代,70代
```

### ハッシュタグ（volume 順）

```
#昭和の常識 #昭和の暮らし #昭和のお金 #昭和レトロ #昭和100年
```

### ⚖️ Quét compliance (`youtube-compliance.md`)

| mục | kết quả |
|---|---|
| từ nhạy ở title/thumbnail | ✅ sạch — không có 殺/血/死/自殺/虐待… |
| tên người/công ty thật | ✅ không có (店 đều là 魚屋/米屋 chung chung) |
| số liệu YMYL | ✅ mọi con số có nguồn cấp 1 ở §1; không claim tư vấn tài chính hiện hành |
| AI video | 🔴 **PHẢI TICK「altered/synthetic content」** (100% t2v) |
| nhạc/ảnh | BGM orgel free −40dB; cấm 昭和歌謡 thật |

---

## 4. THUMBNAIL — spec 3 bản (⏳ chưa render, xem §6)

Khuôn **K-COLLAGE** (`03_THUMBNAIL_FORMULA.md`) + biến thể K-PHOTO đang thử từ video 08.
Chữ **giống hệt nhau ở cả 3 bản** (biến thử là HÌNH — `ab-3title-3thumb.md` §3 mục 6):

| khối | chữ | vai |
|---|---|---|
| chip 年代 | `昭和40〜60年` | mốc |
| HERO 1 | `母のお金の常識` | ① VỀ CÁI GÌ (chứa keyword đo cao nhất `常識`) |
| **HERO 2 — ĐỎ, TO NHẤT** | `妻に年金はなかった` | ② CHUYỆN GÌ XẢY RA |
| burst | `5選` | đếm |

- **T1** = K-COLLAGE: 4 ô sepia (給料袋を分ける手 / 通い帳 / 夜の内職 / 米びつ) + **1 ô MÀU RỰC** = 茶封筒.
- **T2** = đổi **1 biến hình**: giữ nguyên chữ, thay collage bằng **1 ảnh có NGƯỜI** (母が封筒を並べている手元 + 顔).
- **T3** = đổi **layout**: mặt người chiếm nửa khung, chữ dồn nửa còn lại.

⚠️ Gate 4 của `audience-45plus.md` §1 (≥1 khuôn mặt) — T1 collage không có mặt, T2/T3 có ⇒ bộ 3 tự phủ.

---

## 5. SỐ ĐO GATE (chạy 2026-09-17)

```
=== CHECK SCRIPT FORMULA — 15_haha-no-okane_TTS.md (truc B) — BAN v2 ===
    5033 ky -> 17.0 phut @ 4.93 ky/s   |   DONG CO: LIST
  [OK] DONG CO chinh          LIST            (phap/che do 20 · moc nam 1/296)
  [OK] dong mem               6               >=5
  [OK] moc nam                17 (1/296)      >=8 va 1/<=500
  [OK] so ky                  5033 (17.0')    4289-5324
  [OK] vao muc 1              54.0s           <=60s
  [OK] nay-xua 11 · naze 7 · phap 20 · loi thuat 11 · **chung nhan 5** (ban v1: 2)
  [warn] ngu quan 12 (1/419)  — E-LIST khong doi; K1 (ban 100K) chi 1/2888
  SONG: 734..1363 ky = 1.9x · muc dai nhat #5 @73% bai
KET QUA: SACH toan bo gate CHAN.
```

**Gate tag (`humanize-script-voice.md` §2):** tag đứng một dòng riêng = **0** · tag giữa dòng = **0** ·
mật độ **89 cụm / 1 cụm per 56 ký** (video 14 = 1/73 · video 11 = 1/115).

🔴 **Bẫy đã dính và đã sửa trong lượt này, ghi để không lặp:** bản đầu có **40 tag nằm giữa dòng**
(kiểu `。[速0.9]…`). Cả hai script đã render của kênh (11, 14) đều có **0** tag giữa dòng — luật
「tag chỉ ăn ở ĐẦU DÒNG」 được thi hành nghiêm, tag giữa dòng sẽ bị TTS **đọc thành lời**. Đã tách
dòng tại đúng 40 chỗ (tất cả đều đứng sau `。` hoặc `」` nên không vỡ câu).

---

## 6. VIỆC CÒN LẠI TRƯỚC KHI RENDER

1. ⛔ **Render demo giọng 1–2 đoạn** (`humanize-script-voice.md` §3) — đoạn cold open + mục 5 — trước khi render cả bài.
2. `06_VIDEO/15_haha-no-okane/` chưa tạo. Prompt t2v: `gen_prompts_15.py` **phải `import videogen_lib`**, chỉ khai P/C/S (`04_VIDEOGEN_PROMPTS.md`).
3. Trần **8,0 giây/clip**; spreader chia theo **TRẦN**, không theo trung bình.
4. **Đủ asset mới được render** (`render-background.md` §1.5).
5. Bộ **3×3** chưa đủ: có 3 title, **chưa có 3 thumbnail** → `upload_pack.py` sẽ hét `🔴 GATE 3×3`.
6. 目次 chốt từ `timeline.json` SAU render, không dùng số ước ở §3.
7. Lịch: bộ ngày **C = T3·T5·T7, 18:00 JST**. Video 14 (昭和の職場) **đã render, chưa đăng** ⇒ 14 đi slot trước, 15 đi slot kế.

---

## 7. VÒNG ĐÁNH GIÁ RETENTION — chấm bản v1, và 5 thứ đã sửa (2026-09-17)

### 7.1 Chấm bản v1: **6/10**

Bản v1 **sạch mọi gate máy** mà vẫn chỉ đáng 6 điểm — đúng bài học đã ghi ở `05_SCRIPT_FORMULA.md` §0:
*gate đo CẤU TRÚC, không đo sức giữ chân*. Năm lỗi đo được:

| # | lỗi | số đo bản v1 |
|---|---|---|
| **1** | 🔴 **KHÔNG CÓ OPEN LOOP.** Bài mở bằng 5 câu mô tả đẹp rồi vào thẳng mục 1. Người xem không nợ một câu trả lời nào ⇒ **không có lý do cơ học nào để ở lại tới mục 5** | 0 loop |
| **2** | 🔴 **5 mục RỜI RẠC.** Mỗi mục là một "điều đương nhiên" độc lập, hết mục là hết. Không có sợi chỉ vật lý nối chúng | 0 cầu nối giữa các mục |
| **3** | **Chứng nhân dùng 1 lần rồi vứt.** 「七十代になる知人のお母さん」 xuất hiện ở giây 15 rồi biến mất khỏi bài | 証人 = **2** lần |
| **4** | **Cold open spoil mất đỉnh bài.** Câu 5 của v1 đã nói thẳng 「その母には、自分の名前の年金がありませんでした」 — tức **bán mất payoff của mục 5 ngay ở giây 20**, rồi bắt người ta xem 16 phút để nghe lại điều đã biết | — |
| **5** | Mục 5 là đỉnh nhưng **chưa từng được hứa**; 4 mục đầu không ai dẫn người xem về phía nó | — |

### 7.2 Cái đã sửa ở v2 — **một cú sửa, không phải năm cú vá**

⭐ **Trục sửa: cho chứng nhân một HIỆN VẬT, rồi lấy hiện vật đó làm xương sống cả bài.**
知人 không chỉ *kể lại*, mà **đang giữ cuốn 家計簿 của mẹ mình**. Từ đó:

| | v1 | **v2** |
|---|---|---|
| **open loop** | không có | 「最後までめくっても、**どこにも書かれていない項目が、ひとつだけあります**」 — là **CÂU HỎI treo**, không phải lời đếm (`feedback_openloop_la_cau_hoi_khong_phai_dem`), và nó **giấu** đáp án thay vì bán trước |
| **nối 5 mục** | rời | mỗi mục = **một trang của cùng cuốn sổ**: bìa trong ghi 9 tên phong bì → trang tiệm (ツケ) → tháng chữ nhỏ lại (内職) → trang dấu son (月賦) → **trang cuối** (年金) |
| **cầu nối** | 0 | **4 cầu**, mỗi cầu 2 câu, kết mục N mở mục N+1 (vd: 「ところが、そのツケが払いきれない月もありました。ある月から、急に、**字が細かくなる**」) |
| **証人** | 2 lần | **5 lần**, rải suốt bài |
| **payoff mục 5** | nói trước ở giây 20 | dồn về đúng chỗ: 「ここまでが、ノートに書いてあることです… **書かれていなかったのは、最後のひとつだけでした**」 rồi mới vào mục 5 |
| **CTA giữa** | CTA trơn | CTA + **nhắc lại loop** (「書かれていなかった項目の話は、このあとすぐです」) — giữ người qua đúng mốc 50% |
| **đóng bài** | kết luận chung | 証人 quay lại lần cuối: sổ dừng ở cuối 昭和50年代 vì mắt bà kém; chế độ đến **ngay sau đó** → 「間に合ったのか、間に合わなかったのか。ノートには、そこまでは書いてありません」 |

### 7.3 ⚖️ RANH GIỚI YMYL của cuốn sổ — đọc trước khi dựng hình

Cuốn 家計簿 là **ký ức của chứng nhân**, đúng loại với 「65の私の父の話です」 của K1 (`05_SCRIPT_FORMULA.md` §4 E7).
🔴 **Không một con số nào trong bài được rút ra từ nó.** Mọi số/mốc vẫn từ §1 (厚労省・総務省・衆議院).
Sổ chỉ chở **hình ảnh** (9 cái tên trên bìa trong, chữ nhỏ lại, dấu son, trang cuối).
⛔ Khi dựng t2v: **cấm** làm cận cảnh trang sổ có **số tiền đọc được** — vừa là bịa hiện vật, vừa dính
`feedback_so_tren_hinh_phai_do_font_ve`. Sổ quay ở góc nghiêng/tay lật, chữ không đọc ra.

### 7.4 Ba lỗi máy bắt được trong chính vòng sửa này

1. 🔴 **Câu CTA chứa chữ 「五点目」 ⇒ gate đếm thành MỤC THỨ 6** (27 ký), tỉ số sóng nhảy lên **48,3×**.
   Gate `ITEM` bắt mọi cụm `◯点目` **ở bất cứ đâu trong bài**, không chỉ ở đầu mục. ⇒ **Ngoài heading mục,
   cấm viết `◯点目` trong lời kể.** Đã đổi thành 「このあとすぐです」.
2. **Vào mục 1 = 60,0s** — đúng mép trần. Đã rút 6 chỗ ở cold open/promise → **54,0s**.
   ⚠️ Đây là số **ƯỚC**; hệ số đọc của kênh đã sai 4 lần (CLAUDE.md §Sản xuất) ⇒ **chốt lại từ `timeline.json`**,
   nếu render thật >60s thì cắt tiếp ở PROMISE, không cắt ở 3 cú sốc.
3. **đóng mềm rơi về 5** (sát sàn) sau khi viết lại → đã thêm 1 câu 「〜気がします」 ở cuối mục 5.

### 7.5 Còn nợ — nói thẳng

- **ngũ quan 1/419** vẫn ở tầng CẢNH BÁO (chuẩn E-SCENE là 1/250). Bài này chạy động cơ **E-LIST**
  như K1 (K1 chỉ 1/2.888 mà vẫn 100K+), nên không chặn — nhưng nếu muốn lên nữa thì đây là khoản rẻ nhất:
  thêm tiếng/mùi vào mục 2 và mục 4.
- **Chưa render demo giọng.** Bài này sống bằng khoảng lặng (`[間0.9]` trước mục 5, `[間0.6]` trước loop);
  nghe mới biết nhịp có ăn không. `humanize-script-voice.md` §3 bắt buộc bước này.
- 🔴 **Thứ kịch bản KHÔNG chữa được: CTR và mismatch thumbnail ↔ 30 giây đầu.** Video 06 của kênh
  PASS mọi gate mà vẫn rớt **62% trước 0:30** vì thumbnail hứa một đằng, mở bài kể một nẻo
  (`CHANNEL_DIAGNOSIS_2026-09-03.md` §5.3). ⇒ Thumbnail của bài này **bắt buộc** phải mang đúng
  hai thứ mà cold open bán: **cuốn sổ/phong bì** và **câu "妻に年金はなかった"**. Spec ở §4.

---

## 8. LỚP HÌNH — SLIDES + prompt t2v (dựng 2026-09-17)

### 8.1 Thứ tự chạy (vòng tròn phụ thuộc, đừng đảo)

```
run_voice15.cmd  ──► voice.wav + timeline.json + subs.srt     (AivisSpeech port 10101 phải bật)
      ↓
build_slides_15.py ──► 03_SCRIPTS/15_haha-no-okane_SLIDES.json + clips/_MAP.txt
      ↓
gen_prompts_15.py  ──► videogen_FLOW.txt (169 dòng) + _TENFILE.txt + _BLOCKS.md
```
🔴 `video_render.py` đòi SLIDES **trước cả khâu giọng**, mà `build_slides` lại cần `timeline.json`
— thứ chỉ có **sau** khi tổng hợp giọng. Đó là lý do có `make_voice_15.py` riêng (gọi thẳng
`render_audio_timeline()` của renderer, cùng cache, cùng cách đo mốc). ⛔ Đừng ước timeline bằng
số ký — đã đo: lệch dồn +8,6s (`feedback_timeline_phai_do_tu_wav_that`).

### 8.2 Số đo SLIDES (gate SẠCH)

| | |
|---|---|
| tổng | **915,6s = 15,26 phút** · 125 dòng lời |
| số clip | **169** |
| dài clip | min 3,03s · trung bình 5,42s · **max 7,84s** (trần cứng 8,0s — không khe nào vượt) |
| nhịp | **11,1 đổi hình/phút** (Style B của bản 219K, `CLAUDE.md` §Visual) |
| cue cứng | **122/169** neo đúng đầu dòng lời; còn lại là cắt trong lòng dòng dài |
| entry 0 | `video: true` ✅ |

🔴 **Một lỗi gate bắt được, phải sửa ở KỊCH BẢN chứ không ở builder:** câu
「皆さまの思い出が、次のページになります。」 xuất hiện **2 lần** (CTA giữa + CTA cuối) ⇒ `match`
không còn duy nhất ⇒ builder không biết neo clip vào dòng nào. Đã đổi câu cuối thành
「いただいた思い出が、そのまま次のページになります。」 rồi synth lại (cache theo nội dung nên chỉ
dòng đó được đọc lại). ⇒ **Luật: trong một script, đừng để hai dòng có cùng phần mở đầu.**

### 8.3 Thế giới hình — 3 nhân vật, 1 hiện vật

- **A_HAHA** (người mẹ, 割烹着) = **đôi mắt chính, 122/169 clip là POV của bà** (72%). Lý do không
  phải thẩm mỹ: cả bài là *"bàn tay đó làm gì với tiền"*, và POV một người là cách rẻ nhất giữ
  "nhân vật đồng nhất" — chỉ phải giữ MỘT thân người xuyên 169 clip.
- **A_IMA** (chứng nhân 70 tuổi, thời NAY) = người **đang cầm cuốn 家計簿**. Motif lật sổ quay lại ở
  mọi khối — đó là thứ nối 5 mục thành một mạch (§7.2).
- **A_CHICHI** = người bố. ⛔ **Trần 3 nhân vật có tên** (gate): hàng cá, người giao hàng, người thu
  tiền đều hạ xuống **danh ngữ** (`the fishmonger` / `the delivery man` / `the collector`) vì họ chỉ
  xuất hiện vài clip, không cần khoá đồng nhất.
- ⛔ **Nhân vật trẻ em đã bị gỡ hoàn toàn** — filter Veo chặn từ trẻ em, và giữ lại thì thành nhân
  vật thứ 4. Các cảnh đó chuyển sang A_CHICHI.

### 8.4 Bốn vòng sửa gate (80 → 44 → 10 → 2 → 0)

| vòng | lỗi đỏ | sửa ở TẦNG NÀO |
|---|---|---|
| 1 | **80** | chuỗi khai thiếu `out` (28 cảnh) · chuỗi `B` rải rác khắp bài không liền nhau · chuỗi dùng 2 preset |
| 2 | **44** | ⭐ `CUT` **tự tính bằng máy**: cắt chuỗi tại mọi chỗ đổi framing trong cùng (khối, preset) — trước đó viết tay nên sót ~30 chỗ |
| 3 | **10** | `while …` phải chứa từ SECONDARY thật (`shivers`/`glows`/`daylight … moves` **không** khớp — phải là `shadow`/`sway`/`wind`/`steam`/`light moves`) · bỏ 4 cast phụ · 2 ca OCCLUDE (nhét tiền vào túi / dúi xuống gạo → *áp phẳng dưới nẹp tạp dề* / *đặt lên rồi phủ vải*) |
| 4 | **0** ✅ | 9 cảnh thiếu **hướng tương đối camera** (thêm `left to right across the frame` / `staying in place`) |

⭐ **Bài học dùng lại được:** vòng 2 là vòng rẻ nhất vì nó **không sửa nội dung cảnh nào** — chỉ
thay một luật viết tay bằng 5 dòng tính CUT. Mỗi lần gate báo cùng một lỗi ở ~30 chỗ, hỏi ngay
*"cái này là lỗi của 30 cảnh hay của một luật?"* (`ai-video-regen.md` §0).

### 8.5 Số đo lô prompt

`169 prompt · dài 1.827–4.008 ký (trung bình 3.175)` · POV 72% · họ động tác: MANIP 156 · MOVE 79 ·
WORK 68 · VEHICLE 40 · SOCIAL 18 · CARE 16 · PLAY 10 · EAT 5 · REACT 2 — **MANIP/MOVE 39%** (dưới
trần 45%), **31 shot vui chơi/quây quần** (cần ≥12). 0 prompt chứa từ trẻ em, 0 prompt `hands only`.

### 8.6 ⚠️ MỘT PHÁT HIỆN CHƯA SỬA — guard `Avoid:` nằm ở **62–75%** prompt

`ai-video-regen.md` §2 là luật đo được: **cấm cái gì thì phải cấm trong 15% ĐẦU prompt**, đặt cuối
thì model bám tả cảnh và bỏ qua (đo thật: guard số ở 55% → 4/6 clip vẫn có số; đưa lên 2% → sạch).
Nhưng `videogen_lib.py` ghép khối `AVOID` **gần cuối** — đo trên lô này: **169/169 prompt có
`Avoid:` ở 62–75%**.

⛔ **Tao KHÔNG tự sửa**, vì `videogen_lib` là công thức dùng chung của **mọi video kênh này** —
đổi thứ tự khối là đổi toàn bộ lô 14 đang chờ đăng và mọi lô sau, và chưa có phép đo nào của
showa nói lô hiện tại đang hỏng vì lý do đó. Hai đường, cần user chọn:
- **ⓐ** giữ nguyên, gen thử 10 clip đầu rồi soi — nếu lỗi chuyển động (giật/trượt chân/lặp động tác)
  xuất hiện thì mới đảo thứ tự;
- **ⓑ** đảo ngay trong `videogen_lib`: đưa `AVOID` lên ngay sau câu khai mở, rồi **gen lại lô 14 để
  đối chứng** (nếu không thì hai lô khác công thức, không so được).

### 8.7 Việc còn lại

1. Bơm `videogen_FLOW.txt` vào extension Flow → tải 169 clip → đổi tên theo `videogen_TENFILE.txt`,
   rồi map sang `clips/clip_<index>.mp4` bằng `clips/_MAP.txt`.
   🔴 Renderer định danh clip **theo SỐ THỨ TỰ SLOT**, không theo tên mô tả — đặt tên mô tả vào
   `clips/` thì renderer coi như **không có clip nào** và âm thầm fallback ảnh tĩnh, `EXITCODE=0`.
2. Soi nghiệm thu bằng `tools/review_clips.py` (sheet 4 frame + dải mép) — contact sheet 1 frame đã
   từng cho qua 24/24 clip lỗi.
3. **Đủ 169 clip mới được render video** (`render-background.md` §1.5).
4. SFX cho từng clip (`CLAUDE.md` §Visual) — gain tính từ mean đo được, `alimiter … level=disabled`.
5. Thumbnail 3 bản (§4) — hiện mới có 3 title, gate 3×3 sẽ hét.

### 8.8 ⭐ VÒNG SỬA COLD OPEN — user: *"30s đầu phải sinh động lên. Ngồi nhìn mấy cái phong bì thì tù quá"* (2026-09-17)

**Chẩn đoán bản đầu — hai tầng cùng hỏng, không phải một:**

| tầng | bản đầu | vì sao tù |
|---|---|---|
| **NHỊP** | 7 clip / 37,9s = **5,4s mỗi cảnh** | cold open dùng chung trần 8s với thân bài. Nhưng 30–40s đầu là chỗ rớt nặng nhất — nó cần nhịp **khác** phần còn lại. Peer đo được: 60 giây đầu **7–8 cắt** |
| **LOẠI CẢNH** | **6/7 là cận cảnh bàn tay trên mặt bàn** · 0 khung rộng · 0 người di chuyển · 1 bối cảnh rưỡi | mắt không có gì để bám. Cả đoạn là một cái bàn |

**Sửa ở TẦNG TOOL (nhịp) — `build_slides_15.py`:**
- Thêm **trần riêng cho cold open**: `HOOK_END = 37.9` · `HOOK_MAX = 3.4s` → **7 → 13 clip**, trung bình **2,7s/cảnh**.
- Thêm **sàn `MIN_CLIP = 2.2s`**: trần 3,4 làm vài dòng bị chẻ đôi thành 1,79s — vụn tới mức mất cảm giác "một cảnh". Sàn ưu tiên hơn trần nhịp.
- 🔴 **Tách HAI TRẦN khác vai — đây là phần đáng học:** gate bản đầu chặn theo `HOOK_MAX` nên **báo đỏ một SLIDES hoàn toàn lành** (khe 3,59s). Hai trần đo hai thứ khác nhau:
  · `MAX_CLIP = 8,0s` = **trần KỸ THUẬT** — vượt là renderer `-stream_loop` lặp clip ⇒ **CHẶN**;
  · `HOOK_MAX = 3,4s` = **mục tiêu NHỊP** — vượt chỉ là chậm hơn ý muốn ⇒ **cảnh báo**.
  Cùng bệnh với `audience-45plus.md` §6.10: *gate chặn phải đo cái thật sự hỏng, không đo mục tiêu thẩm mỹ.*

**Sửa ở TẦNG CẢNH (loại hình) — 13 cảnh HOOK viết lại từ đầu:**

| | bản đầu | bản v2 |
|---|---|---|
| cận cảnh tay | **6/7** | **2/16** |
| khung rộng / có người | 1/7 | **11/16** |
| bối cảnh | 2 | **5** (chanoma · ima_ie · shotengai · daidokoro · genkansaki) |
| góc máy | 4 loại | **8 loại** — wide 4 · medium 3 · high 2 · pov_look 2 · pov_hand 2 · low 1 · pov_sit 1 · ots 1 |

- **Mở bằng nhịp ĐẾN NƠI**, không dựng sẵn: mẹ **đi vào** từ hành lang, ôm chồng phong bì, quỳ xuống bàn (wide, có người, có chuyển động).
- **Cú đấm thị giác ở cảnh 2**: góc **thấp ngang mặt bàn**, hàng phong bì chạy dài về phía xa — thấy ngay *"chín cái"*, thay vì cận một cái.
- **Ba cú sốc = ba bối cảnh khác nhau, đều có người**: phố chợ đông (nhận cá rồi đi tiếp, không rút ví) → bếp đêm nhìn từ phòng tối (một bóng người dưới bóng đèn duy nhất) → cửa nhà (người thu tiền đóng dấu son).
- **Chứng nhân xuất hiện bằng NGƯỜI, không bằng tay**: ông cụ **đi vào phòng**, ngồi xuống, mở sổ (medium) — rồi mới tới hai cảnh lật sổ.
- **Cảnh dán nhãn** đóng bằng wide: mẹ ôm cả chồng phong bì trước ngực, cả phòng phía sau.

🔴 **Một lỗi gate đáng ghi:** hai cảnh RỘNG liên tiếp cùng bối cảnh (`wide → high`) bị chặn — *"mắt sẽ chờ chúng khớp mà model không giữ được phòng"*. Đổi cảnh 2 sang góc **`low`** vừa gỡ lỗi vừa cho hình đẹp hơn ý ban đầu.

**Số đo sau vòng sửa:** SLIDES **176 clip** (169 → 176, chỉ HOOK+INTRO đổi) · nhịp **11,5 đổi hình/phút** · clip ngắn nhất **2,36s** · gate SLIDES + gate prompt đều **SẠCH** · POV toàn video 68%.

### 8.9 PHÉP THỬ ⓐ — lô 10 clip, kiểm vị trí guard `Avoid:` (user chốt 2026-09-17)

**Câu hỏi cần trả lời:** khối `Avoid:` của `videogen_lib` nằm ở **65–75%** prompt (đo trên chính 10
prompt này). Luật `ai-video-regen.md` §2 nói câu CẤM phải ở **≤15%** đầu, đặt sau thì model bỏ qua —
nhưng bằng chứng đó đến từ kênh **nenkin**, nơi cấm **số/chữ**. Ở đây cấm **lỗi chuyển động**.
⇒ Thử 10 clip để có bằng chứng của **chính kênh này** trước khi đụng thư viện dùng chung.

**File:** `videogen_FLOW_TEST10.txt` (10 dòng) + `videogen_TENFILE_TEST10.txt` (tên file khớp thứ tự).
Lô này = **H0–H9, tức trọn cold open** ⇒ một lượt gen kiểm được **cả hai** việc: guard có ăn không,
và 30 giây đầu đã hết tù chưa.

**Soi bằng:** `py tools/review_clips.py 06_VIDEO/15_haha-no-okane/clips_raw --edges`
(sheet 4 frame/clip: 0,8s · 3,0s · 5,2s · 7,4s — ⛔ contact sheet 1 frame đã từng cho qua 24/24 clip lỗi).

**Thang NHẬN / LOẠI — chốt trước khi soi, áp một thang cho cả lô** (`ai-video-regen.md` §1):

| | ❌ LOẠI | ✅ NHẬN |
|---|---|---|
| **chuyển động** (đúng thứ `Avoid:` đang cấm) | hình **giật/nhảy frame** · **chân trượt** trên chiếu · **lặp lại động tác** rồi undo · tay/chân **bẻ cong như cao su** · người **trôi** không bước | nhịp hơi chậm · tay hơi cứng |
| **thân người** | bàn tay/cẳng tay **không có thân** trong khung (POV hỏng) · người **biến mất** giữa clip | thân bị cắt bởi mép khung |
| **chữ/số** | chữ Nhật giả **cỡ đọc được** trên sổ/phong bì · số tiền hiện rõ | nét chữ li ti không đọc ra (sổ quay nghiêng — đúng ý §7.3) |
| **bối cảnh** | đổi hẳn căn phòng giữa clip · viền đen/lỗ răng ở mép | đồ đạc xê dịch nhẹ |

**Đọc kết quả:**
- **≤2/10 clip lỗi chuyển động** ⇒ guard ở 70% **vẫn ăn** với loại cấm này ⇒ **giữ nguyên `videogen_lib`**,
  gen tiếp 166 clip còn lại. Ghi kết quả vào đây để lần sau không phải hỏi lại.
- **≥4/10 lỗi chuyển động** ⇒ luật §2 áp đúng cả ở đây ⇒ chuyển sang **ⓑ**: đảo khối `AVOID` lên đầu
  trong `videogen_lib`, xuất lại 176 prompt, **và gen lại lô 14 để đối chứng** (không thì hai video
  khác công thức, sau này so số vô nghĩa).
- **3/10** = vùng xám ⇒ gen thêm 10 clip nữa (H10–B6) rồi mới quyết, đừng chốt trên mẫu 10.

⚠️ **Đừng đọc lô này như phép đo về NỘI DUNG cold open.** Nó cũng cho biết 30s đầu trông thế nào,
nhưng đó là câu hỏi khác (§8.8) và tiêu chí khác — hình có sinh động không, chứ không phải có lỗi không.

### 8.10 🎞️ MÀU PHIM HOÀI CỔ (user chốt 2026-09-17: *"màu phim nó hoài cổ hơn đi"*)

**Chia việc ở hai tầng — đây là phần quan trọng nhất của mục này:**

| tầng | lo gì | vì sao |
|---|---|---|
| **PROMPT** (`PROF` trong `gen_prompts_15.py`) | chỉ giữ model **khỏi gen ra ảnh QUÁ RỰC / QUÁ NÉT** | prompt **không** điều khiển được màu chính xác (`media-library.md` §2.10 ⑥). Để model tự lo màu thì 176 clip ra 176 tông ⇒ video loang lổ |
| **GRADE hậu kỳ** (`tools/grade_showa.py`) | **toàn bộ màu** | ffmpeg áp ĐỀU cho cả lô, sửa lại **không tốn credit gen**, và chỉnh được **sau khi đã nhìn thấy clip thật** |

🔴 **STYLE riêng qua `prof=`, KHÔNG sửa mặc định của `videogen_lib`** — sửa mặc định là đổi luôn lô 14
(171 clip đã gen, đang chờ đăng) và mọi video sau; hai lô khác công thức thì sau này so số vô nghĩa.
Cùng lý do đã ghi ở §8.6 với khối `Avoid:`.

### 8.10.1 Ba preset màu (`tools/grade_showa.py`)

| preset | làm gì | dùng khi |
|---|---|---|
| `showa70_soft` | ấm nhẹ, giữ sáng, vignette mờ, hạt vừa | cảnh trong nhà vốn đã tối |
| **`showa70`** ⭐ | ấm + bạc màu + halation quanh cửa sổ/đèn + hạt + vignette | **mặc định** |
| `showa70_deep` | bạc màu mạnh, ám vàng–lục rõ, hạt dày | gần phim tư liệu nhất, nhưng **ăn mất chi tiết vùng tối** |

### 8.10.2 🔴 HAI LẦN PRESET SAI — và cả hai chỉ lộ ra khi ĐO, không lộ khi nhìn

Chuẩn đối chiếu: phim tư liệu **thật** (`measure_filmlook.py`, Japan Today 1959) —
`luma 66,3 · contrast 50,1 · sat 62,4 · grain 17,76 · đen 14,7%`.

| vòng | tưởng là | đo ra | nguyên nhân |
|---|---|---|---|
| 1 | "ám vàng mạnh = hoài cổ" | **sat 75,6 → 90,1** (phải GIẢM về 62) · **grain 19,9 → 11,3** (phải TĂNG) | ① `colorbalance` mạnh làm **bão hoà HSV TĂNG** — ám màu mạnh chính là bão hoà cao theo phép đo ② `noise` đặt **trước** `unsharp` ⇒ hạt bị chính khối làm-mềm xoá sạch |
| 2 | "crush bóng cho bệt như phim" | **luma 111 → 49** (quá tối) · **đen 29,7%** (gấp đôi mức phim thật) | crush 0,09 + `brightness −0,03` + `contrast 1,08` cộng dồn |
| 3 ✅ | | **luma 60,4 · đen 15,3% · grain 14,9** — sát mốc phim thật | |

⚠️ **VÀ THƯỚC `sat` KHÔNG DÙNG ĐƯỢC Ở ĐÂY.** Nó là `S` trong HSV = `(max−min)/max`. Khi ảnh bị làm
tối / crush bóng thì `min` về 0 nhanh hơn `max` ⇒ **S tăng dù đã hạ saturation thật**. Đo được:
bản cuối vẫn báo `sat 100,7` trong khi mắt thấy **nhạt màu hơn hẳn** bản gốc.
⇒ **So `sat` giữa hai ảnh lệch luma nhiều là so sai.** Muốn đo bão hoà cho đúng thì phải khớp luma
trước, hoặc đổi sang độ lệch chuẩn kênh a·b trong Lab. Ở vòng này tao chốt bằng **luma + đen% + grain**
(ba thước không bị nhiễu) rồi **duyệt mắt** — đúng họ với `feedback_do_pixel_cua_so_quet`.

🔴 **Bẫy thứ ba, cùng lượt:** `--compare` in dòng `TRUOC | SAU -> …` **dù ffmpeg đã thất bại** —
`drawtext` cần fontconfig, máy này không có (đúng bẫy `render-background.md` §2.7 ①). Đã bỏ `drawtext`
và bắt tool kiểm `returncode` + `os.path.exists` trước khi báo xong.

### 8.10.3 Cách dùng

```bash
py tools/grade_showa.py <clip>.mp4 --compare [--preset showa70_deep]   # 1 frame TRUOC|SAU, duyệt mắt
py tools/grade_showa.py <clip>.mp4 --measure                           # số trước/sau + mốc phim thật
py tools/grade_showa.py 06_VIDEO/15_haha-no-okane/clips_raw --out 06_VIDEO/15_haha-no-okane/clips
```
Grade **không ghi đè bản gốc** (`--out` bắt buộc) — còn để so lại. Có resume theo mtime.
📌 Ảnh so sánh 4 mức đã dựng: `06_VIDEO/14_showa-no-shokuba/clips/_grade_compare/_4MUC.png`
(gốc · soft · showa70 · deep) — dựng trên clip **video 14** vì video 15 chưa gen clip nào.

### 8.10.4 Việc kèm theo

- `videogen_FLOW.txt` + `videogen_FLOW_TEST10.txt` đã **xuất lại** theo STYLE mới (176 dòng / 10 dòng).
- Lô thử ⓐ (§8.9) giờ kiểm **hai** thứ trong cùng một lượt: vị trí guard `Avoid:` **và** màu mới.
- ⏳ Chốt preset nào là mặc định cho video 15 — chờ user chọn giữa `soft` / `showa70` / `deep`.

### 8.11 👘 CHÍNH XÁC THỜI ĐẠI — trang phục + phong tục (user chốt 2026-09-17)

> *"Tôi muốn câu chuyện chạm đúng người Nhật thời đó. Quần áo phong cách ăn mặc, phong tục tập quán đúng kiểu showa"*

**Chẩn đoán:** cast và preset bản trước tả **chung chung** — `apron smock` · `dress shirt` ·
`tea cabinet` · `low wooden table`. Model sẽ gen ra quần áo hiện đại vô danh và một căn phòng có thể
ở bất kỳ nước nào. ⇒ Chi tiết thời đại phải nằm trong **CAST và PRESET**, vì hai khối đó đi vào **mọi**
prompt — chứ không rải vào từng cảnh.

**✅ Verify trước khi viết (không đoán):** 割烹着 là biểu tượng nội trợ Showa và **chỉ bắt đầu bị
エプロン kiểu Tây lấn từ 昭和40年代 trở đi** (昭和館 · Wikipedia). Bài này trục chính **昭和45年 =
1970** ⇒ 割烹着 vẫn đúng, và **bên dưới là đồ Tây** (blouse + váy), không phải kimono — 1970 thành thị
đã mặc đồ Tây. ⛔ Không dùng もんぺ (đồ thời chiến, lệch ~25 năm).

| | trước | sau |
|---|---|---|
| **mẹ** | "a plain white apron smock" | **áo choàng bếp trắng tay dài buộc nơ sau lưng**, khoác trên blouse + váy ngang gối, tóc **uốn ngắn** |
| **bố** | "white short-sleeved dress shirt" | sơ mi trắng ngắn tay + **cà vạt bản hẹp nới lỏng**, **quần âu ống rộng** + thắt lưng da, tóc chải sát |
| **phòng khách** | bàn thấp, tủ trà, TV | **ちゃぶ台 tròn**, đèn huỳnh quang **kéo dây** chụp thuỷ tinh, **điện thoại quay số đen** trên chân riêng, TV gỗ **có cánh cửa che màn hình**, **神棚** trên cao, lịch **để trắng** trên cột |
| **bếp** | bồn, bếp ga | bồn **bê tông sâu**, bếp ga **hai vòng** + ấm ám khói, kệ hở **bát men + hộp thiếc**, **米びつ gỗ**, **giấy dính ruồi** treo trần |
| **phố chợ** | hàng cá, hàng rau | cá cân bằng **cân treo**, gói bằng **giấy báo**, rau trong **thùng gỗ**, **のれん để trắng**, phụ nữ xách **giỏ tre** |
| **ngõ** | hàng rào, cột điện | thêm **hộp chuông báo cháy** trên cột, **thùng thư tròn đỏ** ở góc |
| **phòng chiếu** | tủ trà | thêm **仏壇**, **風呂敷** gấp trên tủ, **hốc tường có tranh cuộn** |

⚠️ **Mọi vật có CHỮ thật (lịch, のれん, biển hiệu) đều phải ghi `blank`/`unmarked`** — không thì model
vẽ chữ Nhật giả, và chữ đó **luôn nát** (`media-library.md` §2.9).

🔴 **Một lỗi tự gây, đáng ghi:** script thay `P`/`C` dùng regex `^ "key": "...”` — mà **`CROWD` cũng có
đúng những khoá preset đó** (`"shotengai"`, `"michi"`, `"ginkou"`, `"genkansaki"`) ⇒ 4 giá trị crowd
bị ghi đè bằng cả đoạn mô tả bối cảnh. Cú pháp vẫn hợp lệ, gate vẫn chạy, **không có gì báo đỏ**.
⇒ Khi sửa hàng loạt bằng regex, phải kiểm **khoá đó có xuất hiện ở dict nào khác không** — và kiểm lại
giá trị sau khi thay, đừng chỉ tin số lần thay.

### 8.11.1 ⭐ HỆ QUẢ CHO LỚP MÀU — 24 clip THỜI NAY không được grade

Đo lô mới: **152/176 prompt có `aged film stock`**, 24 prompt còn lại **không** — và cả 24 đều là
cảnh `ima_ie`. Đó **không phải lỗi**: `videogen_lib` có `STYLE_MODERN` riêng (sạch, sắc nét) cho cảnh
hiện đại, và nó đang làm đúng.

🔴 **Nhưng nó lộ ra một cái bẫy ở bước grade:** nếu chạy `grade_showa.py` lên **cả thư mục** thì 24 clip
thời nay cũng bị phủ màu phim 1970 ⇒ **xoá mất đối lập xưa/nay**, mà đối lập đó chính là cơ chế của
bài này (cuốn sổ cũ trong tay người thời nay, §7.2). Đã thêm cờ:

```bash
py tools/grade_showa.py 06_VIDEO/15_haha-no-okane/clips_raw \
   --out 06_VIDEO/15_haha-no-okane/clips --exclude ima_ie
```
Clip khớp `--exclude` được **copy nguyên**, không grade.

### 8.12 🔬 KẾT QUẢ LÔ THỬ 10 CLIP (2026-09-17) — **CHƯA ĐẠT**, và phép thử ⓐ đã trả lời

Nguồn: `F:\Youtube\Dự_án_mới_15_ccabfo8a` → 10 clip, **1280×720 · 24 fps · 8,000s**.
Sheet soi: `06_VIDEO/15_haha-no-okane/_sheets/review_1.jpg` (4 frame/clip) + crop 1:1 ở `_sheets/full/`.

**✅ Đúng:** 24 fps **khớp `channels.py` showa** (không judder — `feedback_fps_clip_phai_khop_renderer`) ·
割烹着 trắng tay dài + tóc búi ✓ · phòng Showa đúng chất (tatami, 障子, đèn tròn treo, TV gỗ, báo trên
sàn) · chợ đông người đúng thời · H4 · H5 · H7 · H9 sạch.

**❌ Ba nhóm lỗi:**

| # | lỗi | số clip | tầng |
|---|---|---|---|
| **1** | 🔴 **VIỀN PHIM ĐEN + lỗ răng + góc bo tròn** quanh khung | **5/10** (H0·H1·H2·H3·H6) | **LỚP** |
| **2** | 🔴 **Biển hiệu chữ Nhật giả** phủ kín khung chợ, cỡ đọc được | 1 (H6) | **LỚP** |
| **3** | người thu tiền mặc **quần yếm denim xanh** (spec ghi "grey work jacket"), và khung **chỉ thấy từ thắt lưng xuống** | 1 (H8) | clip |

#### 🔴 Lỗi 1+2 chính là câu trả lời của phép thử ⓐ — **guard ở 70% KHÔNG ĂN**

`AVOID` của `videogen_lib` cấm **rõ ràng** cả hai thứ: *"any frame or border around the image"* và
*"any letters, words, numbers or logos on any object"*. Nhưng nó nằm ở **65–75%** prompt.
Kết quả thực: **5/10 clip có viền phim**, 1 clip đầy chữ giả.
⇒ Vượt ngưỡng đã chốt ở §8.9 (**≥4/10 → chuyển ⓑ**). Luật `ai-video-regen.md` §2 đúng cả ở kênh này.

⚠️ **Và tao góp phần gây ra lỗi 1:** STYLE mới (§8.10) có cụm *"as if the print has sat in a box for
fifty years"* — nó mô tả một **VẬT THỂ PHIM**, nên model vẽ luôn khung phim. Câu này nằm ở đầu, câu
cấm viền nằm ở cuối ⇒ câu ở đầu thắng. **Đã bỏ cụm đó**, giữ màu bằng cụm tả MÀU thuần.

#### Cách thi hành ⓑ mà **không** phải gen lại lô 14

Thêm móc **`prof["HEAD"]` opt-in** vào `videogen_lib.build()` — khối đặt ở **đầu tuyệt đối** của prompt
(trước cả framing). Không khai `HEAD` thì trả chuỗi rỗng ⇒ **prompt của lô 14 không đổi một ký tự**,
không phải gen lại. Video 15 khai `GUARD` gồm hai câu cấm đã hỏng thật (viền phim · chữ trên biển hiệu).

**Đo lại sau khi sửa: `176/176 prompt có guard ở 1–3%`** (luật đòi ≤15%).

🔴 **Một bẫy Python mất một vòng mới thấy:** hàm mới đặt tên `_head`, mà `build()` **đã có biến local
`_head`** (chuỗi mô tả POV) ⇒ `UnboundLocalError`. Nhưng lần chạy đầu **vẫn "thành công"** vì
`__pycache__` giữ bản cũ — tức tao suýt kết luận "móc không ăn" trong khi nó còn chưa chạy.
⇒ **Sửa thư viện xong thì xoá `tools/__pycache__` trước khi đo.** Đã đổi tên thành `_head_block`.

#### ⚠️ Hai thứ lô này xác nhận, ghi để khỏi bàn lại

1. **Vẫn PHẢI grade màu.** Đo clip thật: `grain 1,9–8,0` (phim thật **17,8**) · `luma 92–153`
   (mục tiêu **66**) · `đen 0,9–13,1%` (mục tiêu **14,7%**). STYLE kéo được *tông ấm*, nhưng
   **không** kéo được hạt/độ sáng/đen bệt ⇒ đúng phân công đã ghi ở §8.10: màu là việc của grade.
2. **Clip ra 720p**, renderer xuất 1080p ⇒ sẽ phải upscale. Nếu Flow có tuỳ chọn 1080p thì **nên bật
   trước khi gen 166 clip còn lại** — upscale 720→1080 làm mềm chi tiết, mà bài này nhiều cận cảnh chữ/vật nhỏ.

**Việc tiếp:** gen lại đúng 10 clip này bằng `videogen_FLOW_TEST10.txt` **mới** (đã có guard ở đầu)
rồi soi lại. Nếu viền phim và chữ giả biến mất ⇒ chốt công thức, gen 166 clip còn lại.

### 8.13 👪 KHUNG PHẢI CÓ NGƯỜI NHÀ (user chốt 2026-09-17)

> *"Video ngồi 1 mình thì có thêm các con hoặc chồng vào. Cứ có 1 người ngồi 1 góc thế nó hơi lạc so với cảnh tượng gia đình"*

**Đo trước khi sửa:** **47/63** cảnh trong nhà (`chanoma` · `chabudai` · `zashiki`) **không có một
mệnh đề người nào** — khung chỉ có mẹ. Đúng như user nói: bài kể về một gia đình mà hình thì toàn
một người ngồi lẻ.

**⛔ Không thể thêm nhân vật trẻ em — ràng buộc thật, không phải lựa chọn:** filter của Veo chặn từ
trẻ em (`child`/`boy`/`girl`/`pupil`…), đã phải gỡ nhân vật con ở vòng gate trước. Và **trần 3 nhân
vật có tên** đã dùng hết (A_HAHA · A_CHICHI · A_IMA) — thêm cast thứ tư là gate đỏ.

**⇒ Cách làm:** thêm người bằng **mệnh đề nền `as …` + nâng CROWD**, tức lớp người **vô danh** của
`videogen_lib` (EXTRA_LOCK). Khung có người mà không phá trần cast, không dùng từ bị chặn.

| | trước | sau |
|---|---|---|
| `chabudai` (cận mặt bàn) | `solo` | **`few`** — vẫn thấy **tay/chén/báo của người nhà ở rìa khung** |
| `zashiki` | `solo` | **`few`** — có người ở phòng bên kia màn giấy |
| mệnh đề người | 16/63 cảnh | **61/63** |

Mệnh đề **xoay vòng 5 biến thể** mỗi bối cảnh, không lặp một câu 20 lần. Với cận cảnh mặt bàn thì
không tả được cả người, nên đưa **dấu hiệu có người** vào rìa khung: *chén trà thứ hai trong tầm với ·
một đôi tay khác đặt ở mép xa · một bàn tay với lấy ấm · tờ báo ai đó vừa đặt xuống · bóng người ngồi
đối diện đổ qua mặt bàn*.

**⛔ Bốn chỗ GIỮ NGUYÊN một mình — vì một mình chính là nội dung:**
- `daidokoro` (bếp đêm, mục 3): cả nhà đã ngủ, mẹ làm một mình — **đó là luận điểm của mục**.
- `engawa` (cuối bài): khoảng lặng.
- `ima_ie` (thời NAY): một người với cuốn sổ — đối lập xưa/nay.
- **G5** (bút treo trên trang giấy mà không viết) · **G26** (tắt đèn) — hai cảnh đỉnh bài, cô đơn có chủ ý.

Gate vẫn **SẠCH** · 45 cảnh được thêm người · `SOCIAL 21 · EAT 16` (trước: 19 · 5) · guard vẫn ở
đầu **176/176** prompt.
