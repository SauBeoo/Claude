---
type: changelog
created: 2026-05-24
updated: 2026-05-24
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
