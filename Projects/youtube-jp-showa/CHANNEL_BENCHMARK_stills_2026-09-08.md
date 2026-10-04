# CHANNEL_BENCHMARK — MỔ LỚP HÌNH 3 VIDEO 191K–232K VIEW (đo 2026-09-08)

> User đưa 3 file mp4 (`C:\Users\tuana\Downloads\Showa`) và bảo *"mổ xẻ và phân tích phong cách làm video"* + *"nếu nó là ảnh tĩnh thì từ ảnh tĩnh đó hóa động cho tao"*.
> **Mọi số dưới đây đo bằng máy** (ffprobe · ffmpeg · OpenCV · YouTube Data API), không phải cảm giác.
> ⚠️ Không phải "triệu view" — thật là **191.738 · 219.055 · 232.737**. Kênh `あの頃の昭和` tổng 3,33M.
> Ba video này **chính là nguồn của `kichban1/2/3`** đã mổ phần LỜI ở `05_SCRIPT_FORMULA.md`. Lần này mổ phần **HÌNH**.

## 0. KẾT LUẬN 1 DÒNG

**Cả 3 video 191–232K view đều là ẢNH TĨNH 100% — 0 pan, 0 zoom, 0 clip động.** Hai video của `あの頃の昭和` giữ **một tấm ảnh 15,8–18,0 giây** (max 47–49s), cả bài chỉ **62–65 ảnh cho 19–21 phút**. Thứ duy nhất động trong khung là **phụ đề** và **một chip tiêu đề ở góc**.

⇒ Hai luật lớn của mình bị phủ định: **① trần ~6 giây/frame** · **② sàn "ảnh chính đổi ≤9,0s"** (`audience-45plus.md` §2.0b).

🔴 **CẬP NHẬT CUỐI NGÀY — user chốt GIỮ t2v (lượt 2): *"viết lại cho tao thành prompt video đi. Chú ý là video tao sinh ra tối đa được 8s thôi"*.**
Tức bằng chứng "ảnh tĩnh là đủ" **không** dẫn tới việc bỏ t2v; nó dẫn tới hai thứ khác:
- **Trần 8s/clip của máy gen làm Style A BẤT KHẢ THI** (không clip 8s nào phủ nổi một ảnh giữ 16–49 giây) ⇒ kênh chạy **Style B của bản 219K** (giữ 5,0s/cảnh, chuyển mềm nhiều).
- **Ảnh tĩnh + hóa động (§5) xuống vai ĐƯỜNG LUI** — dùng khi hết credit t2v hoặc cảnh nào t2v gen mãi không đạt. Tool đã dựng và đã đo xong.

## 1. BA VIDEO — metadata

| | E7dF | QeHE | hmDu |
|---|---|---|---|
| kênh | **昭和の音がする** | あの頃の昭和チャンネル | あの頃の昭和チャンネル |
| sub kênh / số video | **1.970 / 4 video** | 10.100 / 397 video | 10.100 / 397 |
| view | **219.055** | **232.737** | **191.738** |
| đăng | 2026-08-30 (9 ngày) | 2026-04-13 | 2026-03-09 |
| dài | 18′04 | 20′37 | 18′54 |
| like / comment | 1.437 / 276 | 2.191 / 623 | 1.579 / 239 |
| tag · độ dài desc | 48 tag · 2.426 ký | 79 tag · **283 ký** | 79 tag · **283 ký** |
| cat | 22 | 22 | 22 |
| nguồn script đã mổ | `kichban1.md` | `kichban2.md` | `kichban3.md` |

⭐⭐ **Phát hiện đắt nhất của lượt đo: `昭和の音がする` có ĐÚNG 4 VIDEO.**

| ngày | view | dài | tiêu đề |
|---|---|---|---|
| 2026-08-09 | **164.439** | 11′17 | 集団就職の夜行列車 |
| 2026-08-11 | **3.855** | **22′23** | 7万3千円の白黒テレビ |
| 2026-08-21 | **68.483** | 11′20 | 昭和の仕事図鑑10選 |
| 2026-08-30 | **219.055** | 18′04 | 昭和の常識20選 |

Kênh **3 tuần tuổi, 4 video, 1.970 sub → 449.099 view** = **112K view/video**, view/sub = **111×**.
🔴 **Nó phá tan lập luận "kênh mình mới nên chưa có rail"** — kênh này còn mới hơn, ít video hơn, và nổ ngay từ video ĐẦU TIÊN. Không cần back catalog, không cần 397 video như あの頃の昭和.
⚠️ Và video **chết** của nó (3.855) là video **DÀI NHẤT (22′23)** — 3 video ăn đều ở **11–18 phút**. Cùng chiều với dải 14,5–18′ mình đang chạy.

## 2. LỚP HÌNH — SỐ ĐO (cái đáng giá nhất)

Cách đo: rút frame **2 fps toàn video** ở 160×90 gray, **bỏ dải phụ đề (1/3 dưới) + dải chip (1/6 trên)**, tính MAD giữa hai frame liền nhau, gom frame liên tiếp thành MỘT lần chuyển cảnh.

| | E7dF 219K | QeHE 232K | hmDu 191K | **MÌNH (video 09/10/11)** |
|---|---|---|---|---|
| **số ảnh cả bài** | 161 | **65** | **62** | 121 clip · 135 clip |
| **ảnh/phút** | 8,9 | **3,2** | **3,3** | ~7,5 · 8,2 |
| **giữ mỗi ảnh (trung vị)** | 5,0s | **18,0s** | **15,8s** | 8s |
| giữ trung bình | 6,7s | 19,4s | 18,8s | 7,3s |
| **giữ dài nhất** | 26,5s | **47,0s** | **49,0s** | 9,9s |
| ảnh giữ **>10s** | 20% | **68%** | **55%** | 0% |
| ảnh giữ <3s | 14% | 6% | 5% | 0% |
| **MAD vùng ảnh (trung vị)** | 2,78 | **2,00** | **1,21** | — |
| frame ảnh **y hệt** frame trước | **39%** | **34%** | **44%** | — |
| dissolve ≥1,0s | 62 lần | 6 | 5 | 0 |

**Đọc:**
1. 🔴 **MAD vùng ảnh 1,2–2,8 = chỉ nhiễu nén.** Ảnh **không hề chuyển động**: không pan, không zoom (đo affine: hệ số zoom trung vị **1,0000**), không parallax. 34–44% frame **y hệt bit-đối-bit** frame trước.
2. **Hai phong cách khác nhau, cùng ~200K:**
   - **Style A — `あの頃の昭和`:** 62–65 ảnh / 20 phút · **giữ 16–18 giây/ảnh** · cắt cứng (5–6 dissolve cả bài).
   - **Style B — `昭和の音がする`:** 161 ảnh / 18 phút · giữ **5 giây/ảnh** · **62 dissolve dài** (chuyển mềm liên tục).
3. **Style A rẻ đến mức khó tin:** 62 ảnh cho một video 20 phút. Mình đang gen **135 clip video** cho một video 16,5 phút.

⚠️ **BẪY PHÉP ĐO — ghi lại vì suýt kết luận sai 3 lần trong một lượt:**
- `ffmpeg scdet` cho **270 cắt (13,1/phút)** ở QeHE, plateau ổn định từ th=0,03→0,10 nên trông rất đáng tin. **Sai:** phụ đề đổi chiếm cả dải ngang nên scene-score vượt 0,10 → **đếm phụ đề thành cắt cảnh**. Đo lại bằng MAD **đã bỏ dải phụ đề** → **3,2/phút**, lệch **4×**.
- Vòng đầu tao phân loại tĩnh/động bằng `cv2.findTransformECC` với **`MOTION_EUCLIDEAN` — khuôn này KHÔNG CÓ SCALE**, mà Ken Burns chủ yếu là ZOOM ⇒ mọi cú zoom bị chấm là "chuyển động thật". Đổi sang `MOTION_AFFINE` thì E7dF nhảy từ 16% → **78% tĩnh**.
- Vòng sau tao thử tách grain bằng `blur(d).mean()/d.mean()` → ra **1,0 khắp nơi**, vì **box-blur bảo toàn giá trị trung bình**. Chỉ số vô nghĩa.
⇒ Ba lần đều là **cùng một bệnh**: tin số trước khi soi mắt. Chỉ khi dán 6 frame liền nhau lên một sheet mới thấy ngay "ảnh y hệt, chỉ phụ đề đổi". Cùng họ `feedback_do_pixel_cua_so_quet` (lần thứ 5).

## 3. BỐ CỤC KHUNG + CHỮ

| | E7dF (昭和の音がする) | QeHE + hmDu (あの頃の昭和) |
|---|---|---|
| chip/banner tiêu đề | **không** | **banner 2 dòng góc trên-TRÁI, treo SUỐT video** (【昭和30年〜40年】+ tên bài) + số mục ④ đứng trước |
| chữ ở giây 0 | ⭐ **CÂU HOOK vẽ TO đè lên ảnh**: 「水を飲むと**バテる**」 (chữ バテる đỏ) | banner tiêu đề + phụ đề thường |
| phụ đề | 1 dòng, trắng viền đen, dải đáy (band 8–9) | **2 dòng, dải 60–80% chiều cao** (band 6–7, mực 28–55%) — cao hơn đáy khung |
| loudness | **−15,4 LUFS** · LRA 3,7 | −17,3 · LRA 2,5 · **−20,1** · LRA 2,5 |
| khoảng lặng ≥0,6s | **4 khoảng / 18 phút** (nói liền tù tì) | 51 khoảng (35s) · 42 khoảng (29s) |
| tốc độ đọc | **5,33 ký/s** | **5,44** · **5,92** |

**Đọc:**
- **Ta đọc chậm hơn winners 8–49%**: trục A **3,98 ký/s** · trục B 4,93 vs winners 5,33–5,92. Luật `audience-45plus.md` §5.2 (`speed ≤0,90`, "nói chậm cho tệp 45+") **không phải thứ winners làm** — và cả 3 đều ăn đúng tệp 45+.
- **Ta to hơn winners 2–6 dB** (chuẩn kênh −14 LUFS). LRA của họ 2,5–3,7 = rất phẳng, giống ta.
- ⭐ **Kỹ thuật rẻ nhất và mạnh nhất đo được: vẽ CÂU HOOK lên ảnh ở giây 0** (E7dF). Người xem đọc được lời hứa trước khi nghe hết câu đầu.

## 4. HÌNH ĐẦU TIÊN — `media-library.md` §2.0 bị 2/3 bản thắng vi phạm

| | frame 0 | có phải CHỦ THỂ của bài? |
|---|---|---|
| E7dF (常識20選) | sân bóng chày + câu hook vẽ to | ✅ khớp câu mở (mục 6 部活で水禁止) |
| QeHE (5つの風習) | ảnh tư liệu mấy người phụ nữ ngồi | ❌ **ảnh DỰNG BỐI CẢNH THỜI ĐẠI**, không phải 風習 nào |
| hmDu (家庭料理5選) | phố đông xe thời 高度経済成長 | ❌ **cũng vậy** — không phải món ăn nào |

⇒ Luật *"asset đầu tiên phải hiện đúng CHỦ THỂ của bài"* không phổ quát. Thứ **cả 3 đều làm** là: **hình khớp với CÂU ĐANG ĐỌC** (hmDu mở bằng 「日本は高度経済成長の真っただ中」 → đúng ảnh phố đông xe). ⇒ Cơ chế thật là **khớp CÂU**, không phải khớp CHỦ ĐỀ BÀI.

## 5. HÓA ĐỘNG — `Projects/_media_library/animate_still.py` (dựng cùng ngày)

Winners chứng minh **ảnh tĩnh là đủ**. Nhưng giữ 16–18 giây một tấm ảnh **chết cứng** là chỗ mình vượt được — mà 🔴 **KHÔNG được vượt bằng Ken Burns** (`feedback_video_no_motion_mot_giong`: user ghét "slide rung rung"; zoompan upscale gây shimmer).

**Cách giải: khung ĐỨNG YÊN, chỉ vài thứ BÊN TRONG khung động.**

| lớp | hiệu ứng | dùng cho |
|---|---|---|
| CỤC BỘ (có mặt nạ) | `steam` · `smoke` (chỉ LÀM SÁNG) · `glow` (đèn/cửa sổ thở) · `dustbeam` (bụi trong vệt nắng) · `ripple` (nước) · `sway` (rèm/cỏ) · `shimmer` (hơi nóng) | mỗi ảnh chọn 2–3 nguồn chuyển động **có thật trong cảnh** |
| PHIM (toàn khung, không dịch khung) | `grain` 8mm · `flicker` máy chiếu · `dust` hạt bụi · `scratch` xước mờ · `vig` vignette thở | mọi ảnh |

**7 preset theo loại cảnh:** `kitchen` · `tatami` · `street` · `night` · `office` · `water` · `flat` (chỉ lớp phim).

**Gate máy trong chính tool** — nó tự đo lại clip vừa dựng:
```
MAD frame-to-frame : phải > 3   (ảnh tĩnh của winners: 1,2-2,8)
DỊCH KHUNG (px)    : max < 1,0  -> "OK — khung đứng yên"; ≥1,0 = 🔴 rung, sai ràng buộc
```
**Đo thật trên ảnh của mình** (`10_tsugakuro/slides/trans_04.png`, 6s @30fps): **MAD 6,67 · dịch khung max 0,05px** ✅. Preset nhẹ (`flat`/`tatami`/`street`) ra MAD 1,07–1,88 = **ngang ảnh tĩnh của winners**, tức quá nhẹ → phải nâng biên độ, và gate bắt được điều đó.

⚠️ **Hai lỗi đã sửa khi dựng tool, đều chỉ lộ khi soi sheet 4 frame:**
1. `steam`/`smoke` bản đầu dùng `(f−0,5)×k` nên **làm TỐI một nửa số pixel** → ra **vệt bẩn trên mặt gỗ**. Hơi/khói thật **chỉ thêm sáng**, không hút sáng → đổi thành `clip(f−0,55, 0, None)`.
2. `scratch` vẽ đường 1px đặc → thành **vạch kẻ giả**. Phải blend 45% + thưa hơn 4×.

### 5.1 GIÁ THẬT của lớp hóa động (đo 2026-09-08)

| | số đo | ghi chú |
|---|---|---|
| thời gian dựng | **>2 phút cho 1 clip 16s @1080p30** | 60 clip ⇒ ~2–2,5 giờ CPU ⇒ **phải chạy nền** (`render-background.md`) |
| dung lượng | crf18 = **97 MB/16s** → crf23 = **~18 MB/6s** (≈3 MB/giây) | grain là kẻ thù của x264. Clip này là **file TRUNG GIAN** (video_render re-encode lại) nên mặc định đã đặt **`--crf 23`** |
| số ảnh cần gen | **55–65 ảnh** cho video 16,5′ (Style A) | thay cho **135 clip t2v** ⇒ rẻ hơn ~2,5× và không tốn credit Flow |
| ⏳ việc còn mở | grain resize + remap chạy mỗi frame ở full-res là chỗ chậm nhất | có thể hạ grain về 1/4 res và chỉ gọi `remap` khi spec có hiệu ứng dịch |

## 6. HẠN DÙNG
- Đo lại khi có video của mình chạy khuôn ảnh-tĩnh + hóa động (≥3 video) → so AVD/retention 60s với video 09/10 (t2v).
- ⚠️ **Không cái nào trong đây chứng minh GIỮ CHÂN.** Đây là **chữ ký sản xuất** đo từ file video của bản thắng, không phải nhân quả — không ai có retention của họ. Cùng cảnh báo với `audience-45plus.md` §2.0-bis.
- Mẫu **3 video / 2 kênh**. E7dF chỉ 9 ngày tuổi khi đo.
