---
description: Tạo/mở daily note hôm nay với template chuẩn
argument-hint: (không cần argument)
allowed-tools: Read, Write, Edit, Glob
---

# Daily Note

Trả lời bằng tiếng Việt.

## Việc cần làm

1. Lấy ngày hôm nay format `YYYY-MM-DD`
2. Path: `E:\Claude\SecondBrain\60_Daily\<YYYY>\<MM>\<YYYY-MM-DD>.md`
   (Tạo thư mục `<YYYY>\<MM>` nếu chưa có)

### Nếu file CHƯA tồn tại:

Đọc template `E:\Claude\SecondBrain\99_Meta\templates\daily.md` và tạo file mới với các placeholder đã thay:
- `{{date:YYYY-MM-DD}}` → ngày hôm nay
- `{{date:dddd, DD/MM/YYYY}}` → thứ + ngày tiếng Việt (vd: `Friday, 23/05/2026`)

**Không tự bịa template** — luôn dùng template ở `99_Meta/templates/daily.md` làm nguồn duy nhất. Nếu template thay đổi, command này tự khớp theo.

### Nếu file ĐÃ tồn tại:

- KHÔNG ghi đè
- In nội dung hiện tại
- Hỏi: "File daily hôm nay đã có. Muốn (a) thêm entry, (b) chỉ xem, (c) tạo entry mới ở section nào?"

## Sau khi xử lý

In path file để tôi mở trong Obsidian.

## Lưu ý cho command khác

Các section chuẩn trong daily (theo template hiện tại):
- `## 🎯 3 việc quan trọng nhất hôm nay`
- `## 📥 Quăng vào (mọi thứ chợt nghĩ trong ngày)`
- `## 💡 Ý tưởng đáng nhớ`
- `## 📚 Đã chắt lọc` — `/paper-full` Phase 3 append vào đây
- `## 🔚 Cuối ngày: nhìn lại`

Command khác (như `/paper-full`) khi append vào daily PHẢI dùng đúng tên section ở trên.
