# YouTube Upload SEO — RULE TOÀN HỆ THỐNG

> Áp cho **nenkin** + **showa** và kênh mở sau. Nguồn: checklist "20 bước trước khi đăng" (user cấp 2026-07-15), điều chỉnh cho kênh faceless JP.
> Rule này lo **SEO/metadata lúc upload**; từ ngữ an toàn xem `youtube-compliance.md`, CTA xem `cta-midvideo.md`.

## 0. Ý ĐỒ
YouTube đọc video qua: **tên file gốc → tiêu đề → 3 dòng đầu mô tả → mô tả đầy đủ → phụ đề**. Rẻ, làm 1 lần, quyết định thuật toán hiểu đúng chủ đề. Mọi mục dưới **bắt buộc**, output **ghi vào file script** (mục Đóng gói CTR), không chỉ in ra chat.

## 0.5 ĐO TREND YOUTUBE 30 NGÀY TRƯỚC KHI ĐỀ XUẤT METADATA (bắt buộc)
1. **Nguồn:** Google Trends chế độ **YouTube Search**, 30 ngày, geo JP:
   `https://trends.google.com/trends/explore?date=today%201-m&geo=JP&gprop=youtube&q=<k1,..,k5>&hl=ja`
   (hoặc pytrends — memory `project_trends_pytrends_khong_can_chrome`).
2. **Quy trình** = skill `trend-keywords`: pool 10–20 ứng viên → rổ ≤5 + **anchor bridging** về một thang → lấy related queries. Không bịa số.
3. **Chống nhiễu:** volume nhỏ hay ra chuỗi 0 → đối chiếu **web search 12 tháng** (`date=today 12-m`, bỏ gprop) để phân biệt từ chết vs nhiễu mẫu + bắt mùa vụ. Ghi rõ số từ nguồn nào.
4. **Áp:** keyword volume cao nhất **ĐÚNG INTENT** → đầu title + dòng 1 mô tả · **hashtag xếp theo volume giảm dần** (3 cái đầu hiện trên video) · tag phủ long-tail + tag nhận diện kênh · **LOẠI keyword volume cao nhưng SAI INTENT** · keyword đang đỉnh mùa → ghi khuyến nghị thời điểm đăng.
5. **Bảng điểm + kết luận + ngày đo ghi vào file script.** Áp cho CẢ title LẪN thumbnail (`audience-45plus.md` §1 gate 7).

## 1. TRƯỚC KHI UPLOAD
### 1.1 Tên file video = slug từ khóa chính
Chữ thường, gạch ngang, không dấu, **romaji của keyword chính** (vd `koukin-uketori-kouza-45nichi.mp4`). Gói CTR in sẵn tên file đề xuất.
### 1.2 Phụ đề `.srt`: tự upload, KHÔNG auto-caption
Luôn tải `subs.srt` (bản SẠCH, không phải `_styled`) lên ở bước phụ đề.

## 2. METADATA CHÍNH
### 2.1 Tiêu đề: từ khóa chính đứng ĐẦU
- Keyword quan trọng nhất trong **5–7 từ đầu**, lọt vùng ~**28–30 ký tự full-width**.
- Không viết hoa toàn bộ, không giật tít sai nội dung. Giữ format tiêu đề đã chốt của từng kênh.
### 2.2 Ba dòng đầu 概要欄
Nêu **về gì / cho ai / được gì**, keyword chính **1 lần tự nhiên**. ❌ Cấm lời chào, cấm dồn disclaimer/credit lên đầu.
Thứ tự 概要欄: **① 3 dòng hook → ② 目次 → ③ nội dung → ④ disclaimer → ⑤ credit → ⑥ hashtag**.
### 2.3 Mô tả đầy đủ ~400–600 ký tự JP
Theo **timeline** (khớp chapter), chèn **từ khóa liên quan/đồng nghĩa** (không lặp keyword chính), link playlist cùng chủ đề.
### 2.4 Bộ nhận diện metadata TẦNG KÊNH — nhất quán mọi video
Chốt 1 lần trong CLAUDE.md project, rồi áp y hệt:
1. **categoryId chuẩn kênh** — đo từ kênh **ĐANG thắng** ngách, ghi kèm kênh nguồn + ngày đo, **đo lại khi kênh nguồn tụt** (`youtube-jp-health/tools/bench_channels.py <channelId>`). Cấm áp categoryId chéo ngách.
2. **Rổ 10–12 tag nhận diện kênh CỐ ĐỊNH** đứng đầu; tổng ~25–40 tag, không dưới 15.
3. **3 hashtag nhận diện kênh cố định** đứng đầu dòng hashtag; hashtag đặt **CUỐI desc**.
4. **Khung desc cố định** (hook → 目次 → topical → disclaimer → hashtag).
Tầng kênh (1 lần, audit lại khi 0-view): channel description ≥300 ký · keywords ~15–28 cụm · banner · country/defaultLanguage.

## 3. TÍCH HỢP VÀO PIPELINE
Gói CTR của skill `script-*` phải xuất: **Tên file upload** · **3 dòng đầu 概要欄** · **Mô tả đầy đủ**, ghi vào file script; quét chéo `youtube-compliance.md` trước khi giao.

## 4. 🔴 GATE MÁY CHO MÔ TẢ (`Projects/youtube-jp-chouhen/tools/upload_pack.py`)
- `find_block()` so chuỗi **`casefold()`** → heading hoa/thường đều đọc được; có nhánh đọc heading `概要欄` trần.
- Ô `[3] DESCRIPTION` rỗng → **tự HÉT tại chỗ** `🔴🔴 THIẾU MÔ TẢ — ĐỪNG ĐĂNG`.
- Gate chất lượng: `<400 ký` → cảnh báo · không có mốc `\d{1,2}:\d{2}` → cảnh báo thiếu 目次.
📌 **Heading trong script là giao diện máy đọc**, không phải chữ trang trí. Cảnh báo phải nằm **đúng ô sắp copy**, không cuối file.

## 5. 🔴 目次 PHẢI ĐO TỪ BẢN RENDER
Lệch **tăng dần** theo thời gian = chữ ký của mốc ước, không đo → đi tìm chỗ ước, đừng sửa từng mốc.
1. **Viết 目次 SAU khi render**, lấy mốc từ `subs.srt` / scene plan của chính bản mp4 sắp đăng.
2. **Mọi mốc cách ≥10 giây** (dưới mức đó YouTube không tạo chương).
3. **Mốc đầu `00:00`**.
```python
assert moc[0][0] == 0
assert all(b - a >= 10 for (a, _), (b, _) in zip(moc, moc[1:]))
```
⚠️ Cảnh báo *"mp4 MỚI hơn script → soát lại 目次"* của `upload_pack.py` — đừng bỏ qua.

### 5.1 ⚖️ Credit phải đúng sự thật
Credit là lời khai nguồn gốc: ghi credit cho thứ không dùng là sai; thiếu credit CC BY là vi phạm license. **Mỗi lần đổi nguồn asset (stock → AI, đổi TTS, đổi BGM) phải rà lại khối credit** của khuôn 概要欄.

## ✅ CHECKLIST UPLOAD NHANH
0. Đã đo Trends gprop=youtube 30 ngày, bảng điểm ghi vào script? (§0.5)
1. File video đã rename thành slug keyword?
2. `subs.srt` sạch sẵn để upload tay?
3. Keyword chính trong 5–7 từ đầu title, lọt ~30 full-width?
4. 3 dòng đầu mô tả: về gì / cho ai / được gì + keyword 1 lần?
5. Mô tả đầy đủ theo timeline + từ khóa liên quan + playlist?
6. Đã quét compliance?
7. 目次 đo từ `subs.srt` của chính bản sắp đăng, `00:00`, cách ≥10s? (§5)
8. Từng dòng credit trỏ tới thứ thật sự có trong bản render? (§5.1)
