---
type: moc
topic: claude-code
updated: 2026-05-24
tags: [moc, claude-code, ai-workflow, prompt-engineering]
status: active
---
2
# 🗺️ Claude Code — Map of Content

> Tổng hợp tri thức về workflow làm việc với Claude Code: prompt engineering, EPCC, plan mode, review pattern, decision cost.

## 🌱 Khái niệm nền tảng

- [[subagent-reviewer-bu-bias-cua-session-chinh]] — Session chính tích bias "biết code đúng"; subagent fresh-context là cách rẻ nhất bù bias
- [[context-window-tai-nguyen-huu-han]] — Context window là toàn bộ bộ nhớ làm việc của LLM agent — cố định, hữu hạn, mọi thứ đều chiếm slot
- [[subagent-context-isolation-pattern]] — Subagent có context window riêng độc lập; dùng để offload read-heavy task mà không tốn context main thread
- [[auto-compact-mat-nuance]] — Auto-compact là lossy compression — constraint quan trọng có thể bị vứt bỏ, không nên phó mặc

## 🛠️ Phương pháp & kỹ thuật

- [[plan-mode-workflow-5-buoc]] — Plan Mode 5 bước: align với Claude trước, code sau, tránh rollback
- [[4-thanh-phan-cua-prompt-tot-claude-code]] — Prompt tốt cần đủ Context + Constraints + Success Criteria + Think Hard Trigger
- [[test-suite-bien-code-phase-thanh-vong-lap-tu-sua]] — Test suite reliable biến Code phase thành vòng lặp tự sửa, không cần human-in-the-loop
- [[calibrate-workflow-claude-code-theo-task-size]] — Mức độ rigid của EPCC scale theo task size, không có 1 workflow đúng cho mọi task

## 💭 Luận điểm đáng tranh luận

- [[cost-thay-doi-tang-theo-phase-trong-ai-workflow]] — Chi phí thay đổi tăng theo phase: $ Plan → $$ Code → $$$ sau commit
- [[tech-debt-o-leaf-node-co-the-chap-nhan]] — Tech debt ở leaf node (không ai depend vào) có thể chấp nhận; review effort dồn vào interfaces
- [[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]] — Prompt cụ thể dài hơn nhưng cắt đi nhiều vòng làm rõ, tổng context tiêu tốn ít hơn
- [[compact-khi-do-dang-clear-khi-doi-task]] — /compact khi đang dở task giữ context liên tục; /clear khi đổi task tránh nhiễu từ session cũ
- [[skill-on-demand-vs-claudemd-always]] — CLAUDE.md cho context luôn cần; skill cho context chỉ cần khi làm loại task cụ thể
- [[mcp-server-overhead-cost-truoc-prompt]] — MCP server tốn context ngay khi load — overhead này ăn vào budget trước cả khi gõ prompt đầu tiên

## ❓ Câu hỏi mở

- *(chưa có)*

## 📚 Tài liệu tham khảo

*(Paper summaries liên quan — đặt ở `10_Projects/claude-code-101/sources/` hoặc `30_Resources/claude-code/`)*

- *(chưa có)*

## 📂 Project liên quan

- `10_Projects/claude-code-101/` — project học Claude Code

---

**Cách dùng MOC này:** Mọi atomic/resource liên quan Claude Code, AI coding workflow, prompt engineering → thêm link vào đúng section. MOC là điểm vào duy nhất cho chủ đề.
