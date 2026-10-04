# KHÁM KÊNH 真夜中の朗読便 — 2026-08-01

> Đo bằng YouTube Analytics API, 14 video, cửa sổ 25/06–01/08.
> ⚠️ **`impressions` và `impressionsClickThroughRate` đã bị Google rút** (từ 2026-07-30) → mọi kết
> luận dưới đây dựa trên **views · averageViewPercentage · traffic source · audienceWatchRatio ·
> relativeRetentionPerformance** — những metric CÒN trả về. Không có CTR trong file này.
> **Đè lên `CHANNEL_DIAGNOSIS_2026-07-28.md` và `CTR_PLAN_2026-07-28.md`** ở 3 điểm ghi ở §5.

## 0. KẾT LUẬN MỘT CÂU

**Kênh giỏi kể chuyện, dở mở đầu — và YouTube quyết định phát hay không dựa trên phần đầu.**
Sau giây ~60 đường retention **phẳng đẹp** ở cả video chết; toàn bộ khoảng cách giữa video 331 view
và video 1 view nằm gọn trong **60 giây đầu**.

## 1. TRẠNG THÁI PHÂN PHỐI — chỉ có MỘT rail sống

| Ngày | View | AVD% | Nguồn traffic |
|---|---|---|---|
| **07-27** | **331** | **33,3** | RELATED 281 (85%) · SUBSCRIBER 26 · YT_OTHER 18 |
| **07-25** | **228** | **35,1** | RELATED 165 (72%) · SUBSCRIBER 51 |
| 07-06 | 91 | 26,2 | RELATED 80 (88%) |
| 07-17 | 15 | 22,2 | YT_CHANNEL 5 · RELATED 5 |
| 07-22 | 14 | 13,0 | YT_CHANNEL 7 · RELATED 5 |
| 07-29 | 13 | 22,5 | RELATED 11 |
| 07-23 | 9 | 23,9 | RELATED 4 · YT_CHANNEL 3 |
| 07-19 | 8 | 26,9 | YT_SEARCH 4 · END_SCREEN 2 |
| 07-12 / 07-14 | 5 / 5 | 18,3 / 20,8 | YT_CHANNEL |
| 07-09 | 3 | 0,7 | YT_CHANNEL 1 |
| **07-28** | **1** | **10,0** | RELATED 1 |

🔴 **`BROWSE_FEATURES` = 0 TUYỆT ĐỐI ở cả 14 video.** Không một view nào từ trang chủ/feed. Kênh
chưa từng được YouTube đưa vào browse. → **Rail duy nhất có thể mua được là RELATED_VIDEO**, và mọi
quyết định packaging/nội dung phải nhắm vào đúng nó (`YT_CHANNEL` là mình tự bấm vào kênh, không
phải phân phối).

### 1.1 ⭐ NGƯỠNG AVD% MỞ RAIL — số sạch nhất tìm được

| AVD% | kết quả | mẫu |
|---|---|---|
| **≥ 33%** | **rail MỞ → 228–331 view** | 07-25 (35,1) · 07-27 (33,3) |
| 26–27% | rail hé → 91 view | 07-06 (26,2) |
| **≤ 24%** | **rail ĐÓNG → 1–15 view** | 07-29 (22,5) · 07-23 (23,9) · 07-17 (22,2) · 07-22 (13,0) · **07-28 (10,0)** |

**AVD% = phút xem thực ÷ độ dài.** Nên có đúng hai cách nâng: (a) giữ người lâu hơn, (b) **cắt độ
dài**. Đây là chỗ độ dài quay lại có ý nghĩa — nhưng **qua cơ chế AVD%, KHÔNG qua "bucket median"**
(xem §5.1).

## 2. ĐIỂM RỚT — mốc 3%, không phải 2 phút

`audienceWatchRatio` theo `elapsedVideoTimeRatio`:

| video | 1% | **3%** | 5% | 10% | 20% | 50% | 90% |
|---|---|---|---|---|---|---|---|
| 07-27 (331v) | 1,01 | **0,52** | 0,44 | 0,40 | 0,35 | 0,43 | **0,46** |
| 07-25 (228v) | 0,99 | **0,57** | 0,53 | 0,41 | 0,41 | 0,37 | 0,35 |
| 07-06 (91v) | 1,05 | **0,51** | 0,34 | 0,30 | 0,32 | 0,33 | 0,31 |
| 07-29 (13v) | 1,00 | **0,38** | 0,23 | 0,23 | 0,23 | 0,23 | 0,15 |

**Hai điều đọc ra:**
1. **Cú rớt duy nhất đáng kể là 1% → 3%** (mất 42–62%). Sau mốc 5% đường **phẳng** ở MỌI video —
   07-29 giữ 0,23 phẳng tuyệt đối từ 5% đến 70%, tức **ai còn lại thì nghe hết**. Thân truyện không
   phải vấn đề.
2. Khác biệt thắng/chết nằm đúng ở mốc 3%: **0,52–0,57 (thắng) vs 0,38 (chết)**.

📐 **Mốc 3% quy ra giây theo độ dài:** video 34′ → **giây 62** · video 40′ → giây 73 · video 29′ →
giây 52. → **Luật "2 PHÚT ĐẦU" trong CLAUDE.md là quá rộng. Cửa tử thật là ~60 GIÂY.**

## 3. relativeRetentionPerformance — số YouTube dùng để quyết định phát

Phân vị so với video cùng độ dài trên toàn YouTube (0,5 = trung bình ngách):

| video | 1% | **3%** | 5% | 10% | 15% | 30% | 50% | 90% |
|---|---|---|---|---|---|---|---|---|
| 07-27 (331v) | 0,36 | **0,37** | 0,37 | 0,35 | **0,68** | 0,61 | 0,61 | 0,60 |
| 07-25 (228v) | 0,33 | **0,37** | 0,43 | 0,45 | 0,45 | 0,50 | **0,73** | 0,38 |
| 07-06 (91v) | 0,48 | **0,39** | 0,44 | 0,54 | 0,61 | **0,85** | 0,80 | 0,43 |
| 07-29 (13v) | 0,24 | **0,15** | **0,14** | 0,17 | 0,30 | 0,47 | 0,45 | 0,19 |

🔴 **Ở 60 giây đầu, MỌI video của kênh đều nằm 0,24–0,48 = DƯỚI trung bình ngách.**
🟢 **Từ mốc 15% trở đi thì 0,58–0,85 = TRÊN trung bình ngách** (07-06 đạt 0,85 = phân vị 85%).

Đó là chân dung đầy đủ: **văn và giọng của kênh tốt hơn trung bình ngách rõ rệt — nhưng chưa video
nào vượt trung bình ngách ở phần YouTube dùng để chấm.**

**Ngưỡng đo được: `relPerf@3% ≥ 0,37` → rail mở · `≤ 0,15` → rail đóng.**

## 4. 🔴 ÁP VÀO VIDEO 14 (đã render, CHƯA đăng) — cold open đặt sai chỗ

Video 14 dài **34:15** → cửa tử ở **giây 62 = ký tự thứ 300** của `_TTS.md`.

| beat | ký | giây | % | vị trí so với cửa tử |
|---|---|---|---|---|
| câu mở của mẹ chồng | 0 | 0 | 0,0% | ✅ trong |
| stake "ăn vào là vào viện" | 146 | 30 | 1,5% | ✅ trong |
| láng giềng cười | 256 | 53 | 2,6% | ✅ trong |
| con trai "về ngay" | 351 | 72 | 3,5% | 🟠 **sau 3%** |
| 🔴 **cú đâm 「あの袋、そば粉だった」** | **529** | **109** | **5,3%** | ❌ **quá trễ** |
| 🔴 **lời hứa 「六年間で、十九回だよ」** | **634** | **130** | **6,3%** | ❌ **quá trễ** |
| cú đâm 「帰ってくるたびに寝てたから」 | 695 | 143 | 6,9% | ❌ quá trễ |

**Cả hai đòn mạnh nhất của bài đều nằm SAU cửa tử.** Ở giây 62 người nghe chỉ mới biết: bà mẹ chồng
khoe với láng giềng, tôi có dị ứng, láng giềng cười. Chưa biết **có bột trong món ăn**, chưa biết
**19 lần**.

So sánh: 07-27 (331 view) đặt cú sốc vào **câu đầu tiên** — 義母「嫁の菓子工房は仏間にするわｗ」＋
義弟夫婦 đã sống trong nhà. Cùng dài 40′42 mà AVD 33,3%.

### 4.1 Việc phải làm — sửa cold open v3

Dồn **cả hai đòn vào trước ký 300**. Cách rẻ nhất về chữ, không phá cấu trúc 9 nhịp:

- Cắt/nén 3 khối hiện đang chiếm ký 82–300: câu 「私は頭を下げた。ありがとうございます、と。」·
  đoạn giải thích 「その食べ物の名前は、この家の全員が知っている…十六年、毎年言ってきたからだ。」
  (50 ký, là **lời kể nền** — đúng thứ luật 60 giây cấm) · 「咲江は満足そうに、菜箸を持ち直した。」
- Đưa 「あの袋、そば粉だった」 lên ~ký 180 và 「六年間で、十九回だよ」 lên ~ký 260.
- Thông tin nền (dị ứng nặng đến mức nào, 16 năm đã nói) **đẩy xuống sau ký 300**, nhỏ giọt bằng
  thoại trong xe.

⚠️ **Chi phí: sửa lời = render lại voice + toàn bộ video (~1,5 giờ máy)** vì cache TTS theo nội dung
dòng và cue FX/SLIDES bám chuỗi `match`. Chưa làm — **chờ user chốt.**

## 5. BA ĐIỂM ĐÈ LÊN TÀI LIỆU CŨ

### 5.1 "Siết độ dài về 25–32′" — CĂN CỨ SAI, kết luận vẫn dùng được nhưng vì lý do khác
`CTR_PLAN_2026-07-28.md` §độ dài dựa trên **median view/ngày theo bucket** của 246 video đối thủ
(25–35′ = 3.939 · 50–70′ = 757). Nhưng số của CHÍNH kênh phủ định cách đọc đó: **07-27 dài 40′42
ăn 331 view — cao nhất kênh**, còn 07-28 dài 34′04 ăn **1 view**. Cùng bucket, chênh 331 lần.
→ **Độ dài không phải biến nhân quả.** Nó chỉ ăn qua **AVD% = phút xem ÷ độ dài** (§1.1): cắt ngắn
là cách *gián tiếp* nâng AVD% khi không nâng được retention. Giữ khuyến nghị 25–32′ nhưng **ghi
đúng lý do**, và đừng dùng độ dài để giải thích video chết.

### 5.2 "Cửa tử là 2 PHÚT đầu" → **~60 GIÂY** (mốc 3%)
CLAUDE.md §LUẬT 2 PHÚT ĐẦU + skill `script-chouhen` MỤC 10 đang ghi 600–700 ký ≈ 2 phút, suy từ
video 00 (mốc 6% của bản 44′). Số 14 video cho thấy cú rớt nằm ở **mốc 3%**, sau đó phẳng.
→ **Ngân sách cold open phải tính theo mốc 3% của ĐỘ DÀI THẬT**: 34′ → 300 ký · 30′ → 265 ký ·
40′ → 355 ký. Cold open v2 của video 14 là **837 ký** — dài gấp 2,8 lần cửa tử.

### 5.3 Nhịp đăng 5–7 video/tuần — nên PHANH
CLAUDE.md cho phép tự lên 7/tuần khi buffer ≥5. Nhưng 11/14 video đang ở AVD ≤27% = rail đóng, và
`relPerf@3%` chưa video nào vượt 0,48. Thêm video ở mức đó = thêm mẫu dưới-trung-bình vào điểm kênh
(đúng cơ chế đã giết kênh health). → **Giữ 3–5/tuần cho tới khi có 2 video liên tiếp `AVD ≥33%`.**

## 6. NGƯỠNG THEO DÕI (thay mốc CTR cũ vì metric đã bị rút)

| chỉ số | ngưỡng "rail mở" | đo ở đâu |
|---|---|---|
| `averageViewPercentage` | **≥ 33%** | API, có ngay |
| `relativeRetentionPerformance` @3% | **≥ 0,37** | API, có ngay |
| `audienceWatchRatio` @3% | **≥ 0,50** | API, có ngay |
| % view từ `RELATED_VIDEO` | ≥ 70% | API, có ngay |
| `BROWSE_FEATURES` > 0 | **chưa từng xảy ra** — mốc quan trọng nhất cần đợi | API |
| impressions / CTR | ⛔ Google đã rút — đọc tay Studio nếu cần | Studio |

Đo lại: **2026-08-15** (sau 3 video áp cold open v3).

## 7. LIÊN QUAN
- `CHANNEL_DIAGNOSIS_2026-07-28.md` · `CTR_PLAN_2026-07-28.md` (bị đè ở §5)
- `.claude/rules/audience-45plus.md` §4.1 (độ dài) · `youtube-upload-seo.md` §0.5 (Trends)
- Bảng Trends 2026-08-01 + Title v3: `03_SCRIPTS/14_gibo-no-uchiko.md` § Đóng gói CTR
- Script đo lại: `/tmp/diag14.py` (traffic+AVD) · `/tmp/ret14.py` (retention) — **nên đưa vào
  `tools/channel_diag.py`, việc còn mở**
