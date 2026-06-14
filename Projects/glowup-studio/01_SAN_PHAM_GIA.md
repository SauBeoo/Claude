# 01 — Sản phẩm & Bảng giá

> 3 tầng, mũi nhọn là **WEB** (dễ chốt khách đầu), tiền bền nằm ở **Tầng 2 + 3** (dòng tiền lặp lại).
> Giá dưới đây là khung khởi điểm cho khách spa nhỏ/vừa ở VN — điều chỉnh theo quy mô tiệm & vùng.

---

## Tầng 1 · WEBSITE (một lần) — mũi nhọn

**"Website trọn gói cho spa"** — đẹp, chuẩn điện thoại, đầy đủ để khách tìm thấy & đặt lịch.

| Gói | Nội dung | Giá | Thời gian |
|---|---|---|---|
| **Cơ bản** | 1 trang (one-page) đẹp: giới thiệu, dịch vụ + giá, gallery, nút Gọi/Zalo/Map | **5–6 triệu** | 5–7 ngày |
| **Tiêu chuẩn** | 4–5 trang: Trang chủ · Dịch vụ & bảng giá · Hình ảnh (trước/sau) · Về tiệm · Liên hệ/Đặt lịch | **8–10 triệu** | 7–10 ngày |
| **Cao cấp** | Tiêu chuẩn + form đặt lịch + blog/SEO cơ bản + tối ưu Google Maps | **10–12 triệu** | 10–14 ngày |

**Luôn có trong mọi gói:**
- Mobile-first (khách spa ~90% xem điện thoại), load nhanh, đẹp đúng tông tiệm.
- Nút nổi **Gọi · Zalo · Đặt lịch** + nhúng Google Maps.
- Gallery hình ảnh / trước–sau.
- Footer "Made by GlowUp Studio ✦" (lan truyền thương hiệu).

> **Mẹo chốt:** luôn đưa khách xem demo `portfolio/demo-spa-01/` trước. "Mẫu này em làm cho tiệm giống bên mình — bên mình
> muốn tông nào ạ?" Bán cái nhìn-thấy-được, không bán lời hứa.

### 🌐 Tên miền & Hosting (PHẢI nói rõ khi báo giá)

Web có **2 loại chi phí** — tách bạch để khách không hiểu lầm "mua 1 lần xài mãi":

| Loại | Là gì | Tính chất |
|---|---|---|
| **Phí làm web** (5–12tr) | Tiền **công** thiết kế + dựng | **Một lần** |
| **Tên miền + hosting** | Chỗ web "sống" trên mạng | **Định kỳ hằng năm** |

- **Tên miền:** `.vn` ~**750–830k/năm**, `.com` ~**250–350k/năm** (số ước lượng — check lại nhà đăng ký).
- **Hosting:** web tĩnh/Astro/Next static → deploy **MIỄN PHÍ** (Vercel/Netlify/Cloudflare Pages), SSL free.
  Chỉ tốn phí khi khách cần thứ nặng (WordPress + DB, email theo tên miền) — spa nhỏ hầu như không cần.
  → Chi phí định kỳ thực tế gần như **chỉ là tên miền ~800k/năm**.

**Mô hình tính (đã chốt 14/06): "Năm đầu tặng → năm 2 gộp bảo trì".**
1. Giá web đã **bao tên miền + hosting MIỄN PHÍ năm đầu** (chi phí ~800k mình chịu, nhỏ — dùng làm điểm chốt).
2. **Từ năm 2** → mời vào gói **Bảo trì (Tầng 3)**: phí tháng đã gồm tên miền + hosting + cập nhật nội dung.
3. → Biến chi phí vận hành thành **dòng tiền lặp lại**, đúng triết lý "tiền bền ở Tầng 3".

> **Câu nói mẫu với khách:** *"Phí 8tr là tiền em dựng web, trả một lần thôi. Tên miền với chỗ đặt web
> thì **năm đầu em bao trọn** cho chị. Từ năm sau, gói bảo trì 500k/tháng em lo hết tên miền + chỗ đặt +
> cập nhật bảng giá, banner khuyến mãi — chị khỏi đụng tay kỹ thuật gì cả."*

---

## Tầng 2 · TỰ ĐỘNG HOÁ (n8n) — upsell + phí tháng

Chào **sau khi** web xong ("giờ mình tự động hoá luôn khâu chăm khách nhé"). Đây là chỗ giải đúng nỗi đau
lớn nhất của spa: **khách quên hẹn (no-show)** và **khách không quay lại**. Chi tiết flow: `02_N8N_AUTOMATION.md`.

| Gói | Nội dung | Setup (một lần) | Duy trì/tháng |
|---|---|---|---|
| **Nhắc hẹn** | Tự động nhắc lịch hẹn qua Zalo/SMS → giảm no-show | **3 triệu** | 500k |
| **Chăm khách** | Nhắc hẹn + cảm ơn & xin review sau buổi + nhắc quay lại (rebooking) | **5 triệu** | 800k–1tr |
| **Toàn diện** | Chăm khách + gom lead từ form/FB ads (auto trả lời + đặt lịch) + báo cáo doanh thu tuần | **8 triệu** | 1,2–1,5tr |

**Vì sao đáng tiền (cách nói với khách):**
> "Mỗi khách quên hẹn là một ghế trống = tiền mất. Hệ thống nhắc tự động kéo khách quay lại đều — phí
> duy trì 1 tháng thường chưa bằng 1–2 lượt khách quay lại."

---

## Tầng 3 · BẢO TRÌ + CONTENT (retainer) — dòng tiền lặp lại

| Gói | Nội dung | Giá/tháng |
|---|---|---|
| **Bảo trì web** | **Tên miền + hosting** + cập nhật nội dung/bảng giá + đổi banner khuyến mãi + backup | **500k–800k** |
| **Bảo trì + Content** | Bảo trì web + X bài/clip content mỗi tháng do vợ làm | **1,2–2 triệu** |

> Mục tiêu chiến lược: **gom 15–20 khách retainer** (Tầng 2 + 3) ≈ **10–30 triệu/tháng** gần như tự chảy.
> Đây mới là "thu nhập bền vững" — số web bán được chỉ là phương tiện để có khách retainer.

---

## Combo gợi ý (đóng gói cho dễ bán)

- **GlowUp Khởi đầu:** Web Cơ bản — *5–6tr*.
- **GlowUp Tỏa sáng:** Web Tiêu chuẩn + Automation Nhắc hẹn — *11–13tr* + 500k/tháng.
- **GlowUp Toàn diện:** Web Cao cấp + Automation Chăm khách + Bảo trì+Content — *17–20tr* + ~2,5tr/tháng.

---

## Nguyên tắc báo giá

1. **Luôn 3 mức** (neo giá): khách thường chọn mức giữa.
2. **Tách phí một lần và phí tháng rõ ràng** — đừng giấu phí duy trì.
3. **Cọc 50%** trước khi làm, 50% khi bàn giao.
4. Báo giá kèm **link demo** + thời gian hoàn thành cụ thể.
5. Với khách đầu tiên: có thể giảm để lấy **case study + cho quay clip** — đổi giá lấy chứng cứ.
6. **Luôn tách "phí làm web (một lần)" và "tên miền+hosting (định kỳ)"** — bao năm đầu, năm 2 mời vào bảo trì (xem mục Tên miền & Hosting ở Tầng 1).

---

↩ [[glowup-studio]] · tổng quan dự án & sơ đồ liên kết
