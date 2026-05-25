---
description: Archive 1 project từ 10_Projects sang 40_Archive sau khi chạy đủ checklist (≥3 atomic, post-mortem, README DONE, outputs)
argument-hint: <ten-project> (vd: claude-code-101)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Archive Project — chuyển project xong sang 40_Archive

Sử dụng agent **librarian**. Trả lời bằng tiếng Việt.

## Quy tắc bất biến

- ❌ KHÔNG `rm` — chỉ `mv` (PowerShell `Move-Item`).
- ❌ KHÔNG move khi checklist chưa pass — phải báo cáo lý do, chờ user xác nhận skip hay fix.
- ✅ Trước khi move, **bắt buộc** ghi entry vào `99_Meta/CHANGELOG.md`.
- ✅ Update README của project: `status: DONE — YYYY-MM-DD` trước khi move.

## Đầu vào

- Tên project: `$1` (vd: `claude-code-101`)
- Path nguồn: `E:\Claude\SecondBrain\10_Projects\$1\`
- Path đích: `E:\Claude\SecondBrain\40_Archive\<năm-hiện-tại>\$1\`

Nếu `$1` rỗng hoặc folder không tồn tại → in lỗi, dừng. KHÔNG đoán project name.

## Việc cần làm

### Phase 1: Pre-flight (DỪNG nếu fail)

1. Verify `10_Projects/$1/` tồn tại. Không có → báo lỗi, dừng.
2. Verify `40_Archive/<năm>/` tồn tại. Không có → tạo bằng `New-Item -ItemType Directory`.
3. Đọc `10_Projects/$1/README.md` lấy: status hiện tại, mô tả 1 dòng, deadline (nếu có).

### Phase 2: Checklist (báo cáo, KHÔNG move)

Chạy 4 check và trình bày bảng:

| # | Check | Trạng thái | Chi tiết |
|---|---|---|---|
| 1 | ≥3 atomic notes liên quan project? | ✅/❌ | List slug atomic match (grep `[[$1` hoặc `source.*$1` trong `50_Atomic/**/*.md`) |
| 2 | Có `post-mortem.md` trong project? | ✅/❌ | File tồn tại không |
| 3 | README có `status: DONE — <ngày>` không? | ✅/❌ | Đọc frontmatter README |
| 4 | Outputs cuối cùng trong `outputs/`? | ✅/❌ | List file `.md` trong `outputs/` |

**Highlight:**
- ✅ Pass all → sang Phase 3.
- ❌ Có check fail → liệt kê cụ thể, đề xuất action fix (vd: "Cần tạo `post-mortem.md` trước — muốn tôi mở template không?"). DỪNG chờ user.

### Phase 3: Đề xuất move (DỪNG chờ duyệt)

Khi checklist pass (hoặc user xác nhận skip một số check), trình bày:

```
Đề xuất archive:
  From: E:\Claude\SecondBrain\10_Projects\$1\
  To:   E:\Claude\SecondBrain\40_Archive\<năm>\$1\

Trước khi move sẽ làm:
  1. Update README frontmatter: status: DONE — <YYYY-MM-DD>
  2. Append entry vào 99_Meta/CHANGELOG.md
  3. Move folder (Move-Item, không copy)

Xác nhận? (yes / sửa lại / hủy)
```

### Phase 4: Thực thi (chỉ khi user duyệt)

Theo thứ tự:

1. **Update README**: dùng `Edit` đổi `status: <cũ>` → `status: DONE — <hôm nay>` trong frontmatter `10_Projects/$1/README.md`. Nếu README chưa có field `status` → thêm vào frontmatter.

2. **Log CHANGELOG**: append entry vào `99_Meta/CHANGELOG.md` với format:

   ```markdown
   ## YYYY-MM-DD — Archive project `$1`

   **Bối cảnh:** project hoàn thành, chuyển sang 40_Archive theo quy trình `/archive-project`.

   ### 📦 Archive

   | File | Thay đổi | Lý do |
   |---|---|---|
   | `10_Projects/$1/README.md` | `status: <cũ>` → `status: DONE — <ngày>` | Đánh dấu hoàn thành trước khi archive |
   | `10_Projects/$1/` → `40_Archive/<năm>/$1/` | Move toàn bộ thư mục | Project xong, lưu kho |

   **Atomic notes đã chắt lọc từ project (sống tiếp ở 50_Atomic/):**
   - [[<slug-atomic-1>]]
   - [[<slug-atomic-2>]]
   - ...

   **Outputs cuối cùng (trong `40_Archive/<năm>/$1/outputs/`):**
   - <file-1.md>
   - <file-2.md>
   ```

3. **Move folder**: dùng `Bash` chạy `Move-Item` (PowerShell):

   ```powershell
   Move-Item -Path "E:\Claude\SecondBrain\10_Projects\$1" -Destination "E:\Claude\SecondBrain\40_Archive\<năm>\"
   ```

   Lưu ý: dùng PowerShell vì shell mặc định là PowerShell. KHÔNG dùng `mv` Unix.

4. **Verify**: chạy `Test-Path` cả nguồn (phải false) và đích (phải true). Nếu sai → báo cáo, không tự rollback (chờ user).

### Phase 5: Báo cáo cuối

```
✅ Archive xong: $1

  📁 Nguồn: 10_Projects/$1/  → đã rỗng (verify Test-Path = False)
  📦 Đích:  40_Archive/<năm>/$1/  → tồn tại (Test-Path = True)
  📜 CHANGELOG: đã ghi entry <ngày>
  ⚛️ Atomic notes link ngược về project: <N> note (không broken nhờ giữ nguyên slug)

⚠️ Cần làm thủ công:
  - Update [[00_HOME]] section "Đang làm" — xóa `$1` khỏi Project active
  - Update MOC liên quan nếu cần (Mở thấy link `[[10_Projects/$1/...]]` thì sửa thành `[[40_Archive/<năm>/$1/...]]`)
```

## Lỗi thường gặp

- **Atomic count = 0**: project chưa chắt lọc — gợi ý chạy `/paper-atomize` trước khi archive.
- **Đường dẫn có khoảng trắng**: luôn quote bằng `"..."` trong PowerShell.
- **Đã tồn tại `40_Archive/<năm>/$1/`**: cảnh báo (project trùng tên?), KHÔNG tự overwrite.
