---
type: concept
created: 2026-06-08
tags: [claude-code, context-window, subagent]
status: seed
---

# Subagent — mẫu "cách ly context" (answer without journey)

Có những việc **đọc thì nhiều mà kết luận thì ít**: ví dụ "tìm tất cả TODO trong repo, gom theo module". Nếu để Claude chính tự làm, nó phải mở hàng chục file — và toàn bộ đống file đó **bày hết lên bàn chính**, làm đầy context dù bạn chỉ cần một danh sách ngắn cuối cùng.

Mẫu **subagent** giải quyết đúng chỗ đó: bạn cử một "trợ lý" có **cái bàn riêng 200k token** đi làm phần lục lọi. Nó đọc thỏa thích trên bàn của nó, rồi **chỉ mang về bản tóm tắt** — cái bàn chính của bạn vẫn sạch.

Đây là quy tắc **"answer without journey"**: bạn nhận *câu trả lời* mà không phải gánh *hành trình* tìm ra nó. Việc đọc-nhiều-trả-ít chính là ứng viên hoàn hảo để giao cho subagent: explore codebase lạ (cử 4 subagent đọc 4 module song song), đọc log nặng MB, dò tài liệu thư viện…

## Liên hệ

- [[context-window-tai-nguyen-huu-han]] — vấn đề mà mẫu này bảo vệ: giữ bàn chính sạch
- [[compact-khi-do-dang-clear-khi-doi-task]] — chữa cháy khi bàn đã đầy; subagent là phòng bệnh từ đầu

## Nguồn

- Trích từ: [[2026-claude-code-101-quan-ly-context]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.5, chiến thuật 3 "Subagent outsource exploration"
