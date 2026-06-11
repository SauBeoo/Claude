---
type: claim
created: 2026-05-30
tags: [claude, projects, skills]
status: seed
confidence: high
---

# Luận điểm: Projects lưu kiến thức, Skills thực thi quy trình

Hai feature hay bị nhầm nhất. Câu thần chú để không bao giờ lẫn: **"Projects store knowledge. Skills perform tasks."** Project là cái **WHAT** — thông tin Claude cần *biết* (brand guide, tài liệu, template, lịch sử). Skill là cái **HOW** — *cách* Claude *làm* một việc (các bước, methodology, ràng buộc).

## Lập luận ủng hộ

- Project = kho tra cứu, sống xuyên mọi chat trong project. Skill = cỗ máy quy trình, tự kích hoạt khi prompt khớp mô tả.
- Chúng **bổ trợ, không thay thế**: một Skill có thể kéo kiến thức từ Project rồi xuất ra sản phẩm. Project cấp *thông tin*, Skill cấp *quy trình*.
- Ánh xạ vault SecondBrain: kho `50_Atomic/` + template + MOC = Project; các lệnh `find-related-notes`, `create-atomic-note` (có SKILL.md + các bước) = Skill.

## Lập luận phản biện

- Ranh giới đôi khi mờ: một skill cần "đọc tài liệu" có thể tự mang theo vài file reference — trông giống chứa knowledge. Nhưng mục đích vẫn là *quy trình*, không phải kho tra cứu.

## Quan điểm của tôi

Tin cao. Test nhanh: nếu thứ đó là *thông tin để tra* → Project; nếu là *cách làm lặp lại* → Skill. Tạo "skill" chỉ để chứa 50 PDF = nhầm, đó là Project.

## Liên hệ

- [[progressive-disclosure-skills]] — cơ chế Skill nạp dần
- [[instructions-project-nhu-code]] — cách "lập trình" một Project

## Nguồn

- Trích từ: [[claude-101-anthropic-academy]]
- Khoá Claude 101 (Anthropic Academy) — bài 1.5 (Projects), 1.7 (Skills)
