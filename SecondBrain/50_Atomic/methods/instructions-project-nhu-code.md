---
type: method
created: 2026-05-30
tags: [claude, projects, prompting]
status: seed
---

# Cách viết Project Instructions như code

Đừng coi instructions là "lời khuyên mơ hồ". Coi như **code** — Claude sẽ tuân theo nhất quán như một chương trình đã viết sẵn.

## Khi nào dù

Khi setup một Claude Project và muốn mọi chat trong đó hành xử nhất quán (tông, format, quy trình) mà không phải nhắc lại mỗi lần.

## Các bước

1. Viết instruction theo **4 phần**:
   - **Context** dự án (bạn là ai, project làm gì, audience).
   - **Process** (workflow): "IF tôi upload transcript → tạo summary theo template X".
   - **Tone & style**: cụ thể, không "hãy chuyên nghiệp" mà "viết như senior consultant — chắc chắn, không sáo rỗng".
   - **Ràng buộc cụ thể**: "< 200 từ", "luôn có CTA", "ALWAYS tránh từ: synergy, leverage".
2. Dùng cú pháp điều kiện như code: `IF ... THEN ...`, `ALWAYS ...`.
3. Đặt **tên file descriptive** trong knowledge base — Claude retrieve *bằng tên file*. `Q4-2025-Brand-Guidelines.pdf` ✅, `doc1.pdf` ❌.

## Lưu ý/cạm bẫy

- Instruction mơ hồ ("be professional") = Claude phải đoán → output lệch. Cụ thể luôn thắng.
- Knowledge base vs conversation: upload **≥2 lần / dùng lại** → knowledge base (mọi chat thấy); upload **1 lần / chỉ 1 chat** → để conversation-level.
- Kho >20 file → Claude tự bật **RAG** (chỉ kéo đoạn liên quan); không phải làm gì, capacity ~10x.
- Cập nhật knowledge base định kỳ (quý) — doc cũ → câu trả lời cũ.

## Ví dụ thực tế

Vault SecondBrain như một Project: instruction = các rule trong `CLAUDE.md` ("IF có tài liệu → chắt kiến thức tái dùng vào atomic, trung thực, viết ELI5"); knowledge base = template + MOC + atomic cũ; conversation-level = file PDF đang tóm tắt lúc này.

## Liên hệ

- [[projects-store-knowledge-skills-perform-tasks]] — Project là cái "WHAT"
- [[feedback-cu-the-khi-iterate-ai]] — cùng nguyên lý "cụ thể > mơ hồ"

## Nguồn

- Trích từ: [[claude-101-anthropic-academy]]
- Khoá Claude 101 (Anthropic Academy) — bài 1.5, "Add project instructions" & "RAG"
