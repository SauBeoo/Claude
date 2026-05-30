---
description: Tự viết daily hôm nay từ git activity + thay đổi trong vault
argument-hint: (không cần argument)
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Daily Write — tự viết nhật ký hôm nay

Trả lời bằng tiếng Việt.

> **Khác với `/daily`:** `/daily` chỉ tạo file rỗng từ template rồi chờ tôi điền.
> `/daily-write` **tự viết nội dung** 2 phần (Việc đã làm + Đã chắt lọc) dựa trên
> dữ liệu thật từ git và vault. Đây là ngoại lệ có chủ đích so với quy tắc
> "không tự điền daily" trong `SecondBrain/.claude/CLAUDE.md` — chỉ áp dụng cho command này.

## Bước 0 — Xác định file daily

1. Ngày hôm nay format `YYYY-MM-DD`.
2. Path: `E:\Claude\SecondBrain\60_Daily\<YYYY>\<MM>\<YYYY-MM-DD>.md`
3. **Nếu file CHƯA tồn tại:** đọc template `E:\Claude\SecondBrain\99_Meta\templates\daily.md`,
   tạo file mới (thay placeholder `{{date:YYYY-MM-DD}}` và `{{date:dddd, DD/MM/YYYY}}`).
   Tạo thư mục `<YYYY>\<MM>` nếu chưa có.
4. **Nếu file ĐÃ tồn tại:** đọc nội dung hiện tại, **không ghi đè** — sẽ merge ở Bước 3.

## Bước 1 — Thu thập tín hiệu (git + vault)

Chạy trong repo `E:\Claude` (repo này chứa cả vault SecondBrain). Dùng ngày hôm nay
làm mốc. Các lệnh tham khảo (chỉnh ngày cho đúng):

```bash
# Commit hôm nay (subject + hash)
git -C E:/Claude log --since="<YYYY-MM-DD> 00:00:00" --until="now" --pretty="- %s (%h)"

# File đã đổi qua các commit hôm nay (để phân loại)
git -C E:/Claude log --since="<YYYY-MM-DD> 00:00:00" --name-status --pretty="%h %s"

# Thay đổi CHƯA commit (staged + modified + untracked)
git -C E:/Claude status --porcelain
```

- `git status --porcelain`: cột `??` = file mới chưa track (atomic/paper mới hay nằm ở đây),
  `M`/`A` = đã sửa/thêm. Lấy hết để không bỏ sót.
- Nếu trong `E:\Claude\Projects\` có repo con riêng và bạn thấy dấu hiệu làm việc ở đó hôm nay,
  có thể `git -C` vào từng repo con để lấy commit — nhưng **ưu tiên repo `E:\Claude`** (đã phủ vault).

## Bước 2 — Phân loại tín hiệu

Gom file đã đổi/tạo hôm nay thành 3 nhóm:

| Nhóm | Đường dẫn nhận diện | Đưa vào section daily |
|---|---|---|
| **Sources đã xử lý** | `00_Inbox/paper-chua-doc/`, `10_Projects/*/sources/`, `10_Projects/*/papers/` | `📚 Đã chắt lọc → Sources` |
| **Atomic mới** | `50_Atomic/{concepts,claims,methods,questions}/` | `📚 Đã chắt lọc → Atomic mới` |
| **Việc khác** | Code trong `Projects/`, `.claude/` config, MOC, guide, template... | `🌙 EVENING → Việc xong / chưa xong` |

- Link dạng Obsidian: `[[<slug-không-đuôi-md>]]` (vd `[[self-attention-la-weighted-sum]]`).
- File mới (`??`/`A`) = "đã tạo"; file `M` của note cũ = "đã cập nhật" — ghi rõ để phân biệt.

## Bước 3 — Viết & merge vào daily

Chỉ điền **2 vùng**, các vùng còn lại **không động tới** (chúng là kế hoạch/quan điểm của tôi):

### a) `## 🌙 EVENING` → "Việc xong / chưa xong"
- Tổng hợp commit + việc khác thành 3–6 gạch đầu dòng ngắn gọn, tiếng Việt tự nhiên
  (không liệt kê hash thô trừ khi hữu ích).
- "Chưa xong": nếu `git status` còn nhiều thay đổi dở (file `M` chưa commit) → suy luận
  việc đang làm dở, ghi vào — nhưng **đánh dấu là suy đoán**.

### b) `## 📚 Đã chắt lọc` → "Sources:" và "Atomic mới:"
- Điền link `[[...]]` các source/atomic phát hiện ở Bước 2.

### Quy tắc merge (BẮT BUỘC — không phá nội dung tôi đã ghi)
1. Placeholder rỗng (dòng chỉ có `- ` hoặc trống) → **điền vào**.
2. Tôi đã ghi sẵn nội dung → **append xuống dưới**, không ghi đè.
3. Mọi dòng do command tự sinh thêm marker cuối dòng: ` _(auto)_`
   → để tôi biết dòng nào máy suy ra, dòng nào tự tôi viết. Nội dung suy đoán
   (không chắc chắn) thêm `⚠️` đầu dòng.
4. Tuyệt đối **không** chạm: "3 việc quan trọng hôm nay", "Quăng vào", "Ý tưởng đáng nhớ",
   "Bài học đáng nhớ" — đó là phần của tôi.
5. Nếu một nhóm rỗng (vd hôm nay không atomize) → để placeholder nguyên, đừng bịa.

## Bước 4 — Báo cáo

1. In path file để tôi mở trong Obsidian.
2. Tóm tắt: đã điền gì vào section nào, có suy đoán nào cần tôi xác nhận (`⚠️`),
   phần nào để trống chờ tôi tự viết.
3. **Không bịa**: nếu git/vault hôm nay không có hoạt động → nói thẳng "hôm nay
   không phát hiện activity nào", điền `-` và để tôi tự ghi.
