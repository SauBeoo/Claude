---
type: concept
created: 2026-06-08
tags: [claude-code, subagent, code-review]
status: seed
---

# Subagent reviewer — đôi mắt mới không dính bias session

Claude chính đã ngồi trong session từ đầu: chính nó viết đoạn code đó, nên nó **"biết" code đó đúng** — đúng cái bẫy của người tự chấm bài mình. Đó là *bias session*.

Trước khi commit, cử một **subagent reviewer**: một agent phụ có context window riêng, **bắt đầu từ con số 0**, chỉ đọc `git diff`, test liên quan và CLAUDE.md. Vì không dự phần viết code, nó nhìn bằng *đôi mắt mới* và thường bắt được lỗi mà session chính bỏ qua (case study: subagent tóm được edge case "empty buffer" mà 20 phút code không thấy).

Đây là "second opinion" rẻ và nhanh nhất: 5 phút review có thể cứu một bug mà 2 tiếng code không nhìn ra. Quy tắc: **luôn có một bước review trước commit**, dù chỉ 2 phút.

## Liên hệ

- [[epcc-workflow-bon-phase]] — đây là công cụ của phase Commit
- [[subagent-context-isolation-pattern]] — cùng cơ chế subagent (context riêng), nhưng dùng cho mục đích khác: giữ context sạch

## Nguồn

- Trích từ: [[2026-claude-code-101-epcc-workflow]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.4, "Subagent code reviewer" (chi tiết Bài 2.6)
