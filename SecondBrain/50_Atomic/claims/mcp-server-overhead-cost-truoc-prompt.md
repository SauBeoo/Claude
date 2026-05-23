---
type: claim
created: 2026-05-24
tags: [claude-code, mcp, context-management, tooling]
status: seed
confidence: high
---

# Luận điểm: MCP server overhead là chi phí ăn vào context TRƯỚC khi bạn gõ prompt đầu tiên

## Lập luận ủng hộ

- Mỗi MCP server load *toàn bộ* tool definitions vào context khi session start, **không phải on-demand**. Một server có thể tốn 2–15k token chỉ cho schema.
- Số liệu cụ thể từ ví dụ trong tài liệu: 12 server connected = ~50k token = 25% context window đã bị tiêu thụ *trước khi* user gõ ký tự đầu tiên.
- Khác với CLAUDE.md (load luôn nhưng thường nhỏ và relevant), MCP overhead có thể *hoàn toàn vô nghĩa* trong session đó (figma server bật khi không design, jira server bật khi team đã chuyển công cụ).
- Giải pháp clean: `.mcp.json` per-project enable đúng những server thực sự cần. Disable rộng rãi mặc định, cài lại khi cần — rẻ hơn để context bị ăn mòn liên tục.

## Lập luận phản biện

- Tính năng "MCP tool search mode" (Claude Code tự switch sang load on-demand khi server vượt 10% context) làm giảm áp lực này — nếu stable thì lập luận "ăn trước prompt" yếu đi.
- Một số MCP server có schema rất gọn (~2k) hoặc rất cần thiết (linear, slack cho team dùng hàng ngày) → tắt mặc định có thể gây ma sát workflow.
- Với context window 1M (Opus 4.7), 50k overhead = 5% — không còn cấp thiết phải tối ưu.

## Quan điểm của tôi

Tin **high confidence** cho user dùng default 200k context và bật MCP "phòng khi cần". Quy tắc đáng nhớ: **MCP là chi phí cố định, không phải biến**. Đầu session bạn đã trả tiền cho mọi server, dù dùng hay không. Vì vậy hãy treat MCP list như package.json của session — chỉ cài cái thực sự dùng.

Với context 1M, áp lực giảm nhưng quy tắc vẫn đúng về *hygiene* — không có lý do mang theo schema không liên quan.

## Liên hệ

- [[context-window-tai-nguyen-huu-han]] — nền tảng giải thích vì sao 50k overhead là vấn đề
- [[skill-on-demand-vs-claudemd-always]] — tương phản: skill load on-demand, MCP load always (trừ tool search mode)
- [[compact-khi-do-dang-clear-khi-doi-task]] — sau /clear, MCP overhead vẫn còn → cần disable trước session
- [[cost-thay-doi-tang-theo-phase-trong-ai-workflow]] — cùng họ "cost của setup giai đoạn sớm": MCP bật là quyết định ở phase setup, ăn vào mọi prompt sau đó

## Nguồn

- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 khóa Claude Code 101 (bản tiếng Việt v1.0), chiến thuật 5
