# CHANNEL BACKFILL — 60代からの食卓 (2026-07-22)

> Audit API (token shokutaku, force-ssl) + benchmark ngách **長生きの秘訣** (cùng ngách health, đã đo). Áp luật MỚI `youtube-upload-seo.md mục 2.4` (bộ nhận diện metadata tầng kênh) — health làm xong hôm nay, shokutaku CHƯA.
> ⚠️ Chỉ ghi lên kênh SAU khi user duyệt.

## 0. ĐO SO BENCHMARK

| Tín hiệu | shokutaku hiện tại | Kết luận |
|---|---|---|
| **Mô tả kênh** | **TRỐNG (0 ký)** ❌ | Lỗ cold-start #1 (giống health) |
| Channel keywords | 3 cụm (quoted) ❌ | Nâng 24 cụm |
| **Banner** | KHÔNG ❌ | gen + duyệt sau |
| Trailer | ゆで卵 (mQev) — **video 0 tag, yếu** | → đổi 腎臓 (BKh, khung cảnh báo, desc 1358, retention 96% trong rổ đúng) |
| categoryId | **22** cả 7 ✓ | GIỮ (đúng benchmark, KHÔNG theo cat 27 co-dai) |
| audioLang / country | ja / JP ✓ | OK |
| Playlist | 1 public | đủ, thêm sau |
| **Rổ tag nhận diện kênh** | ❌ không có | Lỗ 2.4 #2 |
| **Số tag/video** | **納豆 4, ゆで卵 0** ❌❌ · còn lại 11–22 | 2 video hỏng nặng |
| **3 hashtag cố định** | ❌ mỗi video 1 kiểu | Lỗ 2.4 #3 |

납두 (natto BL7K) có block 26 tag NẰM SẴN trong script — chỉ chưa dán. ゆで卵 (mQev) không có script → dựng tag đề tài từ title.

## A. TẦNG KÊNH
- **Mô tả kênh (A1):** 496 ký, giọng persona みのり (chào → cho ai → học được gì → lịch 日火木土 → CTA like/share → disclaimer「わたしは医師ではありません」giữ ranh giới YMYL). Nội dung đầy đủ trong `scratchpad/shokutaku_apply.py`.
- **Keywords (A2):** 3→24 cụm (thêm 60代からの食卓/みのり/血圧/血糖値/腎臓/食べてはいけない/和食…).
- **Banner (A3):** chưa có asset → gen + duyệt riêng sau.
- **Trailer:** ゆで卵(0 tag) → 腎臓 BKh-sdhsNUg.

## B. NHẬN DIỆN TẦNG KÊNH (áp mọi video)
- **Rổ 12 tag cố định (prepend):** 60代からの食卓, シニア 健康, 60代 食事, 高齢者 食事, 高齢者 栄養, 健康長寿, 健康寿命, シニアライフ, 食生活 改善, 生活習慣病 予防, **食べてはいけない, 60代 食べてはいけない** (2 tag cuối = bắc cầu rổ CẢNH BÁO thắng, theo chẩn đoán mục 1a).
- **3 hashtag cố định lead:** `#60代からの食卓 #シニア健康 #健康長寿`

## C. VÁ TAG 7 VIDEO (basket + đề tài, dedup) — dry-run OK
納豆 4→30 · ゆで卵 0→26 · あずき 18→27 · トマト 21→30 · 牛乳 22→30 · 腎臓 18→26 · ブルーベリー 11→22. Chi tiết tag/hashtag từng video trong `scratchpad/shokutaku_apply.py`.

## TRẠNG THÁI
- [x] User duyệt (2026-07-22, "Ghi tất cả qua API")
- [x] Apply API 2026-07-22 — TẤT CẢ OK + verify sạch: desc 0→496 + keywords 3→24 + trailer ゆで卵→腎臓(BKh) + tag 7 video (納豆 4→30, ゆで卵 0→26, あずき 18→27, トマト 21→30, 牛乳 22→30, 腎臓 18→26, ブルーベリー 11→22) + 3 hashtag nhận diện lead cả 7. categoryId GIỮ 22.
- [ ] Banner (sau)
- [x] Verify — sạch

## Đòn bẩy tiếp (ngoài backfill, đã ghi CHANNEL_OPTIMIZE.md — không lặp)
Backfill chỉ vá phân loại. Bệnh thật shokutaku = **CTR 1,7% (thumbnail v5 đã render, chờ swap) + title lệch rổ 良い→cảnh báo (mục 1b) + payoff #1 ≤4' + volume 4/tuần**. Title steering (mục 1b) là editorial, cần duyệt riêng — chưa làm ở pass này.
