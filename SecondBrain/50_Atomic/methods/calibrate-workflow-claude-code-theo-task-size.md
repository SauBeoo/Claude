---
type: method
tags: [claude-code, workflow, decision-table, epcc]
source: [[2026-claude-code-101-epcc-workflow]]
created: 2026-05-23
status: seed
---

# Mức độ rigid của workflow EPCC phải scale theo task size — không có 1 workflow đúng cho mọi task

**Nguyên tắc**: Workflow EPCC (Explore → Plan → Code → Commit) là công cụ, không phải nghi lễ. Full EPCC cho mọi task = anti-pattern. Skip EPCC cho task lớn cũng anti-pattern.

**Bảng calibration**:

| Task size | Explore | Plan | Code | Commit | Time |
|---|---|---|---|---|---|
| **Tiny** (fix typo, đổi constant) | Skip | Skip | Nhanh | Minimal | 2-5p |
| **Easy** (thêm field, fix bug 1 file) | Optional | Optional | Normal | Minimal | 5-15p |
| **Medium** (feature mới, refactor module) | Required | Required | Normal + test | Full review | 20-60p |
| **Hard** (redesign arch, cross-cutting) | Extended | Multiple rounds | Phased + nhiều test | Multi commits | 2-8h |
| **Massive** (legacy modernization) | Days | Days | Phased over weeks | Per-phase commit | Weeks |

**Áp dụng thực tế**:

- **Tiny**: `Fix typo "recieve" → "receive" trong src/constants.ts:47` → Code + Commit. 2 phút. Vào Plan Mode cho task này là overhead vô nghĩa.
- **Hard**: Plan nhiều vòng, Code phase chia phases, commit mỗi phase riêng. Tránh 1 commit khổng lồ 5000 dòng — không ai review nổi.

**Anti-pattern phổ biến**:
- Full EPCC cho tiny task → mất đà, demotivating.
- Skip Plan cho medium+ task để "save time" → 10 phút Plan tiết kiệm 30-90 phút debug.

**Nguyên tắc cốt**: Workflow phải phục vụ bạn, không ngược lại. Đo task size trước → chọn rigid phù hợp.

## Bằng chứng / nguồn
- Từ [[2026-claude-code-101-epcc-workflow]], trang 13: bảng calibration đầy đủ với 5 task tier.
- Anti-pattern #5: "Full EPCC cho tiny task" — overhead workflow lớn hơn task.

## Liên quan
- [[plan-mode-workflow-5-buoc]]
- [[epcc-workflow-claude-code]]
- [[cost-thay-doi-tang-theo-phase-trong-ai-workflow]]
- [[test-suite-bien-code-phase-thanh-vong-lap-tu-sua]]

## Câu hỏi mở
- Làm sao estimate task size *trước khi* explore? Đôi khi "tiny" thực ra là "hard" trá hình.
