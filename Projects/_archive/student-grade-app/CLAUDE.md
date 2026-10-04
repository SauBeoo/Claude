# CLAUDE.md cho project student-grade-app

## Bối cảnh

Web app cá nhân quản lý điểm sinh viên. Stack: FastAPI + React + SQLite.
Chỉ chạy local, không deploy production, không có user khác.

## Vai trò mặc định

Kích hoạt agent **coder** khi mở project này.

## Liên kết vault

```
Vault: E:\Claude\SecondBrain\
```

Khi user nói "lưu kinh nghiệm coding này vào bộ não":
→ Path: `E:\Claude\SecondBrain\20_Areas\coding-practices\<slug>.md`

Project này KHÔNG có thư mục riêng trong `10_Projects/` của vault (vì là sản phẩm cá nhân, không phải project nghiên cứu).

## Quy ước code

### Backend (Python)

- Style: PEP 8, dùng `ruff` để lint
- Type hints bắt buộc cho public function
- Naming:
  - `snake_case` cho function/variable
  - `PascalCase` cho class
  - `UPPER_CASE` cho constant
- Docstring style: Google

### Frontend (React)

- Functional components only (không class)
- Hooks: `useState`, `useEffect` đủ, không over-engineer state management
- File naming: `PascalCase.tsx` cho component, `camelCase.ts` cho util
- TailwindCSS utility classes, không custom CSS

### Database

- Migration bằng Alembic
- Naming table: số ít, snake_case (`student`, `grade`, không phải `Students`)
- Soft delete (`deleted_at` column), không hard delete

## Test

- pytest cho backend
- Coverage tối thiểu 70% cho service layer
- Test file đặt cạnh source file: `services/grade.py` → `tests/test_grade.py`

## Khi user nhờ review code

1. Đọc toàn file
2. Phân loại issue (🔴 bug / 🟠 logic / 🟡 smell / 🔵 style)
3. Đưa example code cho mỗi đề xuất
4. Sau khi review, hỏi: "Có gì hay đáng lưu vào bộ não 2 không?"

## Quy tắc Git

- Branch naming: `feat/<slug>`, `fix/<slug>`, `refactor/<slug>`
- Commit message: tiếng Anh, format conventional commits
  - `feat: add csv import endpoint`
  - `fix: correct gpa calculation rounding`
- KHÔNG tự động commit. Chỉ commit khi user yêu cầu.

## Secret

- API key, password → `.env`, đã .gitignore
- Khi chia sẻ code/log với Claude, redact secret trước
