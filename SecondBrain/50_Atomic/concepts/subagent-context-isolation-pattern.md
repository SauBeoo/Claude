---
type: concept
created: 2026-05-24
tags: [claude-code, subagent, context-management, design-pattern]
status: seed
---

# Subagent là context isolation pattern

Subagent là một instance Claude chạy song song với main thread, có **context window 200k token riêng độc lập**. Bạn giao cho nó một task read-heavy (đọc 50 file để tìm TODO, đọc log MB để tìm error pattern, explore một module để hiểu kiến trúc), nó tiêu thụ context window *của riêng nó*, rồi trả về cho main thread *chỉ một đoạn summary*. Toàn bộ exploration chi tiết bị discard.

Đây là một dạng *context isolation pattern* — tương tự process isolation trong OS hay sandboxing trong browser: việc nặng được nhốt vào không gian riêng để không "lây nhiễm" sang không gian chính. Cùng họ với pattern "fresh eyes" của subagent reviewer ở EPCC commit phase — cả hai đều dựa trên nguyên tắc *chia tách trạng thái để giữ chất lượng quyết định*.

Quy tắc thực hành: **"answer without journey"** — khi bạn chỉ cần answer mà không cần xem journey (tìm endpoint nằm ở đâu, file nào dùng deprecated function, có security issue nào không), hãy outsource cho subagent. Khi bạn cần journey (đang implement feature, cần biết từng bước Claude làm gì để approve hoặc điều chỉnh), giữ trong main thread.

## Liên hệ

- [[subagent-reviewer-bu-bias-cua-session-chinh]] — case cụ thể của pattern này: dùng subagent fresh-context để review code bù bias session chính
- [[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]] — chiến thuật bổ sung; subagent dùng khi không thể cụ thể hóa prompt (cần exploration)
- [[compact-khi-do-dang-clear-khi-doi-task]] — subagent là cách *tránh* phải compact/clear sớm
- [[auto-compact-mat-nuance]] — subagent giúp main context không phình → giảm risk auto-compact mất nuance
- [[context-window-tai-nguyen-huu-han]] — nền tảng

## Nguồn

- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 khóa Claude Code 101 (bản tiếng Việt v1.0), chiến thuật 3
