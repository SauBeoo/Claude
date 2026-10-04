# remotion-vox

Project dựng video **Vox-style paper-collage** bằng Remotion + Claude Code —
**từ 2026-08-15 nâng thành TOOL DỰNG VIDEO KIỂU CAPCUT**: state = `project.json`
(Zod), 1 composition generic render mọi project, editor web local (timeline
drag/trim + Player + Inspector + undo/redo), importer từ pipeline kênh
(`_TTS.md`/`SLIDES.json`/`channels.py`), karaoke caption từ **mora VOICEVOX**,
template 9 kênh, render nền + cache content-aware, round-trip về `06_VIDEO/`.
Repo code: `E:\Claude\Projects\remotion-vox\` (đọc `remotion-vox.md` trong đó để chạy).
Skill điều khiển: `.claude/skills/vox-collage-video/` (đường ưu tiên mới =
`auto_collage.py` + editor; flow JSX per-video đã lỗi thời).

## Nguồn gốc
- Video: "Chỉ 5 phút - Mình đã tạo Vox-style Video chỉ bằng Claude Code & Remotion"
  (kênh **Non-tech làm AI** — Elly), https://www.youtube.com/watch?v=2-VBgZZfERs
- Skill gốc lấy từ Google Doc trong description; 4 file đi kèm (process_cutout /
  generate_sfx / example-scene / animation-variants) tự viết lại theo spec vì Doc
  chỉ chứa SKILL.md.

## Ý tưởng lõi (đáng nhớ)
- Look Vox = ảnh stock **cắt nền thật** (silhouette + viền sticker trắng) xếp lớp trên
  nền giấy grid, chip tag highlighter + **1 punch-phrase/scene timing theo từ** —
  KHÔNG phải caption bar chạy chữ.
- Ranh giới scene = ranh giới câu của srt/Whisper, không chia đều máy móc.
- Chống flat bằng ĐA DẠNG: entrance animation không lặp 2 scene liên tiếp + rải cả bộ
  11 SFX + idle motion liên tục sau entrance.
- Deliverable mặc định là **Remotion Studio preview**, không render MP4 mỗi vòng lặp.

## Trạng thái
- 2026-08-15 (sáng): skill + project + demo 16.5s (OkuraDemo, audio health 09) chạy xong,
  duyệt 5 frame bằng mắt đạt look.
- 2026-08-15 (tối): nâng cấp CapCut-tool hoàn tất P0–P5 — okura-demo convert sang
  project.json render giống hệt; import thật health 34 (30′, 121 slide, 398 dòng phụ đề,
  2.346 từ karaoke mora); editor verify bằng Chrome; bài học kỹ thuật ghi ở
  `Projects/remotion-vox/remotion-vox.md` §Bài học build.

## Liên hệ
- Khác [[video-vox]] (lớp thẻ annotate ffmpeg cho pipeline kênh YouTube).
