# CLAUDE.md — Context project "YouTube Khám Phá"

> Claude Code đọc file này tự động khi làm việc trong project. Mục đích: hiểu dự án, ra quyết định nhất quán.

## Tổng quan

- **Loại:** Kênh YouTube faceless, niche **Unexplained Mysteries** (bí ẩn chưa lời giải + hiện tượng khoa học kỳ lạ).
- **Định hướng cốt lõi:** **VIEW NGOẠI — khán giả nói tiếng Anh** (US/UK, mở rộng CA/AU). KHÔNG nhắm khán giả Việt. Lý do: RPM gấp nhiều lần (US $4–8 vs VN $0.3–1), thị trường khổng lồ, AI voice tiếng Anh cực tự nhiên.
- **Format:** **CHỈ long-form 8–12 phút** trong 3 tháng đầu (chưa Shorts, chưa trộn chủ đề). **100% faceless, AI voice tiếng Anh (ElevenLabs).**
- **Người làm:** mới hoàn toàn; vốn 500k–2tr/tháng (ElevenLabs là khoản chính); 3–4h/ngày; **tiếng Anh yếu → dùng AI cho toàn bộ script + voiceover.**
- **Bắt đầu:** Tháng 6/2026.
- **Liên kết vault:** kiến thức làm YouTube/content → `E:\Claude\SecondBrain\20_Areas\` hoặc `30_Resources\`.

## Quyết định đã chốt

1. ✅ Faceless 100%, AI voice — không lộ mặt, không giọng thật.
2. ✅ Khán giả quốc tế / tiếng Anh — mọi thứ public bằng tiếng Anh.
3. ✅ **Niche: UNEXPLAINED MYSTERIES** (chốt 24/06/2026, pivot từ Space/Science). Lý do: hook tự nhiên cực mạnh, tư liệu vô tận, RPM TB ($4–8) nhưng view bù lại, AN TOÀN cho người mới (không dính YMYL). Tài chính RPM cao ($15–40) để nâng cấp sau.
4. ✅ **Chỉ long-form 8–12 phút** trong GĐ đầu. Shorts để Phase 3+ (cắt từ long-form). Một niche + một định dạng + lặp lại → thuật toán hiểu để đề xuất.
5. ✅ Quy trình script chống tiếng Anh yếu: dàn ý tiếng Việt → AI viết script EN giọng hồi hộp → rà dữ kiện → ElevenLabs đọc.
6. ⏳ Tên kênh: chưa chốt (tên tiếng Anh).

## Nguyên tắc làm việc với user

- **Giao tiếp: tiếng Việt.** Nhưng **mọi nội dung kênh (kịch bản, tiêu đề, mô tả, tên): tiếng Anh.**
- User có nền **IT** → dùng analogy kỹ thuật được, thích **data-driven + trade-off rõ ràng**, ghét khen suông.
- **Critique thật, có bằng chứng** — user muốn đánh giá critical trước khi scale, không validate cho vui.
- Không tự commit Git, không tự xóa file (theo CLAUDE.md toàn cục).
- Khi viết kịch bản tiếng Anh: viết trực tiếp bằng tiếng Anh tự nhiên, KHÔNG dịch từ tiếng Việt. Luôn kiểm chứng dữ kiện/số liệu (không bịa).

## Cấu trúc tài liệu

| File | Nội dung |
|---|---|
| `00_CHIEN_LUOC.md` | Niche Mysteries, định dạng, tên, kiếm tiền, nguyên tắc vàng + cạm bẫy |
| `01_ROADMAP_90_NGAY.md` | Lộ trình tuần-theo-tuần (long-form only, bắt đầu 24/06/2026) |
| `02_SETUP_KENH.md` | Checklist tạo & tối ưu kênh |
| `03_QUY_TRINH_FACELESS.md` | Quy trình sản xuất 1 long-form A→Z + chiến lược batch |
| `04_CONTENT_IDEAS.md` | 20 ý tưởng Mysteries (EN + hook) + template kịch bản |
| `05_MAIL_KENH_TRUST_2026.md` | Chọn mail/kênh, build trust, chính sách 2026 |
| `research/` | Đối thủ, từ khóa | `scripts/` | Kịch bản | `assets/` | Brand kit |

## Trạng thái hiện tại

🟢 **Phase 0 — Nền tảng & công cụ** (tuần của 24/06/2026). Niche + định dạng đã chốt. Việc tiếp theo: cài bộ tool (VidIQ/CapCut/Canva/ElevenLabs), tạo Google account riêng, lập Google Sheet "YouTube Journey", nghiên cứu 5 đối thủ mystery, thử 30s giọng ElevenLabs, brainstorm tên kênh.

## Change log

| Date | Change |
|---|---|
| 2026-05-30 | Tạo project. Chốt định hướng view ngoại/tiếng Anh (pivot từ khán giả Việt). |
| 2026-06-24 | **Pivot in place:** niche Space/Science → **Unexplained Mysteries**; thu hẹp định dạng còn **chỉ long-form 8–12p** (bỏ Shorts GĐ đầu). Viết lại 00/01/03/04 theo hồ sơ người mới (3–4h/ngày, tiếng Anh yếu). Giữ nguyên 02 + 05 (hạ tầng niche-agnostic). |
