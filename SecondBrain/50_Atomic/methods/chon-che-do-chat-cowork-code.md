---
type: method
created: 2026-05-30
tags: [claude, claude-desktop, cowork]
status: seed
---

# Cách chọn chế độ Chat / Cowork / Code

Đừng dùng búa tạ để đập hạt dẻ, cũng đừng lấy kéo cắt cây. Chọn đúng "đồ nghề" theo việc.

## Khi nào dùng

Mỗi lần định giao một việc cho Claude trên Desktop và phân vân nên mở tab nào.

## Các bước

1. **Đếm số bước + xem loại việc:**
   - **≤ 3 bước, hỏi-đáp nhanh** → **Chat** (bạn lái từng bước).
   - **> 3 bước, hoặc cần đọc folder / dùng tool ngoài** → **Cowork** (giao mục tiêu, Claude lập plan + chạy).
   - **Đụng tới codebase** (sửa code, chạy test, commit) → **Code**.
2. **Việc lặp lại định kỳ?** → dùng Cowork **Scheduled Task**, đừng gõ tay mỗi lần.
3. **Luôn đọc & duyệt plan** trước khi để Cowork/Code chạy — đây là chỗ bạn lái.

## Lưu ý/cạm bẫy (anti-pattern)

- ❌ Mở Cowork chỉ để hỏi 1 câu → overhead plan/clarify làm chậm. Dùng Chat.
- ❌ Paste 10 file vào Chat rồi "phân tích hết" → Chat giới hạn context, không có subagent. Dùng Cowork + folder access.
- ❌ Dùng Code cho việc không phải dev (vd viết marketing copy) vì "thấy nó mạnh". Sai đồ nghề.
- ❌ Bấm approve plan mà không đọc → Claude đi sai hướng 30 phút mới biết.

## Ví dụ thực tế

- "Giải thích đoạn code này làm gì" → **Chat**.
- "Đọc 50 báo cáo trong /reports/, tổng hợp memo + bảng rủi ro" → **Cowork**.
- "Test fail ở branch X, tìm root cause, đề xuất fix, commit" → **Code**.

## Liên hệ

- [[3-che-do-claude-desktop]] — đặc tính từng mode
- [[scheduled-tasks-tu-dong-hoa-viec-lap]] — xử lý việc lặp
- [[delegate-repeatable-keep-judgment]] — quyết định giao việc nào trước khi chọn mode

## Nguồn

- Khoá Claude 101 (Anthropic Academy) — bài 1.4, "So sánh 3 chế độ" & "Anti-patterns khi chọn mode"
