# CHANNEL_DIAGNOSIS — 昭和くらし図鑑 (khám 2026-09-03, đề bài: thumbnail + title, CTR thấp)

> Số đo: YouTube Data API (token nenkin, public stats) + **đọc tay Studio** (Profile hiện tại có quyền quản lý kênh)
> + contact sheet 7 thumbnail của mình vs 4 kênh đối thủ (`06_VIDEO/_diagnose_2026-09-03/sheet_*.jpg`, `data.json`).
> Kênh 20 ngày tuổi, 7 video, 1 sub. Mọi số CTR dưới đây đều ở **mẫu nhỏ** — đọc chiều hướng, không đọc phần trăm lẻ.

## 0. KẾT LUẬN 1 DÒNG

CTR **không** phải chỗ hỏng nặng nhất: 5/7 video được cấp **<600 vé**, tức YouTube chưa test; video duy nhất được cấp vé
(初任給, 4,9K imp) thì **rớt 62% trước giây 30** dù CTR 3,5%. Nhưng bao bì đúng là chỗ phải sửa **trước**, vì 7/7 thumbnail
là một khuôn, hero là DANH TỪ nhãn, không NGƯỜI, tông nâu đều — và title 7/7 mở bằng tag SEO 【昭和100年】 chiếm 1/4 vùng hiển thị.

## 1. SỐ (Studio, 28 ngày, đọc 2026-09-03)

| video | đăng | imp | CTR | view | unique | AVD | nguồn chính |
|---|---|---|---|---|---|---|---|
| 06 初任給の封筒 | 08-29 | **4.855** | **3,5%** | 1.285 | 185 | **1:45** (18%) · **38% còn lại @0:30** | browse 98% |
| 02 商店街 | 08-20 | 1.909 | **5,1%** | 299 | 168 | **4:59** | browse 88% |
| 01 給食 | 08-18 | 564 | 4,8% | 80 | — | ~2:50 | — |
| 04 昭和45年の朝 | 08-25 | 221 | 1,4% | 21 | — | — | — |
| 03 教室の道具 | 08-22 | 178 | 2,8% | 14 | — | — | — |
| 05 駄菓子屋 | 08-27 | 69 | 4,4% | 8 | — | — | — |
| 07 町の音 | 09-01 | 64 | 3,1% | 9 | — | — | — |
| **kênh** | | **7.860** | **3,9%** | 1.716 | | | |

Đọc:
- **Vé mới là biến quyết định.** 5/7 video <600 imp → CTR 1,4–4,8% ở mẫu đó là nhiễu, không kết luận được thumbnail nào hơn.
- **Video 06 là ca đáng đọc nhất:** được đẩy browse rộng (4,9K imp, gấp 2,5× video 02) → CTR tụt về 3,5% (bình thường khi tệp rộng ra),
  **rồi 62% người bỏ đi trước 0:30**, AVD 1:45 so với 4:59 của 商店街. Vòi mở rồi tự đóng ở tầng retention, không ở tầng CTR.
- Search dẫn vào 06 toàn từ khoá lệch (`日活映画 無料配信`, `白い巨塔 田宮二郎`) → YouTube chưa hiểu chủ đề kênh (`youtube-suggested-growth.md` §1.5).
- Video dẫn view sang 商店街: 3/5 là video 昭和 cùng ngách (安かった物5選 · 昭和にはあった今は見なくなったもの10選 · 家庭料理5選) → khu phố đúng.

## 2. VÌ SAO 06 RỚT Ở 0:30 — thumbnail hứa SỐ, 30 giây đầu kể MOOD

Thumbnail live: banner `銭湯38円 ラーメン120円 映画351円` + hero `ぜんぶ使ったら 残りは？` (câu đố số).
30 giây đầu (`subs.srt`): 「指先が、汗ばんでいました。茶色い封筒。開ける前に、指で、厚みを確かめました…あなたは、覚えていますか」 —
**không một con số nào tới 0:31**, số đầu tiên (2万5千円) ở ~1:05. Người bấm vì 3 con giá → nghe tuỳ bút → đi.
Đây là **mismatch thumbnail ↔ cold open**, đúng loại lỗi `media-library.md` §2.0 nói ở tầng hình, lặp lại ở tầng lời.
⇒ Sửa bao bì mà không sửa 30 giây đầu theo cùng lời hứa thì video sau được cấp vé vẫn rớt y như 06.

## 3. THUMBNAIL — 6 lỗi đo trên sheet (mình vs あの頃の昭和 9,9K sub · あの頃の日本 40 sub/10,6K view)

| # | mình (7/7) | đối thủ ăn view | hệ quả |
|---|---|---|---|
| 1 | **7 thumb = 1 khuôn** K-collage: chip 全N点 · banner năm · trắng 「今では消えた」 · đỏ 「昭和の◯◯」 | cùng khuôn kênh nhưng **chữ đổi hoàn toàn từng video**, ảnh khác nhau rõ | trên feed 7 cái nhìn như 1 → không có lý do bấm cái thứ hai |
| 2 | hero đỏ = **DANH TỪ nhãn**: 昭和の給食 · 教室の道具 · 昭和の商店街 · 駄菓子屋 · 昭和の町の音 | hero = **MỆNH ĐỀ có gap**: 今では信じられない5選 · こんなに安かった · 今の若者は意味も知らない · なぜ消えた？ | trả lời "về cái gì" nhưng không "chuyện gì xảy ra" (thiếu ② gate 7 `audience-45plus` §1) |
| 3 | collage 3–4 ô, vật nhỏ, **0/7 có NGƯỜI** | **1 ảnh thật** có NGƯỜI (mẹ + bé, cậu bé uống sữa, ông thổi kèn) chiếm khung | ở 120px collage thành mảng vụn; không có mặt = không có điểm neo (gate 4) |
| 4 | tông **sepia nâu đều 7/7** | nền đen-trắng/sepia **nhưng** chữ đỏ 2 dòng ~50–55% khung + chip xanh/đỏ rực | trong feed 昭和 toàn kênh khác cũng nâu → mình không nổi; hero mình chỉ ~30% khung |
| 5 | **2 khối phụ** (chip 全10点 + banner 昭和30年〜40年代) | 1 chip năm ở góc | 2 khối không đọc được ở 120px mà chiếm 1/6 khung |
| 6 | 「今では消えた」 6/7 | 「今では信じられない／今じゃ考えられない」 | benchmark 08-29 §2: hook 消えた ở tầng BÉT, hook chênh-lệch-với-hôm-nay ở tầng TOP (31×) |

⚠️ Cái **không** hỏng: chữ đọc được ở 168px và 120px cả 7/7 (gate 5 đạt); kanji không nát; ✦ sạch. Vấn đề là **nội dung chữ + bố cục**, không phải thi hành.

## 4. TITLE — 4 lỗi

1. **7/7 mở bằng 【昭和100年】** = 7 ký trong ~28 ký hiển thị, là tag SEO, **không nói gì với người xem**. Đối thủ mở bằng
   【昭和40年〜50年】 = mốc THỜI ĐẠI → người xem tự lọc "cái này của tôi" trong 0,3s. (`昭和100年` giữ ở tag/hashtag/概要欄 là đủ.)
   ⓘ Live title là 昭和100年 trong khi METADATA 03–07 + CLAUDE.md ghi 昭和101年 — có người đổi tay, tài liệu đang lệch kênh.
2. Khuôn 「◯◯から消えた◯◯N選｜liệt kê…あなたは何点覚えていますか？」 6/7 → hook 消えた (tầng bét, §3 mục 6) và **đuôi câu hỏi nằm ngoài vùng
   hiển thị** → vô dụng trên feed, chỉ đọc được khi đã bấm.
3. Vùng hiển thị (~28 ký) hiện chứa: tag + 「◯◯から消えた◯◯N選」 — **không có con số giá / không có mệnh đề gap** nào lọt vào.
4. Title duy nhất có 3 giá cụ thể (06) là title duy nhất được đẩy — khớp tầng TOP của đối thủ (安かった物 · お金の常識), n=1 nhưng cùng chiều với 42 video đo 08-29.

## 5. ĐỀ XUẤT (chưa làm — chờ user chốt, `feedback_chot_truoc_khi_dang`)

### 5.1 Thumbnail — mở khuôn **K-PHOTO** làm T3 song song K-collage, đọc bằng Test & compare
- **1 ảnh thật** (Commons PD / still cắt từ phim NARA đã có sổ) có **NGƯỜI + VẬT to** chiếm khung, tông ảnh gốc (đen-trắng/sepia được).
- **2 dòng chữ đỏ 袋文字 ~50% khung**: dòng 1 = mệnh đề gap (今では信じられない／こんなに安かった／なぜ消えた？), dòng 2 = chủ đề + keyword đo cao nhất.
- **1 chip năm** góc trên (昭和40〜50年, nền xanh/đỏ rực). ⛔ bỏ chip 全N点, bỏ dòng trắng 「今では消えた」.
- Đường test đúng luật `ab-3title-3thumb.md`: chạy **Studio Test & compare** trên 02 + 06 (2 video có vé): T1 collage hiện tại vs T3 K-PHOTO, ≥7 ngày, **giữ nguyên title trong lúc test**.
- Trong lúc test: kênh mới >5 video tới đăng T1 collage + T2 + **T3 K-PHOTO** như luật 3×3 vốn đòi (video 07 chỉ có 1 bản T3, video 03/05 chỉ có T1 — gate 3×3 đã bị bỏ qua).

### 5.2 Title — đổi TUẦN TỰ sau khi test thumbnail xong (videos.update, mỗi bản ≥7 ngày)
Khuôn mới: `【昭和XX〜YY年】<mệnh đề gap ≤12 ký><chủ đề>N選｜<2–3 vật/giá>` — mọi thứ ăn tiền lọt 28 ký đầu, bỏ đuôi 何点覚えていますか (chuyển sang pinned comment).
Ví dụ (chưa đo Trends lại — phải đo theo `youtube-upload-seo.md` §0.5 trước khi áp):
- 06: `【昭和45年】初任給2万5千円、全部使ったら残りは？｜銭湯38円・ラーメン120円・映画351円`
- 02: `【昭和30〜40年】今では考えられない商店街の当たり前30選｜通い帳・御用聞き・紙のふた`
- 01: `【昭和40〜50年】今の子は信じない昭和の給食10選｜鯨の竜田揚げ・脱脂粉乳・ソフト麺`

### 5.3 Cái đứng trên cả hai: khớp 30 giây đầu với lời hứa của thumbnail
Video có thumbnail SỐ thì **con số đầu tiên phải ra trước 0:15** (06: đưa 「二万五千円」 lên câu 2), rồi mới tuỳ bút. Gate `≤60s vào vật đầu` của kênh đang PASS mà vẫn rớt 62% — gate đo "vào vật", không đo "trả lời hứa".

### 5.4 Farm cái đã có vé
06 là video duy nhất được đẩy → PART2 trục tiền (お金の常識・安かった物) theo `upload-schedule.md` §0.9b, nhưng **chỉ sau khi 5.3 được áp** — thêm video vào cùng khuôn mở bài là thêm mẫu AVD 1:45 vào điểm kênh.

## 6. HẠN DÙNG
Đọc lại sau 5 video hoặc khi Test & compare trả CTR (≥7 ngày). Kênh <500 imp/video ở 5/7 → **không kill trục** nào từ số này (`youtube-suggested-growth.md` §3 mục 4).

## 7. ĐÃ ÁP CHO VIDEO 08 (cùng ngày)
- Title A1/A2/A3 viết lại theo §4 → `03_SCRIPTS/08_okane-joushiki.md` §Đóng gói CTR; `_upload/METADATA.txt` đã regen (`upload_pack --force`).
- Thumbnail: T1 giữ K-collage đã gen · T2/T3 = **K-PHOTO** (prompt `06_VIDEO/08_okane-joushiki/thumb_prompts_FLOW.txt`, 2 dòng, TEXT @ 7%). Chờ user gen → `thumb_T2_okane.png` / `thumb_T3_okane.png` → chạy lại `upload_pack --force`.
- Luật kênh: `CLAUDE.md` §2 (title) + §3 (thumbnail) ghi trạng thái THỬ; `03_THUMBNAIL_FORMULA.md` §1.5 khuôn K-PHOTO.
- ⚠️ **Bẫy tool bắt được:** `upload_pack --force` **không xoá** `thumbnail_T2/T3` cũ trong `_upload/` khi file `thumb_T2/T3_*` nguồn đã bị dời đi → METADATA vẫn liệt kê 3 thumbnail, gate 3×3 im lặng, người upload sẽ bốc nhầm bản collage cũ. Đã dời tay sang `_thumb_old/_upload_stale/` + ghi 🔴 vào METADATA. Cùng họ `media-library.md` §2.10 ⑦ (tool thấy MỘT file khớp tên ≠ thấy ĐÚNG file). ⏳ việc mở: `--force` phải dọn `thumbnail*` trước khi gói lại.
