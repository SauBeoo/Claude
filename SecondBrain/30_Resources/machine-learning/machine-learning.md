# 30_Resources/machine-learning — Tài liệu ML đáng dùng lại

Note ở đây là **tóm tắt blog post, paper rời, video lẻ, cheat sheet** về ML — không gắn project, không thuộc 1 khóa hay sách cụ thể.

## Khi nào note vào đây?

- ✅ 1 blog post hay về transformer, RAG, fine-tuning — không gắn project
- ✅ 1 paper kinh điển bạn đọc để mở rộng nền (không phải cho project research cụ thể)
- ✅ Cheat sheet / cấu hình mẫu / repo hay muốn revisit

## Khi nào KHÔNG note vào đây?

- ❌ Paper đọc cho project ML cụ thể → `10_Projects/<project>/sources/`
- ❌ Sách ML → `30_Resources/books/`
- ❌ Khóa học ML → `30_Resources/courses/`
- ❌ Khái niệm ML chín → atomize sang `50_Atomic/concepts/` và link vào `99_Meta/MOCs/ML-MOC.md`

## Cấu trúc note đề xuất

```markdown
---
type: resource
source_type: blog | paper | video | repo
url: 
status: archived | re-visit
tags: [ml, <sub-topic>]
---

# Tiêu đề

## Lý do lưu (1 câu)
## TL;DR
## Khi nào revisit
## Ý đáng atomize → [[link 50_Atomic]]
```

## Quan hệ với ML-MOC

`99_Meta/MOCs/ML-MOC.md` hiện đang skeleton. Khi bạn note đủ 5 resource ML + bắt đầu atomize → ML-MOC sẽ active.

## Ví dụ note đáng tạo đầu tiên

- `karpathy-makemore-blog-series.md`
- `paper-attention-is-all-you-need-2017.md` *(nếu đọc làm nền tảng)*
- `huggingface-fine-tuning-guide.md`
