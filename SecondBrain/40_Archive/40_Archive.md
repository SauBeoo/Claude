# 40_Archive — Đã hoàn thành

Project xong → vào đây. **Không xóa** — vì 1 năm sau bạn vẫn có thể cần đọc lại.

## Tổ chức

```
40_Archive/
├── 2024/
├── 2025/
└── 2026/
```

Mỗi năm 1 thư mục con. Project archive đặt theo tên gốc:

```
40_Archive/2025/<project-name>/
40_Archive/2026/<project-name>/
```

Ví dụ giả định: `40_Archive/2026/course-python-2026-spring/` sau khi khóa học kết thúc.

## Quy trình archive

Khi project xong, trước khi `mv` vào đây, hãy làm checklist:

- [ ] Đã chắt lọc ít nhất 3 atomic notes từ project này chưa? (`50_Atomic/`)
- [ ] Đã thêm "post-mortem.md" trong project: cái gì hay, cái gì dở, nếu làm lại sẽ làm khác?
- [ ] Đã update note dự án (folder note) với status "DONE — <ngày>"?
- [ ] Outputs cuối cùng (paper, slide, video link) đã được lưu trong `outputs/`?

Sau đó:
```bash
mv 10_Projects/<project-name> 40_Archive/2026/
```

## Tại sao không xóa?

- Bạn sẽ thường xuyên cần tham chiếu lại cách bạn đã làm trước đây
- Atomic notes ở `50_Atomic/` có link ngược về project gốc — xóa project sẽ làm broken link
- Disk dung lượng rẻ, ký ức công việc thì không
