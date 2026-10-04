# Media Library — asset ảnh/clip + ảnh AI (RULE TOÀN HỆ THỐNG)

> **Nguồn sự thật DUY NHẤT** về kho media chung và chính sách visual. Kênh đang chạy: **nenkin · showa**.

## 1. KHO CHUNG

```
E:\Claude\Projects\_media_library\
├── clips\  photos\   # asset STOCK
├── INDEX.json        # kind, source, source_id, url, license, queries[], tags[], used_in[], w/h/duration
└── media_lib.py      # module + CLI (search / ingest-* / mark-used / stats)
```
- Tool mới: `sys.path.insert(0, r"E:\Claude\Projects\_media_library")` rồi dùng `search()` / `link_out()` / `add_file()` / `mark_used()` — đừng tự viết cơ chế riêng.
- Tra tay: `python media_lib.py search "<query>" --kind clip --unused-for <project>`.

## 2. ⛔ KHÔNG TÁI DÙNG ASSET (user chốt 2026-07-29)
> *"làm video nào tải ảnh và video của video đó thôi."*

1. **Mỗi video tải bộ ảnh/clip MỚI của riêng nó.** Nhánh "lấy TỪ KHO" đã tắt ở mọi tool fetch.
2. Kho + INDEX đổi vai thành **SỔ ĐEN + hồ sơ license**: file mới vẫn nhập kho để ghi `used_in` + license; fetch tool đối chiếu ứng viên mạng (Pexels id / Commons title / url) với asset đã lên sóng, trùng thì bỏ qua. **Sổ đen là điều kiện sống của chính sách** — thiếu nó cùng query trả lại đúng asset cũ.
3. **Asset đã bị loại khi duyệt mắt không được quay lại:** mọi cơ chế chọn asset tự động phải trừ danh sách đã loại (`rejected/`) trước khi chọn. Loại = tạo link vào `rejected/` **và** xoá tên ở pool (hardlink — chỉ `mv` thì lần fetch sau tạo lại). Duyệt mắt soi bộ **ĐƯỢC CHỌN cuối cùng**, không phải bộ mới tải.
4. **Trong cùng video cũng không trùng ảnh** (callback kể chuyện cũng phải đổi ảnh khác).
5. Muốn bật lại tái dùng → hỏi user.

## 2.0 ⭐ HÌNH ĐẦU TIÊN PHẢI LÀ CHỦ ĐỀ (chốt 2026-07-30)
**nenkin:** asset entry 0 phải hiện đúng **CHỦ THỂ của bài** (vật/giấy tờ đang nói), không ảnh mood/bối cảnh/ẩn dụ. Thumbnail → frame đầu phải liền mạch (health đo được 41–69% rớt trước giây 60). Câu mở là triệu chứng/ẩn dụ → vẫn lấy ảnh chủ thể, đẩy ảnh minh hoạ xuống entry 1–2. Kiểm: che chữ ô đầu contact sheet, vẫn nhận ra video về gì. Chủ thể frame đầu cùng loại với chủ thể thumbnail.

🟡 **showa (đo 2026-09-08, `youtube-jp-showa/CHANNEL_BENCHMARK_stills_2026-09-08.md` §4):** 2/3 bản thắng KHÔNG mở bằng chủ thể bài; thứ cả 3 làm là **hình khớp CÂU ĐANG ĐỌC**. ⇒ entry 0 khớp **câu mở**; câu mở dựng bối cảnh thời đại thì ảnh bối cảnh là ĐÚNG. (Ưu tiên: memory `feedback_showa_coldopen_clip_that_giay_0` + `youtube-jp-showa/CLAUDE.md`.)
⚠️ Không đổi ở kênh nào: **mismatch với LỜI HỨA của thumbnail** (hứa con số mà 30s đầu kể tuỳ bút → rớt 62%).

### 2.0b ⑦ Thẻ CHỮ không tính là "chủ thể"
Lớp sân khấu dễ lách entry 0 bằng một thẻ chữ số to — **vi phạm**, vì che chữ đi không còn gì. Entry 0 phải có **ẢNH của vật** (nenkin 11: ảnh tờ 申告書 + số hero đặt bằng `pins`). ⚖️ Giấy tờ trong ảnh phải **chung chung, ô trống, không chữ** — cấm dựng bản sao giấy chính thức; giấy THẬT chỉ ở 原典ショット (screenshot, không phải WebFetch).

## 2.10 🖼️ ẢNH AI — prompt, cắt ô, watermark

### ① `--ar` bị bỏ qua — tool luôn xuất **1376×768 (16:9)** (đo 3 lô). Đừng thiết kế theo `--ar`.

### ② Layout **COVER-CROP**, lệch tỉ lệ là cắt mép
| slot (`make_stage`) | khoá | khung | tỉ lệ | mất khi cắt từ 1376×768 |
|---|---|---|---|---|
| ảnh lớn trong bảng | `img` | 940×588 | 1.60 | 11% |
| ảnh NỀN bảng | `bgimg` | 1376×846 | 1.626 | 9% |
| icon/avatar | `icon` | 132×132 | 1.00 | 44% |
Screenshot 原典 phải chụp **cột hẹp + chữ to** (JS `max-width` 620–780px, `font-size` 30–34px) rồi crop đúng tỉ lệ slot.

### ③ ⭐ Mọi thứ quan trọng trong **85% BÊN TRÁI**, chừa 15% phải trống
Cả crop tỉ lệ lẫn ✦ đều ăn ở bên phải ⇒ chủ thể lệch trái thì hai cú cắt vô hại.

### ④ Ảnh NỀN phải NHẠT — dùng `bgimg`, KHÔNG `fill`
- `fill` (hộp (1010,536)–(1400,852)) **đè chữ** của `check`/`steps`. Chỉ an toàn ở `big`/`art`.
- Nền dưới `bg_veil 0.78` + chữ navy ⇒ prompt ghi `LOW CONTRAST and airy`, `no dark masses, no strong shadows`, chừa trống nửa trên (đo: nền đậm 56–57% → 2–12%).

### ⑤ Watermark ✦: CẮT, đừng patch — đo lại TỪNG LÔ
- Patch texture để lại vệt chữ nhật trên nền có vân. Cắt mép phải thì sạch tuyệt đối, tỉ lệ vẫn đúng vì slot nào cũng cắt ≥9% phải.
- **Toạ độ ✦ khác nhau giữa các lô và giữa các ảnh cùng lô** (nền tối/xám → ✦ to hơn, có tia dài). Mốc cắt lấy theo **ảnh xấu nhất của lô**, soi cả ảnh nền sáng lẫn tối.
- 🔴 **Định vị ✦ bằng máy không tin được** (template học từ lô khác · residual-max rơi vào cánh sao/mép chữ · local contrast bị nét chữ áp đảo — trượt 4/4 ở ảnh có chữ, 7/8 ở lô nền kem). ⇒ **Chốt vị trí bằng MẮT** trên 5–8 mẫu crop góc dưới-phải, ghi hằng số theo **từng lô kích thước**: `1376×768 → (0,928W · 0,878H)` · `2752×1536 → (0,958W · 0,926H)` và có thể thêm `(0,930W · 0,890H)` (số dấu không cố định — quét template toàn ảnh để chốt số lượng).
- **Số đo và exit code không chứng minh ✦ đã sạch** (residual cao sau cắt có thể là vân thật; log "đã vá N/N" là lời khai).
- Tool cắt: `Projects/youtube-jp-co-dai/tools/strip_wm_crop.py` (backup `_wm_orig/`, `--restore`, không cắt 2 lần) · nenkin: `youtube-jp-nenkin/tools/ingest_art_12.py`, `tools/strip_wm_crop29.py`.

### ⑤b 🔴🔴 LUẬT CỨNG — MỌI ẢNH AI, KHÔNG NGOẠI LỆ: XOÁ ✦ TRƯỚC KHI GIAO (user chốt 2026-08-14)
Áp cho slide · **thumbnail** · ảnh minh hoạ · ảnh nền thẻ. Còn ✦ = **chưa xong**: không vào SLIDES, không gói upload, không báo "dùng được".
1. **Quét CẢ LÔ trong folder nguồn** (`~/Downloads`), không chỉ ảnh user dán vào chat.
2. **Chọn nhánh theo việc CHỮ có chạy sát mép không** (không theo "có bake chữ hay không"):
   | | chữ/nội dung KHÔNG sát mép phải | chữ chạy tới ~0,97W |
   |---|---|---|
   | cách | **CẮT** phải ~0,905–0,943W + trim 16:9 **chia đôi trên/dưới** + resize | **VÁ** |
   | tool | `strip_wm_crop.py` / `strip_wm_crop29.py` | `youtube-jp-shokutaku/tools/strip_wm_thumb.py` |
   Trim hết ở đáy có thể cắt viền badge — đo lề trước. Nghiệm thu cắt: template ✦ lấy từ chính ảnh gốc, `matchTemplate` trên bản cắt, peak phải tụt về nhiễu (0,997 → 0,358).
3. **Cách VÁ theo nền:**
   - Nền gradient mịn **theo chiều dọc** (tường, bàn phẳng) → **trung vị TỪNG HÀNG** + loại pixel nét chữ khỏi mặt nạ + nhiễu ±1,2; tâm sau vá khớp nền ±2 mức. ❌ copy khối bên cạnh (lệch tông) · ❌ tách alpha (gỡ ~70%).
   - Nền gradient **chéo** (vệt nắng) → `cv2.inpaint` (NS) + **ghép lại vân tần số cao** từ vùng toàn-nền bên cạnh (`src − GaussianBlur(src,6)`), blend theo `distanceTransform`, nhiễu ±0,8. Tool: `youtube-jp-health/tools/strip_wm_grain.py`. Bán kính mask đúng cỡ sao; offset lấy vân không được trùm sao khác. Un-blend thì kernel median phải lớn hơn đường kính sao.
   - **Xem residual CÓ DẤU trước** (`ảnh − GaussianBlur(ảnh,2.5)`): ✦ có thể là **nét TỐI mảnh**. Khi đó và khi ✦ đè lên **biên chất liệu** → **phép ĐÓNG/MỞ** (`CLOSE k=3` cho nét tối, `OPEN k=5` cho nét sáng; kernel nhỏ hơn bề dày vật thật gần đó). Tool: `youtube-jp-co-dai/tools/strip_wm_star.py`. ✦ trên biên chất liệu thì mọi phép nội suy đều phá biên → ưu tiên CẮT nếu được.
4. **✦ đè lên nét chữ → LOẠI ảnh, gen lại.** Prompt chừa góc dưới-phải thành mặt phẳng trống chỉ làm ✦ rơi vào chỗ vá được, không đẩy ✦ đi.
5. **Nghiệm thu = soi 1:1, cả 4 góc.** Sheet thu nhỏ cho qua ✦.
6. **Ảnh VECTOR PHẲNG thì CẮT, đừng vá** (snap-màu-palette hỏng theo hai hướng: siết thì sót, nới thì ăn vào hình — **dấu hiệu SAI ĐƯỜNG**, không phải thiếu tinh chỉnh). Cắt 0,905W ⇒ sạch 95/95 ngay vòng đầu.
7. 🔴 **Tool cắt hàng loạt phải TỰ CHỪA ảnh 原典** (screenshot vốn không có ✦, cắt là mất chữ + khung khoanh đỏ = phá bằng chứng YMYL). Nhận diện bằng cụm mực nhỏ:
   ```python
   lab, n = ndimage.label(gray < 140); small = ((sizes >= 6) & (sizes <= 400)).sum()
   if small >= 600: bỏ qua   # 原典 1.271–2.056 · vector ≤176
   ```
   ⛔ Đừng liệt kê chỉ số ô bằng tay (trôi khi đổi plan). Template-match lấy mẫu từ vùng PHẲNG trả peak 1,000 ở cả ảnh không có ✦ → quyết định cuối vẫn là sheet crop 1:1 + mắt.
8. **Pillarbox trước khi cắt ✦** (clip ⋮ Animate/Flow từ ảnh không 16:9 bị đệm viền đen): đo mép 4 cạnh = số cột/hàng liên tiếp có max-kênh ≤22 tại ≥3 mốc thời gian, **soi mắt** (tường tối cũng ≤22) → `crop=iw-L-R:ih-6:L:3` → rồi mới 0,905W. Mẫu: `youtube-jp-showa/tools/assemble_clips_17r.py` (`BARS` + gate `edge_bars`).
9. Xuất bản đã vá ra **file riêng**, không ghi đè; **không dùng cùng một tên output cho hai nguồn**; file trung gian đặt tên **ngoài pattern tool quét** (`_wm_fixed_T3.png`, không `thumb_T3_*_clean.png` — `upload_pack.py` sẽ gói nhầm).
10. **Mỗi lô gen quét lại từ đầu** — lô thumbnail và lô slide cùng video có thể khác nhau.

### ⑥ Prompt điều khiển được VỊ TRÍ, KHÔNG điều khiển TỈ LỆ
Xin `filling the LEFT two-thirds` + `from the knees up` → người toàn thân nhỏ đặt đúng bên trái. Ép cỡ bằng **quan hệ với MÉP KHUNG**: `CROPPED BY THE BOTTOM EDGE at the knees, head almost touching the top edge`. Luật chung của mọi prompt ảnh AI.

### ⑧ Pad ảnh AI lên canvas đơn sắc → TRIM viền + dải trắng
Generator để lại **viền 1–3px** và **đường kẻ ngang + dải trắng đáy** (thi hành câu "white band along the bottom") ⇒ thành khung khi ghép lên canvas.
1. Crop cứng 5px mỗi mép (⛔ auto-detect viền ăn nhầm nội dung chạm mép).
2. Hàng nội dung thấp nhất cách đáy >20px → có dải trắng; **đường kẻ = khối nội dung MỎNG ≤6px mà ngay trên là trắng** → cắt (nhận bằng độ dày, không bằng độ phủ ngang).
3. Gate: **bậc nhảy** độ sáng trong 5px đầu ở 3 mép trái/phải/trên `>12` = còn viền (đo bậc, không đo độ tối; bỏ mép đáy). Mẫu: `youtube-jp-shokutaku/tools/ingest_slides_18.py::trim_border`.
Không sửa được từ prompt — cứ xin dải trắng, cắt ở tầng ingest.

### ⑨ 🎭 Cast cắt nền (nhân vật 2 mép sân khấu)
1. Gen nền **MAGENTA `#FF00FF`**, không nền trắng (cụ già tóc bạc + áo kem).
2. Vệt tím: **CO MASK vào ~3px** (`cv2.erode`) nhờ viền trắng sticker dày; ⛔ đừng "sửa màu" pixel viền (suy màu từ pixel nhiễm không bao giờ sạch). Sau vá 0–24px tím (từ ~1.400).
3. **Giữ BLOB LỚN NHẤT** (`connectedComponentsWithStats`) — ✦ trắng nhạt trên magenta không bị ngưỡng màu loại.
4. Ghép tên file: **khoá GIỚI TÍNH trước**, rồi mới từ khoá hành động (từ khoá phải ĐẶC TRƯNG).
5. Nghiệm thu: đo vệt tím bằng máy (bán trong suốt `R−G>40 và B−G>40`) + dán lên **đúng màu nền khung**; cùng một người xuyên mọi tư thế.
6. Có N tư thế thì phải có `POSE_MAP` đổi theo đoạn bài — một cặp cố định = như có 1 ảnh.
7. **Cân theo CỠ ĐẦU**: scale đầu = `HEAD_PX`, cắt bớt dưới cho cùng chiều cao, dán đáy cùng mốc. Đo đầu bằng **bề rộng trung vị ở dải y 6–14% từ đỉnh** (tay giơ ngang đầu phá mốc vai), cao ≈ rộng/0,72. Dán theo mép TRONG, cách thẻ ~8px.
8. Chip nhãn đoạn + dấu nhấn **vẽ bằng FONT** (`make_stage.F()/fit()`), đừng nhờ AI bake.
9. 🔴 **Hai góc phải khung đã có chủ**: trên-phải = badge nhận diện kênh (dán sau khi ghép slide), dưới-phải = timestamp YouTube. Đừng vẽ gì vào đó.
Tool mẫu: `youtube-jp-shokutaku/tools/cutout_cast.py`.

## 2.11 ⭐ ẢNH CHO THẺ ANNOTATE PHẢI LÀ MACRO
Style lock giữ tông cũng khoá luôn framing (bối cảnh phòng + cửa sổ ⇒ không ảnh nào macro). Dùng hai biến thể: `STYLE` (có bối cảnh) và `STYLE_MACRO` (`subject FILLS THE FRAME, tight crop, plain dark background, NO room, NO window, NO furniture`) cho mọi ảnh bị annotate đè. Mẫu: `youtube-jp-co-dai/tools/gen_slides19.py`.

## 3. ẢNH hay CLIP theo TỪNG ENTRY
| kênh | lớp hình |
|---|---|
| **nenkin** | ⛔ **bỏ clip AI t2v/i2v từ v27**, giữ ảnh AI tĩnh + thẻ chữ/sơ đồ vẽ bằng font (`audience-45plus.md` §2.0-quater-b). |
| **showa** | theo `youtube-jp-showa/CLAUDE.md` (khuôn v08: ảnh THẬT cận đúng vật được đọc, đúng thập niên; AI chỉ lấp; clip AI theo `camera-language.md` §0.5). |

Luật chung: vật/thao tác cụ thể → ẢNH; clip lệch nội dung → hạ về ảnh; **duyệt contact sheet bằng mắt trước render**. Stock-clip là `"video": true`, footage tự quay là `"handmade": true` — đừng gắn lẫn.

## 4. LICENSE
Chỉ nhận nguồn free-thương-mại (Pexels / Openverse cc0,by / Wikimedia CC0/BY / tư liệu CC BY như kho peloquin 1971). License + url gốc lưu trong INDEX; CC BY thì ghi credit vào ATTRIBUTIONS.md của video.
