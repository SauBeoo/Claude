# BÀI THỬ "REALISM" — hướng dẫn bấm gì (2026-09-22)

> Mục tiêu: trả lời bằng SỐ + MẮT câu *"clip của mình ảo, clip 異世界さんぽ thật — vì sao?"*.
> Giả thuyết đã đo: không phải model. Là **máy đứng · ảnh-trước-rồi-hoá-động · ánh sáng một nguồn · prompt ngắn**.
> Sinh prompt: `python tools/gen_test_realism.py` · Đo kết quả: `python tools/check_realism.py <thư mục clip>`

## 0. Ba file, ba việc

| file | dùng ở đâu | bao nhiêu |
|---|---|---|
| `still_FLOW.txt` | Flow chế độ **Image** (hoặc Gemini app) → ảnh khung đầu | 6 dòng = 6 cảnh, gen mỗi cảnh 2 ảnh, chọn 1 |
| `motion_FLOW.txt` | Flow **Frames to Video**, kèm ảnh vừa chọn làm **khung đầu** | 6 dòng, dán TAY từng cái |
| `t2v_FLOW.txt` | Flow **Text to Video** thường — đối chứng "không có ảnh thì sao" | 6 dòng, bơm bằng extension như mọi lần |

Dòng thứ *i* của ba file là cùng một cảnh. `TENFILE.txt` ghi tên clip để đặt khi tải về.

## 1. Gen ẢNH khung đầu (≈10 phút)

1. Mở tab Flow đang dùng, vào một project. Ở ô nhập, đổi cấu hình từ **Video** sang **Image**
   (nút chọn kiểu đầu ra nằm cạnh ô prompt; panel extension có nút 🔍 KIỂM TRA TAB in ra cấu hình đang chọn).
2. Bơm `still_FLOW.txt` bằng extension như bơm ảnh showa (6 dòng, mỗi dòng 1 ảnh, để 2 lượt/dòng nếu Flow cho chọn số ảnh).
3. Với mỗi cảnh chọn **1 ảnh**, theo đúng 3 câu:
   - người trong ảnh có **đang ở nhịp 1** của hành động không (tay chạm shutter, xô đã kéo về sau, bát đang hạ)?
   - ánh sáng có **một nguồn + có bóng** không? Ảnh sáng đều như bưu thiếp → bỏ.
   - có **chữ bịa** không? Có → bỏ, đừng sửa.
4. Tải 6 ảnh về, đặt tên `R_<id>_frame.png` theo `TENFILE.txt` (vd `R_04_shutter_frame.png`).

## 2. Hoá động bằng Frames to Video (≈15 phút, dán tay)

Chế độ này extension **chưa bơm được** vì phải kèm ảnh. Làm tay 6 lần:

1. Trong ô prompt Flow, mở menu kiểu tạo (nút **+** hoặc menu cạnh ô nhập) → chọn **Frames to Video**
   (tên có thể hiện là *フレームから動画* / *Frames to video*). Nếu chỉ thấy *Ingredients to Video* thì dùng nó,
   thả đúng **1 ảnh** — tác dụng gần như nhau cho bài thử này.
2. Thả ảnh `R_<id>_frame.png` vào ô **khung đầu** (start frame). **Không** thả khung cuối.
3. Dán dòng tương ứng của `motion_FLOW.txt` → model **Veo 3.1** (chọn bản *Quality* nếu có) → **Start generation**.
4. Xong 6 cái, tải về, đặt tên `R_<id>_i2v.mp4`.

## 3. Đối chứng t2v (≈8 phút, extension)

Bơm `t2v_FLOW.txt` như mọi lần (Text to Video). Tải về, đặt tên `R_<id>_t2v.mp4`.
Đây là để tách hai biến: nếu i2v ≈ t2v thì "ảnh-trước" không quan trọng, cái ăn là máy đứng + ánh sáng.

## 4. Đo

Cho cả 12 clip vào một thư mục (vd `F:/Youtube/Dự_án_mới_32_xxx`) rồi:

```
python tools/check_realism.py "F:/Youtube/Dự_án_mới_32_xxx"
```

Nó in bảng 4 số so với mẫu, và dựng **sheet 4 frame cỡ thật** cho từng clip trong `_realism_check/`.

| số | mẫu 異世界さんぽ | lô mình hôm nay | mốc ĐẠT |
|---|---|---|---|
| ① MAD trong shot p50 | 1,5 | 9,4 | ≤ 3,0 |
| ② % khung gần đứng yên | 35,6% | 0,6% | ≥ 20% |
| ③ % shot máy DI | 32% | 95% | **0%** (bài thử khoá máy hết) |
| ④ sáng TB / % cháy trắng | 65 / 0,5% | 111 / 3,6% | 55–95 / ≤ 1% |

**Rồi soi sheet bằng mắt** — 4 câu, số không thay được: ① mặt có sượng/đổi người giữa clip không
② tay và vật to (shutter, xô nước, bát, khăn) có đúng vật lý không ③ có chữ bịa không
④ hành động có đủ 3 nhịp (dẫn → đỉnh → lắng) hay bung ngay giây đầu.

## 5. Đọc kết quả — quyết định gì

- **i2v thắng cả số lẫn mắt** → đổi pipeline tập 01 sang ảnh-trước (34 ảnh + 34 i2v), và mở bàn sửa công thức v3
  (POV/HANDHELD/PACE) — lúc đó mới sửa `04_VIDEOGEN_STYLE_S100.md`, không sửa trước.
- **i2v ≈ t2v, cả hai thắng lô cũ** → cái ăn là **máy đứng + ánh sáng + prompt ngắn**; giữ t2v cho rẻ.
- **Cả hai vẫn sượng như cũ** → lỗi ở tầng model/scene, không ở chỉ đạo máy; lúc đó mới bàn Kling/Hailuo.
  Nhưng theo `feedback_youtube_khong_dau_tu_them`: chưa có doanh thu thì không mua tool mới.

⚠️ Đừng đổi prompt giữa 6 cảnh khi gen lại — một biến một lần. Prompt trượt 2 lần = lỗi ở prompt (`ai-video-regen.md` §7).
