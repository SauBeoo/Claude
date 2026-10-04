# 08_ANALYTICS_LOG — 古代の秘訣 (co-dai) · sổ A/B + sổ đổi title trên kênh

> Sổ này là **nơi duy nhất** ghi: video nào đang chạy bản A/B nào, đổi title ngày nào, và số đo được.
> Luật: `.claude/rules/ab-3title-3thumb.md` · `.claude/rules/youtube-upload-seo.md` §0.5
> Tạo 2026-08-05 khi làm loạt thay thumbnail + title A/B.

---

## 0. 🔴 ĐỌC TRƯỚC — API KHÔNG tạo được A/B test thumbnail

`thumbnails.set` của YouTube Data API **chỉ đặt MỘT ảnh đang hiện**. Chức năng **"Test & compare"** (nạp 2–3 ảnh, YouTube luân phiên rồi trả CTR từng bản) **chỉ có trong YouTube Studio, phải nạp bằng tay**. Không có endpoint API nào cho nó.

→ **Quy trình đúng:**
1. Tool dựng file T1/T2 (đã xong, xem §1)
2. **Người** mở Studio (Chrome `Profile 6`) → video → Thumbnail → **Test & compare** → nạp T1 + T2
3. Để chạy **≥7 ngày**, **GIỮ NGUYÊN TITLE suốt lúc đó** (đổi title giữa chừng = lẫn 2 biến, kết quả vô nghĩa)
4. Chốt thumbnail → **rồi mới** xoay title A2/A3 tuần tự, mỗi bản ≥7 ngày, ghi ngày vào §2

⛔ Đừng dùng `update_live.py --only-thumb` để "đẩy T2" — nó **ghi đè** T1 chứ không tạo test. Chỉ dùng khi muốn THAY hẳn.

---

## 1. BỘ T1 / T2 — 4 video, sẵn sàng nạp Studio (2026-08-05)

> 🟡 **HẠ ƯU TIÊN 2026-08-12** — đọc §5 trước khi bỏ giờ vào mục này. CTR đo tay ra **4,7% tổng /
> 14,3% ở bản tốt nhất = ĐẠT** ⇒ thumbnail **không phải nghi phạm**. Việc còn đáng làm ở tầng ảnh chỉ
> là 2 bản **0% CTR**: video **03** (142 imp) và **17** (20 imp).

| video | videoId | T1 (đang live) | T2 (mới, chưa nạp) | biến thử |
|---|---|---|---|---|
| 02 蚊の庭 | `NWPnrezfBDc` | `06_VIDEO/_relive/stamped_02.jpg` | `06_VIDEO/_relive/t2/final/thumb_T2_02.jpg` | **ẢNH** (chữ y nguyên) — chậu hoa nắng + muỗi ngoặt ra, thay cảnh vườn cũ |
| 07 すだれ | `OZj3enOedQk` | `06_VIDEO/_relive/stamped_07.jpg` | `.../thumb_T2_07.jpg` | **ẢNH + thủ pháp** — mũi tên nhiệt dội khỏi rèm sáo, chữ đổi sang `熱の7割` |
| 05 スズメバチ | `lQ7P_jN9mqM` | `06_VIDEO/_relive/stamped_05.jpg` | `.../thumb_T2_05.jpg` | **ẢNH + chữ** — cùng một tổ HAI kích cỡ (ゴルフボール→バスケットボール), chữ `千匹` |
| 14 蚊トラップ | `Edfjmu-gRjg` | `06_VIDEO/_relive/stamped_14.png` | `.../thumb_T2_14.jpg` | **ẢNH + chữ** — luồng hơi thở nhìn thấy được, chữ `50m` |

⚠️ **Chỉ `02` là A/B SẠCH** (đổi đúng 1 biến = ảnh, chữ giữ nguyên). `05` `07` `14` đổi **cả ảnh lẫn chữ** → nếu chúng thắng thì **không biết thắng vì cái nào**. User chốt 2026-08-05 chấp nhận đánh đổi này để lấy bản đâm hơn. Ghi ra để sau đọc số không kết luận sai.

Tất cả T2: 2731×1536 đúng 16:9 · dưới trần 2 MB · có dấu nhận diện kênh · đọc rõ ở 168px.

---

## 2. TITLE A/B — xoay TUẦN TỰ, mỗi bản ≥7 ngày

> **KHÔNG có A/B title chính thức trên YouTube.** Đổi bằng `videos.update`, mỗi bản ≥7 ngày, tự ghi sổ. Và **chỉ bắt đầu xoay title SAU KHI test thumbnail xong** (§0 bước 4).

### 02 蚊が寄りつかない庭 — `NWPnrezfBDc`
| | title | ký | giả thuyết |
|---|---|---|---|
| **A1** đang live | `蚊が寄りつかない庭は数百円で作れる――業界が広めたがらない10の植物の知恵` | 37 | baseline (âm mưu 業界) |
| **A2** | `蚊が寄りつかない庭は「置くだけ」――数百円の10の植物で作れる` | 32 | **khớp thumbnail mới** (`置くだけでいい`+`10の植物`) → title và ảnh cộng hưởng |
| **A3** | `虫よけスプレーを買う前に――蚊が寄りつかない庭は、数百円の植物10種でできる` | 39 | đổi kiểu hook: chặn hành vi sắp làm (買う前に) |

### 07 すだれ・日除け — `OZj3enOedQk`
| | title | ký | giả thuyết |
|---|---|---|---|
| **A1** đang live | `すだれ・打ち水・室外機の日除け――昔の涼み方で、エアコンの電気代は下がる` | 36 | baseline (liệt kê 3 vật) |
| **A2** ⭐ | `すだれで熱の7割を止める――数百円で、エアコンの電気代が下がる昔の涼み方` | 36 | **khớp thumbnail mới** (`熱の7割`); `すだれ` (đo 42, keyword dẫn) vẫn ở vị trí 1 |
| **A3** | `エアコンが効かない本当の理由は窓――すだれと日除けで、熱の7割を数百円で止める` | 40 | đổi hook: chẩn đoán nguyên nhân |

### 05 スズメバチ — `lQ7P_jN9mqM`
| | title | ký | giả thuyết |
|---|---|---|---|
| **A1** đang live | `スズメバチに巣を作らせない――数百円でできる昔の知恵３つ` | 28 | baseline (đã sửa 2026-07-26 theo đo Trends) |
| **A2** ⭐ | `スズメバチの巣は夏に千匹になる――春の数百円で、そもそも作らせない昔の知恵` | 38 | **khớp thumbnail mới** (`千匹`+`春なら数百円`). `スズメバチ`(81) @1 · `巣`(49) @8 — giữ cả 2 nhánh keyword đã đo |
| **A3** | `スズメバチはなぜ毎年同じ場所に巣を作るのか――春先の数百円でできる備え` | 36 | đổi hook: bí ẩn. **Chính góc benchmark 昔の人の知恵 đã dùng** (5,9K view/5 ngày) và có trong video (第2章) |

### 14 蚊の発酵トラップ — `Edfjmu-gRjg`
| | title | ký | giả thuyết |
|---|---|---|---|
| **A1** đang live | `なぜ蚊はあなたばかり刺すのか――答えは息にありました。300円の発酵トラップと、江戸の水がめの知恵` | 50 | baseline (dài, curiosity cá nhân) |
| **A2** ⭐ | `蚊は50メートル先からあなたの息を追ってくる――300円のトラップで先回りする` | 38 | **khớp thumbnail mới** (`50m`+`300円の仕掛け`). Đây là **ứng viên #2 đã vetted trong script 14**, chưa từng dùng |
| **A3** | `【蚊トラップ自作】材料は砂糖とイーストと洗剤だけ――5分で作れる300円の仕掛け` | 40 | đổi hook: DIY/how-to + 【】. Ứng viên #3 trong script 14 |

**Compliance đã quét cả 12 title:** không từ nhóm cấm (殺/血/死/自殺). ⚠️ Cố ý **không** dùng `殺虫剤` ở A3 của 02 (chứa 殺) → thay bằng `虫よけスプレー`. Mọi tình tiết nêu ra đều có trong video tương ứng.

---

## 3. SỔ ĐỔI TITLE / THUMBNAIL — ghi mỗi lần đụng kênh

| ngày | video | đổi gì | ghi chú |
|---|---|---|---|
| 2026-08-05 | 08 `3YSNgh0s-N8` | thumbnail → bản mới + dấu kênh | `thumbnails.set`, có backup rollback |
| 2026-08-05 | 01 `fHv_oPjO1t0` · 03 `4q25pvkcq4Y` · 04 `7V_mTCRb8tw` · 06 `yZ3RhYJu-dU` | thumbnail → **ảnh mới** + dấu kênh | 04 sửa xong vi phạm nhãn hiệu (bình xịt in tên) |
| 2026-08-05 | 02 · 05 · 07 · 14 | thumbnail → **giữ ảnh cũ, chỉ thêm dấu kênh** | bản B1 cũ đã qua gate, không gen lại |
| 2026-08-05 | 01 `fHv_oPjO1t0` | thumbnail → **v4 K3 macro hero** (bột ホウ酸 rơi vào dầm bị mối + 3–7 con mối macro), **bỏ ❌/✅** | `06_VIDEO/_thumb_v4/01_v4_brand.jpg`. Lý do đo được: bản trước chủ thể (bột) chỉ **3,62%** khung còn ✗+○ ăn **4,2%** → 120px không thấy chủ thể. ❌/✅ cũng đã 4/9 video = quá trần. Dấu 「秘」 phải `--pos tl` (tay chiếm góc trên–phải). Dòng chính `500円` **25,3%** khung — **rớt** trần ≥1/3, đọc rõ ở 120px. Rollback: `plan_01_thumb_backup.json` |
| 2026-08-05 | 04 `7V_mTCRb8tw` | thumbnail → **v4b** (sương ハッカ油 + gián trên bàn bếp sáng), **bỏ ❌/✅ + bỏ chia đôi khung** | `06_VIDEO/_thumb_v4b/04_v4_brand.jpg`. Lý do đo được ở bản cũ: con gián chỉ **0,92%** khung, TỐI trên gạch tối → ở 120px còn ~8×11px; ✗+○ ăn 4,86% = gấp 5 lần. Dòng chính `薬なし` **30,9%** (sát nhất từ trước tới nay, trần ≥1/3 thiếu 26px). Dấu 「秘」 về đúng vị trí khoá `tr`. Rollback: `plan_04_thumb_backup.json` · ⚠️ **user chốt dùng bản gen có 4 con gián NẰM NGỬA dù tao đã cảnh báo mismatch** (video dạy 寄せ付けない, không diệt) — nếu sau này CTR/policy có vấn đề thì đây là biến cần đảo trước, prompt A2 đã soạn sẵn để gen lại |
| 2026-08-05 | 05 · 07 · 02 | **ảnh v3 mới ĐÃ LÀM SẠCH nhưng CHƯA SET** | `06_VIDEO/_thumb_v3/0*_v3_brand.jpg` + 3 title mới — chờ user chốt (`02_THUMBNAIL_PROMPTS.md` §ĐỢT v3) |
| ⏳ | 02 · 05 · 07 · 14 | **nạp T2 vào Studio Test & compare** | **việc của người**, API không làm được (§0) |
| ⏳ | 4 video trên | xoay title A2 → A3 | **chỉ sau khi** test thumbnail xong |

## 4. VIỆC CÒN MỞ (không phải thumbnail)

> ⛔ **Lượt 2026-08-12 user chốt KHÔNG đụng kênh thật** → cả 2 việc dưới **vẫn treo**, đã cập nhật số mới.

- ✅ **2 video TRÙNG — ĐÃ XONG.** Verify API 2026-08-12: `Edfjmu-gRjg` (07-30) **đã ở `private`**, `_4RttFsrYtw` giữ public (101 imp / CTR 2,0% / 8 view). Không phải làm gì nữa. ⚠️ Nhưng bảng title §2 mục 14 vẫn ghi `Edfjmu-gRjg` là "A1 đang live" → **dòng đó đã CHẾT**, đừng dùng.
- 🔴🔴 **categoryId — ĐÃ VERIFY BẰNG API 2026-08-12, VÀ TỆ HƠN CẢ HAI FILE GHI: `22` ở 10/14 video.**

  | ngày | cat | video |
  |---|---|---|
  | 07-15 · 07-19 · 07-22 | **27** ✅ | シロアリ · 蚊の庭 · 雑草 |
  | 07-31 | **27** ✅ | 蚊トラップ (`_4RttFsrYtw`) |
  | **07-23 · 07-26 · 07-27 · 07-28 · 07-30 · 08-03 · 08-05 · 08-07 · 08-10 · 08-12** | **22** 🔴 | ゴキブリ · スズメバチ · 排水溝 · **すだれ** · なぜ蚊 · 梅干し · 扇風機 · 漬物 · 10円玉 · 生ゴミ |

  🔴 **Câu trong `CLAUDE.md` §📐 điểm 1 — *"3 video đầu đã sửa 22→27 ngày 2026-07-22, áp TỰ ĐỘNG từ video 04"* — SAI.** Đúng 3 video đầu được sửa tay, rồi **từ 07-23 mọi video quay lại 22**; cơ chế "tự động" chưa bao giờ chạy. Đây là lỗi im lặng đã sống **20 ngày**.
  ⚠️ **ĐỌC ĐÚNG MỨC — bản đầu của dòng này NÓI QUÁ, đã sửa 2026-08-12.** Câu cũ: *"category sai = YouTube xếp vào cụm nội dung sai = càng khó dựng đồ thị co-view"* → **đó là cơ chế SUY RA, không đo được.**
  - ✅ **Đo được:** benchmark `昔の人の知恵` để **27 ở 22/22**, co-dai **22 ở 10/14**. Khác biệt là thật, và là 1 trong 2 biến cấu trúc còn lại (`CHANNEL_DIAGNOSIS_2026-08-12.md` §6b).
  - ❌ **KHÔNG đo được:** categoryId có ảnh hưởng tới phân phối hay không. Category là **tín hiệu YẾU** so với title/mô tả/nội dung/co-view. Không có bằng chứng nào trong workspace cho thấy 22 vs 27 làm đổi view.
  ⇒ Vì vậy nó **KHÔNG** ngang hàng với biến khuôn title (§📐 7c — cái đó có bằng chứng từ 2 nguồn độc lập). Đáng sửa vì **rẻ và đúng**, không phải vì nó là nghi phạm.
  ✅ **GỐC RỄ ĐÃ TÌM RA, đo được 2026-08-12 — KHÔNG phải lỗi tool:**
  `upload_api.py::API_CFG["co-dai"]` ghi **đúng** `categoryId: "27"`, và **đúng video duy nhất đăng qua API** (07-31, `_4RttFsrYtw`) **là 27**. Mười video sai đều là **ĐĂNG TAY trong Studio**, và Studio lấy từ:
  > **`Cài đặt → Chế độ mặc định cho video tải lên → tab Cài đặt nâng cao → Danh mục = 「Mọi người và blog」`** (= People & Blogs = **22**).

  🔴 **CÙNG MỘT HỌ LỖI với memory `project_studio_default_upload_tags`** (tag rác lặp cũng từ đúng ô デフォルト設定 này, chỉ khác field) — và bài học ở đó áp y nguyên: **dọn video mà không tắt NGUỒN thì mọc lại sau 1 video.**
  **USER CHỐT 2026-08-12: chỉ chặn NGUỒN, KHÔNG sửa 10 video cũ.**
  1. ⏳ **Đổi ô `Danh mục` trong mặc định upload → `Giáo dục`** — **việc của USER** (đổi cài đặt tài khoản, Claude không tự bấm). Đường bấm: `Studio → Cài đặt (góc dưới-trái) → Chế độ mặc định cho video tải lên → tab Cài đặt nâng cao → Danh mục → Giáo dục → Lưu`.
  2. ⛔ **`videos.update` cho 10 video cũ — KHÔNG LÀM** (user chốt).
     ⚖️ **Đánh đổi đã biết trước, ghi thẳng:** 10/14 video đang public **vẫn nằm ở cụm nội dung sai (People & Blogs)** trong khi benchmark để 27 ở 22/22. Chúng tiếp tục nạp tín hiệu cụm sai cho YouTube, và **10/14 là đa số kho video** — tức phần lớn dấu vết của kênh vẫn lệch. Đây là quyết định đã chọn, **đừng "phát hiện lại" rồi đề xuất sửa** trừ khi có bằng chứng mới.
     📌 Nếu bao giờ đảo ý: lệnh là `videos.update part=snippet` (phải gửi lại **đủ** `title`/`description`/`tags`/`categoryId`/`defaultLanguage`, thiếu field nào là **XOÁ** field đó) + backup JSON trước khi ghi.

  ⓘ Cùng ô đó, 2 field khác đã ĐÚNG, không cần đụng: `Ngôn ngữ video` = Tiếng Nhật · `Ngôn ngữ tiêu đề và nội dung mô tả` = Tiếng Nhật.

---

## 5. 📊 SỔ CTR + IMPRESSIONS — ĐỌC TAY TRONG STUDIO (mở 2026-08-12)

> 🔴 **Vì sao phải đọc tay:** `impressions` và CTR **bị Google rút khỏi Analytics API từ 2026-07-30**
> (memory `project_api_impressions_bi_rut`). Không có sổ này thì kênh **mù hoàn toàn** về cửa vào.
> Cách đọc + URL Studio: `CHANNEL_DIAGNOSIS_2026-08-12.md` §5.
>
> ⚠️⚠️ **ĐÂY ĐÚNG LOẠI VIỆC SẼ TRÔI** — y như bài học cold open 60s trôi ở 6/6 script. Trôi thì không
> phải "đổi cách đo", mà là **bỏ đo**, và lúc đó mọi kết luận về thumbnail/title đều thành phỏng đoán.
> **Nhịp: 1 lần/tuần.** Bỏ 2 tuần liên tiếp → coi như sổ chết, phải nói thẳng ra chứ đừng đoán tiếp.

### 5a. BASELINE — lifetime 4/7 → 11/8/2026, đo 2026-08-12

**Tổng kênh: 1.397 imp · CTR 4,7% · 110 view · AVD 5:05 = 21,6%**

| # | video | dài | imp | CTR | view | AVD | AVD% |
|---|---|---|---|---|---|---|---|
| **07** | すだれ | 24:38 | **512** | 5,1% | 41 | 2:38 | **10,7%** |
| 03 | 雑草 | 12:14 | 142 | **0%** 🔴 | 4 | 3:18 | 27,0% |
| 05 | スズメバチ | 27:11 | 131 | 3,8% | 7 | 12:16 | 45,1% |
| 14 | 蚊トラップ | 20:00 | 101 | **2,0%** | 8 | 4:26 | 22,2% |
| 02 | 蚊の庭 | 25:18 | 98 | **14,3%** ⭐ | 19 | 5:22 | 21,2% |
| 06 | 排水溝ぬめり | 18:28 | 97 | 1,0% | 3 | 6:16 | 34,0% |
| 04 | ゴキブリ | 19:14 | 78 | 2,6% | 3 | 6:30 | 33,8% |
| 08 | 梅干し | 22:49 | 70 | 2,9% | 3 | 0:28 | 2,1% |
| 15 | 扇風機 | 25:49 | 67 | **9,0%** | 6 | 2:41 | 10,4% |
| 01 | シロアリ | 22:47 | 44 | **11,4%** | 12 | 7:05 | 31,2% |
| 16 | 漬物 | 28:34 | 23 | 4,4% | 1 | 28:32 | *nhiễu* |
| 17 | 排水溝10円玉 | 24:04 | 20 | **0%** 🔴 | 1 | 9:19 | *nhiễu* |
| 14b | なぜ蚊 (**TRÙNG**) | 20:00 | 9 | 0% | 1 | 13:08 | *nhiễu* |
| 18 | 生ゴミ | 20:52 | **4** | 25,0% | 1 | 20:50 | *nhiễu* |

⚠️ 4 dòng cuối có **1 view** ⇒ AVD là **NHIỄU**, gần như chắc là chính user xem. Đừng trích.

### 5b. Đọc ra gì — 3 dòng, chi tiết ở `CHANNEL_DIAGNOSIS_2026-08-12.md`

1. ⛔ **CTR ĐẠT ⇒ ngừng đổ công vào khuôn thumbnail.** Bảng T1/T2 ở §1 + bộ title A/B ở §2 **hạ ưu tiên**, không phải nghi phạm. Chỉ còn **2 việc lẻ**: thay thumbnail **03** và **17** (0% CTR — không ăn nổi một click).
2. ⭐ Biến mới = **INTENT của query search** (`CLAUDE.md` §📐 điểm 7b). AVD search **3:09** vs browse **9:49**.
3. 🔴 `Video đề xuất` = **0 impressions suốt đời kênh**; `「Kênh mà khán giả xem」` = **không đủ dữ liệu**.

### 5c. Bảng ghi hằng tuần (điền tiếp xuống dưới)

| ngày đọc | imp kênh | CTR kênh | AVD search | `Video đề xuất` có dòng? | `「Kênh khán giả xem」` | ghi chú |
|---|---|---|---|---|---|---|
| 2026-08-12 | 1.397 | 4,7% | **3:09** | **KHÔNG** | không đủ dữ liệu | baseline (§5a) |
| ⏳ 2026-08-19 | | | | | | |
| ⏳ **2026-08-22** | | | | | | **mốc quyết định** — bảng ngưỡng ở `CHANNEL_DIAGNOSIS_2026-08-12.md` §6 |
| ❌ 08-19 → 09-05 | | | | | | **SỔ CHẾT 3,5 TUẦN** — không ai đọc. Từ 09-06 chuyển sang §6 (API, tool) để không phụ thuộc đọc tay |
| 2026-09-06 | *API không cấp* | *API không cấp* | — | 22 video: RELATED_VIDEO tổng **1 view** (07) | — | kéo bằng `pull_retention.py`, xem §6 |

## 6. 📈 SỔ RETENTION THEO VIDEO — Analytics API, tool `tools/pull_retention.py` (mở 2026-09-06)

> Vì sao có mục này: **mọi số retention thật của kênh dừng ở video 07 (2026-08-12)**; video 18→30 không có
> một số khán giả nào, §5c chết 3,5 tuần (hàng ⏳ 08-19 / 08-22 trống). 7 video liên tiếp gate PASS mà v1 vẫn
> bị trả — tinh chỉnh gate suốt thời gian đó là **đoán**. Mục này là vòng đo để công thức `04_FORMULA.md` có số.
> Kéo: `python tools\pull_retention.py` → `06_VIDEO/_diagnose/RETENTION_<ngày>.md` + `curves/<NN>_<id>.json` (100 điểm).

### 6a. Hai luật đọc — rút ra ngay ở lần kéo đầu, đừng bỏ

1. 🔴 **Ngưỡng là ORGANIC ≥10 view, KHÔNG phải view ≥10.** Video 24 カメムシ có **52 view** — nhiều nhất trong
   13 video spec mới — nhưng traffic là **EXT_URL 21 · search 5 · NO_LINK 1**: link mở tay/test. AVD **4,7%**
   của nó là số BẨN. Đọc nó thành "spec 45s thất bại" là kết luận sai từ dữ liệu rác. Tool đã lọc.
2. 🔴 **Ghép `subs.srt` theo TITLE, không theo thời lượng.** Ghép theo thời lượng nhầm 2/5: 01 (22′47) ăn srt
   của 08 (22′49), 24 (18′33) ăn srt của 28 (18′48) → "câu giết" trỏ vào kịch bản khác. Cùng họ với bẫy
   resume "file tồn tại ≠ file đúng" (`render-background.md` §2.5).

### 6b. Bảng — lần kéo #1, 2026-09-06 (@60s so chuẩn **70%** của `youtube-suggested-growth.md` §4)

| # | video | đăng | view (organic/ext) | AVD | AVD ngày1 | @15s | @30s | @45s | @60s | 3′ | 10′ | 20′ | search/browse/related | điểm curve |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | シロアリ駆除に10万円払う前 | 2026-07-15 | 13 (10/3) | 31.1% | 28.6% | 95 | 48 | 42 | **45** | 42 | 33 | 17 | 2/0/0 | 100 |
| 02 | 蚊が寄りつかない庭は数百円― | 2026-07-19 | 22 (22/0) | 19.5% | 22.5% | 86 | 53 | 43 | **38** | 33 | 16 | 38 | 17/0/0 | 100 |
| 07 | すだれ数百円――熱の7割は窓 | 2026-07-28 | 62 (51/8) | 14.8% | 1.9% | 87 | 56 | 40 | **34** | 29 | 21 | 18 | 42/0/1 | 100 |
| 17 | 排水溝の掃除はもういらない？ | 2026-08-10 | 18 (10/0) | 11.9% | 0.0% | — | — | — | **—** | — | — | — | 8/0/0 | 0 |

**Bỏ qua (organic <10 — curve là nhiễu):** 05 スズメバチ (10 view / organic 9) · 14 蚊トラップ (12 / 6, ext 6) ·
15 扇風機 (10 / 9) · **24 カメムシ (52 / 5, ext 22)** · 15 video còn lại <10 view (gồm toàn bộ 18→23, 25→30).
⚠️ 17 排水溝 đủ organic (10) nhưng API **không trả curve** (0 điểm) — YouTube giữ curve khi mẫu quá nhỏ.

### 6c. Đọc ra gì

- **Không video spec-45s nào (18→30) có curve đọc được.** Mốc @45s ≥85% / sàn ≥55% của `CLAUDE.md` §③ vẫn
  **chưa có một số nào để đối chiếu**, sau 13 video. ⇒ **Lần kéo #1 của điều kiện dừng:** 3 tuần liên tiếp
  không video 18→30 nào đạt organic ≥10 → ghi "kênh mù", DỪNG tinh chỉnh gate WARN (O18/O19/⑥), thước đo
  chuyển hẳn sang `04_FORMULA.md` §7 (v1 có được nhận không cần v2).
- **@60s so chuẩn 70%:** 01 = 44,9 · 02 = 38,3 · 07 = 34,4 — cả 3 video cũ đều **dưới chuẩn 25–36 điểm**.
  Đây là lần đầu mốc 70% được ghi cho co-dai (rule chốt 08-21, chưa từng áp).
- **Hồi quy tool (plan D5):** 01 khớp docstring `check_coldopen.py` tuyệt đối (AVD 31,1% · @45 41,7) · 07 lệch
  ≤3đ · 02 lệch 8đ ở @30 (mẫu 19→22 view + nội suy giữa 2 điểm 1% thay vì đọc 1 điểm). Tool đúng.
- **AVD ngày 1 vs lifetime:** 01 28,6→31,1 · 02 22,5→19,5 · 07 **1,9→14,8** (ngày 1 của 07 là 5 view rác).
  Bài học chouhen "đọc ngày 1" chỉ đúng khi ngày 1 có ≥10 organic — ở kênh này thì chưa.

### 6d. Bảng ghi hằng tuần (điền tiếp — cùng ngày cố định, THỨ HAI)

| ngày kéo | video có curve (organic≥10) | video 18→30 đạt ngưỡng | ghi chú |
|---|---|---|---|
| 2026-09-06 | 4 (01·02·07·17) | **0** | lần #1 điều kiện dừng · 24 bị loại vì EXT_URL 22/52 |
| ⏳ 2026-09-14 | | | |
| ⏳ 2026-09-21 | | | |
| ⏳ 2026-09-28 | | | **lần #3 — nếu vẫn 0 → ghi "kênh mù", dừng tinh chỉnh gate** |

