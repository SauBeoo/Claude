---
type: method
created: 2026-06-08
tags: [claude-code, workflow, delegation]
status: seed
---

# 3-Task Framework (Boris): Easy / Medium / Hard — ai cầm lái?

Trước khi giao việc cho Claude Code, hỏi: *việc này thuộc loại nào?* Boris Cherny chia 3 loại, mỗi loại đổi **ai cầm lái** và dùng chế độ quyền nào:

| Loại | Ví dụ | Ai lái | Chế độ | Thời gian |
|---|---|---|---|---|
| **Easy** (one-shot) | Fix typo, đổi màu, thêm comment | Claude | Auto Accept | < 5 phút |
| **Medium** (planned) | Dark mode toggle, JWT refresh, endpoint mới | Claude (sau khi plan) | Plan Mode → Auto Accept | 15–60 phút |
| **Hard** (you drive) | Refactor kiến trúc auth, migrate schema DB | **Bạn** | Default (review từng bước) | 1 giờ+ |

Mấu chốt: **càng khó, bạn càng phải cầm lái nhiều hơn** — không phải vì Claude kém, mà vì rủi ro đi sai hướng nhân lên theo độ phức tạp. Easy thì thả cho Claude chạy; Hard thì bạn quyết từng bước.

## Liên hệ

- [[3-permission-modes-claude-code]] — bảng này quyết định chọn chế độ quyền nào
- [[calibrate-workflow-theo-task-size]] — cùng tinh thần "đo theo task size" nhưng cho việc skip phase EPCC

## Nguồn

- Trích từ: [[2026-claude-code-101-prompt-dau-tien]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.3, "Boris's 3-Task Framework"
