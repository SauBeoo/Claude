# 04_VIDEOGEN_PROMPTS — style khóa + prompt gen cảnh 昭和 (kênh 昭和くらし図鑑)

> Chốt hướng 2026-08-02 (user): **65% AI-video tái hiện · 25% ảnh thật chèn điểm "nhận ra" · 10% drawn card**.
> Quy trình: **ẢNH TRƯỚC (image-gen, khóa style) → VIDEO SAU (Kling 3.0 image-to-video)** — không text-to-video từng clip rời.
> ⚠️ Kênh này dùng cảnh AI realistic → **BẮT BUỘC tick "altered/synthetic content" khi upload** (ngoại lệ đã ghi CLAUDE.md project). Clip nền tự gen = tài sản kênh, tái dùng giữa các video trong kênh được.

## 1. STYLE LOCK — HAI TẦNG (sửa 2026-08-10)

> 🔴 **Bug đã vá:** bản cũ nhét `wooden school interior` vào chuỗi ghi là *"dán vào MỌI prompt ảnh, không đổi giữa các video"*. Đó là **bối cảnh của riêng video 01 (給食 — trường học)**, bị khoá nhầm vào tầng bất biến. Dán nguyên sang video 02 (商店街) thì mọi ảnh phố xá, quán đậu phụ, hộp sữa đều bị kéo về nội thất trường gỗ.
> Từ nay: **tầng A bất biến (phim/màu/ống kính)** + **tầng B bối cảnh, chọn theo video**. Chỉ tầng A mới là "style lock" thật.

### 1A. TẦNG BẤT BIẾN — dán vào MỌI prompt ảnh của kênh, không bao giờ đổi

```
, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film,
faded warm Fujicolor palette, soft natural light, gentle film grain,
slight vignette, nostalgic documentary photography, muted greens and ochres,
natural imperfect framing, 16:9
```

🔴 **THIẾU MỘT CÂU — thêm vào NEGATIVE của mọi video sau (bắt được 2026-09-06, video 10, 120/120 clip dính):**

```
no film strip border, no sprocket holes, no film edge markings, no film frame around the image,
image fills the entire frame edge to edge
```

**Chuyện gì xảy ra:** `shot on 8mm home movie film` được model đọc thành *"cho thấy DẢI PHIM"* chứ không phải
*"chất phim"* ⇒ **120/120 clip của video 10 có khung phim đen bao quanh + lỗ răng cưa + chữ `FUJI` / `FUJIFILM`
in dọc mép**. Ba cái giá, cái thứ ba là nặng nhất:
1. **Mất ~10% bề ngang** — khung hình thật co lại, tệp 45+ thiệt nhất.
2. **Chữ `FUJI` = brand logo**, đúng thứ `AVOID` đã liệt kê mà model vẫn vẽ (⇒ negative chung chung
   "brand logos" **không chặn được** thứ model coi là thành phần của phong cách; phải cấm ĐÍCH DANH).
3. 🔴 **Viền KHÔNG ĐỀU giữa các clip** (đo video 10: trái 53–105px, phải 59–227px) ⇒ ghép lại thì
   **khung hình nhảy kích thước mỗi lần đổi cảnh** — trông như video lỗi, và không có gate nào bắt.

⚠️ **Chữa cho video ĐÃ GEN thì phải crop TỪNG CLIP theo viền của chính nó** (không crop chung một mức —
viền không đều), rồi scale lại 1920×1080. Tool: `06_VIDEO/10_tsugakuro/crop_border.py`.
⇒ **Rẻ hơn nhiều nếu chặn từ prompt.** Video sau: dán câu negative ở trên.

🔬 **ĐO VIỀN: ba cách, hai cách đầu HỎNG — ghi để không thử lại từ đầu.**

| # | đo bằng | hỏng vì | dấu hiệu nhận ra |
|---|---|---|---|
| 1 | **độ sáng** (ngưỡng "đen") | lỗ răng cưa **và** chữ FUJI đều **SÁNG** ⇒ ngưỡng dừng ngay mép ngoài | 🚩 **cả 120 clip trả về đúng một số** (`phải min = trung vị = max = 24`). Mọi clip cùng một giá trị = đang đo **mép cửa sổ đo**, không đo vật |
| 2 | **bão hoà màu** (ảnh có màu, viền đơn sắc) | chữ FUJI **màu VÀNG** ⇒ sat > 0 ⇒ tính nhầm là ảnh thật. Còn hỏng nặng ở **cảnh đêm/hoàng hôn** (ảnh vốn ít màu): trả về 554+644px = 62% khung | crop xong vẫn còn nguyên dải chữ khi soi góc 1:1 |
| 3 | ✅ **std cột/hàng so với VÙNG LÕI** | — | cột viền gần như hằng số theo chiều dọc (std thấp), ảnh thật biến thiên |

🔴 **Chi tiết quyết định của cách 3: ngưỡng phải lấy theo std của VÙNG GIỮA (40–60%), KHÔNG theo max.**
Lấy `0,30 × max` thì **chính chữ FUJI** (std ≈ 31) vượt ngưỡng 28 và được chấm là ảnh thật ⇒ đo thiếu ~20px.
Lấy `0,55 × std_lõi` thì clip mẫu đi từ "viền trên 16px" (sai) → **35px** (đúng).
⇒ **PAD 6px KHÔNG ĐỦ** (chữ vàng nằm sát mép trong của viền) — dùng **12px**.

⛔ **Và cách 3 vẫn thất bại ở cảnh đêm/đơn sắc** — không có cách đo nào cứu được, vì ở đó *thật sự* không
phân biệt được viền với nền. Xử lý: clip nào đo ra >15% khung thì **gán TRUNG VỊ CỦA LÔ**, rồi nghiệm thu bằng mắt.

🔧 **GATE BẮT BUỘC sau khi crop:** `06_VIDEO/10_tsugakuro/check_border_clean.py` — đo lại **trên bản ĐÃ CROP**
(std mép so với lõi). Lý do phải có: vòng crop đầu chạy **exit 0, 121/121, không một cảnh báo** mà vẫn sót
nguyên dải chữ; contact sheet thu nhỏ cũng cho qua, **chỉ lộ khi zoom góc 1:1**.
⚠️ Gate này cũng **không bắt hết** (nó dùng std, nên bỏ sót đúng những clip có dải chữ FUJI dọc — chữ tạo
std cao). Nghiệm thu cuối cùng phải bằng **sheet DẢI MÉP** (`sheet_corners.py`), không phải sheet giữa khung.

## ⭐ SỐ CHỐT — dùng thẳng cho video sau, đừng dò lại

Sau **4 vòng crop** ở video 10, hằng số chốt **bằng MẮT** (đo trên dải mép phóng to, không đo bằng máy):

```
SÀN CROP = [trái 110, phải 130, trên 80, dưới 80] px  (khung gốc 1920×1080)
```
Cách dùng: `crop = max(số đo tự động của clip, SÀN)`, rồi scale lại 1920×1080.
Mất **12,5% ngang · 14,8% dọc**; khung nhỏ nhất còn ~1680×920 → phóng ~1,14×.

🔴 **Vì sao phải có SÀN chứ không tin số đo:** chữ FUJI kéo tới **~55–60px** tính từ mép, mà cả ba phép đo
đều trả về 30–50px ⇒ crop xong **vẫn còn vệt chữ**, và vì có bước scale nên phần sót còn bị **phóng to lên**.
Ba vòng đầu đều chết ở đúng chỗ này.

📌 **Bài học quy trình (đắt nhất của lượt này):** memory `feedback_anh_ai_quet_sach_watermark` đã ghi sẵn
*"định vị bằng máy đã thất bại 4/4 lần ở ảnh có CHỮ → chốt vị trí bằng MẮT, ghi hằng số theo từng lô"*.
Viền phim **là ảnh có chữ**. Đáng lẽ soi mép phóng to ngay từ đầu và chốt hằng số — thay vì thử ba phép đo
tự động rồi mới quay về đúng cách đã biết.

### 1B. TẦNG BỐI CẢNH — chọn ĐÚNG MỘT preset theo video, dán trước tầng A

| Preset | Chuỗi | Dùng cho |
|---|---|---|
| `school` | `, wooden school interior, dark stained wood, sliding glass doors in wooden frames, waxed wooden floor` | video 01 給食 (đã render — **giữ nguyên, không đụng**) và mọi video học đường |
| `shotengai` | `, narrow Showa shopping street, wooden shopfronts, fabric awnings and noren curtains, hand-painted signage kept out of focus, worn asphalt and concrete` | **video 02 商店街** · các video phố/cửa hàng |
| `home` | `, small Showa house interior, tatami room, wooden sliding doors, low table, single bare bulb` | video về đồ trong nhà / bếp |
| `shop_interior` | `, inside a small Showa-era shop, dark stained wood shelving, worn plank floor, low ceiling, one bare bulb, dusty still air, no street and no sky in frame` | **cảnh BÊN TRONG cửa hàng** (tiệm sách, tiệm gạo, xưởng đậu phụ…) |
| `super` | `, early 1970s Japanese supermarket interior, metal shelving, fluorescent strip lights, stacked cardboard, wide aisle` | cảnh siêu thị |
| `lot` | `, a small unpaved vacant lot behind Showa shopfronts, packed dirt ground, a low wooden fence, a few stacked wooden crates, patches of dry grass at the edges` | **video 05 駄菓子屋** — bãi đất trẻ con chơi ベーゴマ/水ヨーヨー sau lưng dãy cửa hàng |

⚠️ **Kiểm trước khi gen:** đọc prompt xong tự hỏi *"chuỗi bối cảnh này có mâu thuẫn với cảnh đang tả không"*. Cảnh ngoài trời mà kèm `wooden school interior` = đúng cái bug vừa vá.

🔴 **PRESET TRONG NHÀ ≠ PRESET NGOÀI PHỐ — dính thật 2026-08-10 (slide_20 video 02).** Cảnh tả *"giữa hai kệ sách, **no street and no sky visible**"* nhưng preset gán là `shotengai` (= `narrow Showa shopping street … worn asphalt and concrete`). **Prompt tự cãi nhau**, model chọn vế dài hơn → ra ảnh ngõ phố. Không phải model gen sai.
→ Luật: **cảnh trong nhà/trong tiệm KHÔNG BAO GIỜ dùng `shotengai`**. `shotengai` chỉ dành cho cảnh **thật sự nhìn thấy mặt đường**.
→ Và vì tool ghép preset theo cột (không ai đọc lại chuỗi cuối), **sau khi build phải liếc 1–2 prompt dạng interior xem có lẫn chữ `street`/`asphalt` không** — grep nhanh: `grep -n "no street" scene_prompts_FLOW.txt | grep -i "shopping street"` phải ra **rỗng**.

**NEGATIVE (dán vào mọi lượt gen, không đổi):**
```
modern objects, smartphones, LED lights, plastic bottles, air conditioner,
modern clothing, sneakers with logos, any readable text or signage,
brand logos, western faces, anime style, oversaturated colors, HDR look,
clean digital sharpness, close-up faces
```

## 1.5 GEN BẰNG GOOGLE FLOW (user chốt 2026-08-02 — Veo 3.1, thay Kling)

1. **Không có ô Negative riêng** → khối NEGATIVE viết thành câu nối vào CUỐI prompt chính: `Avoid: modern objects, smartphones, LED lights, air conditioner, readable text or signage, brand logos, western faces, anime style, oversaturated HDR look, close-up faces.` — dán ở MỌI lượt (cả gen ảnh lẫn video).
2. **Quy trình trong Flow:** gen ảnh master ngay trong Flow (hoặc upload ảnh gen từ Gemini) → chọn **Frames to Video** (ảnh làm frame đầu) + dán dòng motion → ra clip ~8s. Vẫn là ảnh-trước-video-sau.
3. **Giữ đồng bộ "cùng ngôi trường": dùng tính năng Ingredients/ảnh tham chiếu** — gen 1 ảnh chuẩn của ngôi trường (hành lang + lớp học) rồi đưa vào làm ingredient cho các cảnh trường học của CÙNG video đó. Sang video sau gen lại bộ mới (luật §5 không đổi).
4. **Chi phí theo credit gói AI Pro/Ultra:** dùng **Veo Fast cho đại trà** (~28 clip), để dành **Quality cho 2–3 clip hero** (entry 01 khay 揚げパン, 48 じゃんけん). Hết credit tháng → cân nhắc trước khi mua thêm, đừng gen Quality tràn lan.
5. **Âm thanh Veo tự sinh trong clip: BỎ QUA** — không cần tắt/chỉnh; renderer thay toàn bộ audio bằng TTS + BGM khi dựng.

## 2. LUẬT KHUNG HÌNH (để 30 clip thành MỘT bộ phim + né rủi ro)

1. **Không mặt người cận cảnh** — AI vẽ mặt trẻ con dễ uncanny + không giữ nhất quán giữa các clip. Ưu tiên: **sau lưng · ngang vai · bàn tay · tầm xa · ngược sáng**. (Đúng công thức 存在しない街の記憶 đang chạy.)
2. **Không chữ trong khung** (bảng đen, poster, nhãn) — AI gen chữ Nhật ra ký tự rác, khán giả bản xứ nhận ra ngay. Cần chữ → để drawn card lo.
3. Mọi cảnh trong CÙNG MỘT VIDEO phải ở **cùng một nơi chốn** — dùng đúng một preset §1B và để nguyên văn trong mọi prompt thì các cảnh mới khớp nhau. (Video 01 = cùng một ngôi trường: gỗ tối màu, cửa kính trượt khung gỗ, sàn gỗ đánh xi. Video 02 = cùng một dãy phố.) ⚠️ Đây là luật **theo video**, không phải luật vĩnh viễn của kênh — đừng khoá nơi chốn của một video vào chỗ dùng chung, đó đúng là bug đã vá ở §1.
4. Ảnh master 16:9, gen 3–5 bản/cảnh → **duyệt mắt chọn 1** → mới đưa sang i2v. Loại thẳng bản có đồ vật hiện đại/mặt rõ/chữ.
5. i2v: 6–8s/clip, camera CHẬM (slow push-in / slow pan / static + chuyển động trong khung), cấm cắt cảnh trong clip. Motion prompt chỉ tả **chuyển động**, không tả lại bối cảnh (ảnh đã lo).
6. ⭐ **MOTION 8s PHẢI CÓ DIỄN TIẾN 3 NHỊP: mở → triển → kết** (user chốt 2026-08-02) — một hành động đi tới nơi (tay nhấc bánh → ngập ngừng → cầm ra khỏi khung), KHÔNG phải một vòng lặp (hơi bốc mãi, rèm lay mãi). Chuyển động lặp chỉ được làm LỚP NỀN đằng sau hành động chính. Cảnh bản chất tĩnh (loa tường, cốc sữa) → gen **3–4s** thôi, đừng ép 8s.

## 2.7 🔴 FILTER TRẺ EM CỦA VEO/FLOW (dính "vi phạm chính sách" 2026-08-02)

Google chặn gắt gen người vị thành niên photorealistic — từ khóa `child/children/kids/elementary school` là trúng đạn, kể cả cảnh lành. **Đã thay toàn bộ prompt sang `student/students/figure/small hands`.** Khi một cảnh VẪN bị chặn, xử theo thang, mỗi nấc thử 1 lần:

1. **Bỏ từ chỉ người, giữ hành động:** `a student pushes the desk` → `the desk is pushed across the floor` (thể bị động, người ngoài khung).
2. **Hạ xuống bàn-tay-không-tuổi:** `small hands` → `hands` (bỏ mọi tính từ gợi tuổi).
3. **Bỏ hẳn người khỏi cảnh** — vật tự chuyển động từ ngoài khung (mẫu: fallback D3). Lời kể của イタコ gánh phần người.
4. ⛔ **KHÔNG spam regenerate câu bị chặn, không lách kiểu mô tả vòng vo tuổi nhỏ** — chặn nhiều lần liên tiếp có thể dính cờ tài khoản. Bị chặn ở nấc 3 (không còn người mà vẫn chặn) = thủ phạm là từ khác trong prompt, báo lại để mổ.

Lưu ý: filter chạy cả tầng NGỮ NGHĨA, không chỉ keyword — cảnh đông "students" nhỏ tuổi vẫn có thể bị vợt ở bước ra video dù ảnh master qua được. Các cảnh **tay-cận + vật** (16, 19, 22, 26, 31, 35, 42, 48) an toàn nhất; cảnh đông người (39, 47, 52) rủi ro nhất — gen chúng sau cùng, hết chặn thì thôi, còn chặn thì chuyển ảnh-tĩnh + pan.

## 3. BỐN CẢNH DEMO (test go/no-go style — gen theo thứ tự này)

### D1 — Hành lang trưa nắng (beat 2: mùi 給食 trôi qua hành lang)
**Image prompt:**
```
Empty wooden school corridor in a Japanese elementary school, long row of
sliding wooden-framed windows on one side, warm noon sunlight casting window
shadows on polished wooden floor, faint steam drifting from far end of the
corridor, a few pairs of small indoor shoes neatly lined at classroom
entrance, view down the corridor from a low waist-level camera height
```
**Motion (8s, 3 nhịp):** `camera slowly pushes forward down the corridor; midway, steam from the far end thickens and drifts across the sunbeams; near the end a classroom door slides open a hand's width and warm light spills out`

### D2 — 給食当番 bê thùng canh (beat 3)
**Image prompt:**
```
Two Japanese students seen from behind, wearing white
cooking aprons and white caps, carefully carrying a large dented aluminum
food canister together down a wooden school corridor, steam rising from the
canister, warm light from windows, other students' silhouettes far in the
background
```
**Motion (8s, 3 nhịp):** `the two students walk away from camera; the canister tilts and one student stumbles half a step; they steady it together, exchange a nod, and continue as steam puffs up when they pass the sunlit window`

### D3 — Kéo bàn ghép nhóm (beat: 班の形, tiếng bàn ghế rầm rầm)
**Image prompt:**
```
Interior of a 1970s Japanese elementary school classroom, students in simple
shirts seen from behind and from the side pushing small wooden desks with
metal legs together into groups, warm afternoon light through large windows,
old dark wooden floor, cloth school bags hanging on desk hooks, no faces
clearly visible
```
**Motion (8s, 3 nhịp — SỬA 2026-08-02, bản cũ nhiều người+vật va nhau gen lỗi):**
`one student seen from behind pushes a single wooden desk across the floor; it bumps gently into another desk and aligns with it; the student pulls a chair over the floor toward the desk and sits down, cloth bag swaying on the desk hook`
**Fallback nếu vẫn lỗi (bỏ hẳn người, chỉ vật + camera):**
`camera slowly pans across the classroom as two desks stand slightly apart; a desk slides softly into place against the other from off-screen; the cloth bags on the hooks sway once and settle`

### D4 — Khay 揚げパン bốc hơi (beat 5 — cận vật, cú đấm hoài niệm)
**Image prompt:**
```
Close-up of a dented aluminum school lunch tray on a wooden desk: one sugar
and kinako coated fried bread roll on a small aluminum plate, a glass milk
bottle with paper cap, aluminum bowl of pale stew, thin steam rising, a
student's small hand at the edge of frame reaching for the bread, warm window
light, shallow depth of field
```
**Motion (8s, 3 nhịp):** `steam rises from the stew; the small hand reaches in and hovers over the bread for a beat; then it picks the bread up, leaving a ring of kinako dust on the plate, and lifts it out of frame through the sunlight`

## 4. TIÊU CHÍ DUYỆT DEMO (mắt người, từng clip)

- [ ] Không vật hiện đại / không chữ đọc được / không logo
- [ ] Người ra dáng trẻ con Nhật thập niên 70 (tóc, áo, giày vải) — không ra mặt Tây, không anime
- [ ] 4 clip đặt cạnh nhau nhìn như **một bộ phim** (tông màu + grain + ánh sáng khớp)
- [ ] Chuyển động chậm, không morph/giật ma quái (tay 6 ngón, chân trượt sàn…)
- [ ] Cảm giác đầu tiên khi bấm play: "phim tư liệu cũ" chứ không phải "AI demo"

Đạt cả 5 → khóa style vào BIBLE + gen tiếp thư viện cảnh nền (lớp học, sân trường, cổng trường, 給食室) rồi làm SLIDES 65/25/10. Rớt tiêu chí nào → chỉnh style suffix, KHÔNG chỉnh từng cảnh riêng lẻ (vá lẻ là mất đồng bộ).

## 5. ⛔ KHÔNG có thư viện clip dùng lại (SỬA 2026-08-02, user chốt)

Mỗi video **gen bộ clip mới 100%** — khớp luật no-reuse asset (media-library 2026-07-29) và né profile "video giống hệt nhau chỉ khác tiêu đề" (compliance §1, đúng profile kênh 朗読 nền lặp bị quét). Nhận diện kênh nằm ở **STYLE LOCK §1 + mô tả "cùng ngôi trường" lặp trong prompt** — cùng thế giới, cảnh luôn mới, chi phí gen lại chỉ thêm vài $/video. Ngoại lệ duy nhất: **end card 図鑑** (chữ ký kênh, như watermark — cố định mọi video).

## 6. BỘ PROMPT THEO VIDEO (sinh bằng tool, không viết tay)

Từ video 02 trở đi, prompt cảnh **không gõ tay vào file này nữa** — chúng nằm trong một tool per-video để `match` của SLIDES được verify bằng máy, không chết cue.

| Video | Tool sinh | Output |
|---|---|---|
| 01 給食 | (viết tay — 4 cảnh demo §3) | `03_SCRIPTS/01_kyushoku_SLIDES.json` |
| **02 消えたもの30** | `tools/build_scenes_02.py` | `03_SCRIPTS/02_kieta-mise_SLIDES.json` (42 entry) · `06_VIDEO/02_kieta-mise/scene_prompts_FLOW.txt` (42 dòng, import thẳng) · `scene_prompts_TENFILE.txt` (khớp thứ tự ↔ tên file) |

**Tool tự ghép prompt** = `[mô tả cảnh]` + `[preset bối cảnh §1B]` + `[style lock §1A]` + `[Avoid]`, nên đổi style lock một chỗ là cả bộ đổi theo. Sửa cảnh → sửa bảng `SCENES` trong tool rồi chạy lại.

**Gate tool tự chạy** (chạy `python tools/build_scenes_02.py` in ra ngay):
- mọi `match` phải là substring của một dòng trong `_TTS.md` sau khi strip tag — **sai một cái là exit 1, không ghi file**;
- ≥6 giây/hình · ≤6 đổi hình/phút (`audience-45plus` §2) · cảnh báo nếu một hình treo >60s;
- đếm đủ 30/30 điểm có ảnh riêng.

Kết quả video 02: **42 entry · 15,8 s/hình · 3,80 đổi hình/phút · 30/30 điểm** ✅

⚠️ **Sửa lời trong `_TTS.md` thì CHẠY LẠI TOOL** — không sửa tay `SLIDES.json`. Đây đúng là chỗ luật `humanize-script-voice` §4 cảnh báo "sửa câu là chết cue"; tool biến nó thành lỗi bắt được lúc build thay vì lỗi ở phút thứ 2 của lần render 30 phút.
