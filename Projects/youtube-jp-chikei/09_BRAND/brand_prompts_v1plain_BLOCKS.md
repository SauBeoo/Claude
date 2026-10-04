# Prompt ảnh kênh 地形と地名の日本史 — bản người đọc

> Viết 2026-09-16. File dùng để BƠM là `brand_prompts_FLOW.txt` (có chữ) và
> `brand_prompts_PLATE.txt` (không chữ) — mỗi prompt **1 dòng**. Map tên file: `..._TENFILE.txt`.
> Luật: `ab-3title-3thumb.md` §3 mục 7–8 + §3.1 · `media-library.md` §2.10.

## 0. ⚠️ ĐỌC TRƯỚC — hai ràng buộc quyết định cách viết

**① Generator luôn xuất 16:9, không có 1:1.** Avatar YouTube là **hình VUÔNG** (hiển thị bé nhất
ở **48px**). Nên mọi prompt avatar dưới đây đều bắt **bố cục tròn, đối xứng, nằm gọn giữa khung**
để crop vuông không mất gì. Crop xong mất ~44% bề ngang — đó là chuyện bình thường, không phải hỏng.

**② Gen ở cỡ LỚN nếu tool cho chọn.** Banner cần **2560×1440**:
- lô **2752×1536** → thu nhỏ xuống 2560×1440 = **nét**;
- lô **1376×768** → phải phóng **1,86×** = mềm nét, chữ nhỏ sẽ nhoè.
⇒ Ưu tiên lô 2K cho banner. Avatar thì lô nào cũng đủ (chỉ cần ≥800px sau crop).

## 1. 🔴 KHUYẾN NGHỊ: BANNER ĐI ĐƯỜNG **PLATE** (nền không chữ)

Luật chung của workspace là **prompt phải bake chữ** (`ab-3title-3thumb.md` §3 mục 8) — vì với
thumbnail, user cần thấy bộ mặt thật lúc gen. Ở **banner** thì tao khuyên ngược lại, và đây là lý
do kỹ thuật chứ không phải ngại việc:

| | banner | avatar |
|---|---|---|
| chữ phải gen | `地形と地名の日本史` = **9 ký kanji rậm** + 1 dòng phụ 13 ký | `地形` = **2 ký** |
| rủi ro nát kanji | **rất cao** — vượt xa mọi ca đã chạy được trong workspace | thấp |
| chữ hiển thị cỡ nào | **to nhất trang kênh**, một nét sai là thấy ngay | bé (48–176px) |
| sửa chữ sau này | phải gen lại cả ảnh | — |

⇒ **Banner: lấy prompt `B*` trong PLATE.txt** (nền sạch, chừa dải giữa trống) rồi để tao đóng chữ
bằng Noto Sans JP: `python tools/make_brand.py --bg 09_BRAND/<file>.png`.
⇒ **Avatar: lấy prompt `A*` trong FLOW.txt** (bake sẵn 2 chữ) — 2 ký tự thì gen được, và vẫn có
plate `A*p` dự phòng nếu nét xấu.

## 2. BỐ CỤC BANNER — chỗ nào được có gì

```
◄────────────────── 2560 px, thấy trên TV ──────────────────►
         ◄────── 1546×423 VÙNG AN TOÀN (mọi thiết bị) ──────►
┌────────────────────────────────────────────────────────────┐
│  rìa: bị cắt trên mobile — KHÔNG để chi tiết quan trọng     │
│      ┌──────────────────────────────────────────┐          │
│      │   DẢI NÀY PHẢI SẠCH — chỗ đóng chữ       │          │
│      └──────────────────────────────────────────┘          │
│  nửa dưới: đường nét địa hình / sông chảy ngang             │
└────────────────────────────────────────────────────────────┘
```
Câu bắt buộc trong mọi prompt banner: *"clean uncluttered horizontal band across the middle third,
no objects and no text there"*.

## 3. BA HƯỚNG HÌNH (mỗi hướng = 1 giả thuyết, giống luật A/B)

| mã | hướng | bán cảm giác gì |
|---|---|---|
| **B1** | **Bàn làm việc của người đọc bản đồ** — bản đồ địa hình cũ trải trên gỗ, com-pa, thước tỉ lệ, ánh sáng cửa sổ | "có người thật ngồi tra cứu" — gần `ブラタモリ` nhất |
| **B2** | **Nhìn từ trên xuống một thung lũng có sông uốn khúc**, phong cách bản đồ vẽ tay + đường đồng mức | "đây là kênh về HÌNH DẠNG ĐẤT" — thuần bản sắc nhất |
| **B3** | **Hai lớp thời gian**: nửa trái phố xưa ố vàng, nửa phải phố nay, một dòng sông xanh nối hai bên | "60 năm đổi mặt" — đúng trục T3 土地の履歴 |

| mã | avatar |
|---|---|
| **A1** | Đĩa tròn navy, bên trong là **lát cắt địa hình** (đường sườn đồi) + chữ `地形` |
| **A2** | Đĩa tròn kem, **đường đồng mức** đồng tâm + một dòng sông xanh cắt ngang + chữ `地形` |

## 4. SAU KHI GEN — 3 bước, đừng bỏ bước nào

1. 🔴 **Xoá watermark ✦** (`media-library.md` §2.10 ⑤b — *"lúc nào cũng phải xoá"*). Lô
   **2752×1536 có HAI dấu**; lô 1376×768 có một. Soi **cả 4 góc ở cỡ 1:1**, sheet thu nhỏ cho qua ✦.
2. **Crop**: avatar → vuông giữa khung; banner → về đúng 2560×1440.
3. **Đóng chữ + kiểm**: `python tools/make_brand.py --bg <file>` rồi soi `avatar_prev48.png`
   (chữ còn đọc được không) và `banner_safearea.png` (chữ có lọt vùng an toàn không).
