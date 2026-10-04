# HeyGen — người dẫn nhép miệng theo giọng VOICEVOX (kinishinai bài 1, demo)

> Khuôn mẫu: video `ku8qF5wrFxg` (介護保険料) — người dẫn ~21% thời lượng, 14 lần, trung vị 9s; người lệch PHẢI, ô chữ bên TRÁI.
> Gói free (đo 2026-10-01): 3 video/tháng · ≤3 phút · 720p · **watermark lớn** · Avatar IV ≈ 1 phút/tháng ⇒ **free chỉ để THỬ, không đăng được**. Đăng thật = gói Creator ~$29/tháng → user quyết.

## File đã chuẩn bị (thư mục này)
| file | dùng ở bước | nội dung |
|---|---|---|
| `host_IMG_FLOW.txt` | ① gen ảnh | 3 prompt người dẫn phòng sáng. Dòng 1 = ảnh MỐC mặt; dòng 2–3 gen kèm ảnh 1 làm reference |
| `demo_01_jikoshoukai.mp3` | ④ | 11,3s · 「私は、ずっと、そうでした。デパートの売り場で三十四年…」 |
| `demo_02_radio.mp3` | ④ | 11,3s · 「家事をしながら、ラジオのように…」 |

## Các bước
1. **Gen ảnh người dẫn** trong Flow/Nano Banana bằng `host_IMG_FLOW.txt`. Chọn 1 ảnh: mặt nhìn thẳng, rõ, miệng ngậm, micro không che miệng. Gửi ảnh cho Claude → cắt ✦ → nhận lại `host_upload.png`.
2. **Đăng ký / đăng nhập** heygen.com (Gmail bất kỳ; không dính kênh YouTube nào).
3. **Tạo Photo Avatar:** menu **Avatars** → tạo avatar mới từ ảnh → tải `host_upload.png` lên.
4. **Làm video:** trang Home → **Photo to Video** (hoặc **Create video → Single Scene**) → chọn avatar vừa tạo → ở ô kịch bản chọn **Upload audio** (KHÔNG gõ chữ, không chọn giọng HeyGen) → tải `demo_01_jikoshoukai.mp3`.
5. **Engine:** chọn **Avatar IV** (nhép đẹp nhất; free có ~1 phút/tháng — 2 file demo tổng 23s là vừa).
   **Custom motion** (nếu có ô): `gentle small nods, soft natural blinking, calm hands resting on the desk, no big gestures`.
6. **Khổ:** **Landscape 16:9** → **Generate**. Lặp lại bước 4–6 với `demo_02_radio.mp3`.
7. **Tải về** 2 file mp4 → bỏ vào `~/Downloads` → báo Claude. Claude ghép vào đúng 2 chỗ trong video + ô chữ trái + chip chương như mẫu, để mày duyệt.

## Kiểm khi nhận về (Claude làm)
- thời lượng mp4 = thời lượng mp3 (HeyGen không được tự kéo giãn) · miệng khớp tiếng ở 4 mốc · watermark HeyGen ở đâu · ✦ còn không.
