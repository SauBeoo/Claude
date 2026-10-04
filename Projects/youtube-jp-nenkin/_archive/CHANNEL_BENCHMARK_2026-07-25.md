# BENCHMARK NGÁCH 年金・給付金 — đo API 2026-07-25

> Đo trực tiếp YouTube Data API (channels.list + videos.list) cụm 9 kênh ngách, xếp theo **sub/tháng** = tốc độ thật, không theo tổng sub (tổng sub thưởng cho kênh già).
> Lý do đo: user hỏi "ngách này nhiều kênh lớn làm rồi, đi hướng này ổn không?" — câu trả lời phải bằng số.

## 1. BẢNG ĐO

| Kênh | Sub | #video | Tổng view | Tuổi (tháng) | Lập | **sub/tháng** | **view/video** |
|---|---|---|---|---|---|---|---|
| **年金・給付金完全攻略** | 132.000 | **12** | 5,88M | **4,1** | **2026-03** | **31.847** | **490.103** |
| **元ハロワ職員まゆみのお金の安心相談室** | 162.000 | 34 | 8,14M | 8,5 | 2025-11 | 19.088 | 239.495 |
| **『資産保全学』50,60代の賢い資産の守り方** | 174.000 | 76 | 19,6M | 13,0 | 2025-06 | 13.425 | 257.856 |
| みんなの給付金・補助金ちゃんねる | 551.000 | 429 | 72,3M | 45,8 | 2022-10 | 12.041 | 168.507 |
| きな子のシニアお金ゼミ | 167.000 | 117 | 17,1M | 29,1 | 2024-02 | 5.730 | 146.491 |
| 税金・社会保障教育ちゃんねる | 70.500 | 145 | 11,0M | 37,4 | 2023-06 | 1.884 | 76.206 |
| シニアの年金・給付金速報 | 114.000 | 247 | 22,7M | 90,0 | 2019-01 | 1.266 | 91.943 |
| 給付金チャンネル | 87.100 | **1.971** | 35,2M | 91,2 | 2018-12 | 954 | **17.848** |
| フクロウの年金・給付金解説室 | 41.400 | 39 | 5,85M | 80,4 | 2019-11 | 514 | 149.976 |

## 2. BA KẾT LUẬN — đảo giả định cũ

### 2a. Ngách đang MỞ RỘNG, không bão hòa. Kênh càng MỚI càng tăng nhanh.
3 kênh tăng nhanh nhất đều lập **2025-06 trở về sau**; 3 kênh chậm nhất đều lập 2018–2019. Không có kênh già nào giữ được tốc độ. Đây là dấu hiệu **cầu tăng nhanh hơn cung** (sóng cải cách 2026 + dân số già), không phải red ocean đã chia hết phần.
→ Kênh nenkin lập 2026-07 **không hề muộn**.

### 2b. 完全攻略 KHÔNG phải "kênh già chiếm đất" — nó mới **4,1 tháng**, chỉ hơn nenkin 4 tháng.
Trước đây ta dùng "12 video → 130K" làm bằng chứng precision-model nhưng **không biết tuổi kênh**. Nó lập **2026-03**, tức bắt đúng sóng cải cách 4/2026 và nổ trong 4 tháng. Nghĩa là:
- ⚠️ **Video top của nó (定期便に載らない 3,79M) là video MỚI, đang khỏe, thuộc kênh 132K** → đánh trực diện query này lúc kênh mình 0 sub là chọn chỗ khó nhất. **PHẢI lùi topic này về sau** (xem `02_CONTENT_PLAN` GĐ C).
- ✅ Nhưng nó chứng minh: một kênh lập cùng thời điểm với mình, ngách này, vẫn nổ được trong 4 tháng.

### 2c. VOLUME LÀ CHIẾN LƯỢC THUA — chênh 27 lần hiệu suất/video.
| | 完全攻略 | 給付金チャンネル |
|---|---|---|
| Số video | **12** | **1.971** |
| Sub | **132.000** | 87.100 |
| View/video | **490.103** | **17.848** |
164 lần số video → **ít sub hơn**. Cày số lượng trong ngách này không mua được gì.
→ **Đây là căn cứ hạ nhịp đăng** (chốt 2026-07-25: 3/tuần → **2/tuần T2·T4**), dồn công vào chất lượng từng video.

## 3. MÓC ĐỊNH VỊ của 3 kênh thắng nhanh — và của mình

| Kênh | Móc | Copy được? |
|---|---|---|
| 元ハロワ職員まゆみ | **Uy tín người trong hệ thống** ("tôi từng làm ở Hello Work") — dạng mạnh nhất của motif 役所が教えない | ❌ TUYỆT ĐỐI KHÔNG — bịa tư cách = vi phạm YMYL rule + gian dối |
| 『資産保全学』 | Khung **「学」= một môn học** (資産保全学) | ✅ **Đã có bản tương đương: 研究室** — 174K/13 tháng xác nhận khung học thuật KHÔNG lép ở ngách này |
| 完全攻略 | **「完全攻略」= trọn bộ, đọc hết hộ bạn** + độ dài 25–59′ | phần nào — mình đi bằng chiều sâu từng đề tài |
| **nenkin (mình)** | 研究室 + dàn モニター + **⭐ 原典を見せる (chiếu tài liệu gốc, khoanh đỏ con số)** | — |

**Kết luận về khác biệt:** 研究室 đã được validate, nhưng còn *mềm* so với 元ハロワ職員. Lớp bù đắp **honest và không ai làm**: chiếu đúng trang 日本年金機構/厚労省 lên màn hình + khoanh đỏ con số đang đọc → biến 「当研究室は原典を一緒に読む」 từ lời nói thành **bằng chứng thị giác**. Kênh persona-giả không dám copy (họ không có nguồn thật để chiếu). Đã khắc vào skill `script-nenkin` (GĐ0d + GĐ4) + chuẩn visual CLAUDE.md + khuôn thumbnail G.

## 4. THÔNG SỐ SẢN XUẤT đo từ kênh thắng
- **Độ dài:** まゆみ 19′ · 税金・社会保障 18′ · 資産保全学 43′ · 完全攻略 25–59′ → chuẩn 18–25′ của mình OK, **video flagship nên kéo 25–30′**.
- **Nhịp:** 完全攻略 ~0,7/tuần (12 video/4,1 tháng) · まゆみ ~1/tuần · 資産保全学 ~1,3/tuần → **cả 3 kênh nhanh nhất đăng ≤1,3/tuần**. Nhịp 2/tuần của mình vẫn cao hơn họ; nếu lớp 原典+thumbnail không theo kịp thì **hạ 1/tuần còn tốt hơn ra 2 video nhạt**.
- **Góc 2026年改正 ĐÃ có người cày** từ tháng 3–4/2026 (完全攻略 lập 2026-03; 資産保全学 có video 繰上げ繰下げ 2026改正 557K; まゆみ có 2026新ルール+申請忘れ 2,57M) → dư địa còn ở **mốc hiệu lực SAU** (遺族年金 2028, 基礎年金底上げ, 標準報酬上限, 適用拡大) + vòng cập nhật 年度 hằng năm.

## 5. VIỆC PHÁI SINH (đã làm cùng ngày)
- [x] Hạ nhịp 3/tuần → **2/tuần T2·T4 19:00 JST**, sync `upload-schedule.md` + `upload_pack.py` + `CLAUDE.md`
- [x] Thêm lớp **原典を見せる** vào skill `script-nenkin` + chuẩn visual + khuôn thumbnail
- [x] Tái xếp `02_CONTENT_PLAN.md`: long-tail sâu lên GĐ A, **mega-evergreen (定期便に載らない / 何歳受給の末路 / いくらもらえる) lùi về sau khi có uy tín**
- [ ] Đo lại bảng này mỗi 6–8 tuần (đặc biệt: 完全攻略 có giữ được 31.8K sub/tháng không, hay tốc độ 4 tháng đầu là hiệu ứng sóng cải cách)
