# youtube-jp-nagaiki — 長生きごはんの知恵袋

Kênh YouTube faceless **食べ合わせ・食べ方 cho người Nhật 60–80 tuổi** — kênh brand thứ 2 mở 2026-08-01 thay thế kênh health (みんなの健康ノート) sau khi kênh đó bị đóng vòi phân phối cấp kênh (xem `../youtube-jp-health/CHANNEL_DIAGNOSIS_2026-08-01.md`).

## Thông tin kênh
- **Tên:** 長生きごはんの知恵袋 · **Handle:** @nagaiki-gohan · **Channel ID:** `UCBkpkLFZoj5gl4NzKmOC3zQ`
- **Gmail/Profile:** saubeooo04@gmail.com — Chrome **Profile 13** (chung Gmail với health cũ; Studio mặc định mở kênh cũ → đổi kênh hoặc vào thẳng `studio.youtube.com/channel/UCBkpkLFZoj5gl4NzKmOC3zQ`)
- **categoryId:** 27 Education (đo 2026-08-01: 2 kênh benchmark 5/5 video đều 27)
- **Lịch:** T5 19:00 JST, 1 video/tuần khởi điểm (`upload_pack.py` key `nagaiki`)

## Chiến lược nội dung
- **Công thức lõi:** 食べ合わせ §7 `../youtube-jp-health/BENCHMARK_RIVALS_2026-07-29.md` — 1 món quen rẻ × 「cách ăn phí X%」 × đáp án che; title 【知らないと損/実は逆効果/9割が知らない】; dài 22–27′.
- **Bằng chứng format:** 健康栄養研究室 lập 2026-07-20, 9 ngày = 516 sub / 45K view.
- ⛔ **CHỈ đăng nội dung CHƯA TỪNG public.** Cấm bê video 05–22 của health sang (inauthentic §1). Đạn hợp lệ: video 28 (黒柳徹子, đã render trong health, chưa đăng) + script 23–27 render mới.
- Mọi gate của health áp nguyên: cold open ≤60s (`check_coldopen60.py`), humanize ≥4/6 mũi + 15–25 tag, drawn/genten, thumbnail 45+ (≤3 dòng, dòng chính ≥1/3 khung, mặt biểu cảm).

## Tài liệu project
- **`CLAUDE.md`** — hiến pháp kênh: công thức 食べ合わせ 6 khóa (§1) + 6 sai lầm đã trả giá bằng số (§2) + gate bắt buộc (§3) + pipeline (§4) + tồn kho & thứ tự đăng (§5) + điều kiện tăng nhịp (§6). **Đọc trước khi làm bất cứ gì cho kênh này.**
- `02_BRANDING.md` — avatar/banner (đã lên kênh 2026-08-01) + quy trình xử lý ảnh.
- Tồn kho: script 23/25/27 (làn ĂN) + video 28 đã render — **chuyển từ health sang 2026-08-01**, health chỉ còn giữ 24/26 (làn chết, đóng băng).

## Cách chạy
- Script/video sản xuất trong project này (`04_SCRIPTS`, `06_VIDEO`); tool dùng chung của health: render `python ../youtube-jp-health/tools/video_render.py <TTS> --channel nagaiki` (hồ sơ trong `channels.py` — watermark/palette tạm kế thừa health, chốt lại khi duyệt demo đầu).
- Đóng gói: `python ../youtube-jp-chouhen/tools/upload_pack.py <slug> --channel nagaiki`.
- Token API: `credentials/token.json` — OAuth phải chọn đúng kênh **長生きごはんの知恵袋** (không phải みんなの健康ノート).

## Vault tương ứng
`E:\Claude\SecondBrain\10_Projects\youtube-jp-nagaiki\`
