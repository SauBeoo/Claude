---
name: video-vox
description: Dựng LỚP HÌNH KIỂU VOX (explainer) cho video YouTube — scene plan đi TRƯỚC asset, ảnh thật làm NỀN để annotate đè lên, chart/sơ đồ động, thẻ 原典. Trigger khi user nói "dựng vox", "làm thẻ vox", "lớp hình kiểu Vox", hoặc sau khi một skill `script-*` xuất `_TTS.md` mà bài có nhiều số liệu / cơ chế vô hình / mốc thời gian. Tool dùng chung mọi kênh (`Projects/_media_library/make_vox.py`), gate máy `check_vox.py`.
---

# Dựng lớp hình kiểu VOX

> Chốt **2026-08-06** sau khi user chấm bản cũ *"không đúng lắm"* và đưa video
> `I Made a Vox-Style Explainer Video With One Prompt (Claude)` (Zubair Trabzada | AI Workshop).
> Thứ lấy từ video đó là **quy trình**, không phải Higgsfield: ① **scene plan đi TRƯỚC asset**
> ② đóng gói thành **skill file** ③ vốn từ vựng hình = **collage ảnh thật + chart động**.
> Kiến trúc & lý do kỹ thuật: docstring của `Projects/_media_library/make_vox.py`.

## 0. BỆNH ĐANG CHỮA (đọc trước, đừng lặp)

Đo trên `youtube-jp-co-dai/03_SCRIPTS/16_..._SLIDES.json` — 120 entry / **62 thẻ vox**:

| | số | nghĩa |
|---|---|---|
| `title` (băng vàng + chữ) | **39 (63%)** | 39 khung GIỐNG HỆT nhau → PowerPoint, và rơi vào *inauthentic content* (`youtube-compliance.md` §1) |
| `flow` (ảnh thật + annotation đè) | **1** | chữ ký Vox — dùng đúng 1 lần |
| ảnh full-khung không annotation | 58 | 2 lớp chạy song song, **không gặp nhau trong 1 khung** |
| collage / timeline / process / line / dot | **0** | vốn từ vựng thiếu gần hết |

**Vox = annotate ĐÈ LÊN ảnh + chart động. Bản cũ = thẻ chữ ĐỨNG CẠNH ảnh.** Đó là toàn bộ khác biệt.

---

## GĐ1 · SCENE PLAN ĐI TRƯỚC ASSET ⛔ không được bỏ

Đây là chỗ video kia làm đúng mà mình làm ngược — 39 thẻ `title` sinh ra chính vì dựng thẻ trước khi nghĩ.

Đọc `_TTS.md`, chia thành **beat** (một ý = một beat, thường 15–30 giây). Với MỖI beat trả lời đúng 3 câu:

1. **Beat này nói về VẬT, về SỐ, hay về CƠ CHẾ vô hình?** → quyết `kind` (bảng GĐ2).
2. **Một câu duy nhất người xem phải mang đi là gì?** → đó là `head`/`title`/`note` của thẻ. Không viết được thành 1 câu ≤20 ký tự Nhật thì beat đang gộp 2 ý — tách ra.
3. **Cần mấy element, cái nào hiện TRƯỚC?** Trần **3 element**. Nhiều hơn = pháo hoa, không phải Vox.

**Output = mục `## 🎥 VOX PLAN` ghi THẲNG vào file script** (không chỉ in ra chat — [[feedback_luu_prompt_vao_file]]):

```markdown
## 🎥 VOX PLAN

| slot | match (chuỗi trong _TTS.md) | kind | nền | message 1 câu | element (thứ tự hiện) | ảnh cần fetch |
|---|---|---|---|---|---|---|
| 03 | 塩の濃さを変えるだけで | stat | phẳng | 三か月もつ | số đếm lên → 2 cột → note | — |
| 16 | 冷蔵庫という道具 | flow | **ảnh** | 保存食ではなく、料理 | pin 冷蔵庫 → mũi tên | 冷蔵庫の中の漬物 |
| 45 | 乳酸菌は空気が | process | phẳng | 空気を抜く道具 | 重石 → 水の膜 → 乳酸菌 | — |
| 62 | 家庭での発生が | source | phẳng | 厚労省 令和6年6月 169人 | tên cơ quan → câu → số | — |
```

**Trần số lượng:** `title` ≤ **4/video** (hồ sơ kênh `title_cap`). Ai cũng muốn thêm thẻ chữ vì nó dễ — gate X1 chặn.

---

## GĐ2 · BẢNG LUẬT CHỌN KIND (thay việc chọn theo cảm tính)

| beat nói về | kind | nền | ghi chú |
|---|---|---|---|
| **vật/món/thao tác cụ thể** | `flow` | **ẢNH THẬT** ⭐ mặc định mới | `pins` ghim nhãn lên đúng chỗ, `arrows` chỉ hướng |
| nhiều vật đặt cạnh nhau | `collage` | cutout rembg | **≤2 ô** trên kênh có phụ đề to (3 ô → ảnh chỉ cao ~200px, tool cảnh báo) |
| 1 con số đắt | `stat` | phẳng / ảnh | số đếm lên, lấp gần hết vùng chữ |
| 2+ số so nhau | `bar` | phẳng | `"hot": -1` để nhấn cột CUỐI |
| xu hướng theo thời gian | `line` | phẳng | nhãn điểm cuối tự nhấn |
| tỉ lệ người/đơn vị | `dot` | phẳng | 1 chấm = 1 đơn vị — mạnh nhất cho「95%は…」 |
| đúng/sai · trước/sau | `compare` | 1–2 bên ảnh | **có ảnh thì BỎ nhãn chữ** (ảnh là nhãn). Hai bên phải ĐỐI NHAU ✗ vs ○ |
| cơ chế vô hình (khí/nhiệt/nước) | `room` | phẳng | 3 preset `exchange`/`mix`/`stack`; hình được bleed dưới phụ đề |
| quy trình A→B→C | `process` | phẳng | ≤4 bước, `"hot": true` cho bước chốt |
| mốc lịch sử | `timeline` | phẳng | mốc cuối tự tô đỏ |
| **trích nguồn thật** | `source` | phẳng | **≥1/video** — gate X5 |
| đầu chương | `title` | phẳng / ảnh | **trần 4/video**, không 2 thẻ liền nhau |
| **trang hồ sơ tích luỹ** ⭐ | `board` | giấy trắng grain | user chốt 2026-08-08 đêm: *"đọc thông tin nào thì thông tin đó BAY VÀO gắn vào trang"*. **Mỗi CUE một thẻ board**: item cũ nằm sẵn, item `"new": true` bay vào cue đó (label/photo/text bay + xoay đậu + bóng co; stamp SLAM; arrow/string/circle/cross reveal). Dissolve 0.4s giữa cue → nhìn liền như MỘT trang sống. Item: `{"type": "label\|photo\|stamp\|text\|arrow\|circle\|cross\|string", "x","y", "new", "t"}`; photo qua `cut` (rembg+sticker); món mới nhất tự có glow thở. Chuỗi 3–5 cue board liên tiếp được miễn X3 về mặt tinh thần (cùng kind nhưng nội dung tích luỹ) — nếu gate kêu thì xen 1 thẻ khác kind giữa 2 chuỗi board |

Khai báo trong `*_SLIDES*.json` (renderer đã hiểu, **không phải mổ renderer**):

```json
{"match": "<chuỗi CÓ THẬT trong _TTS.md>", "photo": false, "video": true,
 "vox": {"kind": "flow", "bg": "photo", "kicker": "一つ目", "head": "…",
         "pins": [[1400, 300, "重石"]], "arrows": [[1300, 360, 1080, 470, 0.18]]}}
```

🔴 **Cờ là `"video": true`, KHÔNG phải `"handmade": true`** (cờ đó nghĩa là footage TỰ QUAY). Gate lớp thủ công đã bỏ 2026-08-09, nhưng hai cờ vẫn là hai loại dữ liệu khác nhau — đừng gắn lẫn.

---

## GĐ3c · LỚP ĐẠO CỤ ANALOG (đại tu 2 — user chốt 2026-08-08 sau khi chê nét vector "thô")

Annotation không còn là nét PIL vẽ — là **VẬT THẬT dán + làm động** (mổ video tham
chiếu: `_media_library/VOX_COLLAGE_PLAN_2026-08-08.md`): mũi tên/khoanh/gạch X = **sáp
đỏ texture thật** (reveal kiểu đang vẽ tay) · nhãn = **chữ Nhật thật đóng lên giấy xé
prop + đinh ghim/băng dính**, thả rơi có bóng · số chốt (timeline/原典) = **con dấu
grunge SLAM** · nối vật = **dây chỉ đỏ** căng giữa 2 đinh (`prop_string`).
- Kho prop: `_media_library/props/` (20 PNG + INDEX.json; gen 1 lần bằng
  `props/PROPS_PROMPTS.md`, prep bằng `props/props_prep.py` — mực đỏ key theo ĐỘ ĐỎ,
  vật đặc rembg). Kênh **thiếu props → tool tự rơi về nét vector cũ**, không gãy.
- Nền phẳng tự rắc 1 vết đời sống (cà phê/mực) DƯỚI safe_bottom — tầng analog.
- ⭐ **Camera + chuyển cảnh (2026-08-08 chiều, user: "chuyển cảnh mượt hơn, sinh động hơn"):**
  ① **settle** 0.5s đầu thẻ (cả khung zoom 1.045→1, máy quay 'đậu' xuống tài liệu)
  ② **push-in** liên tục ~4.5%/clip (zoompan hậu kỳ, knob `"camera": "push"` — nền và
  annotation trôi CÙNG nhau nên pin không lệch; tắt bằng `"camera": None`)
  ③ nhãn giấy **lắc ±0.4°** quanh đinh theo nhịp idle (sin nguyên chu kỳ — loop sạch)
  ④ ranh giới thẻ trong VIDEO THẬT: `video_render.py` đã biết **dissolve TỚI CLIP**
  (trích frame 0 của mp4) + co-dai bật `transition: dissolve/0.4` trong `channels.py`
  — hết cắt phần phật khi vào thẻ vox (audience-45plus §2.3).
  ⑤ **PARALLAX 2.5D** (đại tu 3, knob `"parallax": True`): ảnh nền clean được rembg
  tách chủ thể (giữ nguyên vị trí, không trim) → camera thở làm 2 lớp trôi lệch 50%
  tốc độ = chiều sâu thật; chủ thể <4% hoặc >62% khung thì tự bỏ. Khe hở sau lưng
  chủ thể vá bằng blur.
  ⑥ **Micro-physics**: con dấu slam → cả khung DƯ CHẤN 4px tắt dần 0.45s (cắt cứng —
  exp không về 0 tuyệt đối, để trôi là vỡ assert loop) · nhãn giấy rơi ease-in rồi
  **nảy 1 nhịp 7px** · mọi chuyển động camera/lớp đều affine sub-pixel, cấm resize
  bậc pixel nguyên (tái phạm bệnh zoompan).

## GĐ3b · ĐƯỜNG ẢNH AI (user chốt 2026-08-08 — "cho tao prompt, tao gen, mày làm hiệu ứng")

Thay vì fetch stock: Claude viết prompt (STYLE ANCHOR cố định của kênh + bố cục chừa
copy-space theo kind) → **user gen** → Claude soi ảnh đặt toạ độ pin/mũi tên theo chi
tiết THẬT trong ảnh → dựng thẻ với `"photo": <path>` + `"photo_style": "clean"` (tool
KHÔNG darken tranh/ảnh có copy-space sẵn; chữ ink + highlight vàng).
- Mẫu chạy được: `youtube-jp-co-dai/06_VIDEO/_vox_ai_demo/` (PROMPTS.md + `_prep.py`
  vá watermark ✦ + xoá logo thật + `ai_slides.json` + DEMO_AI_6the.mp4).
- ⚖️ BẮT BUỘC trước khi dùng: vá watermark model, **xoá logo/nhãn hiệu thật** (ca SANYO),
  loại bản dính chữ AI giả. Ảnh minh hoạ không realistic → không tick synthetic; ảnh
  photoreal generic (vật, không người/sự kiện thật) → cân nhắc theo `youtube-compliance.md` §2.

### 🔴 HAI LUẬT ĐÚC TỪ VIDEO 19 CO-DAI (2026-08-12) — đọc trước khi viết prompt

**① STYLE LOCK GIỮ TÔNG NHƯNG KHOÁ LUÔN FRAMING → phải có 2 biến thể.**
Lô 1 của video 19 (82 ảnh) có tông **rất đồng nhất** mà **không một ảnh nào là macro thật**:
mọi ảnh thành *"phòng washitsu đẹp + vật nhỏ ở đâu đó"* — ống **gốm** thay ống thoát nước, bã
cà phê **rắc trên mép bàn** thay hạt phóng đại, thẻ 「miệng cống nhìn thẳng」 **không có miệng
cống trong khung**. Nguyên nhân là chính STYLE string: cụm `Japanese home interior, soft
natural daylight from a side window` **ép framing phòng vào MỌI ảnh**.
🔴 Với thẻ vox đây là **chí tử** — vox *annotate ĐÈ LÊN* ảnh; chủ thể mờ thì pin và mũi tên
trỏ vào không khí. ⇒ **Ảnh cho thẻ vox LUÔN dùng biến thể macro:**
```
STYLE_MACRO = "Photorealistic extreme close-up macro photograph, the subject FILLS THE FRAME
and is the only thing visible, tight crop, plain dark out-of-focus background, NO room,
NO window, NO furniture, NO tableware in view. …"
```
Giữ `STYLE` (có bối cảnh) cho ảnh thường/mood. Mẫu: `youtube-jp-co-dai/tools/gen_slides19.py`
(`STYLE` / `STYLE_MACRO` / `MACRO_LINES` / `VOXSUBJ`).

**② PROMPT ẢNH THẺ VOX PHẢI LẤY TỪ BẢNG RIÊNG, KHÔNG ĐƯỢC RƠI VÀO FALLBACK.**
Bug thật ở video 19: generator lấy chủ đề ảnh theo **dòng thoại**, mà thẻ vox không có key
trong bảng đó → **18/18 ảnh vox nhận prompt mặc định của khúc**; thẻ 原典 `東京都下水道局`
nhận prompt *"chảo dầu"*, thẻ `澱粉科学 1972` nhận *"bột và bát"*. ⇒ Giữ **`VOXSUBJ`** = bảng
tên-thẻ → chủ thể ảnh, và assert mọi thẻ có ảnh đều tra được trong bảng đó.

**③ THỨ TỰ: SLIDES + PREVIEW → USER DUYỆT → RỒI MỚI XUẤT PROMPT ẢNH.**
Ở video 19 làm ngược (giao 81 prompt cùng lúc với SLIDES) → user gen 82 ảnh xong mới phát hiện
slide cần sửa + prompt sai ⇒ **phải gen lại 36/81 ảnh**. Xem [[feedback_duyet_slide_truoc_khi_gen_anh]].

---

## GĐ3 · FETCH ẢNH — query phải khác trước

Ảnh giờ là **NỀN để đặt chữ**, không phải minh hoạ đứng riêng. Ba điều đổi:

1. Thêm **`copy space` / `plain background` / `on white`** vào query — ảnh kín chi tiết thì không có chỗ đặt chữ.
2. **Tải MỚI riêng video này**, không lấy từ kho (`media-library.md` §2 — kho là SỔ ĐEN).
3. **Entry 0 vẫn phải là CHỦ THỂ của bài** (`media-library.md` §2.0) — không đổi.
4. **Duyệt sheet ẢNH trước khi dựng thẻ.** Ảnh không có vùng trống → hạ thẻ về kind phẳng; ⛔ **đừng dim đè cả ảnh** ([[feedback_thumbnail_bg_brightness]]).

---

## GĐ4 · DỰNG THẺ

```bash
cd E:\Claude\Projects\_media_library
python make_vox.py demo <out_dir> --channel co-dai                       # bộ 12 kind mẫu
python make_vox.py <SLIDES.json> <clips_dir> --channel co-dai --still    # PNG duyệt nhanh
python make_vox.py <SLIDES.json> <clips_dir> --channel co-dai            # mp4 thật
python make_vox.py <SLIDES.json> <clips_dir> --channel co-dai --only 7 22
```

- Mỗi thẻ ra 1 mp4 **≥30 giây** = INTRO entrance 2.5–4.5s @30fps + **IDLE LOOP 4s** (glow
  thở / pulse-ring / sheen — lặp không mối nối tới hết clip); `video_render.py` tự
  loop+trim theo cue. ⭐ **Đại tu 2026-08-07** (user: *"video gen ra xấu quá"*): hết cảnh
  "động 4s rồi đứng hình 26s"; ảnh nền qua `treat_photo` **darken/duotone** (hết scrim
  trắng tẩy ảnh); nền phẳng có **grain**; đồ hoạ/khối màu được **TRÀN xuống dưới
  safe_bottom** (chữ có nghĩa vẫn trên) — hết cảnh nửa dưới trống trơn.
- Spec per-card mới (tuỳ chọn): `"photo_style": "duotone:ink|blue|warm"` (mặc định
  darken theo kênh) · `"tone": "accent"` cho title (cả khung vàng) · `"anim_sec"` đè cửa
  sổ intro (tool tự tính floor theo số element, khai nhỏ hơn cũng không cắt entrance).
- **`.sig` sidecar**: spec/ảnh/tool/knob style kênh không đổi thì skip, đổi thì tự dựng
  lại (`render-background.md` §2.5 — resume phải biết ASSET ĐÃ ĐỔI).
- **Kênh chưa khoá hồ sơ `vox` trong `channels.py` thì tool TỪ CHỐI chạy.** Khoá sau khi duyệt demo, đừng điền bừa. Knob style: `photo_treatment/duotone/grain/ghost/sticker/highlight`.
- Duyệt PNG có thể thêm **`--sub-mock`**: vẽ mock phụ đề 2 dòng lên bản `--still` —
  kiểm một lần nhìn cả "chữ có nghĩa không bị đè" lẫn "nửa dưới không còn trống".

### Vùng an toàn — hiểu con số này trước khi trách bố cục

Tool tự tính `safe_bottom` từ `sub_style`+`sub_size` của kênh. **co-dai (`outline`/26, 2 dòng) → y=678**, tức
**nửa dưới khung là của phụ đề** và vùng chữ chỉ còn ~400px. Hệ quả thiết kế, không phải lỗi:

- **MỘT ý mỗi thẻ.** Không nhồi head + sơ đồ + note + nhãn vào một khung.
- ⭐ Từ đại tu 2026-08-07: CHỮ CÓ NGHĨA vẫn trên `safe_bottom`, nhưng **đồ hoạ/khối
  màu/ghost number được tràn xuống dưới** (phụ đề đè phần trang trí là thiết kế) —
  sheet không còn trống nửa dưới; muốn thấy đúng khung lúc phát thì duyệt bằng `--sub-mock`.
- Kênh nào hạ `sub_size` thì vùng chữ tự rộng ra, không phải sửa tool.

---

## GĐ5 · DUYỆT MẮT contact sheet (bắt buộc)

⭐ **`_vox_sheet.jpg` CHỈ CÓ THẺ VOX — chưa đủ để duyệt cả video** (user chốt 2026-08-12:
*"tao cần duyệt từng frame 1"*). Ảnh thường được `video_render.build_slides()` ghép **trong lúc
render** nên trước đó không có gì soi; kênh dùng `make_stage` thì có đủ PNG, kênh dùng `vox` thì
không. ⇒ Xuất preview **TỪNG entry**:
```bash
python <proj>	ools\preview_frames.py <SLIDES.json> 06_VIDEO\<slug>   # → preview/frame_NN.png + _sheet_pN.jpg
```
Tool gọi **thẳng `video_render.make_slide()`** (đúng hàm renderer dùng) nên thấy gì là render ra
thế; chỉ khác 2 điểm: phụ đề là MOCK, và chưa có crop-pan 1,12×. Mẫu:
`youtube-jp-co-dai/tools/preview_frames.py`.

`clips/_vox_sheet.jpg`. Ba câu hỏi:

1. **Che chữ đi — có nhận ra beat nói gì không?** Không → thẻ đang là chữ trang trí, đổi kind.
2. **3 thẻ liền nhau có khác layout không?** Giống nhau → đúng bệnh video 16.
3. **Có chữ nào chạm/đè nhau, hoặc rơi xuống dưới `safe_bottom`?**

Đọc cả **cảnh báo tool in ra** — chúng là chỗ đã sai một lần rồi: `pin lấn dải message` · `collage ảnh chỉ cao Npx` · `hero xuống Npx` · `title không vừa cỡ tối thiểu` · `compare có ảnh nên BỎ nhãn`.

---

## 🔧 THẺ TRÊN ẢNH — vá `make_vox.py` 2026-08-12 (user chốt, co-dai video 19)

**Bệnh:** dải vàng highlight sau tiêu đề **chỉ được nối vào `flow`/`timeline`**; `bar`/`line`/
`compare`/`process` gọi `head_line()` trần → tiêu đề mực đậm trên ảnh tối là **mất chữ**. Và nhãn
trục của `line` / nhãn cột của `bar` vẽ bằng `P["muted"]`/`P["ink"]` cỡ 36–46 **không stroke**.

**Đã đo và LOẠI 3 cách chữa bằng ảnh** (đừng thử lại): `darken` → mất nhãn trục · `scrim`
top=0/195 → **không ăn** · `duotone:ink` → line tạm được nhưng **bar TỆ HƠN**. ⇒ Nguyên nhân
không ở ảnh mà ở **chính nhãn**.

**Vá 6 chỗ trong `_media_library/make_vox.py`:** `head_line(..., highlight=on_ph)` cho 4 kind ·
helper **`_onph()`** (trả kwargs stroke; `on_ph=False` → **rỗng**, nhánh cũ nguyên vẹn) ·
`_bars()` thêm tham số `on_ph` · `k_line` trục + nhãn mốc · `kicker(on_photo=…)` ·
`src_label(on_photo=…)`.

⭐ **Bán kính ảnh hưởng = chỉ kênh có hồ sơ `vox`.** Đo 2026-08-12: **`co-dai` là kênh DUY NHẤT**
có khối `vox` trong `channels.py`; **nenkin KHÔNG dùng `make_vox`** (nó dùng `make_stage`). Mọi
thay đổi gác sau `on_ph` nên thẻ không khai `bg:photo` chạy y hệt bản cũ. Smoke test:
`make_vox.py demo --channel <k> --still` → 13/13 kind.
⚠️ Hệ quả biết trước: video co-dai **17** (15 thẻ) và **18** (3 thẻ) đã đăng cũng có chart mang
ảnh → **re-render sẽ trông khác bản đã lên sóng**. Backup: `make_vox.py.bak_20260812` + `.bak2_…`.

**✅ Xác nhận trên bản render thật (co-dai 19, duyệt 10 frame 2026-08-13):** thẻ `process`
(198,5s · 201,5s), `line` (640s), `stat` trên ảnh (480s) — tiêu đề, nhãn trục `今夜/三日/一月/半年`,
và số `100円` **đều đọc rõ trên ảnh tối**. Bản vá ăn ở cả 4 kind, không thẻ nào bị mất chữ.

### 🟡 Việc CÒN MỞ, phát hiện cùng lượt: cột trắng của `process` chạy xuống dưới dải phụ đề

Ở `process`, **hộp cột trắng cao gần trọn khung** (≈y 350→1070) nên phụ đề nằm **trên nền trắng**,
trong khi phần còn lại của video phụ đề nằm trên ảnh tối. Vẫn **đọc được** (nhờ `outline` viền đen
của `audience-45plus.md` §3.1 — đúng chỗ luật đổi sang outline lại hoá có lợi), nhưng viền đang phải
gánh toàn bộ; và nó **lệch nhìn** so với các frame khác.

📌 **Vì sao `safe_bottom` KHÔNG bắt được:** `safe_bottom()` chỉ chặn **chữ có nghĩa** của thẻ (nhãn
cột `50度のお湯` nằm ở ĐỈNH hộp, ~y 480 → hợp lệ). Nó **không biết gì về nền vẽ dưới chữ.**
⇒ Đây là lỗ của gate, không phải lỗi thi hành.
⇒ **Cách sửa khi tới lượt đụng `k_process`:** hạ đáy hộp cột về `safe_bottom(...)` thay vì mép khung,
để dải phụ đề luôn rơi trên ảnh. ⛔ **Đừng re-render video 19 vì việc này** — chữ đọc được, và
`feedback_bot_render_lai` chỉ cho render lại khi video **hỏng thật**.

---

## GĐ6 · GATE MÁY (FAIL = không render)

```bash
python E:\Claude\Projects\_media_library\check_vox.py <SLIDES.json> --channel co-dai --tts <..._TTS.md>
```

| | luật |
|---|---|
| **X1** | `title` ≤ `title_cap` (4) và không 2 thẻ `title` liền nhau |
| **X2** | ≥50% thẻ vox mang ẢNH THẬT (`bg:"photo"` có ảnh · `collage`/`compare` có cutout) |
| **X3** | không kind nào lặp >2 lần LIÊN TIẾP |
| **X4** | mọi toạ độ chữ (`pins`) nằm TRÊN `safe_bottom` |
| **X5** | ≥1 thẻ `source` (原典) — **GIỮ** dù rule handmade đã bỏ; căn cứ giờ là §YMYL của project + `youtube-compliance.md` §1 |

Chạy CÙNG LƯỢT với gate cấu trúc của kênh, ví dụ co-dai:

```bash
python tools\check_coldopen.py 17 && python E:\Claude\Projects\_media_library\check_vox.py ^
    03_SCRIPTS\17_..._SLIDES.json --channel co-dai --tts 03_SCRIPTS\17_..._TTS.md
```

⚠️ Gate này **KHÔNG kiểm chuỗi `match`** — đó là `check_cues.py` (`youtube-jp-health/tools`). Sửa lời thoại thì chạy **cả hai** (`humanize-script-voice.md` §4: sửa câu là chết cue).

---

## GĐ7 · RENDER NỀN

Theo `render-background.md`: bọc `.cmd` + log ra `06_VIDEO/<slug>/render.log` + `EXITCODE`, gọi `run_in_background: true`, **không bao giờ foreground**. Xong = `EXITCODE=0` **và** duration khớp `subs.srt` **và** đã duyệt ≥4 frame bằng mắt — trong đó **bắt buộc 1 frame là thẻ `flow`/`collage`** để xác nhận chữ không bị hộp phụ đề đè.

---

## BA ĐIỀU KHÔNG ĐỔI

1. **Chuyển động nằm TRONG khung**, không ở nhịp cắt → `audience-45plus.md` §2 (≤6 đổi hình/phút) vẫn giữ. ⛔ Đừng bê tool này sang làm cut nhanh.
2. **1 giọng, 1 style nền** ([[feedback_video_no_motion_mot_giong]]); không pan/Ken Burns lên thẻ vox (chuyển động đã bake trong clip).
3. **Nguồn thật vẫn bắt buộc** (thẻ `source` = 原典) — nhưng vì §YMYL cấm bịa số/nguồn, KHÔNG phải vì gate lớp thủ công (đã bỏ 2026-08-09). Vẫn là **việc của Claude lúc viết script**, không phải việc user ([[feedback_user_khong_quay_duoc]]).

## ĐIỀU KHÔNG HỨA

Lớp hình đẹp hơn **không mở vòi phân phối**. co-dai đang `BROWSE/SUGGESTED = 0` và bệnh đã đo là retention 60–75 giây đầu (`CHANNEL_DIAGNOSIS_2026-07-30.md`); đối thủ nổ view chỉ dùng stock-fade (`BENCHMARK_RIVALS_2026-07-29.md`). Đây là lớp **giữ chân + moat**, không phải thuốc chữa view — đọc số sau khi làm xong thì đừng lẫn nhân quả ([[feedback_khong_suy_dien_co_che_nhan_qua]]).

## LIÊN QUAN
- Tool + lý do từng quyết định kỹ thuật: `Projects/_media_library/make_vox.py` (docstring + comment tại chỗ)
- Hồ sơ vox từng kênh: `Projects/youtube-jp-health/tools/channels.py` khoá `"vox"`
- Asset: `.claude/rules/media-library.md` · Lớp thủ công: ĐÃ BỎ (`.claude/rules/handmade-layer.md`)
- Nhịp/phụ đề/tuổi 45+: `.claude/rules/audience-45plus.md` · Chạy nền: `.claude/rules/render-background.md`
