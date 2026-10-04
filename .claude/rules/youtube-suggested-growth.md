# YouTube — SUGGESTED-FIRST: hàng xóm mục tiêu · swipe file · vòng portfolio (RULE TOÀN HỆ THỐNG)

> Áp cho **nenkin** + **showa**. Chốt 2026-08-21, đúc từ `SecondBrain/30_Resources/video-editing/The YouTube Growth Lie No One Talks About.md` (Evan Carmichael).
> ⚠️ Số trong nguồn là số của kênh người ta — đối chiếu số đo của mình trước khi tin (§0). Rule này thêm 3 bước vào pipeline + 1 vòng review tháng, không thay gate hiện có.

## 0. MỆNH ĐỀ GỐC + SỐ ĐO CỦA MÌNH
**Claim:** YouTube là **referral engine** (kênh nguồn ~92% view từ suggested); top 10% video ăn 79% view.

| Kênh | Số đo | Khớp claim? |
|---|---|---|
| **nenkin** | Analytics API 90 ngày (2026-08-21): SUBSCRIBER 90,7% · SEARCH 3,4% · RELATED 2,2% · BROWSE 0 | ⏳ organic quá nhỏ, giữ SEO đầy đủ |
| **showa** | chưa đo | — đo trước khi kết luận |

- Analytics API **đọc được traffic source** bằng token kênh (chỉ `impressions`/CTR bị rút) — đừng suy rộng "API chết".
- ⛔ **Không suy rộng "tags = 0 / bỏ SEO"**: chỉ đúng với kênh ĐO ĐƯỢC rail đề xuất là nguồn chính. nenkin/showa giữ `youtube-upload-seo.md` đầy đủ.
- ⭐ Claim *"packaging = 70% trận đánh"* khớp độc lập với kết luận đã đo trong workspace → đừng cắt lớp bao bì để tiết kiệm giờ.

## 1. HÀNG XÓM MỤC TIÊU — bước bắt buộc trước khi viết script
Hỏi *"video mình xứng đáng xếp CẠNH video nào"* — làm "perfect next watch" của một video đang thắng.
1. Mở video top ngách (≤30 ngày nếu được) bằng **đúng Chrome profile kênh**, nhìn cột suggested = "khu phố" muốn vào.
2. Ghi vào script heading **`### HÀNG XÓM MỤC TIÊU`**: link + title + view + kênh của 1–3 video + 1 dòng "vì sao mình là next-watch của nó".
3. Title + thumbnail nói cùng **ngôn ngữ thị giác** của sidebar đó (khuôn kênh vẫn giữ).
4. Khám kênh: đối chiếu `insightTrafficSourceDetail` — trượt 3 video liên tiếp = cách chọn hàng xóm sai.

### 1.5 🔴 "Đúng tệp nhân khẩu" ≠ "đúng khu phố" — kiểm bằng video DẪN
Nhân khẩu (tuổi/giới) đúng không có nghĩa YouTube hiểu **chủ đề**. Ca nenkin (`youtube-jp-nenkin/CHANNEL_DIAGNOSIS_2026-08-29.md` §3.5): 65+ = 75%, CTR 7,7%, nhưng **19/24 video dẫn RELATED là bóng chày/idol/drama** → vách −30 điểm ở giây 20–30 ở mọi video.
1. Khám kênh phải kéo **danh sách video dẫn RELATED** (`nenkin/06_VIDEO/_diagnose/pull_curves.py`), tra title bằng `videos.list`, **đếm tỉ lệ cùng ngách**.
2. <5/24 cùng ngách: **đừng chữa vách 20–30s bằng cold open**. Việc đúng là **dạy YouTube chủ đề**: keyword đo được đứng ĐẦU title (bỏ tag 【】 chung chung lặp) · title/thumbnail nói ngôn ngữ **hàng xóm thật** · end screen + **playlist theo trụ** · search làm mỏ neo.
3. ⛔ Không tăng nhịp khi tỉ lệ còn thấp. ⛔ Không đổi thumbnail khi CTR đã cao.
4. Đọc lại sau 5 video: tỉ lệ cùng ngách phải tăng; view không phải thước đo của việc này.

## 2. SWIPE FILE — sổ title đã chứng minh
1. Mỗi project có **`01_SWIPE_TITLES.md`**; mỗi dòng: `title · kênh · view · sub · tỉ số view/sub · ngày ghi · link`.
2. **Ngưỡng nhận: view ≥ 3× sub của kênh đăng** (ngưỡng tự chọn), ưu tiên video ≤30 ngày.
3. **Chọn đề tài mới: mở sổ TRƯỚC, sáng tác SAU.** Góc trong sổ + chưa làm + qua gate ngách = ứng viên số 1.
4. Tool: `python Projects/youtube-jp-chouhen/tools/swipe_titles.py [--group <key>]` · `youtube-jp-health/tools/bench_channels.py <channelId>`.
5. Mục >6–8 tuần → đo lại. Title của kênh đã sụp là số rác.

## 3. VÒNG PORTFOLIO THÁNG — 3–5 trục + 1 ô thử nghiệm
1. Trục nội dung đã chốt trong CLAUDE.md kênh = series; gắn nhãn trục cho mọi video.
2. Cuối tháng đọc Studio: watch time + sub theo trục → ghi `08_ANALYTICS_LOG.md`.
3. Trục bét 2 tháng liên tiếp → thay bằng trục thử nghiệm; trục thắng → farm thêm góc.
4. 🔴 **Phanh mẫu nhỏ:** kênh <500 impressions/video thì chỉ ghi sổ, **không kill trục**.

## 4. MỐC RETENTION PHÚT 1 = 70% (để ĐỌC, không phải gate)
Khám kênh ghi cả **% tuyệt đối còn lại ở 60s** (so 70%) và **percentile `relPerf@60s`**. Không thêm gate mới.

## 5. DRILL CẮT ĐÔI ×2 cho cold open
Viết xong cold open → cắt một nửa → cắt một nửa nữa; phần sống sót thường là chỗ nên bắt đầu. Làm **trước** khi chạy gate cold open của kênh.

## 6. ⛔ BA THỨ TRONG NGUỒN KHÔNG ÁP
1. **"Title và thumbnail không lặp nhau"** — ngược luật `feedback_thumbnail_yeu_to_title`. User chốt 2026-08-21: **thử qua A/B, không đổi luật** — lần đóng gói tới, bản **T3** làm theo triết lý này (thumbnail tải cảm xúc/stake, chữ không lặp title); thắng mới bàn đổi luật.
2. **"10 thumbnail + 15 title"** — giữ **3×3** (`ab-3title-3thumb.md`).
3. **"Tags vô giá trị"** — không áp chung; chỉ kênh đo được rail đề xuất là nguồn chính mới đi SEO nhẹ.

## 7. LIÊN QUAN
SEO: `youtube-upload-seo.md` · A/B: `ab-3title-3thumb.md` · Nhịp + phanh: `upload-schedule.md` · Benchmark ≤30 ngày: memory `feedback_benchmark_30_ngay`.
