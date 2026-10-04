# youtube-jp-suimin-rekishi — 睡眠用・長編歴史朗読

> Kênh faceless JP kể **sử Nhật thành truyện dài 2–3 tiếng nghe trước ngủ**: 江戸庶民の暮らし, 昭和史 đời thường, nhân vật, 地方史 — giọng đều, nhịp chậm, chương mục rõ.
> Con bài TỐC ĐỘ của đợt nghiên cứu 2026-07-23 (cửa sổ đang mở, sẽ đông) — bằng chứng: `SecondBrain/10_Projects/youtube-niche-research-2026/youtube-niche-research-2026.md`.

## Vì sao ngách này (số đo API 2026-07-23)

- **Cửa sổ có số đo:** ぐっすり眠れる歴史 lập 2026-03-08 → sau 4,5 tháng: 40.500 subs / 54 video / 5,18M views, đăng 3 ngày/video ~3h, hit 江戸時代 621K. Kênh cùng sóng おやすみ歴史館 (2025-12): 14,5K subs, video 2,5–7,5h đều 12–67K view. Cầu đang vượt cung.
- **Loyalty thói quen:** nghe MỖI ĐÊM — sub để có gì nghe tối nay.
- **Khớp pipeline nhất:** kịch bản dài + TTS + visual tĩnh ukiyo-e/tư liệu PD = đúng bộ máy sẵn có.
- **Tiền:** video 3h mid-roll dày; RPM khối giải thích 150–450円 — ăn bằng watch-time thay đơn giá.

## Khán giả

JP 40–70, nghe trước ngủ + làm việc nhà. Ngách con còn trống: 江戸庶民の暮らし bản dài, 昭和史 đời thường, 地方史, 事件史 kiểu hồ sơ.

## Format

- Video 2–3h, script ~45.000–50.000 ký tự (gấp ~3 chouhen), chia batch; visual tĩnh tranh PD + tư liệu, đổi bộ từng video (kho `_media_library`).
- Render dài: bài chia chunk + resume sẵn có (chouhen/co-dai đã có playbook).

## ⚠️ Rủi ro số 1: inauthentic content 07/2025 (đúng profile "AI voice + nền tĩnh")

Khiên bắt buộc mọi video: kịch bản gốc dẫn NGUỒN SỬ LIỆU trong 概要欄 · visual đổi từng video · chương mục 目次 riêng · engagement device (giấu シークレットワード trong video kéo comment — học từ benchmark) · không đúc template hàng loạt.

## Hạ tầng kênh

- **Chrome profile:** `Default` (rebrand từ chouhen) — Gmail tuananh96freemail. **Đậu API audit → upload full-auto `upload_api.py`** — đúng kênh cần đăng dày khi cửa sổ mở. Rebrand: ẩn video cũ (private), đổi branding, cập nhật browser_profiles.json + CHANNELS/API_CFG.
- Tên kênh / persona / giọng / lịch: **CHƯA CHỐT** — xem CLAUDE.md.

## Trạng thái

- 2026-07-23: lập project. Ưu tiên khởi động ĐẦU TIÊN trong 4 kênh mới (cửa sổ thời gian).

## Next steps

1. Mổ benchmark bằng mắt: ぐっすり眠れる歴史 + おやすみ歴史館 (cấu trúc chương, giờ đăng, title format, categoryId/tag, cách dẫn nguồn, secret word).
2. Đo Trends: 睡眠用 歴史 / 聞き流し 歴史 / 江戸時代 睡眠 / 歴史 朗読 長編.
3. Chốt tên kênh + giọng (VOICEVOX trầm đều — voice test 3h-endurance: nghe 10 phút liên tục không mỏi) + lịch đăng (nghi khung tối trước ngủ — đo giờ benchmark).
4. Script #1: đề tài 江戸庶民の暮らし nhánh chưa ai làm bản dài (hit 621K là bằng chứng đề tài).
