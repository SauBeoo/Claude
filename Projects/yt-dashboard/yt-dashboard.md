# yt-dashboard

Web dashboard **local** quản lý pipeline YouTube đa kênh — lớp vỏ UI cho bộ engine CLI (`upload_pack` / `pipeline_status` / `analytics_report`). Tạo 2026-07-19.

## Chạy

```
double-click run_dashboard.cmd        # hoặc: python dashboard.py
→ tự mở http://127.0.0.1:8765
```
Cần: `pip install flask` (1 lần). Chỉ bind localhost — không lo bảo mật.

## Làm được gì

- **Tab 📋 Dự án (2026-07-23, tab mặc định):** bảng quản lý danh mục kênh cho giai đoạn **pivot ngách** — cả kênh đang chạy lẫn kênh đang rebrand/lên kế hoạch, độc lập với CHANNELS (kênh mới chưa cấu hình sản xuất vẫn theo dõi được). Nguồn sự thật `projects.json`.
  - **Trạng thái hoạt động/không (bán tự động):** mỗi card có dropdown 🟢 Hoạt động / 🟡 Đang rebrand / ⚪ Lên kế hoạch / ⏸ Tạm dừng — đổi là lưu ngay vào `projects.json`; card viền màu + sắp xếp theo trạng thái rồi đợt khởi động.
  - **Update TỰ ĐỘNG (dò realtime):** nút 🔄 + mỗi lần mở tab tự dò từ hệ thống → chip `🌐 profile Chrome tồn tại? · 🔑 token API · 📄 N script · 🎬 N video · 📤 N đã đăng` (đếm thật trong `0N_SCRIPTS`/`0N_VIDEO`/`07_UPLOADED`, đọc `credentials/token.json`, check profile trong Chrome User Data + gmail login lệch mapping). Endpoint `/api/projects`.
  - **Checklist chuẩn bị:** mục ⚙ tự tick khi hệ thống phát hiện (vd có script #1 → tick `script1`); mục còn lại (benchmark/trends/identity/rebrand) tick tay, lưu `done_ticks` trong `projects.json`. Thanh tiến độ N/N.
  - **Đặt lịch đăng ngay trong card (2026-07-23):** kênh MỚI (ngoài CHANNELS) → chọn thứ trong tuần + 1 giờ cố định (giờ thị trường JST/KST) → lưu `projects.json`, hiện khung **🆕 "dự kiến"** trên tab Lịch đăng (chưa có video). Kênh TRONG CHANNELS (health/nenkin + 4 kênh cũ) → lịch **đọc-chỉ** (theo rule upload-schedule.md + CHANNELS, đã hiện sẵn trên lịch) để tránh 2 nguồn sự thật đá nhau. Endpoint `/api/project_schedule`.
  - **Cả kênh CŨ (2026-07-23):** bảng gồm 12 mục — 4 kênh mới rebrand + 4 kênh gốc (chouhen/shokutaku/co-dai/kr-romfan, cùng profile với kênh mới trong lúc chuyển tiếp) + nenkin/health giữ + kaigo (nằm chờ) + stickman (tạm dừng). Đổi status 1 kênh TRONG CHANNELS sang ⏸ paused **tự đồng bộ** `channels_state.json` → tắt kênh khỏi lịch/scan (bật lại khi status ≠ paused).
  - **Bán tự động khác:** nút 📂 Repo (mở folder repo), ▶ Studio (mở Chrome đúng profile_dir kênh — dùng profile_dir trực tiếp vì key project mới ≠ key mapping cũ), 🗑 gỡ khỏi bảng (không đụng file thật), form ➕ thêm dự án mới (checklist chuẩn bị mặc định). Endpoint `/api/project_set` · `/api/project_add` · `/api/project_del` · `/api/proj_open`.
- **Tab Tổng quan:** trạng thái mọi kênh (script → render → gói → đã đăng), badge màu, slot 7 ngày tới + đề xuất video↔slot; nút theo giai đoạn: 📦 Đóng gói · 📋 Upload · 📂 mở folder · ✓ Đã đăng (chuyển kho).
  - **Bật/tắt kênh (2026-07-19):** nút 💤 trên đầu mỗi kênh = tắt kênh ngưng hoạt động → ẩn khỏi danh sách, lịch đăng, select analytics/job (không scan luôn — nhẹ hơn); kênh tắt gom vào ô "💤 Kênh đang tắt" cuối trang, bấm ▶ bật lại. State ở `channels_state.json` (dashboard-side, KHÔNG đụng engine — CLI pipeline_status vẫn thấy đủ 6 kênh, data không mất gì).
- **Tab 📅 Lịch đăng (2026-07-19):** lịch 7 ngày GỘP cả 6 kênh theo từng ngày, quy hết về **giờ VN (giờ bấm nút)** kèm giờ địa phương, ghép video trong queue vào từng slot (GÓI SẴN trước, RENDER ✓ sau — RENDER ✓ gắn nhãn "chưa gói!"), **slot chưa có video → cảnh báo đỏ** nhìn phát biết tuần này thiếu hàng ở đâu. Nguồn slot = `CHANNELS[key]["slots"]` trong upload_pack.py (rule `upload-schedule.md` Mục 1) — endpoint `/api/schedule`.
  - **Đổi tay được:** dropdown từng slot ghim video khác / để trống (📌, lưu `schedule_overrides.json` — chỉ đổi ghép hiển thị, slot khác tự dồn, ghim ngày qua tự dọn); nút **📦⏰** = gói lại video đó với `--slot` đúng giờ slot → **chốt giờ hẹn thật vào METADATA.txt**. Đổi lịch cố định hàng tuần → sửa rule + `CHANNELS` (web tự theo, không có bảng chép tay thứ 2).
  - **🤖 AI nghiên cứu giờ vàng (2026-07-19):** nút trên tab Lịch (theo kênh đang chọn) — AI (`claude -p`, subscription) nhận 3 nguồn: lịch cố định kênh + baseline rule `upload-schedule.md` + **giờ đăng thật ↔ view thật** từng video (API, kênh có token; không token vẫn chạy theo baseline) → chẩn đoán slot, tín hiệu data (kèm caveat cỡ mẫu), kết luận GIỮ/ĐỔI + cách A/B test 2–4 tuần. Report tự lưu `history/<kênh>/*_ai-schedule.md`. Endpoint `/api/ai_schedule`.
  - **➕ Thêm slot lẻ (2026-07-19):** form đầu tab (kênh + ngày + giờ VN) thêm slot 1 ngày bất kỳ (lưu `extra_slots.json`, tự đổi ra giờ local kênh cho `--slot`, chen đúng thứ tự thời gian nên queue tự dồn theo); slot thêm tay hiện ➕ + nút ✕ xóa (xóa dọn cả ghim gắn vào). "Dời giờ" 1 slot cố định = ghim ∅ trống slot cũ + ➕ slot giờ mới. Slot ngày qua tự dọn. Panel upload tự phát hiện **giờ hẹn trong METADATA đã qua** → gạch đỏ + cảnh báo + nút "📦 Gói lại (giờ mới)".
- **Panel Upload (thay hẳn METADATA.txt, đủ ①→⑨ — 2026-07-19):** title / 概要欄 / tags / pinned với nút **Copy từng ô** + ⑤ nhắc upload `subs.srt` thủ công (cảnh báo đỏ nếu thiếu trong gói) + ⑥ **preview ảnh thumbnail** ngay trên panel, giờ hẹn JST+VN, checklist tick (tự thêm dòng "đo lại Google Trends 30 ngày" — job script headless chỉ ước lượng), cảnh báo pre-flight đỏ.
- **Tab Analytics:** kéo views/likes qua Data API (kênh có token) + 🔬 mổ từng video (theo ngày/nguồn traffic/keyword/retention) + nút đối chiếu kênh thật (--check/--sync). **Khối 🔥 video <72h** hiện riêng trên đầu (bước ⑤ vòng đời — theo dõi cú đẩy đầu). **Mọi lần chạy analytics/AI đều tự lưu snapshot vào `history/<kênh>/`** (engine giữ stateless, dashboard tự lo history — sau này so tuần/vẽ trend từ đây).
- **🤖 AI phân tích (kênh + từng video):** bấm nút → server kéo số liệu tươi rồi đưa cho **Claude Code headless (`claude -p`)** phân tích: phát hiện + nguyên nhân (kèm độ tin cậy) + hành động ưu tiên; per-video thì chẩn đoán giai đoạn sóng đề xuất + đọc retention curve. Chạy trên subscription Claude sẵn có — KHÔNG cần API key, không tốn phí token. Prompt nằm trong `dashboard.py` (AI_PROMPT_CHANNEL / AI_PROMPT_VIDEO). ~30–90 giây/lần.

- **Tab 🏭 Sản xuất (jobs):** chọn kênh + loại job → phóng **1 Claude Code agent chạy nền** (`claude -p`, cwd = repo kênh → tự ăn CLAUDE.md + skill của kênh):
  - ✍️ **Script**: nhập đề tài → agent viết trọn kịch bản + TTS + gói CTR theo skill kênh (trend chỉ ước lượng bằng WebSearch — đo lại Google Trends trước khi upload).
  - 🩹 **Fix meta (2026-07-19, spawn từ panel Upload):** panel tự soi thiếu gì (title/desc/tags/pinned/thumbnail/srt/file SEO) → nút "🤖 AI bổ sung thiếu (N)" phóng agent viết phần thiếu vào mục Đóng gói CTR của script theo format chuẩn kênh + SEO rule + compliance, rồi tự `upload_pack --force` gói lại. Thiếu srt thì agent chỉ báo (phải chạy job Render). Tab Lịch đăng cũng có nút **📋** trên slot GÓI SẴN mở thẳng panel này.
  - 🎬 **Render**: nhập slug → agent chạy pipeline render của kênh (stage/resume, media kho chung, verify). Cần voice engine đang mở.
  - 🖼️ **Thumbnail**: nhập slug → agent theo luật thumbnail kênh; cần ảnh AI gen thì nó dừng lại đưa prompt + đường dẫn đặt ảnh, có ảnh rồi thì ghép chữ + duyệt 3 cửa.
  - Log stream trực tiếp trên web (dịch từ stream-json), nút kill, job chạy nhiều phút→vài giờ vẫn sống khi đóng tab. Quyền agent: allowlist tool (Bash/Read/Write/Edit/...), KHÔNG dùng --dangerously-skip-permissions.
  - **Bền + an toàn (2026-07-19):** job persist qua `jobs/registry.json` — restart dashboard vẫn thấy job đang chạy (probe PID); kill = `taskkill /F /T` giết cả cây (claude + ffmpeg/python con); chặn spawn job trùng (type+kênh+slug); cảnh báo khi 2 render chạy song song (tranh voice engine); chấm ● VOICEVOX/AivisSpeech ngay trên tab báo engine mở chưa; job xong → toast + nút bước kế (script→render→thumbnail→📦 gói); mọi request check Host header (chặn DNS rebinding).

## Kiến trúc & tái sử dụng

```
config.json { tools_dir, port }   ← ⭐ đổi tools_dir = dùng cho bộ kênh/workspace khác
dashboard.py                      Flask; đọc = import hàm engine, ghi = subprocess CLI
templates/index.html + static/    vanilla JS + CSS dark, không build step
```
- KHÔNG chứa logic nghiệp vụ — nguồn sự thật vẫn là script .md + filesystem + engine tools. Thêm kênh mới vào `CHANNELS` (upload_pack.py) là dashboard tự hiện.
- Engine yêu cầu (interface tối thiểu trong tools_dir): `upload_pack.py` (CHANNELS, PROJECTS_ROOT, find_video_dir, CLI --force/--done/--thumb), `pipeline_status.py` (scan_channel, upcoming_slots, CLI --check/--sync), `analytics_report.py` (CLI --channel).

## Không làm (v1)

Upload file lên YouTube từ web (vẫn Studio kéo thả / upload_api sau audit) · sửa metadata trên web (sửa ở script rồi Đóng gói lại) · LAN/mobile · auth.

## Liên quan

- Rule vận hành: `E:\Claude\.claude\rules\upload-schedule.md` (mục 1.5 — vòng đời chuẩn 1 video)
- Engine: `E:\Claude\Projects\youtube-jp-chouhen\tools\`
- Vault: `E:\Claude\SecondBrain\10_Projects\yt-dashboard\yt-dashboard.md`


## Bộ A/B thumbnail + title trong panel Upload (thêm 2026-08-01)

**Hiển thị:** panel Upload mục **⑥** tự chuyển sang chế độ A/B khi gói `_upload/` có **>1** file
`thumbnail*.png` — hiện 3 ảnh cạnh nhau (220px, có caption `T1 · thumbnail.png`), kèm cảnh báo đỏ
*"Test & compare chỉ A/B được THUMBNAIL, giữ nguyên title ≥7 ngày"*. Mục **②b** hiện bộ title A/B,
mỗi dòng có nút `copy`, dòng đầu ghi *← DÙNG KHI ĐĂNG*.

**Ba file đã sửa:**
| file | sửa gì |
|---|---|
| `youtube-jp-chouhen/tools/upload_pack.py` | gom mọi `thumb_T<N>_*.png` của video → `_upload/thumbnail.png` (N=1) + `thumbnail_T<N>.png`; `parse_ctr()` bóc thêm bảng `### 3 TITLE A/B` từ script → ghi khối `[A1]/[A2]/[A3]` vào METADATA mục [2], và danh sách ảnh vào mục [6] |
| `dashboard.py` | `/api/metadata` trả thêm `thumbs[]` + `ab_titles[]` (bóc từ METADATA); `/api/thumb` nhận `?v=thumbnail_T2.png` — có `re.fullmatch` chặn path traversal |
| `static/app.js` + `static/style.css` | render 3 ô ảnh + khối ②b, class `.thumb-ab` / `.ab-title-row` |

⚠️ **PHẢI RESTART DASHBOARD** sau khi sửa (`dashboard.py` nạp code 1 lần lúc khởi động — cùng bẫy đã
ghi ở `upload-schedule.md` mục 1.5 với `CHANNELS`): `taskkill /PID <pid python dashboard.py> /F` rồi
chạy lại `run_dashboard.cmd`.

⚠️ **Quy ước tên bắt buộc:** bản A/B phải đặt `thumb_T1_*.png`, `thumb_T2_*.png`, `thumb_T3_*.png`
trong `06_VIDEO/<slug>/`. Tên khác (`thumb_A_scene.png`, `thumb_G_portrait.png`…) **không** được gom —
cố ý, để bản thử nháp không lọt vào gói upload.
