# GEN LẠI CLIP AI — vòng soi · loại · sửa prompt

> **Nguồn sự thật DUY NHẤT** cho vòng *gen clip → soi → loại → sửa prompt → gen lại* (Veo/Flow t2v · i2v · ảnh→Animate).
> Chốt 2026-09-15, đúc từ nenkin video 25: **3 vòng gen lại, 9 → 5 → 3 clip**. Rule lo **NHẬN/LOẠI + CÁCH SỬA PROMPT**.
> Viết prompt từ đầu: `media-library.md` §2.10 + CLAUDE.md từng kênh. Ngôn ngữ máy quay: `camera-language.md`. Render: `render-background.md`.

## 0. NGUYÊN TẮC GỐC — sửa ĐÚNG TẦNG
Mỗi lần soi ra lỗi, hỏi: **«Lỗi của MỘT CLIP hay của MỘT LỚP?»** Cả 3 vòng video 25 đều là một lớp, và lớp đó nằm trong **TOOL sinh prompt**. Sửa prompt tay là sửa triệu chứng.

## 1. ⭐ THANG NHẬN / LOẠI — chốt bằng CÂU HỎI

| | ❌ LOẠI, gen lại | ✅ NHẬN, ghi sổ |
|---|---|---|
| **Số** | số to đọc ra thành **mệnh đề của bài** (`75` = 75歳) · **số tiền SAI** (`44.900` thay `844,900`) | vạch trục · vạch thước · bàn phím máy tính · số trang li ti |
| **Chữ** | chữ Nhật giả **cỡ đọc được** chiếm mảng lớn (biển hiệu giữa khung · nền hoá nguyên trang báo) | mảnh báo ở rìa · texture li ti · nhãn mờ |
| **Người/vật** | **bàn tay người thật** thò vào khung hoạt hoạ · vật đổi trạng thái sai (kính biến mất, phong bì nhân đôi) | chi tiết thừa đúng ngôn ngữ hình |

🔴 ① **Ghi sổ mọi thứ CỐ Ý NHẬN** kèm lý do (không thì lượt sau gen lại clip đã duyệt). ② **Một thang cho cả lô** — cùng mức thì cùng quyết định.

## 2. 🔴🔴 CẤM cái gì thì CẤM Ở ĐẦU PROMPT

| lượt | guard SỐ | guard CHỮ | guard NỀN | kết quả |
|---|---|---|---|---|
| vòng 1 | 55% | 43% | 30% | 4/6 clip "cấm số" có số |
| vòng 2 | **2%** | 43% | 30% | số sạch · 2 clip nền hoá tường báo chữ giả |
| vòng 3 | **2%** | **2%** | **2%** | ✅ 3/3 sạch |

Cùng định luật với thumbnail (`ab-3title-3thumb.md` §3.1 — khối TEXT trong 15% đầu): ở đó XIN chữ, ở đây CẤM chữ. ⇒ **Gom mọi luật CẤM vào MỘT khối ngay sau câu khai mở**, để câu nhắc ngắn ở chỗ cũ.
```python
pos = p.find("NO FIGURES") if "NO FIGURES" in p else p.find("EXACTLY ONE FIGURE")
assert pos * 100 // len(p) <= 15,  "guard nam qua sau trong prompt"
```

## 3. 🔴 VẬT MỜI GỌI THẮNG CÂU CẤM — phải BỎ VẬT
Nhiệt kế → `75` + vạch · lưới lịch → `1人`, `Mon Tue` · cột xu → `7`, `2` · thước → `50 31 50` · **biểu đồ ĐƯỜNG** → trục có vạch số.
⇒ Tách kho vật: `NUMFREE` (hình khối thuần — cột, bánh tròn, mũi tên) và `SCALED` (mang thang số). Cảnh không có số thật chỉ lấy `NUMFREE`. Vật mà chữ/số là lý do tồn tại (lịch, nhiệt kế) → **bỏ khỏi cả hai kho**.

## 4. 🔢 SỐ TRÊN HÌNH — ba đòn bẩy theo thứ tự

| # | đòn bẩy | chữa được | ca thật |
|---|---|---|---|
| ① | `crisp` | ~không gì (crisp ≠ correct) | `130 000` méo |
| ② | đánh vần `1 3 0 , 0 0 0` + "đúng một lần" | sai thứ tự, bản sao thứ hai | vẫn `13,000` |
| ③ | ⭐ **ĐẾM CHỮ SỐ** `Count them: 6 digits in total, do not drop a digit` | rớt/thừa ký tự | ✅ `130,000` |

② nói THỨ TỰ, không nói ĐỘ DÀI; ③ thêm ràng buộc model tự kiểm được. Hai clause bắt buộc kèm: `dấu phẩy, không phải dấu chấm` · `đứng tách hẳn mọi nhân vật và đạo cụ, không tay/băng dính/kéo/mép rách nào che`.
⛔ Hết ba mà vẫn sai → **DỪNG**: ① bỏ số khỏi clip, để Remotion vẽ bằng **font** (an toàn nhất) ② nhận bản tốt nhất nếu số đúng chỉ lỗi vụn ③ đổi thiết kế cảnh.

## 5. ⚠️ CẢNH MỎNG DỄ BỊA CHỮ NHẤT
Cảnh ≤3 phần tử mà khối bố cục đòi "lấp đầy khung" ⇒ model lấp bằng giấy báo có chữ. Nói rõ lấp bằng GÌ: *«lấp bằng hình cắt người/vật và mảng giấy hình học — không bao giờ bằng chữ»*. Đếm phần tử trước khi gen; ≤3 = soi kỹ hơn.

## 6. 🔴 GATE ĐỌC TRÚNG VĂN CỦA CHÍNH MÌNH
Gate quét cả prompt sẽ bắt chính câu CẤM (`no tally marks…`). Quét **đúng khối nội dung**:
```python
sc = p.split("SCENE (...):")[1].split("<mốc kết>")[0]
```
Luật chung: gate chưa từng báo đỏ, hoặc báo đỏ hàng loạt ngay lần đầu → **nghi gate trước dữ liệu**.

## 7. 📋 QUY TRÌNH MỘT VÒNG
```
1. SOI   — mỗi clip ≥4 mốc (0,3 / 2,6 / 5,2 / 7,6s), strip 1:1. ⛔ Sheet thu nhỏ cho qua số méo/chữ giả.
           Số phải đúng ở CẢ 4 frame.
2. PHÂN  — theo thang §1; ghi lý do LOẠI và CỐ Ý NHẬN vào TENFILE của lô.
3. HỎI   — «một clip hay một lớp?» → sửa ở TOOL sinh prompt.
4. GATE  — guard ≤15% · khối cấm không có câu xin ngược · vật SCALED không có trong cảnh cấm số · không framing thiếu thân.
5. XUẤT  — file riêng `vox<NN>_REDO<k>.txt` + `_TENFILE` ghi vì sao từng clip bị loại.
6. NHẬN  — ingest, soi 1:1 cả 4 góc tìm ✦ (`media-library.md` §2.10 ⑤), từng lô.
```
⭐ **Prompt trượt 2 lần liên tiếp ⇒ lỗi ở PROMPT**, không ở lượt gen. Đổi token chủ thể giữ nghĩa, hoặc đổi thiết kế cảnh.

## 8. LIÊN QUAN
- Prompt từ đầu · ✦ · macro: `media-library.md` §2.10–2.11
- Máy quay · diễn xuất · gate `check_cammove.py`/`check_realism.py`: `camera-language.md`
- Memory: `feedback_so_tren_hinh_phai_do_font_ve` · `feedback_prompt_khoi_chung_huy_mo_ta` · `feedback_ai_video_hong_thao_tac_tay`
- Render sau khi đủ clip: `render-background.md` §1.5
