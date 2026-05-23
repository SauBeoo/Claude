# Slash Commands + Agent — Claude Code

Bộ command và agent cho workflow "Bộ não 2" — hỗ trợ nguồn tài liệu đa định dạng.

## Định dạng hỗ trợ

- `.pdf` — paper, báo cáo, sách scan
- `.md` — note Markdown (từ vault Obsidian khác, blog xuất ra)
- `.docx` — Word document (cần pandoc hoặc python-docx)
- `.txt` — text thuần
- `.html` — web lưu về (tự bỏ nav/sidebar/ads)
- `.epub` — sách điện tử (cần pandoc hoặc ebook-convert)
- File text khác — đa số đều xử lý được nếu đọc được

"Paper" trong tên command hiểu theo nghĩa rộng: **bất kỳ nguồn nào cần chắt lọc thành kiến thức**.

## Cài đặt

### 1. Commands

Copy 6 file `.md` (trừ `researcher.md` và `README.md`) vào `E:\Claude\.claude\commands\`:

```powershell
mkdir E:\Claude\.claude\commands -Force
# Copy: paper-summarize.md, paper-atomize.md, paper-full.md, link-notes.md, inbox-clean.md, daily.md
```

### 2. Agent

Copy `researcher.md` vào `E:\Claude\.claude\agents\`:

```powershell
# Đè lên file researcher.md cũ (nếu có)
# Backup file cũ trước nếu bạn đã tùy chỉnh:
copy E:\Claude\.claude\agents\researcher.md E:\Claude\.claude\agents\researcher.backup.md
```

### 3. Tùy chọn — cài tool convert

Nếu hay đọc `.docx` hoặc `.epub`:

```powershell
winget install pandoc
# Hoặc cho python-docx:
pip install python-docx
```

Khởi động lại `claude` trong terminal. Gõ `/` xem command, gõ `/agent researcher` để kích hoạt agent.

## Danh sách command

### Workflow nguồn tài liệu (chính)

| Command | Dùng khi |
|---------|----------|
| `/paper-summarize <file> [project]` | Tóm tắt 1 nguồn (bất kỳ định dạng nào) → lưu source note |
| `/paper-atomize <source-note>` | Tách source note thành atomic notes |
| `/link-notes <note1> [note2...]` | Tìm note cũ liên quan + thêm `[[wiki link]]` |
| `/paper-full <file> <project>` | Chạy cả 3 bước, dừng giữa mỗi phase |

### Bảo trì bộ não

| Command | Dùng khi |
|---------|----------|
| `/inbox-clean` | Cuối tuần dọn `00_Inbox/` |
| `/daily` | Đầu/cuối ngày, tạo daily note |
| `/moc-update` | Định kỳ (cuối tuần), quét atomic chưa được index vào MOC nào |

### Cơ chế "nó lưu vào đâu?"

Khi chạy workflow, đầu ra được index vào hệ thống như sau:

| Nguồn → Đích | Cơ chế |
|---|---|
| Atomic mới → MOC | `/paper-atomize` Phase 3 đề xuất append vào MOC khớp tag (hoặc tạo MOC mới). Dừng chờ duyệt |
| Source note + atomic → Daily | `/paper-full` cuối Phase 3 hỏi "ghi vào daily không?" → append section `📚 Đã chắt lọc` |
| Atomic orphan → MOC (batch) | `/moc-update` định kỳ quét, gom atomic chưa có nhà → đề xuất phân loại |

Quy tắc match atomic ↔ MOC: **tag overlap**. Atomic có `tags: [a, b]` match với MOC có `tags: [moc, a, ...]`. Mapping `type` → section trong MOC:
- `concept` → 🌱 Khái niệm nền tảng
- `method` → 🛠️ Phương pháp & kỹ thuật
- `claim` → 💭 Luận điểm đáng tranh luận
- `question` → ❓ Câu hỏi mở

## Quy ước đặt tên file

Tên file đề xuất khác nhau theo **loại nguồn**:

| Loại nguồn | Công thức | Ví dụ |
|------------|-----------|-------|
| Paper học thuật | `<năm>-<tác-giả>-<từ-khóa>.md` | `2017-vaswani-attention-is-all-you-need.md` |
| Blog / article | `<năm>-<site>-<từ-khóa>.md` | `2024-stratechery-ai-strategy.md` |
| Chương sách | `<năm>-<tác-giả>-<sách>-ch<N>.md` | `2018-newport-deep-work-ch3.md` |
| Báo cáo | `<năm>-<tổ-chức>-<chủ-đề>.md` | `2024-mckinsey-state-of-ai.md` |
| Note / khác | `<năm>-<chủ-đề>.md` | `2024-ideas-llm-tutoring.md` |

Khi chạy command:

1. **Metadata đủ** → agent đề xuất tên, bạn chỉ Enter
2. **Thiếu metadata** → agent đoán + đề xuất, hỏi confirm
3. **Muốn xem option khác** → gõ `?`
4. **Muốn đặt khác** → gõ tên mới

→ 90% trường hợp chỉ nhấn Enter.

## Cấu trúc lưu note

```
SecondBrain\10_Projects\<project>\
└── sources\           ← Lưu source note (paper, blog, sách, báo cáo, note...)
    ├── 2024-smith-llm.md
    ├── 2024-mckinsey-ai-report.md
    └── 2024-newport-deep-work-ch3.md
```

`50_Atomic\` luôn flat (không sub-folder) — atomic notes phân loại bằng `tags`, không phải folder.

## Workflow cho người mới (tuần 1)

### Source #1 — chạy từng command để hiểu rõ

```
# Có thể là PDF, blog đã save .html, hoặc Markdown từ vault khác
/paper-summarize sources/2024-smith.pdf llm-edu
# → đọc note trong Obsidian, sửa "Đánh giá của tôi"

/paper-atomize SecondBrain/10_Projects/llm-edu/sources/2024-smith-llm.md
# → chọn atomic muốn tạo

/link-notes <các atomic vừa tạo>
```

### Source #2 trở đi — full workflow

```
/paper-full sources/2024-stratechery-ai.html llm-edu
```

## Triết lý thiết kế

1. **Luôn có điểm dừng** — agent không tự ý làm xong, luôn chờ duyệt ở mốc quan trọng
2. **Template thích nghi theo loại nguồn** — paper tóm khác blog, blog khác sách
3. **Không xóa, chỉ di chuyển**
4. **Không bịa** — thiếu info → ghi "Không tìm thấy"
5. **Tiếng Việt mặc định**

## Thêm command mới

Tạo file `.md` trong cùng folder:

```markdown
---
description: Mô tả ngắn (hiện trong menu /)
argument-hint: <cú-pháp-args>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Tên command

Hướng dẫn cho Claude (tiếng Việt).
Dùng $1, $2 cho args, $ARGUMENTS cho toàn bộ.
```

## Khi nào sửa các file này?

Sau **mỗi nguồn xử lý**, ghi friction log vào daily note:
- Command/agent có hỏi sai gì không?
- Output có chỗ nào lệch chuẩn bạn muốn?
- Cấu trúc tóm tắt cho loại nguồn này có đủ không?

Cuối tuần 1: mở file `.md` ra, sửa trực tiếp. **Bộ command + agent sống**, không cố định.

## Phụ lục: troubleshooting

**Claude Code không thấy command mới?**
→ Khởi động lại `claude` (Ctrl+C, gõ lại `claude`)

**Agent researcher không xuất hiện?**
→ Kiểm tra file ở `E:\Claude\.claude\agents\researcher.md` (không phải `commands\`)
→ Gõ `/agents` trong claude để xem danh sách

**Convert DOCX/EPUB lỗi?**
→ Cài pandoc: `winget install pandoc`
→ Hoặc copy nội dung paste vào file `.txt` rồi xử lý

**Agent đặt tên file kỳ cục?**
→ Gõ `?` để xem phương án khác
→ Hoặc gõ thẳng tên bạn muốn
→ Cuối tuần sửa quy tắc trong `paper-summarize.md` mục "Công thức tên"
