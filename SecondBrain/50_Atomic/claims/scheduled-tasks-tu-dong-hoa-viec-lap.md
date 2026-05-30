---
type: claim
created: 2026-05-30
tags: [claude, cowork, automation, scheduled-tasks]
status: seed
confidence: high
---

# Luận điểm: Việc lặp định kỳ thì setup Scheduled Task, đừng gõ tay mỗi lần

Nếu sáng nào bạn cũng gõ lại y nguyên một prompt ("tổng hợp lịch + email + Slack cho tôi"), bạn đang lãng phí. Cowork cho phép định nghĩa task + lịch **một lần** → Claude tự chạy mỗi ngày/tuần/tháng. Việc của bạn chuyển từ "làm admin mỗi sáng" sang "mở mắt đã có sẵn câu trả lời".

## Lập luận ủng hộ

- Toán đơn giản: 5 phút gõ tay/ngày = ~25 giờ/năm cho *đúng một* task. Setup 1 lần xoá sạch khoản này.
- Máy tắt lúc đến giờ? Claude catch-up khi bạn mở lại — không mất task.
- Kết hợp subagent + skill → task tự động hoá thực thụ, không chỉ nhắc việc.

## Lập luận phản biện

- Chỉ đáng setup khi task *thật sự lặp* và prompt đã ổn định; task hay đổi yêu cầu thì gõ tay linh hoạt hơn.
- Vẫn cần review output định kỳ (diligence) — "tự chạy" không có nghĩa "khỏi kiểm".

## Quan điểm của tôi

Tin cao. Đây là "killer feature" ít người dùng đủ. Quy tắc: thấy mình làm cùng một setup ≥3 lần → dừng lại, tự động hoá.

## Liên hệ

- [[chon-che-do-chat-cowork-code]] — Scheduled Task nằm trong nhánh Cowork
- [[delegate-repeatable-keep-judgment]] — việc lặp/có pattern là ứng viên tự động hoá

## Nguồn

- Khoá Claude 101 (Anthropic Academy) — bài 1.4, "Scheduled tasks (killer feature)"
