---
type: source-note
source_type: book-chapter
source_file: 2.5 - Quản lý Context.pdf
title: "Bài 2.5: Quản lý Context"
authors: Khóa học "Claude Code 101" — bản tiếng Việt v1.0 (gốc Anthropic)
year: 2026
url: https://notebooklm.google.com/notebook/2a42eeff-a797-44cd-86d5-f8b8a4ee491b
project: claude-code-101
module: "Vận hành Claude Code chuyên nghiệp"
lesson_id: "2.5"
estimated_time: 25 phút
level: Cơ bản → Trung cấp
tags: [book-chapter, claude-code, context-window, compact, clear, subagent, mcp, course-material]
status: summarized
created: 2026-05-24
---

# Bài 2.5: Quản lý Context

## TL;DR

Context window là **bộ nhớ làm việc 200k token** mà Claude Code phải dùng cho mọi prompt, file read, tool call — đầy thì attention "loãng" và auto-compact có thể *âm thầm xóa* chi tiết quan trọng. Bài đưa ra ba lệnh cốt lõi để cầm cương: `/context` (chẩn đoán), `/compact` (nén & giữ task hiện tại), `/clear` (reset hoàn toàn) — với **quy tắc vàng**: còn dở task → compact, đổi task → clear, đừng để auto-compact tự kích hoạt. Năm chiến thuật chủ động giảm tiêu thụ context: (1) prompt cụ thể, (2) đẩy ngữ cảnh repeat vào CLAUDE.md, (3) outsource exploration cho subagent, (4) dùng skill thay hardcode trong CLAUDE.md, (5) tắt MCP server không dùng — kèm 5 anti-patterns thường gặp và 4 mẹo nâng cao (pin trước compact, `#` shortcut, multi-session với git worktree, ước lượng context trước prompt).

## Mục tiêu học tập (theo tác giả)

Sau bài này người học sẽ có thể:

1. Giải thích context window là gì và tại sao là tài nguyên quan trọng nhất khi dùng Claude Code.
2. Phân biệt khi nào nên dùng `/compact` và khi nào nên dùng `/clear`.
3. Đọc kết quả lệnh `/context` để biết phần nào đang chiếm chỗ trong bộ nhớ làm việc.
4. Áp dụng 5 chiến thuật tiết kiệm context: prompt cụ thể, CLAUDE.md, subagent, skill, MCP cleanup.
5. Tránh 4 anti-patterns thường gặp khiến context "phình to vô tội vạ".

## Bối cảnh trong khóa học

Bài 2.5 nằm ở **Module "Vận hành Claude Code chuyên nghiệp"**. Đi cặp với Bài 2.4 (Workflow EPCC): EPCC dạy *trình tự* làm việc, bài này dạy *cách giữ tài nguyên* để trình tự đó chạy được trong session dài. Tiền đề cho Bài 2.7 (CLAUDE.md), Bài 2.8 (Subagent), Bài 2.9 (Skill), Bài 2.10 (MCP) — đều là các kỹ thuật được giới thiệu ở đây dưới góc nhìn "tiết kiệm context".

Câu chuyện mở đầu rất "đời": dev debug auth 30 phút, đọc 18 file, chạy 12 test, web search 4 lần → auto-compact nhảy → Claude "quên" rule "JWT secret rotate mỗi 7 ngày". Bài học: **không quản lý chủ động = mất ký ức ngẫu nhiên**.

## Khái niệm cốt lõi

### Context window dưới góc nhìn dev

Context window mặc định 200.000 token (~150k từ tiếng Anh, ~80–100 file mã nguồn cỡ trung bình). Gồm các thành phần:

| Thành phần | Token điển hình |
|---|---|
| System prompt (Claude Code core) | ~5k |
| CLAUDE.md (project + user + nested) | 2–10k |
| MCP server tool definitions | 5–30k |
| Skills (chỉ tên + description khi chưa load) | ~200/skill |
| Conversation + tool calls + results | Phình dần theo session |

Khi đầy ~80% → auto-compact tự kích hoạt: Claude tóm tắt rồi vứt bỏ tool result chi tiết, thay bằng đoạn summary. **Risk**: chi tiết nói cách đây 50 prompt có thể chỉ còn 1 dòng, hoặc biến mất hoàn toàn.

Phép so sánh tác giả đánh giá chuẩn nhất với thực tế: *"trí nhớ ngắn hạn của con người — nhớ 7 phút trước rõ, nhớ 2 giờ trước thì mơ hồ"*.

### 3 lệnh cầm cương

| Lệnh | Hành động | Khi nào |
|---|---|---|
| `/context` | XEM breakdown context theo category | Mọi quyết định bắt đầu từ đây |
| `/compact` | Nén hội thoại, GIỮ tóm tắt task hiện tại | Còn dở task, context >70% |
| `/clear` | XÓA hết, chỉ giữ CLAUDE.md + system + MCP defs | Xong task / đổi task hoàn toàn |

**Quy tắc vàng**: Cứ 30–45 phút gõ `/context`. Còn dở → compact. Đổi task → clear. Đừng phó mặc auto-compact.

### Bảng so sánh compact vs clear vs auto-compact

| Tiêu chí | /compact | /clear | Auto-compact |
|---|---|---|---|
| Trigger | Chủ động | Chủ động | Hệ thống tự khi ~80% |
| Giữ tóm tắt task | ✅ | ❌ | ✅ (có thể mất chi tiết) |
| Token sau khi xong | ~20–40k | ~5–10k | ~60–100k |
| Risk mất nuance | Thấp | N/A (xóa hết) | Trung bình → Cao |
| Tốt cho | Long feature dev | Workflow nhiều task nhỏ | Bảo hiểm cuối cùng |

## 5 chiến thuật tiết kiệm context

1. **Be specific** — Prompt mơ hồ ("sửa cái bug auth") khiến Claude thám tử ~25k token. Prompt cụ thể (file + dòng + nguyên nhân + cách fix) ~3k token. *Một câu prompt chi tiết hơn 50 từ có thể tiết kiệm 20.000 token đọc file.*
2. **CLAUDE.md cho ngữ cảnh repeat** — Quy tắc dùng pnpm, test command, vị trí migration, export style... đẩy vào CLAUDE.md. Trade-off: CLAUDE.md cũng tốn context → **chỉ đưa thứ lặp lại ≥3 lần trong các session khác nhau**.
3. **Subagent outsource exploration** — Task read-heavy nhưng answer-light ("tìm tất cả TODO group theo module") → spawn subagent. Subagent có context window 200k riêng, chỉ trả về summary, main context giữ sạch. *Quy tắc "answer without journey"*.
4. **Skill thay hardcode trong CLAUDE.md** — CLAUDE.md load *luôn luôn*. Skill load *on-demand* (Claude đọc name + description, chỉ load full khi match request). PR review checklist → nên là skill, không nên là CLAUDE.md.
5. **Dọn MCP server không dùng** — Mỗi MCP tốn 2–15k token chỉ cho tool definitions. 5 server không relevant = 30k token vô nghĩa. Lệnh `/mcp disable <name>` hoặc cấu hình `.mcp.json` per-project. *Thà cài lại khi cần hơn để context bị ăn mòn.*

## Case studies — quản lý context theo role

- **Backend Engineer** (long feature 4–6h): prompt chi tiết → /context mỗi giờ → /compact khi >60% → subagent đọc docs library → /compact lần nữa khi chuyển từ implement sang viết test.
- **Product Designer ship code**: /clear mỗi khi đổi component → CLAUDE.md có design tokens → skill `/polish-design` với checklist → subagent check accessibility → 8 polish PR/ngày, context never >30%.
- **DevOps incident response**: prompt cực ngắn cực cụ thể → subagent đọc log MB → /clear trước khi apply fix → /clear lần nữa để viết postmortem.
- **CS Student học codebase mới**: KHÔNG đọc tất cả → spawn 4 subagent song song explore 4 module → main context tổng hợp 4 summary ~10k token → hiểu kiến trúc trong 30 phút thay vì 2 ngày.

## 5 anti-patterns

1. **"Just keep going"** — session 4h không gõ /context lần nào → auto-compact 3 lần → mất nuance dồn lại = mất trí nhớ ngắn hạn.
2. **"Tải tất cả file để Claude hiểu"** — project 1000+ file = 500k+ token, không vừa context. Đúng: CLAUDE.md mô tả high-level + subagent explore module khi cần.
3. **Mix nhiều task khác nhau trong 1 session** — Claude bị "ám" bởi pattern task cũ, đề xuất design pattern lệch lạc cho task mới. Đúng: một session = một task tập trung.
4. **Bật mọi MCP server "phòng khi cần"** — 12 server connected = 50k token (25% context) mất trước khi gõ prompt đầu tiên.
5. **Dùng /clear khi đang dở task quan trọng** — mất quyết định + file đang sửa + edge case đã thảo luận → phải brief lại từ đầu, tốn hơn cả compact.

## Mẹo nâng cao

- **Pin trước /compact**: Trước khi compact, ghi quyết định quan trọng vào CLAUDE.md → dù tóm tắt drop chi tiết, CLAUDE.md vẫn giữ rule cho mọi session sau.
- **`#` shortcut cho memory**: Gõ `#` rồi nhập note → Claude hỏi lưu vào CLAUDE.md project/user/nested. Cách nhanh nhất biến correction thành persistent memory.
- **Multi-session với git worktree**: Hai task song song = hai terminal tab + `git worktree add` → mỗi tab context window riêng, không "ám" lẫn nhau.
- **Estimate context trước prompt**: File reads (~500–2000/file) + grep (~1–3k) + web search (~2–5k) + test output (5–50k). Dự kiến >60k → tách task hoặc dùng subagent.

## Bài tập áp dụng (theo tác giả)

1. **Audit context session hiện tại** (~10 phút): /context → ghi % và category chiếm nhiều → action (disable MCP / trim CLAUDE.md / compact) → /context lại → ghi tiết kiệm bao nhiêu.
2. **Workflow /compact vs /clear** (~15 phút, 1 sáng): list 3 task khác nhau → sau mỗi task, quyết định compact (liên quan) hay clear (không liên quan) → cuối ngày đếm số lần compact / clear / auto-compact (mục tiêu auto = 0).
3. **Context budget cho task lớn**: ước lượng cost (CLAUDE.md + file reads + web search + tool calls + conversation overhead) → lên plan (compact mỗi N phút, subagent cho gì, MCP nào tắt) → so estimate vs actual sau task.

## Điểm mạnh & điểm yếu (theo tôi)

**Mạnh:**
- Bảng so sánh `/compact` vs `/clear` vs auto-compact cực kỳ tiện để tra cứu — đủ ngắn để in dán bàn.
- Tỉ trọng "prompt cụ thể" được nhấn mạnh đúng chỗ — đa số người dùng tin "ngắn = tiết kiệm" là sai lầm phổ biến.
- 4 case study theo role (backend / designer / devops / student) giúp người đọc tự ánh xạ vào workflow của mình, không bị abstract.

**Yếu:**
- Chưa nói rõ cách *đo* xem auto-compact đã drop chi tiết nào — sau compact, người dùng không biết mất gì cho tới khi gặp hậu quả.
- Mẹo "pin vào CLAUDE.md trước compact" có thể bị abuse → CLAUDE.md phình theo thời gian, vi phạm quy tắc "chỉ thứ lặp ≥3 lần". Tác giả không cảnh báo.
- Con số 200k token là default Anthropic hiện tại — nhưng model cao cấp (Opus 4.7 1M context) khiến quy tắc "30–45 phút /context lần" có thể quá thường. Bài không phân biệt theo model.

## Ý tưởng nảy ra khi đọc — ứng viên atomic

- [ ] **`/compact` vs `/clear`: quy tắc còn dở vs đổi task** → atomic-claim. Quy tắc nhị phân ngắn gọn, dễ tái sử dụng trong nhiều note hướng dẫn workflow khác.
- [ ] **Prompt cụ thể tiết kiệm context hơn prompt ngắn** → atomic-claim. Phản trực giác, đáng standalone để link vào các bài về prompt engineering.
- [ ] **Subagent là "context isolation pattern"** (quy tắc "answer without journey") → atomic-concept. Cùng họ với `[[claude-code-subagent-fresh-eyes]]` đã có trong vault.
- [ ] **Auto-compact mất nuance như compress JPEG nhiều lần** → atomic-concept. Phép so sánh dễ nhớ, có thể link cross-domain.
- [ ] **MCP server overhead = cost trước khi prompt** → atomic-claim. Số liệu cụ thể (2–15k/server, 25% nếu 12 server) — dùng được khi thảo luận kiến trúc tooling.

## Liên kết

- Project: [[10_Projects/claude-code-101]]
- Source note cùng module: [[2026-claude-code-101-epcc-workflow]], [[2026-claude-code-101-prompt-dau-tien]]
- Atomic đã chắt từ source này (2026-06-08): [[context-window-tai-nguyen-huu-han]], [[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]], [[compact-khi-do-dang-clear-khi-doi-task]], [[mcp-server-overhead-cost-truoc-prompt]], [[subagent-context-isolation-pattern]]
- Index: [[claude-code-MOC]]

## Chỗ chưa chắc

- Tài liệu nhắc "tool search mode khi MCP >10%" nhưng nói "feature chưa stable" — không rõ tại thời điểm 2026-05-24 đã stable chưa, cần kiểm tra docs Anthropic hiện hành.
- Con số "30–45 phút /context lần" áp dụng cho context window 200k. Với model 1M context (Opus 4.7) — chưa rõ tỉ lệ có nên giãn ra không.
