---
type: method
created: 2026-06-08
tags: [claude, productivity, automation, use-case, roi]
status: seed
---

# Cách chấm điểm chọn use case đầu tiên để tự động hóa

Bạn vừa học một đống thứ hay ho và muốn áp dụng hết. Nhưng nếu ôm 5 việc cùng lúc thì không việc nào làm tới nơi. Phải chọn **một** việc để bắt đầu — và đây là cái cân để chọn cho khỏi cảm tính.

Cạm bẫy hay gặp: chọn việc "tốn nhiều thời gian nhất mỗi lần" (vd báo cáo quý ngốn 4 giờ). Nghe hợp lý mà sai — vì nó chỉ nhìn **một lần**, quên mất việc đó cả quý mới làm một bận.

## Khi nào dùng

Khi có nhiều việc muốn giao cho Claude và phân vân nên bắt đầu từ đâu.

## Các bước

Cho mỗi việc, chấm 1-5 rồi cộng theo trọng số:

```
Điểm = Frequency × 3  +  Time saved × 2  +  Setup effort × 1  +  Variability × 2
```

- **Frequency** (số lần/tuần) — **×3, nặng nhất**: làm càng thường, lợi ích càng cộng dồn.
- **Time saved** (mỗi lần) — ×2: tiết kiệm trực tiếp.
- **Setup effort** (1=khó, 5=dễ) — **×1, nhẹ nhất**: vì setup chỉ tốn *một lần*, lợi ích thì lặp mãi.
- **Variability** (1=mỗi lần mỗi khác, 5=ổn định) — ×2: việc càng đều đặn giống nhau, automation càng ăn.

Chọn việc điểm cao nhất làm trước, làm tới nơi, đo kết quả, rồi mới thêm việc thứ hai.

## Lưu ý/cạm bẫy

- Insight cốt lõi: **tần suất × độ ổn định ăn đứt thời-gian-mỗi-lần**. Việc nhỏ lặp hằng ngày > việc to nhưng hiếm.
- Đừng để "ngại setup" cản việc cao tần — setup là chi phí một lần, đừng cân nó nặng.
- Bắt đầu bằng việc *độ khó vừa, tần suất cao* để có "quick win" tạo đà; đừng nhằm việc khó nhất trước (fail sớm → nản).

## Ví dụ thực tế

Daily standup note (5 lần/tuần, 15 phút, ổn định) ≈ **33 điểm** vs báo cáo tổng kết quý (0.1 lần/tuần, 4 giờ, mỗi lần mỗi khác) ≈ **15 điểm** → chọn daily note trước, dù mỗi lần nó chỉ tiết kiệm 15 phút.

## Liên hệ

- [[delegate-repeatable-keep-judgment]] — chỉ tự động hóa cái lặp lại được; chấm điểm chính là cách lượng hóa "cái lặp lại"
- [[scheduled-tasks-tu-dong-hoa-viec-lap]] — việc cao-tần ổn định chính là ứng viên số 1 cho Scheduled Task

## Nguồn

- Claude 101 — Bài 1.11: Claude theo vai trò (Scoring framework + anti-patterns), Anthropic Academy, 2026
