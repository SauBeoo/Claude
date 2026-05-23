# .claude-global — Cấu hình Claude Code toàn cục

Đây là bộ agents và skills toàn cục cho Claude Code. Đặt ở `~/.claude/` để mọi project đều dùng được.

## Cài đặt trên Windows

```powershell
# 1. Tạo thư mục .claude trong home (nếu chưa có)
mkdir $HOME\.claude

# 2. Copy nội dung của thư mục này vào đó
# Đổi <đường-dẫn-folder-này> thành đường dẫn thực tế
xcopy /E /I .\* $HOME\.claude\

# 3. Verify
ls $HOME\.claude
# Expected: CLAUDE.md, agents/, skills/
```

Hoặc dùng PowerShell:
```powershell
Copy-Item -Recurse -Force .\* $HOME\.claude\
```

## Cài đặt trên macOS/Linux

```bash
mkdir -p ~/.claude
cp -r ./* ~/.claude/
ls ~/.claude
```

## Cấu trúc

```
~/.claude/
├── CLAUDE.md              # Quy tắc khung toàn cục
├── agents/                # 5 agents
│   ├── researcher.md
│   ├── teacher.md
│   ├── coder.md
│   ├── creator.md
│   └── librarian.md
└── skills/                # 5 skills
    ├── vault-routing/SKILL.md
    ├── summarize-pdf-paper/SKILL.md
    ├── create-atomic-note/SKILL.md
    ├── inbox-cleanup/SKILL.md
    └── find-related-notes/SKILL.md
```

## Cách dùng

### Gọi agent

Trong Claude Code session, gõ:
```
/agent researcher
```

Hoặc nhắc tự nhiên:
```
"Đeo mặt nạ researcher giúp tôi tóm tắt paper này"
```

### Skills tự động

Skills sẽ tự kích hoạt khi Claude phát hiện trigger trong câu hỏi. Ví dụ:
```
User: "Dọn inbox giúp tôi"
→ Claude tự gọi skill `inbox-cleanup`
```

Bạn không cần gọi skill bằng tên — chỉ cần mô tả việc cần làm.

## Tùy biến

- **Sửa agent:** mở `agents/<tên>.md`, sửa nội dung. Có hiệu lực ở session tiếp theo.
- **Thêm agent mới:** tạo file `agents/<tên-mới>.md` theo format có sẵn.
- **Sửa CLAUDE.md:** đây là quy tắc khung — sửa cẩn thận, ảnh hưởng mọi phiên làm việc.

## Hierarchy ưu tiên

Khi cùng 1 quy tắc bị định nghĩa nhiều nơi:

1. `./CLAUDE.md` trong project hiện tại (cao nhất)
2. `./.claude/CLAUDE.md` trong project
3. `~/.claude/CLAUDE.md` (file này, toàn cục)

Quy tắc trong project sẽ ghi đè toàn cục. Ví dụ, project nghiên cứu có thể quy định "luôn dùng IEEE citation style" — ghi đè quy tắc citation mặc định.

## Verify đã cài đúng

Mở Claude Code, gõ:
```
"Cho tôi xem các agent có sẵn"
```

Expected response: liệt kê 5 agent (researcher, teacher, coder, creator, librarian).

Nếu Claude không thấy → check lại path `~/.claude/agents/`.
