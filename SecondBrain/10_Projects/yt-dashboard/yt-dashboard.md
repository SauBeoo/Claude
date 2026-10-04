# yt-dashboard

Folder-note tri thức cho project **yt-dashboard** — web dashboard local quản lý pipeline YouTube 6 kênh.

- Repo code: `E:\Claude\Projects\yt-dashboard\` (xem `yt-dashboard.md` trong repo để biết cách chạy + kiến trúc)
- Ra đời: 2026-07-19, sau khi hoàn thiện bộ engine CLI (upload_pack / pipeline_status / analytics_report)

## Quyết định thiết kế đáng nhớ

1. **Local web, không phải hosted/artifact** — UI phải đọc/ghi filesystem + chạy tool local (đóng gói, move kho, mở folder) → bắt buộc chạy trên máy; localhost = không lo bảo mật.
2. **Dashboard là lớp vỏ, engine là nguồn sự thật** — không viết lại logic nghiệp vụ; đọc = import hàm, ghi = subprocess gọi CLI (giữ log chuẩn + isolation sys.exit). Nhờ vậy CLI và web luôn cho kết quả giống nhau.
3. **Tái sử dụng qua `config.json → tools_dir`** — trỏ sang bộ engine khác là chạy cho workspace/bộ kênh khác, không sửa code.
4. Điểm ăn tiền UX: **Panel Upload copy-từng-ô** thay cho mở METADATA.txt bôi đen thủ công.

## Bài học

- (chưa có — bổ sung khi vận hành thực tế)
