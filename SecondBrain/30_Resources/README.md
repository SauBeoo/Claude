# 30_Resources — Tham khảo theo chủ đề

Nơi lưu **tài liệu từ người khác** mà bạn quan tâm: bài blog, paper kinh điển, khóa học hay, cheatsheet, công cụ...

## Khác Areas thế nào?

- **Areas** = đúc kết kinh nghiệm **của chính bạn** về vai trò bạn đảm nhận.
- **Resources** = sưu tầm tài liệu **của người khác** về chủ đề bạn quan tâm.

Ví dụ:
- "Cách tôi review code của sinh viên" → `20_Areas/teaching/`
- "Bài blog của Google về code review" → `30_Resources/programming/`

## Thư mục con theo chủ đề

Đặt tên thư mục theo **chủ đề kiến thức**, không phải theo loại tài liệu.

✅ Đúng: `machine-learning/`, `video-editing/`, `web-development/`
❌ Sai: `videos/`, `pdfs/`, `bookmarks/` (vì 1 chủ đề có nhiều loại tài liệu)

## Cấu trúc note Resource điển hình

```markdown
---
type: resource
source: <link>
author: <ai viết>
date-added: 2026-05-23
tags: [machine-learning, transformer]
---

# Tiêu đề tài liệu gốc

## Tại sao tôi lưu

(1-2 câu — vì sao tài liệu này đáng nhớ)

## Tóm tắt ý chính

- ...
- ...

## Trích dẫn đáng nhớ

> "..."

## Liên kết

- Áp dụng vào: [[ten-project-hoac-area]]
- Atomic note liên quan: [[50_Atomic/concepts/ten-note]]
```

## Khi nào "chắt lọc" Resource thành Atomic?

Khi bạn đọc 3-4 resource về cùng 1 ý và **bắt đầu có quan điểm riêng** — đó là lúc viết atomic note ở `50_Atomic/` bằng lời của bạn, có link ngược về các resource nguồn.
