---
type: claim
created: 2026-05-24
tags: [claude-code, skill, claude-md, context-management]
status: seed
confidence: high
---

# Luận điểm: Đặt vào CLAUDE.md nếu luôn relevant, đặt vào skill nếu chỉ relevant cho một loại task

## Lập luận ủng hộ

- CLAUDE.md **load mọi lúc** — bất kể bạn đang debug runtime bug hay review PR hay viết doc, toàn bộ nội dung ngồi trong context. Đẩy 200 dòng "PR review checklist" vào đây = bạn phải gánh 200 dòng đó cả khi debug.
- Skill **load on-demand** — Claude chỉ đọc tên + description (~200 token mỗi skill), chỉ load full body khi request match. 200 dòng PR checklist chỉ tốn 200 token cho tới khi bạn ask review.
- Quy tắc chuyển đổi rõ ràng: nếu nội dung *luôn relevant* (project layout, build command, code style, naming convention) → CLAUDE.md. Nếu chỉ *relevant cho 1 loại task cụ thể* (review checklist, commit message format, polish design checklist, deploy runbook) → skill.
- Hệ quả tốt thứ hai: skill ép bạn *đặt tên* và *mô tả* rõ task, giúp tổ chức kiến thức theo task chứ không phải theo project — dễ reuse hơn.

## Lập luận phản biện

- Skill phụ thuộc Claude nhận đúng intent để load — nếu mô tả skill không tốt, có thể không kích hoạt khi cần, dẫn tới Claude bỏ sót quy tắc quan trọng.
- Với content rất ngắn (5–10 dòng), overhead "Claude phải match intent" không xứng — đặt thẳng vào CLAUDE.md đơn giản và chắc chắn hơn.
- Người mới có thể bị overwhelm khi vừa phải duy trì CLAUDE.md vừa quản lý skill library — đôi khi gộp vào CLAUDE.md là pragmatic tradeoff.

## Quan điểm của tôi

Tin **high confidence**. Quy tắc này là cách rõ nhất để chia nội dung "luôn nhớ" vs "nhớ khi cần". Lưu ý của bài gốc đáng nhớ: *chỉ đưa vào CLAUDE.md những gì lặp lại ≥3 lần trong các session khác nhau* — đây là phép thử dễ áp dụng để quyết định.

Một insight phụ: skill cũng là một dạng "context isolation" giống [[subagent-context-isolation-pattern]] — nhưng isolation theo *thời điểm load* thay vì *thread*. Cả hai cùng giải quyết một bài toán nền: làm sao có nội dung lớn nhưng không phải gánh nó liên tục.

## Liên hệ

- [[subagent-context-isolation-pattern]] — pattern họ hàng: isolation theo thread; skill = isolation theo thời điểm load
- [[context-window-tai-nguyen-huu-han]] — nền tảng
- [[mcp-server-overhead-cost-truoc-prompt]] — tương phản: MCP load always (như CLAUDE.md), skill load on-demand
- [[compact-khi-do-dang-clear-khi-doi-task]] — sau /clear, CLAUDE.md re-load, skill chỉ load metadata → skill rẻ hơn nhiều lần lặp
- [[calibrate-workflow-claude-code-theo-task-size]] — cùng tinh thần "load đúng thứ đúng lúc thay vì luôn luôn"; calibrate setup theo nhu cầu

## Nguồn

- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 khóa Claude Code 101 (bản tiếng Việt v1.0), chiến thuật 4
