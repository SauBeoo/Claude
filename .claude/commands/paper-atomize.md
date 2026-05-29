---
description: Tách atomic notes từ một paper note (Bước 4 workflow paper)
argument-hint: <đường-dẫn-paper-note.md>
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Chắt lọc Atomic Notes

Sử dụng agent **researcher**. Trả lời bằng tiếng Việt.

## Đầu vào
- Paper note: $1

## Việc cần làm

### Phase 1: Đề xuất (DỪNG LẠI CHỜ TÔI DUYỆT)

1. Đọc paper note ở $1, đặc biệt mục "Ứng viên Atomic Notes"
2. Đề xuất 3-5 atomic notes. Mỗi cái trình bày như sau:

   ```
   ### [N]. <Tên file đề xuất>.md
   - **Type**: concept | claim | method | question
   - **Một câu**: <Ý chính trong 1 câu khẳng định>
   - **Tại sao đáng tách**: <1 câu>
   - **Liên kết tiềm năng**: <tên note cũ có thể link tới, nếu có>
   ```

3. **Quy tắc đặt tên atomic note**:
   - Dạng câu khẳng định, không phải chủ đề chung
   - ❌ "LLM trong giáo dục.md"
   - ✅ "LLM-tăng-engagement-khi-feedback-tức-thì.md"
   - Dùng dấu gạch ngang, không dấu cách
   - Có thể giữ tiếng Việt có dấu

4. **DỪNG LẠI**. Hỏi tôi: "Bạn muốn tạo những atomic nào? (gõ số, vd: 1,3,4 hoặc 'tất cả')"

### Phase 2: Tạo (sau khi tôi duyệt)

Với mỗi atomic được chọn:

1. Tạo file tại `E:\Claude\SecondBrain\50_Atomic\<tên-file>.md`

2. **Format**:
   ```markdown
   ---
   type: <concept|claim|method|question>
   tags: [<tag1>, <tag2>]
   source: [[<tên paper note không có .md>]]
   created: <ngày>
   ---

   # <Tên atomic — câu khẳng định đầy đủ>

   <Nội dung — TỐI ĐA 300 từ, 1 ý duy nhất>

   ## Bằng chứng / nguồn
   - Từ [[<paper note>]], trang X: "<trích ngắn>"

   ## Liên quan
   - [[<note khác nếu có và tạo (không tạo thì không cần)>]]

   ## Câu hỏi mở
   - <Nếu có>
   ```

3. **Quy tắc viết atomic**:
   - 1 atomic = 1 ý. Nếu viết 2 ý, tách 2 file
   - **Viết theo kiểu ELI5 — như giải thích cho một đứa trẻ 5 tuổi**: dùng ví dụ/phép so sánh đời thường (mở đầu "Tưởng tượng..." rất tốt), câu ngắn, từ quen thuộc. Thuật ngữ kỹ thuật chỉ giữ ở tiêu đề hoặc khi bắt buộc — phải giải thích ngay bằng lời thường. Tự kiểm: "đứa trẻ đọc có hình dung ra không?"
   - Dưới 300 từ. Nếu dài hơn = chưa atomic đủ

4. Sau khi tạo xong, sang Phase 3.

### Phase 3: Index vào MOC (DỪNG LẠI CHỜ DUYỆT)

Mục tiêu: mọi atomic đều có "nhà" trong 1 MOC để sau này truy hồi theo chủ đề.

1. **Quét MOC hiện có**: `Glob` `E:\Claude\SecondBrain\99_Meta\MOCs\*.md`. Với mỗi MOC, đọc frontmatter `tags:` (bỏ qua tag chung `moc`).

2. **Match theo tag overlap** cho từng atomic vừa tạo:
   - Lấy `tags:` của atomic
   - Tìm MOC nào có ít nhất 1 tag trùng (case-insensitive, bỏ dấu nếu cần)
   - Nếu nhiều MOC cùng match → ưu tiên MOC có nhiều tag trùng nhất

3. **Trình bày đề xuất**:

   ```
   ## Đề xuất index MOC

   ### Atomic 1: <tên-atomic>.md
   - Tags: [a, b, c]
   - Type: concept → section "🌱 Khái niệm nền tảng"
   - **MOC khớp**: [[ML-MOC]] (trùng tag: a, b)
   - Sẽ append: `- [[<tên-atomic>]] — <1 câu mô tả>`

   ### Atomic 2: <tên-atomic>.md
   - Tags: [x, y]
   - **Không MOC nào khớp** → đề xuất tạo MOC mới:
     - Tên file gợi ý: `<topic>-MOC.md` (vd: `affiliate-MOC.md`)
     - Topic: <topic chính rút từ tag>
   ```

4. **Mapping type → section trong MOC**:
   - `concept` → `## 🌱 Khái niệm nền tảng`
   - `method` → `## 🛠️ Phương pháp & kỹ thuật`
   - `claim` → `## 💭 Luận điểm đáng tranh luận`
   - `question` → `## ❓ Câu hỏi mở`

5. **DỪNG**. Hỏi tôi: "Áp dụng đề xuất nào? (vd: 1,2 / 'tất cả' / 'bỏ qua' / 'sửa MOC X')"

6. **Thực thi sau khi duyệt**:
   - **Append vào MOC có sẵn**: dùng `Edit` thêm dòng `- [[<atomic>]] — <mô tả>` ngay dưới heading section đúng. Nếu section chỉ có `*(chưa có)*` → thay thế dòng đó. Cập nhật frontmatter `updated: <ngày hôm nay>`.
   - **Tạo MOC mới**: dùng skeleton sau, đặt ở `E:\Claude\SecondBrain\99_Meta\MOCs\<topic>-MOC.md`:

     ```markdown
     ---
     type: moc
     topic: <topic>
     updated: <YYYY-MM-DD>
     tags: [moc, <tag1>, <tag2>]
     status: active
     ---

     # 🗺️ <Topic> — Map of Content

     ## 🌱 Khái niệm nền tảng
     - *(chưa có)*

     ## 🛠️ Phương pháp & kỹ thuật
     - *(chưa có)*

     ## 💭 Luận điểm đáng tranh luận
     - *(chưa có)*

     ## ❓ Câu hỏi mở
     - *(chưa có)*

     ## 📚 Tài liệu tham khảo
     - *(chưa có)*

     ---

     **Cách dùng MOC này:** Mọi atomic/resource liên quan <topic> → thêm link vào đúng section.
     ```

     Sau đó append atomic vào section tương ứng (thay `*(chưa có)*`).

7. **In báo cáo cuối**:
   - ✅ <N> atomic đã tạo
   - 🗺️ <M> MOC đã cập nhật: [[MOC-1]], [[MOC-2]]
   - 🆕 <K> MOC mới tạo: [[MOC-mới]]
   - 🔗 Đề xuất chạy `/link-notes` để tìm liên kết giữa các atomic
