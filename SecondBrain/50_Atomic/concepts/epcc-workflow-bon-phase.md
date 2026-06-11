---
type: concept
created: 2026-06-08
tags: [claude-code, workflow, epcc]
status: seed
---

# EPCC — vòng lặp 4 phase, dồn sức vào nửa đầu

EPCC = **Explore → Plan → Code → Commit**: vòng lặp chuẩn khi làm việc với Claude Code.

- **Explore** (~20%) — đọc file, hiểu pattern, tìm xem việc nằm ở đâu.
- **Plan** (~30%) — lập plan, review, duyệt.
- **Code** (~40%) — viết, chạy test, sửa.
- **Commit** (~10%) — review lần cuối rồi push.

Điều phản trực giác và quan trọng nhất: **Explore + Plan chiếm ~50% thời gian, nhưng đó là *đầu tư* chứ không phải phí phạm.** Giống như đo hai lần rồi cưa một lần — bỏ qua đo đạc thì cưa nhanh nhưng cưa hỏng, làm lại còn lâu hơn. Hai dev cùng một ticket: người nhảy thẳng vào code loay hoay 2 tiếng; người Explore+Plan trước xong trong 25 phút. Khác biệt **không** ở tài năng, mà ở workflow.

> "Nếu chỉ rút ra một thứ từ khóa này, hãy để nó là workflow này." — Boris Cherny

(Tỷ lệ % là minh họa cho task medium, **không phải con số cứng** — task càng khó, Plan càng chiếm tỷ trọng lớn.)

## Liên hệ

- [[cost-thay-doi-tang-theo-phase]] — vì sao dồn sức vào Plan: sửa ở plan rẻ nhất
- [[calibrate-workflow-theo-task-size]] — task nhỏ thì skip Explore/Plan, đừng cứng nhắc

## Nguồn

- Trích từ: [[2026-claude-code-101-epcc-workflow]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.4 "Workflow Explore → Plan → Code → Commit"
