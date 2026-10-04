# Công thức TITLE + THUMBNAIL thắng — ngách 年金/老後 (bóc từ đối thủ, xem tận mắt 2026-07-22)

> Nguồn: nhìn thật 9 thumbnail top-video của 4 kênh thắng (年金・給付金完全攻略 130K, シニアの年金・給付金速報 113K, News65 173K 漫画, 節約看護師りょう 748K). Tải về `scratchpad/thumbs/`.

---

## ⚡ CHỐT 2026-08-06 — ĐỔI QUY TRÌNH: Claude CHỈ ĐƯA PROMPT, và BỎ khuôn tool

> user: *"thôi không cần theo thumbnail cũ… không cần theo khuân mẫu trong project"* → *"lưu lại rule đi sau đưa prompt cho tao thôi"*

**Từ video 08 trở đi, kênh nenkin:**
1. **Claude viết PROMPT, user gen ảnh.** KHÔNG dựng thumbnail bằng `tools/make_thumb_genten.py` / `make_thumb_45.py` nữa — 2 tool này hạ xuống **fallback**, chỉ dùng khi bản gen lỗi kanji.
2. **Prompt phải ghi vào mục Đóng gói CTR của file script**, không chỉ in ra chat.
3. **Khuôn mới「TELOP」 thay 原典/A-45** (mẫu đầy đủ: `03_SCRIPTS/08_nenkin-shikyubi-8gatsu14ka-tedori.md` §THUMBNAIL): nền gradient vàng kem sáng + sunburst · **số âm khổng lồ ~40% chiều cao**, vàng viền đen, nghiêng 4° · mũi tên đỏ dày đổ xuống · mặt 60代 cutout viền trắng ở 40% phải · tiền 1万円 crop mờ góc dưới trái · **góc dưới PHẢI để trống** (YouTube đè timestamp).
   Khuôn này đi theo Mục 1 (DNA chung của kênh thắng) ở trên — tức **quay về đúng công thức ngách**, khác với 原典 (nền giấy, tĩnh, nhã) vốn là đường riêng của kênh.

### ⚠️ Đã đánh đổi có chủ ý — đọc trước khi đọc số
- Bỏ 原典 = **mất lớp nhận diện** đang dùng ở 3 video live (01 `bWl2jE9l8z4` · 02 `uPlyzkGYfCs` · 04 `MfEKhbXdTXY`, đổi 2026-08-03) **và mất mốc baseline để đọc A/B**.
- Thắng CTR → §6 (khuôn A-45) và mục 原典 coi như thay bằng TELOP. Thua → quay về 原典 và **ghi rõ đã thử gì** vào `08_ANALYTICS_LOG.md`.
- ⚠️ Ở mức **114 impressions/28 ngày** thì CTR chưa đọc được (`08_ANALYTICS_LOG.md` 2026-08-03: cấm đọc CTR khi impressions <500). Đừng kết luận khuôn nào thắng bằng mẫu này.

### 🔴 Rủi ro kanji (không bỏ qua)
AI hay méo `万`/`千`/`減` hoặc bịa chữ lạ. Đường an toàn: gen cùng prompt nhưng **xoá các dòng về text + thêm `NO text anywhere`**, rồi đốt chữ bằng code. Nếu để AI vẽ chữ → **soi từng ký tự ở full-size** trước khi trình user.

### Giữ nguyên, không đổi
Gate 3 cửa (**168px** · **120px** · **góc dưới phải trống**) · đủ **3 bản A/B** (`ab-3title-3thumb.md`) · mặt = người **hư cấu/vô danh**, cấm mặt người thật cụ thể (`youtube-compliance.md` §2) · không 外来語, không từ nhóm 殺/血/死 · mọi tình tiết trên thumbnail phải CÓ THẬT trong video.

---
## 1. DNA CHUNG (mọi kênh thắng đều có)

1. **CON SỐ TIỀN là nhân vật chính** — chiếm ~1/3 khung, TO NHẤT: `234万円失う` · `年金24%減` · `100万円支給` · `5万円還付`. Hoặc **giấu số bằng `?万` / `○万円`** = curiosity (完全攻略_2「○万円吹き飛ぶ」, 看護師_1「?万超」).
2. **Bộ màu tín hiệu:** 🟡 VÀNG = chủ đề/thời điểm (banner trên) · 🔴 ĐỎ = mất mát/hậu quả (số lỗ, 支給停止, ガクン減) · 🔵 XANH/🟨 VÀNG = được (支給/最強/還付). Chữ luôn viền đen/trắng dày, đọc được ở 120px.
3. **Banner TRÊN = móc thời điểm/khẩn:** `2026年4月激変` · `7月中に必ず確認して！` · `10月15日の年金` · `60歳の誕生日！` (nền đen hoặc đỏ, chữ vàng).
4. **Mảnh cảm xúc bên phải / chia đôi:** mặt người thật nữ 50–60代 (完全攻略/速報 — uy tín) HOẶC **nhân vật いらすとや ông/bà lo lắng + đạo cụ** (通帳/財布 — 看護師/速報, thân thiện senior) HOẶC mặt 漫画 biểu cảm mạnh (News65). Mặt phải LỘ CẢM XÚC (lo/sốc/mừng).
5. **Banner dọc trái nhỏ:** `知らないと大損` / `絶対確認して` (lặp lại nhận diện).
6. **Giấu đáp án** (`?歳` / `?万` / `コレ`) = không spoil, buộc bấm xem.

## 2. HAI KHUÔN BỐ CỤC (chọn theo nội dung)

**Khuôn A — 3 TẦNG STACK** (完全攻略/速報, hợp video "1 chế độ, 1 con số"):
```
[banner trên: thời điểm/khẩn — vàng/đen]
[dòng điều kiện: 申請をしないと / ここ確認しないと — trắng viền đỏ]
[dòng hậu quả: 234万円失う！ — ĐỎ khổng lồ]      + mặt/nhân vật bên phải
```

**Khuôn B — CHIA ĐÔI 対比** (News65/看護師, hợp video "A vs B / 得 vs 損"):
```
[banner trên: chủ đề — đen/vàng]
TRÁI xấu (tối/xanh, mặt buồn, 65歳=超大損)  |  PHẢI tốt (sáng/vàng gold, mặt mừng, ?歳=最強)
[banner dọc trái: 知らないと大損]  [nhãn vàng chữ đỏ: con số/mốc mỗi bên]
```

## 3. TITLE — công thức (khớp thumbnail, đo từ top-video)
`【bracket khẩn/đối tượng】+ thời điểm(2026年4月/7月中) + 大損/申請しないと + SỐ TIỀN LỖ định lượng(生涯500万円/234万円/年6万円) + 役所が教えない/末路/激変` — giữ đáp án ẩn.
Ví dụ thắng: `【50歳以上必須】申請しないと大損！ねんきん定期便に載らない年金4選！` (3.79M) · `知らないと生涯500万円以上損をします！` (2.29M) · `2年はやめるな！60歳退職 vs 62歳退職` (777K).

## 4. ÁP CHO NENKIN — giữ trần YMYL (khác đối thủ ở 3 điểm)

Nenkin THEO khuôn A/B + số hero + màu tín hiệu + いらすとや ông/bà cảm xúc, NHƯNG:
1. **KHÔNG dùng mặt người thật kiểu chính khách** (完全攻略/速報 dùng ảnh giống 高市 — nenkin né: dễ hiểu lầm "người thật/chính trị", vi phạm rule không đảng phái + misleading). → Dùng **いらすとや ông/bà** (như 看護師/速報_1) — an toàn, thân thiện senior, đúng chất 研究室.
2. **KHÔNG 絶対/必ず** trên title (trần YMYL) → thay `知らないと損する場合が多い` / `確認したい` / `かも`. (Chữ `大損`/`損` trên THUMBNAIL thì OK — không thuộc bảng cấm.)
3. **Số phải CÓ THẬT trong bài** (nguồn 日本年金機構/厚労省) — dùng số thật hoặc giấu `?万円` rồi trả lời trong video; cấm bịa để giật.

**Mẫu áp cho video 01 (在職老齢年金 4月改正) — khuôn A:**
- Banner trên (vàng/đen): `2026年4月 制度激変`
- Điều kiện (trắng viền đỏ): `働きながら年金`
- Hậu quả (đỏ khổng lồ, giấu số): `いくら止まる?` hoặc số thật `65万円の壁`
- Bên phải: いらすとや ông đi làm + phong bì lương, mặt lo.
- Banner dọc trái: `60代は要確認`
- **Title v2:** `【2026年4月改正】働きながら年金、いくら止まる?65万円の新ルールを研究しました｜在職老齢年金`

## 4b. PROMPT ẢNH AI cho video 01 (khuôn A) — user gen, Claude ghép chữ

> Quy trình: user gen ảnh này → lưu `06_VIDEO/01_zaishoku/scene_v2_ai.jpg` → chạy `python tools/make_thumb_khuonA.py 06_VIDEO/01_zaishoku/thumbnail_v2_khuonA.png --bg 06_VIDEO/01_zaishoku/scene_v2_ai.jpg` → Claude ghép chữ + duyệt 3 cửa. Chủ thể BÊN PHẢI, trái+trên chừa tối cho chữ.

**Prompt chính (English — Gemini / Flux / MJ):**
```
Photorealistic YouTube thumbnail background, 16:9, no text anywhere.
A worried Japanese man in his early 60s, short grey-flecked hair, wearing a business-casual shirt and cardigan (a re-employed senior office worker). He sits at a home desk, holding a Japanese pension/payment notice and a pay envelope, looking at them with an anxious, furrowed-brow expression, one hand near his chin. He is placed on the RIGHT THIRD of the frame, upper body, turned slightly toward the left.
The LEFT two-thirds and the TOP of the image are kept clean, softly out of focus and darker (a dim muted home interior) so large text can be overlaid there.
Warm but slightly tense lighting, shallow depth of field, sharp detail on his face and hands, realistic natural Japanese features, documentary money-anxiety mood, 4k.
No text, no letters, no numbers, no logo, no watermark. --ar 16:9
(negative: text, letters, watermark, deformed hands, extra fingers, distorted face, cartoon, anime, cluttered left side, busy bright background)
```

**Prompt dự phòng (nếu mặt người ra xấu — chuyển sang vật thể):**
```
Photorealistic 16:9 thumbnail background, no text. A Japanese pension payment envelope ("年金" style official envelope) and a pay slip lying on a wooden table, with a few 10,000-yen banknotes partially visible, and a worried senior man's hand (early 60s) resting near them. Objects grouped on the RIGHT side; the LEFT two-thirds and TOP darker, softly blurred and simple for text overlay. Soft dim home lighting, tense money-anxiety mood, shallow depth of field, 4k. No text, no letters, no logo, no watermark. --ar 16:9
```
> Compliance: nhân vật HƯ CẤU AI (không phải người thật cụ thể) → thumbnail OK, KHÔNG cần tick synthetic. Không dàn dựng sự kiện/địa điểm thật. Số 65万円 (chữ ghép PIL) là ngưỡng thật cải chính 2026.

## ✅ ĐÃ THI HÀNH (2026-07-22)
- Tool riêng khuôn A: **`tools/make_thumb_khuonA.py`** — mode gradient+いらすとや (test) HOẶC `--bg <ảnh AI>` full-bleed + scrim trái. Đã dựng thumbnail v2 video 01 (在職老齢年金) từ ảnh AI (ông 60代 lo cầm 年金支払書, user gen theo prompt mục 4b) → **swap live qua `thumbnails.set` 2026-07-22** (video bWl2jE9l8z4). Qua đủ 3 cửa duyệt. File: `06_VIDEO/01_zaishoku/thumbnail_v2_khuonA.png`.
- Title video 01 giữ nguyên bản live (chưa đổi title v2 — chờ user chốt riêng nếu muốn).

## 4c. Video 02 (繰り下げ 65 vs 70) — khuôn A, ĐÃ DỰNG 2026-07-22 (chờ video render+up mới swap)
- Ảnh AI (user gen theo prompt hướng 2): ông ~65 trầm ngâm đọc 年金ガイドブック + lịch tường → `06_VIDEO/02_kurisage/scene_v2_ai.jpg`.
- Prompt đã dùng: `...pensive Japanese man mid-60s, hand on chin, gazing at a pension guidebook/wall calendar, weighing a decision, RIGHT-third, left/top dark...` (hướng 2 mục trên).
- Lệnh ghép: `python tools/make_thumb_khuonA.py 06_VIDEO/02_kurisage/thumbnail_v2_khuonA.png --bg 06_VIDEO/02_kurisage/scene_v2_ai.jpg --cx 0.50 --banner1 "65歳？70歳？" --banner2 "どっちが得？" --l1 "70歳まで待つと" --l2 "損する人も！？" --tag "得の分かれ目は?" --vban "決める前に"`
- Loss-forward (khớp hook script 02); số break-even ~84歳 giấu (curiosity). CHƯA swap — video 02 chưa upload.
- Tool giờ nhận text qua argparse (--banner1/2 --l1 --l2 --tag --vban --cx) → tái dùng cho mọi video nenkin.

## 5. HỆ THỐNG MỚI 2026-07-25 — TOOL RIÊNG + BADGE + SỔ XOAY 8 KHUÔN (port bài học textwall của health)

### 5a. Tool
- **`tools/make_thumb.py` (BẢN RIÊNG nenkin, port từ health 2026-07-25):** đủ layout v3 stack / panel / **`--textwall`** (`--line1..4 --color1..4 --inset1 --inset2`) + **badge nhận diện mặc định BẬT**. Xuất kèm preview480/preview120 (duyệt ở 120px trước khi chốt).
- `tools/make_thumb_khuonA.py` GIỮ — khuôn A vẫn là 1 khuôn trong rổ xoay.
- Lệnh mẫu khuôn C (đã test OK với ảnh video 05):
  `python tools/make_thumb.py <ảnh_AI.jpg> <out.png> --textwall --line1 "<hook vàng>" --line2 "<hành vi trắng>" --line3 "<hậu quả+số ĐỎ, to nhất>" --line4 "<payoff trắng>" --color1 yellow --color3 red --inset1 <ảnh>`

### 5b. Badge nhận diện CỐ ĐỊNH (phần BẤT BIẾN — mọi thumbnail)
Mẩu tag 「**年金研究室**」 nền **navy đậm / chữ+viền vàng 山吹** (đảo màu với badge health — ăn theo bộ màu signature kênh), nghiêng nhẹ có bóng, luôn ở góc phía ẢNH (đối diện cột chữ). Mặc định bật trong tool; `--badge-pos` chỉnh góc. Đây là con dấu nhận kênh trong 0.5s trên browse — mọi thứ khác XOAY, badge KHÔNG đổi.

### 5c. SỔ XOAY 8 KHUÔN (luật inauthentic — không lặp khuôn của video liền trước; ghi khuôn đã dùng vào header script)
| Khuôn | Mô tả | Hợp với |
|---|---|---|
| **A** | 3 tầng stack trên ảnh AI (banner móc thời điểm → 2 dòng → tag) — `make_thumb_khuonA.py` | video 改正/tin mới |
| **B** | Chia đôi 対比 A-vs-B (2 nửa 2 màu, số 2 bên) | 対決型 (任意継続vs国保, 60 vs 65) |
| **C** ⭐ | **Textwall-số**: nền đen + ≤4 dòng trái (vàng→trắng→**ĐỎ số tiền/hậu quả TO NHẤT**→trắng) + inset phải = ảnh AI 60代/cast いらすとや | mặc định ưu tiên — khuôn thắng ngách senior |
| **D** ⭐ | **Textwall-giấu số**: như C nhưng dòng đỏ = `?万円`/`?歳` (curiosity gap), inset = đạo cụ 通帳/phong bì | evergreen いくらもらえる/何歳 |
| **E** | **研究ノート**: nền trang sổ lab + con dấu đỏ + 1 số hero (tận dụng visual signature sẵn) | video tổng kết/保存版 |
| **F** | Cast đôi cảm xúc đối lập (lo vs yên tâm) + nhãn số mỗi bên | video 末路/lựa chọn |
| **G** ⭐ | **原典/giấy tờ khoanh đỏ**: close-up trang tài liệu gốc (年金機構/厚労省) hoặc 通知書/定期便 dựng lại + **vòng khoanh ĐỎ quanh con số** + số to bên cạnh. Khuôn này khuếch đại móc nhận diện **原典を見せる** (chuẩn visual CLAUDE.md + skill GĐ0d) — thứ 元ハロワ職員-type kênh không copy được | series 書類を読む · video ngưỡng/điều kiện · mọi video có 原典ショット mạnh |
| **H** | Thang ngưỡng/timeline tối giản (bar vs vạch đỏ) + số | video 計算/ngưỡng |
| **I** ⭐⭐ MỚI 2026-08-10 | **「紙が主体」— tờ giấy làm CHỦ THỂ, chữ BAKE trong ảnh AI**: phong bì/はがき/通知書 chiếm khung, **KHÔNG mặt người, KHÔNG mascot**, 4 dòng 袋文字 (banner vàng → dòng phụ trắng → **HERO vàng to nhất** → dải đỏ đáy). Prompt kèm cả text, user gen — không đốt chữ bằng tool | **mọi video lớp A「◯月に届く紙」** — đây là lớp đề tài mạnh nhất ngách |

> **Khuôn I ra đời từ phép đo 2026-08-10** (`CHANNEL_BENCHMARK_fukurou-tanuki_2026-08-10.md` §2.3):
> bản **1.000.000 view** của `フクロウ`（8月から届くこの封筒）**không có mặt người** — chủ thể là **cái
> phong bì**. Cả hai kênh đối thủ đều đặt **ảnh tờ giấy + mũi tên đỏ** làm trung tâm.
> Nó **củng cố** ngoại lệ miễn-gate-mặt của nenkin (`audience-45plus.md` §1.2), không phá.
> ⚠️ **Khác khuôn G ở chỗ nào:** G là **原典 THẬT** (ảnh chụp trang cơ quan, khoanh đỏ) — dùng để
> dựng uy tín; I là **giấy CHUNG CHUNG do AI gen** (phong bì trơn, không logo) — dùng để dựng nhận
> diện vật thể. ⛔ **Cấm gen giấy tờ có logo/tên 日本年金機構** — đó là dựng lại giấy tờ chính thức
> (`youtube-compliance.md`). Thứ có thật chỉ được xuất hiện ở lớp 原典 trong video.
> Bản mẫu đầu tiên: `06_VIDEO/10_shien-kyufukin-hagaki-9gatsu/thumb_prompts_BLOCKS.md`.

- **C/D/G/I là mặc định ưu tiên** (I khi đề tài là một tờ giấy cụ thể sắp về nhà người xem)
- **C/D/G là mặc định ưu tiên** (C/D cho hook số, **G khi có 原典ショット mạnh** — vừa CTR vừa dựng uy tín); A/B/E/F/H xoay vào cho đủ nhịp. Đọc rõ ở **120px** là cửa duyệt số 1.
- Mỗi video dựng **2 bản khác khuôn** (chính + variant B) lưu `06_VIDEO/<slug>/` — variant B chờ swap khi CTR <3% với ≥500–1.000 impressions/7 ngày (xem `08_ANALYTICS_LOG.md`; quy trình swap qua `thumbnails.set` như video 01 ngày 07-22). CẤM swap khi impr <500.
- Trần YMYL giữ nguyên (mục 4): không 絶対/必ず, không 殺/血/死/破産, không mặt người thật kiểu chính khách, số phải thật hoặc giấu `?万`.
- DNA không đổi: **số tiền là nhân vật chính ~1/3 khung** + bộ màu vàng/đỏ/xanh + banner móc thời điểm. CHỮ + SỐ + cảm xúc kéo CTR; diagram chỉ là phụ.

---

## 📌 KHUÔN ĐANG KHOÁ CỦA KÊNH — trạng thái thật, đọc trước §6 (cập nhật 2026-08-10)

| Thời điểm | Khuôn khoá | Ai dựng chữ |
|---|---|---|
| 2026-08-01 | **A-45** (`make_thumb_45.py`) — §6 dưới | tool |
| 2026-08-06 | **TELOP** (chip 対象 + hero + dải đỏ) — chốt ở `ab-3title-3thumb.md`/queue §4 | **user gen ảnh, Claude chỉ đưa prompt** |
| ~~2026-08-10 sáng~~ | ~~**I「紙が主体」** — chủ thể là tờ giấy, KHÔNG mặt người~~ | ⛔ **BỎ, chưa từng gen bản nào** |
| **2026-08-10 tối → nay** | ⭐ **BAKE 9 KHỐI** — chép đúng ảnh **video 09 đã lên sóng** | **user gen, prompt BAKE SẴN CHỮ** |

### ⭐ KHUÔN CHỐT: **BAKE 9 KHỐI** (user chốt 2026-08-10 bằng cách dán chính ảnh 09)

Khuôn = 9 khối, đo bằng máy trên `07_UPLOADED/09_koukin-uketori-koza-ikou-kakuninsho/_upload/thumbnail.png`:
**① banner navy trên cao ~1/5 khung, chữ trắng · ② nền giấy kẻ ô kem lưới xanh, mép ngả vàng ·
③ HERO vàng 袋文字 viền đen + halo trắng, RỘNG ~2/3 khung · ④ vòng tròn đỏ vẽ tay 2 vòng quanh hero ·
⑤ ruy-băng đỏ nghiêng ~-6° dưới hero, chữ trắng · ⑥ mũi tên đỏ cong viền đen trỏ vào hero ·
⑦ ảnh cắt-nền người mặt SỐC, viền trắng sticker, 1/3 phải, cao TRỌN khung · ⑧ đạo cụ góc dưới-trái,
ô 郵便番号 đỏ RỖNG · ⑨ badge navy `年金研究室` dưới-trái.**

- **Prompt mẫu đủ 3 bản + bảng số đo:** `06_VIDEO/10_shien-kyufukin-hagaki-9gatsu/thumb_prompts_BLOCKS.md`.
  Cách viết prompt (5 bước + khung khối): `.claude/rules/ab-3title-3thumb.md` **§3.1**.
- 🔴 **Khuôn 「紙が主体」 (không mặt người) BỊ BỎ** dù nó dựa trên bản 1M view của `フクロウ`. Lý do:
  nó **chưa từng được gen thử bản nào**, còn khuôn 09 thì **đã có ảnh thật đang chạy trên kênh** và
  user chọn đúng ảnh đó. **Một khuôn đã ra hàng thắng một khuôn chỉ có trên giấy.**
- ⭐ **HỒI SINH LÀM SLOT T3 A/B (2026-08-31, kế hoạch user duyệt):** từ v19, bản **T3** của bộ 3×3
  = khuôn 「紙が主体」 — **0 mặt người, tờ giấy/phong bì chiếm khung, mũi tên đỏ trỏ vào giấy**,
  4 dòng 袋文字 (banner vàng → dòng phụ trắng → HERO vàng → dải đỏ đáy). KHÔNG đổi khuôn chốt
  (T1/T2 vẫn BAKE 9 KHỐI) — T3 là biến layout đúng luật `ab-3title-3thumb.md` §3, để Studio
  Test & compare tự trả CTR. Căn cứ đo 08-31: bản 1,43M của フクロウ (0 mặt, phong bì+mũi tên),
  保健室 0 mặt/25 thumbnail, カメ先生 (154 sub/ngày) cũng chạy khuôn giấy-chữ không mặt.
  Chữ 3 bản GIỐNG NHAU (biến thử là HÌNH); T3 thắng ổn định → mở bàn đảo khuôn chốt.
- ⚠️ **Hệ quả lên `audience-45plus.md` §1.2:** khuôn này **CÓ mặt người**, trong khi §1.2 vừa **miễn
  gate 4 (mặt) cho nenkin** vì kênh chuẩn `お金の保健室` đo được **0 mặt / 25 thumbnail**. Miễn ≠ cấm,
  nên không vi phạm — nhưng ghi thẳng: đây là **lệch khỏi phép đo đó**, và là **biến phải xét lại đầu
  tiên** nếu CTR không lên. Đừng "phát hiện lại" rồi tưởng có lỗi.
- ⚠️ Bộ chữ vẫn phải qua **gate 7** + **bảng đo keyword**; vật nhận diện đo thấp thì để ở **HÌNH**,
  không lên chữ (ca `緑の封筒` 33/Very low của video 10).

⚠️ **§6 bên dưới là LỊCH SỬ, không còn là khuôn chốt** — nó vẫn đúng về **toán học của gate 2**
(dòng chính cao 360px ⇒ ~360px/ký ⇒ quá 4 ký không vừa 1920 ⇒ **dòng chính phải là CON SỐ**), và
đó là lý do giữ nguyên. `make_thumb_45.py` nay là **đường lui** khi ảnh AI nát kanji.
📌 **Bổ chính cho §6 từ phép đo 2026-08-10:** toán học đó chỉ đúng khi bắt hero **cao ≥34%**. Bản 09
đang chạy có hero **cao ~18% nhưng rộng ~2/3 khung** và **đọc được ở 120px** — tức legibility mua bằng
**BỀ NGANG**, và trần "≤4 ký" của §6 nới ra được: **5 ký vẫn đọc tốt** (`45日で同意`, `6万7千円`).

## 6. ⭐ KHUÔN **A-45** — ~~KHUÔN CHỐT CỦA KÊNH~~ (2026-08-01, thi hành `.claude/rules/audience-45plus.md` §1 · việc §6.4)

> Lý do ra đời: video 06 dựng lệch hẳn bộ nhận diện (user bắt được), soi lại thì **cả 5 thumbnail live đều KHÔNG đạt gate 45+**: dòng chính chỉ cao 11–13% khung (gate đòi ≥1/3) và có 5 khối chữ (gate đòi ≤3). Sửa lệch 1 video = lại lệch kênh → **đổi khuôn ở tầng KÊNH, áp lại cả loạt**.
> Đây là khuôn A cũ **giữ nguyên bộ nhận diện**, chỉ đổi phần thân để lọt gate.

**Tool: `tools/make_thumb_45.py`** (khuôn A cũ `make_thumb_khuonA.py` GIỮ để tham chiếu, KHÔNG dùng cho video mới).

| Phần | Quy cách | Gate 45+ |
|---|---|---|
| Banner đen trên, cao **186** | vàng (móc/đối tượng) + `　` + ĐỎ viền trắng (hậu quả/thời điểm) | = dòng chữ **1** |
| Dải **ĐỎ dọc trái** rộng 96 | **BỎ CHỮ** — thành vạch màu nhận diện | không tính dòng |
| Dòng điều kiện TRẮNG viền đen | ≤8 ký, cỡ tự co trong 47% ngang | = dòng **2** |
| **Dòng chính ĐỎ viền trắng** | **2–4 ký (số tiền/số tuổi)**, tool tự scale tới **≥34% chiều cao khung** | = dòng **3** ✅ |
| Tag vàng bo góc | **BỎ** (cắt để về ≤3 dòng) | — |
| Ảnh | chủ thể bên phải, scrim tối trái 60% | mặt ở §gate 4 |

- **Dòng chính phải là CON SỐ** (42万 · 700万 · 6万円 · 何歳?). Toán học của gate: cao 360px ⇒ mỗi ký ~360px ngang ⇒ **quá 4 ký là không thể vừa khung** — nên số, không phải câu.
- Lệnh mẫu: `python tools\make_thumb_45.py <V>\thumbnail_45.png --bg <V>\scene_45.jpg --banner1 "配偶者が年下なら" --banner2 "届出を忘れずに" --l1 "届出をしないと" --hero "42万"` → tool tự in `% khung` + ĐẠT/CHƯA ĐẠT, kèm `_preview168.png`.

### 6a. Đã áp lại cho 4 video LIVE (2026-08-01)

| Video | banner (vàng / đỏ) | dòng 2 | **dòng chính** | cao | gate 4 (mặt) |
|---|---|---|---|---|---|
| 02 繰り下げ | 65歳？70歳？ / どっちが得？ | 得なのは | **何歳?** | 34,0% | 🟡 mặt nhỏ, xa |
| 04 支援給付金 | 知らないと損 / 申請しないと消える | もらえるのは年 | **6万円** | 34,1% | ❌ **không có mặt** |
| 05 60歳退職 | 定年前に確認 / あと2年が分かれ道 | 60歳で辞めると | **700万** | 34,2% | 🟡 mặt nhỏ, xa |
| 06 加給年金 | 配偶者が年下なら / 届出を忘れずに | 届出をしないと | **42万** | 34,2% | ✅ 2 mặt to |

- ⚠️ **Ảnh nền AI gốc của cả 4 đã bị `upload_pack --done` prune** → nền được **tái tạo từ chính bản live** (`prep_bg.py` / `prep_all.py`: xoá vùng chữ bake bằng blur lấy từ nửa phải sạch chữ, mask đục→tan; 06 thêm bước dịch ảnh lên 70px để banner nuốt badge). Đây là bản vá, không phải ảnh mới.
- 🔴 **CÒN NỢ 2 gate, KHÔNG vá được bằng chữ — phải gen ảnh mới:** **gate 4** (04 không có khuôn mặt nào; 02/05 mặt quá nhỏ ở 168px) và **gate 6** (02/04/05 nền tối moody, rule đòi nền sáng tương phản cao). Prompt gen ở §6b.
- **Video 01** (1280×720, chủ thể đứng GIỮA khung) không salvage được — chữ mới sẽ đè lên người. Cần ảnh mới hẳn, hoặc để nguyên vì là video cũ nhất.

### 6b. Prompt ảnh nền cho lần gen tới (đạt nốt gate 4 + 6)

Khung chung — **cận cảnh hơn, nền SÁNG, mặt to ≥20% chiều cao khung, chủ thể lệch PHẢI**:
```
Photorealistic YouTube thumbnail background, 16:9, no text anywhere.
[NHÂN VẬT] — upper body / chest-up, face large in frame, clear readable expression of
[worry / realization / relief]. Placed on the RIGHT THIRD, turned slightly toward the left.
Background: BRIGHT, clean, softly blurred bright interior (white wall, daylight window).
The LEFT two-thirds kept simple and uncluttered for large text overlay.
Natural realistic Japanese features, soft even lighting on the face, 4k.
No text, no letters, no numbers, no logo, no watermark. --ar 16:9
negative: text, letters, watermark, deformed hands, extra fingers, distorted face, cartoon,
anime, western faces, dark moody background, subject too far from camera, cluttered left side
```
- **02** → `a Japanese man about 65, hand on chin, a pension guidebook and a wall calendar beside him, pensive weighing-a-decision expression`
- **04** → `an elderly Japanese woman about 70 holding an unopened official postcard and a bank passbook, worried "did I miss something" expression` (bắt buộc CÓ MẶT — bản hiện tại chỉ có bàn tay)
- **05** → `a Japanese man about 60 in a suit holding a resignation envelope, uneasy hesitant expression`

Gen xong → `06_VIDEO/<slug>/scene_45.jpg` → chạy lại đúng lệnh §6 (chữ giữ nguyên) → duyệt `_preview168.png` → `thumbnails.set`.
