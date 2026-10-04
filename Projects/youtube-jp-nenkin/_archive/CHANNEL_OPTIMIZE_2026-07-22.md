# 年金と老後のお金研究室 — Khám kênh + benchmark + hot topics (2026-07-22)

> Đo qua token API nenkin (vừa tạo) + benchmark 14 kênh ngách 年金/老後 (search API, đo public: subs/cadence/categoryId/top-video-by-view).
> Cùng ngày backfill 2.4: chouhen/co-dai/health/shokutaku ✓. nenkin = cold-start thuần, làm bài bản luôn.

## 0. CHẨN ĐOÁN KÊNH (số thật)

| Chỉ số | Giá trị | Đọc |
|---|---|---|
| Video / sub / view | **1 / 0 / 3** | Cold-start thuần, mới đăng 2026-07-20 |
| Analytics | **RỖNG (0 impressions)** | Thuật toán chưa đem đi chào — chưa đủ tín hiệu để phân loại/phân phối |
| Mô tả kênh / keywords / banner / playlist / trailer | **TRỐNG hết** | Tầng kênh trần trụi — nặng hơn co-dai lúc mổ (co-dai còn 2 video) |
| **categoryId video 01** | **22 (SAI)** | Benchmark faceless-slide để **27 Education** → phải đổi |
| Độ dài video 01 | **13m30s** | NGẮN so với chuẩn ngách (20–30′+) — xem Mục 3 |
| Tags/hashtag video 01 | 22 tag + 3 hashtag, có tag nhận diện cuối | Ổn, chỉ cần chuẩn hóa theo rổ 2.4 |
| **Chủ đề video 01 (在職老齢年金 4月激変)** | ✅ ĐÚNG HÀNG | Chính là chủ đề video top 2.4M của 節約看護師りょう — topic tốt, chỉ thiếu phân phối |

**Kết luận:** bệnh KHÔNG phải chọn sai chủ đề (01 trúng chủ đề viral nhất ngách). Bệnh = **(a) mới 1 video + tầng kênh trống → thuật toán chưa có gì để phân loại; (b) cat sai; (c) hơi ngắn.** Đòn bẩy = **đổ volume (4 script đã viết → render/up) + lấp tầng kênh (cat 27) + kéo dài video.**

## 1. BENCHMARK NGÁCH (đo API 2026-07-22)

### Kênh cùng MÔ HÌNH faceless-slide (học trực tiếp)
| Kênh | Sub | #video | cat | Nhịp | Độ dài | Top video |
|---|---|---|---|---|---|---|
| **年金・給付金完全攻略** | 130K | **12** | **27** | ~tháng→tuần | 25–59′ | 3.79M (ねんきん定期便に載らない年金4選) |
| **シニアの年金・給付金速報** | 113K | 247 | **27** | 週2–3 | 23′–1h32 | 461K (手取り変わる人) |
| フクロウの年金解説室 | 41K | 38 | — | — | — | — |
| 年金・給付金チャンネル | 40K | 13 | — | — | — | — |

> 完全攻略 = **12 video → 130K sub** = bằng chứng ngách này KHÔNG cần cày số lượng, cần TRÚNG + tầng kênh sạch + cat đúng. Đây là hình mẫu gần nhất của nenkin.

### Mô hình khác (tham khảo, KHÔNG copy)
- **News65 (漫画)** 173K, cat 22 — story hóa bằng 漫画; top 1.37M (60歳で年金…手取り計算). ⭐ Hợp tuyến "story 年金生活" của nenkin nhưng nenkin làm slide, không 漫画.
- 節約看護師りょう 748K (cat 26, mặt thật y tá), 70代さと (cat 26 vlog thật), 年金のホンネ (2064 shorts phỏng vấn) — khác format, không bắt chước.

### Title pattern thắng (đo từ top video)
`【知らないと大損】/【申請忘れ続出】/【50歳以上必須】` + **số tiền lỗ định lượng** (生涯500万円損 · 年6万円ムダ · +7万円) + `役所が教えない/年金事務所が教えない` + `末路/後悔しない/危険` + `2026年新ルール/4月から激変`.

## 2. TOA TỐI ƯU (tăng view/đề xuất)

### 2a. SỬA NGAY qua API (reversible, tao đề xuất — chờ duyệt)
1. **categoryId video 01: 22 → 27** (khớp 2 benchmark faceless-slide). 
2. **Backfill tầng kênh (luật 2.4)** — desc kênh (persona 研究室, giữ YMYL) + keywords ~24 + rổ 12 tag nhận diện + 3 hashtag cố định + playlist + trailer = video 01. (Cat 27 cho mọi video sau.)
3. Nội dung cụ thể: soạn trong bản apply (giống health/shokutaku).

### 2b. EDITORIAL (video sau, không sửa video cũ)
- **Kéo dài 20–25′** (ngách explainer chuộng dày; 完全攻略/速報/News65 đều 20–30′+; video 13.5′ của nenkin ngắn hơn chuẩn). Content chế độ đủ chất để dày mà không loãng.
- **Title đổi sang khung "大損/申請しないと/末路/○○万円損"** + giữ trần YMYL (không 絶対/必ず, không tên chính trị). Persona 研究室「役所が教えない数字を一緒に読む」khớp motif "役所が教えない" đang thắng.
- **Volume:** 4 script đã viết (01–04) → render + up đều tay T2·T4; 完全攻略 chứng minh 12 video trúng là đủ nổ.

## 3. 🔥 CHỦ ĐỀ HOT — xếp lại theo TOP VIDEO benchmark (mạnh hơn tín hiệu search đơn thuần)

| Hạng | Chủ đề | Bằng chứng benchmark | Trạng thái nenkin |
|---|---|---|---|
| 🥇 | **年金は何歳から受給が正解｜60/65/70/75で受け取った人の末路** | 看護師 1.37M+969K · News65 1.37M+766K+757K(4人の末路) — evergreen TO NHẤT | Script 02 (65vs70) → **mở rộng 4 mốc + khung 末路**, đẩy sớm |
| 🥈 | **60歳で即退職は危険｜2年だけ再雇用で老後資金が激変** | 看護師 1.14M · News65 891K+777K | **CHƯA có → viết mới** (dùng cast 高橋/田中) |
| 🥉 | **申請しないともらえない｜ねんきん定期便に"載らない"年金・給付金** | 完全攻略 3.79M (top ngách) · 看護師 539K | Script 04 (支援給付金) cùng mạch → làm thêm bản "定期便に載らない" |
| 4 | **年金通知書の読み方**（額改定・振込通知書, 6月/10月/12月) | 完全攻略 1.05M+244K · 速報 343K+ | **CHƯA có** — seasonal recurring, dễ nổ mỗi đợt gửi thông báo |
| 5 | **住民税非課税世帯になる条件・裏技｜支給停止申出書** | News65 578K · 速報 140K+124K | **CHƯA có → viết mới** |
| 6 | **定年後の健康保険の選び方（任意継続 vs 国保）で損しない** | 看護師 615K | **CHƯA có** — trục thuế/phí, an toàn YMYL |
| 7 | **65歳から介護保険料が倍増？** | 看護師 509K | **CHƯA có** (nối #6, cụm "phí sau nghỉ hưu") |
| — | 在職老齢年金 4月改正 (script 01) | 看護師 2.4M | ✅ ĐÃ up — chủ đề đúng, chỉ thiếu phân phối |

> ⚠️ Mỗi chủ đề TRƯỚC khi thành script vẫn đo YouTube Search 30d (rule 0.5). Bảng này để xếp ưu tiên hàng đợi — bổ sung #2/#4/#5/#6 vào 02_CONTENT_PLAN.

## 4. VIỆC TIẾP
- [x] Duyệt → apply 2a (cat 27 + backfill tầng kênh) qua API — **XONG 2026-07-25**, hồ sơ + bộ nhận diện chốt tại `CHANNEL_BACKFILL_2026-07-25.md` (phần lớn đã live từ ~07-24, ngày 07-25 vá nốt: dòng lịch desc kênh + rổ tag/hashtag video 02/04)
- [x] Bổ sung hot topics #2/#4/#5/#6 vào 02_CONTENT_PLAN hàng đợi — xem roadmap 90 ngày trong `02_CONTENT_PLAN.md` (2026-07-25)
- [ ] Render + up 4 script đã viết (đổ volume) — 04 lên 07-25 19:00, 05 xếp T2 27/07, 03 chờ mổ trụ
- [ ] Video sau: kéo 20–25′ + title khung 大損/末路 — khắc vào skill `script-nenkin`
