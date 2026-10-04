# CAST + FX PROPS cho kênh 古代の秘訣 — bộ gen 1 lần, dùng cho MỌI video sau

> user chốt 2026-08-18: **avatar = ảnh AI thật (photoreal)** + **FX dày (mỗi 30–40 giây một hiệu ứng)**.
> Bơm `CAST_FLOW.txt` (mỗi prompt 1 dòng) vào extension. Tên file đích ở `CAST_NAMES.txt`.

## 🔴 HỆ QUẢ PHẢI BIẾT TRƯỚC — video sẽ phải TICK "altered/synthetic content"

`youtube-compliance.md` §2.1 (đảo chiều 2026-08-09) cho phép dùng ảnh AI người **hư cấu** trong video,
**đổi lại bắt buộc tick ô khai báo khi upload**. Từ video 21 trở đi, mọi video co-dai có avatar đều
phải tick — `upload_pack.py` chưa có cờ này nên **phải tick TAY trong Studio**.

⛔ **Không đổi**: cấm mặt người thật cụ thể · cấm dàn dựng sự kiện/địa điểm có thật · cấm nhân vật
xưng bác sĩ/chuyên gia · **thumbnail vẫn KHÔNG dùng mặt người** (luật kênh 2026-08-05 giữ nguyên).

## ⚙️ Yêu cầu kỹ thuật cho CẢ 7 ảnh

- **Nền XÁM PHẲNG đồng nhất** (không hoa văn, không đồ vật) — `rembg` cắt nền sạch hơn hẳn.
- **Ánh sáng dịu, đều, không đổ bóng gắt** — bóng gắt làm viền cutout rách.
- Toàn thân hoặc 3/4 người, chừa lề quanh người.
- **Không chữ, không logo, không watermark.** Ảnh có ✦ tao vẫn cắt được nhưng cắt là mất lề.
- ⭐ **NHẤT QUÁN NHÂN VẬT** là chỗ khó nhất: 3 ảnh của 語り手 phải ra CÙNG một người. Gen cả 3 trong
  một lượt, cùng seed nếu tool cho phép. Ra khác mặt thì gen lại — avatar đổi mặt giữa video là hỏng.

## 👤 Nhân vật 1 — 語り手 (người kể, khớp giọng nam trầm 青山龍星)

Nam Nhật **58 tuổi**, tóc ngắn muối tiêu, **áo sơ mi xám xanh** tay dài, quần vải sẫm, dáng điềm đạm.
Xuất hiện ở: câu tự trào (「白状しますと…」), câu chỉ dẫn (「〜してください」), câu chốt triết lý.

| tên file | tư thế |
|---|---|
| `kataribe_talk.png` | đứng thẳng, hai tay hơi mở, đang nói, nhìn về phía người xem |
| `kataribe_point.png` | **chỉ tay sang PHẢI**, thân hơi nghiêng theo tay |
| `kataribe_wry.png` | gãi gáy, cười ngượng nhẹ (dùng cho câu tự trào 3 hộp thuốc tẩy) |

## 👵 Nhân vật 2 — 母 (mẹ, trong hồi ức)

Bà cụ Nhật **78 tuổi**, tóc bạc búi gọn, **tạp dề hoa nhạt** ngoài áo len mỏng màu kem.
Xuất hiện đúng 2 chỗ: câu thoại 「お客さんの来る家は、風呂場でわかるのよ」 (phút 2) và khi câu đó
quay lại ở phút 19.

| tên file | tư thế |
|---|---|
| `haha_talk.png` | đứng nói, hai tay lau vào tạp dề, vẻ mặt bình thản |
| `haha_back.png` | **quay lưng đi**, nhìn nghiêng qua vai (câu 「また台所へ戻っていきました」) |

## 💬 Prop bổ sung — bong bóng thoại (bộ props hiện có chưa có)

Vẽ **bút sáp trắng viền đỏ trên nền trắng phẳng**, cùng chất liệu với `arrow_curve.png`/`circle_1.png`
đã có, **ruột RỖNG** (tao đổ chữ vào sau).

| tên file | mô tả |
|---|---|
| `bubble_left.png` | bong bóng bầu dục, **đuôi chỉ xuống-TRÁI** |
| `bubble_right.png` | bong bóng bầu dục, **đuôi chỉ xuống-PHẢI** |

## 📋 Sau khi mày gen xong

Quăng vào một folder Downloads rồi báo tao. Tao sẽ: cắt nền bằng `rembg` → kiểm viền cutout →
nhập vào `_media_library/props/` (bubble) và `_media_library/avatars/co-dai/` (cast) → nối vào
`make_shot.py` → dựng lại clip.
