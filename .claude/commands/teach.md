---
description: Đọc 1 file hoặc folder rồi dạy theo quy trình gia sư (skill tutor)
argument-hint: <đường-dẫn-file-hoặc-folder> [trình-độ] [mục-tiêu]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
---

# /teach — Dạy tôi từ tài liệu này

Sử dụng agent **teacher**. Kích hoạt skill **tutor** (gia sư toàn diện) với nguồn là một **file** hoặc một **folder** tôi chỉ định. Trả lời bằng tiếng Việt.

Vai trò kết hợp: dùng **phong cách & nguyên tắc sư phạm của agent `teacher`** (hook bằng vấn đề, ví dụ trước lý thuyết, sandwich feedback, phân bổ độ khó Bloom, liên hệ thực tế VN) để vận hành **quy trình gia sư của skill `tutor`** (lộ trình + ôn tập giãn cách + atomic/flashcard + theo dõi tiến độ).

Toàn bộ triết lý dạy, 4 chế độ, giọng văn, và Bước 4-7 (dạy / ôn / củng cố / chốt) tuân theo `~/.claude/skills/tutor/SKILL.md`. Command này chỉ chuẩn hoá **đầu vào** (file/folder) cho Bước 2-3.

## Đầu vào
- `$1` — đường dẫn **file** hoặc **folder** (cũng nhận URL https://...).
- `$2` (tuỳ chọn) — trình độ hiện tại của tôi.
- `$3` (tuỳ chọn) — mục tiêu học.

## Bước A — Nhận diện nguồn

Kiểm tra `$1`:

1. **URL** (bắt đầu `http`) → `WebFetch`, coi như 1 nguồn đơn.
2. **File** → đọc bằng tool phù hợp (PDF/MD/DOCX/TXT/HTML/EPUB → `Read`; định dạng cần convert → gợi ý pandoc).
3. **Folder** → `Glob` liệt kê các file đọc được bên trong (`.md`, `.pdf`, `.txt`, `.docx`, `.html`, `.epub`...).
   - Sắp xếp theo thứ tự tự nhiên (số chương / tên file) để suy ra trình tự học.
   - **Outline trước, đào sâu sau:** đọc tiêu đề + đoạn mở đầu mỗi file để nắm bức tranh tổng thể; chưa cần đọc toàn văn ngay.
   - Gộp tất cả file thành **MỘT learning track tổng hợp** (không tách mỗi file 1 track). Mỗi file/cụm file ≈ 1 module trong roadmap.

In ngắn gọn cho tôi xác nhận đã nhận diện đúng:
```
📥 Nguồn: <file đơn | folder X file | URL>
   - <liệt kê file nếu là folder, kèm thứ tự suy ra>
Chủ đề tôi đoán: <…>. Đúng không, hay bạn muốn điều chỉnh trọng tâm?
```

## Bước B — Vào quy trình tutor

Từ đây chạy đúng skill **tutor**:

1. **Bước 0** — kiểm tra `20_Areas/learning/` xem đã có track cho chủ đề này chưa. Có rồi → tiếp tục track cũ (Bước 5 ôn tập trước). Chưa có → track mới.
2. **Bước 1** — hỏi định cỡ (trình độ / mục tiêu / thời lượng / hỏi-ngược hay giảng). Nếu tôi đã đưa `$2`/`$3` thì dùng luôn, chỉ hỏi phần còn thiếu.
3. **Bước 2** — nghiên cứu kỹ nguồn (đào sâu phần sẽ dạy) **+ bổ sung nguồn web bắt buộc** (`WebSearch`/`WebFetch`) để có ví dụ rõ hơn, đối chiếu, kiểm chứng chỗ doc nói mơ hồ. Gọi `find-related-notes` tìm note cũ liên quan trong vault.
4. **Bước 3** — dựng roadmap nhiều module từ nội dung folder/file, tạo `_track.md` + `flashcards.md`, trình tôi duyệt trước khi dạy.
5. **Bước 4-7** — dạy → ôn → tạo atomic/flashcard (cho tôi xem trước) → chốt buổi, đúng như SKILL.md.

## Ràng buộc (kế thừa từ tutor + CLAUDE.md)
- Không bịa; doc nói gì vs web nói gì vs suy luận của bạn — tách bạch.
- Không tự tạo atomic/flashcard hàng loạt khi chưa cho tôi xem; atomic luôn `seed`.
- Không tự commit Git, không tự xoá file.
- Folder lớn → đừng cố nhồi hết trong 1 buổi; bám thời lượng tôi chọn, thà ít mà thạo.
