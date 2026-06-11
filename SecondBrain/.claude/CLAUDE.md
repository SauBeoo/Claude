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
4. **Tìm note liên quan** trong vault, nhưng mục "## Liên hệ" chỉ giữ **tối đa 2 link load-bearing** (xem "Quy tắc liên kết & đồ thị" bên dưới).
5. Status mặc định = `seed`.
6. **Viết thân note theo kiểu ELI5** — dễ như giải thích cho một đứa trẻ 5 tuổi: ví dụ/phép so sánh đời thường, câu ngắn, từ quen thuộc. Thuật ngữ kỹ thuật chỉ giữ ở tiêu đề hoặc khi bắt buộc, giải thích ngay bằng lời thường. (Áp dụng cho cả `/paper-atomize`.)

## Quy tắc liên kết & đồ thị (graph hygiene)

Mục tiêu: graph là **đồ thị tri thức**, không phải đồ thị thao tác. Đừng để nó "lằng nhằng".

1. **Mỗi note một vai trò** (không để nhiều note cùng index một bộ atomic → tránh "quạt trùng"):
   - **MOC** = mục lục duy nhất theo chủ đề, giữ toàn bộ link + chia nhóm. Mỗi domain lớn một MOC riêng (vd `claude-MOC`, `claude-code-MOC`).
   - **Source/course note** = provenance, chỉ fan tới atomic chắt ra từ chính nó.
   - **daily** = nhật ký, chỉ link cái tạo ra hôm đó. **_track** = bảng tiến độ, link tối thiểu.
   - **atomic** = (ngầm nối MOC) + tối đa **2** atomic load-bearing.

2. **"## Liên hệ" của atomic: tối đa 2 link** mạnh nhất — cái thực sự sẽ bấm theo. KHÔNG liệt kê link "cùng tinh thần/anh em" mềm. MOC đã lo việc duyệt-theo-chủ-đề nên cắt link ngang không làm atomic mồ côi.

3. **Cross-domain bridge tiết kiệm:** nối 2 cụm chủ đề chỉ bằng 1–2 nhịp cầu thật đắt giá, đừng dán mọi thứ thành một khối.

4. **Provenance source→atomic (BẮT BUỘC khi chắt atomic):**
   - Đầu section "## Nguồn" của atomic, thêm: `- Trích từ: [[<source/course note>]]`.
   - Trong source/course note: liệt kê atomic đã chắt ra + link tới MOC.
   - Note nguồn của một khóa học đặt ở `30_Resources/courses/<slug>.md`.

5. **Node nên ẩn khỏi global graph** (loại operational/log/study, không phải tri thức) qua *Graph settings → Filters*: `daily`, `_track`, `flashcards`, `CHANGELOG`, `README`, `templates`, `guides`, `00_HOME`, và note nguồn khóa (vì fan trùng MOC). Provenance/log xem bằng **Local Graph** + Backlinks, không nhồi vào global.

6. **Cấu hình graph baseline** (`.obsidian/graph.json`): `showOrphans:false`, `hideUnresolved:true`, `textFadeMultiplier` âm (nhãn chỉ hiện khi zoom gần), tô màu theo tầng PARA, `repelStrength` cao để giãn node.

> Chấm cô đơn còn lại trong graph = "đèn báo" chủ đề chưa được chắt/nối — hữu ích, không phải lỗi. Đừng cố nối ép.

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

## Quy tắc bảo trì hệ thống (BẮT BUỘC)

Mọi lần Claude thay đổi cấu trúc/quy tắc/file trong vault → phải làm **cùng turn**:

1. **Có quy tắc/command/skill/agent mới** → thêm vào `99_Meta/guides/huong-dan-van-hanh-secondbrain.md` (đặc biệt mục 8 nếu là command). Không "để sau".
2. **Có edit/move/rename file đã tồn tại** → ghi entry vào `99_Meta/CHANGELOG.md` theo format mẫu cuối file đó.
3. **Tạo file mới** → KHÔNG cần log CHANGELOG (Git history đã đủ).
4. **User trực tiếp gõ sửa** → KHÔNG log (chỉ log khi Claude thay mặt).

Thứ tự thao tác: làm thay đổi → update guides (nếu cần) → update CHANGELOG → báo cáo cuối. Bỏ bước nào = chưa xong.

Chi tiết: xem mục 14 trong `99_Meta/guides/huong-dan-van-hanh-secondbrain.md`.

## Liên kết với Projects ngoài vault

Project code thực tế đặt ở `E:\Claude\Projects\<tên-project>\`. Trong vault, `10_Projects/<tên-project>/` chỉ chứa **ghi chú về project**, không chứa code.

Nếu cần đọc code → `cd E:\Claude\Projects\<tên-project>\` rồi làm việc với Claude Code ở đó.
