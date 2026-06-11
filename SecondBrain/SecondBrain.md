# SecondBrain — Bộ não thứ 2

Đây là vault Obsidian dùng làm bộ não thứ 2 cho công việc nghiên cứu, giảng dạy, lập trình và sáng tạo content.

## Tổ chức theo PARA + Atomic

| Thư mục | Mục đích | Đặc điểm |
|---|---|---|
| `00_Inbox/` | Vùng đệm cho mọi thứ mới | Phải dọn trong 7 ngày |
| `10_Projects/` | Việc đang làm, có deadline | Xong → chuyển sang `40_Archive` |
| `20_Areas/` | Trách nhiệm/vai trò dài hạn | Duy trì mãi |
| `30_Resources/` | Tham khảo theo chủ đề | Tích lũy mãi |
| `40_Archive/` | Project đã hoàn thành | Đóng băng, chỉ đọc |
| `50_Atomic/` | Ý tưởng đã chắt lọc, liên kết | Trái tim của bộ não 2 |
| `60_Daily/` | Daily note, journal | Theo ngày |
| `99_Meta/` | Template, MOC, cấu hình | Hạ tầng của vault |

## Quy tắc 3 câu

1. **Note mới** → quăng vào `00_Inbox/` trước, phân loại sau.
2. **Ý tưởng chín** → viết thành atomic note ở `50_Atomic/`, liên kết bằng `[[wiki-link]]`.
3. **Project xong** → move sang `40_Archive/<năm>/`, không xóa.

## Quy tắc khi làm việc với Claude Code

Xem `.claude/CLAUDE.md` ở root vault này.

## Khởi tạo lần đầu

```bash
# Mở vault này trong Obsidian
# File > Open vault > chọn thư mục này

# (Tùy chọn) Init Git
git init
git add .
git commit -m "init: vault structure"
```
