# KHÁM KÊNH 古代の秘訣 — 2026-07-30

> 🔴 **MỐC THỜI GIAN CỦA FILE NÀY ĐÃ BỊ ĐÈ — đọc `CHANNEL_DIAGNOSIS_2026-08-11.md` trước.**
> Vẫn ĐÚNG: BROWSE/SUGGESTED = 0, thumbnail nền tối là thủ phạm, ngách không chết, volume không mở vòi.
> ĐÃ SAI 2 chỗ: ① **cửa tử là giây 15–45, không phải giây 75** (đo curve 3 video) ② **các con số
> "vào bài ở giây 1134" ở §4b là RÁC** — gate cũ không dò được câu chuyển 「さて、ここからが今日の核心です」
> nên cộng dồn tới hết bài; số thật là 135–194 giây. Và câu *"07 denkidai ~100s (tốt nhất)"* ở §3b
> là bằng chứng gate cũ xếp hạng NGƯỢC: 07 chính là video retention **tệ nhất kênh** (AVD 12,12%).

> Phép đo: YouTube Data API + Analytics API (token readonly co-dai), 8 video đã đăng 07-15 → 07-30.
> Đối chiếu benchmark 昔の人の知恵 (UCYJ2D_D1q7_sYGorIB2_6iA) đo cùng ngày.
> ⚠️ **Metric `impressions`/`impressionsClickThroughRate` ĐÃ BỊ GOOGLE RÚT khỏi Analytics API** (đo 2026-07-30: "Unknown identifier" ở mọi dạng query — hồi khám health 07-27 còn đọc được). Từ nay muốn số impressions phải đọc tay trong YouTube Studio (Chrome Profile 6). Mọi kết luận CTR dưới đây là SUY LUẬN từ bằng chứng gián tiếp, không phải số đo.

## 1. SỐ HIỆN TRẠNG (đo được)

- **8 video / 15 ngày → 36 view tổng · 1 sub · 0 like · 2 comment.** Video "tốt nhất": 02 蚊の庭 14 view, 01 シロアリ 12 view. Video 03/06/08 = 1–2 view.
- **Traffic toàn kênh:** YT_SEARCH 16 · YT_CHANNEL 10 · SUBSCRIBER 7 · YT_OTHER_PAGE 3 · **BROWSE = 0 · SUGGESTED = 0 (không có dòng nào suốt 15 ngày)**.
- **Retention (mẫu NHỎ 12–14 view, đọc là tín hiệu yếu):**
  - Video 01 (22'47"): còn **50% ở mốc 1'08** → 41,7% (2'16) → avg 31,1%.
  - Video 02 (25'18"): còn **28,6% ở mốc 1'15** (mất 71% trong 75 giây đầu) → avg ~19%.
- **Index & hạng search: SẠCH, không án phạt.** Title-exact hạng 3–5; 「すだれ 電気代」 hạng 19; 「蚊 発酵トラップ」 hạng 5 (video mới đăng cùng ngày). Branding đủ: desc 332 ký, 28 cụm keyword, country JP.

## 2. BENCHMARK CÙNG NGÀY — ngách KHÔNG chết, cửa vẫn mở

昔の人の知恵: **14 video / ~5 tuần tuổi → 10.000 sub / 726K view.** Floor ~4K view/video, hit 蚊 07-06 **460K**, video 07-27 đã 14K sau 3 ngày. Nhịp hiện tại ~5/tuần (tăng so với 2,62 đo 07-28).

**Trùng đề tài trực tiếp — cùng đề, chênh 3–4 bậc độ lớn:**

| Đề tài | Benchmark | Mình |
|---|---|---|
| スズメバチ対策 | 21.346 (07-17) | **4** (05, 07-26) |
| 涼み方/điện mùa hè | 8.533 (07-15) | **9** (07, 07-28) |
| 蚊 | 460.936 (07-06) | **14 + 1** (02 + 08) |

→ Đề tài chọn ĐÚNG (cầu proven). Bệnh không nằm ở đề tài, không nằm ở index, không nằm ở tuổi kênh (benchmark cũng ~5 tuần, nổ từ video #2 除湿 46K).

## 3. CHẨN ĐOÁN

**Kênh chưa từng được YouTube phát ra ngoài (browse/suggested = 0 tuyệt đối).** YouTube test mọi video mới bằng một nhúm impressions; test không chuyển đổi thì không mở rộng. Hai lever chuyển đổi đều đang yếu:

### 3a. Thumbnail (suy luận CTR — impressions không còn đọc được)
Đặt 8 thumbnail mình cạnh 8 thumbnail benchmark (contact sheet: `06_VIDEO/_diag_thumbs/_sheet.jpg` + `_bench_sheet.jpg`):

| | Benchmark (floor 4K) | Mình (floor 1) |
|---|---|---|
| Nền | **8/8 SÁNG** (trời, tường trắng, vườn xanh) | **6/8 TỐI moody** |
| Lời hứa | **CON SỐ kết quả**: 最大-21℃無料で冷却 · 6,000円=無限の水 · 替刃1枚で6か月/30秒 | Văn chương tease: だから隠された · だから増えていた · 数百円の知恵 |
| Bố cục | 1 vật thể chính + mũi tên đỏ chỉ vào | Nhiều chi tiết (04: cả kệ sản phẩm; 02: muỗi+❌+cây) |
| Nhận diện | **Mascot ông lão nón lá lặp lại** (2/8) | Không có yếu tố lặp |

Nền tối moody đúng là thủ phạm đã bị kết án ở health 07-21 ("gần như tàng hình trên browse") — lỗi cũ lặp ở kênh mới.

### 3b. Retention mở bài (đo được, mẫu nhỏ)
Mất 50–71% khán giả trong ~75 giây đầu — cùng họ bệnh với health (relPerf@60s đáy phân vị). co-dai **chưa có gate cold-open-60s bằng máy** như health (`check_coldopen60.py`); skill có luật hook nhưng không ai đo.

**⭐ BỔ SUNG 2026-07-30 (sau khi port gate `tools/check_coldopen.py`, quét 12/12 script):**
thời điểm VÀO BÀI (chương/mẹo đầu tiên) đo bằng hệ số 5,625 ký/s:

| Script | Vào bài ở | Script | Vào bài ở |
|---|---|---|---|
| 07 denkidai | ~100s (tốt nhất) | 08 hozonshoku | ~240s |
| 13 veranda | ~143s | 14 ka-trap | ~298s |
| 10 kankisen | ~197s | 04 gokiburi | ~403s |
| 03 zassou | ~211s | **05 suzumebachi** | **~643s (10'43"!)** |

→ **0/12 đạt trần 75s.** Cấu trúc hiện tại: hook → tease → khối dặn dò an toàn → câu chào kênh → nostalgia → tiền-loop → RỒI MỚI vào bài. Khán giả rời ở giây 75 vì tới lúc đó chưa nhận được gì. Đây là lời giải khớp nhất cho retention đo được ở §trên. Video 05 (4 view) cũng chính là video dạo đầu dài nhất.

### 3c. Volume không mở được vòi (bài học nenkin/health lặp lại)
Đang đăng 3,7/tuần vào kênh vòi đóng = mỗi video thêm 1 mẫu xấu. 完全攻略 ramp 1/tuần vẫn nổ video #3; benchmark co-dai nổ video #2. Không có bằng chứng nào cho thấy đăng dày mở vòi ở kênh 0-phân-phối.

## 4. ĐỀ XUẤT (CHỜ USER QUYẾT — chưa làm gì)

1. **Đổi hệ thumbnail sang khuôn benchmark** (nền SÁNG + 1 vật + SỐ kết quả to + mũi tên đỏ), làm lại trước cho 3 video mùa nóng còn cầu: 07 denkidai · 08 ka-trap · 05 suzumebachi. Đổi thumbnail video cũ = rẻ, không re-render. Cân nhắc luôn **mascot cố định** (ông lão/bà lão kiểu 古代) — vừa nhận diện vừa là lớp `character`.
2. **Port gate `check_coldopen60.py` sang co-dai** — mẹo đầu tiên phải vào ≤60–90s; quét script 14 tồn kho trước khi render.
3. **Hạ nhịp 4/tuần → 1–2/tuần phép thử sạch** cho tới khi thấy view BROWSE đầu tiên (tiền lệ health 1/tuần, nenkin 1/tuần). Slot dồn công vào thumbnail + 60s đầu.
4. Title: giữ keyword-đầu, nhưng đưa **con số kết quả** vào nửa hiển thị (benchmark: 数百円/－21℃/6か月 xuất hiện ở cả title lẫn thumbnail). 【】 không bắt buộc ở ngách này (benchmark chỉ 2/14).

## 4b. CẬP NHẬT 2026-08-01 (check lại theo yêu cầu user)

- **Số:** 8 video public (+1 bản trùng 14 đã chuyển private — xử lý đúng) · **49 view** (36 → 49, +13/2 ngày, chủ yếu 07 denkidai 9→12 + 02 ka-niwa 14→15) · 1 sub.
- 🔴 **BROWSE/SUGGESTED vẫn = 0 tuyệt đối, kể cả cửa sổ 7 ngày gần nhất** (đo Analytics API 2026-08-01: 7d = SEARCH 7 · SUBSCRIBER 4 · CHANNEL 3 · khác 3). Search vẫn là nguồn organic duy nhất.
- **Tiến độ 4 đề xuất §4:** ① thumbnail B1 — video 14 ✅ đã set; **05 + 07 v2 vẫn CHỜ USER GEN ẢNH** (prompt sẵn trong script §サムネ v2) ② gate `check_coldopen.py` ✅ đã port ③ lịch 2/tuần T2·T6 ✅ đã chốt ④ title số kết quả — áp từ video mới.
- ⚠️ **Video 14 KHÔNG phải phép thử sạch của công thức mới:** thumbnail B1 mới nhưng cold open CŨ (vào bài ~298s, render trước khi có gate). Video chuẩn-mới-đủ-cả-hai đầu tiên sẽ là video kế tiếp (nếu rewrite cold open trước render). Đừng đọc kết quả 14 như phán quyết công thức.
- **Tồn kho:** script 08–13 đã viết + TTS nhưng CHƯA render, **cả 6 đều fail gate cold open** (vào bài 143–403s) → phải rewrite 60–90s đầu trước khi render (sửa đủ 3 chỗ theo `humanize-script-voice.md` §4: `_TTS.md` + `.md` + quét match SLIDES nếu có).

## 5. GHI CHÚ KỸ THUẬT
- Contact sheet 2 bên: `06_VIDEO/_diag_thumbs/_sheet.jpg` (mình) · `_bench_sheet.jpg` (benchmark).
- Lệnh đo lại: `python tools/analytics_report.py --channel co-dai` (chouhen/tools) + query search API bằng token co-dai. Impressions: đọc tay Studio Profile 6.
- Channel ID mình: UCVlmm1sz7cvTIQ3uSaSct_w · benchmark: UCYJ2D_D1q7_sYGorIB2_6iA.
