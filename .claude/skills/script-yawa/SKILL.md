---
name: script-yawa
description: Engine biên kịch kênh 人生哲学の夜話 (yawa, JP 50–70). Khuôn LIỆT KÊ 語りかけ型 — nói thẳng với あなた suốt bài, その一…その七, người quen làm ví dụ, câu 古典 thật có nguồn, câu chuyện chốt ở cuối. Dùng mỗi khi viết/sửa kịch bản cho youtube-jp-yawa, hoặc khi nhắc tới script 人生の話, 60代 手放す/後悔/孤独/人間関係 video. Quy trình 6 giai đoạn: chọn đề từ bảng đo → 古典ソース FIRST → người quen + dàn ý 4 nhịp/mục → viết → gate → gói CTR.
---

# script-yawa

Engine viết kịch bản cho kênh **人生哲学の夜話**. **Nguồn sự thật của khuôn = `Projects/youtube-jp-yawa/05_SCRIPT_FORMULA.md` (v3, khuôn liệt kê)** — skill này lo QUY TRÌNH; khuôn đổi thì sửa file đó, đừng chép số vào đây.
Bản mẫu thi hành: `Projects/youtube-jp-yawa/03_SCRIPTS/01_danshari-kokoro_TTS.md` (v6). Bằng chứng: `01_SOURCES/HOT_FORMULA_2026-09-29.md`.

## VAI TRÒ
Người kể **vô danh**, điềm đạm, **nói thẳng với 「あなた」 từ đầu tới cuối**, với người 60–70 tuổi đang nằm trước khi ngủ hoặc làm việc nhà. Không xưng thầy/chuyên gia/僧侶, không giảng đạo. Không có nhân vật chính; chỉ có **một người quen** (「私の知人の、七十代の女性は…」) làm ví dụ xuyên bài.
⛔ Đừng quay lại khuôn truyện xuyên bài (v4 bài 1) — user đã bác: *"tao muốn liệt kê như kịch bản [mẫu]"*.

## GIAI ĐOẠN 0 — CHỌN ĐỀ
1. Mở `01_SOURCES/HOT_FORMULA_*.md` + `TOPICS_*.md` + `01_SWIPE_TITLES.md` (nếu có) mới nhất **trước khi sáng tác**. Ưu tiên đề **đau XÃ HỘI** (bị xa lánh · cô đơn cạnh người thân · mất vai trò sau 定年 · bị coi thường).
2. ⛔ Từ chối đề sức khoẻ/ăn uống/thuốc (YMYL) và đề cần số chế độ tiền (→ nenkin).
3. Đo Trends gprop=youtube 30 ngày (skill `trend-keywords`). Ghi bảng điểm vào header script.
4. Ghi `### HÀNG XÓM MỤC TIÊU` (1–3 video thắng ≤30 ngày).

## GIAI ĐOẠN 1 — 古典ソース FIRST
Chọn **1 câu chủ lực** (cho câu chuyện chốt) + 1–2 câu phụ (mục 3, mục 7) từ 青空文庫/Wikisource. Mở trang nguồn thật, chép nguyên văn + đoạn + link + bản dịch có nguồn vào bảng `### 古典ソース`. Không kiểm được = không dùng. ⛔ Câu gán cho ブッダ/偉人 trên web.

## GIAI ĐOẠN 2 — NGƯỜI QUEN + DÀN Ý
1. **Người quen** (hư cấu): tuổi 65–75, nghề cũ, một chi tiết đời (sống với ai), **một câu cửa miệng**. Xuất hiện ở ≥3 mục (mỗi lần 1 câu thoại + việc bà/ông đã làm thử) và là nhân vật **câu chuyện chốt**.
2. **Câu chuyện chốt:** một cú trả lời đã hứa ở đoạn mở (bài 1: lá thư chồng giấu trong túi giấy) + nối với câu 古典 chủ lực — hai lời nói cùng một điều.
3. **N mục** (5/7): mỗi mục = tên hành động + **bối cảnh vật khác nhau** + 4 nhịp (mô tả · vì sao/gỡ tội · góc khác · làm ngay) + 1 câu あなた (mỗi mục một kiểu). **Mục mạnh nhất để cuối** và trêu nó ở đoạn mở.
4. **Sổ chống khuôn:** ghi vào header điều bài này KHÁC 3 bài gần nhất (đề · người quen · kiểu khoảnh khắc mở · câu 古典).

## GIAI ĐOẠN 3 — VIẾT
Theo §2–§4 của `05_SCRIPT_FORMULA.md` (mẫu 70s ở §2.1). Nhắc nhanh:
- ① **mặc định = biến thể NỖI SỢ (§2.2):** khoảnh khắc có GIỜ/TIẾNG → nỗi sợ thật (làm phiền con · cô độc · bị coi thường) → do dự → 「心当たり」 ≤0:45. ⛔ tên/tuổi, câu khái quát, 「こんにちは」, doạ bệnh/số bịa.
- Mỗi mục = một 「迷い」, thêm nhịp [SỢ] và [LỢI ÍCH]. 風水 ≤3 chỗ, chỉ dạng 「〜と言われています」, không hứa kết quả (§2.3). Kết trả nỗi sợ ở đầu.
- ② **GỠ TỘI** trước 0:55 (biến thể nỗi sợ) / 0:40 (không nỗi sợ). ③ đảo nghĩa + hứa N + **giấu mục mạnh nhất** + **hứa câu chuyện chốt** + câu mời. Đoạn mở ≤70s.
- ④ cầu vào (vì sao cách thông thường thất bại). **Mục 1 ≤2:00.**
- ⑤ その一…: 4 nhịp/mục. ⑥ câu chuyện chốt + 古典 chủ lực, một chỗ bật cười trước đỉnh. ⑦ tóm + hỏi comment móc vào ① (kèm ví dụ) + xin sub + câu chúc.

## GIAI ĐOẠN 4 — GATE (chạy hết, báo kết quả, không tự bỏ gate)
- 9 gate §9 của `05_SCRIPT_FORMULA.md`.
- In mốc giây từng dòng của 70s đầu (ký cộng dồn ÷ 285 × 60) và mốc từng 「その◯」.
- 2 gate tag của `humanize-script-voice.md` §2.1 = 0 dòng.
- Chấm theo bảng so công thức ở `HOT_FORMULA_*.md` §3, báo điểm + chỗ thiếu; nói rõ điểm là phán đoán.
- Render demo 1–2 đoạn (70s đầu + câu chuyện chốt) trước khi render cả bài.

## GIAI ĐOẠN 5 — XUẤT + GÓI CTR
- Ra: `03_SCRIPTS/<NN>_<slug>.md` (header: bảng Trends · HÀNG XÓM MỤC TIÊU · 古典ソース · sổ chống khuôn · số ký/ước thời lượng · bảng mũi tiêm · gate) + `<NN>_<slug>_TTS.md`.
- Gói CTR đúng format `upload_pack.py`: `### Title CHỐT` (fence) · `### 3 TITLE A/B` · `### Tên file upload` · `### 3 dòng đầu 概要欄` · `### 概要欄 — 本文` (目次 viết SAU render · 「本作品はシニア世代をテーマにした創作物語です」 · 引用 古典 · credit `AivisSpeech：morioki`) · `### タグ` 15–40 · `### ハッシュタグ`.
- Prompt thumbnail 3 bản theo `ab-3title-3thumb.md` §3.1 → `06_VIDEO/<slug>/thumb_prompts_*.txt`.
- Quét compliance title/thumbnail/概要欄 và **báo trước khi giao**.

## CẤM
Funnel LINE/quà tặng · CTA giữa bài · hứa tuyệt đối · slideshow đọc danh ngôn · câu Phật/偉人 không nguồn · chép câu của kênh khác · tên người/công ty thật · đổi giọng giữa bài · tag đứng một dòng riêng.
