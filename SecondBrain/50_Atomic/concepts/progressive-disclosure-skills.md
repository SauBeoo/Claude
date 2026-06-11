---
type: concept
created: 2026-05-30
tags: [claude, skills, context-window]
status: seed
---

# Progressive disclosure — cách Skills nạp dần theo nhu cầu

Tưởng tượng một tủ sách dạy nghề: bạn chỉ cần đọc *gáy sách* để biết "có cuốn này tồn tại", chỉ rút ra đọc khi thực sự cần. Skills hoạt động y vậy — "hé lộ dần", không nạp tất cả một lúc:

1. **Lúc nghỉ (startup):** chỉ nạp **tên + mô tả** mỗi skill vào system prompt (~30–50 token/skill). Claude "biết có skill đó", chưa nạp nội dung.
2. **Khi khớp (match):** prompt của bạn khớp mô tả 1 skill → mới nạp **full SKILL.md** vào context.
3. **Nạp lồng (nested):** skill cần file phụ (`references/`, `assets/`, `scripts/`) → nạp/chạy tiếp khi cần.

Kết quả: **cài 50 skill mà context không phình.** Bằng chứng tận mắt: lệnh `/context` liệt kê hàng chục skill mà mỗi cái chỉ ~20–100 token — vì chúng mới ở bước 1.

Hệ quả thực hành: **`description` của skill là tối quan trọng** — nó là thứ *duy nhất* Claude thấy lúc nghỉ, nên quyết định skill có được đánh thức đúng lúc không. Description tồi = skill có cũng như không.

## Liên hệ

- [[projects-store-knowledge-skills-perform-tasks]] — Skill là cái "HOW"

## Nguồn

- Trích từ: [[claude-101-anthropic-academy]]
- Khoá Claude 101 (Anthropic Academy) — bài 1.7, "Cách Skills hoạt động — progressive disclosure"
