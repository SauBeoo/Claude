# Quy ước Tag toàn vault

Tag là tầng phân loại **xuyên thư mục**, bổ sung cho cấu trúc PARA chứ không thay thế.

## Nguyên tắc

1. Tag viết **không dấu, gạch ngang**: `machine-learning` chứ không phải `machine learning` hay `MachineLearning`.
2. **Tối đa 5 tag** cho 1 note. Nhiều hơn = mất ý nghĩa.
3. Tag đặt trong frontmatter YAML, không rải khắp body:
   ```yaml
   ---
   tags: [machine-learning, transformer, attention]
   ---
   ```

## 3 nhóm tag chính

### 🔵 Nhóm chủ đề (chính, bắt buộc)

Lĩnh vực kiến thức. Mỗi note nên có **đúng 1 tag chủ đề chính**.

- `machine-learning`
- `web-development`
- `teaching`
- `research-methodology`
- `content-creation`
- `video-production`
- `productivity`
- `philosophy`

### 🟢 Nhóm loại (mô tả note này là gì)

- `paper` — tóm tắt paper
- `lecture` — bài giảng
- `video` — kịch bản video
- `moc` — Map of Content
- `daily` — daily note
- `project` — project README

### 🟡 Nhóm trạng thái/độ chín

Chỉ dùng cho atomic notes:

- `seed` 🌱 — vừa gieo
- `growing` 🌿 — đang phát triển
- `evergreen` 🌳 — đã chín

## Tag không nên dùng

❌ Tag quá rộng: `note`, `idea`, `important` — không giúp lọc gì.
❌ Tag trùng tên thư mục: `inbox`, `projects` — thông tin này đã có trong path.
❌ Tag cảm xúc nhất thời: `wow`, `cool`, `hay-qua` — không tái dùng được.

## Khi nào nên tạo tag mới?

Khi bạn có **ít nhất 3 note** muốn nhóm lại mà chưa có tag phù hợp → tạo tag mới và thêm vào file này.
