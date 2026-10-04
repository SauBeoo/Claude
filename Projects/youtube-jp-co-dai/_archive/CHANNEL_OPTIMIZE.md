# CHANNEL_OPTIMIZE — 古代の秘訣 (co-dai) — Mổ 0-view 2026-07-21

> Nguồn số liệu: YouTube Data/Analytics API (token readonly `credentials/token.json`) + soi browser đối thủ 2026-07-21.
> Cùng khung với đợt mổ chouhen/shokutaku/health 2026-07-21 (xem memory `project_kenh_0view_chan_doan`).

## 1. HIỆN TRẠNG KÊNH (đo 2026-07-21)

- 2 video public · tổng 21 view · **1 sub** · country JP đúng.
- **Video 01** `fHv_oPjO1t0` シロアリ駆除に10万円払う前に… (đăng 07-15, 22'47"): **12 view / 6 ngày**.
  - Nguồn traffic: YT_CHANNEL 5 · SUBSCRIBER 3 · YT_OTHER_PAGE 3 · YT_SEARCH 1 → **0 view từ BROWSE/RELATED/SUGGESTED**.
  - Retention (mẫu 12 view, nhiễu nặng): rớt còn 50% tại 1'08", 33% tại ~25%, đuôi 100% còn 8%. Avg view 31,1% (~7 phút/view).
- **Video 02** `NWPnrezfBDc` 蚊が寄りつかない庭は数百円で作れる… (đăng 07-19, 25'18"): **9 view / 2 ngày**, 1 comment. Chưa đủ data retention.
- **Cả 2 video index #1** khi search đúng title → KHÔNG án phạt / suppression.
- ⚠️ **Lỗ kỹ thuật phát hiện qua API: channel description RỖNG + channel keywords RỖNG** (`brandingSettings`). Đối thủ nhồi description đầy keyword + 3 hashtag.

**Kết luận bệnh:** giống chouhen video 01–06 — video **chưa từng được thuật toán phát impressions** (0 browse/related). Không phải sai rổ meta (khác shokutaku): title/thumbnail/tag/desc đã bám đúng công thức kênh thắng ngách. Kênh 6 ngày tuổi, 2 video, 0 sub — chưa tích đủ lượt test trong ngách đang RẤT đông kênh mới.

## 2. BENCHMARK CHỐT: 昔の人の知恵 (@昔の人の知恵)

> Chính là "kênh 生活の知恵 7.5K sub, video 348K" đã ghi trong CLAUDE.md mục thumbnail (2026-07-16). Đo lại 2026-07-21:

- **Lập kênh 08/06/2026 (6 tuần), video đầu ~3 tuần trước. 8 video → 554.032 view / 8,46K sub.**
- Bảng video (mới → cũ):

| Tuổi | Đề tài | View | Dài |
|---|---|---|---|
| 13h | 銅線 khử カビ nhà (4.000年の知恵) | 1,6K | 23:42 |
| 4d | スズメバチ巣 対策 (駆除業者が知られたくない) | 4,3K | 15:12 |
| 5d | 数百円の液体 hồi sinh 木製品 | 13K | 20:23 |
| 6d | 冷房なし 扇風機+ペットボトル làm mát | 6,4K | 25:22 |
| 2w | **蚊が抗えないもの (trap phát酵 + cây)** | **427K** 🔥 | 18:02 |
| 2w | 二枚の金属 浄化 nước | 71K | 29:29 |
| 3w | 除湿剤 tự chế 数百円 (除湿はこれ1つでOK!) | 45K | 18:58 |
| 3w | 屋根裏換気 アーミッシュ | 3,6K | 40:32 |

- **1 hit 蚊 chiếm 77% tổng view** → hit kéo cả kênh (related + channel page + sub base 8,46K làm bệ phóng cho video sau: video 13h tuổi đã 1,6K view).
- Nhịp đăng: **~1 video / 2–3 ngày** (8 video/3 tuần). Độ dài 15–29' là chủ lực (video 40' là con flop nhất kênh).
- Title format: `[hành động/lợi ích + số tiền rẻ]――[なぜ忘れられたのか／業者が知られたくない]` — co-dai đang dùng ĐÚNG format này, không cần đổi.
- Thumbnail: **ảnh thật macro + chữ VÀNG/TRẮNG viền đen KHỔNG LỒ (≥1/3 khung) + mũi tên đỏ + badge giá (約600円/電気代0円/34℃→21℃)** — loud hơn mức co-dai đang làm.
- **Video hit gắn nhãn AI (altered/synthetic) công khai vẫn 427K** → disclosure không giết phân phối (trùng phát hiện 長生きの秘訣 bên shokutaku).
- Description kênh: dài, nhồi keyword tự nhiên + #昔の人の知恵 #暮らしの知恵 #生活の知恵.

## 3. HỆ SINH THÁI NGÁCH (đo cùng ngày)

- **驚きの世界** (@驚きの世界-i9j): 7 video → 1,43K sub; hit 貧しい家庭の知恵25選 88K/3w, 祖父母の知恵25選 10K/2w. Format listicle 25選, dài 36–62'. → Kênh trẻ thứ 2 đang nổ, format khác (listicle đời sống 昭和).
- **ライフハック雑学**: video 庭から蚊が消滅 100円 → **63K view / 6 ngày**. → Rổ 蚊対策×庭 đang cực nóng giữa mùa.
- **今日も静かな一日**: 164 video / 5,68K sub, **ngừng đăng ~2 tháng**; view đời thường 100–2,4K; video ホウ酸 シロアリ (nguồn transcript video 01) chỉ 968 view/3 tháng. → Trần của format "đều đều không hit"; đừng lấy làm chuẩn.
- Ngách có nhiều kênh clone mới lập (search "昔の人の知恵" ra 3-4 kênh trùng tên 1–17 sub) → cửa sổ ngách đang mở nhưng cạnh tranh test tăng nhanh.

## 3.5 BẢN ĐỒ CHỦ ĐỀ ĐỐI THỦ (đo API 2026-07-22 — top video theo view từng kênh)

| Kênh | Lành nghề chủ đề | Bằng chứng view |
|---|---|---|
| **昔の人の知恵** (8,4K sub/8 video) | Mẹo NHÀ + VƯỜN theo mùa, khung "知恵 bị lãng quên + góc dòng tiền": côn trùng (蚊/スズメバチ), nước, 除湿, làm mát, カビ, phục hồi đồ gỗ | 蚊トラップ 428K · 浄水 71K · 除湿 45K |
| **ライフハック雑学** (15,8K sub/88 video, 5M tổng) | Mẹo vặt gia đình NHANH + tẩy rửa + côn trùng theo THÁNG (deadline marketing 「◯月中に必ずコレやって」): 黄ばみ, ムカデ, コバエ, アリ, khử mùi, 雑草 100円, 除湿 | 黄ばみプラスチック 982K · ムカデ tháng 5 685K · 雑草100円 525K · コバエ tháng 4 385K · 除湿 211K |
| **庭づくり大好きおじさん** (167K sub/316 video, 58M tổng) | 雑草対策 CHUYÊN SÂU (ドクダミ・スギナ nỗi ám ảnh quốc dân) + DIY sân vườn; format thực chứng "làm thử cho xem" | ドクダミ hasami 8,4M · ドクダミ khô 1 ngày 7,2M · 防草 1,9M · 蚊 100均 1,5M |
| **今日も静かな一日** (5,6K sub/164 video — kênh nguồn transcript video 01) | 家庭菜園/tự cung tự cấp + thực phẩm senior: đậu protein, siêu thực phẩm chống lão hóa, trồng cà chua/khoai, "cây bị lịch sử lãng quên", 食べ方×腎臓 | 大豆超え protein 77K · diệt côn trùng 1 thìa 56K · 神食材 não/cơ 35K |
| **驚きの世界** (1,4K sub/7 video) | Listicle hoài niệm 昭和 25選: mẹo nhà nghèo, ông bà tự lập, cơm chủ phụ 昭和, nghề tay biến mất | 貧しい家庭の知恵25選 89K · 主婦ごはん30選 14K |
| (tham chiếu chéo) **長生きの秘訣** — rổ shokutaku | 食べ物×cảnh báo×tạng (卵×腎臓 502K) — xem CHANNEL_OPTIMIZE shokutaku | 96K sub/151 video |
| (tham chiếu chéo) **苦しみの物語** — rổ chouhen | スカッと朗読 revenge, 2–3 video/ngày | 70–143K/video với 1,2K sub |

**Rổ đề tài ăn tiền giao thoa cho co-dai (xếp theo trần view đã chứng minh):** ① 雑草/ドクダミ/スギナ (trần 8,4M — video 03 đúng rổ) ② côn trùng theo mùa: 蚊 (428K–1,5M), ムカデ (685K, mùa 5), コバエ (385K, mùa 4), アリ (128K), スズメバチ ③ tẩy rửa/phục hồi: 黄ばみ (982K), カビ, đồ gỗ, khử mùi ④ 除湿/làm mát không điều hòa (45K–211K) ⑤ 家庭菜園 tự cung + cây bị lãng quên (35K–77K). Giờ đăng thắng của ngách: **11:00–13:00 JST** (8/8 video 昔の人の知恵; hit 428K lúc 13:00). Format deadline 「◯月中に」 của ライフハック雑学 = kỹ thuật urgency đáng mượn.

## 4. CHẨN ĐOÁN TỔNG (đối chiếu 2 kênh)

| | 古代の秘訣 | 昔の人の知恵 |
|---|---|---|
| Tuổi kênh lúc đo | 6 ngày (video đầu) | 6 tuần, video đầu 3 tuần |
| Video / nhịp | 2 · ~2/tuần (T6+CN) | 8 · ~1/2–3 ngày |
| Title format | ✅ giống nhau | (gốc format) |
| Thumbnail | Đúng hướng, chữ nhỏ hơn, ít badge giá | Chữ khổng lồ + badge giá + nhiệt độ |
| Channel desc/keywords | ❌ RỖNG | ✅ nhồi đủ |
| Đề tài | シロアリ (hẹp), 蚊×庭 plants (đúng sóng) | Pain-point mùa hè phổ quát: 蚊/除湿/カビ/làm mát |
| Phân phối | 0 impressions | Hit 蚊 427K kéo cả kênh |

Bệnh co-dai KHÔNG phải content/metadata sai — là **cold-start chưa đủ vé số**: mỗi video đăng = 1 lượt thuật toán test; kênh mới cần volume + đề tài trúng sóng mùa để 1 video "trúng" rồi kéo cả kho như đối thủ. 2 video/6 ngày là quá ít mẫu để kết luận kênh hỏng — nhưng lịch 2/tuần hiện tại là quá mỏng so với playbook kênh thắng.

## 5. HƯỚNG SỬA — TRẠNG THÁI THI HÀNH (user duyệt toàn bộ 2026-07-21, đã làm cùng ngày)

1. ✅ **Channel description + keywords ĐÃ ĐIỀN** qua API `channels.update` (2026-07-21): description JP đầy đủ + 3 hashtag (#生活の知恵 #昔の知恵 #古代の秘訣), keywords 13 cụm, country JP, lang ja. Script: scratchpad `update_branding.py` (chạy xong, không cần giữ).
2. ✅ **Video 03 夏の雑草 ĐÃ ĐÓNG GÓI** — `06_VIDEO/03_natsu-zassou/_upload/` (title chốt 雑草は抜くと増える…, 目次 timestamp thật từ srt 12:13, tags, thumbnail K5 flat-lay, hẹn giờ **2026-07-22 T4 11:00 JST = 09:00 VN** — gói lại 2026-07-22 sáng theo giờ mới). Script 03 đã thêm khối "ĐÓNG GÓI UPLOAD FINAL" format chuẩn parser. Còn thao tác tay: kéo thả Studio (profile 6) theo METADATA [1]→[8], xong chạy `--done`. Lưu ý: video 03 KHÔNG có BGM (audio mono = voice only) → credit chỉ VOICEVOX + Pexels.
3. ✅ **Lịch ĐÃ NÂNG 4/tuần: T2·T4·T6·CN, giờ chốt lại 11:00 JST cố định (user 2026-07-22, theo giờ đo thật benchmark)** — sửa slots upload_pack.py + bảng `.claude/rules/upload-schedule.md`. Đề tài ưu tiên khi viết tiếp: 蚊トラップ発酵 (427K proven), 除湿, カビ, làm mát không 冷房, ゴキブリ, スズメバチ — giữ 15–25'.
4. ✅ **Luật thumbnail ĐÃ KHẮC vào CLAUDE.md project** (chữ ≥1/3 khung + badge giá 数百円/0円 + badge số liệu) — áp từ video 04; thumbnail video 03 giữ bản user đã duyệt K5.
5. ✅ **Luật cold open ≤15s ĐÃ KHẮC vào skill** `script-co-dai/SKILL.md` (Mục 10 hook + checklist điểm 1) — áp từ script sau; video 03 stake đã nằm câu 1-2, không re-render.
6. **KHÔNG đổi:** title format, độ dài 20–25', giọng NHK, cấu trúc chương dòng tiền — đang đúng meta kênh thắng.

## 5.5 VÁ METADATA TOÀN KÊNH ĐỢT 2 (2026-07-22 — user duyệt "Ghi TẤT CẢ", áp qua API, theo khung audit chouhen cùng ngày)

Đo sâu metadata benchmark (昔の人の知恵 + 驚きの世界 qua API) → 2 kênh thắng đồng nhất 4 tín hiệu mà co-dai lệch. Đã vá:
1. ✅ **categoryId 22→27 (Education)** cả 3 video — cả 2 kênh thắng đều cat 27.
2. ✅ **Rổ 12 tag nhận diện kênh cố định** đứng đầu tag mọi video (benchmark: 10 tag đầu lặp y hệt toàn kênh, tổng 42–69 tag) → 3 video giờ ~25–31 tag.
3. ✅ **3 hashtag kênh cố định `#生活の知恵 #昔の知恵 #古代の秘訣`** đứng đầu dòng hashtag cuối desc (benchmark dùng bộ cố định kể cả trên hit 431K); video 03 có hashtag nằm DÒNG 1 desc → đã dời xuống cuối.
4. ✅ **Desc video 01 viết lại 447→~1.100 ký** (3 dòng hook + đoạn topical, chỉ dùng fact có sẵn); chuẩn benchmark 1.200–1.800.
5. ✅ **Banner** (bản PIL cổ thư ấm `06_VIDEO/channel_banner_draft.png`) + **trailer = video 02 蚊** + **playlist public đầu tiên** `PLP6QDSdnMp2Q` (3 video) + channel keywords mở 13→28 cụm.
6. ✅ Credit VOICEVOX: user đổi ý giữa chừng → **ĐÃ GỠ khỏi cả 3 desc** (xem CLAUDE.md mục compliance — ngoại lệ luật gốc, kèm ghi chú license).
7. ✅ Video 03 chạy `--done` chuyển kho (giữ mp4 vì không cắt TikTok — phễu hủy).
8. 📌 Phát hiện: benchmark 昔の人の知恵 từ 15/07 đã tăng nhịp lên **~1 video/NGÀY** (video 23h tuổi = 2,4K view) — ngách đua volume, lịch 4/tuần là SÀN.
9. Quy tắc đúc ra đã khắc: CLAUDE.md project (mục 📐 METADATA CHUẨN KÊNH) + `.claude/rules/youtube-upload-seo.md` mục 2.4 (áp mọi kênh).

## 6. VIỆC KHÔNG LÀM

- Không panic sau 6 ngày — chouhen video 00 cần ~1 tuần mới vào ramp. Đo lại sau khi có 6–8 video.
- Không copy nguyên bộ visual/đề tài đối thủ liên tiếp (luật inauthentic content) — rewrite 100% như skill quy định.

## 7. KHÁM LẠI BẰNG STUDIO — 2026-07-28 chiều (đủ 7 video, trả lời câu user "tỉ lệ xem + giữ chân rất thấp")

> Nguồn: YouTube Studio profile co-dai, cửa sổ 28 ngày 30/6–27/7 (impressions/CTR không có trong API — đo browser).

### 7.1 Số toàn kênh
**36 view · 277 impressions · CTR 6,9% · AVD 7:23 · +1 sub.** Kênh có 7 video, video đầu 15/07 → **13 ngày tuổi lúc đo**.

| Ngày | Video | Dài | View | Imp | CTR |
|---|---|---|---|---|---|
| 15/7 | 01 シロアリ | 22:47 | 12 | 36 | 13,9% |
| 19/7 | 02 蚊 10 plants | 25:18 | 14 | 67 | **17,9%** ← mạnh nhất kênh, có comment |
| 22/7 | 03 雑草 | 12:14 | 3 | 80 | 0% |
| 23/7 | 04 ゴキブリ | 19:14 | 2 | 32 | 3,1% |
| 26/7 | 05 スズメバチ | 27:11 | 3 | 28 | 3,6% |
| 27/7 | 06 排水溝 | 18:28 | 1 | 23 | 0% |
| 28/7 | 07 すだれ | 24:38 | 4 | 10 | 0% (vừa đăng) |

Nguồn view: **YouTube Tìm kiếm 44,4%** · Trang kênh 27,8% · Duyệt xem 19,4% · Suggested ≈ 0 (**chỉ 2,5% impressions từ đề xuất**).

### 7.2 Chẩn đoán (đối chiếu cảm nhận user)
1. **"Tỉ lệ xem thấp" — đúng hiện tượng, sai tên bệnh.** CTR 6,9% không hề thấp (chouhen chỉ 3,2%); kênh **chưa từng được thuật toán phát**: 277 imp/28 ngày cho cả 7 video. So sánh nội bộ: chouhen cùng trạng thái suốt 3 tuần đầu, đến video #8 (ngày 19, remake premise proven + 29′) rail mở → 5.100 imp/video ngay lập tức.
2. **"Tỉ lệ giữ chân thấp" — KHÔNG kết luận được.** 1–14 view/video = nhiễu thống kê thuần; AVD 7:23 trên video 19–27′ (~31%) là mức bình thường ngách. Cấm sửa retention dựa trên mẫu này.
3. **Không án phạt:** search vẫn dẫn 44% view, index tốt (đối chiếu §1).
4. **Metadata/lịch hết chỗ vá** (đã làm §5/§5.5) — đổi thêm chỉ tạo nhiễu.

### 7.3 Việc đã làm theo chẩn đoán (2026-07-29, user chốt hướng "dồn cụm 蚊")
- Đo premise 蚊 ≤30 ngày qua API: **蚊トラップ発酵 (昔の人の知恵, `1-p4aqr-Naw`) 456.738 view · 21.749/ngày — #1 toàn ngách**, đã có 2 kênh remake đều ăn (81K · 14,7K). Trends YouTube JP: cầu search cụm 蚊 thấp (2–6 điểm vs anchor すだれ 42) nhưng 「蚊 トラップ 自作」 breakout → video sống bằng suggested, đúng loại cửa kênh đang cần mở.
- **Script #14 ka-hakko-trap** viết + đóng gói xong (nửa TRAP của nguồn; nửa cây = video 02 → cụm session 2 video nhắc chéo). Chen sau #10, slot **T2 03/08** (ngày mạnh nhất ngách); chuỗi tease đã nối lại 07→08→09→10→14→11.
- Sổ: `00_TOPIC_LOG.md` (lịch mới + trục 害虫 6/14 → #15 bắt buộc ngoài 害虫).

### 7.4 Mốc đọc số kế tiếp
- **Khi đủ 10–12 video (~08–10/08):** tín hiệu thành công = ≥1 video được cấp lô imp **>500** từ browse/suggested (mốc hiện tại: max 80). Video 14 là ứng viên chính — premise đã được chứng minh phân phối ở 3 kênh.
- Nếu 12 video mà suggested vẫn ≈0 → mổ sâu lớp thumbnail/cold-open theo khung health (CHANNEL_DIAGNOSIS health 07-27), không đổi biến trước đó.
- Retention chỉ được phép chẩn đoán khi có video ≥100 view.
