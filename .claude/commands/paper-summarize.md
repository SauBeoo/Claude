---
description: Tóm tắt tài liệu (PDF, MD, DOCX, TXT, HTML, EPUB, URL) và lưu vào SecondBrain
argument-hint: <đường-dẫn-file-hoặc-URL> [tên-project]
allowed-tools: Read, Write, Glob, Grep, Bash, WebFetch
---

# Tóm tắt nguồn tài liệu

Sử dụng agent **researcher**. Trả lời bằng tiếng Việt.

"Paper" ở đây hiểu theo nghĩa rộng: paper học thuật, bài blog, trang web, chương sách, note từ vault khác, tài liệu đồng nghiệp gửi — bất kỳ nguồn nào cần chắt lọc.

## Đầu vào
- Nguồn: $1 — có thể là **đường dẫn file** (PDF / MD / DOCX / TXT / HTML / EPUB) hoặc **URL** (https://...)
- Project (tùy chọn): $2

---

## QUY TRÌNH

### Bước A: Nhận diện loại đầu vào & đọc nội dung

**Ưu tiên 1 — Kiểm tra URL**:
- Nếu $1 bắt đầu bằng `http://` hoặc `https://` → dùng **WebFetch** để fetch nội dung
- Sau khi fetch: bỏ nav/sidebar/footer/ads, lấy phần main content
- Nếu WebFetch trả về nội dung quá ít hoặc lỗi → báo user:
  ```
  ⚠️ Không fetch được đầy đủ nội dung từ <URL>.
     Có thể do paywall / cần login / trang render bằng JavaScript.
     Giải pháp:
     (a) Bạn copy-paste nội dung vào .txt rồi tôi xử lý
     (b) Tải file PDF/HTML về máy rồi cung cấp đường dẫn
     (c) Dùng reader mode / archive.org và gửi tôi link đó
  ```

**Ưu tiên 2 — Nhận diện file theo đuôi** (lowercase):

| Đuôi | Cách đọc | Lưu ý |
|------|----------|-------|
| `.pdf` | Read tool | Có thể có nhiều trang, cấu trúc rõ |
| `.md` | Read tool | Có thể đã có YAML frontmatter — đọc trước |
| `.txt` | Read tool | Không có cấu trúc, cần suy đoán nhiều |
| `.docx` | Convert sang text trước (xem chú thích dưới) | Có thể có heading, table |
| `.html` | Đọc rồi loại bỏ tag, lấy content chính | Bỏ nav/sidebar/footer/ads |
| `.epub` | Convert sang text/markdown trước | Sách → tóm tắt theo chương hoặc tổng |
| Đuôi khác | Hỏi tôi cách xử lý | |

**Chú thích về DOCX và EPUB**:

Có thể dùng bash để convert nếu cần:
```bash
# DOCX → text (cần pandoc hoặc python-docx)
pandoc "$1" -t plain
# hoặc:
python -c "from docx import Document; d=Document('$1'); print('\n'.join(p.text for p in d.paragraphs))"

# EPUB → markdown
pandoc "$1" -t markdown
```

Nếu lệnh convert lỗi → báo tôi: `⚠️ Không convert được <file>. Lý do: <...>. Bạn có thể (a) cài pandoc, (b) gửi tôi text đã copy thủ công.`

### Bước B: Trích metadata

Mỗi loại nguồn cách trích khác:

| Loại | Nguồn metadata |
|------|----------------|
| URL (web) | `<title>`, `<meta name="author">`, `<meta property="og:*">`, `<time>`, schema.org |
| URL (arXiv) | title, authors, year từ abstract page |
| URL (blog/medium/substack) | byline, published date, canonical URL |
| PDF (paper) | Trang 1: title, authors, year |
| PDF (sách/báo cáo) | Cover + table of contents |
| MD | YAML frontmatter trước, rồi heading H1 |
| DOCX | Heading 1 đầu tiên, properties nếu có |
| TXT | Đoán từ vài dòng đầu — thường ít info |
| HTML (local) | `<title>`, `<meta>`, `<h1>`, schema.org |
| EPUB | Metadata block, table of contents |

Tìm:
- **Tiêu đề** (bắt buộc cố gắng tìm)
- **Tác giả** (nếu có)
- **Năm/ngày** (nếu có)
- **Nguồn**: URL gốc (giữ nguyên, không rút gọn)
- **Loại nguồn**: paper / blog / web-article / book-chapter / report / note / docs / khác
- **2-3 từ khóa cốt lõi**

### Bước C: Đề xuất tên file

**Công thức theo loại nguồn**:

| Loại nguồn | Công thức |
|------------|-----------|
| Paper học thuật | `<năm>-<họ-tác-giả>-<từ-khóa>.md` |
| Blog / web article | `<năm>-<tên-site>-<từ-khóa>.md` |
| Trang docs / wiki | `<năm>-<tên-sản-phẩm-hoặc-org>-<chủ-đề>.md` |
| Chương sách | `<năm>-<tác-giả>-<tên-sách-rút-gọn>-ch<N>.md` |
| Báo cáo | `<năm>-<tổ-chức>-<chủ-đề>.md` |
| Note/khác | `<năm>-<chủ-đề>-<từ-khóa-phụ>.md` |

**Quy tắc chung**:
- Lowercase, không dấu (chuyển ký tự tiếng Việt)
- Dấu gạch ngang `-`, không dấu cách
- Bỏ stopword: a, the, of, in, for, and
- Độ dài 30-60 ký tự

**Ví dụ**:
- Paper: `2017-vaswani-attention-is-all-you-need.md`
- Blog: `2024-stratechery-ai-strategy-shift.md`
- Web article: `2025-openai-how-o3-reasons.md`
- Docs: `2024-anthropic-tool-use-guide.md`
- Chương sách: `2018-newport-deep-work-ch3.md`
- Báo cáo: `2024-mckinsey-state-of-ai.md`
- Note rời: `2024-ideas-llm-tutoring.md`

#### 3 tình huống xử lý:

**TH1 — Metadata đầy đủ**:
```
📂 Loại nguồn: <paper/blog/chương sách/báo cáo/note>
   Tên file đề xuất: <tên>.md
   (Enter để OK / gõ tên khác / "?" xem phương án khác)
```

**TH2 — Thiếu metadata**:
```
⚠️ Loại nguồn: <đoán>
   Thiếu: <năm? tác giả? title?>
   Tôi đoán:
   - <field>: <giá trị hoặc "?">

   Đề xuất: <tên-có-placeholder>.md
   Gõ tên bạn muốn (Enter để dùng đề xuất):
```

**TH3 — Không xác định được loại**:
```
⚠️ File này tôi không chắc thuộc loại nào.
   Nội dung tôi thấy: <2-3 câu mô tả>

   (a) Đặt tên thủ công, tôi tóm tắt tiếp
   (b) Dừng
```

### Bước D: DỪNG chờ tên file

Không lưu khi chưa có tên xác nhận.

### Bước D.5: OUTLINE-FIRST — Trích cấu trúc nguồn trước khi viết

**Đây là bước CHỐNG MẤT NỘI DUNG quan trọng nhất.** Trước khi viết bất kỳ section nào của tóm tắt, phải liệt kê **toàn bộ heading lớn** (H1/H2/H3) trong nguồn — không chỉ heading "method/result/conclusion".

Format outline (ghi vào scratch, KHÔNG lưu file):
```
OUTLINE NGUỒN (heading lớn theo thứ tự xuất hiện):
1. <Heading 1> — trang/section X
2. <Heading 2> — trang/section Y
...
N. <Heading N> — trang/section Z

Section bắt buộc phải có trong tóm tắt (đánh dấu ✓):
- [ ] Mọi heading H1
- [ ] Mọi heading H2 dài > 1 trang
- [ ] Mọi section đặc biệt: Anti-patterns, Case studies, Bài tập, Tips, Takeaways, Mục tiêu học tập, FAQ
- [ ] Story/ví dụ mở đầu nếu tác giả dùng để framing
- [ ] Bảng so sánh (giữ format bảng trong tóm tắt nếu quan trọng)
```

**Quy tắc fidelity**:
- Mỗi heading H1/H2 trong outline → phải có ít nhất 1 đoạn tương ứng trong tóm tắt
- Không gộp 3 section khác nhau vào 1 bullet
- Section "Anti-patterns / Mẹo / Case studies / Bài tập / Takeaways" tự nó là content có giá trị tái sử dụng → **phải có riêng**, không tóm thành 1 dòng

### Bước E: Tóm tắt (template thích nghi theo loại nguồn)

#### Template chuẩn (paper / blog / chương sách / báo cáo)

```markdown
---
type: source-note
source_type: <paper|blog|web-article|book-chapter|report|note|docs|other>
source_file: <tên file gốc — để trống nếu là URL>
title: <tiêu đề đầy đủ>
authors: <nếu có>
year: <nếu có>
url: <URL gốc — bắt buộc điền nếu nguồn là URL>
tags: [<source_type>, <chủ-đề-chính>]
status: summarized
created: <ngày hôm nay>
---

# <Tiêu đề>

## TL;DR
<2-3 câu cô đọng>

## Nội dung chính
<Cấu trúc tùy loại — xem hướng dẫn dưới>

## Đánh giá của tôi (để trống)
- Điểm hay:
- Nghi ngờ / muốn đào sâu:
- Liên quan đến project nào:

## Ứng viên Atomic Notes
<3-5 ý có thể tách. ĐỪNG tạo file.>

## Trích dẫn quan trọng
<Quote ngắn + vị trí (page/section/timestamp)>
```

#### Phần "Nội dung chính" theo từng loại:

**Paper học thuật**:
```markdown
### Vấn đề nghiên cứu
### Phương pháp
### Kết quả chính (3-5 điểm)
### Hạn chế tác giả tự nhận
```

**Blog / article**:
```markdown
### Luận điểm chính
### Lập luận của tác giả
### Bằng chứng / ví dụ tác giả dùng
### Phản biện tiềm năng (nếu có)
```

**Chương sách (ngắn — < 15 trang)**:
```markdown
### Bối cảnh trong sách (chương này nằm ở đâu)
### Ý chính của chương
### Khái niệm/định nghĩa quan trọng
### Ví dụ tác giả dùng
```

**Chương sách / bài giảng / tutorial dài (≥ 15 trang)** — KHÔNG dùng template ngắn ở trên:

Phải dùng **adaptive template** — phản ánh đúng các section gốc. Bộ section tối thiểu:

```markdown
### Mục tiêu học tập (nếu tác giả liệt kê)
### Bối cảnh trong khóa học / cuốn sách (chương này nằm ở đâu, liên hệ chương trước/sau)
### Mở đầu / Story framing (nếu có — tác giả thường dùng để motivate)

### <Section chính 1 theo heading gốc>
### <Section chính 2 theo heading gốc>
### <Section chính N theo heading gốc>
(Mỗi heading H1/H2 lớn trong nguồn → 1 section ở đây. Không gộp.)

### Anti-patterns / Common mistakes (nếu nguồn có)
### Mẹo / Tips nâng cao (nếu nguồn có — liệt kê đầy đủ, không tóm)
### Case studies / Ví dụ thực chiến (nếu nguồn có — mỗi case 1 đoạn)
### Bài tập / Áp dụng (nếu nguồn có — copy nguyên đề bài, không paraphrase mất ý)
### Tóm tắt / Takeaways của tác giả (nếu có)
### Khái niệm / định nghĩa quan trọng (glossary cho người tra cứu nhanh)
```

**Quy tắc**: Section "Anti-patterns", "Mẹo nâng cao", "Case studies", "Bài tập", "Takeaways" trong source dài thường là *content tự đứng có giá trị tái sử dụng* — không bao giờ được tóm bằng 1 dòng. Liệt kê đủ, mỗi item 2-5 dòng.

**Báo cáo / industry report**:
```markdown
### Phạm vi nghiên cứu
### Số liệu / dữ liệu chính
### Phát hiện quan trọng
### Methodology / nguồn dữ liệu
```

**Note / tài liệu khác**:
```markdown
### Nội dung chính
### Context (ai viết, khi nào, cho ai)
### Điểm đáng lưu ý
```

### Bước E.5: COVERAGE CHECK — Đối chiếu outline gốc ↔ tóm tắt

Trước khi save, **bắt buộc** đối chiếu outline đã trích ở Bước D.5 với tóm tắt vừa viết. Tự hỏi:

- [ ] Mỗi heading H1/H2 trong outline có đoạn tương ứng trong tóm tắt chưa?
- [ ] Section đặc biệt (Anti-patterns / Mẹo / Case studies / Bài tập / Takeaways) có còn không, hay bị tóm thành 1 dòng?
- [ ] Bảng so sánh / bảng quyết định trong nguồn có được giữ format bảng không?
- [ ] Story/ví dụ mở đầu của tác giả có được nhắc đến không?
- [ ] Trích dẫn quan trọng có đủ vị trí (trang/section) không?
- [ ] Tỷ lệ độ dài tóm tắt / độ dài nguồn có phù hợp không? (Quy ước: nguồn < 10 trang → tóm ~20-30%; 10-30 trang → ~15-20%; > 30 trang → ~10-15%)

Nếu thiếu — **quay lại Bước E bổ sung trước khi save**, không save nửa vời rồi sửa.

### Bước F: Lưu file

- Có $2: `E:\Claude\SecondBrain\10_Projects\$2\sources\<tên>.md`
  (Chuyển thư mục từ `papers\` sang `sources\` vì giờ là nguồn đa dạng)
- Không có $2: hỏi project, hoặc đề xuất từ chủ đề

### Bước G: Báo cáo

```
✅ Đã lưu: <path>
📎 Loại nguồn: <type>
📋 Ứng viên atomic (<N>):
   1. <title>
   2. <title>
⚠️ Chỗ không chắc:
   - <nếu có>

➡️ Tiếp theo: /paper-atomize <path>
```

---

## Quy tắc bất biến

- KHÔNG tạo atomic notes ở command này
- KHÔNG bịa nội dung. Thiếu → ghi "Không tìm thấy trong nguồn"
- Trích dẫn phải có vị trí (page/section/heading)
- KHÔNG lưu khi chưa có tên file xác nhận
- **KHÔNG bỏ qua section dài > 1 trang trong nguồn** — phải có đoạn tương ứng trong tóm tắt
- **KHÔNG ép nguồn dài vào template 4-section cứng** — adaptive theo cấu trúc gốc
- **Outline-first** (Bước D.5) là bắt buộc với nguồn ≥ 15 trang hoặc có ≥ 5 heading H2
- **Coverage check** (Bước E.5) là bắt buộc trước khi save
- Với HTML: chỉ lấy main content, bỏ navigation/ads
- Với EPUB sách dài: hỏi tôi muốn tóm tắt cả sách hay chương nào
