# 60代からの食卓 — Playbook cải tiến kênh (từ data Analytics 2026-07-21)

> Đúc từ phân tích Analytics thật (token API + Studio) ngày 2026-07-21. Kênh: 7 video · 1 sub · 56 view · CTR ~1,7%.
> Mục tiêu: qua được "bài test vài trăm impression" của YouTube để nó nâng bậc reach.
> ⭐ **2026-07-29: nếu bật lại kênh, đọc trước `../youtube-jp-health/BENCHMARK_RIVALS_2026-07-29.md` §7–8** — công thức bóc từ network đối thủ mới nổ view (món quen × 食べ合わせ × đáp án che, 25′, thumbnail tường chữ + hộp cyan): áp nguyên khối cho shokutaku, khớp sẵn với "rổ cảnh báo" bên dưới; payoff #1 phải ≤ phút 2 (bệnh cũ 8:20). Kênh vẫn ⏸ NGƯNG — dòng này chỉ ghi sổ, không đổi slots.

## 0. CHẨN ĐOÁN GỐC (số thật)

| Triệu chứng | Số | Đọc |
|---|---|---|
| Impressions/video | 289–528 rồi phẳng | YouTube chỉ thả lô test nhỏ, chưa nâng bậc |
| **CTR** | **1,7–2,4%** | dưới ngưỡng ~4% → không graduate |
| Retention 90s đầu | còn 43% ở phút 1,5 | hook + intro quá dài |
| **第6位 xuất hiện** | **phút 8:20** | ⚠️ 8 phút mới có payoff đầu = giết cold traffic |
| Độ dài | 35 phút | quá tham cho kênh non; video 14' (ゆで卵) được đẩy mạnh nhất |

**Phát hiện vàng — YouTube đề xuất NHẦM RỔ:** video 腎臓 khi đặt cạnh 「老化アルデヒド」(rổ chống lão hóa) → xem **10 giây** (98 impr, flop). Khi đặt cạnh 「四毒・船瀬俊介」(rổ cảnh báo thực phẩm thực-dưỡng) → **xem 96% một video 35 phút** (chỉ 11 impr). → Nội dung KHÔNG dở; **metadata phát tín hiệu sai rổ.**

**Rổ thắng (target):** "食べてはいけない / 危険な食べ物 / 腎臓に悪い / 四毒" cho 60代 — khung CẢNH BÁO, không phải khung "món tốt giúp bạn".

---

## 1. ĐÒN BẨY #1 — LÁI VỀ RỔ THẮNG qua METADATA (làm NGAY, sửa video đã đăng trong Studio, reversible)

### 1a. TAG — thêm tag bắc cầu sang rổ cảnh báo (tag không hiển thị công khai → dùng khung "悪い/危険" thoải mái, không dính compliance title)
Hiện tag toàn khung "良い" (tốt) → YouTube xếp vào rổ helpful. Bổ sung tag rổ thắng cho **08 腎臓**:
```
腎臓に悪い食べ物,食べてはいけない,腎臓に良い食べ物,腎臓,腎臓を守る食べ物,60代 食べてはいけない,危険な食べ物,塩分 腎臓,クレアチニン 下げる,eGFR,慢性腎臓病 食事,むくみ 原因,60代 食事,シニア 健康,玉ねぎ 効能,さば缶 健康,大根おろし,減塩 コツ,腎臓に良い食事,60代からの食卓
```
(4 tag đầu 腎臓に悪い/食べてはいけない/60代 食べてはいけない/危険な食べ物 = cầu nối sang rổ 96%-retention.)

### 1b. TITLE — LEAD bằng khung cảnh báo/curiosity, không lead bằng "良いランキング"
- ❌ Hiện: `腎臓に良い食べ物ランキング6選｜60代は「足す」が正解でした` (thuần tích cực → rổ アルデヒド)
- ✅ Đổi lead sang khung nghi vấn/cảnh báo (giữ payoff tích cực ở vế sau):
  1. `その「腎臓にいい」逆効果かも？60代が"水に流してる"6つの正解【食べ物】`
  2. `60代が腎臓に「足してるつもり」で疲れさせてる食べ方｜正解は6つ`
  3. `腎臓に悪いと思ってた…実は逆？60代の台所の6つの味方【ランキング】`
- Bằng chứng: video 「その『体にいい』が腎臓を疲れさせる?」(khung nghi vấn) chính là bản hút được rổ 96%. Khung này ĂN.
- ⚠️ Compliance: title/thumbnail KHÔNG 死・血・殺・透析; 疲れさせる/逆効果/水に流す = sạch.

### 1c. THUMBNAIL — khớp khung với title (cả 2 cùng "cảnh báo/tiếc của"), 1 điểm nhấn đọc được ở 120px
- Giữ hướng 捨ててた？/正解はコレ (đã curiosity + regret — tốt). Nhưng phải đồng bộ: nếu title khung cảnh báo thì thumbnail đừng khung "món ngon tốt".
- Test đè chữ đỏ cảnh báo 1 cụm cực lớn (VD `逆効果！?`) + mosaic món đáp án.

---

## 2. ĐÒN BẨY #2 — HOOK & CẤU TRÚC (áp cho video MỚI; video cũ không re-render)

1. **Payoff đầu tiên (第◯位 / mẹo #1) phải tới trước ~phút 2–3, KHÔNG phải phút 8.** Hiện checklist 12 câu + tự giới thiệu chiếm 8 phút đầu.
2. **Cắt checklist 12 câu → 5–6 câu sắc nhất** (むくみ/靴下の跡/泡/夜間トイレ/血圧). Phần còn lại rải sau, hoặc bỏ.
3. **Dời khối tự giới thiệu みのり + xin đăng ký ra SAU 第6位** (đang đúng luật cold-open nhưng vẫn nằm trong 8 phút đầu — kéo xuống sau payoff 1).
4. **90 giây đầu**: stake (câu 1) → 2–3 triệu chứng → "6 món, 1位 là món định番 mà nhà mày đang làm hỏng" (open loop) → vào 第6位 luôn.

## 3. ĐÒN BẨY #3 — ĐỘ DÀI

- Video 14' (ゆで卵) được đẩy mạnh nhất; 35' bị bóp sớm nhất. **Hạ chuẩn kênh non xuống ~15–20 phút** (6.000–7.000 ký tự) cho tới khi qua sandbox, thay vì 35–40'.
- Ít món hơn nhưng payoff dày hơn > nhiều món lê thê.

## 4. KỲ VỌNG THỰC TẾ (không tô hồng)

- Kênh **đang bị YouTube test** (1 sub, 7 video) — bình thường. Không chết, không bị bóng đè (impressions > 0).
- Các sửa trên **tăng xác suất graduate**, KHÔNG đảm bảo viral. Cần **10–20 video đều tay** để YouTube chốt rổ + có baseline Analytics riêng.
- Đo lại sau 2–3 tuần: CTR có nhích về 3–4%? Rổ đề xuất có dịch sang 四毒/警告 (mục "Nội dung giúp người xem tìm thấy")?

## 5. MỔ ĐỐI THỦ CHUẨN — 長生きの秘訣 (@長生きの秘訣22, soi browser 2026-07-21)

> Chọn làm mẫu vì: đúng ngách food×health シニア faceless, **tick nhãn "Tạo bằng AI" công khai mà vẫn ăn reach** (nhãn AI không phải án tử), tuổi kênh gần mình nhất trong nhóm thắng lớn. Đối chiếu thêm: ドクター健康ラボ 16,9K · 男の健康大学 6,8K · 長生きする健康雑学 128K nhưng 1.500 video ngắn kiểu cày cũ — không đáng học.

### 5.0 Đường cong trưởng thành (bài học kỳ vọng)
- **96,6K sub / 151 video / ~12 tháng tuổi.** Nhưng: **~2 tháng đầu (30+ video) lạc đề + flop** — điều hòa, thời trang, diệt cỏ, 100–2.900 view, độ dài lung tung 30–47′.
- **Tháng thứ 3 khóa rổ 「食べ物 × cảnh báo × tạng × シニア」→ nổ ngay loạt:** 納豆に「これ」100K · 魚やめて 77K · 白内障×食べ物 14K · たんぱく質TOP5 8,3K. Từ đó hit đều 15K–695K.
- → Kênh mình 7 video/56 view **đang ở đúng giai đoạn flop-tìm-rổ mà đối thủ cũng từng trải**. Bệnh không phải "chết kênh", là chưa vào rổ + chưa đủ volume.

### 5.1 Bảng bắt bệnh (họ vs mình)

| Chiều | 長生きの秘訣 (thắng) | 60代からの食卓 (hiện tại) | Kết luận |
|---|---|---|---|
| **Khung title** | 【tag cảnh báo】絶対に避けたい／危険／NG／実は間違い + **giấu đáp án** (コレ・ここ・この食品) | 「腎臓に良い食べ物ランキング」— khung tích cực | Khớp chẩn đoán Mục 0: sai rổ. Khung cảnh báo + curiosity gap là chuẩn ngách |
| **Thumbnail** | **Chữ khổng lồ 3 dòng** (trắng/đỏ/vàng viền đen đậm) chiếm ~2/3 khung + ảnh thật + mũi tên đỏ — đọc rõ ở 120px | Ảnh moody 1 điểm nhấn + cột chữ thanh lịch | Cùng bệnh chouhen: đẹp nhưng lạc meta rail. CTR 1,7% vs kênh thắng |
| **Payoff #1** | **4:36** (video 22′) — trước đó: stake 30s → triệu chứng → gỡ friction → open loop | **8:20** (video 35′) | Đòn bẩy #2 Mục 2 đúng hướng, chốt mốc ≤4′ |
| **Open loop xương sống** | Hứa 「たった1つの確認ポイント」ở 4:20 → **trả ở 19:30** (gần cuối) → kéo retention xuyên video | Open loop theo từng món | Học: 1 loop LỚN xuyên video, trả sát cuối |
| **Cấu trúc kép** | 「4 tránh + 4 nên」— sợ trước, thưởng sau | Ranking 6 món tốt | Khung "X tránh + Y nên" = cảnh báo mở màn nhưng kết dương — hợp compliance mình |
| **Độ dài** | Sau pivot ổn định **20–30′** (thời flop toàn 30–47′!) | 35–40′ | Chính đối thủ cũng bỏ video dài khi tỉnh ra. Đòn bẩy #3 chuẩn: 15–25′ |
| **Nhịp đăng** | **週4回 công khai trong 概要欄** (thực tế cách nhật) | thưa | Volume = số lượt thuật toán chia bài test (giống kết luận chouhen) |
| **概要欄** | Boilerplate kênh + 1 câu SEO + disclaimer + 4 hashtag — KHÔNG timeline công phu | Mô tả SEO đầy đủ | Description không phải yếu tố thắng — đừng đổ thêm công vào đó, dồn công vào thumbnail/title |
| **CTA** | Chỉ cuối video: like → 「comment tôi đọc hết」→ đăng ký → tease 次回 | CTA giữa ~50% + cuối | Giữ CTA giữa của mình (rule hệ thống), không học gì thêm |
| **Kiếm tiền phụ** | Gắn 4 sản phẩm Rakuten affiliate đúng chủ đề video | chưa | Ghi nhận, tính sau khi kênh sống |
| **Persona** | "Nữ bác sĩ AI" áo blouse + kể 「患者さん」 | みのり gian bếp, cấm xưng bác sĩ | ⚠️ KHÔNG copy — vi phạm ranh giới YMYL mình đã chốt. みのり giữ nguyên; độ "đanh" lấy từ khung cảnh báo, không lấy từ mạo danh |

### 5.2 Việc rút ra (chờ user duyệt trước khi sửa skill/rule)
1. **Thumbnail đổi hệ text-dominant cảnh báo** (3 dòng chữ lớn viền đậm + ảnh thật + mũi tên) — đụng chuẩn Phần E `02_THUMBNAIL_TITLE_RULES.md` user đã chốt → **cần user quyết** (giống cú chuyển text-wall bên chouhen).
2. **Độ dài hạ 15–25′ + payoff #1 ≤ phút 4 + 1 open loop lớn trả sát cuối** (khớp đòn bẩy #2, #3 đã ghi ở trên).
3. **Nâng nhịp đăng lên cách nhật trở lên** khi tồn kho cho phép (chouhen đã chốt 1/ngày sau mổ 0-view).
4. **Kho premise proven để REMAKE/viết mới cùng rổ:** 納豆+「これ」(100K) · 魚 tránh/nên 4+4 (77K) · パン 4+4 (đang chạy, cả 養生ノート・老後健康 cũng remake đề này) · 卵×腎臓 (502K) · 果物×腎臓 (519K) · ゼラチン (485K) · 麦茶 vs nước. Đề nào cũng khớp 4 trụ CONTENT_PLAN.
5. **Nhãn AI không đáng sợ** — đối thủ tick 「Âm thanh/hình ảnh tạo bằng AI」 công khai vẫn 96K sub. Hết lăn tăn chuyện disclosure.
6. **Compliance khi bắt chước title/thumbnail họ:** 危険・避けたい・NG・逆効果・実は間違い・寿命を縮める = sạch; **né** 死滅・がんの原因 (họ dùng, mình không theo — YMYL + bảng từ mục 3 luật gốc); tuyệt đối không 医師警告/áo blouse.

## 5.4 BENCHMARK ĐO SÂU API (2026-07-22) — giờ đăng + top chủ đề 長生きの秘訣

- **Giờ đăng (14 video gần nhất): 13/14 video trong 19:00–19:58 JST, đều đặn CÁCH NHẬT (2 ngày/video ~ 3-4/tuần)** — đăng THẲNG VÀO đầu peak senior 19時台 (総務省), không đăng trước 2–3h như baseline Buffer. Shokutaku/health đang đăng 16:00 JST → 2 trường phái; số của kênh thắng nghiêng 19h. Muốn đổi → chờ user duyệt, đổi thì đo A/B 2 tuần.
- View gần đây dao động mạnh 764–29K (không phải video nào cũng nổ), hit tháng 6: 一日2食 94K · 夜中3時に目が覚める 79K → kênh sống bằng tỉ lệ trúng ~1/5 video, không phải trúng đều.
- **Top chủ đề mọi thời đại (rổ đề tài):** シミ/da lão hóa 695K · ゼラチン 486K · サバ缶 ăn sai cách 428K · phòng ung thư bằng ăn uống 297K · thói quen đi bộ 100 tuổi 270K · 麦茶 249K+195K · 肩甲骨 100 lần/ngày 220K · ヨーグルト ăn đêm 207K. Mẫu số: **thực phẩm/động tác RẺ QUEN THUỘC × cơ chế trẻ hóa (mạch máu・não・da・xương khớp) × khung 衝撃/9割/知らないと損**. Gần đây kênh mở thêm mảng "đồ nguy hiểm trong nhà" (100均 nguy hiểm 29K).
- ⚠️ Kênh cùng ngách 輝く毎日 (6,8K sub) — claim kiểu 「糖尿病薬より5倍効く果物」 = medical misinformation risk, kênh đã chết từ 11/2025: **anti-model**, đừng học từ ngữ của nó (みのり giữ trần YMYL như luật).

## 5.5 TỒN KHO CHỜ UP — thumbnail đã quét v5 (2026-07-21 tối)

- ✅ `06_VIDEO/05_kyabetsu-tabeawase/thumbnail_v5.png` — 晩酌のキャベツ／お守り？／実は誤解 (nền cab_6038039 bắp cải cắt sáng + cà chua; thay bản vB moody tối + thumbnail.png placeholder navy trùng với 2 video health). Đã copy đè `thumbnail.png` cho upload_pack.
- ✅ `06_VIDEO/09_ryokucha-naizoshibo/thumbnail_v5w.png` (folder có v5 đánh-số-cũ nên thêm hậu tố w) — 毎日の緑茶／NGな飲み方／逆効果かも!? (nền slide_02 chén trà xanh sáng; text giữ khung cảnh báo cũ vốn đã chuẩn, chỉ đổi nền sáng + phóng chữ). Đã copy đè `thumbnail.png`.
- Video ĐÃ đăng của kênh này (7 cái) sẽ quét v5 đợt riêng — azuki xong rồi (`07_UPLOADED/04_azuki-rokutsu/thumbnail_v5.png`, chờ swap Studio).

## 6. CHECKLIST ÁP DỤNG
- [ ] Video đã đăng (08 腎臓, ゆで卵, 05–07): đổi TAG + đổi TITLE khung cảnh báo + thay dần thumbnail v5 (Studio, không re-upload) — gói text đề xuất sẵn ở Mục 1
- [x] ~~Skill + luật~~ **ĐÃ SỬA 2026-07-21 (user OK "sửa theo công thức thắng"):** skill `script-shokutaku` (mặc định 15–25′, bộ xương v2 payoff ≤4′, persona sau món #1, open loop trả 80–85%, title P0, thumbnail 3 dòng v5) · `02_THUMBNAIL_TITLE_RULES.md` → v5 WARNING-FIRST · project `CLAUDE.md` (khối PLAYBOOK SANDBOX) · `03_CONTENT_PLAN.md` mục 2.5 (khung cảnh báo + kho premise proven) · `upload-schedule.md` + `upload_pack.py` slots (4/tuần CN·T2·T4·T6; health dời sang T3·T7)
- [ ] Video tiếp theo viết theo playbook này (bắt đầu từ hàng đợi 10–12 đã re-angle theo mục 2.5 CONTENT_PLAN)
- [ ] Thumbnail v5 đầu tiên: nâng cấp `make_thumb.py` thêm mũi tên/khoanh đỏ, render xong thay bảng mẫu Phần E
- [ ] Sau 2–3 tuần đo lại bằng `analytics_report.py --channel shokutaku` (CTR nhích 3–4%? rổ đề xuất dịch sang 警告?)
