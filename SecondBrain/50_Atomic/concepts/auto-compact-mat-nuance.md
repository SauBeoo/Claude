---
type: concept
created: 2026-05-24
tags: [claude-code, context-management, lossy-compression]
status: seed
---

# Auto-compact mất nuance — không nên phó mặc

Khi context window gần chạm ~80%, Claude Code tự kích hoạt **auto-compact**: đọc lại toàn bộ hội thoại + tool results, tóm tắt thành đoạn ngắn, vứt bỏ chi tiết. Đây là *lossy compression* — và lossy ở đây không phải tỉ lệ đều, mà thiên về vứt bỏ chi tiết "tưởng như không liên quan". Một constraint quan trọng bạn nói cách đây 50 prompt (ví dụ: "JWT secret rotate mỗi 7 ngày") có thể bị nén còn 1 dòng, hoặc biến mất hoàn toàn.

Tệ hơn: nếu một session bị auto-compact 2–3 lần liên tiếp, tác động dồn lại — Claude có "trí nhớ ngắn hạn của người mất trí". Mỗi vòng compact lại nén chính cái summary đã nén ở vòng trước, độ chi tiết giảm theo cấp số. Tương tự việc copy-paste một JPEG qua nhiều lần lưu lại: từng lần một nhìn vẫn ổn, nhưng dồn lại artifact xuất hiện ở mọi đường viền.

Hệ quả thực hành: **không phó mặc auto-compact**. Chủ động `/context` mỗi 30–45 phút, quyết định trước khi hệ thống quyết định thay. Trước khi compact thủ công, có thể "pin" decision quan trọng vào CLAUDE.md để dù tóm tắt có drop thì rule vẫn sống ở session sau.

## Liên hệ

- [[compact-khi-do-dang-clear-khi-doi-task]] — quy tắc chủ động thay auto-compact
- [[context-window-tai-nguyen-huu-han]] — nền tảng giải thích tại sao auto-compact tồn tại
- [[subagent-context-isolation-pattern]] — giảm tốc độ phình context → giãn khoảng cách giữa các lần auto-compact
- [[subagent-reviewer-bu-bias-cua-session-chinh]] — cùng họ "bias từ context tích lũy": note kia về bias do session dài, note này về mất nuance do compact dồn lại

## Nguồn

- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 khóa Claude Code 101 (bản tiếng Việt v1.0)
