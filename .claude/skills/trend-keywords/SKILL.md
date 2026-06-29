---
name: trend-keywords
description: Sử dụng skill này khi cần tìm từ khóa/chủ đề đang HOT (trending) trên thị trường, đo bằng Google Trends. Trigger khi user nói "tìm key trending", "key nào đang hot", "tìm từ khóa hot ở [nước]", "chủ đề nào đang lên", dán link kênh YouTube để phân tích chủ đề, hoặc nhập 1 keyword để đào ngách nhỏ đang hot bên trong nó.
---

# Skill: Trend Keywords — Tìm từ khóa hot bằng Google Trends

Tìm và xếp hạng từ khóa/chủ đề đang trending ở một quốc gia, đo thật trên Google Trends (không bịa số). Hỗ trợ 3 chế độ nhập + đào ngách nhỏ. Output: bảng ~20 key hot nhất theo điểm + danh sách breakout queries.

## Khi nào dùng
- User muốn tìm chủ đề/từ khóa hot cho content (YouTube, blog, SEO, sản phẩm).
- User dán **link kênh YouTube** → phân tích chủ đề trúng của kênh đó.
- User nhập **1 keyword** → tìm ngách nhỏ đang lên trong keyword đó.
- User không nhập gì → tự tìm trending.

---

## BƯỚC 0 — Xác định đầu vào & quốc gia (LUÔN hỏi nếu thiếu)

Hỏi gọn 2 thứ (dùng AskUserQuestion nếu user chưa nói rõ):

1. **Chế độ nào?**
   - **A. Link kênh/đối thủ** — user có link YouTube (hoặc kênh khác) → mổ chủ đề trúng → suy ra seed keyword.
   - **B. Nhập keyword** — user cho 1 từ khóa gốc → đào ngách nhỏ + related queries đang tăng bên trong.
   - **C. Tự tìm** — không có input → quét trending theo lĩnh vực user quan tâm.

2. **Dùng ở quốc gia nào?** → suy ra `geo`, `hl`, và **ngôn ngữ keyword** (interest trên Trends phụ thuộc ngôn ngữ search trong nước đó).

| Nước | geo | hl | Ngôn ngữ keyword |
|---|---|---|---|
| Nhật | JP | ja | tiếng Nhật |
| Mỹ | US | en | tiếng Anh |
| Hàn | KR | ko | tiếng Hàn |
| Việt Nam | VN | vi | tiếng Việt |
| Anh | GB | en | tiếng Anh |
| Đài Loan | TW | zh-TW | tiếng Trung phồn thể |

> Nếu chế độ A (link kênh nước này) nhưng muốn làm thị trường nước khác → **map keyword sang ngôn ngữ nước đích**, đo theo geo nước đích.

---

## BƯỚC 1 — Lấy danh sách keyword ứng viên (candidate pool, ~20–30 từ)

### Chế độ A — Mổ kênh
1. Load browser tools: `ToolSearch "select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__tabs_create_mcp"`
2. `tabs_context_mcp` → `navigate` tới `<link kênh>/videos`.
3. `get_page_text` lấy tiêu đề + **lượt xem** mỗi video (N = nghìn). Bấm tab "Phổ biến/Popular" để xếp theo view nếu cần.
4. Rút **công thức trúng**: nguyên liệu/chủ đề/chỉ số lặp lại + định dạng. Xếp chủ đề theo view.
5. Liệt kê ~20–30 keyword ứng viên (đã map sang ngôn ngữ nước đích).

### Chế độ B — Đào ngách trong 1 keyword
- Keyword gốc là hạt giống. Mở rộng ứng viên = các biến thể + chủ đề con (tự brainstorm theo ngữ cảnh nước đó).
- Phần "ngách nhỏ đang hot" lấy chủ yếu từ **related queries** ở Bước 3.

### Chế độ C — Tự tìm
- Mở `https://trends.google.com/trending?geo=<GEO>` (急上昇/Trending now) + Trends theo category để gom ứng viên trong lĩnh vực user quan tâm.

---

## BƯỚC 2 — Đo trên Google Trends + ANCHOR BRIDGING (cốt lõi)

⚠️ **Hiểu đúng điểm Trends:** số 0–100 là **tương đối trong rổ** — chỉ từ mạnh nhất chạm ~100, trung bình ~78–80; từ khác co lại bên dưới. Không phải điểm tuyệt đối. Vì so tối đa **5 từ/lần**, để xếp hạng >5 từ trên **cùng 1 thang**, dùng **mốc nối (anchor)**.

**Quy trình:**
1. URL explore: `https://trends.google.com/trends/explore?date=today%2012-m&geo=<GEO>&q=<t1,t2,t3,t4,t5>&hl=<HL>`
2. **Mỗi rổ ≤5 từ. Chọn 1 từ ANCHOR cố định xuất hiện ở MỌI rổ** (chọn từ tầm trung, ổn định). Các rổ kế tiếp luôn gồm anchor + 4 từ mới.
3. Sau khi trang load (chờ ~2s nếu cần), **dùng `get_page_text`** (KHÔNG screenshot) — nó trả về:
   - Bảng `平均` (average) chính xác từng từ.
   - Chuỗi thời gian theo tuần (xem rising/seasonal).
   - **関連キーワード/Related queries (注目=rising %, 人気=top)** — mỏ vàng ngách nhỏ.
   - Nếu `get_page_text` lỗi "No text" → cuộn xuống 2–3 nấc, chờ, thử lại.
4. **Chuẩn hóa về thang chung:** lấy giá trị anchor ở rổ đầu làm gốc. Với mỗi rổ sau, nhân tất cả từ trong rổ với `(anchor_gốc / anchor_rổ_đó)`. → mọi từ về cùng 1 thang.
5. Đo bao nhiêu rổ để phủ hết ~20–30 ứng viên.

**Kiểm tra nhất quán:** tỉ lệ giữa 2 từ chung qua các rổ phải xấp xỉ nhau (lệch <15%). Lệch nhiều → đo lại rổ đó.

---

## BƯỚC 3 — Lấy breakout queries (ngách nhỏ đang hot)

- Với mỗi keyword trụ (đặc biệt chế độ B), mở explore **đơn lẻ**: `...&q=<keyword>` → `get_page_text` → đọc **関連キーワード (注目)**.
- Giữ query có `% tăng` cao HOẶC `急激増加 (breakout)`.
- **Lọc noise:** bỏ query do tin tức/người nổi tiếng/game/anime/thú cưng chi phối — chỉ giữ cái khớp ngữ cảnh user.
- Đây chính là "ngách nhỏ đang hot" để ra ý tưởng nội dung.

---

## BƯỚC 4 — Xuất kết quả

### Bảng chính — ~20 key hot nhất (xếp điểm GIẢM DẦN)

| # | Keyword (bản địa) | Nghĩa | Điểm (thang chung) | Tín hiệu | Breakout |
|---|---|---|---|---|---|
| 1 | … | … | 78 | 📈 đang lên / ⏸️ ổn định / 🍂 theo mùa | +800% (nếu có) |

- **Điểm**: thang thống nhất (ghi rõ từ anchor = bao nhiêu).
- **Tín hiệu**: dựa chuỗi thời gian — *đang lên* (cuối kỳ cao), *ổn định*, *theo mùa* (đỉnh theo mùa, sẽ hạ — phải cảnh báo!).

### Mục "🔥 Ngách nhỏ đang hot" — breakout queries
Liệt kê query tăng mạnh nhất (đã lọc noise), kèm % và nghĩa.

### Ghi chú trung thực (BẮT BUỘC)
- Nói rõ điểm là **tương đối** (anchor = X), không phải tuyệt đối.
- Cảnh báo các từ chỉ cao **theo mùa**.
- Nếu candidate pool nhỏ hơn 20 thì nói thật, không độn cho đủ.

---

## Nguyên tắc
- **Đo thật, không bịa số.** Mọi điểm/% phải từ Google Trends thật.
- **Dùng `get_page_text`** ưu tiên hơn screenshot (chính xác + đỡ tốn).
- **Mỗi rổ ≤5 từ, luôn có anchor** — đây là điểm khiến xếp hạng >5 từ đáng tin.
- Tránh rabbit hole: nếu Trends lỗi/không load sau 2–3 lần thử → báo user, không lặp vô hạn.
- Tham khảo case mẫu đã làm: `E:\Claude\Projects\youtube-jp-health\01_KEYWORD_RESEARCH_NHAT.md`.
