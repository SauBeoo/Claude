# 20_Areas/learning

Nơi lưu các **learning track** do skill `tutor` tạo — mỗi chủ đề user đang được dạy là một thư mục con:

```
learning/
└── <chu-de-slug>/
    ├── _track.md       # lộ trình + tiến độ + nhật ký buổi học (template: learning-track)
    └── flashcards.md   # thẻ ôn tập spaced-repetition (template: flashcards)
```

- Atomic note chắt lọc từ buổi học vẫn nằm ở `50_Atomic/` chung (qua skill `create-atomic-note`).
- Trạng thái module: ⬜ chưa học · 🟡 đang học · ✅ đã thạo · 🔁 cần ôn lại.
- Track `status: done` có thể archive sang `40_Archive/` khi học xong hẳn.
