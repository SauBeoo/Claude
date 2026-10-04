# CLAUDE.md toàn cục

File này đặt ở `~/.claude/CLAUDE.md`, áp dụng cho mọi phiên Claude Code của tôi.

## Về tôi

- Chuyên môn: IT, đang mở rộng sang nghiên cứu, giảng dạy, content
- Ngôn ngữ ưa dùng: **tiếng Việt** (trừ khi đang code/comment)
- Máy: Windows, workspace gốc `E:\Claude\`

## Hệ thống của tôi

```
E:\Claude\
├── SecondBrain\          # Vault Obsidian — bộ não 2
└── Projects\             # Code repos thực thi
```

Cấu hình Claude:
- Toàn cục: `~/.claude/` (file này, agents/, skills/)
- Project: `<project>/.claude/CLAUDE.md` — ghi đè nếu có

## Nguyên tắc khung

1. **Tiếng Việt mặc định**, code/biến/comment kỹ thuật giữ tiếng Anh.
2. **Không tự xóa file** — `rm` chỉ khi tôi yêu cầu rõ.
3. **Không tự commit Git** — chỉ commit khi tôi yêu cầu.
4. **Hỏi trước khi đoán** — khi không chắc, đề xuất 2-3 phương án, không tự quyết.
5. **Đường dẫn tuyệt đối** khi cross-project — tránh confused về cwd.

## Agents có sẵn

Đặt ở `~/.claude/agents/`. Gọi bằng `/agent <tên>`:
`researcher` (paper → atomic notes) · `teacher` (bài giảng, đề thi) · `coder` (review, refactor, test) · `creator` (content, kịch bản) · `librarian` (quản lý vault).

## Skills có sẵn

Đặt ở `~/.claude/skills/`. Claude tự gọi khi phát hiện phù hợp:

- Vault: `vault-routing` · `summarize-pdf-paper` · `create-atomic-note` · `inbox-cleanup` · `find-related-notes` · `tutor`
- YouTube đang chạy:
  - `script-nenkin` — kịch bản kênh 年金と老後のお金研究室 (`Projects/youtube-jp-nenkin`)
  - `script-yawa` — kịch bản kênh 人生哲学の夜話 (`Projects/youtube-jp-yawa`, khuôn `05_SCRIPT_FORMULA.md`)
  - kênh showa 昭和くらし図鑑 (`Projects/youtube-jp-showa`) — **chưa có skill riêng**, viết theo `05_SCRIPT_FORMULA.md` + `CLAUDE.md` của project
  - `video-render` (showa) · `video-vox` · Remotion `remotion-vox` (nenkin, xem `youtube-jp-nenkin/CLAUDE.md` §②)

## YouTube — PHẠM VI HIỆN TẠI (chốt 2026-09-24)

**Chỉ còn 2 kênh đang làm: `nenkin` và `showa`** + ⭐ **`yawa` 人生哲学の夜話** (rebrand kênh chouhen 2026-09-28, đang dựng khung — `Projects/youtube-jp-yawa/CLAUDE.md`) + 🆕 **`kyori` 心の距離の心理学** (tâm lý quan hệ 60+, rebrand từ kênh 古代の秘訣 2026-09-30, Profile 6 — `Projects/youtube-jp-kyori/CLAUDE.md`; kênh 1/3 của bộ tâm lý 60+) + 🆕 **`teinengo` 定年後のこころ研究室** (sau nghỉ hưu, rebrand từ みんなの健康ノート 2026-09-30, Profile 13 — `Projects/youtube-jp-teinengo/CLAUDE.md`; kênh 2/3) + 🆕 **`kinishinai` 他人の目を気にしない心理学** (không bận tâm ánh mắt người khác, rebrand từ 60代からの食卓 2026-09-30, Profile 3 — `Projects/youtube-jp-kinishinai/CLAUDE.md`; kênh 3/3). Mọi kênh khác (chouhen, health, nagaiki, shokutaku, co-dai, kaigo, akiya, kr-romfan, chikei, stickman, retrofuture) **tạm dừng** — rule đã gỡ phần của chúng. Muốn bật lại kênh nào → nói trước, khôi phục từ git history.
⚠️ Vài tool dùng chung vẫn nằm trong folder kênh đã dừng (vd `Projects/youtube-jp-chouhen/tools/upload_pack.py`, `youtube-jp-health/tools/video_render.py` + `channels.py`) — **đừng xoá các folder đó**.

## YouTube — luật dùng chung (đọc file luật, ở đây chỉ là mục lục)

Mọi file ở `.claude/rules/`. Đổi luật → chỉ sửa file đó.

| Việc | File luật | Điểm không được quên |
|---|---|---|
| Tuân thủ policy | `youtube-compliance.md` | Tự quét title/thumbnail/概要欄/tag và **báo trước khi giao**; né 殺/血/死ね/自殺… ở title+thumbnail; ảnh AI realistic trong video → tick altered/synthetic |
| Khán giả 45+ | `audience-45plus.md` | Thumbnail chữ to + gate 168px · phụ đề cháy sẵn `outline` ≥22 · nenkin: `check_motion.py` phải **SACH 5/5**, bỏ clip AI · showa: nhịp riêng §2.0-ter |
| Chất người | `humanize-script-voice.md` | ≥4/6 mũi tiêm · 15–25 tag · **tag chỉ ở đầu dòng, dính liền câu** · render demo 1–2 đoạn trước |
| Ảnh AI / media | `media-library.md` | **Xoá watermark ✦ mọi ảnh AI, cả lô, soi 1:1 cả 4 góc** · không tái dùng asset · entry 0 = chủ thể |
| Sơ đồ `zu` (nenkin) | `stage-zu-layout.md` | `check_zu_layout.py … --probe` phải **SẠCH 13/13** trước render · luật BA KHỐI |
| Gen lại clip AI | `ai-video-regen.md` | «một clip hay một lớp?» · guard CẤM trong 15% đầu prompt · số để font vẽ |
| Máy quay t2v (showa) | `camera-language.md` | §0.5 máy khoá/trôi một bước · chỗ đứng của người · bỏ token `35mm` · `check_cammove.py` |
| Render | `render-background.md` | **Luôn chạy nền** · `.cmd` ASCII + CRLF · đủ asset mới render · resume phải biết asset đã đổi |
| SEO upload | `youtube-upload-seo.md` | Đo Trends gprop=youtube 30 ngày trước · keyword đầu title · 目次 đo từ bản render |
| A/B 3×3 | `ab-3title-3thumb.md` | 3 title + 3 thumbnail; prompt thumbnail kèm text, TEXT ở 15% đầu |
| Suggested-first | `youtube-suggested-growth.md` | Ghi `### HÀNG XÓM MỤC TIÊU` · swipe file · kiểm video DẪN RELATED |
| CTA giữa video | `cta-midvideo.md` | Câu canonical từng kênh ở ~50% |
| Lịch đăng | `upload-schedule.md` | nenkin T3·T5·CN 19:00 · showa T3·T5·T7 18:00 JST · slot là chỗ trống, không phải chỉ tiêu |
| Browser profile | `channel-browser.md` | nenkin `Profile 17` · showa `Profile 15` · cấm login chéo |

## Khi vault và project tương tác

- Code/coding-knowledge → `SecondBrain\20_Areas\coding-practices\`
- Paper liên quan project research → `SecondBrain\10_Projects\<project>\papers\`
- Bài học chung không gắn project → `SecondBrain\20_Areas\` hoặc `30_Resources\`

Mỗi project repo nên có `CLAUDE.md` riêng chỉ rõ vault path tương ứng.

## Đặt tên file tổng quan (folder-note) — graph hygiene

**File tổng quan của một folder/project = tên folder, KHÔNG dùng `README.md`.**
Vd: `Projects/glowup-studio/glowup-studio.md`, `SecondBrain/10_Projects/<x>/<x>.md`.

- Lý do: graph Obsidian lấy nhãn node = tên file → mỗi folder hiện 1 hub có nhãn rõ; tránh loạt chấm "README" trùng nhau.
- `README.md` chỉ giữ ở gốc workspace (`E:\Claude\README.md`) và các template.

**Khi tạo project mới → tạo folder-note ở CẢ hai chỗ:**
1. `Projects/<name>/<name>.md` — tổng quan repo code.
2. `SecondBrain/10_Projects/<name>/<name>.md` — folder note tri thức.
