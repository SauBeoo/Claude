---
type: claim
tags: [ai-workflow, plan-mode, decision-cost, claude-code]
source: [[2026-claude-code-101-epcc-workflow]]
created: 2026-05-23
status: seed
---

# Chi phí thay đổi tăng theo phase: $ trong Plan → $$ trong Code → $$$ sau commit

Khi làm việc với AI coding (đặc biệt Claude Code), chi phí điều chỉnh hướng đi (course-correct) **tăng dần theo phase** mà thay đổi xảy ra:

| Phase xảy ra thay đổi | Chi phí | Loại công việc |
|---|---|---|
| **Plan phase** | $ | Chỉnh vài chữ trong plan, revise approach |
| **Code phase** | $$ | Rollback code đã viết, refactor, viết lại |
| **Sau commit/push** | $$$ | Revert PR, re-review, re-test, communication overhead |

**Hệ quả thực tế**: Plan Mode (Shift+Tab) không phải tính năng "luxury" — là cơ chế **tiết kiệm tiền và thời gian** hiệu quả nhất. Đầu tư 10 phút align ở Plan phase có thể tránh được 30-90 phút debug ở Code phase, hoặc nhiều giờ rollback sau commit.

**Áp dụng**: Trước task medium+ (15+ phút), vào Plan Mode → đọc kỹ plan Claude trả → comment thật nhiều câu hỏi "edge case nào miss?", "thứ tự có đúng?", "approach có conflict architecture?" — đây là lúc câu hỏi rẻ nhất.

**Nguyên tắc rộng hơn**: Argument này áp dụng cho mọi quy trình có nhiều phase (research, design, manufacturing): thay đổi càng sớm càng rẻ. Nhưng với AI coding, hiệu ứng đặc biệt rõ vì Code phase chạy nhanh — sai 1 chữ trong plan thành rollback cả module trong vài phút sau.

## Bằng chứng / nguồn
- Từ [[2026-claude-code-101-epcc-workflow]], trang 5: "Thay đổi trong Plan phase: $ — Thay đổi trong Code phase: $$ — Thay đổi sau khi commit: $$$"
- Tác giả (Boris Cherny) gọi Plan Mode là "the cheapest place to course-correct".

## Liên quan
- [[plan-mode-workflow-5-buoc]]
- [[calibrate-workflow-claude-code-theo-task-size]]

## Câu hỏi mở
- Có dạng task nào mà nguyên tắc này KHÔNG đúng không (ví dụ: prototype throwaway)?
