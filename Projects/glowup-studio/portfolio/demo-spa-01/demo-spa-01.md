# Demo Spa 01 — "Lụa Spa & Beauty"

Web demo đầu tiên của GlowUp Studio. **Mục đích kép:**
1. **Mẫu chào khách** — đưa chủ spa xem để họ hình dung ("tiệm mình cũng có web đẹp vậy").
2. **Nguyên liệu content** — quay clip trước/sau khai trương kênh TikTok (xem `03_CONTENT_SOCIAL.md`).

> Đây là tiệm **giả định** để demo. Không phải khách thật.

---

## Cách xem

Double-click `index.html` → mở bằng trình duyệt. **Không cần cài gì** (Tailwind + font + ảnh tải qua CDN,
nên cần mạng để hiển thị ảnh & style).

## Cách deploy (miễn phí, để có link gửi khách)

- **Netlify Drop:** kéo-thả thư mục `demo-spa-01` vào https://app.netlify.com/drop → có link ngay.
- **Vercel:** `vercel` trong thư mục này, hoặc kéo lên qua dashboard.
- **GitHub Pages:** push lên repo, bật Pages.

---

## Có gì trong demo

- Mobile-first, tông màu thương hiệu (kem/hồng/champagne/nâu), font Playfair + Be Vietnam Pro.
- Nút nổi **Gọi · Zalo · Đặt lịch**.
- Các mục: Hero · Dịch vụ · Bảng giá (3 mức) · Hình ảnh · Về tiệm · Form đặt lịch + bản đồ · Footer.
- Footer "Made by GlowUp Studio ✦" — mỗi web là một danh thiếp lan truyền.

## Tuỳ biến nhanh cho từng khách

- Đổi tên tiệm: tìm "Lụa Spa" trong `index.html`.
- Đổi màu: sửa `tailwind.config` ở phần `<head>` (các mã HEX).
- Đổi ảnh: thay URL Unsplash bằng ảnh thật của tiệm.
- Đổi dịch vụ/giá: sửa trong section `#dich-vu` và `#bang-gia`.
- Form đặt lịch hiện chỉ là demo (chưa gửi đi). Khi làm khách thật → nối vào Google Sheet/Zalo
  bằng n8n Flow 5 (xem `02_N8N_AUTOMATION.md`).

---

## Đường nâng cấp (sau này)

Bản này cố tình là **1 file HTML tĩnh** để xem/deploy tức thì. Khi cần web khách nhiều trang, có blog/SEO,
hoặc khách tự sửa nội dung → chuyển sang **Astro** hoặc **Next.js + Tailwind** (xem stack trong `CLAUDE.md`),
giữ nguyên hệ màu & font để nhất quán thương hiệu.
