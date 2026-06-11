---
type: concept
created: 2026-06-08
tags: [claude-code, permission-mode, plan-mode]
status: seed
---

# 3 chế độ quyền của Claude Code: Default / Auto Accept / Plan

Claude Code cho bạn 3 mức "dây cương" về việc nó được tự ý làm gì — gạt qua lại bằng **Shift+Tab**:

| Chế độ | Hành vi | Hợp với |
|---|---|---|
| **Default (Approval)** | Hỏi xác nhận **từng** lần sửa file / chạy lệnh | Branch production, lần đầu dùng, task nhạy cảm (auth/payment) |
| **Auto Accept** | Tự duyệt sửa file, vẫn hỏi khi chạy shell | Sandbox / dev branch đã tách, plan đã review |
| **Plan Mode** | **Read-only**: chỉ đọc/phân tích, trả về plan, không sửa gì | Task phức tạp, cần align trước khi code |

Ý quan trọng nhất là **Plan Mode**: nó *khóa tay* Claude ở chế độ chỉ-đọc, nên Claude không thể "lỡ tay" bắt đầu viết code giữa chừng — bạn duyệt plan xong mới thả cho nó chạy. Quy tắc nhanh: task < 5 phút → Default/Auto Accept; task > 30 phút hoặc chạm nhiều file → **Plan Mode trước**.

## Liên hệ

- [[3-task-framework-easy-medium-hard]] — chọn chế độ nào theo độ khó của task
- [[epcc-workflow-bon-phase]] — Plan Mode là công cụ của phase Plan

## Nguồn

- Trích từ: [[2026-claude-code-101-prompt-dau-tien]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.3, "3 Permission Modes"
