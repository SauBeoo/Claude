# THUMBNAIL v6 — làm lại 10 video live của 60代からの食卓 (soạn 2026-08-05)

> Phạm vi user chốt: **video 01–10, CHỪA 11 麦茶 + 12 ヨーグルト**. Hai bản chừa lại chính là 2 bản đo tốt nhất kênh và là **KHUÔN CHUẨN** mà 10 bản mới phải đồng bộ theo.
> Cách làm user chốt: **Claude viết prompt → user gen AI → Claude làm sạch + đóng dấu + đo gate + đẩy.**
> ⚠️ Đọc trước: `CLAUDE.md` §CHIẾN LƯỢC ghi rõ **thumbnail KHÔNG phải bệnh đo được của kênh này** (`BROWSE = 0` là cấp kênh; bệnh là nửa khán giả bỏ đi trước giây 45). Đợt này làm vì 3 lý do khác: **3 video rớt gate đọc được**, **9/12 video thiếu dấu nhận diện**, và chưa có bộ A/B 3×3.

## 0. ĐO BẢN LIVE — vì sao 10 video này phải làm lại

| # | món | dòng chính | sáng TB | phán |
|---|---|---|---|---|
| 04 | 牛乳 | **13,6%** | **38** (gần như đen) | 🔴 rớt nặng nhất — ở 168px không đọc được gì |
| 06 | トマトジュース | **16,7%** | 72 | 🔴 rớt |
| 05 | 納豆 | **19,4%** | 47 | 🔴 rớt |
| 08 | 緑茶 | 20,7% | 88 | 🟡 sát ngưỡng |
| 10 | キャベツ | 23,1% | 147 | 🟡 chữ nhỏ (nền sáng thì tốt) |
| 07 | あずき | 30,7% | 107 | ✅ chỉ thiếu dấu |
| 09 | はちみつ | 37,5% | 96 | ✅ nhưng **38 mảnh chữ** = rối |
| 03 | 腎臓 | 39,7% | 100 | ✅ chỉ thiếu dấu |
| 02 | ブルーベリー | 41,4% | **48** rất tối | 🟡 |
| 01 | ゆで卵 | 48,6% | 72 tối | 🟡 |
| *11* | *麦茶* | *50,3%* | *98* | *KHUÔN CHUẨN — chừa* |
| *12* | *ヨーグルト* | *37,5%* | *173* | *KHUÔN CHUẨN — chừa* |

**6/12 video nền tối (sáng TB <90)** — mà chính `02_THUMBNAIL_TITLE_RULES.md` **v5 (2026-07-21)** đã hạ khuôn "FULL-BLEED tối moody" xuống làm biến thể phụ (*"đẹp nhưng thua meta rail"*), và `audience-45plus.md` §1 gate 6 đòi nền sáng. Tức 6 video đang chạy khuôn mà chính kênh đã khai tử.

## 1. KHUÔN KHOÁ — đo từ 2 bản chuẩn, khớp nhau từng thông số

| yếu tố | spec | đo ở |
|---|---|---|
| dải vàng mép **TRÁI** | rộng **1,41% bề ngang** (18px/1280), màu **#FFDE00**, hết chiều cao | có ở CẢ 11 và 12 |
| badge tròn **食卓** | đỏ **#FF3D31**, chữ trắng, **đường kính 25,7% chiều cao** (185px/720), lề ~1,5–3% | cả 11 và 12 |
| vị trí badge | **góc ĐỐI DIỆN cột chữ** (11: chữ phải → badge dưới-trái · 12: chữ trái → badge trên-phải) | — |
| cột chữ | **3 dòng 袋文字 viền đen dày**, xếp dọc một bên, dòng 2 TO NHẤT | cả 2 |
| màu chữ | dòng 1 **trắng** · dòng 2 **đỏ hoặc vàng, cực to** · dòng 3 màu còn lại | cả 2 |
| ảnh | **SÁNG**, 1 chủ thể (món macro hoặc 1 mặt biểu cảm), chiếm nửa đối diện cột chữ | cả 2 |
| cấm | ✗/○, mũi tên, chia đôi khung, collage, nhãn hiệu đọc được | — |

🔴 **Dải vàng + badge 食卓 KHÔNG bake bằng AI** — nhận diện chỉ có giá trị khi giống từng pixel qua mọi video, AI mỗi lần vẽ một kiểu. Tool đóng dấu: **`tools/stamp_brand_shokutaku.py --corner tr|tl|br|bl`** (spec khoá cứng trong file, đã verify ra đúng 185px = 25,7%). Cùng nguyên tắc dấu 「秘」 của co-dai.

## 2. PROMPT MẪU — ĐÃ THAY BẰNG MỤC 2b

> ⛔ Khối mẫu có chỗ trống `[...]` đã **bỏ** (2026-08-05). Nó có **10 token khác nhau / 11 lần
> xuất hiện**, mà tao lại mô tả là "thay 4 chỗ" (đếm *loại thông tin*, không phải đếm cái nhìn
> thấy) → dễ dán thiếu một token mà không ai phát hiện. **Dùng Mục 2b: 10 khối đã điền sẵn.**

## 2b. ⭐ 10 PROMPT ĐÃ ĐIỀN SẴN — copy nguyên khối, KHÔNG phải thay gì

> Sửa 2026-08-05: mục 2 ghi "thay 4 chỗ" là **SAI** — khối mẫu có **10 token khác nhau / 11 lần xuất hiện**
> (`[SCENE] [MÓN] [SIDE_IMG] [SIDE_TEXT]×2 [C2] [C3] [L1] [L2] [L3] [CORNER]`), đếm bằng máy.
> "4 chỗ" là đếm *loại thông tin*, không phải đếm cái nhìn thấy trong khối → dễ dán thiếu.
> Nên bỏ hẳn việc thay chỗ trống: dưới đây là 10 khối đã điền, mỗi video một khối.

### 01 ゆで卵 — `mQevRS1qBbk` · badge `--corner tr`

```
Bright high-key food photograph, 16:9. Sunlit Japanese kitchen or dining table, warm
natural daylight from a window, pale wood and light surfaces — the whole frame reads bright
and clean, never moody, never dark.

ONE SINGLE SUBJECT: halved boiled eggs with glossy yolks in a small ceramic dish. It sits on the right side of the frame, sharply focused,
appetising, filling roughly half the width. Everything else is soft and out of focus. No
hands, no people faces, no props competing for attention, no readable labels, no brand
names, no text on any packaging.

The left side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the left side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  そのゆで卵
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  半分ムダ
  line 3, bright yellow, medium ..........................  原因はコレ

Keep the top-right corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 02 ブルーベリー — `31KXwgHbLY0` · badge `--corner bl`

```
Bright high-key food photograph, 16:9. Sunlit Japanese kitchen or dining table, warm
natural daylight from a window, pale wood and light surfaces — the whole frame reads bright
and clean, never moody, never dark.

ONE SINGLE SUBJECT: a white bowl of fresh blueberries with a few frosted frozen ones beside it. It sits on the left side of the frame, sharply focused,
appetising, filling roughly half the width. Everything else is soft and out of focus. No
hands, no people faces, no props competing for attention, no readable labels, no brand
names, no text on any packaging.

The right side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the right side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  凍ったまま？
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  恵み半分
  line 3, bright yellow, medium ..........................  正解はコレ

Keep the bottom-left corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 03 腎臓・野菜 — `BKh-sdhsNUg` · badge `--corner tr`


> ⭐ **SỬA 2026-08-05 vòng 2 (user: "liên quan đến thận thì có hình ảnh thận chứ").** Bản đầu tao chỉ để rau —
> **sai luật đã có của kênh**: `CLAUDE.md` §Thumbnail bước 0 「ý chính vào HÌNH」 = video về tạng thì **hình phải có tạng**,
> mô hình THẬT ghép chìm vào cảnh, **cấm sticker/illustration/collage** (memory `feedback_thumbnail_organ_topic_phai_co_tang`).
> Bản live #03 vốn ĐÃ có hình thận → prompt cũ là bước thụt lùi. Điều duy nhất bỏ khỏi luật cũ: chữ 「cảnh moody」 —
> v5 + `audience-45plus.md` đòi nền SÁNG, nên giữ 「mô hình thật, chìm vào cảnh, một ảnh liền」 nhưng đổi sang high-key.
> Thêm chặn gore: mô hình y khoa sạch, KHÔNG được ra thịt sống/máu (né advertiser-friendly + tệp 60–80).

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen counter, warm natural daylight
from a window, pale wood and light surfaces — the whole frame reads bright and clean, never
moody, never dark.

ONE SINGLE SUBJECT, on the right side of the frame: a realistic anatomical model of a human
kidney — a clean medical teaching model in smooth matte material, bean-shaped, natural
muted red-brown tones, one half cut open to show the inner structure. It stands upright on
the counter, sharply focused, lit by the same daylight as the rest of the scene so it looks
photographed in place, not pasted in. It fills roughly one third of the frame.

Arranged low around its base, smaller and slightly out of focus: fresh vegetables —
cucumber, a wedge of cabbage, a tomato. They frame the model without competing with it.

IMPORTANT on the model: it must read as a clean educational anatomy model, NOT as raw meat,
NOT bloody, NOT wet, no gore, nothing surgical. One seamless photograph — no cut-out edges,
no sticker, no cartoon or illustrated organ, no collage, no panel, no drop shadow around it.

The left side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the left side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  体にいいのに
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  腎臓が疲れる
  line 3, bright yellow, medium ..................  5つの食べ物

Keep the top-right corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 04 牛乳 — `DD_AED6woII` · badge `--corner bl`


> ⭐ **SỬA 2026-08-05 vòng 2 — áp luật organ-topic của prompt 03** (user: *"sửa những cái đó theo prompt 03 mới nhất"*).
> `CLAUDE.md` §Thumbnail bước 0 「ý chính vào HÌNH」: nói về tạng thì hình phải CÓ tạng, mô hình THẬT, một ảnh liền.
> 🔑 **Cách tránh 2 tiêu điểm** (bệnh vừa dọn ở co-dai): món và mô hình phải nằm **CÙNG MỘT CHÙM** — sát nhau, cùng
> vũng sáng, cùng độ sâu, món ở trước và nét hơn. Cấm đặt hai thứ ở hai nửa khung đối diện.

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen counter, warm natural daylight
from a window, pale wood and light surfaces — the whole frame reads bright and clean, never
moody, never dark.

ONE SINGLE CLUSTER on the left side of the frame — the food and the anatomy model stand
together, touching, in the same pool of daylight, at the same depth. They must read as one
subject, never as two separate objects in opposite halves of the picture.

  · FORWARD and sharpest: a tall glass of cold milk with condensation running down the glass.
  · DIRECTLY BEHIND, clearly visible and slightly smaller: a realistic anatomical model of a
    cross-sectioned human bone, dry ivory-white matte material, the cut face showing the
    porous honeycomb inner structure. A clean educational model, lit by the same daylight as
    the milk so it looks photographed in place, not pasted in.

IMPORTANT on the anatomy model: it must read as a clean educational teaching model, NOT as
raw meat, NOT bloody, NOT wet, no gore, nothing surgical. One seamless photograph — no
cut-out edges, no sticker, no cartoon or illustrated organ, no collage, no panel, no drop
shadow around it.

The right side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the right side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  毎朝の牛乳
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  骨に裏目！?
  line 3, bright yellow, medium ..................  見直す3つ

Keep the bottom-left corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 05 納豆 — `BL7KtdXpl_A` · badge `--corner tr`


> ⭐ **SỬA 2026-08-05 vòng 2 — áp luật organ-topic của prompt 03** (user: *"sửa những cái đó theo prompt 03 mới nhất"*).
> `CLAUDE.md` §Thumbnail bước 0 「ý chính vào HÌNH」: nói về tạng thì hình phải CÓ tạng, mô hình THẬT, một ảnh liền.
> 🔑 **Cách tránh 2 tiêu điểm** (bệnh vừa dọn ở co-dai): món và mô hình phải nằm **CÙNG MỘT CHÙM** — sát nhau, cùng
> vũng sáng, cùng độ sâu, món ở trước và nét hơn. Cấm đặt hai thứ ở hai nửa khung đối diện.

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen counter, warm natural daylight
from a window, pale wood and light surfaces — the whole frame reads bright and clean, never
moody, never dark.

ONE SINGLE CLUSTER on the right side of the frame — the food and the anatomy model stand
together, touching, in the same pool of daylight, at the same depth. They must read as one
subject, never as two separate objects in opposite halves of the picture.

  · FORWARD and sharpest: a bowl of natto topped with chopped spring onion, with a banana
    and half an avocado resting beside it.
  · DIRECTLY BEHIND, clearly visible and slightly smaller: a realistic anatomical model of a
    human kidney — a clean medical teaching model in smooth matte material, bean-shaped,
    natural muted red-brown tones, one half cut open to show the inner structure. Lit by the
    same daylight as the food so it looks photographed in place, not pasted in.

IMPORTANT on the anatomy model: it must read as a clean educational teaching model, NOT as
raw meat, NOT bloody, NOT wet, no gore, nothing surgical. One seamless photograph — no
cut-out edges, no sticker, no cartoon or illustrated organ, no collage, no panel, no drop
shadow around it.

The left side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the left side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  納豆と一緒
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  腎臓に負担
  line 3, bright yellow, medium ..................  7つの組合せ

Keep the top-right corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 06 トマトジュース — `dabD8WcvXu8` · badge `--corner bl`

```
Bright high-key food photograph, 16:9. Sunlit Japanese kitchen or dining table, warm
natural daylight from a window, pale wood and light surfaces — the whole frame reads bright
and clean, never moody, never dark.

ONE SINGLE SUBJECT: a tall glass of tomato juice, with a plain unlabelled bottle blurred behind. It sits on the left side of the frame, sharply focused,
appetising, filling roughly half the width. Everything else is soft and out of focus. No
hands, no people faces, no props competing for attention, no readable labels, no brand
names, no text on any packaging.

The right side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the right side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  毎朝の一杯
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  食塩入り！?
  line 3, bright yellow, medium ..........................  ラベル一行

Keep the bottom-left corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 07 あずき — `utNRgxBSf-8` · badge `--corner tr`

```
Bright high-key food photograph, 16:9. Sunlit Japanese kitchen or dining table, warm
natural daylight from a window, pale wood and light surfaces — the whole frame reads bright
and clean, never moody, never dark.

ONE SINGLE SUBJECT: a rustic bowl heaped with cooked azuki beans and a wooden spoon. It sits on the right side of the frame, sharply focused,
appetising, filling roughly half the width. Everything else is soft and out of focus. No
hands, no people faces, no props competing for attention, no readable labels, no brand
names, no text on any packaging.

The left side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the left side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  あずき一さじ
  line 2, bright yellow, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  体が変わる
  line 3, bright red, medium ..........................  6つの変化

Keep the top-right corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 08 緑茶 — `ySxrtSzj8Bg` · badge `--corner bl`

```
Bright high-key food photograph, 16:9. Sunlit Japanese kitchen or dining table, warm
natural daylight from a window, pale wood and light surfaces — the whole frame reads bright
and clean, never moody, never dark.

ONE SINGLE SUBJECT: a Japanese teacup of bright green tea beside a small kyusu teapot. It sits on the left side of the frame, sharply focused,
appetising, filling roughly half the width. Everything else is soft and out of focus. No
hands, no people faces, no props competing for attention, no readable labels, no brand
names, no text on any packaging.

The right side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the right side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  毎日の緑茶
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  半分ムダ
  line 3, bright yellow, medium ..........................  NGは4つ

Keep the bottom-left corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 09 はちみつ — `LvBPBN1Jg4U` · badge `--corner tr`

```
Bright high-key food photograph, 16:9. Sunlit Japanese kitchen or dining table, warm
natural daylight from a window, pale wood and light surfaces — the whole frame reads bright
and clean, never moody, never dark.

ONE SINGLE SUBJECT: a glass jar of golden honey with a wooden dipper lifting a thread of honey. It sits on the right side of the frame, sharply focused,
appetising, filling roughly half the width. Everything else is soft and out of focus. No
hands, no people faces, no props competing for attention, no readable labels, no brand
names, no text on any packaging.

The left side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the left side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  はちみつに
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  働き半分
  line 3, bright yellow, medium ..........................  避ける3つ

Keep the top-right corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

### 10 キャベツ — `Iazj6ey7gyI` · badge `--corner bl`

```
Bright high-key food photograph, 16:9. Sunlit Japanese kitchen or dining table, warm
natural daylight from a window, pale wood and light surfaces — the whole frame reads bright
and clean, never moody, never dark.

ONE SINGLE SUBJECT: a half cabbage with its cut face toward the camera showing the layers, on a bright cutting board. It sits on the left side of the frame, sharply focused,
appetising, filling roughly half the width. Everything else is soft and out of focus. No
hands, no people faces, no props competing for attention, no readable labels, no brand
names, no text on any packaging.

The right side of the frame is a calm, uncluttered, evenly lit area with no important
detail — the text column goes there.

TEXT baked in on the right side, three lines stacked, heavy rounded Japanese gothic, each
line 袋文字 with a thick black outline and a soft drop shadow. The three lines together fill
about 80% of the frame height:
  line 1, WHITE, smaller ........................  茹でてる？
  line 2, bright red, THE BIGGEST — glyph height at least one third of the frame
  height, it should feel almost too big .........  4割 逃げる
  line 3, bright yellow, medium ..........................  正解はコレ

Keep the bottom-left corner free of important detail — no text there and no key part of the
subject — a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do
NOT draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no arrows, no icons, no split screen, no
watermark.
```

## 2c. KHUÔN **v6b SINH ĐỘNG** — 9 prompt còn lại (soạn 2026-08-05, sau khi user gen video 04)

> user: *"cho tao cái prompt nó sinh động như này đi. Có cả hiệu ứng nhưng ít thôi nhé không nó sẽ rối mắt"*.
> **Bản mẫu = video 04 user đã gen** (`06_VIDEO/_thumb_v6/src/04_src.jpg`): ly sữa + mô hình xương + hạt Ca²⁺ phát sáng + **BẢNG ĐEN** đặt chữ.

**Đo bản mẫu ở 120px — cái gì sống, cái gì chết:**

| yếu tố | ở 120px |
|---|---|
| 3 dòng chữ trên **bảng đen** | **đọc rõ cả 3** — dù dòng vàng chỉ **19,5%** khung |
| ly sữa + mô hình xương | nhận ra được ✓ |
| hạt `Ca²⁺` | còn đốm sáng, **chữ Ca²⁺ mất hẳn** → hết là thông tin |
| dải icon **① ② ③** | **một vệt xám nhòe** = đúng chỗ rối mắt, lại lặp thông tin của chữ 「見直す3つ」 |
| sáng TB | **154** — sáng, đạt gate nền sáng ✓ |

⭐ **Phát hiện đưa thành khuôn: thứ làm chữ đọc được ở 120px là TẤM BẢNG ĐEN, không phải cỡ chữ.**
Chữ trên bảng đen thắng cả những bản chữ to hơn nhưng đặt trực tiếp lên ảnh (01 ゆで卵 dòng chính
48,6% mà vẫn khó đọc vì nền lẫn). Nên v6b khoá bảng đen làm vùng chữ cố định.

**Định mức hiệu ứng — khoá bằng SỐ, không nói "ít thôi"** (nói bằng lời thì mỗi lần gen một kiểu):
đúng **1 hệ hiệu ứng** · **5–7 hạt** · mỗi hạt **≥3% chiều cao khung** (sống được ở 120px) ·
**1 đường duy nhất** · chỉ **hạt to nhất** được mang chữ · **cấm** dải icon ①②③, sơ đồ nhỏ,
badge phụ, mũi tên, tia sáng, sparkle, motion-blur.

**Hiệu ứng phải MANG NGHĨA của bài, không trang trí** — mỗi video một cơ chế: mất chất bay đi
(01·02·08·09·10) · chất chảy VÀO tạng (03) · gánh nặng đọng lại trên tạng (05) · muối rơi vào ly
(06) · chất toả ra (07).

⚠️ **Video 04 GIỮ NGUYÊN, không gen lại** — nó tốt, chỉ dải icon là thừa; đừng lặp dải icon đó ở
9 bản còn lại.


### 01 ゆで卵 — `mQevRS1qBbk` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the left side of the frame:
    halved boiled eggs with glossy yolks in a small ceramic dish
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the right side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single gentle arc of 5 to 7 soft glowing warm-white spheres drifting UP AND AWAY from the eggs and out of the frame - the nutrition being lost
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  そのゆで卵
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   半分ムダ
  line 3, BRIGHT YELLOW with a black outline ....  原因はコレ

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 02 ブルーベリー — `31KXwgHbLY0` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the left side of the frame:
    a white bowl of fresh blueberries with a few frosted frozen ones beside it
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the right side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single gentle arc of 5 to 7 soft glowing deep-violet spheres drifting UP AND AWAY from the frozen berries and out of the frame - the goodness escaping
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  凍ったまま？
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   恵み半分
  line 3, BRIGHT YELLOW with a black outline ....  正解はコレ

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 03 腎臓・野菜 — `BKh-sdhsNUg` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the right side of the frame:
    a realistic anatomical model of a human kidney (clean matte medical teaching model, bean-shaped, muted red-brown, one half cut open to show the inner structure) standing upright, with fresh cucumber, a cabbage wedge and a tomato low around its base
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the left side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single gentle arc of 5 to 7 soft glowing pale-green spheres travelling FROM the vegetables INTO the kidney model - support flowing in
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  体にいいのに
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   腎臓が疲れる
  line 3, BRIGHT YELLOW with a black outline ....  5つの食べ物

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 05 納豆 — `BL7KtdXpl_A` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the right side of the frame:
    a bowl of natto topped with chopped spring onion, a banana and half an avocado beside it, and directly behind them a realistic anatomical model of a human kidney (clean matte medical teaching model, bean-shaped, muted red-brown, one half cut open)
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the left side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single gentle arc of 5 to 7 soft glowing amber spheres travelling FROM the food and SETTLING ON the kidney model, the ones nearest the kidney slightly larger - a burden piling up
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  納豆と一緒
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   腎臓に負担
  line 3, BRIGHT YELLOW with a black outline ....  7つの組合せ

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 06 トマトジュース — `dabD8WcvXu8` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the left side of the frame:
    a tall glass of tomato juice with a plain unlabelled bottle blurred behind it
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the right side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single narrow stream of 6 or 7 small bright-white salt crystals falling from above INTO the glass, catching the light - salt being added without you noticing
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  毎朝の一杯
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   食塩入り！?
  line 3, BRIGHT YELLOW with a black outline ....  ラベル一行

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 07 あずき — `utNRgxBSf-8` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the left side of the frame:
    a rustic bowl heaped with cooked azuki beans with a wooden spoon
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the right side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single gentle arc of 5 to 7 soft glowing warm-gold spheres rising FROM the bowl and spreading outward - goodness being released
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  あずき一さじ
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   体が変わる
  line 3, BRIGHT YELLOW with a black outline ....  6つの変化

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 08 緑茶 — `ySxrtSzj8Bg` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the left side of the frame:
    a Japanese teacup of bright green tea beside a small kyusu teapot
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the right side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single wisp of steam rising from the cup carrying 5 to 7 soft glowing pale-green spheres UP AND AWAY out of the frame - the benefit escaping with the heat
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  毎日の緑茶
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   半分ムダ
  line 3, BRIGHT YELLOW with a black outline ....  NGは4つ

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 09 はちみつ — `LvBPBN1Jg4U` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the left side of the frame:
    a glass jar of golden honey with a wooden dipper lifting a thread of honey
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the right side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single gentle arc of 5 to 7 soft glowing warm-amber spheres rising from the honey thread, the highest ones fading out - the goodness weakening
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  はちみつに
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   働き半分
  line 3, BRIGHT YELLOW with a black outline ....  避ける3つ

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

### 10 キャベツ — `Iazj6ey7gyI` · badge `--corner tr`

```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the left side of the frame:
    a half cabbage with its cut face toward the camera showing the layers, on a bright cutting board
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the right side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    a single wisp of steam rising from the cut face carrying 5 to 7 soft glowing pale-yellow spheres UP AND AWAY out of the frame - the vitamin C boiling off
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  茹でてる？
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   4割 逃げる
  line 3, BRIGHT YELLOW with a black outline ....  正解はコレ

Keep the top-right corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory.
```

## 3. BẢNG 10 VIDEO — thay vào 4 chỗ trong prompt mẫu

Bố cục **so le** giữa các video liền nhau (chữ trái ↔ chữ phải) để không thành "12 video giống hệt nhau chỉ khác tiêu đề" (`youtube-compliance.md` §1), trong khi dải vàng + badge giữ nhận diện.

| # | videoId | MÓN + SCENE | SIDE_TEXT / SIDE_IMG / CORNER | L1 (trắng) | L2 (to nhất) | L3 |
|---|---|---|---|---|---|---|
| 01 | `mQevRS1qBbk` | halved boiled eggs, glossy yolks, in a small ceramic dish on a bright wooden table | left / right / **tr** | `そのゆで卵` | `半分ムダ` 🔴đỏ | `原因はコレ` 🟡vàng |
| 02 | `31KXwgHbLY0` | a white bowl of fresh blueberries, a few frosted frozen ones beside, bright | right / left / **bl** | `凍ったまま？` | `恵み半分` 🔴 | `正解はコレ` 🟡 |
| 03 | `BKh-sdhsNUg` | **mô hình thận y khoa thật** (nửa cắt lộ cấu trúc) đứng trên bàn sáng, rau tươi vây quanh chân — một ảnh liền, cấm sticker/collage | left / right / **tr** | `体にいいのに` | `腎臓が疲れる` 🔴 | `5つの食べ物` 🟡 |
| 04 | `DD_AED6woII` | ly sữa lạnh **+ mô hình XƯƠNG cắt ngang lộ cấu trúc rỗng** ngay sau, cùng một chùm | right / left / **bl** | `毎朝の牛乳` | `骨に裏目！?` 🔴 | `見直す3つ` 🟡 |
| 05 | `BL7KtdXpl_A` | tô natto + chuối + bơ **+ mô hình THẬN** ngay sau, cùng một chùm | left / right / **tr** | `納豆と一緒` | `腎臓に負担` 🔴 | `7つの組合せ` 🟡 |
| 06 | `dabD8WcvXu8` | a tall glass of tomato juice, bright, a plain unlabelled bottle blurred behind | right / left / **bl** | `毎朝の一杯` | `食塩入り！?` 🔴 | `ラベル一行` 🟡 |
| 07 | `utNRgxBSf-8` | a rustic bowl heaped with cooked azuki beans, a wooden spoon, bright table | left / right / **tr** | `あずき一さじ` | `体が変わる` 🟡vàng | `6つの変化` 🔴đỏ |
| 08 | `ySxrtSzj8Bg` | a Japanese teacup of bright green tea beside a small kyusu teapot, sunlit | right / left / **bl** | `毎日の緑茶` | `半分ムダ` 🔴 | `NGは4つ` 🟡 |
| 09 | `LvBPBN1Jg4U` | a glass jar of golden honey with a wooden dipper lifting a thread of honey, sunlit | left / right / **tr** | `はちみつに` | `働き半分` 🔴 | `避ける3つ` 🟡 |
| 10 | `Iazj6ey7gyI` | a half cabbage, cut face toward camera showing layers, on a bright cutting board | right / left / **bl** | `茹でてる？` | `4割 逃げる` 🔴 | `正解はコレ` 🟡 |

**Mọi dòng ≤6 ký** (luật kênh A1 cho ≤8, nhưng `audience-45plus.md` §1 siết ≤6 — lấy cái chặt hơn).
**Video 07 cố ý đảo màu** (dòng 2 vàng, dòng 3 đỏ): bài này là khung LỢI ÍCH chứ không phải cảnh báo, đỏ-to sẽ nói sai giọng. Đúng biến thể 「MÓN→TWIST→STAKE」 mà v5 cho phép ≤1/3 số video.

### 3.1 Mọi claim đã đối chiếu với 概要欄 của chính video (chống mismatch)

| # | claim trên thumbnail | câu trong video |
|---|---|---|
| 01 | 半分ムダ | 「大切なたんぱく質を半分も体に届けられていない**かもしれません**」 |
| 02 | 恵み半分 · 凍ったまま | 「間違い①：凍ったまま食べる」·「恵みを半分も受け取れていない」 |
| 03 | 腎臓が疲れる · 5つの食べ物 | 「腎臓を、じわじわと疲れさせていた」·「食べ物を五つ」 |
| 04 | 骨に裏目 | 「骨のための牛乳が裏目に」（chính title）·「乳糖を分解する力は少しずつ弱まり」 |
| 05 | 腎臓に負担 · 7つ | 「60代の腎臓には納豆との『重ね食べ』が静かな負担に」·「食べ物7つ」 |
| 06 | 食塩入り · ラベル一行 | 「その一杯が、毎朝そっと塩を足していた」·「見分け方は、裏ラベルのたった一行」 |
| 07 | 体が変わる · 6つの変化 | 「60代の体に起きる6つの変化」（chính title） |
| 08 | 半分ムダ · NGは4つ | 「内臓脂肪への力を半分捨てているかもしれません」·「NGな飲み方4つ」 |
| 09 | 働き半分 · 避ける3つ | 「組み合わせ次第で働きが半分になってしまうことがあります」·「避けたい3つ」 |
| 10 | 4割逃げる | 「茹でるとビタミンCが4割逃げる？」 |

⚠️ Claim nào cũng có 「かも/ことがあります/？」 trong nguồn → giữ 「!?」 hoặc dấu ？ trên thumbnail ở những dòng khẳng định mạnh (04 · 06 đã có). YMYL: **cấm** 治る/完治/絶対 (`CLAUDE.md` §YMYL).

## 4. SAU KHI USER GEN — việc của Claude (đúng luồng đã chạy ở co-dai)

1. Soi **từng ký tự** chữ bake — bẫy đã dính thật: co-dai video 02 gen ra 「置くだけ**＝**でいい」.
2. Xoá watermark ✦ bằng **clone-stamp offset do máy tìm** (`_thumb_v3/fix_v3.py`: `best_offset` + `clone_patch`). ⛔ KHÔNG dùng `cv2.inpaint` — nền có kết cấu thì nó trả về ô phẳng còn hằn bóng hình sao.
3. Chuẩn khung: ảnh gen ra **2752×1536 = 1,7917, KHÔNG phải 16:9** → center-crop rồi resize **1920×1080**.
4. `python tools\stamp_brand_shokutaku.py <ảnh> --corner <theo bảng> --preview`.
5. **Đo bằng máy** dòng chính có ≥1/3 khung không — đừng hứa trước (bài học co-dai 01: đoán đạt, gen ra 25,3%).
6. Duyệt **168px + 120px**, đặt cạnh `_sheet168.png` xem có phải bản tối nhất hàng.
7. PNG >2 MB thì giao `.jpg` q92 (trần YouTube 2 MB).
8. Đẩy: `python ..\youtube-jp-nenkin\tools\update_live.py <plan.json> --project E:\Claude\Projects\youtube-jp-shokutaku --only-thumb --apply` — **dry-run trước**, tự backup, **KHÔNG đụng title/概要欄/tag**.

## 4b. ✅ ĐÃ ĐẨY LÊN KÊNH — **10/10 video**, 2026-08-05

`thumbnails.set` qua `youtube-jp-nenkin/tools/update_live.py --only-thumb --apply`.
**Title / 概要欄 / tag GIỮ NGUYÊN 100%.** File giao `06_VIDEO/_thumb_v6/<NN>_v6_brand.jpg`
(1920×1080, 0,37–0,46 MB) · rollback `plan_v6_backup.json` · tool `06_VIDEO/_thumb_v6/process_v6.py`
(chạy lại 1 lệnh) + `find_sparkles.py`.

| # | videoId | badge | sáng TB | ✦ |
|---|---|---|---|---|
| 01 ゆで卵 | `mQevRS1qBbk` | tl | 170 | sạch |
| 02 ブルーベリー | `31KXwgHbLY0` | tl | 186 | sạch |
| 03 腎臓・野菜 | `BKh-sdhsNUg` | bl | 178 | sạch |
| 04 牛乳 | `DD_AED6woII` | bl | 180 | sạch |
| 05 納豆 | `BL7KtdXpl_A` | tr | 174 | sạch |
| 06 トマトジュース | `dabD8WcvXu8` | tl | 170 | sạch |
| 07 あずき | `utNRgxBSf-8` | tr | 169 | ⚠️ **còn 2 ✦ mờ — CỐ Ý** (xem bẫy 4) |
| 08 緑茶 | `ySxrtSzj8Bg` | tl | 178 | sạch |
| 09 はちみつ | `LvBPBN1Jg4U` | tr | 177 | sạch |
| 10 キャベツ | `Iazj6ey7gyI` | tl | 189 | sạch |

Trước đợt này 6/12 video nền tối (sáng <90); giờ cả 10 ở **169–189** và cùng bộ nhận diện
(dải vàng + badge 食卓) giống nhau từng pixel.

### 🔴 Bốn bẫy đã dính khi xử lô này — đọc trước khi làm lô sau

1. **File src cũ ⇒ đóng dấu lên ẢNH CŨ.** Lô trước để lại `src/04_src.jpg` (bản bảng đen);
   script có `if not src.exists()` nên bản 04 mới bị bỏ qua, contact sheet hiện ảnh cũ, **không
   một cảnh báo**. Dấu hiệu duy nhất: sáng TB 154 (cũ) vs 180 (mới). → **LUÔN ghi đè src.**
   Cùng họ bẫy resume của renderer (`render-background.md` §2.5): hỏi *"file có chưa"* thay vì
   *"file còn ĐÚNG không"*.
2. **Badge tự chọn góc có thể ĐÈ MẤT CHỮ / che CHỦ THỂ.** 05 badge `bl` trùm đúng chữ 「7」 của
   「7つの組合せ」; 08 badge `bl` trùm chén trà. Hàm chấm điểm chỉ đo mật độ chữ + năng lượng
   biên — **nó không biết đâu là phần nhận diện của món**. → luôn duyệt mắt sau khi đóng dấu.
3. **Đo "dòng chính" bị MÓN ĐỎ làm nhiễu** — cà chua (06), mô hình thận (03·05) đều đỏ → báo
   **54,1%** ảo. Đã siết: chỉ đo trong nửa khung có cột chữ + trừ ô badge. ⚠️ Sau khi siết,
   03·05·07 ra **đúng 31,9% cả ba** — trùng nhau ở 3 ảnh khác nhau là **đáng ngờ**, đừng dùng số
   này làm bằng chứng. Bằng chứng là duyệt mắt 168/120px.
4. ⭐ **XOÁ WATERMARK ✦: hộp cố định KHÔNG dùng được, và có lúc phải BỎ VÁ.**
   - Mỗi ảnh có **HAI ✦ cạnh nhau** (to ~96px + nhỏ ~48px). `WM_BOX` cố định (đúc từ co-dai) chỉ
     trùm cái nhỏ → cái to còn nguyên trong khi lệnh in như thành công. **Đã đẩy 9 video mang
     lỗi này lên kênh rồi mới phát hiện** (bắt được nhờ soi mắt, không nhờ số).
   - Dò tự động cũng gãy 3 kiểu: ⓐ dò trên ảnh đã thu nhỏ 1920 → vệt mờ tụt dưới ngưỡng, hiện
     lại sau nén JPEG ⇒ phải dò ở **full-res** ⓑ nới ngưỡng thì bắt **dương tính giả** (đáy ly
     sữa, điểm sáng lọ mật) ⇒ khoá `quad=(0.80,0.76)` ⓒ `MORPH_CLOSE` **nhập nhèm 2 sao thành 1
     hộp NẰM GIỮA** chúng → vá vào khoảng trống, không trúng cái nào ⇒ dùng hộp tay trùm cả chùm.
   - `best_offset` còn **clone từ chỗ có ✦ khác** (07 có 3 vệt) → vá xong dán thêm sao mới ⇒ thêm
     `best_offset_avoid`.
   - 🛑 **07 あずき: DỪNG VÁ, giữ 2 ✦ mờ.** Vệt nằm đúng ranh sáng/tối chéo trên bàn gỗ vân ngang;
     đã thử best_offset 2 trục · ép `dy=0` giữ vân · hộp trùm cả chùm — cách nào cũng hằn một
     **VỆT CHỮ NHẬT rõ hơn hẳn** watermark mờ. Giữ nguyên là lựa chọn **ít xấu hơn**. Muốn sạch
     tuyệt đối thì **gen lại ảnh 07**, không vá thêm.

## 5. VIỆC CÒN MỞ
- **A/B 3×3** (`ab-3title-3thumb.md`): bộ này là T1 (baseline khuôn mới). T2 = đổi 1 biến hình (giữ nguyên chữ). T3 = đổi layout → **thêm 1 mặt biểu cảm 60–70代** như bản chuẩn 11 麦茶 (đó cũng là bản duy nhất của kênh đạt gate 4 của `audience-45plus.md`). Chưa làm.
- Kênh chưa quyết có đưa **mặt người** vào thành mặc định hay không. Bản 11 (có mặt) đo tốt nhất kênh về cỡ chữ, nhưng cỡ mẫu view = 0 nên **không có bằng chứng CTR** — đừng kết luận sớm.
- 10 bản này đều **giữ nguyên title** — nếu sau muốn xoay title thì theo `ab-3title-3thumb.md` §1: xong test ảnh mới đổi title, không đổi cùng lúc.
