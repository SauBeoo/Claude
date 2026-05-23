---
type: concept
created: 2026-05-24
tags: [claude-code, context-window, foundational]
status: seed
---

# Context window là tài nguyên hữu hạn — không phải vô hạn

Context window là *toàn bộ bộ nhớ làm việc* mà một LLM agent (như Claude Code) có thể nhìn thấy tại một thời điểm: system prompt, CLAUDE.md, MCP tool definitions, skill metadata, hội thoại, mọi tool call và mọi tool result. Tất cả nhét chung vào một "túi" cố định kích thước (mặc định 200.000 token với các model Anthropic, ~80–100 file mã nguồn cỡ trung bình).

Hai hệ quả ít ai để ý: **(1)** mọi thứ trong túi là đầu vào cho lần inference tiếp theo — túi càng đầy thì mỗi câu trả lời càng đắt (tiền) và chậm (thời gian); **(2)** quan trọng hơn, khi gần đầy thì attention "loãng" — model bắt đầu xao lãng chi tiết nằm xa ở đầu hội thoại. Tức là *chất lượng giảm* trước khi *capacity hết*. Phép so sánh chuẩn: trí nhớ ngắn hạn của con người — nhớ 7 phút trước rõ, nhớ 2 giờ trước thì mơ hồ.

Đây là khái niệm nền cho mọi chiến thuật quản lý: compact, clear, subagent, skill on-demand, MCP cleanup — tất cả chỉ có lý do tồn tại *vì* context hữu hạn. Hiểu được hữu hạn → mới đặt câu hỏi đúng: "thứ này có đáng chỗ trong túi không?"

## Liên hệ

- [[auto-compact-mat-nuance]] — cơ chế hệ thống đối phó khi túi sắp đầy
- [[compact-khi-do-dang-clear-khi-doi-task]] — chiến thuật người dùng đối phó khi túi sắp đầy
- [[subagent-context-isolation-pattern]] — chiến thuật tránh túi đầy ngay từ đầu
- [[prompt-cu-the-tiet-kiem-context-hon-prompt-ngan]] — chiến thuật tiết kiệm túi khi prompt
- [[mcp-server-overhead-cost-truoc-prompt]] — chi phí cố định ăn vào túi trước cả prompt đầu tiên
- [[skill-on-demand-vs-claudemd-always]] — quy tắc chọn đặt cái gì vào túi luôn luôn vs khi cần

## Nguồn

- [[2026-claude-code-101-quan-ly-context]] — Bài 2.5 khóa Claude Code 101 (bản tiếng Việt v1.0)
