# THUMBNAIL tập 01 — 「雲の上の一日」 · bộ A/B 3×3

> Luật: `.claude/rules/ab-3title-3thumb.md` (3 title + 3 thumbnail, mỗi bản đổi ĐÚNG 1 biến) ·
> `audience-45plus.md` §1 (gate chữ/mặt) · `media-library.md` §2.10 ⑤b (⛔ **xoá watermark ✦ trước khi giao**)
> File bơm extension: `thumb_prompts_FLOW.txt` (1 prompt/dòng) · tên file: `thumb_prompts_TENFILE.txt`

---

## 1. 3 TITLE A/B — mỗi bản một GIẢ THUYẾT

| | title | ký | giả thuyết thử |
|---|---|---|---|
| **A1** ⭐ dùng khi đăng | `昭和100年　雲の上の町の一日` | 15 | keyword dẫn = **昭和100年** (nhãn thế giới) |
| **A2** | `雲の上に町があったら　昭和100年の暮らし` | 21 | đổi keyword dẫn sang **雲の上** (hình ảnh) |
| **A3** | `セーターが編み上がるまでの、ある一日` | 19 | đổi kiểu hook: bỏ thế giới, **bán câu chuyện** |

⚠️ **Chưa đo Trends.** `youtube-upload-seo.md` §0.5 bắt đo trước khi chốt — kênh chưa có video nên
chưa chạy. **Đo trước khi đăng**, và nếu 雲の上 / 昭和100年 lệch nhau nhiều thì đảo A1/A2.

---

## 2. 3 THUMBNAIL — mỗi bản đổi ĐÚNG MỘT BIẾN

**Chữ giống hệt nhau ở cả 3 bản** (`ab-3title-3thumb.md` §3 mục 6) — biến thử là HÌNH:

| dòng | chữ | vai |
|---|---|---|
| trên | `昭和100年` | ① về cái gì |
| ⭐ hero | `雲の上の町` | ② chuyện gì — dòng to nhất |
| dưới | `そこにも、夕飯がある` | ③ móc cảm xúc |

| | biến đổi | hình |
|---|---|---|
| **T1** baseline | — | **toàn cảnh**: thị trấn trên cột đá, biển mây, cầu treo, hoàng hôn |
| **T2** đổi 1 biến HÌNH | **có NGƯỜI** (giữ nguyên chữ) | mẹ ở lan can, lưng quay, nhìn ra biển mây |
| **T3** đổi LAYOUT | tỉ lệ chữ/ảnh đảo | cận **một ô cửa sáng đèn** trên vách đá, chữ chiếm nửa trái |

⚠️ **Gate `audience-45plus` §1:** hero `雲の上の町` là **5 ký** (trần 6 ✅). Gate 2 (hero ≥1/3 chiều cao)
**dự kiến RỚT** như 18/20 ca đã đo của workspace — đó là dải tự nhiên 20–31% của layout có dòng phụ, không
phải lỗi thi hành. **Duyệt bằng mốc 168px và 120px**, ghi số đo vào `08_ANALYTICS_LOG.md`.

---

## 3. PROMPT — khung khối (bản người đọc; bản bơm ở `_FLOW.txt`)

Cả 3 dùng chung **khối 1–3**, chỉ khác **khối 4 (LAYOUT/HÌNH)**.

### ① REAL + chống anime *(giống prompt clip — cùng bệnh, cùng thuốc)*
```
Live-action photography, a real photograph: real timber with grain, real rock, real cloth, real skin with pores. NOT an illustration, NOT anime, NOT a cartoon, NOT a painting, NOT concept art, NOT a 3D render, NOT CGI; no outlines, no flat colour, no cel shading, no stylised faces.
```

### ② TEXT — đặt trong 15% ĐẦU prompt (`ab-3title-3thumb.md` §3.1 Bước 3)
```
TEXT, exactly these three blocks of Japanese and nothing else, burned into the image, every character correctly formed and crisp:
line 1, white on a narrow deep-navy band across the top: 昭和100年
line 2, LARGEST by far, warm cream with a heavy black outline and white halo, across the middle: 雲の上の町
line 3, smaller, pale yellow on a dark red ribbon low on the left: そこにも、夕飯がある
```

### ③ THẾ GIỚI + ÁNH SÁNG
```
A retro-futuristic Japan of the year Showa 100: weathered timber Showa houses built on terraces cut into enormous natural rock pillars that stand out of a sea of white cloud, long suspension bridges between the pillars, paper lanterns, hand-painted signboards. The rock pillars are rooted in the earth far below the cloud, NOT floating islands, nothing is flying. Everything old but cared for — worn smooth from use, never rusted, never derelict. Deep saturated cobalt sky with pure brilliant white cumulus, crisp-edged and sculpted, the way a summer sky looks on strong colour slide film; ONLY the sky carries that heightened colour, everything below the skyline stays photographic. Soft open light, gentle contrast, nothing glaring.
```

### ④ LAYOUT — khác nhau ở đây
- **T1** `Wide view of the whole town on its rock pillars at golden hour, the sea of cloud lit gold below it, no people, the camera looking slightly down from a neighbouring pillar.`
- **T2** `The mother — a Japanese woman of about forty in a small-flowered apron, her hair in a low bun — stands at a timber handrail seen from behind and slightly to the side, looking out over the lit sea of cloud; she fills the right third of the frame.`
- **T3** `Close on one small square lit window in a timber wall on the rock face at dusk, warm orange inside, a paper lantern beside it, the sea of cloud soft behind; the picture occupies only the right half of the frame and the left half is dark timber where the text sits.`

### ⑤ ĐÓNG — bắt buộc cả 3
```
Keep the very bottom-right corner free of text and of anything important. No watermark, no logo, no signature, no extra text. 16:9, 1280x720.
```

---

## 4. ⚠️ BA VIỆC BẮT BUỘC SAU KHI GEN

1. 🔴 **XOÁ WATERMARK ✦** — `media-library.md` §2.10 ⑤b. Thumbnail **phải VÁ, không được CẮT** (chữ hero
   chạy sát mép). Soi **1:1 cả 4 GÓC**, sheet thu nhỏ cho qua ✦. Ảnh còn ✦ = **chưa xong**.
2. 🔴 **Soi TỪNG KÝ TỰ** của 3 dòng chữ ở cỡ thật. Sai một nét là **loại, gen lại** — kanji rậm 雲/夕 rủi ro nhất.
3. **Duyệt 168px và 120px** (`audience-45plus` §1 gate 5) — ở 120px `雲の上の町` phải là thứ đọc được đầu tiên.

## 5. ĐẶT TÊN
`thumb_T1_zenkei.png` · `thumb_T2_hahaoya.png` · `thumb_T3_mado.png`
→ `upload_pack.py` tự gói thành `thumbnail.*` + `thumbnail_T2.*` + `thumbnail_T3.*`
