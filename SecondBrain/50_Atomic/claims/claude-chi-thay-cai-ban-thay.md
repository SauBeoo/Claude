---
type: claim
created: 2026-06-03
tags: [claude, security, permissions, connectors, enterprise-search]
status: seed
confidence: high
---

# Luận điểm: Claude chỉ thấy cái bạn thấy — security boundary của bạn = của Claude

Tưởng tượng bạn đưa chìa khóa nhà mình cho một trợ lý. Trợ lý đó mở được nhà **bạn** — nhưng không mở được nhà hàng xóm, vì chìa khóa là của bạn, không phải chìa vạn năng.

Mọi feature kết nối của Claude (Connectors, Enterprise Search, Research + integrations) đều chạy bằng **credentials của chính người dùng** (OAuth). Nên Claude đọc được inbox *của bạn* chứ không phải của sếp; search được channel bạn *đã được mời* chứ không phải private channel của team khác. Không có "tài khoản thần" nào đọc toàn bộ hệ thống — kể cả Enterprise Search cấp công ty cũng FILTER kết quả theo quyền của từng người hỏi.

## Lập luận ủng hộ

- Setup Enterprise Search 2 bước: admin connect tool cho org, nhưng **từng user vẫn phải tự authenticate** — chính bước này enforce phân quyền
- Search chạy live qua tool gốc, không có index/copy riêng → tool gốc tự kiểm tra quyền như khi bạn login tay

## Lập luận phản biện

- MCP server độc hại vẫn exfiltrate được data *trong phạm vi quyền của bạn* — "chỉ thấy cái bạn thấy" không có nghĩa vô hại, 1 inbox rò rỉ cũng đủ thành sự cố
- Prompt injection có thể lừa Claude *dùng sai* quyền hợp lệ (vd gửi data ra ngoài qua action được phép)

## Quan điểm của tôi

Tin ở mức cao — đây là nguyên tắc kiến trúc, không phải lời hứa marketing. Nhưng bài học kèm theo: quyền của TÔI chính là attack surface, nên grant tối thiểu.

## Liên hệ

- [[mcp-usb-c-cho-ai]] — chuẩn mở bên dưới các connector
- [[chon-tool-theo-cau-hoi]] — Enterprise Search trong bộ 4 tool đều tôn trọng nguyên tắc này
- [[output-troi-chay-khong-dong-nghia-dung]] — cùng họ "đừng tin mặc định, hiểu cơ chế rồi hãy tin"

## Nguồn

- Claude 101 — Bài 1.8 (security model) + Bài 1.9 (Enterprise Search permissions), Anthropic Academy, 2026
