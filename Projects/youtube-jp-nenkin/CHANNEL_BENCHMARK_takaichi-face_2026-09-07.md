# BENCHMARK — "mặt bà thủ tướng 高市早苗" trên thumbnail ngách 年金 (2026-09-07)

> **Câu hỏi của user:** *"tao thấy những kênh cho ảnh bà thủ tướng Nhật vào nó dễ ăn đề xuất"* —
> 3 kênh dẫn chứng: `@ATM速報` · `@年金_フクロウ` · `@年金給付金完全攻略`.
> **Kết luận: giả thuyết KHÔNG đứng được.** Ba phép đo dưới bác nó, và có một kênh cùng tuổi
> **không dùng mặt** đang chạy nhanh hơn **9×**.
> Phép đo: YouTube Data API (token nenkin) + tải thumbnail maxres về soi mắt 1:1.
> Tool: `../youtube-jp-health/tools/bench_channels.py`.

## 0. Xác nhận nhận diện (đúng phần này của user)

Đúng là **高市早苗**. Nhưng **hai loại ảnh khác nhau về rủi ro**, đừng gộp:

| kênh | loại ảnh | dấu nhận biết |
|---|---|---|
| 完全攻略 · フクロウ | **ẢNH BÁO CHÍ THẬT** | nếp nhăn, ánh sáng studio/hội trường, micro trong khung, tóc rối tự nhiên |
| **ATM速報** | **AI dựng lại mặt** | da mịn phẳng bất thường, viền cắt-nền cứng, 議員バッジ vẽ thêm, nền ghép cờ Nhật + cờ Mỹ + biểu đồ |

## 1. Bảng đo

| kênh | lập | tuổi | sub | video | view | **view/ngày** | sub/ngày | mặt Takaichi | nhịp/tuần | cat |
|---|---|---|---|---|---|---|---|---|---|---|
| 年金・給付金完全攻略 | 2026-03-21 | 170d | 145.000 | 16 | 7.014.544 | **41.262** | 853 | **11/12** (thật) | 0,70 | 27 |
| **カメ先生のもらえるお金** | 2026-08-01 | 37d | 5.460 | 32 | 792.599 | **21.422** | 148 | **0/9** | 7,64 | 27 |
| 定年前後のお金の教室 | ~2026-08-08 | 30d | 2.790 | — | ~552.000 | ~18.400 | 93 | — | — | — |
| フクロウの年金・給付金解説室 | 2019-11-13 | 2490d | 46.700 | 45 | 7.610.164 | 3.056 | 19 | 9/12 (thật) | 1,24 | 27 |
| **ATM速報** (kênh user gửi ảnh) | 2026-08-10 | 28d | **390** | 8 | 66.066 | **2.360** | 14 | 5/8 (**AI**) | 2,15 | 22 |
| 年金と老後のお金研究室 (mình) | 2026-07-20 | 49d | 7 | 20 | 6.130 | 125 | 0 | 0 | 3,23 | 27 |

## 2. Ba phép bác giả thuyết

### ① Trong cùng kênh 完全攻略, cái mặt giải thích ~0% biến thiên
Nó dán mặt Takaichi từ **video #1**. Bốn video đầu (đã soi thumbnail, **4/4 đều có mặt**):

| ngày | view | thumbnail |
|---|---|---|
| 2026-03-21 | 5.426 | 年金ルール改悪点4選 — có mặt |
| 2026-03-27 | 12.626 | 65歳以上年金6.7万円一生増額 — có mặt |
| **2026-04-03** | **4.457.932** | 申請をしないと234万円失う — có mặt |
| 2026-04-22 | 88.029 | 90万円支給 助成金9選 — có mặt |

Cùng một khuôn mặt, view chênh **822×**. Tính cả 16 video thì dải là 3.394 → 4.457.932 = **1.313×**.
⇒ Mặt là **hằng số**, không thể là biến giải thích.

### ② Hai hit lớn nhất của フクロウ là hai thumbnail KHÔNG có mặt
| view | view/ngày | thumbnail |
|---|---|---|
| **1.667.239** | 32.653 | 「この封筒返さないと年金口座自動登録される」 — **ảnh cái PHONG BÌ** |
| **100.878** | 1.708 | 「7月に届く介護保険通知書 減税できます」 — **ảnh tờ 通知書** |

Trung vị view/ngày: **9 bản có mặt = 868** · **3 bản không mặt = 1.708**.

### ③ Kênh mới chạy nhanh nhất ngách là kênh 0 mặt
**カメ先生のもらえるお金** lập 2026-08-01 — **cùng tuổi ATM速報** (2026-08-10):

| | カメ先生 | ATM速報 |
|---|---|---|
| mặt Takaichi | **0/9** | 5/8 (AI) |
| thumbnail | nền navy trơn, 0 người, chữ chạy trọn bề ngang | mặt AI + text-wall đỏ/vàng |
| view/ngày | **21.422** | 2.360 |
| sub/ngày | **148** | 14 |

Kênh **không mặt** nhanh hơn **9× view, 10,6× sub**.

### ④ (phụ) Ngay trong ATM速報, mặt cũng không phân biệt được
| # | view/ngày | thumbnail |
|---|---|---|
| 緑の封筒・隠れ給付金 | **3.079** | có mặt |
| 在職定時改定 年金+給料 | **2.167** | **KHÔNG** mặt (cặp vợ chồng già AI) |
| 2027年 住民税 | 1.270 | có mặt |
| 8月14日 年金額激変 | 693 | có mặt |
| 年収の壁 239万円 | 452 | có mặt |
| **新幹線半額** | **80** | không mặt — **lệch đề tài** |
| **羽田空港 新ルール** | **2** | không mặt — **lệch đề tài** |

Hai video bét bảng đúng khuôn thumbnail, đúng chữ to, nhưng **đi khỏi 紙・年金**.
⇒ Biến quyết định là **ĐỀ TÀI**, không phải mặt.
⚠️ Và ATM速報 đang nguội: 5 video mới **452 v/ngày** vs 5 video trước **693**.

## 3. Cái thật sự lặp lại ở mọi hit

**MỘT TỜ GIẤY / PHONG BÌ CỤ THỂ ĐANG ĐẾN + KỲ HẠN + ĐỘNG TỪ MẤT.**

| view | hero thumbnail | mặt? |
|---|---|---|
| 4.457.932 | 9月中に必ず確認して！**申請をしないと234万円失う** | có |
| 1.667.239 | この封筒返さないと**年金口座自動登録される** | **không** |
| 1.053.248 | 6月に届く年金通知書｜ここ確認しないと**○万円吹き飛ぶ**（số bị CHE） | có |
| 100.878 | 7月に届く介護保険通知書 減税できます | **không** |
| 42.001 | まもなく郵送｜隠れ給付金｜通帳を確認して | có |

Mặt xuất hiện ở cả hit lẫn flop. **Tờ giấy + kỳ hạn + động từ mất** thì chỉ ở hit.

## 4. Đối đầu trực tiếp — cùng đề tài 緑の封筒, cùng tháng 9

| | ATM速報 | mình (video 24) |
|---|---|---|
| view | **42.001** | **974** |
| bề ngang chữ hero | ~90% khung | ~55% (cast ông cụ chiếm nửa phải) |
| nền | đỏ/vàng cháy, tương phản cao | kem nhạt kẻ ô + navy — **tương phản thấp ở 168px** |
| chip đối tượng trong TITLE | có | không (đã bỏ 【】 từ 08-29) |

⭐ **Đây là bằng chứng thứ hai, ĐỘC LẬP, cho `audience-45plus.md` §6.10:** thứ mua được
legibility là **BỀ NGANG**, không phải chiều cao. カメ先生 bỏ hẳn người **để lấy trọn bề ngang** —
và nó là kênh mới chạy nhanh nhất ngách.

⚠️ Phân biệt hai loại 【】: mình bỏ `【見逃し厳禁】` (cảnh báo chung chung, đúng — nó bắt cả feed
drama/bóng chày). カメ先生 dùng `【配偶者を亡くされた方へ】` = **chip ĐỐI TƯỢNG**. Hai thứ khác nhau;
bỏ cái thứ nhất không có nghĩa là bỏ cái thứ hai.

## 5. Rủi ro nếu copy — vì sao KHÔNG làm

1. **Luật của chính workspace đã cấm** — `youtube-compliance.md` §2: thumbnail cấm **mặt người
   thật cụ thể**. Không có ngoại lệ nào cho chính trị gia.
2. **ATM速報 làm nặng nhất:** không phải ảnh báo chí mà là **AI likeness của một thủ tướng đương
   nhiệm**, đặt trước cờ Nhật / Quốc hội, cho nội dung chính sách mà bà ấy phụ trách. Đây là nhóm
   YouTube xử nặng nhất (misleading metadata + likeness/synthetic policy), cộng 肖像権・パブリシティ権
   ở Nhật với lý do 報道 rất yếu vì đây là nội dung kiếm tiền dùng mặt bà ấy làm 客寄せ.
3. **Rủi ro tăng theo thành công.** ATM速報 mới 28 ngày — nó chưa chứng minh sống sót, mới chứng
   minh **chưa bị để ý**. 完全攻略 145K sub thì mất là mất sạch.
4. Và theo §2, thứ đánh đổi lấy rủi ro đó **gần bằng 0**.

## 6. Ba việc đổi thay vào đó (đã áp cho video 21)

1. **Bỏ cast khỏi thumbnail**, hero chạy **≥85% bề ngang** (khuôn カメ先生). Cast đang ăn nửa khung
   để đổi lấy thứ `audience-45plus.md` §1.2 đã **miễn gate** cho nenkin.
2. **Trả 【】 về title dạng ĐỐI TƯỢNG** (`【65歳以上の方へ】`), không phải cảnh báo.
3. **Hero = VẬT + động từ mất** (`この秋 届く紙を｜出さないと年2万円`), số đẩy xuống dòng phụ hoặc
   che bằng ○ như 完全攻略.

Tool dựng: `tools/make_thumb_kame.py` — chữ do **Noto Sans JP Black** vẽ nên luôn sắc nét.
🔴 **Cố ý lệch khỏi `feedback_thumbnail_nenkin_chi_dua_prompt`** (nenkin = chỉ đưa prompt, user gen):
khuôn này **100% typography, 0 nội dung ảnh** ⇒ không có gì để gen, mà gen chữ Nhật thì chắc chắn
nát kanji. Đây đúng nhánh "đường an toàn" mà chính memory đó đã ghi: *gen không chữ rồi đốt chữ
bằng code* — ở đây phần "gen" rỗng nên chỉ còn phần đốt chữ.

## 7. Hạn dùng & việc còn mở
- **Đo lại sau 6–8 tuần** (`bench_channels.py` với 5 channelId trong bảng §1). ATM速報 mới 28 ngày
  và đang nguội — nếu nó chết trong 2 tháng thì đó là dữ liệu, ghi vào đây.
- **Chưa đo được:** cái mặt có nhích CTR biên hay không. Có thể có. Nhưng nó **không thể** là lý do
  kênh lên, vì trong cùng kênh nó không phân biệt hit với flop (§2①).
- Mẫu ở §2② và §2③ nhỏ (n=3, n=1 kênh). Ba phép bác **cùng chiều** nên kết luận đứng được, nhưng
  đừng trích một phép lẻ ra như số chắc.
- Nếu bộ T2/T3 khuôn カメ先生 thắng CTR ở Studio Test & compare → cập nhật
  `03_THUMBNAIL_TITLE_FORMULA.md` thành khuôn kênh và ghi vào `08_ANALYTICS_LOG.md`.
