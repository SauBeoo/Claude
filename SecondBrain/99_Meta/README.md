# 99_Meta — Hạ tầng của vault

Đây là nơi chứa **công cụ** để vận hành vault, không phải nội dung.

## Thư mục con

- `templates/` — Template note (Obsidian sẽ dùng khi tạo note mới)
- `MOCs/` — Map of Content — index theo chủ đề

## Templates có sẵn

| File | Dùng khi nào |
|---|---|
| `paper-summary.md` | Tóm tắt 1 paper nghiên cứu |
| `atomic-concept.md` | Tạo atomic note loại concept |
| `atomic-claim.md` | Tạo atomic note loại claim |
| `atomic-method.md` | Tạo atomic note loại method |
| `atomic-question.md` | Tạo atomic note loại question |
| `daily.md` | Daily note hằng ngày |
| `lecture.md` | Soạn 1 buổi giảng |
| `video-script.md` | Kịch bản video |
| `project-readme.md` | README cho project mới |

## Cách cấu hình Obsidian dùng templates

Settings > Templates:
- Template folder location: `99_Meta/templates`
- Date format: `YYYY-MM-DD`
- Time format: `HH:mm`

Settings > Core plugins > bật **Templates**, **Daily notes**, **Templater** (community plugin, mạnh hơn Templates mặc định).

## MOC — Map of Content là gì?

MOC = 1 note đặc biệt, là "trang index" theo chủ đề. Khi bạn có 30+ atomic notes về Machine Learning, tạo `ML-MOC.md` để gom link lại:

```markdown
# ML Map of Content

## Khái niệm nền tảng
- [[gradient-descent-la-gi]]
- [[overfitting-la-gi]]

## Attention & Transformer
- [[self-attention-la-weighted-sum]]
- [[positional-encoding-can-thiet-vi]]

## Câu hỏi mở
- [[lieu-llm-co-thuc-su-hieu-ngon-ngu]]
```

MOC là "đường vào" tri thức theo chủ đề, atomic notes là "ngôi nhà" của tri thức.
