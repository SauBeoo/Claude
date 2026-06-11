---
type: method
created: 2026-06-08
tags: [claude-code, prompt-engineering]
status: seed
---

# 4 thành phần của một prompt tốt cho Claude Code

Khi brief cho Claude Code, một prompt "đủ dùng" cần 4 phần — thiếu phần nào là Claude phải tự đoán phần đó:

1. **Context** — file nào, folder nào, vùng nào của codebase. (Dùng `@src/auth/login.ts` để nạp đúng file thay vì tả bằng lời.)
2. **Constraints** — được/không được dùng thư viện gì, style, deadline. Cái Claude **không** được làm.
3. **Success Criteria** — "xong" trông thế nào? Test nào phải pass? API trả gì?
4. **"Think hard" trigger** (chỉ khi task khó) — thêm `think hard` / `think harder` / `ultrathink` cuối prompt để Claude suy nghĩ sâu hơn.

Mẹo: 3 dòng cụ thể (Fix gì / Ràng buộc gì / Test nào pass) đủ cho hầu hết task medium. Cạm bẫy ngược lại là **không định nghĩa "done"** → Claude loop vô tận (tối ưu, refactor, thêm test, thêm docs…).

## Liên hệ

- [[prompt-la-brief-khong-phai-command]] — vì sao cần 4 phần này: bạn đang brief, không ra lệnh
- [[3-permission-modes-claude-code]] — task khó (cần "think hard") thường đi kèm Plan Mode

## Nguồn

- Trích từ: [[2026-claude-code-101-prompt-dau-tien]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.3, "Anatomy của prompt tốt"
