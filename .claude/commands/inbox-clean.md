---
description: Dọn 00_Inbox theo quy tắc PARA, không xóa - chỉ archive
argument-hint: (không cần argument)
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Dọn dẹp Inbox

Sử dụng agent **librarian**. Trả lời bằng tiếng Việt.

## Quy tắc bất biến
- ❌ KHÔNG xóa file nào — chỉ di chuyển
- ❌ KHÔNG tự ý phân loại — luôn đề xuất, chờ tôi duyệt
- ✅ Mọi thứ quá 7 ngày trong Inbox phải có quyết định

## Việc cần làm

### Bước 1: Liệt kê

Quét `E:\Claude\SecondBrain\00_Inbox\`. Với mỗi file:

```
| # | Tên file | Tuổi (ngày) | Loại | Tóm tắt 1 dòng |
```

Highlight:
- 🔴 Quá 7 ngày
- 🟡 3-7 ngày
- 🟢 Mới

### Bước 2: Đề xuất phân loại

Với mỗi file, đề xuất ĐÚNG 1 đích đến:

| Đích | Khi nào |
|------|---------|
| `10_Projects/<X>/` | Có deadline, kết quả cụ thể, đang làm |
| `20_Areas/<role>/` | Kinh nghiệm dài hạn theo vai trò |
| `30_Resources/<topic>/` | Tham khảo từ người khác, chưa chắt lọc |
| `50_Atomic/` | Đã là 1 ý cô đọng (hiếm khi từ Inbox) |
| `40_Archive/` | Quan trọng nhưng không dùng nữa |

Nếu file đáng tách thành nhiều atomic → ghi "→ cần `/paper-atomize` hoặc tương đương".

### Bước 3: DỪNG chờ duyệt

In bảng đề xuất. Hỏi: "Áp dụng? (all / số cụ thể: 1,3,5 / 'tôi tự sửa')"

### Bước 4: Di chuyển

Chỉ move file được duyệt. Sau mỗi file:
- ✅ Đã move `<file>` → `<đích>`

### Bước 5: Báo cáo cuối

```
📥 Inbox đầu: <N> file
📤 Đã xử lý: <M> file
📌 Còn lại: <K> file (chưa quyết định)
🔴 File quá hạn còn lại: <list>
```

Nếu còn file quá 7 ngày chưa xử lý → cảnh báo và đề xuất lý do (vd: "Cần thêm context", "Có thể archive").
