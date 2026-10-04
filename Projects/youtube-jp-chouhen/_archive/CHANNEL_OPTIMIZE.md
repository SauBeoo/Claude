# CHANNEL_OPTIMIZE — 真夜中の朗読便 (chouhen) — Mổ 0-view 2026-07-21

> Nguồn số liệu: YouTube Data/Analytics API (token chouhen readonly, hoạt động tốt) + soi browser đối thủ 2026-07-21.
> File này ghi lại KẾT QUẢ MỔ (bản gốc nằm trong memory phiên 2026-07-21) — các luật rút ra ĐÃ khắc vào `CLAUDE.md` project, skill `script-chouhen`, `.claude/rules/upload-schedule.md`. Cùng khung với shokutaku/health/co-dai (CHANNEL_OPTIMIZE.md của từng project).

## 1. HIỆN TRẠNG LÚC MỔ (2026-07-21)

- **KHÔNG án phạt/suppression:** cả 4 video test đều index #1 khi search đúng title; country=JP đúng.
- **Video 00 (jikyu1350, LEGACY):** video DUY NHẤT từng được phân phối thật — **78 view từ RELATED_VIDEO**, ramp 07-08→07-13 (đỉnh 28 view/ngày) rồi chết đứng 07-14 (token thiếu metric impressions/CTR nên không rõ lý do tắt). **Retention tốt: ~30–35% phẳng suốt 44'** → nội dung không phải vấn đề.
- **Video 01–06: chưa từng được phát impressions** — 1–6 view/video, toàn nguồn YT_CHANNEL. Bệnh = thuật toán không đem đi chào, không phải người xem chê.

## 2. BENCHMARK: 苦しみの物語 (kênh nhỏ đang thắng ngách)

- **1.230 subs / 144 video, ăn 70K–143K view/video** → ngách スカッと朗読 VẪN chia bài cho kênh nhỏ, không phải "hết cửa".
- Playbook của nó (khác chouhen 4 điểm):
  1. **2–3 video/NGÀY** — volume = số lượt thuật toán test.
  2. **26–48 phút/video** (chouhen lúc đó 60–70').
  3. Title **【スカッとする話】TAG ĐỨNG ĐẦU** (chouhen quote-đầu tag-cuối — lệch meta hiện tại của rail).
  4. Thumbnail **TEXT-WALL 4–5 dòng chữ khổng lồ** kể trọn setup (chouhen scene cinematic AI đẹp nhưng lạc meta ở related rail 120px).
- Bài học video 00: được phân phối nhờ **premise-matching** — bản remake truyện jikyu1350 nổi tiếng được đặt cạnh các bản khác trong related rail. Premise proven = cửa vào rail của kênh 0-sub.

## 3. LUẬT ĐÃ KHẮC (đối chiếu nơi ghi)

| Luật rút ra | Nơi ghi | Trạng thái |
|---|---|---|
| Chuẩn video **30–40'** (~9–12k ký), bỏ 60–70' | `CLAUDE.md` project + skill `script-chouhen` | ✅ chốt 2026-07-21 |
| **1 video/NGÀY 18:00 JST** (slots 7 ngày) | `CLAUDE.md` + `.claude/rules/upload-schedule.md` + slots upload_pack | ✅ chốt 2026-07-21 |
| **Ưu tiên chế độ A·REMAKE premise proven-viral** | `CLAUDE.md` project (mục chọn premise) | ✅ chốt 2026-07-21 |
| Title **tag-đầu 【スカッとする話】** | skill `script-chouhen` (format title) | ✅ |
| Thumbnail **text-wall v3 mặc định** (make_thumb_textwall.py), scene AI = dự phòng | `CLAUDE.md` project + skill `thumbnail-chouhen` | ✅ |
| Video 00–06 chuẩn cũ: KHÔNG re-render | `CLAUDE.md` | ✅ |

## 3.5 BENCHMARK ĐO SÂU (API 2026-07-22) — giờ đăng + key chủ đề 苦しみの物語

- **Giờ đăng (14 video gần nhất): slot cố định 07:00 · 09:00 · 12:00 JST — toàn BUỔI SÁNG/TRƯA**, 2–3 video/ngày đều tăm tắp (7h×5, 9h×6, 12h×3). KHÔNG đăng tối — khán giả nữ trung-cao niên nghe スカッと lúc làm việc nhà buổi sáng + nghỉ trưa. Chouhen đang đăng 18:00 JST → **cân nhắc dời/thêm slot sáng 07:00–09:00** (chờ user duyệt).
- View 14 video gần nhất: 1,6K–24K/video trong vài ngày (1,2K sub) — phân phối đều, không phụ thuộc hit.
- **Key chủ đề top view (rổ premise ăn tiền):** ① 義母/義実家 áp bức + giấy ly hôn (144K) ② trẻ con vô tình tố giác ngoại tình của bố/chồng — twist qua miệng 孫/娘 (118K, 24K) ③ chồng bệnh tật/xe lăn mà vẫn phản bội người vợ gánh gia đình (71K, 22K) ④ 仕送り — tiền chu cấp bị vòi/cắt (48K×2) ⑤ con cái du học/thành đạt khinh mẹ (48K) ⑥ thừa kế gia nghiệp bị cướp (6,9K mới đăng). Mẫu số chung: **người phụ nữ trung niên bị chính gia đình phản bội → lật kèo bằng sự thật/tiền/pháp lý**.

## 3.7 BACKFILL TOÀN KÊNH (2026-07-22 — user duyệt, đã áp qua API)

Audit phát hiện tầng KÊNH rỗng (desc/keywords/banner/playlist đều trống — cold-start như co-dai) + video 00–04 metadata nghèo dù gói 概要欄/tags **đã soạn sẵn trong script nhưng chưa từng dán lên YouTube** (upload tay trước khi có upload_pack). Đã vá toàn bộ theo `CHANNEL_BACKFILL_2026-07-22.md`: mô tả kênh + keywords + banner + trailer→video 07 + playlist public + title tag-đầu/desc đầy đủ/tags ~19–25/credit AivisSpeech+BGM cho cả 7 video + upload srt caption cho 02/03. Video 05 (musume-no-sakubun) phát hiện **chưa từng đăng** (nằm nhầm 07_UPLOADED) → đã đóng gói slot 23/07 09:00 JST.

## 4. VIỆC CÒN MỞ

- Token chouhen thiếu metric impressions/CTR → nguyên nhân video 00 "tắt ramp" 07-14 chưa kết luận được; theo dõi khi video mới (07/08 GÓI SẴN) lên sóng theo lịch mỗi ngày.
- Phễu Shorts/TikTok đã HỦY (user 2026-07-21) — không đề xuất lại.
