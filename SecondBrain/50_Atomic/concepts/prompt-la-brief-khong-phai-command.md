---
type: concept
created: 2026-06-08
tags: [claude-code, prompt-engineering, mindset]
status: seed
---

# Prompt là bản brief, không phải câu lệnh

Sai lầm gốc của người mới dùng Claude Code: gõ prompt như **ra lệnh cho máy** ("add WebP conversion"). Đúng ra phải coi nó như **giao việc cho một kỹ sư rất giỏi nhưng vừa mới vào công ty sáng nay** — thông minh, code nhanh, nhưng **chưa biết gì về codebase của bạn**: không biết file nào ở đâu, team đang dùng thư viện nào, quy ước đặt tên ra sao.

Với một người như vậy, bạn không "ra lệnh" — bạn **brief**: bối cảnh, ràng buộc, thế nào là xong. Chất lượng output phụ thuộc vào chất lượng bản brief, **không phải** vào việc model thông minh tới đâu.

> "Đừng dùng Claude Code để viết code trước. Hãy dùng nó để *hỏi* về codebase trước đã." — Boris Cherny, Anthropic

Đổi mindset từ "gõ lệnh" sang "brief cho đồng nghiệp mới" là bước đầu tiên, và là bước quyết định nhất.

## Liên hệ

- [[4-thanh-phan-prompt-tot]] — một bản brief tốt gồm những gì
- [[4d-framework-ai-fluency]] — cùng phép ẩn dụ "AI như thực tập sinh siêu giỏi"; brief tốt = chữ D "Description"

## Nguồn

- Trích từ: [[2026-claude-code-101-prompt-dau-tien]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.3 "Prompt Đầu Tiên"
