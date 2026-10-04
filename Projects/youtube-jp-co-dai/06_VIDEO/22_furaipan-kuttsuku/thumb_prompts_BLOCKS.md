# Thumbnail video 22 — フライパン · khuôn **B1 (bright) lồng K1 (arrow)**

> Bản NGƯỜI ĐỌC. Bản để bơm vào extension là `thumb_prompts_FLOW.txt` (mỗi prompt 1 dòng, **cùng nội dung, cùng thứ tự khối**).
> Luật: `.claude/rules/ab-3title-3thumb.md` §3 mục 8 + §3.1 · khuôn kênh: `02_THUMBNAIL_PROMPTS.md` (B1 · K1) · badge/brand: `tools/stamp_brand.py`.

## Bảng chữ (GIỐNG NHAU ở cả 3 bản — biến thử là HÌNH)

| khối | chữ | màu | vai |
|---|---|---|---|
| dòng phụ trên | `くっつくフライパン` | vàng `#FFD200`, viền đen | ① VỀ CÁI GÌ (keyword đo được cao nhất) |
| **HERO** | `10分で戻る` | trắng, viền đen dày + halo | ② CHUYỆN GÌ XẢY RA + con số — **TO NHẤT, rộng ~2/3 khung** |
| dải đỏ đáy | `油は敷くな` | trắng trên dải đỏ `#E03A3A` | ③ PHẢI LÀM GÌ (đảo thói quen) |
| badge góc dưới–TRÁI | `3000円` | chữ ink trên khối amber | số tiền theo khuôn B1 |

⛔ Góc dưới–PHẢI để trống (YouTube đóng timestamp) · góc trên–PHẢI để trống (dấu kênh `stamp_brand.py` sẽ đè sau).

## Bảng số đo (đo từ thumbnail đã lên sóng của kênh — B1)

| khối | tỉ lệ |
|---|---|
| HERO | rộng **~2/3 bề ngang khung**, cao ~28–30% |
| dòng phụ trên | ~18% chiều cao, đặt ngay trên HERO |
| dải đỏ | ~20% chiều cao, sát đáy nhưng chừa lề |
| chủ thể (chảo) | chiếm ~1/3 khung, lệch phải (T1/T2) hoặc giữa (T3) |

## Khung khối — T1 (baseline B1 + K1 arrow)

```
16:9 bright high-key photograph, Japanese kitchen, bold Japanese text burned into the image.

TEXT, exactly these 3 blocks and nothing else:
top line, yellow with black outline: くっつくフライパン
hero line, white with thick black outline, LARGEST and WIDEST: 10分で戻る
bottom red banner, white text: 油は敷くな

LAYOUT: hero line spans about two thirds of the frame width, sitting in the middle band;
yellow line directly above it; red banner across the lower area, leaving the very bottom-right corner empty.
BACKGROUND: sunlit bright kitchen counter, white tiles, crisp daylight, flat, no shadows.
LEFT: an old dull cast-iron frying pan, greyish and patchy, food stuck to it.
RIGHT: the same pan restored, deep black, glossy, light reflecting off the smooth surface.
BETWEEN THEM: one thick curved red arrow pointing from the dull pan to the glossy pan.
BOTTOM-LEFT: a small amber tag reading 3000円, no other characters written anywhere.

Text must be perfectly formed Japanese characters, crisp and legible.
Keep the very bottom-right corner and the top-right corner free of text.
No watermark, no logo, no signature, no additional text, no people, no faces. --ar 16:9
```

## Khung khối — T2 (đổi ĐÚNG 1 biến hình: cảnh macro giọt nước — chữ giữ nguyên)

```
16:9 bright high-key macro photograph, bold Japanese text burned into the image.

TEXT, exactly these 3 blocks and nothing else:
top line, yellow with black outline: くっつくフライパン
hero line, white with thick black outline, LARGEST and WIDEST: 10分で戻る
bottom red banner, white text: 油は敷くな

LAYOUT: hero line spans about two thirds of the frame width in the middle band;
yellow line directly above it; red banner across the lower area, bottom-right corner empty.
BACKGROUND: the dark glossy surface of a hot cast-iron pan filling the frame, bright kitchen light above.
SUBJECT: a single round water droplet beading up and rolling on the hot surface, sharp focus, tiny wisp of steam.
COLOR: warm daylight, high contrast between the silver droplet and the black iron.
BOTTOM-LEFT: a small amber tag reading 3000円, no other characters written anywhere.

Text must be perfectly formed Japanese characters, crisp and legible.
Keep the very bottom-right corner and the top-right corner free of text.
No watermark, no logo, no signature, no additional text, no people, no faces. --ar 16:9
```

## Khung khối — T3 (đổi LAYOUT: một chảo nhìn từ trên, chữ dồn cột trái)

```
16:9 bright high-key overhead photograph, bold Japanese text burned into the image.

TEXT, exactly these 3 blocks and nothing else, stacked in the LEFT third:
top line, yellow with black outline: くっつくフライパン
hero line, white with thick black outline, LARGEST: 10分で戻る
bottom red banner, white text: 油は敷くな

LAYOUT: all three text blocks stacked in the left third of the frame, hero line largest;
the pan occupies the right two thirds, bottom-right corner free of text.
BACKGROUND: pale wooden kitchen table, bright even daylight, flat, no shadows.
SUBJECT: one cast-iron frying pan seen straight from above, half of its surface dull and patchy,
the other half deep black and glossy, the boundary running down the middle of the pan.
DETAIL: a folded paper towel and a spoonful of oil resting beside the pan.
BOTTOM-LEFT: a small amber tag reading 3000円, no other characters written anywhere.

Text must be perfectly formed Japanese characters, crisp and legible.
Keep the very bottom-right corner and the top-right corner free of text.
No watermark, no logo, no signature, no additional text, no people, no faces. --ar 16:9
```

## Sau khi gen — quy trình bắt buộc

1. **Soi TỪNG ký tự** chữ Nhật (`くっつくフライパン` · `10分で戻る` · `油は敷くな` · `3000円`). Sai một nét = **loại, gen lại** — đừng cứu.
2. **Xoá watermark ✦** — thumbnail bake chữ ⇒ **VÁ, KHÔNG cắt** (`media-library.md` §2.10⑤b, tool `youtube-jp-shokutaku/tools/strip_wm_thumb.py`). Soi **1:1 cả 4 góc**, không dùng sheet thu nhỏ.
3. `python tools\stamp_brand.py <thumb>.jpg -o thumb_T1_furaipan.jpg --preview` (dấu kênh góc trên–phải).
4. Đặt tên `thumb_T1_*.png|jpg` · `thumb_T2_*` · `thumb_T3_*` trong chính thư mục này (gate 3×3 của `upload_pack.py` đọc theo tên).
5. Duyệt 3 cửa: che chữ → có ra chủ đề không · đặt cạnh `01_hosan-shiroari/thumbnail_v3_final.jpg` → có cùng "kiểu" kênh không · **168px và 120px** → đọc được HERO không.
