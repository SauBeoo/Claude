---
type: claim
created: 2026-06-08
tags: [claude-code, context-window, compact, clear]
status: seed
---

# Còn dở task thì `/compact`, đổi task thì `/clear`

Khi cái bàn làm việc của Claude Code sắp đầy, bạn có hai cách dọn — và chọn sai thì hoặc mất việc đang làm, hoặc giữ rác không cần:

- **`/compact`** = gom đống giấy tờ lại thành **một bản tóm tắt, GIỮ lại** mạch task hiện tại. Dùng khi **còn đang dở** một việc dài (token còn ~20–40k sau khi nén).
- **`/clear`** = **dọn sạch bàn**, chỉ chừa lại nội quy (CLAUDE.md + system). Dùng khi **xong hẳn / chuyển sang việc khác** (token còn ~5–10k).

**Quy tắc nhị phân để khỏi phải nghĩ:** *còn dở → compact · đổi task → clear.* Và cứ 30–45 phút gõ `/context` một lần để biết bàn đầy bao nhiêu.

Vì sao đừng phó mặc cho **auto-compact** (hệ thống tự dọn khi ~80%)? Vì nó dọn *âm thầm* và có thể vứt mất chi tiết quan trọng mà bạn không hay. Chủ động compact/clear đúng lúc = bạn kiểm soát cái gì được giữ, cái gì bỏ. Mục tiêu lý tưởng: số lần auto-compact = **0**.

Một cái bẫy: đừng `/clear` khi đang dở việc quan trọng — mất hết quyết định + file đang sửa + edge case đã bàn, brief lại từ đầu còn tốn hơn cả compact.

## Liên hệ

- [[context-window-tai-nguyen-huu-han]] — cái bàn mà 3 lệnh này dọn
- [[subagent-context-isolation-pattern]] — cách khác để khỏi phải dọn bàn: đừng bày lên bàn chính ngay từ đầu

## Nguồn

- Trích từ: [[2026-claude-code-101-quan-ly-context]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.5, "3 lệnh cầm cương" + "Quy tắc vàng"
