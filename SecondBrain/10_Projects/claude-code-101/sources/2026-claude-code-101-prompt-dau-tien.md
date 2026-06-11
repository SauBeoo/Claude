---
type: source-note
source_type: docs
source_file: Prompt Đầu Tiên.pdf
title: "Bài 2.3 — Prompt Đầu Tiên"
authors: Anthropic
year: 2026
url:
tags: [docs, claude-code, prompt-engineering, plan-mode]
status: summarized
created: 2026-05-23
---

# Bài 2.3 — Prompt Đầu Tiên

## TL;DR
Prompt không phải là command mà là **brief** — bạn đang giao việc cho một kỹ sư tài năng nhưng chưa biết gì về codebase của bạn. Bài này dạy cách viết prompt đủ context/constraint/success criteria, phân biệt 3 permission modes (Default / Auto Accept / Plan Mode), và áp dụng Boris's 3-task framework để chọn cách tiếp cận đúng cho từng loại task.

## Nội dung chính

### Luận điểm chính
Chất lượng output của Claude Code phụ thuộc trực tiếp vào chất lượng prompt, không phải khả năng của model. Thay đổi mindset từ "ra lệnh" sang "brief cho kỹ sư" là bước đầu tiên.

> "Don't use Claude Code to write code first. Use it to ask questions about the codebase." — Boris Cherny, Anthropic

### 3 Permission Modes (toggle bằng Shift+Tab)

| Mode | Hành vi | Best for |
|------|---------|----------|
| **Default (Approval)** | Hỏi xác nhận từng lần edit/chạy lệnh | Production branch, lần đầu dùng |
| **Auto Accept** | Tự động approve edit file, vẫn hỏi khi chạy shell | Sandbox, dev branch đã tách |
| **Plan Mode** | Read-only: đọc/phân tích, trả về plan, không sửa gì | Task phức tạp, cần align trước |

**Quy tắc nhanh:** Task < 5 phút → Default hoặc Auto Accept. Task > 30 phút hoặc chạm nhiều file → Plan Mode trước.

### Boris's 3-Task Framework

| Loại | Ví dụ | Ai drive | Mode | Thời gian |
|------|-------|----------|------|-----------|
| **Easy** (one-shot) | Fix typo, đổi màu, add comment | Claude | Auto Accept | < 5 phút |
| **Medium** (planned) | Dark mode toggle, JWT refresh, new API endpoint | Claude (sau plan) | Plan Mode → Auto Accept | 15-60 phút |
| **Hard** (you drive) | Refactor auth architecture, migrate DB schema | **Bạn** | Default (từng bước review) | 1+ giờ |

### Anatomy của prompt tốt (4 thành phần)

1. **Context** — file nào, folder nào, codebase area nào
2. **Constraints** — library được/không được dùng, style, deadline
3. **Success Criteria** — kết quả trông như thế nào? Test nào phải pass?
4. **"Think Hard" Trigger** (nếu task khó) — thêm `think hard` / `think harder` / `ultrathink` vào cuối prompt

### Plan Mode Workflow (cho Medium task)
1. `Shift+Tab` → vào Plan Mode
2. Viết prompt với đủ context + constraint
3. Claude trả về plan chi tiết (không sửa file)
4. Review plan, comment điều chỉnh nếu cần
5. Approve → Claude chuyển sang Auto Accept để execute

### 5 Anti-patterns phổ biến

1. **Prompt quá broad** — "Build me an app" → Claude không biết stack, auth, DB
2. **Skip Plan Mode cho task > 30 phút** → mất thời gian rollback khi Claude đi sai hướng
3. **Auto Accept trên production branch** → dùng Default mode, tạo feature branch trước
4. **Không define "done"** → Claude loop vô tận (optimize, refactor, thêm test, thêm docs...)
5. **"Fix tất cả bugs"** → scope không giới hạn, Claude thay đổi behavior ngoài dự kiến

### Mẹo nâng cao

- **Extended thinking triggers:** `think hard` (bug khó), `think harder` (task phức tạp), `ultrathink` (architectural decision)
- **@filename syntax:** Dùng `@src/auth/login.ts` thay vì mô tả file bằng lời — Claude load đúng context
- **Multi-line ngắn gọn:** 3 dòng cụ thể đủ cho hầu hết task medium (Fix / Constraint / Test)
- **Interrupt sớm:** Bấm ESC khi Claude đi sai hướng thay vì để chạy hết rồi rollback

## Đánh giá của tôi (để trống)
- Điểm hay:
- Nghi ngờ / muốn đào sâu:
- Liên quan đến project nào:

## Ứng viên Atomic Notes

1. **Prompt là brief, không phải command** — mindset shift cốt lõi khi dùng Claude Code
2. **Boris's 3-Task Framework (Easy/Medium/Hard)** — cách phân loại task để chọn approach
3. **3 Permission Modes của Claude Code** — Default vs Auto Accept vs Plan Mode, khi nào dùng cái nào
4. **4 thành phần của prompt tốt** — Context + Constraints + Success Criteria + Think Hard Trigger
5. **Plan Mode workflow cho Medium task** — 5 bước align trước khi execute

## Atomic đã chắt (2026-06-08)

- [[prompt-la-brief-khong-phai-command]], [[4-thanh-phan-prompt-tot]], [[3-permission-modes-claude-code]], [[3-task-framework-easy-medium-hard]]
- Index: [[claude-code-MOC]]
- *(Ứng viên "Plan Mode workflow" đã gộp vào [[3-permission-modes-claude-code]] + [[epcc-workflow-bon-phase]] để tránh trùng.)*

## Trích dẫn quan trọng

> "Don't use Claude Code to write code first. Use it to ask questions about the codebase."
— Boris Cherny (trang 2, phần "Mở đầu")

> "Shift+Tab into plan, align with Claude first. Once I feel good about the plan, I go into Auto Accept."
— Boris Cherny (trang 6, phần "Medium: Plan trước, execute sau")

> "Prompt mạnh thường nhanh hơn và ít token hơn, dù bản thân prompt dài hơn."
— trang 16, phần "Bài tập 2"
