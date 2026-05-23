---
description: Chạy trọn workflow nguồn tài liệu (tóm tắt + đề xuất atomic + liên kết)
argument-hint: <đường-dẫn-file-hoặc-URL> <tên-project>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Workflow nguồn tài liệu — trọn gói

Sử dụng agent **researcher**. Trả lời bằng tiếng Việt.

Chạy 3 phase liên tiếp, DỪNG LẠI chờ duyệt giữa mỗi phase. Tuyệt đối không tự ý nhảy phase.

Hỗ trợ: **PDF, MD, DOCX, TXT, HTML, EPUB** và **URL** (https://...).

## Đầu vào
- Nguồn: $1 — đường dẫn file hoặc URL
- Project: $2

## PHASE 1: Tóm tắt

Thực hiện đúng như `/paper-summarize $1 $2`:
- Nếu $1 là URL → dùng WebFetch để fetch nội dung trước
- Nhận diện loại nguồn (file/web), đọc bằng tool phù hợp
- Trích metadata theo cấu trúc của loại nguồn
- **Đề xuất loại nguồn (paper / blog / book chapter / report / note / other) + tên file**
- DỪNG chờ tôi xác nhận (Enter / gõ tên khác / "?" xem phương án khác)
- Tóm tắt theo template thích nghi với loại nguồn
- Lưu vào `E:\Claude\SecondBrain\10_Projects\$2\sources\<tên>.md`
- In path + ứng viên atomic + chỗ không chắc

**DỪNG**. Hỏi: "Tiếp tục Phase 2 (chắt lọc atomic) không? (yes/no/sửa)"

- "no" → kết thúc
- "sửa" → hỏi tôi cần sửa gì, sửa note, hỏi lại
- "yes" → sang Phase 2

## PHASE 2: Chắt lọc Atomic

Thực hiện đúng như `/paper-atomize <path-note-vừa-tạo>`:
- Đề xuất 3-5 atomic từ note
- DỪNG, chờ tôi chọn số nào
- Tạo các file atomic vào `50_Atomic\`

**DỪNG**. Hỏi: "Tiếp tục Phase 3 (tìm liên kết) không? (yes/no)"

## PHASE 3: Liên kết

Thực hiện đúng như `/link-notes <atomic-vừa-tạo>`:
- Tìm note cũ liên quan
- Đề xuất link
- DỪNG chờ duyệt
- Thêm link

## Tổng kết cuối

```
✅ Nguồn: <tên> (loại: <type>)
📄 Source note: <path>
⚛️ Atomic notes mới: <N>
🔗 Liên kết đã tạo: <M>
⏱️ Ghi vào nhật ký 60_Daily/<ngày>.md không? (yes/no)
```

Nếu "yes" → thêm vào daily note phần "Đã chắt lọc" với link tới source note.
