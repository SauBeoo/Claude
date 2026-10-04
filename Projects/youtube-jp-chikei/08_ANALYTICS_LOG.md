# 地形と地名の日本史 — SỔ ĐO

> Mọi con số về kênh ghi vào đây, kèm NGÀY và CÁCH ĐO. Sổ trống thì mọi phanh ở
> `00_CHANNEL_BIBLE.md` §4 đều vô hiệu — không có gì để so.

## 0. MỐC GỐC (2026-09-16, lúc tiếp quản)

| | |
|---|---|
| channelId | `UCfXuolJMQ-3CMpmTeQVkwKA` (từ `사우 오디오`) |
| sub / video / view | **0 / 3 / 56** |
| 3 video cũ | audio drama KR — ✅ **đã đặt private 2026-09-16** (Studio báo "3/3") |
| handle | ✅ **@chikei-chimei** |
| lịch | T3・T6・CN 20:00 JST |

## 1. SỔ XOAY TRỤC + VÙNG (chống lặp — `02_CONTENT_PILLARS.md` §4)

| # | slug | ngày đăng | trục | vùng | ô hình "chỉ kênh này có" |
|---|---|---|---|---|---|
| | | | | | |

⛔ Không 2 video liên tiếp cùng trục · không 3 video liên tiếp cùng vùng.

## 2. SỐ ĐO THEO VIDEO

| # | ngày | view 7d | view 28d | AVD | nguồn chính | ghi chú |
|---|---|---|---|---|---|---|
| | | | | | | |

## 3. A/B — thumbnail (Studio Test & compare) + title (tuần tự ≥7 ngày)

| video | T1 CTR | T2 CTR | T3 CTR | bản thắng | ngày đọc |
|---|---|---|---|---|---|
| | | | | | |

## 4. KHÁM KÊNH — bắt buộc kéo VIDEO DẪN

Sau **10 video**: chạy `insightTrafficSourceDetail` (RELATED) → tra title/kênh → **đếm tỉ lệ
cùng ngách**. <5/24 ⇒ YouTube chưa hiểu chủ đề kênh → `youtube-suggested-growth.md` §1.5.
⛔ Đừng đọc tuổi/giới rồi kết luận "đúng tệp" — bài học
`feedback_dung_tep_nhan_khau_khac_dung_khu_pho`.

| ngày khám | imp/video | CTR | browse | suggested | search | RELATED cùng ngách | kết luận |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## 5. NHẬT KÝ QUYẾT ĐỊNH

- **2026-09-16** — ✅ **ĐỔI MẶT KÊNH XONG bằng Studio** (không qua API vì token không ghi được):
  tên `地形と地名の日本史` · handle `@chikei-chimei` · mô tả 639 ký · 28 keywords JP ·
  country KR→**JP** · đơn vị tiền USD→**JPY** · ngôn ngữ video mặc định → **tiếng Nhật** ·
  avatar + banner (dựng từ 断面図 代々木→渋谷) · **3 video KR → private**. Verify lại bằng API.
  ⚠️ `snippet.defaultLanguage` của KÊNH vẫn `en` — Studio không có ô sửa nó; chỉ `channels.update`
  (API) đổi được, nên treo tới khi có token ghi. Ảnh hưởng nhỏ: nó chỉ nói ngôn ngữ metadata kênh.
- **2026-09-16** — 🔴 **Token kế thừa từ kr-romfan KHÔNG ghi được lên kênh**: `channels.list(mine=True)`
  trả `totalResults: 0` ⇒ lúc OAuth đã chọn **account cá nhân** thay vì **brand channel**. Đọc thì
  được (đọc bằng `id=`), nhưng `channels.update` và `videos.update` đều **403**. Phải OAuth lại
  bằng `tools/auth.py` (đã thêm scope `.../auth/youtube` — `force-ssl` KHÔNG đủ cho
  `channels.update`). ⇒ **Bài học mang đi được: `mine=True` trả 0 là dấu hiệu token sai chủ thể —
  kiểm cái này TRƯỚC khi đổ lỗi cho scope.**
- **2026-09-16** — Lập kênh bằng cách chuyển đổi `사우 오디오`. Chốt: tên 地形と地名の日本史 ·
  trục T1+T2 lõi (①đóng gói lại) · lớp hình = bản đồ 国土地理院 + ảnh AI phụ · lịch T3・T6・CN
  20:00 · 3 video KR → private. Giọng **麒ヶ島宗麟** (user nghe 4 demo rồi chốt) — tránh trùng 青山龍星 của 3 kênh khác.
