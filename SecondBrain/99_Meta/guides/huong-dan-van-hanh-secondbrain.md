 ---
type: guide
topic: secondbrain-workflow
created: 2026-05-24
updated: 2026-06-08
tags: [guide, secondbrain, workflow, meta]
status: active
---

# 📘 Hướng dẫn vận hành SecondBrain — từ "lưu trữ" sang "tái sử dụng"

> Tài liệu này dành cho **bản thân tôi**. Mục tiêu: biến vault từ "kho note đọc xong quên" thành "công cụ sản xuất output". Đọc lại mỗi tháng, cập nhật khi workflow thay đổi.

---

## 0. Triết lý gốc — đọc lại mỗi khi nản

Vault này **không phải Wikipedia cá nhân**. Mỗi note tồn tại vì 1 trong 3 lý do:

1. **Sẽ được tái sử dụng** trong output thực tế (blog, video, lecture, code, quyết định)
2. **Là nguồn nguyên liệu** để chắt lọc thành thứ ở (1)
3. **Là sổ mục lục** giúp tìm lại (1) và (2) nhanh

Note nào không thuộc 3 loại trên → archive hoặc xóa khỏi đầu. **Khối lượng không phải KPI; output mới là.**

> **Test kim loại:** sau 6 tháng, nếu mở vault ra mà không có note nào từng được dùng để sản xuất ra cái gì → hệ thống đã thất bại, bất kể đẹp đến đâu.

---

## 1. Mô hình 3 phase

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  PHASE 1: NẠP   │ →  │ PHASE 2: CHẮT   │ →  │ PHASE 3: TÁI    │
│                 │    │       LỌC       │    │   SỬ DỤNG       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ Đọc paper/video │    │ Tách atomic     │    │ Output thực:    │
│ Source note đầy │    │ notes nhỏ       │    │ blog, video,    │
│ đủ (TL;DR, ý,   │    │ Mỗi note 1 ý    │    │ lecture, tweet, │
│ trích dẫn)      │    │ Link liên hệ    │    │ quyết định      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ 00_Inbox/       │    │ 50_Atomic/      │    │ 10_Projects/    │
│ 10_Projects/    │    │ (qua MOC index) │    │ <X>/outputs/    │
│  <X>/sources/   │    │ 99_Meta/MOCs/   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       30 phút                30 phút              30-120 phút
       /paper                 /paper               (deliverable)
```

**Lỗi thường gặp:** dừng ở Phase 1 (chìm trong tóm tắt) hoặc Phase 2 (atomize đẹp nhưng không bao giờ mở lại).
**Cách chữa duy nhất:** **luôn có ít nhất 1 deliverable đang chạy** ở Phase 3 để ép Phase 1+2 phải phục vụ nó.

---

## 2. Các loại note và vai trò

| Loại | Folder | Mục đích | Trigger tạo | Ví dụ thực |
|---|---|---|---|---|
| **Source note** | `10_Projects/<X>/sources/`<br>hoặc `00_Inbox/paper-chua-doc/` | Tóm tắt 1 tài liệu đầy đủ. Là *kho nguyên liệu*. | Đọc xong 1 paper/video/bài | `2026-claude-code-101-quan-ly-context.md` |
| **Atomic note** | `50_Atomic/{concepts,claims,methods,questions}/` | 1 ý duy nhất, tự đứng vững, tái sử dụng ≥3 lần. | Phase 2: chắt lọc từ source | `context-window-tai-nguyen-huu-han.md` |
| **MOC (Map of Content)** | `99_Meta/MOCs/` | Sổ mục lục theo chủ đề. Là cửa vào duy nhất khi cần dùng atomic. | Khi 1 chủ đề có ≥5 atomic | `claude-code-MOC.md` |
| **Output** | `10_Projects/<X>/outputs/` | Sản phẩm cuối: bài viết, slide, kịch bản, thread | Phase 3: deliverable | `thread-quan-ly-context.md` |
| **Daily** | `60_Daily/<năm>/<tháng>/` | Sổ tay ngày. Ghi "đã làm gì với vault hôm nay". | Mỗi sáng | `2026-05-24.md` |
| **Area note** | `20_Areas/<area>/` | Kinh nghiệm đúc kết về vai trò (dạy/nghiên cứu/coding). | Khi rút bài học cá nhân | (chưa có nhiều) |
| **Resource** | `30_Resources/<chủ-đề>/` | Bài blog/khóa học/video người khác viết hay. | Khi muốn lưu reference. | (chưa có nhiều) |

**Nguyên tắc vàng:** Atomic là **đơn vị tái sử dụng**, source là **đơn vị truy vết nguồn**, MOC là **đơn vị khám phá lại**. Đừng nhầm vai trò.

---

## 3. Workflow hàng ngày (10–15 phút)

Mỗi sáng (hoặc cuối ngày):

1. Mở daily note hôm nay (`/daily` skill).
2. Trả lời 3 câu trong daily:
   - **Hôm nay tôi sẽ đẩy deliverable nào tiến lên?** (Phase 3 commitment)
   - **Có nguồn mới nào cần nạp?** (Phase 1)
   - **Có atomic note nào còn dở, cần hoàn thiện?** (Phase 2)
3. Nếu có cuộc họp/bài học/insight bất chợt → ghi nhanh vào `00_Inbox/y-tuong-chot/` (1 file/ý, slug ngắn).
4. **Không atomize ngay** — để ý tưởng "ủ" 1–2 ngày, chắt lọc khi vào batch hàng tuần.

> Không bắt buộc viết note mới mỗi ngày. **Bắt buộc** review daily 1 lần/ngày.

---

## 4. Workflow hàng tuần (Sunday review, 45–60 phút)

Chủ Nhật cuối tuần (hoặc rảnh nhất):

### Bước 1 — Dọn Inbox (10 phút)
Dùng skill `/inbox-clean`. Quyết định từng file:
- **Project đang chạy?** → move sang `10_Projects/<X>/`
- **Kinh nghiệm cá nhân?** → `20_Areas/`
- **Resource người khác?** → `30_Resources/`
- **Ý chốt dùng được nhiều lần?** → atomize (xem Bước 3)
- **Không xài nữa?** → `40_Archive/`

### Bước 2 — Atomize nguồn đã đọc (15 phút)
Với mỗi source note tuần này:
- Dùng skill `/paper-atomize` để tách 2–5 atomic notes.
- **Chỉ atomize ý nào pass test "tái sử dụng ≥3 lần"** — ý chỉ dùng được trong duy nhất paper đó thì để nguyên trong source, không atomize.

### Bước 3 — Link và cập nhật MOC (10 phút)
- Mở `/moc-update` skill → quét atomic notes chưa được index.
- Với mỗi atomic mới: mục "## Liên hệ" giữ **tối đa 2 link load-bearing** + dòng `- Trích từ: [[source]]`. Atomic không bị mồ côi nhờ **được MOC index**, không phải nhờ nhồi nhiều link ngang (xem mục 15).
- Thêm atomic mới vào MOC chủ đề tương ứng.

### Bước 4 — Đẩy 1 deliverable (15 phút tối thiểu)
Mỗi tuần **bắt buộc** đẩy ít nhất 1 deliverable tiến 1 bước:
- Có thể là 1 paragraph blog, 1 tweet, 1 slide, 1 đoạn lecture.
- **Khi viết, mở MOC trước, không mở Google.** Nếu MOC không đủ → ghi lại "lỗ hổng tri thức" làm question note ở `50_Atomic/questions/`.

---

## 5. Workflow theo deliverable (Phase 3 chi tiết)

Mỗi khi cần sản xuất output (blog/video/lecture/thread/quyết định):

```
1. Xác định chủ đề → mở MOC tương ứng (99_Meta/MOCs/)
2. Quét MOC, pick ≤7 atomic notes phù hợp nhất với deliverable
3. Mở từng atomic note → đọc chính nó + theo link [[...]] thêm 1 cấp
4. Lập dàn ý: mỗi mục dàn ý = 1 atomic note
5. Viết draft: mỗi đoạn paraphrase từ atomic (KHÔNG copy-paste)
6. Trong draft, link [[...]] tới atomic gốc (nếu output là markdown nội bộ)
7. Output đặt ở 10_Projects/<X>/outputs/<slug>.md
8. Sau khi xong: ngược lại cập nhật atomic — nếu phát hiện ý mới khi viết
   → bổ sung vào atomic gốc (network effect: output làm note giàu hơn)
```

**Test xem deliverable này đã xài bộ não 2 đủ chưa:**
- ✅ Dàn ý có ít nhất 3 mục map 1-1 với atomic notes có sẵn
- ✅ Đã mở MOC ít nhất 1 lần trong lúc viết
- ✅ Đã thêm ≥1 link `[[...]]` mới giữa atomic notes nhờ làm deliverable này
- ❌ Nếu không có 1 cái nào → deliverable không tận dụng vault, hệ thống chưa sinh giá trị

---

## 6. Workflow theo nguồn mới (Phase 1+2 chi tiết)

Khi gặp nguồn mới đáng nạp (paper, video YouTube dài, bài blog sâu, sách):

```
1. Quyết định nguồn này có đáng nạp không?
   - Có dùng được cho project đang chạy / area đang phát triển? → có
   - Chỉ "đọc cho biết"? → đừng nạp, đánh dấu xong
   
2. Skill /paper-full chạy cả 3 bước:
   2a. Tóm tắt → source note đầy đủ ở 00_Inbox/paper-chua-doc/ hoặc 10_Projects/<X>/sources/
   2b. Đề xuất 2-3 atomic notes có thể tách ra (chờ user xác nhận)
   2c. Tìm note cũ liên quan trong vault, gợi ý [[wiki link]]

3. User xác nhận atomic nào nên tách → /paper-atomize tách thành 50_Atomic/
   QUAN TRỌNG: atomic notes BẮT BUỘC nằm ở 50_Atomic/, KHÔNG ở 10_Projects/

4. Cập nhật MOC chủ đề → thêm atomic mới vào đúng section

5. Trong section "📚 Đã chắt lọc" của daily note hôm đó, ghi:
   - Source: [[<slug>]]
   - Atomic mới: [[<slug-1>]], [[<slug-2>]]
```

---

## 7. Quy tắc viết atomic note tốt

Atomic note **chết** = atomic không bao giờ được mở lại. Cách tránh:

| Tiêu chí | Pass | Fail |
|---|---|---|
| **1 ý duy nhất** | "Prompt cụ thể tiết kiệm context hơn prompt ngắn" | "Mọi thứ về prompt engineering" |
| **Tự đứng vững** | Đọc mình nó hiểu được, không cần đọc source | "Như đã nói ở Bài 2.5..." (cần context bên ngoài) |
| **Tiêu đề là câu hoàn chỉnh** | `prompt-cu-the-tiet-kiem-context-hon-prompt-ngan.md` | `prompt.md`, `note-1.md` |
| **Liên kết đúng mức** | ≤2 link ngang load-bearing + được MOC index + có link nguồn | Cô lập hoàn toàn, HOẶC nhồi mọi link "cùng tinh thần" |
| **Có "Quan điểm của tôi"** | Bạn đồng ý/phản biện gì, confidence level | Chỉ tóm tắt người khác |
| **Có nguồn truy vết** | Link về source note | Không rõ từ đâu ra |
| **Tái sử dụng ≥3 lần** | Dùng được trong nhiều context khác nhau | Chỉ dùng được trong 1 paper đó |
| **Trẻ 5 tuổi hiểu được (ELI5)** | "Tưởng tượng cả lớp nhìn nhau, ai quan trọng thì nghe nhiều hơn" | "Tính trọng số softmax trên dot-product Q·K" mà không giải thích bằng lời thường |

> **ELI5 — giải thích như cho trẻ 5 tuổi:** thân atomic phải đơn giản tới mức một đứa trẻ 5 tuổi cũng nắm được ý chính. Dùng ví dụ/phép so sánh đời thường (mở đầu "Tưởng tượng..." rất tốt), câu ngắn, từ quen thuộc. Thuật ngữ kỹ thuật chỉ giữ ở tiêu đề hoặc khi bắt buộc — và giải thích ngay sau đó bằng lời thường. Đây là kỹ thuật Feynman: viết được đơn giản nghĩa là bạn đã thực sự hiểu.

Frontmatter chuẩn:
```yaml
---
type: concept | claim | method | question
created: YYYY-MM-DD
tags: [chủ-đề-chính, chủ-đề-phụ]
status: seed | growing | evergreen
confidence: low | medium | high   # chỉ với claim
---
```

---

## 8. Vai trò Claude Code trong workflow này

Claude Code là **trợ lý vận hành vault**, không phải thay thế suy nghĩ của bạn.

| Skill / Agent | Khi dùng | Output |
|---|---|---|
| `/daily` | Mỗi sáng | Mở/tạo daily note rỗng từ template (tôi tự điền) |
| `/daily-write` | Cuối ngày (hoặc bất kỳ) | Tự viết daily: quét git + vault hôm nay, điền "Việc xong/chưa xong" + "Đã chắt lọc"; gắn marker `_(auto)_`, không chạm phần kế hoạch/quan điểm của tôi |
| `/paper-summarize` | Có nguồn mới, chỉ cần tóm tắt | Source note ở 00_Inbox hoặc project |
| `/paper-atomize` | Source note đã chín, muốn tách atomic | Atomic notes ở 50_Atomic/ |
| `/paper-full` | Nguồn mới + muốn chạy nguyên workflow | Source + đề xuất atomic + link |
| `/link-notes` | Đang viết note, muốn tìm note cũ liên quan | List `[[...]]` gợi ý |
| `find-related-notes` skill | Trước khi viết note mới về X | List note đã có về X |
| `/inbox-clean` | Sunday review, dọn 00_Inbox | Đề xuất move (không tự move) |
| `/moc-update` | Sunday review, sync MOC | List atomic chưa index |
| `/archive-project <tên>` | Project xong, chuyển sang 40_Archive | Checklist → update note dự án → log CHANGELOG → move folder |
| `/promote-atomic [<slug>]` | Định kỳ (quý) nâng status seed→growing→evergreen | Báo cáo theo tiêu chí link/tuổi/usage, chờ duyệt từng note |
| Agent `researcher` | Đọc paper khó/dài, cần chuyên sâu | Source note chi tiết |
| Agent `creator` | Sản xuất output dài (blog, video script) | Output ở 10_Projects/<X>/outputs/ |
| Agent `librarian` | Dọn vault, archive project, audit cấu trúc | Report + action items |

**Quy tắc:** Claude **đề xuất**, bạn **quyết định**. Không bao giờ để Claude tự move/delete/atomize mà không xác nhận.

---

## 9. Checklist tự kiểm hàng tháng

Mở vault, kiểm 7 câu này. Nếu ≥5 câu "không" → workflow đang lệch, ngồi xuống fix.

1. ☐ Tháng này tôi đã sản xuất ≥1 output (Phase 3) dùng atomic notes có sẵn?
2. ☐ Mỗi atomic tháng này: ≤2 link ngang load-bearing, được MOC index, có link nguồn?
3. ☐ MOC chủ đề chính tôi đang theo đã được cập nhật trong 30 ngày qua?
4. ☐ Inbox (`00_Inbox/`) có ≤10 file pending (không ứ đọng)?
5. ☐ Có ≥1 project đang Active ở `10_Projects/` (vault không "ngủ đông")?
6. ☐ Tôi có thể nói ngay 3 atomic notes hữu ích nhất tháng này (chứng tỏ dùng thật, không chỉ tạo)?
7. ☐ Daily notes 30 ngày qua điền ≥70% ngày (không bỏ bê)?

---

## 10. Anti-patterns thường gặp — tự nhận diện

### ❌ "Collector's fallacy" — sưu tầm thay vì dùng
**Triệu chứng:** Lưu paper liên tục, atomize đẹp, nhưng không bao giờ mở lại.
**Chữa:** Luật 1-deliverable — luôn có 1 output đang chạy, mọi nạp/chắt lọc phải phục vụ nó.

### ❌ "Note quá to" — atomic không atomic
**Triệu chứng:** Một note 500+ dòng cover nhiều ý.
**Chữa:** Mỗi atomic 1 ý. Note dài là source, không phải atomic.

### ❌ "Note cô lập" — không vào MOC
**Triệu chứng:** Atomic mới tạo không link gì và không được MOC nào index.
**Chữa:** Thêm 1–2 link ngang load-bearing + đảm bảo MOC chủ đề có index nó. (Đừng nhồi link cho đủ số — xem mục 15.)

### ❌ "Over-link / quạt trùng" — graph lằng nhằng
**Triệu chứng:** Mỗi atomic link 4–6 note "cùng tinh thần"; nhiều hub (MOC + _track + daily + note nguồn) cùng fan tới một bộ atomic → mạng nhện.
**Chữa:** Mỗi atomic ≤2 link load-bearing; mỗi node một vai trò; ẩn node log/provenance khỏi global graph (mục 15).

### ❌ "MOC trống" — không có sổ mục lục
**Triệu chứng:** Có 30 atomic notes nhưng không MOC nào → không tìm lại được.
**Chữa:** Sau 5 atomic cùng chủ đề → tạo MOC ngay.

### ❌ "Folder spaghetti" — không theo PARA
**Triệu chứng:** Note nằm sai folder, không nhớ logic.
**Chữa:** Đọc lại bảng quyết định ở `SecondBrain/.claude/CLAUDE.md`.

### ❌ "Daily note formal quá" — biến daily thành báo cáo
**Triệu chứng:** Bỏ qua daily vì "không có gì để báo cáo".
**Chữa:** Daily là sổ tay cá nhân, 3 dòng cũng đủ. Mục tiêu là *liên tục*, không phải *hoàn chỉnh*.

### ❌ "Atomize ngay khi đọc" — không ủ đủ lâu
**Triệu chứng:** Vừa đọc paper xong atomize ngay → atomic thường lặp lại source, không có insight cá nhân.
**Chữa:** Để 1–2 ngày ủ. Atomize trong Sunday review khi đã có khoảng cách.

---

## 11. Roadmap trưởng thành vault

| Giai đoạn | Đặc điểm | Khoảng atomic | Mục tiêu |
|---|---|---|---|
| **Seed** (tuần 1–4) | Vault sơ khai, vài atomic, chưa có output | <20 | Cài thói quen daily + 1 deliverable nhỏ |
| **Sapling** (tháng 2–3) | Có 2–3 MOC, đã ship 1–2 output từ vault | 20–80 | Network effect bắt đầu xuất hiện |
| **Tree** (tháng 4–12) | MOC dày đặc, output ra đều, atomic re-link nhau tự nhiên | 80–300 | Mỗi output mới chỉ cần ráp atomic có sẵn |
| **Forest** (năm 2+) | Atomic notes giàu, link mạng nhện, vault tự gợi ý ý mới | 300+ | Vault sản sinh ý tưởng mới qua link |

**Hiện tại bạn ở đâu?** (2026-05-24) — 16 atomic, 3 MOC, chưa có output từ vault → đang ở **cuối Seed, đầu Sapling**. Mục tiêu 3 tháng tới: lên Sapling vững — ship 2–3 output, đạt 40–50 atomic chất lượng.

---

## 12. Cấu trúc thư mục tham chiếu nhanh

```
SecondBrain/
├── 00_Inbox/              # Buffer, dọn hàng tuần
│   ├── y-tuong-chot/      # Ý vụt qua, chưa phân loại
│   └── paper-chua-doc/    # Paper chưa gắn project
│
├── 10_Projects/           # Việc đang chạy, có deadline / mục tiêu
│   └── <project>/
│       ├── <project>.md   # Folder note: mục tiêu, status, deadline
│       ├── sources/       # Phase 1: source note
│       ├── notes/         # Ghi chú họp, sinh viên
│       └── outputs/       # Phase 3: deliverable thực tế
│
├── 20_Areas/              # Vai trò dài hạn (dạy, nghiên cứu, coding)
├── 30_Resources/          # Tài liệu người khác có thể đáng dùng lại
├── 40_Archive/            # Project / area đã xong, không xóa
│
├── 50_Atomic/             # Phase 2: tri thức tái sử dụng
│   ├── concepts/          # Khái niệm
│   ├── claims/            # Luận điểm có thể tranh luận
│   ├── methods/           # Quy trình / kỹ thuật
│   └── questions/         # Câu hỏi mở chưa trả lời
│
├── 60_Daily/<năm>/<tháng>/   # Daily notes
│
└── 99_Meta/
    ├── MOCs/              # Map of Content per chủ đề
    ├── templates/         # Template các loại note
    └── guides/            # ← Hướng dẫn vận hành (file này)
```

---

## 13. Khi nào đọc lại file này

- ☐ Đầu mỗi tháng (audit)
- ☐ Khi cảm thấy vault "vô dụng" (motivation drop)
- ☐ Trước khi nạp một nguồn lớn (paper >30 trang, sách)
- ☐ Trước khi bắt đầu 1 project mới
- ☐ Khi onboard ai khác vào hệ thống của mình

---

## 14. Quy tắc bảo trì hệ thống — guides & changelog

> File hướng dẫn và changelog là **xương sống** của hệ thống. Không cập nhật → 3 tháng sau quên hết quy ước, lặp lại sai lầm cũ.

### 14.1. Khi có quy tắc/workflow mới → phải vào guides

Bất kỳ thay đổi nào tạo ra **quy tắc mới, command mới, skill mới, agent mới** đều phải được phản ánh trong file này (`huong-dan-van-hanh-secondbrain.md`). Trigger update:

- Tạo command mới (`/<name>`) → thêm dòng vào **bảng mục 8** (Vai trò Claude Code).
- Tạo skill/agent mới → thêm dòng vào mục 8.
- Đổi convention đặt tên / cấu trúc thư mục → update mục 2 (Các loại note) hoặc mục 12 (Cấu trúc thư mục).
- Đổi workflow định kỳ (daily/weekly/monthly) → update mục 3, 4, hoặc 9.
- Đổi tiêu chí atomic / promote / archive → update mục 7 hoặc mục mới tương ứng.
- Đổi quy tắc liên kết / đồ thị (graph) → update mục 15.

**Quy tắc:** *cùng commit / cùng turn* với thay đổi gốc — không "để sau". Nếu Claude làm thay đổi → Claude tự cập nhật guides ngay.

### 14.2. Khi có thay đổi file đang tồn tại → phải vào CHANGELOG

Mọi **edit** file đã có trong vault (do Claude thay mặt) đều phải log vào `99_Meta/CHANGELOG.md`. Quy tắc cụ thể:

| Hành động | Log CHANGELOG? |
|---|---|
| Edit nội dung file đã có (do Claude) | ✅ Bắt buộc |
| Tạo file mới hoàn toàn | ❌ Không (xem `git log --diff-filter=A`) |
| Move file (vd archive project) | ✅ Bắt buộc — ghi cả đường đi từ-tới |
| Đổi tên file | ✅ Bắt buộc — ghi tên cũ + tên mới |
| Promote status atomic (seed → growing → ...) | ✅ Bắt buộc |
| User trực tiếp gõ sửa | ❌ Không (chỉ log khi Claude thay mặt) |
| Sửa MEMORY.md hoặc file ngoài vault | ❌ Không vào CHANGELOG vault — ghi vắn vào entry nếu liên quan |

**Format entry** — xem mẫu cuối CHANGELOG.md, hoặc copy template sau:

```markdown
## YYYY-MM-DD — Tiêu đề đợt sửa

**Bối cảnh:** lý do, link tham chiếu (vd: [[huong-dan-van-hanh-secondbrain]] section X).

### 🔧 <Nhóm thay đổi>

| File | Thay đổi | Lý do |
|---|---|---|
| `path/to/file.md` | Tóm tắt 1 dòng | Vì sao đổi |
```

### 14.3. Thứ tự thao tác (cho Claude khi tự động hóa)

Khi thực hiện thay đổi tự động (qua command, agent, hoặc tự ý đề xuất + user duyệt), thứ tự **bất biến**:

1. **Làm thay đổi gốc** (move file, edit nội dung, tạo file, ...).
2. **Update guides** nếu thay đổi tạo ra quy tắc/command mới (mục 14.1).
3. **Update CHANGELOG** ghi lại thao tác (mục 14.2).
4. **Báo cáo cuối** cho user — liệt kê: gì đã đổi, log ở đâu, cần manual gì.

Bỏ bước nào → coi như chưa xong. Nếu user can thiệp giữa chừng → ghi lại trạng thái hiện tại, không "giả vờ đã xong".

### 14.4. Audit định kỳ guides + CHANGELOG

- **Mỗi tháng** (cùng dịp mục 9): mở guides, đọc lướt — có quy tắc nào không còn dùng? có command nào đã bỏ? Xóa hoặc đánh dấu deprecated.
- **Mỗi quý**: scroll CHANGELOG, gom entry cùng chủ đề thành mục "lịch sử thay đổi" tóm gọn. CHANGELOG quá dài (>500 dòng) → tách file theo năm: `CHANGELOG-2026.md`, `CHANGELOG-2027.md`.

---

## 15. Graph hygiene — quy tắc liên kết & đồ thị

> Graph là **đồ thị tri thức**, không phải đồ thị thao tác. Quy tắc giữ nó dễ đọc, dễ tìm (đúc kết 2026-06-08 sau đợt dọn graph "lằng nhằng"). Đồng bộ với `SecondBrain/.claude/CLAUDE.md` mục "Quy tắc liên kết & đồ thị".

### 15.1. Mỗi node một vai trò (tránh "quạt trùng")
Đừng để nhiều note cùng index một bộ atomic (vd MOC + _track + daily + note nguồn cùng fan tới 18 atomic → mạng nhện chồng nhau).
- **MOC** = mục lục duy nhất theo chủ đề, giữ toàn bộ link + chia nhóm. Mỗi domain lớn một MOC riêng (vd `claude-MOC`, `claude-code-MOC`).
- **Source/course note** = provenance, chỉ fan tới atomic chắt ra từ chính nó.
- **daily** = nhật ký, chỉ link cái tạo ra hôm đó. **_track** = bảng tiến độ, link tối thiểu.
- **atomic** = (được MOC index) + tối đa 2 link ngang load-bearing.

### 15.2. Atomic: "## Liên hệ" tối đa 2 link
Chỉ giữ 2 link mạnh nhất — cái thực sự sẽ bấm theo (note nền tảng / cặp vận hành / đối lập). KHÔNG liệt kê link "cùng tinh thần / anh em" mềm. **Câu cũ "atomic không link = chết" được thay bằng "atomic không vào MOC = chết"** — MOC lo reachability nên cắt link ngang không làm note mồ côi.

### 15.3. Cross-domain bridge tiết kiệm
Nối hai cụm chủ đề chỉ bằng 1–2 nhịp cầu thật đắt giá, đừng dán mọi thứ thành một khối (vd Claude 101 ↔ Claude Code 101 chỉ nối qua `prompt-la-brief↔4d-framework` và `mcp-server-overhead↔mcp-usb-c`).

### 15.4. Provenance source→atomic (bắt buộc khi chắt)
- Đầu "## Nguồn" của atomic: `- Trích từ: [[<source/course note>]]`.
- Source/course note: liệt kê atomic đã chắt ra + link tới MOC.
- Note nguồn một khóa học → `30_Resources/courses/<slug>.md`.

### 15.5. Node nên ẩn khỏi global graph
Loại operational/log/study (không phải tri thức) → lọc qua *Graph settings → Filters*: `daily`, `_track`, `flashcards`, `CHANGELOG`, `CLAUDE`, `README` (chỉ còn README gốc workspace + README các code repo chưa đổi tên), `templates`, `guides`, `00_HOME`, và note nguồn khóa (fan trùng MOC). Provenance/log xem bằng **Local Graph** + Backlinks, không nhồi vào global.

> **Lưu ý (2026-06-11):** note index của mỗi folder PARA không còn tên `README.md` mà đổi theo **folder-note convention** (`<folder>/<folder>.md`, vd `10_Projects/10_Projects.md`, `50_Atomic/50_Atomic.md`). Nhờ vậy khi hiện trong graph chúng có nhãn rõ ràng (hub của folder) thay vì loạt chấm "README" trùng tên. README code repo trong `Projects/` cũng đã đổi tên theo folder.

### 15.6. Baseline `.obsidian/graph.json`
Vault Obsidian mở từ `E:\Claude` nên graph index cả `Projects/` lẫn `SecondBrain/`. Cấu hình hiện tại (2026-06-11) — **graph hiện cả tri thức SecondBrain lẫn cụm Projects**, giữ gọn bằng cách ẩn operational + orphan:
- **Filter:** `-path:".obsidian" -path:".claude" -file:"CHANGELOG" -file:"README" -file:"CLAUDE" -file:"00_HOME" -file:"tag-system" -file:"flashcards" -file:"track" -path:"60_Daily" -path:"99_Meta/templates" -path:"99_Meta/guides"` — ẩn config + node operational (cả vault lẫn root), **không** loại `Projects/`.
- **Color group**: 5 tầng PARA của SecondBrain + `Projects/` (cam) để tách cụm code/dự án khỏi tri thức.
- `showOrphans:false` (đã thử `true` thấy rối → tắt chấm cô đơn; nhờ vậy file Projects lẻ không nối cũng không hiện), `hideUnresolved:true`. Thông số lực/hiển thị (`textFadeMultiplier`, `repelStrength`, `scale`...) do user tự tinh chỉnh trong app.

> Bài học: muốn graph gọn mà vẫn đủ → ẩn theo **vai trò** (operational/config) + tắt orphan, đừng loại nguyên một cây thư mục. Muốn xem "đèn báo" chủ đề chưa chắt → bật tạm `showOrphans`.

---

## Nguồn cảm hứng

- Tiago Forte — *Building a Second Brain* (CODE + PARA)
- Sönke Ahrens — *How to Take Smart Notes* (Zettelkasten, atomic notes)
- Andy Matuschak — *Evergreen notes* (atomic + densely linked)

**Lưu ý:** Cả 3 nguồn trên đáng atomize thành atomic notes riêng nếu bạn đọc kỹ.

---

> *"A second brain is not a collection — it's a workshop."* — Tự nhắc mình.
