---
type: learning-track
created: 2026-05-30
updated: 2026-06-03
subject: "Claude 101 — làm chủ hệ sinh thái Claude"
source: "E:\\Claude\\SecondBrain\\00_Inbox\\Anthropic courses\\01 - Claude 101 (17 PDF)"
level_start: "intermediate"   # đã rành agent/Claude Code, chưa chuyên sâu hệ sinh thái Claude.ai
goal: "Hiểu để dùng việc + dạy lại được cho người khác"
tags: [claude, ai-fluency, anthropic, learning]
status: learning
---

# Lộ trình học: Claude 101 — làm chủ hệ sinh thái Claude

> **Nguồn gốc:** Khoá Claude 101 (bản tiếng Việt chuyên sâu v2.0), 14 bài / 5 module — Anthropic Academy
> **Mục tiêu:** Hiểu đủ sâu để dùng trong công việc IT/giảng dạy *và dạy lại* cho người khác
> **Trình độ xuất phát:** Trung cấp — đã rành agent & Claude Code, chưa chuyên sâu hệ sinh thái Claude.ai/Desktop

## Bản đồ kiến thức (roadmap)

Các module sắp theo thứ tự phụ thuộc. Trạng thái: ⬜ chưa học · 🟡 đang học · ✅ đã thạo · 🔁 cần ôn lại

| # | Module / Bài | Trạng thái | Buổi học | Atomic notes | Flashcards |
|---|--------------|-----------|----------|--------------|------------|
| 1 | Claude là gì + nền tư duy (1.1–1.2): Constitutional AI, steerable, C-T-R | ⏭️ bỏ qua (đã biết) | - | - | - |
| 2 | **AI Fluency: 4D Framework + Iteration + Eval (1.3)** ⭐ | ✅ đã thạo | Buổi 1 | 5 | 7 |
| 3 | Môi trường: Chat / Cowork / Code (1.4) | ✅ đã thạo | Buổi 2 | 4 | 6 |
| 4 | Tổ chức việc: Projects + Artifacts + Skills (1.5–1.7) ⭐ | ✅ đã thạo | Buổi 3 | 4 | 6 |
| 5 | Mở rộng: Connectors/MCP + Enterprise Search + Research (1.8–1.10) | ✅ đã thạo | Buổi 4 | 4 | 7 |
| 6 | Thực chiến + Tổng kết + Tự kiểm tra (1.11–1.14) | ⬜ | - | - | - |

## Nhật ký buổi học

### Buổi 1 — 2026-05-30 — AI Fluency: 4D Framework + Iteration + Eval
- **Đã dạy:** 4D Framework (Delegation/Description/Discernment/Diligence); Iteration mindset (prompt đầu = nháp junior, feedback cụ thể, khi nào restart); Delegation-Diligence loop + Eval.
- **Bài tập / kết quả:** (1) Áp 4D vào việc review code — nắm tốt Delegation + Diligence, cài checkpoint "xin xác nhận trước khi sửa". (2) Rewrite feedback mơ hồ → cụ thể: tốt về cấu trúc, còn thiếu ràng buộc độ dài. (3) Feynman phản biện "cứ tin AI" — chắc, bật ra gần đủ loop.
- **Điểm user chưa chắc:** mắt xích "phải có ground truth (data cũ đã biết đáp án) thì mới đo được đúng/sai" — hiểu sau khi siết; ràng buộc độ dài/format khi iterate hay quên.
- **Atomic tạo:** [[4d-framework-ai-fluency]], [[output-troi-chay-khong-dong-nghia-dung]], [[delegation-diligence-loop]], [[feedback-cu-the-khi-iterate-ai]], [[delegate-repeatable-keep-judgment]]
- **Flashcards thêm:** 7 thẻ

### Buổi 2 — 2026-05-30 — Môi trường: Chat / Cowork / Code
- **Đã dạy:** 3 chế độ Claude Desktop (1 trí tuệ); Chat vs Cowork (ai lái / đơn vị việc / output); Cowork & Code chung engine Claude Code nhưng khác phạm vi; Ask/Code/Plan; quy tắc chọn mode + anti-patterns; Scheduled Tasks/subagents.
- **Bài tập / kết quả:** (1) Ví dụ Chat vs Cowork — Chat chuẩn; ví dụ Cowork thực ra nghiêng Code (đụng codebase) → dùng để dạy ranh giới Cowork/Code. (2) Feynman anti-pattern "gõ lại daily brief" — chỉ đúng fix (Scheduled Task) + automation bằng subagent/skill.
- **Điểm user chưa chắc:** ranh giới **Cowork vs Code** (việc đụng codebase → Code, không phải Cowork) — đã làm rõ trong buổi, cần theo dõi.
- **Atomic tạo:** [[3-che-do-claude-desktop]], [[cowork-code-chung-engine-agentic]], [[chon-che-do-chat-cowork-code]], [[scheduled-tasks-tu-dong-hoa-viec-lap]]
- **Flashcards thêm:** 6 thẻ

### Buổi 3 — 2026-05-30 — Tổ chức việc: Projects + Artifacts + Skills ⭐
- **Đã dạy:** "Projects store knowledge, Skills perform tasks" (WHAT/HOW, bổ trợ); Project instructions như code + retrieve bằng tên file + knowledge vs conversation + RAG; Skills progressive disclosure (tie với `/context`), built-in vs custom, tạo qua hội thoại, portable; khi nào KHÔNG tạo skill; Artifacts (6 loại, iterate từng bước, reusable template, test logic).
- **Bài tập / kết quả:** (1) Ôn Cowork/Code: đúng cả a/b. (2) Phân biệt Project/Skill: đúng bản chất, ánh xạ chuẩn vào vault. (3) Viết instruction IF/THEN ELI5 — tốt, lấy từ CLAUDE.md. (4) Feynman skill chung chung: ban đầu nói "đáng tạo", đã siết lại → generic thì KHÔNG tạo, chỉ tạo khi có methodology cụ thể.
- **Điểm user chưa chắc:** anti-pattern "skill quá generic" — phản xạ đầu là "đáng tạo"; cần nhớ generic = dùng prompt, đừng tạo skill.
- **Atomic tạo:** [[projects-store-knowledge-skills-perform-tasks]], [[progressive-disclosure-skills]], [[instructions-project-nhu-code]], [[artifacts-output-tuong-tac]]
- **Flashcards thêm:** 6 thẻ

### Buổi 4 — 2026-06-03 — Mở rộng: Connectors/MCP + Enterprise Search + Research
- **Đã dạy:** Connectors giết vai middleware (read + take action); MCP = "USB-C cho AI" (chuẩn mở, ai cũng viết MCP server); 2 loại connector (web/desktop extension); security 4 nguyên tắc (scoped, you-see-what-you-see, revocable, review code untrusted); Enterprise Search = pre-built Project cho org, 2-step setup (admin configure / user authenticate riêng); Research mode agentic multi-step + decision tree 4 tools; craft prompt 5 phần; meta-prompt nhờ Claude draft trước khi Research.
- **Bài tập / kết quả:** (1) Ôn đầu buổi 2/3: skill generic ✓ (nhớ "quy trình"), Cowork/Code ✗ (đoán thêm điều kiện sai — lần 2), ground truth ✓ (thiếu ý mẫu đủ lớn). (2) Decision tree 4 tools: **4/4 đúng**. (3) MCP server cho tool nội bộ — suy ra được sau scaffold USB-C. (4) Research prompt: ban đầu thiếu hẳn SECTIONS + CITATIONS; sau khi hạ độ khó ("section = câu hỏi cho quyết định") tự viết được 3 sections tốt; vẫn quên đưa 3 tính năng bắt buộc thành section check.
- **Điểm user chưa chắc:** (a) Phản xạ "đọc được TOÀN BỘ hệ thống" — nói sai 2 lần trong buổi, ngược nguyên tắc you-see-what-you-see; (b) Cowork vs Code vẫn lung lay (lần 2); (c) Viết [SECTIONS] từ quyết định — mới vỡ ra trong buổi, cần luyện thêm.
- **Atomic tạo:** [[mcp-usb-c-cho-ai]], [[claude-chi-thay-cai-ban-thay]], [[chon-tool-theo-cau-hoi]], [[nho-ai-draft-prompt-truoc-khi-research]]
- **Flashcards thêm:** 7 thẻ

## Ôn buổi sau (đầu Buổi 5)
- [ ] (Buổi 4 — vấp 2 lần) "You see what you see": connector/Enterprise Search có đọc được "toàn bộ hệ thống" không? Vì sao không?
- [ ] (Buổi 2 — vấp 2 lần) Cowork vs Code: đụng codebase → Code, không có điều kiện phụ.
- [ ] (Buổi 4) Sections của Research prompt sinh ra từ đâu khi mù domain?

## Điểm yếu cần củng cố (carry-over)

- [x] Iterate: ràng buộc độ dài/format — ✅ tự nhớ ở Buổi 4 (ghi "500 từ" không cần nhắc), xóa sổ.
- [x] Delegation-Diligence loop: test trên data cũ có đáp án — ✅ ôn đầu Buổi 2 + Buổi 4, đã chắc.
- [x] Anti-pattern "skill quá generic" — ✅ ôn đầu Buổi 4, nhớ đúng chữ "quy trình/methodology".
- [ ] Cowork vs Code — ✗ sai lần 2 ở Buổi 4 (tự chế điều kiện "test xong mới dùng Cowork"). Ôn lại Buổi 5.

## Ý tưởng mở rộng / câu hỏi mở

- Liên hệ 4D Framework với cách bạn đang dùng Claude Code (agent, subagent) — buổi 3/5.
- So sánh Delegation-Diligence loop với "eval" trong dev workflow thực tế của bạn.
