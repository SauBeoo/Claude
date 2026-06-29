# CLAUDE.md — youtube-jp-health

> Rule riêng cho project kênh faceless sức khỏe người già Nhật. Ghi đè/bổ sung CLAUDE.md toàn cục.

## Vault tương ứng

Tri thức/research làm kênh → `SecondBrain/10_Projects/youtube-jp-health/`.

## ⚠️ RULE BẮT BUỘC khi viết kịch bản

**Mọi lần viết kịch bản cho project này PHẢI nương theo skill `script-healthy`** (`~/.claude/skills/script-healthy/SKILL.md`):
- Chạy đủ 4 giai đoạn (bóc công thức → dàn ý → viết từng phần → lọc & xuất bản sạch).
- Tuân thủ NGUYÊN TẮC CỐT LÕI của skill: viết mới 100%, KHÔNG sao chép/paraphrase sát kịch bản tham chiếu; chỉ học CÔNG THỨC.
- Tuân thủ YÊU CẦU VĂN PHONG của skill (câu dài ngắn xen kẽ, giọng tâm tình, chi tiết đời thường...).

## Bổ sung riêng project (chặt hơn skill)

1. **Độ dài mặc định: 15–20 phút** (~5500–6500 ký tự tiếng Nhật giọng chậm). KHÔNG tự giãn 30–40 phút trừ khi user yêu cầu rõ. Xem [[feedback_script_healthy_length]].
2. **YMYL — TUYỆT ĐỐI không bịa nguồn/số:**
   - KHÔNG bịa tên viện/đại học/学会 + số liệu cụ thể (vd「慶應大学病院」「吸収率が半分」). Đây là lỗi nặng nhất của script đối thủ.
   - Claim y khoa luôn làm mềm:「〜と言われています」「〜と考えられています」.
   - Bắt buộc có câu khuyên hỏi bác sĩ ở cuối + lưu ý người dùng thuốc (vd thuốc chống đông).
   - Muốn "uy tín học thuật" → chèn NGUỒN THẬT (厚労省/学会) sau khi rà, đừng để AI bịa. Xem `03_RUI_RO_YMYL.md`.
3. **Nhân vật case study mới mỗi script:** tên + thành phố + tuổi (60–70+) khác nhau, không lặp giữa các script.
4. **Chọn key theo `05_KEY_MATRIX.md`** (bắt chéo món × tạng/chỉ số). Ưu tiên key có breakout query thật.

## Lưu kịch bản

- File script → `04_SCRIPTS/<số>_<tên-món>.md`, đánh số tăng dần.
- Header mỗi file: ngách, format, độ dài, ghi chú công thức + cảnh báo YMYL.
- **Ghi thật rồi verify** (Glob/Read) — không báo "đã lưu" khi chưa gọi tool. Xem [[feedback_khong_bao_lao_da_lam]].

## Cấu trúc tài liệu

| File | Nội dung |
|---|---|
| `youtube-jp-health.md` | Tổng quan project |
| `01_KEYWORD_RESEARCH_NHAT.md` | Nghiên cứu từ khóa Google Trends JP |
| `02_CONTENT_IDEAS.md` | 16 tiêu đề + công thức tiêu đề/hook |
| `03_RUI_RO_YMYL.md` | Phân tích rủi ro YMYL |
| `05_KEY_MATRIX.md` | Ma trận key món × chỉ số + shortlist |
| `04_SCRIPTS/` | Kịch bản hoàn chỉnh |
