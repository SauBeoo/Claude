---
type: claim
created: 2026-05-24
tags: [claude-code, context-management, workflow]
status: seed
confidence: high
---

# Luận điểm: Đang dở task thì /compact, đổi task thì /clear — đừng nhầm hai lệnh

## Lập luận ủng hộ

- `/compact` giữ lại tóm tắt task hiện tại (decisions, file đang sửa, edge case đã thảo luận), chỉ vứt bỏ tool result chi tiết không còn cần — chính xác thứ ta muốn khi chưa xong task.
- `/clear` xóa toàn bộ hội thoại (chỉ giữ CLAUDE.md + system + MCP defs), về ~5–10k token — chính xác thứ ta muốn khi đổi task để Claude không bị "ám" bởi pattern task cũ.
- Nhầm `/clear` khi đang dở task = phải brief lại Claude từ đầu, tốn nhiều thời gian hơn một lần `/compact`. Mất quyết định đã đồng thuận = rủi ro lệch hướng cao.
- Nhầm `/compact` khi đã đổi task = tóm tắt task cũ vẫn ngồi trong context, bias Claude khi đề xuất design cho task mới (ví dụ: vừa fix auth xong, refactor DB lại bị "ám" bởi defensive try-catch).

## Lập luận phản biện

- Có trường hợp đang dở task nhưng task đã sai hướng nghiêm trọng → `/clear` rồi brief lại có thể *rẻ hơn* tiếp tục với context lệch. Quy tắc không phải tuyệt đối.
- Với model context window lớn (Opus 4.7 1M), áp lực phải compact giảm đáng kể, ranh giới giữa "đang dở" và "đổi task" trở nên ít quan trọng — có thể giữ nguyên không cần lệnh nào.

## Quan điểm của tôi

Tin **high confidence** — đây là heuristic có giá trị thực tế cao, phản trực giác đủ để đáng nhớ (vì người mới thường mặc định "context cao = clear cho sạch"). Edge case của model 1M không vô hiệu hóa quy tắc, chỉ giãn ngưỡng kích hoạt.

## Liên hệ

- [[auto-compact-mat-nuance]] — lý do không nên phó mặc auto-compact dẫn tới việc phải chủ động chọn compact/clear
- [[context-window-tai-nguyen-huu-han]] — nền tảng giải thích vì sao cần lệnh quản lý
- [[subagent-context-isolation-pattern]] — pattern bổ sung khi cần isolation thay vì compact/clear
- [[cost-thay-doi-tang-theo-phase-trong-ai-workflow]] — nhầm /clear khi đang dở = trả $$$ để brief lại; cùng nguyên tắc "chi phí điều chỉnh tăng theo giai đoạn"
- [[calibrate-workflow-claude-code-theo-task-size]] — cùng tinh thần "calibrate thay vì rule cứng"; workflow scale theo task size, quyết định compact/clear phụ thuộc trạng thái task

## Nguồn

- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 khóa Claude Code 101 (bản tiếng Việt v1.0)
