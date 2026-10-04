# THUMBNAIL PROMPT — kênh 真夜中の朗読便 (chốt 2026-07-28) — ⚠️ KHÔNG CÒN LÀ MẶC ĐỊNH

> 🔴 **ĐẢO CHỐT 2026-07-29 (user):** kênh quay về **TEXT-WALL render bằng `make_thumb_textwall.py`** — chữ tool vẽ đè scene, 5–6 dòng, kiểu video 07 amamidokoro. Nguồn sự thật mới: `CLAUDE.md` mục Thumbnail + skill `thumbnail-chouhen`.
> File này giữ làm **PHƯƠNG ÁN B / A-B test** — chỉ dùng khi user chỉ định.
>
> ~~Cách làm thumbnail của kênh từ 2026-07-28: Claude xuất PROMPT, user tự gen. KHÔNG render bằng tool nữa.~~ (chỉ sống 1 ngày)
> File này là bản gốc để copy khi chạy phương án B. Mỗi video chỉ thay: 3 nhân vật + 6 dòng chữ.

## 1. TEMPLATE (copy nguyên, điền chỗ `<…>`)

```
Photorealistic YouTube thumbnail, 16:9, Japanese domestic drama, cool cinematic grade.
ONE single continuous photograph of ONE room — no collage, no inset frame, no split screen,
no border, no visible seam anywhere.

COLOUR GRADE: cool and moody. Teal-blue shadows, neutral-cool highlights, low overall warmth,
slightly desaturated skin. A cool steel-blue key light enters from the RIGHT and rakes across
the room, so the LEFT side of the same room falls into deep natural shadow. Both halves are
equally SHARP and IN FOCUS, same film grain, same cool colour — the left is darker only
because of the lighting, never because of blur. Wood grain and shoji lattice stay clearly
visible in the shadowed left side.

RIGHT 52% OF THE FRAME — three Japanese characters, layered by depth, all three faces visible,
none overlapping another face:
- FOREGROUND lower right, LARGEST — THE HEROINE: a BEAUTIFUL elegant Japanese woman ~35,
  delicate refined features, fair flawless skin, large expressive eyes, soft glossy black hair,
  quietly stunning, in <trang phục nữ chính>. Expression: <biểu cảm đỉnh của nữ chính>.
  A cool steel-blue rim light traces her cheek and hair so she separates from the background.
  She is the visual anchor.
- MID-GROUND upper left of this group: <nhân vật thứ hai — tuổi, trang phục>.
  Expression: <biểu cảm>. Eyes open with pupils clearly visible — NOT rolled back,
  no eye whites showing.
- BACKGROUND between them, smaller: <phản diện — tuổi, trang phục>, <hành động>,
  <biểu cảm khinh>, colder and darker in tone than the heroine.

LEFT 48% OF THE FRAME — over the shadowed part of the same room, exactly SIX lines of Japanese
text, left-aligned, stacked tightly, every glyph carrying a thick black outline and a drop
shadow so it stays readable over the photograph.

STRONGLY VARIED TEXT SIZES — this size contrast is what pulls the eye. Relative cap heights in
brackets. Render the text EXACTLY, character for character: no extra characters, no missing
strokes, no invented kanji.

Line 1  [1.0x]   ice white #F2F7FF, with <từ khoá> in warm yellow #FFE200   <dòng 1>
Line 2  [0.65x]  ice white #F2F7FF                                          <dòng 2>
Line 3  [1.35x]  ice white #F2F7FF, with <từ khoá> in warm yellow #FFE200   <dòng 3>
Line 4  [0.8x]   soft light cyan #8CEBFF                                    <dòng 4>
Line 5  [0.65x]  ice white #F2F7FF, with <từ khoá> in amber #FFB703         <dòng 5>
Line 6  [1.8x]   amber #FFB703 with a thick WHITE outer glow, the LARGEST line, spanning the
                 full width across the very bottom of the frame             <dòng 6>

Typography: heavy bold Japanese gothic sans-serif (M PLUS 1p Black style). Lines 1-5 each fill
the width of the left column; the 1.35x and 1.8x lines must be unmistakably bigger than the
0.65x lines at a glance. The only warm colours in the whole image are the yellow and amber
text accents — everything else stays cool.
No magenta, no pink, no purple, no pure saturated red anywhere in the text.
Filmic grade, 4k, natural attractive Japanese faces, strong contrast between the three
expressions: <cảm xúc 1>, <cảm xúc 2>, <cảm xúc 3>.

(negative: blurred background, bokeh on the left side, gaussian blur, out-of-focus left half,
solid flat black panel, separate dark rectangle, different exposure between halves, visible
seam, collage, inset frame, split screen, warm orange grade, sepia, all text the same size,
uniform text size, magenta text, pink text, purple text, pure red text, plain or harsh-looking
heroine, aged heroine, distorted faces, deformed hands, extra fingers, cartoon, anime,
rolled-back eyes, white eyes, possessed look, horror, misspelled Japanese, garbled kanji,
invented characters, extra characters, random latin letters, watermark, logo)
```

**Xuất 16:9, ≥2560×1440.** Lưu `06_VIDEO/_series_assets/thumb_<NN>_ai.jpg`.

## 2. LUẬT VIẾT 6 DÒNG CHỮ

| Dòng | Cỡ | Màu | Vai | Ký tự |
|---|---|---|---|---|
| 1 | 1.0x | trắng băng + từ khoá VÀNG | bối cảnh mở | ≤9 |
| 2 | 0.65x | trắng băng | bồi | ≤9 |
| 3 | **1.35x** | trắng băng + từ khoá VÀNG | **câu sốc** (thường là thoại) | ≤9 |
| 4 | 0.8x | **CYAN NHẠT** | thoại phản diện 「…ｗ」 | ≤9 |
| 5 | 0.65x | trắng băng + từ khoá AMBER | bồi, dẫn vào đòn | ≤9 |
| 6 | **1.8x** | **AMBER + quầng trắng** | đòn bỏ lửng | ≤9 |

- **≤9 ký/dòng, tổng ~50 ký** — càng nhiều ký tự thì model càng dễ viết sai kanji. Đừng nhồi thêm dòng.
- Nội dung 6 dòng lấy từ KHỐI 2 của script (skill `script-chouhen`), phải **có thật trong thân truyện**.
- Quét từ cấm theo `.claude/rules/youtube-compliance.md` mục 3 TRƯỚC khi đưa prompt.

## 3. CĂN CỨ CỦA BẢNG MÀU (đo WCAG 2026-07-28, đừng vặn lại bằng cảm tính)

Tương phản độ chói của từng màu trên **nền tối** / **khi chữ đè lên ảnh**. Mắt 45–70 cần ≥7x trên nền tối và ≥4,5x khi đè ảnh:

| Màu | nền tối | đè ảnh | |
|---|---|---|---|
| trắng băng `#F2F7FF` | **15,3x** | **5,4x** | ✅ màu NỀN của chữ |
| kem `#FFF6E0` | 15,3x | 5,4x | ✅ (bản ấm, dùng khi grade ấm) |
| vàng ấm `#FFE200` | 12,6x | 4,5x | ✅ từ khoá |
| thép nhạt `#D6E6F5` | 12,9x | 4,6x | ✅ dự phòng |
| cyan nhạt `#8CEBFF` | 12,1x | 4,3x | ✅ thoại phản diện |
| amber `#FFB703` | 9,4x | 3,4x | ⚠️ **phải có quầng trắng** |
| cam `#FF9600` | 7,7x | 2,9x | ⚠️ |
| tím `#BE60FF` | 5,0x | 1,9x | 🔴 KHÔNG dùng |
| hồng neon `#FF2E93` | 4,8x | 1,8x | 🔴 KHÔNG dùng |
| **đỏ `#FF1818`** | **4,2x** | **1,5x** | 🔴 **tệ nhất** — đã bỏ khỏi chuẩn |

Ba nguyên tắc rút ra:
1. **Mỗi dòng tối đa MỘT điểm nóng**, phần còn lại là trắng băng. Nhiều điểm nóng = cảm giác "lộn xộn".
2. **Không đặt hai dòng bão hòa cạnh nhau** (hồng cạnh cyan là cặp rung, gây mỏi mắt thật).
3. Ảnh tông LẠNH thì **hai màu ấm duy nhất là vàng + amber** → chúng độc quyền hút mắt. Đây là lý do bảng màu và grade phải đi cùng nhau.

⚠️ Đỏ thuần từng là dòng đòn của v5.5/v5.6 và **chỉ sống được nhờ quầng trắng** — không phải nhờ màu. Đỏ góp 21% vào độ chói và bị sai sắc (mắt hội tụ bước sóng đỏ ở độ sâu khác) → chữ đỏ lớn trên nền tối nhoè viền với mắt 45–70.

## 4. KHI CHỮ AI SAI KANJI (dự phòng)

Model viết ~50 ký tự tiếng Nhật thì **rất dễ sai ít nhất một chữ**: thêm/thiếu nét, ra kanji không tồn tại, lặp chữ. Với khán giả nữ Nhật 45–70, kanji sai = tín hiệu hàng rác.

**Luật: một chữ sai là KHÔNG đẩy lên kênh.**
1. Gen xong → Claude soi từng ký tự đối chiếu 6 dòng gốc, báo chữ nào lệch.
2. Sai mà ảnh đẹp → **gen lại ảnh KHÔNG CHỮ** (bỏ toàn bộ khối text + đổi thành `TOP 20% / BOTTOM 30% empty` như bản cũ) rồi dùng tool vẽ chữ:
   `python tools/make_thumb_textwall.py <out> --lines <6 dòng> --colors "e,e,e,s,e,a" --accent y --accent2 a --halo 5 --weights "0.78,0.52,1.0,0.66,0.52,1.0" --wide 5 --align left --indent 26 --block fill --outline 0.032 --fat 0 --panel-w 0.52 --bg <ảnh>`
   (`e` kem · `s` cyan nhạt · `a` amber — 3 màu đã thêm vào tool 2026-07-28)
3. Toàn bộ cờ + bản thử của tool: `06_VIDEO/_thumb_v5_demo/V5_DEMO_2026-07-28.md`.

## 5. VÍ DỤ ĐÃ ĐIỀN — video 10 `haha-no-gamaguchi`

Nhân vật: 私 (nữ chính 35, suit xám, sốc đau) · 母 (72, cardigan, mắt trống không nhận ra con) · 弟嫁 (35, kimono đen, khoanh tay cười khinh).

```
Line 1  四年ぶりの実家で      (từ khoá vàng: 実家)
Line 2  母は私を他人扱い
Line 3  母「ご予約の方?」     (từ khoá vàng: ご予約)
Line 4  弟嫁「認知症ｗ」
Line 5  だが母の財布から      (từ khoá amber: 財布)
Line 6  貸金庫の鍵が出た
```

Thumbnail đang trên sóng của video này (`CHOT_v5_6`, render bằng tool, bảng màu hồng/đỏ cũ) — thay khi có bản gen theo chuẩn này.
