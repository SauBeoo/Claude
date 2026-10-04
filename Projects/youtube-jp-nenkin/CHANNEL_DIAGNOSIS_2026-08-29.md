# KHÁM KÊNH nenkin 2026-08-29 — retention thấp: bệnh ở ĐÂU thật sự, và còn phải sửa gì

> Nguồn số: API (`06_VIDEO/_diagnose/out.txt` + `curves_2026-08-29.{txt,json}`, tool mới `pull_curves.py`) ·
> Studio đọc tay qua Chrome Profile nenkin (`06_VIDEO/_diagnose/studio_2026-08-29/*.jpg`) ·
> transcript 3 hit đối thủ (`06_VIDEO/_diagnose/rival_subs/*.vtt`).
> Đây là bản ĐÁNH GIÁ — chưa sửa gì trên kênh/script. Việc ghi lên kênh chờ user gật.

## 0. TÓM 5 DÒNG

1. **Vòi ĐÃ MỞ, bao bì ĐANG ĂN, khán giả ĐÚNG TỆP.** 28 ngày: **23,7K impressions · CTR 7,7%** · browse 91,8% · tuổi **65+ = 74,9% · 55–64 = 22,6%** · nam 88%. Video 15 vừa nổ lần 2 (158 → **1.116 view**, 98,7% browse). Ba thứ này KHÔNG phải bệnh — đừng đụng thumbnail/title/lịch để "chữa retention".
2. **Giả thuyết 08-20 ("sửa 50 giây đầu, cắm あなた @0:03") BỊ BÁC.** Video 15 chạy khuôn mở mới → relPerf@60s **0,14**, tệ nhất kênh (v12 khuôn cũ = 0,24). Cả 5 video có curve đều rơi **−30 điểm đúng ở giây 19→29** bất kể lời mở khác hẳn nhau ⇒ vách 20–30s **không nằm ở CHỮ cold open**. Studio còn ghi "52% ở giây 30 = như thông thường".
3. **Chỗ mất thật là PHÚT 1→3, và nó trùng đúng khối モニター kể chuyện.** 4 video có モニター vào ở giây 58–85 đều mất **13–22 điểm** trong 60→120s; video 09 (không モニター ở đó, đi thẳng 3 mục + 第一章 sự thật) **đứng phẳng 0,37→0,37** và relPerf leo 0,34→0,62. Đây là đối chứng NỘI KÊNH duy nhất, và nó chỉ đúng một chỗ.
4. **Studio đo AVD "bình thường" cho v15 = 3:51, mình = 2:32** (−1:19). Mốc cần đạt không phải "relPerf 0,4 ở 60s" nữa mà là **AVD ≥3:50 / AVP ≥27%**.
5. **Script 18 (chưa render) đang lặp y khuôn bị nghi:** モニター 松本さん vào **giây 18**, kể 釣り仲間・課長38年 tới phút 2. Đây là chỗ sửa rẻ nhất trước khi đốt một lượt render.

## 1. SỐ ĐO

### 1.1 Kênh (Studio, 1–28/08) — `studio_2026-08-29/channel_*.jpg`
| chỉ số | số | đọc |
|---|---|---|
| Views | 2,7K (28d) · 2.705 tổng | 2 cú nổ: v12 (08-17→19) và v15 (08-27→29) |
| Impressions | **23,7K** · 86,3% do YouTube đề xuất | vòi mở thật, không còn "0 tuyệt đối" |
| CTR | **7,7%** (v15 riêng: 5,4K imp · 6,4%) | tốt cho browse — bao bì không phải nút thắt |
| Traffic | browse **91,8%** · suggested 3,2% · search 2,7% | kênh sống bằng home feed, không phải search |
| AVD | 2:49 | |
| Khán giả | **65+ 74,9% · 55–64 22,6% · 45–54 2,5%** · nam 88% · JP 82% · mobile 49% / PC 47% | đúng tệp mục tiêu — bộ khuôn 45+ bắn đúng đích |
| Người xem mới | 99,6% | chưa có tệp quay lại; sub +6 |
| ⚠️ v15: 1,1K view / **235 người xem riêng biệt** | ≈4,7 view/người | bất thường — xem §3.4 |

### 1.2 Curve retention 0–100% (API, đo 08-29) — `curves_2026-08-29.txt`
awr = % còn xem · relPerf = phân vị so video cùng độ dài (0,5 = trung bình)

| video | khuôn mở | 9–10s | **19–20s** | **29–30s** | 60s | 120s | 180s | relPerf@60 | AVP | AVD |
|---|---|---|---|---|---|---|---|---|---|---|
| 09 公金受取口座 (search) | あなた @0s, 3 mục @56s, KHÔNG モニター | — | (15s 0,80) | 0,59 | **0,37** | **0,37** | 0,34 | 0,34 | 20,2% | 5:07 |
| 12 住民税の紙 (1.457v) | ngụ ngôn 2 nhà, 田中 @77s | 0,93 | 0,93 | **0,61** | 0,41 | 0,28 | 0,26 | 0,24 | 16,0% | 2:38 |
| 13 遺族年金 (49v) | 佐藤 sớm | 0,94 | 0,80 | 0,59 | 0,55 | 0,35 | 0,33 | 0,23 | 27,5% | 4:40 |
| 14 非課税148万 (77v) | 中村 @0s (bàn bếp 2 phong bì) | 0,91 | 0,84 | 0,68 | 0,47 | 0,31 | 0,32 | 0,18 | 21,6% | 3:33 |
| **15 10月振込 (1.116v)** | **あなた @3s · stake @3s (khuôn MỚI)**, 中村 @61s | 0,94 | 0,93 | **0,61** | 0,48 | 0,26 | 0,24 | **0,14** | 17,1% | 2:32 |

Đọc:
- **Vách 19→29s: −30 ±3 điểm ở 12 · 15; −20 ở 13; −16 ở 14; −21 ở 09.** Có ở mọi video, bất kể mở bằng あなた hay モニター hay ngụ ngôn. ⇒ **không phải biến "chữ cold open"**. relPerf ở giây 9 đã chỉ 0,25–0,28 (đáy phân vị) khi awr còn 0,93 — tức mọi video cùng độ dài trên YouTube giữ được ~0,97 ở giây 9, mình rớt sớm hơn họ vài điểm ngay từ đầu.
- **60→120s:** 12 −13 · 13 −20 · 14 −16 · **15 −22** · **09 ±0**. Bốn video mất là bốn video đưa モニター + chi tiết đời (農協 記帳「ジジ、ジジ」, 台所のテーブル, 再雇用 週5日) vào đúng cửa sổ này. Video 09 ở cùng cửa sổ đọc **3 mục sẽ trả lời + 「では、第一章。まず、事実から」** → phẳng tuyệt đối.
- **Cuối bài relPerf leo 0,4–0,8** = người ở lại đến cuối là người thích — thân bài từ phút 4 không phải bệnh (kết luận 08-20 vẫn đứng ở đoạn này).

### 1.3 Đối thủ — 60s đầu của 3 hit (transcript, `rival_subs/`)
| hit | view | 0–20s | 20–45s | 45–75s |
|---|---|---|---|---|
| フクロウ 8月封筒 | 1,39M | **mệnh lệnh** 「この封筒、絶対に捨てないでください」+ hậu quả 自動登録 | 「そんなこと本当にあるの？…と今思いませんでしたか」→ **対象** 「今年金を受け取っている方」 + 期限 | **lộ trình 3 câu** 「今回の動画では①正体②何が変わる③手続き」+ **open-loop** 「後半で落とし穴」 |
| フクロウ 年金通知書 | 1,36M | thông báo sắp tới + 「放置すると見逃す」 | 「国は教えてくれません」 → 「こんにちは、ふくろうです」@33s | **hứa kết quả** 「最後まで見れば…理解できます」@58s |
| お金の保健室 請求書3パターン | 37K (kênh 2,7K sub) | 「3つのパターンの方だけ」+ phản bác định kiến 65歳 | **đối thoại 2 giọng** hỏi–đáp nhanh, số 63歳/女性 | 「まず今年ご自分に届くのか、ここから確かめます」 |

Cả 3: **không nhân vật hư cấu, không chi tiết đời, không 間 dài**; tới giây ~60 người xem đã biết ① nó nói về mình ② sẽ được gì ③ bài có mấy phần. Của mình ở giây 60: v15 「こんにちは、研究室です。新潟県上越市の、中村さん。71歳、おひとり暮らしです。」 — người xem chưa biết bài có mấy phần, đang được kể về một người lạ.

## 2. PHÁN QUYẾT GIẢ THUYẾT 08-20

| giả thuyết 08-20 | phán quyết | bằng chứng |
|---|---|---|
| "Vách 20–50s do cold open ngôi thứ ba, thiếu あなた" | ❌ **BÁC** | v15 có あなた @3s + stake @3s → vách y hệt (0,93→0,61), relPerf@60 0,14 < 0,24 của v12 |
| "Thân bài khoẻ, chỉ sửa 50s đầu là xong" | 🟡 **nửa đúng** | thân bài từ phút 4 khoẻ (relPerf 0,4–0,8), nhưng **phút 1–3 mất thêm 15–22 điểm** — 08-20 chỉ nhìn tới 60s |
| "Video 09 tốt hơn vì あなた + deadline @21s" | 🟡 **đổi cách đọc** | 09 KHÔNG tốt hơn ở 30s (0,59 ≈ 12/13); nó tốt hơn ở **60→180s** (phẳng) — vì đoạn đó là lộ trình + sự thật, không phải モニター |
| Gate G6/G7/G8 (`check_pace.py`) | ⚠️ đang đo **biến không quyết định** | v15 PASS 8/8 gate mà retention tệ nhất — đúng `feedback_gate_pass_khong_phai_retention` lần thứ hai |

## 3. NGUYÊN NHÂN — tách ĐO ĐƯỢC / SUY RA

### 3.1 ĐO ĐƯỢC
- (a) Vách 19→29s tồn tại ở **mọi** video, độc lập với lời mở. Studio gọi mức 52% @30s là "như thông thường".
- (b) Video có モニター trong 60–120s mất 13–22 điểm; video không có → phẳng. n=5, 1 đối chứng — **tín hiệu mạnh nhất có được**, chưa phải nhân quả.
- (c) AVD mình 2:32–2:38 vs "bình thường" Studio 3:51 cho cùng video ⇒ thiếu **~80 giây/người**.
- (d) Bao bì, phân phối, tệp tuổi: đều đạt (§1.1).

### 3.2 SUY RA (chưa đo được, xếp theo độ tin)
1. **Khối モニター kể chuyện là chỗ mất phút 2** — người xem 65+ bấm vì「10月15日 −1万6千円」muốn biết *mình* bị trừ bao nhiêu; giây 61 lại nghe về ông 中村 ở 上越市 đi 農協 記帳. Khuôn `humanize` (6 mũi tiêm) + cast モニター cố định là **bản sắc kênh** nhưng đang đặt **sai chỗ**: đối thủ 1,3M view không có lớp này trong 2 phút đầu. Giữ cast, **dời xuống sau khi trả câu hỏi chính** (đối thủ お金の保健室 dùng đối thoại hỏi–đáp, không dùng tiểu sử).
2. **Vách 20–30s có thể là lớp "dựng" chứ không phải chữ:** cùng giọng VOICEVOX 雀松朱司 0,9 + thẻ chữ `make_stage`/2 cast tĩnh ở mọi video; v15 đúng giây 19–30 là thẻ `pict` 「役所の間違いでも、詐欺でもありません」 (một câu PHỦ ĐỊNH nỗi lo — làm xẹp lý do ở lại). Không kiểm được bằng số hiện có; cách kiểm rẻ: video 18 dựng Remotion (hình khác hẳn) — nếu vách 20–30s **vẫn** −30 thì thủ phạm còn lại là giọng/nhịp TTS.
3. **Tốc độ nạp thông tin thấp:** 3 hit đối thủ nói xong 対象 + stake + lộ trình + open-loop trong 60–75s; mình dùng 56s cho hook rồi mới chào, tới 85s vẫn chưa nói bài có mấy phần. `[間0.8][速0.82]` rải ở 4–5 câu đầu làm 60s đầu chở ít chữ hơn.

### 3.3 Không phải nguyên nhân (đã loại)
- Thumbnail/title/khuôn TELOP (CTR 7,7%) · lịch/giờ · tệp tuổi lệch · category (chỉ 09/11 sai cat 22, không liên quan retention) · độ dài (14–17′ đúng dải 13–17′ đối thủ).

### 3.4 ⚠️ Bất thường phải ghi: 1.116 view / 235 người xem riêng biệt (v15)
4,7 view/người trên traffic browse là cao bất thường (thường 1,1–1,5). Hai cách đọc: người 65+ xem lại nhiều lần (tốt) — hoặc **autoplay/preview trên home feed tính thành view**, tức 1.116 "view" chỉ tương đương ~235 lượt xem có chủ đích. Nếu là cách sau, nó **giải thích luôn vách 20–30s ở mọi video** (người không bấm chủ động bỏ ở ~20s) và làm "Studio: 52% @30s là thông thường" thành hợp lý. ⏳ Kiểm: Studio → v12 → Reach → "Số người xem riêng biệt" (trang không load lượt này). Nếu v12 cũng ~4–5×, chuyển cách đo retention sang **AVD của người ở lại >30s**, đừng chữa vách 20s.


### 3.5 ⭐ KIỂM "ĐỀ XUẤT SAI TỆP" (user hỏi 08-30) — ĐÚNG MỘT NỬA, và nửa đó giải thích được vách 20–30s

**Nhân khẩu học ĐÚNG** (API theo video): JP **100%** (Studio hiện 82% vì phần "không xác định") · v12: 65+ nam 59,4% · 55–64 nam 22,5% · 65+ nữ 9% · v15: 65+ nam 100% (mẫu Analytics 167). Không có tệp trẻ, không có nước ngoài.

**Nhưng SỞ THÍCH SAI.** Tra 24 video đang dẫn người sang kênh mình (`insightTrafficSourceDetail` RELATED, cả kênh):

| nhóm | video dẫn | số |
|---|---|---|
| cùng ngách tiền hưu | 失業保険不正受給 · 65歳で「この金額」貯めている · 年金と暮らし 74歳 · あゆみ 年金/公金受取口座 · 2ch シニア再雇用 | **5/24** |
| giải trí nam cao tuổi | プロ野球 ×3 · SKE48 · 麻雀 · BreakingDown · 漁師メシ · 高校野球 | 9 |
| drama/不倫/歌舞伎町/ラブホ/ナース | リセットボタン · アンマスク · リーガル探偵 · 鶯谷ラブホ · ぶーちゃんねる · ジャックポット · さきっちょナース | 7 |
| khác (副業 Claude Code · 人生相談 · シニア漫画 · メンバー動画) | | 3 |

⇒ YouTube đang xếp kênh vào **"feed đàn ông 65+ nói chung"** (biết TUỔI+GIỚI, chưa biết CHỦ ĐỀ). Home feed `what-to-watch` = 1.647/1.654 view của bucket SUBSCRIBER cũng là cùng cơ chế. Khớp với: **CTR cao (7,7%)** — số tiền trên thumbnail hút bất kỳ ông 65+ nào — rồi **rơi −30 điểm ở giây 20–30** khi người ta nhận ra "không phải thứ tôi hay xem", **4,7 view/người** (cùng một pool nhỏ bị đẩy lại nhiều lần), và **AVD mobile 131s < desktop 200s** (feed điện thoại = lướt).

**Vì sao YouTube chưa biết chủ đề:** kênh 6 sub, 0% view từ subscriber thật, search chỉ 57 view/6 tuần, RELATED trong ngách chỉ 5 lượt ⇒ **không có tín hiệu "người xem 年金 xem kênh này"**. Tín hiệu duy nhất YouTube có là nhân khẩu học của người bấm thumbnail.

**Hệ quả cho cách đọc retention:** vách 20–30s **phần lớn là khán giả sai sở thích bỏ đi** — sửa script không kéo lại được nhóm này; và đây là lý do khuôn mở mới (v15) không đổi được gì. Phần mất **phút 1→3 (モニター)** thì vẫn là lỗi của mình, vì người còn ở lại sau 30s đã là người có quan tâm.

**Đề xuất — dạy YouTube CHỦ ĐỀ, bằng tín hiệu nó đọc được:**
1. **Kéo view từ ĐÚNG hàng xóm** (`youtube-suggested-growth.md` §1): 5 video cùng ngách đang dẫn view là 5 hàng xóm thật → title/thumbnail video 18+ nói cùng ngôn ngữ với **あゆみ / フクロウ / 年金と暮らし** (「◯月に届く◯◯」「放置すると自動登録」), không phải 【見逃し厳禁】 chung chung — tag đầu đó đang bắt cả feed drama.
2. **Search làm mỏ neo chủ đề:** 57 view search toàn từ khoá đúng ngách (公金受取口座 ×10, 年金支給日, 特別支給の老齢厚生年金) và AVD search 203s > browse 159s. Mỗi video bắt buộc có **1 keyword đo được đứng đầu title** (§0.5 SEO) — v12/v14/v15/v16 hiện mở bằng 【見逃し厳禁】, keyword đứng thứ 2.
3. **Giữ người xem trong kênh** để YouTube thấy chuỗi 年金→年金: end screen trỏ video cùng cụm (END_SCREEN cả đời kênh = **1 view**), 1 playlist duy nhất 16 video → tách **3 playlist theo trụ** (年金の計算 / 給付金・届く紙 / 税・保険料) và pin comment link video kế. Chi phí ~0.
4. **Sửa lệch nhỏ:** channel description ghi 「毎週 月・水・金 19時」 nhưng lịch thật T3·T5·CN → sửa (cú ghi lên kênh, chờ gật).
5. **Không làm:** đổi thumbnail để "hút đúng người hơn" khi CTR 7,7% — bao bì không phải chỗ hỏng; và **không** tăng nhịp: đẩy thêm video vào feed sai sở thích là thêm mẫu AVD 2:30 vào điểm kênh.

⏳ Đo lại 2026-09-05 bằng `insightTrafficSourceDetail` RELATED: tỉ lệ video dẫn **cùng ngách** phải tăng từ 5/24 — đó là thước đo "YouTube đã hiểu chủ đề", không phải view.

## 4. ĐỀ XUẤT — xếp theo chi phí/độ tin

### 4.1 Áp NGAY cho video 18 (chưa render — sửa script rẻ hơn sửa video) — cần user gật vì đụng script
1. **Dời khối モニター 松本さん ra khỏi 0–120s.** Hiện: 松本 @18s, 釣り仲間 @93s, 課長38年 @116s. Thay bằng khuôn 09/đối thủ: 0–20s あなた + 4万3千円 (đã có) → 20–45s **đối tượng + phản bác định kiến** (「早くもらったほうが得」は…) → 45–75s **lộ trình 3 số sẽ tính + open-loop câu hỏi 通院** → 「まず、事実から」. 松本さん vào ở mục tính số đầu tiên (~phút 2,5–3) với **≤1 chi tiết đời**.
2. **Cắt `[間]`/`[速0.8x]` trong 75s đầu** xuống ≤2 tag (giữ 1 [間] trước con số) — nhịp đầu phải dày chữ như đối thủ; lớp humanize dồn về phút 3+.
3. **Thẻ 20–30s KHÔNG được là câu phủ định/nhượng bộ** (kiểu 「詐欺ではありません」「去年までは正しかった」) — đặt câu **mở rộng hậu quả** hoặc con số thứ hai.
4. Sau khi 18 lên sóng 5–7 ngày: so **60→120s** với v15 (−22) và **AVD với 3:51**. Đây là phép đo A/B thật đầu tiên cho giả thuyết モニター.

### 4.2 Đổi GATE (việc của tao, làm khi user gật — không đụng kênh)
- `check_pace.py` thêm **G9: không tên モニター trong 0–120s** (trừ khi bài là hồ sơ nhân vật) và **G10: ≤2 tag 間/速 trong 75s đầu**; **G11: có câu lộ trình (「三つ」「まず」「今日は…を確かめます」) trước 75s**. Gỡ kỳ vọng "G6–G8 chữa retention" khỏi docstring.
- Mốc đọc mới ghi vào `08_ANALYTICS_LOG.md`: **AVD ≥3:50 · awr@120s ≥0,40** (v09 mức 0,37 là sàn), thay cho relPerf@60s.

### 4.3 Việc user QUYẾT
| việc | số để quyết | khuyến nghị của tao |
|---|---|---|
| Nhịp đăng (treo từ 08-20) | 2 cú nổ/9 video; browse 92%; sub +6; **RELATED chỉ 3,2%** → chưa đạt điều kiện "đang được đề xuất" của `upload-schedule.md` §0.9 | **Giữ 3/tuần**, dồn công vào sửa phút 1–3. Lên 1/ngày lúc AVD còn 2:32 = bơm thêm mẫu retention đáy vào điểm kênh |
| Trailer kênh = v12 (AVP 16%) | người xem mới 99,6% | Đổi sang v13 (AVP 27,5%, AVD 4:40) — rẻ, chờ gật |
| Bản sắc cast モニター | đối thủ 1,3M không có; mình mất 13–22 điểm đúng chỗ đặt nó | **Giữ cast nhưng dời sau phút 3**, không bỏ |

### 4.4 Ghi lên kênh (chờ gật từng cái — `feedback_chot_truoc_khi_dang`)
- v09 + v11 **categoryId 22 → 27** (`videos.update`).
- v01/02/04 thiếu 「音声: VOICEVOX:雀松朱司」 trong 概要欄 (license) — treo từ 08-20.
- Title: **7/9 video gần nhất mở bằng `【見逃し厳禁】`** → trang kênh nhìn như một khuôn; đối thủ フクロウ đổi tag đầu mỗi video (期限切れ注意 / 6月中に確認 / 50歳以上必見 / 申請忘れ続出). Không đổi title đang test thumbnail; áp cho video 18+ (A2/A3 trong bộ 3 title).
- v15 suggested-from list có video rác không liên quan (母「早く入れて❤️」, 鶯谷ホテル) — chỉ 1,3% traffic, ghi để theo dõi, không làm gì.

## 5. MỐC ĐỌC LẠI
- **2026-09-05**: v18 đủ 5 ngày → so 60→120s và AVD với bảng §1.2. Cùng lượt kiểm §3.4 (unique viewers v12).
- Nếu v18 (Remotion + dời モニター) **vẫn** rơi −30 ở 20→30s → nghi giọng TTS: render demo 60s đầu bằng giọng khác (hoặc speed 1,0) để user nghe so.
- Tool: `python 06_VIDEO/_diagnose/pull_curves.py` (curve 0–100% mọi video ≥20 view) — chạy thay `diagnose_channel.py` khi cần full curve.
