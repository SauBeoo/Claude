# CLAUDE.md — youtube-jp-chimei

> Rule riêng cho kênh 地名・地形・河川史 (JP 45–70, documentary). Ghi đè/bổ sung CLAUDE.md toàn cục.

## Vault tương ứng

Tri thức/research → `SecondBrain/10_Projects/youtube-jp-chimei/`. Bằng chứng chọn ngách: `SecondBrain/10_Projects/youtube-niche-research-2026/`.

## Trạng thái project — MỚI LẬP (2026-07-23), CHƯA CHỐT

- **Tên kênh / persona:** CHƯA CHỐT. Định hướng persona: người dẫn tài liệu kiểu NHK (kế thừa chất co-dai), "đọc đất như đọc sử".
- **Giọng TTS:** CHƯA CHỐT — ứng viên số 1: VOICEVOX 青山龍星/ノーマル/0.9 (giọng co-dai cũ, cùng profile rebrand nên kế thừa tự nhiên); xác nhận bằng voice test.
- **Lịch đăng:** CHƯA CHỐT — co-dai cũ đăng 11:00 JST theo benchmark 生活の知恵; ngách mới phải đo giờ đăng đối thủ thắng trước (bài học 2026-07-22), đừng bê nguyên.
- **CTA giữa video:** soạn câu canonical khi chốt persona → thêm `.claude/rules/cta-midvideo.md` mục 2 (điểm chèn: ranh giới chương gần 50%, như co-dai).
- **Profile:** ⚠️ **CHƯA CÓ (cập nhật 2026-07-24)** — Profile 6 nay giữ cho co-dai (user quyết không rebrand co-dai). Chimei cần **profile/Gmail MỚI** trước khi khởi động; chốt profile rồi cập nhật browser_profiles.json + CHANNELS.

## ĐỊNH VỊ — nhánh NGHIÊM TÚC, không đấu nhánh giật gân

- Trục nội dung: ① 地名の由来 theo vùng/chủ đề ② 河川史・治水 (sông từng gây lụt, đất từng là lòng sông) ③ 災害地名 (địa danh cảnh báo — 蛇/滝/久保/沼…) ④ 地形と暮らし (vì sao phố này ở đây).
- **CẤM đi nhánh 怖い地名 giật gân kiểu mystery** (đã bị kênh 100K+ công nghiệp hóa; mình thắng bằng chiều sâu tư liệu). Đề tài 災害地名 làm bằng giọng khoa học + nguồn, không hù.
- **⛔ NÉ TUYỆT ĐỐI: 差別地名 / 部落 liên quan** — vùng nhạy cảm xã hội Nhật, một video sai là chết kênh. Địa danh nào dính lịch sử 部落 → bỏ đề tài, không lách.
- Thiên tai = YMYL nhẹ: khuyến cáo tra ハザードマップ chính thức của 自治体, không phán "chỗ này nguy hiểm đừng mua nhà" (dính BĐS + kiện tụng); nói "địa danh là MỘT gợi ý, hãy xác nhận bản đồ chính thức".

## Fact & nguồn (xương sống uy tín — cũng là khiên inauthentic)

- Từ nguyên địa danh nhiều thuyết → LUÔN 「〜という説があります」, nêu 2 thuyết khi có; nguồn: 角川日本地名大辞典, tư liệu 自治体, 柳田國男『地名の研究』 (public domain — trích được).
- Bản đồ/không ảnh: 国土地理院 (地理院タイル + 空中写真 各年代) — dùng free kèm ghi nguồn 「出典: 国土地理院」 đúng điều khoản; bản đồ cổ PD. 概要欄 có mục 参考資料.
- Số thảm họa lịch sử: nguồn 内閣府防災/気象庁/tư liệu 自治体.

## Kịch bản

- ~20–30 phút; khung kể: mở bằng 1 câu hỏi về cái tên quen thuộc (「なぜ渋谷は"谷"なのか」) → bóc lớp theo bản đồ thời gian → payoff "giờ bạn nhìn phố này khác rồi". Cold open theo nguyên tắc câu-1-là-stake.
- Mỗi video kết bằng mời comment địa danh quê người xem (vòng lặp đề tài từ khán giả — engagement thật + mỏ đề tài).
- Đóng gói CTR đủ bộ theo `youtube-upload-seo.md` (Trends trước title), tag block, ghi vào file script.

## Visual & render

- **Moat = bản đồ so sánh xưa–nay:** dựng tool overlay/side-by-side từ 地理院 tiles + 空中写真 (khâu production mới của kênh — làm proof 1 cái trước khi viết script #1). Còn lại ảnh tĩnh + pan `--motion` nhẹ.
- Render chung `../youtube-jp-health/tools/video_render.py`, BGM -40dB, phụ đề ≤2 dòng, chia chunk khi dài.

## Lưu file

- Script → `03_SCRIPTS/<số>_<slug>.md`. Video → `06_VIDEO/<slug>/`. Media qua `_media_library` (bản đồ tải mới cũng nhập kho, kind ảnh, tag "chimei-map").
