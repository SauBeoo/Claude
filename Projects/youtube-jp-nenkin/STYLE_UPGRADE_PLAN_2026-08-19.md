# KẾ HOẠCH — nội dung card xuất hiện kiểu りょう (chốt style, 2026-08-19)

> User yêu cầu: giữ **khung sân khấu nenkin** (nền navy + 2 nhân vật + card giữa + dải phụ đề),
> nhưng **nội dung TRONG card** xuất hiện theo phong cách video mẫu
> `https://www.youtube.com/watch?v=6DN88wQyBFg` — 節約看護師りょう,
> 「【知らないと大損】2026年からは〇〇歳が最強！…受給開始年齢…」, 35′49, **970K view**.
> Thay いらすとや bằng **ảnh AI gen** (user gen, Claude viết prompt).
> ⚠️ Đây là chép **cơ chế xuất hiện**, không chép bố cục nguyên con.

## 1b. NHỊP ĐO BẰNG MÁY (file local, beat sheet 1fps đoạn 2:20–3:20 + 4 contact sheet toàn video)

- 1 thẻ sống **6–14s**, trong thẻ có **2–4 lần pop**, khoảng cách **3–6s/pop** — phần tử hiện đúng lúc lời đọc chạm ý, KHÔNG lắp hết trong 2s đầu rồi đứng im.
- Mỗi thẻ có 1 cú **PUNCH**: bong bóng TRÒN đặc màu (xanh đậm/đỏ) chứa số 「最大24%減」「44万円減少」 pop-scale vào — điểm nhấn của thẻ.
- **Color coding học 1 lần dùng cả bài**: 繰り上げ=CAM · 繰り下げ=XANH LÁ, giữ suốt 36 phút.
- Trục tuổi/banner **giữ nguyên làm nền** khi ý mới hiện; thẻ cũ được **gọi lại nguyên trạng** khi lời đọc quay lại (3:08 lặp đúng bảng của 2:29) — khớp cơ chế `pre`/`held` sẵn có.
- Từ vựng hình toàn video: banner đỏ mục lớn · checklist ✔ đỏ · timeline trục tuổi + vùng fill · line chart 損益分岐点 · bảng to có khung đỏ highlight từng vùng · thẻ tối/moody cho beat cảm xúc · panel màu label + illustration to · 原典 screenshot kèm link · bong bóng thoại từ nhân vật · persona đứng góc phải bình luận.
- Video mẫu **không burn phụ đề** — chữ to trên màn thay phụ đề. Nenkin GIỮ dải phụ đề như cũ (khung không đổi theo yêu cầu user).

## 1. CÁI ĐO ĐƯỢC TỪ VIDEO MẪU (soi frame 120s · 300–304s · 620s)

| # | Cơ chế | Chi tiết đo được |
|---|---|---|
| 1 | **Headline hiện TRƯỚC, đứng một mình** | t=300s: chỉ có headline trên khung trắng, phần dưới TRỐNG — chờ lời đọc chạm ý mới hiện tiếp |
| 2 | **Khối nội dung pop vào LẦN LƯỢT theo lời đọc** | t=304s: 2 panel navy đã pop vào dưới headline (cách nhau ~1–2s), mỗi panel = label + hình |
| 3 | **Keyword tô màu NGAY TRONG câu** | headline đen + cụm đắt màu ĐỎ (「いつ受け取るか」「年金が1円も貰えない」); label trên nền navy thì keyword VÀNG (「切り崩す」「寿命は違う」) |
| 4 | **HÌNH là nhân vật chính, không phải icon** | hình chiếm ~60–70% diện tích panel; heo đất khóc + tiền vỡ, cặp vợ chồng già lo lắng — hình chở CẢM XÚC, chữ chỉ 5–8 ký |
| 5 | **Mật độ thấp** | mỗi màn: 1 headline + 1–2 khối. Có màn chỉ 1 hình to giữa khung (cái cân + đồng xu, t=120s) |
| 6 | **Không camera** | zero pan/zoom — chỉ build-on. Đúng triết lý make_stage hiện tại |

## 2. STAGE HIỆN TẠI — có gì / thiếu gì

**Đã có sẵn (không đụng):** sân khấu cố định + build-on (`app`/`app_fly`/`blend`, RISE 26px,
APP 0.42, PACE 1.35) · sync cue theo `match` · resume `.sig` · sổ `_MISSING_ART.json` ·
layout `zu` + 13 gate · palette kênh.

**Thiếu 3 thứ để ra chất りょう:**

| Thiếu | Hiện trạng | Cần |
|---|---|---|
| **Layout hình-là-chính** | ảnh chỉ là `fill` góc 390×316, hoặc layout `art` 940×588 đơn lẻ; các layout chữ (check/zu/big) hình là phụ | 2 layout mới: `pict` (1 hero art giữa card + caption) và `panels` (1–3 panel navy label-vàng + art, pop lần lượt) |
| **Keyword màu inline** | `title()` vẽ 1 màu navy duy nhất | marker trong text (`《…》` → đỏ trên nền sáng / vàng trên navy), đo bề rộng từng run bằng `getlength` (LUẬT SỐ 1: đo, không đoán) |
| **Nhịp pop theo LỜI ĐỌC** | mốc t0 là hằng cứng trong layout (0.72 / 1.12…) | khoá `beats: [giây]` trong spec — builder tính từ timing TTS/srt của cue; thiếu thì fallback nhịp đều như cũ |
| **Tỉ lệ hình/video** | video 14: **5/66 entry có ảnh** (7,6%) — còn lại là chữ + sơ đồ | nhắm **≥60% thẻ có hình** (≈35–45 ảnh/video) |

## 3. KẾ HOẠCH THI HÀNH

### ✅ GĐ1 ĐÃ XONG 2026-08-19 — `make_stage.py` (KHÔNG bump VERSION: thẻ cũ giữ nguyên sig)

Đã cài 4 cơ chế, demo chạy thật ở `06_VIDEO/_demo_pict/` (mp4 + `_stage_sheet.jpg`):

| Cơ chế | Cách dùng trong spec | Ghi chú |
|---|---|---|
| **Keyword màu inline** | marker `《…》` trong `title` / `cap` (art·big·pict) / `label` panel | nền sáng → đỏ `KW_ON_LIGHT` · panel màu tối → vàng `KW_ON_DARK`. Text không marker đi đường vẽ cũ từng byte |
| **Layout `pict`** | `{"layout":"pict","panels":[{"label","img","tone"}], "cap"}` — 1–3 panel | tone: navy(mặc định)/red/green/amber/paper. Label tự ĐỒNG CỠ giữa các panel. Hỗ trợ `pre` như check |
| **Pin `badge`** | `{"kind":"badge","t":"最大\n24%減","at":[x,y],"tone":"blue/red/green/navy/amber","r":0.155,"beat":5.0}` | punch tròn đặc màu kiểu りょう — **1 badge/thẻ**, nhiều là loãng |
| **Nhịp `beats`** | `"beats":[giây,…]` (check=từng dòng · big=[hero,cap,note] · art=[ảnh,cap] · pict=[panel…,cap]) · pin dict có `"beat":giây` riêng | GIÂY THẬT tính từ đầu clip; thiếu khoá → nhịp dồn cũ. Gate mới trong `cmd_slides`: beats vượt trần `--sec` → 🔴 |

An toàn đã kiểm: ① spec không marker/beats render y hệt cũ ② `_sig` thêm quét ảnh NESTED (`panels[].img` + `pins[prop].img` — vá luôn lỗ sig cũ của prop) nhưng giữ nguyên thứ tự phần cũ → video 13/14 **không thẻ nào bị vô hiệu sig oan** (đã quét: 0 nested img) ③ sổ `_MISSING_ART` đếm thêm `panels[].img` cùng lượt (luật §1.5 phái sinh).

**Nhịp khuyến nghị khi builder ghi beats (từ số đo りょう):** phần tử cách nhau **3–6s**, headline luôn đứng một mình ~2–3s đầu, badge rơi đúng giây giọng đọc nói con số. Cue của thẻ phải dài ≥ beat cuối + 1,5s.

**🔴 HAI LUẬT rút từ vòng duyệt demo đầu tiên (user bắt 2026-08-19):**
1. **Ảnh panel/art phải là ảnh CHỦ THỂ choán khung (STYLE_MACRO)** — ⛔ cấm lấy ảnh họ `bg_*` (chủng ảnh gen làm NỀN NHẠT theo §2.10 ④, cố ý LOW CONTRAST + chừa trống) đưa vào panel: panel sẽ trống hoác. Ca gốc: demo clip_01 dùng `bg_60man.png` → user: *"ảnh này trống quá"*.
2. **Pin trỏ-vào-ảnh (`circle`/`arrow`/`zoom`) chỉ đặt SAU khi ảnh đã về và soi mắt** — đặt trước theo toạ độ bịa là khoanh vào không khí (ca gốc: demo clip_02, user: *"tự dưng khoanh đỏ làm gì?"*; cùng bệnh với §2.11 "pin trỏ vào không khí"). Lúc builder viết SLIDES trước khi có ảnh: chỉ dùng `badge` (không phụ thuộc nội dung ảnh); pin trỏ-ảnh thêm ở vòng duyệt sau khi gen.

**⚠️ PROMPT ẢNH CHO PANEL `pict` — KHÁC luật ảnh full-khung:** panel 2 cột chỉ rộng ~420px trong khi ảnh gen ra 1376×768 → cover-crop **cắt bỏ ~2/3 bề ngang, giữ GIỮA**. Vậy ảnh cho panel: **chủ thể ĐỨNG GIỮA khung, bố cục DỌC được ưu tiên** — ngược với luật "85% bên trái" của ảnh full (`media-library.md` §2.10 ③ vẫn đúng cho layout `art`/`bgimg`, đừng trộn). Watermark ✦ ở góc phải ảnh gốc sẽ bị crop 2 cột tự cắt mất, nhưng panel 1 cột (rộng ~580px) thì KHÔNG — vẫn phải qua bước xoá ✦ như mọi ảnh.

### GĐ1 (kế hoạch gốc, đã thi hành như trên)
1. `title()` + `tw()` hỗ trợ marker keyword màu (`《…》`).
2. Layout **`pict`**: headline → 1 hero art to giữa card (max ~860×520, cover-crop) → caption dưới. Nhịp: headline t=0, art pop t≈beats[0], caption t≈beats[1].
3. Layout **`panels`**: headline → 1–3 panel navy bo góc, mỗi panel = label (keyword vàng) + art; pop lần lượt theo `beats`. 2 panel = so sánh (thay được nhiều ca `compare`), 1 panel = nhấn.
4. Khoá `beats` đọc ở mọi layout mới; `_pop` (phóng to) dùng cho art hero cho có lực.
5. 🔴 **Luật phái sinh render-background §1.5:** khoá art mới (`pict.img`, `panels[].img`) phải vào tập `want` của `_MISSING_ART.json` **cùng lượt sửa** + vào `_sig`.

### GĐ2 — style-lock ảnh AI (thay いらすとや)
1. Viết **STYLE string chung** cho cả kênh: flat illustration senior JP, nét dày, nền trắng/kem phẳng, palette khớp stage (navy/amber/đỏ/xanh của `channels.py`), nhân vật ông bà 60–70 biểu cảm rõ. 2 biến thể: `STYLE_SCENE` (người + tình huống) / `STYLE_MACRO` (vật: phong bì, sổ, tiền — vật FILL khung, media-library §2.11).
2. Prompt xuất theo chuẩn cũ: bảng người đọc trong script + `art_prompts_FLOW.txt` 1 dòng/prompt (user bơm extension). Chủ thể trong **85% bên trái**, đè cỡ bằng quan-hệ-mép-khung, `no watermark` + ô giấy tờ để trống (media-library §2.10).
3. Ảnh về → ingest 1 lệnh: đổi tên + **cắt ✦ theo lô** (đo mắt 5–8 mẫu trước, hằng số theo lô — máy đo đã fail 4/4) + crop đúng tỉ lệ slot. Mẫu: `tools/ingest_art_12.py`.
4. Ảnh flat illustration = không realistic → không đổi trạng thái tick synthetic hiện tại của kênh.

### ✅ GĐ3 ĐÃ ÁP VÀO VIDEO 14 (2026-08-19, user chốt "áp vào video 14 đi")

- **make_stage:** `beats` nối thêm vào `L_zu` (map lên node theo thứ tự, edge tự theo) và `L_compare` (beats[0..1]=panel, [2..]=row). Công thức end của L_zu đổi thành `max(t0s)+0.74` — trùng từng số với công thức cũ khi không beats.
- **builder `build_slides_14.py`:** ① **AUTO-BEATS** — mọi thẻ ≥2 phần tử được gắn `beats` ước từ hệ số 5,72 ký/giây, mốc BÁM ĐẦU DÒNG gần nhất (dòng ≈ ý ≈ lời đọc), trải 1,6s → cuối cue −0,5s, bước ≥0,8s; thẻ ghi beats tay thì auto nhường ② 4 thẻ chuyển đổi: compare 2通知書 → **pict 2-panel xanh/đỏ** (số vào label) · cols3 この線に触れるかた → **pict 3-panel người** · zu なんだ5千円 → **pict 1-panel paper** · zu 渡辺ひとこと → **art** (quote lên title) ③ **15 keyword màu 《…》** vào title/cap ④ gate pict (trần ký label theo bề rộng panel thật, panel không img = lỗi) ⑤ danh sách ảnh in cuối builder gộp cả `panels[].img`.
- **Kết quả:** 66 thẻ · 15:43 · nhịp 4,20 đổi hình/phút · layout {art 6 · pict 3 · zu 28 · big 10 · check 11 · source 5 · compare 2 · steps 1} · gate builder PASS · `check_zu_layout` ✅ SẠCH 13/13 · still 66 thẻ đã dựng.
- **Ảnh chờ (12):** 9 AI (prompt ở `06_VIDEO/14_…/art_prompts_FLOW.txt`, 9 dòng — 2 dòng đầu giữ nguyên prompt cũ) + **3 genten là SCREENSHOT trang thật + khoanh đỏ, KHÔNG gen AI** (nenkin.go.jp · mhlw.go.jp · city.joetsu).
- Thẻ có hình sau lượt này: 15 thẻ mang hình (art 6 + pict 3 với 6 panel-ảnh) — chưa tới mốc 60% của plan gốc, là chủ ý: giữ nguyên lớp `zu` 28 thẻ (xương sơ đồ vừa qua 6 vòng sửa), nhịp beats mới phủ **100% thẻ**, hình tăng dần ở video sau.

**🔴 Vòng duyệt 2 (user bắt 2 lớp lỗi trên still, 2026-08-19 tối) — sửa ở TẦNG TOOL, bump `stage-1.3`:**
1. **Node `label` của zu giả định chữ 1 DÒNG** — khuôn `line()` mới dùng label 2 dòng (「去年\n147万円」) → khung bao dòng 1, dòng 2 lòi ra. Vá: `_zu_extent` đo cao theo số dòng + ngang theo dòng DÀI NHẤT; draw dùng `fit_ml`/`tw_ml`; đường 1 dòng giữ nguyên từng số → thẻ cũ không đổi pixel. Dính 6 thẻ `line()`.
2. **`L_source` vẽ `org` bằng cỡ cứng 46, không fit** → org dài tràn mép phải khung vàng (clip_24 「新潟県上越市（掲載日…）」); và hộp cao cứng 330 trong khi doc 3 dòng chạm đáy. Vá: org `fit()` theo bề rộng thật + hộp cao theo số dòng doc + note bám đáy hộp mới.
⚠️ Builder gate không bắt được cả hai vì chúng là lỗi **VẼ** (trần ký tự đều qua) — đúng loại chỉ lộ khi soi 1:1 (`stage-zu-layout.md` §6). Sau vá: gate 13/13 vẫn SẠCH, 66 still dựng lại đã soi các thẻ dính.

### GĐ3 (kế hoạch gốc — đã thi hành như trên)
1. Sửa builder SLIDES video 14: chuyển ~60% thẻ sang `pict`/`panels` (giữ `zu` cho sơ đồ cơ chế, `source` cho 原典, `big` cho số đắt — りょう cũng có frame kiểu đó).
2. `--still --force` → duyệt sheet + soi 1:1 → viết prompt → user gen → ingest → dựng **demo mp4 1–2 phút** cho user nghe/nhìn nhịp pop theo giọng → OK mới dựng cả bài.
3. Gate giữ nguyên: `check_zu_layout` cho thẻ zu · trần ký tự §2.1 audience-45plus · sổ thiếu ảnh chặn render.

## 4. ĐÁNH ĐỔI, BIẾT TRƯỚC
- **Công gen ảnh tăng ~7×** (5 → 35-45 ảnh/video). Extension bơm FLOW.txt gánh được, nhưng vòng duyệt ✦ + soi kanji cũng tăng theo.
- **Không vứt lớp `zu`**: 13 gate vừa xây xong (2026-08-17/18) vẫn là xương của phần cơ chế; りょう style chỉ thay các thẻ **liệt kê/cảm xúc/tình huống** — đúng chỗ check/big đang trống mực (đo 4,2%).
- Nhịp pop trong 1 thẻ **không tính là đổi hình** (gate ≤6 đổi hình/phút đo ở mức thẻ) — nhưng đừng vì thế nhét 6 khối/thẻ; trần 3 khối như りょう.
