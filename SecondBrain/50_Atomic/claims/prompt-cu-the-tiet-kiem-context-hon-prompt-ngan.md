---
type: claim
created: 2026-06-08
tags: [claude-code, context-window, prompt-engineering]
status: seed
---

# Prompt cụ thể (dài hơn) lại tiết kiệm context hơn prompt ngắn

Nghe ngược đời: prompt **dài hơn** mà lại **tốn ít** bộ nhớ hơn? Đúng vậy.

Hình dung bạn nhờ một người thợ: nói "sửa cái bug auth đi" thì anh ta phải đi **lục tung cả nhà** — mở 18 ngăn tủ, đọc 12 tờ giấy — mới đoán ra bạn muốn gì. Mỗi lần lục là tốn chỗ trên bàn làm việc (~25k token đọc file lan man). Còn nếu bạn nói thẳng "file `auth/login.ts` dòng 40, token hết hạn không refresh, sửa bằng cách gọi `refreshToken()` trước khi verify" — anh ta đi thẳng tới chỗ cần, làm luôn (~3k token).

> Một câu prompt chi tiết hơn 50 từ có thể **tiết kiệm 20.000 token** đọc file mò mẫm.

Mấu chốt: token tốn nhiều nhất **không phải** ở prompt bạn gõ, mà ở **hành trình mò mẫm** khi prompt mơ hồ. Cho sẵn file + dòng + nguyên nhân + cách fix = cắt luôn hành trình đó. "Ngắn = tiết kiệm" là hiểu lầm phổ biến nhất.

## Liên hệ

- [[context-window-tai-nguyen-huu-han]] — vì sao tiết kiệm token lại quan trọng

## Nguồn

- Trích từ: [[2026-claude-code-101-quan-ly-context]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.5, chiến thuật 1 "Be specific"
