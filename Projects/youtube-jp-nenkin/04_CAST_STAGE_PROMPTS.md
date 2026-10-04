# Prompt bộ NHÂN VẬT SÂN KHẤU — 年金と老後のお金研究室 (viết 2026-08-08)

> Dùng cho tool `E:\Claude\Projects\_media_library\make_stage.py` (sân khấu cố định, xem
> `CHANNEL_BENCHMARK_okane-hokenshitsu_2026-08-08.md` §2.3). Hai nhân vật đứng hai mép
> khung, **xuất hiện trong MỌI video** → gen **một lần, xài mãi**.
> Demo đang chạy bằng いらすとや (`06_VIDEO/_stage_demo/stage_demo.mp4`); bộ này thay nó.

## 0. QUY TRÌNH — 4 bước, user chỉ làm bước 1

1. **User:** gen ảnh bằng web free, **nền TRẮNG PHẲNG** (không cần nền trong suốt).
2. **User:** bỏ file thô vào `E:\Claude\Projects\youtube-jp-nenkin\assets\cast\_raw\`.
3. **Claude:** cắt nền bằng `rembg` (đã có, 2.0.76) + cắt ô + chuẩn hoá cao 1280px + đặt
   đúng tên → `assets/cast/`.
4. **Claude:** render lại demo để duyệt mắt trước khi khoá bộ.

⚠️ **KHÔNG cần xuất PNG trong suốt.** Phần lớn web gen free không làm được alpha, và nền
trắng phẳng cho `rembg` cắt sạch hơn nền tự động của chúng.

## 1. ⭐ CÁCH NHANH — 2 PROMPT, mỗi nhân vật 1 TỜ 6 BIỂU CẢM

Gen **cả sheet trong một lần** thì 6 biểu cảm chắc chắn cùng một khuôn mặt / cùng bộ đồ —
gen rời 6 lần gần như luôn lệch. Tao cắt ô sau.

### 1.1 案内役 (bên TRÁI) — sheet 6 biểu cảm

```
A character expression sheet: 2 rows x 3 columns grid, 6 poses of THE SAME character,
identical face, hairstyle and outfit in every cell, evenly spaced, plain flat pure white
background, thin light-gray line separating cells.

Character: a calm Japanese man in his early 50s, short neat black hair with a little gray
at the temples, thin silver-rimmed glasses, gentle approachable face, slight smile.
Outfit: white dress shirt with a navy blue knitted vest, no tie, holding a plain clipboard
in one hand. Neutral, trustworthy, like a friendly city-hall counter advisor.

Framing in every cell: waist-up (bust shot), body turned three-quarters toward the RIGHT
side of the frame, head fully visible with clear margin above, cropped at the waist.

The 6 poses, left to right, top row then bottom row:
1. standing calmly, one open palm gesturing to his right, warm neutral expression
2. pointing with index finger to his right, attentive expression
3. both hands open in an explaining gesture, eyebrows slightly raised
4. one hand on his chest, soft reassuring smile, gentle nod
5. one index finger raised, serious careful expression, no anger
6. a small confident nod with a closed-mouth smile, hands relaxed

Art style: clean flat vector illustration, bold clear outlines, simple cel shading, limited
palette of navy blue, white, warm gray and a touch of amber, minimal detail, high contrast
so it stays readable when shrunk very small. Modern Japanese explainer-video look.
```

### 1.2 聞き手 (bên PHẢI) — sheet 6 biểu cảm

```
A character expression sheet: 2 rows x 3 columns grid, 6 poses of THE SAME character,
identical face, hairstyle and outfit in every cell, evenly spaced, plain flat pure white
background, thin light-gray line separating cells.

Character: a friendly Japanese man around 68 years old, short thinning gray hair, kind
lived-in face with soft wrinkles, no glasses. Outfit: soft olive-green cardigan over a
cream collared shirt. He is an ordinary retiree, warm and a little unsure — the viewer's
stand-in, never an expert.

Framing in every cell: waist-up (bust shot), body turned three-quarters toward the LEFT
side of the frame, head fully visible with clear margin above, cropped at the waist.

The 6 poses, left to right, top row then bottom row:
1. listening quietly, calm neutral face, hands at his sides
2. one hand touching his chin, thinking, eyes slightly narrowed
3. surprised, eyes wide open, eyebrows up, mouth slightly open
4. worried, eyebrows drawn together, head tilted slightly down
5. relieved, exhaling with a soft smile, shoulders lowered
6. nodding in understanding, clear warm smile, one hand lightly raised

Art style: clean flat vector illustration, bold clear outlines, simple cel shading, limited
palette of navy blue, white, warm gray, olive green and a touch of amber, minimal detail,
high contrast so it stays readable when shrunk very small. Modern Japanese explainer-video
look. MUST match the art style of the other character sheet exactly.
```

### 1.3 Negative prompt (dán vào ô negative nếu tool có)

```
text, letters, japanese text, watermark, logo, signature, name badge, ID card, stethoscope,
medical cross, hospital, lab equipment, syringe, money symbols, photorealistic, 3d render,
heavy gradients, busy background, furniture, desk, shadows on background, cropped head,
extra fingers, deformed hands, multiple different faces, inconsistent outfit
```

## 2. NẾU SHEET RA LỆCH — 12 prompt rời (dự phòng)

Cách dùng: gen **ảnh #1 trước**, duyệt xong thì **đính chính ảnh đó làm ảnh tham chiếu**
cho 5 ảnh sau kèm câu 「same character, same face, same outfit as reference」.

**Khối STYLE ANCHOR — dán vào MỌI prompt rời:**

```
Clean flat vector illustration, bold clear outlines, simple cel shading, limited palette of
navy blue, white, warm gray and a touch of amber, minimal detail, high contrast, modern
Japanese explainer-video look. Waist-up bust shot, head fully visible with clear margin
above, cropped at the waist. Plain flat pure white background. No text, no logo.
```

| # | Tên file sẽ đặt | Nhân vật | Câu tư thế nối sau STYLE ANCHOR |
|---|---|---|---|
| 1 | `sensei_present.png` | 案内役 | standing calmly, one open palm gesturing to his right, warm neutral expression, turned three-quarters right |
| 2 | `sensei_point.png` | 案内役 | pointing with index finger to his right, attentive expression |
| 3 | `sensei_explain.png` | 案内役 | both hands open in an explaining gesture, eyebrows slightly raised |
| 4 | `sensei_reassure.png` | 案内役 | one hand on his chest, soft reassuring smile, gentle nod |
| 5 | `sensei_caution.png` | 案内役 | one index finger raised, serious careful expression, not angry |
| 6 | `sensei_conclude.png` | 案内役 | a small confident nod with a closed-mouth smile, hands relaxed |
| 7 | `kikite_listen.png` | 聞き手 | listening quietly, calm neutral face, hands at his sides, turned three-quarters left |
| 8 | `kikite_think.png` | 聞き手 | one hand touching his chin, thinking, eyes slightly narrowed |
| 9 | `kikite_surprised.png` | 聞き手 | surprised, eyes wide open, eyebrows up, mouth slightly open |
| 10 | `kikite_worried.png` | 聞き手 | worried, eyebrows drawn together, head tilted slightly down |
| 11 | `kikite_relieved.png` | 聞き手 | relieved, exhaling with a soft smile, shoulders lowered |
| 12 | `kikite_nod.png` | 聞き手 | nodding in understanding, clear warm smile, one hand lightly raised |

## 3. 🔴 HAI QUYẾT ĐỊNH THIẾT KẾ — nói rõ để mày đảo được nếu không thích

### 3.1 案内役 KHÔNG mặc áo blouse trắng (khác demo hiện tại)

Demo đang dùng `kenkyuin.png` = **áo blouse trắng phòng thí nghiệm**. Bộ mới cho mặc
**gi-lê len navy + sơ mi trắng, cầm bìa kẹp hồ sơ**. Lý do:

- Luật YMYL của kênh (`CLAUDE.md` §RULE 1 + `youtube-compliance.md` §5) cấm persona gợi
  **tư cách hành nghề**. Áo blouse trắng trên một kênh nói về TIỀN dễ đọc thành "chuyên gia
  có bằng" — đúng thứ mình đã tự cấm khi bỏ ý định bịa móc 「元ハロワ職員」.
- Đối thủ mặc áo blouse được vì brand của nó là **保健室** (phòng y tế trường học) — cái áo
  là chơi chữ với tên kênh. Brand mình là **研究室 tiền hưu**, không có chỗ tựa đó.
- Gi-lê + bìa hồ sơ đọc ra 「người ở quầy hướng dẫn」 — khớp đúng định vị đã chốt:
  「người cùng đọc tài liệu gốc giúp bạn」.

→ Muốn giữ áo blouse thì đổi 1 dòng trong prompt (`white lab coat over a light blue shirt`),
nhưng tao khuyên không.

### 3.2 聞き手 là nhân vật MỚI, không phải một trong 7 モニター

Dàn `モニター` (田中/佐藤/鈴木/高橋/山田/伊藤/松本) là **nhân vật của case study**, xoay theo
đề tài và sống trong tấm bảng. Nếu bắt một người trong đó đứng mép khung mọi video thì hoặc
là 6 người kia mất vai, hoặc mỗi video đổi người đứng mép = mất nhận diện. Nên 聞き手 là vai
riêng: **người hỏi hộ khán giả**, không tên, không số liệu, không bao giờ là ca tính tiền.

📌 **Tùy chọn +6 ảnh (chưa cần ngay):** thêm một 聞き手 **nữ 65 tuổi** để xoay theo đề tài
(遺族年金 / 加給年金 / パート社保 hợp giọng nữ hơn). Copy prompt §1.2, đổi mô tả nhân vật.
Đối thủ có đúng 2 học trò và xoay theo chủ đề — nhưng nó có 25 video rồi, mình thì chưa.

## 4. GATE DUYỆT — 3 cửa, rớt 1 là gen lại

1. **Cửa 168px:** thu ảnh còn cao 168px → **vẫn phân biệt được biểu cảm** (ngạc nhiên vs lo
   vs gật). Không phân biệt được = nét quá mảnh hoặc mặt quá chi tiết → gen lại "bolder
   outlines, simpler face".
2. **Cửa nhất quán:** dán 6 ảnh cạnh nhau — **cùng một người**? Lệch tóc/kính/áo/tuổi = gen
   lại cả sheet, đừng vá lẻ.
3. **Cửa cặp đôi:** đặt 案内役 cạnh 聞き手 — **cùng một nét vẽ**? Một bên line mảnh, một bên
   bo tròn là hỏng (đúng bệnh của demo hiện tại: いらすとや ghép với line-art).

## 5. COMPLIANCE (quét trước khi khoá bộ)

- ✅ Nhân vật **hư cấu**, không dựa mặt người thật cụ thể → ảnh minh hoạ tĩnh do AI =
  **production assistance, KHÔNG phải tick "altered/synthetic"** (`youtube-compliance.md` §2).
- ⛔ Không huy hiệu / thẻ tên / bằng cấp / logo cơ quan trên người (gợi tư cách hành nghề).
- ⛔ Không ống nghe, chữ thập y tế, dụng cụ thí nghiệm (né đọc nhầm thành y tế).
- ⛔ Không chữ Nhật trong ảnh — chữ nào cũng phải do tool vẽ, nếu không sửa nội dung là
  phải gen lại ảnh.

## 6. ✅ ĐÃ LÀM (2026-08-08) — bộ thật đang chạy

User gen 2 sheet **4×2 = 8 ô/nhân vật** (nhiều hơn 6 ô yêu cầu). Đã cắt xong bằng
`_media_library/cut_cast_sheet.py` (rembg model `isnet-anime` + giữ blob lớn nhất +
autocrop alpha + chuẩn hoá cao **1280px**). File thô giữ ở `assets/cast/_raw/`.

| 案内役 (trái) | 聞き手 (phải) |
|---|---|
| `sensei_present` mở lòng bàn tay | `kikite_listen` tay lên tai, lắng nghe |
| `sensei_point` chỉ tay vào bảng | `kikite_think` tay chạm cằm |
| ~~`sensei_explain`~~ ⛔ **LOẠI** | `kikite_surprised` mắt mở to |
| `sensei_hold` ôm bìa, mỉm cười | `kikite_worried` nhíu mày |
| `sensei_reassure` tay lên ngực | `kikite_down` buồn/xuôi vai |
| `sensei_caution` giơ 1 ngón | `kikite_relieved` thở phào |
| `sensei_serious` nghiêm, trung tính | `kikite_talk` cười, đang nói |
| `sensei_conclude` gật, cười khép | `kikite_nod` gật, hiểu ra |

⛔ **`sensei_explain` rớt gate §4 cửa 2 (nhất quán):** ô đó model vẽ **tóc khác** (bù xù,
mất vệt bạc thái dương) và **mất bìa kẹp hồ sơ** → đứng cạnh 7 ô kia là lộ ngay. File vẫn
nằm trong `assets/cast/` nhưng **không đưa vào vòng xoay**. Cần tư thế "hai tay mở giải
thích" thì gen lại riêng ô đó, đính ảnh `sensei_present` làm tham chiếu.

🔴 **Bài học kỹ thuật đáng giữ — cân theo CỠ ĐẦU, không theo chiều cao khung.** 案内役 chụp
tới hông (đầu ≈ 23% chiều cao ảnh), 聞き手 chụp tới ngực (≈ 34%). Cho cả hai cùng cao 560px
thì đầu ông già to gấp rưỡi = nhìn như hai thế giới. `make_stage.py::CAST_SCALE` giờ giữ hệ
số riêng từng nhân vật (`sensei 1.00 · kikite 0.70`). Gen thêm nhân vật mới với khung ảnh
khác → **phải thêm hệ số**, không thì lệch.

Đã chạy: `FALLBACK` → `sensei_present`/`kikite_listen`; 4 cảnh demo gắn biểu cảm theo nhịp
(chỉ tay → ngạc nhiên → trấn an → gật); render lại `06_VIDEO/_stage_demo/stage_demo.mp4`
(24,5s) + duyệt 4 frame bằng mắt.

**Còn lại (chưa làm):** style phụ đề `bar` trong `video_render.py` · nối khoá `"stage"` vào
SLIDES.json · tùy chọn 聞き手 nữ 65 tuổi · bộ ICON §7.

## 7. BỘ ICON DÙNG CHUNG — 28 hình, gen MỘT lần (đề xuất 2026-08-08)

> 📄 **BẢN .TXT ĐỂ IMPORT VÀO EXTENSION** (mỗi dòng = 1 prompt trọn vẹn, không xuống dòng
> giữa chừng — xem [[project_flow_batch_ext]]):
> · `assets/prompts/icons_28_batch.txt` — **28 dòng**, mỗi dòng 1 icon rời
> · `assets/prompts/sheets_batch.txt` — **5 dòng**: ① tờ 28 icon dạng lưới 7×4 ② sheet
>   案内役 ③ sheet 聞き手 nam ④ sheet 聞き手 **nữ 65** (tùy chọn) ⑤ vá riêng ô
>   `sensei_explain` bị lệch
>
> **Chọn dòng nào:** `icons_28_batch.txt` cho ra **28 ảnh riêng, độ phân giải cao, tao khỏi
> cắt** nhưng có nguy cơ **lệch nét giữa các ảnh**; dòng 1 của `sheets_batch.txt` cho ra
> **1 tờ chắc chắn cùng nét** nhưng mỗi icon chỉ ~1/28 độ phân giải. Ngách này ưu tiên
> **đồng bộ hơn độ nét** (icon hiện ở cỡ ~80–140px trong bảng) → **thử tờ lưới trước**,
> lệch quá thì mới quay sang batch 28 dòng.

**Vấn đề:** icon trong tấm bảng hiện do `make_stage.py` vẽ bằng code — nét mảnh đều, không
cùng ngôn ngữ hình với hai nhân vật (viền dày, bo tròn). Đứng cùng khung là thấy lệch.

🔴 **ĐỪNG gen lẻ theo từng video.** Mỗi video cần bộ icon khác nhau (年金手帳 / 通帳 / はがき
/ 印鑑 / カレンダー / 役所 / 天秤…). Gen lẻ = mỗi lần làm video phải chờ, và style trôi dần
qua từng đợt gen. Gen **một tờ dùng chung** thì cả kênh nói cùng một thứ tiếng hình mãi mãi.

**Lưới 7 cột × 4 hàng = 28 icon**, thứ tự đọc trái→phải, trên→dưới (tao cắt theo đúng thứ tự
này, đừng đảo):

```
A 7x4 grid icon sheet, 28 separate icons, one icon per cell, evenly spaced, each icon
centered in its own cell with generous empty margin, plain flat pure white background,
thin light-gray line separating the cells.

Row 1: a sealed envelope, a postcard, a Japanese pension handbook (small booklet), a bank
passbook, a bank cash card, a personal seal stamp (hanko), a wall calendar
Row 2: a clock, a house, a bank building with columns, a city hall building, a hospital
building, a single standing person, an elderly married couple standing together
Row 3: a stack of documents, an application form with a pen, a calculator, a wallet, a
money pouch with a yen symbol, a bar chart going up, a bar chart going down
Row 4: a balance scale, a magnifying glass, a checklist with ticks, a mailbox, a
smartphone, a padlock, a warning triangle with an exclamation mark

Art style: bold clean outlines of uniform thickness, simple flat shapes, gentle rounded
corners, minimal interior detail, flat cel coloring with a limited palette of deep navy
blue, white, warm gray and a single amber accent. Friendly modern Japanese explainer-video
icon set. Every icon must share the exact same line weight, the same corner rounding and
the same palette so they read as ONE family. High contrast, still readable when shrunk to
80 pixels. No text, no letters, no numbers, no logos, no gradients, no drop shadows,
no photorealism, no 3d.
```

**Negative:** `text, letters, numbers, japanese characters, logo, watermark, gradients, drop
shadow, 3d render, photorealistic, thin hairlines, inconsistent line weight, busy detail`

**Gate riêng cho icon (ngoài 3 cửa §4):**
1. **Cửa 80px:** thu mỗi icon còn 80px — vẫn nhận ra là vật gì. Không ra = chi tiết thừa.
2. **Cửa gia đình:** dán 28 cái cạnh nhau — **cùng độ dày nét, cùng độ bo góc**? Lệch một
   vài cái thì chỉ gen lại **cả tờ**, đừng vá lẻ (vá lẻ chắc chắn lệch).
3. **Cửa cặp với nhân vật:** đặt 1 icon cạnh `sensei_present` — cùng ngôn ngữ hình chưa?

**Nếu không gen:** không sao, `make_stage.py` vẫn có 7 icon vector tự vẽ và tao nâng độ dày
nét lên cho gần bộ nhân vật. Bộ 28 icon là **nâng cấp, không phải chặn đường**.

### 7.1 ✅ ĐÃ LÀM (2026-08-09) — 28 icon + 聞き手 nữ đang chạy

User gen đủ 5 dòng của `sheets_batch.txt`. Kết quả nhận/loại:

| Tờ | Xử lý |
|---|---|
| **Lưới 28 icon** | ✅ **NHẬN** → `assets/icons/*.png` (28 file, 512px, nền trong). Cắt bằng `_media_library/cut_icon_sheet.py` |
| **聞き手 nữ 65** | ✅ **NHẬN** → `josei_listen … josei_nod` (8 file), hệ số `CAST_SCALE["josei"]=0.70` |
| Sheet 案内役 (gen lại) | ⛔ **KHÔNG dùng** — xem §7.2 |
| Sheet 聞き手 nam (gen lại) | ⛔ **KHÔNG dùng** — xem §7.2 |
| Ảnh lẻ vá `sensei_explain` | ⛔ **KHÔNG dùng** — nét khác hẳn bộ đang chạy |

🔴 **Cắt icon KHÔNG dùng rembg** — có tool riêng `cut_icon_sheet.py`. Lý do: rembg đoán
"vật thể", với line-art phẳng nó ăn mất nét mảnh hoặc giữ lại mảng trắng. Icon có cách đúng
và tất định hơn: **flood-fill từ 4 mép** — trắng nào NỐI ra mép = nền (xoá), trắng nào bị
nét bao kín (ruột nhà, mặt đồng hồ, thân lịch) = phần của hình (giữ). Không mô hình, không
ngẫu nhiên, chạy lại ra đúng file cũ.

### 7.1b ✅ VÒNG VÁ (2026-08-09, `fixes_batch.txt` — 4/4 nhận)

Vòng đầu có 5 icon dính chữ và 2 nhân vật lệch họ nét. Đã gen lại và thay hết:

| Vá | Kết quả |
|---|---|
| `form` (chữ Nhật BỊA 「入抜書」) | ✅ thay — mặt giấy trống trơn, chỉ còn dòng kẻ + ô |
| `nenkin_techo` `passbook` `cashcard` `bank` (chữ `BANK` / `PENSION HANDBOOK`) | ✅ thay — **sạch chữ hoàn toàn** (gen lưới 2×2) |
| `sensei_explain` | ✅ **giờ ĐÚNG họ A** → vào vòng xoay, 案内役 đủ 8 tư thế |
| `josei_*` (8 ảnh) | ✅ gen lại theo họ A — da ấm, đổ bóng, má ửng, viền dày |

🔴 **Bí quyết làm cho khớp họ nét: ĐÍNH ẢNH THAM CHIẾU + tả đặc điểm bằng chữ.** Prompt vòng
1 chỉ ghi 「MUST match the art style of the other character sheets」 → model không thấy tờ kia
nên vẽ theo họ của nó. Vòng 2 đính `sensei_present.png` / `kikite_listen.png` **và** tả thẳng
「warm peachy skin tones, visible soft cel shading on hair and clothing folds, slightly
heavier dark navy outlines, gentle blush」 → khớp ngay. Gen thêm nhân vật sau này thì làm y vậy.

🔴 **BẪY TỈ LỆ CỦA ẢNH GEN LẺ (đo được, không đoán).** Ảnh gen **một mình** bị crop sát hơn
ảnh cắt từ sheet → cùng một nhân vật mà **đầu to hơn giữa các cảnh**. Đo `cao đầu / cao ảnh`:
`sensei_present` 0.452 · `sensei_point` 0.453 · `sensei_reassure` 0.480 · nhưng
**`sensei_explain` 0.534** (+16%). Đã thêm `CAST_SCALE_FILE = {"sensei_explain": 0.85}` trong
`make_stage.py` — bù riêng từng file, thắng hệ số nhóm. **Mọi ảnh gen lẻ sau này phải đo lại
và bù**, không thì nhân vật "phình đầu" ở đúng cảnh đó.
📌 Cùng lượt đã nâng `kikite` 0.70 → **0.78** (đo ra đầu ông ấy nhỏ hơn 案内役 ~15%).

### 7.2 Vì sao KHÔNG thay bộ nhân vật bằng bản gen lại

Đợt 09/08 sinh ra **hai họ nét khác nhau**: họ **A** (đang chạy, gen 08/08) da ấm hơn,
có đổ bóng, viền dày; họ **B** (gen 09/08: 案内役 mới + 聞き手 nữ) phẳng hơn, nét mảnh hơn.
Trộn 案内役 của A với 案内役 của B thì thành hai người khác nhau giữa các video.

- **Giữ A làm bộ chính** — đã cắt xong, đã wired, đã render duyệt, và **viền dày đọc tốt hơn
  ở cỡ nhỏ** (đúng hướng gate 45+).
- **Nhận riêng 聞き手 nữ của B** vì A không có nhân vật nữ nào cả. Đã **đo thật, không đoán**:
  dựng khung 案内役(A) đứng cạnh 聞き手 nữ(B) rồi soi ở **480px** — ở cỡ phát sóng **không
  nhìn ra khác biệt nét**. Chênh lệch chỉ lộ khi phóng 1280px, mà người xem không bao giờ
  thấy cỡ đó.
- Muốn tuyệt đối sạch thì gen lại nữ theo họ A: thêm vào prompt 「warmer skin tones, visible
  soft shading on hair and clothes, slightly heavier outlines」.
