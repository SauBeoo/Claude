# 06_mizumawari-numeri — PROMPT ẢNH AI (user tự gen)

> Bộ prompt gen ảnh tĩnh cho video 06. **Ảnh AI TĨNH = production assistance → KHÔNG cần tick "altered/synthetic content"** (khác AI video: có 1 clip AI realistic là phải tick cả video — luật `.claude/rules/youtube-compliance.md` §2).
> Gen ảnh **SẠCH, KHÔNG CHỮ** — chữ/telop do tool `tools/bake_telop.py` nướng lên sau. Tránh nhãn hãng thật trên chai lọ, tránh mặt người nhìn thẳng.

## 0. STYLE CHUNG — dán TRƯỚC mọi prompt (giữ cả video một tông)

```
Photorealistic cinematic documentary still, Japanese home interior, soft natural
daylight from a side window, warm neutral palette, muted colors, shallow depth of
field, fine detail, calm quiet mood, 16:9 horizontal, no text, no logos, no brand
labels, no human faces.
```

Vì sao phải khoá tông: đoạn proof `06_VIDEO/06_proofA/` chứng minh stock chắp vá tông (bình xịt nền hồng–xanh, cụm rau Ý) làm khung telop/split trông nghiệp dư dù layout đúng. Cả video dùng 1 style string → mọi khung nhìn như một bộ phim.

## 1. LUẬT ĐẶT TÊN (bắt buộc — tool đọc theo tên)

Đặt ảnh gen xong vào `06_VIDEO/06_mizumawari-numeri/slides_img/`:

| Khuôn | Tên file | Ghi chú |
|---|---|---|
| Ảnh thường / telop | `slide_NN.jpg` | NN = index entry trong `_SLIDES.json` (đếm từ 00) |
| Split-screen | `slide_NN_L.jpg` + `slide_NN_R.jpg` | 2 nửa trái/phải |

Index cụ thể tao gán khi dựng `06_mizumawari-numeri_SLIDES.json`. Ảnh gen trước khi có index thì cứ đặt tên mô tả (vd `numeri_drain_foam.jpg`), tao rename vào đúng chỗ.

## 2. ƯU TIÊN 1 — 3 ảnh chốt tông (gen trước, để tao dựng lại proof bằng ảnh thật đúng tông)

| # | Dùng ở đâu | Prompt (nối sau style chung) |
|---|---|---|
| P1 | **Bọt trong lỗ thoát nước** — nền cho telop「二酸化炭素の泡」(thay ảnh bọt macro stock hiện tại) | Extreme close-up of a stainless steel kitchen sink drain with white baking soda powder around the rim, fresh white foam actively fizzing and bubbling up out of the drain opening, wet stainless surface, water droplets, soft daylight from the left. |
| P2 | **Nửa PHẢI của split-screen「酸」** (thay ảnh cà chua/basil bị crop trượt) | A plain glass bottle of clear vinegar and a small dish of white citric acid powder on a wooden kitchen counter in a Japanese home, dark muted background, single soft window light from the right, unlabeled bottle. |
| P3 | **Nửa TRÁI của split-screen「アルカリの洗剤」** | Several tall plastic household cleaning spray bottles lined up on a shelf, all completely blank and unlabeled, cool grey-blue plastic, dim indoor light, slightly cluttered utility shelf, muted desaturated tone. |

> Gen mỗi prompt 2–3 bản, chọn bản **không có chữ dính trên chai** và **chủ thể lệch một bên** (chừa chỗ cho telop). P2 và P3 phải cùng độ sáng — split-screen đặt cạnh nhau, lệch sáng là lộ ghép.

## 3. ĐOẠN PHÒNG TẮM (浴室) — giữ nguyên từ bản trước

Before/After = P5 & P7 **cùng góc, cùng khung** (đây là "bằng chứng" của video — quan trọng hơn mọi hiệu ứng).

| # | Match câu thoại | Prompt (nối sau style chung) |
|---|---|---|
| P4 | 浴室の汚れは、二つの顔を持っています | A clean, tidy, empty modern Japanese unit bathroom: white bathtub, tiled wall, a mirror above the washing area, soft morning light through a frosted window, calm mood. Wide establishing shot. |
| P5 | 鏡にこびりつく、白いうろこ模様 (**BEFORE**) | Close-up of a bathroom mirror covered in cloudy white limescale water spots in a fish-scale pattern, the reflection hazy and dull. Straight frontal angle. |
| P6 | キッチンペーパーにしみ込ませ…ラップをかぶせて | Close-up of a hand smoothing transparent cling film over a wet paper-towel compress pressed against a limescale-covered mirror, the paper towel visibly damp. Macro, realistic. |
| P7 | 一時間ほど置いて (**AFTER** — cặp P5, y hệt góc) | The same bathroom mirror, identical framing and angle as before, now perfectly clear and spotless, sharp clean reflection of the bright bathroom. |
| P8 | なぜ、ラップをかぶせるのでしょうか | Macro close-up of transparent cling film clinging tightly to a wet mirror, tiny water droplets trapped underneath the film, glistening — conveying moisture kept from drying out. |
| P9 | 昔の人が、湿布で薬をなじませた | Nostalgic warm sepia-toned still of a folded damp cloth compress being pressed onto a forearm, old-fashioned Japanese home-remedy mood, soft vintage light, hands/arm only, no face. |
| P10 | 重曹をふりかけ、スポンジで軽くこすれば | Extreme close-up of a hand sprinkling white baking soda powder from a small wooden spoon onto a damp cleaning sponge on the edge of a clean white bathtub, water droplets, soft side light. |

## 4. LỚP「昔の暮らし」— chỗ stock trống hoàn toàn (gen sau khi chốt tông)

Đây là lớp làm kênh khác đám lifehack: cảnh không thể quay được. Prompt bỏ 「Japanese home interior」của style chung, thay bằng bối cảnh cổ.

| # | Match câu thoại | Prompt |
|---|---|---|
| P11 | かまどに残った草木の灰を、水に浸していました (灰汁) | Photorealistic documentary still of an old Japanese farmhouse kitchen from the Showa era: a wood-ash filled clay stove (kamado), a wooden bucket of water with grey wood ash settling at the bottom, dim light from a small window, earthen floor, no people, muted sepia tone, 16:9, no text. |
| P12 | 昔の日本の台所には、専用の洗剤なんて一本もありませんでした | Photorealistic documentary still of a traditional Japanese kitchen sink area (doma) from the early Showa era: a stone or wooden basin, a kettle, a bamboo brush, nothing modern, cold morning light, austere and clean, no people, 16:9, no text. |
| P13 | 灰も、酢も、塩も、最後のひとかけらまで使い尽くしました | Photorealistic still life of a wooden shelf in an old Japanese house holding a clay salt pot, an unlabeled vinegar bottle and a bowl of wood ash, warm low evening light, dust in the air, nostalgic, 16:9, no text. |

## 5. QUY TRÌNH SAU KHI CÓ ẢNH

1. Đặt ảnh vào `06_VIDEO/06_mizumawari-numeri/slides_img/` theo tên (Mục 1).
2. `python tools/bake_telop.py 03_SCRIPTS/06_mizumawari-numeri_SLIDES.json 06_VIDEO/06_mizumawari-numeri/slides_img` — nướng telop/split (bản gốc tự cất ở `slides_img/_raw/`, chạy lại không nướng đè).
3. `python E:\Claude\Projects\youtube-jp-health\tools\video_render.py 03_SCRIPTS/06_mizumawari-numeri_TTS.md --img-dir ... --clips-dir ... --sub-style outline --bgm <file> --bgm-gain -40`
