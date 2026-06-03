---
type: method
created: 2026-06-03
tags: [claude, research, prompting, meta-prompt]
status: seed
---

# Cách nhờ chính AI draft prompt trước khi bấm Research (khi mù domain)

Tưởng tượng bạn đi khám bệnh lần đầu: bạn không biết thuật ngữ y khoa nào cả, nhưng bạn vẫn nói được *triệu chứng và điều mình muốn* — bác sĩ sẽ tự đặt câu hỏi chuyên môn giúp bạn. Với Research mode cũng vậy: bạn không cần biết domain để ra lệnh nghiên cứu domain đó — hãy để Claude "làm bác sĩ" trước.

Vấn đề gốc: Research prompt tốt cần chỉ định **[SECTIONS]** — nhưng nếu bạn mù lĩnh vực thì không biết section nào đáng hỏi. Giải pháp 2 nhịp: **chat thường (rẻ, vài giây) để Claude đề xuất cấu trúc → duyệt → rồi mới bấm Research (đắt, 30 phút)**.

## Khi nào dùng

Cần chạy Research về lĩnh vực mình không rành (chọn platform, due diligence, market lạ) — không tự nghĩ ra nổi sections/constraints.

## Các bước

1. Chat thường (CHƯA bật Research): *"Tôi muốn research [topic] để [quyết định]. Giúp tôi draft Research prompt tốt hơn — sections nào hữu ích nhất? Constraints nào nên chỉ định?"*
2. Claude đề xuất sections + constraints → bạn gật/lắc/sửa từng cái theo nhu cầu thật của mình
3. Ghép thành prompt 5 phần (Context/Scope/Sections/Constraints/Output) → bật Research

## Lưu ý/cạm bẫy

- Sections luôn sinh ra từ **quyết định của bạn**, không phải từ kiến thức domain — "lo tiền" → section chi phí; "phải chọn" → section khuyến nghị. Phần bạn thiếu chỉ là câu hỏi domain-specific, và đó là phần nhờ AI.
- Đừng quên ràng buộc OUTPUT (độ dài, format, audience) và CITATIONS (nguồn ưu tiên + date range) — thiếu date range là dính data lỗi thời.

## Ví dụ thực tế

Chọn platform dạy lập trình online: tự viết được "so sánh chi phí, pros/cons" nhưng không biết hỏi gì về kỹ thuật → nhờ Claude draft, nó bổ sung section "khả năng chấm code tự động, export dữ liệu học viên" — thứ mình không biết để mà hỏi.

## Liên hệ

- [[chon-tool-theo-cau-hoi]] — bước đứng trước: xác định có đáng dùng Research không
- [[feedback-cu-the-khi-iterate-ai]] — cùng nguyên tắc: ràng buộc cụ thể quyết định chất lượng output
- [[4d-framework-ai-fluency]] — đây là Description nâng cao: dùng AI để cải thiện chính brief cho AI

## Nguồn

- Claude 101 — Bài 1.10: Research mode (Tip 4 + prompt template), Anthropic Academy, 2026
