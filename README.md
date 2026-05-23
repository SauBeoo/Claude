# E:\Claude\ — Hệ thống làm việc của tôi

Workspace tổng hợp gồm bộ não 2 (SecondBrain) + project repos (Projects) + cấu hình Claude Code (.claude-global).

## 📂 Cấu trúc

```
E:\Claude\
│
├── SecondBrain\              # 🧠 Bộ não 2 — vault Obsidian
│   ├── 00_Inbox\             # Vùng đệm
│   ├── 10_Projects\          # Note về project đang chạy
│   ├── 20_Areas\             # Kinh nghiệm dài hạn
│   ├── 30_Resources\         # Tham khảo theo chủ đề
│   ├── 40_Archive\           # Đã hoàn thành
│   ├── 50_Atomic\            # Ý tưởng đã chắt lọc ⭐
│   ├── 60_Daily\             # Daily note
│   └── 99_Meta\              # Template, MOC
│
├── Projects\                 # 💻 Code repos
│   ├── research-llm-education-2026\   # Project nghiên cứu
│   └── student-grade-app\             # Project sản phẩm
│
└── .claude\           # ⚙️ Cấu hình Claude Code
    ├── CLAUDE.md
    ├── agents\               # 5 agents (researcher, teacher, coder, creator, librarian)
    └── skills\               # 5 skills
```

**Lưu ý:** `.claude-global\` ở đây chỉ là **bản copy để bạn đọc**. Cài đặt thật phải copy vào `C:\Users\<tên-bạn>\.claude\` thì Claude Code mới nhận.

## 🚀 Bước cài đặt

### 1. Giải nén/copy vào E:\Claude\

```powershell
# Đặt 3 thư mục SecondBrain, Projects, .claude-global vào E:\Claude\
```

### 2. Install cấu hình Claude

```powershell
# Copy nội dung .claude-global\ vào ~/.claude/
mkdir $HOME\.claude -Force
Copy-Item -Recurse -Force E:\Claude\.claude-global\* $HOME\.claude\
```

### 3. Mở vault trong Obsidian

- Mở Obsidian → "Open folder as vault" → chọn `E:\Claude\SecondBrain\`
- Settings → Templates → Template folder: `99_Meta/templates`
- Settings → Daily notes → New file location: `60_Daily/YYYY/MM`

### 4. Init Git cho từng repo (tùy chọn)

```powershell
# Vault (private repo)
cd E:\Claude\SecondBrain
git init
git add .
git commit -m "init: vault structure"

# Project research
cd E:\Claude\Projects\research-llm-education-2026
git init
git add .
git commit -m "init: project skeleton"

# Project app
cd E:\Claude\Projects\student-grade-app
git init
git add .
git commit -m "init: project skeleton"
```

### 5. Test Claude Code

```powershell
cd E:\Claude\SecondBrain
claude
# Trong session, gõ:
> "Liệt kê các agent có sẵn"
```

Expected: Claude liệt kê 5 agent (researcher, teacher, coder, creator, librarian).

## 🎯 Workflow cơ bản

### Khi đọc paper

```
cd E:\Claude\Projects\research-llm-education-2026
claude
> "Tóm tắt paper trong D:\Downloads\new-paper.pdf"
```

Claude (đeo mặt nạ researcher) tóm tắt → lưu vào `SecondBrain\10_Projects\research-llm-education-2026\papers\` → đề xuất atomic notes.

### Khi soạn bài giảng

```
cd E:\Claude\SecondBrain
claude
> "/agent teacher
> Soạn buổi 9 môn Python về Debug"
```

Claude tìm atomic notes liên quan trong vault → tạo lecture note với link tham khảo.

### Khi code

```
cd E:\Claude\Projects\student-grade-app
claude
> "Review hàm calculate_gpa() trong app/services/grade.py"
```

Claude (đeo mặt nạ coder) review. Sau khi xong:
```
> "Lưu kinh nghiệm này vào bộ não"
```
→ Tạo note ở `SecondBrain\20_Areas\coding-practices\`.

### Khi dọn dẹp

```
cd E:\Claude\SecondBrain
claude
> "/agent librarian
> Dọn Inbox và đề xuất chắt lọc tuần này"
```

## 📚 Đọc thêm

- Cấu hình Claude: `.claude-global\README.md`
- Quy tắc vault: `SecondBrain\.claude\CLAUDE.md`
- Tag system: `SecondBrain\99_Meta\tag-system.md`
- Hướng dẫn từng thư mục vault: README.md trong mỗi thư mục
