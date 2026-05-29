---
name: create-atomic-note
description: Sử dụng skill này khi cần tạo 1 atomic note mới trong vault SecondBrain. Trigger khi user nói "tạo atomic note", "viết note về X", "lưu ý này thành atomic", hoặc khi đề xuất từ skill khác (summarize-pdf-paper) được user xác nhận.
---

# Skill: Create Atomic Note

Tạo atomic note theo template, link tự động đến note liên quan.

## Khi nào dùng

- User yêu cầu tạo atomic note tường minh
- Sau khi summarize-pdf-paper, user chọn atomic note muốn tạo
- Trong quá trình chắt lọc (librarian agent đề xuất, user chọn)

## Quy trình

### Bước 1: Xác định loại

Hỏi (nếu chưa biết):
```
Atomic note này loại gì?
- concept: khái niệm "X là gì?"
- claim: luận điểm có thể tranh luận
- method: phương pháp "Cách làm X"
- question: câu hỏi mở chưa trả lời
```

### Bước 2: Đặt slug tên file

- Slug không dấu, gạch ngang
- Ngắn nhưng đủ rõ (5-10 từ)
- Tránh từ chung chung ("note-ve-X")

Ví dụ tốt:
- `self-attention-la-weighted-sum.md`
- `cach-day-debug-bang-rubber-duck.md`
- `lieu-llm-co-thuc-su-hieu-ngon-ngu.md`

Ví dụ xấu:
- `attention.md` (quá ngắn, không biết về cái gì)
- `note-ve-attention-trong-transformer-cua-paper-vaswani.md` (quá dài)

### Bước 3: Tìm note liên quan (skill find-related-notes)

Trước khi tạo, scan vault để tìm:
- Atomic notes cùng tag/chủ đề
- Notes trong project nguồn (paper, lecture, daily)

Đề xuất 3-5 link `[[...]]` để chèn vào mục "Liên hệ".

### Bước 4: Tạo file theo template

Dùng template tương ứng:
- concept → `99_Meta/templates/atomic-concept.md`
- claim → `99_Meta/templates/atomic-claim.md`
- method → `99_Meta/templates/atomic-method.md`
- question → `99_Meta/templates/atomic-question.md`

Frontmatter:
```yaml
---
type: concept | claim | method | question
created: YYYY-MM-DD
tags: [tag1, tag2]  # 1-3 tag, không quá 5
status: seed       # mặc định, sẽ growing/evergreen sau
---
```

Body:
- **Heading H1:** tiêu đề tự nhiên có dấu tiếng Việt
- **Nội dung:** 1-3 đoạn ngắn, mỗi đoạn 2-4 câu, BẰNG LỜI USER (không copy nguyên văn nguồn). **Viết theo kiểu ELI5** — xem nguyên tắc #5 bên dưới.
- **Liên hệ:** 3-5 link `[[...]]` đã tìm ở bước 3
- **Nguồn:** link ngược về paper/note gốc

### Bước 5: Update MOC (nếu có)

Nếu atomic note thuộc chủ đề đã có MOC trong `99_Meta/MOCs/`:
- Đề xuất user: "Thêm link note này vào ML-MOC không?"
- KHÔNG tự thêm

### Bước 6: Confirm output

Response:
```
✅ Tạo atomic note:
   File: 50_Atomic/concepts/self-attention-la-weighted-sum.md
   Type: concept
   Status: seed
   Tags: [machine-learning, attention, transformer]
   Liên kết: 3 notes ([[X]], [[Y]], [[Z]])
   Nguồn: [[10_Projects/.../attention-is-all-you-need]]

Cần điều chỉnh gì không?
```

## Nguyên tắc atomic note

1. **1 ý duy nhất.** Nếu viết tới ý thứ 2 — tách ra note khác.
2. **Đứng độc lập.** Đọc note không cần đọc thứ khác cũng hiểu.
3. **Lời của user.** Không copy nguyên văn. Diễn đạt lại.
4. **Nhiều link.** Atomic note không có link = atomic note chết.
5. **Giải thích như cho trẻ 5 tuổi (ELI5).** Thân note viết sao cho một đứa trẻ 5 tuổi cũng nắm được ý chính:
   - Dùng **ví dụ / phép so sánh đời thường** (lớp học, đồ chơi, nấu ăn...). Mở đầu kiểu "Tưởng tượng..." rất hiệu quả.
   - **Câu ngắn, từ quen thuộc.** Tránh câu lồng nhiều mệnh đề.
   - **Thuật ngữ kỹ thuật chỉ giữ ở tiêu đề** hoặc khi bắt buộc — và phải giải thích ngay bằng lời thường ngay sau đó.
   - Tự kiểm: *"Đọc câu này, một đứa trẻ có hình dung ra không?"* Nếu không → viết lại đơn giản hơn.

## Lưu ý

- Nếu user đưa nội dung quá dài (>500 từ) → đề xuất tách thành 2-3 atomic notes
- Nếu nội dung quá ngắn (<50 từ) → hỏi user có muốn mở rộng không
- Status mặc định luôn là `seed`, đừng tự nâng lên `growing`/`evergreen`
