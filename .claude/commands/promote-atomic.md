---
description: Promote atomic notes seed → growing → evergreen theo tiêu chí link/tuổi/usage. Có thể chạy batch (không arg) hoặc cho 1 slug.
argument-hint: [<slug-atomic>] (optional — không có thì quét batch)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Promote Atomic — nâng status seed → growing → evergreen

Sử dụng agent **librarian**. Trả lời bằng tiếng Việt.

Mục đích: định kỳ (quý hoặc khi cảm thấy "vault có note nhưng chẳng có note nào chín") đánh giá lại độ trưởng thành của atomic notes. Atomic không chín → không bao giờ thành output thật.

## Quy tắc bất biến

- ❌ KHÔNG tự promote — luôn đề xuất, chờ user duyệt từng cái (hoặc "tất cả").
- ❌ KHÔNG demote (evergreen → growing) qua command này — nếu cần demote, user làm thủ công.
- ✅ Mọi lần promote → ghi entry vào `99_Meta/CHANGELOG.md`.
- ✅ Chỉ sửa frontmatter `status:`, KHÔNG đổi nội dung body.

## Tiêu chí promote (rule-based, có thể override bằng tay)

### seed → growing

Đạt **≥2 trong 3** điều kiện sau:

1. Có **≥2 link `[[...]]` out** (note liên hệ tới note khác).
2. Đã được edit ít nhất 1 lần sau khi tạo (file `modified` > `created` ≥ 1 ngày — kiểm bằng `git log -- <file>` nếu repo có Git, hoặc qua `created` frontmatter vs ngày hiện tại ≥ 14 ngày).
3. Có **≥1 link in** từ note khác (note khác `[[link]]` đến nó — grep `[[<slug>]]` trong vault).

### growing → evergreen

Đạt **≥2 trong 3** điều kiện sau:

1. Có **≥3 link out** + **≥2 link in** (note thật sự nằm trong mạng lưới).
2. Đã được dùng trong ít nhất 1 output thực — grep `[[<slug>]]` trong `10_Projects/*/outputs/**/*.md` hoặc `40_Archive/**/outputs/**/*.md`.
3. Tuổi ≥ 60 ngày kể từ `created` (đã ủ đủ lâu, không phải insight non).

## Đầu vào

- **Không argument** → quét toàn bộ `50_Atomic/**/*.md`, batch review.
- **Có `$1`** → chỉ xét 1 atomic note có slug = `$1` (vd: `self-attention-la-weighted-sum`).

## Việc cần làm

### Phase 1: Inventory

1. Nếu có `$1`: tìm file `50_Atomic/**/<$1>.md`. Không thấy → báo lỗi, dừng.
   Nếu không có `$1`: `Glob` `E:\Claude\SecondBrain\50_Atomic\**\*.md`, bỏ `README.md`.

2. Với mỗi atomic, đọc frontmatter lấy: `type`, `status`, `created`, `tags`.

3. Tính metric cho từng atomic:
   - **link_out**: đếm `[[...]]` trong body (regex `\[\[[^\]]+\]\]`).
   - **link_in**: với mỗi atomic, grep `[[<slug>]]` trong toàn vault (`Glob` `**/*.md`), đếm file khác nhau ref tới nó.
   - **age_days**: `today - created`.
   - **used_in_output**: grep `[[<slug>]]` trong `10_Projects/**/outputs/**/*.md` + `40_Archive/**/outputs/**/*.md`. True nếu ≥1 file ref.

### Phase 2: Đánh giá

Phân loại atomic thành 4 nhóm:

- **A. seed → growing đề xuất**: status hiện tại = `seed` AND đạt ≥2/3 tiêu chí seed→growing.
- **B. growing → evergreen đề xuất**: status hiện tại = `growing` AND đạt ≥2/3 tiêu chí growing→evergreen.
- **C. Không đủ điều kiện**: chưa đạt — báo cáo *thiếu gì* để user biết cần làm gì.
- **D. Đã evergreen / không cần đổi**.

### Phase 3: Trình bày báo cáo

```
## Báo cáo promote — quét <N> atomic

### 🌱 → 🌿 Đề xuất promote seed → growing (<count>)

| # | Slug | Type | Tuổi | link_out | link_in | Lý do đạt |
|---|---|---|---|---|---|---|
| 1 | <slug> | concept | 18d | 3 | 1 | ✓ ≥2 link out, ✓ ≥1 link in |
| 2 | <slug> | claim | 30d | 2 | 0 | ✓ ≥2 link out, ✓ tuổi ≥14d |

### 🌿 → 🌳 Đề xuất promote growing → evergreen (<count>)

| # | Slug | Type | Tuổi | link_out | link_in | used_in_output | Lý do đạt |
|---|---|---|---|---|---|---|---|
| 3 | <slug> | method | 72d | 5 | 3 | ✓ (thread-quan-ly-context.md) | ✓ links đủ, ✓ đã dùng output |

### ⏳ Chưa đủ điều kiện (<count>)

| Slug | Status hiện tại | Thiếu gì |
|---|---|---|
| <slug> | seed | Chỉ 1 link out, chưa ai ref tới, tuổi 5d → đợi thêm |
| <slug> | growing | 4 link out nhưng chưa dùng trong output, tuổi 40d → cần ship output dùng note này |

### 🌳 Đã evergreen (<count>)
- [[<slug-1>]], [[<slug-2>]], ...
```

### Phase 4: DỪNG chờ duyệt

```
Promote cái nào?
  - 'tất cả' — promote hết nhóm A + B
  - 'A' — chỉ nhóm seed → growing
  - 'B' — chỉ nhóm growing → evergreen
  - '1,3,5' — chọn số cụ thể (theo cột # trong báo cáo)
  - 'bỏ qua' — không làm gì
```

### Phase 5: Thực thi (chỉ khi user duyệt)

Với mỗi atomic được chọn:

1. Dùng `Edit` đổi frontmatter `status: <cũ>` → `status: <mới>`.
2. Thu thập thông tin vào danh sách log.

### Phase 6: Log CHANGELOG

Append entry vào `99_Meta/CHANGELOG.md`:

```markdown
## YYYY-MM-DD — Promote atomic notes (batch / single)

**Bối cảnh:** quét định kỳ qua `/promote-atomic`. <N> atomic được nâng status.

### 🌿 Promote status

| File | Thay đổi | Lý do |
|---|---|---|
| `50_Atomic/<type>/<slug>.md` | `status: seed` → `status: growing` | 3 link out, 1 link in, tuổi 18d |
| `50_Atomic/<type>/<slug>.md` | `status: growing` → `status: evergreen` | 5 link out, đã dùng trong `thread-quan-ly-context.md` |
```

### Phase 7: Báo cáo cuối

```
✅ Promote xong:
  🌱 → 🌿 <count> note
  🌿 → 🌳 <count> note
  📜 CHANGELOG: đã ghi entry <ngày>

💡 Note còn lại không promote — gợi ý hành động:
  - <slug>: thiếu link in → mở MOC chủ đề, link ngược vào
  - <slug>: chưa dùng output → đưa vào dàn ý deliverable tiếp theo
```

## Edge cases

- **Atomic không có frontmatter `status`**: coi như `seed`, đề xuất thêm field nếu user duyệt.
- **`created` parse fail** (sai format hoặc thiếu): bỏ tiêu chí tuổi cho note đó, ghi chú "(chưa rõ tuổi)".
- **Slug trùng giữa 2 folder**: cảnh báo, không tự đoán — yêu cầu user chỉ rõ.
- **Link in tự đếm bản thân**: file ref `[[<chính-slug>]]` của chính nó (hiếm) → loại trừ.
