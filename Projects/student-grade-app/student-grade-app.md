# student-grade-app

Web app cá nhân để quản lý điểm sinh viên của các môn tôi đang dạy.

## 🎯 Mục tiêu

- Tự nhập điểm nhanh hơn Excel
- Tự tính GPA, xếp hạng theo môn
- Export ra PDF/Excel cho phòng đào tạo
- Chỉ dùng cho cá nhân, không multi-tenant

## 🏗️ Stack

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** React + TailwindCSS
- **DB:** SQLite (đơn giản, đủ dùng)
- **Auth:** không có (chạy local)

## 📂 Cấu trúc

```
student-grade-app/
├── README.md
├── CLAUDE.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── docs/
```

## 🚀 Chạy local

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (terminal khác)
cd frontend
npm install
npm run dev
```

## 🔗 Liên kết vault

Project này không có note nghiên cứu — KHÔNG có folder tương ứng trong `10_Projects/`.

Tuy nhiên, khi học được kinh nghiệm coding gì hay → lưu vào:
`E:\Claude\SecondBrain\20_Areas\coding-practices\`

Ví dụ kinh nghiệm đã rút ra từ project này:
- `cach-round-so-thap-phan-ngay-khi-tinh-toan.md`
- `khi-nao-dung-sqlite-thay-postgres.md`

## 📌 TODO

- [ ] Setup FastAPI skeleton
- [ ] Schema database
- [ ] CRUD API endpoints
- [ ] Frontend forms
- [ ] Import CSV từ Excel cũ
- [ ] Export PDF

## 🔗 Liên kết nội bộ

- [[student-grade-app/CLAUDE|CLAUDE.md — cấu hình Claude cho project]]
