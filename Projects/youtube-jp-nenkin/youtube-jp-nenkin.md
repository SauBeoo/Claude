# youtube-jp-nenkin — 年金と老後のお金研究室 (JP 50–70)

> Folder-note tổng quan project. Tạo 2026-07-19. Vault tri thức: `SecondBrain/10_Projects/youtube-jp-nenkin/`.
> **Tên kênh CHỐT (user, 2026-07-19): 「年金と老後のお金研究室」.**
> Trạng thái: **SETUP — còn chờ chốt persona + giọng TTS (Mục 3).**

## 1. Vì sao ngách này (data thật, đo 2026-07-19)

- **Nỗi bất an #1 của 50–60代 Nhật** = tiền tuổi già (65%+ lo thiếu; 60代 91,4% nói tiết kiệm không đủ).
- **Volume search khổng lồ:** 年金 = 73 điểm trên thang 卵=78 — gần bằng từ khóa lớn nhất từng đo, gấp ~2,8 lần trụ 血圧 của kênh health. Chi tiết: `01_KEYWORD_RESEARCH.md`.
- **Lỗ hổng danh mục:** 6 kênh hiện có (health, shokutaku, chouhen, co-dai, kr-romfan, stickman) chưa kênh nào đụng tiền hưu.
- **Không mùa vụ**, nhịp theo tin chính sách (改正/給付金) → luôn có chuyện để nói, evergreen + timely trộn được.

## 2. Concept kênh

- **Khán giả:** JP 50–70, sắp/đang nhận 年金, lo "mình nhận được bao nhiêu, đủ sống không, luật đổi gì".
- **Format:** faceless, voice + slide/diagram (tái dùng nguyên pipeline `video-render` của health), 15–25 phút.
- **2 tuyến nội dung (trộn 2:1):**
  1. **Giải thích chế độ** (kiểu 完全攻略): 改正 2026, 給付金, いくらもらえる simulation theo case tuổi/nghề — số liệu từ nguồn THẬT (日本年金機構, 厚労省, 総務省家計調査).
  2. **Story hóa đời sống 年金生活** (kiểu 朗読 nhẹ): case hư cấu "vợ chồng 65 tuổi sống bằng 22万円/tháng" — mượn kỹ thuật kể chuyện chouhen, disclaimer hư cấu.
- **Trụ nội dung theo data** (`01_KEYWORD_RESEARCH.md` mục 2):
  A. 改正・給付金 nóng (在職老齢年金 2026 +2.650%) · B. いくらもらえる evergreen (+90–130%) · C. 繰り下げ/繰り上げ chiến lược · D. 平均貯蓄額/生活費 so sánh (breakout) · E. cảnh báo lừa đảo 年金 (breakout) · F. 遺族年金/thừa kế.

## 3. Trạng thái chốt

1. ✅ **Tên kênh (user chốt 2026-07-19):** 「年金と老後のお金研究室」 — keyword 年金 nằm thẳng trong tên.
2. ✅ **Lịch đăng (chốt 2026-07-19, đã ghi vào `.claude/rules/upload-schedule.md`):** **T2 + T4, 16:00–17:00 JST (14:00–15:00 VN)** — peak senior 19–20時台 (総務省) trừ 3h, weekday trống so với 6 kênh kia. **⭐ Rule riêng 支給日:** video 給付金/年金生活/いくらもらえる đăng **1–3 ngày TRƯỚC ngày 15 tháng chẵn** (lương hưu về tài khoản 15 các tháng 2·4·6·8·10·12, rơi cuối tuần dời lên trước — 2026: 13/02, 15/04, 15/06, 14/08, 15/10, 15/12), đè lịch thường nếu trùng. Nguồn: 日本年金機構.
3. ✅ **Persona + giọng (user chốt 2026-07-19):** nghiên cứu viên điềm đạm 研究室, mở bài bằng case đời thường, không xưng FP. Giọng **VOICEVOX 雀松朱司/ノーマル (52)/0.9** — demo duyệt: `00_VOICE_TEST/demo_52_suzumatsu-akashi_normal.wav`. CTA canonical: `cta-midvideo.md` mục 2.4b.
4. ✅ **Script #1 (2026-07-19):** `03_SCRIPTS/01_zaishoku-rorei-nenkin-kaisei-2026.md` — 在職老齢年金 2026年4月改正 (51万→65万円), fact verify 厚労省, gói CTR đủ.
5. ⏳ Còn lại: render video #1 (pipeline video_render.py health, cần SLIDES.json) · entry `CHANNELS` upload_pack.py + `API_CFG` upload_api.py khi lên sóng.

## 4. ⚠️ Compliance riêng ngách tiền (YMYL tài chính — nghiêm như y tế)

- **KHÔNG tư vấn đầu tư/sản phẩm cụ thể** (mua cổ phiếu X, quỹ Y) — chỉ giải thích CHẾ ĐỘ công khai + con số trung bình có nguồn.
- **KHÔNG hứa hẹn kết quả** (「必ず得する」 cấm) — dùng 「〜の場合が多い」「制度上は〜」.
- **Số liệu = nguồn thật, ghi năm:** 日本年金機構 / 厚労省 / 総務省家計調査. Chế độ đổi liên tục → mỗi video ghi 「2026年◯月時点の情報です」 + câu khuyên xác nhận tại 年金事務所/chuyên gia.
- **Không đảng phái:** né hẳn tên chính trị gia/đảng (loại noise 石破給付金 ngay từ keyword).
- Story hóa → disclaimer フィクション như chouhen. Quét từ nhạy title/thumbnail theo `.claude/rules/youtube-compliance.md` như mọi kênh.

## 5. Cấu trúc tài liệu (sẽ mọc dần)

| File | Nội dung |
|---|---|
| `youtube-jp-nenkin.md` | Folder-note này |
| `01_KEYWORD_RESEARCH.md` | ✅ Trend JP đo 2026-07-19 (2 rổ + breakout + đối thủ) |
| `02_CONTENT_IDEAS.md` | (chưa) — danh sách tiêu đề đầu tay từ breakout |
| `CLAUDE.md` | ✅ Rule riêng project |
| `03_SCRIPTS/` | (chưa) — kịch bản |
