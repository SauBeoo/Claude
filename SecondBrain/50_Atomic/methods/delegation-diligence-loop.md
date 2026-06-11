---
type: method
created: 2026-05-30
tags: [claude, ai-fluency, eval]
status: seed
---

# Cách dùng Delegation-Diligence Loop để tin AI có căn cứ

Bạn không bao giờ giao tay lái cho tài xế mới mà chưa thử. Bạn cho họ chạy một đoạn đường bạn đã thuộc lòng — chạy đúng đoạn đó thì mới tin giao đoạn lạ. Loop này làm y hệt với AI: cho nó làm lại một task bạn **đã từng tự làm và biết đáp án**, xem có tái tạo được không, rồi mới giao việc thật.

## Khi nào dùng

Khi bạn muốn giao AI một task quan trọng/lặp lại nhưng chưa biết nó có đáng tin cho *đúng task đó của mình* không (vd: phân tích số liệu khách hàng, review code, reconcile sổ sách).

## Các bước

1. **Chọn 1 task cụ thể** — không phải "AI phân tích data giúp tôi", mà "phân tích điểm danh vs. tỉ lệ có việc làm quý 2".
2. **Tìm data cũ có ground truth** — bản bạn đã làm tay, biết kết quả đúng. Đây là "đề có đáp án".
3. **Bảo AI làm lại** task cũ đó (prompt như khi làm thật).
4. **So output với đáp án** — đừng giả định đúng; soi đúng chỗ nào, sai/sót chỗ nào.
5. **Tinh chỉnh brief** — bổ sung context AI còn thiếu; ghi lại để lần sau.
6. **Thử câu khó hơn** để dò giới hạn → lặp lại bước 3, hoặc dừng (đã đủ tin / kết luận task không nên giao).

## Lưu ý/cạm bẫy

- **Mấu chốt: test trên data CŨ có đáp án, không phải data MỚI.** Không có ground truth thì "kiểm tra" cũng chỉ là tin bằng cảm giác.
- Cả 2 kết cục đều có giá trị: tái tạo được → có quy trình đã kiểm chứng; không được → biết để khỏi giao (tránh sai lầm đắt đỏ).
- Validate xong vẫn phải sanity-check mỗi output mới — niềm tin không bao giờ là 100%.

## Ví dụ thực tế

Muốn biết đề xuất sửa code của Claude có đáng tin không → đưa nó một bug mình đã từng tự fix, xem nó có chỉ đúng chỗ + đúng cách không. Làm vài lần sẽ biết *loại* lỗi nào nó bắt tốt, loại nào hay "nghe hợp lý mà sai".

## Liên hệ

- [[output-troi-chay-khong-dong-nghia-dung]] — vấn đề mà loop này giải quyết
- [[4d-framework-ai-fluency]] — loop vận hành 2 chữ D: Discernment + Diligence

## Nguồn

- Trích từ: [[claude-101-anthropic-academy]]
- Khoá Claude 101 (Anthropic Academy) — bài 1.3, case study Rio (Valley Veterans Services)
