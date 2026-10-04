# 年金と老後のお金研究室 — KHÁM KÊNH (2026-07-28)

> Đo bằng YouTube Data API + YouTube Analytics API (token `credentials/token.json`, có `yt-analytics.readonly`)
> + quét public API 3 kênh benchmark cùng ngách. Tool: **`tools/diagnose_channel.py`** (chạy lại 1 lệnh), dữ liệu thô `06_VIDEO/_diagnose/out.txt`.
> Cùng khuôn với mổ health `youtube-jp-health/CHANNEL_DIAGNOSIS_2026-07-27.md` để so chéo được.

## 0. TÓM TẮT 6 DÒNG

1. Kênh **8 ngày tuổi** (lập 2026-07-20), **4 video, 7 view tổng, 0 sub**. Đây là cold-start, **KHÔNG phải bị đánh**.
2. **Không có án phạt, không bị deindex:** 4/4 video `public`, index search bình thường — video #4 **hạng 1** cho long-tail 「60歳 即退職 老後資金 700万円」, video #3 **hạng 2** cho 「年金生活者支援給付金 申請 消える」.
3. Metadata cấp video **sạch**: `defaultLanguage=ja` + `defaultAudioLanguage=ja` · phụ đề tự tải lên (2 track/video) · thumbnail `maxres` · **categoryId 27 khớp benchmark 23/24 video** · 27–32 tag · trailer đã đặt · channel keywords 143 ký.
4. **Chưa có 1 view nào từ browse (trang chủ) hay suggested (related).** Traffic chỉ: `YT_CHANNEL` 2 · `SUBSCRIBER` 2 · `YT_SEARCH` 1. → YouTube **chưa đưa kênh vào rail đề xuất**.
5. 🔴 **Phát hiện nặng nhất — LỆCH FORMAT NGÁCH ở 2 điểm đo được:** độ dài video **bằng NỬA** chuẩn ngách, và title **không dùng 【】** trong khi 51/52 video benchmark đều dùng.
6. ✅ **ĐÃ ĐỌC STUDIO (bổ sung cùng ngày, Chrome profile Default): impressions = 50 · CTR = 6,0%.** → Không phải "phát mà không ai bấm". **YouTube gần như CHƯA PHÁT kênh này cho ai.** Chi tiết §1.2 — đây là câu trả lời cho câu hỏi bỏ ngỏ ở §5.

---

## 1. SỐ THẬT CỦA KÊNH

| | |
|---|---|
| Lập kênh | 2026-07-20 (8 ngày) |
| sub / video / view | **0 / 4 / 7** |
| country / defaultLanguage (cấp KÊNH) | JP / **`en`** ⚠️ nên là `ja` |
| trailer | ✅ đã đặt |
| channel keywords | 143 ký (đủ) |

### 1.1 Bốn video đã đăng

| # | Đăng (JST) | Ngày | Dài | view | Title |
|---|---|---|---|---|---|
| 1 | 07-20 **16:44** | T2 | 13'30 | 3 | 在職老齢年金が4月から激変｜65万円まで年金カットゼロ… |
| 2 | 07-22 19:00 | T4 | 15'39 | 2 | 年金の繰り下げ受給、70歳まで待つと本当に得?… |
| 3 | 07-25 19:00 | T7 | 15'16 | **0** | 年金生活者支援給付金、申請しないと消えるお金｜… |
| 4 | 07-28 19:00 | T3 | 20'19 | 1 | 【2年はやめないで】60歳の即退職で老後資金が約700万円減るワケ｜… |

### 1.2 ⭐ SỐ TỪ YOUTUBE STUDIO — impressions & CTR (đọc trực tiếp 2026-07-28, khung 28 ngày 30/6–27/7)

> Nguồn: Studio → Số liệu phân tích → **Nội dung** + **Chế độ nâng cao** (bảng theo video).
> Đây là số **API không cấp được** (`Unknown identifier (impressions)`), phải mở browser mới có.

| Video | Dài | view | Thời gian xem (giờ) | **Impressions** | **CTR** |
|---|---|---|---|---|---|
| 在職老齢年金 | 13'30 | 3 | 0,3 | **23** | **8,7%** |
| 年金生活者支援給付金 | 15'16 | 2 | 0,5 | **14** | **7,1%** |
| 年金の繰り下げ受給 | 15'39 | 2 | 0,3 | **6** | 0% |
| **TỔNG KÊNH** | — | **7** | **1,1** | **50** | **6,0%** |

- Thời lượng xem TB toàn kênh **9:04** · từ impressions **10:35** · tổng thời gian xem từ impressions **0,53 giờ**.
- Nguồn view: **Duyệt xem (browse) 42,9% · Trang kênh 42,9% · Search 14,3% · Video đề xuất (suggested) 0,0%**.

### 🔴 KẾT LUẬN ĐỔI SAU KHI CÓ SỐ NÀY

**Câu hỏi "chưa được phát" hay "phát mà không ai bấm" → trả lời được: CHƯA ĐƯỢC PHÁT.**

1. **50 impressions / 28 ngày / 4 video. Video nhiều nhất được 23 lần hiển thị.** Đây không phải "phân phối kém" — đây là **chưa hề có cuộc thử nghiệm nào**.
   - Đối chiếu health cùng workspace: health được **~18.600 impressions** (một video 5.500) rồi mới bị tắt vòi. nenkin: **23**.
   - Hai kênh 0-view nhưng **hai bệnh khác nhau hoàn toàn**: health = *đã được phát, retention đáy → bị đóng vòi*. nenkin = *chưa được phát*.
2. **CTR KHÔNG phải bệnh.** 8,7% và 7,1% đều **trên** mốc ngách 4–6%. ⚠️ Nhưng n=23 và n=14 → **vô nghĩa thống kê**, không được lấy làm bằng chứng "thumbnail tốt". Điều đọc được đúng mức: *chưa có dấu hiệu thumbnail là vấn đề*.
3. **Suggested = 0,0%.** Chưa vào rail đề xuất lần nào — bình thường với kênh 8 ngày/0 sub, nhưng đó là nơi 完全攻略 ăn 3,84M.
4. **AVD 9:04 trên video ~15′ ≈ 58–60% AVP** — con số này nếu giữ được khi có mẫu thật thì là **khỏe**. Nhưng 7 view (phần lớn là view chính chủ) ⇒ chưa kết luận gì. Đây là chỗ tuyệt đối không được tự khen.

**Hệ quả cho hành động:** vì bệnh là *chưa được phát*, mọi công đổ vào **sửa thumbnail là đổ vào không khí** (giống kết luận health nhưng vì lý do khác). Đường ra khỏi cold-start chỉ có 2 cửa:
- **Cửa 1 — SEARCH (tự chủ được):** đề tài phải có **cầu tìm kiếm thật**. nenkin đang hạng 1–2 cho long-tail của mình, nhưng đó là long-tail **volume bé**. → chọn đề theo trend đo được, không chọn theo cảm giác.
- **Cửa 2 — BROWSE/SUGGESTED (phải được YouTube mời):** cần watch-time/impression đủ cao để YouTube mở thêm. Đây đúng là chỗ **độ dài 15′ vs 26–37′ của ngách** làm mình tự bó tay: cùng CTR, video 30′ trả về gấp đôi phút xem trên mỗi lần hiển thị.

---

**Đọc:** 4 video/8 ngày = **3,5 video/tuần** — cao hơn trần 2/tuần đang ghi trong luật. Ngày rải **T2·T4·T7·T3** (không nhịp), video #1 lệch giờ (16:44 thay vì 19:00). AVP của 2 video có view là 42,8% và 52,5% — **nhưng chỉ 2–3 view, phần lớn là view của chính chủ → con số này KHÔNG có nghĩa thống kê.**

---

## 2. 🔴 LỆCH FORMAT NGÁCH — chỗ đắt nhất

Đo 3 kênh benchmark (public API, 12–20 video mới nhất mỗi kênh):

| Kênh | sub | Độ dài (median) | Title mở bằng 【】 |
|---|---|---|---|
| 年金・給付金完全攻略 | 132K | 25,9–59,5′ (**~36′**) | **12/12** |
| シニアの年金・給付金速報 | 114K | 25–92′ (**37,5′**) | **19/20** |
| 節約看護師りょう | 748K | 17–41′ (**26,0′**) | **20/20** |
| **nenkin (mình)** | 0 | **13,5–20,3′ (15,5′)** | **1/4** |

1. **Độ dài bằng nửa chuẩn ngách.** Không kênh benchmark nào có video dưới 17′; median cả 3 đều 26–37′. Hit 3,84M của 完全攻略 dài 25,2′, hit 1,05M dài 36,4′.
   → Cơ chế **có thể** giải thích (chưa kiểm chứng trên kênh này): rail suggested xếp theo watch-time/impression; cùng một AVP thì video 30′ trả về gấp đôi phút xem của video 15′. Ngách này người xem đang **tra một chế độ** nên chịu ngồi lâu.
2. **Title không có 【】.** 51/52 video benchmark mở bằng 【】 (【政府は絶対言わない！】【50歳以上必見】【緊急解説】). nenkin dùng dấu `｜` phân đoạn. Health cũng vừa bị bắt đúng lỗi này (`youtube-jp-health/CHANNEL_DIAGNOSIS_2026-07-27.md`) — **2 kênh cùng lặp một lỗi** ⇒ là lỗi khuôn, không phải lỗi lẻ.

> ⚠️ Cả hai đều là **tương quan đo được**, chưa phải nhân quả đã kiểm chứng: mẫu benchmark nhỏ, và các kênh đó còn hơn nenkin ở mọi thứ khác (tuổi kênh, sub, tệp có sẵn). Cách kiểm: sửa **1 biến/lần**, đo lại.

---

## 3. CÚ COLD-START CỦA KÊNH THẮNG — dùng để đặt kỳ vọng

`年金・給付金完全攻略` lập **2026-03-21**, sau 4 tháng → **132.000 sub / 5,95M view / chỉ 12 video**:

| # | Ngày | Cách video trước | Dài | view |
|---|---|---|---|---|
| 1 | 03-21 14:51 T7 | — (ngày lập kênh) | 25,9′ | 4.799 |
| 2 | 03-28 08:49 T7 | 7 ngày | 28,6′ | 12.000 |
| 3 | 04-03 23:42 T6 | 6 ngày | 25,2′ | **3.841.951** 🔥 |
| 4 | 04-15 05:11 T4 | 12 ngày | 30,5′ | 20.482 |
| 5 | 04-22 22:19 T4 | 7 ngày | 36,7′ | 86.046 |
| 6 | 05-01 03:32 T6 | 9 ngày | 36,4′ | **1.050.871** |
| 7 | 05-08 08:51 T6 | 7 ngày | 30,2′ | 29.620 |
| 8 | 05-15 19:26 T6 | 7 ngày | 45,9′ | **433.779** |
| 9 | 05-24 15:07 CN | 9 ngày | 40,6′ | 32.953 |
| 10 | 06-02 10:59 T3 | 9 ngày | 46,8′ | 244.598 |
| 11 | 06-28 12:51 CN | 26 ngày | 37,6′ | 6.597 |
| 12 | 07-21 14:56 T3 | 23 ngày | 59,5′ | 190.640 |

**Bốn điều đọc được:**
1. **Nhịp lúc ramp = ~1 video/tuần** (7–12 ngày), không phải 2–4/tuần. Sau khi có tệp mới giãn ra 23–26 ngày.
2. **Hit đến ở video #3, ngày thứ 13.** Video #1–2 chỉ 4,8K và 12K → 2 video đầu ít view là BÌNH THƯỜNG, kể cả với kênh sau này ăn 3,84M.
3. **Hit rate ~4/12** (≥190K view) — phần lớn video vẫn 6K–33K. Đây là ngách "trúng thì trúng lớn", không phải ngách đều đều.
4. 🔴 **GIỜ ĐĂNG CỦA WINNER RẢI BỪA: 03:32 · 05:11 · 08:49 · 12:51 · 14:51 · 14:56 · 15:07 · 19:26 · 22:19 · 23:42.** Kênh 132K sub **không có giờ cố định nào** mà vẫn ăn 3,84M.
   → **Giờ/ngày đăng KHÔNG phải cái mở vòi phân phối ở ngách này.** Nó là chuyện thói quen khán giả (đáng giữ ổn định), nhưng đừng trông nó chữa 0-view. Đây là điều chỉnh thẳng vào giả định cũ trong `.claude/rules/upload-schedule.md`.

---

## 4. LỊCH ĐĂNG — CHỐT LẠI (trả lời trực tiếp câu hỏi)

**Nói thẳng trước: lịch đăng KHÔNG phải thứ đang chặn phân phối của kênh này.** Bằng chứng ở §3.4 (winner đăng giờ bừa vẫn 3,84M). Thứ tự ưu tiên thật: **① độ dài 25–40′ ② title 【】 ③ đề tài mega-evergreen** rồi mới tới lịch. Nhưng lịch vẫn phải sửa, vì cái đang chạy sai theo hướng ngược:

| | Trước | **Sau (chốt 2026-07-28)** |
|---|---|---|
| Nhịp | 2/tuần (T3·T6) — thực tế đã đăng **3,5/tuần** | **1 video/tuần** |
| Ngày | T3 + T6 | **T6 cố định** (T3 = slot phụ có điều kiện) |
| Giờ | 19:00 JST | **19:00 JST — GIỮ NGUYÊN** |

**Vì sao hạ xuống 1/tuần:**
1. Winner lúc ramp chạy **~1 video/tuần** (7–12 ngày/video) và ăn hit ở video #3. Không có tiền lệ nào trong ngách thắng bằng volume — 給付金チャンネル 1.971 video chỉ 87K sub, kém 完全攻略 **27 lần hiệu suất/video** (`CHANNEL_BENCHMARK_2026-07-25.md`).
2. **Độ dài phải tăng gấp đôi** (15,5′ → 25–40′) ⇒ công/video tăng gấp đôi. Giữ 2/tuần = chắc chắn phải hạ chất hoặc bỏ slot.
3. 4 video đầu đã đăng dày (3,5/tuần) mà vẫn 0 browse/suggested ⇒ thêm volume không phải đòn mở vòi.

**T3 = slot phụ, CHỈ bật khi:**
- Video trục **支給日** (給付金/年金生活/いくらもらえる) cần đăng **1–3 ngày trước ngày 15 tháng chẵn** — mốc kế tiếp **14/08/2026 (T6)** → dùng **T3 11/08**. Với lịch chỉ-T6 thì T6 gần nhất trước đó là 07/08 (sớm 7 ngày, ngoài cửa sổ) ⇒ **T3 tồn tại là để phục vụ đúng việc này**.
- Hoặc tin chính sách nóng cần ra trong tuần.
- Ngoài 2 trường hợp trên: **để trống T3**, đừng lấp cho đủ số.

**Vì sao chọn T6 làm slot cố định** (bằng chứng, kèm giới hạn):
- 完全攻略: **4/12 video đăng T6**, và **2 hit lớn nhất đều T6** (3,84M · 1,05M); median view ngày T6 = 742K.
- Cả cụm tiền-senior JP khóa T6: 節約看護師りょう **T6 = 48/50 video** (median 106K view/video); みんなの給付金 long-form **chỉ T3+T6**.
- ⚠️ **Giới hạn:** 4 mẫu, và 2 hit đó là **đề tài mega-evergreen** (定期便に載らない年金 · 年金通知書の読み方) — rất có thể đề tài quyết định, không phải thứ Sáu. Đây là tương quan, đừng đọc thành nhân quả.

---

## 5. VIỆC CÒN MỞ — chưa làm được bằng API

1. ✅ **ĐÃ GIẢI QUYẾT cùng ngày:** `impressions`/CTR không có trong Analytics API (`Unknown identifier (impressions)`) → **đã đọc trực tiếp từ Studio bằng browser** (user để sẵn Chrome Default đăng nhập kênh nenkin). Kết quả + kết luận: **§1.2**. Đáp án: **chưa được phát (50 impressions), CTR không phải bệnh.**
   - **Cách lấy lại lần sau:** Studio → 「Số liệu phân tích」 → tab **Nội dung** (4 ô: view · Lượt hiển thị hình thu nhỏ · CTR · Thời lượng xem TB) → **Chế độ nâng cao** để có bảng theo từng video. URL đi thẳng: `studio.youtube.com/channel/UC3MOM94mNkKzlp-9Sxz91bA/analytics/tab-content/period-default`.
   - ⚠️ Ghi lại lệch tài liệu: `.claude/rules/channel-browser.md` map nenkin ↔ `Profile 17`, nhưng lần đo này chạy trên **Default** (user chủ động để sẵn). Nếu chốt dùng Default lâu dài thì phải sửa mapping, không thì lần sau mở sai profile.
2. **Retention chưa đo được** — 7 view thì YouTube không trả `audienceWatchRatio`/`relativeRetentionPerformance`. Ngưỡng cần theo dõi khi có ≥50–100 view/video: **relPerf@60s ≥ 0,40** (health chết ở 0,10–0,14).
3. ✅ **ĐÃ SỬA 2026-08-01:** `defaultLanguage` cấp KÊNH `en` → `ja` (channels.update part `brandingSettings`, user gật qua plan; verify title/country/description giữ nguyên). Ghi sổ: `08_ANALYTICS_LOG.md` block 2026-08-01.

## 6. VIỆC KHÔNG NÊN LÀM

- ❌ Đừng đăng dày để "kích thuật toán" — ngách này volume là chiến lược thua, có số chứng minh.
- ❌ Đừng đổi giờ đăng để cứu 0-view: winner đăng 03:32 sáng vẫn ăn 3,84M.
- ❌ Đừng sửa nhiều biến cùng lúc (bài học health 07-21/07-22: đổi thumbnail + backfill metadata + đổi giờ cùng lúc → không đọc được biến nào ăn công).
- ❌ Đừng kết luận "kênh bị đánh" — 4/4 video index tốt, 2 video hạng 1–2 cho long-tail của chúng.
