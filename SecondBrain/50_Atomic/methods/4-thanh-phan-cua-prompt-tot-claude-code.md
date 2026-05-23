---
type: method
tags: [claude-code, prompt-engineering, checklist]
source: [[2026-claude-code-101-prompt-dau-tien]]
created: 2026-05-23
---

# Prompt Claude Code hiệu quả cần đủ 4 thành phần: Context, Constraints, Success Criteria, và Think Hard Trigger

Một prompt tốt không cần dài — cần **cụ thể**. Task càng lớn, càng cần đủ 4 thành phần:

**1. Context**
Cho Claude biết đang làm việc ở đâu: file nào, folder nào, function nào, dòng bao nhiêu.
- ❌ "Sửa bug authentication"
- ✅ "Hàm `verifyPassword()` trong `src/auth/login.ts` dòng 42-58"

**2. Constraints**
Giới hạn kỹ thuật và quy ước team: library được/không được dùng, style, bundle size, deadline.
- ✅ "Không dùng thư viện ngoài. Chỉ dùng Tailwind dark: variants + localStorage."

**3. Success Criteria**
Định nghĩa "done" rõ ràng — kết quả trông như thế nào, test nào phải pass.
- ✅ "Dark mode toggle hiển thị ở header. Unit test pass. Preference giữ lại khi reload."

**4. "Think Hard" Trigger** *(chỉ khi task phức tạp)*
Thêm vào cuối prompt để kích hoạt extended thinking:

| Trigger | Khi nào |
|---------|---------|
| `think hard` | Bug không rõ nguyên nhân |
| `think harder` | Task đặc biệt phức tạp |
| `ultrathink` | Architectural decision quan trọng |

**Nguyên tắc cốt lõi:** Mỗi prompt mạnh đều trả lời ngầm 3 câu hỏi: Claude cần đọc file nào? Constraint là gì? "Done" trông như thế nào?

## Bằng chứng / nguồn
- Từ [[2026-claude-code-101-prompt-dau-tien]], trang 10-11: "Prompt mạnh luôn trả lời 3 câu hỏi ngầm: Claude cần đọc file nào để hiểu vấn đề? Constraint là gì? 'Done' trông như thế nào?"

## Liên quan
- [[plan-mode-workflow-5-buoc]]
- [[subagent-reviewer-bu-bias-cua-session-chinh]]
- [[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]] — giải thích *tại sao* cần specific: prompt mơ hồ tốn ~25k token "thám tử", prompt cụ thể ~3k

## Câu hỏi mở
- Với task Easy (< 5 phút), có cần đủ 4 thành phần không, hay Context + Criteria là đủ?
