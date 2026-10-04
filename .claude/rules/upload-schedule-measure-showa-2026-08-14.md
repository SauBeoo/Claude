# ĐO NGÀY ĐĂNG CỤM 昭和 — 2026-08-14 (bằng chứng lịch showa)

> `Projects/youtube-jp-chouhen/tools/measure_upload_days.py --group showa` — 9 kênh × 50 video, JST, tách shorts (<8′).
> Dữ liệu thô: `Projects/youtube-jp-chouhen/06_VIDEO/_measure/days_out_showa.{txt,json}`. Áp vào `upload-schedule.md` §1.2.

## 1. Kênh được tính
| Kênh | sub | nhịp/tuần | NGÀY long-form | median view/ngày | GIỜ |
|---|---|---|---|---|---|
| **伊東彩のほんのり昭和回顧** ⭐ | 142K | 2,41 | **T3=19 · T7=19 · T5=11**, ngày khác ≈0 | T7 23.928 · T3 21.479 · T5 12.710 | **19:00 khoá 50/50** |
| **なつかし昭和チャンネル** ⭐ | 39,2K | 0,98 | rải T2/T4/T5/T7/CN | **T5 148.622** · T4 144.761 · … · T6 42.208 (bét) | 16:00 |
| 昭和の記憶装置 (tham khảo, mẫu 1102 ngày) | 70,9K | 0,32 | T3/T6 nhiều nhất | T5 178.761 · T6 172.939 · T3 135.621 | 19h=23 · 18h=22 |

Loại khỏi chọn ngày: ボンバイエイ · 残響誌 (rải đều, median phẳng thấp) · 昭和の女 · 存在しない街 · ヤチノ (phần lớn shorts) · THEヤバイ昭和 (ngừng đăng).

## 2. Kết luận NGÀY → **T3 · T5 · T7**
T5 mạnh ở cả 3 kênh (lõi) · T7 median #1 của 伊東彩 · T3 19 video của 伊東彩. Loại T6 (伊東彩 0 video) · T2 (median bét) · T4/CN (伊東彩 0 video). Giãn 2-2-3.

## 3. Kết luận GIỜ → **18:00 JST**
Ngách là 18–19h. Chọn 18 vì 19:00 là giờ của nenkin, trùng ngày T3·T5 → lệch 1h vẫn nằm trong dải đo được (記憶装置 22/50 video đăng 18h).

## 4. Đánh đổi nhịp
Kênh hiệu suất/video cao nhất đăng **≤1/tuần** (記憶装置 0,32 · なつかし 0,98), kênh 3,3/tuần chỉ 630–6.900 view. Vẫn giữ 3/tuần theo nhịp chuẩn user chốt.
🛑 **Phanh:** 5 video đầu median ≤500 view + `BROWSE_FEATURES` = 0 → hạ về 1/tuần T5 18:00; ghi vào `youtube-jp-showa/08_ANALYTICS_LOG.md`.

## 5. Hạn dùng
Đo lại sau 6–8 tuần (cùng lệnh). 伊東彩 là cột chống duy nhất — nó đổi lịch thì §2 đổ. Ngày đăng không chữa được bao bì: trận đánh vẫn là thumbnail + 60s đầu.
