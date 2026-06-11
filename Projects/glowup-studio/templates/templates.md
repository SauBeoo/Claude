# templates/ — Tài sản tái dùng

Nơi chứa các "khuôn" dùng đi dùng lại cho mọi khách (biên lợi nhuận tăng dần theo thời gian).

> Hiện **trống** — sẽ điền dần khi có khách thật. Đây là chủ đích, không phải thiếu sót.

## Sẽ chứa

- `n8n/` — workflow tự động hoá export `.json` (xem playbook `02_N8N_AUTOMATION.md`):
  - `flow-1-nhac-hen.json` (build trước — dễ & bán được ngay)
  - `flow-2-xin-review.json`
  - `flow-3-rebooking.json`
  - mỗi file kèm `README` hướng dẫn import + cần điền gì (Zalo OA ID, Sheet ID…).
- `tin-nhan/` — mẫu tin nhắn Zalo/SMS (nhắc hẹn, cảm ơn, rebooking, sinh nhật).
- `bao-gia/` — mẫu báo giá 3 mức (xem `01_SAN_PHAM_GIA.md`).
- `web/` — (tuỳ chọn) khung web spa nhiều trang khi chuyển sang Astro/Next.

## Quy tắc

- Không commit API key/token thật vào template (dùng env/credential n8n).
- Mỗi template phải "khách không rành kỹ thuật cũng dùng được" — comment tiếng Việt, README rõ ràng.

---

↩ [[glowup-studio]] · tổng quan dự án & sơ đồ liên kết
