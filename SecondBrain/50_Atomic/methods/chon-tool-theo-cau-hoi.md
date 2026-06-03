---
type: method
created: 2026-06-03
tags: [claude, research, enterprise-search, web-search, extended-thinking]
status: seed
---

# Cách chọn đúng tool cho đúng câu hỏi: Web search / Extended Thinking / Enterprise Search / Research

Tưởng tượng bạn cần đi lại: ra đầu ngõ thì đi bộ, sang quận khác thì xe máy, đi tỉnh thì xe khách, đi nước ngoài thì máy bay. Không ai bắt máy bay ra đầu ngõ — nhưng người mới dùng Claude hay "bắt máy bay" kiểu đó: bật Research 30 phút cho một câu hỏi tra 10 giây là xong.

## Khi nào dùng

Mỗi lần định hỏi Claude một câu cần thông tin — dừng 2 giây, phân loại câu hỏi trước.

## Các bước

1. **Quick fact, 1-2 nguồn là đủ?** → **Web search** (vài giây). Vd: tỷ giá hôm nay, địa chỉ công ty.
2. **Suy luận thuần, không cần info ngoài?** (debug logic, toán, phân tích) → **Extended Thinking**.
3. **Câu trả lời nằm trong knowledge NỘI BỘ công ty?** (policy, quyết định cũ, blocker của team) → **Enterprise Search** (~30 giây).
4. **Đa nguồn + cần report có cấu trúc + citation?** (so sánh vendor, market analysis, literature review) → **Research mode** (5-45 phút).

## Lưu ý/cạm bẫy

- Research cho quick fact = đợi 5 phút cho câu 10 giây. Ngược lại, web search cho việc cần 20 nguồn = kết quả nông.
- Research mà prompt mơ hồ = chờ 30 phút nhận report rác — đầu tư 3-5 phút craft prompt trước (xem [[nho-ai-draft-prompt-truoc-khi-research]]).
- Có thể kết hợp: Research + tắt web search = deep-research thuần nội bộ qua connectors.

## Ví dụ thực tế

"Quy trình xin nghỉ phép công ty + blocker của team Platform?" → Enterprise Search (nội bộ). "So sánh 5 LMS cho khóa học lập trình, report trình ban giám hiệu" → Research mode.

## Liên hệ

- [[chon-che-do-chat-cowork-code]] — anh em song sinh: kia chọn *môi trường làm việc*, đây chọn *công cụ tra cứu*
- [[claude-chi-thay-cai-ban-thay]] — Enterprise Search filter theo quyền của bạn
- [[delegate-repeatable-keep-judgment]] — Research cho input, quyết định vẫn là của bạn

## Nguồn

- Claude 101 — Bài 1.10: Research mode (decision tree + comparison matrix), Anthropic Academy, 2026
