---
type: claim
created: 2026-05-30
tags: [claude, ai-fluency, hallucination]
status: seed
confidence: high
---

# Luận điểm: AI trả lời "trôi chảy" không đồng nghĩa với "đúng"

Một AI giỏi viết có thể nói sai một con số quan trọng mà giọng văn vẫn mượt như thật — gọi là *hallucination*. Câu chữ hay không phải bằng chứng của sự thật; nó chỉ là bằng chứng AI viết tốt. Tin vào độ trôi chảy giống như tin một người ăn nói lưu loát chỉ vì họ nói hay.

## Lập luận ủng hộ

- AI sinh chữ theo xác suất "câu nào nghe hợp lý", không theo "câu nào kiểm chứng được" — nên nó có thể bịa fact, ngày tháng, citation rất thuyết phục.
- Muốn biết đúng/sai phải *thẩm định* (Discernment): đối chiếu con số với nguồn tin cậy, click thử citation, hỏi giả định.
- Mà thẩm định chỉ có nghĩa khi có **cái để đối chiếu** (ground truth). Không có ground truth thì "kiểm tra lại" cũng chỉ là tin bằng cảm giác.

## Lập luận phản biện

- Với task rủi ro thấp (brainstorm, nháp nội bộ), trôi chảy "đủ dùng" — không phải lúc nào cũng cần thẩm định gắt.
- Bật web search / yêu cầu cite nguồn làm giảm hallucination đáng kể.

## Quan điểm của tôi

Tin cao. Mức độ thẩm định nên tỉ lệ với stakes: memo nội bộ ~20% thời gian review, sản phẩm gửi khách hàng = 100%.

## Liên hệ

- [[4d-framework-ai-fluency]] — đây là lý do tồn tại của chữ D "Discernment"
- [[delegation-diligence-loop]] — cách build niềm tin có căn cứ thay vì cảm tính

## Nguồn

- Khoá Claude 101 (Anthropic Academy) — bài 1.3, mục "5 common challenges" & "Diligence"
