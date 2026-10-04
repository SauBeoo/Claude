# youtube-jp-shokutaku — 「60代からの食卓」

> Repo thực thi kênh faceless ăn uống & sức khỏe cho người Nhật 60–80 tuổi. Tri thức/research: `SecondBrain/10_Projects/youtube-jp-shokutaku/`.

## Là gì

Kênh YouTube Nhật **「60代からの食卓」** — voice-over dài **35–40 phút**, giọng kính ngữ mềm mại chậm rãi, persona người dẫn **みのり** (người đồng hành của bữa ăn tuổi sáu mươi). Chủ đề: ăn uống → giữ tự lập, tránh 透析・脳卒中・寝たきり, không thành gánh nặng cho con cái.

**Kênh MỚI, chạy song song với `youtube-jp-health`** (kênh đó 15–30 phút, persona khác, VOICEVOX 青山龍星, skill `script-healthy`). Đừng lẫn 2 kênh:

| | youtube-jp-health | youtube-jp-shokutaku |
|---|---|---|
| Persona | (trung tính) | みのり (có câu chào/kết cố định) |
| Độ dài | 15–30 phút | **35–40 phút** (10.500–12.800 ký tự) |
| Chế độ | viết mới từ formula | **A·REMAKE transcript** + B·viết mới |
| Skill | `script-healthy` | `script-shokutaku` |

## Cấu trúc thư mục

| Đường dẫn | Nội dung |
|---|---|
| `youtube-jp-shokutaku.md` | File này — tổng quan |
| `CLAUDE.md` | Rule riêng project (đọc TRƯỚC khi viết) |
| `03_CONTENT_PLAN.md` | **Hàng đợi chủ đề (user chốt 2026-07-19)** — 5 key theo 4 trụ, script 08–12; chọn đề tài theo file này |
| `01_SOURCES/` | Transcript nguồn để REMAKE (chế độ A) + log đề tài |
| `04_SCRIPTS/<NN>_<slug>.md` | Kịch bản sạch — bản đọc: `<NN>_<slug>_TTS.md` |
| `06_VIDEO/` | Output render (slide, ảnh, thumbnail, mp4) |

## Cách làm 1 video

1. Chọn đề tài theo hàng đợi `03_CONTENT_PLAN.md` (hoặc dán transcript mẫu vào `01_SOURCES/` nếu REMAKE).
2. Gọi skill `script-shokutaku` → chạy 4 bước ngầm, xuất 3 phần (gõ 「つづき」 để nối phần kế) + tiêu đề/thumbnail.
3. Lưu `04_SCRIPTS/<NN>_<slug>.md`, tạo bản `_TTS.md`.
4. Render: skill `video-render` (voice AivisSpeech 0.9–0.95, style photo, phụ đề hộp trắng).

## Nguyên tắc bất di bất dịch

- Persona みのり **KHÔNG tự xưng** 医師・先生・管理栄養士・専門家; cấm cụm 医師が解説・医師警告 ở mọi nơi.
- **Bịa nguồn/số liệu = lỗi nặng nhất.** Nguồn thật giữ nguyên tên (厚労省/学会/久山町研究…); không chắc thì hedge, không gắn tên tổ chức.
- YMYL: cấm 治る/治す; có disclaimer cuối + nhắc かかりつけの先生; cảnh báo điều kiện khi chạm nhóm rủi ro (kali cho người bệnh thận, natto × ワーファリン).
- Ghi thật rồi verify — không báo "đã lưu" khi chưa gọi tool.
