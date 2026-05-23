---
name: find-related-notes
description: Sử dụng skill này khi cần tìm các note đã có trong vault liên quan đến chủ đề/keyword đang làm. Trigger trước khi soạn bài giảng, viết content, tạo atomic note mới, hoặc khi user hỏi "tôi đã viết gì về X chưa". Đây là skill core của bộ não 2 — tái sử dụng tri thức cũ.
---

# Skill: Find Related Notes

Tìm note liên quan trong vault TRƯỚC khi viết mới — tái sử dụng tri thức cũ là mục đích của bộ não 2.

## Khi nào dùng

- Trước khi soạn bài giảng → tìm atomic notes về chủ đề
- Trước khi viết blog/video script → tìm ý đã có
- Trước khi tạo atomic note mới → tránh trùng lặp
- Khi user hỏi "tôi đã viết gì về X chưa"
- Khi cần dẫn link `[[...]]` trong note mới

## Quy trình

### Bước 1: Xác định keyword

Từ yêu cầu của user, trích xuất:
- **Keyword chính:** 1-2 từ khóa quan trọng nhất
- **Keyword phụ:** 3-5 từ liên quan (synonym, broader, narrower)

Ví dụ: "Soạn bài về debug"
- Chính: `debug`, `error`
- Phụ: `bug`, `traceback`, `troubleshoot`, `exception`

### Bước 2: Scan vault có thứ tự ưu tiên

Tìm theo thứ tự (note càng chín càng ưu tiên):

1. **`50_Atomic/`** — atomic notes (cao nhất, đã chắt lọc)
2. **`20_Areas/`** — kinh nghiệm đúc kết
3. **`10_Projects/`** — note từ project (kể cả archive)
4. **`30_Resources/`** — tài liệu tham khảo
5. **`60_Daily/`** — daily notes (thấp nhất, thường thô)

### Bước 3: Match cách nào?

Sử dụng kết hợp:
- **Tên file** chứa keyword
- **Tag** trong frontmatter chứa keyword
- **Body text** chứa keyword (grep)
- **Wiki-link** từ notes khác trỏ đến

```bash
# Ví dụ tìm về "attention"
grep -r "attention" E:\Claude\SecondBrain\50_Atomic\ --include="*.md" -l
```

### Bước 4: Đánh giá độ liên quan

Với mỗi note tìm được, đánh giá:
- 🟢 **Rất liên quan:** keyword chính trong title/heading
- 🟡 **Liên quan:** keyword phụ trong body
- 🔘 **Mơ hồ liên quan:** chỉ match qua tag chung

### Bước 5: Báo cáo có cấu trúc

Output cho user (hoặc agent gọi skill này):

```
🔍 Tìm thấy 7 notes liên quan đến "debug" (sắp theo độ chín):

🌳 Atomic evergreen (đã chín, dùng được ngay):
- [[50_Atomic/methods/cach-day-debug-bang-rubber-duck]] 🟢
- [[50_Atomic/concepts/error-message-la-tin-hieu-khong-phai-lo-au]] 🟢

🌿 Atomic growing:
- [[50_Atomic/claims/sinh-vien-dung-chatgpt-de-debug-khong-giam-ky-nang]] 🟡

🔁 Areas (kinh nghiệm):
- [[20_Areas/teaching/cach-feedback-bai-tap-loi-cua-sv]] 🟡

🎯 Projects (note từ project):
- [[10_Projects/course-python-2026-spring/lectures/buoi-08-error-handling]] 🟢
- [[40_Archive/2025/course-python-2025-fall/lectures/buoi-09-debug]] 🟡

📚 Resources:
- [[30_Resources/programming/blog-debug-techniques-by-julia-evans]] 🔘

📝 Đề xuất:
- Dùng 3 atomic notes (🟢) làm xương sống bài giảng
- Tham khảo lecture cũ ở Archive để giữ tính nhất quán
- Có 1 claim (🟡) chưa được verify — có thể là câu hỏi mở cho sinh viên
```

### Bước 6: Để user/agent quyết dùng cái nào

KHÔNG tự động chèn link. Trình bày, để user/agent gọi quyết định.

## Lưu ý

- **Không bỏ qua Archive.** Project cũ chứa rất nhiều ý đã dùng được.
- **Không over-include.** Nếu match >15 notes, lọc lại keyword cho hẹp.
- **Empty result không phải lỗi.** Vault mới có thể chưa có note nào → báo "chưa có", không bịa.
- **Cross-reference.** Note A link đến B, B link đến C → C cũng có thể liên quan, mở rộng tìm.

## Tip nâng cao

Khi vault lớn (>500 notes), có thể dùng:
- Obsidian's graph view để hiểu cluster
- Plugin "Smart Connections" (semantic search) — không cần cấu hình thêm
- Plugin "Dataview" để query qua frontmatter
