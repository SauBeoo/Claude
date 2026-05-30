---
type: method
created: 2026-05-30
tags: [claude, ai-fluency, prompting]
status: seed
---

# Cách iterate với AI bằng feedback cụ thể

Coi câu trả lời đầu tiên của AI như **bản nháp của một đồng nghiệp junior**: đã có khung, bạn không phải bắt đầu từ con số 0, nhưng cần feedback để hoàn thiện. Bí quyết: đừng vứt đi viết lại từ đầu (Claude nhớ cả hội thoại — vứt đi là mất hết context), mà tinh chỉnh bằng feedback *cụ thể*.

## Khi nào dùng

Mỗi khi output chưa ưng ý nhưng đã gần đúng — thay vì xoá và mở chat mới.

## Các bước

1. **Chỉ rõ CHỖ** sai/yếu (đoạn nào, câu nào, số nào).
2. **Nói cách SỬA** thành cái gì cụ thể.
3. **Thêm ràng buộc** độ dài / format nếu lỗi là "lan man" hoặc "sai cấu trúc".

So sánh:

| ❌ Yếu (AI phải đoán) | ✅ Mạnh (AI biết làm gì) |
|---|---|
| "Ngắn hơn đi" | "Cắt 2 đoạn đầu; kết viết theo hướng hành động" |
| "Sửa lại đi" | "Giá ở đoạn 2 sai, phải là 4.99$; sửa và tính lại margin" |
| "Chi tiết hơn" | "Thêm 2 ví dụ `curl`; phần chức năng rút còn 3–5 bullet" |

## Lưu ý/cạm bẫy

- "Cụ thể hơn đi" cũng là feedback *yếu* — vì chính nó không cụ thể.
- **Trần 3–5 lần iterate.** Quá đó mỗi lần chỉ tinh chỉnh ~5% → thà tự sửa tay. Dấu hiệu nên *restart*: >15 message và AI lặp lại chính nó, hoặc chủ đề đã trôi quá xa.
- Trước khi restart: bảo AI "tóm tắt context chat này thành 5 bullet" để mang sang chat mới — giữ context, vứt phần rối.

## Ví dụ thực tế

Bản nháp mô tả API endpoint bị dài dòng & thiếu ví dụ → feedback mạnh: "Thiếu ví dụ — thêm 2 ví dụ `curl`. Phần chức năng lan man, rút còn 3–5 bullet. Input/output trình bày dạng bảng. Toàn bài ≤ 250 từ."

## Liên hệ

- [[4d-framework-ai-fluency]] — đây là kỹ năng cho chữ D "Description"
- [[output-troi-chay-khong-dong-nghia-dung]] — iterate xong vẫn phải thẩm định trước khi ship

## Nguồn

- Khoá Claude 101 (Anthropic Academy) — bài 1.3, mục "Iteration Mindset"
