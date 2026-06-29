# Quy trình sản xuất 1 video faceless (A→Z)

> Mục tiêu: biến quy trình thành dây chuyền lặp lại → batch nhanh, chất lượng ổn định.
> Một long-form **8–12 phút** faceless: ~4–6h nếu chưa quen, ~2.5–3.5h khi thành thạo.

## Dây chuyền 7 bước

```
1. Ý tưởng + SEO  →  2. Kịch bản  →  3. Lồng tiếng (AI voice)
   →  4. Hình ảnh/B-roll  →  5. Dựng + phụ đề  →  6. Thumbnail  →  7. Đóng gói (title/mô tả/SEO)
```

### Bước 1 — Ý tưởng + SEO
- Lấy từ `04_CONTENT_IDEAS.md`. Mỗi video = **1 bí ẩn/câu hỏi rõ ràng**.
- Dùng **VidIQ** (free) kiểm tra từ khóa: chủ đề có người tìm không? đối thủ làm chưa? → chọn góc còn "đất".
- Viết **hook 3 giây** TRƯỚC kịch bản. Hook = câu khiến KHÔNG lướt được. VD: *"In 1959, nine hikers fled their tent into the snow — barefoot. No one knows why."*

### Bước 2 — Kịch bản (giải bài toán tiếng Anh yếu)
- **Quy trình cố định:** viết ý tưởng/dàn ý bằng **tiếng Việt** → yêu cầu AI (Claude/ChatGPT/Gemini) viết thành **script tiếng Anh giọng kể chuyện hồi hộp** → AI dịch & trau chuốt → đưa vào ElevenLabs đọc.
- KHÔNG viết tiếng Việt rồi dịch word-by-word (lộ văn dịch). Để AI viết thẳng tiếng Anh tự nhiên.
- Cấu trúc giữ chân: **Hook → Đặt vấn đề → Triển khai (3–5 ý, mỗi ý 1 "mini-hook") → Cao trào → Chốt + CTA**.
- Văn nói, câu ngắn. Long-form 8–12 phút ≈ **1.200–1.800 từ**.
- ⚠️ **LUÔN kiểm chứng dữ kiện/số liệu** — AI hay bịa. Sai sự thật trong video bí ẩn = mất uy tín ngay.
- Lưu vào `scripts/[so-thu-tu]-[ten-video].md`.

### Bước 3 — Lồng tiếng (AI voice) ⭐ khoản đầu tư chính
- **Giọng TIẾNG ANH** trên **ElevenLabs** — giọng trầm/bí ẩn hợp niche mystery, gần như không phân biệt được với người thật (free → gói rẻ vài trăm k/tháng). Test nhiều giọng, chốt 1 giọng "nhận diện kênh".
- Mẹo tự nhiên hơn: chèn dấu câu để ngắt nghỉ, dùng tag cảm xúc, nghe lại chỉnh nhấn nhá.
- Xuất file audio → đây là "xương sống" để khớp hình.

### Bước 4 — Hình ảnh / B-roll
- **Nguồn miễn phí an toàn:** Pexels, Pixabay (video/ảnh).
- **AI tạo ảnh** cho cảnh khó kiếm (di tích bí ẩn, cảnh tái hiện): **Leonardo.ai** (free), Bing Image Creator.
- Quy tắc: hình **đổi mỗi 3–5 giây** để giữ nhịp. Faceless tĩnh = người xem ngủ gật.
- Nhạc nền hồi hộp: **YouTube Audio Library** (an toàn 100%), Pixabay Music.
- ⚠️ TUYỆT ĐỐI không lấy clip/ảnh có bản quyền của người khác (3 gậy mất kênh).

### Bước 5 — Dựng + phụ đề
- Công cụ: **CapCut** (free, dễ, auto caption).
- Khớp audio → hình → cắt khoảng lặng → thêm nhạc nền (giảm volume -18 đến -22dB dưới giọng).
- **Phụ đề bám theo lời** (nhiều người xem tắt tiếng) — CapCut auto caption rồi sửa lại.
- Thêm zoom/chuyển cảnh nhẹ + hiệu ứng âm thanh (whoosh) ở điểm nhấn → tăng hồi hộp.
- Xuất **1080p, 30fps, ngang 16:9**.

### Bước 6 — Thumbnail (quyết định 80% lượt click)
- **Canva** (free), 1280×720px. Quy tắc: **1 chủ thể rõ + chữ to 3–5 từ + màu tương phản + khơi tò mò**.
- Niche mystery: dùng tông tối, dấu hỏi, vùng mờ/khoanh đỏ → cảm giác "có gì đó giấu kín". A/B test 2 mẫu nếu được.

### Bước 7 — Đóng gói SEO
- **Tiêu đề (EN):** từ khóa + lời hứa/tò mò. VD: *"The Hikers Who Vanished Without Explanation (Dyatlov Pass)"*.
- **Mô tả:** 2–3 câu đầu tóm tắt (chứa từ khóa) + timestamps + nguồn + CTA + 3–5 hashtag.
- **Playlist** + **end screen** + **card** điều hướng video khác → tăng thời gian xem phiên.

---

## Chiến lược batch (cho quỹ 3–4h/ngày)

Đừng làm tuần tự từng video. **Gom theo bước** (1 sprint ~1 tuần cho 5 long-form):

| Buổi (~3–4h) | Việc |
|---|---|
| Buổi 1 | Brainstorm + viết **5 kịch bản** 1 lượt (tiếng Việt → AI ra tiếng Anh) |
| Buổi 2 | Lồng tiếng **cả 5** trên ElevenLabs + gom hình/b-roll |
| Buổi 3 | Dựng 2 video |
| Buổi 4 | Dựng 2 video |
| Buổi 5 | Dựng nốt 1 + làm 5 thumbnail + đóng gói SEO + lên lịch đăng |

→ 1 "sprint" ~5 buổi cho **5 long-form** → đủ đăng 2–2.5 tuần. Lặp lại.

## Mở rộng SAU (chưa làm 3 tháng đầu)
- Khi đã vững long-form: mỗi long-form chứa 2–4 đoạn "tự đứng được" → cắt thành **Shorts** dọc 9:16, đổi hook đầu, phụ đề to.
- → Từ 5 long-form có thêm 10–15 Shorts gần như miễn phí. **Nhưng chỉ bật khi quy trình long-form đã trơn** (xem roadmap Phase 3).

## Bộ công cụ (starter kit)

| Khâu | Công cụ | Chi phí |
|---|---|---|
| Ý tưởng/SEO | VidIQ | Free |
| Kịch bản | ChatGPT / Gemini / Claude | Free |
| **Voiceover** ⭐ | **ElevenLabs** | Free → vài trăm k/tháng |
| Hình ảnh | Pexels + Pixabay + Leonardo.ai | Free |
| Dựng | CapCut | Free |
| Thumbnail | Canva | Free |
| Nhạc | YouTube Audio Library | Free |
| Lên lịch + phân tích | YouTube Studio | Free |
