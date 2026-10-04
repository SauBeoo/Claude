# 真夜中の朗読便 — KHÁM KÊNH + NÂNG NHỊP (2026-07-28)

> Đo bằng YouTube Data API + Analytics API (token chouhen, đã đậu audit) — `tools/analytics_report.py --channel chouhen [--video <id>]`.
> Lý do khám: user thấy kênh "đang được đề xuất" và muốn tạm để 1 video/ngày. **Số xác nhận user đúng về rail**, nhưng nút thắt nằm ở tồn kho.

## 1. RAIL ĐỀ XUẤT ĐÃ MỞ — số chứng minh

| Ngày | Dài | View | Ghi chú |
|---|---|---|---|
| 07-09 | 1h04'43 | 3 | |
| 07-12 | 1h17'10 | 5 | |
| 07-14 | 1h00'28 | 5 | |
| 07-17 | 54'49 | 14 | |
| 07-19 | 1h07'03 | 8 | |
| 07-22 | 51'48 | 12 | |
| 07-23 | 55'31 | 7 | |
| **07-25** | **29'03** | **227** 🔥 | |
| **07-27** | **40'42** | **174** 🔥 | |
| 07-28 | 34'04 | 2 | vừa đăng |

Kênh: **3 sub · 387 view tổng · 11 video**.

### 1.1 Nguồn traffic của video 227 view (07-25, `gyQg-oLCwBc`)

```
RELATED_VIDEO      95 views · 996 phút    ← 98%
NO_LINK_OTHER       1 view
YT_OTHER_PAGE       1 view · 19 phút
```

→ **Không phải search, không phải browse. Đúng là rail đề xuất (suggested).** Đây là lần đầu kênh vào được rail.

### 1.2 Retention video đó — KHỎE

| Mốc | Còn lại |
|---|---|
| 5% (1'27") | 55,7% |
| 10% (2'54") | 41,2% ⚠️ rớt mạnh nhất |
| 25–45% (7'–13') | 34–38% |
| 50% (14'31", vùng CTA) | 36,1% |
| 70% (20'20") | **44,3%** (đỉnh cục bộ) |
| 90% (26'08") | 36,1% |
| 100% (29'03") | 27,8% |

AVD **10'28" / 29'03" = 36,1% AVP**. Đường retention **phẳng 34–44% suốt thân bài**, không tụt dần — đuôi giữ được người.

## 2. VÌ SAO KÊNH NÀY ĐƯỢC TĂNG NHỊP MÀ health/nenkin THÌ KHÔNG

| | chouhen | health | nenkin |
|---|---|---|---|
| Đã được phát chưa | ✅ rail đề xuất mở (95/97 view) | ✅ ~18.600 impressions | ❌ **50 impressions** |
| Retention | ✅ phẳng 34–44% | 🔴 relPerf@60s **0,10–0,14** (đáy 10%) | ❓ chưa đủ mẫu |
| Ngách thưởng volume? | ✅ winner 嫁子 **8,75 video/tuần** · 苦しみ 18,4/tuần | ❌ 若返り 0,25/tuần median 141K | ❌ 完全攻略 0,69/tuần → 132K sub |
| **Kết luận nhịp** | **TĂNG** | **1/tuần** | **1/tuần** |

Nguyên tắc rút ra: **chỉ tăng nhịp khi rail đã mở VÀ retention khỏe VÀ ngách thưởng volume.** Thiếu 1 trong 3 thì thêm video chỉ là thêm mẫu xấu vào điểm trung bình kênh (ca health).

## 3. BIẾN ĐANG ĂN LÀ ĐỘ DÀI ≤40', KHÔNG PHẢI VOLUME

7 video dài **51'–1h17' → 3–14 view**. 2 video **29' và 40' → 227 và 174 view**. Khớp đúng chuẩn kênh đã sửa 2026-07-21 (30–40') và đo ngách 14 ngày (≤32′ view TB 19.585 · >40′ 13.140).

⚠️ **Đây là tương quan trên mẫu nhỏ (2 video), không phải nhân quả đã chứng minh** — 2 video đó cũng mới hơn (được đẩy vào rail lúc rail vừa mở) và premise khác. Nhưng nó cùng chiều với đo ngách nên đủ để hành động.

## 4. NHỊP CHỐT + PHANH (user chốt 2026-07-28)

**5/tuần T2–T6 09:00 JST · TỰ lên 7/tuần khi buffer ≥5 video đã render chờ đăng.**

- ⚙️ Cơ khí: `_chouhen_slots()` trong `tools/upload_pack.py` — đếm folder trong `06_VIDEO` có `.mp4` và chưa `--done`. **Gate là NĂNG LỰC SẢN XUẤT thật**, không phải số video đã đăng (đó là lỗi của hàm `_kaigo_slots()` cũ đã bị xoá: nó càng đăng càng tự tăng nhịp, không liên quan có hàng hay không).
- **Bỏ T7/CN:** đo 50 video/kênh → CN là ngày median view **bét** của 嫁子 (23,7K = nửa T2), T7 bét ở 苦しみ. 2 kênh đối thủ dồn volume vào cuối tuần nhưng đó là chỗ họ **xả hàng**, không phải chỗ khán giả ăn.
- **Giờ 09:00 giữ nguyên.**

### 🛑 NGƯỠNG PHANH — kiểm mỗi tuần, chạm 1 điều là hạ về 3–4/tuần

1. **3 video liên tiếp < 50 view** (mốc: 2 video đang chạy được 174–227).
2. **Retention mốc ~10% thời lượng (≈2'54") tụt dưới 30%** (hiện 41,2%). Rail mở nhờ retention — mất retention là mất rail.
3. Bỏ ≥2 slot/tuần vì hết hàng → nhịp đang vượt năng lực, hạ trước khi chất tụt.
4. Bất kỳ cảnh báo YPP / 「一般的、または繰り返しの多いコンテンツ」.

## 5. ⚠️ RỦI RO PHẢI CANH KHI CHẠY NHỊP CAO

1. 🔴 **TỒN KHO = 0.** 6 video đã đăng · **0 script sẵn sàng · 0 video render chờ đăng · `01_SOURCES` RỖNG** (không có transcript nguồn nào). Nhịp 5/tuần từ kho rỗng = mỗi ngày phải ra 1 script 9–12k ký + 1 lần render + 1 lần duyệt clip bằng mắt.
2. 🔴 **Việc phải làm TRƯỚC tiên: nạp transcript nguồn vào `01_SOURCES`.** Cái ăn 227 view là **bản REMAKE premise proven-viral** (bằng chứng cũ: video duy nhất từng được phân phối là bản remake truyện jikyu1350). Hết nguồn → buộc phải viết mới → mất cửa vào rail.
3. **Giữ 29–40'.** Đừng để nhịp cao làm script tụt xuống 20' hay phình lên 50'.
4. **Policy inauthentic content (07/2025):** 1 video/ngày remake theo khuôn là đúng profile YouTube nhắm. Kênh đã đậu audit API 2026-07-23 nhưng **đó không phải giấy miễn trừ** — giữ luật đổi ≥8/10 yếu tố + rewrite 100% + không đoạn ≥25 ký trùng nguồn.
5. **Duyệt clip đúng chỗ** (`_render_plan.json`, không chỉ clip mới tải) — bài học video 09 phải render lại từ đầu.

## 6. ĐO LẠI

- Sau mỗi video: `analytics_report.py --channel chouhen` (view/like) + `--video <id>` (traffic + retention).
- Câu hỏi mở: 2 video hit có giữ được đà sau 7 ngày, hay 227/174 chỉ là cú test rail một lần? Đọc lại **04/08**.
- Chưa đo được: impressions/CTR (API chouhen cũng không cấp `impressions` — cần Studio profile `Default` của chouhen theo `.claude/rules/channel-browser.md`).
