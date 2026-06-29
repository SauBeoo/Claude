# Lead Tool — 1 trang giấy (bản nháp v0) — ⛔ ĐÃ GẤP LẠI

> **KẾT LUẬN (2026-06-25): KHÔNG theo đuổi ý "bán tool/bán data" này nữa.** Lý do: (1) bán lại data đi cào = commodity biên lợi nhuận quá mỏng, nhà cung cấp còn là đối thủ; (2) mua/bán dữ liệu cá nhân bị Luật BVDLCN (hiệu lực 1/1/2026) cấm, phạt tới 3 tỷ.
>
> ➡️ **Năng lực gom lead được giữ lại, chuyển thành PHỄU đi săn khách cho GlowUp.** Thiết kế thực tế ở: `Projects/glowup-studio/07_PHEU_KHACH.md`.
>
> Phần dưới giữ làm nhật ký phân tích (để khỏi đi lại vết xe đổ).

---

> Tên còn tạm, đổi sau. Mục tiêu trang này: **chốt bán cái gì, cho ai, giá bao nhiêu — trước khi đụng 1 dòng code.**
> Nguyên tắc: chỉ làm 1 tool (gom lead). 3 tool kia (auto đăng / nuôi acc / AI content) để SAU khi cái này có khách trả tiền.

---

## 1. Một câu định nghĩa
Tool chạy trên web, gom danh sách khách tiềm năng (lead) theo ngành/khu vực, **xuất ra file dùng được ngay** cho dân chạy ads / sale / MMO. Thu phí **theo tháng**, không bán đứt.

## 2. Cào nguồn nào (chọn 1 để làm MVP, đừng ôm hết)

> ⚠️ **CHỐT QUAN TRỌNG (2026-06-25):** Việt Nam nằm trong **Google Maps Platform Prohibited Territories**. ⇒ **KHÔNG tự gọi Google Maps Platform API từ VN** — không hợp pháp, billing không sống, key bị khoá bất kỳ lúc nào. (Đây cũng là lý do thật khiến lead-engine GlowUp bị `403`.) Nếu muốn data Maps → phải qua bên thứ 3.

| Nguồn | Lấy được gì | Độ khó | Ghi chú |
|---|---|---|---|
| **Bên thứ 3 cào Maps** (Outscraper / SerpAPI / Apify) ⭐ | Tên, SĐT, địa chỉ, web, rating | Thấp (gọi API họ) | **ƯU TIÊN xét đầu tiên** — họ gọi từ US, mình chỉ trả tiền/kết quả → né được lệnh cấm VN. CẦN kiểm: giá/1.000 kết quả + có lãi sau khi cộng giá bán không. |
| Tự scrape web Maps công khai | như trên | Cao | DIY, vẫn vi phạm ToS Google, mong manh (IP ban) → nền xám, cân nhắc kỹ |
| Web vàng / niên giám / sàn VN | SĐT, ngành, địa chỉ | Thấp | Nguồn nội địa, ít rủi ro pháp lý hơn, data tạp hơn |
| Fanpage / Group FB | Tên page, link, follow | Cao | Hay bị khoá → làm sau |

→ **MVP: ưu tiên thử bên thứ 3 trước.** Nếu giá họ ăn hết margin → quay sang nguồn nội địa VN. **Bỏ hẳn ý "tự gọi Google Maps Platform API".**

## 3. Lấy field gì (output)
Xuất file **Excel/CSV**, mỗi dòng 1 lead:
`Tên cơ sở | SĐT | Địa chỉ | Quận/Tỉnh | Ngành | Website (có/không) | Rating | Link Maps`

> Field "có website hay không" rất giá trị — dân bán dịch vụ web/marketing lọc đúng tệp "chưa có web" để chào hàng. (Đây cũng đúng tệp GlowUp luôn → 1 mũi tên 2 đích.)

## 4. Bán cho ai (chọn 1 chân dung khách đầu tiên)
- **Dân chạy ads / agency nhỏ** — đói data để gọi/nhắn. Trả tiền đều nhất. ⭐ ƯU TIÊN
- Dân sale B2B (bảo hiểm, phần mềm, thiết bị) — cần lead theo ngành.
- Chính mày / GlowUp — khách "số 0", dùng nội bộ để gom lead spa.

→ Khách đầu tiên nên là **chính mày + 3-5 người quen chạy ads** để test. Đừng mở bán đại trà ngày 1.

## 5. Giá (theo tháng, không bán đứt)
| Gói | Giá/tháng (nháp) | Hạn mức |
|---|---|---|
| Dùng thử | 0đ | 50 lead / lần, 1 lần |
| Cơ bản | 199k | 2.000 lead/tháng |
| Pro | 499k | 10.000 lead/tháng + lọc nâng cao |

> Con số là phỏng đoán — chốt thật sau khi hỏi 3-5 khách "trả bao nhiêu thì mua".

## 6. Vì sao không bị crack
Logic cào nằm trên **server của mày**. Khách chỉ thấy web + bấm nút + tải file. Không có file .exe để share lậu → moat tự nhiên.

## 7. MVP nhỏ nhất có thể bán (làm đúng từng này, không hơn)
1. 1 trang web: ô nhập **ngành + khu vực** → bấm → tải CSV.
2. Engine cào Google Maps (tái dùng cách lead-engine).
3. Đăng nhập + giới hạn lượt theo gói (license theo tài khoản).
4. 1 cổng thanh toán VN (chuyển khoản/Momo) — lúc đầu duyệt tay cũng được.

## 8. Câu hỏi sống còn chưa trả lời (điền trước khi code)
- [ ] Chi phí cào 1.000 lead Google Maps là bao nhiêu? (API/proxy) → quyết định giá có lãi không.
- [ ] 3-5 người quen chạy ads có thật sự trả 199k/tháng không? (đi hỏi, đừng đoán)
- [ ] Pháp lý/ToS: cào Google Maps ở mức này rủi ro tới đâu?

---
**Bước kế tiếp đề xuất:** trả lời 3 câu mục 8 (nhất là cái chi phí + đi hỏi 3 người) → rồi mới dựng MVP.
