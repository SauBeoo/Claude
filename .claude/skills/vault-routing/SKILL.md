---
name: vault-routing
description: Sử dụng skill này khi cần phân loại file/note mới vào đúng thư mục trong vault SecondBrain (PARA + Atomic). Trigger khi user nói "lưu vào bộ não", "đặt note này ở đâu", "phân loại file này", hoặc khi tạo note mới mà chưa rõ đích.
---

# Skill: Vault Routing

Phân loại note vào đúng thư mục theo PARA + Atomic.

## Khi nào dùng

- User download file mới (paper, screenshot, voice memo)
- User viết ghi chú trong chat và muốn lưu lại
- Khi cần move file từ Inbox đi đâu khác
- Khi tạo atomic note mới

## Bảng quyết định

| Đặc điểm note | Đích |
|---|---|
| Không chắc, vừa nhận | `00_Inbox/` |
| Paper PDF chưa đọc | `00_Inbox/paper-chua-doc/` |
| Paper đã tóm tắt, gắn project | `10_Projects/<project>/papers/` |
| Paper tóm tắt, không gắn project | `00_Inbox/paper-chua-doc/` (chờ phân loại sau) |
| Ghi chú họp/meeting | `10_Projects/<project>/meetings/` |
| Ý tưởng/note nhanh | `00_Inbox/y-tuong-chot/` |
| Daily journal | `60_Daily/<năm>/<tháng>/YYYY-MM-DD.md` |
| Kinh nghiệm dạy học | `20_Areas/teaching/` |
| Kinh nghiệm coding | `20_Areas/coding-practices/` |
| Kinh nghiệm nghiên cứu | `20_Areas/research-methodology/` |
| Kinh nghiệm làm content | `20_Areas/content-creation/` |
| Bài blog/video hay từ web | `30_Resources/<chủ-đề>/` |
| Cheatsheet/tài liệu kỹ thuật | `30_Resources/<lĩnh-vực>/` |
| Atomic concept | `50_Atomic/concepts/` |
| Atomic claim (luận điểm) | `50_Atomic/claims/` |
| Atomic method (cách làm) | `50_Atomic/methods/` |
| Atomic question (câu hỏi mở) | `50_Atomic/questions/` |
| MOC (Map of Content) | `99_Meta/MOCs/` |
| Project xong | `40_Archive/<năm>/<project>/` |

## Quy trình

1. Đọc nội dung note
2. Xác định:
   - Có gắn với project cụ thể không? → 10_Projects
   - Là kinh nghiệm bản thân không? → 20_Areas
   - Là tham khảo từ người khác? → 30_Resources
   - Là ý tưởng độc lập đáng nhớ? → 50_Atomic
3. Nếu không chắc → đề xuất 2 phương án, hỏi user
4. **Không tự move** — đề xuất path, đợi user xác nhận

## Quy ước tên file

- Slug không dấu, gạch ngang: `cach-doc-paper-hieu-qua.md`
- Daily: `YYYY-MM-DD.md`
- Project folder: `<loại>-<chủ-đề>-<thời-gian>` (vd: `research-llm-education-2026`)

## Ví dụ

User: "Tôi vừa đọc bài blog của Karpathy về training LLM, lưu vào bộ não"

Response:
```
Đề xuất đích: 30_Resources/machine-learning/karpathy-training-llm-blog.md
Lý do: Tham khảo từ người khác, chủ đề ML. Không phải kinh nghiệm bạn tự đúc kết.
Tạo file ở đó OK?
```
