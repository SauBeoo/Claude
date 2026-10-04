# 08 — ANALYTICS LOG + NGƯỠNG PHANH: 親の介護とお金ノート

> Sổ đo. Cập nhật **sau mỗi video (72h)** và **cuối mỗi tuần**. Dữ liệu lấy bằng:
> `python E:\Claude\Projects\youtube-jp-chouhen\tools\analytics_report.py --channel kaigo` (cần `credentials/token.json`) + YouTube Studio (impressions/CTR/AVD).

## §0 NHỊP ĐĂNG & CƠ CHẾ PHANH (user chốt 2026-07-25)

> ⭐ **SỬA 2026-07-28 (user chốt sau khi đo lại 50 video/kênh benchmark, thay mẫu 20 video cũ).**

**Nhịp HIỆN HÀNH: T3 + T6, 19:00 JST — 2 video/tuần CỐ ĐỊNH.** T6 = slot mũi nhọn (dồn video mạnh nhất), T3 = slot thứ hai.
⚙️ Nhịp nằm thẳng trong `CHANNELS["kaigo"]["slots"]` của `upload_pack.py`; hàm `_kaigo_slots()` (tự nhảy 7 ngày/tuần khi `07_UPLOADED` ≥5) **ĐÃ XOÁ**.

**Cái gì đổi so với 2026-07-26 và VÌ SAO:** quyết định cũ là "5 video đầu T2·T4·T6 → TỪ VIDEO #6 là 1 video/NGÀY", thi hành dù biết ngược benchmark. Đo lại bằng số đã đảo nó:
- **節約看護師りょう** (748K sub, hiệu suất/video cao nhất nhóm): **T6 = 48/50 video**, nhịp **1,02 video/tuần**, median **105.975 view/video**.
- **みんなの給付金・補助金** (551K): long-form **CHỈ đăng T3 (15) + T6 (16)** — ngày khác 0 long-form; median T6 19,2K > T3 13,3K.
- Phản ví dụ nhịp cao **trong cùng cụm ngách**: まるごと安全相続ch-あまおう đăng **~1 video/ngày (7,29/tuần)** → 50 video mới nhất chỉ **3.655–6.994 view median**, video mới nhất 1.264 view.
→ Bằng chứng đầy đủ: `.claude/rules/upload-schedule-measure-2026-07-28.md`.
→ **Checkpoint sau video #5 quay lại đúng 1 vai: đọc số để biết CÓ ĐƯỢC TĂNG nhịp hay không** (không còn chuyện nhịp tự lên).

**Bảo lưu đã ghi (nay đã thành căn cứ chính):** benchmark cùng cụm ngách tiền cho thấy volume là chiến lược thua — 給付金チャンネル **1.971 video → 87.100 sub** (17.848 view/video) vs 年金・給付金完全攻略 **12 video → 132.000 sub** (490.103 view/video) = **27× hiệu suất/video**; 3 kênh tăng nhanh nhất ngách đều ≤1,3 video/tuần. Cộng thêm policy 15/07/2026 đổi tên 量産コンテンツ → 「一般的、または繰り返しの多いコンテンツ」. Vì vậy nhịp cao được thi hành **kèm 2 phanh dưới đây**.

### Phanh 1 — GATE 5 ĐIỂM (kiểm từng video, trước khi đăng)
Chi tiết ở `CLAUDE.md`. Thiếu 1 điểm → **BỎ SLOT, KHÔNG đăng bù.**
1 số tiền của cast trước phút 2 · 2 ≥2 原典ショット (shot đầu ≤3 phút) · 3 trả lời được 「なぜ」 · 4 hành động có địa chỉ + hạn · 5 khác trục + khác khuôn.

### Phanh 2 — CHECKPOINT SỐ

**Checkpoint sau video #5 — đọc số để biết CÓ ĐƯỢC TĂNG nhịp (3/tuần, thêm T2) hay giữ 2/tuần:**
| Chỉ số | Ngưỡng "khỏe" | Ghi chú |
|---|---|---|
| AVD (average view duration %) | **≥ 28%** | nenkin đo được 42,8% / 52,5% với tệp senior; tệp 50代 trẻ hơn nên hạ ngưỡng |
| CTR | **≥ 3%** | health chết ở 2,6% với thumbnail moody |
| Impressions | **> 0 và tăng qua 3 video liên tiếp** | Bài học co-dai: 0 impressions = cold-start/branding rỗng, KHÔNG phải nội dung dở |
| GATE | Không video nào fail GATE 2 lần liên tiếp | Fail liên tiếp = chưa đủ năng lực sản xuất → không được nghĩ tới tăng nhịp |

> ✅ Nhịp KHÔNG còn tự tăng (2026-07-28). Muốn lên 3/tuần thì phải đủ cả 4 ngưỡng trên **và** sửa tay `CHANNELS["kaigo"]["slots"]` trong `upload_pack.py` (hoặc đặt `slots` tay trong `projects.json` — dashboard ưu tiên slots đặt tay). Ngày thêm vào đầu tiên nên là **T2** (完全攻略 chưa từng đăng T2 nhưng スガワラ median T2 352K — tín hiệu yếu; đừng thêm T4/T5, đó là 2 ngày đo được là yếu nhất cụm).

**Ngưỡng PHANH (bất kỳ điều nào → xét hạ về 1/tuần, chỉ giữ T6):**
- AVD trung bình 5 video gần nhất **< 25%**
- CTR **< 2,5%**
- view/video **giảm liên tiếp 3 video**
- Đã **bỏ ≥2 slot trong 1 tuần** vì hết hàng qua GATE
- **Bất kỳ** cảnh báo YPP / 「一般的、または繰り返しの多いコンテンツ」 / limited ads

## §1 SỔ ĐO TỪNG VIDEO

| # | Slug | Trục | Khuôn thumb | Đăng | 72h view | CTR | AVD | Impr | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | (chưa có video) |

## §2 SỔ ĐO TUẦN

| Tuần | #video đăng | #slot bỏ (fail GATE) | View tổng | Sub | CTR TB | AVD TB | Quyết định nhịp |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## §3 BẢNG "3 BỆNH" — chẩn đoán khi số xấu (đừng đoán bừa)

| Triệu chứng | Bệnh | Sửa ở đâu |
|---|---|---|
| Impressions ~0 | **Cold-start / branding tầng kênh rỗng** — máy chưa biết đặt kênh vào rổ nào | `youtube-upload-seo.md` §2.4: categoryId · rổ 12 tag nhận diện · 3 hashtag cố định · channel description ≥300 ký · channel keywords. KHÔNG phải lỗi script |
| Impressions cao + CTR thấp | **Thumbnail/title** | `03_THUMBNAIL_TITLE_FORMULA.md` — swap variant B, đổi khuôn, số tiền to hơn |
| CTR ổn + AVD thấp (rớt phút 0–2) | **Cold open / dàn ý** | skill `script-kaigo` GĐ3: câu 1 phải là mất mát + số; case+số trước phút 2; giải thích chay ≤45s |
| AVD tụt giữa bài | **Khối tính quá dài / thiếu re-hook** | Chèn beat quy đổi đời thường, ○×クイズ, CTA ~50% |
| View đều nhưng không sub | **Thiếu lý do quay lại** | Bible §8.5: hẹn tập đích danh, 兄弟に見せる1枚, playlist theo trục |

## §4 LỊCH ĐO ĐỊNH KỲ

- **72h sau mỗi video:** ghi §1.
- **Cuối tuần:** ghi §2 + đối chiếu ngưỡng §0.
- **Mỗi 6–8 tuần:** đo lại `CHANNEL_BENCHMARK_2026-07-25.md` (bảng đối thủ + đề tài) và cập nhật ma trận trục ở `02_CONTENT_STRATEGY.md` theo view thật của chính kênh.
- **Khi kênh đủ ~10–20 video:** YouTube Studio → Audience → "When your viewers are on YouTube" **đè lên giờ đăng tạm** trong `.claude/rules/upload-schedule.md`.
