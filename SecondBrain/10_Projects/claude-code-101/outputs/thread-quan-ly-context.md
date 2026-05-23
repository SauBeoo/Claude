---
type: output
format: social-thread
platform: twitter-linkedin
project: claude-code-101
status: draft-v1
created: 2026-05-24
target_audience: dev đang dùng Claude Code / AI coding tool
tags: [output, social, claude-code, context-management]
sources_used:
  - "[[claude-code-MOC]]"
  - "[[context-window-tai-nguyen-huu-han]]"
  - "[[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]]"
  - "[[compact-khi-do-dang-clear-khi-doi-task]]"
  - "[[mcp-server-overhead-cost-truoc-prompt]]"
  - "[[subagent-context-isolation-pattern]]"
---

# Thread: 5 sai lầm về Context khi dùng Claude Code

> **Bài tập Phase 3 đầu tiên** — viết thread CHỈ dùng atomic notes có sẵn trong vault, không mở lại PDF gốc. Mục tiêu: chứng minh atomic notes đủ để sản xuất content.

## Dàn ý → atomic mapping

| Tweet | Ý chính | Atomic note dùng |
|---|---|---|
| 1 (hook) | Context window không phải vô hạn; chất lượng giảm trước khi capacity hết | [[context-window-tai-nguyen-huu-han]] |
| 2 | "Prompt ngắn = tiết kiệm" là sai — prompt cụ thể tiết kiệm hơn | [[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]] |
| 3 | `/compact` vs `/clear`: dùng nhầm là tự bắn vào chân | [[compact-khi-do-dang-clear-khi-doi-task]] |
| 4 | Bật MCP "phòng khi cần" = ăn 25% context trước khi gõ prompt | [[mcp-server-overhead-cost-truoc-prompt]] |
| 5 (twist) | Subagent là cách rẻ nhất tránh full context | [[subagent-context-isolation-pattern]] |
| 6 (CTA) | Tổng kết + invite | — |

---

## Draft v1 — 6 tweet

### 🧵 Tweet 1 (hook)

5 sai lầm khiến Claude Code "quên" giữa session — và cách dev pro tránh.

Context window 200k token không phải vô hạn.
Tệ hơn: chất lượng tụt **trước khi** đầy.
Khi đầy ~80%, attention loãng, Claude xao lãng chi tiết bạn nói 50 prompt trước.

Như trí nhớ ngắn hạn người: 7 phút trước nhớ rõ, 2 giờ trước mơ hồ.

👇

---

### Tweet 2 — Sai lầm #1: tin "prompt ngắn = tiết kiệm"

Sai lầm phổ biến nhất:

❌ "sửa cái bug auth" (5 từ)
→ Claude làm thám tử, đọc 15 file, grep toàn project → **~25k token** chỉ để hiểu yêu cầu.

✅ "file `auth/jwt.ts` dòng 42, biến `exp` đang tính bằng giây thay vì ms" (~50 từ)
→ Claude vào việc thẳng → **~3k token**.

**30 giây gõ specific = đỡ Claude 20 lần file read.**

Prompt cụ thể ≠ prompt dài lê thê. Đủ context để khỏi đoán là đủ.

---

### Tweet 3 — Sai lầm #2: nhầm `/compact` với `/clear`

Hai lệnh nhìn giống nhau, hậu quả ngược nhau:

🔹 `/compact` — nén hội thoại, **GIỮ** tóm tắt task hiện tại
🔹 `/clear` — **XÓA** sạch, về lại system prompt + CLAUDE.md

Quy tắc:
- Còn dở task → `/compact` (giữ memory)
- Đổi sang task khác → `/clear` (tránh bias task cũ)

Dùng `/clear` khi đang dở = phải brief lại từ đầu, đắt hơn cả `/compact`.
Dùng `/compact` khi đổi task = bị task cũ "ám" design task mới.

---

### Tweet 4 — Sai lầm #3: bật mọi MCP server "phòng khi cần"

12 MCP server connected = **~50k token = 25% context** đã mất.

Trước khi bạn gõ ký tự đầu tiên.

MCP load *toàn bộ* tool schema vào context khi session start, không phải on-demand. Server Figma bạn không dùng hôm nay vẫn ăn 5k token chỉ để "có sẵn phòng khi".

Treat MCP list như package.json: chỉ cài cái thực sự dùng cho session này. Lệnh `/mcp disable <name>` là bạn của bạn.

---

### Tweet 5 — Sai lầm #4: cố nhồi mọi thứ vào main thread

Cần tìm tất cả `TODO` group theo module? Cần grep deprecated function?

**Đừng đọc trong main thread.** Đó là *answer without journey* task.

Spawn subagent: nó có context window 200k riêng, đọc 50 file của nó, trả về cho bạn 1 đoạn summary 500 token.

Main thread của bạn vẫn sạch như mới.

Tương tự process isolation trong OS — việc nặng nhốt vào không gian riêng, kết quả tinh chiết mới chảy về main.

---

### Tweet 6 — Sai lầm #5 + CTA

Sai lầm cuối: **phó mặc auto-compact**.

Khi context đạt ~80%, Claude tự nén — nhưng đây là lossy compression. Constraint quan trọng bạn nói 50 prompt trước có thể bị nén còn 1 dòng, hoặc biến mất.

Quy tắc của tôi:
- Mỗi 30-45 phút gõ `/context`
- Chủ động compact/clear trước khi hệ thống quyết định thay bạn
- Pin decision quan trọng vào CLAUDE.md trước khi compact

Quản lý context = quản lý chất lượng output.

---

## Self-review trước khi đăng

- [ ] **Hook có "kéo" đọc tiếp không?** Tweet 1 có hứa giá trị + tạo tò mò (5 sai lầm)
- [ ] **Mỗi tweet đứng vững riêng** (có thể quote tweet lẻ vẫn hiểu)
- [ ] **Có ví dụ cụ thể** ở tweet 2 (so sánh 2 prompt) và tweet 4 (số 50k token)
- [ ] **Tránh thuật ngữ không giải thích** — "auto-compact", "lossy compression" — đã giải thích inline
- [ ] **CTA cuối** — đoạn "quản lý context = quản lý chất lượng" làm closing line, không cần "follow me" trắng trợn

---

## Reflection sau khi viết — feedback cho vault

*(Điền sau khi viết xong)*

**Atomic nào dùng được luôn, không cần sửa?**
→ ✅ `prompt-cu-the-tiet-kiem-context-hon-prompt-ngan` — ví dụ 25k vs 3k token paste thẳng ra tweet được.
→ ✅ `mcp-server-overhead-cost-truoc-prompt` — số liệu 12 server = 50k token rất "tweetable".

**Atomic nào thiếu, phải bịa thêm khi viết?**
→ ⚠️ Không có atomic cụ thể về `/context` command (lệnh chẩn đoán) — chỉ nhắc trong source note. Có thể đáng atomize riêng.
→ ⚠️ Không có atomic về "pin decision vào CLAUDE.md trước compact" — đáng tách thành method note.

**Link cross-atomic nào nảy ra mới?**
→ Ý "treat MCP như package.json" (tweet 4) có thể là claim riêng — kết nối MCP overhead với hygiene mindset của dev.

**→ TODO sau khi đăng thread:**
- [ ] Tạo atomic `lenh-context-de-chan-doan-context-window.md` (method)
- [ ] Tạo atomic `pin-decision-vao-claudemd-truoc-compact.md` (method)
- [ ] Cập nhật MOC claude-code thêm 2 atomic mới

---

## Next steps

1. Đọc lại draft sau 12h (cold review)
2. Cắt bớt nếu quá dài (Twitter 280 ký tự/tweet) — hiện tweet 3, 4 có thể chia 2
3. Quyết định post Twitter hay LinkedIn (LinkedIn có thể giữ format dài hơn)
4. Sau khi post: ghi feedback engagement vào file này, làm input cho deliverable tiếp theo
