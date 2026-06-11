---
type: claim
created: 2026-06-08
tags: [claude-code, context-window, mcp]
status: seed
---

# Mỗi MCP server bật lên là tốn context TRƯỚC KHI bạn gõ prompt

Mỗi MCP server bạn kết nối phải khai báo cho Claude biết "tôi có những tool gì, dùng ra sao" — phần khai báo đó nằm sẵn trên bàn làm việc **ngay từ giây đầu tiên**, tốn khoảng **2–15k token mỗi server**, dù bạn chưa hề dùng tới nó.

Giống như bày sẵn 12 bộ đồ nghề lên bàn "phòng khi cần": bật đại 12 server = ~50k token, tức **25% cái bàn** đã mất trước cả khi gõ chữ đầu tiên. 5 server không liên quan = 30k token vứt đi vô nghĩa.

**Hệ quả thực hành:** chỉ bật MCP server cho việc đang làm. Server không dùng → `/mcp disable <tên>` hoặc cấu hình `.mcp.json` riêng từng project. *Thà cài lại khi cần còn hơn để nó âm thầm ăn mòn context cả session.*

## Liên hệ

- [[context-window-tai-nguyen-huu-han]] — cái "bàn" mà MCP chiếm chỗ
- [[mcp-usb-c-cho-ai]] — MCP là gì (chuẩn cắm chung) — note này nói về *cái giá* của việc cắm

## Nguồn

- Trích từ: [[2026-claude-code-101-quan-ly-context]]
- Khoá Claude Code 101 (gốc Anthropic) — Bài 2.5, chiến thuật 5 "Dọn MCP server không dùng"
