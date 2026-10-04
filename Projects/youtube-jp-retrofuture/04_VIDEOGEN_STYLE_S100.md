# BỘ PROMPT t2v「S100」— 昭和100年 レトロフューチャー (kênh không lời, full POV)

> ⭐⭐⭐ **CÔNG THỨC v4 「REALISM」 — CHỐT 2026-09-22 tối (user duyệt sau 3 vòng thử, *"tạm rồi"* → *"áp dụng cho quy tắc tạo video cho kênh này"*).**
> **ĐÈ §7 · §7.8 · §7.9 · §8 (full POV · máy cầm tay · chuyển động phân cực · float)** — giữ để tra, KHÔNG dùng nữa.
> Thi hành: khối chung **`Projects/_media_library/realism_blocks.py`** (máy · ánh sáng · nhịp người — dùng chung với showa)
> + thế giới của kênh `tools/blocks_s100.py::WORLD_SHORT` → **`tools/gen_ep01_v4.py`** (34 cảnh × still + motion + t2v)
> → Flow: Image (Nano Banana 2) → chọn ảnh → ⋮ **Animate** → Veo 3.1 → đo **`Projects/_media_library/check_realism.py`**.
> Bốn điều chốt, mỗi điều có số ở §12: ① **góc thứ ba**, máy **KHOÁ** 2/3 cảnh · **TRÔI một bước/8s** 1/3 cảnh (mẫu: 32% shot di, 8–10 px/s)
> ② **ảnh trước → Animate** (thế giới + ánh sáng nằm trong ảnh, prompt động chỉ nói máy + hành động) ③ **nắng vàng một nguồn** ban ngày
> (mẫu 108 sáng / +27 ấm; ⛔ không "muted" — vòng 2 xám lạnh vì mốc đo trộn ngày–đêm) ④ **người cử động chậm**, một động tác trải hết 8s
> (mẫu 14 px/s, 10% khung động; lô cũ 37 px/s, 87%). **Tháp tầng phải ở nửa trên khung ở MỌI cảnh ngoại.** Prompt 1,0–2,1k ký, không 13k.
> ⚠️ Còn mở sau vòng 3: cháy trắng 3–6% ở cảnh nắng (mẫu 0,5%) · i2v tự trôi máy 2–6% dù khoá. Kịch bản 34 cảnh (bản Ⓑ) giữ nguyên.

> ⭐⭐⭐ **BẢN v3 — 2026-09-22: THẾ GIỚI VIẾT LẠI LẦN THỨ TƯ, và lần này theo VIDEO MẪU A**
> (`PUotm8YDbKM`, user: *"tao muốn giống hệt video mẫu từ cách di chuyển, quay phim, và phong cảnh đi"*).
> Mổ 16 frame của mẫu ⇒ thế giới của nó là **東雲町**: phố Showa **mặt đất, chật kín** ở tiền cảnh
> (hẻm · 商店街 có mái · tiệm たばこ · hòm thư đỏ · xe đạp · dây điện · dây leo) **+ SIÊU ĐÔ THỊ
> CHỒNG TẦNG** ở hậu cảnh (hàng lớp nhà và cầu cạn xếp lên tận trời, tàu chạy ngang, mây tích trắng).
>
> ⛔ **Bỏ hẳn khỏi v2:** cột đá khổng lồ · biển mây · cầu treo · nhà trên cây · 雲上駅. Mẫu **không có
> một thứ nào** trong số đó. §5.2 (trời) · §5.1 (cổ ≠ gỉ) · §7 (POV) · §7.8 (rung tay) **giữ nguyên** —
> chúng đã đo được là đúng, lỗi nằm ở **địa lý**, không ở chất ảnh.
>
> 🔴 **VÀ LỖI LỚP ĐẮT NHẤT BẮT ĐƯỢC CÙNG LƯỢT: khối THẾ GIỚI nằm ở 58–69% độ dài prompt.** Tức thứ
> user đòi nhất đứng đúng chỗ mà `ai-video-regen.md` §2 đã đo là model **bỏ qua**. Đó mới là lý do bản
> gen trước "không giống mẫu một tí nào" — không phải vì câu chữ tả sai, mà vì nó nằm quá sau. Prompt
> 12.000 ký thì không nhét hết vào 15% đầu được ⇒ kiến trúc **TUYÊN BỐ SỚM → CHI TIẾT SAU**: khối
> `HEAD` (~1.300 ký) mở đầu mọi prompt, chở **thế giới hai lớp + cấm chữ bịa + cấm số + cấm mặt méo**;
> các khối chi tiết giữ nguyên ở sau. Đo lại sau khi cài: thế giới xa **3%** · cấm chữ **5%** · cấm mặt **6%**.
>
> 🔧 **Luật giờ nằm trong CODE, không nằm trong file này:** `tools/blocks_s100.py` là nguồn sự thật duy
> nhất của mọi khối (v2 có hai bản khối ở hai tool ⇒ đúng bệnh `_sig`). File `.md` này giải thích **vì
> sao**, code quyết định **cái gì**.
>
> ⏳ **ĐANG NGHIỆM THU:** `tools/gen_test_world.py` sinh **3 cảnh thử** (hẻm đi bộ · đứng nhìn siêu đô
> thị · 商店街 đông người) → `06_VIDEO/01_kumo-no-ue/_test_world_FLOW.txt`. **Đạt rồi mới viết lại 40
> cảnh của tập 01** — mỗi lần đổi thế giới là một lần viết lại toàn bộ shot list, nên không đổ 40 cảnh
> trước khi 3 cảnh này qua mắt.

> File LUẬT của kênh `youtube-jp-retrofuture`. Prompt bơm extension: `videogen_ep01_DEMO_FLOW.txt`.
> ⭐⭐ **BẢN v2 — 2026-09-21, viết lại DNA hình sau khi user dán 2 VIDEO MẪU** (`~/Downloads/Vientuong`,
> 485s + 400s) và nói *"tao thấy nó anime quá, tao muốn kiểu như này"*. v1 đã bị đè ở **năm chỗ**, xem §0.
> Đọc cùng: `camera-language.md` · `ai-video-regen.md` · `media-library.md` §2.10.

## 0. VÌ SAO v1 RA ANIME — ba nguyên nhân, đều nằm trong prompt, không nằm ở công cụ

| # | v1 làm gì | tại sao nó kéo về anime | v2 |
|---|---|---|---|
| **1** | bảng vật liệu `cream enamel · mint green · bulbous rounded · chrome trim · glass domes` | đó là **từ vựng MINH HOẠ retro-futurism**, không phải từ vựng ảnh chụp | **vật liệu hữu cơ CÓ TUỔI ĐƯỢC CHĂM**: gỗ lên nước bóng, thép sơn bạc màu đều, đồng đánh bóng, vải bạt, giấy, lá, rêu, đèn lồng — §5 (⚠️ **không phải GỈ MỤC** — xem §5.1) |
| **2** | `floating island slung beneath gas balloons` | 🔴 **VẬT MỜI GỌI PHONG CÁCH**: trong dataset, đảo bay + Nhật Bản dính chặt với Laputa/Ghibli ⇒ model tự trả về anime **dù prompt không xin**. Cùng cơ chế `35mm` → cuộn phim: *negative không thắng token, phải BỎ token* | ⛔ **bỏ đảo bay** (user chốt). Thay bằng **thành phố gỗ chồng tầng quanh cây khổng lồ + hạ tầng đường ray xếp lớp ở xa** — đúng 2 video mẫu — §6 |
| **3** | chỉ có `filmed on a modern cinema camera` | quá yếu để chống hai lực trên | **khối `REAL_S100` đứng NGAY CÂU ĐẦU** — §1 |
| **4** | `NO letters` ở mọi cảnh | mẫu **đầy biển hiệu 風呂・銭湯・ゆ・氷・くすのき電器 và chữ ĐÚNG NÉT** — đó là thứ chở hồn Showa mạnh nhất, mất nó thì phố trông trống trơn bất thường | **bật chữ có kiểm soát** (user chốt) — §3 |
| **5** | `hard bright sunlight casting deep shadows` | gắt | **nắng loang qua tán lá + đèn lồng cam trong bóng râm** — và số đo xác nhận: mẫu có **contrast 50,3** so với 60–61 của KIOKU |

### 0.1 📊 SỐ ĐO 12 FRAME CỦA 2 VIDEO MẪU — mốc nghiệm thu mới

| | mẫu (trung vị 12 frame) | `STYLE_KIOKU` cũ | đọc |
|---|---|---|---|
| **contrast** (std luma) | **50,3** | 60–61 | 🔴 **mềm hơn hẳn** — đây là "dịu mắt" đo được |
| **ấm (R−B)** | **+22,0** | +20…+23 | ✅ khớp, giữ tông ấm |
| **bão hoà** | **36,4%** | 33–36% | ✅ khớp |
| **sáng** | 78 tổng · **84–94 ban ngày** · **21–29 cảnh đêm** | 91–99 | ban ngày gần khớp; ⭐ mẫu **dám để cảnh đêm rất tối** |

⇒ **Mốc mới cho bản render:** contrast **48–54** · R−B **+18…+26** · bão hoà **33–40%** · sáng ban ngày
**82–96**. Cảnh đêm được phép xuống **20–35** — đừng "sửa" nó lên.

---

## 1. ⭐⭐⭐ `REAL_S100` — KHỐI ÉP ẢNH THẬT, ĐẶT NGAY CÂU ĐẦU

> Đây là câu chống anime. Nó phải đứng **trước cả POV_LOCK và AVOID**, vì nó quyết định *loại hình ảnh*,
> còn hai khối kia chỉ quyết định *nội dung trong hình*.

```
Live-action photography, shot on a real camera: real human skin with pores and stray hairs, real woven cloth, real weathered timber with grain and splits, real old metal worn smooth by years of use, real leaves and moss, real dust in the air. This is a photograph of a real place, NOT an illustration, NOT anime, NOT a cartoon, NOT a painting, NOT a watercolour, NOT concept art, NOT a 3D render, NOT CGI, NOT a video game; no outlines around objects, no flat blocks of colour, no cel shading, no stylised faces, no oversized eyes, no painterly brush strokes, no glowing magical particles.
```

🔴 **Chín chữ `NOT` là cố ý.** Một câu `photorealistic` đơn lẻ **không thắng nổi** hai lực kéo ở §0 —
phải gọi đích danh từng phong cách cần loại. Cùng cách đã dùng với `no film strip and no sprocket holes`.

⚠️ **`REAL_S100` KHÔNG thay được việc bỏ token mời gọi** (§0 mục 2). Nó là lớp thứ hai. Lớp thứ nhất
vẫn là: **đừng viết đảo bay nếu không muốn Ghibli.**

---

## 2. ⛔ `AVOID_S100` — đặt ngay sau `REAL_S100`, trong 15% đầu prompt

```
no smartphone, no tablet, no flat screen, no touchscreen, no LED lighting, no laptop, no plastic drink bottle, no modern sportswear and no sneakers with logos; no glossy black plastic and no brushed aluminium anywhere; no rust and no rusted metal, no flaking or peeling paint, no grime, no mould, no decay, nothing broken and nothing derelict or abandoned — this is a well-kept neighbourhood, not a slum and not a ruin;
people may glance towards you for a moment and then carry straight on with what they were doing, the way you glance at someone you live with, but nobody holds a long stare into the lens, nobody poses or performs for you, no staged tableau and no group lined up facing you; nobody reacts to the robot, points at it or stares at it — the robot is completely ordinary to everyone present;
no face filling the whole frame; no dark vignette and no shading at the corners, no sepia or brown-washed colour, no faded washed-out look, no HDR look, no oversaturated colour, no harsh glaring sunlight and no blown-out highlights;
no camera shake, no jerky or stuttering motion, no speed ramping, no slow motion, no reversing motion;
no rubbery bending limbs, no feet sliding across the ground, no floating or gliding people, no disembodied hands, no extra fingers, no morphing objects;
no frame and no border of any kind around the picture, no film strip and no sprocket holes.
```

⭐ Câu `nobody reacts to the robot` thi hành **quy tắc 5 của bible** — thiếu nó, thế giới thành
*"phim về một con robot"* thay vì *"một thế giới có robot"*.

---

## 3. 🈂️ CHỮ TRONG KHUNG — BẬT, CÓ KIỂM SOÁT (đảo luật 2026-09-21, user chốt)

v1 cấm chữ tuyệt đối. Mẫu chứng minh **t2v hiện tại gen được kanji đúng nét** ở biển hiệu ngắn, và biển
hiệu là thứ chở không khí Showa mạnh nhất — nhất là với kênh **không lời**.

**✅ ĐƯỢC, và nên có 1–3 cái mỗi cảnh phố:**
```
old shop signs in Japanese: short painted or enamelled signboards of two to four large characters — 風呂, 銭湯, ゆ, 氷, 鮮魚, 電器, 食堂 — hand-painted on wood or enamel, weathered, hung over the shopfronts; a noren curtain with one or two characters on it; the characters must be correctly formed, crisp and legible
```

**⛔ CẤM (giữ nguyên từ luật cũ, mỗi cái một lý do đã trả giá):**
- **Số tiền, bảng giá, lịch, nhiệt kế, cân có mặt số** → vật mời gọi số, model điền bậy (`ai-video-regen.md` §3)
- **Câu dài / đoạn văn / poster chữ nhỏ dày đặc** → nát chắc chắn
- **Chữ làm CHỦ ĐỀ khung** (biển hiệu chiếm giữa khung, đọc ra thành mệnh đề của bài)
- **Chữ Latin, số Ả Rập, logo thương hiệu thật**

🔴 **Nghiệm thu: soi TỪNG KÝ TỰ ở cỡ thật.** Sai một nét là **loại clip, gen lại** — không "để tạm sửa
sau". Kanji rậm (鮮魚・電器) rủi ro cao hơn kana (ゆ・氷) ⇒ cảnh nào cần chắc thì xin kana.
⚖️ **Cái giá đã biết trước:** tỉ lệ clip phải gen lại sẽ **cao hơn v1**. Đó là đánh đổi để lấy hồn Showa.

---

## 4. 👥 `CAST_LOCK` — NGƯỜI LÀ NHÂN VẬT (đảo 2026-09-21, user: *"tao muốn làm video kiểu như này"*)

> 🔴 **BA ĐẢO LỚN CÙNG LÚC** sau khi mổ 16 frame của video mẫu `pJPST9DG92I`:
> ① ⛔ **BỎ FULL POV** → quay **góc thứ ba** (mẫu: 16/16 frame góc ba, thấy cả người, thấy mặt)
> ② ⛔ **BỎ ROBOT** → **người thường đang làm việc** là nhân vật (mẫu: 0 robot)
> ③ ✅ **biển hiệu DÀY ĐẶC** (mẫu: 森上駅 · 森書房 · 日の出食堂 · 八百屋 · 松風湯 · くすのき電器 ·
> ラジオ・電球 · 立入禁止 · và cả **トマト180円**)
>
> ⚠️ **Cái mất, ghi thẳng:** POV + robot khối cứng từng làm kênh **gần như miễn nhiễm bệnh trôi danh
> tính** — người xem không bao giờ xuất hiện, robot thì khoá được bằng danh từ. Bỏ cả hai là **nhận lại
> bệnh nặng nhất của t2v**. Bù bằng §4a, và đây là việc phải làm nghiêm, không phải khuyến nghị.

### 4a 🔒 KHOÁ CAST — dán NGUYÊN VĂN, không đổi một chữ, ở MỌI prompt có nhân vật đó

t2v không nhớ gì giữa hai clip. Cách duy nhất giữ một người là **mô tả y hệt nhau mọi lần**.

```
THE MOTHER: a Japanese woman of about forty, small and slight, her hair pinned up in a low bun with a few strands loose at the temple, a pale blue short-sleeved cotton blouse and a small-flowered apron, plain dark trousers, no make-up, an ordinary tired kind face.
```
```
THE DAUGHTER: a Japanese girl of about eight, a blunt bob cut to her jaw with a straight fringe, a white short-sleeved shirt under a pale yellow pinafore dress, white socks and worn leather shoes, a round face with slightly chapped cheeks.
```
```
THE FATHER: a Japanese man of about forty-five, tall and lean, hair parted at the side and going grey above the ears, a white short-sleeved shirt with the collar open and grey work trousers, a squarish face with deep lines at the mouth.
```

**Ba luật thi hành:**
1. **Mỗi tập tối đa 2–3 người được khoá.** Người còn lại là **khách qua đường** — tả chung
   (`an old man in a cardigan`, `two schoolgirls`), **không cần khoá**, và **không được cận mặt**.
2. ⭐ **Người được khoá thì mới cho thấy mặt rõ.** Ai không khoá thì quay **từ sau lưng, ba-phần-tư,
   hoặc ở xa** — đây là mẹo đã dùng nhiều lần: *giấu mặt là cách rẻ nhất chống trôi danh tính*.
3. ⛔ **Không cận mặt kín khung** — giữ `no face filling the whole frame` trong AVOID.

### 4b 🎬 FRAMING GÓC THỨ BA — thay hẳn khối POV cũ

```
Filmed from a normal third-person camera position, the way a documentary crew standing in the street would film it: we see the whole person in the frame, not their point of view. The camera is at the eye height of someone standing nearby, and nobody in the shot is aware of it.
```

⭐ **Cỡ cảnh theo mẫu** (đo 16 frame): **wide và medium là chủ lực** — nhiều khung thấy trọn một đoạn
phố trên cây với người nhỏ trong đó; medium khi có trao đổi (ông bán rau cúi xuống đưa đồ cho cậu bé,
bà chủ quán bưng bát cho khách). ⛔ **Gần như không có close-up mặt.**

### 4c 👨‍👩‍👧 VÌ SAO VẪN CẦN CAST CỐ ĐỊNH — thứ thay cho robot
Robot từng là **lý do bấm tập thứ hai**. Bỏ nó thì **gia đình cố định** phải gánh vai đó: cùng ba người
ấy, cùng căn nhà ấy, tập nào cũng có. Không có cái này thì kênh thành một chuỗi cảnh đẹp rời rạc —
đúng thứ `youtube-compliance.md` §1 gọi là inauthentic content.

## 5. 🎨 `STYLE_S100` v2 — vật liệu hữu cơ, ánh sáng loang, tương phản mềm

```
a retro-futuristic Japan of the year Showa 100, an alternate present where the Showa era never ended and its technology kept advancing along its own mechanical, atomic and pneumatic path,
built almost entirely of ordinary lived-in materials rather than shiny new ones — everything here is old but cared for — swept, wiped down and kept in repair, worn smooth and glossy from use rather than broken, paint faded soft and even rather than peeling, brass and copper kept polished; no rust, no flaking paint, no grime, nothing derelict and nothing abandoned, so: timber darkened and polished by decades of hands, the grain raised and smooth, painted corrugated steel in soft faded green and cream, copper pipe polished to a warm glow where hands touch it, galvanised tin, canvas awnings and cloth noren, paper lanterns, painted enamel signboards, hand-blown glass, glazed ceramic, brass fittings polished by use, old hard plastic mellowed to a soft warm tone, and everywhere leaves, moss, creepers and potted plants growing over it all,
warm natural colour, a little on the warm side, with deep green foliage, honey-coloured timber, the warm orange of lantern light, and clear turquoise water,
a deep clear blue sky with big soft white cumulus clouds standing in it, the blue and the white strong against each other,
but the light itself soft and open: dappled sunlight falling through the leaves in shifting patches, shadows staying soft and filled with bounced light, warm orange lantern glow pooling in the shaded places, and the far distance fading gently into pale haze; nothing glaring, nothing burnt out, gentle contrast, easy on the eyes,
shallow depth of field, the subject sharp and everything behind it melting softly out of focus,
one out-of-focus object sitting in the near foreground at the very edge of the frame so the picture has a near layer, a subject layer and a far layer,
fine photographic film grain over the whole picture,
evenly exposed right into all four corners with no darkening or shading at the edges,
the picture is a clean rectangle running right out to all four edges with nothing around it,
horizontal landscape video in 16:9 aspect ratio, 1920x1080 widescreen, clearly wider than it is tall, not vertical and not square
```

⭐ **Ba câu chở cả style, đừng cắt:** ① `ordinary worn materials rather than shiny ones` ②
`dappled sunlight … shadows soft and filled` ③ `the far distance fading gently into pale haze`
(sương xa là thứ tạo chiều sâu mà mẫu dùng ở **mọi** khung ngoại).

⚖️ **Đánh đổi ghi rõ:** v1 dùng `hard bright sunlight` học từ `STYLE_KIOKU` — vốn đúc từ **3 video
141–196K đã đo**. Rời khỏi nó là lựa chọn theo mẫu của user, **và lần này có số đỡ lưng** (contrast mẫu
50,3 vs KIOKU 60–61). 🛑 Nếu bản render trông **bệt, thiếu chiều sâu**: đừng bật lại nắng gắt — tăng
tương phản MÀU, thêm một vệt nắng xiên, dày hạt phim, hoặc đẩy sương xa mạnh hơn.

---

### 5.1 🔴 "CỔ" ≠ "GỈ" — dải hẹp phải trúng (user chốt 2026-09-21: *"trông cổ chứ không nhất thiết phải han gỉ"*)

Lúc chữa bệnh anime, tao nhồi từ vựng **ĐỔ NÁT** và đếm được **22 chỗ `rusted`** trong bộ prompt. Sai:

| | |
|---|---|
| ⛔ **MỚI CỨNG BÓNG LOÁNG** | `cream enamel · chrome · bulbous` — đây là v1, ra anime/đồ chơi |
| ⛔ **GỈ MỤC BỎ HOANG** | `rusted · patinated · pitted · chipped · flaking · grime` — đây là v2, trông **nghèo khổ và bỏ bê**, không phải cổ |
| ✅ **CŨ ĐƯỢC CHĂM** | mòn nhẵn vì tay người, gỗ lên nước, đồng đánh bóng, sơn **bạc màu ĐỀU** (không tróc), kính hơi gợn sóng, **sạch sẽ** |

**Bảng thay từ (đã áp 56 chỗ trong prompt, 12 chỗ trong luật):**

| ⛔ bỏ | ✅ dùng |
|---|---|
| `rusted corrugated iron` | `painted corrugated steel in soft faded green and cream` |
| `patinated copper` | `copper polished to a warm glow where hands touch it` |
| `tarnished brass` | `brass kept polished by the family, warm and glowing` |
| `weathered silvered timber` | `timber darkened and polished by decades of hands, the grain raised and smooth` |
| `enamel yellowed with age` | `enamel mellowed to warm ivory` |
| `pitted glass` · `chipped paint` · `gone chalky` | bỏ hẳn |

⭐ **Câu chốt, dán trong mọi prompt** — nó là thứ phân biệt chính xác hai thái cực:
```
everything here is old but cared for — swept, wiped down and kept in repair, worn smooth and glossy from use rather than broken, paint faded soft and even rather than peeling, brass and copper kept polished; no rust, no flaking paint, no grime, nothing derelict and nothing abandoned
```

⚠️ **Đây là dải HẸP, canh cả hai phía.** Cấm gỉ quá mạnh mà không có vế khẳng định (`worn smooth and
glossy from use`) thì model nhảy về **mới cứng** = quay lại bệnh anime. Luôn đi cặp: **một câu cấm mục +
một câu xin mòn-nhẵn-vì-dùng.**

---

## 5.2 ⭐⭐⭐ TRỜI RỰC MÀ NGƯỜI VẪN THẬT — và **VÌ SAO CÂU CÔ LẬP KHÔNG ĐỦ** (sửa 2 lần, 2026-09-21)

> user: *"trời xanh hẳn, mây trắng hẳn, trời với mây phong cách anime tí"* → tao viết
> `the way the sky looks in a Japanese animated film` **+ câu cô lập** `ONLY the sky … everything below
> stays photographic`. Gen ra: **phong cảnh đúng ý, nhưng NGƯỜI thành nhân vật 3D** — mặt tròn, mắt to,
> da nhẵn như figure. user: *"nhân vật lại anime rồi, tao chỉ muốn phong cảnh anime thôi"*.

🔴🔴 **BÀI HỌC — lần thứ TƯ cùng một định luật, và lần này tao đã tự cảnh báo rồi vẫn vấp:**
**CÂU CÔ LẬP KHÔNG THẮNG ĐƯỢC TOKEN PHONG CÁCH.** Viết `animated film` ở bất kỳ đâu trong prompt thì
nó nhuộm **toàn bộ** khung, kể cả khi ngay sau đó có `ONLY the sky … everything else photographic`.
Cùng cơ chế: `35mm` → cuộn phim · `floating island` → Ghibli · `glowing` → anime. **Phải BỎ TOKEN.**

### ✅ Cách đúng: xin ĐẶC TÍNH của bầu trời đó, bằng tham chiếu NHIẾP ẢNH
```
The sky is a deep saturated cobalt blue, deepening towards the top of the frame, and the cumulus clouds are pure brilliant white with crisp defined edges and clear sculpted volume, piled high and lit hard from one side — the blue and the white pushed strongly against each other, vivid and clean, the way a summer sky looks photographed on strong colour slide film, like an old railway travel poster. ONLY the sky and the clouds carry that heightened colour: everything below the skyline — the people, their skin and clothes, the timber, the rock, the signboards — stays completely photographic and real.
```
⭐ `strong colour slide film` + `old railway travel poster` cho **đúng hiệu ứng** (xanh đậm, mây trắng nét,
tương phản mạnh) mà **không có một chữ nào thuộc họ hoạt hình**. Câu cô lập vẫn giữ — nhưng giờ nó là
lớp thứ hai, không phải lớp duy nhất.
⚠️ ⛔ Đừng dùng tên phim cụ thể (`Velvia`, `Kodachrome`) — `camera-language.md` §7.1 đã đo: số hiệu
phim/ống kính làm model vẽ ra chính cuộn phim.

### ✅ Và một khối RIÊNG ép NGƯỜI — `REAL_S100` ở đầu prompt là chưa đủ
Phải có khối thứ hai, **đặt ngay trước phần tả cảnh** (trong 25% đầu), nói riêng về người:
```
THE PEOPLE ARE REAL PHOTOGRAPHED HUMAN BEINGS, not characters: real skin with visible pores, fine lines, uneven tone and a few blemishes, stray flyaway hairs, slightly crooked teeth, ordinary imperfect faces of ordinary ages, real cloth that creases and hangs with its own weight. They are NOT 3D characters, NOT CG models, NOT dolls, NOT illustrated and NOT stylised in any way: no smooth plastic skin, no enlarged eyes, no shrunken noses, no perfectly symmetrical faces, no doll-like proportions, no glossy hair. If the sky above them looks like a poster, the people below must still look like a documentary photograph.
```
⭐ **Câu cuối là câu chốt**: nó nói thẳng ra cái ranh giới mà hai tầng phải giữ, bằng ngôn ngữ của ảnh
chứ không phải của phong cách.

## 5.3 👥 PHỐ TẤP NẬP MÀ KHÔNG MÉO MẶT — sửa lần 2 (2026-09-21)

> user: *"lỗi nhân vật phụ nhiều quá nhìn méo hết mặt"* — ngay sau lượt tao nâng mật độ lên 20–40 người.

🔴 **Tao tự tạo ra mâu thuẫn, và đây là bài học chính:**

| tao viết | hệ quả |
|---|---|
| *"kể riêng 5–7 người, mỗi người MỘT việc khác nhau"* (để đám đông không thành khối dính) | model **dựng từng người có mặt rõ ở tiền cảnh** |
| *"đám đông không mặt nào đủ gần để nhìn rõ"* | câu trên đã kéo họ lên trước rồi — câu này thua |

⇒ **Mỗi người phụ được KỂ RIÊNG là một khuôn mặt model phải vẽ**, mà mặt phụ là chỗ t2v hỏng nhiều nhất.

### ✅ BỐN LỚP, áp cùng lúc — không lớp nào đủ một mình

1. **Giảm người được kể riêng xuống 2–4**, phần còn lại gộp: `beyond them a steady flow of thirty or more
   people, all of them tiny in the frame` — **cảm giác đông đến từ SỐ ĐÔNG MỜ, không từ số người được tả**.
2. ⭐ **Mỗi người phụ được kể riêng phải kèm một CHỈ HƯỚNG che mặt**: `seen from behind` · `facing away` ·
   `with their backs to us` · `head down over the scales` · `cap brim low` · `three-quarters turned`.
   ⭐⭐ **Thiết kế cảnh sao cho việc quay lưng là TỰ NHIÊN**: ở ga thì cả đám hướng về phía tàu; ở phố chiều
   thì ai cũng đang **đi về nhà, tức đi xa khỏi máy**. Đám đông quay lưng có lý do thì không trông dàn dựng.
3. ⭐⭐ **Đẩy đám đông RA NGOÀI TIÊU ĐIỂM** — đòn mạnh nhất và miễn phí, vì shallow DoF đã có sẵn trong
   STYLE: `well behind them and soft in the shallow focus` · `blurred and faceless in the depth of field`.
   **Mặt nằm ngoài nét thì không có mặt để méo.**
4. ⭐ **Cho model một ĐƯỜNG THOÁT** thay vì chỉ cấm:
   `if a background face cannot be rendered cleanly it must be turned away or left out of focus rather than
   shown`. Cộng negative cụ thể: `no distorted or melted faces, no asymmetric eyes, no warped hands`.

📌 Luật 4 là thứ đáng nhớ nhất: **câu cấm suông ép model làm một việc nó không làm nổi; cho nó một lối
thoát hợp lệ thì nó đi lối đó.** Cùng họ với việc bỏ token thay vì cấm token.

🛑 **Phanh:** nếu vẫn méo → hạ tổng số người ở cảnh phố xuống ~15 và đẩy xa thêm. ⛔ Đừng chữa bằng cách
kể chi tiết hơn về họ — đó chính là nguyên nhân.

## 6. ⭐⭐ `WORLD_KIT` v2 — THẾ GIỚI BỐN TẦNG, KHÔNG CÒN ĐẢO BAY

> 🔴 **Bỏ `A1 đảo bay treo khinh khí cầu`** (user chốt) — nó là vật mời gọi phong cách mạnh nhất (§0 mục 2).
> Tầng cao giờ do **thành phố gỗ chồng tầng + hạ tầng xếp lớp ở xa** đảm nhiệm, đúng 2 video mẫu.
> ⭐ **Mỗi cảnh NGOẠI phải thấy ≥2 TẦNG.** Mỗi món phải gán được **địa chỉ trong khung** (§6.9).

### 🌳 A. TẦNG CÂY — xương sống của thế giới
```
an enormous ancient camphor tree, its trunk as wide as a house, with wooden dwellings darkened and polished by years built in rings around it at four different heights, their windows small and square with wooden frames, their walls silvered plank and painted tin
a whole grove of these tree-towns, the lit windows glowing warm orange among the dark green leaves like rows of lanterns
rope-and-plank bridges strung from one great tree to the next, paper lanterns hung along their handrails, the planks worn pale in the middle where everyone walks
wooden stairways and ladders zig-zagging up the trunks, a small brass-cage lift running up the centre on a chain
copper rainwater pipes spiralling down the bark into glazed ceramic cisterns among the roots, moss and ferns growing where the water spills
laundry poles and hydroponic grow-tubes lashed to the branches, washing moving gently in the leaves
```

### 🏘️ B. TẦNG PHỐ CHỒNG TẦNG — Showa chật chội xếp lên cao
```
a narrow Showa alley of timber and tin shopfronts crammed together, air-conditioner-less windows propped open with sticks, potted plants in tin cans crowding every doorstep, a bicycle leaning on a wall
a covered shopping arcade under a long ribbed roof, hand-painted enamel signboards hanging in rows, warm orange lamps strung along the beams, fish and vegetables laid out on sloping stands
the same streets stacked four and five levels high, one arcade roof forming the street of the level above, wooden stairs cutting between them
a dense tangle of black power cables sagging overhead from pole to pole, pneumatic tubes running alongside them with brass junction boxes
laundry drying on poles from every upper window, futons hung over the railings to air
```

### 🏗️ C. TẦNG HẠ TẦNG XA — thứ làm khung hình thành viễn tưởng
```
far in the background, enormous elevated railway viaducts stacked in layers one above another, curving away into the haze, a train crossing on each level
a spiral monorail rail winding up around a distant tower like a ribbon, a single car climbing it
great concrete pylons rising out of the town and carrying the upper levels of the city away into the pale distance
a glass pneumatic lift tube running straight up the side of a tower, a capsule travelling inside it
the whole far skyline fading into soft pale haze so that the layers read as distance, never as a flat backdrop
```

### 🌊 D. TẦNG MẶT NƯỚC & DƯỚI NƯỚC
```
a floating quarter of timber pod houses resting on riveted steel pontoons, the whole street rising and falling very slightly on the swell, ropes and old rubber tyres slung along its edges
wooden boardwalks and gangplanks between the floating houses, nets and glazed ceramic floats drying on the rails
a bulbous cream and mint ferry skimming a hand's width above the water on its air cushion, throwing a fine ring of spray
the water clear turquoise and very calm, the whole floating street mirrored in it
under the surface, domes of thick curved glass held in brass ribs resting on the pale sand, their round windows glowing warm orange from inside, glass tube corridors running between them with people walking through, shoals of small silver fish crossing above, strings of bubbles rising steadily from brass vents, rippling bands of sunlight sliding over the glass
```

### 🚋 E. XE CỘ
```
a bulbous bubble car with a wraparound curved glass canopy, huge round frog-eye headlamps, a chrome bumper and paintwork dulled by weather, floating a hand's width above the road on a faint shimmer of air
a single-rail train hovering thirty centimetres above its rail, riveted steel flanks, rounded nose, small round windows, its destination board an old mechanical flip board far away and out of focus
a pill-shaped commuter bus with tail fins, kneeling down on its air cushion at the stop with a long sigh of escaping air
a three-wheeled delivery truck with a wooden flatbed, riding low on an air cushion instead of wheels
a tofu seller's three-wheeler with a mechanical brass bell that strikes itself as it goes
a cable car of riveted steel sliding along heavy cables between the tree-towns
a bicycle with a glowing flywheel hub humming softly where the chain should be
```

### 🏠 F. TRONG NHÀ
```
a rice cooker shaped like a polished steel sphere with a pressure gauge on top, a wisp of steam lifting from its valve
a cooktop of three ceramic rings glowing warm orange from the atomic element beneath them
a rounded refrigerator with a circular vault-style door and a chrome turning handle, its enamel mellowed to warm ivory
a pneumatic delivery tube mouth set into the kitchen wall with a brass flap, a capsule dropping through it with a thud
a television in a wooden cabinet on thin splayed legs, its bulging convex glass screen showing soft grey static, brass dials down one side
a black bakelite rotary telephone with a tiny round videophone screen set into its base
tatami mats edged with strips of warm glowing metal trim that light up softly where someone has just stepped
a low wooden chabudai table whose top is a warming plate, bowls steaming on it
a sealed glass sphere in the alcove holding a bonsai growing in luminous solution
a glass globe ceiling lamp in a cage of brass ribs, and paper lanterns in the corners
a three-bladed metal desk fan turning in a chrome cage, a floral enamel thermos flask, a red furoshiki bundle
```

### 🛣️ G. ĐƯỜNG XÁ & HẠ TẦNG MẶT ĐẤT
```
the road surface is not asphalt but interlocking cast concrete slabs with visible seams, a faintly glowing magnetic guide strip inlaid down the middle of each lane, worn smooth in the wheel tracks
a moving walkway running the length of the arcade, its slatted metal belt sliding along under a continuous rubber handrail
a raised roundabout where the signal is a glass globe on a cast iron post, swelling from warm orange to mint green
manhole covers of cast iron in concentric circular patterns venting thin steam
a red cylindrical post box with a pneumatic tube running from its base down into the ground
a tall vending machine of enamelled steel with a curved glass front, thick glass bottles riding round inside on a slow conveyor lit warm orange
a public telephone in a round glass capsule booth with a bakelite handset inside
street trees in round steel planters under their own little glass cloches
```

### 🈂️ H. BIỂN HIỆU & HÀNG HOÁ (§3 — chữ có kiểm soát)
```
short hand-painted signboards of two to four large Japanese characters hung over the shopfronts, enamel or wood, the paint faded soft and even
a noren cloth curtain in the doorway with one or two characters on it, moving in the draught
milk in glass bottles with foil caps delivered through a pneumatic hatch in the door
vegetables in ceramic boxes with vacuum-sealed glass lids, a little fog clinging inside
fish laid on crushed ice behind a curved glass case cooled by bare copper coils
sweets in glass test tubes stoppered with cork, standing in a wooden rack
a wire shopping basket whose handle folds flat with a spring catch
```

### ☁️ I. BẦU TRỜI — mọi cảnh ngoại ≥1
```
overhead: a deep clear blue sky with big soft white cumulus clouds, crossed by sagging black power cables, pneumatic tubes running between rooftops, laundry lines strung between the buildings, the branches of the great trees, and far off the stacked elevated viaducts curving away into pale haze with a train crossing one of them
```

### 6.9 🔴 BA LUẬT DÙNG KHO
1. ⭐ **Nhồi nhiều thì phải PHÂN TẦNG + GÁN ĐỊA CHỈ.** `in the near foreground at the left edge, out of
   focus: … · filling the middle, sharp: … · just past it on the right: … · further back in the shade: …
   · and beyond them in the haze: …`. **Món nào không nói được nó nằm ở đâu thì bỏ** — đó là món nhồi
   cho đủ. Không còn trần số món (user bỏ giới hạn ký tự).
2. ⭐ **Vật phải đang ĐƯỢC DÙNG.** Nồi cơm bốc hơi · ống khí nén vừa rơi viên nang · noren lay trong gió
   · băng chuyền đang trôi · nước nhỏ từ ống đồng xuống chum. Vật đứng yên = catalogue.
3. ⚖️ **Thứ tự vẫn quyết định** dù dài bao nhiêu: `REAL → POV → AVOID → ROBOT → ACTION → CAM → WORLD →
   STYLE`, và **nhắc lại 3 câu cốt tử ở dòng cuối**.

---

## 7. ⭐⭐⭐ FULL POV — MÁY ĐI NHƯ NGƯỜI ĐI BỘ (quay lại POV 2026-09-22, user chốt)

> Lịch sử: POV (v1) → **bỏ POV, góc thứ ba** (khi bám video mẫu) → ⭐ **quay lại FULL POV, nhưng lần này
> máy phải có DÁNG ĐI CỦA NGƯỜI**, không phải dolly trượt. user: *"cam di chuyển như người đang đi bộ
> góc nhìn POV ấy. Full POV nhé"*.

### 7a Ba tư thế của người xem — mỗi cảnh đúng MỘT
Khác hẳn bản POV đầu (chỉ có breath/step). Giờ tư thế của **người xem** quyết định cả nhịp lẫn tốc độ:

| pose | dùng khi | khối |
|---|---|---|
| ⭐ `walk` | đang đi trên phố, cầu, sân ga | *"lifts and settles by about the width of a finger with each unhurried pace, drifts a hair's breadth side to side as your weight changes from one foot to the other, one soft rise and fall about every second — **the gait of someone strolling**, never a jog, never a stumble, never a camera on a shaking rig"* |
| `stand` | dừng lại nhìn | thở, ±1cm, mỗi 3–4 giây |
| `sit` | ngồi ở bàn, bên futon, trên ván | như `stand` nhưng vững hơn |

**Phân bổ 40 cảnh: stand 20 · walk 13 · sit 7** — tức **67% cảnh người xem đứng hoặc ngồi**. Người đi bộ
thật cũng dừng lại nhìn; đó là lý do tự nhiên để giữ trần chống walking-simulator và chống say hình,
không phải một thoả hiệp kỹ thuật.

### 7b 🔴 ĐƠN VỊ TỐC ĐỘ ĐỔI THEO TƯ THẾ — chỗ dễ sai nhất
Bản góc thứ ba đo *"đi không quá MỘT MÉT trong 8 giây"*. **Với POV đi bộ thì một mét là đứng yên.**
| pose | câu số đo |
|---|---|
| `walk` | *"in the whole eight seconds you cover only **four or five unhurried paces**, the kind of walk of someone with nowhere to be"* |
| `stand`/`sit` | *"your head turns or leans by only a little, the framing changing by about a tenth"* |

⇒ **Đo lại `check_cammove.py` sau khi gen: cảnh `walk` sẽ vượt mốc 80px/8s và đó là ĐÚNG.**
Mốc 30–80px chỉ còn áp cho `stand`/`sit`. Đừng "sửa" cảnh walk cho vừa mốc cũ — đó là so sai đơn vị,
đúng bệnh đã dính hai lần (MAD cả bài vs trong shot · đoạn mẫu có cắt cảnh).

### 7c Hai câu giữ POV không hỏng (giữ nguyên từ bản POV đầu)
```
No part of the viewer's own body is ever in the picture — no hands, no arms, no legs, no feet, no lap, no shoulders, and no reflection of the viewer in any glass, water, metal or mirror — and the viewer is never seen from outside.
You never look down at your own hands or feet: your eyes are always looking out, around, ahead or up.
```
🔴 Câu thứ hai là câu cứu mạng: `camera-language.md` §6.3 đo được **POV nhìn xuống tay mình hỏng 14/21
clip**. Cấm hướng nhìn đó là cấm luôn cả lớp lỗi.
⭐ Và POV thì **người trong khung ĐƯỢC liếc mình** — không có câu đó thì người xem là bóng ma trong chính
phố của mình. Luật hẹp: *liếc một thoáng rồi làm tiếp, không nhìn chằm chằm, không tạo dáng*.

### 7d ⭐ MỖI CẢNH PHẢI KHAI "BẠN ĐANG Ở ĐÂU" — 40/40
`camera-language.md` §1.1: chiều cao chỉ là số đo, chưa trả lời *"tôi đang đứng ở đâu"*. Tool có field
`you` cho từng cảnh: *sitting on the next stool along the counter* · *walking a few paces behind the girl
on her way to school* · *sitting on the boards a little way along the walkway from her*.
⛔ Không định danh người xem (không tên, tuổi, giới) — chỗ trống để khán giả tự lắp mình vào.

### 7e 🔧 BÀI HỌC CÔNG CỤ: POV hoá ở TẦNG HÀM, đừng sửa 40 chuỗi
Khối `cam` của 40 cảnh vốn viết cho góc thứ ba (`the camera then edges…`). Sửa bằng cách replace văn bản
**trượt 35/40** — vì chuỗi trong source bị **ngắt dòng** giữa các cụm nên không khớp mẫu dài.
✅ Cách đúng: hàm `povify()` chạy lúc build, thay từ mẫu NGẮN nhất (`the camera then tilts` → `you then
raise your eyes`, rồi `the camera` → `you`). Kết quả: **0 chỗ sót**.
📌 Luật chung: **đổi một quy ước xuyên suốt thì đổi ở nơi ghép, không ở nơi khai** — cùng họ với
"sửa ở TOOL, không sửa triệu chứng".

## 7.8 ⭐⭐⭐ MÁY PHẢI **CẦM TAY**, KHÔNG PHẢI GẮN RIG (đo 2026-09-22)

> user: *"tôi thấy nó nhẹ nhàng nó rung rung giống người đi bộ mà"* — sau khi xem lại video mẫu A.

🔴 **Prompt của tao đang CẤM THẲNG thứ user muốn.** Ba khối tư thế đều kết bằng
`never shakes, never jitters, never stutters and never lurches`, cộng `smooth and mechanical as if the
camera were on a dolly` ⇒ ép về **mượt tuyệt đối, 0 rung**. Đó chính là chỗ "chưa giống".

### 7.8a SỐ ĐO — phase-correlate từng frame ở phân giải gốc, tách dải tần

| shot mẫu | nhịp 0,8–2,5 Hz | **jitter >4 Hz** | |
|---|---|---|---|
| s_216 | 0,020 | **0,161** | có rung |
| s_280 | 0,128 | **0,236** | có rung |
| s_32 | 0,077 | **0,100** | có rung |
| s_248 | 0,038 | **0,050** | có rung nhẹ |
| 4 shot còn lại | — | <0,05 | mượt |

⇒ **4/8 shot có rung li ti, biên độ 0,05–0,24 px/frame.** Mắt đọc ra là "cầm tay", nhưng **nhỏ tới mức
không gây say** — đó là lý do nó không phạm tinh thần luật chống handheld.
⚠️ **Đo ở 320×180 thì KHÔNG THẤY GÌ** (mọi shot đều "mượt"): rung dưới ¼ pixel bị nuốt khi hạ phân giải.
Phải đo ở phân giải gốc. 📌 Cùng họ `feedback_do_pixel_cua_so_quet` — **cửa sổ đo thô hơn vật cần đo**.

### 7.8b ✅ KHỐI `HANDHELD` — dán mọi prompt
```
The picture is carried, not mounted: it has the faint natural unsteadiness of a camera held in the hands of someone on foot rather than locked to a tripod or a dolly. The frame never sits perfectly still — it breathes and settles by a hair, and there is the smallest live tremor in it the whole time, the kind you feel rather than see. But it stays gentle: no jolt, no swing, no wobble, no bounce, nothing sharp or sudden, and the tremor is always smaller than you would notice if you were not looking for it.
```
⭐ **Hai câu giữ nó không thành lắc:** `the kind you feel rather than see` và `always smaller than you
would notice if you were not looking for it` — tả **ngưỡng nhận biết**, không tả biên độ bằng con số
(model không làm theo số px được). Cùng cách đã cứu float và tốc độ.

### 7.8c ĐỔI TRONG `AVOID`
`no camera shake, no jerky or stuttering motion` → **`no violent camera shake, no jolting, no swinging,
no wobble and no stuttering motion`**. Cấm rung **MẠNH**, không cấm rung li ti.

⚖️ **Ngược `audience-45plus` §2** (cấm handheld cho tệp 45+). Chấp nhận có chủ ý: biên độ đo được
**<¼ px/frame**, tức dưới ngưỡng gây mệt, và đây là chữ ký đo được của ngách. 🛑 Nếu bản render bị chê
chóng mặt thì đây là biến đầu tiên tắt.

### 7.8d 🔴 BÀI HỌC CÔNG CỤ — LẶP LẦN THỨ BA
Replace chuỗi DÀI trên source Python **trượt 33/40** vì chuỗi bị **ngắt dòng** giữa các cụm.
Đã dính ở `povify` (35/40), ở `safe_signs` (10/16), và giờ ở đây.
✅ **Luật chốt: mọi phép dọn quy ước làm trên TEXT ĐÃ GHÉP, không làm trên source.** Tool giờ có
`polish()` chạy ở dòng `return` cuối cùng của `build()` — chỗ duy nhất chắc chắn thấy toàn văn.

## 7.9 ⭐⭐⭐ CHUYỂN ĐỘNG PHẢI **PHÂN CỰC**, KHÔNG TRUNG BÌNH (đo video mẫu A, 2026-09-22)

> user: *"tao muốn cách quay phim, chuyển động kiểu này"* (video A `PUotm8YDbKM`). Đo bằng máy:
> dò 62 ranh giới cảnh, cắt 14 shot sạch, chạy ECC affine đầu↔cuối từng shot.

### 7.9a ⭐ SỐ ĐO — và một phát hiện đổi cách nhìn cả kênh

| | video A | mốc tao đang đặt |
|---|---|---|
| độ dài shot | **62 shot, TẤT CẢ đúng 8,0s** | — |
| chuyển cảnh | **CẮT CỨNG** (shot không chồng nhau) | dissolve 0,5s |
| nước máy chủ đạo | **DOLLY IN 6/11**, scale **+6%…+18%** | — |
| dịch khung / 8s | trung vị **117px**, dải **7 → 395px** | 30–80px |

⭐⭐ **Video A cũng là clip t2v 8 giây ghép lại — cùng công cụ, cùng ràng buộc với mình.** Không phải phim
quay thật. Nghĩa là mọi thứ nó làm được thì mình làm được; khoảng cách nằm ở prompt, không ở thiết bị.

⭐⭐ **Và đây là điều đáng giá nhất: mẫu KHÔNG trung bình — nó PHÂN CỰC.**
2/11 shot **gần tĩnh hẳn** (6,6px · 17,1px · scale 0.997) · 6/11 shot **đi rất rõ** (117 → 395px), 3 shot
"cú di lớn tới mức ECC không hội tụ". **Không có shot nào ở mức giữa.**
🔴 Còn bộ prompt của tao đang đặt **mọi cảnh ở mức giữa** — cảnh nào cũng nhúc nhích một chút. Đó chính
là thứ làm nó vừa không tĩnh vừa không có lực.

### 7.9b ⚖️ MÂU THUẪN VỚI *"cam nhanh quá"* — giải thế nào

Lượt trước user chê nhanh, tao ghìm xuống 30–80px. Mẫu đi **117px trung vị**, gấp rưỡi tới gấp năm.
⇒ Vấn đề hồi đó **không phải BIÊN ĐỘ mà là CHẤT**: dolly trượt đều đều, vô cớ, ở góc thứ ba thì 100px
cũng thấy nhanh; POV đi bộ có nhịp bước và có lý do thì 300px vẫn thấy tự nhiên.
📌 **Bài học: khi user chê "nhanh/chậm", hỏi xem họ chê CON SỐ hay chê CẢM GIÁC.** Sửa nhầm biến là mất
một vòng — ở đây là hai vòng.

### 7.9c THI HÀNH — hai đầu, bỏ hẳn mức giữa

| pose | câu số đo |
|---|---|
| ⭐ `walk` (13/40) | *"in these eight seconds you take **five or six paces** and the scene visibly opens up and comes towards you — by the last frame you are clearly **several metres further in**, close enough that what was in the middle distance is now right in front of you. **It is a walk, not a drift.**"* |
| `stand`/`sit` (27/40) | *"You are **completely still**. The framing barely changes at all — your head leans or turns only a fraction, and **nothing in the picture slides or drifts because of you**. Whatever moves is the people, the cloth, the steam or the cloud moving on their own."* |

**Mốc `check_cammove` mới:** `walk` **100–300px** (vượt mốc cũ là ĐÚNG) · `stand`/`sit` **<25px**.
⛔ Không còn mốc 30–80px cho bất kỳ cảnh nào.

### 7.9d 🔴 BẪY ĐÃ DÍNH: cảnh TĨNH mà khối `cam` vẫn nói "move back"
Khối `cam` của 40 cảnh viết từ thời góc thứ ba (`the camera then edges back`). Khi `stand`/`sit` đổi sang
*"completely still"*, **9 cảnh chứa hai câu chọi thẳng nhau** trong cùng một prompt.
✅ Chữa ở **tầng hàm**, không sửa 27 chuỗi: `povify(text, pose)` — với `stand`/`sit` thì mọi động từ di
chuyển đổi thành **ánh mắt**: `your gaze then widens slowly and steadily outward` · `your gaze then
travels slowly and steadily inward`. Người ngồi yên vẫn đổi được khung hình — **bằng mắt, không bằng chân**.
⚠️ Phải xếp mẫu DÀI trước mẫu NGẮN trong bảng thay, nếu không `draw … straight back` lọt lưới (đã dính).

### 7.9e ✂️ CẮT CỨNG, BỎ DISSOLVE
`SLIDES.json` đổi `dissolve_sec: 0.5 → 0.0`, độ dài **5:00 → 5:20** (giữ trọn 8s mỗi clip).
⚖️ **Ngược `audience-45plus` §2** (đòi dissolve ≥0,4s cho tệp 45+) — chấp nhận có chủ ý: tệp kênh này
rộng hơn 45+, và cắt cứng là **chữ ký đo được** của ngách. 🛑 Nếu retention tụt ở mốc chuyển cảnh thì
đây là biến đầu tiên xét lại.

## 8. ⭐⭐ `FLOAT_S100` — MÁY DẬP DÌU, KHÔNG PHẢI MÁY TRƯỢT RAY

| | | |
|---|---|---|
| ⛔ **rung** (handheld) | ngẫu nhiên, biên độ lớn | vẫn cấm — gây say, t2v làm ra thành *giật* |
| ⛔ **trượt ray** | mượt tuyệt đối, tốc độ phẳng lì | bỏ — với POV thành cảm giác trôi như ma |
| ⭐ **dập dìu** | có chu kỳ, biên độ **rất nhỏ**, đều | mặc định |

🔴 **Sửa một câu chống lại chính mục đích:** `never speeding up or slowing down` cấm luôn ease. Tách:
```
the move eases gently in at the start and gently out at the end, with no sudden change of speed and no speed ramping
```

**Tả bằng CƠ CHẾ, không bằng tính từ** (xin `gentle bobbing` ⇒ model trả về **lắc**):

**① `BREATH` (~60% cảnh — đứng/ngồi nhìn)**
```
the whole frame floats very gently, the way the view does when someone is simply standing there breathing: it drifts up and down by less than a centimetre, one slow rise and fall every three or four seconds, and it never shakes, never jitters, never stutters and never lurches
```
**② `STEP` (~40% — đi bộ)**
```
the frame carries the soft rhythm of someone walking slowly and unhurriedly: it rises and falls by no more than a finger's width with each step and drifts a hair's breadth from side to side as the weight changes, one soft rise and fall about every second and a half, even and predictable, and it never shakes, never jitters, never stutters and never lurches
```
**③ `SETTLE` (≤1 lần/tập — ngồi xuống)**
```
the frame comes to rest the way a person does when they sit down and settle: one last small downward drift, a brief overshoot of a finger's width, and then it holds still and only breathes
```

⚠️ Một cảnh **một mức float**. ⛔ `STEP` cho cảnh đứng yên = lắc lư vô cớ.
🔴 **Gate máy không đo được float** (dao động ±1cm chìm dưới ngưỡng `check_cammove`) ⇒ **duyệt bằng MẮT**,
câu hỏi duy nhất: *"trông như người đang đứng/đi, hay như máy trượt trên ray?"* Đừng bịa gate số cho nó.

---

## 8.5 ⭐⭐ TỐC ĐỘ MÁY — PHẢI LÀ SỐ ĐO, KHÔNG PHẢI TÍNH TỪ (đo 2026-09-21 trên clip đã gen)

> user: *"cam di chuyển chậm thôi nhanh quá"*. Đo bằng `check_cammove.py` trên **8 clip đã gen** và
> **10 đoạn 8s cắt từ 2 video mẫu**:

| | mẫu (đoạn 1-shot sạch) | 8 clip của mình |
|---|---|---|
| dolly `\|scale−1\|` | 1–8% | 0–**17%** |
| ⭐ **đường đi / 8 giây** | **13 · 26 · 64 px** | **116 · 204 · 247 · 331 px** |

⇒ **Quãng máy đi gấp 3–5 lần mẫu.** Tool còn tự báo `ECC không hội tụ (cú di quá lớn)` ở D1 và D5.

🔴 **Nguyên nhân: prompt viết `slowly and steadily` — một TÍNH TỪ — và không hề nói ĐI BAO XA trong 8
giây.** Model tự quyết. Đây là **lần thứ tư** cùng một định luật trong dự án này:

| xin bằng tính từ | model trả về |
|---|---|
| `gentle bobbing` | lắc |
| `roughly twice the height` (thumbnail) | 1,03× |
| `filling the LEFT two-thirds` | người toàn thân nhỏ |
| ⭐ `slowly and steadily` | **đường đi 331px / dolly +17%** |

### ✅ Câu thi hành — dán sau khối hai mốc, MỌI cảnh
```
The whole move is tiny and very slow: over the entire eight seconds the camera travels no further than one slow step, about a metre at most, and the framing changes by only about a tenth — it is so slow that at any single moment you cannot be sure it is moving at all, and you only notice it by comparing the first frame with the last.
```
Cảnh **tilt** thay vế giữa bằng: `the tilt covers about thirty degrees in total and takes all eight seconds`.

⭐ **Câu đắt nhất là vế cuối** — `you only notice it by comparing the first frame with the last`. Nó tả
**CƠ CHẾ NHẬN BIẾT**, không tả cảm giác; đó là thứ model làm theo được. Cùng cách đã dùng cho float
(`±1cm, một nhịp mỗi 3–4 giây`) thay cho chữ "dập dìu".

### 🔧 Mốc nghiệm thu mới (thêm vào gate §10)
`check_cammove.py`: **đường đi ≤ 80px/8s** · `|scale−1| ≤ 10%` · ⛔ **không clip nào được báo
`ECC không hội tụ`** — ở lô này nó có nghĩa là cú di quá lớn.
⚠️ Nhưng vẫn phải giữ **sàn** của gate cũ (`|scale−1| ≥5%` HOẶC `dịch ≥8px`) — chậm quá thành **máy
chết**, và `camera-language.md` §8.2 đã đo: 3/7 clip máy không di là lỗi ngược lại. **Dải đúng: đường đi
30–80px, scale 5–10%.**

### ⚠️ BẪY ĐO — ghi để không so sai lần sau
5/10 đoạn mẫu báo `ECC không hội tụ`, nhưng ở đó **không phải vì máy đi nhanh mà vì đoạn 8s cắt ra CHỨA
CẮT CẢNH** (mẫu cắt ~5s/cảnh). Đường đi của chúng bị thổi lên và **không so được** với clip của mình —
vốn là một shot liền không cắt. Chỉ 3 đoạn một-shot-sạch (13 · 26 · 64px) mới là mốc hợp lệ.
📌 Cùng họ bẫy `MAD cả bài vs MAD trong shot` (`camera-language.md` §8): **kiểm ĐƠN VỊ trước khi so số.**

---

## 9. 🎥 MÁY QUAY — `camera-language.md`

1. **Đúng MỘT nước máy** mỗi cảnh.
2. ⭐ **LUẬT HAI MỐC (§4.1)**: `the shot begins on … the camera then travels … and the shot ends on …`.
   Viết tên kỹ thuật trần trụi ⇒ đo được **51,6% khung đứng yên**.
3. ⭐ **Khai chỗ đứng của máy (§1.1)** — chỗ một người đứng được.
4. **Chiều cao máy = tư thế người trong cảnh.** ⛔ `at chest height` là mặc định SAI cho cảnh trong nhà.
5. 🔴 **t2v KHÔNG làm được TRỤC ĐỨNG** (§7.5, đo 0,995–1,009 = không di, 3/3 ca) ⇒ ⛔ cấm
   `pedestal / crane down / sink down`; cần hạ máy thì viết `DOLLY IN, forward and dropping as it goes`.

⛔ Cấm ở kênh này: dutch tilt · bird's eye · whip pan · handheld · zoom · `respectful distance` ·
`hands only` / `feet only`.

---

## 10. 🔧 GATE — chạy TRƯỚC khi bơm prompt (mọi phép so chuỗi qua `.casefold()`)

```python
p, lo = prompt, prompt.casefold()
assert lo.find("live-action photography")    * 100 // len(p) <= 10, "REAL_S100 nam qua sau"
assert lo.find("first-person point of view") * 100 // len(p) <= 20, "POV_LOCK nam qua sau"
assert sum(1 for m in MOVES.values() if m[:34] in lo) == 1,         "phai dung 1 nuoc may"
for bad in ("35mm","16mm","respectful distance","holds one position","slight vignette",
            "hands only","feet only","name tag","nobody looks at the camera",
            "pedestal","crane down","sink down","never speeding up or slowing down",
            "gas balloon","floating island","airship",          # §0 muc 2 — vat moi goi Ghibli
            "cream enamelled","mint green plastic","bulbous rounded"):  # §0 muc 1 — tu vung minh hoa
    assert bad not in lo, bad
assert "not anime" in lo and "not an illustration" in lo, "thieu khoi chong anime"
assert "no part of the viewer's own body" in lo,          "thieu khoi cam than the"
assert "the shot begins" in lo and "the shot ends" in lo, "thieu LUAT HAI MOC"
assert "eases gently in at the start" in lo,              "thieu ease"
assert ("simply standing there breathing" in lo) ^ ("soft rhythm of someone walking" in lo), "float"
assert tiers(p) >= 2 or is_interior,                      "canh ngoai phai thay >=2 tang"
```

🔴 **GATE PHẢI `casefold()` — đã báo đỏ giả 8/8 ngay lần chạy đầu:** gate kiểm chữ thường còn prompt mở
câu bằng `No part…` chữ hoa ⇒ **trượt toàn bộ 8 prompt hợp lệ**. Đúng bug đã từng làm **mất trắng ô mô
tả của một video** (`youtube-upload-seo.md` §4). 📌 Và đúng bài học `audience-45plus.md` §2.0h:
**gate báo đỏ hàng loạt ngay lần đầu thì nghi GATE trước, đừng đi sửa nội dung.**

**Gate trên clip đã gen:** `% khung đứng yên ≤10%` · `MAD blur trong shot ≥8,2` ·
`check_cammove.py`: `|scale−1| ≥5%` HOẶC `dịch ≥8px`.

---

## 11. NGHIỆM THU — soi ≥4 mốc/clip ở CỠ THẬT (0,3 / 2,6 / 5,2 / 7,6s)

| ❌ LOẠI | ✅ NHẬN |
|---|---|
| ⭐ **trông như anime / tranh vẽ / CGI** — viền nét, màu phẳng, mặt cách điệu | ảnh chụp có hạt, da có lỗ chân lông, gỗ có vân |
| ⭐ khung có **mảng lớn trông y hệt 1975 thường**, không một chi tiết máy nào | chi tiết máy nhỏ, khuất một phần |
| **chữ Nhật sai nét / méo / chữ giả** (§3) | biển 2–4 ký tự đúng nét · chữ li ti ngoài tiêu điểm ở rìa |
| có người **phản ứng với robot** | người đi ngang chỉ liếc rồi làm tiếp |
| robot **mọc chân** hoặc mất bánh xe | bánh xe khuất sau đồ vật |
| lọt **vật nhánh số hoá** (màn phẳng, LED trắng, nhựa đen bóng) | đèn nixie cam, bảng lật mờ |
| **thân người xem lọt khung** hoặc bóng người trong kính/nước | — |
| cảnh ngoại chỉ thấy **1 tầng** | — |

**Mốc màu bản render (§0.1):** contrast **48–54** · R−B **+18…+26** · bão hoà **33–40%** ·
sáng ban ngày **82–96** (cảnh đêm 20–35, đừng sửa lên).

🔴 **Ghi ra sổ mọi thứ CỐ Ý NHẬN** kèm lý do. 🔴 **Prompt trượt 2 lần liên tiếp = lỗi ở PROMPT**, đổi
token hoặc đổi thiết kế cảnh, đừng retry y nguyên.

---

## ✅ CÔNG THỨC ĐÃ CHỐT — v3, duyệt 2026-09-22 (dùng cho MỌI video sau)

> Đúc từ **2 vòng gen thử × 3 cảnh** + **1 phép đo 63 shot của video mẫu**. Nguồn sự thật của
> mọi khối là **`tools/blocks_s100.py`** — file `.md` này giải thích *vì sao*, code quyết định *cái gì*.

### 1. THỨ TỰ KHỐI — đây là thứ quyết định, không phải câu chữ

Đo được 2 lần: khối nằm sau ~30% độ dài prompt thì **model bỏ qua** (`ai-video-regen.md` §2).
Prompt của kênh dài 12–14k ký nên **không nhét hết vào 15% đầu được** ⇒ sắp theo **thứ đang hỏng**:

| # | khối | vị trí đo được | vì sao ở đây |
|---|---|---|---|
| 1 | `HEAD` | **0%** | ảnh thật + phố gần + thành phố xa + vật không-phải-của-ta + chống mặt méo |
| 2 | `MEGACITY` | **7%** | tháp xoắn — hỏng 2/3 cảnh ở vòng 1 |
| 3 | `RETRO_TECH` | **7–16%** | vật viễn tưởng TIỀN CẢNH — hỏng 3/3 |
| 4 | `NO_TEXT_NUM` | **15–24%** | chữ bịa — hỏng 3/3 |
| 5 | `REAL` · `POV` | 23–35% | đã đo là có tác dụng từ v2, không cần sớm hơn |
| 6 | `MOMENT` + khoảnh khắc | 39–45% | |
| 7 | `TOWN` `GREEN` `MATERIALS` `PEOPLE` `AVOID` | 50–90% | `AVOID` là khối dài nhất ⇒ để cuối, đặt đầu thì nó đẩy mọi thứ xuống |

🔴 **Ba lỗi đã trả giá, đừng lặp:**
- **Thêm khối mới rồi nối vào cuối** — `RETRO_TECH` rơi xuống 67–75%, đúng lỗi vừa sửa ở vòng trước, lặp ở chỗ khác. **Thêm khối = phải đo lại vị trí cả bộ.**
- **Cắt `HEAD` cho ngắn** làm câu chống mặt méo tụt 6% → 81% ⇒ **lượt cắt tự tạo hồi quy**. Cắt xong phải đo lại.
- **Nhãn gate viết tay, ngưỡng viết tay** ⇒ sửa một chỗ là lệch (nhãn nói `<=20%`, biểu thức còn `<= 12`). Nhãn phải **sinh từ chính ngưỡng** (`_at()` trong `gen_test_world.py`).

### 2. ⭐⭐ TỐC ĐỘ — mẫu GẦN NHƯ KHÔNG DI MÁY

Đo 63 shot của `PUotm8YDbKM` (`tools/measure_pace_ref.py`):

| | dịch khung / 8 giây |
|---|---|
| trung vị | **36,5px** = **2,8% bề ngang** khung 1280 |
| p25 · p75 | 13,6 · 100,2 |
| shot < 20px (≈đứng yên) | **30%** |
| shot < 40px | **54%** |
| jitter trong shot (trung vị) | **0,032** |

🔴 **Đây lật một giả định gốc:** kênh được thiết kế quanh "POV đi bộ", nhưng cái "nhẹ nhàng dập dìu"
của mẫu đến từ **người và vật động trong một khung đứng**, KHÔNG từ máy đi.
⇒ Mặc định `PACE["creep"]` (một bước chậm/8s). `stroll` chỉ khi cảnh đòi; `walk` gần như không dùng.
⇒ **Phần lớn cảnh là `pose="stand"`.**

🔴 **BẪY ĐƠN VỊ đã dính 2 lần:** "117px median" hôm trước đo trên **cửa sổ 8 giây bất kỳ** của video
mẫu — cửa sổ nào chứa **cắt cảnh** thì dịch khung khổng lồ ⇒ median bị đẩy lên gấp 3. Clip của mình là
**MỘT shot 8s không cắt** ⇒ phải so với **SHOT** của mẫu. Cùng họ `camera-language.md` §8 (MAD cả bài
vs MAD trong shot) và `feedback_do_pixel_cua_so_quet` — lần thứ 7 trong workspace.

**Mốc nghiệm thu** (`tools/check_test_world.py`): `walk` 12–70px · `stand` ≤20px · jitter 0,01–0,12 · khung đứng yên ≤10%.

### 3. ⭐⭐ VIỄN TƯỞNG PHẢI Ở TIỀN CẢNH

Vòng 1: viễn tưởng chỉ khai ở `MEGACITY` = hậu cảnh xa ⇒ **W1 có tháp** (nhìn dọc hẻm, tháp rơi đúng
điểm tụ nên model buộc phải vẽ) nhưng **W2/W3 ra thành phố kính hiện đại** = mất sạch.
⇒ **Hậu cảnh là thứ model tuỳ ý bỏ; tiền cảnh thì không.**

- `RETRO_TECH` dán **MỌI cảnh**: máy bán hàng đồng-kính có đồng hồ áp suất · xe ba bánh nồi hơi ·
  ống khí nén gửi thư dọc mặt tiệm · đèn đường chao thuỷ tinh hở dây tóc · TV lồi tủ gỗ ·
  quạt lồng đồng · máy tính tiền cơ · monorail một ray ngay trên mái. **Trong tầm với.**
- `MEGACITY` phải **gọi tên hình dáng không có thật**: `impossible spiralling ziggurats that widen as
  they rise, tier stacked on tier like a pagoda grown enormous`. Câu cũ "rank upon rank of buildings"
  chính là thứ gọi ra tháp kính.
- ⛔ Cấm cyberpunk: không neon · hologram · tháp kính · xe bay · **không gì lơ lửng**.
- Mọi vật retro **không mang chữ/số**.

### 4. ⭐⭐ CẢM XÚC — và cảnh cảm xúc thì MÁY PHẢI ĐỨNG

Vòng 1 không có khoảnh khắc nào, vì **hai nguyên nhân cộng dồn**: (a) không cảnh nào được thiết kế
một khoảnh khắc (b) máy đi nên có cũng vụt qua. Bằng chứng: bà cụ たばこ hiện rõ frame 1 của W1 rồi
**mất hẳn ở frame 4**.

⇒ `MOMENT` + kho `MOMENTS` trong `blocks_s100.py`. Luật:
1. **Vòng cung 3 nhịp, đỉnh ở nhịp GIỮA** — dẫn tới → bung ra → lắng lại (`camera-language.md` §6.6).
2. **Tả bằng CƠ THỂ**, cấm gọi tên cảm xúc: `mắt nhíu thành hai nếp` không phải `bà cười`.
3. **Là một TRAO ĐỔI** — giữa hai người, hoặc giữa người và vật trong tay họ (§6.2).
4. 🔴 **Cảnh có `moment` ⇒ `pose="stand"`.** Clip 8 giây không làm được vừa chuyển cảnh vừa cảm xúc.
5. Cảnh không có `moment` phải là **cảnh THỞ** (`crowd="none"`) — chuyển động do hơi nước, quạt, tàu,
   phơi phóng, bóng mây. Gate `cam-xuc-hay-tho` kiểm bằng XOR, không cho cảnh nào "lỡ cỡ".

### 5. CHỮ — XIN, đừng CẤM

Cấm suông ở 5% prompt vẫn **trượt 3/3 clip** (苑忉朶 · 木脊筒専 · 余車圧). Vì phố Nhật **buộc phải có
biển hiệu**, cấm hết thì model tự bịa để lấp — đúng định luật *negative không thắng token phong cách*.
⇒ **≤2 biển trong khung mang chữ, mỗi biển ĐÚNG MỘT từ quen** (`たばこ` `ゆ` `氷` `パン` `さかな`);
mọi biển khác là **mảng màu trơn / bị mái che / xoay cạnh / mờ xa**. Gate `chu-chi-tu-quen` chặn mọi
ký tự ngoài whitelist. Và cấm số/giá/đồng hồ ở mọi chỗ, nhất là góc khung.

### 6. NGƯỜI — Showa, không phải thời nay
Cấm **khẩu trang** · đồ có logo · balo/túi hiện đại · điện thoại. Vòng 1 W3 dính cả khẩu trang lẫn
đồ thời nay dù `AVOID` đã có sẵn khối cấm đồ hiện đại — thiếu đúng chữ "face masks".

### 7. QUY TRÌNH cho video sau
```
gen_prompts_<ep>.py  (import blocks_s100)  →  gate SẠCH
   ↓  bơm _FLOW.txt vào extension, gen 2–3 cảnh ĐẠI DIỆN trước
check_test_world.py <thư mục>   →  bảng số + sheet 4 frame cỡ thật
   ↓  soi MẮT: ① tháp xoắn ② vật retro tiền cảnh ③ khoảnh khắc ④ chữ bịa
đạt → mới gen cả tập
```
⚠️ **Số không chứng minh thế giới đúng.** Cả 4 câu soi mắt ở trên đều không có phép đo nào thay được.

## 12. ⭐⭐ ĐO "ĐỘ THẬT" — mẫu 異世界さんぽ vs lô mình, và BÀI THỬ REALISM (2026-09-22, chưa chốt)

> user, sau khi xem `pJPST9DG92I` (異世界さんぽ, 昭和 tree-city drama, 6:40, **32K view / 11 ngày**):
> *"Tôi thấy video này nó rất thật, còn video của tôi nó ảo quá. Như này thì dùng model nào là oke."*

**Trả lời bằng số, không bằng model:** 概要欄 của họ khai `企画：Gemini (Google AI Pro) · 画コンテ：ChatGPT ·
映像：Advanced Multimodal AI · 音声：Generative Audio AI · BGMなし・主人公なし` ⇒ gần chắc cùng bộ Google Veo
như mình. **Model không phải biến khác biệt.** Đo bằng `tools/check_realism.py`:

| | 異世界さんぽ | lô mình cùng ngày (`Dự_án_mới_31`, 109 clip) |
|---|---|---|
| MAD trong shot (p50 / mean) | **1,5 / 2,8** | 9,4 / 11,1 |
| % khung gần đứng yên (<1,0) | **35,6%** | 0,6% |
| % shot có MÁY DI | **32%** | 95% |
| hold | trung vị ~6s, có cắt tỉa | 8,0s nguyên clip |
| sáng TB / % pixel cháy | **65 / 0,5%** (50% cảnh tối) | 111 / 3,6% (1% cảnh tối) |
| 60fps | **giả** — 24fps nhân đôi (46,6% cặp frame trùng) | — |

🔴 **Cái này CHỌI với §7–§7.9 (full POV, máy cầm tay, walk 100–300px).** Mẫu "thật" là **góc thứ ba, máy
khoá cứng 2/3 số shot**, để vật lý (futon giũ · búa gõ ray · đèn pin · hơi nước bồn tắm) tự kể; ánh sáng
một nguồn có haze, nửa video là chạng vạng/đêm; mặt ba-phần-tư hoặc cúi xuống vật. Lô mình: máy bay 95%
shot, mọi cảnh sáng đều kiểu bưu thiếp, cháy trắng gấp 7.
⚠️ Nhưng §7 đúc từ video A (`PUotm8YDbKM`, 存在しなかった街) — cũng đo được **36,5px/8s = gần như không di
máy** (§CÔNG THỨC §2). Tức HAI mẫu đều nói **máy đứng**; chỗ khác nhau là POV (video A) vs góc ba (video này).
Bài học không phải "POV sai", mà là lô 31 đã trôi lên 95% máy di **dù rule nói creep** — cần đo lại vì sao
(`WALK`/`HANDHELD`/`PACE["walk"]` có đang thắng `SLOW_STAND` không).

**Bài thử A/B (chưa gen, chưa chốt):** `tools/gen_test_realism.py` → `06_VIDEO/01_tou-no-fumoto/_realism/`
— 6 cảnh của bản Ⓑ, đổi 4 biến cùng lúc: ① góc thứ ba, máy **khoá cứng** (`LOCKED_CAM`) ② **ảnh tĩnh trước →
Frames-to-Video** (`STILL_HEAD`) ③ ánh sáng **một nguồn, mờ bụi, không cháy** (`LIGHT_MUTED`) ④ prompt **ngắn**
1,2–2,3k ký thay 13,8k. Kèm 6 prompt t2v thuần cùng cảnh để tách biến ②. Khối mới ở cuối `blocks_s100.py`
(mục ⑥); bước bấm gì: `_realism/HUONG_DAN.md`. Mốc đạt: MAD p50 ≤3,0 · khung yên ≥20% · máy di 0% ·
sáng 55–95 / cháy ≤1% — **và** sheet 4 frame soi mắt. Thắng thì mới mở bàn sửa §7; thua thì §7 giữ nguyên.

**✅ Kết quả clip thử ĐẦU TIÊN (2026-09-22 19:00, tao tự bấm trong Flow, profile `saubeo.killuaa` 50 credit/ngày):**
cảnh `04_shutter`, Nano Banana 2 (ảnh) → Animate → **Veo 3.1 Lite** (Quality 100 credit không đủ), prompt động 1.6k ký.
`check_realism.py`: **MAD p50 1,10 · khung yên 36,2% · máy di 0% · sáng 65 / cháy 0,11%** — trùng mẫu ở cả 4 số.
Soi 8 frame: đủ 3 nhịp (tay lên shutter → shutter lên, đèn trong tiệm sáng → chống tay sau lưng nhìn phố → đi vào),
mặt quay lưng/ba-phần-tư, tay–vật to đúng vật lý. ⚠️ Còn: watermark **✦ + chữ "Veo" góc dưới-phải** (Flow bắt buộc
theo vùng, không tắt được → cắt 0,905W như slide, `media-library.md` §2.10 ⑤) · vài chữ nhỏ trên noren/poster trong tiệm
(cỡ không đọc được, NHẬN theo `ai-video-regen.md` §1). ⇒ Với **cùng model Lite**, chỉ đổi chỉ đạo (máy khoá + ảnh trước +
ánh sáng một nguồn + prompt ngắn) đã đưa 4 số từ vùng lô 31 về vùng mẫu. **Model không phải biến.** Còn phải gen đủ
6 cảnh + 6 t2v đối chứng trên account Pro trước khi chốt.

**🔴 Vòng 2 (3 clip Lite, 19:12) — "thật" đạt nhưng user: *"vẫn chưa giống video minh hoạ lắm"*. Đo ra hai lỗi, một là của tao:**
| | mẫu **ban ngày** (0–150s) | mẫu đêm | 3 clip mình |
|---|---|---|---|
| sáng TB | **108** | 31 | 66–90 |
| ấm (R−B) | **+27** | +7 | **−26 … +18** |
① **Mốc "sáng 55–95" là số RÁC**: trung bình cả video mẫu = trộn ngày với đêm. Ban ngày họ là **nắng vàng xuyên lá**,
tao lại viết `LIGHT_MUTED["day"]` = *"muted, nothing bright"* ⇒ clip xám lạnh. Cùng họ `feedback_do_pixel_cua_so_quet`
(cửa sổ đo không khớp vật), **lần thứ 8**. Đã sửa: `LIGHT_MUTED["day"/"interior"]` → nắng ấm một phía, dappled, giữ
*không cháy*; `check_realism.py` ④ chỉ còn chấm % cháy, sáng TB in ra để mắt so theo giờ trong ngày.
② **Thế giới vắng**: 2/3 clip là phố Showa thường, không một vật viễn tưởng nào — vì bài thử đặt `world=False` ở 4/6
cảnh. Mẫu có 巨樹 tree-city ở **mọi** khung ngoại, và đó là thứ người xem gọi là "giống". Đã sửa: `WORLD_SHORT` to hơn
(chiếm nửa trên khung, có tỉ lệ với phố) + `world=True` cho mọi cảnh ngoại + 2 cảnh mở rộng thành wide.
⚠️ Gate ① (MAD p50 ≤3,0) là mốc **cả lô** trộn cảnh thở + cảnh hành động; 3 clip toàn hành động (nước, trao gói) ra 4,3
là hợp lý, **không phải lỗi** — đọc kèm cột từng clip. Yaoya i2v có máy trôi nhẹ (scale 1,02) → i2v vẫn có thể lệch khoá.

**Vòng 2b — user: *"video nó di chuyển mượt lắm, kiểu dịu dàng êm"*. Đo lại bằng optical flow, ra thứ tao đo thiếu:**
| | mẫu | lô 31 ("ảo") | 3 clip thử |
|---|---|---|---|
| % diện tích khung ĐANG động | **10%** | **87%** | 7–24% |
| tốc độ phần đang động | **14 px/s** | 37 | 15–26 |
| máy ở shot có di | trôi **8–10 px/s**, zoom ±3–8%/shot | tới 1000px/8s | 0 |
⇒ "Êm" = **ít thứ động + thứ động thì chậm**, KHÔNG phải đứng yên. Lô 31 ảo vì cả khung bơi (máy bay). Bài thử
khoá máy 100% là đi quá sang bên kia; mẫu vẫn để 1/3 shot trôi nhẹ. Đã sửa: `DRIFT_CAM` cho 2/6 cảnh, `SUBJECT_GENTLE`
(người cử động chậm, một động tác trải hết 8s) thay câu "natural real-time speed", gate ③ nới thành *≤40% shot di và
di phải là trôi nhẹ*, thêm gate ⑤ diện tích động ≤25% · ⑥ tốc độ ≤22 px/s. Chuyển cảnh của mẫu là cắt cứng (không dissolve).


**✅ Vòng 3 (3 clip 1080p, 19:40, prompt `REGEN_3canh_vong3.txt`) — user: *"tạm rồi"* → CHỐT v4.** Đo: sáng **110** (mẫu ngày 108) ·
ấm **+34/+38** (mẫu +27) · tốc độ phần động **15 px/s** (mẫu 14) · thế giới có mặt 3/3 · nước và trao gói đúng vật lý · máy: shutter khoá
đúng, hai cảnh kia trôi 37–43px (mizumaki cố ý, yaoya là i2v tự trôi). Chưa bằng mẫu: **cháy trắng 3,4–6,2%** (mẫu 0,5%) → `LIGHT["day"]`
đổi "nothing burnt out" thành *"the brightest patches kept just short of white"*, đo lại ở lô sau. Gate ② (khung yên ≥20%) chỉ có nghĩa cho
cảnh KHOÁ — lô toàn cảnh trôi/hành động ra 0% là bình thường, đọc theo cột từng clip.
