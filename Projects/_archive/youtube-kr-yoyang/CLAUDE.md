# CLAUDE.md — youtube-kr-yoyang

> Rule riêng cho kênh 장기요양·요양원 가족 가이드 (KR, con cái 40–60). Ghi đè/bổ sung CLAUDE.md toàn cục.

## Vault tương ứng

Tri thức/research → `SecondBrain/10_Projects/youtube-kr-yoyang/`. Bằng chứng chọn ngách: `SecondBrain/10_Projects/youtube-niche-research-2026/`.

## Trạng thái project — MỚI LẬP (2026-07-23), CHƯA CHỐT

- **Tên kênh / persona:** CHƯA CHỐT. Định hướng: người đồng hành ấm áp đã "đi trước một bước" trong hành trình lo cho bố mẹ — thấu cảm gánh nặng + cảm giác tội lỗi, KHÔNG giọng công ty bán dịch vụ (kênh công ty trong ngách view 3 chữ số vì khán giả không tin), KHÔNG tự xưng 요양보호사/bác sĩ.
- **Giọng TTS:** CHƯA CHỐT — ứng viên 1: Azure ko-KR-SunHiNeural (nữ ấm, đã có sẵn); test thêm InJoon deep cho vai info. Key env AZURE_SPEECH_KEY, region koreacentral; KHÔNG gọi bằng curl git-bash (hỏng encoding — bài học kr-romfan).
- **Lịch đăng:** CHƯA CHỐT — đo giờ đăng benchmark ngách info-senior KR trước (đừng bê 21:00 KST của audio-drama — tệp và hành vi khác).
- **CTA giữa video:** soạn câu canonical 해요체 ấm khi chốt persona → thêm `.claude/rules/cta-midvideo.md` mục 2.
- **Profile:** `Profile 12` (rebrand từ kr-romfan 사우 오디오, Gmail ladykiller301096). Chưa rebrand.

## ⚠️ RULE BẮT BUỘC — YMYL nhẹ (chế độ + tiền, KHÔNG y tế/pháp lý cụ thể)

1. **Chỉ nói chế độ công khai + tiền:** 노인장기요양보험 các cấp, chi phí, thủ tục. Nguồn số BẮT BUỘC: 국민건강보험공단 (건보공단) / 보건복지부 / 통계청 — rà link trước khi vào script. KHÔNG bịa số/nguồn.
2. **KHÔNG tư vấn y tế** (치매 chẩn đoán/điều trị — chỉ nói THỦ TỤC xin cấp độ, khuyên khám bác sĩ) và **KHÔNG tư vấn pháp lý cá nhân hóa**.
3. **KHÔNG gợi ý lách chế độ** (mẹo khai gian điểm 치매 để lên cấp…) — nói "chuẩn bị đúng và đủ hồ sơ", không dạy gian lận.
4. **Chế độ có hạn dùng:** mỗi video ghi thời điểm thông tin (「◯년 ◯월 기준」); chính sách 장기요양 đổi hằng năm → cuối video khuyên xác nhận với 건보공단.
5. **Không hứa hẹn tuyệt đối**; case gia đình kể trong video = hư cấu 100%, đổi tên/địa danh mỗi script.
6. **Không nêu tên 요양원/công ty thật** khi chê; khen/so sánh dùng tiêu chí chung.

## Kịch bản

- 15–25 phút, tiếng Hàn 해요체 ấm (khác 한다체 của kr-romfan). Khung kế thừa nenkin: case-driven — 1 gia đình hư cấu + con số chạy + phán quyết; cold open loss-aversion (câu 1 = mất mát cụ thể: 「요양원 비용, 준비 없이 가면 월 ◯◯만원…」), giữ căng ~25–30s rồi hé lối thoát; trần YMYL giữ nguyên.
- Tiền LUÔN là 원 (won bản địa). Đo hệ số ký tự hangul/phút bằng demo Azure trước khi lên dàn ý (đừng mượn hệ số VOICEVOX).
- 3 tuyến xen kẽ: ① thủ tục & cấp độ (등급 신청, mẹo hồ sơ đúng luật) ② tiền (chi phí thật từng loại hình, 가족요양 lương, hỗ trợ) ③ tình huống gia đình (chọn viện, anh em chia gánh, cảm giác tội lỗi — tuyến kể chuyện). 2 video liền không cùng tuyến.
- Đóng gói CTR đủ bộ theo `youtube-upload-seo.md` (Trends geo=KR trước title), tag block, ghi vào file script.

## Visual & render

- Ảnh tĩnh + slide diagram tiền (khuôn thang chi phí / bảng so sánh 요양원 vs 요양병원 vs 방문요양); pipeline: voice Azure (tool kr-romfan) + dựng hình `../youtube-jp-health/tools/video_render.py` — pass ghép chữ Hàn kiểm font trước (test 1 slide có hangul + phụ đề trước khi render full).
- BGM -40dB, phụ đề ≤2 dòng. Media qua `_media_library`.

## Lưu file

- Script → `03_SCRIPTS/<số>_<slug>.md`. Voice → `04_VOICE/<slug>/` (theo nếp kr-romfan). Video → `06_VIDEO/<slug>/`. Vòng đời chuẩn upload-schedule.md 1.5.
