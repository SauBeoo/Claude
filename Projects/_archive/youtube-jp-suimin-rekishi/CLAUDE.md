# CLAUDE.md — youtube-jp-suimin-rekishi

> Rule riêng cho kênh 睡眠用・長編歴史朗読 (JP 40–70, nghe trước ngủ). Ghi đè/bổ sung CLAUDE.md toàn cục.

## Vault tương ứng

Tri thức/research → `SecondBrain/10_Projects/youtube-jp-suimin-rekishi/`. Bằng chứng chọn ngách: `SecondBrain/10_Projects/youtube-niche-research-2026/`.

## Trạng thái project — MỚI LẬP (2026-07-23), CHƯA CHỐT

- **Tên kênh / persona / giọng TTS / lịch đăng:** CHƯA CHỐT — chốt sau khi mổ benchmark (ぐっすり眠れる歴史, おやすみ歴史館) + đo Trends. Giọng: VOICEVOX trầm–đều, test độ bền tai 10 phút liên tục; nhịp chậm hơn chuẩn kênh thường (khán giả đang thiu ngủ).
- **CTA giữa video:** ⚠️ KHÔNG dùng khuôn CTA sôi nổi — kênh ngủ phải CTA kiểu thì thầm ngắn ở ranh giới chương; soạn câu canonical riêng khi chốt persona, thêm vào `.claude/rules/cta-midvideo.md` mục 2 (điểm chèn: ranh giới 章 gần 50%, KHÔNG hiệu ứng SFX card ồn ào — cân nhắc `--no-cta` cho overlay và chỉ giữ câu voice).
- **Profile:** `Default` (rebrand từ chouhen, Gmail tuananh96freemail) — kênh có **API full-auto** (`upload_api.py`). Chưa rebrand — làm trước video đầu; giữ nếp compliance vì YouTube có thể re-review.

## ⚠️ RULE SỐNG CÒN — KHIÊN INAUTHENTIC (07/2025, enforce 01/2026)

Kênh này nằm ĐÚNG profile bị quét ("AI voice + nền tĩnh + video dài hàng loạt"). Mọi video BẮT BUỘC đủ 5 khiên:
1. **Kịch bản gốc 100%** viết từ nguồn sử liệu thật; 概要欄 ghi mục 参考文献 (sách/tư liệu đã tham khảo) — vừa là khiên vừa là uy tín.
2. **Visual đổi từng video** — bộ tranh ukiyo-e/ảnh tư liệu riêng qua kho `_media_library` (rule ưu-tiên-chưa-dùng); CẤM nền loop giống nhau hàng loạt (ví dụ bị YouTube nêu đích danh).
3. **目次 chương mục riêng** từng video (cũng là SEO + trải nghiệm ngủ: người nghe tua về chương đang dở).
4. **Engagement device:** giấu シークレットワード ở đâu đó trong video, mời comment — bằng chứng người thật nghe thật (học từ benchmark ぐっすり).
5. **Không đúc template:** xoay khuôn kể (biên niên / một-ngày-của-X / hồ sơ nhân vật / hỏi-đáp dẫn chuyện); 2 video liền không cùng khuôn.

## Nội dung & fact

- Sử liệu phải đúng: số/năm/tên lấy từ nguồn tin được (sách nghiên cứu, bảo tàng, tư liệu công); thuyết chưa chắc → nói rõ 「〜という説があります」. KHÔNG dựng chuyện gán cho nhân vật thật (khác chouhen hư cấu).
- Vùng né: 部落/差別 lịch sử, mô tả gore chi tiết trận mạc/tra tấn (kênh ngủ — không khí êm), tranh cãi chính trị sử hiện đại (靖国, chiến tranh nhìn nhận…). 事件史 làm kiểu hồ sơ xã hội, theo bảng từ mục 3 compliance ở title/thumbnail.
- Cấu trúc chuẩn ngủ: mở 60–90s dặn "nghe rồi ngủ cũng được" (benchmark làm vậy — giảm áp lực xem) → chương 15–25 phút → KHÔNG twist giật mình cuối, năng lượng đi XUỐNG dần về cuối video.

## Kịch bản & TTS

- Script 2–3h ≈ 45.000–50.000 ký tự, chia batch ~5.000 ký tự; số 漢数字 hay Ả Rập chốt khi chốt giọng; đo hệ số ký tự/phút bằng demo thật trước khi lên dàn ý dài.
- TTS 1 giọng nhất quán, nhấn nhá chỉ 速/抑揚/間 ([[feedback_video_no_motion_mot_giong]]); 間 dài hơn chuẩn ở ranh giới chương.

## Visual & render

- Slide tĩnh (KHÔNG motion rung — kênh ngủ càng phải tĩnh), tranh PD (Wikimedia/メトロポリタン/ColBase), tối màu, chữ ít; BGM cực khẽ -40dB hoặc không BGM (test 80s demo trước khi chốt mức).
- Render 3h: bắt buộc chia chunk + resume (playbook `project_co_dai_health_render_resume` + chia đôi pass chouhen); ước lượng dung lượng/thời gian render trước khi chạy.
- CTA overlay hiệu ứng: mặc định TẮT (`--no-cta`) — chờ quyết định câu CTA thì thầm riêng.

## Lưu file

- Script → `03_SCRIPTS/<số>_<slug>.md` (+ `_TTS.md`). Video → `06_VIDEO/<slug>/`. Vòng đời chuẩn upload-schedule.md 1.5; kênh này dùng `upload_api.py` khi rebrand xong.
