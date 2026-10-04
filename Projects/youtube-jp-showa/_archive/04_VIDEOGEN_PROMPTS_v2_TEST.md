# 04_VIDEOGEN_PROMPTS **v2 — BẢN THỬ** (chưa đè v1)

> Viết 2026-08-04 sau khi mổ kênh mẫu **存在しない街の記憶** (video `FbS5U2HYdVo`, 5:22, 141.5K view/28 ngày).
> ⚠️ **Chưa thay `04_VIDEOGEN_PROMPTS.md`.** File này là bản thử để gen lại D1–D4 rồi đặt cạnh bản cũ. Đạt thì merge vào v1, rớt thì xoá file này.
> Ba luật của v1 mà bản này **cố tình làm ngược** (chờ user chốt): ① bỏ style 8mm/faded/grain ② cho phép CHỮ trong khung ③ cho phép MẶT người.

## 0. Vì sao đổi — bằng chứng, không phải cảm tính

| v1 làm gì | Kết quả thật (D1, 2026-08-04) | Kênh mẫu làm gì |
|---|---|---|
| `8mm home movie film, faded, grain, vignette, muted greens` | 4/4 ảnh ra **trường BỎ HOANG**: tường bong, hành lang tối, bụi dày, không người → không khí phim kinh dị | 9/9 frame **nắng gắt, trời xanh bão hoà, nét 4K, 60fps**. Không một hạt grain giả |
| `no readable text or signage` (cấm chữ) | 2/4 ảnh vẫn tự vẽ poster chữ rác → phải loại 50% | Biển hiệu chữ Nhật **SẠCH, đọc được**: 松尾燃料店 · みのり食堂 · 浮島市場 · ラーメン味平 · 大洋丸. Chính nó tạo cảm giác thật |
| `close-up faces` bị cấm | Cảnh nào cũng trống người → nguội | Mặt cận, biểu cảm rõ, không cần nhân vật nhất quán (góc documentary) |
| Trông vào prompt để đồng bộ tông | 4 ảnh 4 tông | **Lightroom đồng bộ màu TỪNG ảnh** (bước ③ họ công bố) |

**Nguyên tắc gốc của v2:** *chất 昭和 đến từ VẬT TRONG KHUNG (đồ vật, quần áo, biển hiệu, kiến trúc), KHÔNG đến từ lớp giả-phim-cũ.* Lớp giả cổ làm model hiểu là "cũ = hỏng = bỏ hoang".

---

## 1. STYLE LOCK v2 — dán ĐUÔI vào MỌI prompt ảnh

```
, photorealistic documentary photograph of everyday life in 1970s Japan (Showa
era), building in active daily use and well kept, bright natural midday
daylight, crisp clear focus, rich natural colour, warm wood tones, fresh green
foliage outside the windows, soft realistic shadows, faint haze in the air,
shot on a modern full-frame camera with a 35mm lens, calm observational
framing, period-accurate objects and clothing, 16:9
```

## 2. AVOID v2 — Flow không có ô Negative, nên nối câu này vào CUỐI mọi prompt

```
Avoid: film grain, heavy vignette, faded or washed-out colour, sepia tint, dust
and scratches, abandoned or derelict building, peeling walls, ruins, mould,
horror or eerie mood, empty lifeless space, modern objects, smartphones, LED
lighting, air conditioners, plastic bottles, logo-branded sneakers, anime or
illustration style, HDR oversaturation, wide-angle distortion, garbled or
nonsensical lettering.
```

⭐ Bốn từ gánh cả bản vá: **`abandoned`, `derelict`, `peeling walls`, `ruins`** + cụm dương **`in active daily use and well kept`**. Đó là chỗ D1 chết.

## 3. LUẬT KHUNG HÌNH v2 (thay Mục 2 của v1)

1. ✅ **CHO PHÉP mặt người** — mặt ở cỡ trung, biểu cảm sinh hoạt bình thường, **không nhìn thẳng ống kính**. Không cần nhân vật nhất quán giữa các cảnh (khoảng cách documentary). Vẫn cấm mặt người thật cụ thể (compliance §2).
2. ✅ **CHO PHÉP chữ Nhật — nhưng phải ĐƯA ĐÚNG KÝ TỰ trong prompt**, đặt trong 「」. Model gen theo chuỗi cho sẵn thì ra chữ sạch; để nó tự nghĩ thì ra rác. Mẫu: `a small hand-painted wooden signboard reading 「給食室」 in neat brush lettering`.
   → **Soi từng biển hiệu khi duyệt.** Sai nét thì (a) gen lại, (b) đổi sang chữ ngắn hơn 2–3 ký, hoặc (c) bỏ biển hiệu khỏi prompt cảnh đó. **Không** quay lại lệnh cấm chữ toàn diện.
3. **Cùng MỘT ngôi trường** ở mọi cảnh: lặp nguyên văn cụm `wooden school with dark wood trim, sliding wooden-framed windows, polished wooden floor, clean plastered walls` trong mọi prompt cảnh trường.
4. **Gen 8 bản/cảnh** (Nano Banana 2 chạy x4, làm 2 lượt), duyệt mắt chọn 1. v1 gen 4 là quá ít — kênh mẫu gen 「何千枚」 rồi lọc.
5. **Ảnh phải qua duyệt TRƯỚC khi i2v.** Không bao giờ i2v một ảnh chưa duyệt (i2v đắt gấp nhiều lần ảnh).
6. i2v: **1 chuyển động/cảnh**, camera chậm, **cấm cắt trong clip**, 5–8s. Motion prompt chỉ tả CHUYỂN ĐỘNG, không tả lại bối cảnh.

---

## 4. BỐN CẢNH — PROMPT ẢNH v2 (dán nguyên khối, đã gồm style + avoid)

### D1 — Hành lang trưa nắng (beat 2: mùi 給食 trôi qua hành lang)

```
A wooden corridor of a Japanese elementary school in active daily use at noon,
long row of sliding wooden-framed windows down the left side flooding the
polished wooden floor with bright sunlight, the window grid reflected on the
floor, thin steam drifting from the far end of the corridor where the lunch
room is, several pairs of white canvas indoor shoes neatly lined up outside a
classroom door, two or three children walking far away at the end of the
corridor, clean plastered walls with dark wood trim, camera at child eye height
looking straight down the corridor, photorealistic documentary photograph of
everyday life in 1970s Japan (Showa era), building in active daily use and well
kept, bright natural midday daylight, crisp clear focus, rich natural colour,
warm wood tones, fresh green foliage outside the windows, soft realistic
shadows, faint haze in the air, shot on a modern full-frame camera with a 35mm
lens, calm observational framing, period-accurate objects and clothing, 16:9.
Avoid: film grain, heavy vignette, faded or washed-out colour, sepia tint, dust
and scratches, abandoned or derelict building, peeling walls, ruins, mould,
horror or eerie mood, empty lifeless space, modern objects, smartphones, LED
lighting, air conditioners, plastic bottles, logo-branded sneakers, anime or
illustration style, HDR oversaturation, wide-angle distortion, garbled or
nonsensical lettering.
```

**Motion (i2v):**
```
slow steady push-in down the corridor at walking pace, thin steam drifting
through the sunbeams, dust motes floating in the light, the distant children
keep walking away, curtains breathing slightly; camera steady, single
continuous shot, no cut, no camera shake
```

### D2 — 給食当番 bê thùng canh (beat 3)

```
Two Japanese elementary school children seen from behind, wearing white cooking
smocks and white caps, carrying a large dented aluminium soup canister together
by its side handles down a bright wooden school corridor, steam rising from the
lid, other children walking further ahead down the corridor, midday sunlight
pouring through sliding wooden-framed windows on the right, polished wooden
floor, clean plastered walls with dark wood trim, camera behind them at child
eye height, photorealistic documentary photograph of everyday life in 1970s
Japan (Showa era), building in active daily use and well kept, bright natural
midday daylight, crisp clear focus, rich natural colour, warm wood tones, fresh
green foliage outside the windows, soft realistic shadows, faint haze in the
air, shot on a modern full-frame camera with a 35mm lens, calm observational
framing, period-accurate objects and clothing, 16:9.
Avoid: film grain, heavy vignette, faded or washed-out colour, sepia tint, dust
and scratches, abandoned or derelict building, peeling walls, ruins, mould,
horror or eerie mood, empty lifeless space, modern objects, smartphones, LED
lighting, air conditioners, plastic bottles, logo-branded sneakers, anime or
illustration style, HDR oversaturation, wide-angle distortion, garbled or
nonsensical lettering.
```

**Motion (i2v):**
```
the two children walk slowly away from the camera in step, the heavy canister
swaying gently between them, steam rising from the lid, camera follows at the
same walking pace; single continuous shot, no cut, no camera shake
```

### D3 — Kéo bàn ghép nhóm (beat 班の形)

```
Interior of a Japanese elementary school classroom at lunch time in the early
1970s, children in white short-sleeved shirts and navy shorts or skirts pushing
small wooden desks with metal legs together into facing groups, seen from the
side and from behind at seated height, bright midday sunlight through tall
sliding wooden-framed windows, clean green chalkboard, cloth school bags
hanging on desk hooks, warm polished wooden floor, natural motion blur on the
moving children, photorealistic documentary photograph of everyday life in
1970s Japan (Showa era), classroom in active daily use and well kept, bright
natural midday daylight, crisp clear focus, rich natural colour, warm wood
tones, fresh green foliage outside the windows, soft realistic shadows, faint
haze in the air, shot on a modern full-frame camera with a 35mm lens, calm
observational framing, period-accurate objects and clothing, 16:9.
Avoid: film grain, heavy vignette, faded or washed-out colour, sepia tint, dust
and scratches, abandoned or derelict building, peeling walls, ruins, mould,
horror or eerie mood, empty lifeless space, modern objects, smartphones, LED
lighting, air conditioners, plastic bottles, logo-branded sneakers, anime or
illustration style, HDR oversaturation, wide-angle distortion, garbled or
nonsensical lettering.
```

**Motion (i2v):**
```
desks slide together across the wooden floor as the children lean in and push,
one child sits down on a chair, dust motes drifting in the sunbeams, static
camera with very slight handheld drift; single continuous shot, no cut
```

### D4 — Khay 揚げパン bốc hơi (beat 5 — cận vật, cú đấm hoài niệm) ⭐ HERO

```
Close-up of a school lunch set on a wooden classroom desk: a shallow dented
aluminium tray holding one sugar-and-kinako coated deep-fried bread roll on a
small aluminium plate, a glass milk bottle with a paper cap, an aluminium bowl
of pale cream stew, a pair of aluminium chopsticks, thin steam rising from the
stew, a child's small hand entering from the edge of the frame reaching for the
bread roll, bright window light from the left, shallow depth of field,
photorealistic documentary photograph of everyday life in 1970s Japan (Showa
era), classroom in active daily use and well kept, bright natural midday
daylight, crisp clear focus on the tray, rich natural colour, warm wood tones,
soft realistic shadows, shot on a modern full-frame camera with a 50mm macro
lens, calm observational framing, period-accurate objects, 16:9.
Avoid: film grain, heavy vignette, faded or washed-out colour, sepia tint,
abandoned or derelict building, peeling walls, horror or eerie mood, modern
objects, plastic packaging, printed labels, anime or illustration style, HDR
oversaturation, garbled or nonsensical lettering.
```

**Motion (i2v):**
```
steam rises slowly from the stew, the small hand reaches in and lifts the bread
roll off the plate, static camera, focus stays on the tray; single continuous
shot, no cut
```

### D5 (thêm mới) — Biển hiệu 給食室, TEST chữ Nhật

Cảnh này **chỉ để kiểm tra một câu hỏi**: model có gen được chữ Nhật sạch không. Kết quả quyết định có bỏ được lệnh cấm chữ của v1 hay không.

```
A small hand-painted wooden signboard above a doorway in a Japanese elementary
school, reading 「給食室」 in neat black brush lettering on a pale cream board,
the doorway slightly open with warm steam and light spilling out, stacked
aluminium food canisters visible inside, clean plastered wall with dark wood
trim, camera straight on at adult eye height, photorealistic documentary
photograph of everyday life in 1970s Japan (Showa era), building in active
daily use and well kept, bright natural daylight, crisp clear focus, rich
natural colour, warm wood tones, soft realistic shadows, shot on a modern
full-frame camera with a 35mm lens, 16:9.
Avoid: film grain, faded colour, sepia, abandoned or derelict building, peeling
walls, ruins, horror mood, modern objects, LED lighting, anime style, HDR
oversaturation, garbled or nonsensical lettering, extra text, English text.
```

**Motion (i2v):** `steam drifts out through the half-open doorway, the light inside flickers gently, static camera; no cut`

---

## 5. CÁCH CHẠY LƯỢT THỬ NÀY (đúng thứ tự, đừng nhảy bước)

1. **Flow → Cài đặt tác nhân**: ảnh `Nano Banana 2` · 16:9 · **x4** · video `Veo 3.1 - Fast` · 16:9 · x1. Giữ `Xác nhận trước khi tạo = Luôn luôn` (để thấy giá credit trước khi trừ).
2. Gen ảnh **D1 → D5**, mỗi cảnh **2 lượt x4 = 8 bản**. Câu dẫn cho agent: `Generate 4 images, 16:9, using this prompt EXACTLY as written without rewriting or shortening it: <dán khối trên>`.
3. **DUYỆT MẮT** theo bảng Mục 6 → chọn 1 bản/cảnh. Chưa duyệt thì tuyệt đối không i2v.
4. i2v **ĐÚNG 2 cảnh trước** (D1 + D4) = 40 credit, đặt cạnh clip D1 bản cũ. So xong mới quyết có gen tiếp D2/D3/D5.
5. Ghi kết quả (đạt/rớt từng tiêu chí) xuống Mục 7 file này.

## 6. BẢNG DUYỆT — rớt 1 dòng là loại bản đó

| # | Kiểm | Rớt thì |
|---|---|---|
| 1 | Trường **đang hoạt động**, không bỏ hoang/tường bong | thêm mạnh `in active daily use`, tăng số trẻ trong khung |
| 2 | **Sáng, nét, màu no** — không xám/mốc/sepia | kiểm lại đã xoá hết từ film-decay chưa |
| 3 | Chữ trong khung: **đúng ký tự hoặc không có chữ nào** | gen lại, hoặc rút chữ xuống 2–3 ký, hoặc bỏ biển hiệu |
| 4 | Người: dáng trẻ Nhật thập niên 70 (tóc, áo trắng, giày vải), **không mặt Tây, không anime** | thêm `Japanese children` vào đúng câu tả người |
| 5 | Không vật hiện đại / logo / nhựa | đã có trong Avoid, gen lại |
| 6 | 5 cảnh đặt cạnh nhau **nhìn như một bộ phim** (cùng tông, cùng ánh sáng) | ⚠️ đây là chỗ prompt KHÔNG giải được → phải sang bước đồng bộ màu (Mục 8) |
| 7 | Cảm giác đầu tiên: "phim tư liệu" chứ không "AI demo" | rớt cái này thì rớt cả bộ |

## 7. KẾT QUẢ LƯỢT THỬ (điền sau khi chạy)

| Cảnh | Ảnh đạt/8 | Chữ sạch? | Ghi chú |
|---|---|---|---|
| D1 | | — | |
| D2 | | — | |
| D3 | | — | |
| D4 | | — | |
| D5 | | ⬅️ câu hỏi chính | |

## 8. VIỆC CÒN THIẾU SO VỚI KÊNH MẪU (prompt không giải được)

Kênh mẫu công bố bước ③: gen ảnh → **Photoshop vá chỗ méo** → **Lightroom đồng bộ màu/sáng/contrast từng ảnh**. Đây là lý do 30 cảnh của họ nhìn như một bộ phim còn 4 ảnh của mình mỗi ảnh một tông. **Prompt không thay được bước này.**

Hai đường:
- **ⓐ Tool tự viết** — script ffmpeg/PIL áp một bộ curve+WB+contrast chung cho cả bộ ảnh sau khi chọn (rẻ, tự động, đủ để ép tông). Tao viết được, ~1 lượt.
- **ⓑ Lightroom/Photoshop thật** — chuẩn như họ, nhưng thêm phần mềm + thời gian tay/ảnh.

⛔ Chưa làm gì ở mục này. Chốt hướng rồi làm.

## 9. LIÊN QUAN
- Bản v1 đang khoá (chưa sửa): `04_VIDEOGEN_PROMPTS.md`
- Số đo kênh mẫu + toolchain 8 bước họ công bố: xem lượt chat 2026-08-04 (chưa đúc thành file — nếu chốt đảo format thì viết `05_BENCHMARK_SONZAI.md`)
- Nhịp dựng ≤6 đổi hình/phút (quyết định số clip/video): `.claude/rules/audience-45plus.md` §2
- Watermark Veo trên gói Pro + chi phí credit: lượt chat 2026-08-04
