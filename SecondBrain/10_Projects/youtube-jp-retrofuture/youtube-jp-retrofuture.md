---
tags: [project, youtube, ai-video, retrofuture]
status: active
created: 2026-09-21
---

# youtube-jp-retrofuture — 昭和100年 レトロフューチャー

Folder note tri thức. Repo code: `E:\Claude\Projects\youtube-jp-retrofuture\`

## Kênh này là gì
Kênh YouTube JP **không lời kể, không phụ đề**, 100% video AI (t2v). Bán **không khí + thế giới quan**:
một Nhật Bản nơi thời Showa chưa bao giờ kết thúc, giờ là 昭和100年, công nghệ tiến theo nhánh
**cơ khí + nguyên tử + khí nén** thay vì nhánh số hoá. Nhân vật xuyên suốt: robot gia dụng ロボ太.

🔴 **Riêng hoàn toàn với `youtube-jp-showa`** (bảo tàng ký ức có lời kể, số liệu, mốc năm). Dùng chung
tool, không dùng chung nội dung/cast/clip.

## Bài học có thể tái dùng ở kênh khác

### 1. ⭐ Tiền đề là một CÂU — thế giới phải là DANH TỪ
Bản prompt đầu chỉ ghi *"alternate present-day Japan where the Showa era never ended"* → model trả về
**Nhật 1975 bình thường**, không một chi tiết viễn tưởng nào. User bắt lỗi ngay.
⇒ Phải kê **kho vật cụ thể** (kiến trúc · phương tiện · đồ đạc · bầu trời) và ép mỗi prompt lấy 3–5 món.
📌 Cùng định luật đã đo 3 lần ở chỗ khác: **model nghe DANH TỪ và VỊ TRÍ, không nghe KHÁI NIỆM hay TỈ LỆ**
(`media-library.md` §2.10 ⑥ · `camera-language.md` §0 ②).

### 2. ⭐ Chọn nhân vật theo ĐIỂM YẾU CỦA CÔNG CỤ
t2v không khoá được danh tính người → chọn **robot** làm nhân vật chính: khối cứng, màu phẳng, tả bằng
6 danh từ là ra đúng. Và spec **bánh xe thay chân + bàn tay 3 ngón to** bịt sẵn 3 bệnh nặng nhất
(chân trượt, chi cao su, ngón thừa). Đây là cách biến hạn chế công cụ thành lựa chọn sáng tạo.

### 3. Vật mời gọi chữ/số phải BỎ VẬT, không chỉ cấm bằng chữ
Thẻ tên 名札 · đồng hồ có mặt số · bảng ga lật — ba vật mời gọi chữ/số. Sửa **spec của vật**
(khăn đỏ thay thẻ tên · mặt đồng hồ trống · bảng ga để xa ngoài tiêu điểm), không thêm câu cấm.
📌 `ai-video-regen.md` §3.

### 4. "Không lời" không có nghĩa "không chữ"
Video 0 chữ tuyệt đối làm YouTube **không hiểu chủ đề kênh** (lỗi đã đo ở showa: search dẫn vào toàn
từ khoá lệch). Giải bằng **telop kiểu 字幕スーパー ≤6 dòng/video** — không phải phụ đề, là **đạo cụ của
thế giới**, và vẽ bằng font chứ không nhờ AI bake.

### 5. Kênh không lời chỉ có 4 động cơ giữ chân
**nhạc · nhân vật · thế giới có quy tắc · vòng lặp thời gian.** Kênh sống là kênh có ≥2. Concept nào
không trả lời được "động cơ nào" thì loại, dù prompt đẹp cỡ nào.

## Liên quan
- [[project_youtube_jp_showa]] — kênh 昭和 có lời kể, **khác hẳn**
- [[feedback_nhan_vat_dong_nhat_va_noi_lien]] — t2v không có character-lock cho người
- [[feedback_ai_video_hong_thao_tac_tay]] — 58/73 clip hỏng ở thao tác tay với vật nhỏ
- [[feedback_ai_nguoi_that_thay_anime]] — photoreal, tick altered/synthetic
