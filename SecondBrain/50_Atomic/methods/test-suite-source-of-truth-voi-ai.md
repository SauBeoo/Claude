---
type: method
created: 2026-06-08
tags: [claude-code, testing, workflow]
status: seed
---

# Test suite là "nguồn chân lý" — biến phase Code thành vòng lặp tự sửa

Khi codebase có test suite chạy được, phase Code tự nó thành một **vòng lặp khép kín**:

```
Claude implement → chạy test → fail → đọc lỗi → sửa → chạy lại
        ↑                                              ↓
        └──────────────── tự lặp ──────────────────────┘
```

Claude **tự biết khi nào xong** (test xanh) — bạn không phải ngồi canh và trả lời "đúng chưa?" sau mỗi bước. Test là thứ phân xử khách quan thay cho cảm giác.

Không có test → Claude phải hỏi liên tục, bạn phải QA thủ công, và bạn **không biết** feature đúng hay không cho tới khi tự bấm thử.

**Hệ quả mạnh — test-driven prompt:** thay vì "implement feature X", hãy bảo *"viết test cho X trước, tôi review, rồi mới implement để test pass."* Việc viết test trước ép cả bạn và Claude nghĩ rõ "đúng trông thế nào" trước khi gõ dòng code đầu tiên → ít bug, code sạch hơn.

## Liên hệ

- [[epcc-workflow-bon-phase]] — đây là thứ làm phase Code chạy mượt, ít back-and-forth
- [[claude-code-subagent-fresh-eyes]] — lớp kiểm tra thứ hai sau khi test xanh

## Nguồn

- Trích từ: [[2026-claude-code-101-epcc-workflow]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.4, "Test suite là source of truth" + Mẹo "Test-driven prompt"
