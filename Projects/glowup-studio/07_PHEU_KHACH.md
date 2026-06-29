# Phễu khách GlowUp — từ danh sách thô → hợp đồng web/automation

> Chốt hướng (2026-06-25): KHÔNG bán tool/bán data (commodity biên mỏng + dính Luật BVDLCN — xem memory `project-vn-data-law-lead`). Thay vào đó: **dùng năng lực gom lead làm PHỄU đi săn khách cho GlowUp.** Cùng 1 con dao, nhưng tự đào vàng thay vì bán dao.
>
> Kinh tế học khác một trời vực: 50 lead tốn ~0đ (Outscraper free 500) → chốt 1 hợp đồng web = 5–15 triệu. ROI gấp hàng trăm lần so với bán data 199k.

## Cần xây gì (tối thiểu — đừng hơn)
1. **Cách gom:** Outscraper (free 500 lead) hoặc Apify actor rẻ → export CSV. KHÔNG tự gọi Google Maps API từ VN.
2. **1 Google Sheet** = vừa lọc/chấm điểm vừa theo dõi trạng thái. (Không cần web/app.)
3. **Kịch bản chào** (gọi + Zalo). Hết. Bắt tay làm được ngay tuần này.

---

## 6 bậc phễu

### Bậc 0 — GOM
- Nguồn: Google Maps qua bên thứ 3. Lọc theo: **spa / nail / salon** + **1 quận mục tiêu** (làm 1 quận trước, đừng rải).
- Field lấy: `Tên tiệm | SĐT | Địa chỉ | Quận | Có website? | Rating | Số review | Link Maps`.
- Hợp pháp: gom thông tin tiệm công khai để tự dùng. KHÔNG bán lại.

### Bậc 1 — LỌC & CHẤM ĐIỂM (đây là bí quyết)
Bộ lọc vàng = **tiệm CHƯA CÓ WEBSITE** (hoặc web cũ/rác). Đó đúng là người cần thứ GlowUp bán.
Chấm hạng:
- **Hạng A** (ưu tiên săn): chưa có web + rating 3.8–4.8 + nhiều review (>50). → Tiệm đông khách = có tiền = đáng làm web, mà lại đang thiếu web.
- **Hạng B**: chưa có web nhưng ít review / mới mở.
- **Hạng C**: đã có web ổn → bỏ qua (chưa phải khách bây giờ).
→ Output: shortlist **20–50 tiệm hạng A** ở 1 quận.

### Bậc 2 — CHUẨN BỊ MỒI (cá nhân hoá, 2 phút/tiệm)
Với mỗi tiệm hạng A:
- Search Google "spa + [khu vực]" → chụp màn hình: tiệm họ **không** ra, mà **đối thủ có web** ra trên.
- Ghi 1 quan sát cá nhân hoá để mở lời. Đây là thứ biến "spam" thành "tư vấn" — và giữ mày đúng phía Nghị định 91 (mang giá trị, không phải rác).

### Bậc 3 — CHẠM (đa điểm, đúng luật NĐ 91/2020)
- Kênh: **Zalo / gọi trong 8h–17h**, **tối đa 1 cuộc/24h/số**. Có cho từ chối (opt-out).
- **Chạm 1 (gọi/Zalo):** câu mở giá trị → xin 2 phút.
- **Chạm 2 (sau 2–3 ngày nếu im):** gửi screenshot "khách search không thấy tiệm mình".
- **Chạm 3:** chốt 1 lịch tư vấn 15 phút.

**Kịch bản mở mẫu (sửa giọng của mày):**
> "Chào chị, em xem trên Google thấy tiệm mình **4.8 sao, hơn 200 review** — khách quý tiệm thật. Mà em thử search 'spa [khu vực]' thì lại ra mấy tiệm khác có website lên trước, tiệm mình không thấy đâu. Em làm web cho spa, có cách kéo tiệm mình lên. Chị cho em xin **2 phút** em chỉ chị xem nhé?"

### Bậc 4 — TƯ VẤN & CHỐT (15 phút)
- Show demo / screenshot. Chỉ ra **nỗi đau**: mất khách vào tay đối thủ có web.
- Giải pháp = gói GlowUp (web + automation). Mồi: làm **landing demo trước**, thích thì làm full.

### Bậc 5 — ĐO & LẶP
Đếm phễu từng bậc để biết nghẽn ở đâu:
`Lead A gom → Chạm được → Quan tâm → Hẹn tư vấn → Chốt`
Giả định thực tế để chạy thử: **100 lead A → 40 chạm → 10 quan tâm → 4 hẹn → 1–2 chốt.**

---

## Việc cụ thể MẺ ĐẦU (làm tuần này)
1. Chọn **1 quận** (vd Q.Tân Bình).
2. Gom **50 spa/nail hạng A chưa có web** (Outscraper free).
3. Cá nhân hoá + **chạm 20 tiệm**.
4. Mục tiêu: **1–2 buổi tư vấn**, kỳ vọng **1 hợp đồng**.
→ Xong mẻ này mày có số thật (tỷ lệ chốt) để biết phễu sống hay cần chỉnh — trước khi nhân rộng.
