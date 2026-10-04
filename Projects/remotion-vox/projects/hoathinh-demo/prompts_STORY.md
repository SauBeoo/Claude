# hoathinh-demo — 「Mèo Cam và Ngọn Đèn Bay Mất」 (~80 giây, 12 cảnh)

> Bộ prompt demo phim hoạt hình từ ảnh gen. **Bản dùng để import extension:
> `prompts_FLOW.txt` (mỗi prompt 1 dòng, đúng thứ tự cảnh 1→12).** File này là bản đọc.

## Vì sao ảnh sẽ ĐỒNG NHẤT
Mỗi prompt đều lặp **nguyên văn** 2 khối:
- **STYLE (khoá phong cách):** `hand-painted 2D animation film still, storybook watercolor style, soft brush edges, warm cinematic lighting, gentle film grain`
- **NHÂN VẬT (khoá nhận diện):** `a small chubby orange tabby cat wearing a tiny red scarf, big round amber eyes, short legs`
- Ánh sáng đi theo cung thời gian: hoàng hôn (1–3) → chạng vạng (4–5) → đêm trăng (6–12) — phim có nhịp thời gian thật.
- Đuôi mọi prompt: `no text, no letters, no watermark, 16:9`.

## Bảng cảnh (khớp thứ tự dòng trong FLOW.txt)

| # | Cảnh | Vai trong phim | Tool sẽ dựng |
|---|---|---|---|
| 1 | Toàn cảnh làng ven sông hoàng hôn | Mở màn | pan chậm + title |
| 2 | Mèo ngồi mái ngói ngắm đèn lồng | Giới thiệu nhân vật | zoom nhẹ vào mèo |
| 3 | Gió cuốn đèn bay mất | Biến cố | zoom-punch + SFX whoosh |
| 4 | Mèo phi qua khe hai mái nhà | Rượt đuổi 1 | pan nhanh + beat cut |
| 5 | Chạy xuyên chợ đêm | Rượt đuổi 2 | pan ngược hướng + SFX |
| 6 | Đèn mắc trên cây đa khổng lồ | Chướng ngại | wipe vào, pan từ dưới lên |
| 7 | Cận mặt quyết tâm leo cây | Nút căng | zoom chậm vào mắt |
| 8 | Với tay chạm đèn trên cành mảnh | Đỉnh điểm (slow-mo) | giữ lâu + im lặng nhạc |
| 9 | Cành gãy — rơi ôm đèn | Cú ngã | zoom-punch + SFX drop |
| 10 | Đáp xuống đống rơm | Thở phào | dissolve + SFX boing |
| 11 | Treo đèn lại trước cửa | Giải quyết | pan ấm |
| 12 | Mèo ngủ dưới đèn, trời sao | Kết | zoom out chậm + nhạc kết |

## Cách gen
- **Ảnh** (Flow/gen ảnh): mỗi dòng 1 ảnh, 16:9, cỡ lớn nhất có thể. Gen dư 2 bản/cảnh rồi giữ bản ưng nhất càng tốt.
- **Hoặc clip img2video** (Flow video): dùng đúng prompt làm text, mỗi cảnh 1 clip 4–8s — tool ăn được cả mp4.
- Gen xong **vứt hết vào một folder** (giữ đúng thứ tự tên file 01→12 nếu đặt được tên) rồi đưa đường dẫn — phần còn lại tool lo: quét watermark ✦ cả lô, dựng project (camera move + thoại + SFX + nhạc), render.

## Thoại/intertitle dự kiến (tool đốt vào phim, KHÔNG nằm trong ảnh)
1 「Ngôi làng bên sông, mùa đèn lồng.」 · 3 「Á! Cơn gió!」 · 6 「Cao quá…」 ·
8 「…một chút nữa thôi.」 · 11 「Về chỗ cũ nhé.」 · 12 「Hết.」
