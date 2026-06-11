
\
type: claim
created: 2026-06-08
tags: [claude-code, workflow, plan-mode]
status: seed
---

# Sửa càng muộn càng đắt: $ → $$ → $$$ theo phase

Chi phí của một thay đổi **tăng vọt** theo việc bạn phát hiện nó ở phase nào:

```
Sửa trong phase Plan:    $    (chỉnh vài chữ trong plan)
Sửa trong phase Code:    $$   (rollback code, viết lại)
Sửa sau khi Commit:      $$$  (revert PR, re-review, re-test)
```

Đây là lý do kinh tế khiến **Plan Mode đáng giá**: nó cho bạn phát hiện sai hướng *khi sửa còn rẻ nhất* — lúc plan mới chỉ là chữ, chưa thành code, chưa lên PR. Một vòng revise plan tốn 1–2 phút; cũng sai lầm đó để lọt tới sau commit thì tốn hàng giờ revert.

Hệ quả thực hành: đừng tiếc 10 phút Plan. 10 phút đó thường cắt 30–90 phút debug về sau.

## Liên hệ

- [[epcc-workflow-bon-phase]] — vì sao Plan (~30%) đáng được đầu tư
- [[3-permission-modes-claude-code]] — Plan Mode read-only là chỗ "sửa giá $"

## Nguồn

- Trích từ: [[2026-claude-code-101-epcc-workflow]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.4, "Plan — nơi rẻ nhất để course-correct"
