# 50_Atomic — Trái tim của bộ não 2

Đây là nơi tri thức **đã chín** sống. Mỗi note ở đây là 1 viên gạch độc lập, liên kết với các viên gạch khác qua `[[wiki-link]]`.

## 4 quy tắc của Atomic Note

1. **1 note = 1 ý duy nhất.** Không phải 1 paper. Không phải 1 buổi học. Một ý.
2. **Đứng độc lập.** Đọc note này không cần đọc thêm thứ gì khác cũng hiểu.
3. **Viết bằng lời của bạn.** Không copy nguyên văn từ nguồn — nếu copy thì để trong block trích dẫn `>`.
4. **Có nhiều liên kết.** Mỗi note nên có 2-5 link đến note khác. Đây là sức mạnh thật sự.

## 4 loại note

| Thư mục | Loại | Tiêu đề bắt đầu bằng |
|---|---|---|
| `concepts/` | Khái niệm — "X là gì?" | Tên khái niệm |
| `claims/` | Luận điểm có thể tranh luận | Câu khẳng định |
| `methods/` | Phương pháp — "Cách làm X" | "Cach-" hoặc verb |
| `questions/` | Câu hỏi mở chưa trả lời được | Câu hỏi |

## Quy ước đặt tên file

`<slug-khong-dau-noi-bang-gach-ngang>.md`

✅ Đúng:
- `self-attention-la-weighted-sum.md`
- `cach-viet-abstract-thu-hut.md`
- `lieu-llm-co-thuc-su-hieu-ngon-ngu.md`

❌ Sai:
- `Self Attention.md` (có khoảng trắng, có hoa)
- `tự chú ý là gì.md` (có dấu — wiki-link sẽ phiền)

Tên file = link, nên ngắn, không dấu, không khoảng trắng.

## Cấu trúc 1 atomic note

```markdown
---
type: concept | claim | method | question
created: 2026-05-23
tags: [chủ-đề-1, chủ-đề-2]
status: seed | growing | evergreen
---

# Tiêu đề tự nhiên (có dấu, có hoa)

(1-3 đoạn ngắn, mỗi đoạn 2-4 câu)

## Liên hệ

- [[note-lien-quan-1]] — vì sao liên quan
- [[note-lien-quan-2]] — vì sao liên quan

## Nguồn

- [[10_Projects/claude-code-101/sources/2026-claude-code-101-quan-ly-context]]
- [Link bên ngoài nếu có]
```

## Status (trạng thái trưởng thành)

- **seed** 🌱 — vừa gieo, ý tưởng còn thô
- **growing** 🌿 — đã suy nghĩ thêm, có liên kết
- **evergreen** 🌳 — đã chín, dùng được để viết bài/dạy/làm video

Định kỳ (vd: mỗi tháng) review các seed → growing → evergreen.

## Workflow điển hình

1. Đọc paper trong `00_Inbox/paper-chua-doc/`
2. Tóm tắt vào `10_Projects/<project>/papers/<paper>.md`
3. **Trong khi tóm tắt**, nảy ra ý hay → tạo atomic note ở đây với status `seed`
4. Tháng sau review, mở rộng → `growing`
5. Khi dùng được để viết content/bài giảng → `evergreen`
