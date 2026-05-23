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

- `researcher` — đọc paper, tóm tắt, đề xuất atomic notes
- `teacher` — soạn bài giảng, đề thi, feedback sinh viên
- `coder` — review code, refactor, viết test
- `creator` — content video, bài blog, kịch bản
- `librarian` — quản lý vault: dọn Inbox, chắt lọc atomic, archive

## Skills có sẵn

Đặt ở `~/.claude/skills/`. Claude tự gọi khi phát hiện phù hợp:

- `vault-routing` — phân loại file mới vào đúng PARA folder
- `summarize-pdf-paper` — tóm tắt paper theo template
- `create-atomic-note` — tạo atomic note với link tự động
- `inbox-cleanup` — dọn Inbox, đề xuất phân loại
- `find-related-notes` — tìm note liên quan trong vault trước khi viết mới

## Khi vault và project tương tác

- Code/coding-knowledge → `SecondBrain\20_Areas\coding-practices\`
- Paper liên quan project research → `SecondBrain\10_Projects\<project>\papers\`
- Bài học chung không gắn project → `SecondBrain\20_Areas\` hoặc `30_Resources\`

Mỗi project repo nên có `CLAUDE.md` riêng chỉ rõ vault path tương ứng.
