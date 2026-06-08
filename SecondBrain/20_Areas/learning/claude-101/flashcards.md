---
type: flashcards
created: 2026-05-30
subject: "Claude 101 — làm chủ hệ sinh thái Claude"
track: "[[_track]]"
tags: [flashcards]
---

# Flashcards: Claude 101

> Định dạng tương thích plugin **Obsidian Spaced Repetition**.
> - Thẻ 1 dòng:  `Câu hỏi :: Đáp án`
> - Thẻ nhiều dòng: `Câu hỏi` → dòng `?` → `Đáp án`
> Nếu không dùng plugin: dùng "chế độ quiz" của skill tutor để ôn thủ công.

#flashcards/claude-101

<!-- Mỗi thẻ kiểm tra ĐÚNG 1 ý. Hỏi "tại sao/khi nào", tránh hỏi định nghĩa thuộc lòng. -->

<!-- ===== Buổi 1 (2026-05-30) — AI Fluency: 4D + Iteration + Eval ===== -->

AI Fluency gồm mấy năng lực, là những gì? Người mới hay sót chữ D nào?
?
4 năng lực (4D): **Delegation** (giao gì) · **Description** (brief thế nào) · **Discernment** (thẩm định output) · **Diligence** (chịu trách nhiệm cuối). Người mới thường chỉ lo Description, hay sót **Discernment** và **Diligence**.

Tại sao "viết prompt giỏi" chưa đủ để gọi là AI-fluent?
?
Vì brief giỏi mới là 1/4 (chữ Description). Bỏ qua Discernment → không soi ra chỗ AI bịa; bỏ Diligence → ship sai rồi tự gánh. Fluent = làm tốt cả 4D.

Vì sao "không ưng là xoá đi viết lại từ đầu" lại phí với Claude mà không phí với Google?
?
Google quên bạn sau mỗi query (mỗi lần là tờ giấy trắng), nên viết lại không mất gì. Claude **nhớ cả hội thoại** — xoá đi là vứt toàn bộ context đã gây dựng, quay về vạch 0.

Phân biệt feedback yếu vs mạnh khi iterate — cho 1 ví dụ chuyển đổi.
?
Yếu = AI phải đoán ("ngắn hơn đi"). Mạnh = chỉ rõ **chỗ + cách sửa + ràng buộc**. VD: "ngắn hơn đi" → "cắt 2 đoạn đầu, kết theo hướng hành động, ≤ 200 từ".

Khi nào nên *restart* chat thay vì iterate tiếp?
?
Khi đã >15 message và AI bắt đầu lặp chính nó, hoặc chủ đề trôi quá xa. Trần ~3–5 lần iterate. Trước khi restart: bảo AI tóm tắt context thành 5 bullet để mang sang chat mới.

Delegation-Diligence loop giải quyết câu hỏi gì? Bước nào là mấu chốt?
?
Câu hỏi: "với task *cụ thể của tôi*, làm sao biết AI đáng tin?". Mấu chốt: test trên **data CŨ đã biết đáp án (ground truth)**, không phải data mới — không có đáp án thì "kiểm tra" cũng chỉ là tin bằng cảm giác.

Vì sao "AI trả lời trôi chảy" không đủ để tin giao việc thật?
?
Trôi chảy chỉ chứng minh AI viết tốt, không chứng minh đúng (hallucination: bịa số/fact với giọng mượt). Phải thẩm định có ground truth trước; mức review tỉ lệ với stakes.

<!-- ===== Buổi 2 (2026-05-30) — Chat / Cowork / Code ===== -->

Chat vs Cowork khác nhau ở "ai lái" và "đơn vị công việc" thế nào?
?
**Chat**: 1 lượt = 1 câu trả lời, *bạn* lái từng bước (đồng nghiệp ghé bàn hỏi 1 câu). **Cowork**: 1 *mục tiêu* = nhiều giờ, *Claude* tự lập plan + thực thi (đồng nghiệp nhận project cả tuần).

Cowork và Code chung cái gì bên dưới? Điều đó nói lên gì về Cowork?
?
Chung **engine Claude Code**. → "Làm việc dài hơi" (viết phần mềm hay rà 50 hợp đồng) là cùng một bộ máy agentic: chia task, chạy nhiều bước, gọi subagent, dùng tool. Cowork = bộ máy đó khoác giao diện cho người không-code.

Cowork vs Code: phạm vi truy cập khác nhau ra sao?
?
**Cowork** = workspace giới hạn, chỉ folder bạn share (knowledge work, an toàn hơn). **Code** = full project: file system, terminal, git, dev tools (làm phần mềm thật).

Ask / Code / Plan — mỗi mode đánh đổi gì?
?
**Ask**: đề xuất từng thay đổi, chờ duyệt (visual diff) — kiểm soát cao nhất, chậm. **Code**: tự áp file, chỉ hỏi trước khi chạy lệnh — cân bằng, mặc định. **Plan**: vạch toàn bộ chiến lược trước khi đụng — cho refactor phức tạp.

Quy tắc chọn Chat / Cowork / Code?
?
≤3 bước, hỏi-đáp nhanh → **Chat**. >3 bước hoặc cần folder/tool ngoài → **Cowork**. Đụng codebase (sửa code, test, commit) → **Code**.

Vì sao gõ lại prompt "daily brief" mỗi sáng là anti-pattern? Sửa thế nào?
?
Lặp setup tay = ~25h/năm/task lãng phí. Sửa: dùng **Scheduled Task** trong Cowork — định nghĩa task + lịch 1 lần, Claude tự chạy mãi (máy tắt thì catch-up khi mở lại).

<!-- ===== Buổi 3 (2026-05-30) — Projects / Artifacts / Skills ===== -->

Câu thần chú phân biệt Projects vs Skills? WHAT/HOW là cái nào?
?
**"Projects store knowledge. Skills perform tasks."** Project = cái **WHAT** (thông tin Claude cần biết). Skill = cái **HOW** (quy trình Claude làm). Bổ trợ, không thay thế.

Progressive disclosure là gì? Vì sao cài 50 skill mà context không bloat?
?
Nạp dần: lúc nghỉ chỉ nạp tên+mô tả (~30–50 token/skill); khi prompt khớp mới nạp full SKILL.md; file phụ nạp khi cần. Nên cài nhiều skill mà context vẫn nhẹ (thấy rõ trong `/context`).

Vì sao `description` của một skill lại tối quan trọng?
?
Vì nó là thứ DUY NHẤT Claude thấy lúc nghỉ (progressive disclosure) → quyết định skill có được đánh thức đúng lúc không. Description tồi = skill có cũng như không.

Khi nào KHÔNG nên tạo skill?
?
Khi skill chung chung, không có methodology/template/ràng buộc cụ thể (vd "viết nội dung hay hơn") → không hơn gì Claude mặc định. Trường hợp đó dùng một prompt tốt là đủ.

Knowledge base vs conversation-level: quy tắc "lần thứ 2"?
?
Upload ≥2 lần / dùng đi dùng lại (brand guide, template) → **knowledge base** (mọi chat thấy). Upload 1 lần, chỉ relevant 1 chat → để **conversation-level**.

Artifact tương tác (calculator, dashboard) xong có nên tin ngay không? Vì sao?
?
Không. Artifact tương tác CÓ logic → có thể sai công thức/bug. Phải test 3–5 input trước khi ship — đúng tinh thần "trôi chảy ≠ đúng" (Discernment).

<!-- ===== Buổi 4 (2026-06-03) — Connectors/MCP + Enterprise Search + Research ===== -->

Vì sao công ty có tool nội bộ KHÔNG cần chờ Anthropic để Claude kết nối được?
?
Vì **MCP là chuẩn mở** (USB-C cho AI) — spec công khai, team tự viết **MCP server** cho tool của mình theo chuẩn → Claude (và mọi AI hỗ trợ MCP) cắm vào dùng ngay. Connector mọc từ cộng đồng, không từ Anthropic.

Web connector vs Desktop extension khác nhau ở đâu?
?
**Web**: cloud services (Slack, Drive, Jira...), chạy cả web + desktop. **Desktop extension**: chạy **local** qua Claude Desktop — access file system, native app, browser control; không có trên web.

Đồng nghiệp định cài MCP server vô danh từ GitHub vào máy có Gmail công ty — rủi ro THẬT là gì (và không phải là gì)?
?
KHÔNG phải "lộ toàn bộ hệ thống" — server chạy bằng credentials người cài, chỉ với tới data *của người đó*. Rủi ro thật: **exfiltrate inbox của họ** (vẫn đủ thành sự cố) + code local có thể xin thêm quyền file system. Quy trình: trusted source → review code → sandbox → minimal permissions.

Vì sao nói "security boundary của bạn = security boundary của Claude"?
?
Mọi feature kết nối (Connectors, Enterprise Search, Research+integrations) chạy bằng **OAuth credentials của chính bạn** → tool gốc enforce phân quyền như khi bạn login tay. Claude thấy đúng cái bạn thấy — không hơn. Hệ quả: quyền của bạn chính là attack surface → grant tối thiểu.

Enterprise Search khác gì "chat thường + connectors tự cắm"?
?
Connectors tự cắm = hộp đồ nghề **của bạn** (tự setup từng cái, phải biết data ở tool nào). Enterprise Search = hộp đồ nghề **của cả org, sắp sẵn**: admin setup 1 lần, custom instructions, Claude tự search nhiều nguồn đồng thời. Nhưng user vẫn authenticate credentials riêng → permissions không đổi.

4 câu hỏi → 4 tool: chọn thế nào giữa Web search / Extended Thinking / Enterprise Search / Research?
?
Quick fact 1-2 nguồn → **Web search** (giây). Suy luận thuần không cần info ngoài → **Extended Thinking**. Knowledge nội bộ org → **Enterprise Search** (~30s). Đa nguồn + report + citation → **Research** (5-45 phút).

Muốn chạy Research về domain mình mù tịt — làm sao viết được [SECTIONS]?
?
2 nhịp: (1) sections sinh từ **quyết định của bạn** (lo tiền → mục chi phí; phải chọn → mục khuyến nghị), không cần biết domain; (2) phần domain-specific → **chat thường nhờ Claude draft prompt trước** ("sections nào hữu ích? constraints nào nên có?"), duyệt xong mới bấm Research. 3-5 phút craft đỡ 30-60 phút report rác.

<!-- ===== Buổi 5 (2026-06-08) — Use cases by role + Flavors + Tổng kết khóa ===== -->

Công thức chấm điểm chọn use case đầu tiên? Tiêu chí nào nặng nhất, nhẹ nhất, vì sao?
?
`Frequency×3 + Time saved×2 + Setup effort×1 + Variability×2`. **Frequency ×3 nặng nhất** (làm càng thường, lợi ích càng cộng dồn). **Setup ×1 nhẹ nhất** vì setup chỉ tốn *một lần*, còn lợi ích lặp mãi.

Vì sao "chọn việc tốn nhiều giờ nhất mỗi lần để tự động hóa trước" là bẫy?
?
Vì nó chỉ nhìn **một lần**, quên tần suất. Việc ngốn 4h nhưng cả quý 1 lần thua xa việc 15 phút làm mỗi ngày. Insight: **tần suất × độ ổn định ăn đứt thời-gian-mỗi-lần**.

"Claude" có phải là trang claude.ai không? "Flavor" nghĩa là gì?
?
Không. **Claude là trí tuệ**; claude.ai chỉ là một cánh cửa. Flavor = cùng trí tuệ đó đặt ngay nơi bạn làm việc (Code/Slack/Excel/Chrome) để cắt cú nhảy tool (~30s + đứt tập trung mỗi lần).

Khi so 2 flavor nên hỏi câu gì? (KHÔNG phải "cái nào thông minh hơn")
?
Hỏi **"cái này cắt được thao tác thừa nào?"** — vì cùng một trí tuệ Claude cả, khác nhau ở **ma sát thao tác**. VD Claude for Excel sửa thẳng trong file đang mở, cắt vòng upload→tải→ghép tay của claude.ai.

Claude for Chrome có gì phải dè chừng?
?
Đang là **research preview** (chưa tôi luyện kỹ) → chỉ việc low-stakes + web tin cậy. KHÔNG dùng cho giao dịch ngân hàng, nhập dữ liệu nhạy cảm, quyết định rủi ro cao.

Công thức C-T-R viết prompt gồm 3 phần nào? Phần nào người ta hay quên?
?
**Context** (bạn là ai, làm gì, cho ai) + **Task** (động từ, làm gì cụ thể) + **Rules** (tone, format, độ dài, ràng buộc). Hay quên nhất là **Context** — mà đó là chữ quan trọng nhất: "Claude mang trí tuệ, BẠN mang context; prompt rỗng context → output rỗng".
