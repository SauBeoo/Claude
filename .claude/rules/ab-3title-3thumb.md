# A/B 3×3 — mỗi video 3 TITLE + 3 THUMBNAIL (RULE TOÀN HỆ THỐNG)

> **Nguồn sự thật DUY NHẤT** về bộ A/B. Áp cho **nenkin** + **showa** và kênh mở sau.
> Chốt 2026-08-02 (user: *"tao cần 3 title và 3 ảnh để dùng chức năng test a/b… cho tất cả project"*).
> Rule lo **PHẢI GIAO CÁI GÌ + ĐỌC KẾT QUẢ**. Khuôn hình: file thumbnail của kênh; format title: CLAUDE.md kênh; đo keyword: `youtube-upload-seo.md` §0.5.

## 0. LUẬT
**Mọi video: gói upload phải có ĐỦ 3 title A/B + 3 thumbnail A/B.** Thiếu = chưa đóng gói xong.

## 1. ⚠️ Hai thứ CHẠY KHÁC NHAU
| | THUMBNAIL | TITLE |
|---|---|---|
| Cơ chế | Studio → Thumbnail → **"Test & compare"** (3 ảnh, trả CTR từng bản) | ❌ không có A/B chính thức |
| Cách chạy | song song, tự động | **TUẦN TỰ** bằng `videos.update`, mỗi bản ≥7 ngày |
| Kết quả | Studio trả CTR | tự ghi sổ ngày đổi + so CTR giữa các quãng |

🔴 Lúc test thumbnail **GIỮ NGUYÊN TITLE**. Thứ tự: **đăng bằng A1 → test 3 thumbnail ≥7 ngày → chốt thumbnail → mới xoay A2/A3**.

## 2. BA TITLE — mỗi bản một GIẢ THUYẾT
| | vai | thử cái gì |
|---|---|---|
| **A1** ⭐ | = **Title CHỐT** | bản mạnh nhất theo phép đo Trends |
| **A2** | đổi **KEYWORD DẪN** | ứng viên volume cao thứ hai (đúng intent) |
| **A3** | đổi **KIỂU HOOK** | con số ↔ bí ẩn (「あの◯◯の正体」) ↔ nghịch lý ↔ quote |

1. **A1 trùng đúng từng ký tự với block `Title CHỐT`** (tool đọc A1 làm bản đăng).
2. Cả 3 giữ **format chuẩn của kênh**.
3. Cả 3 qua **quét compliance** và mọi tình tiết phải **có thật trong video**.
4. Ghi dưới heading **`### 3 TITLE A/B`**, dạng bảng (parser đọc ô `` ` ` `` ở cột 2):
```markdown
### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `…` | 32 | 年金@0 | keyword volume cao nhất |
| **A2** | `…` | 30 | 給付金@4 | đổi keyword dẫn |
| **A3** | `…` | 28 | — | đổi kiểu hook (bí ẩn) |
```

## 3. BA THUMBNAIL — mỗi bản đổi ĐÚNG MỘT BIẾN
| | vai | biến |
|---|---|---|
| **T1** | baseline = khuôn đang khoá của kênh | không đổi — mốc so |
| **T2** | đổi **1 biến hình** (nền, tông màu, crop) | giữ NGUYÊN chữ T1 |
| **T3** | đổi **layout** (ít dòng + mặt to, chữ ↔ ảnh đảo tỉ lệ) | hỏi "khuôn kênh có sai không" |

1. **Một biến mỗi bản.**
2. Cả 3 qua duyệt **full-size · 168px · 120px** (`audience-45plus.md` §1); rớt 168px → loại, render lại.
3. Tên **`thumb_T1_*.png` · `thumb_T2_*.png` · `thumb_T3_*.png`** trong folder video — `upload_pack.py` gói thành `thumbnail.*` + `_T2` + `_T3`. ⚠️ File trung gian đặt tên **ngoài pattern** `thumb_T*` (tool bắt nhầm bản chưa hoàn chỉnh).
4. **Trần 2 MB** → vượt thì xuất `.jpg` q95 cạnh nó.
5. Mặt người: stock ẩn danh hoặc nhân vật AI hư cấu; cấm mặt người thật cụ thể.
6. 🔴 **Chữ GIỐNG NHAU ở cả 3 bản và phải TẢI CHỦ ĐỀ** (gate 7 `audience-45plus.md` §1: che ảnh vẫn biết video nói gì · từ dẫn trong top 2 bảng đo).
7. 📄 **Prompt gen thumbnail luôn ghi ra `.txt`**, mỗi prompt 1 dòng: `06_VIDEO/<slug>/thumb_prompts_FLOW.txt` + `thumb_prompts_TENFILE.txt`.
8. 🔴 **PROMPT KÈM TEXT — bake chữ vào ảnh** (user chốt 2026-08-10). ⛔ Cấm prompt kết thúc `No text` rồi để tool vẽ chữ. Prompt ghi đủ **7 mục**: ① từng dòng chữ nguyên văn trong ngoặc kép ② vai màu từng dòng ③ dòng nào TO NHẤT ④ 袋文字 (viền đen + halo trắng) ⑤ `Text must be perfectly formed Japanese characters, crisp and legible` ⑥ `no watermark` ⑦ **chừa trống góc dưới PHẢI** (timestamp YouTube).
   - 🛟 Đường lui: 3 plate **KHÔNG chữ** ở **file riêng `thumb_prompts_PLATE.txt`** — ⛔ đừng để chung FLOW (extension bơm cả file → ra ảnh trắng chữ).
   - 🔴 **Trước khi viết: mở 1–2 prompt gần nhất CÙNG KÊNH, chép cấu trúc.** Bản đã gen đúng nét là khuôn.
   - 📐 Prompt chia **KHỐI cách dòng trống**, **mỗi dòng chữ một dòng riêng** (`line 1, white: …`). Nhồi một câu chạy dài → model nuốt chữ.
   - 🔢 **Trần 4 DÒNG chữ** cho ảnh AI (5 dòng gần như chắc méo kanji).
   - ⚠️ Kanji rậm và dấu 「」 hay nát → **soi TỪNG ký tự trước khi giao**, sai một nét là loại.

## 3.1 🧱 CÁCH VIẾT PROMPT — 5 bước (chốt 2026-08-10, nenkin 10)
**Bước 1 — Lấy khuôn từ ẢNH ĐÃ LÊN SÓNG** (`07_UPLOADED/<slug>/_upload/thumbnail.png`), không từ tài liệu. Tài liệu có thể tả quy trình đã chết. Chỏi nhau thì tin ảnh; kiểm 30s: tool có hàm vẽ nổi thành phần đang thấy không.

**Bước 2 — ĐO ảnh đó bằng máy**, ghi tỉ lệ vào prompt: chiều cao banner (nenkin ~1/5 khung) · hero thắng bằng **BỀ NGANG** (~2/3 khung) hay chiều cao · người cao trọn khung hay nửa khung. ⭐ Cái mua legibility là **bề ngang**, không phải chiều cao.

**Bước 3 — Viết theo KHUNG KHỐI, khối `TEXT` ngay câu 2:**
```
<header: khổ + phong cách + "bold Japanese text burned into the image">

TEXT, exactly these N blocks and nothing else:
<vai khối>, <màu>: <nguyên văn tiếng Nhật>
…

LAYOUT:          <chiều cao banner + vị trí hero "tallest AND widest" + bề ngang hero + trang trí + ribbon>
BACKGROUND:      <chất liệu + ánh sáng + "flat, no shadows">
RIGHT THIRD/HALF:<người: tuổi + tóc + áo + BIỂU CẢM in hoa + đạo cụ + viền cắt-nền + chiều cao>
BOTTOM-LEFT:     <đạo cụ góc + "no characters written anywhere">

<dòng chất lượng> + Keep the bottom-right corner free of text.
No watermark, no logo, no signature, no additional text. --ar 16:9
```
- ⭐ **Gate chính: `TEXT` trong 15% ĐẦU prompt** (đặt cuối → model nuốt chữ):
  ```bash
  python -c "l=open('thumb_prompts_FLOW.txt',encoding='utf-8').readline().rstrip();p=l.find('TEXT, exactly');print(len(l),'ky | TEXT @',p*100//len(l),'%')"
  ```
- **Gate phụ độ dài:** vùng đã chứng minh chạy **tới ~1.700 ký** khi TEXT ở đầu (nenkin 22). Vượt → gộp số đo vào MỘT khối `LAYOUT`, đừng cắt số đo; trên 1.700 thì gen T1 trước, soi từng ký tự. TEXT ở đầu mà vẫn nát → ghi độ dài vào đây.
- Bốn câu bắt buộc: `exactly these N blocks and nothing else` · `no characters written anywhere` ở khối đạo cụ (ô 郵便番号 để rỗng) · `Keep the very bottom-right corner free of text` · `No watermark` (vẫn phải đo ✦ theo lô rồi xử lý — `media-library.md` §2.10).

**Bước 4 — Xuất 4 file, mỗi file một việc:**
| File | Vai |
|---|---|
| `thumb_prompts_FLOW.txt` | 1 prompt / 1 dòng, extension bơm thẳng |
| `thumb_prompts_BLOCKS.md` | bản người đọc: khung khối + bảng số đo + bảng chữ (viết dạng khối trước, nén sau) |
| `thumb_prompts_TENFILE.txt` | thứ tự dòng FLOW ↔ `thumb_T1/T2/T3_*.png` |
| `thumb_prompts_PLATE.txt` | 3 plate không chữ (⛔ không trộn vào FLOW) |

**Bước 5 — CHỮ qua 2 phép đo:** gate 7 (về cái gì · chuyện gì · phải làm gì/mốc) + bảng đo keyword (từ dẫn top 2). Vật nhận diện đẹp mắt mà đo thấp (nenkin 10: `緑の封筒` 33) → **đưa vào HÌNH**, keyword đo được (`支援給付金` 61) → lên **chữ**.

## 4. GATE MÁY
`Projects/youtube-jp-chouhen/tools/upload_pack.py` đếm và in (màn hình + cuối `METADATA.txt`):
```
🔴 GATE 3×3: chỉ có N/3 title A/B …
🔴 GATE 3×3: chỉ gói được N/3 thumbnail A/B …
```
Thấy dòng 🔴 = chưa đóng gói xong. (Một cờ = một quyết định: gate 3×3 không được gắn vào cờ SEO.)

## 5. ĐỌC KẾT QUẢ
- **Thumbnail:** T2 thắng → đưa biến hình vào khuôn · T3 thắng → mở bàn đảo khuôn · T1 thắng → khuôn đúng, đừng test lại biến đó.
- **Title:** chỉ đổi sau khi test thumbnail xong; ghi ngày đổi + bản nào vào `08_ANALYTICS_LOG.md`.
- ⚠️ Impressions quá nhỏ thì CTR vô nghĩa — đọc kèm traffic source + retention; đừng kết luận từ 3 con số CTR đầu. A/B để chọn khuôn, không chữa retention.

## 6. LIÊN QUAN
- Đo keyword: `youtube-upload-seo.md` §0.5 · Từ cấm: `youtube-compliance.md` §3 · Gate chữ/mặt 45+: `audience-45plus.md` §1
- Khuôn showa **K-COLLAGE**: `Projects/youtube-jp-showa/03_THUMBNAIL_FORMULA.md` · khuôn nenkin: `youtube-jp-nenkin/03_THUMBNAIL_TITLE_FORMULA.md`
