# 18 — 年金を60歳から受け取ると、月4万3千円減ったまま一生｜窓口で聞かれた一言と、注意点の十一行目

> Kênh: 年金と老後のお金研究室 · **Trụ ① 年金（tính số）** — xoay trụ sau 16(③税) và 17(②給付金/bảo vệ)
> Viết **2026-08-29** · **Thông tin thời điểm 令和8年8月**
> Khuôn: **③質問型（窓口で聞かれる一言）+ fear-forward** — KHÔNG lặp ②事件型 của video 16 và 17
> **Trả lời hẹn tập ĐÍCH DANH đã nói trên sóng cuối video 17:** 「来年、60歳になる松本さんの話です。60歳、65歳、70歳。実際に受け取り始める年齢によって、生涯に受け取る総額は、どれくらい変わるのか。松本さんの決断を追いながら、次回の研究で、一緒に計算します。」
> Độ dài **đo trên wav thật**: **15:14** (913,7s · **bản v3**, `_TTS.md` được sửa lúc 2026-08-30 00:38 + synth lại 00:40 — đảo cấu trúc: câu bạn câu cá lên giây 17 · ba con số lên giây 97 · hồ sơ 松本 dời xuống sau 原典). Timeline **115 dòng**, lệch wav 0,97%. Bản v1 giữ ở `_TTS.md.bak_v1`; v3 đã chạy lại `check_pace.py`: **8/8 ✅** (cold open 1:13 · cast 1:24 · CTA 42% — sát mép dưới · stake/あなた 0:00) · tag 26, 0 lệch, 0 `**`.
> Lớp hình: ⭐ **REMOTION** theo quy trình chuẩn `CLAUDE.md` §② "QUY TRÌNH CHUẨN TỪ VIDEO 18 TRỞ ĐI" — **đây là video ĐẦU TIÊN chạy quy trình đó**. Chi tiết ở mục CHUẨN BỊ DỰNG cuối file.

---

## GĐ0a — LỌC TRỤ

Đề tài: chọn tuổi bắt đầu nhận 老齢年金 (60/65/70) và cái giá của 繰上げ. Nằm nguyên **trụ ① 年金 tính số**. Không đụng 不動産 / 金融商品 / iDeCo / NISA / 介護費用. **PASS.**

⚠️ **Chỗ dễ trùng với video 02 — đã kiểm và tách bạch:**

| | video 02 (2026-07-20) | video 18 (bài này) |
|---|---|---|
| Phạm vi | **65 vs 70** (繰下げ) | **60 vs 65 vs 70**, trọng tâm là **60歳繰上げ** |
| Câu hỏi | 「70まで待つと得か」 | 「早くもらうと何を失うか」 |
| Lõi | 損益分岐点 + timeline 65→90 | **5つの代償（権利が消える）** — 損益分岐点 chỉ là đòn bẩy để lật |
| Cast | 高橋 (chính) | **松本 (chính)** — 高橋 chỉ callback 1 câu |
| Kết luận | chọn thời điểm | **hoãn quyết định một cách có kế hoạch** |

Tức 18 KHÔNG phải bản làm lại của 02: 02 hỏi "chờ có lời không", 18 hỏi "vội thì mất gì". Hai video nối nhau chứ không nuốt nhau.

## GĐ0c — ĐO ĐỐI THỦ + ĐO TREND (làm TRƯỚC khi viết chữ nào)

### 1) Swipe file (`tools/swipe_titles.py --group nenkin`, quét lại **2026-08-29** — số tươi)

- Cụm **受給開始年齢 đang ăn view thật**: `【知らないと大損】年金受給で損をしないための年齢を徹底解説！（繰上げ・繰下げ受給）` — **109.130 view / 30 ngày** (3.638 view/ngày, 年金・給付金完全攻略 143K sub); `【速報!】年金は65歳からだと遅い！…本当に得する年金の受け取り方` — **251.481 view / 50 ngày** (みんなの給付金 553K sub).
- ⇒ Cầu đã proven. **Chỗ trống:** cả hai đều là **「徹底解説」kiểu tổng hợp chế độ**. Không video nào trong rổ quét được đi theo **một người cụ thể** và **không cái nào lấy「取り消せない権利」làm lõi** — chúng dừng ở 損益分岐点. Đó là chỗ bài này đứng.
- Không chọn 2 video 「2027年に年金制度が大激変」 (đang hot, 7.821 view/ngày) vì: luật chưa thi hành đủ ⇒ rủi ro YMYL, **và** nó phá lời hẹn tập đã nói trên sóng ở video 17. Ghi vào hàng đợi.

### ⭐ HÀNG XÓM MỤC TIÊU (`youtube-suggested-growth.md` §1)

| video hàng xóm | kênh | số | vì sao mình là "next watch" của nó |
|---|---|---|---|
| `【知らないと大損】年金受給で損をしないための年齢を徹底解説！（繰上げ・繰下げ受給）` | 年金・給付金完全攻略 (143K) | 109K view/30d | Nó giải thích **chế độ**; người xem xong vẫn chưa biết **mình** nên làm gì. Bài này đưa đúng một người 60 tuổi đi hết quyết định đó, kèm phần nó không nói: 5 quyền bị mất |
| `【速報!】年金は65歳からだと遅い！…本当に得する年金の受け取り方` | みんなの給付金 (553K) | 251K view/50d | Nó đẩy người xem về phía "nhận sớm". Bài này là **mặt còn lại** của đúng câu hỏi đó — vị trí "phản biện" là chỗ rail đề xuất hay ghép |
| `【50代・60代へ】定年退職の手続きは"順番"で損得が変わる` | お金の保健室 (2,7K) | 31K view/35d = **11,5× sub** | Cùng tệp "người vừa/sắp 60", cùng khung "thứ tự quyết định" |

### 2) Google Trends — YouTube Search 30 ngày, geo=JP (đo 2026-08-29)

Rổ 1 (thang gốc): `年金 60歳` **40** · `年金 何歳から` **5** · `繰上げ受給` **~0** · `繰下げ受給` **~0** · `年金 受給開始年齢` **0**
Rổ 2 (anchor = `年金 60歳`, hệ số quy đổi ×1,82): `年金 65歳` 32→**58** · `年金 いくら` 25→**45** · `年金 60歳` 22→**40** · `年金 繰上げ` ~1 · `年金 損` ~1

| keyword | YouTube 30d (quy về 1 thang) | Web 12m | dùng ở đâu |
|---|---|---|---|
| **年金 65歳** | **58** | **68** | ⭐ title A2, dòng 1 概要欄, tag |
| **年金 いくら** | 45 | — | mô tả, tag |
| **年金 60歳** | **40** | 44 | ⭐ title A1 (keyword dẫn), slug, thumbnail |
| 年金 何歳から | 5 | 24 | tag, mô tả |
| 繰上げ受給 / 繰下げ受給 | ~0 | ~2 | **CHỈ tag** |

🔴 **Kết luận đắt nhất của lượt đo: `繰上げ受給`・`繰下げ受給` là TỪ CHẾT — và chết ở CẢ HAI nguồn** (YouTube 30d ~0, web 12m ~2). Tức không phải nhiễu mẫu nhỏ của YouTube: **thuật ngữ chính thức của chế độ không phải thứ người ta gõ**. Người ta gõ `年金 65歳`, `年金 60歳`, `年金 何歳から`.
⇒ **Cấm để 繰上げ/繰下げ làm keyword dẫn ở title/thumbnail/slug.** Đây là **lặp lại đúng bài học video 08** (`年金振込通知書` = 0 điểm) — lần thứ hai kênh này suýt dẫn bằng từ ngành.

## GĐ0b — FACT SHEET (verify TRƯỚC khi viết, 2026-08-29)

| # | Fact | Số | Nguồn (đã mở, đọc tận trang) | 原典ショット |
|---|---|---|---|---|
| 1 | 減額率 繰上げ (sinh từ 昭和37年4月2日 trở đi) | **0,4%/tháng · 60歳 = 24,0%** | 日本年金機構「年金の繰上げ受給」(更新 2024-08-19) | ✅ **shot #1** — bảng 繰上げ減額率早見表, khoanh đỏ dòng `60歳 24.0％` |
| 2 | 減額率 với người sinh 昭和37年4月1日 trở về trước | 0,5%/tháng · 60歳 = 30,0% | ↑ cùng trang | (trong shot #1) |
| 3 | **減額は一生** | 「その減額率は一生変わりません」 | ↑ cùng trang, đoạn mở | ✅ **shot #1** (khoanh câu này) |
| 4 | **繰上げ請求は取消しできない** | 「繰上げ請求を取消しすることはできません」 | ↑ 繰上げ請求の注意点, gạch đầu dòng 3 | ✅ **shot #2** — chụp trọn khối 注意点 (13 dòng) |
| 5 | **事後重症などの障害年金を請求できない** | 「治療中の病気や持病がある方は注意してください」 | ↑ 注意点 | ✅ shot #2 |
| 6 | 65歳まで 遺族厚生年金と併給不可 (chọn một) | — | ↑ 注意点 | ✅ shot #2 |
| 7 | 任意加入・追納 không được | — | ↑ 注意点 | ✅ shot #2 |
| 8 | 雇用保険 基本手当/高年齢雇用継続給付 ⇒ 老齢厚生年金 一部or全部 支給停止 | — | ↑ 注意点 | ✅ shot #2 |
| 9 | 増額率 繰下げ | **0,7%/tháng · 70歳 = 42,0% · 75歳 = 84,0%** | 日本年金機構「年金の繰下げ受給」(更新 **2026-08-12**) | ✅ **shot #3** — 繰下げ増額率早見表 |
| 10 | **繰下げ待機中は加給年金が出ない・加給年金は繰下げても増えない** | — | ↑ 繰下げの注意点, gạch đầu dòng 1 | ✅ shot #3 |
| 11 | 加給年金額（配偶者）令和8年4月から | **243.800 + 特別加算 179.900 = 423.700円/năm** | 日本年金機構「加給年金額と振替加算」(更新 **2026-07-31**) | ✅ shot #4 (tuỳ chọn) |
| 12 | 加給年金 bắt đầu từ **65歳到達時点** (繰上げ KHÔNG kéo sớm) | — | ↑ cùng trang, đoạn 受給要件 | ✅ shot #4 |
| 13 | 老齢基礎年金 満額 令和8年4月分から (sinh 昭和31年4月2日以後) | **847.300円/năm** | 日本年金機構「老齢基礎年金の受給要件…」(更新 2026-04-01) | ✅ shot #5 (tuỳ chọn) |
| 14 | **60歳男性の平均余命** | **23,63年** (→ khoảng 83歳7か月) | 厚生労働省「令和6年簡易生命表の概況」表1 | ✅ **shot #6** — khoanh dòng `60 … 23.63` |

### Phân loại số (luật YMYL #2)

- **① nguồn chính thức, dùng thẳng:** fact 1–14 ở trên.
- **② 計算 tự của 当研究室** (đã show công thức trong lời, và nói rõ là "当研究室が松本さんの数字だけで割り出した"):
  - 松本 60歳受給 = 18万 × 0,76 = **13万6.800円/月** · năm 164万1.600円
  - 松本 70歳受給 = 18万 × 1,42 = **25万5.600円/月** · năm 306万7.200円
  - chênh 60↔65 = **4万3.200円/月** = 51万8.400円/năm
  - 損益分岐点 60 vs 65 = 65 + (164万1.600×5 ÷ 51万8.400) = 65 + 15,83年 = **80歳10か月**
  - 損益分岐点 65 vs 70 = 216万×(X−65) = 306万7.200×(X−70) → **81歳11か月**
  - đến 83歳7か月 (平均余命): 60歳受給 3.874万 vs 65歳受給 4.017万 → chênh **≈143万円**
  - 加給年金 5 năm của 松本 = 42万3.700 × 5 = **211万8.500 ≈ 212万円**
- **③ ballpark phụ thuộc người / đã hedge trong thoại:** mức 支給停止 do 高年齢雇用継続給付 → trong lời nói thẳng 「止まる額は人によって違いますので、必ず、年金事務所で試算してもらってください」. **Cố ý KHÔNG đưa con số %** — chưa verify được ở lượt này, và trích nguyên văn nguồn là đủ đúng.

⚠️ **Cờ rà lại trước ngày đăng:** ① 加給年金 423.700円 và 満額 847.300円 là số **令和8年度**, đổi theo 年度 ② câu hẹn tập 19 nói 高年齢雇用継続給付「令和7年の四月から、率が変わりました」 — **video 19 BẮT BUỘC verify con số % tại 厚労省/ハローワーク trước khi viết**, bài này cố ý không nêu số.

### 原典ショット (GĐ0d) — 3 shot bắt buộc, đều là cơ quan công

1. **shot #1** 日本年金機構「年金の繰上げ受給」— bảng 減額率早見表 + câu 「一生変わりません」 → dùng ở **第3章 (~3:30)**, tức **trong 4 phút đầu** ✓
2. **shot #2** cùng trang, khối 「繰上げ請求の注意点」13 dòng → dùng ở **第7章**, khoanh đỏ dòng 取消しできません và dòng 障害年金
3. **shot #3** 日本年金機構「年金の繰下げ受給」— 増額率早見表 + dòng 加給年金額を受け取ることができません → **第8章**

Compliance: cả 3 đều là trang 日本年金機構 (cơ quan công) ✓ · không chiếu trang báo/blog/công ty ✓ · không dùng giấy tờ thật của người thật ✓.

### ⚠️ MỘT CHỖ LỆCH CANON — đã xử lý, ghi lại để không ai "sửa ngược"

Video 17 (đã lên sóng) hẹn tập bằng câu 「**来年**、60歳になる松本さん」. Nhưng canon của cast là
**松本 ĐÃ 60 tuổi và vừa 定年** — đặt từ video 05, chốt lại ở video 11 (chọn 継続雇用), và ghi trong
`CLAUDE.md` §① bảng cast (`松本(60 千葉)`). Tức **câu hẹn tập của video 17 mới là chỗ sai**, không
phải hồ sơ cast.

Xử lý ở bài này: theo **canon** (60 tuổi, vừa 定年 — nếu không thì cả video 05 lẫn video 11 hỏng
theo), nhưng **bỏ mốc 今年/来年** khỏi câu giới thiệu — viết 「六十歳になったばかりです」. Người xem
video 17 rồi xem bài này sẽ không nghe thấy hai câu đá nhau.
📌 Luật rút ra: **câu hẹn tập cũng là một khẳng định về cast** — trước khi viết 「来年◯歳になる…」 phải
tra bảng cast, y như mọi con số đời của nhân vật.

## GĐ1 — SỔ XOAY KHUÔN (chống inauthentic)

| | video 16 | video 17 | **video 18 (bài này)** |
|---|---|---|---|
| Trụ | ③ 税 | ② 給付金/bảo vệ | **① 年金** ✓ khác cả hai |
| Khuôn mở bài | ②事件型「詐欺か間違いか」 | ②事件型「電話が鳴る」 | **③質問型「窓口で聞かれる一言」** ✓ không lặp |
| 計算タイム | 引き算の階段 | (không có khối tính) | **三段の階段 60/65/70 + 損益分岐点の割り算** ✓ |
| Closer | ○×クイズ | ○×クイズ 3問 | **行動プラン 3ステップ** ✓ không lặp |
| Cast chính | 高橋 | 鈴木 | **松本** (lần đầu đóng chính từ video 05) ✓ |
| Tuyến | 書類を読む | cảnh báo lừa đảo | **evergreen 決断ガイド** ✓ |

## 🔴 SỬA LẦN 2 (2026-08-29) — user chấm bản v1, tự phê bình trước khi sửa

User hỏi thẳng: *"người xem đến với video này vì cái gì, ở lại vì cái gì"* + *"nội dung không được rời rạc"*.
Bản v1 (giữ ở `_TTS.md.bak_v1`) tự chấm **6/10**. Ba lỗi thật, đo được, không phải cảm giác:

1. **Cold open là THÔNG BÁO, không phải HOOK.** v1 nói hết ngay trong 50 giây đầu: giảm 24% · mất 4万3千円 ·
   không rút lại được · *"hôm nay xác nhận 3 điều"*. Người xem biết trọn nội dung trước phút 1 ⇒ **hết lý do
   ở lại**. Đối chiếu: video 15/16 mở bằng **nghi ngờ** 「詐欺か間違いか」 và đo được `relPerf@30s` gấp đôi
   bản ngôi-thứ-ba trung tính (`08_ANALYTICS_LOG.md` block 2026-08-20).
2. **「5つの代償」 của v1 không phải open-loop — nó là MỤC LỤC.** Báo trước *"có năm thứ sẽ biến mất"* rồi
   6 phút sau đọc đúng năm thứ đó. **Đếm trước ≠ nghi vấn treo.** Open-loop thật phải là một **câu hỏi
   chưa có đáp án**.
3. **"Rời rạc" — bắt được bằng một phép thử, không phải bằng cảm giác:** tráo thứ tự các khối
   三段の階段 ↔ 損益分岐点 ↔ 平均余命 ↔ 5つの代償 ↔ 加給年金 của v1 thì **không ai nhận ra**. Mỗi khối tự
   đóng, không khối nào *cần* khối trước ⇒ đó là định nghĩa của listicle. ⚠️ Đây là **lỗi lặp**: đã tự phê
   bình đúng điều này ở video 16 rồi tái phạm ở 18.

Hai lỗi phụ: **松本 không có rủi ro** (nghe bạn xúi → đi hỏi → quyết đúng ngay; trong khi 鈴木 ở video 17
**đã bấm số 1** rồi mới được cứu — có sai lầm mới có hồi hộp), và **cú lật ở 第5章 tự làm yếu bài**
(*"chênh chỉ 143万"* giải toả nỗi sợ đúng giữa bài, rồi phải dựng lại từ đầu).

### Sửa: một CÂU HỎI LẠ thay cho một DANH SÁCH (giữ nguyên 100% FACT SHEET, chỉ đổi KHUÔN KỂ)

松本 **đã cầm bút, ngòi đã chạm giấy** ở ô 「60歳」. Nhân viên quầy ngẩng lên, hỏi một câu **không liên
quan gì tới tiền**: 「失礼ですが、いま、どこか通院はされていますか」.

⭐ **Câu hỏi đó vừa là hook, vừa LÀ payoff đắt nhất của bài** (繰上げ đóng vĩnh viễn cửa 障害年金) — nên
open-loop và đáp án là **cùng một thứ**, không phải hai thứ ghép cạnh nhau. Đó là điều v1 không có.

Và mọi khối giờ **móc vào câu hỏi đó**, không còn tự đóng:

| khối | v1 (rời) | v2 (móc vào) |
|---|---|---|
| 三段の階段 | "đây là 3 con số" | **vì sao 松本 muốn nộp đơn** |
| 損益分岐点 80歳10か月 | payoff riêng | **và anh ấy tính KHÔNG SAI** ⇒ câu hỏi càng lạ |
| 平均余命 143万 | cú lật làm yếu bài | **đẩy nghi vấn lên đỉnh**: 損得 không giải thích nổi câu hỏi kia |
| 5つの代償 | danh sách đã báo trước | **ĐÁP ÁN, nằm ở dòng thứ 11** của 注意点 |
| 加給年金 212万 | khối thứ 6 | mặt còn lại của cùng một cơ chế "mất quyền chọn" |
| 松本の決断 | quyết định hợp lý | **có sức nặng** vì anh ấy suýt ký thật, và anh ấy CÓ 持病 |

📌 **Chi tiết 「十一行目」 là móc 研究室 mạnh nhất bài** — đếm trên chính trang gốc: khối
「繰上げ請求の注意点」 có **13 dòng**, dòng 障害年金 là **dòng 11**. Cold open hứa *"đọc tới dòng 11 mới
hiểu"*, 第7章 trả đúng dòng 11. Cụ thể, kiểm được, và không kênh nào trong swipe file làm.

⚖️ **Cái mất, ghi thẳng:** v2 **hoãn một phần con số** — v1 bắn 4万3千円 + 「取り消せません」 trong 20 giây
đầu; v2 vẫn đưa 円 ở câu 1 nhưng đẩy 「取り消せない」 xuống 第7章, đổi lấy nghi vấn treo. Nếu retention
0–30s của video này **thấp hơn** video 16/17 thì đây là biến đầu tiên xét lại.

## GĐ2 — DÀN Ý (v2, mốc đo bằng `check_pace.py`)

| Chương | Mốc | Nội dung | Vai |
|---|---|---|---|
| 1 | 0:00–1:07 | あなた + 円 ngay câu 1 → 松本 đang điền đơn → **ngòi bút chạm giấy** → 「いま、どこか通院はされていますか」 → 手を止めました → *"tại sao hỏi bệnh?"* → hứa **十一行目** | 🔴 **open-loop** |
| 2 | 1:07–2:40 | Vì sao 松本 định chọn 60歳: câu của bạn câu cá, lương còn nửa, vợ 55 vẫn đi làm, cà chua ban công | động cơ (không phải khối rời) |
| 3 | 2:40–4:45 | 三段の階段 60/65/70 + quy đổi "tiền nước+gas+điện" + **原典 shot #1** + 「一生、です。」 | 計算タイム |
| 4 | 4:45–6:00 | 損益分岐点 **80歳10か月** — đóng khung là *"bạn của 松本 nói đúng hay sai?"* | payoff #1 |
| 5 | 6:00–7:10 | 平均余命 23,63年 → 差 143万 → **月5千円** → *"損得だけなら、松本さんの計算は間違っていない"* → **đóng nhịp** rồi hỏi lại: **なぜ係の方は通院の話を?** | bản lề, nghi vấn đỉnh |
| 6 | ~7:15 | **CTA** (44% ✓) — đặt SAU khi nhịp 損得 vừa đóng, KHÔNG chặn ngay trước reveal (`cta-midvideo.md` §1 mục 3) | — |
| 7 | 7:15–9:40 | **ĐÁP ÁN** + **shot #2**: 13 dòng · dòng 1 · dòng 3 (取消し不可) · **dòng 11 = 障害年金** → 「治療中の病気や持病がある方は注意してください」 → nhân viên biết dòng đó → **松本「はい」と答えました** → 血圧の薬、五年 | 🔴 **payoff chính** |
| 8 | 9:40–11:10 | Đọc lại các dòng còn lại bằng cùng một con mắt: 繰上げ = 選べる道が減る手続き (dòng 9 · 4 · 7) | mở rộng cơ chế |
| 9 | 11:10–12:40 | Mặt kia: 繰下げ mất **加給年金 212万** + **shot #3** + callback 高橋 | cân bằng |
| 10 | 12:40–14:00 | 松本 **không khoanh tròn, mang đơn về** + 3 quyết định + 「あの人が、あのとき、聞いてくれなかったらね」 | payoff cảm xúc |
| 11 | 14:00–14:25 | 1 誤解 (đã bỏ cái về 加給年金 vì 第9章 nói kỹ rồi) | dọn hiểu lầm |
| 12 | 14:25–15:55 | 研究ノート 4 dòng + 行動プラン 3ステップ + disclaimer | signature |
| 13 | 15:55–16:24 | Hẹn tập 19 đích danh + câu kết cố định | mở loop |

## GĐ3 — COLD OPEN (v3 — sửa 2026-08-30 theo `CHANNEL_DIAGNOSIS_2026-08-29.md` §3.2/§3.5)

**Vì sao đổi khỏi v2:** khám kênh 08-29 đo được 4 video có モニター kể chuyện trong 60–120s mất 13–22 điểm retention, video 09 (không モニター, đọc lộ trình + 「まず、事実から」) đứng phẳng. v2 đưa 松本さん vào giây 18 và kể 釣り仲間・課長38年 tới phút 2 = đúng khuôn bị đo là mất người. Đối thủ 1,3M view (フクロウ) tới giây 60 đã nói xong: 対象 · stake · lộ trình 3 mục · open-loop.

**Khuôn v3 (73s, `check_pace.py` PASS 8/8, đo 2026-08-30):**
| mốc | việc | dòng |
|---|---|---|
| 0:00 | あなた + 円 (giữ y v2) | 六十歳になると、あなたは… 月およそ四万三千二百円 |
| 0:18 | **対象 + phản bác định kiến** | 「早くもらったほうが得だ」…そう聞いたことのある方。いま六十歳前後で請求書が手元にある方。今日は、あなたの回です |
| 0:35 | **lộ trình** | 三つの金額を順番に計算します。六十歳から・六十五歳から・七十歳から |
| 0:52 | **open-loop = câu hỏi 通院** (giữ hook v2, bỏ tên người) | 窓口で「六十歳」に丸をつけようとした方が…「どこか通院はされていますか」 |
| 1:05 | hứa trả ở nửa sau | 答えは日本年金機構のページの十一行目。後半で、一緒に読みます |
| 1:13 | persona + 「まず、事実から」 | → 第3章 số ngay |
| 1:24 | 松本さん xuất hiện **1 dòng** (tên・県・tuổi・見込み額), không tiểu sử | |
| ~3:18 | tiểu sử 松本 (課長38年・奥さま・トマト・釣り仲間) **dời xuống đầu 第4章**, làm cầu vào 「正しいのか」 | |

Tag trong 75s đầu: **2** (`[速0.9]` dòng 1 · `[間0.6]` trước câu hỏi). Thẻ hình 20–30s = câu 対象/phản bác, không câu phủ định.
⚖️ Cái mất so v2: cảnh 窓口 mất chi tiết "ngòi bút chạm giấy"; mũi tiêm humanize ①④ (qua cast) dời từ phút 1 xuống phút 3 — vẫn đủ ≥4/6.
📊 Đo sau 5 ngày: **60→120s** so v15 (−22 điểm) · **AVD so 3:51**. Đây là phép đo A/B đầu tiên cho giả thuyết モニター.

<details><summary>(LƯU TRỮ) GĐ3 v2 — đã đè 2026-08-30</summary>


Khuôn **③質問型「窓口の一言」**. Ba việc trong 67 giây, không việc nào là mục lục:
1. **あなた ở chữ thứ 3, 円 ngay câu 1** (gate ⑦ + ⑥ đều đo được **0:00**) — người xem biết ngay đây là tiền của mình.
2. **Dựng một hành động đang dở**: ngòi bút đã chạm giấy. Không phải "một tờ giấy sẽ đến nhà" (v1) mà là
   **một người sắp làm điều không thể rút lại, ngay lúc này**.
3. **Đóng loop bằng câu hỏi, không bằng danh sách**: 「なぜ、病院の話を聞かれるのか」 + hứa 「十一行目まで
   読むことになりました」. Câu persona ở **1:07** chỉ nói *sẽ tính 3 con số rồi đi tới đáp án* — cố ý
   **không** tiết lộ có mấy thứ sẽ mất.


</details>

## GĐ4 — CHẤT NGƯỜI (`humanize-script-voice.md` — ngoại lệ §1.1: mũi ①④ đi qua CAST)

| Mũi | Đạt? | Ở đâu (v2) |
|---|---|---|
| ① trải nghiệm thật (qua CAST) | ✅ | 松本 nghe bạn câu cá xúi → về nhà nghĩ lại → **ra tận quầy điền đơn** |
| ② thoại + chi tiết đời sống vô dụng-về-thông-tin | ✅ | 3 câu thoại: bạn câu cá · nhân viên quầy · 「あの人が、あのとき、聞いてくれなかったらね」 · cà chua bi |
| ③ ký ức giác quan đúng tệp | ✅ | 4万3.200円 = tiền nước + gas + điện một tháng, còn dư · 血圧の薬、五年ほど前から |
| ④ tự làm thứ mình khuyên (qua CAST) | ✅ | 松本 tự ra quầy, tự mang đơn về **mà không khoanh tròn** |
| ⑤ đóng nhân vật bằng CẢM XÚC | ✅ | 「あの人が、あのとき、聞いてくれなかったらね」 → 「トマトが採れたら話す、と笑っていました」 |
| ⑥ phá nhịp câu ≥3 lần | ✅ | 「一生、です。」 · 「二十三年待って、百四十三万円。」 · 「そして松本さんは、その質問に——「はい」と、答えました。」 · 「血圧の薬を、五年ほど前から、飲み続けています。」 |

**6/6**, và khác v1 ở hai chỗ: **nhân vật có RỦI RO** (suýt ký) và **có bí mật giữ tới phút 9** (持病).
Người dẫn vẫn đúng vai 案内役 — không một câu trải nghiệm cá nhân.

## GĐ5 — RETENTION AUDIT + gate máy (v2)

```
python tools/check_pace.py 18_nenkin-60sai-kuriage-tsuki4man3sen
=== tổng 16:24 ===
  ✅ hết cold open            1:07   (≤1:15)
  ✅ nhân vật đầu tiên        0:17   (≤2:00)
  ✅ số con SỐ trong 30s đầu     0   (≤8)
  ✅ cửa sổ 45s dày SỐ nhất  2 @ 13:30 (≤20)
  ✅ CTA giữa video            44%   (42–58%)
  ✅ STAKE (円/日) đầu tiên     0:00   (≤0:22)
  ✅ あなた xuất hiện            0:00   (≤0:10)
  ✅ mở bài ngôi-thứ-ba         OK
✅ đạt hết (8/8)
```

Gate tag `humanize-script-voice.md` §2 — **cả ba phải sạch**:
- tag KHÔNG ở đầu dòng: **0** ✓
- tag đứng MỘT DÒNG RIÊNG (bẫy đổi mặc định vĩnh viễn): **0** ✓
- 🔴 **markdown đậm lọt vào `_TTS.md`: 0** ✓ — bản v2 đầu tiên có **2 dấu sao đôi** ở 第8章, và **TTS sẽ
  đọc chúng thành lời**. Gate cũ không bắt (nó chỉ soi `[...]`). ⇒ **Từ nay quét thêm dấu sao đôi / gạch
  dưới đôi / dấu thăng trong mọi `_TTS.md`.**
- tổng tag: **28** (dải ~15–25, sát trần — 2 đỉnh bài dùng cụm 3 tag nên đội số). Đã tỉa từ **57**.
- Đỉnh bài: `[間1.2][速0.8][後間1.0]` ở 「八十歳と、十か月」 **và** ở 「事後重症などによる障害年金を、請求
  することができなくなります」 (dòng 11 — đỉnh thật của bài) · `[間1.0][速0.8][後間0.8]` ở 「二百十二万円が、
  まるごと消えます」 · `[間0.8][速0.85]` ở 「「はい」と、答えました」.

**Audit riêng nenkin (7 mục):**
1. Giải thích chay >45s? — không; khối dài nhất (第7–8章) bị chẻ bằng số dòng 原典 và bằng 松本.
2. Case trước phút 2? — **0:17** ✓ (v1: 1:14)
3. Số nào ngoài FACT SHEET? — không.
4. Khối tính đặc có beat quy đổi? — ✅ 「水道代とガス代と電気代」 và ⭐ mới: 「二十三年待って、百四十三万円。月にならせば、五千円ほど」
5. Persona/CTA sau payoff đầu? — ✅ CTA 44%, đặt sau khi nhịp 損得 đóng, ngay trước khi mở nhịp mới.
6. ≥2 原典ショット + câu dẫn 「赤で囲んだところ」? — ✅ 3 shot.
7. Shot đầu trong 3 phút đầu? — ⚠️ **~4:00**, muộn hơn v1. Đánh đổi có chủ ý: 第1–2章 giờ là truyện, chưa
   phải chỗ mở tài liệu. **Bù lại**: cold open đã hứa 「十一行目」 nên 原典 được **nhắc tên** từ giây 55.

**Đường năng lượng v2:** câu hỏi lạ (tò mò) → người + động cơ → tính tiền (lý) → *"anh ấy tính đúng"*
(nghi vấn dâng) → **CTA** → đáp án dòng 11 (payoff) → 「はい」+ 血圧の薬 (đấm cảm xúc) → mở rộng cơ chế →
mặt kia → quyết định → ノート.
⭐ Khác mọi video 「徹底解説」 của ngách ở một điểm: bài này **không kết luận bằng 損益分岐点** — nó dùng
損益分岐点 làm **bằng chứng rằng câu hỏi kia không thể giải thích bằng tiền**.

## GĐ6 — ĐÓNG GÓI CTR

### Title CHỐT

```
年金を60歳から受け取ると月4万3千円減ります｜請求書に丸をつける前に
```

> 🔴 **Đổi 2026-08-30** (khám kênh §3.5): kênh đang bị xếp vào feed "nam 65+ nói chung" vì YouTube chưa đọc được CHỦ ĐỀ; keyword đo được (`年金 60歳`) phải **đứng đầu**, tag 【】 cảnh báo chung chung hạ xuống A3. Đây là lệch có chủ ý so với khuôn 『【】＋事件』 của CLAUDE.md — là phép thử, đọc kết quả bằng tỉ lệ RELATED cùng ngách (5/24 → ?).

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `年金を60歳から受け取ると月4万3千円減ります｜請求書に丸をつける前に` | 34 | **年金@0 · 60歳@3** | keyword đứng ĐẦU, không 【】 — dạy YouTube chủ đề (§3.5 khám kênh); đuôi = cảnh cold open |
| **A2** | `【65歳より前は要注意】年金を早くもらった人が失う5つの権利` | 31 | 65歳@2 · 年金@11 | đổi keyword dẫn sang `年金 65歳` (**58đ, cao nhất rổ**) + đổi mất-tiền → mất-quyền |
| **A3** | `【取り消せません】年金を60歳から受け取ると月4万3千円減ります` | 33 | 年金@8 | khuôn 【】 chuẩn kênh (bản A1 cũ) — đối chứng cho giả thuyết "bỏ 【】 giúp đúng khu phố" |

⚖️ Cả 3 sạch từ tắt-ad, không 外来語, không tên đảng/người thật; mọi tình tiết (月4万3千円 · 5つの権利 · câu hỏi ở quầy) **đều có thật trong video**.

### 3 THUMBNAIL A/B — ĐÃ SỬA 2026-08-30, bỏ khuôn 4 khối cũ

> 🔴 Spec ban đầu (4 khối: chip 対象 + banner + HERO + dải đỏ) **bị bỏ**: đây đúng là lỗi mà video 16
> vừa chẩn đoán và sửa thật ("4 khối chữ chồng nhau → ở 168px thành tường chữ, không điểm nhấn đơn
> lẻ. Bản nổi nhất chỉ có 3 khối. Gate 3 `audience-45plus.md` §1 đòi tổng ≤3 dòng"). Áp bài học đó:
> **bỏ chip 対象**, dùng khuôn **3 khối + badge**, giống chính xác cấu trúc video 16.

Chữ **GIỐNG NHAU cả 3 bản** (biến thử là HÌNH):

| khối | chữ | vai |
|---|---|---|
| banner navy trên | `年金 60歳から` | ① VỀ CÁI GÌ — keyword đo được cao nhất rổ (40đ) |
| **HERO vàng** | `月4万3千円減` | ② CHUYỆN GÌ XẢY RA — số verified (FACT SHEET) |
| dải đỏ đáy | `請求書に丸をつける前に` | ③ PHẢI LÀM GÌ — echo cold open, KHÔNG spoil payoff dòng 11 |
| badge góc dưới-trái | `年金研究室` | nhận diện kênh |

| | biến đổi | mô tả |
|---|---|---|
| **T1** `thumb_T1_madoguchi-pen.png` | baseline | nửa người ông 60t, ngòi bút đông cứng trên tờ đơn, nền kem sáng |
| **T2** `thumb_T2_madoguchi-counter.png` | đổi 1 biến HÌNH | bối cảnh → quầy 年金事務所, chữ/bố cục giữ nguyên |
| **T3** `thumb_T3_pen-shutai.png` | đổi LAYOUT | bỏ mặt người, tờ đơn+ngòi bút cận cảnh làm HERO — khuôn `紙が主体` (フクロウ 1,3M view) lần đầu thử ở kênh này |

Gate bắt buộc: đọc được HERO + dải đỏ ở 168px/120px · nền sáng · xoá watermark ✦ bằng cách **VÁ**
(không cắt — chữ hero chạy sát mép) · soi 1:1 cả 4 góc.
📄 Đã xuất: `thumb_prompts_FLOW.txt` (TEXT @8-10%, 1190-1418 ký, đạt gate) + `_BLOCKS.md` (đầy đủ 6
mục, kèm lý do đổi spec) + `_TENFILE.txt` + `_PLATE.txt` (3 bản không chữ, đường lui khi kanji nát).

### Tên file upload

```
nenkin-60sai-uketori-4man3sen-gen.mp4
```

### 3 dòng đầu 概要欄

```
年金は60歳から受け取れます。ただし、その月から24％減り、減額は一生続きます。取り消しもできません。
この動画は、60歳・65歳・70歳で受け取る総額がどれだけ変わるのか、損と得の分かれ目は何歳なのかを、千葉県の松本さん（60歳・会社員）の見込み額で計算した研究記録です。
そして、損得の計算には出てこない「早くもらうと消える5つの権利」まで、日本年金機構の原典を見ながら確かめていきます。
```

### Mô tả đầy đủ

```
年金は60歳から受け取れます。ただし、その月から24％減り、減額は一生続きます。取り消しもできません。
この動画は、60歳・65歳・70歳で受け取る総額がどれだけ変わるのか、損と得の分かれ目は何歳なのかを、千葉県の松本さん（60歳・会社員）の見込み額で計算した研究記録です。
そして、損得の計算には出てこない「早くもらうと消える5つの権利」まで、日本年金機構の原典を見ながら確かめていきます。

──────────────
■ 目次
00:00 60歳の窓口で聞かれる一言
00:50 松本さん（60歳・千葉）のケース
01:55 三段の階段｜60歳・65歳・70歳でいくら違うか
04:00 損と得の分かれ目は「80歳10か月」
05:20 平均余命で見ると、差は思ったより小さい
07:05 早くもらうと消える5つの権利
10:20 では待てばいいのか｜加給年金という落とし穴
11:50 松本さんが決めた3つのこと
13:10 よくある誤解を2つ
13:45 今日の研究ノート＋今日からできること3つ
14:50 次回予告
──────────────

■ この動画で分かること
・60歳から受け取ると、ひと月あたり0.4％、最大24％減ること（昭和37年4月2日以後生まれの方の場合）
・その減額が一生続き、あとから取り消せないこと
・70歳まで待つと42％増えるが、その間の加給年金は受け取れないこと
・損と得の分かれ目の計算方法（ご自身の数字でも同じように出せます）
・繰上げ請求で「請求できなくなるもの」「選べなくなるもの」

■ 今日からできること
1. ねんきんネットまたはねんきん定期便で、65歳からの見込み額を紙に書き出す
2. その数字に0.76を掛ける（60歳から受け取った場合のおおよその額）
3. 治療中の病気・持病の有無と、配偶者が年下かどうかを、その紙に書き添える

■ ご注意
本動画は令和8年8月時点で公表されている制度・金額をもとに、当研究室が整理したものです。
金額や制度は改定されることがあります。また、実際の受給額・支給停止の有無は、加入記録やお勤めの状況によって一人ひとり異なります。
最終的なご判断の前に、必ずお近くの年金事務所、またはねんきんダイヤルでご確認ください。
特定の金融商品や投資をおすすめするものではありません。
登場する松本さんをはじめとするモニターの皆さまは、制度を分かりやすくお伝えするための架空の人物です。

■ 出典
日本年金機構「年金の繰上げ受給」「年金の繰下げ受給」「加給年金額と振替加算」「老齢基礎年金の受給要件・支給開始時期・年金額」
厚生労働省「令和6年簡易生命表の概況」

音声: VOICEVOX:雀松朱司

#年金 #老後のお金 #年金と老後のお金研究室 #繰上げ受給 #定年
```

### タグ

```
年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金, 65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金, 年金 60歳, 年金 65歳, 年金 何歳から, 繰上げ受給, 繰下げ受給, 年金 繰り上げ, 減額率, 損益分岐点, 加給年金, 障害年金, 遺族厚生年金, 高年齢雇用継続給付, 年金請求書, 定年退職, 60歳 定年, 老齢基礎年金, 老齢厚生年金, 日本年金機構, 平均余命, 年金事務所
```

### Pinned comment

```
今日の研究ノートです。
① 60歳から受け取ると、ひと月0.4％・最大24％減り、それが一生続きます
② 松本さんの場合、月18万円 → 月13万6,800円（差は月4万3,200円）
③ 損と得の分かれ目は、およそ80歳10か月
④ 繰上げ請求は取り消せず、事後重症などによる障害年金も請求できなくなります
⑤ 70歳まで待つと、待っている間の加給年金（松本さんの場合およそ212万円）は受け取れません

皆さまにお聞きしたいことがあります。
あなたは、何歳から受け取るおつもりですか。そして、その理由は「金額」ですか、それとも別のことですか。
差し支えない範囲で、コメントで教えてください。いただいたケースは、今後の「視聴者の実験室」の回で、匿名のまま計算させていただくことがあります。

※本動画は令和8年8月時点の情報です。実際の金額は加入記録によって異なりますので、最終的なご判断の前に年金事務所でご確認ください。
```

## Compliance quét nhanh (`youtube-compliance.md`)

| # | Mục | Kết quả |
|---|---|---|
| 1 | Từ tắt-ad ở title/thumbnail/概要 hiển thị (殺/血/死/破産…) | ✅ sạch. Có 「亡くなれば」 trong THÂN BÀI (bối cảnh tính 損益分岐点, không phải tiêu đề/thumbnail) — luật §0.1: chỉ quét ở title/thumbnail/3 dòng đầu |
| 2 | Cảnh AI realistic trong video | ✅ có ảnh AI (paper-collage) → **TICK "altered/synthetic content"** khi upload theo §2.1 (đảo chiều 2026-08-09) |
| 3 | Misleading | ✅ 月4万3千円・5つの権利・取り消せません đều có thật trong video |
| 4 | Tên thật người/công ty/thương hiệu | ✅ không có |
| 5 | Disclaimer YMYL + thời điểm | ✅ trong lời (第11章) + 概要欄 + pinned |
| 6 | Nhân vật hư cấu | ✅ ghi rõ trong 概要欄 |
| 7 | Credit giọng | ✅ 「音声: VOICEVOX:雀松朱司」 |

## 🎬 CHUẨN BỊ DỰNG — trạng thái 2026-08-30 (builder XONG, chờ 19 ảnh AI)

Video **ĐẦU TIÊN chạy quy trình Remotion chuẩn** (`CLAUDE.md` §②). Đã làm bước 1→3, 4, 6 (trừ asset AI), 7 (still 3 đỉnh + 2 bảng). Còn 5 (gen ảnh) và 8 (render).

### ⭐ 3 cải tiến đã cài (user chốt 2026-08-30 sau khi đọc `08_ANALYTICS_LOG` + benchmark)

| # | Cải tiến | Bằng chứng | Thi hành (trong `tools/build_remotion_18.py`) |
|---|---|---|---|
| ① | **Lớp ÂM THANH chuẩn kênh** | video 17 lên sóng **chỉ có giọng** (project.json 1 track audio) dù `channels.py` chốt BGM −40dB, `cta-midvideo.md` §5 bắt inject | track `trk-bgm` (Wholesome.mp3 đọc từ `channels.CHANNELS["nenkin"]["bgm"]`, vol 0,010) · `run_n18full.cmd` 3 bước: render → loudnorm −14 LUFS (chuỗi `VOICE_AF` chép từ `video_render.py`) → `cta_inject.py --lang jp` (srt từ `tools/timeline_to_srt.py`) |
| ② | **"Máy quay" ở 3 đỉnh bài** | video 12 rớt −30 điểm ở giây 20→30; đỉnh 1 bài này rơi 48s | `peak=<dòng>` → clip `video` zoom-punch trên chính hero (`hero_box` fit chiều cao) + SFX 1 chùm/đỉnh (`paper`/`thud`/`drop`, 3 chùm/15′ = đúng trần) + sticker `exit: fade` trước cú slam. Gate: peak phải có hero, không stat/formula |
| ③ | **Color coding 繰上げ=ĐỎ / 繰下げ=XANH** | りょう 970K: học màu 1 lần dùng cả bài | `KURIAGE/KURISAGE/BASE65` áp lên PUNCH · splash `sp` · formula `fcolor` · bảng `sandan`/`kimeta` per-row (**TextClip.tsx** nhận tiền tố `#rrggbb\|` — thêm mới, project cũ không đổi) |

Phụ: **lặp giảm** — sticker 50→25 lượt/16 file (max 3) · photocard 10→13 (không hero nào >3; `kakari_explain` 3 lần rải 392/490/581s).

### 🔴 Bài học lượt này — neo theo CHỈ SỐ DÒNG vỡ ngay khi lời bị sửa song song
`_TTS.md` được sửa (bởi phiên khác) trong lúc builder đang viết theo timeline 123 dòng → timeline mới 115 dòng, **mọi `L=` lệch**; builder crash `IndexError` (dòng 120 > 114). Đã neo lại tay toàn bộ SCENES/PUNCH/SFX (`scratchpad/reanchor18.py`). ⇒ Lần sau: **trước khi chạy builder, so `len(timeline.lines)` với số dòng builder đang giả định**; và đừng sửa `_TTS.md` khi builder đang được viết — hoặc báo nhau.

### ✅ 19 ảnh AI ĐÃ NHẬN + xử lý 2026-08-30 (Downloads/download · (1) · (2)) — builder ra **45/45 asset, 0 🔴**

- 13 photocard chọn từ lô B (00:57), riêng `kakari_explain` lấy 00[A] để cùng một cô nhân viên với `kakari`; cắt ✦ 1229 + soi 1:1 hai góc phải: sạch. 6 sticker magenta → `cutout_sticker.py --v18`: 0 vệt tím, ✦ bị lọc theo blob.
- Fix phát sinh: hero sticker `zoom-through` chồng với footage slam ở đỉnh L=3 (nền nhòe) → bỏ hero sticker khi peak rơi ngay đầu scene.

<details><summary>(cũ) danh sách 19 ảnh đã chờ</summary>

### 19 ảnh AI chờ user gen (tên đã khớp builder, KHÔNG đổi)
- **13 photocard** — `06_VIDEO/18_.../art_prompts_photocard18_FLOW.txt` (+`_BLOCKS.md`, `_TENFILE.txt`): `madoguchi · pen · kakari · matsumoto_counter · kenkyu · tsuri · matsumoto · tomato · kazoku · jikai · kakari_explain · madoguchi_close · matsumoto_home` → `make_photocard.py` (xoá ✦ cắt 1229) → `photocard/`
- **6 sticker** — `sticker_prompts_v18_FLOW.txt`: `magnifying_glass · house_bills · heart_pulse · medicine_bottle · percent_badge · signpost` (nền MAGENTA) → `cutout_sticker.py` → `sticker/`
- ✅ **4 原典 card đã xong bằng ảnh THẬT** (screenshot nenkin.go.jp, khoanh đỏ, `tools/ingest_genten_18.py`): `card_genten_01` (減額率 60歳=24%) · `02` (13 dòng, khoanh 3 & 11) · `03` (増額率 70歳=42%) · `03b` (注意点 dòng 1 加給年金)

</details>

### Render (điều kiện ĐÃ đạt: 0 dòng 🔴 THIẾU)
`cmd //c E:\Claude\Projects\remotion-vox\run_n18full.cmd` chạy **nền** → kiểm `out\n18full.log` có `RENDER_EXIT=0 · LOUDNORM_EXIT=0 · CTA_EXIT=0 · EXITCODE=0` · `ffprobe` duration ≈ 913,7s · `ebur128` I ≈ −14 LUFS · soi ≥10 still khi render ~10%.

**Slot đề xuất:** bộ ngày B — **T3 · T5 · CN 19:00 JST** (`upload-schedule.md` §0.9). Không phụ thuộc 支給日.
