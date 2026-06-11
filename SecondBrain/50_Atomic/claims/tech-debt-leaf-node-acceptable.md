---
type: claim
created: 2026-06-08
tags: [claude-code, architecture, code-review]
status: seed
---

# Tech debt ở "leaf node" thì chấp nhận được — dồn công review vào interface

Từ case study Anthropic sửa 22.000 dòng code RL: không phải chỗ nào cũng cần code hoàn hảo. Họ cố tình tập trung implement vào **"leaf node"** — đoạn code mà **không có gì khác phụ thuộc vào nó** — và chấp nhận nợ kỹ thuật ở đó.

Phép so sánh: lá cây có héo vài chiếc cũng không sao, nhưng **thân và cành** (interface, phần được nhiều chỗ khác gọi tới) mà mục thì cả cây đổ. Nên review của con người nên dồn vào *phần extensible / interface*, không rải đều mọi dòng.

> "Tech debt in leaf nodes is okay because nothing depends on them." — đội kỹ sư Anthropic

Mindset rút ra: với code AI-assisted khối lượng lớn, đừng đòi perfect khắp nơi — **phân bổ sự kỹ tính theo mức độ phụ thuộc**.

## Liên hệ

- [[calibrate-workflow-theo-task-size]] — cùng tư duy phân bổ công sức theo mức rủi ro/phụ thuộc
- [[claude-code-subagent-fresh-eyes]] — review tập trung vào interface là review hiệu quả

## Nguồn

- Trích từ: [[2026-claude-code-101-epcc-workflow]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.4, case study "22.000-line RL code change"
