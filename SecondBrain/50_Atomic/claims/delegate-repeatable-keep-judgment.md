---
type: claim
created: 2026-05-30
tags: [claude, ai-fluency, delegation]
status: seed
confidence: high
---

# Luận điểm: Giao AI việc lặp lại, giữ lại việc cần phán xét

Hãy giao cho AI những việc *có pattern, làm đi làm lại, kiểm tra được* (format, tổng hợp, phân loại, bản nháp đầu). Giữ lại cho mình những việc *cần phán xét và trách nhiệm* (chiến lược, quyết định nhân sự, giá trị đạo đức). Quy tắc nhanh: **nếu làm sai mà bạn là người chịu trách nhiệm, thì bạn phải review trước khi ship.**

## Lập luận ủng hộ

- AI mạnh ở việc có khuôn mẫu và output đối chiếu được với ground truth; yếu ở việc cần context riêng tư + chịu trách nhiệm.
- Mẹo thử: "Nếu một senior trong team làm giúp 60% việc này, tôi có OK không?" — OK thì đó là ứng viên để giao AI.
- Giữ phần judgment lại chính là cách cài "checkpoint" an toàn (vd: AI đề xuất sửa code nhưng người quyết fix nào được nhận).

## Lập luận phản biện

- Ranh giới "execution vs judgment" đôi khi mờ — một số việc lặp lại vẫn ẩn chứa phán xét tinh tế, cần thử mới biết.
- Khi AI ngày càng giỏi, vùng "nên giao" sẽ mở rộng — quy tắc cần xem lại định kỳ.

## Quan điểm của tôi

Tin cao. Đây là kim chỉ nam cho chữ D "Delegation". Nó cũng giải thích vì sao Claude Code mặc định xin phép trước khi đụng file: giao execution, giữ judgment.

## Liên hệ

- [[4d-framework-ai-fluency]] — quy tắc cho chữ D "Delegation"
- [[delegation-diligence-loop]] — cách kiểm chứng một việc *có thật sự* giao được không

## Nguồn

- Trích từ: [[claude-101-anthropic-academy]]
- Khoá Claude 101 (Anthropic Academy) — bài 1.0 & 1.3 ("Delegate what's repeatable, keep what needs judgment")
