---
type: concept
created: 2026-06-03
tags: [claude, mcp, connectors, integration]
status: seed
---

# MCP — "USB-C cho AI"

Tưởng tượng ngăn kéo nhà bạn ngày xưa: mỗi điện thoại một loại dây sạc riêng, mua máy mới là phải mua dây mới. Rồi USB-C ra đời — 1 chuẩn chung, cắm máy nào cũng chạy.

**MCP (Model Context Protocol)** làm đúng việc đó cho AI. Trước MCP, muốn AI nói chuyện với Slack hay Jira thì mỗi hãng AI phải tự viết "dây sạc riêng" cho từng tool — chậm và manh mún. MCP là **chuẩn cắm chung, công khai** (Anthropic open-source): ai đọc spec cũng viết được một **MCP server** — cục "chuyển đổi đầu cắm" cho tool của mình.

Hệ quả quan trọng nhất: công ty bạn có tool nội bộ → team tự viết MCP server theo chuẩn → Claude (và mọi AI hỗ trợ MCP) cắm vào dùng được ngay, **không cần xin phép hay chờ Anthropic**. Đó là lý do có hàng trăm connector do cộng đồng tự build.

## Liên hệ

- [[claude-chi-thay-cai-ban-thay]] — connector mạnh đến đâu vẫn bị chặn bởi permission của người dùng
- [[progressive-disclosure-skills]] — cùng triết lý "chuẩn mở + nạp khi cần" của hệ sinh thái Claude

## Nguồn

- Trích từ: [[claude-101-anthropic-academy]]
- Claude 101 — Bài 1.8: Connectors — Kết nối tools qua MCP (Anthropic Academy, 2026)
