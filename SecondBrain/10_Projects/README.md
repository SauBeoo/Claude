# 10_Projects — Việc đang làm

Mỗi project = 1 thư mục con. Project có **deadline** và **kết quả cụ thể**.

## Quy ước đặt tên thư mục

`<loại>-<chủ-đề>-<thời-gian>`

Ví dụ:
- `research-nlp-2026/` — nghiên cứu NLP năm 2026
- `course-python-2026-spring/` — môn Python học kỳ xuân 2026
- `book-deep-learning-vol1/` — sách Deep Learning quyển 1
- `video-series-llm-explained/` — series video giải thích LLM
- `product-app-quanly-sinhvien/` — sản phẩm app quản lý sinh viên

## Cấu trúc bên trong mỗi project

```
<project-name>/
├── README.md           # Mục tiêu, deadline, status, link tới project repo nếu có
├── notes/              # Ghi chú quá trình làm
├── papers/             # (Nếu nghiên cứu) — atomic note cho từng paper đọc
├── outputs/            # Sản phẩm: slide, paper, video, code
└── meetings/           # Note họp với cộng sự/sinh viên
```

Project repo (code thực tế) **đặt ngoài vault**, ở `E:\Claude\Projects\<project-name>\`. Vault chỉ chứa **ghi chú về project**, không chứa code.

## Khi project xong

```
mv 10_Projects/<project> 40_Archive/<năm>/
```

Trước khi move, dành 15 phút **chắt lọc** ý tưởng hay nhất trong project thành atomic note ở `50_Atomic/`. Đây là cách tri thức từ project không bị mất khi project kết thúc.
