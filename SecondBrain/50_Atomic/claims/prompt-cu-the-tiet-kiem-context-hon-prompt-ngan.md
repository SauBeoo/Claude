---
type: claim
created: 2026-05-24
tags: [claude-code, prompting, context-management]
status: seed
confidence: high
---

# Luận điểm: Prompt cụ thể tiết kiệm context hơn prompt ngắn

## Lập luận ủng hộ

- Prompt mơ hồ ("sửa cái bug auth") buộc Claude làm thám tử: đọc 10+ file `src/auth/*`, grep "auth" toàn project, đọc test để đoán "bug là gì" → ~25k token chỉ để hiểu yêu cầu.
- Prompt cụ thể (file + dòng + nguyên nhân + cách fix mong muốn) ~3k token là đủ để Claude vào việc thẳng. Tiết kiệm ~20k token = 10% context window mặc định.
- 30 giây gõ specific = đỡ Claude 20–30 lần file read. Tỉ lệ đầu tư rất cao.
- Hệ quả phụ: prompt cụ thể giảm risk Claude *đoán sai* và làm lệch → tiết kiệm cả thời gian sửa lại.

## Lập luận phản biện

- Có trường hợp ta thực sự chưa biết bug ở đâu — exploration là việc phải làm, không phải lãng phí. Prompt cụ thể giả định người gõ đã localize được vấn đề.
- Prompt quá dài có thể trở thành noise: nếu nhồi cả context không liên quan ("project dùng pnpm... team theo flow gitlab...") → cũng tốn token vô nghĩa. Cụ thể ≠ dài.
- Với task khám phá kiến trúc (CS student vào codebase mới), prompt cụ thể không khả thi — phải dùng subagent thay vì cố cụ thể hóa.

## Quan điểm của tôi

Tin **high confidence** cho 80% task hàng ngày của dev. Đây là điều phản trực giác nhất trong bài 2.5 — nhiều người mặc định "prompt ngắn = ít token = tiết kiệm". Sai ở chỗ: token tiết kiệm ở prompt bị trả ngược (gấp 8–10 lần) ở giai đoạn Claude tự tìm hiểu.

Quy tắc của tôi: nếu đã biết file + dòng → luôn gõ ra. Nếu chưa biết → dùng [[subagent-context-isolation-pattern]] để khám phá.

## Liên hệ

- [[4-thanh-phan-cua-prompt-tot-claude-code]] — định nghĩa *thế nào* là specific (Context + Constraints + Success Criteria + Think Hard); note này giải thích *tại sao* cần specific (context cost)
- [[subagent-context-isolation-pattern]] — pattern thay thế khi prompt cụ thể không khả thi (cần exploration)
- [[context-window-tai-nguyen-huu-han]] — nền tảng giải thích vì sao token tiết kiệm có giá trị
- [[compact-khi-do-dang-clear-khi-doi-task]] — chiến thuật phòng thủ; prompt cụ thể là chiến thuật tấn công
- [[plan-mode-workflow-5-buoc]] — hệ quả thực hành: align trước khi code thay vì để Claude đoán

## Nguồn

- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 khóa Claude Code 101 (bản tiếng Việt v1.0)
