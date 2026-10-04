# CÔNG THỨC RETENTION — chouhen (bản không phụ thuộc độ dài)

> Đo bằng YouTube Analytics API ngày **2026-08-11** — 9 video, curve 20 mốc mỗi video.
> User chốt: *"cứ dựa vào công thức mà làm, ngắn hay dài đâu quan trọng."* → công thức dưới đây tính bằng **PHÚT TUYỆT ĐỐI**, độ dài là **kết quả** của số sóng viết ra, không phải tham số đầu vào.
> **Đè lên** `CHANNEL_DIAGNOSIS_2026-08-01.md` §5.1–5.2 · `CLAUDE.md` §LUẬT 2 PHÚT ĐẦU · §Độ dài.

---

## 0. KẾT LUẬN — HAI CÂU

1. **Kênh không chết vì video dài — nó chết vì PHẦN MỞ BÀI GIÃN RA THEO ĐỘ DÀI.** Đồng hồ khán giả chạy bằng **phút**, không bằng **phần trăm**; mọi luật cũ tính theo % là lý do 6/6 video 50′+ chết. Chữa bằng **đóng băng mở bài** rồi cộng **sóng**.
2. **Cửa tử thật là GIÂY 16–35** (§3.2b): gần như không ai bỏ đi trong 16 giây đầu, rồi mất 23,7đ (video 12) hoặc 43,0đ (video 09) trong ~17 giây. **Một câu lời kể đặt vào cửa sổ đó đắt hơn cả 26 phút còn lại.**

⭐ **Muốn AVD >60%: bỏ hẳn khối 回想** → §4.4. Một đòn đó đưa video 12 từ 27′34 xuống 25′14 và AVD **55,7% → 60,8%** mà không cần giữ người giỏi hơn một giây nào. Nhưng **>60% và bài 50′+ loại trừ nhau** — 60% ở 52′ đòi 31,2 phút xem = 2× kỷ lục kênh.

---

## 1. BẢNG GỐC — retention tại 2 mốc PHÚT tuyệt đối

| video | dài | AVD | phút xem | @~11′ | @~16′ | **Δ** | cú lật đầu |
|---|---|---|---|---|---|---|---|
| **12** gibo-rikontodoke | 27′34 | **51,6%** | **14,2′** | 52% (11′01) | **59%** (16′32) | **+7,0** | **11′41** |
| **09** aikagi-mudan-doukyo | 40′42 | 32,0% | 13,0′ | 40,8% (10′10) | 42,5% (16′16) | **+1,7** | **15′52** |
| 07-06 | 43′59 | 26,2% | 11,5′ | 28,6% (10′59) | 29,7% (15′23) | +1,1 | ~21′ |
| **07-17** | 54′49 | **28,9%** | **15,6′** | **45%** (10′57) | **30%** (16′26) | **−15,0** | ❌ không có |
| 07-22 | 51′48 | 16,1% | 8,1′ | 23,8% (10′21) | 19,1% (15′32) | **−4,7** | ❌ không có |
| 07-19 | 67′03 | 18,2% | 12,0′ | 18,8% (10′03) | 12,5% (13′24) | **−6,3** | ❌ không có |

🔴 **Chia đôi sạch, 6/6 không ngoại lệ:** cú lật đầu rơi **trước phút 16** → Δ **dương**. Không có → Δ **âm**.

### 1.1 Ca đắt nhất: 07-17 cầm được khán giả rồi ném đi
Giữ **45% ở phút 11** — cao hơn cả video 09 (40,8%) — rồi **mất 15 điểm trong 5 phút** vì giữa phút 11 và 16 không có cú lật nào. Nó vẫn mang về **15,6 phút xem**, **nhiều hơn video 12** (14,2′). ⇒ Vấn đề của nó là **cấu trúc**, không phải độ dài.

### 1.2 Cơ chế: khung 9 nhịp tính theo % nên tự giãn ra

Khung hiện hành đặt thác trả thù (NHỊP 5) ở ~46–51% thời lượng:

| độ dài | 46–51% rơi vào phút | so cửa phút 12 |
|---|---|---|
| 27′34 | 12′40–14′00 | ✅ trúng cửa |
| 40′42 | 18′43–20′45 | 🟠 trễ 7′ |
| 55′00 | 25′18–28′03 | ❌ trễ 16′ |
| 67′03 | 30′51–34′12 | ❌ trễ 22′ |

**Cùng một khung: ở 27′ trúng cửa, ở 55′ trễ 16 phút.** Khán giả không ghét video dài — họ bỏ ở phút 15 vì tới phút 15 chưa có ai trả giá.

### 1.3 ⭐ Phần mở bài của 2 video thắng — ĐỘ DÀI KHÁC NHAU, PHÚT GIỐNG NHAU

| | video 12 (27′34) | video 09 (40′42) |
|---|---|---|
| mở bài kết thúc ở | **11′41** = 42% | **15′52** = 39% |
| tính theo % | gần như bằng nhau | gần như bằng nhau |
| tính theo PHÚT | **11,7′** | **15,9′ (+36%)** |
| Δ retention 11′→16′ | **+7,0** | +1,7 |

Hai video cùng "39–42%" nhưng lệch nhau **4,2 phút thật** — và đúng 4,2 phút đó là toàn bộ khoảng cách giữa AVD 51,6% và 32,0%. **Đây là bằng chứng trực tiếp rằng % là đơn vị sai.**

---

## 2. ⭐⭐ LUẬT SCALING — phần mở bài ĐÓNG BĂNG, chỉ cộng SÓNG

```
Độ dài video  =  11′ (mở bài, CỐ ĐỊNH)  +  3,5′ × N sóng  +  3′ (kết)
```

| N sóng | độ dài ra | ký (@265/phút) | ghi chú |
|---|---|---|---|
| 4 | ~28′ | ~7.400 | ≈ **video 12** (5 sóng / 27′34) — vùng đã chứng minh |
| 6 | ~35′ | ~9.300 | |
| 8 | ~42′ | ~11.100 | |
| **10** | **~49′** | **~13.000** | |
| 12 | ~56′ | ~14.800 | |
| 13 | ~59′ | ~15.600 | trần thực tế |

🔴 **Đây là chỗ 6 video dài đã làm SAI:** chúng giãn **phần mở bài** ra 25–34 phút rồi nhét 1 thác trả thù ở cuối. Đúng phải là **giữ mở bài 11 phút và viết THÊM SÓNG**. Video 52′ cần **11 sóng**, không phải 1 thác dài hơn.

**Đo thật khoảng cách giữa các sóng của video 12** (AVD 51,6%): 11′41 → 14′44 → 18′21 → 21′59 → 25′04 = gap **3,0 / 3,7 / 3,6 / 3,1 phút**. ⇒ **3,5′/sóng là số của bản thắng**, không phải số tao chọn.

### 2.1 Hệ quả nội dung: N sóng = N lần MỘT người/tổ chức trả giá

Không viết được 11 sóng bằng cách kéo dài 1 cú lật. Phải có **danh sách người trả giá**, mỗi người/tổ chức là 1 sóng riêng:

`義母 · 夫 · 愛人 · 義弟/義妹 · 会社 hoặc 銀行 · 世間体/近所 · 親族会議 · 弁護士/司法書士 · 役所 · 記者/SNS · 遺言/登記`

Video 12 dùng 5 (夫 · 愛人 · 義母 · 銀行 · 融資). Muốn 52′ thì cần **~11 đầu mối trả giá**, hoặc cho một người trả **nhiều lần theo tầng** (mất mặt → mất tiền → mất chỗ đứng).

---

## 3. Sáu biến còn lại (đo từ 09 + 12)

### 3.1 Gap giữa 2 beat ≤ 2′45″ — biến mạnh thứ hai

| | video 09 | video 12 |
|---|---|---|
| gap dài nhất | **4′14″** | **2′43″** |
| số gap ≥3′26″ | **5** | **0** |

**MỌI hố retention của video 09 nằm trong một gap ≥3′26″:**

| gap trong 目次 | % video | retention |
|---|---|---|
| 05:33 → 09:05 (3′32) | 20% | **34,0%** đáy |
| 10:10 → 14:11 (4′01, 回想) | 30% | **34,5%** đáy |
| 15:52 → 20:06 (4′14) | 45% | 36,4% |
| 25:03 → 28:29 (3′26) | 65% | **34,2%** |
| 29:27 → 33:36 (4′09) | 80% | 36,2% |

### 3.2 Cold open đo bằng GIÂY, không bằng ký tự

60 giây đầu của cả 18 video đều tải 265–345 ký ⇒ **ngân sách ký không phải chỗ khác nhau.** Khác là **cái gì nằm trong đó**:

| mốc | video 12 | video 09 |
|---|---|---|
| giấy tờ gọi tên | **giây 0** (離婚届) | giây 64 (間取り帖) |
| **anomaly người nghe tự soi ra** | **giây 19** (証人欄 có 流れるような、女の字) | giây 89 (ngày 10/3 < nhà xong 11/2) |
| open-loop ĐẾM ĐƯỢC | **giây 51** 「三つのことを知らなかった」→ 一つ/二つ/三つ | giây 124, 2 loop, không đếm |
| chính diện phản đòn | **giây 71** 「ありがとうございます、お義母さん」 | giây 139 |

**Kiểm chéo 18 video:** device 「まだ知らなかった」 có ở **15/18** ⇒ **có device không phải lợi thế, VỊ TRÍ mới là lợi thế.** Đặt trước giây 60: 08 (@0:55 → 273 view) · 12 (@0:51 → AVD 51,6%). Đặt muộn: 10 (@2:22 → 5 view, AVD 10%) · 11 (@2:04 → 48 view).

### 3.2b ⭐⭐ CỬA TỬ THẬT LÀ **GIÂY 16–35** — không phải 30s, không phải 60s

Kéo `audienceWatchRatio` ở độ phân giải **1%** (thay vì 5%):

| | video 12 (AVD 51,6%) | video 09 (AVD 32,0%) |
|---|---|---|
| giây 16 / 24 | **96,7%** | **100,6%** |
| giây 33 / 48 | **73,0%** | **57,6%** |
| **mất trong ~17 giây** | **−23,7đ** | **−43,0đ** |
| giây 49 / 73 | 67,2% | 50,8% |
| giây 66 | 62,3% | — |
| **giây 82** | **65,6% ↑ HỒI +3,3đ** | — |
| giây 97/99 | 62,3% | 48,4% |

🔴 **Gần như KHÔNG AI bỏ đi trong 16 giây đầu** (96,7% và 100,6%). Toàn bộ cú giết gói trong **~17 giây tiếp theo**. Đây là cửa sổ đắt nhất của cả video — nó mất nhiều điểm hơn toàn bộ 26 phút còn lại cộng lại.

**Cái gì giết video 09 — xác định được đúng câu.** Giây 24–48 của nó:
```
[24] 「二階は拓也たちね。          [32] 床の耐荷重から換気の位置まで、私が二年かけて決めた部屋だった。 ← ☠
[26] それから、そこの――」        [39] 「嫁のお菓子ごっこの部屋は、仏間にするわ」  ← câu đòn, TỚI GIÂY 39
[28] 義母は顎で…示した。          [43] 工房の入り口には、見たことのない仏壇の箱が…
```
**Giây 32 là một câu LỜI KỂ giải thích kỹ thuật, đặt đúng tâm cửa tử**, và câu đòn tới giây 39 mới nổ. Video 12 có **0 câu lời kể ≥25 ký** trong cửa sổ đó — nó đặt **anomaly ở giây 19**.

⇒ **R3b (gate CHẶN): trong giây 16–35 phải có ĐÚNG 0 câu lời kể ≥25 ký.** Chỉ được có thoại · câu kể ngắn <25 ký · anomaly. Đo bằng máy: `check_retention.py` in ra từng câu vi phạm kèm giây.

⭐ **Phát hiện thứ hai, dùng được ngay: câu phản đòn KÉO NGƯỜI QUAY LẠI, không chỉ giữ.** Video 12 hồi **+3,3 điểm** ở giây 82 (62,3 → 65,6), ngay sau 「ありがとうございます、お義母さん」 ở giây 71. ⇒ R5 mạnh hơn tưởng; nhắm >60% thì đẩy câu này về **~giây 50**.
⚠️ Một phần trong 23,7 điểm là **bounce không cứu được** (bấm nhầm, lệch thumbnail) → đừng nhắm 0.

### 3.3 🔴 LOOP COLD OPEN PHẢI ĐÓNG Ở ~80–85%, KHÔNG ĐÓNG SỚM

| | anomaly mở | đóng ở | retention nửa sau |
|---|---|---|---|
| **12** | giây 19 (女の字) | **21′59 = 80%** | 54–60%, **tăng** |
| 09 | giây 89 (注文控え) | **15′52 = 39%** | 32–43%, phẳng thấp |

Video 09 **đốt loop lớn nhất ở phút 16**, rồi còn 25 phút sống bằng loop nhỏ. Càng dài thì lỗi này càng chết: **loop cold open là dây duy nhất đủ sức kéo người nghe qua phút 40.**

### 3.4 回想 — trần 2′30″, mở ở PHÚT 8–11 (không phải "sau 20%")

| | video 12 | video 09 |
|---|---|---|
| vị trí / dài | 05′11 / **2′20** | 10′10 / **4′01** |
| retention | 59→55% (−4) | 40,8→34,5% (−6,3) |

回想 là beat duy nhất không có xung đột hiện tại → **luôn** là hố. Chữa bằng làm ngắn, không phải dời. ⚠️ Luật cũ "không mở 回想 trước 20%" ở bài 55′ đẩy nó tới phút 11 — **vẫn được, nhưng phải xong trước phút 11 để SÓNG 1 kịp cửa.**

### 3.5 Cú lật phải ĐƯỢC ĐÁNH SỐ
Video 09 là video **duy nhất** của kênh có đuôi quay lên ngang mốc 5% (43,3% vs 43,0%) — nhờ **5 cú lật đánh số** 逆転①→⑤. Đây là thứ nên bê nguyên từ 09.

### 3.6 Câu ngắn — tín hiệu YẾU, không làm gate
Ký/phụ đề: 12 = 14,8 (ngắn nhất kênh) · 09 = 17,1 · nhóm 50′+ chết = 20,5–22,0. Đúng chiều nhưng video 11 có 15,6 mà chỉ 48 view ⇒ **khuyến nghị ≤16 ký/câu, không gate.**

---

## 4. 🎯 KHUNG **RETENTION-A** — viết theo phút, dài bao nhiêu cũng dùng

### 4.1 Phần MỞ BÀI — cố định 11 phút, không bao giờ giãn

| Khối | Phút | Ký | Việc phải làm |
|---|---|---|---|
| **COLD OPEN** | 0–1′20 | ~350 | giấy tờ gọi tên **giây 0** · anomaly người nghe tự soi **giây ≤25** · 「三つのことを知らなかった」+ liệt kê 一つ/二つ/三つ **giây ≤60** · chính diện phản đòn **giây ≤80** → **mở 3 loop** |
| **A · Nhục nhã leo thang** | 1′20–8′ | ~1.750 | 3–4 beat sỉ nhục, **mỗi beat gài 1 vật chứng** (đừng chỉ mắng) → mở 1 loop |
| **回想 ngắn** | 8′–10′30 | ~650 | **≤2′30.** Chỉ tải MỘT thứ: vì sao chính diện có quyền lực ẩn |

### 4.2 Phần SÓNG — lặp N lần, mỗi sóng 3′30″

Mỗi sóng có đúng 3 việc, theo thứ tự:
1. **Nạp** (~1′) — một vật chứng/một người mới bước vào
2. **Nổ** (~1′30) — 逆転Ⓝ: một người/tổ chức trả giá, **đánh số**
3. **Gieo** (~1′) — **mở loop mới TRƯỚC khi sóng sau bắt đầu**

| Sóng | Rơi vào phút | Vai |
|---|---|---|
| **SÓNG 1** | **10′30–14′** 🔴 hạn chót **phút 12** | đòn nhỏ nhất: 1 cuộc gọi / 1 câu hỏi làm lộ một lời nói dối |
| SÓNG 2 | 14′–17′30 | vật chứng GIẤY nổ (契約/届/登記/明細) |
| SÓNG 3 | 17′30–21′ | bên thứ ba chính danh vào (司法書士/弁護士/銀行/監査) |
| SÓNG 4 | 21′–24′30 | đòn thể chế: mất tiền / mất chức / bị cấm cửa |
| SÓNG 5 | 24′30–28′ | nội bộ phe ác vỡ, đồng minh trở giáo mang vật chứng mới |
| … | mỗi sóng +3′30 | thêm một người/tổ chức trả giá (§2.1) |
| **SÓNG N−1** | — | thân phận ẩn của chính diện lộ công khai |
| **SÓNG N** | **≥85% thời lượng** 🔴 | **ĐÓNG LOOP COLD OPEN** — anomaly ở giây 19 mới được giải thích ở đây |

- **CTA** (`cta-midvideo.md` §2.1): đặt **ngay sau sóng ở gần mốc 50%**, không đặt trước một cú nổ.
- **Bất biến:** số loop đang mở **không bao giờ về 0** trước SÓNG N.

### 4.3 KẾT — 3 phút
因果応報 từng nhân vật + chữ ký kênh (verbatim, `cta-midvideo.md` không đụng NHỊP 9).

---

## 4.4 ⭐⭐ CẤU HÌNH NHẮM **AVD >60%** — `dài = 8′ + 3,5′×N + 2′30`

```
dài 24–26′  =  8′ mở bài (BỎ HẲN 回想)  +  3,5′ × 4 sóng  +  2′30 kết
SÓNG 1 phút 7–8 · anomaly giây ≤20 · phản đòn giây ~50 · loop cold open đóng ≥78%
giây 16–35: 0 câu lời kể
```

🔴 **60% VÀ BÀI 50′+ LOẠI TRỪ NHAU — chốt trước khi viết:**

| dài | phút xem cần cho AVD 60% | so kỷ lục kênh (15,6′) |
|---|---|---|
| **25′** | **15,0′** | ✅ **đã làm được** (video 12 ngày 1 = **15,34′**) |
| 27′34 | 16,5′ | +6% |
| 40′ | 24,0′ | +54% |
| 52′ | **31,2′** | **+100% — ngoài tầm** |

📌 **Số nền tốt hơn con số lifetime cho thấy:** video 12 đạt **55,7% ở NGÀY 1** (83 view, 15,34′ xem); 51,6% là lifetime bị traffic nhỏ giọt kéo xuống. **Khoảng cách thật tới 60% là 4,3 điểm.**

**Bốn đòn, xếp theo hiệu quả trên mỗi công bỏ ra:**

| | đòn | được | rủi ro |
|---|---|---|---|
| **L1** ⭐ | **BỎ HẲN khối 回想** (2′20, nằm đúng vùng trũng 59→55%) | 27′34 → **25′14** ⇒ 15,34/25,23 = **60,8%** — vượt 60% **mà không cần giữ người giỏi hơn một giây** | thấp nhất; lai lịch rải vào thoại |
| **L2** | **SÓNG 1 về phút 7–8** (đang 11′41) | +3–4đ — trũng dính sát mặt trước sóng 1 | GIẢ THUYẾT, chưa ai làm sớm hơn |
| **L3** | **Viết lại giây 16–35** (mất 23,7đ) | nhiều nhất về lý thuyết | khó nhất; một phần là bounce không cứu được |
| **L4** | **Cắt 1′ đuôi** 因果/新しい朝 (70%→100% mất 16đ) | cùng L1 → 24′14 ⇒ **63,3%** | thấp |

⚠️ **L1 đè R6 của chính file này** (R6 cho phép ≤2′30). Với mục tiêu >60% thì 回想 = **0**.
⚠️ **L1 + L2 KHÔNG được đặt làm ngưỡng CHẶN** — video 12 vi phạm cả hai (回想 2′20 · sóng 1 ở 11′41) mà vẫn đạt 55,7%; chặn ở mức mục tiêu là **fail chính bản thắng**. Đó là bài học đã mắc một lần với R11 (đặt 85% → fail video 12 → phải hạ về 78%).

---

## 5. GATE — 12 số, kiểm bằng máy

| # | Chỉ số | Ngưỡng CHẶN | Mục tiêu >60% | Căn cứ |
|---|---|---|---|---|
| R1 | Độ dài | **= 10,5\|14 + 3,5×N** | 24–26′ | §2, §4.4 |
| R2 | Giấy tờ/vật chứng gọi tên | ≤ giây **10** | — | §3.2 |
| R3 | Anomaly người nghe tự soi | ≤ giây **25** | ≤ giây **20** | §3.2 |
| **R3b** | **Giây 16–35: câu lời kể ≥25 ký** | **= 0 — CHẶN** | — | §3.2b ⭐⭐ |
| R4 | Open-loop đếm được (3 loop) | ≤ giây **60** | — | §3.2 |
| R5 | Chính diện phản đòn lần đầu | ≤ giây **80** | **~giây 50** | §3.2b |
| R6 | 回想 | ≤**2′30** & xong trước **phút 11** | **BỎ HẲN (= 0)** | §3.4, §4.4 |
| **R7** | **Gap dài nhất giữa 2 beat** | **≤2′45 — CHẶN** | — | §3.1 ⭐ |
| **R8** | **SÓNG 1** | **≤ phút 12 — CHẶN** | **phút 7–8** | §1 ⭐⭐ |
| R9 | Số sóng, đánh số 逆転Ⓝ | **≥4** | 4 | §2 |
| **R10** | **Gap giữa 2 sóng** | **≤4′** (video 12: 3,0–3,7) | — | §2 |
| **R11** | **Loop cold open đóng ở** | **≥78% — CHẶN** (video 12 = 80%) | — | §3.3 ⭐ |

### Dự đoán
Bài 27–30′ áp đủ 11 số → AVD **50–55%** (video 12 đạt 51,6% khi đã thoả 8/11).
Bài 49–52′ áp đủ 11 số → phút xem **17–19′**, AVD **34–38%**. Căn cứ: 07-17 đã mang về 15,6 phút xem **trong khi vi phạm R8 và R10**; sửa 2 số đó là phần thiếu.
⚠️ **Chưa mẫu nào của kênh chạy đủ 11 số** → đây là dự đoán, 3 video đầu là phép thử.

---

## 6. BA ĐIỀU KHÔNG ĐƯỢC ĐỌC LẪN

### 6.1 Công thức này chữa RETENTION, không chữa PHÂN PHỐI
Sau video 12 (07-30) kênh **sụp về 0–4 view suốt 10 video liên tiếp** (07-31→08-08), rồi 08-09=5, 08-10=17, 08-11=1. Ba video có view thật (09=367 · 08=273 · 12=124) đăng gọn trong 6 ngày 07-25→07-30. **Rail đóng sau 07-30 là vấn đề riêng**, cần mổ traffic 10 video đó. Áp công thức không tự kéo view về.

### 6.2 Càng dài càng phải giữ người lâu gấp bội — đó là cái giá thật
AVD 33% (ngưỡng mở rail) đòi: **8,9 phút xem** ở bài 27′ · **13,4′** ở bài 40′ · **17,2′** ở bài 52′. Tốt nhất kênh từng làm được là **15,6′** (07-17). ⇒ bài ≤40′ nằm trong vùng đã chứng minh; bài 50′+ đòi vượt kỷ lục kênh **+10%**. Viết được, nhưng biết trước.
🛑 **Phanh:** 3 video liên tiếp AVD ≤28% → hạ về 27–30′ (N=4–5), đừng cố lần thứ tư.

### 6.3 Đường song song rẻ hơn nhiều
`audience-45plus.md` §4.1 cho phép **>60′ dạng 総集編/まとめ** = nối 2–3 tập ĐÃ ĐĂNG + thumbnail mới + 目次. Chi phí ~0, thời lượng xem cao, không mang rủi ro retention của tập lẻ. Kênh có 22 tập → ghép được ngay, đăng slot T7/CN.

---

## 7. LIÊN QUAN
- Số bị đè: `CHANNEL_DIAGNOSIS_2026-08-01.md` §5.1 (bucket độ dài), §5.2 (cửa tử 60s — vẫn đúng, bổ sung cửa **phút 12**)
- Khung 9 nhịp cần sửa: `.claude/skills/script-chouhen/SKILL.md` MỤC 10 + 14
- `.claude/rules/audience-45plus.md` §3, §4.1 · `.claude/rules/cta-midvideo.md` §2.1, §3
- Đo lại: `python tools/analytics_report.py --channel chouhen --video <ID>` sau 72h
- Gate máy: `python tools/check_retention.py <slug>`
