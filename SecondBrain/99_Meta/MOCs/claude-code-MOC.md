---
type: moc
topic: claude-code
updated: 2026-05-23
tags: [moc, claude-code, ai-workflow, prompt-engineering]
status: active
---

# 🗺️ Claude Code — Map of Content

> Tổng hợp tri thức về workflow làm việc với Claude Code: prompt engineering, EPCC, plan mode, review pattern, decision cost.

## 🌱 Khái niệm nền tảng

- [[subagent-reviewer-bu-bias-cua-session-chinh]] — Session chính tích bias "biết code đúng"; subagent fresh-context là cách rẻ nhất bù bias

## 🛠️ Phương pháp & kỹ thuật

- [[plan-mode-workflow-5-buoc]] — Plan Mode 5 bước: align với Claude trước, code sau, tránh rollback
- [[4-thanh-phan-cua-prompt-tot-claude-code]] — Prompt tốt cần đủ Context + Constraints + Success Criteria + Think Hard Trigger
- [[test-suite-bien-code-phase-thanh-vong-lap-tu-sua]] — Test suite reliable biến Code phase thành vòng lặp tự sửa, không cần human-in-the-loop
- [[calibrate-workflow-claude-code-theo-task-size]] — Mức độ rigid của EPCC scale theo task size, không có 1 workflow đúng cho mọi task

## 💭 Luận điểm đáng tranh luận

- [[cost-thay-doi-tang-theo-phase-trong-ai-workflow]] — Chi phí thay đổi tăng theo phase: $ Plan → $$ Code → $$$ sau commit
- [[tech-debt-o-leaf-node-co-the-chap-nhan]] — Tech debt ở leaf node (không ai depend vào) có thể chấp nhận; review effort dồn vào interfaces

## ❓ Câu hỏi mở

- *(chưa có)*

## 📚 Tài liệu tham khảo

*(Paper summaries liên quan — đặt ở `10_Projects/claude-code-101/sources/` hoặc `30_Resources/claude-code/`)*

- *(chưa có)*

## 📂 Project liên quan

- `10_Projects/claude-code-101/` — project học Claude Code

---

**Cách dùng MOC này:** Mọi atomic/resource liên quan Claude Code, AI coding workflow, prompt engineering → thêm link vào đúng section. MOC là điểm vào duy nhất cho chủ đề.
