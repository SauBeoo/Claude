---
type: concept
tags: [claude-code, code-review, ai-bias, subagent]
source: [[2026-claude-code-101-epcc-workflow]]
created: 2026-05-23
status: seed
---

# Claude trong session viết code có bias "biết code đúng" — subagent reviewer fresh-context là cách rẻ nhất bù bias đó

**Quan sát**: Khi Claude đã ở trong 1 session từ đầu — đọc files, lập plan, viết code — nó tích lũy **bias**: nó "biết" code đó đúng vì chính nó viết. Bias này không phải lỗi của Claude — là hệ quả tất yếu của context window đầy thông tin "đã quyết định".

**Cơ chế subagent reviewer**:
- Spawn subagent với context window **độc lập** (không có history session chính).
- Subagent chỉ đọc git diff + related tests + CLAUDE.md.
- Trả về: summary changes, potential bugs, missing edge cases, code style violations, recommendation approve/sửa.

**Tại sao hoạt động**: Subagent bắt đầu *fresh*, không có sunk cost cognitive của session chính. Nó có thể nhìn code như reviewer thực thụ — không bị thuyết phục bởi "logic đã thảo luận 30 phút trước".

**Khi nào dùng**:
- Trước mọi commit của task medium+.
- Đặc biệt critical với code security/payment/auth.
- 5 phút review subagent thường catch bug mà 2 tiếng code session chính bỏ qua.

**Nguyên tắc rộng hơn**: Đây là phiên bản AI của "fresh pair of eyes" trong human code review. Argument không phụ thuộc AI — bias của session-có-context cũng tồn tại ở human developer sau khi đã code 4 tiếng liền. Sự khác biệt: spawn subagent rẻ và nhanh hơn nhiều so với kéo đồng nghiệp review.

## Bằng chứng / nguồn
- Từ [[2026-claude-code-101-epcc-workflow]], trang 12: "Claude đã ở trong session đó từ đầu. Nó có bias — nó đã viết code đó, nó 'biết' code đó 'đúng'. Subagent reviewer bắt đầu fresh, không có bias đó."

## Liên quan
- [[tech-debt-o-leaf-node-co-the-chap-nhan]]
- [[4-thanh-phan-cua-prompt-tot-claude-code]]
- [[subagent-context-isolation-pattern]] — generalization: pattern rộng hơn (context isolation), note này là case cụ thể (reviewer)
- [[auto-compact-mat-nuance]] — cùng gốc nguyên nhân: bias từ context tích lũy; auto-compact mất nuance là dạng khác của vấn đề
- [[context-window-tai-nguyen-huu-han]] — nền tảng: bias chỉ tồn tại vì context hữu hạn và tích lũy

## Câu hỏi mở
- Subagent có bias riêng của nó không (vd: prompt đã frame "tìm bug" sẽ làm subagent over-report false positives)?
