---
description: Quét 50_Atomic/, tìm atomic chưa được index vào MOC, đề xuất cập nhật (chạy định kỳ)
argument-hint: (không cần argument)
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Cập nhật MOC — quét batch

Sử dụng agent **librarian**. Trả lời bằng tiếng Việt.

Dùng khi: cuối tuần / định kỳ muốn đảm bảo mọi atomic đều có "nhà" trong MOC. Khác với `/paper-atomize` (chạy on-the-fly cho atomic mới), lệnh này quét toàn bộ.

## Việc cần làm

### Bước 1: Inventory

1. Quét toàn bộ atomic: `Glob` `E:\Claude\SecondBrain\50_Atomic\**\*.md` (bỏ folder note `50_Atomic.md`).

2. Với mỗi atomic, đọc frontmatter, lấy:
   - `type` (concept/claim/method/question)
   - `tags`
   - Tên file (không có `.md`)

3. Quét toàn bộ MOC: `Glob` `E:\Claude\SecondBrain\99_Meta\MOCs\*.md`.

4. Với mỗi MOC, đọc:
   - `tags:` frontmatter
   - Toàn bộ wiki links `[[...]]` trong nội dung — đây là tập atomic đã được index

### Bước 2: Tìm orphan

Với mỗi atomic, kiểm tra: tên atomic có xuất hiện trong `[[...]]` của bất kỳ MOC nào không?
- Có → đã index, bỏ qua
- Không → là **orphan**, đưa vào danh sách cần xử lý

### Bước 3: Match orphan với MOC

Với mỗi orphan, dùng **logic tag overlap** (giống `/paper-atomize` Phase 3):
- Lấy tags của atomic
- Match với `tags:` frontmatter của MOC (bỏ qua tag chung `moc`)
- Ưu tiên MOC có nhiều tag trùng nhất

Phân loại orphan thành 2 nhóm:
- **Nhóm A — có MOC khớp**: gợi ý append vào MOC nào
- **Nhóm B — không MOC nào khớp**: gợi ý tạo MOC mới (group các orphan cùng tag chính)

### Bước 4: Trình bày đề xuất

```
## Báo cáo orphan

Đã quét: <X> atomic, <Y> MOC.
Atomic đã index: <Z>
Atomic orphan: <N>

## Nhóm A — append vào MOC có sẵn

### [[ML-MOC]]
1. [[<atomic-1>]] (type: concept) → section "🌱 Khái niệm nền tảng"
2. [[<atomic-2>]] (type: method) → section "🛠️ Phương pháp & kỹ thuật"

### [[claude-code-MOC]]
3. [[<atomic-3>]] (type: method) → section "🛠️ Phương pháp & kỹ thuật"

## Nhóm B — không MOC nào khớp, đề xuất tạo mới

### MOC mới: `affiliate-MOC.md`
- Tag chính: affiliate, mindset
- Atomic sẽ index:
  4. [[chi-toi-uu-nhung-gi-trong-tam-kiem-soat]] (concept)
  5. [[lead-la-tai-san-dai-han]] (concept)

### MOC mới: `systems-thinking-MOC.md`
- Tag chính: systems-thinking
- Atomic sẽ index:
  6. [[<atomic-x>]] (concept)
```

### Bước 5: DỪNG LẠI chờ duyệt

Hỏi tôi:
```
Áp dụng đề xuất nào?
- 'tất cả' — append hết nhóm A, tạo hết nhóm B
- 'nhóm A' — chỉ append vào MOC có sẵn
- 'nhóm B' — chỉ tạo MOC mới
- '1,3,5' — chọn số cụ thể (theo số trong báo cáo)
- 'bỏ qua' — không làm gì
```

### Bước 6: Thực thi

**Mapping type → section trong MOC** (giống `/paper-atomize`):
- `concept` → `## 🌱 Khái niệm nền tảng`
- `method` → `## 🛠️ Phương pháp & kỹ thuật`
- `claim` → `## 💭 Luận điểm đáng tranh luận`
- `question` → `## ❓ Câu hỏi mở`

**Append vào MOC có sẵn**:
- Dùng `Edit` thêm dòng `- [[<atomic>]] — <1 câu mô tả lấy từ heading H1 của atomic>` ngay dưới heading section đúng
- Nếu section chỉ có `*(chưa có)*` → thay thế bằng dòng mới
- Cập nhật frontmatter `updated: <ngày hôm nay>`

**Tạo MOC mới**: dùng skeleton:

```markdown
---
type: moc
topic: <topic>
updated: <YYYY-MM-DD>
tags: [moc, <tag1>, <tag2>]
status: active
---

# 🗺️ <Topic> — Map of Content

## 🌱 Khái niệm nền tảng
- *(chưa có)*

## 🛠️ Phương pháp & kỹ thuật
- *(chưa có)*

## 💭 Luận điểm đáng tranh luận
- *(chưa có)*

## ❓ Câu hỏi mở
- *(chưa có)*

## 📚 Tài liệu tham khảo
- *(chưa có)*

---

**Cách dùng MOC này:** Mọi atomic/resource liên quan <topic> → thêm link vào đúng section.
```

Sau đó append từng atomic vào section tương ứng.

### Bước 7: Báo cáo cuối

```
✅ Cập nhật xong:
- 🗺️ <M> MOC đã cập nhật: [[MOC-1]], [[MOC-2]]
- 🆕 <K> MOC mới tạo: [[MOC-mới-1]]
- ⚛️ <N> atomic đã được index
- ⚠️ <P> atomic vẫn orphan (nếu user bỏ qua 1 số đề xuất) — list ra
```
