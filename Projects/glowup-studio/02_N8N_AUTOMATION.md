# 02 — Playbook Tự động hoá (n8n) cho spa

> Đây là tầng tạo **dòng tiền lặp lại** và là khác biệt lớn của GlowUp so với "thợ làm web" thường.
> Tái dùng know-how n8n self-hosted từ project `ai-luoi`.
> Lượt này là **spec/playbook** — code workflow `.json` sẽ build dần vào `templates/`.

---

## Nỗi đau của spa mà automation giải (bán theo cái này)

1. **No-show / quên hẹn** → ghế trống = mất tiền trực tiếp. ⭐ ưu tiên #1.
2. **Khách không quay lại** → spa sống nhờ khách quay lại đều, nhưng không ai nhắc.
3. **Ít review** → khách mới không tin nếu Google/Facebook trống đánh giá.
4. **Lead rơi rớt** → khách nhắn FB/inbox lúc tiệm bận → trả lời trễ → mất khách.
5. **Chủ không nắm số liệu** → không biết tuần này bao nhiêu lịch, doanh thu bao nhiêu.

---

## Danh sách flow (theo độ ưu tiên & độ dễ)

### ✅ Flow 1 — Nhắc lịch hẹn tự động  *(ưu tiên #1, dễ, bán kèm gói Nhắc hẹn)*
- **Trigger:** lịch hẹn trong Google Sheet / Google Calendar (hoặc form đặt lịch trên web).
- **Hành động:** trước hẹn 24h và 2h → gửi tin nhắn Zalo/SMS nhắc khách.
- **Kết quả bán được:** "giảm khách quên hẹn".
- **Node chính:** Schedule/Cron → đọc Sheet → lọc hẹn sắp tới → gửi Zalo ZNS/SMS → đánh dấu "đã nhắc".

### ✅ Flow 2 — Cảm ơn + xin review sau buổi  *(dễ, tăng uy tín)*
- **Trigger:** sau giờ hẹn X giờ (lịch chuyển trạng thái "đã xong").
- **Hành động:** gửi lời cảm ơn + link đánh giá Google/Facebook + (tuỳ chọn) mã giảm giá lần sau.
- **Kết quả bán được:** "tự động gom đánh giá 5 sao".

### ✅ Flow 3 — Nhắc quay lại (rebooking)  *(tiền nằm ở đây — khách cũ)*
- **Trigger:** sau buổi gần nhất X tuần (theo loại dịch vụ: nail ~3–4 tuần, facial ~4–6 tuần…).
- **Hành động:** nhắn "đến lúc chăm sóc lại rồi nè" + ưu đãi nhẹ + link đặt lịch.
- **Kết quả bán được:** "kéo khách cũ quay lại đều".

### ✅ Flow 4 — Sinh nhật + ưu đãi  *(giữ khách, dễ)*
- **Trigger:** ngày sinh khách (từ data) → trước 3 ngày.
- **Hành động:** lời chúc + voucher sinh nhật tự động.

### ⚙️ Flow 5 — Gom lead + auto trả lời  *(khó hơn, gói Toàn diện)*
- **Trigger:** form web / tin nhắn Facebook Page / FB Lead Ads.
- **Hành động:** tự động trả lời ngay ("cảm ơn anh/chị, bên em sẽ gọi lại…") + lưu lead vào Sheet +
  thông báo chủ tiệm + (tuỳ chọn) đề xuất khung giờ đặt lịch.
- **Kết quả bán được:** "không bỏ sót khách nhắn lúc tiệm bận".

### 📊 Flow 6 — Báo cáo doanh thu/lịch tuần  *(giữ chân khách retainer)*
- **Trigger:** mỗi sáng Thứ 2.
- **Hành động:** tổng hợp lịch hẹn + doanh thu tuần trước từ Sheet → gửi chủ tiệm qua Zalo/email.

---

## Tech & công cụ

| Thành phần | Lựa chọn |
|---|---|
| Engine | **n8n self-hosted** (founder deploy — miễn phí, kiểm soát data) |
| Lưu data | **Google Sheets** (khách xem được, đơn giản) → Supabase/Postgres khi scale |
| Nhắn tin | **Zalo OA / Zalo ZNS** (chính ở VN), **SMS brandname** (qua NCC VN), email backup |
| Đặt lịch | Form trên web (Tầng 1) đẩy thẳng vào Sheet/Calendar |
| Lịch | Google Calendar hoặc Sheet (tuỳ khách quen cái nào) |

---

## Nguyên tắc khi build (cho Claude Code & founder)

- **Không hardcode key/token** — dùng credential/env của n8n.
- **Mỗi template có README**: cách import, cần điền gì (Zalo OA ID, Sheet ID…), cách test.
- **Comment từng node bằng tiếng Việt** — vì có thể bàn giao cho người không rành kỹ thuật.
- **Test với 1–2 record giả** trước khi chạy thật (tránh spam tin nhắn khách).
- **Tôn trọng quy định nhắn tin** (Zalo ZNS cần template duyệt; tránh gửi giờ khuya; có opt-out).
- Đóng gói export `.json` vào `templates/` kèm ảnh chụp luồng.

---

## Lộ trình build templates (sau giai đoạn chào khách)

1. Build **Flow 1 (Nhắc hẹn)** đầu tiên — dễ nhất, demo được ngay, bán được ngay.
2. Có khách Tầng 2 đầu tiên → build Flow 2 + 3 cho chính khách đó (vừa làm vừa hoàn thiện template).
3. Chuẩn hoá thành "Automation Pack cho spa" tái dùng cho mọi khách sau → biên lợi nhuận tăng dần.
