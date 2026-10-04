# youtube-jp-retrofuture — 昭和100年 レトロフューチャー

**Kênh YouTube JP, clip AI 100%, KHÔNG lời kể, KHÔNG phụ đề.** Lập concept 2026-09-21.

> ⭐⭐ **CÁCH QUAY = CÔNG THỨC v4 「REALISM」 (chốt 2026-09-22):** góc thứ ba · máy KHOÁ 2/3 + TRÔI một bước 1/3 · **ảnh Nano Banana → Animate**
> (không t2v thuần) · nắng vàng một nguồn · người cử động chậm · prompt ngắn. Khối chung `Projects/_media_library/realism_blocks.py`,
> thế giới riêng `tools/blocks_s100.py::WORLD_SHORT`, tool `tools/gen_ep01_v4.py`, đo `_media_library/check_realism.py`.
> Bằng chứng + số: `04_VIDEOGEN_STYLE_S100.md` banner đầu file và §12. ⛔ POV/máy cầm tay của v3 hết hiệu lực.

> 🔴 **Kênh RIÊNG, không dính `youtube-jp-showa`.** Khác tệp, khác thứ bán, khác pipeline, khác gate.
> Bảng so sánh đầy đủ ở `00_WORLD_BIBLE.md` đầu file. Dùng chung **tool**, không dùng chung **nội dung**.

## Một câu
Nếu thời Showa chưa bao giờ kết thúc — bây giờ là **昭和100年**, và trong nhà có một con robot.

## Cấu trúc repo

| File | Vai |
|---|---|
| `00_WORLD_BIBLE.md` | **LUẬT** — 6 quy tắc thế giới · spec robot ロボ太 · format · telop · âm thanh · compliance |
| `01_EPISODE_IDEAS.md` | 12 tập đầu + shot list demo tập 1 + quy trình nghiệm thu |
| `04_VIDEOGEN_STYLE_S100.md` | **Bộ prompt t2v** — `AVOID_S100` · `ROBOT_LOCK` · `STYLE_S100` · ⭐ `WORLD_KIT` (kho nhà cửa/xe cộ/đồ đạc viễn tưởng) · gate |
| `videogen_ep01_DEMO_FLOW.txt` | 8 prompt tập 1, **1 dòng/prompt**, bơm thẳng extension Flow |
| `videogen_ep01_DEMO_TENFILE.txt` | thứ tự dòng FLOW ↔ tên file clip |
| `06_VIDEO/` | thư mục dựng từng tập |
| `tools/` | `blocks_s100.py` (thế giới) · **`gen_ep01_v4.py`** (34 cảnh still+motion, công thức v4) · `gen_test_realism.py` (6 cảnh thử) · `check_realism.py` (wrapper → `_media_library`) · `gen_ep01_ichinichi.py` (bản Ⓑ POV — kịch bản còn dùng, cách quay hết hiệu lực) |

## Ba thứ quyết định kênh này sống hay chết

1. ⭐ **Thế giới phải NHÌN RA trong 3 giây.** Tiền đề là một câu; model chỉ dựng được từ **danh từ cụ thể** →
   mọi prompt phải kê ≥1 kiến trúc + 1 phương tiện + 1 đồ vật từ `WORLD_KIT`.
2. ⭐ **Không ai được phản ứng với robot.** Đó là thứ biến "phim về một con robot" thành "một thế giới có robot".
3. ⚠️ **Nhạc** — không lời thì nhạc là 50% sản phẩm, và đây là rủi ro **chưa giải**. Phải thử nghe
   trước khi cam kết kênh. City pop thật có bản quyền, không dùng được.

## Vì sao robot (lý do kỹ thuật, không phải thẩm mỹ)
t2v **không khoá được danh tính người**, nhưng **khoá được robot** — khối cứng, màu phẳng, 6 danh từ là ra đúng.
Và spec **bánh xe thay chân + bàn tay 3 ngón** bịt sẵn 3 bệnh nặng nhất của t2v (chân trượt, chi cao su, ngón thừa).

## Vault
`SecondBrain/10_Projects/youtube-jp-retrofuture/`

## Luật toàn hệ thống áp vào đây
`camera-language.md` (máy quay) · `ai-video-regen.md` (vòng gen lại) · `media-library.md` §2.10 (ảnh AI, watermark)
· `audience-45plus.md` §1 (thumbnail) · `ab-3title-3thumb.md` (A/B 3×3) · `youtube-compliance.md` §2.1 (⚠️ **bắt buộc
tick synthetic**) · `render-background.md` (render chạy nền) · `channel-browser.md` · `upload-schedule.md`

## Trạng thái
🟡 **Concept + CÁCH QUAY đã chốt (v4, 2026-09-22), CHƯA lập kênh.** Việc tiếp: gen 34 ảnh (`v4_STILL_FLOW.txt`) → chọn → Animate
(`v4_MOTION_FLOW.txt`) → `check_realism.py` → ghép → thử nhạc → rồi mới lập kênh.
