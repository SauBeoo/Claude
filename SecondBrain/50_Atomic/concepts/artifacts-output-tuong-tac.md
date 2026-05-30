---
type: concept
created: 2026-05-30
tags: [claude, artifacts]
status: seed
---

# Artifacts — output đứng-một-mình, tương tác

Thay vì nhét 300 dòng code vào giữa đoạn chat, Claude mở một **cửa sổ riêng** bên cạnh và dựng ra thứ *dùng được ngay*: một trang web chạy thật, một biểu đồ tương tác, một file tải về. Đó là Artifact.

6 loại phổ biến: document (Word/Excel/PDF…), code, trang HTML, ảnh SVG, sơ đồ Mermaid, và **React component** (app có logic thật: calculator, dashboard).

Claude tự tạo artifact khi nội dung *đáng kể + tự đứng được + sẽ tái dùng*. Muốn ép: bảo "create as an artifact".

3 điều cốt lõi:
- **Iterate từng-thay-đổi-một** (đổi màu → xem → tăng size → xem); mỗi version được lưu, rollback được. Đừng dồn 10 yêu cầu.
- **ROI cao nhất = "reusable template"**: build 1 lần (template proposal, checklist, calculator), publish/save, dùng hàng chục lần.
- **Artifact tương tác CÓ logic = có thể có bug.** Phải test 3–5 input trước khi tin — đúng tinh thần "trôi chảy ≠ đúng".

Share 3 kiểu: copy/download (cá nhân), share nội bộ org (Team/Enterprise), publish public (ai có link cũng xem + "remix" được; không bị Google index).

## Liên hệ

- [[projects-store-knowledge-skills-perform-tasks]] — Artifact là sản phẩm đầu ra; Project/Skill là kiến thức/quy trình tạo ra nó
- [[output-troi-chay-khong-dong-nghia-dung]] — vì sao phải test logic artifact trước khi tin

## Nguồn

- Khoá Claude 101 (Anthropic Academy) — bài 1.6 "Artifacts — Sáng tạo tương tác"
