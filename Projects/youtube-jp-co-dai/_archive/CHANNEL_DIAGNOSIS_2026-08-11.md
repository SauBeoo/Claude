# KHÁM KÊNH 古代の秘訣 — 2026-08-11 · RETENTION + mục tiêu AVD 60%

> ➡️ **ĐỌC KÈM `CHANNEL_DIAGNOSIS_2026-08-12.md`** (đo TAY trong Studio, có `impressions` + CTR mà API
> không còn cấp). Bản 08-12 **BỔ SUNG, không đè file này** — hai kết luận lõi ở đây (**cửa tử giây
> 15→45** và **KHÔNG cắt độ dài**) vẫn đúng nguyên vẹn. Nhưng nó thêm 3 thứ file này **không thể thấy**:
> ① **CTR đã ĐẠT (4,7% tổng, 14,3% ở bản tốt nhất)** ⇒ đừng đổ công vào thumbnail
> ② **80% impressions đến từ search, và search là traffic AVD 3:09** — bẩn gấp 3 mọi nguồn khác
> ③ **`「Kênh mà khán giả xem」 = không đủ dữ liệu`** ⇒ YouTube chưa có cụm khán giả nào để đặt kênh vào rail.
> ⚠️ Và: spec cửa-45-giây của file này hiện có **0 video đo được** (video 18 mới 4 impressions).

> Phép đo: YouTube Analytics API (token readonly co-dai) + Data API, 13 video đã đăng 07-15 → 08-10.
> Benchmark 昔の人の知恵 (`UCYJ2D_D1q7_sYGorIB2_6iA`) đo cùng ngày, 21 video long-form.
> **Đè mốc 75 giây của `CHANNEL_DIAGNOSIS_2026-07-30.md`.** File đó vẫn đúng về BROWSE=0, về
> thumbnail nền tối, và về chuyện ngách không chết — cái sai duy nhất là **mốc thời gian**.
> ⚠️ `impressions`/CTR vẫn bị Google rút khỏi API (từ 2026-07-30) → muốn số đó phải đọc tay Studio.

---

## 0. SỐ HIỆN TRẠNG

- **13 video / 27 ngày → 95 view · 1 sub · 489 phút xem.**
- **AVD kênh 5′09″ = 21,94%** trên video dài 22–28′.
- **Traffic: `YT_SEARCH` 58 · `YT_CHANNEL` 14 · `SUBSCRIBER` 10 · `EXT_URL` 5 · khác 8.**
  🔴 **`BROWSE_FEATURES` = 0 · `SUGGESTED` = 0 — tuyệt đối, kể cả cửa sổ 7 ngày gần nhất** (7d: SEARCH 19 · CHANNEL 3 · khác 2). Search là cửa organic duy nhất, y như 07-30.

**AVD từng video** (`averageViewPercentage`, xếp theo view):

| videoId | video | dài | view | AVD | phút xem |
|---|---|---|---|---|---|
| `OZj3enOedQk` | 07 すだれ | 24′38 | 35 | **12,12%** | 2′59 |
| `NWPnrezfBDc` | 02 蚊の庭 | 25′18 | 18 | 22,38% | 5′39 |
| `fHv_oPjO1t0` | 01 シロアリ | 22′47 | 12 | **31,15%** | 7′05 |
| `z72HHaxlHJw` | 15 扇風機 | 25′49 | 6 | 10,42% | 2′41 |
| `_4RttFsrYtw` | 14 蚊トラップ | 20′00 | 6 | 28,88% | 5′46 |
| `lQ7P_jN9mqM` | 05 スズメバチ | 27′11 | 4 | 48,65% | 13′13 |
| `4q25pvkcq4Y` | 03 雑草 | 12′14 | 4 | 27,00% | 3′18 |
| `yZ3RhYJu-dU` | 06 ぬめり | 18′28 | 3 | 34,01% | 6′16 |
| `7V_mTCRb8tw` | 04 ゴキブリ | 19′14 | 3 | 33,81% | 6′30 |
| `3YSNgh0s-N8` | 08 保存食 | 22′49 | 2 | 2,04% | 0′27 |
| `822klc0yrv8` | 16 漬物 | 28′34 | 1 | 99,94% | 28′32 |
| `d-ExmQK1Fok` | 17 排水溝 | 24′04 | 0 | — | — |

⚠️ **Video ≤6 view là NHIỄU, không phải phép đo** (16 = 99,94% từ **1 view**; 05 = 48,65% từ 4 view;
08 = 2,04% từ 2 view). Chỉ **01 · 02 · 07** có đủ mẫu để API trả **đường cong retention**; 15/16/17
trả **0 điểm curve** — tức **hai video đầu dùng lớp vox mới (16, 17) CHƯA đo được gì**, đừng kết
luận theo hướng nào.

---

## 1. CỬA TỬ LÀ GIÂY 15 → 45, KHÔNG PHẢI GIÂY 75

`audienceWatchRatio` + `relativeRetentionPerformance` theo `elapsedVideoTimeRatio`:

| video | @15s | @30s | @45s | @75s | AVD | relPerf 60s đầu |
|---|---|---|---|---|---|---|
| 01 シロアリ | **100%** | **50,0%** | 41,7% | — | 31,15% | 0,38–0,46 |
| 02 蚊の庭 | 88,9% | 61,1% | **50,0%** | 33,3% | 22,38% | **0,17–0,25** |
| 07 すだれ | 88,2% | **52,9%** | 41,2% | 35,3% | 12,12% | 0,25–0,38 |

🔴 **Gần như KHÔNG ai bỏ đi trong 15 giây đầu (88–100%)** ⇒ toàn bộ cú giết gói trong ~30 giây sau
đó, mất nhiều điểm hơn cả 20+ phút còn lại. Video 01 mất **50 điểm trong 14 giây** (13,7s → 27,3s).

⭐ **Hệ quả tích cực: bản vá 2026-07-21 ("stake + con số tiền trong ~84 ký đầu") ĐÃ CHẠY** — chính
nó giữ được 88–100% ở giây 15. Đừng đảo nó; xây tiếp lên nó.

⚠️ `relPerf` 0,17–0,46 = phân vị đáy 17–46% của YouTube ở 60 giây đầu. **Đây là cơ chế giữ vòi
đóng**, không phải tuổi kênh, không phải index (07-30 đã loại 2 giả thuyết đó).

### 1b. Đọc đúng giây 22–45 của video 07 (AVD 12,12% — tệ nhất) — lỗi là GÌ

`07_UPLOADED/07_natsu-denkidai-suzumi/_upload/subs.srt`, giây THẬT:

| giây | dòng | vai thật |
|---|---|---|
| 19 | 熱のうち、およそ7割は、窓や開口部から入ってきます | ✅ fact mạnh nhất của cold open |
| **21** | 住宅の断熱を調べた業界の試算です | ❌ **gán nguồn** — 0 thông tin mới |
| **25** | 壁でも、屋根でもなく、窓です | ❌ nhắc lại lần 2 |
| **29** | 内側から布をかぶせても、熱は、もう部屋の中に入っています | ❌ nhắc lại lần 3 |
| **35** | そこで今日、いちばん先にお話しするのは、この二つです | ❌ **MỤC LỤC** |
| 44 | どちらも数百円から始められて、今日の夕方には終わります | ❌ vẫn là hứa, chưa có hành động |
| 102 | 古代の秘訣へようこそ | ❌ câu chào ăn ~7s |
| 111 | さて、一つ目の逆効果から見ていきましょう | ← mới VÀO BÀI |

**Bốn câu liên tiếp không trả gì ở giây 21–45.** Đúng đoạn phẳng đó là chỗ đường cong đi 88% → 41%.

### 1c. Gate cũ CANH SAI CỬA — và trả số RÁC

`tools/check_coldopen.py` bản 2026-07-30 đo **một** thứ: "chương/mẹo đầu tiên ≤75 giây".

1. 🔴 **Nó chấm video 07 là script TỐT NHẤT kênh (~100s — ghi thẳng trong bản 07-30 §3b)** — mà 07
   là video retention **TỆ NHẤT** (12,12%). **Gate xếp hạng NGƯỢC với thực tế đo được.**
2. 🔴 **Bug regex:** `ITEM` không biết câu chuyển hiện hành 「さて、ここからが今日の核心です。」 → 3/6
   script tồn kho báo **~1134–1189 giây**, số thật **135–194 giây**. Gate trả số vô nghĩa thì sẽ bị
   bỏ qua — đúng bệnh *"luật kiểm bằng mắt thì sẽ trôi"*, chỉ khác là lần này luật có gate mà gate hỏng.

### 1d. GỐC RỄ NẰM TRONG SPEC, không phải ở tay viết

`.claude/skills/script-co-dai/SKILL.md` MỤC 10 (bản cũ) **thiết kế sẵn** đoạn dạo đầu 2 phút rưỡi:
`Hook (0:00–1:30, ~450 ký tự)` → `Chào kênh + CTA sớm (1:30–2:30)` ⇒ thân bài bắt đầu ở **2:30**.
MỤC 14 điểm 1 chốt lại: `Hook 90 giây đầu…`. Đó chính là con số đo được ở 5/5 script tồn kho
(135–194s). **Không phải viết sai — viết ĐÚNG một spec SAI.**

---

## 2. 🎯 MỤC TIÊU AVD 60% — SỐ HỌC CỦA NÓ (user chốt 2026-08-11)

`AVD% ≈ chiều cao TRUNG BÌNH của đường cong retention`. Nên câu hỏi đầu tiên phải là: *nếu CHỈ cắt
video ngắn thì AVD được bao nhiêu?* Tích phân hình thang 3 đường cong thật:

| cắt tại | 01 シロアリ | 02 蚊の庭 | 07 すだれ |
|---|---|---|---|
| 5′ | **45,0%** | 35,7% | 36,7% |
| 10′ | 39,9% | 25,9% | 30,2% |
| 12′ | 38,9% | 24,8% | 29,3% |
| 15′ | 37,7% | 23,4% | 26,9% |
| 18′ | 37,0% | 23,8% | 23,8% |
| nguyên bản | 32,9% | 25,1% | 19,4% |

🔴 **Cắt xuống 5 PHÚT vẫn chỉ 45%.** Cắt về 12′ đáng **+6 điểm**, không phải +28. Vì đường cong đã
tụt còn 50% ở giây 30–45 nên **mọi cửa sổ bắt đầu từ 0 đều bị cái vách đó kéo xuống.**

⇒ ⭐⭐ **60% AVD được mua TRỌN trong 45 GIÂY ĐẦU, KHÔNG mua bằng độ dài.**

**Hai con số phải đạt:**
1. **@45s ≥ 85%** (nay 41,2–50,0%) — đắt nhất, ăn ~+25 điểm AVD.
2. **sàn thân bài ≥ 55%** (nay 41,7% @3′ → 33,3% @10′ → 16,7% @20′ — thân bài rò rỉ liên tục).

⚠️ **60% CHƯA CÓ TIỀN LỆ trong workspace.** Cao nhất từng đo: chouhen video 12 **51,6% lifetime /
55,7% ngày 1** — và đó là **DRAMA** (lực kéo tự truyện). Kênh tài liệu không có lực đó.
**Mốc chặng: 40% → 50% → 60%.** 🛑 **Phanh: 3 video liên tiếp ≤30% ⇒ mốc 60% sai với ngách này,
mổ lại chứ đừng vá tiếp.**

---

## 3. ĐỘ DÀI **KHÔNG** PHẢI BIẾN — ĐỪNG CẮT NGẮN

Benchmark 昔の人の知恵, 21 video long-form đo 2026-08-11: **median 21,9′**, dải 15,2–31,3′.

| view/ngày | view | dài | ngày | title |
|---|---|---|---|---|
| **37.980** | 341.820 | **23,0′** | 08-02 | キッチンの排水口に絶対に流してはいけない5つのもの |
| 13.481 | 485.345 | 18,0′ | 07-06 | もう蚊から逃げるのはやめましょう |
| 7.041 | 28.167 | 29,7′ | 08-07 | なぜ私たちは、家を冷やすために塩を使わなくなったのか |
| 2.322 | 58.066 | 15,2′ | 07-17 | 【スズメバチ対策】なぜ毎年同じ場所に巣を作るのか |

Ta 22–28′ = **cùng dải với benchmark**, và hit của họ là **23,0′**. ⇒ **KHÔNG áp cú cắt kiểu nenkin**
(25–30′ → 13–17′). Cắt ngắn ở ngách này là sửa sai chỗ, và sẽ đốt luôn moat 「なぜ効くのか」.

📌 Hai kết luận §2 và §3 **CÙNG CHIỀU**, không mâu thuẫn: §2 nói cắt ngắn *không mua được* 60%;
§3 nói cắt ngắn *cũng không cần cho view*. Cả hai đều dẫn về: **giữ 25′, sửa 45 giây đầu.**

---

## 4. GATE MỚI + BẢNG HIỆU CHUẨN

`tools/check_coldopen.py` viết lại 2026-08-11 (giữ tên + CLI cũ). Bộ luật:

| | luật | ngưỡng |
|---|---|---|
| **O1** 🔴 | mẹo/hành động đầu tiên vào bài | ≤30s (168 ký) |
| **O2** 🔴 | giây 0–45: câu MỤC LỤC / tuyên bố | = 0 |
| **O3** 🔴 | giây 0–45: câu GÁN NGUỒN / nhắc lại | = 0 |
| **O4** 🔴 | câu chào 「古代の秘訣」 | phải SAU mẹo 1 |
| **O5** 🔴 | 60s đầu: câu miễn trừ / dặn dò an toàn | = 0 |
| **O6** 🔴 | giây 0–45: câu **KHÔNG TRẢ TIỀN** | ≤1 |
| **O7** 🟡 | stake + con số trong ~84 ký đầu (15s) | có |
| **O9** 🔴 | gap giữa 2 payoff xuyên thân bài | ≤2′30″ |
| **O10** 🟡 | tuyên bố "mẹo mạnh nhất để CUỐI" trong 60s đầu | có |

**"Trả tiền" = câu có ≥1 trong NĂM đồng tiền:** ① con số/đơn vị **mới** ② động tác ③ nghịch lý
④ **nhập giác quan** ⑤ **câu hỏi kéo người xem vào**.

### 4a. 🔴 BẢNG HIỆU CHUẨN — và lỗi mà nó BẮT ĐƯỢC

Gate cũ chết vì **chưa ai đối chiếu nó với retention thật lần nào**. Nên bản mới có chế độ
`--calib`: đọc `_upload/subs.srt` (timeline giọng THẬT) của video đã lên sóng rồi so với AVD đo được.

| | 02 蚊の庭 (AVD **22,38%**) | 07 すだれ (AVD **12,12%**) | đúng chiều? |
|---|---|---|---|
| O1 vào bài | **0s** ✅ | 111s 🔴 | ✅ |
| O6 câu không trả tiền | **3** | **6** | ✅ |
| tổng rule FAIL | **2** | **5** | ✅ |

⭐ **Bản ĐẦU của O6 xếp NGƯỢC** — nó chỉ nhận 3 đồng tiền (số mới · động tác · nghịch lý) nên chấm
video 02 là **8** câu không-trả-tiền, tệ hơn video 07 (**6**), dù AVD 02 gần gấp đôi. Nguyên nhân:
cold open của 02 là **cảnh nhập giác quan thuần** (「夏の夕暮れを思い浮かべて」「耳元で響く羽音もない」),
**không một con số nào**, mà giữ 88,9% @15s. Cộng thêm một lỗi bỏ sót: `10種類` không được đếm vì
`NUM` thiếu đơn vị 種類.
⇒ Đã thêm đồng tiền ④ **nhập giác quan** và ⑤ **câu hỏi** (đúng mũi tiêm ③ của
`humanize-script-voice.md`), thêm 種類/通り/か月… vào `NUM`. Sau khi sửa: **02 = 3 · 07 = 6**, đúng chiều.
**Bài học: gate nào chưa hiệu chuẩn thì chưa được tin — kể cả gate mới viết bằng bằng chứng.**

⚠️ **HIỆU CHUẨN 2 ĐIỂM, KHÔNG PHẢI 3.** Video **01 シロアリ (31,15% — bản tốt nhất kênh) KHÔNG hiệu
chuẩn được**: `07_UPLOADED/01_hosan-shiroari/_upload/` chỉ còn `METADATA.txt` + `thumbnail.jpg`,
**mất cả script lẫn `subs.srt`** (đăng trước khi có flow gom script vào `_scripts/`). Đừng ghi là
đã xác nhận 3 điểm.

---

## 4b. 🔴 CLIFF THỨ HAI — bài học từ script CŨ (đo thêm cùng ngày)

Mục §1 chỉ mổ 45 giây đầu. Soi tiếp **cú rớt lớn nhất SAU cold open** của 3 curve, rồi tra đúng câu bằng `subs.srt` thật:

| video | mốc | mất | nội dung tại đó | chẩn đoán |
|---|---|---|---|---|
| **07** | giây **311** (phút 5) | **−14,7đ** | 308s「今日の夕方から、始められます」← vừa trả xong mẹo 1 → 311s「この番組を初めてご覧になる方は」→ 314s「登録のボタンを押して」→ 321s câu hỏi comment | ⭐ **CTA/登録 đặt NGAY SAU payoff.** Người xem vừa nhận hàng, đáng lẽ bị đẩy vào chuyện tiếp, lại bị hỏi một câu ⇒ đóng tab. **Cú rớt nặng nhất của cả bài sau cold open.** |
| **07** | giây **695–709** (phút 11) | **−11,8đ** | 「場を清め、木々の葉を生き返らせ」「もてなしの作法として」「実利と礼儀が、一つになっていた習わしでした」 — 4 câu liền, 0 số, 0 động tác. Câu MỞ「ところが、落とし穴があります」tới ở **709s = sau khi đã mất người** | **Khối lịch sử/văn hoá THUẦN** = cùng cơ chế đã giết cold open, chỉ khác chỗ |
| **02** | giây **1215** (80%) | **−11,1đ** | 「秋には鮮やかな紫色の実をつけ…庭の景色を豊かにしてくれます」 (bài đang nói **chống muỗi**) | **Chi tiết phụ / mô tả trang trí** không phục vụ mục đích bài |
| **02** | giây **183–196** (12%) | −11,1đ | 「むしろ、栄養が豊かすぎない土のほうが…」「香りの成分が濃くなる傾向が」 | chi tiết trồng trọt phụ, không ai hỏi |

**Hai gate mới sinh ra từ đây:**
- **O14** — CTA phải nằm ở chỗ có **LOOP ĐANG MỞ**, không phải ngay sau một payoff (≥1 câu MỞ trong 3 câu trước CTA). `--calib` xác nhận: **07 FAIL O14** (CTA ở 10′03″ ngay sau payoff), đúng cú −14,7đ.
- **O15** — cấm **run ≥4 câu liền không trả tiền** ở BẤT KỲ đâu trong bài. `O9` đo gap theo PHÚT nên không bắt được 4 câu ≈ 18 giây.

🔴 **GIỚI HẠN CỦA O15 — ghi thẳng, đừng đọc quá mạnh.** Hiệu chuẩn cho thấy O15 **KHÔNG discriminating giữa 2 video**: **02 có 27 run @ AVD 22,38%** · **07 có 24 run @ 12,12%** ⇒ nhiều run hơn mà retention tốt hơn. Và 24 run × 11,8đ thì vượt 100% ⇒ **phần lớn run 4 câu KHÔNG gây cú rớt đo được nào.** Bằng chứng của O15 là **CỤC BỘ** (một run trùng đúng cú −11,8đ), không phải bằng chứng so-giữa-video.
⇒ **Một run là NGHI PHẠM, không phải BỊ KẾT ÁN.** Giữ ở mức FAIL vì rẻ để thoả và nó buộc văn phải dày, **nhưng đừng dùng số run để so 2 script**, và đừng kết luận "cắt hết run là AVD lên". Thứ đã chứng minh được vẫn là **cold open (O1/O6)** và **vị trí CTA (O14)**.

📌 **Trần của O15 hiệu chuẩn theo ca thật:** cả 3 cú rớt đều là **đúng 4 câu liền** ⇒ chặn từ 4. Trần 3 câu đã thử và **LOẠI** — nó bắt cả khối reveal cơ chế của script 18 (giây 331/378/1006); 3 câu liền là nhịp bình thường của văn dày.

---

## 5. VIỆC ĐÃ LÀM / CÒN MỞ

✅ Viết lại `tools/check_coldopen.py` (O1–O10 + `--calib` + fix bug regex 「さて、ここからが核心」).
✅ Sửa spec skill `script-co-dai` MỤC 10 (cold open 0:45, chào kênh SAU mẹo 1, gate SÀN 2′30″) + MỤC 14 điểm 1.
✅ Sửa `CLAUDE.md` §9b + thêm §🎯 RETENTION.
✅ Park script 09–13 (`03_SCRIPTS/_PARKED.md`) — user chốt viết mới từ đầu.
⏳ Viết video 18 theo spec mới = **phép thử sạch đầu tiên** (cold open mới + lớp vox mới).

**Còn mở, cố ý không làm trong lượt này:**
- **Thumbnail/title** — user chốt lượt này chỉ retention. Bộ T2 + title A2/A3 của 4 video vẫn chờ nạp Studio bằng tay (`08_ANALYTICS_LOG.md` §1, §3).
- **Suy rộng sang kênh khác** — cửa sổ 15–45s rất có thể áp cho health/shokutaku/nenkin/kaigo/akiya (health đã có `relPerf@60s` 0,10–0,14), và `audience-45plus.md` §6.9 để mở gate `check_45plus.py`. **Mỗi kênh phải hiệu chuẩn trên curve của CHÍNH NÓ** — bài học §4a cho thấy luật bê nguyên sang là xếp ngược.
- **Xu hướng AVD theo ngày đăng đang ĐI XUỐNG** và chưa giải thích được: 01 (31,2%) → 02 (22,4%) → 14 (28,9%) → 07 (12,1%) → 15 (10,4%). Mẫu 1–6 view nên có thể nhiễu thuần; nếu 2 video tới vẫn ≤15% thì mổ lại.
- **Video đã đăng không sửa được retention** — thay nội dung phải xoá + upload lại = trùng lặp (`youtube-compliance.md` §1). 12 video cũ giữ nguyên, vẫn kéo relPerf trung bình kênh xuống một thời gian.

## 6. LỆNH ĐO LẠI

```bash
# AVD + curve retention 1 video
metrics=audienceWatchRatio,relativeRetentionPerformance · dimensions=elapsedVideoTimeRatio · filters=video==<id>
# gate script trước render
python tools\check_coldopen.py <NN>
# hiệu chuẩn lại gate sau khi có video mới đủ view
python tools\check_coldopen.py --calib
```
Channel ID mình: `UCVlmm1sz7cvTIQ3uSaSct_w` · benchmark: `UCYJ2D_D1q7_sYGorIB2_6iA`.
