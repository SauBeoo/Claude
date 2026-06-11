---
type: changelog
created: 2026-05-24
updated: 2026-06-12
tags: [meta, changelog, system-log]
---

# 📜 CHANGELOG — Lịch sử sửa đổi hệ thống vault

> **Mục đích:** ghi lại các thay đổi với file **đã tồn tại** trong vault — để truy vết "ai/khi nào đổi gì, vì sao".
>
> **Quy tắc ghi log:**
> - ✅ Edit nội dung file đang có → log ở đây.
> - ❌ Tạo file mới → KHÔNG log (xem qua `git log --diff-filter=A` hoặc Obsidian).
> - ❌ Edit nội dung do user trực tiếp gõ → KHÔNG log (chỉ log khi Claude thay mặt).
> - Mỗi entry: file path + tóm tắt thay đổi (1 dòng) + lý do.

## 2026-06-11 — Đổi README index → folder-note để graph đọc được; dọn lại filter graph

**Bối cảnh:** graph rối vì (1) filter `search` trong `graph.json` bị reset về rỗng → index lại cả `Projects/`; (2) hàng chục file `README.md` (mỗi folder PARA + mỗi project) hiện cùng nhãn "README" trong graph → không phân biệt được node nào là gì. Xử lý: **đổi tên README index theo folder-note convention** (`<folder>/<folder>.md`) để node có nhãn rõ; và sau khi thử giữ cả Projects thấy vẫn rối, **chốt graph = chỉ tri thức SecondBrain** (khôi phục chuẩn cũ `path:SecondBrain`), ẩn node operational + ẩn chấm cô đơn.

### 🔧 Thay đổi file đang tồn tại

| File | Thay đổi | Lý do |
|---|---|---|
| `E:\Claude\.obsidian\graph.json` | `search` rỗng → ẩn config + node operational (`-path:".obsidian" -path:".claude" -file:"CHANGELOG" -file:"README" -file:"CLAUDE" -file:"00_HOME" -file:"tag-system" -file:"flashcards" -file:"track" -path:"60_Daily" -path:"99_Meta/templates" -path:"99_Meta/guides"`) NHƯNG giữ Projects; `showOrphans:true→false`; 6 color group (5 tầng SecondBrain + Projects cam) | Graph = tri thức SecondBrain + cụm Projects, ẩn operational + chấm cô đơn |
| 21× `SecondBrain/**/README.md` → `<folder>/<folder>.md` | Rename folder-note (vd `10_Projects/README.md`→`10_Projects/10_Projects.md`, `50_Atomic/README.md`→`50_Atomic/50_Atomic.md`) | Graph hiện nhãn folder rõ thay vì loạt "README" trùng |
| 9× `Projects/**/README.md` → `<folder>/<folder>.md` | Rename README các code repo (glowup-studio + sub, ai-luoi, freelance-kit demos, research-llm, student-grade-app, youtube-kham-pha) | Cùng lý do |
| `00_HOME.md` | 3 link `…/claude-code-101/README`, `…/idea-aff/README`, `50_Atomic/README` → folder-note mới | Theo file đã đổi tên |
| `99_Meta/MOCs/claude-code-MOC.md`, `…/sources/2026-claude-code-101-epcc-workflow.md` | Link `…/claude-code-101/README` → `…/claude-code-101/claude-code-101` | nt |
| `Projects/glowup-studio/glowup-studio.md`, `Projects/freelance-kit/00_CHIEN_LUOC.md`, `Projects/glowup-studio/CLAUDE.md` | Sửa link/text nội bộ trỏ README đã đổi tên | nt |
| `.claude/commands/{archive-project,moc-update,promote-atomic}.md` | Bỏ hardcode `README.md`: archive đọc/ghi `10_Projects/$1/$1.md`; moc/promote bỏ glob `50_Atomic.md` | Command từng hardcode README → gãy sau rename |
| `.claude/agents/librarian.md`, `.claude/CLAUDE.md` (vault) | Note dự án = folder note; cập nhật mục graph hygiene (5,6) theo filter mới (`path:SecondBrain` + ẩn operational, `showOrphans:false`) | Đồng bộ doc với thực tế |
| `99_Meta/guides/huong-dan-van-hanh-secondbrain.md` | Cập nhật mục 15.5/15.6, sơ đồ cây, bảng command | nt |
| `tag-system.md`, `99_Meta.md`, `40_Archive/40_Archive.md`, `10_Projects/10_Projects.md`, `30_Resources/courses/courses.md` | Sửa text/sơ đồ cây "README" → tên folder note | Đồng bộ tài liệu |
| `60_Daily/2026/05/2026-05-30.md`, `60_Daily/2026/06/2026-06-03.md` | Gỡ toàn bộ `[[wikilink]]` trong section "📚 Đã chắt lọc" + EVENING → đổi thành text/backtick (atomic, MOC, _track, flashcards) | User muốn daily không nối vào cụm tri thức trong graph; giữ tên note dạng text để vẫn đọc được provenance |
| `99_Meta/templates/daily.md`, `.claude/commands/daily-write.md` | Đổi quy ước section "📚 Đã chắt lọc": ghi tên note dạng text/backtick thay vì `[[wikilink]]` | Để daily TƯƠNG LAI cũng không tự nối vào graph (tutor không ghi daily nên không cần sửa) |

**File mới (không thuộc diện log, ghi để truy vết):** `10_Projects/claude-code-101/claude-code-101.md`, `10_Projects/idea-aff/idea-aff.md` — folder note cho 2 project thiếu index (4 link trong `00_HOME`/MOC trước đó dangling, nay đã trỏ đúng).

**Lưu ý:** chốt cuối — graph hiện **cả SecondBrain (tri thức) lẫn Projects (cụm cam)**; chìa khoá giữ gọn là ẩn hết node operational/config + `showOrphans:false` (thay vì loại nguyên `path:SecondBrain`). User đã chỉnh tay các thông số lực/hiển thị (`textFadeMultiplier`, `repelStrength`, `scale`...) → giữ nguyên, không đụng.

---

## 2026-06-11 — Dọn graph: ẩn file operational ngoài SecondBrain, nối provenance idea-aff

**Bối cảnh:** user thấy graph nhiều chấm lẻ. Nguyên nhân chính: vault Obsidian mở từ `E:\Claude` nên graph hiển thị cả ~35 file .md operational trong `Projects/` (roadmap, chiến lược, README các code repo) — không phải tri thức, không có link. Xử lý theo quy tắc graph hygiene: ẩn operational, chỉ nối link thật.

### 🔧 Thay đổi file đang tồn tại

| File | Thay đổi | Lý do |
|---|---|---|
| `E:\Claude\.obsidian\graph.json` | Filter thêm `path:SecondBrain` (loại toàn bộ `Projects/` + README gốc) và `-file:tag-system`; trước đó cùng đợt: `showOrphans:false→true`, `textFadeMultiplier` âm→dương, thêm color group `40_Archive` | Graph chỉ hiển thị tri thức trong vault; nhãn hiện không cần hover; user muốn thấy chấm đèn báo |
| `10_Projects/idea-aff/sources/xay-he-thong-funnel-affiliate-voi-ai.md` | Thêm `- Trích từ: [[ai-affiliate-funnel]]` vào "## Liên kết" | Provenance summary→bản gốc (2 file cùng nội dung đang đứng lẻ trong graph) |
| `.claude/CLAUDE.md` (vault) | Cập nhật điểm 6 mục graph hygiene: baseline mới `path:SecondBrain`, `showOrphans:true`, textFade dương | Đồng bộ rule với cấu hình thực tế user đã chốt |

**Chấm lẻ giữ nguyên (đèn báo, không nối ép):** `ML-MOC` (skeleton, status: planned), `20_Areas/investing/mentor-dau-tu-co-phieu-hoi-thoai` (chủ đề investing chưa chắt atomic). Link `[[50_Atomic/concepts/chi-toi-uu-nhung-gi-trong-tam-kiem-soat]]` trong summary idea-aff đang **unresolved** — atomic ghi "đã tạo" nhưng chưa tồn tại.

---

## 2026-06-08 — Sửa nhãn note nguồn Claude 101 cho trung thực

**Bối cảnh:** user phát hiện note `claude-101-anthropic-academy` đội lốt `source-note` nhưng thực ra chỉ là index (không có nội dung tóm tắt — 15 PDF gốc chưa summarize, atomic được học thẳng qua `/teach`). User chọn "sửa nhãn cho trung thực" thay vì backfill.

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| `30_Resources/courses/claude-101-anthropic-academy.md` | `type: source-note→source-index`, `status: distilled→index-only`, sửa path source_file đúng, thêm cảnh báo rõ "đây là bản đồ nguồn, KHÔNG phải tóm tắt; 15 PDF chưa summarize" | Không nói dối về việc đã gen source; phân biệt với Claude Code 101 (có source thật) |

---

## 2026-06-08 — Chốt quy tắc "graph hygiene" vào CLAUDE.md vault

**Bối cảnh:** sau loạt việc dọn graph + provenance + tỉa link, user yêu cầu tổng hợp quy tắc đã áp vào CLAUDE.md để các phiên sau tự tuân.

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| `.claude/CLAUDE.md` | Thêm mục "Quy tắc liên kết & đồ thị (graph hygiene)" (mỗi note một vai trò, atomic ≤2 link, cross-domain bridge tiết kiệm, provenance source→atomic bắt buộc, node nên ẩn khỏi global, baseline graph.json); chỉnh điểm 4 phần tạo atomic ("3-5 link" → "tối đa 2 load-bearing") | Đóng băng quy ước đã thống nhất trong phiên |
| `99_Meta/guides/huong-dan-van-hanh-secondbrain.md` | Thêm **mục 15 "Graph hygiene"**; sửa các chỗ mâu thuẫn "≥3 link" → "≤2 load-bearing + MOC index" (mục 4 Bước 3, mục 7 bảng, mục 9 checklist, mục 10); thêm anti-pattern "Over-link/quạt trùng"; thêm trigger graph vào mục 14.1; `updated: 2026-06-08` | Đồng bộ guide với CLAUDE.md, gỡ mâu thuẫn nội bộ |

---

## 2026-06-08 — Tỉa link ngang giữa atomic (chống tangle)

**Bối cảnh:** sau khi chắt 15 atomic Claude Code + nối provenance, graph atomic↔atomic quá đặc (107 link ngang / 34 atomic + quạt trùng MOC vs note nguồn khóa). User chọn "tỉa mạnh".

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| 26 atomic trong `50_Atomic/{concepts,claims,methods}/` | Tỉa mục "## Liên hệ" còn tối đa 2 link load-bearing/note; chỉ giữ 2 cầu nối cross-domain (`prompt-la-brief↔4d-framework`, `mcp-server-overhead↔mcp-usb-c`) | Giảm tangle: 107 → 66 link ngang. MOC vẫn giữ reachability nên không atomic nào bị mồ côi |

### 📝 Không log

- `.obsidian/graph.json`: thêm `-file:claude-101-anthropic-academy` vào filter để ẩn quạt trùng (note nguồn khóa) khỏi global graph — provenance vẫn xem qua Local Graph. (Config, không thuộc nội dung vault.)

---

## 2026-06-08 — Dọn graph view + thiết lập link provenance (nguồn → atomic)

**Bối cảnh:** graph view "rối mắt", link "loạn không quy củ". Chẩn đoán: graph rối vì (a) config hiển thị mặc định kém và (b) 3 hub (MOC + _track + daily) cùng fan-out 18 atomic giống hệt nhau (log đúng-thiết-kế, không phải rác). Fix bằng filter graph + thiết lập provenance source→atomic, KHÔNG xóa link log. Sau đó user yêu cầu nối atomic với nguồn/sources project → làm cho cả 2 domain (Claude 101 + Claude Code 101).

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| `50_Atomic/{concepts,claims,methods}/*.md` (19 file Claude 101) | Chèn `- Trích từ: [[claude-101-anthropic-academy]]` đầu section "## Nguồn" | Link provenance atomic → note nguồn |
| `10_Projects/claude-code-101/sources/2026-claude-code-101-quan-ly-context.md` | Thay placeholder "Phase 2" bằng 5 link atomic đã chắt + link `claude-code-MOC` | Provenance 2 chiều source ↔ atomic (vá link gãy trong `thread-quan-ly-context`) |
| `10_Projects/claude-code-101/sources/2026-claude-code-101-epcc-workflow.md` | Thay placeholder "chưa có" bằng 6 link atomic Bài 2.4 + `claude-code-MOC` | Provenance source ↔ atomic |
| `10_Projects/claude-code-101/sources/2026-claude-code-101-prompt-dau-tien.md` | Thêm mục "Atomic đã chắt" (4 link Bài 2.3) + `claude-code-MOC` | Provenance source ↔ atomic |

### 📝 File mới (không cần log chi tiết)

- Note nguồn: `30_Resources/courses/claude-101-anthropic-academy.md` (provenance hub 19 atomic Claude 101).
- **15 atomic Claude Code 101**: Bài 2.5 (5) — `context-window-tai-nguyen-huu-han`, `subagent-context-isolation-pattern`, `prompt-cu-the-tiet-kiem-context-hon-prompt-ngan`, `compact-khi-do-dang-clear-khi-doi-task`, `mcp-server-overhead-cost-truoc-prompt`; Bài 2.3 (4) — `prompt-la-brief-khong-phai-command`, `4-thanh-phan-prompt-tot`, `3-permission-modes-claude-code`, `3-task-framework-easy-medium-hard`; Bài 2.4 (6) — `epcc-workflow-bon-phase`, `cost-thay-doi-tang-theo-phase`, `test-suite-source-of-truth-voi-ai`, `claude-code-subagent-fresh-eyes`, `calibrate-workflow-theo-task-size`, `tech-debt-leaf-node-acceptable`.
- MOC mới: `99_Meta/MOCs/claude-code-MOC.md` (index 15 atomic theo 3 bài).
- (Config Obsidian `.obsidian/graph.json` — không thuộc nội dung vault, không log.)

---

## 2026-06-08 — Buổi 5 Claude 101 (HOÀN TẤT KHÓA) + `/moc-update`

**Bối cảnh:** buổi cuối track [[../20_Areas/learning/claude-101/_track|claude-101]] (Module 6: Use cases by role + Flavors + Tổng kết/Quiz 1.11–1.14). Tạo 2 atomic mới; chạy `/moc-update` phát hiện đúng 2 orphan, user duyệt "ok". Track chuyển `status: done` — 6/6 module, 18 atomic, 32 flashcards.

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| `20_Areas/learning/claude-101/_track.md` | Module 6 → ✅; nhật ký Buổi 5; đánh dấu khóa hoàn tất; `status: learning→done`; carry-over còn lại (Context trong C-T-R, Research vs web search); `updated: 2026-06-08` | Quy trình chốt buổi của skill tutor |
| `20_Areas/learning/claude-101/flashcards.md` | Thêm 6 thẻ Buổi 5 (scoring framework, flavors, Chrome preview, C-T-R Context) — tổng 32 thẻ | Cùng lý do |
| `99_Meta/MOCs/claude-MOC.md` | Index 2 atomic mới (1 concept, 1 method); `updated: 2026-06-08` | `/moc-update` — không để atomic orphan |

### 📝 File mới (không cần log chi tiết)

- 2 atomic: `methods/cham-diem-chon-use-case`, `concepts/claude-flavors-cung-tri-tue-nhieu-cua`.

---

## 2026-06-03 — Buổi 4 Claude 101 + `/moc-update` lần đầu

**Bối cảnh:** buổi học thứ 4 track [[../20_Areas/learning/claude-101/_track|claude-101]] (Module 5: Connectors/MCP + Enterprise Search + Research) tạo 4 atomic mới; sau đó chạy `/moc-update` quét batch — phát hiện đúng 4 orphan này, user duyệt "tất cả".

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| `20_Areas/learning/claude-101/_track.md` | Module 5 → ✅; thêm nhật ký Buổi 4; checklist ôn Buổi 5; carry-over (Cowork/Code sai lần 2, "you see what you see" vấp 2 lần); `updated: 2026-06-03` | Quy trình chốt buổi của skill tutor |
| `20_Areas/learning/claude-101/flashcards.md` | Thêm 7 thẻ Buổi 4 (MCP, connector types, security, Enterprise Search, decision tree 4 tools, meta-prompt) — tổng 26 thẻ | Cùng lý do |
| `99_Meta/MOCs/claude-MOC.md` | Index 4 atomic mới vào đúng section (1 concept, 2 method, 1 claim); `updated: 2026-06-03` | `/moc-update` — không để atomic orphan |

### 📝 File mới (không cần log chi tiết)

- 4 atomic: `concepts/mcp-usb-c-cho-ai`, `claims/claude-chi-thay-cai-ban-thay`, `methods/chon-tool-theo-cau-hoi`, `methods/nho-ai-draft-prompt-truoc-khi-research`.

---

## 2026-05-30 — Command mới `/daily-write` (tự viết daily)

**Bối cảnh:** user muốn 1 command tự viết daily thay vì chỉ tạo template rỗng (`/daily`). Chọn phương án: command MỚI riêng biệt, nguồn dữ liệu = git activity + thay đổi vault hôm nay, tự viết 2 phần "Việc xong/chưa xong" + "Đã chắt lọc". Xem [[huong-dan-van-hanh-secondbrain]] mục 8.

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| `99_Meta/guides/huong-dan-van-hanh-secondbrain.md` | Mục 8: thêm dòng `/daily-write` vào bảng vai trò Claude; làm rõ `/daily` chỉ tạo template rỗng | Đăng ký command mới theo quy tắc 14.1 |

### 📝 Thay đổi ngoài vault (chỉ note vắn)

- `E:\Claude\.claude\commands\daily-write.md` — file command mới (tạo mới, không cần log riêng).

---

## 2026-05-27 — Quy tắc viết atomic theo kiểu ELI5 (trẻ 5 tuổi hiểu được)

**Bối cảnh:** user yêu cầu mọi atomic note phải trình bày dễ hiểu nhất, sao cho "một đứa trẻ 5 tuổi cũng hiểu được". User chọn phương án: **ELI5 là nội dung chính của thân note** (không thêm section riêng). Áp dụng nhất quán cho cả 2 đường tạo atomic (skill `create-atomic-note` + command `/paper-atomize`), template, và rule vault.

### 🔧 Thay đổi file đang tồn tại (trong vault)

| File | Thay đổi | Lý do |
|---|---|---|
| `99_Meta/templates/atomic-concept.md` | Placeholder thân note thêm hướng dẫn ELI5 ("Tưởng tượng...", ví dụ đời thường, câu ngắn) | Nhắc phong cách ngay tại chỗ viết |
| `99_Meta/templates/atomic-method.md` | Thêm dòng blockquote nhắc ELI5 dưới H1 (xoá sau khi điền) | Cùng lý do |
| `99_Meta/templates/atomic-claim.md` | Thêm dòng blockquote nhắc ELI5 dưới H1 | Cùng lý do |
| `99_Meta/templates/atomic-question.md` | Thêm dòng blockquote nhắc ELI5 dưới H1 | Cùng lý do |
| `99_Meta/guides/huong-dan-van-hanh-secondbrain.md` | Mục 7: thêm tiêu chí "Trẻ 5 tuổi hiểu được (ELI5)" vào bảng + đoạn giải thích (kỹ thuật Feynman) | Đưa ELI5 thành tiêu chí atomic chính thức |
| `SecondBrain/.claude/CLAUDE.md` | Section "Khi tôi nhờ tạo atomic note về X": thêm mục 6 về viết thân note kiểu ELI5 | Ép Claude tuân thủ ngay từ session sau |

### 📝 Thay đổi ngoài vault (chỉ note vắn)

- `E:\Claude\.claude\skills\create-atomic-note\SKILL.md` — Bước 4 (Body) trỏ tới nguyên tắc ELI5; thêm nguyên tắc #5 "Giải thích như cho trẻ 5 tuổi" (ví dụ đời thường, câu ngắn, thuật ngữ chỉ ở tiêu đề, tự kiểm).
- `E:\Claude\.claude\commands\paper-atomize.md` — Phase 2 "Quy tắc viết atomic": thay "giải thích cho người chưa đọc paper" → "giải thích cho một đứa trẻ 5 tuổi (ELI5)".

---

## 2026-05-25 — Dọn Inbox đợt 2 (`/inbox-clean` — folder `ai-luoi/`)

**Bối cảnh:** chạy `/inbox-clean` lần 2. Inbox còn 1 folder `ai-luoi/` chứa 4 file meta-project (CLAUDE.md, ROADMAP, CONTENT-IDEAS, README) được tạo cùng ngày. Vault đã có sẵn `10_Projects/idea-aff/` với `ke-hoach-kinh-doanh-ai-luoi.md` — cùng project "AI Lười". User duyệt **Phương án A**: gộp vào project có sẵn thay vì tách project mới.

### 🔧 Move file (relocate, không xoá)

| File gốc | Đích | Lý do |
|---|---|---|
| `00_Inbox/ai-luoi/CLAUDE.md` | `10_Projects/idea-aff/CLAUDE.md` | Context file cho Claude Code khi `cd` vào project — giữ trong project folder. |
| `00_Inbox/ai-luoi/ROADMAP-90DAYS.md` | `10_Projects/idea-aff/ROADMAP-90DAYS.md` | Plan thực thi 90 ngày của project — thuộc về project folder. |
| `00_Inbox/ai-luoi/CONTENT-IDEAS.md` | `10_Projects/idea-aff/CONTENT-IDEAS.md` | 30 ý tưởng video + 3 script mẫu — output deliverable của project. |
| `00_Inbox/ai-luoi/README.md` | `10_Projects/idea-aff/README.md` | Hướng dẫn cấu trúc 4 file trên — đi cùng cụm. Không conflict (idea-aff/ chưa có README). |

### ⚠️ Ngoài lề

- Folder `00_Inbox/ai-luoi/` rỗng sau khi move — để user quyết có xoá folder rỗng không (Claude không tự xoá).
- Folder `00_Inbox/paper-chua-doc/` rỗng từ trước (4 file đã staged delete trong git index). Không thuộc phạm vi đợt này.

---

## 2026-05-25 — Dọn Inbox đợt 1 (`/inbox-clean`)

**Bối cảnh:** chạy `/inbox-clean` lần đầu. Inbox có 4 file trong `paper-chua-doc/`, tất cả đều mới 0 ngày tuổi nên không có cảnh báo quá hạn, nhưng cần phân loại trước khi tích lũy. User duyệt phương án `Q1=b, Q2=a, Q3=a`.

### 🔧 Move file (relocate, không xoá)

| File gốc | Đích | Lý do |
|---|---|---|
| `00_Inbox/paper-chua-doc/AI Affiliate.md` | `10_Projects/idea-aff/papers/ai-affiliate-funnel.md` | Nội dung phục vụ trực tiếp project `idea-aff` đang chạy. Đổi tên về slug không dấu theo quy ước. Đáng `/paper-atomize` sau (5 nguyên tắc + 5 bước funnel). |
| `00_Inbox/paper-chua-doc/Lập-kế-hoạch-kinh-doanh.md` | `10_Projects/idea-aff/ke-hoach-kinh-doanh-ai-luoi.md` | Đây là kế hoạch nội bộ project "AI Lười" (mảng affiliate cho seller) — gộp vào `idea-aff` thay vì tách project mới (Q2=a). Đổi slug. |
| `00_Inbox/paper-chua-doc/mentor_dau_tu_hoi_thoai.md` | `20_Areas/investing/mentor-dau-tu-co-phieu-hoi-thoai.md` | Kinh nghiệm dài hạn về vai trò nhà đầu tư cá nhân, không gắn deadline → Area mới `investing` (Q3=a). Đổi slug. Đáng `/paper-atomize` (Mr. Market, Circle of Competence, Loss Aversion, bệnh nghe phím, cost-of-recovery math). |

### 🆕 Folder mới (tạo khi cần đích)

- `10_Projects/idea-aff/papers/` — chỗ chứa paper/clip ngoài phục vụ project.
- `20_Areas/investing/` — Area mới cho vai trò đầu tư cá nhân.

### ⚠️ Ngoài lề

- `00_Inbox/paper-chua-doc/Claude code 101.md` (file rỗng) ở git index trạng thái staged delete TRƯỚC khi phiên `/inbox-clean` bắt đầu (không phải do Claude). User quyết định giữ nguyên trạng thái deleted (không restore).

---

## 2026-05-25 — Thêm 2 command + quy tắc bảo trì hệ thống

**Bối cảnh:** user yêu cầu bù lỗ hổng automation cho 2 thao tác định kỳ (archive project, promote atomic) và bổ sung quy tắc bắt buộc về cập nhật guides + CHANGELOG. Tham chiếu: [[huong-dan-van-hanh-secondbrain]] mục 14 (mới), [[SecondBrain/.claude/CLAUDE.md]] section "Quy tắc bảo trì hệ thống".

### 🆕 Command mới (ngoài vault — chỉ note vắn)

- `E:\Claude\.claude\commands\archive-project.md` — quy trình archive 1 project: pre-flight → checklist (4 mục) → update README status: DONE → log CHANGELOG → `Move-Item` → báo cáo. Dùng PowerShell vì shell mặc định là PS.
- `E:\Claude\.claude\commands\promote-atomic.md` — quét 50_Atomic, đề xuất nâng status seed→growing→evergreen theo rule (≥2/3 tiêu chí: link out, link in, tuổi, used_in_output). Có thể chạy batch hoặc cho 1 slug.

### 🔧 Thay đổi file đang tồn tại

| File | Thay đổi | Lý do |
|---|---|---|
| `99_Meta/guides/huong-dan-van-hanh-secondbrain.md` | Mục 8: thêm 2 dòng cho `/archive-project` và `/promote-atomic` trong bảng "Vai trò Claude Code" | Phản ánh tool mới có sẵn để user biết khi nào dùng |
| `99_Meta/guides/huong-dan-van-hanh-secondbrain.md` | Thêm mục 14 mới "Quy tắc bảo trì hệ thống — guides & changelog" (4 mục con: 14.1 khi cập nhật guides, 14.2 khi log CHANGELOG, 14.3 thứ tự thao tác, 14.4 audit định kỳ) | User yêu cầu quy tắc rõ ràng cho việc duy trì xương sống hệ thống |
| `SecondBrain/.claude/CLAUDE.md` | Thêm section "Quy tắc bảo trì hệ thống (BẮT BUỘC)" sau "Việc Claude KHÔNG được tự ý làm" | Ép Claude tuân thủ ngay từ session sau — quy tắc thường trú |

---

## 2026-05-24 — Audit cấu trúc vault lần 1

**Bối cảnh:** vault ở giai đoạn Seed→Sapling. Audit tổng để fix các điểm yếu trước khi scale usage. Tham chiếu: [[00_HOME]] section "Vấn đề cần fix", [[huong-dan-van-hanh-secondbrain]].

### 🔧 Fix stale example references

| File | Thay đổi | Lý do |
|---|---|---|
| `.claude/CLAUDE.md` | Section "Quy ước đặt tên": slug example `research-nlp-2026` → `claude-code-101`, `idea-aff` | Project `research-nlp-2026` không tồn tại trong vault — example stale gây nhầm lẫn |
| `50_Atomic/README.md` | Section "Cấu trúc 1 atomic note": link `[[10_Projects/research-nlp-2026/papers/attention-is-all-you-need]]` → `[[10_Projects/claude-code-101/sources/2026-claude-code-101-quan-ly-context]]` | Cùng lý do — link example trỏ tới source thật trong vault |
| `10_Projects/README.md` | Section "Quy ước đặt tên thư mục": tách "Đang active" (claude-code-101, idea-aff) vs "Pattern đặt tên gợi ý" cho project tương lai | Tránh nhầm lẫn project example với project có thật |
| `40_Archive/README.md` | 2 thay đổi: (1) path example → generic `<project-name>`, (2) `mv 10_Projects/research-nlp-2026 ...` → `mv 10_Projects/<project-name> ...` | Command example phải reusable, không hardcode tên project không tồn tại |

### 🔧 Simplify daily template

| File | Thay đổi | Lý do |
|---|---|---|
| `99_Meta/templates/daily.md` | Rewrite toàn bộ: 2 section MUST (Morning ~30s + Evening ~60s) + 3 section OPTIONAL (Quăng vào, Ý đáng nhớ, Đã chắt lọc). Thêm "yesterday review" 1 dòng ở Morning. Thêm footer "không có gì → ghi `-` cũng đủ". | Daily habit yếu (1/30 ngày tháng 5). Template cũ có 5 section ngang nhau gây cảm giác "phải đầy đủ" → friction. Tách MUST/MAY rõ ràng giảm rào cản tâm lý. |

### 📝 Memory updates (ngoài vault — chỉ note vắn)

- `~/.claude/projects/E--Claude/memory/MEMORY.md` — thêm 1 entry trỏ tới `feedback_critical_assessment_before_scale.md` (rule: khi user hỏi "tối ưu chưa" → critique thật có bằng chứng, không validate suông).

---

## Mẫu entry cho lần sau

```markdown
## YYYY-MM-DD — Tiêu đề audit/đợt sửa

**Bối cảnh:** lý do đợt sửa này, link tham chiếu.

### 🔧 <Nhóm thay đổi>

| File | Thay đổi | Lý do |
|---|---|---|
| `path/to/file.md` | Tóm tắt 1 dòng | Vì sao đổi |
```

---

**Khi nào đọc lại file này:**
- Audit hàng tháng (mục 9 trong [[huong-dan-van-hanh-secondbrain]])
- Khi thấy 1 quy ước có vẻ "lạ" — tra xem khi nào và vì sao đổi
- Trước khi đổi convention lớn — xem lịch sử có quyết định nào liên quan không
