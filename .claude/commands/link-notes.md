---
description: Tìm note cũ liên quan và đề xuất [[wiki link]] (Bước 5 workflow paper)
argument-hint: <đường-dẫn-note-mới> [thêm-note-khác]
allowed-tools: Read, Edit, Glob, Grep
---

# Liên kết note vào bộ não

Sử dụng agent **librarian**. Trả lời bằng tiếng Việt.

## Đầu vào
- Note(s) mới cần liên kết: $ARGUMENTS

## Việc cần làm

### Bước 1: Đọc note mới
Đọc kỹ nội dung note(s) mới ở $ARGUMENTS. Trích ra:
- Concepts chính
- Tags
- Tác giả / nguồn (nếu có)

### Bước 2: Tìm note liên quan

Tìm trong các thư mục sau theo thứ tự ưu tiên:

1. **`E:\Claude\SecondBrain\50_Atomic\`** — ưu tiên cao nhất (đây là core)
2. **`E:\Claude\SecondBrain\20_Areas\`** — kinh nghiệm dài hạn
3. **`E:\Claude\SecondBrain\10_Projects\`** — note project khác
4. **`E:\Claude\SecondBrain\30_Resources\`** — tham khảo

Dùng Grep tìm theo:
- Từ khóa chính của note mới
- Tag chung
- Tên tác giả (nếu là paper)

### Bước 3: Đề xuất liên kết

Trình bày dạng:

```
## Note: <tên note mới>

### Liên kết đề xuất:

1. [[<note cũ>]] — **Lý do**: <1 câu giải thích quan hệ>
   - Loại liên kết: extends | contradicts | example-of | similar-to | answers
   - Đề xuất vị trí thêm trong note mới: <section>
   - Có nên link ngược lại không? (thêm vào note cũ)

2. ...
```

### Bước 4: DỪNG LẠI chờ duyệt

Hỏi tôi: "Áp dụng những link nào? (vd: 1,3 hoặc 'tất cả' hoặc 'bỏ qua')"

### Bước 5: Thực thi

Với link được duyệt:
- Thêm `[[<note>]]` vào mục "Liên quan" của note mới
- Nếu link 2 chiều: thêm cả vào note cũ
- KHÔNG sửa nội dung khác trong note cũ

In báo cáo:
- ✅ <N> link đã thêm
- ⚠️ Note nào còn cô lập (không tìm thấy liên quan) — có thể cần review thủ công
