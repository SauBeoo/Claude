# Quy trình sản xuất 1 video faceless (A→Z)

> Mục tiêu: biến quy trình thành dây chuyền lặp lại được → batch nhanh, chất lượng ổn định.
> Một long-form 5–8 phút faceless: ~3–5h nếu chưa quen, ~1.5–2.5h khi thành thạo.

## Dây chuyền 6 bước

```
1. Ý tưởng + Hook  →  2. Kịch bản  →  3. Lồng tiếng (AI voice)
   →  4. Hình ảnh/B-roll  →  5. Dựng + phụ đề  →  6. Đóng gói (thumbnail/title/SEO)
```

### Bước 1 — Ý tưởng + Hook
- Lấy từ `04_CONTENT_IDEAS.md`. Mỗi video = **1 câu hỏi/lời hứa rõ ràng**.
- Viết **hook 3 giây** TRƯỚC kịch bản. Hook = câu khiến người ta KHÔNG lướt được. VD: *"Nếu Mặt Trời biến mất ngay bây giờ, bạn sẽ không biết trong 8 phút..."*

### Bước 2 — Kịch bản
- Cấu trúc giữ chân: **Hook → Đặt vấn đề → Triển khai (3–5 ý, mỗi ý 1 "mini-hook") → Cao trào → Chốt + CTA**.
- **Viết bằng tiếng Anh tự nhiên** — KHÔNG viết tiếng Việt rồi dịch (lộ văn dịch ngay). Để Claude/ChatGPT viết tiếng Anh, bạn rà soát ý + dữ kiện.
- Văn nói, câu ngắn, không hàn lâm. Đọc to lên (hoặc cho AI đọc) — vấp/cấn chỗ nào sửa chỗ đó.
- Long-form: 700–1.200 từ (~5–8 phút). Shorts: 80–150 từ (~30–50s).
- **Claude có thể giúp rất nhiều ở hướng tiếng Anh:** brainstorm chủ đề hợp gu khán giả Tây, viết kịch bản tiếng Anh tự nhiên, đánh bóng hook, gợi ý từ khóa SEO tiếng Anh. Bạn LUÔN biên tập lại + **kiểm chứng dữ kiện** (AI bịa số liệu).
- Lưu vào `scripts/[so-thu-tu]-[ten-video].md`.

### Bước 3 — Lồng tiếng (AI voice)
- **Giọng TIẾNG ANH** (khán giả ngoại). Công cụ: **ElevenLabs** — giọng Anh cực tự nhiên, gần như không phân biệt được với người thật (gói ~$5–22/tháng). Đây là lợi thế lớn nhất của hướng view ngoại. Test nhiều giọng, chọn 1 giọng "nhận diện kênh" (giọng Mỹ trầm ấm hợp kể chuyện khám phá).
- Mẹo tự nhiên hơn: chèn dấu câu để ngắt nghỉ, dùng tag cảm xúc của ElevenLabs, nghe lại và chỉnh chỗ nhấn nhá. Kịch bản viết bằng tiếng Anh tự nhiên (xem Bước 2).
- Xuất file audio → đây là "xương sống" để khớp hình.

### Bước 4 — Hình ảnh / B-roll
- **Nguồn miễn phí an toàn:** Pexels, Pixabay, Videvo (video); Unsplash (ảnh).
- **AI tạo ảnh** cho cảnh khó kiếm: Bing Image Creator, Leonardo, Midjourney.
- Quy tắc: hình **đổi mỗi 3–5 giây** để giữ nhịp. Faceless tĩnh = người xem ngủ gật.
- Lưu nhạc nền: **YouTube Audio Library** (an toàn 100%), Pixabay Music.

### Bước 5 — Dựng + phụ đề
- Công cụ: **CapCut** (miễn phí, dễ, auto caption tiếng Việt) hoặc DaVinci Resolve (free, mạnh hơn).
- Khớp audio → hình → cắt khoảng lặng → thêm nhạc nền (giảm volume -18 đến -22dB dưới giọng).
- **Phụ đề bám theo lời** (rất quan trọng — nhiều người xem tắt tiếng). CapCut auto caption rồi sửa lại.
- Thêm hiệu ứng zoom/chuyển cảnh nhẹ, hiệu ứng âm thanh (whoosh) ở điểm nhấn.
- Xuất 1080p, 30fps. Shorts: dọc 9:16. Long-form: ngang 16:9.

### Bước 6 — Đóng gói (quyết định 80% lượt click)
- **Thumbnail** (chỉ long-form): 1280×720px. Quy tắc: **1 chủ thể rõ + chữ to 3–5 từ + màu tương phản + khơi tò mò**. A/B test 2 mẫu nếu được.
- **Tiêu đề**: chứa từ khóa + lời hứa/tò mò. VD: *"Điều Gì Xảy Ra Nếu Bạn Rơi Vào Hố Đen? (Có Thật)"*.
- **Mô tả**: 2–3 câu đầu tóm tắt (chứa từ khóa) + timestamps + nguồn + CTA + 3–5 hashtag.
- **Playlist** + **thẻ kết thúc (end screen)** + **card** điều hướng video khác → tăng thời gian xem phiên.

---

## Chiến lược batch (cho quỹ 5–15h/tuần)

Đừng làm tuần tự từng video. **Gom theo bước:**

| Buổi | Việc | Thời lượng |
|---|---|---|
| Buổi 1 | Brainstorm + viết **5 kịch bản** 1 lượt | 2–3h |
| Buổi 2 | Lồng tiếng **cả 5** + gom hình/b-roll | 2–3h |
| Buổi 3 | Dựng 2–3 video | 3–4h |
| Buổi 4 | Dựng nốt + làm thumbnail + đóng gói + lên lịch đăng | 2–3h |

→ 1 "sprint" ~10–13h cho **5 long-form** → đủ đăng 2–3 tuần. Lặp lại.

## Tái sử dụng (1 long → nhiều shorts)
- Mỗi long-form chứa 2–4 đoạn "tự đứng được" → cắt thành Shorts dọc.
- Đổi hook đầu cho hợp định dạng dọc, thêm phụ đề to.
- → Từ 5 long-form có thêm 10–15 Shorts gần như miễn phí.

## Bộ công cụ tối thiểu (chi phí thấp)

| Việc | Công cụ | Chi phí |
|---|---|---|
| AI voice | ElevenLabs / Vbee / FPT.AI | ~$5/tháng |
| Dựng video | CapCut / DaVinci Resolve | Free |
| Thumbnail/brand | Canva | Free / Pro |
| Video/ảnh stock | Pexels, Pixabay, Unsplash | Free |
| Nhạc | YouTube Audio Library | Free |
| Kịch bản | Claude / ChatGPT | Pro nếu có |
| Lên lịch + phân tích | YouTube Studio | Free |
