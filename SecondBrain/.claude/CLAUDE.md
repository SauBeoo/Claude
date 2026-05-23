# Hướng dẫn Claude Code khi làm việc với vault SecondBrain

Đây là vault Obsidian theo phương pháp PARA + Atomic notes. Đọc kỹ trước khi thao tác.

## Nguyên tắc tối thượng

1. **Ngôn ngữ:** Trả lời và viết note bằng **tiếng Việt** trừ khi tôi nói khác.
2. **Markdown thuần:** Mọi note đều là `.md`. Dùng `[[wiki-link]]` cho liên kết nội bộ.
3. **Không xóa, chỉ archive:** Project xong → move sang `40_Archive/<năm>/`, không bao giờ `rm`.
4. **Tôn trọng cấu trúc PARA:** Trước khi tạo note mới, xác định nó thuộc đâu (xem bảng dưới).

## Bảng quyết định: note mới đi đâu?

| Tình huống | Thư mục đích |
|---|---|
| Tôi nói "lưu lại cái này" mà không nói rõ | `00_Inbox/y-tuong-chot/` |
| Tóm tắt 1 paper cụ thể, không gắn project | `00_Inbox/paper-chua-doc/` |
| Tóm tắt paper cho project X đang chạy | `10_Projects/<X>/papers/` |
| Ghi chú về 1 sinh viên/buổi họp project X | `10_Projects/<X>/notes/` hoặc `meetings/` |
| Kinh nghiệm đúc kết về vai trò (dạy, nghiên cứu) | `20_Areas/<area>/` |
| Bài blog/khóa học/video hay từ người khác | `30_Resources/<chủ-đề>/` |
| Ý tưởng chín, dùng được nhiều lần | `50_Atomic/<loại>/` |
| Daily note hôm nay | `60_Daily/<năm>/<tháng>/YYYY-MM-DD.md` |

Nếu không chắc → để ở `00_Inbox/` và **hỏi tôi**.

## Quy ước đặt tên file

- **Atomic notes:** slug không dấu, gạch ngang. Ví dụ: `self-attention-la-weighted-sum.md`
- **Project, Area, Resource:** slug không dấu. Ví dụ: `claude-code-101`, `idea-aff`, `teaching/`
- **Daily:** `YYYY-MM-DD.md`
- **Trong nội dung (heading, body):** dùng tiếng Việt có dấu tự nhiên.

## Templates

Khi tạo note mới, dùng template tương ứng ở `99_Meta/templates/`:

- Paper → `paper-summary.md`
- Atomic concept → `atomic-concept.md`
- Atomic claim → `atomic-claim.md`
- Atomic method → `atomic-method.md`
- Atomic question → `atomic-question.md`
- Daily → `daily.md`
- Lecture → `lecture.md`
- Video script → `video-script.md`
- Project README → `project-readme.md`

## Khi tôi nhờ "tóm tắt paper này"

1. Đọc PDF (dùng skill `pdf-reading` hoặc tương đương).
2. Tạo note theo template `paper-summary.md`.
3. Đặt ở:
   - Nếu tôi nói project nào → `10_Projects/<project>/papers/<slug>.md`
   - Không thì → `00_Inbox/paper-chua-doc/<slug>.md`
4. **Sau khi tóm tắt, gợi ý 2-3 atomic notes** có thể tạo từ paper này. Không tự tạo, chờ tôi xác nhận.

## Khi tôi nhờ "tạo atomic note về X"

1. Hỏi tôi: concept, claim, method, hay question?
2. Dùng template tương ứng.
3. Đặt ở `50_Atomic/<loại>/<slug>.md`
4. **Tìm 3-5 note có sẵn liên quan** trong vault để gợi ý link `[[...]]`.
5. Status mặc định = `seed`.

## Khi tôi nhờ "soạn bài giảng/video/content"

1. Xác định project nào (`10_Projects/<X>/`).
2. **Tìm atomic notes liên quan trong `50_Atomic/`** trước khi viết — tái sử dụng tri thức cũ là mục đích chính của bộ não 2.
3. Dùng template phù hợp (`lecture.md`, `video-script.md`).
4. Trong nội dung, link `[[...]]` tới các atomic notes đã dùng.

## Khi tôi nhờ "tạo daily note"

1. Tạo file theo template `daily.md` tại `60_Daily/<năm>/<tháng>/YYYY-MM-DD.md`.
2. Không tự điền nội dung — chỉ tạo file theo template, chờ tôi tự điền.
3. Section `📚 Đã chắt lọc` dùng để ghi lại source đã xử lý + atomic notes mới tạo trong ngày — không điền thay tôi.

## Khi tôi nhờ "dọn Inbox"

1. List tất cả file trong `00_Inbox/` cùng ngày tạo.
2. Với mỗi file, gợi ý phân loại theo bảng quyết định ở trên.
3. **Không tự move**, đề xuất trước, chờ tôi gật đầu.

## Khi tôi nhờ "archive project X"

Chạy checklist:
1. Đã có ít nhất 3 atomic notes từ project này chưa? Liệt kê.
2. Đã có file `post-mortem.md` trong project chưa? Nếu chưa, hỏi tôi để cùng viết.
3. Cập nhật README của project: status = "DONE — <ngày>"
4. Đề xuất: `mv 10_Projects/<X> 40_Archive/<năm>/`

## Việc Claude KHÔNG được tự ý làm

- Xóa file (`rm`) — luôn dùng `mv` sang `40_Archive/`
- Đổi cấu trúc thư mục gốc (00_Inbox, 10_Projects, ...)
- Commit Git — chỉ commit khi tôi yêu cầu rõ
- Viết note thay quan điểm của tôi vào `20_Areas/` mà không xác nhận — Areas là kinh nghiệm của tôi, Claude chỉ ghi lại

## Liên kết với Projects ngoài vault

Project code thực tế đặt ở `E:\Claude\Projects\<tên-project>\`. Trong vault, `10_Projects/<tên-project>/` chỉ chứa **ghi chú về project**, không chứa code.

Nếu cần đọc code → `cd E:\Claude\Projects\<tên-project>\` rồi làm việc với Claude Code ở đó.
