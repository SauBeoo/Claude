# 04_VIDEOGEN_PROMPTS — CÔNG THỨC DUY NHẤT cho clip AI text-to-video (kênh 昭和くらし図鑑)

> ⭐⭐⭐ **2026-09-22 tối — CÁCH QUAY clip AI đổi sang CÔNG THỨC 「REALISM」** (CLAUDE.md §Visual khối đầu): góc thứ ba · máy KHOÁ/TRÔI một bước ·
> **ảnh Nano Banana → Animate** · nắng vàng một nguồn · người cử động chậm. Khối chung `Projects/_media_library/realism_blocks.py`, tool mẫu
> `tools/gen_realism_16.py`, đo `_media_library/check_realism.py`. **Nội dung của file này còn hiệu lực ở phần THẾ GIỚI/CAST/ACT/EXTRAS/kho cảnh**
> (§1.1 · §3.5 · §3.6b · §6 · §8.5–8.6); ⛔ phần MOTION v2 (§4) · FRAMING nước máy (§3) · gate MAD ≥8,2 · STYLE "crisp and sharp" hết hiệu lực cho clip AI.

> **v2 — chốt 2026-09-06** sau khi soi 121/121 clip của video 10 (通学路). Bản v1 (2026-08-10) lưu ở
> `_archive/04_VIDEOGEN_PROMPTS_v1_2026-08-10.md`. **Bản thi hành = `tools/videogen_lib.py`** — hằng số
> nguyên văn + gate. `gen_prompts.py` của mọi video **chỉ khai báo cảnh**, không chép hằng số.
> user: *"kiểm tra và hoàn thiện để những video sau prompt chuẩn chỉ, không lỗi nữa… video phải có hồn chứ
> không đơ đơ… một công thức duy nhất."*

## 0. Ba mục tiêu, và bằng chứng vì sao từng luật tồn tại

**Có hồn · không lỗi · đồng nhất.** Mỗi luật dưới đây có một con số phía sau — đừng nới luật nào mà không
có con số mới đè lên.

| cơ chế hỏng | bằng chứng video 10 | luật v2 |
|---|---|---|
| **khung phim + chữ FUJI** | **120/120** clip | STYLE bỏ `shot on 8mm home movie film` (model đọc thành *cho thấy dải phim*) → giữ **chất** phim: `the color, grain and softness of 1970s 8mm film` + `the image fills the entire frame edge to edge`; NEGATIVE cấm **đích danh** `film strip border, sprocket holes, film edge markings` |
| **tay/chân cụt lơ lửng** | **14/21** clip `hands only`; 07·07b·08·E7·E15 `feet only` | ⛔ **cấm mọi framing không có THÂN người**. Cận vật → `over the shoulder, torso and hands in frame`. Gate máy |
| **vật biến hình** | vải vàng→cặp da · que→đĩa · biển đổi chữ | **một vật · một hành động · một clip**; vật tả **nguyên văn** từ CAST + `the same X throughout` |
| **đảo chiều / quay mặt lại** | **H1 — clip mở đầu** đi tới-lui rồi quay mặt vào camera | động từ di chuyển **phải kèm hướng tương đối camera** (`away from the camera, seen from behind, growing smaller` / `toward the camera` / `left to right`) + `never turns around`; NEGATIVE `reversing motion, walking backwards, turning to face the camera`. Gate máy |
| **chữ Latin trên vật** | `RANDSERU` trên cặp · `GEISHA` trên hộp | vật trong CAST ghi `plain unmarked`; NEGATIVE `any letters, words, numbers or logos on any object, bag, sign or box` (v1 chỉ ghi `readable text` — quá chung, không chặn) |
| **mất chủ thể giữa clip** | 12 (người biến mất sau 1s) | MOTION `the subject remains in frame for the whole shot` (tự bỏ khi cảnh cố ý cho người ra khỏi khung) |
| **cast không đồng nhất** | cặp đỏ/nâu/đen · cờ đỏ thay vàng · 04 ra người lớn | CAST bible nguyên văn (màu + chất liệu + `plain unmarked`); trẻ tả bằng **quần áo học sinh** (`plain yellow cotton cap, white short-sleeved shirt, navy shorts`) thay `small figures` mơ hồ |
| **người gập/biến dạng** | 30b (nghiêng ra cửa sổ) | gate cấm `leans out of / bends double / contort / hangs from` |
| **đơ** | 04 · H8 · 22c đứng im | bắt buộc **≥1 chuyển động phụ** (breeze · sway · dust · shadow · weight shift · sleeve/hem) + **3 nhịp** = đúng 2 lần `, then` + cử chỉ vụng/thừa. Gate máy (strict) |
| `A_XXX's` | 3 prompt | gate |

🔴 **Mâu thuẫn đã gỡ:** v1 §2.7 khuyên *"cảnh tay-cận + vật an toàn nhất"* cho filter trẻ em — đúng loại khung
gây lỗi nặng nhất. **Bỏ.** Đường lui mới ở §7.

⚠️ **Cái gate KHÔNG đo được:** vật lý vẫn có thể sai (tay xuyên vật, bước hụt). Nên nghiệm thu bằng mắt (§8) là
bắt buộc, không phải tuỳ chọn — 24 clip lỗi của video 10 đều **qua** contact sheet 1 frame và chỉ lộ trên sheet 4 frame.

## 1. KHUÔN PROMPT — 6 khối, thứ tự cố định, máy ghép

```
[ACT: chủ thể + hành động 3 nhịp] , [FRAMING] , [BỐI CẢNH preset] , [STYLE LOCK] , [MOTION RULES] . [NEGATIVE]
```

Người viết **chỉ viết khối ACT** + chọn 1 preset + chọn 1 khoá FRAMING. Thư viện ghép 5 khối còn lại
(`videogen_lib.build`). Thứ tự này cố định vì model bám phần **đầu** prompt: hành động và khung phải đứng trước bối cảnh.

### 1.1 Viết ACT — 6 luật, mỗi luật một gate

1. **Chủ thể = token cast** (`A_ME`, `A_HAHA`…), không paraphrase. ⛔ Không dùng sở hữu cách `A_ME's` → viết `the jacket of A_ME`.
2. **3 nhịp mở → triển → kết** = đúng **hai** `, then`. Nhịp kết phải là *cử chỉ vụng hoặc thừa* (rocks back on its heels · pats it twice · shifts weight · looks at it) — đây là chỗ "có hồn" nằm.
3. **Di chuyển thì phải có hướng camera:** `walks away from the camera, seen from behind, growing smaller` · `toward the camera, growing larger` · `left to right` · `out of frame to the left`. Không có hướng = model tự do tiến-lùi (H1).
4. **≥1 chuyển động phụ** trong ACT: `a breeze moves the hedge` · `dust drifts off the lines` · `the sleeve catches the light` · `shifts weight onto one foot` · `the curtain moves` · `water ripples`.
5. **Một vật cầm tay, giữ nguyên:** `the same satchel throughout`. Không đổi vật giữa clip, không hai vật cùng đổi tay.
6. **Tư thế đơn giản:** đứng · ngồi xổm · cúi · với tay · bước. ⛔ `leans out of a window` · `bends double` · `spins` · xoay người về camera.

Mẫu đạt (H1 v2, clip mở đầu):
```
A_ME walks away from the camera down the middle of the empty unpaved lane, seen from behind, growing smaller
between the low fences with the satchel swinging at each step, then a breeze lifts a little dust along the ruts
behind it, then the figure reaches the far bend and keeps walking without turning around
```

## 2. STYLE LOCK v3 — nguyên văn (không sửa trong `gen_prompts.py`)

```
1970s Japan (Showa era, around 1970), faded warm 1970s colour photography, low contrast,
fine natural grain, soft natural light, slight vignette, nostalgic documentary look,
muted greens and ochres, natural imperfect framing, the image fills the entire frame edge to edge, 16:9
```

⭐⭐ **v3 (2026-09-10) — BỎ MỌI TỪ CHỈ VẬT LIỆU PHIM. Đây là lần thứ HAI cùng một lỗi, và lần này
tìm được nguyên nhân thật.**

**Số đo:** 90/90 clip của video 11 có **dải phim** — lỗ sprocket + chữ `FUJI` · `FUJIFILM` · `166` ·
`2084` in dọc mép, ăn mất mép hình. Trung vị dải: trái 35px · phải 51px · trên 21px · dưới 24px
(khung 1280×720).

🔴 **Nguồn nằm trong CHÍNH STYLE, không phải negative yếu:**
- `8mm film` → model vẽ **vật liệu** phim ⇒ lỗ sprocket
- `Fujicolor` → model in **tên hãng** lên mép ⇒ chữ FUJI/FUJIFILM

§5 dưới đây đã ghi đúng hiện tượng này (*"chữ FUJI trên dải phim"*) từ v1, và bản v2 **chỉ bỏ**
`shot on 8mm home movie film` mà **giữ lại cả `8mm film` lẫn `Fujicolor`** ⇒ vá chưa hết ⇒ lỗi quay
lại nguyên vẹn ở video 11. **Bài học tổng quát: NEGATIVE KHÔNG BAO GIỜ THẮNG MỘT TOKEN PHONG CÁCH —
phải BỎ token, không phải thêm lệnh cấm.**

Giữ nguyên thứ làm nên vẻ nhìn: bạc màu ấm · tương phản thấp · hạt mịn · vignette · documentary ·
lục/hoàng xịt. Chất phim còn được bù ở khâu grade (`tools/grade_vintage.py`).

⚠️ **Chưa có bằng chứng v3 hết dải phim** — mới sửa 2026-09-10, chưa gen clip nào bằng nó. Lô đầu
tiên phải **soi mép 1:1** (xem §5.1) trước khi gen tiếp cả lô.

⤵ v2 (đến 2026-09-10, đã gây 90/90 clip lỗi): `the color, grain and softness of 1970s 8mm film,
faded warm Fujicolor palette, …`

## 2.1 🔬 NGHIỆM THU DẢI PHIM — soi mép 1:1, ⛔ ĐỪNG tin số đo độ sáng

Hai phép đo bằng máy đã **thất bại liên tiếp** ở đúng chỗ này:

| phép đo | trả về | thật |
|---|---|---|
| "biến thiên dọc ở cột mép" | **2/90** có dải phim | **90/90** |
| "cột SÁNG đầu tiên = đầu nội dung" (dùng để crop) | crop xong, tưởng sạch | **chữ FUJI còn nguyên** |

🔴 Cả hai chết vì cùng một lý do: **dải phim CHỨA nét chữ sáng**, nên mọi phép đo theo độ sáng đều
bị chính cái chữ đó lừa — dò "cột sáng đầu tiên" thì nó dừng ngay tại chữ và crop giữ lại dải.
Cùng bệnh định vị watermark ✦ (`media-library.md` §2.10 ⑤: máy trượt 4/4 ở ảnh có chữ).

✅ **Cách đo đúng — TỈ LỆ PIXEL TRUNG TÍNH:** dải phim gần như đen tuyền (<34) điểm vài nét sáng
(>226) ⇒ rất ít pixel trung tính; cột nội dung thì đầy. Ngưỡng `≥0,42`. Tool:
`06_VIDEO/11_kyuryobukuro/strip_filmborder.py` (đo · `--run` cắt · `--demo` xuất frame trước/sau).

⛔ **Nghiệm thu BẮT BUỘC bằng mắt:** crop **mép trái + mép phải 1:1** của ~14 clip dán thành một
sheet rồi đọc. Sheet thu nhỏ toàn khung **cho qua sạch** cả hai lần.

## 3. FRAMING — danh sách ĐÓNG, mọi khuôn đều có thân người

| khoá | chuỗi nguyên văn | dùng khi |
|---|---|---|
| `wide` | static wide shot at chest height, the whole figure in frame | đi lại, đường, nhóm |
| `medium` | static medium shot at chest height, torso and hands in frame, face out of frame | **thay cho mọi "hands only"** |
| `ots` | over the shoulder, torso and hands in frame, face out of frame | thao tác vật nhỏ (ghim, buộc, xếp) |
| `behind` | seen from behind at chest height, the whole figure in frame | nhân vật đi ra xa |
| `low` | static low angle at knee height, legs and body in frame | **thay cho mọi "feet only"** (bước qua vũng, ván cống, vạch trắng) |
| `high` | static high angle looking down, the figure and the ground in frame | vẽ trên đất, chơi めんこ |
| `pan` / `tilt` | slow pan / slow tilt, figure in frame | cột điện, tháp canh |
| `still` | static wide shot, no people | **chỉ** cảnh trong whitelist không-người |

⛔ Cấm: `hands only` · `feet only` · `hand and X` · `close-up` · `macro` · bất kỳ chuỗi nhắc tay/chân mà không nhắc thân.
Gate: `bad_framing()` — regex tay/chân **và không có** torso/figure/body ⇒ 🔴.

## 3.5 ⭐⭐ EXTRAS — NGƯỜI NỀN (chốt 2026-09-10)

> user: *"Tôi thấy toàn chỉ có 1 nhân vật. Tôi muốn cảnh đông đúc, xum vầy. Cảnh nào cần đơn độc
> mới đơn độc thôi. Chứ video nào cũng chỉ có 1 người xem nó nhàm quá"*

**Khai theo PRESET, không khai theo từng shot.** Chuỗi người nền viết **một lần** trong
`videogen_lib.EXTRAS` (giống STYLE LOCK — máy ghép, người không tự viết); `gen_prompts.py` chỉ chọn
mức, và ghi đè lẻ bằng `CROWD_OVR` khi mức-theo-preset sai.

```python
CROWD = {"keiri": "full", "densha": "full",
         "chanoma": ("solo", "「数え終わるまで、誰も話しかけません」 — im lặng là NỘI DUNG")}
CROWD_OVR = {"H3": "few"}          # keiri ban đêm ≠ keiri giờ hàng chờ
rows = build(S9, P, C, crowd=CROWD)
n_red, n_warn = gate(rows, S9, P, C, crowd=CROWD, ...)
```

| mức | nghĩa | dùng khi |
|---|---|---|
| `full` | đám đông lấp khung | **nơi CÔNG CỘNG** mà lời kể gọi là đông (hàng chờ · 満員電車 · phố ngày lương · nhà tắm · hiệu cắt tóc · ngân hàng · bảng thông báo) |
| `few` | 2–4 người nền | nơi có người nhưng không đông (đường nhà ở chiều tối · phòng kế toán làm đêm · vợ đợi trong hành lang) |
| `solo` | **không thêm ai** | ⚠️ chỉ khi **đơn độc CHÍNH LÀ nội dung** — và phải khai lý do |

🔧 **Gate (đã cài, `videogen_lib.gate`):** in dòng `dam dong: full N · few N · solo N (x% solo)`, và
**`solo` ở `PUBLIC_PRESETS` mà không khai lý do ⇒ 🔴 CHẶN**. `PUBLIC_PRESETS` = keiri · office ·
machi · densha · ekimae · keijiban · sento · tokoya · ginkou. Preset **tư** (chanoma · genkan ·
yakei · yorugenkan) mặc định `solo`, không cần lý do — nhưng nên ghi.

**Bốn chỗ đơn độc HỢP LỆ, đo trên video 11** (không phải "thi hành kém"):
`HESOKURI 13/13` tiền riêng là bí mật · `END 13/13` khối này bán **sự vắng mặt** ·
`CHANOMA 17/19` 「誰も話しかけません」 · `yakei` đường đêm trống là hình ảnh trung tâm của vụ án.

⚠️ **Cái tao KHÔNG có: tỉ lệ đông/vắng chuẩn của ngách.** `CHANNEL_BENCHMARK_stills_2026-09-08.md`
chỉ đo nhịp giữ ảnh và chuyển động, **không đếm người**, và không lưu frame của winner nên không
đo lại được mà không tải lại video. Con số hiện tại (**full 69 · few 21 · solo 64 = 41% solo**) là
suy từ **lời kể của chính bài**, không phải từ benchmark. 🛑 Phanh: nếu retention 60s đầu của video
dùng lớp này **tệ hơn** lô trước thì đám đông là nghi phạm (mặt nền morphing) — soi sheet 4-frame
vùng nền trước khi kết luận, và hạ `full` → `few` chứ đừng về `solo`.

## 3.6b ⭐⭐ CẢNH ĐỜI THỰC — kho cảnh đúng thời 昭和 (chốt 2026-09-10, áp MỌI video sau)

> user: *"thêm nhiều cảnh đời thực nhưng phù hợp với video. Kiểu lễ hội, hút thuốc, đá bóng…"*
> → *"ừa tao muốn làm cho những video sau này"*

**Ba luật xử lý, mỗi luật một lý do — đọc trước khi bốc cảnh từ kho:**

1. 🚬 **THUỐC LÁ = MÔI TRƯỜNG, không phải hành động.** Khói mù trên dãy bàn · gạt tàn đầy · khói bốc
   lên từ gạt tàn. ⛔ **Không cho ai kéo một hơi trên khung**, không đưa thuốc lên miệng, không nhãn
   hiệu. Lý do: rule của workspace không liệt kê thuốc lá, **nhưng YouTube có hạng mục quảng cáo riêng
   cho tobacco** và cảnh người đang hút là chỗ dễ bị siết ad nhất. Cách này giữ đúng chất văn phòng
   昭和 mà không phải cảnh hút. *(Rượu trong 居酒屋 thì khác — nó nằm trong lời kể 「一杯だけ」 và
   không thuộc hạng mục đó; vẫn đừng để ai có vẻ quá chén.)*

2. 📅 **ĐÚNG THỜI ĐẠI mới bật được nút hoài niệm.** Ca gốc: user xin *"đá bóng"* → **đổi thành 野球
   (bóng chày) ở khoảng đất trống**, vì 昭和 40–50年 trẻ con Nhật chơi bóng chày; bóng đá chỉ phổ
   biến sau **J-League 1993**. Đặt bóng đá vào 1970 là sai thời, và tệp 50–70 — đúng tệp trả tiền cho
   cảm giác "hồi đó" — nhận ra ngay. **Sai thời thì cảnh đời thực thành cảnh giả.**

3. 🔗 **CẢNH KHÔNG CÓ TRONG LỜI KỂ thì phải NEO vào một câu có thật.** 祭 · 花見 · 野球 đều không có
   trong script video 11, nên gắn vào: 夏祭り ← 「夏と冬に、もう一つ、厚い封筒が来ます」 · 花見 ←
   「春に、会社の掲示板へ、その年の上げ幅が貼り出される」 · 野球 ← 「見ている子ども」. Luật gốc:
   hình phải khớp **CÂU đang đọc** (`media-library.md` §2.0-bis — cơ chế thật của ngách 昭和 là khớp
   câu, không phải khớp chủ đề bài). ⛔ Không neo được thì **đừng thêm**.

### 🔴 LUẬT SỐ 0 — KHO CẢNH CHỈ BỐC KHI **SCRIPT CÓ BEAT ĐÓ** (user chốt 2026-09-11)

> user: *"ý là dùng cho những script có cảnh đó"* → *"chứ không phải thêm vô tội vạ"*

**Ca gốc — tao đã làm sai đúng cái này ở video 11:** user xin "lễ hội, hút thuốc, đá bóng", tao thêm
**5 cảnh KHÔNG có trong script** (`M3`/`M4` khói thuốc · `HS8` 夏祭り · `S1` 花見 · `K1` 野球), mỗi
cái **suy ra** từ một câu gần đó (「夏と冬」→ lễ hội hè, 「春に」→ hanami). User bác ngay. **Đã gỡ cả 5.**

⇒ **Phân biệt hai thứ, đây là chỗ tao lẫn:**

| | |
|---|---|
| ✅ **Beat CÓ trong lời kể mà shot list bỏ mất** | **PHẢI** dựng lại cho đúng. Video 11: 居酒屋 「今日はいいだろう、給料日だ」 thành *đứng ngoài đếm tiền* · 「その日の夕飯は…いつもと違いました」 có **0 shot** · 銭湯・床屋 「混み」 thành *chủ tiệm dán giấy, không một khách*. 26 ACT sửa theo diện này **giữ nguyên** |
| ⛔ **Cảnh SUY RA từ một câu gần đó** | **KHÔNG thêm.** Neo kiểu 「夏と冬」→夏祭り là suy diễn, không phải beat |

🔧 **Và gate phải theo luật này, nếu không chính nó ép nhét:** mọi ngưỡng họ động tác
(SOCIAL_MIN · FAM_MIN · STROLL ≥4 · VEHICLE ≥4) đã **hạ từ 🔴 chặn xuống ⚠️ cảnh báo** ngày
2026-09-11. Gate chỉ hỏi *"script này có beat vui chơi nào mình bỏ qua không?"* — **script thật sự
không có thì BỎ QUA cảnh báo**. Thiếu chất sống thì sửa ở **tầng SCRIPT**, không nhét cảnh ở tầng prompt.

### Kho cảnh 昭和 40–50年 (1965–1980) — bốc theo BEAT CÓ THẬT, không bốc theo sở thích

| nhóm | cảnh | neo thường dùng |
|---|---|---|
| **Lễ hội · mùa** | 夏祭り (dãy quầy + đèn lồng + yukata) · 盆踊り · 金魚すくい · 縁日 · 花見 công ty (khăn trải, hộp cơm chuyền tay) · 餅つき · 大掃除 cuối năm | thưởng hè/đông · 「春に」 · Tết |
| **Trẻ con** | 空き地で野球 · めんこ · 縄跳び · ゴム跳び · 駄菓子屋 · 紙芝居 (ông đạp xe kể tranh) · 運動会 | 「見ている子ども」 · 「子どもの月謝」 |
| **Phố** | 商店街 đông · 屋台ラーメン · 豆腐屋 thổi kèn · 電気屋の前でテレビを見る群衆 · 福引き · 銭湯 xếp hàng bê chậu · 床屋 đông khách | 「町全体が…息を吸っていた」 · 「銭湯」「床屋」 |
| **Xe cộ** | スーパーカブ · 三輪トラック · ボンネットバス · xe đạp chở thùng · 荷台 chở người · リヤカー | đường về · phố · giao hàng |
| **Nhà** | 縁側でスイカ · 蚊取り線香 · 行水 · cả nhà quanh TV mới · bữa cơm đông người · 家族旅行 ngắm cảnh | 「テレビ、洗濯機、冷蔵庫」 · 「旅行に行くかどうか」 |
| **Công ty** | khói thuốc + gạt tàn (môi trường) · 慰安旅行 · 朝礼 · quạt điện + tay áo xắn · 満員電車の押し屋 | 「社内の空気が軽い」 · 「満員電車」 |

⛔ **Danh sách SAI THỜI, đừng dùng cho 昭和 40–50年:** サッカー · カラオケボックス (1980s) ·
ファミコン (1983) · コンビニ (phổ biến 1980s) · ペットボトル · エアコン · スマホ · 自動改札 ·
áo jeans xé · nhựa trong suốt hiện đại. *(AVOID v3 đã cấm nhóm hiện đại, nhưng nó không biết cái nào
là "sai thời trong phạm vi 昭和" — đó là việc của người viết.)*

### 🔧 Gate (đã cài, `videogen_lib.act_report` gọi trong `gate()`)

```
ho dong tac  : MANIP 132 · MOVE 76 · SOCIAL 36 · WORK 17 · VEHICLE 13 · EAT 13 · PLAY 7 · STROLL 4
chi MANIP/MOVE : 81/154 (52%)  [tran de xuat 45%]
co VUI CHOI/QUAY QUAN: 47 shot  [can >= 12]
```

| ngưỡng | mức | vì sao |
|---|---|---|
| ≥12 shot có SOCIAL/PLAY/EAT · ≥5 họ động tác · ≥4 STROLL · ≥4 VEHICLE | ⚠️ **cảnh báo** *(hạ từ 🔴 ngày 2026-09-11)* | để 🔴 thì gate tự ép nhét cảnh vào script không có beat — đúng cái user kết án. Xem LUẬT SỐ 0 |
| ≤45% shot chỉ có MANIP/MOVE | ⚠️ **cảnh báo** | 🔴 **con số này là ĐOÁN**, không có số đo của ngách. Để nó chặn thì mọi video sẽ đỏ mãi rồi bị bỏ qua — đúng bệnh *"luật kiểm bằng mắt thì sẽ trôi"* |

📌 **Số đo ca gốc (video 11), để so:** trước **4 lượt vui chơi = 0%** · 66% chỉ nhấc/đặt · top động từ
`hold 33 · press 29 · draw 28 · turn 27`. Sau khi viết lại 31 ACT + 40 nhịp kết: **47 shot có vui
chơi/quây quần** · 52% chỉ nhấc/đặt · thêm 4 họ mới (VEHICLE 13 · EAT 13 · PLAY 7 · STROLL 4).

⚠️ **Trần tự nhiên, biết trước:** video mà **đề tài chính là thao tác một vật** (đóng dấu hanko, đếm
tiền, ký giấy) thì MANIP không xuống dưới ~50% được mà không phá đề tài. Đừng đổi nội dung khối lõi
chỉ để làm xanh một con số đoán.


## 4. MOTION RULES v2 — nguyên văn

```
slow deliberate natural human motion, continuous single take, no cuts, the subject remains in frame for the whole shot, no reversing
```
Cảnh có `out of frame` / `out of sight` / `disappears` trong ACT ⇒ thư viện tự dùng bản không có `remains in frame`.

## 5. NEGATIVE v2 — nguyên văn (4 nhóm mới in đậm)

```
Avoid: film strip border, sprocket holes, film edge markings, any frame or border around the image,
modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, sneakers with logos,
any letters, words, numbers or logos on any object, bag, sign or box, brand logos, western faces, anime style,
oversaturated colors, HDR look, clean digital sharpness, close-up faces, fast cuts, camera shake,
reversing motion, walking backwards, turning to face the camera,
disembodied hands, floating limbs, extra fingers, morphing objects, objects changing shape or color
```
Bài học v1: negative **chung** (`brand logos`, `readable text`) không chặn được thứ model coi là *thành phần của
phong cách* (chữ FUJI trên dải phim, chữ trên cặp). Phải cấm **đích danh vật + vị trí**.

## 5.5 ⭐ VẬT PHẢI **DÍNH VÀO NGƯỜI** — vật RỜI trên mặt đất thì model NHÂN BẢN (chốt 2026-09-06)

**Ca gốc: cảnh `C3` của video 10, gen lại BA vòng, sai theo hướng TỆ DẦN.**

| vòng | câu đếm trong prompt | kết quả đếm bằng mắt |
|---|---|---|
| 1 (prompt v1) | `satchels left on the ground` (số nhiều, không đếm) | **3 cặp** / 2 đứa |
| 3 | `exactly two … one satchel each and no other bag in the shot` | **4 cặp** (2 đeo + 2 nhặt) |
| 4 | `nothing worn on either back, both backs completely empty` | **6 cặp** (2 đeo + 2 cầm + **2 vẫn nằm dưới đất**) |

🔴 **Cơ chế:** vật được "nhấc lên" **không biến mất khỏi mặt đất** — model **NHÂN BẢN** vật rời chứ
không **DỜI CHỖ** nó. Càng siết câu đếm càng tệ, vì câu đếm chỉ nói *có bao nhiêu*, không nói
*vật nào là vật nào*.

⭐ **Đối chứng trong chính video 10:** mọi clip chỉ có vật **ĐEO trên người** (H1 mở bài · 13:14 ·
`24b` · `E15`) đều **đúng số tuyệt đối**. Vật gắn vào thân thì model coi là phần của người.

**Luật thi hành:**
1. **Vật phải ĐEO hoặc CẦM** — `strapped on its back`, `held in one hand`. Cấm cảnh mở ra với vật
   nằm dưới đất rồi người cúi xuống nhặt.
2. Muốn nói "không có vật rời" thì **viết câu phủ định**: `no bag or object anywhere on the ground`
   (gate hiểu phủ định, không báo oan).
3. Cần đúng một vật rời (cống, hộp thư, biển) thì **KHÔNG cho ai chạm vào nó** trong clip.
4. **Gate máy** (`videogen_lib.py`): `GROUND_OBJ` × `PICK_UP` → 🔴 **CHẶN**; chỉ `GROUND_OBJ` → ⚠️.
   `GROUND_NEG` miễn câu phủ định. Kiểm chứng: vòng 3 + 4 → 🔴 · vòng 1 → ⚠️ · vòng 5 + H1 → ✅.
5. ⚠️ Quét 121 prompt của video 10: **6 cảnh** có vật rời (`08b` `20b` `24b` `25d` `Y2` `E15`) nhưng
   **không cảnh nào có động tác nhặt** ⇒ chỉ ⚠️, và soi mắt `24b`/`E15` xác nhận **không nhân bản**.
   Tức ranh giới thật là **HÀNH ĐỘNG NHẶT**, không phải sự hiện diện của vật rời.

## 6. CAST BIBLE — quy tắc viết

- Tả bằng **quần áo + vật**, không mặt, không tuổi (filter §7). Mỗi vật cầm/đeo: **màu + chất liệu + `plain unmarked`**.
- Học sinh: `a small figure in a plain yellow cotton cap, white short-sleeved shirt and navy shorts, with a plain unmarked brown leather satchel on its back`.
  ⛔ Không dùng `small figures` trần — model đoán tuổi/ăn mặc tuỳ ý (04 ra người lớn thường phục).
- Người lớn: nghề + 1 chi tiết (`a woman in her fifties wearing a plain pale green sash over a plain dark coat and white cotton gloves`).
- Cần người lạ cho một cảnh (gọi điện, xem bảng tin) → **thêm cast riêng** (`denwa`), đừng mượn cast chính.
- Gate cảnh báo khi vật cầm/đeo thiếu `plain unmarked`.

## 7. FILTER TRẺ EM (Veo/Flow) — đường lui MỚI

Từ cấm: `child/children/kid/boy/girl/elementary/pupil` (gate 🔴). Cảnh vẫn bị chặn thì theo thang:
1. Giữ hành động, **đổi framing sang `behind`** (thấy lưng + mũ vàng + cặp, không mặt) — không phải cận tay.
2. Chuyển vai cho **người lớn trong cast** (bà giao thông, mẹ, ông chủ tiệm) làm cùng hành động.
3. Bỏ người, vật tự chuyển động từ ngoài khung — **chỉ khi cảnh nằm trong whitelist không-người có lý do**.
⛔ Không spam regenerate; chặn ở nấc 3 = từ khác trong prompt, báo lại.

## 8. GATE — máy trước, mắt sau, cả hai bắt buộc

**Máy (`videogen_lib.gate`, chặn cứng ở `strict=True`):** framing không thân · framing ngoài danh sách · di
chuyển thiếu hướng · nhìn/quay về camera · tư thế cấm · 0 hoặc 1 `then` · thiếu chuyển động phụ · `A_XXX's` · từ
trẻ em · không người (trừ whitelist có lý do) · interior lẫn street · STYLE/MOTION/AVOID không nguyên văn · còn
`shot on … film`. `strict=False` chỉ để **vá video đã gen** (3 nhịp · chuyển động phụ · hướng → ⚠️).
Selftest: `python tools/videogen_lib.py --selftest` nạp S của video 10 v1 → phải bắt ≥21 framing + H1.

**Mắt (`tools/review_clips.py <clips_dir> --edges`), sau khi clip về, TRƯỚC crop/stretch/render:**
- `review_N.jpg` — mỗi hàng 1 clip × 4 frame (0,8 · 3,0 · 5,2 · 7,4s). Tìm: tay/chân lơ lửng · vật đổi hình giữa hàng ·
  người biến mất · quay mặt · khoảng cách nhảy gần-xa-gần · chữ trên vật.
- `edges_N.jpg` — dải mép trái + trên. Tìm: vạch đen đều · lỗ răng · chữ vàng.
- ⛔ Contact sheet 1 frame giữa khung **không được dùng làm nghiệm thu** — nó cho qua 24/24 clip lỗi.

🔴 **ĐO ĐƯỢC 2026-09-06 (lô 22 clip v2): STYLE v2 + NEGATIVE đích danh VẪN KHÔNG CHẶN ĐƯỢC VIỀN PHIM** —
22/22 clip mới vẫn có dải đen + chữ `FUJI`, dù prompt đã bỏ `shot on … film`, thêm `the image fills the entire
frame edge to edge` và cấm đích danh `film strip border, sprocket holes, film edge markings`.
⇒ **Bước crop là BẮT BUỘC trong chuỗi sản xuất, không phải phương án dự phòng.** Model gắn dải phim vào
*khái niệm* "1970s 8mm film" ở tầng sâu hơn chữ nghĩa; muốn hết hẳn thì phải bỏ mọi tham chiếu phim khỏi
STYLE (đánh đổi: mất tông nhận diện của 9 video đã đăng — user đã chọn giữ tông).

**Lưới an toàn viền (BẮT BUỘC, không phải tuỳ chọn):** `crop_border.py` với sàn `[110, 130, 80, 80]`px —
hằng số chốt **bằng mắt** sau 4 vòng ở video 10; ba phép đo tự động (độ sáng · bão hoà · std) đều hỏng ở một
loại cảnh khác nhau vì viền chứa đủ ba đặc trưng của ảnh thật (sáng · có màu · biến thiên). Chi tiết: bản v1 lưu trữ.

**Chuỗi sản xuất:** `gen_prompts.py` (gate máy) → user gen → `review_clips.py` (gate mắt) → gen lại clip lỗi →
`crop_border.py` (nếu cần) → `reindex_clips.py` → `stretch_clips.py` (khe từ `timeline.json` thật) → render `--reuse`.

## 8.5 ⭐⭐ NHÂN VẬT ĐỒNG NHẤT + HÀNH ĐỘNG NỐI LIỀN (user chốt 2026-09-06, áp từ video 11)

> user: *"Tao muốn kịch bản phải đồng nhất nhân vật, video phải nhất quán. Hành động của prompt
> trước phải được nối liền với hành động của prompt sau."*

### 8.5a 🔴 GIỚI HẠN THẬT — đọc trước khi hứa

**t2v gen TỪNG clip TỪ ĐẦU, không có character-lock.** Cùng một câu chữ vẫn ra hai khuôn mặt khác
nhau; hai clip liền nhau vẫn là hai lần vẽ độc lập, **pixel ở chỗ cắt không bao giờ khớp**. Nên
"đồng nhất" ở đây là đồng nhất **những thứ model giữ được**, và "nối liền" là nối liền **LOGIC HÀNH
ĐỘNG** để mắt đọc thành liên tục — không phải nối liền khung hình.

| giữ được | KHÔNG giữ được |
|---|---|
| màu mũ · màu áo · màu + chất liệu vật đeo | khuôn mặt · dáng mặt · tuổi cụ thể |
| hướng di chuyển · bối cảnh · giờ trong ngày | vị trí chính xác của chủ thể trong khung |
| tư thế/trạng thái mô tả bằng chữ | ánh sáng khớp từng pixel ở chỗ cắt |

⭐ **Bằng chứng từ video 10:** clip **GIẤU MẶT** (H1 mở bài · 13:14 · C3 vòng 5) đồng nhất tuyệt
đối; clip **THẤY MẶT** thì mỗi lần một người. ⇒ Đây là đòn bẩy mạnh nhất đang có.

### 8.5b LUẬT NHÂN VẬT (cast lock)

1. **Trần 3 CAST có tên cho cả video**, **≤2 CAST trong một cảnh**. Mỗi cast thêm là một trục
   sai lệch nữa. (gate ⚠️)
   🔴 **SỬA 2026-09-10 — câu này trước đây ghi "≤2 NGƯỜI trong một cảnh", và đó là sai tầng.**
   Nó gộp hai thứ khác nhau vào một con số:
   · **CAST** có danh tính, tái xuất hiện nhiều clip ⇒ **phải đồng nhất** ⇒ mỗi người thêm đúng là
     một trục sai lệch ⇒ trần 2 là **đúng, giữ nguyên**.
   · **NGƯỜI NỀN** vô danh, chỉ xuất hiện **một** clip ⇒ **không phải đồng nhất với bất cứ gì** ⇒
     **không sinh trục sai lệch nào**. Trần 2 áp lên nhóm này là vô cớ.
   **Cái giá đã đo được (video 11, 154 shot):** 50% shot **0 người** · 36% shot **1 người** ⇒ **86%
   vắng tanh**, trong khi LỜI KỂ nhắc đông người **30 lần** (列 ×3 · 並び ×2 · 満員 · 混んで ·
   町全体 · 押され · 何千人 ×2…). **Hình chỏi lời** — đó là lỗi thật, không phải sở thích.
   ⇒ Người nền khai bằng **§3.5 EXTRAS** (`videogen_lib.EXTRAS` + `CROWD` trong `gen_prompts.py`),
   và **KHÔNG tính vào trần này**.
   ⛔ **Nhưng người nền phải VÔ DANH** — `EXTRA_LOCK` dán kèm mọi lần: quay lưng hoặc nhìn ngang,
   mờ ngoài tiêu điểm, không mặt nào hướng camera. Thiếu nó thì model vẽ mặt đám đông ⇒ mặt
   morphing ⇒ đám đông **thành một trục sai lệch thật**, tức đúng cái lỗ mà luật cũ tưởng nó bịt.
2. **Nhân vật xuất hiện ≥2 clip thì PHẢI giấu mặt** — framing `behind` / `ots` / `high`, hoặc trong
   act có `seen from behind` · `looking down` · `head bowed`. (gate ⚠️ chỉ đích danh clip nào hở mặt)
3. Mô tả cast **khoá đúng 3 thứ ổn định**: **màu mũ + màu áo + màu/chất liệu vật đeo**. ⛔ Không tả
   mặt, không tả tuổi, không tả kiểu tóc — model tự chế và mỗi lần một khác.
4. Descriptor viết **một lần trong `C`**, mọi cảnh dùng token `A_XXX`. ⛔ Cấm paraphrase (gate đã có).

### 8.5c LUẬT NỐI LIỀN (chain)

Khai báo cảnh theo **CHUỖI 2–4 clip** cùng khối, cùng bối cảnh, cùng nhân vật. `S` nhận thêm 2 trường:

```python
# (sid, blk, act, preset, framing, tier, chain, out)
("A1", "MICHI", "A_ME walks away from the camera …", "michi_asa", "behind", "Q",
 "ch1", "A_ME is standing still at the corner with the satchel still on its back"),
("A2", "MICHI", "the figure shifts its weight …",    "michi_asa", "behind", "Q",
 "ch1", "A_ME has stepped off the kerb"),
("A3", "MICHI", "A_ME crosses the lane away …",      "michi_asa", "behind", "Q", "ch1", None),
```

- **`chain`** = id chuỗi · **`out`** = trạng thái KẾT của cảnh (vị trí + tư thế + vật), **≤110 ký**.
- `build()` tự mở cảnh sau bằng: `continuing in the same place a moment later, <out cảnh trước>, and …`
- ⭐ Trong mệnh đề nối, cast token bung thành **`the same figure` / `the same woman`**, KHÔNG bung lại
  cả mô tả dài — chữ **"the same"** mới là thứ nói với model rằng đây là cùng một người, còn bung mô
  tả dài chỉ khiến nó vẽ lại từ đầu (và prompt phình: đo được 1.963 → 1.748 ký).
- Cảnh **cuối chuỗi** để `out=None`.

**5 gate máy của chuỗi** (`videogen_lib.gate`):

| | luật | mức |
|---|---|---|
| C1 | các cảnh của một chuỗi phải **liền nhau trong `S`** (để file FLOW gen đúng thứ tự) | 🔴 |
| C2 | cùng chuỗi = **cùng preset bối cảnh** — đổi preset giữa chuỗi là đổi cảnh, hết nối liền | 🔴 |
| C3 | cảnh không phải cuối chuỗi **bắt buộc có `out`** | 🔴 |
| C4 | **cấm lật ngược hướng**: đang `away from the camera` mà cảnh sau `toward the camera` | 🔴 |
| C5 | framing không nhảy quá 2 bậc trong chuỗi | ⚠️ |

**Đã kiểm chứng ngược** (chuỗi hỏng cố ý): bắt đúng 🔴 C2 + 🔴 C4, kèm ⚠️ framing nhảy xa và ⚠️ hở mặt.

### 8.5d Ba việc ở tầng KỊCH BẢN, không phải tầng prompt

1. **Mỗi khối script = một chuỗi**, đừng rải nhân vật khắp bài. Nhân vật xuyên bài (kiểu 緑のおばさん
   của video 10) chỉ nên tái xuất hiện ở **2–3 mốc có ý nghĩa**, mỗi mốc là một chuỗi giấu mặt.
2. **Gap ≤ 8,0s mỗi clip** (§2.0b của `audience-45plus`, và lý do kỹ thuật ở log video 10 mục (h)):
   clip không phải kéo ⇒ hết judder ⇒ chuỗi mới thật sự mượt.
3. **Thứ tự trong `S` = thứ tự gen** — chuỗi phải nằm liền khối, vì `videogen_FLOW.txt` bơm theo dòng.

## 8.6 ⭐⭐ NỐI LIỀN LÀ **MẶC ĐỊNH** — và gốc rễ nằm ở KỊCH BẢN (user chốt 2026-09-06)

> user: *"Tao thấy mỗi video như là 1 cảnh riêng biệt ấy, nó không nối liền với hành động của
> video trước."* (mỗi "video" = mỗi clip 8 giây Flow xuất ra)

### 8.6a Số đo trên video 10 — vấn đề to cỡ nào

| | |
|---|---|
| cặp cảnh đứng liền nhau, **cùng khối + cùng bối cảnh** | **57 / 120** |
| trong đó đã nối liền | **0** |
| **độ liền mạch** | **0%** |
| cảnh rời bị gate bắt | **65** |
| khối mở bằng cảnh **đứng sẵn** (không ai đi tới) | **6** (SHUGO · HINGE · Q1 · KAERI1 · KAERI2 · YUGATA) |

⇒ Không phải "vài chỗ đứt". Là **mọi chỗ**, vì §8.5c làm `chain` thành **tuỳ chọn** nên mặc định
vẫn là rời. **Đảo mặc định.**

### 8.6b Máy gom chỗ, người viết nối

```python
from videogen_lib import autochain, linkage
S = autochain(S, cut={"HG1", "E1"})     # cut = chỗ CỐ Ý cắt hẳn (đổi cảnh/đổi thời điểm)
```
`autochain()` tự gom mọi cảnh **liền nhau cùng (khối, preset)** thành chuỗi — trên video 10 nó gom
được **32 chuỗi / 89 trong 121 cảnh** trong một lệnh.
⛔ Nhưng **`out` thì máy không bịa hộ** — đó là việc sáng tác. Gate C3 đòi bằng được: thiếu `out` = 🔴.

**Thước đo mới, in ở mọi lượt gate:**
```
do LIEN MACH        : 41/57 cap da noi (72%)  [muc tieu >=70%]
```

### 8.6c 🔴 GỐC RỄ Ở KỊCH BẢN, không ở prompt

Kịch bản video 10 là **danh mục 30 mục** (「二十一点目」「二十二点目」…). Mỗi 点 là một chủ đề
riêng ⇒ lớp hình **tất yếu** thành 30 vignette rời. Prompt có nối đến mấy mà lời kể nhảy cóc từ
mục này sang mục kia thì mắt vẫn thấy đứt.

Video 10 **đã có xương sống đúng** (*"một con đường, 7:40 sáng → 5 giờ chiều"*) — nhưng kịch bản
**không bao giờ đi bộ giữa hai điểm**, nó chỉ liệt kê. Ba luật cho video 11:

1. **Mỗi khối mở bằng nhịp ĐẾN NƠI.** Nhân vật **đi tới** chỗ đó từ chỗ trước, rồi mới vào nội
   dung điểm mới. ⛔ Cấm mở khối bằng cảnh đứng sẵn tại chỗ. (gate **C7** ⚠️)
2. **Lời kể cũng phải đi bộ.** Chuyển đoạn dùng câu nối theo KHÔNG GIAN + THỜI GIAN
   (「そこから、少し歩くと」「その角を曲がると」「橋を渡ったところに」), ⛔ không nhảy thẳng sang
   「二十二点目」. Con số thứ tự vẫn giữ (kênh THÔNG TIN được đếm — `humanize-script-voice.md` §1.2
   chỉ cấm chouhen), nhưng **trước con số phải có một bước chân**.
3. **`out` của cảnh cuối khối = `in` của cảnh đầu khối sau.** Đây là chỗ nối hai khối; viết ra
   thành chữ trong script (mục Cấu trúc), không để trong đầu.

### 8.6d Bảy gate của chuỗi

| | luật | mức |
|---|---|---|
| C1 | cảnh cùng chuỗi phải **liền nhau trong `S`** | 🔴 |
| C2 | cùng chuỗi = **cùng preset** | 🔴 |
| C3 | cảnh không phải cuối chuỗi **bắt buộc có `out`** | 🔴 |
| C4 | **cấm lật ngược hướng** (đang đi xa ↔ đi về phía camera) | 🔴 |
| C5 | framing không nhảy quá 2 bậc trong chuỗi | ⚠️ |
| **C6** | **cảnh RỜI**: đứng cạnh nhau, cùng khối + cùng bối cảnh mà không nối | 🔴 strict / ⚠️ vá |
| **C7** | **khối mở bằng cảnh đứng sẵn** thay vì nhịp đến nơi | ⚠️ |

### 8.6e 🔒 KHOÁ CÚ MÁY — đòn bẩy mạnh nhất còn lại khi KHÔNG có Extend

Flow **có** `Extend` (gen tiếp từ giây cuối clip trước = liền ở mức pixel) và `Ingredients to Video`
(khoá khuôn mặt bằng ảnh tham chiếu). ⛔ **Nhưng cả hai phải bấm tay trong UI Flow**, mà kênh này gen
bằng **tool ngoài** (user chốt 2026-09-06) ⇒ **không dùng được**. Đường còn lại là text, và đây là
cách vắt kiệt nó:

1. **`CHAIN_LOCK` tự chèn vào mọi cảnh không phải đầu chuỗi** (thư viện làm, không phải gõ tay):
   > *the camera has not moved since the previous shot, the same lens height and the same distance to
   > the subject, the light comes from the same direction and the shadows fall the same way*

   Ba thứ mắt bắt ngay ở chỗ cắt: **góc máy · hướng nắng · cỡ chủ thể trong khung**. Không nói ra thì
   model tự chọn lại cả ba ở mỗi lần gen.
2. **Trong một chuỗi, framing phải GIỐNG HỆT** (siết từ "không nhảy quá 2 bậc"). Đổi framing = đổi cú
   máy = mất cảm giác liên tục. Muốn đổi cú máy thì **cắt chuỗi** (`cut={...}`), đừng đổi giữa chuỗi.
3. Ánh sáng đã tự khoá nhờ **C2 (cùng preset)** — preset chứa cả mô tả giờ/ánh sáng.

### 8.6g ⭐⭐ CAST PLATE — 1 ẢNH THAM CHIẾU khoá nhân vật (user chốt 2026-09-06)

Tool ngoài user đang dùng nhận **text + 1 ảnh**, và ảnh đó là **ảnh THAM CHIẾU** (không phải start
frame). Vậy phân vai rạch ròi:

| | khoá bằng gì |
|---|---|
| **đồng nhất NHÂN VẬT** | ✅ **ảnh tham chiếu** (cast plate) |
| **nối liền HÀNH ĐỘNG** | `chain` + `out` + `CHAIN_LOCK` (text) — ảnh **không** làm được |

**Vì chỉ 1 ảnh/lần gen ⇒ mỗi clip khoá được ĐÚNG MỘT nhân vật.** Đây là lý do kỹ thuật cho trần
**≤2 người/cảnh · ≤3 nhân vật/video** ở §8.5b — không phải luật cho đẹp.

**Thi hành:**
```python
PLATES = {"ME": "cast/me.png", "MIDORI": "cast/midori.png"}   # thu tu = uu tien khi canh co 2 nguoi
write_plate_prompts(C, PLATES, ".")        # -> cast_plates_FLOW.txt (1 prompt/dong) + TENFILE
rows = build(S, P, C, plates=PLATES)       # nhan vat co plate: KHONG ta lai quan ao nua
IMG  = plate_map(S, PLATES)                # {sid: duong dan anh} — clip nao kem anh nao
```

🔴 **Nhân vật đã có ảnh thì KHÔNG tả lại quần áo/màu trong prompt nữa** — `expand_with_plate()` tự
đổi thành `the figure matching the reference image exactly`. Đưa **cả ảnh lẫn mô tả dài** là cho model
**hai nguồn có thể mâu thuẫn**, nó sẽ trộn hai thứ lại. **Ảnh cho hình dạng, chữ cho hành động.**
Nhân vật *không* có plate thì vẫn bung mô tả đầy đủ như cũ.

**Ảnh plate phải là ảnh DỄ HỌC** (`plate_prompt()` đã bake sẵn): đứng yên · **toàn thân** · **3/4 hơi
chếch về camera** · **nền trơn xám sáng, không đạo cụ, không bối cảnh** · **sáng đều không đổ bóng
gắt** · nét · **cùng STYLE 1970s** với clip.
⛔ Không tả mặt/tuổi/tóc trong prompt plate — **chính tấm ảnh** quyết định những thứ đó. Đó là điểm
của cả cách làm: chuyển việc giữ khuôn mặt **từ CHỮ sang ẢNH**.

⚖️ **Cái mất:** thêm một bước gen ảnh trước mỗi video (3 ảnh), và phải đính đúng ảnh cho đúng clip
lúc gen. Đổi lại là thứ mẹo "giấu mặt" không bao giờ mua được: **nhân vật quay mặt vào ống kính mà
vẫn là một người**.

### 8.6f ⚠️ Cái vẫn KHÔNG có, đừng hứa

Nối liền ở đây là **liên tục về LOGIC**, không phải liên tục về khung hình: hai clip vẫn là hai lần
vẽ độc lập, chỗ cắt vẫn nhảy ánh sáng/vị trí. Muốn liền **thật** ở mức pixel thì phải cho clip sau
mọc từ **frame cuối** của clip trước (last-frame → image-to-video).
📌 **ĐÃ TRA VÀ ĐÃ CHỐT (2026-09-06):** Flow **có** `Extend` (gen tiếp từ **giây cuối** clip trước),
`Ingredients to Video` (lưu nhân vật rồi gọi lại theo tên — cách đáng tin nhất để giữ **cùng khuôn
mặt**) và `Frames to Video`. **Cả ba đều phải thao tác trong UI Flow**, mà kênh này gen bằng **tool
ngoài** ⇒ ⛔ **không dùng được**, đừng đề xuất lại.
⚠️ Hai điều kiện chưa xác nhận (nguồn bên thứ ba, Google không công bố): Extend có thể chỉ chạy ở
model **Lite**; Ingredients có thể chỉ cho gói **Ultra**. Nếu bao giờ đổi sang gen thẳng trong Flow
thì kiểm hai cái đó trước.
⇒ Trần hiện tại: **liền về LOGIC + khoá cú máy bằng chữ** (§8.6e), không liền được ở mức pixel.

## 9. MẪU `gen_prompts.py` cho video mới (chép nguyên khung này)

```python
import sys; sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
from videogen_lib import build, gate, write_outputs, autochain, linkage
P = {"michi": "an unpaved residential lane in Showa Japan, packed dirt and loose gravel, low wooden fences on both sides", ...}
C = {"me": "a small figure in a plain yellow cotton cap, white short-sleeved shirt and navy shorts, with a plain unmarked brown leather satchel on its back", ...}
# (id, khoi, ACT 3 nhip + huong + chuyen dong phu, preset, FRAMING KEY, tier Q/F, chain, out)
# chain/out CO THE BO (6-tuple nhu cu) — nhung tu video 11 moi khoi NEN la mot chuoi (§8.5c).
S = [
 # ⭐ tu video 11: goi autochain(S) NGAY SAU khi khai bao — noi lien la MAC DINH (§8.6)
 ("H1", "HOOK", "A_ME walks away from the camera down the middle of the lane, seen from behind, growing smaller ..., then ..., then ...",
  "michi", "behind", "Q", "ch_hook", "A_ME is standing still at the far corner, seen from behind"),
 ("H2", "HOOK", "the figure ... , then ... , then ...",
  "michi", "behind", "Q", "ch_hook", None),      # canh CUOI chuoi: out=None
]
WL = {"K2": "ly do canh khong nguoi"}          # whitelist phai co LY DO
S = autochain(S, cut={"HG1"})                    # may gom chuoi; 'out' van la viec NGUOI VIET
rows = build(S, P, C)
n_red, _ = gate(rows, S, P, C, whitelist_no_human=WL, interior={"genkan_uchi"}, strict=True)
write_outputs(rows, ".")                         # videogen_FLOW.txt · TENFILE.txt · BLOCKS.md
sys.exit(1 if n_red else 0)
```

## 10. Ghi sổ

- **2026-09-06 — v2, ca gốc video 10.** Soi 121/121 clip (sheet 4-frame + sheet mép): **17 lỗi nặng · 15 nhẹ · 89 sạch
  · 120 khung phim**. 15/17 lỗi nặng là framing không thân. Gen lại **22 clip** theo v2 (`06_VIDEO/10_tsugakuro/REGEN_v2_FLOW.txt`);
  9 clip v1 đạt-mắt-nhưng-framing-cấm chỉ đổi prompt, không gen lại (01·05·13b·18·23·23c·23d·26·E13).
  **Chỉ tiêu:** ≤2/22 lỗi sau gen lại; không đạt → sửa công thức trước khi áp video 11.
- ✅ **2026-09-06 — KẾT QUẢ PHÉP THỬ: ĐẠT, 2/22 lỗi** (v1 nhóm này: **22/22 lỗi**). 20/22 sạch hoàn toàn.
  - **Hết sạch loại lỗi nặng nhất**: 0 cánh tay/chân lơ lửng, 0 vật biến hình, 0 quay mặt vào camera.
    `H1` (clip mở đầu) đi ra xa một mạch, không đảo chiều — đúng thứ user bắt. `25d` giờ có cả người ngồi
    ôm đầu gối (v1: chỉ bàn tay trên tường). `E15`/`E7` có chân **và** thân trên vạch trắng.
  - **2 lỗi còn lại:** `30b` người xuất hiện giữa clip rồi **biến mất ở frame cuối** (dù prompt có
    `remains in frame` — gate không đo được cái này, chỉ mắt thấy) · `06` **lệch nội dung** (prompt là
    thẻ tên → model cho ra cờ vàng; không dị dạng, chấp nhận được).
  - ⇒ **Ba luật hiệu quả nhất, xếp theo sức nặng:** ① framing có THÂN người (chữa 15/17 lỗi nặng)
    ② hướng tương đối camera (chữa H1) ③ vật `plain unmarked` + `the same X throughout` (chữa vật biến hình).
  - ⚠️ **Luật `remains in frame` là luật YẾU NHẤT** — `30b` vẫn mất chủ thể. Cảnh "người trong khung cửa
    sổ/khung hẹp" là ca khó riêng; lần sau tả **người TRƯỚC, khung SAU** (`A_HAHA stands at the open window…`
    thay vì `the window slides open and A_HAHA stands inside it`).
- Prompt v2 dài **1.200–1.700 ký** (v1: 800–1.040) do cast nguyên văn + negative đích danh. Chưa thấy Flow từ chối; nếu có thì rút ở P (bối cảnh), không rút ở NEGATIVE.

## §9 PHONG CÁCH QUAY = PHIM TƯ LIỆU QUAN SÁT (chốt 2026-09-11)

> user, sau khi tao cắt được clip thật `Creation of New Wealth 1960` vào video 11:
> *"tao muốn làm video AI như những video thật này"* → *"phong cách quay, cảnh quay, các hành động,
> nhân vật tao muốn thiết kế theo kiểu như thế"*.

🔴 **Bản STYLE cũ đang kéo model về phía ẢNH CHỤP TĨNH, không phải phim tư liệu.** Nguyên văn cũ:
`faded warm 1970s colour photography, low contrast, fine natural grain, soft natural light, slight vignette`.
Năm cụm đó — *faded · low contrast · grain · soft light · vignette* — đều là từ vựng của **ảnh hoài niệm**:
một chủ thể, nền mờ, ánh sáng dịu. Phim tư liệu thật thì ngược hẳn.

**Đo trên chính 2 phim trong kho** (`tools/measure_filmlook.py`, frame resize về cùng 720p):

| | phim thật (Japan Today 1959) | AI cảnh phố | AI trong nhà |
|---|---|---|---|
| bão hoà | 62,4 | **121,1** | **111,2** |
| nét (Laplacian) | 80,1 | **234,7** | 37,3 |
| hạt vùng phẳng | 17,8 | 7,4 | 1,3 |
| pixel trắng cháy | 0,0% | **9,0%** | 0,2% |

⚠️ **Đọc bảng này cho đúng — đây là chỗ tao đã hiểu sai một lượt.** Nhìn số thì kết luận tự nhiên là
"kéo AI về gần cột trái": giảm nét, thêm hạt, giả lập 16mm. **Sai.** User bác ngay: *"bỏ hạt đi nhé,
độ nét tăng lên, ý tao là PHONG CÁCH VIDEO chứ không phải những chỉ số đó"*. Cái giống nhau phải là
**cách quay**, không phải **chất phim**. Số chỉ dùng cho **một** việc: trắng cháy 9% → 0%.

### Thi hành

| tầng | làm gì |
|---|---|
| `videogen_lib.STYLE` | `16mm colour observational documentary footage, crisp and clearly resolved, true-to-life natural colour, natural available light, **deep focus so both the foreground and the background stay readable**, **candid unposed action filmed from a respectful distance, nobody aware of the camera**, **life going on at several distances in the same frame**, natural imperfect framing with the subject slightly off-centre` |
| `videogen_lib.MOTION` | thêm `the camera holds one position and observes` — máy KHÔNG bám chủ thể, cảnh tự diễn ra trước một máy đứng yên |
| `videogen_lib.AVOID` | ⛔ bỏ `clean digital sharpness` (user muốn NÉT) · thêm `not posed for the camera · nobody looking at the camera · no staged tableau · no single person alone on an empty set · no shallow blurred background · no cinematic bokeh · no dramatic studio lighting · no colour-graded film-look` |
| hậu kỳ `tools/grade_clips.py` | **chỉ 2 việc**: highlight rolloff (9,0% → 0,0% pixel cháy) + `unsharp 0.80` (nét 235 → 454). ⛔ KHÔNG hạt, KHÔNG làm mềm, KHÔNG gate weave |

Bản STYLE cũ giữ ở `tools/videogen_lib.py.bak_style_20260911`.

### Ba đặc điểm đọc được từ frame phim thật, để viết ACT theo

1. **Ba cự ly trong một khung** — tiền cảnh có người bị cắt nửa, trung cảnh là chủ thể, hậu cảnh còn
   người khác đang làm việc riêng. Khung của `Creation of New Wealth` @18:16: ~10 công nhân ở 3 lớp sâu.
2. **Chủ thể là MỘT PHẦN của cảnh, không phải trung tâm sân khấu.** Máy móc/quầy hàng/đường phố chiếm
   phần lớn khung; người nằm trong đó.
3. **Không ai diễn cho máy.** Người đi ngang, che khuất, quay lưng — khung là "bắt được" chứ không "sắp đặt".

⚠️ **Cái chưa làm:** ba điểm trên mới nằm ở STYLE (áp cho mọi prompt) và ở lớp `EXTRAS/crowd`
(bật theo preset). Chưa có **gate máy** đo "ACT có mấy cự ly". Chừng nào chưa có, viết ACT phải tự
kiểm bằng câu hỏi: *cảnh này có ai khác đang làm việc riêng ở lớp sau không?*

### §9.1 Hai bệnh của ACT mà gate cũ KHÔNG bắt được (user chỉ 2026-09-11)

Cả hai lọt qua toàn bộ 6 luật ACT hiện có (token cast · đúng 2 `then` · hướng tương đối camera ·
≥1 chuyển động phụ · một vật giữ nguyên · tư thế đơn giản) — vì cả 6 luật đo **hình thức của câu**,
không đo **cảnh có gì xảy ra không**.

**① Tả ĐỘNG TÁC mà không tả VẬT BIẾN ĐỔI.** user: *"hành động cho tiền vào phong bì thì phong bì
phải dày lên chứ"*. Bản cũ: `he slides a thick bundle of banknotes into the envelope` → model vẽ
phong bì **phẳng từ đầu đến cuối**. Cả video này bán chữ 「厚み」 (bề dày), nên phong bì không phồng
lên là mất đúng cái đắt giá nhất.
⇒ **Luật: ACT phải ghi CÁI THAY ĐỔI TRÊN VẬT, không chỉ ghi tay làm gì.**
`…and the envelope swells and grows visibly thicker as the stack goes in` → `folds the flap down
**over the bulge**` → `squares **the fat envelope**`. Nhắc 3 lần, mỗi nhịp một lần.
Quét cả bài: chỉ còn **C15 · J6** cùng bệnh.

**② Nhịp 3 CHẾT.** user: *"hành động gấp giấy xong để đó à, trông nhàm chán"*. Bản cũ của M17 kết
bằng `then lets his hand still` — nghĩa đen là **không làm gì**. Ba nhịp mà nhịp cuối rỗng thì cảnh
chết đúng chỗ đáng lẽ phải có ý.
⇒ Nhịp 3 phải **chở một ý mới**, thường là *phản ứng* hoặc *giấu đi*. M17 neo vào 「三点目、隣の封筒」
(phong bì của **người bên cạnh**) nên nhịp 3 đúng phải là: **liếc sang phong bi người ta → úp phong bì
của mình vào chân để giấu**. So sánh rồi che đi — đó mới là cảnh.

⚠️ **Quét ra 16 shot khớp mẫu ②, nhưng 12 cái là CỐ Ý — đừng sửa hàng loạt.** Đứng yên chính là nội
dung ở: `G7` 「見ないことが、礼儀だった」 · `S17` 「手のひらに現れた」 · `G10` 「何を話しているかは、
分からない」 · `E2`/`E10` (khối END bán sự vắng mặt) · `K6b`/`K7` (nắm ngực trên tàu = lo). Và phần
lớn kết bằng **chuyển động phụ của bối cảnh** (dây đèn lắc, rèm động, bóng dịch) — đúng công thức.
Chết thật chỉ có **4**: `M17` `G4` (đã sửa) · `G1` `F1` (đứng yên trước cửa/quầy) · `S7`.
⇒ Phân biệt: *nhịp 3 có thêm một ý không?* Có → giữ. Chỉ "đứng yên cho bối cảnh động" → chết.

**③ Động tác AI luôn làm hỏng — thêm ĐẠP XE vào danh sách cấm.** user: *"hành động đạp xe đang sai"*.
Cùng họ với `hands only` (14/21 clip hỏng, §8): chân–bàn đạp–xích không bao giờ khớp, hay đạp ngược.
⇒ **Xe đạp chỉ được DẮT (`wheels … from left to right`), không được ĐẠP.** Và đừng đặt framing `low`
(ngang gối) cho cảnh có xe — nó chĩa thẳng vào đúng chỗ hỏng. Bản cũ dính cả ba: đạp + `low` +
`rides towards the camera` (câu cuối còn đánh nhau với AVOID `turning to face the camera`).

### §9.2 "Cảnh nhạt" đôi khi là cảnh **SAI NEO** — soi lời trước khi làm cho nó sinh động

user: *"cái `videogen_FIX3_FLOW.txt` toàn hành động nhạt nhẽo"* (2026-09-11, lô 13 shot khối
茶の間/へそくり). Đi sửa thì bắt được một cái nặng hơn "nhạt":

| | |
|---|---|
| lời @535s | 「どの封筒が薄いかを、母親は、**開けなくても手で覚えていた**」 — sờ là biết phong bì nào mỏng |
| ACT cũ (C12) | `she sets the pencil down across the open ledger` — **không liên quan gì** |

Cảnh đó nhạt **vì nó không phải cảnh của câu đó**. Nếu chỉ "cho nó sinh động hơn" mà không soi lời
thì sẽ ra một cảnh sôi động nhưng vẫn sai. ⇒ **Thấy một cảnh nhạt: kiểm NEO trước, sửa văn sau.**

⭐ **Và chỗ kịch tính bỏ phí lớn nhất: khối へそくり là chuyện GIẤU GIẾM.** Lời có sẵn
「父親が知らないところで、家が回っていた」 — nhưng 12 shot của khối chỉ tả *thao tác ngăn kéo*
(mở ra, giữ, đẩy vào, ấn lại). Viết lại theo mạch giấu giếm thì cùng một hành động thành có gì để xem:
ngoái nhìn ra hành lang trước khi mở · **bóng người lướt qua cửa giấy** rồi vội ấn ngăn kéo phẳng xuống.
Không thêm một vật nào, không bịa một câu nào.

📌 Ba thứ luôn dùng được khi một khối bị nhạt, xếp theo độ rẻ:
① **cho vật biến đổi** (phong bì phồng/xẹp, giấy quạt ra) ② **cho người thứ hai chạm vào việc đó**
(đứa trẻ gạt thẳng từng phong bì) ③ **tìm xung đột đã có sẵn trong lời** (giấu giếm, so bì, thiếu tiền).

### §9.3 ⭐⭐ CHUYỂN ĐỘNG SƯỢNG — 7 nguyên nhân đo được (user chốt 2026-09-11, lô 165 prompt video 12)

> user: *"hành động quạt nhìn nó bị sượng"* → *"lỗi quá"* → *"làm sao chuyển động phải mượt mà và đúng"*.
> Soi cả 165 prompt: **62 shot hỏng**, và **3/7 nguyên nhân nằm ở TẦNG TOOL** — tức mọi video sau
> cũng sẽ dính nếu chỉ sửa lẻ từng prompt.

**A. Ba lỗi TẦNG TOOL (đã vá `videogen_lib.py`, backup `.bak_motion_20260911`):**

| # | Lỗi | Số shot | Vá thế nào |
|---|---|---|---|
| T1 | 🔴 **`expand()` thay token theo THỨ TỰ DICT** ⇒ `A_KO` ăn trước `A_KO2`/`A_KORI`, để lại rác `barefoot2` / `barefootRI` giữa câu | 7 | thay theo **ĐỘ DÀI GIẢM DẦN**. ⚠️ Rác này trông hệt lỗi gõ nên dễ đi sửa nhầm ở prompt |
| T2 | 🔴 **`FRAMINGS['medium']` và `['ots']` chứa `face out of frame`** | **68/111** | bỏ hẳn. Nó là tàn dư của cách né filter trẻ em; §7 nấc 1 nói đường lui đúng là `behind`, **không phải cắt đầu**. Cắt đầu lúc tay vươn quá đầu / áp gáy / trao vật ⇒ ra **tay không đầu**, đúng thứ AVOID đang cấm |
| T3 | **MOTION không có một chữ nào về ĐỘ MƯỢT** | 165 | thêm `at one even speed from first frame to last` · `the weight shifting through the body before each movement` · `every action carried through once in a single unbroken arc and never undone`; AVOID thêm `stuttering or jerky motion, speed ramping, slow motion, skipped or repeated frames, looping or repeating action, an action played and then undone, rubbery bending limbs, feet sliding across the ground, floating or gliding movement` |

**B. Bốn lỗi TẦNG ACT (đã sửa 62 shot):**

| # | Lỗi | Số | Vì sao ra sượng |
|---|---|---|---|
| P1 | **ĐẢO ĐỘNG TÁC** — giơ/hạ · mở/đóng · cúi/ngẩng · đặt/nhấc · chạy đi/quay lại | 37 | AVOID đã cấm `reversing motion` ⇒ **prompt tự đánh nhau với negative của chính nó**. Đây là nguyên nhân #1 |
| P2 | **LẶP** — làm → dừng → làm lại (cưa/dừng/cưa · rót/rót lại · xoay núm/xoay lại) | 4 | model dựng thành loop; loop trong 8 giây = giật |
| P3 | **ĐẾM SỐ LẦN** (`twice`) | 10 | ra động tác **máy đếm nhịp**, biên độ đều tăm tắp. Thay bằng `loose flicks of the wrist … a different angle each time` |
| P4 | **VẬT CỰC NHỎ + ĐẦU NGÓN TAY** (hạt muối · mẩu đá · hạt dưa · quân cờ · 2 ngón kẹp) | 16 | cùng họ `hands only` (14/21 hỏng, §8). Chữa bằng **tả KẾT QUẢ, không tả ngón tay**: `a scatter of white grains appears across the red flesh` |
| P5 | **QUẠT TRÒN (団扇) mà `opens`/`folds`/`closes`** | 11 | 団扇 **cứng, không mở được**; 扇子 mới xếp. Hai lệnh trái nhau ⇒ model **morph cái quạt** |
| P6 | **VẬT/HIỆN TƯỢNG VÔ HÌNH** làm hành động chính (`the cold air of the shaft` · `breathes in`) | 3 | model không có gì để vẽ ⇒ tám giây không sự kiện. Thay bằng thứ nhìn thấy được (nhúng tay vào nước · **vai áo thẫm nước lại**) |
| P7 | **ĐỔI CAO ĐỘ TOÀN THÂN ≥2 lần** (đứng→xổm→đứng) | 4 | chỗ AI vỡ nhiều nhất. Một clip **một tư thế** |

**C. 🔴 `run` — từ báo oan thứ TƯ, sau `drift`(v2) · `round`(09-10) · `head`(09-11).**
Gate chấm 8 shot "di chuyển không có hướng", **6 là oan**: `the melt **runs** down` · `condensation
**runs** down` · `the water is **running** hard` · `lets the slats **run** back down` (chất lỏng/vật),
và `**runs** the door half shut` · `**runs** the flat of her hand along` (**ngoại động từ**).
Vá: thêm danh từ chất lỏng/vật vào `SUBJ_AMBIENT`, và tách `run` khỏi nhóm chung với lookahead
`(?!\s+(?:the|a|an|his|her|its|their|both|two)\b)` — **chạy bộ không bao giờ có tân ngữ trực tiếp**.
📌 Bốn lần cùng một khuôn ⇒ **thêm bất kỳ động từ nào vào `MOVE_VERBS` thì phải quét cả repo tìm
nghĩa thứ hai của nó trước**, đừng đợi gate báo oan rồi mới sửa.

**D. Thứ tự chạy (đã kiểm, 3 vòng mới sạch):**
`sửa tool → sửa ACT → gate → gate báo oan thì SỬA GATE (không sửa nội dung) → gate lại`.
Vòng 1 gate chặn 17 · vòng 2 chặn 12 · vòng 3 chặn 1 · vòng 4 **✅ SẠCH 165/165**.
⚠️ Gate đã bắt đúng **11 chỗ tôi tự làm hỏng khi viết lại** (đánh rơi chuyển động phụ / mất hướng
camera) — đừng bỏ qua gate chỉ vì "mình vừa viết cẩn thận".

**E. Lỗi preset lộ ra cùng lượt:** `G12` (tháo mùng buổi sáng) dùng preset `zashiki` = *"at night …
dark garden"*. Đã thêm preset **`zashiki_asa`**. ⇒ **Mỗi lần chép một shot sang thời khắc khác trong
ngày, preset phải đổi theo** — lỗi này im lặng tuyệt đối, không gate nào bắt.


## §10 ⭐⭐ BA LUẬT t2v RÚT TỪ VIDEO 12 (chốt 2026-09-12, 165 clip, 3 vòng gen)

### 10.1 🔴 CLIP 8 GIÂY MÀ HÀNH ĐỘNG CHỈ 2 GIÂY → MODEL BÙ BẰNG CÁCH **ĐỨNG YÊN**

**Ca đo:** slot 72, lời dẫn 「喉が渇いても、水飲み場は、通り過ぎる」 (khát cũng đi thẳng qua vòi nước).
- Vòng 1: ACT ghi `walks past the row of taps without slowing, then turns his head toward the running water` → thằng bé **dừng lại, cúi đầu, với tay xuống bồn**.
- Vòng 2: thêm `never slowing and never stopping, neither hand ever leaving his side, face held forward` → nó **đứng nguyên một chỗ cạnh bồn 3 giây**, đầu cúi. Đo bằng 8 frame liên tiếp cách 0,42 s: bàn chân **không nhích**.
- Vòng 3: đổi cách viết → ĐẠT.

**Cơ chế:** "đi ngang qua" tốn ~2 s. Còn 6 s model phải lấp. Nó lấp bằng cách cho nhân vật đứng yên, và đứng **ngay tại vật giàu chi tiết nhất khung** — tức đúng cái vật mà luận điểm đang bảo là "không đụng tới".

⛔ **Viết thêm câu cấm là vô ích.** `never slowing`, `never stopping` không phải hành động để diễn; model không có gì để làm trong 6 giây đó.

✅ **Cách sửa: GIAO ĐỦ VIỆC CHO TRỌN 8 GIÂY**, bằng quan hệ với **mép khung** (giống §2 thumbnail: model nghe vị trí, không nghe thời lượng):
```
comes into the picture at the far left edge already in mid-stride and crosses the whole width
of the open ground from left to right at one unbroken walking pace, then ... , then keeps the
same pace all the way to the right edge and goes out of frame
```
📌 Áp cho mọi ACT loại **DI CHUYỂN NGANG QUA**: vào mép nào, đi hết cái gì, ra mép nào.

### 10.2 🔴 CÂU HƯỚNG SỰ CHÚ Ý VỀ PHÍA VẬT → t2v BIẾN THÀNH **TƯƠNG TÁC VỚI VẬT**

`turns his head toward the running water as he passes` → model hiểu thành "ghé vào lấy nước".
Câu này do chính mình thêm để cảnh đỡ khô, và nó **phản lại lời dẫn**.

⛔ **Ở cảnh mà luận điểm là "KHÔNG làm X": tuyệt đối không nhắc X kèm bất kỳ động từ hướng tâm nào**
(`toward`, `at`, `for`, `glance`, `look`, `reach`, `lean`). Chỉ được viết phủ định + **cho nhân vật một đích khác** (đi tới mép khung, nhìn thẳng đường trước mặt).

📌 Đây là **lần thứ 2** cùng một lỗi: lần 1 là C13 (bước qua bồn nước, video 12). Sửa C13 xong **không rà lại các cảnh cùng bối cảnh** nên slot 72 sống sót. ⇒ **Sửa một cảnh thì phải grep cả lô theo TỪ KHOÁ BỐI CẢNH**, không chỉ sửa cái đang bị chỉ.

### 10.3 🔴 SOI FRAME RẢI ĐỀU **KHÔNG** BẮT ĐƯỢC "NHÂN VẬT ĐỨNG YÊN"

9 frame rải đều trên 8 giây → 3 frame liên tiếp nhìn như đang đi (dáng người gần giống nhau).
Chỉ khi rút **8 frame liên tiếp cách 0,4 s và so VỊ TRÍ BÀN CHÂN** mới thấy nó đứng.

✅ **Phép nghiệm thu cho cảnh có DI CHUYỂN:** rút frame liên tiếp, nhìn **điểm tiếp đất**, không nhìn dáng.
Cảnh thao tác tại chỗ (MANIP) thì rải đều vẫn đủ.
