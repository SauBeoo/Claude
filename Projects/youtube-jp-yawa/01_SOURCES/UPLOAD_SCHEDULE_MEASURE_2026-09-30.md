# Đo giờ/ngày đăng — 8 kênh ngách 人生/60代 (2026-09-30)

> API, 50 long-form (≥8′) gần nhất/kênh, bỏ video <3 ngày tuổi, giờ JST. Dữ liệu thô: `_schedule/raw_2026-09-30.json`.
> "Hiệu suất" = view/ngày của video ÷ trung vị view/ngày của chính kênh đó (để kênh lớn không lấn kênh nhỏ).

## 1. Giờ họ chọn
| kênh | giờ |
|---|---|
| シニアの人生寄り添い物語 (39,5K) | **18:00** (50/50) |
| 人間のトリビア (280K) | **18:00** (50/50) |
| 老後の物語 (30,7K) | **18:00** (41/50) |
| ユウリの優しい心理学 | **18:00** (30/35) |
| 心理のコトノハ | **18:05** (13/19) |
| 心がほっとする人生学 · シニアの整え知恵 | **19:00–19:40** |
⇒ Ngách chốt **18:00 JST** (6/8 kênh). Hiệu suất theo giờ: 18h ×0,95 (n=193) · 19h ×1,00 (n=77) — **không khác nhau**, giờ không phải đòn bẩy.

## 2. Ngày
| | 月 | 火 | 水 | 木 | 金 | 土 | 日 |
|---|---|---|---|---|---|---|---|
| số video (8 kênh) | 51 | 33 | 50 | 35 | 42 | 46 | 32 |
| hiệu suất (×trung vị kênh) | 1,04 | 0,88 | **2,01** | 0,62 | **1,77** | 0,86 | 0,71 |
- 2 kênh lớn nhất (寄り添い · トリビア) đều dồn **月・水・土** (+金).
- ⚠️ Hiệu suất tính bằng view/ngày nên bị lệch theo tuổi video; n mỗi ngày 32–51 ⇒ đọc là **xu hướng**, không phải định luật.

## 3. Đề xuất cho yawa
**T4 (水) · T6 (金) 18:00 JST = 16:00 giờ VN** — 2 video/tuần (đúng nhịp khởi điểm 1–2/tuần của `CLAUDE.md`).
- Hai ngày hiệu suất cao nhất bảng; giờ số đông ngách chọn.
- **Không trùng ngày+giờ** với showa (T3·T5·T7 18:00) và nenkin (T3·T5·CN 19:00).
- Muốn 3/tuần: thêm **T2 (月) 18:00** (×1,04, ngày đăng nhiều nhất).
- Đo lại sau 6–8 tuần, hoặc khi kênh đủ 10–20 video thì Studio Analytics đè bảng này.

## 4. ✅ User chốt (2026-09-30)
**T2 · T4 · T6, 18:15 JST (16:15 VN), 3 video/tuần** — lùi 15′ sau giờ đối thủ. Đã cập nhật `upload_pack.py` + `upload-schedule.md` + dashboard.
