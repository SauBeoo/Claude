---
type: source-note
source_type: book-chapter
source_file: Workflow.pdf
title: "Bài 2.4: Workflow Explore → Plan → Code → Commit"
authors: Khóa học "Claude Code 101" — bản tiếng Việt v1.0 (gốc Anthropic)
year: 2026
url: https://notebooklm.google.com/notebook/2a42eeff-a797-44cd-86d5-f8b8a4ee491b
project: claude-code-101
module: "Workflow chuyên nghiệp"
lesson_id: "2.4"
estimated_time: 35 phút
level: Trung cấp
tags: [book-chapter, claude-code, workflow, epcc, plan-mode, course-material]
status: summarized
created: 2026-05-23
---

# Bài 2.4: Workflow Explore → Plan → Code → Commit

## TL;DR

EPCC (Explore → Plan → Code → Commit) là vòng lặp phát triển 4 phase khi làm việc với Claude Code, trong đó **Explore + Plan chiếm ~50% thời gian** nhưng là *investment* để Code phase chạy thẳng. Plan Mode (Shift+Tab) là điểm align rẻ nhất để course-correct trước khi code được viết; subagent reviewer ở Commit phase cung cấp "fresh pair of eyes" bù bias session. Workflow phải **calibrate theo task size** — tiny task skip Explore/Plan, hard task lặp nhiều vòng và commit theo phase. Chương kết bằng 5 anti-patterns thường gặp, 5 mẹo nâng cao, và 2 bài tập áp dụng.

## Mục tiêu học tập (theo tác giả)

Sau bài này người học sẽ có thể:

1. Nắm vững 4 phases của workflow EPCC và mục đích riêng của từng phase.
2. Biết khi nào nên skip phase nào và khi nào cần lặp lại nhiều vòng.
3. Dùng Plan Mode đúng cách để align với Claude trước khi code, tránh course-correct tốn kém.
4. Setup test suite và tools phù hợp để Code phase chạy mượt, ít back-and-forth.
5. Tạo subagent code reviewer cho Commit phase để có "fresh pair of eyes" trước khi push.

## Bối cảnh trong khóa học

Bài 2.4 nằm ở **Module "Workflow chuyên nghiệp"** của khóa Claude Code 101 (tiếng Việt v1.0). Đây là chương trung tâm được tác giả khẳng định ngang trọng số toàn course:

> "If you take one thing away from this course, let it be this workflow." — Boris Cherny, creator of Claude Code (trang 2)

Các bài tiếp theo đều support workflow EPCC:
- **Bài 2.5** — Quản lý Context (`/context`, `/compact`, `/clear`)
- **Bài 2.6** — Code Review và Git Workflow (chi tiết subagent reviewer)
- **Bài 2.7** — File CLAUDE.md (persist workflow rules)

## Mở đầu: Hai dev, cùng task, kết quả ngược nhau

Story Minh vs An — cùng ticket "Add WebP conversion to the image upload pipeline":

- **Minh** (cách cũ): Prompt thẳng "Add WebP conversion…". Claude đoán `upload.ts` + thư viện `sharp`. 20 phút sau build lỗi vì project dùng `jimp`. Pipeline thực ra ở middleware chain. **2 tiếng sau vẫn loay hoay**.
- **An** (EPCC): Shift+Tab → Plan Mode → yêu cầu Claude figure out where + dependencies. Claude khám phá ra pipeline ở `middleware/storage.ts`, project có `jimp` rồi. 5 phút trả plan, An comment yêu cầu xử lý animated GIF, Claude revise, approve, execute, test, commit. **Tổng 25 phút**.

> "Sự khác biệt không phải do An giỏi hơn Minh. Sự khác biệt nằm ở **workflow**."

## EPCC: Bức tranh toàn cảnh

| Phase | Vai trò | Tỷ lệ thời gian (task medium) | Mô tả 1 dòng |
|---|---|---|---|
| **EXPLORE** | Context gathering | ~20% | Đọc files, hiểu patterns |
| **PLAN** | Alignment point | ~30% | Lập plan, review, approve |
| **CODE** | Execution loop | ~40% | Viết code, verify, test |
| **COMMIT** | Confidence gate | ~10% | Review + push, subagent reviewer |

**Lưu ý của tác giả**: Tỷ lệ là *ước tính minh họa* cho task medium complexity (vài giờ). Với task nhỏ hơn, Explore+Plan có thể chỉ chiếm 10-15%. Với task phức tạp (refactor architecture), Plan có thể chiếm 50%+. **Không phải con số cứng**.

**Điều quan trọng nhất**: Explore + Plan = 50% thời gian không phải overhead — là investment để Code chạy thẳng, không zigzag.

## Phase 1: EXPLORE — Đừng để Claude đoán

### Tại sao phase này tồn tại

Claude Code không có sẵn kiến thức về codebase của bạn. Nó không biết:
- Image upload pipeline nằm ở đâu
- Project đã có thư viện nào
- Convention naming function/file của team
- Business logic đặc thù trong pipeline đó

Skip Explore → Claude đoán → đoán sai → debug tốn 30-90 phút.

### Hai cách Explore

**Cách 1 — Plan Mode (read-only)**: Shift+Tab cho tới khi thấy "Plan Mode" dưới text input. Claude chỉ đọc/search/research, không thể edit. Lý tưởng vì:
- Claude không thể "slip" bắt đầu viết code giữa chừng
- Mọi tool call đều read-only (grep, glob, file read, web search)
- Có thể để Claude chạy thoải mái không lo sửa nhầm

**Cách 2 — Prompt explicit** (không cần Plan Mode):
```
Khám phá codebase và cho tôi biết:
- Image upload hiện tại flow như thế nào?
- File nào handle upload logic?
- Thư viện image processing nào đang được dùng?
Đừng thay đổi gì. Chỉ đọc và giải thích.
```

### Explore nên tìm ra điều gì

| Câu hỏi | Tại sao cần biết |
|---|---|
| Feature/pipeline liên quan nằm ở đâu? | Tránh sửa sai file, sai module |
| Pattern hiện tại là gì? | Code mới phải consistent với existing code |
| Dependency nào đã có? | Tránh thêm thư viện trùng lặp |
| Test suite ở đâu? Chạy bằng lệnh gì? | Để Code phase có thể verify sau khi sửa |
| Có constraint nào không rõ ràng? | Business logic ẩn, performance, security rules |

### Anti-pattern: Skip Explore

Triệu chứng phổ biến nhất khi skip Explore:
- Claude viết code dùng thư viện không có trong project (thêm dependency thừa)
- Claude sửa file không phải entry point thực sự
- Code mới không match convention codebase (naming, structure, error handling)
- Build lỗi ngay lần đầu vì môi trường không phù hợp

> **Thời gian tiết kiệm khi skip Explore: 5-10 phút. Thời gian mất thêm khi phải fix: 30-90 phút.**

## Phase 2: PLAN — Nơi rẻ nhất để course-correct

### Tại sao Plan quan trọng hơn Code

Chi phí thay đổi tăng theo phase:
```
Thay đổi trong Plan phase:  $    (chỉnh vài chữ trong plan)
Thay đổi trong Code phase:  $$   (rollback code, viết lại)
Thay đổi sau khi commit:    $$$  (revert PR, re-review, re-test)
```

Plan Mode không phải tính năng luxury — là cơ chế **tiết kiệm tiền và thời gian** hiệu quả nhất khi làm việc với AI.

### Cách vào Plan Mode

`Shift + Tab → Shift + Tab` → cho tới khi status bar hiện "Plan Mode". Claude lúc này không thể edit file — chỉ đọc.

### Cách viết prompt tốt cho Plan phase

Prompt Plan phase phải trả lời 3 câu hỏi:
1. **Task là gì?** (mô tả rõ ràng, không mơ hồ)
2. **Constraints là gì?** (thứ Claude KHÔNG được làm hoặc phải tuân theo)
3. **Success trông như thế nào?** (test suite pass? API trả đúng response? UI render đúng?)

Ví dụ prompt Plan phase chất lượng cao (WebP conversion) — xem case study cuối chương.

### Claude trả plan — bạn làm gì?

**Đừng approve ngay.** Đây là lúc đọc kỹ và hỏi:
- Plan có miss edge case nào không?
- Có bước nào bạn không đồng ý về approach?
- Thứ tự các bước có hợp lý?
- Plan có conflict với architectural decision của team?

Nếu có vấn đề → comment và yêu cầu Claude revise. **Đây là lúc rẻ nhất để thay đổi.**

### Bảng: Plan tốt vs Plan kém

| Tiêu chí | Plan tốt | Plan kém |
|---|---|---|
| Cụ thể | Liệt kê từng file cần sửa, từng function cần thêm | "Modify upload pipeline to support WebP" |
| Thứ tự rõ ràng | Bước 1, 2, 3 logic, dependency rõ ràng | Danh sách không có thứ tự |
| Success criteria | "Test X pass, endpoint Y return Z" | "Feature works" |
| Xử lý edge cases | GIF animated, file size limit, error handling | Chỉ handle happy path |
| Không thêm scope | Chỉ làm đúng yêu cầu | "Và nhân tiện refactor cả module upload" |
| Feasible | Approach khả thi với codebase hiện tại | Assume library/pattern không tồn tại |

### Lặp lại Plan nếu cần

Với task phức tạp, có thể cần nhiều vòng Plan trước khi approve:
```
Round 1: Claude draft plan tổng quan
  → Bạn: "Step 3 cần xử lý race condition — revise"
Round 2: Claude revise, cụ thể hơn về async handling
  → Bạn: "Tốt. Nhưng step 5 dùng jimp chứ không phải sharp"
Round 3: Claude update dependency reference
  → Bạn: "OK, approve."
```

Mỗi vòng revise mất 1-2 phút — tốt hơn nhiều so với debug sau khi code sai.

## Phase 3: CODE — Execute có kiểm soát

### Auto Accept vs Manual Accept

Sau khi approve plan, Shift+Tab thoát Plan Mode, chọn chế độ:

- **Auto Accept** (Shift+Tab → Auto Accept mode): Claude edit file không hỏi từng cái. Nhanh hơn cho task có plan rõ. Tốt khi trust plan đã review. **Cần verify kỹ ở cuối.**
- **Manual Accept** (mặc định): Bạn review từng file edit trước khi Claude apply. Tốt cho task nhạy cảm (security, billing, auth). Là Learning mode — xem Claude làm từng bước. **Chậm hơn nếu plan dài.**

Với task medium (như WebP) → Auto Accept sau khi review plan là hợp lý. Với auth/payment/security → Manual Accept an toàn hơn.

### 3 yếu tố làm Code phase mượt

**Yếu tố 1 — Success criteria explicit**: Claude cần biết "đúng" trông như thế nào. Nói rõ trong plan/prompt:
```
Success = tất cả test trong tests/upload/ pass + không có TypeScript type error + build không fail.
```

**Yếu tố 2 — Add tools phù hợp**:
- **Web UI?** Cài Claude in Chrome extension → Claude control browser tab, test UI trực tiếp, không cần bạn describe lại.
- **Test suite?** Đảm bảo lệnh chạy test rõ ràng (`npm test`, `pnpm test --run`, `pytest -v`). Claude tự chạy sau khi implement.
- **Linting?** Cho Claude biết lệnh lint (`npm run lint --fix`) để tự sửa lint errors.

**Yếu tố 3 — Test suite là source of truth** (quan trọng nhất): Có test suite → Code phase thành vòng lặp tự sửa:
```
Claude implement → chạy test → fail → đọc error → sửa → chạy lại
                          ↑                                  ↓
                          └──────────── lặp tự động ─────────┘
```

Không cần ngồi canh — Claude tự biết khi nào xong (test pass). Không có test → Claude phải hỏi "đúng chưa?" sau mỗi bước → tốn thời gian cả hai.

> **Mẹo**: Trước khi implement, prompt: "Viết test cho feature này trước. Tôi sẽ review test. Sau đó mới implement." Test-driven development với AI cực kỳ hiệu quả.

### Xử lý khi Claude bị kẹt lặp lại

Triệu chứng: Claude mắc đi mắc lại cùng một lỗi → dấu hiệu thiếu context quan trọng.

Cách xử lý:
```
"Claude keep running into the same issue với X.
Hãy lưu solution vào CLAUDE.md để các lần sau không bị lại."
```

Claude viết rule vào CLAUDE.md → session sau không học lại lỗi đó (chi tiết ở Bài 2.7).

### Multi-Claude: Chạy song song cho task lớn

Pattern cộng đồng: *"People run 4-6 Claude instances simultaneously — separate git worktrees, different tasks, no interference."*

```bash
# Terminal tab 1 — feature A
git worktree add ../project-feature-a feature/webp-conversion
cd ../project-feature-a && claude

# Terminal tab 2 — feature B (song song)
git worktree add ../project-feature-b feature/csv-export
cd ../project-feature-b && claude
```

Mỗi instance có context window riêng, branch riêng, không conflict. Chỉ switch tab khi Claude hỏi hoặc cần review.

### Async Accept mode

Shift+Enter khi Claude đang chạy → Async Accept:
- Claude tiếp tục chạy background
- Bạn có thể switch sang task khác hoàn toàn
- Terminal notification khi Claude xong

Hữu ích khi task dài (build + test + fix cycle) mà không muốn ngồi chờ.

## Phase 4: COMMIT — Gate trước khi push

### Tại sao cần phase riêng cho Commit

Với workflow AI-assisted, Commit không chỉ là `git add && commit && push`. Đây là lúc bạn (hoặc subagent reviewer) đọc lại toàn bộ changes với **"fresh eyes"**.

> Claude đã ở trong session đó từ đầu. Nó có **bias** — nó đã viết code đó, nó "biết" code đó "đúng". Subagent reviewer bắt đầu fresh, không có bias đó.

### Subagent code reviewer

Trước khi commit, spawn subagent:
```
Spawn subagent để review tất cả changes tôi vừa làm.
Subagent đọc:
- git diff --staged (hoặc các file tôi vừa sửa)
- Related tests
- CLAUDE.md để check coding standards

Trả về:
1. Summary of changes (2-3 câu)
2. Potential issues hoặc bugs
3. Missing edge cases
4. Code style violations (nếu có)
5. Recommendation: approve to commit hay cần sửa gì
```

Subagent chạy với context window riêng, đọc fresh — "second opinion" rẻ nhất và nhanh nhất (chi tiết Bài 2.6).

### Claude generate commit message

Sau khi review xong (hoặc fix issues từ review):
```
Dựa trên changes và plan vừa thực hiện, generate commit message
theo format của project (xem commit history gần đây để match style).
```

Claude xem `git log`, học style team, generate message phù hợp.

### GitHub Actions integration

Nếu đã setup GitHub Actions với Claude (Bài 2.6) → trong PR comment:
```
@claude fix the failing test in test/upload/webp.test.ts
@claude add missing error handling for corrupt image files
@claude write a summary of changes for this PR
```

Claude tạo commit mới trực tiếp trong PR — không cần pull/sửa/push lại.

## Khi nào skip phase nào? — Bảng calibration

| Loại task | Explore | Plan | Code | Commit | Thời gian |
|---|---|---|---|---|---|
| **Tiny** — sửa typo, đổi 1 constant, rename variable | Skip | Skip | Nhanh | Minimal | 2-5 phút |
| **Easy** — thêm 1 field vào form, fix bug 1 file | Optional | Optional | Normal | Minimal | 5-15 phút |
| **Medium** — feature mới hoàn chỉnh, refactor 1 module | Required | Required | Normal + test | Full review | 20-60 phút |
| **Hard** — redesign architecture, cross-cutting change | Extended | Multiple rounds | Phased + nhiều test | Multiple commits | 2-8 giờ |
| **Massive** — legacy modernization, platform migration | Days | Days | Phased over weeks | Per-phase commit | Weeks |

**Tiny task** — chỉ cần: `Fix typo: đổi "recieve" thành "receive" trong file src/constants.ts dòng 47.` → Code + Commit. 2 phút.

**Hard task** — Plan nhiều vòng, Code nhiều phases:
```
Round 1: Explore overall architecture → understand scope
Round 2: Plan high-level phases → approve phases
Round 3: Plan Phase 1 chi tiết → execute Phase 1 → commit Phase 1
Round 4: Plan Phase 2 chi tiết → execute Phase 2 → commit Phase 2
...
```
Commit nhiều lần (mỗi phase 1 commit hoặc vài commit nhỏ) thay vì 1 commit khổng lồ → dễ review, dễ rollback.

## Ví dụ thực chiến đầy đủ: WebP conversion

Setup project: Node.js + Express API, đã có `jimp`, test = Jest (`npm test`), storage = AWS S3.

### Phase 1: EXPLORE (5-7 phút)

Plan Mode + prompt: "Explore codebase để tôi hiểu current image upload flow: file nào handle upload? Library nào đang dùng? Test ở đâu? S3 integration ở đâu? Đừng thay đổi gì."

Claude report:
- Pipeline: `middleware/storage.ts` (entry point) → `services/upload.service.ts` (business logic)
- Library: `jimp` đã có trong package.json
- Tests: `tests/upload/` — 12 test cases hiện tại
- S3: `services/s3.service.ts` với method `uploadBuffer()`

### Phase 2: PLAN (8-10 phút)

Prompt đầy đủ context + requirements + constraints + success criteria. Claude trả plan 5 steps:
1. Tạo utility `convertToWebP(buffer, mimeType)` trong `services/image.service.ts` — skip nếu GIF
2. Update `middleware/storage.ts` — gọi converter trước `uploadBuffer()`
3. Update `services/upload.service.ts` — replace extension .webp (trừ GIF), update Content-Type
4. Viết tests `tests/upload/webp-conversion.test.ts` — JPEG→WebP, PNG→WebP, GIF→GIF, large file→error
5. Verify — npm test + TypeScript check

User comment: *"jimp không support WebP output natively. Check lại."* → Claude verify: cần `@jimp/plugin-webp` (~50KB, compatible). Cập nhật Step 1 → approve.

### Phase 3: CODE (15-20 phút)

Thoát Plan Mode → Auto Accept → "Execute the plan. Run npm test sau mỗi step."

Claude:
1. Install `@jimp/plugin-webp`
2. Tạo `image.service.ts` với `convertToWebP()`
3. Update `middleware/storage.ts` — gọi converter
4. Update `services/upload.service.ts` — WebP filename
5. Viết 6 test cases

Giữa chừng test "large file error" fail → Claude tự đọc error log → sửa → chạy lại → pass.

Output: 26 passed, 0 failed; TypeScript: 0 errors; Build: success.

### Phase 4: COMMIT (3-5 phút)

Spawn subagent review tất cả changes. Subagent catch **empty buffer edge case** chưa handle → user prompt Claude main sửa + thêm test → test pass.

Claude generate commit message theo style project:
```
feat(upload): add WebP conversion to image upload pipeline

- Convert JPEG/PNG to WebP before S3 upload using @jimp/plugin-webp
- Skip conversion for animated GIFs (preserve format)
- Add graceful fallback if conversion fails
- Handle empty buffer edge case
- Add 7 test cases for conversion logic

Closes #142
```

Push. **Total: ~28 phút** từ đọc ticket đến push.

## Case studies theo role

### Backend Engineer: Refactor service architecture
**Tình huống**: Senior BE ở fintech, refactor payment service từ monolithic → microservices, ~2 ngày estimate.

- **Explore**: Spawn 4 subagents song song map 4 module (payment, billing, notification, webhook) — 30 phút thay vì 1 ngày đọc thủ công
- **Plan**: Nhiều rounds — plan tổng thể (ngày 1), plan chi tiết phase 1 (sáng ngày 2), phase 2 (chiều). Lưu plan ra `.md` commit vào branch
- **Code**: Phased execution — extract payment → commit; extract billing → commit. Không làm một lần
- **Commit**: 8 commits nhỏ per-phase thay vì 1 commit khổng lồ

**Kết quả**: 1.5 ngày (vs 2 ngày estimate), 0 regression bugs.

### Frontend Engineer: Ship UI feature mới
**Tình huống**: FE implement "dark mode toggle" cho dashboard, task medium, 1 buổi sáng.

- **Explore**: Đọc `theme/`, `tailwind.config.ts` để hiểu color tokens
- **Plan**: 1 round đủ, 10 phút — CSS variables, localStorage persistence, system preference detection
- **Code**: Auto Accept + Claude in Chrome extension verify UI trực tiếp browser; test 3 cases (manual, system pref, localStorage)
- **Commit**: Subagent review nhanh, commit gọn

**Kết quả**: 45 phút, không phải debug UI manually lần nào.

### Open source maintainer: Review/merge contributor PRs
**Tình huống**: Maintainer npm package nhận PR đã được review về logic.

- **Explore**: Skip (đã biết codebase)
- **Plan**: Skip (contributor có plan trong PR description)
- **Code**: Checkout PR branch, run tests, dùng Claude verify logic + edge cases
- **Commit**: Subagent review nhanh → approve/request changes

**Kết quả**: Review cycle nhanh hơn 2-3x.

### Anthropic team: 22.000-line RL code change
Quote từ engineering blog: *"Days of human planning. Concentrated implementation on 'leaf nodes' — code that nothing else depends on. Human review focused on extensible parts. Stress tests for stability, verified inputs/outputs without reading all code."*

Bài học:
- **Explore**: Extensive — cả team hiểu codebase trước khi plan
- **Plan**: Days — không phải giờ, không phải phút
- **Code**: Focused trên **leaf nodes** — code không có gì depend vào, tech debt ở đây acceptable
- **Commit**: Chia nhỏ, nhiều phases, stress test riêng

> "Tech debt in leaf nodes is okay because nothing depends on them." → mindset shift: không cần perfect code mọi nơi, concentrate effort vào interfaces và extensible parts.

### Solo founder (vibe-coding): Ship nhanh, iterate
**Tình huống**: Indie hacker SaaS một mình, ưu tiên speed-to-market.

- **Explore**: Ngắn — đã biết codebase
- **Plan**: Dài hơn cần thiết vì Plan là lúc *think through* feature, không chỉ align với Claude
- **Code**: Skip manual review chi tiết. Trust test suite. Focus behavior, không code
- **Commit**: Light review, commit nhanh, iterate

Mindset Karpathy: *"Fully give into the vibes, embrace exponentials, forget code exists."* — Bạn = PM, Claude = engineer.

> **Lưu ý**: Vibe coding phù hợp prototyping + non-critical features. Với security/payment/auth — vẫn cần Code review cẩn thận.

## Anti-patterns: Những cái bẫy phổ biến

### Anti-pattern 1: Skip Plan để "save time"
- **Triệu chứng**: "Plan Mode tốn thêm 10 phút, tôi muốn đi thẳng vào code."
- **Tại sao sai**: 10 phút Plan → tiết kiệm 30-90 phút debug. Đặc biệt task medium+.
- **Hệ quả**: Claude đoán sai approach, code không match codebase, rollback + restart.
- **Fix**: Luôn Plan cho task medium+. Tiny task (typo, rename) skip Plan là exception, không phải rule.

### Anti-pattern 2: Analysis paralysis — Plan mãi, không Code
- **Triệu chứng**: Revise plan lần thứ 6, vẫn thấy "chưa perfect", không dám approve.
- **Tại sao sai**: Plan không predict được mọi thứ. Một số vấn đề chỉ xuất hiện khi implement.
- **Fix**: Plan đủ tốt (không cần perfect) → approve → Code → điều chỉnh khi gặp vấn đề thực tế. **Nếu plan đã cover happy path + main edge cases, approve.** Refinement xảy ra trong Code phase.

### Anti-pattern 3: Code không có test suite
- **Triệu chứng**: Không có test, hoặc test nhưng không reliable.
- **Tại sao sai**: Không có test → Claude không thể tự verify → phải hỏi sau mỗi bước → back-and-forth. Tệ hơn: bạn không biết feature "đúng" hay không cho đến khi manual test.
- **Fix**: Đầu tư viết test suite ngay đầu. Nếu chưa có → prompt Claude viết test trước khi implement. **Test là "source of truth"** cho cả bạn và Claude.

### Anti-pattern 4: Commit không review
- **Triệu chứng**: Code xong → `git add -A && git commit -m "..." && git push` không review.
- **Tại sao sai**: Claude có bias từ session — "biết" code đúng vì chính nó viết. Subagent reviewer fresh không có bias đó, thường catch issue Claude bỏ qua.
- **Fix**: Dù review nhanh 2 phút hay subagent chi tiết 5 phút — **luôn có một bước review trước commit**.

### Anti-pattern 5: Full EPCC cho tiny task
- **Triệu chứng**: Fix typo một chữ mà vẫn vào Plan Mode, viết plan chi tiết.
- **Tại sao sai**: Overhead workflow lớn hơn task. Mất đà, demotivating.
- **Fix**: Calibrate theo task size. Tiny task → Code + Commit trực tiếp. **Workflow là công cụ, không phải nghi lễ bắt buộc mọi lúc.**

## Mẹo nâng cao

### Mẹo 1: `/rewind` — rollback khi đi sai hướng
`Double Escape → /rewind` đưa về conversation state trước đó, bao gồm cả code state (nếu Claude dùng checkpoint). Không phải lúc nào cũng hoàn hảo — `git worktree` hoặc `git stash` vẫn là safety net tốt hơn — nhưng `/rewind` nhanh hơn nhiều cho quick course-correct.

### Mẹo 2: `/compact` giữa các phases
Sau Explore, context đã chứa nhiều file. Trước Plan phase → `/compact` để Claude tóm tắt và giải phóng context (chi tiết Bài 2.5).

### Mẹo 3: Plan-as-document
Với task lớn, đừng để plan chỉ tồn tại trong conversation:
```
"Trước khi approve, lưu plan này vào docs/plans/webp-conversion-plan.md
trong repo. Tôi muốn version control plan này."
```
Lợi ích:
- Plan commit vào repo — team khác xem được
- Session crash vẫn có plan
- Sau khi done, plan trở thành documentation
- Reference lại trong future sessions

### Mẹo 4: Test-driven prompt
Thay vì "implement feature X":
```
"Viết test cases cho feature X trước. Tôi sẽ review.
Sau khi tôi approve tests, implement để tests pass."
```
Force Claude (và bạn) suy nghĩ rõ ràng về expected behavior trước khi viết implementation. Ít bug hơn, cleaner code hơn.

### Mẹo 5: Dùng CLAUDE.md persist workflow rules
Workflow rules muốn Claude follow mọi lúc → đưa vào CLAUDE.md:
```markdown
## Workflow Rules
- Luôn chạy test suite trước khi declare "done"
- Không thêm npm dependency mới mà không list ra và get approval
- Mọi async function phải có error handling
- Commit message format: conventional commits (feat/fix/chore/docs)
```
Claude follow rules trong mọi session, không cần nhắc lại (Bài 2.7).


> Hầu hết người dùng báo cáo: **EPCC task mất ít thời gian hơn về total (kể cả Plan), và ít stress hơn nhiều**.

## Tóm tắt: 5 takeaways

1. **EPCC không phải overhead** — đây là cái làm bạn *nhanh hơn*, không chậm hơn. 50% thời gian Explore+Plan là investment, không phải waste.
2. **Plan Mode là công cụ alignment** — force bạn và Claude agree trước khi code được viết. Đây là nơi rẻ nhất, nhanh nhất để course-correct.
3. **Test suite là multiplier** — có test = Code phase tự vận hành. Không có test = bạn phải làm QA thủ công sau mỗi bước.
4. **Subagent reviewer = fresh eyes** — Claude có bias từ session, subagent không. 5 phút review có thể catch bug mà 2 tiếng code không thấy.
5. **Calibrate theo task size** — Tiny: Code+Commit. Medium: full EPCC. Hard: EPCC nhiều vòng, commit nhiều phases. **Workflow là công cụ, không phải nghi lễ.**

## Khái niệm / định nghĩa quan trọng

- **EPCC**: Explore → Plan → Code → Commit — vòng lặp phát triển chuẩn với Claude Code.
- **Plan Mode**: Read-only state, vào bằng Shift+Tab (1-2 lần). Claude chỉ đọc/search/research, không edit file.
- **Auto Accept mode**: Claude edit file không cần xác nhận từng cái — Shift+Tab vào.
- **Async Accept mode**: Claude chạy background — Shift+Enter khi đang chạy. Notification khi xong.
- **Subagent reviewer**: Agent phụ với context window độc lập, đọc fresh, không có bias session chính.
- **Leaf node code**: Code không có gì depend vào — tech debt ở đây acceptable (Anthropic mindset).
- **Vibe coding** (Karpathy): "Fully give into the vibes" — quản lý product/behavior, để Claude quản code. Phù hợp prototype, không cho security/payment/auth.
- **`/rewind`**: Lệnh rollback conversation + code state (Double Escape → /rewind).
- **`/compact`**: Tóm tắt context để giải phóng window giữa các phase.
- **Multi-Claude**: Pattern chạy 4-6 instance song song qua `git worktree`, mỗi instance context window riêng.

## Đánh giá của tôi (để trống — Claude không tự điền)

- Điểm hay:
- Nghi ngờ / muốn đào sâu:
- Liên quan đến project nào của tôi:

## Ứng viên Atomic Notes

1. **EPCC workflow — bốn phase và phân bổ thời gian không đối xứng** (concept) — định nghĩa workflow + ý "50% Explore+Plan là investment, không overhead".
2. **Cost thay đổi tăng theo phase ($ → $$ → $$$)** (claim) — kinh tế học của Plan Mode, justify tại sao đầu tư vào Plan đáng giá.
3. **Test suite biến Code phase thành vòng lặp tự sửa** (method) — cách Claude tự verify và iterate khi có test, biến QA thủ công thành automation.
4. **Subagent reviewer bù bias session chính** (concept) — Claude có bias từ session đã viết code, subagent fresh-context catch được bug session chính bỏ qua.
5. **Calibrate workflow theo task size** (method) — bảng quyết định Explore/Plan/Code/Commit theo độ phức tạp (tiny → easy → medium → hard → massive).
6. **Tech debt ở leaf node là acceptable** (claim) — mindset Anthropic từ case study 22.000-line RL change, concentrate review vào interfaces/extensible parts.
7. **Test-driven prompt khi làm việc với AI** (method) — yêu cầu Claude viết test trước, review, rồi implement — force suy nghĩ rõ về expected behavior.

## Trích dẫn quan trọng

> "If you take one thing away from this course, let it be this workflow." — Boris Cherny, creator of Claude Code (trang 2)

> "EPCC không phải overhead. Nó là cái làm cho bạn **nhanh hơn**, không phải chậm hơn." (trang 2)

> "Thay đổi trong Plan phase: $ — Thay đổi trong Code phase: $$ — Thay đổi sau khi commit: $$$" (trang 5)

> "Thời gian tiết kiệm khi skip Explore: 5-10 phút. Thời gian mất thêm khi phải fix: 30-90 phút." (trang 5)

> "People run 4-6 Claude instances simultaneously — separate git worktrees, different tasks, no interference." (trang 9)

> "Tech debt in leaf nodes is okay because nothing depends on them." — Anthropic team, case study 22.000-line RL (trang 19)

> "Fully give into the vibes, embrace exponentials, forget code exists." — Andrej Karpathy về vibe-coding (trang 19)

## Tài liệu tham khảo (theo tác giả)

- Claude Code best practices — Anthropic engineering blog
- Introducing Claude Code — Launch post với demo workflow
- Vibe coding in production — Philosophy của workflow AI-assisted development
- Video transcript: "The Explore → Plan → Code → Commit Workflow" — Claude Code 101 course, Lesson 2.4
- Claude in Chrome extension — Tool cho Code phase (web UI testing)
- Lệnh quan trọng: Shift+Tab (Plan Mode), Shift+Enter (Async Accept mode), Escape Escape (/rewind)

## Liên kết

- Project: [[10_Projects/claude-code-101/README]]
- Chapter tiếp theo: Bài 2.5 — Quản lý Context (`/context`, `/compact`, `/clear`)
- Chapter liên quan: Bài 2.6 (Code Review & Git Workflow), Bài 2.7 (CLAUDE.md)
- Atomic notes đã tạo: *(chưa có — chạy `/paper-atomize` để tách)*
