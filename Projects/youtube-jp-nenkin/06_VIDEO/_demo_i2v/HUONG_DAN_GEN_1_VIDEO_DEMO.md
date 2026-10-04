# HƯỚNG DẪN — gen 1 VIDEO DEMO trên Google Flow (i2v)

> Nguồn: `PENSION RESEARCH LAB_ THE TWO PAYMENTS - 2026-09-10_00-29.json` (66 shot / 22 scene)
> + thư mục ảnh đã tải `C:\Users\tuana\Downloads\Sep 09 - 22_34` (102 file).
> Viết 2026-09-10. Selector/nhãn trong đây **đã dò trên tab thật**, không phải đoán.

## 0. ĐƠN VỊ DEMO: 1 SCENE = 3 SHOT = 3 CLIP = 24 giây

Flow tự nhóm **3 shot / 1 scene** và đếm `0/3 ANIMATED` trên thẻ scene. Nên "1 video demo"
đúng nghĩa nhất = **animate hết 3 shot của MỘT scene rồi nối lại**.

| | |
|---|---|
| Chọn demo | **SCENE 01 — Int. Bright Living Room - Day** (Katsuo phát hiện khoản 360.000) |
| Số clip | **3** (mỗi clip 8,000s) → **24 giây** |
| Giá | **3 × 100 credits = 300** ở `Veo 3.1 - Quality` · rẻ hơn nhiều ở `Veo 3.1 - Lite` |
| Vì sao SCENE 01 | nó là **cold open** — đoạn quyết định retention, và tự nó đã là một mạch truyện trọn vẹn (thấy sổ → nhìn số → sững người) |

⛔ **Đừng gen cả 66 shot.** 66 × 100 = **6.600 credits** ≈ nửa tháng credit của gói Ultra.
Xem §7 trước khi nghĩ tới chuyện đó.

---

## 1. CHUẨN BỊ THANH PROMPT (làm 1 lần, không phải mỗi shot)

Mở project Flow → nhìn thanh prompt dưới cùng.

**① Tắt chế độ AGENT nếu đang bật.**
Dấu hiệu đang bật: thanh prompt **KHÔNG có** chip `Video · … · 8s` và **KHÔNG có** 2 ô
`Start` / `End`; thay vào đó có `Agent instructions` + nút bánh răng `Settings`.
→ Bấm chip **`Agent`** để tắt. Bật lại đúng thanh cổ điển thì sẽ thấy:

```
[ Start ]  ⇄  [ End ]
What do you want to create?
[Agent]              Video · 720p · 8s ▭ x1   →
```

🔴 Ở chế độ Agent **không làm được i2v** — không có slot frame nào để đính ảnh.

**② Bấm chip `Video · … · 8s ▭ x1` (Settings trigger) → chọn:**

| ô | chọn | vì sao |
|---|---|---|
| hàng 1 | **`Video`** | không phải Image |
| hàng 2 | **`Frames`** | 🔴 **KHÔNG chọn `Ingredient`** — xem §6 bẫy ① |
| hàng 3 | **`16:9`** | |
| độ phân giải | **`720p` trở lên** | 🔴 mặc định đang là **360p** — không dùng được cho YouTube |
| model | `Veo 3.1 - Lite` cho demo · `Quality` cho bản thật | Lite rẻ hơn; demo là để xem cơ chế, không phải để đăng |
| số bản | **`x1`** | x2 = trả tiền gấp đôi |

Dòng cuối popover ghi thẳng **`Generating will use N credits`** — đọc số đó trước khi bấm gì.

---

## 2. BA SHOT CỦA SCENE 01 — copy-paste trực tiếp

Tên asset dưới đây **ghép bằng MD5** giữa ảnh trong export và ảnh bạn đã tải về
(khớp **66/66**, không phải đoán tên).

### SHOT 1/3 — `Man sitting at table`
```
Katsuo sits at the low wooden table and slowly lowers his eyes to the passbook in his hands, then his shoulders settle. Keep the framing, composition, characters, clothing, props and colours of the given image exactly as they are; the camera stays locked off and does not move, no zoom, no pan, no cut to another shot. Only what is described above moves, once, slowly, and it holds still for the rest of the shot. Any printing on paper or screens stays exactly as in the image; no new text appears, no captions, no watermark, no logo.
```

### SHOT 2/3 — `Man staring in shock`
```
Katsuo holds the stunned expression, only breathing and blinking, then he swallows once and his eyes stay on the page. Keep the framing, composition, characters, clothing, props and colours of the given image exactly as they are; the camera stays locked off and does not move, no zoom, no pan, no cut to another shot. Only what is described above moves, once, slowly, and it holds still for the rest of the shot. Any printing on paper or screens stays exactly as in the image; no new text appears, no captions, no watermark, no logo.
```

### SHOT 3/3 — `Man holding bank passbook`
```
The grip of both hands on the passbook tightens slightly, then the edge of the page lifts a little and settles again. Keep the framing, composition, characters, clothing, props and colours of the given image exactly as they are; the camera stays locked off and does not move, no zoom, no pan, no cut to another shot. Only what is described above moves, once, slowly, and it holds still for the rest of the shot. Any printing on paper or screens stays exactly as in the image; no new text appears, no captions, no watermark, no logo.
```

⚠️ **Shot 3 có tên TRÙNG với shot đầu của Scene 02** — cả hai đều là `Man holding bank passbook`
(bản tải về của shot 3 mang đuôi ` 2` do trùng tên file). Nên khi search sẽ ra **2 kết quả**.
→ **Chọn bằng THUMBNAIL/preview trong hộp thoại**, đừng bấm bừa hàng đầu. Ảnh đúng của Scene 01
là bản **cận hai tay giữ sổ, hậu cảnh phòng khách mờ**; bản của Scene 02 sáng hơn và chặt hơn.

📌 **Vì sao prompt chỉ tả CHUYỂN ĐỘNG, không tả cảnh:** i2v khoá nguyên khung ảnh bạn đã duyệt.
Tả lại quần áo/bối cảnh = đưa **hai nguồn mâu thuẫn** cho model, nó trộn lại. **Ảnh lo hình dạng,
chữ lo hành động.**

📌 **Vì sao bỏ hết chuyển động máy:** Flow tự soạn `motionDescription` và nhét sẵn
`a slow gentle zoom-in` / `a subtle pan` / `rack focus` vào **cả 3 shot** — chọi thẳng với câu
`the camera stays locked off` ở đuôi. Chọn một: hoặc máy khoá (bản trên), hoặc máy động thì
phải **bỏ** câu locked-off. Đừng để cả hai.

---

## 3. LÀM TỪNG SHOT — 6 bước, ~1 phút/shot

1. Bấm ô **`Start`** trong thanh prompt → mở hộp thoại **`Select a frame image`**.
2. Gõ **tên asset** vào ô `Search assets`.
3. Danh sách còn **đúng 1 hàng** → bấm vào hàng đó (preview hiện bên phải — **soi cho đúng ảnh**).
4. Bấm **`Add to prompt`**.
   ✅ Đúng: chip ảnh hiện ở slot `Start`, **không có** dấu ⚠/error.
   🔴 Sai: chip **mờ + có icon lỗi** ⇒ đang ở mode `Ingredient`, quay lại §1 ②.
5. Dán **prompt** vào ô `What do you want to create?`.
6. Nút **`→` (`Start generation`)** sáng lên → bấm. Chờ 1–3 phút.

Xong shot 1 thì lặp cho shot 2, shot 3. Thẻ scene sẽ đổi `0/3` → `1/3` → `2/3` → `3/3 ANIMATED`.

⛔ **Không bấm `→` hai lần cho một shot.** Mỗi cú bấm = một lần trừ credit. Nút mờ lại + ô prompt
sạch = đã gửi rồi, đang chạy.

---

## 4. TẢI VỀ + NỐI THÀNH VIDEO DEMO

Tải 3 clip về **theo đúng thứ tự shot 1 → 2 → 3**, đặt tên `s01_1.mp4`, `s01_2.mp4`, `s01_3.mp4`
vào một thư mục, rồi:

```bash
cd <thư mục chứa 3 clip>
printf "file 's01_1.mp4'\nfile 's01_2.mp4'\nfile 's01_3.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy demo_scene01.mp4
```

⚠️ `-c copy` chỉ chạy khi 3 clip **cùng codec/khổ/fps** — clip Flow cùng lô thì cùng hết.
Nếu ffmpeg báo lỗi, đổi thành `-c:v libx264 -crf 18 -preset veryfast`.

📌 Clip Veo là **8,000s @ 24fps** → demo ra **24,0s**. Nếu sau này ghép vào Remotion thì
project phải để `fps: 24`; ép 30 sẽ **lặp 27% frame** = video rung giật.

---

## 5. NGHIỆM THU — 3 phép, làm hết đừng bỏ

1. **Sheet 4 frame/clip** (0,5s · 2,6s · 5,0s · 7,4s), không phải 1 frame.
   > Lý do: 24 clip lỗi của showa video 10 **đều qua** sheet 1 frame và chỉ lộ ở sheet 4 frame.
2. **Soi đúng 3 lỗi Veo hay mắc ở kênh này:**
   - vật **đổi trạng thái rồi quay lại** (sổ mở → đóng → mở)
   - **thao tác chạy ngược** thứ tự prompt
   - **chữ trên giấy tự sinh ra** (Veo không viết được tiếng Nhật — 0/6 clip đúng)
3. **Khung có bị trôi không** — prompt đã yêu cầu máy khoá, nên frame đầu và frame cuối phải
   cùng bố cục. Trôi = model bỏ qua câu locked-off, cần viết lại prompt gọn hơn.

---

## 6. BỐN BẪY ĐÃ DÍNH THẬT — đọc trước khi mất credit

**① `Ingredient` ≠ `Frames`.** Cùng một ảnh: ở mode `Ingredient` chip ra **mờ + icon error**
(dù ảnh load hoàn hảo) = Flow **từ chối** nó; đổi sang `Frames` thì chip sạch và hiện `Start ⇄ End`.
`Ingredient` dành cho ảnh nhân vật/tham chiếu, **không** nhận ảnh frame.

**② Submit khi slot ảnh RỖNG vẫn chạy được** — và Flow trả về **video text-to-video thường**:
tốn credit, ra sai loại video, **không một dấu hiệu lỗi nào**. Luôn xác nhận chip có mặt trước khi bấm.

**③ Trong trang có HAI ô search.** Ô ở đỉnh trang (lọc thư viện) và ô trong hộp thoại
`Select a frame image`. Gõ vào ô trên cùng thì hộp thoại **không lọc gì**, rồi bạn bấm hàng đầu =
**đính sai ảnh** mà prompt vẫn đúng ⇒ clip ra sai người.

**④ Đang là 360p.** Chip mặc định `Video · 360p · 8s` — gen xong mới phát hiện thì mất cả lô.

---

## 7. KHI MUỐN LÀM CẢ VIDEO (66 shot) — đọc trước khi quyết

| | số |
|---|---|
| 66 shot × 8s | **8,8 phút** hình |
| 66 × 100 credits | **6.600** (Quality) |
| Gói Ultra ~12.500/tháng | ≈ **½ tháng** cho một video |

Ba cách hạ giá, theo thứ tự nên làm:
1. **Chạy `Veo 3.1 - Lite`** cho những shot chỉ có vi-chuyển-động (thở, nháy mắt, tay lắng) —
   phần lớn shot của bài này thuộc loại đó.
2. **Triage:** shot nào prompt chỉ là *"giữ tư thế, thở, nháy mắt"* thì **không cần Veo** —
   `python Projects/_media_library/animate_still.py <ảnh> --out clip.mp4 --dur 8` làm **miễn phí**,
   khung đứng yên + động cục bộ, và có gate tự đo (MAD > 3, dịch khung < 1px).
3. **Gen theo SCENE, đọc kết quả từng scene** — đừng bắn cả 66 rồi mới xem.

⛔ Và trước khi gen lô lớn: **duyệt lại `visualDescription`/`motionDescription` do Flow soạn**.
Đo trên bản demo trước: **6/7 shot** bị Flow tự thêm chuyển động máy hoặc tự đổi sang framing
**chỉ-có-tay** (thứ đo được là **14/21 clip hands-only bị hỏng** ở kênh showa).

---

## 8. NẾU MUỐN CHẠY BẰNG TOOL THAY VÌ BẤM TAY

➡️ **Hướng dẫn riêng, đầy đủ + bảng tool-làm-được-gì:**
`Projects/youtube-jp-showa/tools/flow_batch_ext/HUONG_DAN_CHAY_TOOL.md`

Ba việc tool **KHÔNG** làm, vẫn phải tay: **đặt 720p** · **chọn model** · **tải clip về**.


Extension `Projects/youtube-jp-showa/tools/flow_batch_ext` (v2.4) làm đúng chuỗi §3, tự động:
tab **v2 · ẢNH → VIDEO** → **⚙ CHỐT SETTINGS** → nạp `jobs.jsonl` → **DRY-RUN** → START.

Sinh `jobs.jsonl` cho 3 shot của Scene 01:
```bash
python Projects/youtube-jp-nenkin/tools/story_extract.py \
  "C:/Users/tuana/Downloads/PENSION RESEARCH LAB_ THE TWO PAYMENTS - 2026-09-10_00-29.json" \
  "Projects/youtube-jp-nenkin/06_VIDEO/_demo_i2v/pension" \
  --dl "C:/Users/tuana/Downloads/Sep 09 - 22_34" --scenes 01
```
`--dl` là chỗ ghép tên asset bằng **MD5** (chính xác 100%, thay cho phép đoán theo chữ).

⚠️ Tool và Claude-in-Chrome **không dùng chung một tab được** (`chrome.debugger` độc quyền).
Và extension chỉ thấy tab **cùng Chrome profile** với nó — nạp ở đúng profile của account Flow.

---

## 9. TÓM LẠI — 8 việc

```
1. Mở project Flow, tắt Agent nếu đang bật
2. Settings: Video + Frames + 16:9 + 720p+ + x1 + model
3. Shot 1: Start → search 'Man sitting at table' → Add to prompt → dán prompt → bấm →
4. Shot 2: 'Man staring in shock'
5. Shot 3: 'Man holding bank passbook'   ← có 2 kết quả, chọn bằng preview
6. Tải 3 clip theo thứ tự
7. ffmpeg concat → demo_scene01.mp4 (24s)
8. Sheet 4 frame/clip, soi 3 lỗi ở §5
```
