# Việc phải bấm TAY trong Studio — 2026-09-16

> Chrome profile **Profile 17** (`.claude/rules/channel-browser.md`) · tổng **~25 phút**.
> ⛔ Đặt file ở GỐC PROJECT, không đặt trong `06_VIDEO/<slug>/` — chỗ đó bị
> `upload_pack --done` quét sạch (đã làm mất đúng file checklist của 2026-08-31).

## Đã làm bằng API rồi — mày KHÔNG phải đụng

| việc | kết quả |
|---|---|
| Gán lại 3 playlist trụ | A **9** · B **9** · C **6** (trước: 6/6/11 dồn sai trụ) |
| Khối `▼関連する研究ノート` vào mô tả | **24/24 video**, link có `&list=` |
| Chuẩn hoá 3 hashtag đầu `#年金 #年金生活 #老後のお金` | 24/24 |
| Phụ đề `ja` | **0/24 thiếu** — không phải làm gì |
| Bình luận (nội dung) | 8/8 video đã có sẵn trên trang |

---

## 1. Keywords kênh — 2 phút 🔴 API KHÔNG GHI ĐƯỢC

**Đo được 2026-09-16:** `channels.update` trả HTTP 200 và **echo đúng giá trị mới**, nhưng
`channels.list` đọc lại ngay sau đó vẫn ra **giá trị cũ**. YouTube nuốt lệnh, không báo lỗi.
⇒ Tin response là ghi nhầm vào sổ "đã xong".

**Studio → 設定 → チャンネル → 基本情報 → キーワード** → xoá hết, dán nguyên khối:

```
年金と老後のお金研究室 年金 老後のお金 年金いくらもらえる 在職老齢年金 繰り下げ受給 繰り上げ受給 遺族年金 給付金 年金生活者支援給付金 厚生年金 国民年金 年金受給額 年金改正 2026年年金 退職金 年金制度 年金手続き 年金生活 老齢基礎年金 老齢厚生年金 加給年金 特別支給の老齢厚生年金 公金受取口座 年金振込通知書 扶養親族等申告書 住民税非課税 介護保険料 年金支給日
```

**Bỏ 6 từ** `シニア · 60代 · 50代 · 定年後 · 老後の生活費 · 老後資金` — chúng không nói gì về
年金, chúng nói về **một NHÓM TUỔI**, và nhóm tuổi đúng là thứ YouTube đang phân loại kênh này
theo ("nam 65+ chung chung"). **Thêm 11 thực thể** trong ngách.
⚠️ Tao đã suýt bỏ nhầm cả `給付金` (từ đo được **14,81**, cao thứ hai của kênh) — đã sửa.

## 2. Ghim 8 bình luận — 3 phút

Nội dung **đã đăng sẵn** bằng API, chỉ còn bấm ghim.
Mỗi video: mở trang xem → tìm bình luận của kênh → **⋮ → 固定**.

`8pbdjPxw3ho` · `KmmbwuRHBAg` · `zr9uJbDFaoU` · `BKKyjwd1WBU` · `tsQwDqqreCM` ·
`20xRYX-ra2U` · `jhRgcIiqd_w` · `UzHj5gsqSVY`

## 3. Thẻ (カード) @1:30–2:00 — 7 phút 🔴 KHÔNG CÓ API

Đặt **sau vách 20–30s** và **đúng chỗ mất 60→120s** — đây là thứ chở được nhiều người nhất,
vì ở AVP 15% trên video 14′ thì người xem trung bình rời ở ~**2:06**, **rất ít ai tới được
end screen**.

`Studio → video → 編集 → カード → 動画 → chọn đích → kéo về 1:30–2:00` (~50 giây/video)

| # | video (view) | id | thẻ trỏ tới | vì sao |
|---|---|---|---|---|
| 1 | 10月15日振込 (4.921) | `KmmbwuRHBAg` | `UzHj5gsqSVY` | nam châm RELATED duy nhất đo được |
| 2 | 住民税の紙 (1.462) | `zr9uJbDFaoU` | `S0j16selKvs` | AVP 24,1% |
| 3 | 緑の封筒 (978) | `BKKyjwd1WBU` | `n1eDEoHbEMM` | AVP 19,8%, search-fed |
| 4 | 雇用継続給付 (787) | `tsQwDqqreCM` | `pn9Fi9Bx6_U` | **cố ý** kéo video sai tệp về lõi 年金 |
| 5 | 60歳繰上げ (706) | `20xRYX-ra2U` | `pn9Fi9Bx6_U` | AVP 24,4% |
| 6 | 遺族年金 (569) | `jhRgcIiqd_w` | `pn9Fi9Bx6_U` | cùng chủ đề 遺族 |

## 4. End screen — 7 phút 🔴 KHÔNG CÓ API

`Studio → video → 編集 → 終了画面 → テンプレート「動画1つ+登録」`
🔴 **Phải đổi phần tử video sang ID CỤ THỂ.** Để mặc định 「視聴者に最適な動画」 là **mở lại
feed chung** — đúng cái đang làm hỏng kênh.
🔴 **Phải có phần tử ĐĂNG KÝ** ở cả 7 — sub là nút thắt của YPP, không phải giờ xem.

| # | video | end screen: video | + |
|---|---|---|---|
| 1 | `KmmbwuRHBAg` | `ZbEwsPFCcAA` (AVP 27,5%) | playlist B + đăng ký |
| 2 | `zr9uJbDFaoU` | `ZbEwsPFCcAA` | playlist C + đăng ký |
| 3 | `BKKyjwd1WBU` | `UzHj5gsqSVY` | đăng ký |
| 4 | `tsQwDqqreCM` | `pn9Fi9Bx6_U` | playlist A + đăng ký |
| 5 | `20xRYX-ra2U` | `S0j16selKvs` | playlist A + đăng ký |
| 6 | `jhRgcIiqd_w` | `pn9Fi9Bx6_U` | playlist A + đăng ký |
| 7 | 詐欺 (330) `UzHj5gsqSVY` | `KmmbwuRHBAg` | đăng ký |

Playlist: A `PLSHjlM17Oamc` · B `PLT4QEuxo4MWw` · C `PLZVtF_edAA5s`

## 5. Đọc tay impressions/CTR — 5 phút, **để NGÀY 2026-10-15**

API đã bị Google rút 2 metric này từ 2026-07-30 ⇒ chỉ Studio đọc được.
`Studio → コンテンツ → từng video → リーチ`, đặt **hai** khoảng ngày:
`2026-09-02 → 2026-09-15` và `2026-10-01 → 2026-10-14`.

⚠️ Đây là **biến kiểm soát, không phải mục tiêu**: nó chỉ để phân biệt *"kéo được người đúng
ngách"* với *"YouTube tình cờ phát nhiều impression hơn"*. **Impression tăng ≥50% giữa hai
cửa sổ ⇒ tử số M1 bị nhiễm, chỉ đọc M2.**

---

## Sau khi làm xong

⛔ **ĐỨNG YÊN tới 2026-10-15** — không đổi thêm gì về phân phối, không đổi tiêu đề/thumbnail
của video đang hút view. Đổi thêm một biến là cửa sổ đo mất nghĩa.

Baseline đã chốt hôm nay: `06_VIDEO/_diag/curves_2026-09-15.{txt,json}` ·
kênh **10.685 view · 7 sub · 24 video** · sub/view **0,065%** · RELATED cùng ngách **8/25**.
