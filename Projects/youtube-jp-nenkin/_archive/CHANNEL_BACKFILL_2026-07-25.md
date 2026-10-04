# CHANNEL BACKFILL — 年金と老後のお金研究室 (2026-07-25)

> Đo + vá qua API (token nenkin). Bối cảnh: kế hoạch nâng cấp kênh 2026-07-25 (content-first, giữ 3 trụ).
> ⚠️ Phát hiện khi đo: **phần lớn backfill ĐÃ live từ trước** (desc kênh 512 ký + keywords 24 cụm + country JP + trailer + cat 27 cả 3 video) — apply khoảng 07-24 nhưng checklist trong `CHANNEL_OPTIMIZE_2026-07-22.md` chưa tick nên tài liệu lệch thực tế. File này = nguồn sự thật mới.

## 0. TRẠNG THÁI ĐO ĐƯỢC (trước khi vá, 2026-07-25 ~19:00 JST)

| Tín hiệu | Trạng thái | Kết luận |
|---|---|---|
| Mô tả kênh | 512 ký, đúng persona 研究室, có 3 hashtag lead | ✅ đã có — chỉ SAI dòng lịch (火曜・木曜の夜) |
| Channel keywords | 24 cụm | ✅ đủ |
| country / trailer | JP / bWl2jE9l8z4 (video 01) | ✅ |
| categoryId | 27 cả 3 video (01/02/04) | ✅ (CHANNEL_OPTIMIZE ghi "22 SAI" đã được vá trước đó) |
| defaultLanguage/audioLanguage | ja/ja cả 3 | ✅ |
| Tags video 01 | 30 tag, đã chuẩn hóa | ✅ gần đủ |
| Tags video 02 / 04 | 23 / 20 tag, THIẾU rổ nhận diện | ❌ → vá hôm nay |
| Hashtag lead video 02 / 04 | topical-only, thiếu 3 hashtag kênh | ❌ → vá hôm nay |
| Playlist | 1 playlist chung 「年金・給付金をわかりやすく」 3 video | GIỮ — chia playlist 3 trụ khi mỗi trụ ≥3 video (luật 2.4: playlist không phải yếu tố thắng) |
| Banner | chưa có | ⏳ để sau (giống health — thấp hơn mọi việc content) |
| Stats | 2 video public · 0 sub · 5 view · video 04 lên 19:00 hôm nay | cold-start, bệnh 1 (0 impressions) |

## 1. BỘ NHẬN DIỆN TẦNG KÊNH ĐÃ CHỐT (luật 2.4 — nguồn sự thật, áp MỌI video từ nay)

### 1a. Rổ 12 tag nhận diện kênh CỐ ĐỊNH (đứng đầu tag list, rồi mới tag riêng video; tổng ~25–35)
```
年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金, 65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金
```

### 1b. 3 hashtag nhận diện kênh CỐ ĐỊNH (đầu dòng hashtag, đặt CUỐI 概要欄; + tối đa 3 hashtag đề tài nối sau)
```
#年金 #老後のお金 #年金と老後のお金研究室
```

### 1c. categoryId chuẩn kênh: **27 Education** (đo benchmark 完全攻略 + 速報)

## 2. ĐÃ VÁ HÔM NAY (2026-07-25, script `nenkin_backfill_v2.py`, verify sạch)

- [x] Desc kênh: dòng lịch 「毎週 火曜・木曜 の夜」 → 「**毎週 月・水・金 の19時**に、新しい「研究」をお届けしています。」 (khớp lịch mới T2·T4·T6 19:00 JST)
- [x] Video 01 (bWl2jE9l8z4): tags 30→32 (bổ sung 給付金/定年後のお金 từ rổ 1a)
- [x] Video 02 (uPlyzkGYfCs): tags 23→28 + hashtag lead → `#年金 #老後のお金 #年金と老後のお金研究室 #繰り下げ受給 #加給年金`
- [x] Video 04 (MfEKhbXdTXY): tags 20→27 + hashtag lead → `#年金 #老後のお金 #年金と老後のお金研究室 #年金生活者支援給付金 #給付金`
- ℹ️ YouTube trả tag theo thứ tự sort riêng — membership đủ là đạt, đừng verify bằng thứ tự.

## 3. CÒN LẠI

- [ ] Banner kênh (gen asset + duyệt riêng — không chặn content)
- [ ] Chia playlist theo 3 trụ khi mỗi trụ có ≥3 video (dự kiến giữa GĐ A, ~video 10)
- [x] ~~cat 27~~ · ~~desc/keywords/trailer~~ · ~~rổ tag/hashtag 3 video~~ — XONG
