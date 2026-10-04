# Lớp SƠ ĐỒ `zu` — 13 GATE BỐ CỤC (RULE TOÀN HỆ THỐNG)

> **Nguồn sự thật DUY NHẤT** về bố cục thẻ sân khấu layout `zu` của `Projects/_media_library/make_stage.py`
> — dùng bởi **nenkin** (và kênh nào dùng lại `make_stage` sau này). Chốt **2026-08-17/18** sau 6 lượt
> user chỉ lỗi bằng mắt trên video 13 nenkin (80 thẻ).
> Rule này lo **BỐ CỤC ĐO ĐƯỢC**. Nội dung/chất người xem `humanize-script-voice.md`; cỡ chữ cho tệp
> 45+ xem `audience-45plus.md`; ảnh AI trong thẻ xem `media-library.md` §2.10.

## 0. NGUYÊN TẮC GỐC — gate hình học KHÔNG đo được cái mắt thấy

Trước rule này, tool đã có ba lớp chống **TRÀN** (kẹp vị trí · hộp bao bất đối xứng · gate chồng nhau)
và **không có một lớp nào** đo:

| mắt thấy ngay | gate cũ thấy |
|---|---|
| khoảng trống dồn lên đầu bảng | ✅ không lỗi |
| nội dung dồn nửa trái, nửa phải trắng | ✅ không lỗi |
| hai mũi tên cùng vai dài 600px và 185px | ✅ không lỗi |
| hộp KẾT QUẢ nhỏ hơn hộp nguồn | ✅ không lỗi |
| icon trang trí lẻ ở góc, không nhãn không nối | ✅ không lỗi |

🔴 **Bài học tổng quát: "không tràn, không chồng" ≠ "cân".** Mỗi lần user chỉ một thẻ, phải hỏi *"lỗi
này là một LỚP hay một thẻ?"* — cả 6 lượt đều ra **một lớp**, và đều sửa được ở tầng tool + gate máy.
Sửa lẻ từng thẻ là để lỗi mọc lại ở video sau.

## 1. MƯỜI GATE (đã cài trong `make_stage.py::zu_check` + `_zu_geom` — builder chỉ `import`)

| # | Gate | Ngưỡng | Chữa thế nào |
|---|---|---|---|
| ① | **Đồ trang trí mồ côi** | icon không nhãn + không edge + một mình một hàng | BỎ. Hoặc cho nhãn / nối edge để nó chở thông tin |
| ② | **Khoảng trống dọc đơn** | ≤ **150px** (bỏ qua khe có edge chạy qua — khe đó là NỘI DUNG) | thêm **KHỐI THỨ BA** (§2), không phải dời hai khối cũ |
| ③ | **Phủ ngang** | ≥ **85%** khe an toàn (540–1505) | `_zu_widen` tự kéo; hàng `fix` thì gõ `at[0]` ra hai mép |
| ④ | **Lề đáy card** | ≥ **44px** (kẹp trong `_zu_place`) | tool tự kẹp; đổi số này thì phải hạ `at[1]` của lưới 2×2 theo |
| ⑤ | **Trần trên** | không leo trên `y0` = đáy tiêu đề | tool tự kẹp |
| ⑥ | **Mũi tên lép** | dài ≥ **28% tổng cỡ 2 node** (sàn tuyệt đối 60px) | giãn `at`, hoặc giảm `s`/`lw`/`w` |
| ⑦ | **Mũi tên cùng vai lệch** | ≤ **15%** | §3 — ba điều kiện đủ |
| ⑧ | **Node chồng nhau** | giao > −6px | giãn `at` |
| ⑨ | **Mực sát 4 mép ảnh thật** | quét pixel dải 16px mỗi mép | (thước đo nghiệm thu, không phải gate builder) |
| ⑩ | **ĐÍCH cuối phải TO NHẤT** | ≥ **70%** diện tích node to nhất thẻ | `hero: true` (label) hoặc tăng `s`/`w`. ⛔ **KHÔNG** thu nhỏ nguồn để lách |
| ⑪ | **Mũi tên ĐƠN phải THẲNG** | thẻ 1 liên kết: cùng hàng (\|dy\|≤70) **hoặc** cùng cột (\|dx\|≤70). 🔴 Đếm cả **`dot`** — đường nét đứt chạy chéo cũng sinh 2 góc rỗng y như mũi tên đặc (dính ở thẻ 53). `elbow`/`arc` thì CỐ Ý gãy khúc, miễn | đưa hai đầu về cùng hàng. Sơ đồ toả/hợp lưu (≥2 liên kết) thì chéo là ĐÚNG, gate bỏ qua |
| ⑫ | **Đuôi bong bóng phải CHẠM** thứ nó chú thích | ≤ **140px** theo hướng `tail` | hạ/nâng `at[1]` của bong bóng. Miễn cho bong bóng đã nối bằng edge (`dot` kiểu "lời từ điện thoại") |
| ⑬ | **Node LƠ LỬNG** | thẻ có mạch mũi tên mà node nội dung **có nhãn** nhưng không nối gì + một mình một hàng. ⚖️ **MIỄN "đề bài"**: dòng chữ ở hàng TRÊN CÙNG với `at[1] ≤ 0,30` (thẻ đố nêu câu hỏi rồi mới tới hai đáp án) | đưa vào mạch: thành **nhãn edge** · cùng hàng · nối `dot`+`x` nếu là "lối không đi được" · hoặc thành dải chốt đáy |

### 🔧 LỆNH BẮT BUỘC — chạy TRƯỚC mọi lượt render, không có ngoại lệ

```bash
python Projects/_media_library/check_zu_layout.py <SLIDES.json> --probe <thư mục PNG --still>
```
`✅ SẠCH 13/13 lớp` mới được dựng mp4. Exit 1 = chặn.

- 10 lớp hình học/vị trí: gate gọi thẳng `make_stage.zu_check()` — **cùng một hàm** builder gọi,
  nên không bao giờ có hai bản số lệch nhau (bài học `_sig`).
- 3 lớp cân đối (②③⑨): chỉ có trong file này, vì `zu_check` không đo được chúng.

🔴 **VÌ SAO LÀ MỘT FILE CHỨ KHÔNG PHẢI THÓI QUEN:** cả 13 lớp lỗi đều do **user soi ảnh
full-size** phát hiện, sau khi tao đã duyệt contact sheet và cho qua — trong một buổi user phải
chỉ **6 lượt** mới hết. Thứ tự đúng, không được đảo:

```
build_slides_*.py  (gate 10 lớp, chặn cứng)
   ↓
make_stage … --still --force        ← dựng PNG, RẺ
   ↓
check_zu_layout.py … --probe …     ← 13/13 phải SẠCH
   ↓
soi 1:1 vài thẻ của TỪNG khuôn helper (§6)
   ↓
make_stage … (KHÔNG --still) → mp4  →  video_render.py
```

## 2. ⭐ LUẬT BA KHỐI — thẻ 2 khối thì KHÔNG THỂ cân

**Hình học, không phải thi hành:** hai khối dọc thì chỉ có **một khe** để nhận hết phần trống ⇒ khe
đó luôn ~180px. Đo được ở 7/80 thẻ (bong bóng + 1 hàng · hàng + bong bóng · vòng tròn + hộp kết quả).

⇒ **Mỗi thẻ `zu` nhắm tới ≥ 3 khối dọc:** thường là **hàng nội dung · bong bóng giải thích · dải chốt
đáy**. Khối thứ ba rẻ nhất là **dải chốt** — và nó phải chở nghĩa thật:

- ✅ **số học từ chính 2 số đang có trên thẻ**: `25万 − 13万9千` → 「減るのは、月11万1千円」
- ✅ **mặt còn lại của điều bong bóng vừa nói**: 「かかるのは報酬比例部分だけ」 → 「基礎年金には、かかりません」
- ⛔ **CẤM bịa số/chế độ mới** để lấp chỗ — YMYL của kênh thắng luật bố cục, không có ngoại lệ.

📌 Đừng chữa khe rỗng bằng **đồ trang trí** (gate ①). Đó chính là cái tao đã làm và user gọi ngay ra:
*"sao lại có cái ảnh riêng lẻ ở góc trái thế"*.

## 3. HAI MŨI TÊN CÙNG VAI — ba điều kiện ĐỦ, tính được chứ không canh mắt

"Cùng vai" = ① chung một đầu (toả 1→N / hợp lưu N→1) hoặc ② cùng hướng (cos ≥ 0,985).

1. **Hai nguồn cùng `at[0]`** và **đích ở ĐÚNG trung điểm dọc** của hai nguồn ⇒ hai vector là ảnh
   gương ⇒ **cùng độ dài tuyệt đối** (đo được: 221,2 = 221,2px).
2. **Ô cùng vai khoá `bw` bằng nhau.** Hộp `label` tự co theo **số ký tự**, nên lưới 2×2 ra 4 ô 4 cỡ
   ⇒ mũi tên hàng trên 371px, hàng dưới 117px. `bw` = bề ngang hộp cố định, như ô bảng.
3. **Hai hàng phải cùng phía mốc `CH_TOP` (368px).** 🔴 Bẫy răng dao: node nằm TRỌN trên đỉnh nhân vật
   được dùng **trọn bề ngang card (312–1608)**, dưới mốc thì bị bó vào **khe giữa hai người
   (540–1505)** — thẻ 30 có hàng 1 ở y=366,4, tức trên mốc **1,6px** ⇒ cùng `at[0]=0,14` mà ra
   cx 512 vs 740 ⇒ mũi tên 336 vs 108px.
   ⇒ Đã siết: **chỉ `ribbon`/`chip`/`banner`/`bubble` (hoặc `at[1] ≤ 0,08`) được dùng khung rộng.**
   Với hàng nội dung, `at[0]` phải nghĩa **một điều duy nhất** trong cả thẻ.

## 4. CƠ CHẾ TRONG TOOL (đọc trước khi sửa bố cục bằng tay)

`zu_fit(v)` chạy MỘT LẦN (cờ `_fit`), gọi từ **cả** `L_zu` (vẽ) và `zu_check` (gate) — một phép đo,
hai người dùng:

1. **Phóng to / thu nhỏ** `s` tới khi nội dung lấp ~86% band (thu thì nhắm 0,90; sàn 0,70).
2. **Chia đều khe dọc**, hàng đầu bắt đầu ngay dưới tiêu đề. Hàng GHIM giữ chỗ: `at[1] ≥ 0,86` = dải
   đáy · `≤ 0,12` = cờ/bong bóng đỉnh.
3. **Chia lại bề ngang** (`_zu_respread`) — bắt buộc đi kèm bước 1, nếu không thì phóng `s` xong node
   ăn vào nhau (lần thử đầu: **21 lỗi mới**).
4. **Hàng song số node bằng nhau dùng CHUNG một khung ngang** (gộp span).
5. **Kéo ngang** (`_zu_widen`) — ánh xạ affine tâm các node cho mép trái/phải chạm hai mép khung.
6. **TỰ LÙI CỠ**: thử k từ to xuống, lấy bản to nhất mà `_zu_geom` **sạch**; nến chót = đúng bản tác
   giả ⇒ `zu_fit` **không bao giờ làm xấu đi**.

🔴 **Cờ `fix` là HỢP ĐỒNG.** Builder đặt `fix` cho những sơ đồ mà **khoảng cách CHÍNH LÀ nội dung**
(toả 2 lối · lưới 2×2 nối elbow · hợp lưu chéo). `zu_fit` không đụng hàng có `fix`. Bản đầu bỏ qua cờ
này ⇒ xếp 4 hàng của thẻ hợp lưu thành 4 tầng đều nhau, khe chéo teo còn 38px.

⚠️ **MỘT VIỆC, MỘT TẦNG.** `polish()` của builder từng cũng cân dọc, bằng **bộ hằng số khác** (chia
lưới theo phân số `at[1]`, đoán "nửa banner = 0,115") — hai tầng cùng ghi `at[1]` thì mỗi lần đổi lề
đáy trong tool là sinh lỗi ở builder (nới 26→44px làm thẻ 30 chồng 382×5px). **Đã bỏ bước cân dọc của
polish.** Cân dọc/ngang = việc của TOOL (nó biết cỡ thật từng kind + biết lề kẹp); builder lo NỘI DUNG.

## 5. BỐN BẪY ĐÃ MẤT MỘT VÒNG SỬA MỚI TÌM RA

1. 🔴 **Sửa ở tầng SAI thì số không đổi, và rất dễ tưởng "vá chưa ăn".** Siết lề đáy trong `zu_fit`
   **hai lần** đều vô hiệu — thứ quyết định là **kẹp trong `_zu_place`**.
2. 🔴 **Hai đại lượng khác vai thì đừng gộp.** `span` (thang đổi `at[1]`↔pixel, **phải TRÙNG** `by1`
   của `_zu_place`) bị gộp với `bot` (lề xếp hàng) ⇒ toạ độ co dãn 14px, triệu chứng y hệt lỗi cần chữa.
3. 🔴 **Sàn tuyệt đối là sai cách khi cái mắt đo là TỈ LỆ.** Nâng sàn mũi tên phẳng lên 100px → **9 thẻ
   rớt**, chuỗi 4 node phải thu về `s=0,72` = chữ 27px, **dưới sàn tệp 45+**. Sàn phải tương đối theo
   cỡ node. Cùng họ với `audience-45plus.md` §6.10 (gate "≥1/3 chiều cao" đo sai chiều).
4. 🔴 **Khe có edge chạy qua KHÔNG phải khoảng trống.** Thước đo void bản đầu báo oan 6 thẻ (lưới 2×2:
   khe 201px đó là chỗ mũi tên khuỷu chạy; thẻ toả 2 lối: khe 224px là chỗ mũi tên đi lên).

## 6. NGHIỆM THU — soi 1:1, sheet thu nhỏ CHO QUA

`media-library.md` §2.10 ⑥ áp **y nguyên** cho thẻ sân khấu: cả 10 lớp lỗi trên tao đều **đã duyệt qua
contact sheet 880×495 và cho qua**; chỉ lộ khi user mở ảnh full-size. Bắt buộc:
`--still --force` → **soi 1:1 vài thẻ đại diện của TỪNG khuôn helper** (spine · slots · cols3 ·
two_ways · one_to_n · chain · hợp lưu) → rồi mới dựng mp4.

## 7. LIÊN QUAN
- Cỡ chữ / mặt / độ dài cho tệp 45+: `audience-45plus.md`
- Ảnh AI làm nền thẻ · watermark · macro: `media-library.md` §2.10–2.11
- Đủ asset mới được render · bẫy `.cmd`: `render-background.md` §1.5, §2.6
- Bảng khuôn + kind + lịch sử 4 đợt sửa của kênh nenkin: `Projects/youtube-jp-nenkin/CLAUDE.md` §VISUAL
