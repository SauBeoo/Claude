# PROMPT PACK ĐẠO CỤ — bộ prop analog cho lớp vox "collage hồ sơ" (2026-08-08)

> Gen MỘT LẦN, dùng cho cả kênh. Mỗi prompt gen **2–3 bản**, chọn bản nét nhất.
> Ảnh gen xong bỏ vào: `E:\Claude\Projects\_media_library\props\_raw\` — tên file ghi
> ở từng mục (đuôi .png/.jpg đều được, có số bản thì thêm `_2`, `_3`).
>
> ⚠️ 4 luật chung cho MỌI prompt dưới:
> 1. Vật nằm GIỮA khung, nền **trắng trơn tuyệt đối** (tao rembg cắt nền).
> 2. **KHÔNG chữ, không ký tự** trong ảnh (chữ là việc của tool).
> 3. **KHÔNG bóng đổ** (flat even lighting — bóng tool tự thêm, bóng bake sẵn xoay là gãy).
> 4. Chụp thẳng từ trên xuống (top-down, orthographic).

## CÂU STYLE ANCHOR ĐẠO CỤ (dán vào đầu mọi prompt)

```
Single isolated object photographed top-down on a pure white seamless background, flat even studio lighting, no cast shadow, no text, no letters, no watermark, high detail macro texture, photorealistic.
```

---

## A. Mũi tên bút sáp đỏ — `arrow_straight`, `arrow_curve`, `arrow_hook`

A1 · `arrow_straight.png`
```
[ANCHOR] A hand-drawn arrow stroke made with a red wax crayon on paper, straight with slight natural wobble, rough grainy crayon texture with uneven pressure, simple triangular head drawn by hand, about 3:1 wide, vermilion red.
```

A2 · `arrow_curve.png`
```
[ANCHOR] A hand-drawn arrow made with a red wax crayon, one smooth sweeping curve like an annotation on a detective's document, rough crayon grain, hand-drawn open arrowhead, vermilion red.
```

A3 · `arrow_hook.png`
```
[ANCHOR] A hand-drawn arrow made with a red wax crayon, bending in an L-shaped hook with rounded corner, grainy crayon texture, hand-drawn arrowhead, vermilion red.
```

## B. Vòng khoanh + gạch chéo sáp đỏ — `circle_1`, `circle_2`, `cross_x`

B1 · `circle_1.png`
```
[ANCHOR] A hand-drawn rough ellipse made with a red wax crayon, like someone circling an important item on a document, the stroke does not fully close leaving a small gap, wobbly double-pass line, grainy crayon texture, vermilion red, wide oval about 3:2.
```

B2 · `circle_2.png`
```
[ANCHOR] A hand-drawn rough circle made with a red wax crayon, single quick pass, slightly egg-shaped and imperfect, grainy texture, vermilion red.
```

B3 · `cross_x.png`
```
[ANCHOR] A big hand-drawn X cross made with a red wax crayon, two bold rough strokes with grainy uneven texture and slightly overshooting ends, vermilion red.
```

## C. Dây chỉ đỏ + đinh ghim — `string_arc`, `string_sag`, `pin_red`, `pin_brass`

C1 · `string_arc.png`
```
[ANCHOR] A single piece of thin red cotton twine string lying in a gentle arc curve, visible fiber twist texture, deep red, evenly lit.
```

C2 · `string_sag.png`
```
[ANCHOR] A single piece of thin red cotton twine string held at two ends sagging slightly in the middle like on an investigation board, visible fiber texture, deep red.
```

C3 · `pin_red.png`
```
[ANCHOR] One round-head push pin viewed from a slight top angle, glossy dark red plastic head, short steel needle, macro detail.
```

C4 · `pin_brass.png`
```
[ANCHOR] One vintage brass thumbtack viewed from a slight top angle, aged patina metal flat head, macro detail.
```

## D. Giấy xé làm nhãn (TRỐNG — tool đóng chữ Nhật thật lên) — `label_strip`, `label_tag`, `label_wide`

D1 · `label_strip.png`
```
[ANCHOR] A blank strip of aged cream washi paper torn by hand on all four edges, rough fibrous torn edges, subtle old paper stains, completely blank surface, wide strip about 4:1.
```

D2 · `label_tag.png`
```
[ANCHOR] A blank small rectangle of old kraft paper torn by hand, ragged edges, slightly yellowed with age spots, completely blank, about 2:1.
```

D3 · `label_wide.png`
```
[ANCHOR] A blank wide piece of aged manila paper torn roughly on all edges, one corner slightly folded, fibrous torn texture, completely blank, about 3:1.
```

## E. Băng dính washi — `tape_1`, `tape_2`

E1 · `tape_1.png`
```
[ANCHOR] One short strip of semi-transparent beige washi masking tape with torn ends, subtle paper fiber texture, slightly wrinkled, matte.
```

E2 · `tape_2.png`
```
[ANCHOR] One short strip of semi-transparent off-white masking tape torn at both ends at an angle, slight creases and air bubbles, matte.
```

## F. Khung con dấu TRỐNG (tool đặt chữ vào giữa) — `stamp_round`, `stamp_rect`

F1 · `stamp_round.png`
```
[ANCHOR] A blank round rubber stamp imprint in red ink on white, only the double circle border ring with grunge missing patches and uneven ink bleed, nothing written inside, distressed vintage look, vermilion red ink.
```

F2 · `stamp_rect.png`
```
[ANCHOR] A blank rectangular rubber stamp imprint in red ink, only the thick rough border frame with worn grunge edges and ink smudge, empty inside, vintage archival look, vermilion red ink.
```

## G. Đồ lặt vặt tạo chất — `clip_1`, `stain_coffee`, `smudge_ink`

G1 · `clip_1.png`
```
[ANCHOR] One slightly rusty vintage metal paper clip, macro detail.
```

G2 · `stain_coffee.png`
```
[ANCHOR] A faint dried coffee cup ring stain on white, light brown, partial broken ring, watery edge texture.
```

G3 · `smudge_ink.png`
```
[ANCHOR] A small smudged fingerprint of red ink on white, faded and grainy, vermilion.
```

---

## Sau khi gen
1. Bỏ hết vào `props\_raw\` đúng tên trên.
2. Tao chạy prep: rembg cắt nền → chuẩn hoá → `props/INDEX.json`, rồi sửa `make_vox.py`
   sang chế độ đạo cụ (mũi tên reveal kiểu vẽ tay, nhãn thả rơi, con dấu slam, dây chỉ
   căng dần) → dựng lại 6 thẻ demo `_vox_ai_demo` so 3 đời.
3. Bản nào dính chữ/bóng đổ đậm/nền không trắng → loại, gen lại (3 luật đầu trang).
```
