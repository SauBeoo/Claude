---
name: summarize-pdf-paper
description: Sử dụng skill này khi cần tóm tắt 1 tài liệu nghiên cứu từ file PDF hoặc đường link URL. Trigger khi user nói "tóm tắt paper này", "đọc paper này", "tóm tắt bài này", "tóm tắt link này", hoặc khi user chia sẻ link/file PDF/URL tài liệu.
---

# Skill: Summarize Paper / Article / Chapter

Tóm tắt tài liệu nghiên cứu (PDF, URL, blog, docs, chương sách, tutorial) theo template **thích nghi theo loại nguồn**, đề xuất atomic notes.

## Khi nào dùng

- User cung cấp PDF paper / chương sách / tài liệu khóa học (qua path hoặc upload)
- User dán URL bài báo, blog, trang docs, arXiv, semantic scholar
- User dán abstract/link và nhờ tóm tắt
- Khi reading list bằng PDF hoặc link cần xử lý hàng loạt

## Nguyên tắc cốt lõi: Fidelity-with-Structure

**Tóm tắt PHẢI phản ánh cấu trúc thực tế của nguồn**, không nhồi mọi nguồn vào 1 template cứng. 4 quy tắc:

1. **Outline-first** — Trước khi viết bất kỳ section nào, liệt kê toàn bộ heading H1/H2/H3 trong nguồn.
2. **Không bỏ section dài** — Mọi heading dài > 1 trang phải có đoạn tương ứng trong tóm tắt.
3. **Section đặc biệt giữ nguyên** — Anti-patterns, Mẹo, Case studies, Bài tập, Takeaways, Mục tiêu học tập là content tự đứng → không bao giờ tóm thành 1 dòng.
4. **Coverage check trước khi save** — Đối chiếu outline ↔ tóm tắt, thiếu thì bổ sung.

## Quy trình

### Bước 1: Đọc tài liệu

**Nếu là URL** (`http://` / `https://`):
- Dùng **WebFetch** để fetch nội dung
- Strip boilerplate: nav, sidebar, footer, ads — chỉ giữ main content
- Nếu fetch lỗi / nội dung quá ít → báo user và đề xuất giải pháp thay thế

**Nếu là file PDF**:
- Dùng Read tool đọc PDF
- **Đọc TOÀN BỘ** trước khi tóm tắt — không skip section nào trừ khi PDF > 50 trang (lúc đó dùng strategy structured: TOC → từng chương)
- Với PDF dạng paper học thuật: ưu tiên Abstract → Conclusion → Intro → Method → Results
- Với PDF dạng tutorial / chương sách / bài giảng: đọc tuyến tính theo thứ tự

### Bước 2: Xác định loại nguồn

| Loại | Dấu hiệu |
|------|----------|
| `paper` | Có abstract, method, results, limitations, references |
| `blog` / `web-article` | Có byline + published date + URL canonical |
| `book-chapter` (ngắn, < 15 trang) | Một chương trong sách, không có Anti-patterns/Bài tập |
| `book-chapter` / `tutorial` / `lecture` (dài, ≥ 15 trang) | Có Mục tiêu học tập, Anti-patterns, Case studies, Bài tập, Takeaways |
| `report` | Số liệu + biểu đồ + executive summary |
| `docs` | Tài liệu kỹ thuật, có code block + reference link |
| `note` | Văn bản tự do, ít cấu trúc |

**Nhận biết tutorial/lecture dài**: có "Mục tiêu học tập" + "Bài tập" + "Takeaways" → dùng adaptive template (xem Bước 4b).

### Bước 3: Outline-First (BẮT BUỘC nếu nguồn ≥ 15 trang hoặc ≥ 5 heading H2)

Liệt kê outline trước khi viết:
```
OUTLINE NGUỒN:
1. <Heading> — trang X
2. <Heading> — trang Y
...

Section bắt buộc phải có:
- [ ] Mọi H1
- [ ] Mọi H2 dài > 1 trang
- [ ] Anti-patterns / Mẹo / Case studies / Bài tập / Takeaways nếu có
- [ ] Story/ví dụ framing mở đầu nếu tác giả dùng
- [ ] Bảng so sánh quan trọng (giữ format)
```

### Bước 4: Xác định project & tên file

Hỏi user: "Paper này liên quan project nào trong `10_Projects/`?"
- Có project X → đặt note ở `10_Projects/X/sources/`
- Không gắn project → `00_Inbox/paper-chua-doc/`

Đề xuất tên file theo công thức:
| Loại | Công thức |
|------|-----------|
| Paper | `<năm>-<họ-tác-giả>-<từ-khóa>.md` |
| Blog | `<năm>-<tên-site>-<từ-khóa>.md` |
| Chương sách / lecture | `<năm>-<tác-giả-hoặc-course>-<chủ-đề>.md` |
| Docs | `<năm>-<sản-phẩm>-<chủ-đề>.md` |

**DỪNG chờ user xác nhận tên file trước khi viết.**

### Bước 5: Viết tóm tắt theo template thích hợp

#### 5a. Template chuẩn (paper / blog / chương sách ngắn / báo cáo)

Frontmatter: `type: source-note`, `source_type`, `title`, `authors`, `year`, `url`, `project`, `tags`, `status: summarized`, `created`.

Section:
- **TL;DR** — 2-3 câu
- **Nội dung chính** (cấu trúc tùy loại):
  - Paper: Vấn đề / Phương pháp / Kết quả / Hạn chế
  - Blog: Luận điểm / Lập luận / Bằng chứng / Phản biện
  - Chương sách ngắn: Bối cảnh / Ý chính / Khái niệm / Ví dụ
  - Báo cáo: Phạm vi / Số liệu / Phát hiện / Methodology
- **Đánh giá của tôi** (để trống — user tự điền)
- **Ứng viên Atomic Notes** — 3-7 ý, KHÔNG tạo file
- **Trích dẫn quan trọng** — quote + vị trí

#### 5b. Adaptive template (tutorial / lecture / chương sách dài ≥ 15 trang)

KHÔNG dùng template 4 mục cứng. Phải phản ánh các section gốc:

```markdown
## TL;DR
## Mục tiêu học tập (nếu tác giả liệt kê)
## Bối cảnh trong khóa học / cuốn sách
## Mở đầu / Story framing (nếu có)

## <Section chính 1 theo heading gốc>
## <Section chính 2 theo heading gốc>
## ... mỗi H1/H2 lớn của nguồn → 1 section ở đây ...

## Anti-patterns / Common mistakes (nếu nguồn có — liệt kê đủ, mỗi cái 2-5 dòng)
## Mẹo nâng cao (nếu nguồn có — liệt kê đủ)
## Case studies / Ví dụ thực chiến (nếu nguồn có — mỗi case 1 đoạn)
## Bài tập / Áp dụng (nếu nguồn có — copy đề bài)
## Tóm tắt / Takeaways của tác giả (nếu có)

## Khái niệm / định nghĩa quan trọng (glossary)
## Đánh giá của tôi (để trống)
## Ứng viên Atomic Notes
## Trích dẫn quan trọng
## Liên kết
```

### Bước 6: Coverage check (BẮT BUỘC trước khi save)

Tự hỏi:
- [ ] Mỗi heading H1/H2 outline có đoạn tương ứng trong tóm tắt?
- [ ] Section đặc biệt (Anti-patterns / Mẹo / Case studies / Bài tập / Takeaways) còn không, hay bị tóm thành 1 dòng?
- [ ] Bảng so sánh / quyết định có giữ format bảng không?
- [ ] Story/ví dụ mở đầu có nhắc đến không?
- [ ] Trích dẫn có đủ vị trí (trang/section)?
- [ ] Tỷ lệ độ dài hợp lý? (< 10 trang → tóm ~20-30%; 10-30 trang → ~15-20%; > 30 trang → ~10-15%)

**Thiếu → quay lại Bước 5 bổ sung. Không save nửa vời.**

### Bước 7: Đề xuất atomic notes

Sau khi tóm tắt, đề xuất 3-7 atomic notes có thể tạo:
```
Đề xuất atomic notes từ source này:

1. <slug> — concept | claim | method | question
   Nội dung dự kiến: <1-2 câu>
2. ...

Bạn muốn tôi tạo cái nào? (1/2/3/all/none)
```

KHÔNG tự tạo. Đợi user chọn.

### Bước 8: Move file PDF (nếu user xác nhận)

```
Move PDF gốc từ `00_Inbox/paper-chua-doc/<file>.pdf`
       sang `<đích note>/<file>.pdf` để gắn kèm?
```

## Lưu ý quan trọng

- **Không bịa số liệu.** Không tìm thấy → "Paper không đề cập chỉ số rõ ràng".
- **Không bịa citation.** Bibtex/citation key để placeholder, user điền sau.
- **Phân biệt claim của paper vs claim của bạn.** "Đánh giá của tôi" để trống cho user.
- **Paper dài > 20 trang:** chia 2 lần đọc — skim trước, đọc kỹ phần cần sau.
- **Tutorial/lecture dài:** KHÔNG dùng template ngắn. Adaptive theo cấu trúc gốc.
- **Anti-patterns / Mẹo / Case studies / Bài tập là content tự đứng** — không bao giờ tóm thành 1 dòng.

## Output mẫu

```
✅ Đã tóm tắt: "Bài 2.4: Workflow EPCC"
   File: E:\Claude\SecondBrain\10_Projects\claude-code-101\sources\2026-claude-code-101-epcc-workflow.md
📎 Loại nguồn: book-chapter (tutorial/lecture dài — dùng adaptive template)
📊 Coverage: 18/18 heading lớn được cover; 5 anti-patterns + 5 mẹo + 5 case studies giữ riêng

📝 Đề xuất atomic notes (chưa tạo, chờ bạn chọn):
   1. concept/epcc-workflow-bon-phase
   2. claim/cost-thay-doi-tang-theo-phase
   3. method/test-driven-prompt-voi-ai
   ...

Tạo cái nào?
```
