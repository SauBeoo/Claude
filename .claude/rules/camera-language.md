# NGÔN NGỮ MÁY QUAY cho video AI — góc · chiều cao · cỡ cảnh · lia

> **Nguồn sự thật DUY NHẤT** về cách ra lệnh máy quay trong prompt t2v (Veo/Flow · i2v · ảnh→Animate). Chốt 2026-09-21.
> Nguồn: ① bảng góc quay user cấp (ngữ pháp phim — §2, §4) ② ⭐ đo 108 frame + 10 cặp frame của 3 video 141–196K `昭和の記憶`
> (§1, §3, §5, §7 đến từ đây). Phạm vi: **showa** (§9). Đọc cùng `ai-video-regen.md` · `media-library.md` §2.10 · `audience-45plus.md` §2.
> Bản thi hành: `Projects/youtube-jp-showa/tools/gen_demo16_kioku.py` · `tools/videogen_lib.py`.

## 0. NGUYÊN TẮC GỐC

1. **Máy quay là một NHÂN VẬT.** Nó đứng ở đâu, cao bao nhiêu = *ai đang kể*. Ở mẫu, máy không bao giờ ở tầm người đứng quan sát: ngồi bệt cạnh đứa trẻ, ngồi vào chỗ trống ở bàn, ngồi ghế tàu.
2. **Prompt điều khiển được VỊ TRÍ và HƯỚNG, rất kém ở TỈ LỆ và CỠ** (đã đo 3 lần). Lệnh về cỡ phải nói bằng **quan hệ với MÉP KHUNG** hoặc vật trong cảnh, không nói phần trăm.
3. 🔴 **NEGATIVE KHÔNG THẮNG TOKEN PHONG CÁCH — phải BỎ token** (§7.1).

## 0.5 ⭐⭐⭐ ĐẢO 2026-09-22 — showa: MÁY ĐỨNG / TRÔI MỘT BƯỚC, không "luôn động"

> user: *"video này rất thật, video của tôi ảo quá"* (mẫu 異世界さんぽ, cùng Veo) → *"di chuyển mượt, dịu dàng êm"* → *"áp dụng… cả showa"*.

| | mẫu | lô 109 clip showa 16 theo §4 | vòng 3 công thức mới |
|---|---|---|---|
| MAD trong shot p50 | **1,5** | 9,4 | 2,3–7,9 |
| % diện tích khung đang động | **10%** | **87%** | 10–34% |
| tốc độ phần động | **14 px/s** | 37 | 14–16 |
| shot có máy di / mức di | **32%** · trôi 8–10 px/s, zoom 3–8%/shot | 95% · tới 1000 px/8s | 33–67% |

🔴 **"Êm" = ÍT thứ động + động CHẬM.** Máy đứng hoặc trôi đúng một bước trong 8s; chỉ người và vật họ chạm mới động. Khối `never comes to rest` + `HANDHELD` + walk 100–300px (§4) làm cả khung bơi = "ảo". §4.1 vẫn đúng khi cần một cú di thật, nhưng **không còn là mặc định**.

**Thi hành:** khối chung `Projects/_media_library/realism_blocks.py` — `LOCKED_CAM` 2/3 cảnh · `DRIFT_CAM` 1/3 · `LIGHT` một nguồn (ban ngày **nắng vàng**, ⛔ không "muted": mốc sáng trung bình trộn ngày–đêm làm ảnh xám) · `SUBJECT_GENTLE` · `SILENT_REALTIME` · **ảnh Nano Banana → ⋮ Animate** thay t2v thuần. Thế giới showa = **昭和 thật, cổ điển, ⛔ không viễn tưởng**.
Gate hậu gen `check_realism.py`: MAD p50 ≤3 · khung yên ≥20% (cảnh khoá) · ≤40% shot di và di phải là trôi nhẹ · cháy ≤1% · diện tích động ≤25% · tốc độ ≤22 px/s.
§1–3, §5, §5.1, §6.2, §6.6–6.8, §7.1, §7.4 **giữ nguyên** làm xương.
⚠️ Còn mở: cháy trắng 3–6% cảnh nắng · i2v tự trôi 2–6% ở cảnh khoá. 🛑 Phanh: 3 video chạy khuôn này mà AVD tụt → trả §4.

---

## 1. ⭐ CHIỀU CAO MÁY — mục quan trọng nhất

| chiều cao | token EN | khi nào |
|---|---|---|
| **ngang tầm chủ thể** ⭐ mặc định | `the camera at their own eye height` | đối thoại/trao đổi |
| **tầm ngồi tatami ~50cm** ⭐ | `the camera down at their own seated height on the floor` | 茶の間 · ちゃぶ台 · futon · hiên |
| **tầm mặt bàn** ⭐ | `the camera at the level of the tabletop itself, close enough to reach the dishes` | bàn ăn, bàn học, quầy |
| tầm mắt trẻ con | `the camera at a child's eye height` | trẻ con là chủ thể |
| tầm đứng (ngực) | `the camera at chest height` | ⚠️ mặc định của công cụ và là mặc định SAI — máy thành người ngoài |
| sát đất | `the camera almost on the floor, looking along it` | vật dưới sàn |
| trên cao | `the camera above head height looking down over them` | đám đông |

🔴 **Chiều cao máy = tư thế người trong cảnh.** Họ ngồi thì máy ngồi (107/108 frame mẫu tuân).

### 1.1 ⭐⭐ MÁY ĐỨNG Ở CHỖ CỦA AI

Mỗi prompt khai **một chỗ NGƯỜI đứng được**, dán ngay sau khối chiều cao:
```
the camera stands exactly where <a fourth person at the table / someone sitting beside him on the
veranda / a relative walking in with the children> would be standing, at that person's own height,
and everything is seen from that one place
```
Thiếu nó, t2v chọn chỗ không ai đứng được (giữa mặt bàn, trong tường) ⇒ khung đọc ra "máy bay". Kèm lợi phụ: vai/đầu người khác lấn mép khung = `dirty foreground` miễn phí.

---

## 2. GÓC QUAY

| góc | token EN | dùng để | ⚠️ t2v |
|---|---|---|---|
| **Ngang tầm mắt** ⭐ | `a straight-on shot at their own eye height` | trung lập, đối thoại | an toàn nhất |
| Thấp | `a low angle from below them, looking up` | uy quyền / tầm trẻ con nhìn người lớn | hay méo mặt |
| Cao | `a high angle from above them, looking down` | nhỏ bé, cô đơn | ghi "slightly" kẻo thành bird's-eye |
| Top-down | `a top-down shot looking straight down from directly above` | flatlay | hai bóng đổ chọi nhau, người dẹt |
| Dutch tilt | `the whole frame tilted a few degrees off level` | bất an | tự chỉnh thẳng giữa clip |
| **Qua vai (OTS)** ⭐ | `over the shoulder from just behind them, the back of their head and one shoulder filling the near corner` | đối thoại 2 người | ⭐ cách an toàn nhất quay CẬN VẬT mà không rơi vào `hands only` |
| **POV** ⭐ | xem §6.3 | nhập vai, nhìn ra cửa sổ | hỏng 14/21 clip nếu đòi thấy tay mình |
| **3 phần tư** ⭐ | `seen in three-quarter profile, their face clearly visible but never turned towards the camera` | tư liệu | câu chống "nhìn ống kính" |
| Sau lưng | `seen from directly behind them at their own height` | "đi cùng họ", giấu mặt | ⭐ chống trôi mặt giữa clip |
| **Xuyên khung** ⭐ | `shot from inside the dark room looking out through the open doorway at the bright daylight` | vào/ra, hé lộ | cú đắt nhất ở mẫu |
| **Tiền cảnh bẩn** ⭐ | `shot past an out-of-focus object in the near foreground that fills one side of the frame` | 3 lớp sâu | thay được `hands only` |
| Silhouette | `their figures dark against the bright sky behind them` | chiều tà, kết đoạn | ghi "shadows still hold detail" |

⛔ Không dùng ở kênh senior: dutch tilt · bird's eye · góc thấp cực đoan.

---

## 3. ⭐ CỠ CẢNH

| cỡ | token EN | ở mẫu |
|---|---|---|
| EWS | `a very wide shot, the figures tiny in the landscape` | chỉ đoạn đi đường/chơi ngoài đồng |
| WS | `a wide shot, the whole figure in frame with the room opening away behind` | ~11% |
| **MS** ⭐ | `a medium shot, the figure from the knees up` | chủ lực |
| **MCU** ⭐⭐ | `a close shot, the two of them filling most of the frame from the chest up` | chủ lực thân bài |
| CU | `a close-up of their face and shoulders` | ít |
| ECU | `an extreme close-up of just their hands and the object` | ⛔ CẤM (= `hands only`) |

🔴 Thân bài là **MCU/MS**, không phải WS. **BỎ `respectful distance`** (đẩy mọi cảnh về WS) → `close enough to reach the table` / `near enough that the two of them fill most of the frame`.
📌 ~29% frame mẫu **không có người** (chén trà, rèm, futon trống) = **cảnh thở**, không phải cảnh thừa.

---

## 4. CHUYỂN ĐỘNG MÁY (khi cần cú di thật — mặc định showa là §0.5)

Khối chung cho cảnh máy động:
```
The camera is moving for the whole shot and never comes to rest: one single slow continuous move from
first frame to last and nothing else, the move is smooth and mechanical as if the camera were on a dolly,
never handheld and never shaky, never speeding up or slowing down, and the background stays solid and
does not warp or ripple as it passes.
```

| kỹ thuật | token EN | ⚠️ t2v |
|---|---|---|
| **Dolly in** ⭐ | `a slow steady dolly push straight in towards them, the frame growing tighter from first frame to last` | ✅ ổn định nhất |
| Dolly out | `a slow steady dolly pull straight back away from them, more of the room opening up` | ✅ |
| Tracking | `a slow steady lateral track from left to right, a near foreground object sliding through the front of the frame as it passes` | ✅ nếu có vật tiền cảnh |
| Follow | `the camera travels along behind them at their own walking pace, holding the same distance` | ✅ bỏ câu "subject remains in frame" |
| Pan | `a slow horizontal pan, one single continuous move` | ⚠️ lia rồi lia ngược — ghi "one single" |
| Tilt | `a very slow tilt upward, starting on X and ending on Y` | ✅ |
| Pedestal/crane | — | 🔴 không chạy, xem §7.5 |
| Zoom | `the lens zooms in` | 🔴 ra thành dolly |
| Whip pan | — | 🔴 nát, và phạt tệp 45+ |
| Arc | `the camera arcs slowly around them, keeping them in the middle` | ⚠️ bắt buộc "background stays solid" |
| **Xuyên cửa** ⭐ | `the camera travels forward through the doorway, the dark frame of the door passing out of shot on both sides as the bright room opens up ahead` | ⭐ |
| **Creep + vật động** ⭐ | `the camera creeps forward almost imperceptibly while the curtain, the fan and the rising steam carry all the movement in the frame` | ⭐ nước duy nhất cho cảnh thở; đừng `push` (model thêm người) |
| Handheld | — | ⛔ CẤM |

### 4.1 ⭐⭐ LUẬT HAI MỐC — nước máy là ĐƯỜNG ĐI, không phải NHÃN
Tên kỹ thuật trơ ⇒ model chọn cách rẻ nhất: gần như không đi (demo v2: 7/8 clip dưới ngưỡng, 51,6% khung đứng yên). Khai theo thứ tự:
```
Camera move, the only one in this shot: the shot begins <MỐC ĐẦU>, the camera then <ĐƯỜNG ĐI past/through/over …>,
and the shot ends <MỐC KẾT>, <ngoại cảnh: + the fields and the hills sliding steadily past across the frame the whole time>.
```
🔴 Khối này nằm trong **15% đầu prompt** (§7.2).

### 4.2 MÀU PHONG CẢNH phải xin riêng
Cảnh có phong cảnh trong khung → gọi tên màu của nó: `the landscape outside in full saturated colour — vivid green rice fields, dark green wooded hills, a deep blue summer sky with white cloud — bright and clear, never washed out or hazy`. Vẫn giữ `no oversaturated colour` — xin **đậm**, không xin **rực**.

---

## 5. ⭐ QUANG HỌC

| | token EN | mẫu |
|---|---|---|
| **DOF mỏng** ⭐ | `shallow depth of field, the subject sharp and everything behind them melting softly out of focus` | mọi cảnh người |
| **Ba lớp sâu** ⭐ | `one out-of-focus object in the near foreground at the very edge of the frame, so the picture has a near layer, a subject layer and a far layer` | |
| Deep focus | — | ⛔ ngược mẫu |
| **Nguồn sáng một cửa** ⭐ | `one window as the only source of light, falling off softly into the shade of the room` | chuẩn nội thất |
| Nắng gắt | `hard bright summer sunlight casting deep shadows that still hold their detail` | ngoại cảnh |
| Ngược sáng lá | `strong backlight coming through the leaves` | |
| **Hạt phim** | `fine photographic film grain over the whole picture` | mẫu 21–25 |
| **Chống vignette** ⭐ | `evenly exposed right into all four corners with no darkening or shading at the edges` | mẫu viền/tâm 0,88–1,00 |

### 5.1 ⭐⭐ MÀU RỰC PHẢI ĐẾN TỪ **VẬT**, không từ grade
Khung không có vật màu thì "màu đậm" chỉ đậm cái xám. Màu = **một VẬT được gọi tên** ở chỗ mắt đi qua.

| nhóm | vật đúng thời 昭和 |
|---|---|
| văn phòng phẩm | **朱肉** · 赤鉛筆 · bút chì đỏ-xanh · lọ mực xanh · 黄色い下敷き · celluloid 筆箱 · con dấu cán đỏ |
| nhà/bếp | **花柄の魔法瓶** · 花柄の湯呑み · 赤い風呂敷 · rổ nhựa đỏ · hộp cơm nhôm dán hoa · 赤い毛糸 |
| quần áo | cardigan đỏ gạch/xanh cổ vịt · nơ vàng · tạp dề hoa · cà vạt đỏ sẫm · áo trẻ con sọc đỏ-trắng (một điểm, không cả bộ) |
| hoa/cây | cẩm chướng đỏ · 朝顔 tím · cúc vàng · quả hồng trên khay |
| công sở | 赤い座布団 · băng khai trương đỏ-trắng · sổ bìa đỏ · hộp thư đỏ |

Luật: **≥1 và ≤3 vật rực/cảnh** · đặt trên đường đi của máy hoặc cạnh việc nhân vật làm · kèm `with no writing or marking of any kind on it`. ⚖️ Không nới `no oversaturated colour`.

---

## 6. NGỮ PHÁP GHÉP

- **6.1 Một cảnh = một nước máy.** Gate: đếm token nước máy = 1.
- **6.2 ⭐ Cảnh có người là một TRAO ĐỔI** — ≥2 cast được gọi tên + một động tác đi qua giữa họ (đưa–nhận, rót cho, chỉ cùng một trang). ⛔ một người làm việc một mình = cảnh chết.
- **6.3 🔴 POV chỉ khi hướng nhìn quay RA KHỎI thân người cầm máy** (nhìn ra/lên phòng, không đòi bộ phận nào). ⛔ nhìn xuống tay mình làm việc. Kèm:
  `no part of the viewer's own body is ever in the picture, no hands, no arms, no legs, no feet, no lap and no shoulders in the frame, and the viewer is never seen from outside`. Ngoại lệ duy nhất: một bàn tay đưa lên VẪY và người trong khung vẫy đáp lại.
- **6.4 Phối hợp theo đoạn:** mở = toàn cảnh/góc cao + pan nhẹ · đẩy kịch tính = MS→MCU + dolly in chậm · đối thoại = OTS hai chiều, chèn POV khi nhìn vật · ⭐ mỗi 45–50s một cảnh thở + ~2s lặng.
- **6.5 Cắt trên hành động.** Mẫu ~5,0s/cảnh, 13–28 cắt/phút (2 ngưỡng đo, §8).

### 6.6 ⭐⭐ DIỄN XUẤT — tả bằng CƠ THỂ, có ĐỈNH
`laugh` là tên cảm xúc → t2v trả nụ cười đứng yên 8s. Mỗi ACTION có **vòng cung 3 nhịp, đỉnh ở nhịp 2**: trước-đỉnh (giơ tay, hít hơi) → **ĐỈNH** (bung ra bằng cơ thể) → lắng (thở ra, lau mắt). ⛔ Đỉnh ở nhịp 1.

| cảm xúc | ✅ viết |
|---|---|
| cười to | `her eyes narrow first and the corners of them crease, then her head tips back and her shoulders go with it, and it dies down into a long breath while she wipes one eye with a knuckle` |
| bật cười | `she presses her lips together to hold it in, it escapes through her nose anyway, and she looks down at the table to hide it` |
| cười xã giao | `the mouth goes up but the eyes stay level, and it is gone again a moment later` |
| ngạc nhiên | `her eyebrows go up before the rest of her catches on, her hand stops half way, and only then does she turn her head` |
| bẽn lẽn | `he looks at his own hands, rubs one thumb along the other, and glances up only once` |
| do dự | `her hand goes out, stops short of it, comes back to her lap, and goes out again` |
| nén xúc động | `she swallows once, her chin tightens, and she keeps her eyes wide and dry on purpose` |
| hài lòng | `he lets his breath all the way out and his shoulders drop an inch, and he keeps looking at the same spot` |
| gật | `one small nod, then a second one to herself after he has already looked away` |

⭐ Cảnh ≥3 người: **kể riêng từng người một mệnh đề** (một đạp nước, một che mặt, một quay đi, một đứng nhìn).
⭐ Một động tác VẬT LÝ bắt ở đỉnh (vệt nước bay, hơi trà bốc, tay áo lật, giấy lật trang).

### 6.7 ⭐⭐ CHỮ KÝ BIỂU CẢM THEO NHÂN VẬT — chống "cười công nghiệp"
Một kho câu dùng chung ⇒ mọi người cười giống nhau. Biểu cảm là **chữ ký của nhân vật, khai cạnh mô tả khuôn mặt**.

| ai | chữ ký |
|---|---|
| ông già | `his mouth opens wide and the whole face creases with it, the eyes almost shut, the head going back a little, and it comes out loud before he can stop it` |
| bà già | `her eyes go first and crease into two slits, the cheeks pushing up, the mouth barely opening at all, and her head tilts towards whoever she is looking at` |
| bà già đang làm việc | `it happens while her hands are still working and her eyes stay down on what she is holding, never lifting to be seen` |
| phụ nữ trẻ | `she holds it in behind closed lips and it escapes through her nose, one hand going up towards her mouth and stopping half way, and she looks down and to the side` |
| đàn ông đi làm | `only one side of his mouth goes, and he clears his throat over the top of it and looks back down at the page` |
| trẻ con | `the mouth goes wide with no control over it at all and the whole body goes with it, one shoulder up, the feet still moving` |

Luật: ① khai chữ ký trong `C` của `gen_prompts_*.py`; nhân vật không có chữ ký ⇒ không cho biểu cảm mạnh ② 🔴 hai cast cùng khung khác chữ ký ③ biểu cảm ĐI QUA hành động, không giữ pose ④ mỗi chữ ký ≤3 lần/video, hết thì đổi **cường độ**.
```python
sig = {cast: EXPR[cast] for cast in casts_in_shot if cast in EXPR}
assert len(set(sig.values())) == len(sig), "hai nguoi cung mot dieu cuoi trong mot khung"
for s, n in Counter(all_sigs_in_video).items(): assert n <= 3, "chu ky lap qua 3 lan"
```

### 6.8 ⭐⭐ CHỮ KÝ PHẢI XOAY GIỮA CÁC VIDEO
> user: *"Mỗi video có 1 điệu cười khác nhau đi"*

Ba tầng: ① một khung (6.7 mục 2) ② một video (≤3 lần) ③ ⭐ **giữa các video**: mỗi nguyên mẫu có **kho ≥4 biến thể**, mỗi video rút một biến thể chưa dùng, ghi sổ `Projects/youtube-jp-showa/tools/EXPR_REGISTRY.json` (cùng cơ chế `CAST_REGISTRY.json` của mặt). Kho cạn → viết biến thể mới, ⛔ không dùng lại. Đổi cường độ **không** thay được xoay biến thể.

---

## 7. ⛔ BỆNH CỦA t2v

- **7.1 🔴🔴 `35mm` → model vẽ CUỘN PHIM kèm số in ở mép** (8/8 clip, câu cấm ngay đó không cứu). Bỏ số hiệu ống kính/khổ phim; dùng `fine photographic film grain`. Dải phim còn làm sai phép đo viền/tâm.
- **7.2 Khối nước máy sau ACTION thì máy không động** → nằm trong **15% đầu**, cạnh khối cấm.
- **7.3 Ba nước không điều khiển được:** zoom · whip pan · dutch tilt → làm ở hậu kỳ.
- **7.4 Vật mời gọi thắng câu cấm** (nhiệt kế/lịch/thước/biểu đồ có trục ⇒ điền số) — `ai-video-regen.md` §3.
- **7.5 ⭐⭐ t2v làm được trục TRƯỚC–SAU (dolly: +9…+103% / −18…−39%) và NGANG (track 22–257px), KHÔNG làm được trục ĐỨNG** (PEDESTAL/CRANE/sink down = scale 0,995–1,009, 3/3). Cần hạ máy → **`DOLLY IN, forward and dropping as it goes`** (omiai 0,995 → 1,368). Câu tự mâu thuẫn hướng (`travel backward in` từ vườn vào nhà) cũng không chạy → `DOLLY IN, from the garden into the house`.

---

## 8. GATE NGHIỆM THU

**Trước khi bơm prompt:**
```python
pos = p.find("NO letters"); assert pos*100//len(p) <= 15          # guard trong 15% đầu
assert sum(1 for v in MOVES.values() if v[:34] in p) == 1          # đúng 1 nước máy
for bad in ("respectful distance","holds one position","slight vignette","deep focus so both",
            "35mm","16mm","hands only","feet only","the subject remains in frame"):
    assert bad not in p, bad
assert (("no hands, no arms" in p) == is_pov)                       # khối POV chỉ ở cảnh POV
assert n_cast_in_action >= 2 or is_breath_shot                      # §6.2
```

**Trên clip đã gen (chỉ 2 chỉ số hợp lệ ở mức một clip):**
- **% khung đứng yên** (MAD tiny32 <2,0) **≤10%** (mẫu 3,0–3,8%).
- **MAD blur TRONG shot** — ngưỡng cho clip không cắt đo bằng cách bỏ frame cắt (mẫu 8,25–9,30). ⚠️ Với khuôn §0.5 thì theo gate `check_realism.py`, không theo ngưỡng này.
- 🔴 So cùng đơn vị: MAD cả video cộng cả cú cắt cảnh; clip là một shot không cắt.
- ⛔ `viền/tâm` và `G` là thống kê cả bài — đo sau khi ghép, không đo clip lẻ.
- ⚠️ Nhịp cắt báo 2 ngưỡng (dissolve không tạo đỉnh đơn); `ffmpeg scdet` vô dụng ở footage động.

### 8.2 ⭐⭐ GATE MÁY QUAY
```bash
python Projects/_media_library/check_cammove.py <clip.mp4 | thư mục>
```
NHẬN khi **|scale−1| ≥ 5%** (dolly) **HOẶC** **dịch ≥ 8px** (track). `check_motion` không thay được: MAD không phân biệt máy-di với người-cử-động (lô demo: 7 clip đều MAD 7,2–15 mà 3 clip máy không tiến/lùi). Lô cuối sau khi bỏ trục dọc: **SẠCH 8/8**.
⚠️ `ECC không hội tụ` thường là cú di QUÁ LỚN → tool thang xuống độ phân giải thấp, vẫn không được thì trả "KHÔNG ĐO ĐƯỢC — soi MẮT", không chấm rớt. Bắt buộc `MOTION_AFFINE` (Euclidean không có scale).

---

## 9. PHẠM VI

| kênh | áp |
|---|---|
| **showa** | 🔴 **§0.5 đè §4/§8.1** từ 2026-09-22; §1–3, §5, §6 là xương |
| **nenkin** | 🟡 §1–§5 tham khảo; ⛔ **§4 và §6.5 KHÔNG áp** — `audience-45plus.md` §2.0-quater bắt MAD ≤5,0 · giữ hình ≥3,0s |

🛑 Phanh: 3 video showa chạy rule này mà AVD tụt dưới lô 13–16 → trả khuôn cũ, ghi `08_ANALYTICS_LOG.md`.

## 10. LIÊN QUAN
- Bằng chứng gốc: `Projects/youtube-jp-showa/CHANNEL_BENCHMARK_showa-no-kioku_2026-09-21.md`
- Vòng gen lại: `ai-video-regen.md` · prompt nghe vị trí + ✦: `media-library.md` §2.10 · nhịp 45+: `audience-45plus.md` §2
