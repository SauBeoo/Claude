---
type: moc
topic: claude-code
updated: 2026-06-08
tags: [moc, claude-code, anthropic]
status: active
---

# 🗺️ Claude Code — Vận hành chuyên nghiệp — Map of Content

> Tri thức chắt từ khoá **Claude Code 101** (gốc Anthropic, bản tiếng Việt).
> Project: [[../../10_Projects/claude-code-101/README|claude-code-101]] · Hệ sinh thái Claude.ai nói chung → [[claude-MOC]]

## 📝 Bài 2.3 — Prompt Đầu Tiên
- [[prompt-la-brief-khong-phai-command]] — prompt là bản brief cho kỹ sư mới, không phải câu lệnh
- [[4-thanh-phan-prompt-tot]] — Context + Constraints + Success + "think hard"
- [[3-permission-modes-claude-code]] — Default / Auto Accept / Plan Mode (Shift+Tab)
- [[3-task-framework-easy-medium-hard]] — Easy/Medium/Hard → ai cầm lái + chế độ nào

## 🔄 Bài 2.4 — Workflow EPCC
- [[epcc-workflow-bon-phase]] — Explore→Plan→Code→Commit, 50% nửa đầu là đầu tư
- [[cost-thay-doi-tang-theo-phase]] — sửa càng muộn càng đắt: $ → $$ → $$$
- [[test-suite-source-of-truth-voi-ai]] — test là nguồn chân lý, Code phase tự sửa
- [[claude-code-subagent-fresh-eyes]] — subagent reviewer không dính bias session
- [[calibrate-workflow-theo-task-size]] — chỉnh liều EPCC theo tiny→massive
- [[tech-debt-leaf-node-acceptable]] — nợ kỹ thuật ở leaf node thì chấp nhận được

## 🧠 Bài 2.5 — Quản lý Context
- [[context-window-tai-nguyen-huu-han]] — bộ nhớ làm việc 200k token, tài nguyên quan trọng nhất
- [[subagent-context-isolation-pattern]] — cử trợ lý có bàn riêng, mang về mỗi câu trả lời
- [[compact-khi-do-dang-clear-khi-doi-task]] — còn dở thì `/compact`, đổi task thì `/clear`
- [[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]] — prompt cụ thể (dài hơn) lại tốn ít context
- [[mcp-server-overhead-cost-truoc-prompt]] — mỗi MCP server ăn 2–15k token trước khi gõ prompt

## ❓ Câu hỏi mở
- *(chưa có)*

## 📚 Nguồn (source notes của project)
- [[2026-claude-code-101-prompt-dau-tien]] — Bài 2.3 ✅ đã chắt 4 atomic
- [[2026-claude-code-101-epcc-workflow]] — Bài 2.4 ✅ đã chắt 6 atomic
- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 ✅ đã chắt 5 atomic

---

**Cách dùng:** Mọi atomic/resource về Claude Code → thêm vào đúng bài. Mở một source note + bật **Local Graph** để thấy nó đẻ ra atomic nào.
