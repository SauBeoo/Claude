# KHÁM KÊNH 真夜中の朗読便 — 2026-08-12

> Đo bằng YouTube Data API + Analytics API (token chouhen), **24 video**, cửa sổ 2026-06-01 → 08-12,
> cộng đo **6 kênh đối thủ CÙNG RAIL** — lấy đúng từ `insightTrafficSourceDetail` của chính kênh mình,
> tức là bộ kênh YouTube **thật sự** ghép chouhen vào, không phải bộ kênh tìm bằng search.
> **ĐÈ:** `CHANNEL_DIAGNOSIS_2026-08-01.md` §1.1 (ngưỡng AVD) · `CTR_PLAN_2026-07-28.md` (căn cứ độ dài)
> · `CLAUDE.md` §Title (tag-đầu) · §THUMBNAIL (`--bg-target` thấp).
> ⚠️ `impressions` / CTR vẫn bị Google rút (từ 2026-07-30) → mọi kết luận dưới đây KHÔNG có CTR.

## 0. KẾT LUẬN MỘT CÂU

**Nội dung đã đủ tốt. Kênh chết ở BAO BÌ và SỐ VÉ.**
Chouhen đang chơi luật của một ngách khác — video ngắn, tag đầu title, nền thumbnail dập gần đen
không một bóng người, SEO nặng — trong một rail mà **mọi kênh sống** đều chạy title câu văn trần,
thumbnail đầy người đang diễn, 0 tag, và rất nhiều vé.

---

## 1. SỐ THẬT

Kênh: **5 sub · 1.044 view · 24 video** (5 tuần). **86% view đến từ 5 video.**

| ngày | dài | view | AVD% | phút xem | rail |
|---|---|---|---|---|---|
| 07-06 | 43′59 | 91 | 26,2 | 1.047 | RELATED 80 |
| **07-25** | 29′03 | **273** | 33,0 | 2.613 | RELATED 171 · SUB 87 |
| **07-27** | 40′42 | **367** | 32,2 | 4.805 | RELATED 288 · SUB 48 |
| 07-28 | 34′04 | 4 | 48,6 | 66 | RELATED 3 |
| 07-29 | 33′19 | 47 | 27,8 | 434 | RELATED 42 |
| **07-30** | 27′34 | **124** | 49,2 | 1.680 | RELATED 109 |
| 07-31 | 36′09 | 3 | 53,1 | 57 | SUB 2 · EXT 1 |
| 08-01 | 33′12 | 1 | 0,7 | 0 | RELATED 1 |
| 08-03 | 33′19 | 2 | **49,7** | 33 | SEARCH 1 · RELATED 1 |
| 08-04 | 37′44 | 2 | **49,8** | 37 | RELATED 2 |
| 08-05 | 46′34 | 1 | 0,6 | 0 | SUB 1 |
| 08-06 | 35′17 | **0** | — | 0 | — |
| 08-08 | 36′09 | **0** | — | 0 | — |
| 08-09 | 32′22 | 5 | **53,1** | 85 | RELATED 4 |
| 08-10 | 35′07 | 17 | 35,2 | 210 | RELATED 17 |
| 08-11 / 08-12 | 36′01 / 59′22 | 2 / 2 | — | — | quá mới, chưa có số Analytics |

🔴 **`BROWSE_FEATURES` = 0 TUYỆT ĐỐI trên 24/24 video, suốt đời kênh.** `YT_SEARCH` ≈ 0.
Rail duy nhất từng chạy là `RELATED_VIDEO`.

### 1.1 Loại trừ được án phạt / lỗi cấu hình
`madeForKids=False` · `embeddable=True` · không `regionRestriction` · `license=youtube` ·
cat **24** · `defaultLanguage=ja` ở 16/16 video kiểm · channel `country=JP`, `defaultLanguage=ja`,
keywords + description đủ. **Không có gì bị khoá.**

---

## 2. 🔴 PHÁT HIỆN LẬT NGƯỢC — RETENTION ĐÃ SỬA XONG, VIEW VẪN 0

| video | AVD% | view |
|---|---|---|
| 07-27 (hit lớn nhất kênh) | 32,2 | **367** |
| 07-25 | 33,0 | **273** |
| **08-09** | **53,1** | **5** |
| **08-04** | **49,8** | **2** |
| **08-03** | **49,7** | **2** |

`RETENTION_FORMULA_2026-08-11.md` **đã chạy đúng như thiết kế**: AVD từ 32% lên **50–53%**.
View **không nhúc nhích một chút nào**.

⇒ **Ngưỡng "AVD ≥33% → rail mở · ≤24% → rail đóng" (`CHANNEL_DIAGNOSIS_2026-08-01.md` §1.1) SAI.**
Nó là tương quan đọc ra từ n=14 và bị 3 video mới phủ định thẳng: **AVD cao gấp rưỡi hit mà view kém
70 lần.**

⇒ **Retention không còn là nút thắt.** Công thức 12 số vẫn giữ và vẫn có giá trị — nhưng nó giữ chân
**người ĐÃ vào**, nó **không kéo người vào**. Đừng đổ thêm công vào đó nữa.

📌 Đây là **lần thứ hai** cùng một kiểu sai: cả hai lần đều lấy một tương quan trong nội bộ kênh trên
mẫu <20 video rồi dựng thành ngưỡng nhân quả. Lần sau muốn đặt ngưỡng thì phải có **mẫu ngoài kênh**
hoặc phải chờ biến đó đổi mà kết quả đổi theo.

### 2.1 RELATED của kênh này KHÔNG phải "rail" — nó là đuôi phân mảnh

Video 367 view: **top-25 nguồn RELATED cộng lại chỉ 42 view** (nguồn cao nhất = 4 view).
⇒ 288 view RELATED trải trên **200+ video nguồn khác nhau, mỗi cái 1–4 view**, và trong đó có
bóng chày, mèo cưng, phim Trung, công ty xây dựng, máy đánh bạc.
**0 view đến từ video của chính kênh** ⇒ 24 video **không đỡ nhau**, không có vòng tuần hoàn nội bộ.

Đó không phải hình dạng của "được vào rail". Đó là hình dạng của **được rắc thử một lượt rất rộng rồi
gần như không ai bấm** — tức bài toán **CTR/bao bì**, đúng thứ Google vừa rút mất metric.

---

## 3. BỘ ĐỐI THỦ CÙNG RAIL — chỗ đau thật

| kênh | lập | sub | video | nhịp | **ĐỘ DÀI** | view/video (6 bản mới nhất) |
|---|---|---|---|---|---|---|
| 毎日スカッと | 2023-10 | 19,7K | 69 | **17,5/tuần** | **116–148′** | 872 → **105.183** |
| 裏話オーディオ | 2023-05 | 12,9K | 64 | **21,9/tuần** | **115–153′** | 48 → 2.223 |
| 孤独な桜の木 | 2010 | 3,8K | 84 | **21,9/tuần** | **83–134′** | 541 → 15.764 |
| 語り茶屋 | 2025-08 | 6,05K | 45 | 8,8/tuần | **77–141′** | 7 → 4.868 |
| 人生ドラマ | 2026-05 | 8,24K | 179 | 8,8/tuần | 13–40′ | 2.191 → 15.191 |
| **chouhen** | — | **5** | **24** | 7/tuần | **27–40′** | 0 → 17 |

### 3.1 TITLE — 0/25 video của 4 kênh peer mở đầu bằng `【】`

Họ dùng **câu văn trần 60–90 ký kể trọn setup + cú lật**:
- 毎日スカッと (105K): 「両親が通院のため一晩うちに泊まっただけで、義母は見下して追い出した。夫は黙って見ていただけ。私はその場で夫と義母を家の外へ叩き出した――」
- 孤独な桜の木 (15,8K): 「夫と愛人は海外で結婚式を挙げ、義家族12人も全員出席した。だが夫が帰国すると、入国審査官から冷たい通告を受けた――。**| 感動する話 | スカッとする話**」
- 裏話オーディオ: 「孫5人のうち、義母は私の娘だけ純金40gの祝いを渡さなかった。私は黙って毎月50万円の生活費を止めた。す…」

**chouhen: 24/24 mở bằng `【スカッとする話】`, đóng `【修羅場】【朗読】`.**
Luật "tag là ký tự số 1" (chốt 2026-07-21) đi ngược **toàn bộ** bộ kênh đang thắng cùng rail.
⚠️ Hai kênh **có** dùng 【】 là 嫁子 (233K, lập 2022) và スカっとゼミ! — đều đã có thương hiệu.
Kênh 5 sub dùng khuôn của kênh 233K sub là copy sai thứ.

📌 Cách giữ được keyword: 孤独な桜の木 đẩy nó xuống **ĐUÔI** bằng `| スカッとする話 | 修羅場`.

### 3.2 🔴 THUMBNAIL — chouhen cố tình vứt đúng thứ peer sống nhờ

Soi tận ảnh (peer tải về từ API vs `07_UPLOADED/*/_upload/thumbnail.png`):

| | chouhen 09 (**hit 367**) | chouhen 21 (17 view) | 毎日スカッと (**105K**) | 語り茶屋 / 孤独な桜の木 |
|---|---|---|---|---|
| nền | phòng tối **gần đen** | washitsu sáng | **đen tuyền** | **ảnh cảnh photoreal SÁNG, 70–75% khung** |
| người | **KHÔNG một mặt nào** | 2 người dán 2 mép | **cụm 5 người biểu cảm + phong bì**, dồn 32% phải | **2–4 người đang DIỄN đúng cảnh truyện** |
| chữ | 5 dòng phủ toàn khung | 4 dòng giữa | 6 dòng chiếm 68% trái | **chỉ 2–3 dải, ở đáy/đỉnh** |

**Hai khuôn peer khác hẳn nhau về nền, nhưng GIỐNG NHAU ở đúng một điểm: nhân vật có biểu cảm đang
diễn đúng cảnh truyện.** Khuôn `m08` của chouhen (`--bg-target 30`, và câu luật *"nền p20 phải ≤10/255"*
trong `CLAUDE.md` §THUMBNAIL) **chủ động dập nền xuống gần đen** — tức ném đi đúng thứ đang mua click
cho peer. Thumbnail của video hit lớn nhất kênh là **một căn phòng trống không có ai**.

⚠️ Ghi rõ giới hạn của phép đo này: **không có CTR để chứng minh nhân quả.** Đây là *khác biệt hình
thái đo được* giữa bộ đang thắng và bộ đang thua trong **cùng một rail**, không phải thí nghiệm.

### 3.3 Metadata: thứ chouhen đổ nhiều công nhất, rail này KHÔNG dùng
- 毎日スカッと, video **105.183 view**: **description RỖNG (0 ký), 0 tag.**
- 孤独な桜の木 (15.764 view): 0 tag, desc chỉ có disclaimer フィクション + list phần mềm.
- 語り茶屋 (VOICEVOX, cùng công nghệ): 0 tag, hashtag nhét đuôi title.
- **chouhen: 27–41 tag + 900–1.700 ký mô tả + 目次 ở mọi video.**

Không phải nó hại — nhưng **nó không phải chỗ có đòn bẩy**, và nó đang ăn giờ sản xuất.

### 3.4 SỐ VÉ — rail này là xổ số
Trong **CÙNG một kênh, CÙNG một ngày**: 裏話オーディオ ra 48 view và 2.223 view; 毎日スカッと ra
872 view và 105.183 view. Hit gánh kênh. Peer có 45–3.349 vé. **chouhen có 24.**

### 3.5 ⚠️ Nhưng dài + nhiều KHÔNG tự động thắng
- chouhen **đã thử dài rồi**: 07-09 (1h04)=4 view · 07-12 (1h17)=5 · 07-14 (1h00)=6 · 07-19 (1h07)=17.
- 美しい花の形: **310 video, 2.760 sub → 51 view/video.** Volume không cứu.
⇒ Độ dài/volume là **điều kiện cần, không đủ**. Đó là lý do đi **bao bì trước**.

---

## 4. ĐƯỜNG ĐI ĐÃ CHỐT (user 2026-08-12)

**① Bao bì trước, rồi mới tính tăng vé · ② cắt cả 3 lớp SEO nặng / A-B 3×3 / FX-ambience ·
③ giữ nhịp 1 video/ngày.**

| GĐ | việc | trạng thái |
|---|---|---|
| **1** | TITLE khuôn câu văn trần · THUMBNAIL bắt buộc ≥2 người diễn + 1 vật chứng, 2 khuôn K1/K2 mỗi khuôn 5 video | áp từ video 24 |
| **2** | mô tả về ~300 ký · tag 0–8 · bỏ 目次 · 1 title + 1 thumbnail · bỏ FX.json + ambience (GIỮ `--bgm auto`) | làm cùng GĐ1 |
| **3** | nạp lại `01_SOURCES` (**đang RỖNG**) 20–30 premise proven-viral từ đúng 4 kênh peer trên | dùng giờ tiết kiệm được |
| **4** | **chỉ mở nếu GĐ1 thất bại** — thử độ dài 90–150′ theo khuôn 4/5 peer | chưa mở |

Chi tiết thi hành: `CLAUDE.md` §Title · §THUMBNAIL · §Đóng gói upload.

---

## 5. ĐO LẠI — 2026-08-22 (sau 10 video bao bì mới)

**Bảng quyết định mới — ĐÃ BỎ AVD ra khỏi bảng** (§2 chứng minh nó không liên quan tới view):

| chỉ số | mốc hiện tại | ngưỡng "ăn" |
|---|---|---|
| **trung vị view/video, 10 video mới** | **2** (10 video 07-31→08-12) | **≥20** |
| số video có RELATED ≥50 | **0/11** | ≥2/10 |
| `BROWSE_FEATURES` > 0 | **chưa từng xảy ra** | **>0 lần đầu = mốc quan trọng nhất** |
| CTR (đọc TAY trong Studio) | chưa đo | so với 10 video cũ |

🛑 **Phanh:** trung vị vẫn ≤5 view sau 10 video ⇒ biến không nằm ở bao bì → mở **GĐ4 (độ dài)**,
đừng làm vòng bao bì thứ hai.

### 5.1 Lệnh đo (read-only, đã chạy trong lượt này)
```bash
cd Projects/youtube-jp-chouhen
python tools/analytics_report.py --channel chouhen -n 30          # view/AVD toàn kênh
python tools/channel_diag.py --traffic                            # AVD + traffic source từng video
python tools/channel_diag.py --related <videoId>                  # RELATED đến từ video/kênh nào
python tools/channel_diag.py --peers                              # nhịp/độ dài/title-format bộ peer
```

---

## 6. LIÊN QUAN
- Bị đè: `CHANNEL_DIAGNOSIS_2026-08-01.md` §1.1 · `CTR_PLAN_2026-07-28.md` (độ dài) · `CHANNEL_DIAGNOSIS_2026-07-28.md` §3
- Vẫn đúng, giữ nguyên: `RETENTION_FORMULA_2026-08-11.md` (nhưng hạ khỏi vai "thứ quyết định view")
- Ngoại lệ đã ghi: `.claude/rules/ab-3title-3thumb.md` §6 · `.claude/rules/youtube-upload-seo.md` §5
