# MỔ 3 VIDEO ĐỐI THỦ + SO VỚI v26 — 2026-09-17

> Nguồn: 3 file user tải về `C:\Users\tuana\Downloads\nenkin`. Mọi số dưới đây **đo bằng máy** từ
> chính file video (ffmpeg/numpy), không phải đọc bằng mắt. Metadata lấy qua YouTube Data API.

## 0. BA VIDEO LÀ AI

| video | kênh | lập kênh | video/kênh | sub | **view/video** | bài này |
|---|---|---|---|---|---|---|
| `yHQ85e7ogl8` | 年金・給付金完全攻略チャンネル | 2026-03 | **17** | 148K | **445.618** | 375.501 view / 6 ngày · 32:58 |
| `CPt2eglQqMo` | なぎさのお金案内所 | 2026-05 | **7** | 2,64K | **64.750** | 11.233 view / 1 ngày · 31:17 |
| `VNsWviEinA0` | ひろと【退職とお金】 | 2025-07 | 98 | 44,8K | 62.055 | 9.093 view / 1 ngày · 13:19 |
| — | **年金と老後のお金研究室 (mình)** | 2026-07 | 25 | ~1,5K | **~600** | — |

⚠️ 完全攻略 = **17 video → 7,58 triệu view**. Đây là kênh mà `02_CONTENT_PLAN.md` đã lấy làm
benchmark từ 2026-07-25 ("ít video, đào sâu topic thắng") — nay có thêm lớp HÌNH để học.

---

## 1. 🔴🔴 SỐ ĐO GIẾT NGƯỜI: KHUNG CỦA MÌNH ĐỘNG GẤP 5–9 LẦN HỌ

Đo MAD frame-to-frame @2fps (đã hiệu chuẩn 5 ngưỡng, đã bỏ dải phụ đề — bài học
`audience-45plus.md` §2.0-ter: scdet đếm phụ đề đổi thành cắt cảnh, lệch 4×):

| | cắt/phút (th8, bỏ dải sub) | giữ mỗi hình (trung vị) | hình >10s | **MAD TB** |
|---|---|---|---|---|
| なぎさ (64.750 v/video) | **4,0** | **16,5s** | 65% | **1,06** |
| 完全攻略 (445.618 v/video) | **5,8** | **9,0s** | 39% | **1,94** |
| ひろと (62.055 v/video) | 14,4 | 4,0s | 4% | 4,28 |
| 🔴 **v26 của mình** | **50,7** | **0,5s** | 1% | **9,97** |

**Đọc đúng con số này:** 50,7 "cắt"/phút KHÔNG phải mình đổi ảnh 50 lần — mà là **khung gần như
không bao giờ đứng yên**. Nguồn số 1 (bắt được 2026-09-17, sau khi lượt đầu đếm nhầm thành "0 clip"):
**61 clip AI × đúng 8,000 giây = 488s / 790s = 62% thời lượng**, mỗi clip MAD 3,83–8,35 và **0%
frame đứng yên**. Phần còn lại đến từ: sticker trượt vào, số đếm tăng dần (sheet 60s đầu bắt được
`37,90 0,000` — số đang chạy), zoom-punch, build-on từng dòng, cast đổi tư thế. MAD 9,97 so với
1,06–4,28 là **chữ ký sản xuất khác hẳn ngách**.

🔴 **Và nó ĐI NGƯỢC chính rule của workspace.** `audience-45plus.md` §2 mục 1 ghi trần **≤6 lần đổi
hình/phút** cho tệp 45+ — lý do: *jump-cut dồn dập gây MỆT và thoát video*. Ba kênh thắng chạy
4,0 / 5,8 / 14,4. Mình chạy 50,7.

⚖️ **Vì sao thành ra thế — không phải làm ẩu, mà là tối ưu quá đà một chiều.** §2.0 (chốt 08-30 từ
lời user *"nói với nền trống, frame đứng yên lâu quá"*) đặt **SÀN**: ≤7s phải có một sự kiện hình.
§2.0b siết tiếp: ảnh chính đổi ≤9,0s. Rồi lớp sticker + punch + pop được thêm để lấp sàn đó. Kết quả:
**sàn được thi hành triệt để, trần bị bỏ quên.** Đúng bài học đã ghi ở chính rule đó — *"tối ưu một
chỉ số thì phải hỏi chỉ số nào là biến ĐÁNH ĐỔI của nó"* — lần này biến đánh đổi là **sự tĩnh cần
thiết để người 70 tuổi đọc kịp chữ**.

---

## 2. NỀN: MÌNH TỐI NHẤT VÀ NHẢY MÀU NHIỀU NHẤT

Độ sáng trung bình khung (0–255), lấy mẫu mỗi 10 giây cả bài:

| | sáng TB | % khung tối (<110) | **độ lệch giữa các cảnh** |
|---|---|---|---|
| ひろと | 220 | 0% | 22,5 |
| なぎさ | 214 | 4% | 33,3 |
| **完全攻略 (bản thắng nhất)** | **202** | **0%** | **7,6** ← ổn định gần tuyệt đối |
| 🔴 **v26 của mình** | **180** | 0% | **41,1** |

Bản ăn 445K view/video giữ **một nền duy nhất suốt 33 phút** (lệch 7,6).

ⓘ Bảng này lấy mẫu **mỗi 10 giây**; gate `check_motion.py` lấy mẫu **2 fps** nên số lệch nhẹ
(v26: 180/41,1 ở đây vs 175/43,4 trong gate). Hai cách đo cùng một kết luận — dùng số của GATE khi
nghiệm thu, số ở đây chỉ để so tương đối. Mình nhảy liên tục giữa
**navy đậm** (cảnh tranh cắt dán) và **kem sáng** (thẻ số liệu) — mỗi lần nhảy là một lần mắt người
già phải thích nghi lại.

📌 Đáng chú ý: `CLAUDE.md` §② đã ghi *"nền TRẮNG ẤM (đổi 2026-08-24 từ navy, user chốt)"* — nhưng
v26 đo ra phần lớn vẫn là nền tối. **Quyết định đã có, thi hành chưa tới.**

---

## 3. THỨ 完全攻略 CÓ MÀ MÌNH KHÔNG CÓ — và nó rẻ

Soi sheet giữa bài (phút 5–15):

1. ⭐⭐ **CHIP CHƯƠNG ĐÁNH SỐ ở góc trên-trái MỌI khung**: `1. 所得税0円なのに住民税がかかる理由` ·
   `2. 役所の計算から控除が消える原因` · `3. 住民税が課税世帯へのさらなる負担`.
   Người xem **luôn biết đang ở chương mấy** — vào giữa video cũng không lạc.
2. ⭐⭐ **Màn 「本日の流れ」 NHẮC LẠI GIỮA BÀI** — 5 mục, mục đã xong có **✅ xanh**, mục đang làm tô
   **đỏ**. Đây là thanh tiến độ: *"còn 2 mục nữa"* = lý do ở lại, tái tạo liên tục.
3. **Case có tên + nơi + tuổi + số, đóng khung xanh lá**: 「木下さん夫妻（名古屋市）夫72歳/妻70歳/
   夫の年金額200万円/妻の年金額78万円」 — giống hệt cast モニター của mình, nhưng **hiện thành một
   THẺ đọc được**, không rải rác trong lời.
4. **Tên địa phương thật + hình bản đồ tỉnh** (名古屋市) → cá nhân hoá.
5. Sơ đồ: hộp trắng viền màu theo vai (xanh lá = thu nhập · đỏ = khấu trừ · xám = kết quả), nền kem
   đồng nhất. **Cùng họ với layout `zu` của mình** — chỉ sạch hơn và ít thành phần hơn.

なぎさ thì đi cực đoan ngược lại và vẫn thắng: **1 màn = 1 ý**, nhiều màn chỉ có **một tiêu đề +
một con số** (「均等割がかからない所得」→「35万円」). Không phụ đề. Mascot nhỏ góc phải.

---

## 4. NHIỄU CỐ ĐỊNH: MÌNH CÓ 3, HỌ CÓ 0–1

| | mình (v26) | 完全攻略 | なぎさ | ひろと |
|---|---|---|---|---|
| watermark SUBSCRIBE đỏ | ✅ có | — | — | — |
| mascot cố định | ✅ cú, góc phải | — | ✅ nhỏ, góc phải | — |
| cast 2 mép sân khấu | ✅ có | — | — | — |
| **tổng vật cố định** | **3** | **0** | **1** | **0** |

Ba thứ này chiếm chỗ ở cả 4 mép và không chở thông tin nào của bài.

---

## 5. ÂM THANH — chỗ duy nhất mình đang ĐÚNG

| | LRA | True peak |
|---|---|---|
| 完全攻略 | 3,0 LU | −6,3 dBFS |
| なぎさ | 4,3 LU | −5,4 dBFS |
| ひろと | 2,4 LU | −5,4 dBFS |
| **mình v26** | **3,1 LU** | −1,2 dBFS |

LRA khớp ngách (nén mạnh, đều — nghe tốt trên loa điện thoại). ⚠️ Chỉ peak của mình **−1,2 dBFS**
sát trần, họ để −5,4…−6,3. Nên hạ limiter xuống ≈ −3 dBTP.

---

## 6. PHƯƠNG ÁN — 6 việc, xếp theo (đòn bẩy ÷ công)

| # | Việc | Số đo mục tiêu | Công | Đụng vào đâu |
|---|---|---|---|---|
| **1** | ⭐⭐ **HẠ ĐỘNG**: bỏ số đếm tăng dần (số hiện nguyên), bỏ zoom-punch, sticker chỉ vào/ra ở mốc, build-on chậm lại | **MAD 9,97 → ≤5,0** · giữ hình 0,5s → **≥3,0s** | trung bình | builder Remotion + **phải nới `audience-45plus.md` §2.0/§2.0b** (xem cảnh báo dưới) |
| **2** | ⭐⭐ **MỘT NỀN SÁNG DUY NHẤT cả bài** — bỏ hẳn nền navy, dùng kem/trắng ấm cho mọi cảnh | sáng TB **≥195** · **độ lệch ≤36** (hiện 175 / 43,4) | thấp | `channels.py` palette + builder |
| **3** | ⭐⭐ **CHIP CHƯƠNG ĐÁNH SỐ** góc trên-trái mọi khung + **màn 本日の流れ nhắc lại 2–3 lần giữa bài** với ✅ tiến độ | mọi khung có chip · ≥2 màn tiến độ | thấp | builder (chữ vẽ bằng font, rẻ) |
| **4** | **Giảm nhiễu cố định 3 → 1**: bỏ SUBSCRIBE đỏ, bỏ cast 2 mép ở cảnh có sơ đồ (giữ cú làm nhận diện, hoặc ngược lại) | ≤1 vật cố định | thấp | builder |
| **5** | **1 màn = 1 ý**: thẻ `zu` giảm còn ≤3 thành phần; số đứng trong thẻ trắng riêng, không đè lên hình | — | trung bình | `build_slides_*` + luật `stage-zu-layout.md` |
| **6** | Hạ true peak −1,2 → **−3 dBTP** | — | rất thấp | `alimiter=limit=0.708` |

🔴 **Việc 1 MÂU THUẪN với rule đang chạy — phải quyết, không lách được.** `audience-45plus.md` §2.0
đặt sàn "≤7s phải có sự kiện hình" và §2.0b "ảnh chính đổi ≤9,0s", cả hai sinh từ lời user 08-30/08-31.
Số hôm nay nói ngược: ba kênh thắng giữ hình **9,0 / 16,5 / 4,0 giây** và MAD **1,06–4,28**. Muốn
làm việc 1 thì phải **nới sàn §2.0** cho kênh nenkin — nếu không, gate `check_frame_pace.py` sẽ chặn.
✅ **ĐÃ SỬA RULE 2026-09-17** (user chốt *"sửa lại rule và áp dụng cho những video sau"*):
`audience-45plus.md` **§2.0-quater** + gate máy `Projects/_media_library/check_motion.py`.
Mốc chốt: **MAD ≤5,0** (chỉ trần) · **giữ hình ≥3,0s** (chỉ sàn) · nền **≥195 / lệch ≤36** · peak **≤−3 dBTP**.
🔴 Bản ngưỡng đầu tiên (MAD 2–4, giữ hình 6–9s) **đã bị bỏ vì SAI**: chạy thử thì nó đánh trượt cả ba
kênh đang thắng — 完全攻略 bị loại vì MAD 1,94 *quá tĩnh*. Ngưỡng chỉ chốt SAU khi chạy ngược trên
toàn mẫu; nghiệm thu: 3 kênh thắng **5/5**, v26 **0/5**.

⚠️ **Cái phương án này KHÔNG chữa:** nhịp hình và màu nền là **chữ ký sản xuất**, không phải retention
của họ (không ai có Analytics của 完全攻略). Và biến trội đã đo được của kênh mình vẫn là **nguồn
traffic** (browse AVP 15,2% vs RELATED 27,5%). Đây là lớp *"làm cho giống ngách đang thắng"*, không
phải viên đạn bạc. Phép thử sạch: làm 3 video theo 6 việc trên rồi đọc AVD + % RELATED, ghi vào
`08_ANALYTICS_LOG.md`.

## 7. LIÊN QUAN
- Trần/sàn nhịp hình: `.claude/rules/audience-45plus.md` §2, §2.0, §2.0b, §2.0-ter
- Bẫy đo nhịp (scdet đếm phụ đề): cùng rule §2.0-bis · memory `feedback_do_pixel_cua_so_quet`
- Bố cục thẻ sơ đồ: `.claude/rules/stage-zu-layout.md`
- Benchmark cũ của chính 完全攻略 (nội dung, không phải hình): `CHANNEL_BENCHMARK_2026-07-25.md`
