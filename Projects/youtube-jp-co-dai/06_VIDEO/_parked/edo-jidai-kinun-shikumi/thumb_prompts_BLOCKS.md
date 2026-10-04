# thumb prompts — 20 (v3) · B1 long K6
Bo chu: 江戸時代の火事 / 小判より紙 (HERO) / 通帳はどこですか / badge 今夜10分

PROMPT ẢNH THUMBNAIL — khuôn **B1 (bright) lồng K6 (Lịch sử × hiện tại)**

**Vì sao K6:** tránh **K1** (#15, #17) · **K4** (#16) · **K3** (#19). K6 lần cuối ở **#07, cách hơn 10 video**. Và K6 (「BACKGROUND sepia lịch sử mờ + FOREGROUND vật hiện đại sắc nét」) **chính là xương sống dịch sang hình**: sổ Edo cháy phía sau, **cuốn sổ ngân hàng của người xem** nét căng phía trước.

> 🔴 Prompt **BAKE CHỮ** (`ab-3title-3thumb.md` §3 mục 8 + §3.1): khối `TEXT` ở **15% đầu**, mỗi dòng một dòng riêng, ≤4 dòng, chừa **góc dưới–PHẢI** (timestamp) và **góc trên–PHẢI** (brand plate).
> 📄 4 file: `06_VIDEO/20_edo-jidai-kinun-shikumi/thumb_prompts_{FLOW.txt,BLOCKS.md,TENFILE.txt,PLATE.txt}`

**T1 — baseline khuôn kênh (B1+K6)**
```
Photorealistic 16:9 thumbnail, bright high-key lighting, bold Japanese text burned into the image.

TEXT, exactly these 4 blocks and nothing else:
line 1, small, warm yellow with black outline: 江戸時代の火事
line 2, LARGEST block, spanning about two-thirds of the frame width, white with a thick black outline and white halo: 小判より紙
line 3, medium, on a slim dark red ribbon: 通帳はどこですか
badge, bottom-LEFT corner, amber rounded plate, dark text: 今夜10分

LAYOUT: line 1 across the upper-left; line 2 centred in the middle band, the tallest AND widest element; line 3 on a red ribbon just below it; badge in the lower-left. Keep the upper-right corner completely empty.
BACKGROUND: faded sepia Edo-period merchant street at night, a warm orange glow and thin drifting smoke far in the distance, softly blurred, aged paper texture, airy and low contrast, no visible flames, no people.
FOREGROUND: on a pale wooden table, a modern Japanese bank passbook lying open beside a small stack of gold koban coins that are being left behind, the passbook lit brightly and razor sharp while the coins fall into shadow, lower-right third.
NO people, no faces, no brand logos, no characters written on the passbook pages.

Text must be perfectly formed Japanese characters, crisp and legible. Keep the very bottom-right corner free of text. No watermark, no logo, no signature, no additional text. --ar 16:9
```

**T2 — đổi ĐÚNG 1 biến hình (nền), chữ GIỮ NGUYÊN**
```
Photorealistic 16:9 thumbnail, bright high-key lighting, bold Japanese text burned into the image.

TEXT, exactly these 4 blocks and nothing else:
line 1, small, warm yellow with black outline: 江戸時代の火事
line 2, LARGEST block, spanning about two-thirds of the frame width, white with a thick black outline and white halo: 小判より紙
line 3, medium, on a slim dark red ribbon: 通帳はどこですか
badge, bottom-LEFT corner, amber rounded plate, dark text: 今夜10分

LAYOUT: line 1 upper-left, line 2 the tallest and widest element in the middle band, line 3 on a red ribbon below it, badge lower-left. Keep the upper-right corner completely empty.
BACKGROUND: plain bright off-white studio wall, evenly lit, no texture, no shadows, no fire.
FOREGROUND: the same modern Japanese bank passbook lying open on a pale wooden table beside a small stack of gold koban coins, the passbook brightly lit and razor sharp, the coins duller, lower-right third.
NO people, no faces, no brand logos, no characters written on the passbook pages.

Text must be perfectly formed Japanese characters, crisp and legible. Keep the very bottom-right corner free of text. No watermark, no logo, no signature, no additional text. --ar 16:9
```

**T3 — đổi LAYOUT (panel chữ nửa trái, ảnh nửa phải)**
```
Photorealistic 16:9 thumbnail, bright high-key lighting, bold Japanese text burned into the image.

TEXT, exactly these 4 blocks and nothing else:
line 1, small, warm yellow with black outline: 江戸時代の火事
line 2, LARGEST block, filling the left half of the frame from edge to centre, white with a thick black outline and white halo: 小判より紙
line 3, medium, on a slim dark red ribbon directly beneath line 2: 通帳はどこですか
badge, bottom-LEFT corner, amber rounded plate, dark text: 今夜10分

LAYOUT: the entire left half is a text panel over plain bright background — line 1, then line 2 as the dominant element, then line 3 on a red ribbon, badge tucked into the lower-left. The right half carries the photograph. Keep the upper-right corner completely empty.
BACKGROUND: bright pale plaster wall with a faint sepia Edo street ghosted into it, very low contrast, no fire.
FOREGROUND: on the right half, an old stone well rim seen from above with a thick hand-bound Japanese ledger resting on it, and a modern bank passbook lying beside it, both in full colour and sharp focus, cropped by the bottom edge, warm daylight.
NO people, no faces, no brand logos, no characters written on the ledger or passbook pages.

Text must be perfectly formed Japanese characters, crisp and legible. Keep the very bottom-right corner free of text. No watermark, no logo, no signature, no additional text. --ar 16:9
```

**Đường lui — 3 plate KHÔNG chữ** để riêng ở `thumb_prompts_PLATE.txt`. ⛔ Đừng dán chung `FLOW.txt`.

**Sau khi gen:** ① soi TỪNG ký tự (kanji rậm: 戸・判・帳) ② quét & **cắt** watermark ✦ — đo lại vị trí theo đúng lô (`media-library.md` §2.10⑤) ③ `python tools\stamp_brand.py <thumb>.jpg -o <thumb_final>.jpg --preview` ④ duyệt 3 cửa + 168px/120px ⑤ đặt tên `thumb_T1_*.png` / `thumb_T2_*.png` / `thumb_T3_*.png`.

---
