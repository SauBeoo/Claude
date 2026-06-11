---
type: method
created: 2026-06-08
tags: [claude-code, workflow, epcc]
status: seed
---

# Calibrate EPCC theo kích cỡ task — workflow là công cụ, không phải nghi lễ

EPCC không phải nghi thức bắt buộc làm đủ 4 phase mọi lúc. Bạn **chỉnh liều** theo độ lớn của task:

| Task | Explore | Plan | Code | Commit |
|---|---|---|---|---|
| **Tiny** (sửa typo, đổi 1 hằng số) | bỏ | bỏ | nhanh | tối thiểu |
| **Easy** (thêm field, fix bug 1 file) | tùy | tùy | thường | tối thiểu |
| **Medium** (feature mới, refactor 1 module) | bắt buộc | bắt buộc | + test | review đầy đủ |
| **Hard** (đổi kiến trúc, cross-cutting) | mở rộng | nhiều vòng | chia phase + test | nhiều commit |
| **Massive** (modernize legacy, migrate) | nhiều ngày | nhiều ngày | chia phase theo tuần | commit từng phase |

Hai cái bẫy đối xứng: **full EPCC cho task tiny** (viết plan chi tiết để sửa 1 chữ — mất đà, nản) và **skip Plan cho task medium+** (đoán sai, rollback). Nguyên tắc: *"Workflow là công cụ, không phải nghi lễ"* — dùng đúng liều cho đúng việc.

## Liên hệ

- [[epcc-workflow-bon-phase]] — 4 phase mà bảng này điều chỉnh liều lượng
- [[3-task-framework-easy-medium-hard]] — cùng tư duy "đo theo task size", góc nhìn chọn ai-lái/chế-độ

## Nguồn

- Trích từ: [[2026-claude-code-101-epcc-workflow]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.4, "Bảng calibration" + Anti-pattern 5
