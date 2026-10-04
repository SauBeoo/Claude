# CLAUDE.md cho project research-llm-education-2026

Cấu hình Claude Code khi `cd` vào thư mục này. Ghi đè cấu hình toàn cục.

## Bối cảnh

Project nghiên cứu về LLM trong giáo dục lập trình. Output cuối là bài báo CSEDU/SIGCSE.

## Vai trò mặc định

- Khi mở project này, kích hoạt agent **researcher** mặc định
- Khi user nói "review code thực nghiệm" → chuyển sang agent **coder**

## Liên kết vault

```
Vault: E:\Claude\SecondBrain\
Project notes: E:\Claude\SecondBrain\10_Projects\research-llm-education-2026\
```

Mọi tóm tắt paper, ghi chú nghiên cứu → lưu vào vault path ở trên, KHÔNG lưu trong project repo này.

## Quy tắc viết paper

- Style: IEEE / ACM (TBD theo venue)
- Citation: bibtex placeholder, user điền key sau
- Ngôn ngữ paper: **tiếng Anh**
- Ngôn ngữ note nghiên cứu: **tiếng Việt** (trừ thuật ngữ kỹ thuật)

## Stack thực nghiệm

- Python 3.11
- pandas, numpy, scipy cho stats
- OpenAI API + Anthropic API cho LLM
- Jupyter notebook để document quy trình

## Quy tắc data

- **Không commit dữ liệu sinh viên thật** vào Git (đã .gitignore data/)
- Anonymize: thay tên/MSV bằng ID giả trước khi phân tích
- Backup dataset ở Google Drive private, không public repo

## Khi user nói "đọc paper mới"

1. Skill `summarize-pdf-paper` được kích hoạt
2. Đặt tóm tắt ở `SecondBrain\10_Projects\research-llm-education-2026\papers\`
3. Đề xuất 2-4 atomic notes (theo workflow chuẩn)
4. Update MOC nếu có: `SecondBrain\99_Meta\MOCs\LLM-Education-MOC.md`

## Stats progress

Định kỳ gọi: "Cho tôi xem progress project này"
→ Claude scan:
- Số paper đã tóm tắt: `ls SecondBrain\10_Projects\research-llm-education-2026\papers\ | wc -l`
- Số atomic notes có tag `llm-education`
- Số experiment chạy trong `experiments/`
- Số ngày còn đến deadline

Báo cáo dạng bảng + cảnh báo nếu chậm tiến độ.
