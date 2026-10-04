# BẢNG CHẤM GIỮ CHÂN TRƯỚC KHI GIAO — showa (chốt 2026-09-23)

> user: *"tao muốn video phải thật hấp dẫn, chứ không phải ghép vài cái video vào là được"* → *"có nhé"* (lưu bảng chấm thành gate cố định).
> Chấm **SAU render, TRƯỚC khi giao** — trên chính file mp4, không trên plan.
> ⚠️ Bảng này đo **lỗi dựng đã biết làm người xem thoát**, KHÔNG đo retention thật. Retention thật = Studio (đường giữ chân · mốc 60s · AVD) sau khi đăng.

## Cách chấm
Trích frame **mỗi ô của 60s đầu** (1 frame giữa ô, cỡ thật 1920) + 10 frame rải đều cả bài → soi từng dòng dưới.
**30s đầu < 8/10 thì KHÔNG GIAO**, dựng lại. Ghi điểm + lý do vào `06_VIDEO/<slug>/HOOK_SCORE.md`.

## A. 30 GIÂY ĐẦU (10 điểm — mỗi dòng 1 điểm, sai là 0)
| # | câu hỏi | ca gốc làm ra dòng này |
|---|---|---|
| A1 | Frame 0 có **khớp câu đang đọc** không (che phụ đề vẫn đoán được câu nói gì)? | v18 bản 1: phố đổ nát dưới câu 「母親の葬式の夜」 |
| A2 | Frame 0 có **màu + nét** (không phải phim 360p phóng lên, không đen trắng nhiễu)? | v18 bản 1 |
| A3 | **Chủ thể của bài** (vật/nhân vật chính) **hiện ra trước giây 10** và **không bị phụ đề đè**? | v18: hộp bánh nằm dưới dải phụ đề |
| A4 | **Một nhân vật = một khuôn mặt** suốt 30s (không 3–4 "ông con út" khác nhau)? | v18: 4 mặt trong 30s |
| A5 | Mỗi **danh từ người/vật được đọc lên** có **hình của chính nó** đúng lúc đó? | v18: đọc 「父」 mà hình là chị ở xưởng dệt |
| A6 | Không ô nào **đứng yên/vắng người** quá 4s trong 30s đầu (có người đang làm gì đó)? | |
| A7 | **Câu hỏi treo** (open loop) có trong ≤30s và có **hình nhấn** đi kèm (gương mặt/vật được hỏi)? | |
| A8 | Hành động trong clip AI **đúng lời** (tay mở hộp thì hộp phải đang mở ra, không lơ lửng)? | v18: tay lơ lửng trên hộp đã mở sẵn |
| A9 | 0 chữ AI méo · 0 lính/xe Mỹ · 0 slate · 0 biển tiếng Anh trong khung? | v16 GRAND KYOTO · v18 「お供え」 |
| A10 | Có **1 nhịp tiếng** đúng khoảnh khắc (nắp hộp · còi tàu · giấy) hoặc 1 nhịp **im lặng** trước câu chốt? | |

## B. CẢ BÀI (báo cáo, dòng 🔴 thì chặn)
| # | kiểm | ngưỡng |
|---|---|---|
| B1 | nguồn phim thật đều **≥720p gốc** (không 640×360) | 🔴 chặn nếu còn ô 360p/đen trắng khi đã có bản màu |
| B2 | không ô nào lặp hình trong bài · không trùng sổ đen | 🔴 |
| B3 | mỗi mục mở bằng **khuôn neo** của bài (vd: cái hộp → phong bì → phim năm đó) | báo |
| B4 | chip chương nhìn thấy ở mỗi mục | báo |
| B5 | `make_cells_v3` MAD >3 mọi ô tĩnh · `check_realism` cho ô AI | 🔴 (luật cũ, giữ) |
| B6 | 10 frame rải đều: không frame nào "chết" (không người, không động, không liên quan lời) | báo |

## Lịch sử điểm
| video | bản | A (30s đầu) | ghi chú |
|---|---|---|---|
| 18 hataraku-okane | render 1 (23/09 19:56) | **4/10** | A1 A2 A3 A4 A5 A8 rớt — dựng lại: phim màu 720p + khuôn hộp + 3 gương mặt + SFX |
| 18 hataraku-okane | render 2 HD (23/09 23:08) | **7/10** | A1 ✅ me that nau bep · A2 ✅ mau 720p · A3 ✅ hop o giay 33 (muon) · A4 🟡 ong cu AI chi 1 o · A5 🔴 「兄・姉・父」 cung 1 dong nguoi · A6 ✅ · A7 ✅ · A8 ✅ · A9 ✅ · A10 🔴 chua co SFX. Quet lap: 0 cap o trung. User chon render ban nay (khong dung lai theo v08) |
| 17 kaisha-ga-kureta | mức B (24/09 13:03) | **7/10** | thay 49/66 ô phim 1946 bằng ảnh 1971 + phim 1957–59; A4 🔴 3 mặt cho "ある会社員" · A7 🔴 không câu hỏi treo · A10 🔴 chưa SFX |
| 17 kaisha-ga-kureta | hook Q + SFX (24/09 14:00) | **9/10** | A4 ✅ (chấm lại: một người) · A7 🟡 câu hỏi ở 0:34 · A10 ✅ 発車ベル 0:05 |
| 19 kaimono-joushiki | v08, 17:31 26/09 | **8/10** | A5 🔴 không hình 質札 · A6 🔴 風呂敷/がま口 vắng người 5–7s · A9 bản 1 rớt (がま口 có quảng cáo+URL) → đã thay. 93,4% hình thật; gate lặp hình theo nguồn+dHash |
| 20 sumai-okane | render b (27/09 22:48) | **10/10** | ban 1 = 8/10 (clip Pexels chu viet tay tieng Anh o cau hoi treo; user: 30s dau qua nhieu AI/khong thoi Showa) → thay 3 o AI bang anh THAT (hagaki 1949 · danchi slide · hom thu 1971) + tieng ngan keo 0:02. Quet trung bang mat: go 6 cap (anh tinh cung khung clip do chinh minh chen khi chẻ khe + 4 anh ruong lua) |
| 20 sumai-okane | v3 hook B+ (28/09 01:06) | **10/10** | user van thay "chua thu hut" o ban 10/10 truoc → **bang cham 10 dong KHONG do duoc "co tranh luan/dong cam"**; them hook xung dot + cau hoi chon phe. Mot bai hoc: diem 10/10 cua bang nay la dieu kien CAN, khong du |
