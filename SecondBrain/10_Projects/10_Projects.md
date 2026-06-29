# 10_Projects — Việc đang làm

Mỗi project = 1 thư mục con. Project có **deadline** và **kết quả cụ thể**.

## Quy ước đặt tên thư mục

`<loại>-<chủ-đề>` hoặc `<chủ-đề>-<thời-gian>` nếu có thời hạn cụ thể

**Đang active:**
- `claude-code-101/` — học & viết content về Claude Code
- `idea-aff/` — ý tưởng affiliate marketing
- `youtube-kham-pha/` — kênh faceless niche Unexplained Mysteries (view ngoại, repo ở `Projects/youtube-kham-pha/`)
- `youtube-jp-sukatto/` — kênh faceless AI朗読 thể loại スカッと/ざまぁ thị trường Nhật (repo ở `Projects/youtube-jp-sukatto/`)

**Pattern đặt tên gợi ý (cho project tương lai):**
- `course-<môn>-<học-kỳ>/` — môn dạy theo học kỳ
- `book-<chủ-đề>/` — viết/đọc sách theo chủ đề
- `video-series-<chủ-đề>/` — series video
- `research-<lĩnh-vực>-<năm>/` — nghiên cứu có deadline
- `product-<tên-app>/` — sản phẩm cụ thể

## Cấu trúc bên trong mỗi project

```
<project-name>/
├── <project>.md        # Folder note: mục tiêu, deadline, status, link tới project repo nếu có
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
