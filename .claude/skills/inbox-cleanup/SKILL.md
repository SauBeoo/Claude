---
name: inbox-cleanup
description: Sử dụng skill này khi cần dọn dẹp thư mục 00_Inbox của vault, phân loại các file đang chờ vào đúng PARA folder. Trigger khi user nói "dọn inbox", "phân loại inbox", "Inbox đầy quá".
---

# Skill: Inbox Cleanup

Dọn thư mục `00_Inbox/` định kỳ, phân loại file đi đâu.

## Khi nào dùng

- User yêu cầu trực tiếp ("dọn inbox", "Inbox đầy")
- Định kỳ cuối tuần (nếu user setup auto)
- Khi librarian agent audit vault phát hiện Inbox quá 10 file

## Quy trình

### Bước 1: Scan Inbox

```bash
ls E:\Claude\SecondBrain\00_Inbox\ -R
```

Liệt kê:
- Tên file
- Ngày tạo
- Kích thước
- Loại (PDF/MD/PNG/...)

### Bước 2: Đọc nội dung từng file

Với mỗi file:
- PDF → đọc abstract/đầu trang
- MD → đọc full
- PNG/JPG → mô tả (nếu là screenshot)
- Audio → bỏ qua, đề xuất user xử lý riêng

### Bước 3: Phân loại theo skill vault-routing

Áp dụng bảng quyết định trong `vault-routing/SKILL.md`.

### Bước 4: Tổng hợp thành bảng đề xuất

Output cho user:

```
📥 Inbox status: 8 files

| # | File | Loại | Đề xuất đích | Lý do |
|---|------|------|--------------|-------|
| 1 | paper-llm-feedback.pdf | PDF | 10_Projects/research-llm-education-2026/papers/ | Liên quan project research |
| 2 | y-tuong-buoi-mo-dau.md | MD | 20_Areas/teaching/ideas/ | Kinh nghiệm giảng dạy |
| 3 | screenshot-tweet.png | PNG | 30_Resources/machine-learning/ | Tham khảo về ML |
| ... |

⚠️ 2 file không chắc đặt đâu:
- voice-memo-2026-05-20.m4a: chưa transcribe, đề xuất bỏ qua lần này
- random-link.md: nội dung không rõ chủ đề, đề xuất xóa hoặc giữ thêm 1 tuần

Confirm để move? (y/n/chỉnh sửa)
```

### Bước 5: Move sau khi user xác nhận

- Dùng `mv` (Windows: `move`), KHÔNG `cp` rồi `rm`
- Move xong, báo cáo:
```
✅ Đã move 6/8 file. Inbox còn 2 file (chưa xử lý).
```

### Bước 6: Đề xuất follow-up

```
📝 Đề xuất tiếp theo:
- File #1 (paper) → muốn tóm tắt luôn không? (gọi skill summarize-pdf-paper)
- File #2 (ý tưởng giảng) → muốn mở rộng thành atomic method không?
```

## Nguyên tắc

1. **Bắt đầu từ file lâu nhất.** File ở Inbox >7 ngày = ưu tiên dọn trước.
2. **Không tự xóa.** Kể cả file rác — đề xuất user xóa, không tự `rm`.
3. **Không move file user chưa xem.** Nếu file mới <24h, có thể user đang xử lý.
4. **Đề xuất hơn áp đặt.** "Tôi nghĩ X" thay vì "Nên X".

## Báo cáo cuối

```
📊 Inbox cleanup report:
   - Trước: 8 files
   - Sau: 2 files (giữ lại)
   - Moved: 6 files
   - Cleanup time: 5 phút

📁 Distribution:
   - 10_Projects: 3
   - 20_Areas: 1
   - 30_Resources: 2
```
