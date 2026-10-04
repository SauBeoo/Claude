# Khán giả 45+ — luật đóng gói & dựng (RULE TOÀN HỆ THỐNG)

> **Nguồn sự thật DUY NHẤT** về làm nội dung cho tệp 45+. Phạm vi hiện tại: **nenkin** (年金と老後のお金研究室) · **showa** (昭和くらし図鑑).
> Chốt 2026-07-30 (user cấp 5 quy tắc: thumbnail · nhịp dựng · phụ đề · độ dài · giọng). Tối ưu lại 2026-09-24 (bỏ phần của các kênh đã ngừng).
> Rule này lo **LÀM CHO ĐÚNG TUỔI**. Cấu trúc/retention xem skill `script-*`; chất người xem `humanize-script-voice.md`; từ ngữ an toàn ad xem `youtube-compliance.md`.

## 0. NGUYÊN TẮC GỐC

**Đúng chủ đề nhưng làm theo kiểu dành cho tuổi 20–30 thì nhóm 45+ vẫn thoát ngay.** Đây là tầng **THI HÀNH** (đóng gói + dựng), không phải tầng chọn đề tài. Năm mục dưới là **gate đo được**, không phải gợi ý.

⚠️ Rule này KHÔNG đè lên nguyên nhân đã đo của việc không lên view (retention 60–75 giây đầu, nguồn traffic). Làm đúng 5 mục mà cold open vẫn vào bài muộn thì vẫn không có view.

---

## 1. THUMBNAIL — chữ 4–6 ký tự CỰC TO + 1 khuôn mặt biểu cảm rõ

**Gate đo được (thiếu 1 = làm lại):**
1. **Dòng chính ≤6 ký tự** (full-width).
2. **Dòng chính cao ≥1/3 chiều cao khung** — ⚠️ gate đang tranh chấp, xem §6.10.
3. **Tổng số dòng chữ ≤3.**
4. **≥1 khuôn mặt** biểu cảm đọc được ở 168px (ngạc nhiên · lo · vỡ lẽ). Mặt bình thản không tính. *(nenkin được miễn — §1.2)*
5. **Gate 168px:** mở `*_preview168.png`, đọc được dòng chính + biểu cảm → mới giao.
6. **Nền sáng, chủ thể tương phản cao.** Không moody/tối.
7. 🔴 **CHỮ PHẢI TẢI CHỦ ĐỀ — che ảnh đi vẫn biết video nói về gì** (user chốt 2026-08-09). Bộ chữ trả lời đủ 3 câu: **① VỀ CÁI GÌ** (phải là keyword đo được cao nhất ở `youtube-upload-seo.md` §0.5) · **② CHUYỆN GÌ XẢY RA** (hậu quả/con số, thường là hero) · **③ PHẢI LÀM GÌ / mốc thời gian**.
   - Ca gốc nenkin 09: bộ chữ đầu `簡易書留が届きます` / `45日以内` / `何もしないと` — không biết video về gì, và `簡易書留` đo **0 điểm** trong khi `公金受取口座` = **100**. Sửa → `8月から 公金受取口座に` / `45日で同意` / `断るなら返送`.
   - ⚠️ **Đo keyword xong thì áp cho CẢ title LẪN thumbnail** — lỗi này từng tái phạm ở thumbnail sau khi đã sửa ở title.
   - Tự kiểm 30 giây: che ảnh, chỉ đọc chữ; từ ở banner/hero phải nằm trong **top 2** rổ đo Trends.

⚖️ Mặt = **người stock ẩn danh** hoặc **nhân vật AI hư cấu**; **CẤM** mặt người thật cụ thể (`youtube-compliance.md` §2).

### 1.1 Khuôn kênh
| Kênh | Khuôn | Xử lý |
|---|---|---|
| **nenkin** | khuôn TELOP (chốt 2026-08-06) + khuôn A-45 (`03_THUMBNAIL_TITLE_FORMULA.md` §6, tool `tools/make_thumb_45.py`) | ngoại lệ §1.2 |
| **showa** | K-COLLAGE (`youtube-jp-showa/03_THUMBNAIL_FORMULA.md`) | áp full §1 |

### 1.2 🟡 NGOẠI LỆ nenkin — chip 対象 + dải đỏ, MIỄN gate 4 (user chốt 2026-08-09)
Bằng chứng: `お金の保健室` 25 ngày → 331K view, **0 khuôn mặt trên 25/25 thumbnail** (`youtube-jp-nenkin/CHANNEL_BENCHMARK_okane-hokenshitsu_2026-08-08.md` §2.3).
- **Thêm:** chip 対象 góc trên (`65歳以上のご家族へ` / `50代・60代へ`) · **dải ĐỎ đáy = dòng 3 có nhiệm vụ riêng** (gỡ lo hoặc dấn thêm), không phải trang trí.
- **Miễn:** gate 4. Gate 1·2·3·5·6·7 giữ nguyên.
- **Phép thử:** sau 5 video đọc CTR trong Studio; thấp hơn 4 thumbnail cũ → trả về gate 4, ghi `08_ANALYTICS_LOG.md`. Impressions ~0 thì phép thử vô hiệu.

---

## 2. NHỊP DỰNG — chậm hơn 20–30% so với nội dung tuổi 20–30

**Gate đo được:**
1. **≤6 lần đổi hình/phút** (`số entry ÷ số phút`). *(showa: dải riêng §2.0-ter)*
2. **Không entry nào <6 giây.**
3. **Transition mềm:** `dissolve`, `transition_dur ≥0.4s`. Cấm cut nhanh liên tiếp >3 lần.
4. **SFX ≤1 chùm/5 phút**, chỉ ở mốc kịch tính thật (bộ CTA overlay được miễn).
   🟡 **Ngoại lệ nenkin — lớp ASMR "bàn làm việc"** (user chốt 2026-09-27: *"thêm các tiếng asmr vào cho nó thỏa mãn người nghe"* → duyệt demo *"cũng oke đó"*): tiếng giấy/bút/thẻ **neo đúng mốc chữ vào** (`build28.sync_times`), ~27/phút, thấp hơn giọng 12–17 dB. Tool `youtube-jp-nenkin/tools/asmr31.py` (効果音ラボ, không cần credit). Gate 4 giữ nguyên cho SFX **kịch tính** (whoosh/boom/sting). 🛑 Phanh: 3 video có lớp này mà AVD tụt so với lô trước → bỏ lớp, ghi `08_ANALYTICS_LOG.md`.
5. **BGM −40 dB.**
6. **Pan chậm + ease** (`motion_ease: True`), cấm Ken Burns giật.

⚠️ **Bẫy đo nhịp cắt (đã dính nhiều lần):** `ffmpeg scdet` đếm **phụ đề đổi** thành cắt cảnh (lệch tới 4×, có plateau giả trông rất tin được) và bỏ sót **dissolve dài** (ra 0,13 cắt/phút cho 46 cảnh khác nhau). ⇒ **Bỏ dải phụ đề rồi đo MAD, hiệu chuẩn ngưỡng ở nhiều mức, đối chiếu bằng sheet frame.** Phân loại tĩnh/động bằng `findTransformECC` phải dùng **`MOTION_AFFINE`** (Euclidean không có scale, chấm mọi cú zoom thành chuyển động).

### 2.0-ter 🔴🔴 NGOẠI LỆ showa: bản thắng giữ MỘT ẢNH 16–18 GIÂY (2026-09-08)
Mổ 3 video 191K–232K của ngách (`youtube-jp-showa/CHANNEL_BENCHMARK_stills_2026-09-08.md`):

| | `あの頃の昭和` 232K | `あの頃の昭和` 191K | `昭和の音がする` 219K |
|---|---|---|---|
| số ảnh / thời lượng | **65 / 20′37** | **62 / 18′54** | 161 / 18′04 |
| ảnh/phút | **3,2** | **3,3** | 8,9 |
| giữ mỗi ảnh (trung vị) | **18,0s** | **15,8s** | 5,0s |
| giữ dài nhất | **47,0s** | **49,0s** | 26,5s |
| ảnh giữ >10s | **68%** | **55%** | 20% |
| chuyển động TRONG ảnh | **0** (MAD 2,0) | **0** (MAD 1,2) | **0** (MAD 2,8) |

⇒ Cả trần ≤6/phút lẫn sàn "ảnh đổi ≤9s" (§2.0b) đều bị bản thắng vi phạm theo hai chiều. **Vì sao sàn 9s sai ở đây:** nó đo *"ảnh có đổi không"* thay cho *"khung có chết không"* — hai thứ chỉ trùng khi ảnh tĩnh trơ. Ảnh tĩnh **có hoá động cục bộ** thì khung không chết dù ảnh giữ 18s.

**Thi hành CHỈ showa** (`youtube-jp-showa/CLAUDE.md` §Visual+audio): dải **3,2–8,9 ảnh/phút**; mỗi ô hình qua gate `Projects/_media_library/animate_still.py` — **MAD frame-to-frame >3** và **dịch khung max <1,0px** (không Ken Burns).
⚠️ Chữ ký sản xuất, không phải retention. 🛑 Phanh: 3 video showa AVD tụt dưới lô trước → trả nhịp cũ, ghi `youtube-jp-showa/08_ANALYTICS_LOG.md`.

### 2.0-quater ⭐⭐ TRẦN ĐỘNG MAD + NỀN MỘT TÔNG — đo 3 kênh 年金 đang thắng (2026-09-17)
Bằng chứng: `youtube-jp-nenkin/CHANNEL_BENCHMARK_3video_2026-09-17.md`.

| | view/video | cắt/phút (bỏ dải sub) | giữ mỗi hình | **MAD TB** | sáng nền TB | **độ lệch nền** |
|---|---|---|---|---|---|---|
| なぎさのお金案内所 | 64.750 | 4,0 | **16,5s** | **1,06** | 214 | 33,3 |
| **年金・給付金完全攻略** | **445.618** | 5,8 | **9,0s** | **1,94** | 202 | **7,6** |
| ひろと【退職とお金】 | 62.055 | 14,4 | 4,0s | 4,28 | 220 | 22,5 |
| 🔴 nenkin v26 | ~600 | **50,7** | **0,5s** | **9,97** | **180** | **41,1** |

**Phạm vi:** ✅ **nenkin ÁP** · ⛔ **showa KHÔNG áp** (§2.0-ter đòi MAD >3 mỗi ô — ngược chiều). Bằng chứng chỉ từ ngách 年金 — không suy rộng.

**Thi hành (nenkin):**
1. **MAD bản render ≤5,0** — chỉ TRẦN.
2. **Giữ mỗi hình (trung vị) ≥3,0s** — chỉ SÀN. *(Ba kênh thắng trải MAD 1,06–4,28, giữ 4,0–16,5s ⇒ không có tín hiệu hai đầu; đặt khoảng là bịa mốc.)*
3. **Nền một tông sáng: sáng TB ≥195 · độ lệch giữa cảnh ≤36.** Cấm nhảy nền tối ↔ sáng.
4. 👁 **Vật cố định ≤1** (watermark / mascot / cast 2 mép — chọn ĐÚNG MỘT) — **duyệt MẮT**. Phép đo máy cho mục này đã viết rồi xoá vì cho kết quả ngược mắt; gate sai dụ đi sửa nội dung cho lỗi của công cụ.
5. **True peak ≤ −3 dBTP.**

🔧 **GATE MÁY (hậu render, bắt buộc):** `python Projects/_media_library/check_motion.py <video.mp4>` → `SACH 5/5`. Đọc mp4 đã render, khác `check_frame_pace.py` (đọc project.json trước render) — chạy cả hai.
✅ Nghiệm thu ngược: 3 kênh thắng **5/5**, v26 **0/5**. ⭐ **v27 (16:21): SACH 5/5** — MAD 9,97→1,12 · giữ 0,5→11,0s · nền 175/43,4→221/3,3 · peak −1,2→−3,6. Khuôn: `youtube-jp-nenkin/CLAUDE.md` §②.
🔴 **Luật ngưỡng:** bản ngưỡng đầu (MAD 2–4, giữ 6–9s, "lấy khoảng giữa") đánh trượt cả 3 kênh thắng. **Gate đánh trượt chính mẫu nó học từ là gate sai** — chỉ chốt ngưỡng sau khi chạy ngược trên toàn bộ mẫu.
🔴 **Bài học cơ chế:** sàn §2.0/§2.0b được thi hành triệt để còn trần không tồn tại ⇒ lớp sticker/punch lấp sàn đẩy MAD lên 9,97. **Tối ưu một chỉ số thì hỏi ngay biến ĐÁNH ĐỔI của nó** — ở đây là sự tĩnh để người 70 tuổi đọc kịp.
⚠️ n=3, không có Analytics của họ; biến trội đã đo của kênh mình vẫn là **nguồn traffic**. 🛑 Phanh: 3 video khuôn mới AVD tụt → trả mốc cũ, ghi `08_ANALYTICS_LOG.md`.
📌 Nên làm cùng lượt: **chip chương đánh số góc trên-trái MỌI khung** + màn 「本日の流れ」 nhắc 2–3 lần giữa bài (mục xong ✅, mục đang làm tô đỏ).

### 2.0-quater-b 🎬 ẢNH TĨNH hay CLIP AI? — ngách 年金 trả lời: ẢNH
| | MAD p50 | % khung đứng yên (MAD<0,5) | % khung động mạnh (>8) |
|---|---|---|---|
| 完全攻略 | 0,00 | **92%** | 3% |
| なぎさ | 0,04 | **91%** | 2% |
| ひろと | 0,00 | **89%** | 7% |
| 🔴 nenkin v26 | **3,47** | **29%** | **18%** |

**Chốt cho nenkin:** ① ⛔ **BỎ clip AI t2v/i2v** (`kind:"video"`) — việc CHÍNH: v26 có 61 clip × 8s = **62% thời lượng**, MAD từng clip 3,83–8,35; bỏ từ **v27**. ② ✅ Giữ ảnh AI tĩnh + thẻ chữ/sơ đồ vẽ bằng font (disclosure không phải lý do chọn — cả hai đều phải tick). ③ Bỏ clip trước, đo lại `check_motion.py`, còn dư thì cắt animation Remotion.
🔴 **Bài học đo:** đếm ra **0** ở chỗ lẽ ra phải có thứ gì = nghi phép ĐẾM trước (`find | grep -vc` trả 0 trong khi `clips/` có 61 file). Kiểm 5 giây: `ls` thẳng vào thư mục con.

### 2.0 SÀN SỰ KIỆN HÌNH + phân biệt 4 đại lượng (user chốt 2026-08-30)
> user: *"tầm 7s phải chuyển frame ảnh 1 lần… đang thấy nhiều cái nói với nền trống và frame đứng yên lâu quá."*

| | đại lượng | chống | ngưỡng |
|---|---|---|---|
| ① TRẦN | đổi **ẢNH CHÍNH** (cắt cứng) | MỆT | **≤6/phút** |
| ② SÀN | **SỰ KIỆN HÌNH** (sticker vào/ra · punch · bảng · pop) | CHÁN | **≤7s phải có 1** |
| ③ | scene **không có gì ở vùng giữa** | nền trống | **0 scene** |
| ④ TRẦN ĐỘNG | **MAD** bản render (kể cả animation trong cảnh) | MỆT dạng không thấy | **MAD ≤5,0 · giữ ≥3,0s** (§2.0-quater) |

🔴 Sticker không làm tăng số lần đổi ảnh chính nên không phá **phép đếm** của ①, nhưng phá **thứ ① bảo vệ** (chống mệt) — đó là lý do phải có ④. ② không đụng "entry ≥6s": ② nói khoảng cách sự kiện bên TRONG entry.

### 2.0b SÀN ĐO BẰNG **ẢNH CHÍNH** 8–9s (user chốt 2026-08-31)
> user: *"7s đổi ảnh 1 lần đó nhé nếu nó không phải là số liệu, còn sticker tao không muốn… lặp lại quá nhiều lần"* → *"ừa thế 8-9s đi"*.

| | ngưỡng |
|---|---|
| Ảnh chính (hero) | đổi mỗi **≤9,0s** ở scene ẢNH; **scene SỐ LIỆU (bảng/công thức) MIỄN** |
| Trần đổi ảnh/phút | **6,0** giữ nguyên |
| Sticker | **1 cái/scene**, **≤3 lần/video** mỗi file |

- 8–9s là khoảng **duy nhất** vừa sàn vừa trần (7,0s ⇒ 7,1 đổi/phút, vượt trần).
- **Báo giá số ảnh = `Σ ceil(giây_scene_ảnh ÷ 9)`**, đừng chia tổng (ceil từng scene làm dôi ra).
- Gate ② miễn scene số liệu theo **ranh giới SCENE**, không theo khoảng clip bảng.
- ⚠️ *(Với nenkin từ v27, §2.0-quater đè lên: giữ hình trung vị ≥3,0s, MAD ≤5,0 — sàn 9s vẫn là trần độ dài một ảnh chính.)*

### 2.0c 🔴 Bảng số ít dòng = "nền trống" gate không thấy
- Bảng phải **≥3 DÒNG** (thêm dòng chốt chở nghĩa thật) — ⛔ đừng phóng cỡ chữ (nhãn dài tràn 2 hàng).
- **Căn giữa dọc theo số dòng:** `y = (150+900)/2 − rows×size×1,55/2`, kẹp 200–300. Cỡ theo số dòng: 3→56 · 4→50 · 5→48.
- ⚖️ Dòng chốt = **số học từ chính 2 số trên thẻ** hoặc mặt còn lại của điều vừa nói; **cấm bịa số** (YMYL thắng bố cục).
- ⛔ Đừng chẻ bảng dài thành 2 bảng ngắn — scene số liệu được miễn luật 9s, build-on chính là chuyển động.
- ⏳ Chưa có gate đo "bảng lấp bao nhiêu khung" ⇒ **soi still 1:1 mọi scene có `stat`/`formula` là bắt buộc**.

### 2.0d 🔴 Khung trống ở ĐẦU SCENE — gate đếm khe không thấy
`check_frame_pace` đo khe giữa sự kiện; đầu scene luôn có cụm sự kiện nên sạch, nhưng **vùng giữa khung** vẫn trống tới khi bảng/ảnh vào. **Có sự kiện ≠ có nội dung ở giữa khung.**
- Độ trễ bảng + công thức: `f + min(60, max(20, 0.10×d))` — **trần tuyệt đối 2s**, không theo tỉ lệ.
- Quét bổ sung: mỗi scene, từ đầu scene tới hero/peak/stat/formula đầu tiên **≤2,5s**. ⏳ chưa gộp thành gate ⑤.

### 2.0e–f THẺ CHỮ PHẢI TỰ CO CỠ THEO BỀ RỘNG
- **Thẻ PIL:** vòng co cỡ tới khi dòng dài nhất lọt `W − lề trái − lề phải` (lề phải cộng chỗ vòng khoanh đỏ +26px). Kiểm máy: % pixel mực trong dải 12px sát mép phải >0,5% = tràn.
- **Preset Remotion** (`papercut-stat`, `papercut-formula`) là flex nowrap: vượt `maxWidth` thì ô **bị NÉN, chữ gãy dòng TRONG ô** (「28万」/「円」) — không tràn, không lỗi, chỉ mắt thấy. ⇒ **Builder tự co cỡ trước khi dựng.** Ước: full-width ≈1,0em · ASCII ≈0,55em · +letterSpacing 0,02em + padding; biên an toàn **1,06**.
- ⭐ **Làn sticker co theo MỰC THẬT** của bảng/công thức; khe <200px thì **bỏ sticker** scene đó. Sticker nghiêng 7° nở cả hai bên ⇒ **trừ HAI LẦN** phần nở.
- 🔴 Placement và gate phải **đọc CÙNG một hàm đo mực**; đừng dùng hằng số phỏng đoán (`TBL_INK_X1 = 1140` từng cho qua ca mực tới 1333).

### 2.0f-bis 🔴🔴 Đổi đơn vị hình (SCENE → ĐOẠN ẢNH) ⇒ rà mọi lớp neo vào đơn vị cũ
Khi hero là một DÃY ảnh trong scene, mọi lớp còn neo "hết scene" sẽ hỏng: peak footage **che ảnh mới**, sticker **lạc sang ảnh nó không nói về** (nenkin 19: 41 chỗ). Gate "vượt scene" / "chồng track" đều báo 0 vì **sai ĐƠN VỊ, không sai SỐ**.
- Dựng `segs` **một lần**, hero · peak · sticker **cùng đọc nó**. Peak kết ở cuối đoạn; sticker vào sau ảnh ~2s, chết trước khi ảnh đổi; không đủ **30 frame** thì bỏ.
- Gate: clip nào có `seg_index(from) != seg_index(to-1)` trên trk-peak/sup ⇒ 🔴.
- Nghe user chỉ **một** chỗ thì **đi đếm cả lô**.

### 2.0g 🔬 Đo pixel: kết quả CHẠM MÉP cửa sổ quét = đo lại
Cửa sổ hẹp hơn vật thì số đo là mép cửa sổ (suýt cài hệ số 0,80 thay vì thật 0,948). Số sai kiểu này trông hoàn toàn hợp lý.

### 2.0h–i 🔴 Gate báo đỏ giả
- Mọi tool gate mở đầu bằng `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` (và `stderr`) — crash cp1252 làm builder báo "GATE ĐỎ" trên project sạch.
- `check_frame_pace` trên project có footage động: ② miễn khe nằm trọn trong clip có **đuôi file video** (không miễn cả track); ③ scene có nội dung nếu có clip bắt đầu trong nó **HOẶC** clip chạy qua **điểm giữa** scene. `trk-genten` (ảnh 原典 tĩnh) vẫn bị tính.
- **Định viết "gate này báo đỏ nhưng bỏ qua được" = lúc sửa GATE, không phải ghi chú.**

**🔧 GATE MÁY trước mọi lượt render Remotion:** `python Projects/_media_library/check_frame_pace.py <project.json>` → `GATE NHIP HINH: SACH 3/3`.

### 2.0-sticker Chữa sàn đúng cách (rẻ → đắt)
1. Thêm sticker vào scene trống **bằng FILE MỚI**. 2. Bật `exit` (rút đi cũng là sự kiện). 3. Punch/pop giữa scene dài. 4. Chẻ scene >30s với hero **KHÁC**.
⛔ Không chữa bằng tăng đổi HERO (đâm trần ①). ⛔ Không **xoay vòng cùng một file sticker** qua các vị trí (user kết án: *"rất nhàm, không có tính sáng tạo"*).
⭐ **Nhịp sticker:** 1 sticker **đúng 1 lần/scene**, sticker đầu vào **sau hero ~2s**, các cái sau giãn ~5–6s.
🔴 **Giảm LẶP ≠ giảm SỐ LƯỢNG:** tăng số FILE, giữ số lượt.
📐 Video N giây cần **≥ N/7 sự kiện hình** (15′ ⇒ ≥132).

### 2.1 🔴 Chữ tràn khung `make_stage` — gate là CON SỐ
`fit()`/`fit_ml()` có sàn font; quá sàn thì **tràn, không co**, không báo lỗi. Trần ký tự:

| layout | bề rộng | sàn | trần/dòng | ghi chú |
|---|---|---|---|---|
| `check` | 732px | 30 | **24 ký** | |
| `compare` | 770px | 24 | **32 ký** | **tối đa 3 HÀNG** |
| `steps` | 662px | 30 | **22 ký** | một dòng — **cấm xuống dòng** |
| `source` | 690px | 30 | **23 ký** | |
| `timeline` hộp | `880/n − 52` | 26 | n=3→9 · n=5→4 ký | |
| `timeline` label | `880 × prog` | **40 cố định** | `len × 40 ≤ 880 × prog` | |

Tool sinh SLIDES tự chặn 6 mục trên (mẫu `youtube-jp-nenkin/tools/build_slides_11.py`) + `match` khớp đúng 1 dòng · index tăng · khoảng cách ≥2 dòng · ≤6 đổi hình/phút. Kèm quét dải 30px sát đáy card.
🔴 Khoá `fill` (1010–1400 × 536–852) **đè vùng chữ** của `check`/`steps` → dùng `bgimg`. Thẻ toàn dòng `no` = chữ xám nhạt → dòng trung tính để `ok`.

---

## 3. PHỤ ĐỀ — cháy sẵn, KHÔNG auto-caption

- Burn phụ đề theo câu, **≤2 dòng/khối** (`SUB_MAXLEN=42`). `subs.srt` **upload tay**, cấm auto-caption. ⛔ Cấm upload `subs_styled.srt`.
- **Cỡ ≥22** (`sub_size`).
- ⭐⭐ **`sub_style: "outline"` — chữ trần có viền, KHÔNG nền** (user chốt 2026-08-10: *"Bỏ cái background trắng đi"*). Nguồn: `Projects/youtube-jp-health/tools/channels.py`.
  - ⚖️ Nhận lại rủi ro mất chữ trên nền sáng. Bù bằng: giữ `sub_size ≥22`, viền đủ dày, **duyệt mắt frame nền SÁNG NHẤT**. Mất chữ thật thì dày viền / tăng cỡ / thêm bóng — **đừng quay lại pill**.
  - 🔴 **nenkin:** đổi `bar` → `outline` làm `safe_bottom` **SIẾT 788 → 714** ⇒ chữ thẻ trong dải y 714–788 bị phụ đề đè. Dựng lại clip sân khấu và duyệt 1 frame có phụ đề trước render.

---

## 4. ĐỘ DÀI

| Kênh | Loại | Chuẩn |
|---|---|---|
| **nenkin** | thông tin | **13–17′** (user chốt 2026-08-10) |
| **showa** | thông tin/ký ức | **13–18′** |

**nenkin — bằng chứng:** 14 hit ≥100K của `フクロウの年金・給付金解説室` median **15′00**; kênh clone `タヌキ` rút 18–32′ → 9–12′ và bản ngắn đang thắng (`youtube-jp-nenkin/CHANNEL_BENCHMARK_fukurou-tanuki_2026-08-10.md` §2.1). ⚖️ Chở được ít 制度 hơn — một cú lật mỗi bài. Xét lại sau 5 video nếu AVD tụt.

---

## 5. GIỌNG — người thật > TTS

### 5.1 Giọng người thật KHÔNG thi hành được (không có người đọc JP bản xứ)
→ **Mặc định: giữ TTS + đẩy tối đa chất người** (`humanize-script-voice.md`). Voice-clone chỉ với giọng **có quyền dùng**; muốn thử thì dựng demo 1 đoạn so VOICEVOX.

### 5.2 Gate cứng
1. **`speed ≤ 0,90`** (nenkin 0,90). ⚠️ KHÔNG hạ thêm — "chậm hơn 20–30%" nói về **nhịp dựng**, không phải giọng.
2. **外来語:** ⛔ cấm trong **60 giây đầu, title, thumbnail** · thuật ngữ không phổ thông ở thân bài → thay từ Nhật hoặc kèm cụm giải thích ngay sau · từ đã ngấm đời sống (ビタミン・エアコン・スマホ) giữ.
3. **Từ mới / tiếng trẻ / viết tắt:** cấm (バズる・エビデンス・コスパ・タイパ・サブスク).
4. Giữ ngưỡng **≥4/6 mũi tiêm + 15–25 tag** (`humanize-script-voice.md`).

---

## 6. VIỆC CÒN MỞ

| # | Việc | Trạng thái |
|---|---|---|
| 6.9 | Gate máy `check_45plus.py` (ký tự dòng chính thumbnail · slide/phút · 外来語 60s đầu · speed) | ⏳ — luật kiểm bằng mắt thì sẽ trôi |
| 6.10 | Gate 2 thumbnail "dòng chính ≥1/3 khung" — chọn ⓐ hay ⓑ | 🟡 **chờ user** |

### 6.10 Kết luận đo (≈20 ca, 2026-08-05 → 09-07)
- **Dải tự nhiên theo layout:** "hero + 1–2 dòng phụ/cast kẹp dọc" = **20–31%** · text-wall ≥3–4 dòng = **13–18%** (trần hình học ~20%) · TELOP nenkin (banner ~1/5 + ruy-băng) = **20–22%**. Mọi ca rớt đều **đọc rõ ở 168px VÀ 120px**.
- ⭐ **nenkin 21 (khuôn カメ先生, 0 người):** hero **38,7%** (T2) / **39,8%** (T3), rộng 92,7% → **ĐẠT** lần đầu. ⇒ Gate 2 **không sai về vật lý**, nó chỉ không tương thích khuôn có cast/dòng phụ kẹp dọc. Chưa biết khuôn này có thắng CTR — đọc Test & compare, ghi `youtube-jp-nenkin/08_ANALYTICS_LOG.md` (`CHANNEL_BENCHMARK_takaichi-face_2026-09-07.md`).
- **Thứ mua legibility là BỀ NGANG hero** (ca 20% cao mà rộng ~55–70% vẫn đọc ở 120px), và "dòng nào là chính" còn do **màu + tương phản**, không chỉ chiều cao.
- ⚠️ Giới hạn phép đo: hero trắng trên nền sáng không tách được bằng mask ngưỡng sáng → đo mask viền đen (pixel <70). Mask màu phải giới hạn vùng (badge cùng màu làm số rác). Ô timestamp YouTube chỉ ~4,0%×3,2% khung — đo bằng ô đúng cỡ.
- **Hai đường sửa, chưa chọn:** ⓐ hạ trần khi có dòng phụ (muốn phủ hết ca thì phải ~20% ⇒ gần như không chặn gì) · ⓑ đổi sang **"đọc được dòng chính ở 168px"** (duyệt mắt `*_prev168.png`). ⓑ là đường duy nhất áp được mọi layout. ⛔ Đừng âm thầm bỏ qua gate.
- Model gen **nghe VỊ TRÍ, không nghe TỈ LỆ** — muốn ép cỡ thì tả bằng quan hệ với MÉP KHUNG (`media-library.md` §2.10 ⑥).

## 7. LIÊN QUAN
- Chất người: `humanize-script-voice.md`
- Bản sắc render (giọng/phụ đề/màu): `Projects/youtube-jp-health/tools/channels.py`
- Khuôn thi hành nenkin: `youtube-jp-nenkin/CLAUDE.md` §② · showa: `youtube-jp-showa/CLAUDE.md` §Visual+audio
- Compliance mặt người / video trùng lặp: `youtube-compliance.md` §1, §2
