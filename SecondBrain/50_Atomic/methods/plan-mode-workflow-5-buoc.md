---
type: method
tags: [claude-code, plan-mode, workflow]
source: [[2026-claude-code-101-prompt-dau-tien]]
created: 2026-05-23
---

# Plan Mode workflow gồm 5 bước giúp align với Claude trước khi code, tránh rollback tốn thời gian

Dùng cho **Medium task** (15-60 phút, chạm nhiều file). Nguyên tắc: align trước, code sau.

**Bước 1 — Vào Plan Mode**
Bấm `Shift+Tab` hai lần trong terminal Claude Code. Thanh trạng thái hiển thị `Plan Mode`. Claude chỉ có thể đọc file, không sửa gì.

**Bước 2 — Viết prompt đủ context và constraint**
Cung cấp: tech stack, cấu trúc thư mục liên quan, danh sách yêu cầu cụ thể, constraint kỹ thuật. Đây là bước đầu tư quan trọng nhất.

**Bước 3 — Đọc plan Claude trả về**
Claude đọc các file liên quan rồi trả về plan chi tiết từng bước. Có thể hỏi clarifying questions. Không có gì bị thay đổi ở bước này.

**Bước 4 — Review và comment điều chỉnh**
Đọc plan, gõ phản hồi nếu cần thay đổi approach (skip tính năng, đổi thứ tự, thêm constraint). Claude cập nhật plan theo.

**Bước 5 — Approve và execute**
Confirm "ready to proceed" → Claude chuyển sang Auto Accept mode và bắt đầu execute từng bước trong plan đã được duyệt.

**Khi nào dùng:** Task > 30 phút, feature mới trên codebase chưa quen, bất kỳ khi nào muốn "align trước, code sau".

**Khi nào không cần:** Fix typo, đổi màu, task < 5 phút — Plan Mode là overkill.

## Bằng chứng / nguồn
- Từ [[2026-claude-code-101-prompt-dau-tien]], trang 6-9: demo Dark Mode Toggle end-to-end — từ nửa ngày làm tay xuống còn ~25 phút nhờ Plan Mode workflow
- Boris Cherny: "Shift+Tab into plan, align with Claude first. Once I feel good about the plan, I go into Auto Accept."

## Liên quan
- [[4-thanh-phan-cua-prompt-tot-claude-code]]

## Câu hỏi mở
- Nếu plan Claude trả về sai hoàn toàn (hiểu sai requirement), nên viết lại prompt hay điều chỉnh từng phần?
