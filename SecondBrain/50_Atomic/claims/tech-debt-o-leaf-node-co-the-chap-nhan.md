---
type: claim
tags: [software-architecture, tech-debt, code-review, mindset]
source: [[2026-claude-code-101-epcc-workflow]]
created: 2026-05-23
status: seed
---

# Tech debt ở "leaf node code" (không có gì depend vào) có thể chấp nhận — concentrate review effort vào interfaces

**Định nghĩa leaf node**: Code mà **không có module/function nào khác depend vào**. Đây là code "dead-end" — caller-only, không phải callee của ai khác. Ví dụ: utility function chỉ dùng nội bộ trong 1 file, render component cuối cùng không export.

**Claim**: Khi review code (đặc biệt với AI-assisted development tốc độ cao), **không cần perfect mọi nơi**. Effort review nên concentrate vào:
- **Interfaces** — function signatures, API contracts, types public.
- **Extensible parts** — abstract classes, hooks, plugins — chỗ người khác sẽ build lên.

Leaf node được "okay-to-be-imperfect" vì:
- Refactor leaf node sau không break gì khác — chi phí thay đổi thấp.
- Không depend vào → ít risk lan tỏa.
- AI có thể tự refactor sau, nếu thực sự cần.

**Nguồn gốc**: Mindset này được Anthropic team áp dụng trong case study 22.000-line RL code change. Họ "focused implementation on leaf nodes — code that nothing else depends on. Human review focused on extensible parts."

**Implication thực tế**:
- Khi prompt Claude code review, nói rõ: "Focus on public API and shared modules. Skip deep review for internal helper functions."
- Khi viết code mới, ưu tiên design tốt cho interfaces hơn nội bộ leaf node.
- Tech debt strategic: chấp nhận debt ở leaf node, refuse debt ở interface.

**Cảnh báo**: Định nghĩa "leaf node" có thể sai. Code tưởng leaf hôm nay có thể bị nhiều module depend vào sau 6 tháng. → Audit định kỳ.

## Bằng chứng / nguồn
- Từ [[2026-claude-code-101-epcc-workflow]], trang 19: "Tech debt in leaf nodes is okay because nothing depends on them." — Anthropic team case study.

## Liên quan
- [[epcc-workflow-claude-code]]
- [[subagent-reviewer-bu-bias-cua-session-chinh]]

## Câu hỏi mở
- Tool nào có thể auto-detect leaf node trong codebase (vd: static analysis tìm function không có caller)?
