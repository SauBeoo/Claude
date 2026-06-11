---
type: concept
created: 2026-06-08
tags: [claude-code, context-window, anthropic]
status: seed
---

# Context window — bộ nhớ làm việc hữu hạn của Claude Code

Tưởng tượng Claude Code làm việc trên một **cái bàn nhỏ**. Mọi thứ nó cần lúc này — đề bài bạn giao, file nó vừa mở, kết quả test nó vừa chạy, cả cuốn "sổ nội quy" CLAUDE.md — đều phải nằm trên mặt bàn đó. Bàn rộng ~200.000 token (cỡ 80–100 file code trung bình), nhưng **hữu hạn**: chất càng đầy thì càng khó tìm đúng tờ giấy cần, và khi gần tràn (~80%) hệ thống tự dọn bàn (*auto-compact*) — gom giấy tờ thành một bản tóm tắt rồi **vứt bản gốc đi**.

Vấn đề: lúc dọn, nó có thể bỏ mất chi tiết quan trọng mà bạn nói cách đây 50 lượt — ví dụ rule "JWT secret xoay mỗi 7 ngày" — và bạn **không hề biết là đã mất** cho tới khi gặp hậu quả. Giống trí nhớ ngắn hạn của người: nhớ 7 phút trước thì rõ, 2 giờ trước thì mơ hồ.

Vì thế context window là **tài nguyên quan trọng nhất** khi dùng Claude Code: không phải "model thông minh tới đâu" mà "cái bàn còn chỗ trống không, và những gì đang chiếm chỗ có đáng không".

## Cái gì chiếm chỗ trên bàn

- System prompt lõi (~5k) · CLAUDE.md (2–10k) · định nghĩa tool của MCP server (5–30k) · tên+mô tả các skill (~200/skill) · và **hội thoại + tool call phình dần** theo session.

## Liên hệ

- [[compact-khi-do-dang-clear-khi-doi-task]] — 3 lệnh cầm cương cái bàn này: `/context`, `/compact`, `/clear`
- [[subagent-context-isolation-pattern]] — mượn cái bàn khác để khỏi bày bừa lên bàn chính

## Nguồn

- Trích từ: [[2026-claude-code-101-quan-ly-context]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.5 "Quản lý Context"
