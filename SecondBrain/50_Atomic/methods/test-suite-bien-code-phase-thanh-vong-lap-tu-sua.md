---
type: method
tags: [claude-code, testing, ai-workflow, automation]
source: [[2026-claude-code-101-epcc-workflow]]
created: 2026-05-23
status: seed
---

# Test suite biến Code phase với AI thành vòng lặp tự sửa, không cần human-in-the-loop

**Vấn đề**: Khi không có test suite, mỗi step Claude implement xong, bạn phải tự manual verify, gõ "đúng chưa?" → tốn thời gian cả hai. Tệ hơn: bạn không biết feature "đúng" hay không cho đến khi mở browser/Postman.

**Cơ chế**: Khi có test suite reliable, Code phase trở thành vòng lặp tự động:

```
Claude implement → chạy test → fail → đọc error → sửa → chạy lại
                          ↑                                  ↓
                          └──────────── lặp tự động ─────────┘
```

Claude tự biết khi nào xong (tất cả test pass). Không cần ngồi canh.

**Setup tối thiểu**:
1. Đảm bảo lệnh chạy test rõ (`npm test`, `pytest -v`, `cargo test`) — Claude tự chạy được.
2. Cho Claude biết lệnh lint nếu có (`npm run lint --fix`) để tự sửa style errors.
3. Trong prompt Plan/Code phase, định nghĩa success criteria = "tất cả test trong tests/X/ pass + không có TS error + build success".

**Pattern nâng cao — Test-driven prompt**: Thay vì "implement feature X", prompt:
> "Viết test cases cho feature X trước. Tôi sẽ review. Sau khi approve tests, mới implement."

Force cả bạn và Claude suy nghĩ rõ về expected behavior trước khi viết code → ít bug, cleaner code.

**Anti-pattern**: Code không có test = bạn phải làm QA thủ công sau mỗi bước. Đây là 1 trong 5 anti-patterns chính của EPCC workflow.

## Bằng chứng / nguồn
- Từ [[2026-claude-code-101-epcc-workflow]], trang 8: "Có test suite → Code phase thành vòng lặp tự sửa. Không cần ngồi canh — Claude tự biết khi nào xong."

## Liên quan
- [[plan-mode-workflow-5-buoc]]
- [[epcc-workflow-claude-code]]
- [[calibrate-workflow-claude-code-theo-task-size]]

## Câu hỏi mở
- Với codebase chưa có test, đầu tư bao nhiêu thời gian viết test trước khi để Claude implement là hợp lý?
